#!/usr/bin/env python3
"""
convert_doc.py - Headless Conversion CLI
Discovers LibreOffice, Pandoc, and Python conversion backends to execute high-fidelity document conversions on Windows/Linux/macOS.
"""
import os
import sys
import shutil
import argparse
import subprocess
from pathlib import Path

def find_libreoffice():
    cmd = shutil.which("soffice") or shutil.which("libreoffice")
    if cmd:
        return cmd
    if sys.platform == "win32":
        standard_paths = [
            Path(r"C:\Program Files\LibreOffice\program\soffice.exe"),
            Path(r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"),
            Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "LibreOffice" / "program" / "soffice.exe"
        ]
        for p in standard_paths:
            if p.exists():
                return str(p)
    return None

def find_pandoc():
    cmd = shutil.which("pandoc")
    if cmd:
        return cmd
    if sys.platform == "win32":
        standard_paths = [
            Path(r"C:\Program Files\Pandoc\pandoc.exe"),
            Path(os.environ.get("LOCALAPPDATA", "")) / "Pandoc" / "pandoc.exe"
        ]
        for p in standard_paths:
            if p.exists():
                return str(p)
    return None

def convert_via_libreoffice(input_file: Path, target_format: str, outdir: Path):
    soffice = find_libreoffice()
    if not soffice:
        raise RuntimeError("LibreOffice (soffice) not found in PATH or standard Program Files locations.")
    
    cmd = [soffice, "--headless", "--convert-to", target_format, "--outdir", str(outdir), str(input_file)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"LibreOffice conversion failed: {res.stderr or res.stdout}")
    
    expected_output = outdir / f"{input_file.stem}.{target_format}"
    if not expected_output.exists():
        raise RuntimeError(f"Expected converted file was not created: {expected_output}")
    return expected_output

def convert_via_pandoc(input_file: Path, output_file: Path):
    pandoc = find_pandoc()
    if not pandoc:
        raise RuntimeError("Pandoc not found in PATH or standard Program Files locations.")
    
    cmd = [pandoc, str(input_file), "-o", str(output_file)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Pandoc conversion failed: {res.stderr or res.stdout}")
    return output_file

def convert_pdf_to_docx(input_file: Path, output_file: Path):
    try:
        from pdf2docx import Converter
        cv = Converter(str(input_file))
        cv.convert(str(output_file))
        cv.close()
        return output_file
    except ImportError:
        raise RuntimeError("pdf2docx library not installed. Install via pip install pdf2docx.")

def main():
    parser = argparse.ArgumentParser(description="Antigravity Headless Document Conversion CLI")
    parser.add_argument("input", help="Source document path")
    parser.add_argument("output", help="Target document path or format")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_arg = args.output
    if "." in output_arg:
        output_path = Path(output_arg).resolve()
        target_format = output_path.suffix.lower().lstrip(".")
        outdir = output_path.parent
    else:
        target_format = output_arg.lower().lstrip(".")
        outdir = input_path.parent
        output_path = outdir / f"{input_path.stem}.{target_format}"

    outdir.mkdir(parents=True, exist_ok=True)
    in_ext = input_path.suffix.lower()

    print(f"Converting {input_path.name} -> {target_format.upper()}...")
    try:
        # PDF -> DOCX
        if in_ext == ".pdf" and target_format == "docx":
            res = convert_pdf_to_docx(input_path, output_path)
        # Office -> PDF
        elif in_ext in [".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".odt", ".ods", ".odp"] and target_format == "pdf":
            res = convert_via_libreoffice(input_path, "pdf", outdir)
        # Markdown / HTML / TXT conversions
        elif in_ext in [".md", ".markdown", ".html", ".txt"] or target_format in ["md", "html"]:
            res = convert_via_pandoc(input_path, output_path)
        else:
            # Fallback to LibreOffice
            res = convert_via_libreoffice(input_path, target_format, outdir)

        print(f"Success: Converted to {res}")
    except Exception as e:
        print(f"Conversion Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
