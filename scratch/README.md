# Scratch & Utility Test Scripts — Document OS

This directory contains standalone testing, verification, and experimental document generation scripts designed for developers and power users.

## Scripts

1. **`build_book_flip_pdf.py`**:
   Generates a publication-standard 1.6:1 aspect ratio showcase PDF with embedded Google Fonts (`Playfair Display`, `Source Sans 3`), two-pass interactive Table of Contents, and Amazon KDP / Socrates publishing geometry.
   ```bash
   python scratch/build_book_flip_pdf.py
   ```

2. **`verify_flip_pdf.py`**:
   Performs fast forensic structural inspection on generated PDFs, verifying exact dimensions, page count, and metadata integrity.
   ```bash
   python scratch/verify_flip_pdf.py
   ```

> [!NOTE]
> All core production CLI tools reside in `.agents/plugins/document-os/scripts/`. The scripts here are developer utilities and demonstration builders.
