# Implementation Plan: Antigravity Universal Document Operating System (Document OS)

Transform Antigravity from a generic file-reading agent into a professional, high-fidelity **Document Operating System** capable of reading, parsing, transforming, generating, and quality-assuring all major document formats (`.pdf`, `.docx`, `.xlsx`, `.pptx`, `.md`, `.csv`, `.json`, image/OCR formats) on Windows.

---

## Strategic Evaluation: Point 27 vs. Point 29

In your attached discussion, two distinct directions were presented:
* **Point 27 (My recommended final installation):** Install 8 separate standalone skills (`document-router`, `document-processing`, `document-qa`, `pdf`, `docx`, `xlsx`, `pptx`, `image-ocr`), a long list of pip libraries, and 6 system tools.
* **Point 29 (My strongest recommendation):** Package the system as a unified **"Universal Document Workspace"** (an Antigravity Plugin) containing a coherent skill suite, deterministic helper scripts, safety rules, and validation pipelines.

### Our Recommendation & Strategic Verdict: **Enhanced Point 29 (Unified Plugin Architecture)**
We strongly recommend **Point 29** over Point 27 for the following technical reasons:

1. **Eliminating Prompt Bloat & Conflicting Directives:**
   If you install 8 standalone skills simultaneously from different authors (`skills.sh`, GitHub, etc.), their `SKILL.md` frontmatter descriptions and instructions compete in Antigravity's context. One skill might tell the agent to use `pypdf`, while another says `pdfplumber`, and a third insists on `pdf2docx` or Pandoc. Under Point 29, the **Master Document Router** serves as the single entrypoint and systematically routes tasks to specialized procedural references or sub-skills.
2. **Deterministic Script Substrate vs. LLM Code Hallucination:**
   Office documents (especially OOXML formats like DOCX/XLSX/PPTX) and multi-column PDFs fail when agents attempt to write raw Python code on the fly from memory without validation. Point 29 bundles pre-tested, hardened Python CLI scripts (`inspect_doc.py`, `extract_doc.py`, `convert_doc.py`, `render_doc.py`, `qa_doc.py`) directly inside the plugin. The agent calls these proven CLI tools instead of reinventing the wheel.
3. **Antigravity-Native Plugin Standard:**
   Antigravity officially supports `plugins/<plugin_name>/` containing `plugin.json`, `skills/`, `rules/`, and `hooks.json`. This enables 1-click portable distribution—you can use it locally in this project (`.agents/plugins/document-os/`) or drop it into your global Antigravity config (`~/.gemini/config/plugins/document-os/`) for all projects.

---

## User Review Required

> [!IMPORTANT]
> **Windows System Dependencies (`winget`)**:
> Native Office document rendering (DOCX/PPTX/XLSX &rarr; PDF) and high-fidelity PDF page rendering require system-level tools:
> - **LibreOffice** (`TheDocumentFoundation.LibreOffice`) for headless Office conversion & rendering.
> - **Pandoc** (`JohnMacFarlane.Pandoc`) for Markdown & cross-document interchange.
> - **Tesseract OCR** (`UB-Mannheim.TesseractOCR`) for scanned document image OCR.
> - **Poppler for Windows** for `pdftoppm` / `pdf2image`.
> 
> Our PowerShell install script (`install_document_os.ps1`) will detect which of these are installed and can run `winget install` for any missing tools upon your approval.

> [!NOTE]
> **Python Environment Strategy**:
> We detected Python 3.14.0 on your system. To avoid library conflicts, we recommend creating a dedicated virtual environment (`.venv-docos` inside the project or global tools directory) containing all required libraries (`pypdf`, `pdfplumber`, `pdf2image`, `python-docx`, `openpyxl`, `xlsxwriter`, `pandas`, `python-pptx`, `Pillow`, `pytesseract`, `pdf2docx`). The helper scripts will automatically execute using this venv's Python binary.

---

## Open Questions

1. **Installation Scope**:
   - Do you want this setup installed **locally in the current workspace** (`c:\AntigravityProjects\SkillsPluginsMCP\.agents/`), or **globally** (`~/.gemini/config/plugins/document-os/`) so every Antigravity project automatically has it, or **both** (configured locally now, with an automated export script to global)?
   *(Recommended: Both. We will construct it completely in `.agents/plugins/document-os/` and provide an installation switch in `install_document_os.ps1` to copy it to global).*
2. **System Tool Installation via Winget**:
   - Would you like the installer script to automatically trigger `winget install` for LibreOffice, Pandoc, and Tesseract, or would you prefer it to prompt you for each one?

---

## Proposed Architecture & File Tree

The complete Document OS is structured cleanly within the workspace `.agents/` directory (and can be deployed globally):

```text
c:\AntigravityProjects\SkillsPluginsMCP\
├── GEMINI.md                                  # Root document handling & safety principles
├── install_document_os.ps1                   # Automated setup, dependency installer, & diagnostics
├── .agents/
│   ├── rules/
│   │   └── document-safety.md                # Granular document preservation & mutation rules
│   └── plugins/
│       └── document-os/
│           ├── plugin.json                   # Plugin manifest declaring Document OS
│           ├── skills/
│           │   ├── document-router/          # Master entrypoint skill
│           │   │   ├── SKILL.md              # Router decision tree & progressive disclosure
│           │   │   └── references/           # Detailed format-specific protocols
│           │   │       ├── pdf-protocol.md
│           │   │       ├── docx-protocol.md
│           │   │       ├── xlsx-protocol.md
│           │   │       ├── pptx-protocol.md
│           │   │       ├── image-ocr-protocol.md
│           │   │       └── conversion-matrix.md
│           │   └── document-qa/              # Verification & validation skill
│           │       └── SKILL.md              # Integrity checks, rendering, & report checklist
│           └── scripts/                      # Deterministic Python CLI helpers
│               ├── inspect_doc.py            # Triage & metadata detection
│               ├── extract_doc.py            # Text, table, & image extraction
│               ├── convert_doc.py            # Headless conversion (LibreOffice / Pandoc)
│               ├── render_doc.py             # Page/slide rendering to image for visual QA
│               ├── ocr_doc.py                # Tesseract OCR wrapper for images & scanned PDFs
│               └── qa_doc.py                 # Structural & visual health validator
```

---

## Proposed Changes

### Component 1: Rules & Policies

#### [NEW] [GEMINI.md](file:///c:/AntigravityProjects/SkillsPluginsMCP/GEMINI.md)
- Establishes core document operating principles:
  - **Zero Unintentional Data Loss**: Original documents are read-only by default; edits produce versioned outputs (`filename_modified.ext`) unless explicit overwrites are requested.
  - **Triage First**: Always inspect document structure (scanned vs text, formula vs raw value, layout vs prose) before operating.
  - **Preserve Structure**: Keep styles, formulas, sheet hierarchies, speaker notes, and embedded assets intact.
  - **Mandatory Validation**: Always run QA on newly generated or modified documents before presenting completion.

#### [NEW] [.agents/rules/document-safety.md](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/rules/document-safety.md)
- Specific behavioral directives on permission boundaries:
  - Non-destructive inspection/extraction is automatically allowed.
  - File replacement/deletion requires user confirmation.
  - Office automation commands are scoped and handled cleanly on Windows.

---

### Component 2: Skills & Router Engine

#### [NEW] [plugin.json](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/plugin.json)
- Antigravity plugin manifest defining name (`antigravity-document-os`), version (`1.0.0`), description, and exported skills.

#### [NEW] [document-router/SKILL.md](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/skills/document-router/SKILL.md)
- Master triage and routing skill. Triggers whenever any document file (`.pdf`, `.docx`, `.xlsx`, `.pptx`, `.csv`, `.md`, images) is referenced for reading, writing, conversion, or analysis.
- Defines the 5-step Document Lifecycle:
  1. **Triage**: Run `inspect_doc.py` to identify mimetype, encoding, page count, layers, formulas, or scanned status.
  2. **Route**: Select the specialist path (PDF, DOCX, XLSX, PPTX, OCR, Pandoc).
  3. **Execute**: Use the dedicated Python library or CLI helper script.
  4. **Render**: Generate thumbnail/page previews using `render_doc.py` if visual layout matters.
  5. **Verify**: Run `qa_doc.py` to assert document health and report limitations.

#### [NEW] [Format Protocols (PDF, DOCX, XLSX, PPTX, OCR, Conversion)](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/skills/document-router/references/)
- `pdf-protocol.md`: Rules for searchable vs scanned, table extraction (`pdfplumber`), text extraction (`pypdf`), form filling.
- `docx-protocol.md`: OOXML structure, paragraph/table styles, header/footer preservation, Word-to-PDF pipeline.
- `xlsx-protocol.md`: Formula preservation (`openpyxl` data_only=False vs True), multi-sheet handling, formatting, chart safety.
- `pptx-protocol.md`: Slide master layouts, text box wrapping, shape manipulation, slide export.
- `image-ocr-protocol.md`: Multimodal vision vs Tesseract OCR, binarization, preprocessing.
- `conversion-matrix.md`: High-fidelity vs lossy conversion matrix across all pairs.

#### [NEW] [document-qa/SKILL.md](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/skills/document-qa/SKILL.md)
- Detailed validation protocols: file integrity, missing font detection, formula error scanning (`#REF!`, `#VALUE!`), overflow checking, and conversion fidelity reporting.

---

### Component 3: Deterministic Python CLI Helpers (`scripts/`)

#### [NEW] [inspect_doc.py](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/scripts/inspect_doc.py)
- CLI tool returning structured JSON detailing format, page/sheet/slide count, text density, OCR necessity, metadata, and formula presence.

#### [NEW] [extract_doc.py](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/scripts/extract_doc.py)
- CLI tool to extract plain text, Markdown-formatted tables, or embedded images from PDF, DOCX, XLSX, PPTX.

#### [NEW] [convert_doc.py](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/scripts/convert_doc.py)
- Robust wrapper executing headless LibreOffice (`soffice.exe`) or Pandoc on Windows, automatically discovering their installation paths in standard Program Files locations.

#### [NEW] [render_doc.py](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/scripts/render_doc.py)
- Renders PDF pages or Office slides to PNG images for visual inspection and multi-modal QA review.

#### [NEW] [ocr_doc.py](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/scripts/ocr_doc.py)
- Handles image and scanned PDF OCR via Tesseract with automatic image pre-processing (deskew, contrast enhancement).

#### [NEW] [qa_doc.py](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/scripts/qa_doc.py)
- Automated verification script checking if generated files open without corruption, verifying sheet counts, slide counts, formula validity, and structural integrity.

---

### Component 4: Environment & Automated Installer

#### [NEW] [install_document_os.ps1](file:///c:/AntigravityProjects/SkillsPluginsMCP/install_document_os.ps1)
- Comprehensive Windows PowerShell script that:
  1. Checks Python and creates a dedicated virtual environment `.venv-docos`.
  2. Installs all required Python packages (`pypdf`, `pdfplumber`, `pdf2image`, `pdf2docx`, `pytesseract`, `python-docx`, `openpyxl`, `xlsxwriter`, `pandas`, `python-pptx`, `Pillow`).
  3. Checks for LibreOffice, Pandoc, Tesseract, and Poppler on Windows PATH and Program Files.
  4. Provides optional 1-click `winget` installation commands for missing tools.
  5. Performs end-to-end self-test diagnostics across PDF, DOCX, XLSX, and PPTX creation.
  6. Provides an optional `-Global` switch to sync/link the plugin into `~/.gemini/config/plugins/document-os/`.

---

## Verification Plan

### Automated Preflight & Self-Test
- Run `install_document_os.ps1 -DryRun` and execute `python scripts/inspect_doc.py` against test document samples.
- Generate a sample `.docx`, `.xlsx`, and `.pptx` via Python scripts, convert them, and run `qa_doc.py` to assert 100% integrity.

### Manual Verification
- Review the generated folder tree and files in Antigravity.
- Test routing instructions with a test query (e.g., simulating a document conversion and spreadsheet audit).
