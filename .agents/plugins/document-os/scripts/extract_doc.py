#!/usr/bin/env python3
"""
extract_doc.py - Unified Content Extraction CLI
Extracts text, tables (Markdown), and embedded media from PDF, DOCX, XLSX, and PPTX.
"""
import os
import sys
import argparse
from pathlib import Path

def extract_pdf(filepath: Path, extract_type: str, outdir: Path = None):
    if extract_type == "text":
        from pypdf import PdfReader
        reader = PdfReader(str(filepath))
        for idx, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            print(f"--- Page {idx} ---")
            print(text.strip())
            print()
    elif extract_type == "tables":
        import pdfplumber
        with pdfplumber.open(str(filepath)) as pdf:
            for idx, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                if tables:
                    print(f"### Page {idx} Tables")
                    for table in tables:
                        for row in table:
                            clean_row = [str(c).replace("\n", " ") if c is not None else "" for c in row]
                            print("| " + " | ".join(clean_row) + " |")
                        print()
    elif extract_type == "images":
        from pypdf import PdfReader
        reader = PdfReader(str(filepath))
        outdir = outdir or filepath.parent / f"{filepath.stem}_extracted_images"
        outdir.mkdir(parents=True, exist_ok=True)
        img_count = 0
        for p_idx, page in enumerate(reader.pages, start=1):
            for img_name, img_obj in page.images.items():
                img_count += 1
                img_path = outdir / f"p{p_idx}_{img_count}_{img_name}"
                with open(img_path, "wb") as fp:
                    fp.write(img_obj.data)
                print(f"Extracted image: {img_path}")
        print(f"Extracted {img_count} images to {outdir}")

def extract_docx(filepath: Path, extract_type: str, outdir: Path = None):
    from docx import Document
    doc = Document(str(filepath))
    if extract_type == "text":
        for p in doc.paragraphs:
            if p.text.strip():
                print(p.text)
    elif extract_type == "tables":
        for t_idx, table in enumerate(doc.tables, start=1):
            print(f"### Table {t_idx}")
            for row in table.rows:
                cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]
                print("| " + " | ".join(cells) + " |")
            print()
    elif extract_type == "images":
        outdir = outdir or filepath.parent / f"{filepath.stem}_extracted_images"
        outdir.mkdir(parents=True, exist_ok=True)
        img_count = 0
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                img_count += 1
                img_name = Path(rel.target_ref).name
                img_path = outdir / f"docx_img_{img_count}_{img_name}"
                with open(img_path, "wb") as f:
                    f.write(rel.target_part.blob)
                print(f"Extracted image: {img_path}")
        print(f"Extracted {img_count} images to {outdir}")

def extract_xlsx(filepath: Path, extract_type: str):
    import openpyxl
    wb = openpyxl.load_workbook(str(filepath), data_only=True)
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        print(f"### Sheet: {sheet}")
        for row in ws.iter_rows(values_only=True):
            if any(cell is not None for cell in row):
                clean_row = [str(c) if c is not None else "" for c in row]
                print("| " + " | ".join(clean_row) + " |")
        print()

def extract_pptx(filepath: Path, extract_type: str):
    from pptx import Presentation
    prs = Presentation(str(filepath))
    for s_idx, slide in enumerate(prs.slides, start=1):
        print(f"--- Slide {s_idx} ---")
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    if paragraph.text.strip():
                        print(paragraph.text.strip())
        print()

def main():
    parser = argparse.ArgumentParser(description="Antigravity Unified Document Extraction CLI")
    parser.add_argument("file", help="Path to document file")
    parser.add_argument("--type", choices=["text", "tables", "images"], default="text", help="Extraction target (default: text)")
    parser.add_argument("--outdir", help="Output directory for extracted media")
    args = parser.parse_args()

    path = Path(args.file).resolve()
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    outdir = Path(args.outdir).resolve() if args.outdir else None
    ext = path.suffix.lower()
    if ext == ".pdf":
        extract_pdf(path, args.type, outdir)
    elif ext in [".docx", ".doc"]:
        extract_docx(path, args.type, outdir)
    elif ext in [".xlsx", ".xls"]:
        extract_xlsx(path, args.type)
    elif ext in [".pptx", ".ppt"]:
        extract_pptx(path, args.type)
    else:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            print(f.read())

if __name__ == "__main__":
    main()
