# Document Conversion Fidelity Matrix

Cross-format conversion must always be intentional, aware of lossiness, and executed through the highest-fidelity available engine.

| Source &rarr; Target | Fidelity Level | Recommended Tool | Potential Artifacts / Risks |
| :--- | :--- | :--- | :--- |
| **DOCX &rarr; PDF** | **Near Perfect** (100%) | Headless LibreOffice (`soffice`) | Minor font substitution if fonts are missing |
| **PPTX &rarr; PDF** | **Near Perfect** (98%) | Headless LibreOffice (`soffice`) | Animations/transitions removed |
| **XLSX &rarr; PDF** | **Good** (90%) | Headless LibreOffice (`soffice`) | Page break splits wide tables |
| **MD &rarr; DOCX** | **High** (95%) | Pandoc | Needs `--reference-doc` for custom styles |
| **DOCX &rarr; MD** | **High** (90%) | Pandoc | Complex multi-column layouts flattened |
| **PDF &rarr; DOCX** | **Moderate / Lossy** (70-85%) | `pdf2docx` | Text flow may convert into absolute textboxes |
| **PDF &rarr; MD** | **Structural** (80-90%) | `extract_doc.py` (`pdfplumber`) | Header/footer repetition, table grid reconstruction |
| **XLSX &rarr; CSV** | **Data Only** (100% data) | `pandas` / `openpyxl` | All formulas, formatting, and other sheets lost |
| **CSV &rarr; XLSX** | **Perfect** (100%) | `openpyxl` / `pandas` | Clean import with column auto-width |

## Conversion Rules of Thumb
1. **Never perform double conversions** (e.g. PDF &rarr; DOCX &rarr; PPTX). Always convert from the highest fidelity source available.
2. When converting **PDF &rarr; DOCX**, warn the user about layout textbox artifacts.
3. When converting **XLSX &rarr; PDF**, configure landscape orientation and print area fit if tables are wider than 6 columns.
