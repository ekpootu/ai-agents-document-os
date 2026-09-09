# PDF Processing Protocol

PDF is a composite representation format that requires differentiated handling based on whether it is vector text, scanned raster imagery, forms, or table-centric.

## 1. Triage Decision Tree

```text
PDF Document
├── Has extractable text stream (> 50 chars/page)?
│   ├── YES -> Digital PDF
│   │   ├── Table-heavy? -> Use `pdfplumber` for table grid extraction
│   │   └── Standard text? -> Use `pypdf` or `pdfplumber` text extraction
│   └── NO  -> Scanned / Image PDF
│       └── Route to `ocr_doc.py` (render page to image -> Tesseract OCR)
└── Has interactive AcroForm fields?
    └── Use `pypdf` reader/writer form field mapping
```

## 2. Extraction Best Practices
- **Text Streams**: Use `pypdf.PdfReader` for high-throughput text extraction.
- **Tables**: `pdfplumber` extracts precise cell bounding boxes and reconstructs tabular data as nested lists or Markdown tables.
- **Page Slicing & Merging**: Use `pypdf` for splitting, merging, rotating, or encrypting/decrypting PDF files without re-encoding media.

## 3. PDF Generation Best Practices
- For programmatic PDF report generation, use **ReportLab** (`reportlab.platypus`) with explicit flowables (Paragraphs, Tables, Spacers).
- For document conversion (DOCX &rarr; PDF or PPTX &rarr; PDF), use headless LibreOffice via `convert_doc.py`.

## 4. Verification Checklist
- Confirm page count matches expected output.
- Check for text flow truncation across page boundaries.
- Render sample pages to PNG using `render_doc.py` to inspect visual formatting.
