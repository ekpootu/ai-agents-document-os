# Universal Agent Instructions: AI Agents Document Operating System (Document OS)

This repository contains the **Universal Document Operating System** for AI agents (Antigravity, Claude Code, OpenCode CLI, Cursor, and Cline).

## Quick Agent Reference

When the user asks you to read, analyze, summarize, convert, generate, or validate any document (`.pdf`, `.docx`, `.xlsx`, `.pptx`, `.md`, `.csv`, `.json`, `.png`, `.jpg`):

1. **Activate the Master Router Skill**:
   - Locate instructions in `.agents/plugins/document-os/skills/document-router/SKILL.md` or `.agents/skills/document-router/SKILL.md`.
2. **Execute via Pre-Built Deterministic Scripts**:
   - Inspect document structure:
     `python .agents/plugins/document-os/scripts/inspect_doc.py <file>`
   - Extract text, tables, or images:
     `python .agents/plugins/document-os/scripts/extract_doc.py <file> [--format text|tables|images|markdown]`
   - Headless conversion (PDF/DOCX/PPTX/XLSX/MD):
     `python .agents/plugins/document-os/scripts/convert_doc.py <input_file> <output_file>`
   - Render pages/slides to PNG for visual QA:
     `python .agents/plugins/document-os/scripts/render_doc.py <file> <output_dir>`
   - Validate integrity and check for errors:
     `python .agents/plugins/document-os/scripts/qa_doc.py <file>`
3. **Safety Guarantee**:
   - Always preserve original files. Output modifications to new files or distinct versions unless an in-place edit is explicitly requested by the user.
4. **Brand Identity & Professional Styling**:
   - When creating, designing, or updating any document or web page, activate the `brand-identity` skill at `.agents/skills/brand-identity/SKILL.md`.
   - For professional PDF generation, use the builder script:
     `python .agents/plugins/document-os/scripts/build_professional_pdf.py [output_path]`
   - Design tokens are available at `.agents/skills/brand-identity/resources/brand-tokens.json`.
5. **Interactive 3D Flip Book Generation**:
   - To transform any PDF or presentation into an interactive, digital 3D flipbook with realistic page curl physics, activate the `flipbook-generator` skill at `.agents/plugins/document-os/skills/flipbook-generator/SKILL.md`.
   - Execute: `python .agents/plugins/document-os/scripts/build_flipbook.py <pdf_file> [--outdir <dir>]`
6. **Multimodal Media Sourcing & AI Image Generation**:
   - Enhance documents with visual assets using state-of-the-art AI image models (such as Nanobanana Pro or Imagen 3) or source royalty-free photography and graphics from public domain repositories (Pexels, Pixabay).
7. **Tone of Voice & Writing Clarity**:
   - Communicate in clear, friendly, and accessible English. Break down complex concepts into simple, intuitive explanations without unnecessary technical jargon.
8. **Publishing Proportions & The Golden Ratio**:
   - Utilize the Golden Ratio ($\phi \approx 1.618:1$, $6.0" \times 9.71"$) or the 6" x 9" Universal Trade Standard with Tschichold's Golden Canon of Page Construction to guarantee balanced, readable page geometry.

