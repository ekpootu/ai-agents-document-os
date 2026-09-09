#!/usr/bin/env python3
"""
ocr_doc.py - Deterministic OCR CLI
Runs Tesseract OCR on images and scanned PDFs with automatic image preprocessing.
"""
import os
import sys
import shutil
import argparse
from pathlib import Path

def find_tesseract():
    cmd = shutil.which("tesseract")
    if cmd:
        return cmd
    if sys.platform == "win32":
        standard_paths = [
            Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
            Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
            Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Tesseract-OCR" / "tesseract.exe"
        ]
        for p in standard_paths:
            if p.exists():
                return str(p)
    return None

def preprocess_image(img_path: Path):
    from PIL import Image, ImageEnhance, ImageFilter
    with Image.open(img_path) as img:
        # Convert to grayscale
        gray = img.convert("L")
        # Increase contrast
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(2.0)
        # Sharpen
        sharpened = enhanced.filter(ImageFilter.SHARPEN)
        return sharpened

def ocr_image(img_path: Path, lang: str = "eng", psm: int = 3):
    import pytesseract
    tess_path = find_tesseract()
    if tess_path:
        pytesseract.pytesseract.tesseract_cmd = tess_path
    
    proc_img = preprocess_image(img_path)
    config = f"--psm {psm}"
    text = pytesseract.image_to_string(proc_img, lang=lang, config=config)
    return text

def ocr_pdf(pdf_path: Path, lang: str = "eng", psm: int = 3):
    from pdf2image import convert_from_path
    from render_doc import find_poppler_path
    
    poppler_dir = find_poppler_path()
    images = convert_from_path(str(pdf_path), poppler_path=poppler_dir)
    full_text = []
    for idx, img in enumerate(images, start=1):
        temp_img_path = pdf_path.parent / f"_temp_ocr_{idx}.png"
        img.save(str(temp_img_path), "PNG")
        try:
            page_text = ocr_image(temp_img_path, lang=lang, psm=psm)
            full_text.append(f"--- Page {idx} OCR ---")
            full_text.append(page_text.strip())
        finally:
            if temp_img_path.exists():
                temp_img_path.unlink()
    return "\n\n".join(full_text)

def main():
    parser = argparse.ArgumentParser(description="Antigravity Document OCR CLI")
    parser.add_argument("file", help="Path to image or scanned PDF")
    parser.add_argument("--lang", default="eng", help="OCR language (default: eng)")
    parser.add_argument("--psm", type=int, default=3, help="Page segmentation mode (default: 3)")
    parser.add_argument("--output", help="Save extracted text to file")
    args = parser.parse_args()

    input_path = Path(args.file).resolve()
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    tess = find_tesseract()
    if not tess:
        print("Error: Tesseract OCR executable not found. Ensure Tesseract is installed.", file=sys.stderr)
        sys.exit(1)

    ext = input_path.suffix.lower()
    if ext == ".pdf":
        result = ocr_pdf(input_path, lang=args.lang, psm=args.psm)
    else:
        result = ocr_image(input_path, lang=args.lang, psm=args.psm)

    if args.output:
        out_path = Path(args.output).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"OCR text saved to: {out_path}")
    else:
        print(result)

if __name__ == "__main__":
    main()
