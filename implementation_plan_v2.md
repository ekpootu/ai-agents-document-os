# Implementation Plan: Antigravity Universal Document Operating System (Document OS)

Transform Antigravity (and compatible agent harnesses such as Claude Code, OpenCode CLI, and Cursor) into a professional, high-fidelity **Document Operating System** capable of reading, parsing, transforming, generating, and quality-assuring all major document formats (`.pdf`, `.docx`, `.xlsx`, `.pptx`, `.md`, `.csv`, `.json`, image/OCR formats) on Windows, macOS, and Linux.

---

## Approved User Decisions & Architectural Enhancements

1. **Installation Scope (Dual Deployment):**
   - **Local Workspace**: Installs into `c:\AntigravityProjects\SkillsPluginsMCP\.agents/plugins/document-os/` and root `GEMINI.md`.
   - **Global Configuration**: `install_document_os.ps1` includes a `-DeployGlobal` flag that safely deploys and links the plugin to `$HOME\.gemini\config\plugins\document-os/`.
2. **Safe Automated Winget Provisioning:**
   - The installer checks if LibreOffice, Pandoc, and Tesseract are present in PATH or standard Program Files locations.
   - If missing, it automatically and safely invokes `winget install --silent --accept-package-agreements --accept-source-agreements` for each approved tool.
3. **Dedicated Python Virtual Environment (`.venv-docos`):**
   - Isolates all document processing libraries (`pypdf`, `pdfplumber`, `pdf2image`, `python-docx`, `openpyxl`, `xlsxwriter`, `pandas`, `python-pptx`, `Pillow`, `pytesseract`, `pdf2docx`, `reportlab`) from the host Python.
4. **Cross-Harness Open Standards Portability:**
   - The core skills adhere strictly to the open **Agent Skills specification** (`SKILL.md` with YAML frontmatter).
   - Python helper CLI tools are 100% standalone and CLI-agnostic.
   - An adapter/linker script supports exporting to:
     - **Antigravity** (`.agents/skills/` or `~/.gemini/config/skills/` & `plugins/`)
     - **Claude Code** (`.claude/skills/` or `~/.claude/skills/`)
     - **OpenCode CLI / Cursor / Cline** (`.skills/` or `~/.config/opencode/skills/`).
5. **Dogfooding Milestone — Official PDF Guide Generation:**
   - Once the Document OS toolchain and scripts are fully configured, the agent will execute the Document OS itself to generate a beautifully styled, authoritative PDF user guide: `Antigravity_Document_OS_Comprehensive_Guide.pdf`.
6. **Open Source GitHub Release & Psychology-Driven Landing Page:**
   - Production-ready GitHub repository scaffolding (`README.md`, `LICENSE` [MIT], `CONTRIBUTING.md`, `.github/workflows/ci.yml`).
   - A modern, responsive HTML/CSS landing page (`web/index.html`) engineered with behavioral psychology storytelling:
     - **The Pain (Agitation):** Hallucinated text, corrupt XML files, broken formulas in spreadsheets, missing fonts in slide decks, blown context limits.
     - **The Revelation (Solution):** Deterministic format triage, progressive disclosure skills, bulletproof local Python helpers, and automated visual QA.
     - **The Proof & Why:** Architecture diagrams, zero-loss guarantee, cross-harness compatibility.
     - **Actionable CTAs:** One-line install command, GitHub Star badge, Fork & PR guide, and "Buy Me a Coffee" sponsorship hook.

---

## Complete Folder Tree

```text
c:\AntigravityProjects\SkillsPluginsMCP\
├── GEMINI.md                                  # Root Antigravity document operating rules
├── AGENTS.md                                  # OpenCode & universal agent instructions
├── README.md                                  # GitHub Open Source presentation & quickstart
├── LICENSE                                    # MIT License
├── CONTRIBUTING.md                            # Contribution guidelines & skill addition guide
├── install_document_os.ps1                   # Windows automated setup & winget installer
├── install_document_os.sh                    # Linux/macOS cross-platform installer
├── export_cross_harness.ps1                  # Export to Claude Code, OpenCode, Antigravity
│
├── .agents/
│   ├── rules/
│   │   └── document-safety.md                # Safety, confirmation triggers & immutability rules
│   └── plugins/
│       └── document-os/
│           ├── plugin.json                   # Antigravity Plugin manifest
│           ├── skills/
│           │   ├── document-router/          # Master router & triage skill
│           │   │   ├── SKILL.md
│           │   │   └── references/           # Detailed format protocols
│           │   │       ├── pdf-protocol.md
│           │   │       ├── docx-protocol.md
│           │   │       ├── xlsx-protocol.md
│           │   │       ├── pptx-protocol.md
│           │   │       ├── image-ocr-protocol.md
│           │   │       └── conversion-matrix.md
│           │   └── document-qa/              # Verification & validation skill
│           │       └── SKILL.md
│           └── scripts/                      # Deterministic Python CLI helpers
│               ├── inspect_doc.py            # Triage & metadata detection
│               ├── extract_doc.py            # Text, tables, images extraction
│               ├── convert_doc.py            # Headless conversion engine
│               ├── render_doc.py             # Page/slide rendering to image
│               ├── ocr_doc.py                # Tesseract OCR wrapper
│               ├── qa_doc.py                 # Structural & visual health validator
│               └── build_pdf_guide.py        # Generates official PDF documentation
│
├── docs/                                      # Project documentation & output assets
│   └── Antigravity_Document_OS_Comprehensive_Guide.pdf # Dogfooded PDF artifact
│
└── web/                                       # Open Source Showcase Landing Page
    ├── index.html                            # Psychology storytelling landing page
    └── styles.css                            # Glassmorphic, modern dark-mode aesthetic
```

---

## Proposed Changes by Component

### Component 1: Rules & Safety Policies
#### [NEW] [GEMINI.md](file:///c:/AntigravityProjects/SkillsPluginsMCP/GEMINI.md)
- Core rules: Non-destructive operations, always inspect before modifying, preserve formulas & formatting, validate every generated file before reporting success.
#### [NEW] [AGENTS.md](file:///c:/AntigravityProjects/SkillsPluginsMCP/AGENTS.md)
- Universal Agent Guidelines for OpenCode, Claude Code, and other agent harnesses.
#### [NEW] [.agents/rules/document-safety.md](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/rules/document-safety.md)
- Granular permission model: Read/inspect operations auto-allowed; file overwriting/destructive changes require user confirmation.

---

### Component 2: Antigravity Plugin & Agent Skills
#### [NEW] [plugin.json](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/plugin.json)
- Manifest defining `document-os`, version, skills export, and metadata.
#### [NEW] [document-router/SKILL.md](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/skills/document-router/SKILL.md)
- Master triage and routing skill triggering on all document formats.
#### [NEW] [Format Protocols (6 Reference Documents)](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/skills/document-router/references/)
- `pdf-protocol.md`, `docx-protocol.md`, `xlsx-protocol.md`, `pptx-protocol.md`, `image-ocr-protocol.md`, `conversion-matrix.md`.
#### [NEW] [document-qa/SKILL.md](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/skills/document-qa/SKILL.md)
- Integrity verification, formula error scans (`#REF!`, `#DIV/0!`), slide overflow checks, and visual comparison.

---

### Component 3: Deterministic Python CLI Helpers (`scripts/`)
All scripts are standalone, use standard `argparse`, output clean JSON/text, and handle Windows path encoding.
#### [NEW] [inspect_doc.py](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/scripts/inspect_doc.py)
- Triages documents (type, pages, text vs scanned, layers, formulas).
#### [NEW] [extract_doc.py](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/scripts/extract_doc.py)
- Extracts text, Markdown tables, and images.
#### [NEW] [convert_doc.py](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/scripts/convert_doc.py)
- Auto-locates LibreOffice / Pandoc on Windows and executes headless conversion.
#### [NEW] [render_doc.py](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/scripts/render_doc.py)
- Renders PDF pages or presentation slides to PNG images for visual inspection.
#### [NEW] [ocr_doc.py](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/scripts/ocr_doc.py)
- Tesseract OCR wrapper with image thresholding/preprocessing.
#### [NEW] [qa_doc.py](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/scripts/qa_doc.py)
- Validates file opens cleanly, verifies formulas, checks for corruption.
#### [NEW] [build_pdf_guide.py](file:///c:/AntigravityProjects/SkillsPluginsMCP/.agents/plugins/document-os/scripts/build_pdf_guide.py)
- Builds the publication-quality PDF manual utilizing ReportLab and the Document OS scripts.

---

### Component 4: Environment, Installers & Cross-Harness Export
#### [NEW] [install_document_os.ps1](file:///c:/AntigravityProjects/SkillsPluginsMCP/install_document_os.ps1)
- Windows PowerShell automated installer: Creates `.venv-docos`, installs pip packages, executes safe `winget` installations for missing tools, runs diagnostics, and supports `-DeployGlobal`.
#### [NEW] [install_document_os.sh](file:///c:/AntigravityProjects/SkillsPluginsMCP/install_document_os.sh)
- Linux/macOS bash installer for cross-platform portability.
#### [NEW] [export_cross_harness.ps1](file:///c:/AntigravityProjects/SkillsPluginsMCP/export_cross_harness.ps1)
- Copies or symlinks skills to Claude Code (`~/.claude/skills`), OpenCode (`~/.config/opencode/skills`), and Antigravity global (`~/.gemini/config/`).

---

### Component 5: Dogfooding Artifact & Open Source GitHub Assets
#### [NEW] [docs/Antigravity_Document_OS_Comprehensive_Guide.pdf](file:///c:/AntigravityProjects/SkillsPluginsMCP/docs/Antigravity_Document_OS_Comprehensive_Guide.pdf)
- Fully compiled PDF document detailing architecture, commands, and deployment guide.
#### [NEW] [README.md](file:///c:/AntigravityProjects/SkillsPluginsMCP/README.md)
- Complete GitHub repo documentation with psychological narrative, architectural diagrams, badges, and quickstart.
#### [NEW] [LICENSE](file:///c:/AntigravityProjects/SkillsPluginsMCP/LICENSE)
- MIT License.
#### [NEW] [web/index.html & web/styles.css](file:///c:/AntigravityProjects/SkillsPluginsMCP/web/)
- Responsive, high-converting Open Source landing page utilizing storytelling psychology (Pain &rarr; Epiphany &rarr; Solution &rarr; Verification &rarr; Actionable CTAs for Star, Fork, and Buy Me a Coffee).

---

## Verification Plan

### Automated Execution & Testing
1. Execute `install_document_os.ps1` to configure `.venv-docos`, install Python packages, and verify tool detection.
2. Run `scripts/qa_doc.py` against sample generated files (`.docx`, `.xlsx`, `.pptx`, `.pdf`).
3. Run `scripts/build_pdf_guide.py` to generate the complete user guide PDF.
4. Verify the generated PDF opens, has proper page count, typography, and styling.
5. Launch/inspect `web/index.html` to confirm rich visual aesthetics and responsiveness.
