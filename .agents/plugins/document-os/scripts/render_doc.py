#!/usr/bin/env python3
"""
render_doc.py - Visual Page/Slide Renderer CLI
Renders PDF pages and Office slides (via conversion) to PNG images for visual QA and multi-modal review.
"""
import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path

def find_poppler_path():
    # Check PATH first
    if shutil.which("pdftoppm"):
        return None
    if sys.platform == "win32":
        standard_paths = [
            Path(r"C:\Program Files\poppler\Library\bin"),
            Path(r"C:\Program Files\poppler\bin"),
            Path(r"C:\poppler\Library\bin"),
            Path(r"C:\poppler\bin"),
            Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "poppler" / "bin"
        ]
        for p in standard_paths:
            if (p / "pdftoppm.exe").exists():
                return str(p)
    return None

def render_pdf_to_images(pdf_path: Path, outdir: Path, max_pages: int = 5):
    outdir.mkdir(parents=True, exist_ok=True)
    rendered_images = []
    
    # Try pdf2image with Poppler
    try:
        from pdf2image import convert_from_path
        poppler_dir = find_poppler_path()
        images = convert_from_path(str(pdf_path), first_page=1, last_page=max_pages, poppler_path=poppler_dir)
        for idx, img in enumerate(images, start=1):
            target = outdir / f"{pdf_path.stem}_page_{idx}.png"
            img.save(str(target), "PNG")
            rendered_images.append(str(target))
            print(f"Rendered: {target}")
        return rendered_images
    except Exception as e:
        print(f"pdf2image notice: {e}. Checking fallback...", file=sys.stderr)

    # Fallback: Check pdftoppm CLI directly
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        poppler_bin = find_poppler_path()
        if poppler_bin:
            pdftoppm = str(Path(poppler_bin) / "pdftoppm.exe")

    if pdftoppm:
        prefix = outdir / f"{pdf_path.stem}_page"
        cmd = [pdftoppm, "-png", "-l", str(max_pages), str(pdf_path), str(prefix)]
        subprocess.run(cmd, check=True)
        for f in outdir.glob(f"{pdf_path.stem}_page-*.png"):
            rendered_images.append(str(f))
            print(f"Rendered: {f}")
        return rendered_images


    # Fallback 2: PyMuPDF (fitz)
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(str(pdf_path))
        limit = min(len(doc), max_pages)
        for idx in range(limit):
            page = doc[idx]
            pix = page.get_pixmap(dpi=150)
            target = outdir / f"{pdf_path.stem}_page_{idx + 1}.png"
            pix.save(str(target))
            rendered_images.append(str(target))
            print(f"Rendered: {target}")
        doc.close()
        return rendered_images
    except Exception as e:
        print(f"pymupdf notice: {e}. Checking fallback...", file=sys.stderr)

    raise RuntimeError("No PDF renderer available. Ensure Poppler or PyMuPDF is installed.")


def main():
    parser = argparse.ArgumentParser(description="Antigravity Visual Document Renderer CLI")
    parser.add_argument("file", help="Path to document file (.pdf, .pptx, .docx)")
    parser.add_argument("--outdir", default="./artifacts/previews", help="Target directory for rendered images")
    parser.add_argument("--max-pages", type=int, default=5, help="Maximum pages/slides to render (default: 5)")
    args = parser.parse_args()

    input_path = Path(args.file).resolve()
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    outdir = Path(args.outdir).resolve()
    ext = input_path.suffix.lower()

    if ext == ".pdf":
        render_pdf_to_images(input_path, outdir, args.max_pages)
    elif ext in [".docx", ".pptx", ".xlsx"]:
        # Convert to temp PDF first using convert_doc
        temp_pdf = outdir / f"{input_path.stem}_temp_render.pdf"
        convert_script = Path(__file__).parent / "convert_doc.py"
        res = subprocess.run([sys.executable, str(convert_script), str(input_path), str(temp_pdf)], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Failed to convert {ext} to temporary PDF for rendering: {res.stderr}", file=sys.stderr)
            sys.exit(1)
        render_pdf_to_images(temp_pdf, outdir, args.max_pages)
        if temp_pdf.exists():
            temp_pdf.unlink()
    else:
        print(f"Unsupported format for rendering: {ext}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
