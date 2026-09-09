# Image & OCR Processing Protocol

Working with raster documents (`.png`, `.jpg`, `.jpeg`, `.tiff`, `.webp`, `.bmp`) and scanned PDFs requires a dual strategy: **Multimodal Vision** for semantic reasoning, and **Tesseract OCR** for deterministic text extraction.

## 1. Dual Strategy: When to Use What

| Scenario | Recommended Approach | Tool |
| :--- | :--- | :--- |
| **Document Understanding** (Understanding receipts, diagrams, handwritten charts, layouts) | Model Vision | Read file directly via agent multimodal capabilities |
| **Deterministic Text Extraction** (Verbatim copying of printed text, serial numbers, contracts) | Local OCR Engine | `ocr_doc.py` (Tesseract) |
| **Image Preprocessing** (Low contrast, skewed scans, noisy backgrounds) | Local Image Processing | `Pillow` / `OpenCV` |

## 2. OCR Preprocessing Pipeline
Raw scans often produce noisy OCR results. `ocr_doc.py` applies automated preprocessing:
1. **Grayscale Conversion**: Eliminates color artifacts.
2. **Otsu Binarization / Thresholding**: Converts subtle grays into crisp black text on pure white background.
3. **Deskewing**: Corrects tilted document angles.
4. **PSM (Page Segmentation Mode) Selection**:
   - PSM 3: Fully automatic page segmentation (default).
   - PSM 6: Assume a single uniform block of text.
   - PSM 11: Sparse text (finds as much text as possible in no particular order).
