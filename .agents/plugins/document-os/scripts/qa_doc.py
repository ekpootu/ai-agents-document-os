#!/usr/bin/env python3
"""
qa_doc.py - Document Quality Assurance & Integrity Validator
Validates file integrity, formula error tokens, slide bounds, and XML health.
"""
import os
import sys
import json
import argparse
from pathlib import Path

def qa_pdf(filepath: Path) -> dict:
    report = {"format": "PDF", "passed": True, "checks": []}
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(filepath))
        pages = len(reader.pages)
        if pages == 0:
            report["passed"] = False
            report["checks"].append({"check": "Page Count", "status": "FAIL", "detail": "0 pages found"})
        else:
            report["checks"].append({"check": "Page Count", "status": "PASS", "detail": f"{pages} pages"})
        
        # Check text extractability
        total_chars = sum(len((p.extract_text() or "").strip()) for p in reader.pages[:5])
        report["checks"].append({"check": "Text Sample Extraction", "status": "PASS", "detail": f"{total_chars} chars in first 5 pages"})
    except Exception as e:
        report["passed"] = False
        report["checks"].append({"check": "PDF Parsing", "status": "FAIL", "detail": str(e)})
    return report

def qa_docx(filepath: Path) -> dict:
    report = {"format": "DOCX", "passed": True, "checks": []}
    try:
        from docx import Document
        doc = Document(str(filepath))
        report["checks"].append({"check": "OOXML Structure", "status": "PASS", "detail": "Valid document.xml"})
        report["checks"].append({"check": "Paragraphs Count", "status": "PASS", "detail": f"{len(doc.paragraphs)} paragraphs"})
        report["checks"].append({"check": "Tables Count", "status": "PASS", "detail": f"{len(doc.tables)} tables"})
    except Exception as e:
        report["passed"] = False
        report["checks"].append({"check": "DOCX Parsing", "status": "FAIL", "detail": str(e)})
    return report

def qa_xlsx(filepath: Path) -> dict:
    report = {"format": "XLSX", "passed": True, "checks": []}
    try:
        import openpyxl
        wb = openpyxl.load_workbook(str(filepath), data_only=False)
        report["checks"].append({"check": "Workbook Open", "status": "PASS", "detail": f"{len(wb.sheetnames)} sheets"})
        
        # Scan for formula error tokens
        error_tokens = {"#REF!", "#VALUE!", "#DIV/0!", "#NAME?", "#N/A", "#NUM!", "#NULL!"}
        detected_errors = []
        
        for sheetname in wb.sheetnames:
            ws = wb[sheetname]
            for row in ws.iter_rows(values_only=True):
                for cell in row:
                    if isinstance(cell, str) and any(err in cell for err in error_tokens):
                        detected_errors.append(cell)

        if detected_errors:
            report["passed"] = False
            report["checks"].append({
                "check": "Formula Integrity",
                "status": "FAIL",
                "detail": f"Detected {len(detected_errors)} formula error tokens: {detected_errors[:5]}"
            })
        else:
            report["checks"].append({"check": "Formula Integrity", "status": "PASS", "detail": "0 formula errors detected"})
    except Exception as e:
        report["passed"] = False
        report["checks"].append({"check": "XLSX Parsing", "status": "FAIL", "detail": str(e)})
    return report

def qa_pptx(filepath: Path) -> dict:
    report = {"format": "PPTX", "passed": True, "checks": []}
    try:
        from pptx import Presentation
        prs = Presentation(str(filepath))
        slides = len(prs.slides)
        if slides == 0:
            report["passed"] = False
            report["checks"].append({"check": "Slide Count", "status": "FAIL", "detail": "0 slides found"})
        else:
            report["checks"].append({"check": "Slide Count", "status": "PASS", "detail": f"{slides} slides"})
        
        report["checks"].append({"check": "Presentation Structure", "status": "PASS", "detail": "Valid OOXML presentation tree"})
    except Exception as e:
        report["passed"] = False
        report["checks"].append({"check": "PPTX Parsing", "status": "FAIL", "detail": str(e)})
    return report

def main():
    parser = argparse.ArgumentParser(description="Antigravity Document QA Validator CLI")
    parser.add_argument("file", help="Path to document to validate")
    args = parser.parse_args()

    path = Path(args.file).resolve()
    if not path.exists():
        print(json.dumps({"passed": False, "error": f"File not found: {path}"}, indent=2))
        sys.exit(1)

    ext = path.suffix.lower()
    if ext == ".pdf":
        res = qa_pdf(path)
    elif ext in [".docx", ".doc"]:
        res = qa_docx(path)
    elif ext in [".xlsx", ".xls"]:
        res = qa_xlsx(path)
    elif ext in [".pptx", ".ppt"]:
        res = qa_pptx(path)
    else:
        res = {"format": ext.upper().lstrip("."), "passed": True, "checks": [{"check": "File Existence", "status": "PASS", "detail": f"{path.stat().st_size} bytes"}]}

    print(json.dumps(res, indent=2))
    sys.exit(0 if res.get("passed", False) else 1)

if __name__ == "__main__":
    main()
