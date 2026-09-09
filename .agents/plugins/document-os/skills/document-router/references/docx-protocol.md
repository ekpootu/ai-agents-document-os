# DOCX Processing Protocol

Microsoft Word (`.docx`) files are zipped OOXML packages containing structured XML documents (`word/document.xml`), styles, relationships, and embedded media.

## 1. Core Principles
- **Style-Centric Modification**: Prefer applying semantic styles (`Heading 1`, `Heading 2`, `Normal`, `List Bullet`) over hardcoded font sizes and colors.
- **Table Integrity**: Preserve column widths, cell padding, and header repeat settings across page splits.
- **Preserve Headers & Footers**: Ensure section break properties (`sectPr`) are retained when appending or editing text.

## 2. Tooling Selection
- **Reading & Structured Modification**: `python-docx`
  - Read: Iterate over `doc.paragraphs` and `doc.tables`.
  - Write: Use `doc.add_heading()`, `doc.add_paragraph()`, `doc.add_table()`.
- **Markdown &rarr; DOCX**: `pandoc` with optional reference document template (`--reference-doc=template.docx`).
- **DOCX &rarr; PDF**: Headless LibreOffice (`soffice --headless --convert-to pdf`).

## 3. Preservation Rules
- Never rewrite an entire document with plain text if it contains existing custom formatting, headers, or watermarks.
- For targeted edits in existing DOCX files, open the document in place with `python-docx`, find the target paragraph/table cell, and modify only that specific run/element.
