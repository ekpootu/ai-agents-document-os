---
name: flipbook-generator
description: >-
  Autonomous 3D digital flipbook generator. Transforms multi-page documents
  (PDF, DOCX, PPTX) into publication-grade, interactive HTML5 3D flipbooks with
  realistic page-turning curl physics, dual-page spreads, synthesized page-turn
  audio, thumbnail scrubbers, and zero-dependency offline local execution.
---

# Flip Book Generator Skill

The `flipbook-generator` skill empowers AI agents to convert static, multi-page documents (PDFs, presentations, technical manuals, and whitepapers) into interactive, digital 3D flipbooks.

---

## 1. When to Activate This Skill

Activate this skill whenever the user asks to:
- *"Create a flipbook from this PDF / document"*
- *"Convert this report into a digital book flip viewer"*
- *"Show a realistic 3D page-turning preview of my publication"*
- *"Generate an interactive flip-through video or web book"*

---

## 2. Core Architectural Features

1. **Dual-Page Spread & Authentic Spine Geometry**:
   - Accurately renders pages side-by-side on desktop displays (recto/verso layout) and smoothly folds into a single page on mobile screens.
   - Adds realistic 3D perspective, spine shading, and paper curl gradients.
2. **Web Audio Synthesized Page Turn Sound**:
   - Uses the browser's native Web Audio API to synthesize a soft, realistic paper-turn sound on every flip without requiring external `.mp3` or `.wav` media assets.
3. **Zero-Cloud & Zero-Dependency Offline Execution**:
   - The compiled `index.html` operates entirely locally via `file:///` without requiring npm, node, local web servers, or external CDNs.
4. **Keyboard & Scrub Bar Controls**:
   - Supports `ArrowLeft` / `ArrowRight`, `Spacebar`, `Home`, `End`, and an interactive range slider for quick jumping across hundreds of pages.

---

## 3. How to Execute

### CLI Command

```bash
# Basic generation
python .agents/plugins/document-os/skills/flipbook-generator/scripts/build_flipbook.py <path-to-pdf>

# Customized generation with custom title, author, and output folder
python .agents/plugins/document-os/skills/flipbook-generator/scripts/build_flipbook.py <path-to-pdf> \
  --outdir scratch/flipbook \
  --title "AI Agents Document OS Guide v6.0" \
  --author "Ekpo Otu, Ph.D." \
  --dpi 150
```

### Parameters

| Argument | Description | Default |
|:---|:---|:---|
| `pdf_path` | Absolute or relative path to the input PDF file. | *Required* |
| `--outdir` | Destination directory where `index.html` and `pages/` are created. | `scratch/flipbook` |
| `--title` | Human-readable title displayed in the flipbook header. | `AI Agents Document OS Guide` |
| `--author` | Author or organization attribution string. | `Ekpo Otu, Ph.D.` |
| `--dpi` | Rasterization resolution for page images. | `150` |

---

## 4. Multi-Modal Document Workflow

If starting with an editable format (`.docx`, `.pptx`, `.xlsx`, or Markdown):
1. **Convert to PDF First**:
   ```bash
   python .agents/plugins/document-os/scripts/convert_doc.py input.pptx temp.pdf
   ```
2. **Generate the Flip Book**:
   ```bash
   python .agents/plugins/document-os/skills/flipbook-generator/scripts/build_flipbook.py temp.pdf --outdir previews/presentation_flipbook
   ```
3. **Clean Temporary Files**:
   ```bash
   python .agents/plugins/document-os/scripts/clean_workspace.py --previews
   ```

---

## 5. Artifacts and Directory Layout

A generated flipbook produces the following directory tree:

```
target_directory/
├── index.html       # Standalone interactive 3D viewer
└── pages/           # High-resolution rasterized page images
    ├── page_001.png # Front cover
    ├── page_002.png # Inside front / TOC
    └── ...
```
