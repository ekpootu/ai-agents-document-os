# PPTX Processing Protocol

PowerPoint (`.pptx`) presentations are visual documents defined by slide masters, layout containers, typography, shape geometry, and color palettes.

## 1. Structural Awareness
- **Slide Dimensions**: Modern decks use widescreen (16:9, `13.333 x 7.5 inches`). Legacy decks use standard (4:3, `10 x 7.5 inches`). Always check dimensions before placing elements.
- **Slide Layouts**: Inherit from slide masters (e.g. Title Slide, Title & Content, Two Content, Blank). Use existing layouts rather than manually drawing text frames when possible.
- **Speaker Notes**: Extract speaker notes as valuable context; ensure they are preserved during updates.

## 2. Text Frame & Overflow Control
The most common agent failure in `.pptx` is text overflowing slide margins or colliding with other boxes.
- Enforce strict character limits for bullet points.
- Enable word wrap (`text_frame.word_wrap = True`).
- Keep font sizes proportional (Title: 32-40pt, Subtitle: 20-24pt, Body: 14-18pt).

## 3. Visual Verification Protocol
1. Export presentation to PDF via headless LibreOffice (`convert_doc.py deck.pptx deck.pdf`).
2. Render slide pages to PNGs via `render_doc.py deck.pdf ./previews`.
3. Visually inspect the rendered slide images to verify layout balance, alignment, and absence of text overflow.
