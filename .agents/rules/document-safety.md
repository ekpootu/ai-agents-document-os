# Document Safety, Immutability & Permission Guidelines

This rule enforces permission boundaries and data protection when working with documents.

## Permission Classification

### 1. Automatically Allowed (Read-Only & Triage)
- Running `inspect_doc.py` to inspect metadata, page count, and structure.
- Running `extract_doc.py` to extract text, tables, and images to stdout or temporary analysis artifacts.
- Running `render_doc.py` to generate visual preview thumbnails into temporary artifact directories.
- Reading and verifying checksums or integrity of any document.

### 2. Requires Explicit Confirmation (Destructive & Overwriting Actions)
- Deleting any existing document file.
- Overwriting an existing document file in-place without generating a versioned copy (`_v2`, `_processed`).
- Batch conversions or mass transformations affecting more than 5 documents simultaneously.
- Modifying system-level configuration or software installations outside of the designated `.venv-docos` environment.

## Spreadsheet Formula Protection Policy
- When editing spreadsheets (`.xlsx`), formulas MUST NEVER be converted to plain values unless the user explicitly requested "paste as values" or "strip formulas".
- When updating cells referenced by other formulas, the agent must check downstream formula dependencies using `inspect_doc.py --formulas`.

## Presentation Safety Policy
- When editing or generating PowerPoint decks (`.pptx`), avoid placing unconstrained text inside fixed bounding boxes that cause text collision or truncation.
- Always run visual validation via `render_doc.py` on the first and last slides plus any modified slides.
