# 📄 Antigravity Document Operating System (Document OS)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Antigravity Compatible](https://img.shields.io/badge/Antigravity-Plugins-purple.svg)](https://cloud.google.com)
[![Claude Code Ready](https://img.shields.io/badge/Claude%20Code-Skills-orange.svg)](https://anthropic.com)
[![OpenCode CLI](https://img.shields.io/badge/OpenCode-Portable-green.svg)](https://github.com/ekpootu/ai-agents-document-os)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-☕-yellow.svg)](https://www.buymeacoffee.com/ekpootu)

> **The Universal Document Operating System for AI Agents.**
> Stop LLM document hallucinations, broken spreadsheet formulas, destroyed layouts, and corrupt OOXML files. Give your agents a deterministic, high-fidelity engineering substrate for `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.md`, and OCR.

---

## 🛑 The Pain: Why Document Operations in AI Agents Break

Every developer who has asked an AI agent to *"Analyze this Excel sheet"*, *"Convert this PDF to Word"*, or *"Update this corporate slide deck"* knows the sinking feeling:

1. **Dead Spreadsheet Formulas**: The agent reads an Excel sheet and spits back static numbers, silently wiping out `=SUM()`, `=VLOOKUP()`, and financial calculation graphs.
2. **Corrupted Presentations**: PowerPoint opens with a terrifying warning: *"We found a problem with some content in presentation.pptx. Do you want us to try to recover?"*
3. **Destroyed Word Layouts**: Multi-column documents, custom margins, headers, and company templates are flattened into naked Markdown text.
4. **Context Window Choking**: Feeding a 200-page scanned PDF into context blows token budgets, resulting in hallucinated summaries and massive inference bills.
5. **Zero Accountability**: Agents declare *"I have updated your document!"* without ever testing if the generated file actually opens.

---

## 💡 The Solution: A True Document Operating System

Instead of relying on LLM memory to write raw, one-off scripts, **Document OS** introduces an engineering-grade operating system for documents:

```mermaid
graph TD
    User([User / Agent Task]) --> Router[Master Document Router]
    Router --> Triage[Stage 1: Preflight Triage & Inspection]
    Triage --> Protocol{Stage 2: Specialist Format Protocol}
    Protocol -->|PDF| PDF_Eng[pypdf + pdfplumber + OCR]
    Protocol -->|DOCX| DOCX_Eng[python-docx + OOXML Engine]
    Protocol -->|XLSX| XLSX_Eng[openpyxl + Formula Graph Guard]
    Protocol -->|PPTX| PPTX_Eng[python-pptx + Bound Overflow Guard]
    Protocol -->|Conversion| Conv_Eng[Headless LibreOffice + Pandoc]
    
    PDF_Eng & DOCX_Eng & XLSX_Eng & PPTX_Eng & Conv_Eng --> Render[Stage 4: Multi-Modal Visual Rendering]
    Render --> QA[Stage 5: Automated QA Integrity Validator]
    QA --> Output([Verified High-Fidelity Document])
```

- 🔍 **Triage First**: Analyzes digital text vs scanned layers, formula trees, and sheet layouts before touching data.
- 🛡️ **Zero Unintentional Data Loss**: Read-only by default; versioned outputs; formulas protected.
- ⚡ **Deterministic CLI Helpers**: Tested, standalone Python CLI tools (`inspect`, `extract`, `convert`, `render`, `qa`).
- 👁️ **Visual QA & Multi-Modal Verification**: Renders generated pages and slides to high-resolution PNGs so the agent can visually inspect its work.
- 🌐 **Cross-Harness Freedom**: Native in Google Antigravity, 1-click exportable to Claude Code, OpenCode CLI, Cursor, and Cline.

---

## 🚀 Quickstart & Installation

### Option 1: 1-Click Automated Setup (Windows)

Open PowerShell in your project directory:

```powershell
# Installs Python venv, core packages, and runs diagnostic self-tests
.\install_document_os.ps1

# To also deploy globally across all Antigravity projects:
.\install_document_os.ps1 -DeployGlobal
```

### Option 2: Linux / macOS Setup

```bash
chmod +x install_document_os.sh
./install_document_os.sh
```

### Option 3: Export to Claude Code or OpenCode

```powershell
.\export_cross_harness.ps1 -Target ClaudeCode
.\export_cross_harness.ps1 -Target OpenCode
```

---

## 🛠️ CLI Helper Commands

Document OS provides battle-tested CLI tools ready for agents and humans alike:

```bash
# 1. Triage any document format
python .agents/plugins/document-os/scripts/inspect_doc.py report.pdf

# 2. Extract tables into clean Markdown
python .agents/plugins/document-os/scripts/extract_doc.py financial_model.xlsx --type tables

# 3. Headless cross-format conversion
python .agents/plugins/document-os/scripts/convert_doc.py pitch.pptx pitch.pdf

# 4. Render pages/slides to PNG for visual QA
python .agents/plugins/document-os/scripts/render_doc.py pitch.pdf --outdir ./previews

# 5. Extract text from scanned images/PDFs with adaptive OCR
python .agents/plugins/document-os/scripts/ocr_doc.py receipt.png --output receipt_text.txt

# 6. Validate document integrity & scan formula errors
python .agents/plugins/document-os/scripts/qa_doc.py final_budget.xlsx
```

---

## 📖 Dogfooded Official Guide

We don't just talk about document fidelity; we prove it. The complete 13-page **Antigravity Document OS Comprehensive User Guide v3.0** was generated using our professional PDF engine with embedded Google Fonts (Playfair Display + Source Sans 3), brand-consistent styling, and KDP-quality formatting.

👉 **[Download the Official PDF User Guide v3.0](docs/Antigravity_Document_OS_Comprehensive_Guide_v3.pdf)**

### Document Generation Engines

- **ReportLab** (Primary): Precision PDF generation with embedded fonts, custom layouts, and print-ready output. Used for the v3 guide.
- **WeasyPrint** (Secondary): CSS Paged Media engine for HTML→PDF conversion. Requires GTK3 runtime on Windows. Falls back to ReportLab if unavailable.

---

## 🎨 Brand Identity System

Document OS v3.0 includes a built-in **Brand Identity Skill** that enforces consistent visual standards:

- **Colors**: Royal Blue (`#1A3A8F`), Golden Yellow (`#FFC107`), Deep Navy (`#0D1B4C`)
- **Fonts**: Playfair Display (headings), Source Sans 3 (body), JetBrains Mono (code)
- **Page Layout**: Amazon KDP-compliant margins and chapter formatting
- **Design Tokens**: Machine-readable JSON at `.agents/skills/brand-identity/resources/brand-tokens.json`

---

## 🤝 Community & Support

- ⭐ **Star this repository** if you believe AI agents deserve reliable document tools.
- 🍴 **Fork and contribute** new format specialists and validation routines (see [CONTRIBUTING.md](CONTRIBUTING.md)).
- ☕ **Support Development**: If this project saved your spreadsheets or presentations, consider [Buying Me a Coffee](https://www.buymeacoffee.com/ekpootu) to fuel ongoing maintenance.

---

## 👤 Author

**[Ekpo Otu, Ph.D.](https://linktr.ee/ekpootu)** — Computer Professional, Full Stack Developer, Researcher, Author & Lecturer.

- 🔗 [Linktree](https://linktr.ee/ekpootu) • 💻 [GitHub](https://github.com/ekpootu) • ☕ [Buy Me a Coffee](https://www.buymeacoffee.com/ekpootu)
