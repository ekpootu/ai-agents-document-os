#!/usr/bin/env python3
"""
inspect_doc.py - Document Triage & Inspection CLI
Analyzes document metadata, internal structure, page/sheet counts, formulas, and scan layers.
"""
import os
import sys
import json
import argparse
from pathlib import Path

def inspect_pdf(filepath: Path) -> dict:
    info = {"format": "PDF", "path": str(filepath), "size_bytes": filepath.stat().st_size}
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(filepath))
        info["pages"] = len(reader.pages)
        info["is_encrypted"] = reader.is_encrypted
        
        sample_chars = 0
        for i in range(min(3, len(reader.pages))):
            text = reader.pages[i].extract_text() or ""
            sample_chars += len(text.strip())
            
        info["has_searchable_text"] = sample_chars > 30
        info["sample_character_count_first_3_pages"] = sample_chars
        info["likely_scanned"] = sample_chars <= 30
    except Exception as e:
        info["error"] = str(e)
    return info

def inspect_docx(filepath: Path) -> dict:
    info = {"format": "DOCX", "path": str(filepath), "size_bytes": filepath.stat().st_size}
    try:
        from docx import Document
        doc = Document(str(filepath))
        info["paragraphs_count"] = len(doc.paragraphs)
        info["tables_count"] = len(doc.tables)
        info["sections_count"] = len(doc.sections)
        sample_text = " ".join([p.text for p in doc.paragraphs[:5] if p.text.strip()])
        info["sample_text_preview"] = sample_text[:200]
    except Exception as e:
        info["error"] = str(e)
    return info

def inspect_xlsx(filepath: Path) -> dict:
    info = {"format": "XLSX", "path": str(filepath), "size_bytes": filepath.stat().st_size}
    try:
        import openpyxl
        wb = openpyxl.load_workbook(str(filepath), data_only=False, read_only=True)
        info["sheet_names"] = wb.sheetnames
        info["sheets_count"] = len(wb.sheetnames)
        
        # Check first sheet dimensions
        first_sheet = wb.active
        info["active_sheet"] = first_sheet.title
        info["max_row"] = first_sheet.max_row
        info["max_column"] = first_sheet.max_column
    except Exception as e:
        info["error"] = str(e)
    return info

def inspect_pptx(filepath: Path) -> dict:
    info = {"format": "PPTX", "path": str(filepath), "size_bytes": filepath.stat().st_size}
    try:
        from pptx import Presentation
        prs = Presentation(str(filepath))
        info["slides_count"] = len(prs.slides)
        info["slide_width_inches"] = round(prs.slide_width.inches, 2)
        info["slide_height_inches"] = round(prs.slide_height.inches, 2)
        info["aspect_ratio"] = "16:9" if abs(prs.slide_width.inches / prs.slide_height.inches - 1.777) < 0.1 else "4:3"
    except Exception as e:
        info["error"] = str(e)
    return info

def inspect_image(filepath: Path) -> dict:
    info = {"format": "IMAGE", "path": str(filepath), "size_bytes": filepath.stat().st_size}
    try:
        from PIL import Image
        with Image.open(str(filepath)) as img:
            info["image_format"] = img.format
            info["mode"] = img.mode
            info["width_px"] = img.width
            info["height_px"] = img.height
    except Exception as e:
        info["error"] = str(e)
    return info

def inspect_generic(filepath: Path) -> dict:
    info = {"format": filepath.suffix.upper().lstrip("."), "path": str(filepath), "size_bytes": filepath.stat().st_size}
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = [f.readline() for _ in range(5)]
            info["line_count_sample"] = len(lines)
            info["preview"] = "".join(lines)[:300]
    except Exception as e:
        info["error"] = str(e)
    return info

def main():
    parser = argparse.ArgumentParser(description="Antigravity Document Triage & Inspection CLI")
    parser.add_argument("file", help="Path to document file to inspect")
    parser.add_argument("--json", action="store_true", default=True, help="Output formatted JSON (default: True)")
    args = parser.parse_args()

    path = Path(args.file).resolve()
    if not path.exists():
        print(json.dumps({"error": f"File not found: {path}"}, indent=2))
        sys.exit(1)

    ext = path.suffix.lower()
    if ext == ".pdf":
        res = inspect_pdf(path)
    elif ext in [".docx", ".doc"]:
        res = inspect_docx(path)
    elif ext in [".xlsx", ".xls", ".xlsm"]:
        res = inspect_xlsx(path)
    elif ext in [".pptx", ".ppt"]:
        res = inspect_pptx(path)
    elif ext in [".png", ".jpg", ".jpeg", ".webp", ".tiff", ".bmp"]:
        res = inspect_image(path)
    else:
        res = inspect_generic(path)

    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
