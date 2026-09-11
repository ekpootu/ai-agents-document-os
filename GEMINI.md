# AI Agents Document Operating System (Document OS) Rules

When operating in this workspace, treat document processing as an engineering discipline requiring strict integrity, format awareness, and zero-loss guarantees.

## Fundamental Principles

1. **Zero Unintentional Data Loss & Non-Destructive Mutations**
   - NEVER overwrite or mutate an original document unless the user explicitly commands an in-place overwrite.
   - Default to writing transformed, repaired, or converted outputs with clean descriptive suffixes (e.g., `filename_processed.docx`, `report_v2.pdf`).
   - If in-place modification is explicitly commanded, create a backup copy (`filename.bak.ext`) before modifying.

2. **Triage Before Action**
   - Never assume file contents solely based on extension.
   - Run triage (`inspect_doc.py` or format inspection) first to determine:
     - Is the PDF digital/searchable or a scanned image?
     - Does the Excel file contain dynamic formulas (`=SUM`, `=VLOOKUP`) or static numbers?
     - Does the Word document use structured styles or raw manual formatting?
     - Does the PowerPoint presentation use standard slide masters or custom canvas layouts?

3. **Format Fidelity & Specialized Handling**
   - **PDF**: Do not convert complex multi-column or table-heavy PDFs to plain text without structural extraction. Use `pdfplumber` for tables, `pypdf` for clean text streams, and OCR for rasterized pages.
   - **DOCX**: Preserve styles, headers, footers, table borders, and document metadata. Use `python-docx` for content and OOXML inspection for low-level features.
   - **XLSX**: Always preserve formulas. When reading values for computation, distinguish between stored formulas and evaluated cached values. Never clobber existing formatting, charts, or hidden sheets.
   - **PPTX**: Respect master templates, slide dimensions, and typography. Ensure generated text frames don't overflow slide boundaries.
   - **Images/OCR**: Use multimodal vision for semantic understanding; use Tesseract OCR with image preprocessing for deterministic text extraction.

4. **Mandatory Post-Execution Quality Assurance (QA)**
   - Never report a document task as "Complete" without validating the generated file.
   - Run `qa_doc.py` to confirm that the file opens cleanly, contains expected page/sheet counts, has no formula errors (`#REF!`, `#DIV/0!`, `#VALUE!`), and renders correctly.

5. **Tool Execution Standards**
   - Prefer the deterministic Python CLI helpers in `.agents/plugins/document-os/scripts/` over impromptu, one-off script generation.
   - If LibreOffice (`soffice`) or Pandoc is required for headless conversions, ensure the toolchain is available before executing.

6. **Brand Identity Enforcement**
   - When creating, updating, or designing any document (PDF, DOCX, PPTX) or web page, ALWAYS activate the `brand-identity` skill at `.agents/skills/brand-identity/SKILL.md`.
   - Use the brand color palette: Royal Blue (`#1A3A8F`), Golden Yellow (`#FFC107`), Deep Navy (`#0D1B4C`).
   - Use the font pairings: Playfair Display (display), Source Sans 3 (body), JetBrains Mono (code).
   - Load design tokens from `.agents/skills/brand-identity/resources/brand-tokens.json` for script-driven generation.

7. **Multimodal Media & AI Image Generation**
   - When creating or illustrating documents, generate high-resolution visual assets with cutting-edge AI image generation models (such as Nanobanana Pro or Imagen 3) or source authentic, royalty-free assets from services like Pexels and Pixabay.

8. **Plain Language & Friendly Tone**
   - Write all guides, summaries, and agent communications in clear, friendly, and accessible English. Replace confusing technical jargon with straightforward explanations and clear examples so that every user feels supported.

9. **The Golden Ratio & Harmonious Page Layouts**
   - Format book-length and whitepaper publications using the Golden Ratio ($\phi \approx 1.618:1$, $6.0" \times 9.71"$) or the standard 6" x 9" Trade Trim with Tschichold's Golden Canon of Page Construction, creating spacious, readable, and elegant layouts.

## Author & Attribution

- **Author**: [Ekpo Otu, Ph.D.](https://linktr.ee/ekpootu)
- **Repository**: [github.com/ekpootu/ai-agents-document-os](https://github.com/ekpootu/ai-agents-document-os)
- **Support**: [buymeacoffee.com/ekpootu](https://www.buymeacoffee.com/ekpootu)

