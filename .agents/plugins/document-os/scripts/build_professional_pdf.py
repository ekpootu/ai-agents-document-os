#!/usr/bin/env python3
"""
build_professional_pdf.py — AI Agents Document OS Professional PDF Builder (v4)

Generates an Amazon KDP-standard book-quality PDF using ReportLab with:
- 1.6:1 height-to-width ratio (6.0 in x 9.6 in)
- Embedded Google Fonts (Playfair Display + Source Sans 3)
- Clickable Table of Contents with true destination anchors
- Brand color palette (Royal Blue #1A3A8F, Golden Yellow #FFC107, Deep Navy #0D1B4C)
- Reduced white space and tight content flow
- Running headers/footers with dynamic page numbering
- Author: Ekpo Otu, Ph.D. — https://linktr.ee/ekpootu
"""

import sys
import json
import urllib.request
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Image
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# Page Dimensions: Exact 1.6:1 Height-to-Width Ratio
# ---------------------------------------------------------------------------
PAGE_WIDTH = 6.0 * inch
PAGE_HEIGHT = 9.6 * inch  # 6.0 * 1.6 = 9.6
PAGE_SIZE = (PAGE_WIDTH, PAGE_HEIGHT)
MARGIN = 0.55 * inch
PRINTABLE_WIDTH = PAGE_WIDTH - 2 * MARGIN  # 4.9 inches

# ---------------------------------------------------------------------------
# Brand Tokens
# ---------------------------------------------------------------------------
BRAND = {
    "primary": "#1A3A8F",
    "primary_dark": "#0D1B4C",
    "accent": "#FFC107",
    "accent_dark": "#FF9800",
    "white": "#FFFFFF",
    "bg_light": "#F8F9FA",
    "bg_panel": "#F0F2F5",
    "border": "#DEE2E6",
    "muted": "#6B7280",
    "body": "#212529",
    "success": "#10B981",
    "danger": "#EF4444",
    "info": "#0EA5E9",
    "warning": "#F59E0B",
    "callout_tip_bg": "#EBF0FA",
    "callout_warn_bg": "#FFF8E1",
    "callout_danger_bg": "#FEF2F2",
    "callout_success_bg": "#ECFDF5",
}

C = {k: colors.HexColor(v) for k, v in BRAND.items()}

# ---------------------------------------------------------------------------
# Font Registration — Google Fonts with Fallback
# ---------------------------------------------------------------------------
FONT_DIR = Path(__file__).parent / "templates" / "fonts"

GOOGLE_FONT_URLS = {
    "PlayfairDisplay-Bold": "https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf",
    "SourceSans3-Regular": "https://raw.githubusercontent.com/google/fonts/main/ofl/sourcesans3/SourceSans3%5Bwght%5D.ttf",
}

def _download_font(name: str, url: str) -> Path | None:
    """Download a font file if not already cached."""
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    target = FONT_DIR / f"{name}.ttf"
    if target.exists():
        return target
    try:
        print(f"  Downloading font: {name}...")
        urllib.request.urlretrieve(url, str(target))
        return target
    except Exception as e:
        print(f"  Warning: Could not download {name}: {e}")
        return None

def register_fonts():
    """Register Google Fonts or fall back to built-in Helvetica."""
    fonts_available = True
    for name, url in GOOGLE_FONT_URLS.items():
        p = _download_font(name, url)
        if not p or not p.exists():
            fonts_available = False

    if fonts_available:
        try:
            display_path = FONT_DIR / "PlayfairDisplay-Bold.ttf"
            body_path = FONT_DIR / "SourceSans3-Regular.ttf"

            pdfmetrics.registerFont(TTFont("PlayfairDisplay-Bold", str(display_path)))
            pdfmetrics.registerFont(TTFont("SourceSans3-Regular", str(body_path)))

            pdfmetrics.registerFontFamily(
                "SourceSans3",
                normal="SourceSans3-Regular",
                bold="SourceSans3-Regular",
                italic="SourceSans3-Regular",
                boldItalic="SourceSans3-Regular",
            )
            pdfmetrics.registerFontFamily(
                "PlayfairDisplay",
                normal="PlayfairDisplay-Bold",
                bold="PlayfairDisplay-Bold",
                italic="PlayfairDisplay-Bold",
                boldItalic="PlayfairDisplay-Bold",
            )
            return {
                "display": "PlayfairDisplay-Bold",
                "display_xl": "PlayfairDisplay-Bold",
                "body": "SourceSans3-Regular",
                "body_bold": "SourceSans3-Regular",
                "body_semi": "SourceSans3-Regular",
                "mono": "Courier",
            }
        except Exception as e:
            print(f"  Font registration warning: {e}, using Helvetica fallback")

    return {
        "display": "Helvetica-Bold",
        "display_xl": "Helvetica-Bold",
        "body": "Helvetica",
        "body_bold": "Helvetica-Bold",
        "body_semi": "Helvetica-Bold",
        "mono": "Courier",
    }

# ---------------------------------------------------------------------------
# Style Factory
# ---------------------------------------------------------------------------
def build_styles(fonts: dict) -> dict:
    """Create all paragraph styles calibrated for 6.0" x 9.6" compact page format."""
    base = getSampleStyleSheet()
    s = {}

    s["doc_title"] = ParagraphStyle(
        "DocTitle", parent=base["Heading1"],
        fontName=fonts["display_xl"], fontSize=22, leading=26,
        textColor=C["primary_dark"], alignment=TA_CENTER,
        spaceAfter=4,
    )
    s["doc_subtitle"] = ParagraphStyle(
        "DocSubtitle", parent=base["Normal"],
        fontName=fonts["body"], fontSize=10.5, leading=14,
        textColor=C["primary"], alignment=TA_CENTER,
        spaceAfter=8,
    )
    s["doc_version"] = ParagraphStyle(
        "DocVersion", parent=base["Normal"],
        fontName=fonts["body_semi"], fontSize=8.5, leading=12,
        textColor=C["primary_dark"], alignment=TA_CENTER,
        spaceBefore=2, spaceAfter=2,
    )
    s["doc_author"] = ParagraphStyle(
        "DocAuthor", parent=base["Normal"],
        fontName=fonts["body"], fontSize=9.5, leading=13,
        textColor=C["muted"], alignment=TA_CENTER,
        spaceBefore=10,
    )

    s["chapter_label"] = ParagraphStyle(
        "ChapterLabel", parent=base["Normal"],
        fontName=fonts["body_semi"], fontSize=8.5, leading=12,
        textColor=C["primary"], alignment=TA_CENTER,
        spaceBefore=0, spaceAfter=2,
    )
    s["chapter_title"] = ParagraphStyle(
        "ChapterTitle", parent=base["Heading1"],
        fontName=fonts["display"], fontSize=16, leading=20,
        textColor=C["primary_dark"], alignment=TA_CENTER,
        spaceBefore=0, spaceAfter=6,
    )

    s["h1"] = ParagraphStyle(
        "H1Pro", parent=base["Heading1"],
        fontName=fonts["display"], fontSize=14, leading=18,
        textColor=C["primary_dark"],
        spaceBefore=10, spaceAfter=4, keepWithNext=True,
    )
    s["h2"] = ParagraphStyle(
        "H2Pro", parent=base["Heading2"],
        fontName=fonts["body_bold"], fontSize=11, leading=15,
        textColor=C["primary"],
        spaceBefore=8, spaceAfter=3, keepWithNext=True,
    )
    s["h3"] = ParagraphStyle(
        "H3Pro", parent=base["Heading3"],
        fontName=fonts["body_bold"], fontSize=9.5, leading=13,
        textColor=C["body"],
        spaceBefore=6, spaceAfter=2, keepWithNext=True,
    )

    s["body"] = ParagraphStyle(
        "BodyPro", parent=base["Normal"],
        fontName=fonts["body"], fontSize=8.5, leading=12.5,
        textColor=C["body"], alignment=TA_LEFT,
        spaceBefore=2, spaceAfter=4,
    )
    s["body_center"] = ParagraphStyle(
        "BodyCenter", parent=s["body"], alignment=TA_CENTER
    )
    s["body_bold"] = ParagraphStyle(
        "BodyBold", parent=s["body"], fontName=fonts["body_bold"]
    )

    s["bullet"] = ParagraphStyle(
        "BulletPro", parent=s["body"],
        leftIndent=12, firstLineIndent=-8,
        spaceBefore=1, spaceAfter=2,
    )
    s["bullet_num"] = ParagraphStyle(
        "BulletNumPro", parent=s["body"],
        leftIndent=14, firstLineIndent=-10,
        spaceBefore=1, spaceAfter=2,
    )

    s["callout"] = ParagraphStyle(
        "CalloutPro", parent=base["Normal"],
        fontName=fonts["body"], fontSize=8, leading=11.5,
        textColor=C["body"], spaceBefore=0, spaceAfter=0,
    )
    s["callout_title"] = ParagraphStyle(
        "CalloutTitlePro", parent=base["Normal"],
        fontName=fonts["body_bold"], fontSize=8.5, leading=12,
        textColor=C["primary_dark"], spaceBefore=0, spaceAfter=2,
    )

    s["code"] = ParagraphStyle(
        "CodePro", parent=base["Code"],
        fontName=fonts["mono"], fontSize=7.5, leading=10.5,
        textColor=colors.HexColor("#1F2937"),
        spaceBefore=0, spaceAfter=0,
    )

    s["th"] = ParagraphStyle(
        "THPro", parent=base["Normal"],
        fontName=fonts["body_bold"], fontSize=7.5, leading=10.5,
        textColor=C["white"], alignment=TA_LEFT,
    )
    s["td"] = ParagraphStyle(
        "TDPro", parent=base["Normal"],
        fontName=fonts["body"], fontSize=7.5, leading=10.5,
        textColor=C["body"], alignment=TA_LEFT,
    )

    s["footer_meta"] = ParagraphStyle(
        "FooterMeta", parent=base["Normal"],
        fontName=fonts["body"], fontSize=7, leading=9.5,
        textColor=C["muted"], alignment=TA_CENTER,
    )

    return s

# ---------------------------------------------------------------------------
# Layout Helpers
# ---------------------------------------------------------------------------
def make_callout(text: str, title: str, styles: dict, variant: str = "tip") -> Table:
    """Create a compact branded callout box fitted to 4.9 inch printable width."""
    colors_map = {
        "tip":     (C["primary"],  C["callout_tip_bg"]),
        "warning": (C["warning"],  C["callout_warn_bg"]),
        "danger":  (C["danger"],   C["callout_danger_bg"]),
        "success": (C["success"],  C["callout_success_bg"]),
    }
    border_c, bg_c = colors_map.get(variant, colors_map["tip"])

    content = [
        Paragraph(f"<b>{title}</b>", styles["callout_title"]),
        Paragraph(text, styles["callout"]),
    ]
    t = Table([[content]], colWidths=[PRINTABLE_WIDTH])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_c),
        ("LINEBEFORE", (0, 0), (0, -1), 3.5, border_c),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0.5, C["border"]),
    ]))
    return t

def make_table(headers: list, rows: list, col_widths: list, styles: dict) -> Table:
    """Create a branded data table fitted to 4.9 inch printable width."""
    data = [[Paragraph(f"<b>{h}</b>", styles["th"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(cell), styles["td"]) for cell in row])

    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C["primary"]),
        ("TOPPADDING", (0, 0), (-1, 0), 4),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
        ("BACKGROUND", (0, 1), (-1, -1), C["white"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C["white"], C["bg_light"]]),
        ("GRID", (0, 0), (-1, -1), 0.5, C["border"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 1), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
    ]))
    return t

def accent_rule():
    return HRFlowable(
        width=PRINTABLE_WIDTH, thickness=1.5,
        color=colors.HexColor("#FFC107"),
        spaceAfter=6, spaceBefore=3,
    )

def thin_rule():
    return HRFlowable(
        width=PRINTABLE_WIDTH, thickness=0.4,
        color=C["border"],
        spaceAfter=4, spaceBefore=4,
    )

# ---------------------------------------------------------------------------
# Page Decoration Callbacks (Preserves Links & Anchors)
# ---------------------------------------------------------------------------
def make_page_decorators(fonts: dict):
    def draw_first_page(c: canvas.Canvas, doc):
        c.saveState()
        # Top accent bar
        c.setFillColor(colors.HexColor("#1A3A8F"))
        c.rect(0, PAGE_HEIGHT - 0.18 * inch, PAGE_WIDTH, 0.18 * inch, fill=True, stroke=False)
        # Bottom accent bar
        c.setFillColor(colors.HexColor("#FFC107"))
        c.rect(0, 0, PAGE_WIDTH, 0.12 * inch, fill=True, stroke=False)
        c.restoreState()

    def draw_later_pages(c: canvas.Canvas, doc):
        c.saveState()
        page_num = c.getPageNumber()
        body_font = fonts.get("body", "Helvetica")

        # Running header text & rule
        c.setFont(body_font, 7)
        c.setFillColor(colors.HexColor("#6B7280"))
        c.drawString(MARGIN, PAGE_HEIGHT - 0.38 * inch,
                     "AI Agents Document OS — Comprehensive User Guide v4.0")
        c.setStrokeColor(colors.HexColor("#DEE2E6"))
        c.setLineWidth(0.4)
        c.line(MARGIN, PAGE_HEIGHT - 0.44 * inch, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 0.44 * inch)

        # Running footer rule & text
        c.line(MARGIN, 0.50 * inch, PAGE_WIDTH - MARGIN, 0.50 * inch)

        c.setFont(body_font, 7.5)
        c.setFillColor(colors.HexColor("#6B7280"))
        c.drawCentredString(PAGE_WIDTH / 2.0, 0.35 * inch, f"Page {page_num}")

        c.setFont(body_font, 6.5)
        c.setFillColor(colors.HexColor("#9CA3AF"))
        c.drawString(MARGIN, 0.35 * inch, "© Ekpo Otu, Ph.D. • linktr.ee/ekpootu")
        c.drawRightString(PAGE_WIDTH - MARGIN, 0.35 * inch, "AI Agents Document OS")

        c.restoreState()

    return draw_first_page, draw_later_pages

# ---------------------------------------------------------------------------
# Document Builder
# ---------------------------------------------------------------------------
def build_guide(output_path: Path, fonts: dict, styles: dict):
    """Build the complete AI Agents Document OS Comprehensive Guide v4.0."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=PAGE_SIZE,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="AI Agents Document OS — Comprehensive User Guide v4.0",
        author="Ekpo Otu, Ph.D.",
        subject="Universal Document Operating System for AI Agents",
    )

    story = []

    # ============================================================
    # TITLE PAGE (Tight, elegant, zero excess white space)
    # ============================================================
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("AI Agents Document<br/>Operating System", styles["doc_title"]))
    story.append(Spacer(1, 0.08 * inch))
    story.append(accent_rule())
    story.append(Paragraph("Comprehensive User Guide &amp; Practical Operational Manual", styles["doc_subtitle"]))
    story.append(Spacer(1, 0.10 * inch))

    badge_t = Table(
        [[Paragraph("<b>OFFICIAL VERSION 4.0</b>", ParagraphStyle(
            "badge", fontName=fonts["body_semi"], fontSize=8,
            textColor=colors.HexColor("#0D1B4C"), alignment=TA_CENTER,
        ))]],
        colWidths=[1.6 * inch],
    )
    badge_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFC107")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#D99B00")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    badge_wrapper = Table([[badge_t]], colWidths=[PRINTABLE_WIDTH])
    badge_wrapper.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    story.append(badge_wrapper)

    story.append(Spacer(1, 0.25 * inch))

    # Hero image if available
    hero_path = Path("docs/assets/hero_banner.jpg")
    if hero_path.exists():
        story.append(Image(str(hero_path), width=PRINTABLE_WIDTH, height=2.2 * inch))
        story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("The Engineering Standard for Reliable AI Document Operations", styles["body_center"]))
    story.append(Spacer(1, 0.08 * inch))
    story.append(thin_rule())
    story.append(Spacer(1, 0.10 * inch))
    story.append(Paragraph(
        "E K P O&nbsp;&nbsp;&nbsp;O T U ,&nbsp;&nbsp;&nbsp;P h . D .",
        ParagraphStyle("author_spaced", fontName=fonts["body"],
                        fontSize=9.5, leading=13, textColor=C["muted"],
                        alignment=TA_CENTER, spaceBefore=0)
    ))
    story.append(Spacer(1, 0.05 * inch))
    story.append(Paragraph(
        '<a href="https://linktr.ee/ekpootu" color="#1A3A8F">linktr.ee/ekpootu</a>',
        ParagraphStyle("author_link", fontName=fonts["body"],
                        fontSize=8, leading=11, textColor=C["primary"],
                        alignment=TA_CENTER)
    ))

    story.append(PageBreak())

    # ============================================================
    # TABLE OF CONTENTS (Clickable Anchors & Compact Layout)
    # ============================================================
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Table of Contents", styles["h1"]))
    story.append(accent_rule())

    toc_items = [
        ("ch1", "Chapter 1", "Welcome: What is the AI Agents Document OS?"),
        ("ch2", "Chapter 2", "Quickstart: Daily High-Fidelity Operations"),
        ("ch3", "Chapter 3", "The 5-Stage Deterministic Safety Pipeline"),
        ("ch4", "Chapter 4", "Workspace Architecture & Global Deployment"),
        ("ch5", "Chapter 5", "CLI Command Reference & Automated Tooling"),
        ("ch6", "Chapter 6", "The Zero Unintentional Data Loss Guarantee"),
        ("ch7", "Chapter 7", "Cross-Harness Freedom: Claude, OpenCode & Cursor"),
        ("ch8", "Chapter 8", "Brand Identity, Web Design & Copywriting Skills"),
        ("ch9", "Author",    "About the Author & Community Ecosystem"),
    ]

    toc_rows = []
    for anchor, label, title in toc_items:
        link_col = Paragraph(f'<a href="#{anchor}" color="#1A3A8F"><b>{label}</b>: {title}</a>', styles["td"])
        arrow_col = Paragraph(f'<a href="#{anchor}" color="#1A3A8F"><b>Jump →</b></a>', ParagraphStyle(
            "toc_jump", parent=styles["td"], alignment=TA_RIGHT
        ))
        toc_rows.append([link_col, arrow_col])

    toc_table = Table(toc_rows, colWidths=[4.1 * inch, 0.8 * inch])
    toc_table.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#F1F5F9")),
    ]))
    story.append(toc_table)

    story.append(Spacer(1, 0.2 * inch))
    story.append(make_callout(
        "Every chapter title in this Table of Contents is clickable. Click any item above to navigate directly "
        "to that operational section in this interactive guide.",
        "INTERACTIVE HYPERLINKS", styles, "tip"
    ))

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 1: Welcome
    # ============================================================
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph('<a name="ch1"/>CHAPTER 1', styles["chapter_label"]))
    story.append(Paragraph("Welcome: What is the<br/>AI Agents Document OS?", styles["chapter_title"]))
    story.append(HRFlowable(width=1.8*inch, thickness=1.5, color=C["accent"],
                             spaceAfter=12, spaceBefore=4, hAlign="CENTER"))

    story.append(Paragraph(
        'If you have ever asked an AI assistant to <i>"read this PDF"</i>, <i>"edit this spreadsheet"</i>, or '
        '<i>"fix this PowerPoint presentation"</i>, you know the frustration. Standard LLM agents frequently '
        'hallucinate missing data, silently strip mathematical formulas in Excel, destroy corporate formatting, '
        'or generate corrupt files that fail to open.',
        styles["body"]
    ))
    story.append(Paragraph(
        '<b>AI Agents Document OS is your agent\'s reliable co-pilot.</b> It provides a deterministic safety suite, '
        'forensic inspection engine, and quality auditor in one cohesive architecture. Your agent gains the specialized '
        'protocols needed to process real documents with zero data loss.',
        styles["body"]
    ))

    story.append(make_callout(
        "You do not need to memorize terminal flags or write complex code. Simply speak to your agent in plain English. "
        "AI Agents Document OS triages file structures and applies safety protections automatically.",
        "AUTONOMOUS & NOVICE FRIENDLY", styles, "tip"
    ))

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 2: Quickstart
    # ============================================================
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph('<a name="ch2"/>CHAPTER 2', styles["chapter_label"]))
    story.append(Paragraph("Quickstart: Daily High-Fidelity Operations", styles["chapter_title"]))
    story.append(HRFlowable(width=1.8*inch, thickness=1.5, color=C["accent"],
                             spaceAfter=12, spaceBefore=4, hAlign="CENTER"))

    story.append(Paragraph(
        "When you collaborate with your agent, Document OS automatically detects target file types. "
        "Here are the 5 core everyday scenarios and how to prompt your agent:",
        styles["body"]
    ))

    use_case_table = make_table(
        ["Action", "Sample Prompt", "Document OS Protection"],
        [
            ["<b>Read PDF</b>", '<i>"Read the 2024 Audit and summarize revenue."</i>', "Identifies digital vs scanned layers; extracts tables cleanly."],
            ["<b>Edit XLSX</b>", '<i>"Update Q3 projections by 5%. Preserve formulas."</i>', "Loads workbook with formula graph guard; runs post-QA."],
            ["<b>Convert Doc</b>", '<i>"Convert proposal.docx into a presentation PDF."</i>', "Uses headless LibreOffice for 100% layout fidelity."],
            ["<b>Slide Deck</b>", '<i>"Build a 5-slide PowerPoint in 16:9 layout."</i>', "Applies master templates with word-wrap overflow guard."],
            ["<b>Scanned OCR</b>", '<i>"Extract vendor name and total from receipt.png."</i>', "Applies adaptive sharpening and deskewing before OCR."],
        ],
        [1.1 * inch, 1.8 * inch, 2.0 * inch],
        styles,
    )
    story.append(use_case_table)

    # Pipeline infographic if available
    pipeline_path = Path("docs/assets/pipeline_infographic.jpg")
    if pipeline_path.exists():
        story.append(Spacer(1, 0.12 * inch))
        story.append(Image(str(pipeline_path), width=PRINTABLE_WIDTH, height=2.1 * inch))

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 3: 5-Stage Pipeline
    # ============================================================
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph('<a name="ch3"/>CHAPTER 3', styles["chapter_label"]))
    story.append(Paragraph("The 5-Stage Deterministic Safety Pipeline", styles["chapter_title"]))
    story.append(HRFlowable(width=1.8*inch, thickness=1.5, color=C["accent"],
                             spaceAfter=12, spaceBefore=4, hAlign="CENTER"))

    story.append(Paragraph(
        "Every document task passes through a 5-stage engineering pipeline to guarantee absolute fidelity:",
        styles["body"]
    ))

    pipeline_table = make_table(
        ["Stage", "Action", "Tool / Helper", "Fidelity Target"],
        [
            ["<b>1. Triage</b>", "Structural inspection", "<code>inspect_doc.py</code>", "Detects digital text, counts formulas, checks aspect ratio."],
            ["<b>2. Route</b>", "Protocol selection", "<code>document-router</code>", "Selects verified parser (openpyxl, pdfplumber, python-docx)."],
            ["<b>3. Execute</b>", "Deterministic runs", "<code>extract_doc.py</code><br/><code>convert_doc.py</code>", "Executes tested CLI commands without impromptu scripts."],
            ["<b>4. Render</b>", "Visual verification", "<code>render_doc.py</code>", "Converts pages to high-res PNGs for vision inspection."],
            ["<b>5. QA Audit</b>", "Integrity validation", "<code>qa_doc.py</code>", "Scans for formula errors (#REF!, #DIV/0!) and broken XML."],
        ],
        [0.8 * inch, 1.1 * inch, 1.2 * inch, 1.8 * inch],
        styles,
    )
    story.append(pipeline_table)
    story.append(Spacer(1, 0.12 * inch))

    story.append(make_callout(
        "The 5-stage pipeline runs automatically. The Master Document Router triages structure and sequences "
        "the exact safe tools required for each file format.",
        "PIPELINE AUTOMATION", styles, "success"
    ))

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 4: Workspace Architecture & Global Deployment
    # ============================================================
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph('<a name="ch4"/>CHAPTER 4', styles["chapter_label"]))
    story.append(Paragraph("Workspace Architecture &amp;<br/>Global Deployment", styles["chapter_title"]))
    story.append(HRFlowable(width=1.8*inch, thickness=1.5, color=C["accent"],
                             spaceAfter=12, spaceBefore=4, hAlign="CENTER"))

    story.append(Paragraph(
        "AI Agents Document OS is deployed in two complementary tiers:",
        styles["body"]
    ))
    story.append(Paragraph(
        '• <b>Local Workspace</b> (<code>.agents/plugins/document-os/</code>): '
        'Directly integrated into your project repository. Shares deterministic rules with your entire engineering team.',
        styles["bullet"]
    ))
    story.append(Paragraph(
        '• <b>Global User Profile</b> (<code>~/.gemini/config/plugins/document-os/</code>): '
        'Installed into your user profile so every agent session across all directories inherits Document OS capabilities.',
        styles["bullet"]
    ))
    story.append(Spacer(1, 0.08 * inch))

    story.append(Paragraph("Universal Agent Compatibility", styles["h2"]))
    story.append(Paragraph(
        "Document OS strictly adheres to open agent specifications. Export seamlessly with one command:",
        styles["body"]
    ))
    story.append(Paragraph('<code>.\\export_cross_harness.ps1 -Target All</code>', styles["code"]))
    story.append(Paragraph(
        "This establishes full compatibility with <b>Google Antigravity</b>, <b>Claude Code</b>, <b>OpenCode CLI</b>, and <b>Cursor</b>.",
        styles["body"]
    ))

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 5: CLI Command Reference
    # ============================================================
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph('<a name="ch5"/>CHAPTER 5', styles["chapter_label"]))
    story.append(Paragraph("CLI Command Reference &amp;<br/>Automated Tooling", styles["chapter_title"]))
    story.append(HRFlowable(width=1.8*inch, thickness=1.5, color=C["accent"],
                             spaceAfter=12, spaceBefore=4, hAlign="CENTER"))

    story.append(Paragraph(
        "For CI/CD pipelines, automated scripts, or terminal workflows, use the deterministic CLI helpers:",
        styles["body"]
    ))

    cli_table = make_table(
        ["Command", "Description", "Output / Guarantee"],
        [
            ["<code>inspect_doc.py &lt;file&gt;</code>", "Deep structural triage.", "JSON metadata (pages, sheets, formulas, fonts)."],
            ["<code>extract_doc.py &lt;file&gt; --tables</code>", "Extracts tabular data.", "Clean Markdown tables ready for LLM processing."],
            ["<code>convert_doc.py in.docx out.pdf</code>", "Headless conversion.", "Pixel-perfect conversion via LibreOffice/Pandoc."],
            ["<code>render_doc.py deck.pptx --outdir ./img</code>", "Renders slides/pages to PNG.", "Visual artifacts for multi-modal agent inspection."],
            ["<code>ocr_doc.py receipt.png --output txt</code>", "Tesseract adaptive OCR.", "Pre-processed text extraction with contrast boost."],
            ["<code>qa_doc.py model.xlsx</code>", "Pre/post integrity check.", "Asserts 0 formula errors (#REF!, #DIV/0!)."],
        ],
        [1.6 * inch, 1.5 * inch, 1.8 * inch],
        styles,
    )
    story.append(cli_table)

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 6: Zero Data Loss Guarantee
    # ============================================================
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph('<a name="ch6"/>CHAPTER 6', styles["chapter_label"]))
    story.append(Paragraph("The Zero Unintentional<br/>Data Loss Guarantee", styles["chapter_title"]))
    story.append(HRFlowable(width=1.8*inch, thickness=1.5, color=C["accent"],
                             spaceAfter=12, spaceBefore=4, hAlign="CENTER"))

    story.append(Paragraph(
        "Document OS implements three non-negotiable architectural guarantees to safeguard your critical files:",
        styles["body"]
    ))
    story.append(Paragraph(
        '1.&nbsp;&nbsp;<b>Read-Only Default</b>: The agent never mutates an original document in-place unless '
        'explicitly commanded. Output is written to distinct versions (e.g., <code>budget_v2.xlsx</code>).',
        styles["bullet_num"]
    ))
    story.append(Paragraph(
        '2.&nbsp;&nbsp;<b>Formula Integrity Guard</b>: Dynamic calculation trees (`=SUM`, `=VLOOKUP`) are '
        'protected from being overwritten by static numerical values.',
        styles["bullet_num"]
    ))
    story.append(Paragraph(
        '3.&nbsp;&nbsp;<b>Mandatory Post-Execution QA</b>: No operation is marked "Complete" until '
        '<code>qa_doc.py</code> validates file health, XML syntax, and rendering integrity.',
        styles["bullet_num"]
    ))
    story.append(Spacer(1, 0.1 * inch))

    story.append(make_callout(
        "These rules are hardcoded into AGENTS.md, GEMINI.md, and document-safety.md, providing "
        "an unbreakable guardrail across all agent harnesses.",
        "ENGINEERED INTEGRITY", styles, "warning"
    ))

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 7: Cross-Harness Freedom
    # ============================================================
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph('<a name="ch7"/>CHAPTER 7', styles["chapter_label"]))
    story.append(Paragraph("Cross-Harness Freedom:<br/>Claude, OpenCode &amp; Cursor", styles["chapter_title"]))
    story.append(HRFlowable(width=1.8*inch, thickness=1.5, color=C["accent"],
                             spaceAfter=12, spaceBefore=4, hAlign="CENTER"))

    story.append(Paragraph(
        "Seamlessly portable across all major AI coding platforms with identical safety guarantees:",
        styles["body"]
    ))

    compat_table = make_table(
        ["Platform", "Configuration Path", "Integration Method"],
        [
            ["<b>Google Antigravity</b>", "<code>.agents/plugins/document-os/</code>", "Native plug-and-play."],
            ["<b>Claude Code</b>", "<code>~/.claude/skills/document-os/</code>", "Export via <code>export_cross_harness.ps1</code>."],
            ["<b>OpenCode CLI</b>", "<code>~/.config/opencode/skills/</code>", "Export via <code>export_cross_harness.ps1</code>."],
            ["<b>Cursor IDE</b>", "<code>.cursor/skills/document-os/</code>", "Export via <code>export_cross_harness.ps1</code>."],
        ],
        [1.3 * inch, 1.8 * inch, 1.8 * inch],
        styles,
    )
    story.append(compat_table)

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 8: Brand Identity, Web Design & Copywriting Skills
    # ============================================================
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph('<a name="ch8"/>CHAPTER 8', styles["chapter_label"]))
    story.append(Paragraph("Brand Identity, Web Design<br/>&amp; Copywriting Skills", styles["chapter_title"]))
    story.append(HRFlowable(width=1.8*inch, thickness=1.5, color=C["accent"],
                             spaceAfter=12, spaceBefore=4, hAlign="CENTER"))

    story.append(Paragraph(
        "Version 4.0 introduces an integrated creative suite to ensure generated artifacts look and read like "
        "commercial-grade products:",
        styles["body"]
    ))
    story.append(Paragraph("• <b>Brand Identity Skill</b>: Royal Blue (#1A3A8F), Golden Yellow (#FFC107), and Navy (#0D1B4C) palette.", styles["bullet"]))
    story.append(Paragraph("• <b>Web Design Skill</b>: Synthesizes designmd.ai tokens, neuform.ai depth, and dribbble.com card patterns.", styles["bullet"]))
    story.append(Paragraph("• <b>Copywriting Skill</b>: Adopts the top-ranked skills.sh standard for high-converting headlines and CTAs.", styles["bullet"]))
    story.append(Paragraph("• <b>1.6:1 Publication Standard</b>: Enforces Amazon KDP book aspect ratio with hyperlinked navigation.", styles["bullet"]))

    story.append(Spacer(1, 0.1 * inch))
    story.append(make_callout(
        "This official guide is dogfooded proof: generated with the v4.0 PDF engine, embedded Google Fonts, "
        "clickable anchors, and the strict 1.6:1 height-to-width ratio.",
        "DOGFOODED STANDARD", styles, "success"
    ))

    story.append(PageBreak())

    # ============================================================
    # ABOUT THE AUTHOR
    # ============================================================
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph('<a name="ch9"/>About the Author', styles["h1"]))
    story.append(accent_rule())

    story.append(Paragraph(
        '<b>Ekpo Otu, Ph.D.</b> is a Computer Professional, Full Stack Developer, Researcher, Author, '
        'and Lecturer dedicated to applying computational intelligence to solve real-world problems. '
        'His work focuses on autonomous agent architectures, reliable document engineering, and open-source tooling.',
        styles["body"]
    ))
    story.append(Spacer(1, 0.1 * inch))

    links_table = make_table(
        ["Channel", "URL"],
        [
            ["Author Bio &amp; Projects", '<a href="https://linktr.ee/ekpootu" color="#1A3A8F">linktr.ee/ekpootu</a>'],
            ["GitHub Repository", '<a href="https://github.com/ekpootu" color="#1A3A8F">github.com/ekpootu</a>'],
            ["Support Development", '<a href="https://www.buymeacoffee.com/ekpootu" color="#1A3A8F">buymeacoffee.com/ekpootu</a>'],
        ],
        [1.6 * inch, 3.3 * inch],
        styles,
    )
    story.append(links_table)

    story.append(Spacer(1, 0.15 * inch))

    support_box = Table(
        [[
            Paragraph(
                '☕ <b>Fuel Open-Source Document Engineering</b><br/><br/>'
                'AI Agents Document OS is 100% free and open source under the MIT License. '
                'If this system saved your financial spreadsheets or corporate decks from agent destruction, '
                'consider fueling ongoing maintenance!<br/><br/>'
                '<b><a href="https://www.buymeacoffee.com/ekpootu" color="#1A3A8F">buymeacoffee.com/ekpootu</a></b>',
                ParagraphStyle("support_text", fontName=fonts["body"],
                                fontSize=8.5, leading=13, textColor=C["body"],
                                alignment=TA_CENTER)
            )
        ]],
        colWidths=[PRINTABLE_WIDTH],
    )
    support_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF8E1")),
        ("BOX", (0, 0), (-1, -1), 1.2, C["accent"]),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(support_box)

    story.append(Spacer(1, 0.12 * inch))
    story.append(thin_rule())
    story.append(Paragraph(
        '<i>AI Agents Document Operating System (Document OS) • User Guide v4.0 • MIT Licensed</i>',
        styles["footer_meta"]
    ))

    # --- Build Document with Callbacks ---
    draw_first, draw_later = make_page_decorators(fonts)
    doc.build(story, onFirstPage=draw_first, onLaterPages=draw_later)
    print(f"\n[OK] Successfully generated professional PDF: {output_path}")

def main():
    print("=" * 60)
    print("  AI Agents Document OS — Professional PDF Builder v4")
    print("  Brand: Royal Blue • Golden Yellow • Deep Navy")
    print("  Dimensions: 6.0\" x 9.6\" (1.6:1 Aspect Ratio)")
    print("  Author: Ekpo Otu, Ph.D.")
    print("=" * 60)

    print("\n[1/3] Registering fonts...")
    fonts = register_fonts()
    print(f"  Display: {fonts['display']}")
    print(f"  Body:    {fonts['body']}")

    print("\n[2/3] Building styles...")
    styles = build_styles(fonts)

    print("\n[3/3] Generating PDF...")
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else \
             Path("docs/AI_Agents_Document_OS_Comprehensive_Guide_v4.pdf")
    build_guide(output, fonts, styles)

if __name__ == "__main__":
    main()
