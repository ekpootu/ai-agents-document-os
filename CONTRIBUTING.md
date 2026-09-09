# Contributing to Antigravity Document OS

We are on a mission to bring deterministic engineering standards to AI agent document operations. We welcome contributions from developers, researchers, and agentic workflows enthusiasts.

## How You Can Contribute

1. **Add Format Specialists**:
   - Have expertise in specialized file formats (e.g., Apple Pages/Keynote, LaTeX, ePub, CAD, RTF, HWP/HWPX)?
   - Submit a reference protocol under `.agents/plugins/document-os/skills/document-router/references/` and integrate it into `inspect_doc.py` and `qa_doc.py`.

2. **Enhance QA Validation**:
   - Improve automated detection of broken XML namespaces, font fallbacks, table splits, or formula errors in `qa_doc.py`.

3. **Cross-Harness Adapters**:
   - Extend `export_cross_harness.ps1` and shell equivalents to support upcoming AI agent environments.

## Development Workflow

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
    git clone https://github.com/ekpootu/ai-agents-document-os.git
    cd ai-agents-document-os
   ```
3. Run the installer to configure your environment:
   ```powershell
   .\install_document_os.ps1 -SkipWinget
   ```
4. Make your changes and run self-tests:
   ```powershell
   .\.venv-docos\Scripts\python .agents\plugins\document-os\scripts\qa_doc.py <test_sample>
   ```
5. Commit with descriptive commit messages and open a Pull Request.

## Template & Styling Contributions

- **WeasyPrint Templates**: Add new CSS Paged Media templates under `.agents/plugins/document-os/scripts/templates/`. All templates must use the brand tokens from `.agents/skills/brand-identity/resources/brand-tokens.json`.
- **ReportLab Styles**: Extend `build_professional_pdf.py` with new document layouts (e.g., invoices, research papers, slide handouts).

---

Thank you for helping eliminate document hallucinations in autonomous AI agents!

**Created by [Ekpo Otu, Ph.D.](https://linktr.ee/ekpootu)** • [Buy Me a Coffee ☕](https://www.buymeacoffee.com/ekpootu)
