# Flip Book Generator Examples

This folder demonstrates practical agent invocations and workflow patterns for generating digital 3D flipbooks.

## Example 1: Creating a Showcase Flipbook from a Technical Whitepaper

```bash
python .agents/plugins/document-os/skills/flipbook-generator/scripts/build_flipbook.py \
  docs/AI_Agents_Document_OS_Comprehensive_Guide_v6.pdf \
  --outdir scratch/flipbook_guide_v6 \
  --title "AI Agents Document OS Guide v6.0" \
  --author "Ekpo Otu, Ph.D." \
  --dpi 150
```

## Example 2: Creating a Client Slide Deck Flipbook

When an executive asks to review a slide deck without installing PowerPoint or opening full-screen slide shows:

```bash
# 1. Convert presentation to temporary PDF
python .agents/plugins/document-os/scripts/convert_doc.py quarterly_briefing.pptx temp_briefing.pdf

# 2. Build interactive flipbook
python .agents/plugins/document-os/skills/flipbook-generator/scripts/build_flipbook.py temp_briefing.pdf \
  --outdir previews/quarterly_briefing_flipbook \
  --title "Q3 Executive Briefing Deck"
```
