# Extra Assets & Extraction Workspace — Document OS

This directory serves as the designated workspace for extracted media, document figures, and auxiliary assets.

## Directory Structure

- `extracted_assets/`: The default output directory for visual and raster media extracted from multi-modal documents.

## Generating Extracted Assets

When working with documents containing embedded illustrations, vector charts, or photographic figures, use the core extraction engine to populate this directory:

```bash
# Extract all images from a PDF or Word document into extra/extracted_assets/
python .agents/plugins/document-os/scripts/extract_doc.py <path-to-document> --format images --output extra/extracted_assets/
```

## Privacy & Version Control

All extracted media files (`.png`, `.jpg`, `.jpeg`, `.svg`, `.webp`) placed in `extracted_assets/` are git-ignored by default. This ensures that:
1. Confidential document figures, corporate charts, and private image data remain strictly local to your machine.
2. The Git repository remains lightweight and free of binary media bloat.
3. Every developer or agent can generate their own clean extraction assets on demand.
