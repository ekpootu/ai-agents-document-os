---
name: brand-identity
description: >-
  Enforces consistent brand colors, typography, and page formatting whenever
  creating, updating, or designing documents (PDF, DOCX, PPTX, XLSX) or
  web pages. Automatically loads the brand color palette, professional font
  pairings, and Amazon KDP-ready page layout standards. MUST be activated
  for any document generation, web design, or visual output task.
---

# Brand Identity Design System

> **MANDATORY**: Activate this skill whenever you create, modify, style, or design
> any document (PDF, DOCX, PPTX) or web page. All visual output must conform to
> these brand tokens.

---

## 1. Brand Color Palette

The following colors are extracted from the project's brand reference images
(`brand-color1.png`, `brand-color2.jpeg`, `brand-color3.jpg`) and must be used
consistently across all outputs.

### Primary Colors

| Token | Name | Hex | RGB | Usage |
|:------|:-----|:----|:----|:------|
| `--color-primary` | Royal Blue | `#1A3A8F` | `rgb(26, 58, 143)` | Headers, hero backgrounds, sidebar accents, primary buttons |
| `--color-accent` | Golden Yellow | `#FFC107` | `rgb(255, 193, 7)` | CTAs, highlights, callout badges, star icons, chapter numbers |
| `--color-dark` | Deep Navy | `#0D1B4C` | `rgb(13, 27, 76)` | Dark surfaces, body text on light backgrounds, footer backgrounds |

### Neutral Colors

| Token | Name | Hex | RGB | Usage |
|:------|:-----|:----|:----|:------|
| `--color-white` | White | `#FFFFFF` | `rgb(255, 255, 255)` | Page backgrounds, reverse text on dark surfaces |
| `--color-bg-light` | Soft White | `#F8F9FA` | `rgb(248, 249, 250)` | Alternating table rows, light section backgrounds |
| `--color-bg-panel` | Light Gray | `#F0F2F5` | `rgb(240, 242, 245)` | Callout boxes, code block backgrounds |
| `--color-border` | Border Gray | `#DEE2E6` | `rgb(222, 226, 230)` | Table borders, section dividers, card outlines |
| `--color-muted` | Muted Text | `#6B7280` | `rgb(107, 114, 128)` | Captions, footnotes, secondary body text |
| `--color-body` | Body Text | `#212529` | `rgb(33, 37, 41)` | Primary body text on white backgrounds |

### Semantic Colors

| Token | Name | Hex | Usage |
|:------|:-----|:----|:------|
| `--color-success` | Emerald | `#10B981` | QA pass indicators, success messages |
| `--color-danger` | Coral Red | `#EF4444` | Error states, danger callouts, QA failures |
| `--color-info` | Sky Blue | `#0EA5E9` | Informational callouts, tip boxes |
| `--color-warning` | Amber | `#F59E0B` | Warning callouts, caution indicators |

### Gradient Definitions

| Token | CSS Value | Usage |
|:------|:----------|:------|
| `--gradient-hero` | `linear-gradient(135deg, #1A3A8F 0%, #0D1B4C 100%)` | Hero sections, title page backgrounds |
| `--gradient-accent` | `linear-gradient(135deg, #FFC107 0%, #FF9800 100%)` | CTA buttons, highlight badges |
| `--gradient-card` | `linear-gradient(180deg, #FFFFFF 0%, #F8F9FA 100%)` | Card backgrounds, elevated surfaces |

---

## 2. Typography System

Font pairings extracted from `font-combo1.jpg` reference. These combinations
follow professional publishing standards suitable for Amazon KDP interiors.

### Font Stack

| Role | Primary Font | Weight(s) | Fallback Stack |
|:-----|:-------------|:----------|:---------------|
| **Display / Titles** | Playfair Display | Bold (700), ExtraBold (800) | Georgia, "Times New Roman", serif |
| **Body Text** | Source Sans 3 (Source Sans Pro) | Regular (400), SemiBold (600) | "Helvetica Neue", Helvetica, Arial, sans-serif |
| **Code / Monospace** | JetBrains Mono | Regular (400), Medium (500) | "Fira Code", "Cascadia Code", Consolas, monospace |
| **Captions / Small** | Source Sans 3 | Regular (400), Italic | Same as body |

### Typography Scale

| Element | Font | Size | Weight | Line Height | Letter Spacing |
|:--------|:-----|:-----|:-------|:------------|:---------------|
| Document Title (Cover) | Playfair Display | 32pt / 2.5rem | 800 | 1.2 | -0.02em |
| Chapter Title | Playfair Display | 24pt / 1.75rem | 700 | 1.25 | -0.015em |
| Section Heading (H2) | Source Sans 3 | 16pt / 1.25rem | 700 | 1.3 | 0 |
| Subsection (H3) | Source Sans 3 | 13pt / 1rem | 600 | 1.4 | 0 |
| Body Text | Source Sans 3 | 11pt / 0.85rem | 400 | 1.6 | 0.01em |
| Captions & Footnotes | Source Sans 3 | 9pt / 0.7rem | 400 | 1.4 | 0.02em |
| Code Blocks | JetBrains Mono | 9pt / 0.7rem | 400 | 1.5 | 0 |

### Google Fonts Import (Web)

```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap');
```

### Font Embedding (PDF / Print)

For PDF generation, download and embed font files locally:
- Playfair Display: `resources/fonts/PlayfairDisplay-Bold.ttf`, `PlayfairDisplay-ExtraBold.ttf`
- Source Sans 3: `resources/fonts/SourceSans3-Regular.ttf`, `SourceSans3-SemiBold.ttf`, `SourceSans3-Bold.ttf`, `SourceSans3-Italic.ttf`
- JetBrains Mono: `resources/fonts/JetBrainsMono-Regular.ttf`, `JetBrainsMono-Medium.ttf`

---

## 3. Page Layout Standards (Print / KDP)

These standards produce Amazon KDP-compliant interior formatting suitable for
trade paperback and ebook publishing.

### Page Dimensions

| Format | Width | Height | Use Case |
|:-------|:------|:-------|:---------|
| **Trade Paperback** | 6 in | 9 in | Standard book interior (KDP recommended) |
| **US Letter Guide** | 8.5 in | 11 in | Technical manuals, reports, user guides |
| **A4 International** | 210mm | 297mm | EU/international reports |

### Margins (Trade Paperback 6×9)

| Edge | Measurement | Notes |
|:-----|:------------|:------|
| Top | 0.75 in | Includes running header space |
| Bottom | 0.75 in | Includes page number space |
| Outside | 0.625 in | Outer edge (right on recto, left on verso) |
| Inside (Gutter) | 0.875 in | Binding edge — extra space for spine |

### Margins (US Letter 8.5×11)

| Edge | Measurement |
|:-----|:------------|
| Top | 0.75 in |
| Bottom | 0.75 in |
| Left | 0.75 in |
| Right | 0.75 in |

### Chapter Opener Layout

1. Start each chapter on a recto (right/odd) page
2. Leave ~3 inches from the top of the page before the chapter label
3. Chapter label: Small caps, tracking +0.1em (e.g., "CHAPTER 1:")
4. Chapter title: Playfair Display Bold, 24pt, centered
5. Insert a thin decorative rule (1pt, brand accent color) below the title
6. Begin body text after 24pt vertical space

### Running Headers & Footers

- **Header** (pages 2+): Document/Book title on left, Chapter title on right — Source Sans 3, 8pt, muted color
- **Footer**: Centered page number — Source Sans 3, 9pt
- **Title page and chapter openers**: No headers or footers

### Paragraph Formatting

- First paragraph after heading: No indent
- Subsequent paragraphs: 0.3in first-line indent OR 12pt space-between (choose one style per document, do not mix)
- Justification: Full justify for body text, left-align for code blocks
- Orphan/Widow control: Minimum 2 lines at top/bottom of page

---

## 4. Document Component Styles

### Callout Boxes

```
┌──────────────────────────────────────────┐
│ 🔵 PRO TIP                               │
│ Left border: 4px solid --color-primary    │
│ Background: --color-bg-panel              │
│ Font: Source Sans 3 Italic, 10pt          │
│ Padding: 12px 16px                        │
└──────────────────────────────────────────┘
```

Types and colors:
- **Pro Tip / Note**: Left border `--color-primary` (#1A3A8F), bg `#EBF0FA`
- **Warning / Caution**: Left border `--color-warning` (#F59E0B), bg `#FFF8E1`
- **Danger / Critical**: Left border `--color-danger` (#EF4444), bg `#FEF2F2`
- **Success / Result**: Left border `--color-success` (#10B981), bg `#ECFDF5`

### Tables

- Header row: Background `--color-primary` (#1A3A8F), text white, Source Sans 3 SemiBold
- Body rows: Alternating white / `--color-bg-light` (#F8F9FA)
- Borders: 0.5pt `--color-border` (#DEE2E6)
- Cell padding: 8px horizontal, 6px vertical
- Text: Source Sans 3 Regular, 9pt

### Code Blocks

- Background: `#1E293B` (dark slate) for dark-theme code blocks; `#F8F9FA` for inline
- Font: JetBrains Mono, 9pt
- Border-radius: 6px
- Padding: 16px
- Syntax: Use brand accent color for keywords

---

## 5. Web Design System Tokens

When building or updating web pages, use these CSS custom properties:

```css
:root {
  /* Brand Colors */
  --color-primary: #1A3A8F;
  --color-primary-light: #2450B8;
  --color-primary-dark: #0D1B4C;
  --color-accent: #FFC107;
  --color-accent-hover: #FFD54F;

  /* Neutrals */
  --color-white: #FFFFFF;
  --color-bg-light: #F8F9FA;
  --color-bg-panel: #F0F2F5;
  --color-border: #DEE2E6;
  --color-muted: #6B7280;
  --color-body: #212529;

  /* Semantic */
  --color-success: #10B981;
  --color-danger: #EF4444;
  --color-info: #0EA5E9;
  --color-warning: #F59E0B;

  /* Gradients */
  --gradient-hero: linear-gradient(135deg, #1A3A8F 0%, #0D1B4C 100%);
  --gradient-accent: linear-gradient(135deg, #FFC107 0%, #FF9800 100%);

  /* Typography */
  --font-display: 'Playfair Display', Georgia, serif;
  --font-body: 'Source Sans 3', 'Helvetica Neue', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Spacing & Radius */
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-xl: 28px;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(13, 27, 76, 0.1);
  --shadow-md: 0 4px 12px rgba(13, 27, 76, 0.12);
  --shadow-lg: 0 10px 30px rgba(13, 27, 76, 0.15);
  --shadow-glow: 0 0 25px rgba(26, 58, 143, 0.25);
}
```

---

## 6. Author & Attribution

| Field | Value |
|:------|:------|
| **Author Name** | [Ekpo Otu, Ph.D.](https://linktr.ee/ekpootu) |
| **GitHub** | [github.com/ekpootu](https://github.com/ekpootu) |
| **Buy Me a Coffee** | [buymeacoffee.com/ekpootu](https://www.buymeacoffee.com/ekpootu) |
| **Linktree** | [linktr.ee/ekpootu](https://linktr.ee/ekpootu) |

Include these in document footers, "About the Author" sections, and web page
footer/support sections.

---

## Quick Reference: When to Use This Skill

| Task | Activate Brand Identity? |
|:-----|:------------------------|
| Creating a PDF document | ✅ YES — apply colors, fonts, page layout |
| Generating a DOCX/PPTX | ✅ YES — apply colors, fonts, styling |
| Building or updating a web page | ✅ YES — apply CSS tokens and font imports |
| Writing plain Markdown | ❌ No — Markdown has no visual styling |
| Reading/inspecting a document | ❌ No — read-only operations |
| Running QA validation | ❌ No — validation only |
