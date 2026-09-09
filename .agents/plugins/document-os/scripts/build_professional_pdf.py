#!/usr/bin/env python3
"""
build_professional_pdf.py — Professional Document OS Guide Builder (v3)

Generates a KDP-quality PDF using ReportLab with embedded Google Fonts
(Playfair Display + Source Sans 3), brand color palette, running headers/
footers, chapter openers, callout boxes, and author section.

Brand Tokens:  Royal Blue #1A3A8F | Golden #FFC107 | Navy #0D1B4C
Author:        Ekpo Otu, Ph.D. — https://linktr.ee/ekpootu

Falls back gracefully if custom fonts cannot be downloaded.
"""

import sys
import json
import urllib.request
import tempfile
from pathlib import Path
from reportlab.lib.pagesizes import letter
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
# Font Registration — attempt to use bundled fonts, else Helvetica fallback
# ---------------------------------------------------------------------------
FONT_DIR = Path(__file__).parent / "templates" / "fonts"

# Google Fonts download URLs (static TTF files from GitHub)
GOOGLE_FONT_URLS = {
    "PlayfairDisplay-Bold": "https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf",
    "SourceSans3-Regular": "https://raw.githubusercontent.com/google/fonts/main/ofl/sourcesans3/SourceSans3%5Bwght%5D.ttf",
}

# Variable fonts need special handling — we download the variable font and register it
# under specific names for ReportLab compatibility

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
        path = _download_font(name, url)
        if path:
            try:
                pdfmetrics.registerFont(TTFont(name, str(path)))
            except Exception as e:
                print(f"  Warning: Could not register {name}: {e}")
                fonts_available = False
        else:
            fonts_available = False

    if fonts_available:
        # Variable fonts work at default weight in ReportLab
        # We map all style slots to the available registered fonts
        return {
            "display": "PlayfairDisplay-Bold",
            "display_xl": "PlayfairDisplay-Bold",
            "body": "SourceSans3-Regular",
            "body_semi": "SourceSans3-Regular",
            "body_bold": "SourceSans3-Regular",
            "body_italic": "SourceSans3-Regular",
            "mono": "Courier",  # ReportLab built-in
        }
    else:
        print("  Falling back to Helvetica font family.")
        return {
            "display": "Helvetica-Bold",
            "display_xl": "Helvetica-Bold",
            "body": "Helvetica",
            "body_semi": "Helvetica-Bold",
            "body_bold": "Helvetica-Bold",
            "body_italic": "Helvetica-Oblique",
            "mono": "Courier",
        }

# ---------------------------------------------------------------------------
# Numbered Canvas with Professional Headers/Footers
# ---------------------------------------------------------------------------
class ProfessionalCanvas(canvas.Canvas):
    """Canvas with running headers, footers, and page decorations."""

    def __init__(self, *args, fonts=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self._fonts = fonts or {}
        self._chapter_pages = set()  # pages that are chapter openers

    def mark_chapter_page(self):
        self._chapter_pages.add(len(self._saved_page_states) + 1)

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_decorations(num_pages)
            super().showPage()
        super().save()

    def _draw_decorations(self, total_pages):
        self.saveState()
        page_num = self._pageNumber
        body_font = self._fonts.get("body", "Helvetica")
        is_title_page = (page_num == 1)
        is_chapter = page_num in self._chapter_pages

        # --- Running Header (skip on title page and chapter openers) ---
        if not is_title_page and not is_chapter:
            self.setFont(body_font, 7.5)
            self.setFillColor(colors.HexColor("#6B7280"))
            self.drawString(0.75 * inch, 10.35 * inch,
                            "Antigravity Document OS — Comprehensive User Guide v3.0")
            # Thin header rule
            self.setStrokeColor(colors.HexColor("#DEE2E6"))
            self.setLineWidth(0.4)
            self.line(0.75 * inch, 10.28 * inch, 7.75 * inch, 10.28 * inch)

        # --- Footer rule + page number (skip on title page) ---
        if not is_title_page:
            self.setStrokeColor(colors.HexColor("#DEE2E6"))
            self.setLineWidth(0.4)
            self.line(0.75 * inch, 0.62 * inch, 7.75 * inch, 0.62 * inch)

            self.setFont(body_font, 8)
            self.setFillColor(colors.HexColor("#6B7280"))
            page_text = f"{page_num}"
            self.drawCentredString(4.25 * inch, 0.42 * inch, page_text)

            # Footer left: author
            self.setFont(body_font, 7)
            self.setFillColor(colors.HexColor("#9CA3AF"))
            self.drawString(0.75 * inch, 0.42 * inch,
                            "© Ekpo Otu, Ph.D. • linktr.ee/ekpootu")
            # Footer right: branding
            self.drawRightString(7.75 * inch, 0.42 * inch,
                                 "Powered by Document OS Engine")

        # --- Title page accent bar ---
        if is_title_page:
            # Top accent bar
            self.setFillColor(colors.HexColor("#1A3A8F"))
            self.rect(0, 10.75 * inch, 8.5 * inch, 0.25 * inch, fill=True, stroke=False)
            # Bottom accent bar
            self.setFillColor(colors.HexColor("#FFC107"))
            self.rect(0, 0, 8.5 * inch, 0.15 * inch, fill=True, stroke=False)

        self.restoreState()


# ---------------------------------------------------------------------------
# Style Factory
# ---------------------------------------------------------------------------
def build_styles(fonts: dict) -> dict:
    """Create all paragraph styles using brand fonts and colors."""
    base = getSampleStyleSheet()

    s = {}

    # --- Title Page ---
    s["doc_title"] = ParagraphStyle(
        "DocTitle", parent=base["Heading1"],
        fontName=fonts["display_xl"], fontSize=28, leading=34,
        textColor=C["primary_dark"], alignment=TA_CENTER,
        spaceAfter=6,
    )
    s["doc_subtitle"] = ParagraphStyle(
        "DocSubtitle", parent=base["Normal"],
        fontName=fonts["body"], fontSize=13, leading=18,
        textColor=C["primary"], alignment=TA_CENTER,
        spaceAfter=10,
    )
    s["doc_version"] = ParagraphStyle(
        "DocVersion", parent=base["Normal"],
        fontName=fonts["body_semi"], fontSize=10, leading=14,
        textColor=C["primary_dark"], alignment=TA_CENTER,
        spaceBefore=4, spaceAfter=4,
    )
    s["doc_author"] = ParagraphStyle(
        "DocAuthor", parent=base["Normal"],
        fontName=fonts["body"], fontSize=11, leading=15,
        textColor=C["muted"], alignment=TA_CENTER,
        spaceBefore=20,
    )

    # --- Chapter Opener ---
    s["chapter_label"] = ParagraphStyle(
        "ChapterLabel", parent=base["Normal"],
        fontName=fonts["body_semi"], fontSize=10, leading=14,
        textColor=C["primary"], alignment=TA_CENTER,
        spaceBefore=0, spaceAfter=4,
    )
    s["chapter_title"] = ParagraphStyle(
        "ChapterTitle", parent=base["Heading1"],
        fontName=fonts["display"], fontSize=22, leading=28,
        textColor=C["primary_dark"], alignment=TA_CENTER,
        spaceBefore=0, spaceAfter=8,
    )

    # --- Section Headings ---
    s["h1"] = ParagraphStyle(
        "H1Pro", parent=base["Heading1"],
        fontName=fonts["display"], fontSize=18, leading=23,
        textColor=C["primary_dark"],
        spaceBefore=16, spaceAfter=6, keepWithNext=True,
    )
    s["h2"] = ParagraphStyle(
        "H2Pro", parent=base["Heading2"],
        fontName=fonts["body_bold"], fontSize=14, leading=18,
        textColor=C["primary"],
        spaceBefore=14, spaceAfter=5, keepWithNext=True,
    )
    s["h3"] = ParagraphStyle(
        "H3Pro", parent=base["Heading3"],
        fontName=fonts["body_semi"], fontSize=11.5, leading=16,
        textColor=C["primary_dark"],
        spaceBefore=10, spaceAfter=4, keepWithNext=True,
    )

    # --- Body Text ---
    s["body"] = ParagraphStyle(
        "BodyPro", parent=base["Normal"],
        fontName=fonts["body"], fontSize=10, leading=15,
        textColor=C["body"], alignment=TA_JUSTIFY,
        spaceAfter=6,
    )
    s["body_bold"] = ParagraphStyle(
        "BodyBold", parent=s["body"],
        fontName=fonts["body_semi"],
    )
    s["body_italic"] = ParagraphStyle(
        "BodyItalic", parent=s["body"],
        fontName=fonts["body_italic"],
    )
    s["body_center"] = ParagraphStyle(
        "BodyCenter", parent=s["body"],
        alignment=TA_CENTER,
    )

    # --- Bullet ---
    s["bullet"] = ParagraphStyle(
        "BulletPro", parent=s["body"],
        leftIndent=18, firstLineIndent=-12,
        spaceAfter=4,
    )
    s["bullet_num"] = ParagraphStyle(
        "BulletNum", parent=s["body"],
        leftIndent=18, firstLineIndent=-14,
        spaceAfter=4,
    )

    # --- Code ---
    s["code"] = ParagraphStyle(
        "CodePro", parent=base["Code"],
        fontName=fonts["mono"], fontSize=8.5, leading=12,
        textColor=colors.HexColor("#991B1B"),
        backColor=C["bg_panel"],
        borderPadding=4,
    )

    # --- Table Cells ---
    s["th"] = ParagraphStyle(
        "TableHeader", parent=base["Normal"],
        fontName=fonts["body_semi"], fontSize=8.5, leading=12,
        textColor=colors.white,
    )
    s["td"] = ParagraphStyle(
        "TableCell", parent=base["Normal"],
        fontName=fonts["body"], fontSize=8.5, leading=12,
        textColor=C["body"],
    )

    # --- Callout ---
    s["callout"] = ParagraphStyle(
        "Callout", parent=base["Normal"],
        fontName=fonts["body_italic"], fontSize=9.5, leading=14,
        textColor=colors.HexColor("#0369A1"),
    )
    s["callout_title"] = ParagraphStyle(
        "CalloutTitle", parent=base["Normal"],
        fontName=fonts["body_semi"], fontSize=9, leading=12,
        textColor=C["primary"],
        spaceAfter=2,
    )

    # --- Footer Meta ---
    s["footer_meta"] = ParagraphStyle(
        "FooterMeta", parent=base["Normal"],
        fontName=fonts["body_italic"], fontSize=8,
        textColor=C["muted"], alignment=TA_CENTER,
    )

    return s


# ---------------------------------------------------------------------------
# Reusable Components
# ---------------------------------------------------------------------------
def make_callout(text: str, title: str, styles: dict,
                 variant: str = "tip") -> Table:
    """Create a branded callout box."""
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
    t = Table([[content]], colWidths=[7.0 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_c),
        ("LINEBEFORE", (0, 0), (0, -1), 4, border_c),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("BOX", (0, 0), (-1, -1), 0.5, C["border"]),
    ]))
    return t


def make_table(headers: list, rows: list, col_widths: list, styles: dict) -> Table:
    """Create a branded data table."""
    data = [[Paragraph(f"<b>{h}</b>", styles["th"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(cell), styles["td"]) for cell in row])

    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C["primary"]),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("BACKGROUND", (0, 1), (-1, -1), C["white"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C["white"], C["bg_light"]]),
        ("GRID", (0, 0), (-1, -1), 0.5, C["border"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
    ]))
    return t


def accent_rule():
    """Gradient-like accent horizontal rule."""
    return HRFlowable(
        width="100%", thickness=2,
        color=colors.HexColor("#FFC107"),
        spaceAfter=8, spaceBefore=4,
    )

def thin_rule():
    return HRFlowable(
        width="100%", thickness=0.5,
        color=C["border"],
        spaceAfter=6, spaceBefore=6,
    )


# ---------------------------------------------------------------------------
# Document Content — Comprehensive Guide v3
# ---------------------------------------------------------------------------
def build_guide(output_path: Path, fonts: dict, styles: dict):
    """Build the complete Document OS Comprehensive Guide v3."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
        title="Antigravity Document OS — Comprehensive User Guide v3.0",
        author="Ekpo Otu, Ph.D.",
        subject="Universal Document Operating System for AI Agents",
    )

    story = []

    # ============================================================
    # TITLE PAGE
    # ============================================================
    story.append(Spacer(1, 1.8 * inch))
    story.append(Paragraph(
        "Antigravity Document<br/>Operating System",
        styles["doc_title"]
    ))
    story.append(Spacer(1, 0.15 * inch))
    story.append(accent_rule())
    story.append(Paragraph(
        "Comprehensive User Guide &amp; Practical Operational Manual",
        styles["doc_subtitle"]
    ))
    story.append(Spacer(1, 0.3 * inch))

    # Version badge as a mini table
    badge_t = Table(
        [[Paragraph("<b>VERSION 3.0</b>", ParagraphStyle(
            "badge", fontName=fonts["body_semi"], fontSize=9,
            textColor=colors.HexColor("#0D1B4C"), alignment=TA_CENTER,
        ))]],
        colWidths=[1.5 * inch],
    )
    badge_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFC107")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    badge_wrapper = Table([[badge_t]], colWidths=[7.0 * inch])
    badge_wrapper.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    story.append(badge_wrapper)

    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph(
        "The Engineering Standard for Reliable AI Document Operations",
        styles["body_center"]
    ))
    story.append(Spacer(1, 0.2 * inch))
    story.append(thin_rule())
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph(
        "E K P O&nbsp;&nbsp;&nbsp;O T U ,&nbsp;&nbsp;&nbsp;P h . D .",
        ParagraphStyle("author_spaced", fontName=fonts["body"],
                        fontSize=11, leading=15, textColor=C["muted"],
                        alignment=TA_CENTER, spaceBefore=0)
    ))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        '<a href="https://linktr.ee/ekpootu" color="#1A3A8F">linktr.ee/ekpootu</a>',
        ParagraphStyle("author_link", fontName=fonts["body"],
                        fontSize=9, leading=13, textColor=C["primary"],
                        alignment=TA_CENTER)
    ))

    story.append(PageBreak())

    # ============================================================
    # TABLE OF CONTENTS
    # ============================================================
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Table of Contents", styles["h1"]))
    story.append(accent_rule())

    toc_items = [
        ("1.", "Welcome: What is the Document Operating System?"),
        ("2.", "Quickstart: How to Use Document OS Every Day"),
        ("3.", "The 5-Stage Safety Pipeline"),
        ("4.", "Understanding Your Workspace & Global Deployment"),
        ("5.", "Quick Reference CLI Command Cheat Sheet"),
        ("6.", "The Zero Unintentional Data Loss Guarantee"),
        ("7.", "Cross-Harness Freedom: Claude Code, OpenCode, Cursor"),
        ("8.", "Brand Identity & Professional Document Styling"),
        ("9.", "About the Author"),
    ]
    for num, title in toc_items:
        story.append(Paragraph(
            f'<b>{num}</b>&nbsp;&nbsp;{title}',
            ParagraphStyle("toc_item", fontName=fonts["body"],
                            fontSize=11, leading=20, textColor=C["body"],
                            leftIndent=20)
        ))
    story.append(PageBreak())

    # ============================================================
    # CHAPTER 1: Welcome
    # ============================================================
    story.append(Spacer(1, 2.0 * inch))
    story.append(Paragraph("CHAPTER 1", styles["chapter_label"]))
    story.append(Paragraph("Welcome: What is the<br/>Document Operating System?", styles["chapter_title"]))
    story.append(HRFlowable(width=2*inch, thickness=2, color=C["accent"],
                             spaceAfter=20, spaceBefore=8, hAlign="CENTER"))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph(
        'If you have ever asked an AI assistant to <i>"read this PDF"</i>, <i>"edit this spreadsheet"</i>, or '
        '<i>"fix this PowerPoint presentation"</i>, you might have noticed that things often go wrong. Standard AI agents '
        'frequently hallucinate missing information, accidentally erase vital mathematical formulas in Excel, break '
        'document margins, or deliver files that won\'t even open.',
        styles["body"]
    ))
    story.append(Paragraph(
        '<b>Document OS is your AI agent\'s reliable co-pilot.</b> Think of it as an automated safety suite, forensic '
        'reader, and quality inspector all in one. It gives your Antigravity agent the specialized knowledge and precision '
        'tools needed to work with real documents — without making mistakes or deleting your data.',
        styles["body"]
    ))

    story.append(make_callout(
        "You do not need to memorize complex terminal commands or write Python code! "
        "Simply talk to your Antigravity agent in plain English. Document OS works automatically "
        "behind the scenes to safeguard your documents.",
        "NOVICE FRIENDLY", styles, "tip"
    ))
    story.append(Spacer(1, 0.15 * inch))

    # Hero image if available
    hero_path = Path("docs/assets/hero_banner.jpg")
    if hero_path.exists():
        story.append(Image(str(hero_path), width=7.0 * inch, height=3.2 * inch))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 2: Quickstart
    # ============================================================
    story.append(Spacer(1, 2.0 * inch))
    story.append(Paragraph("CHAPTER 2", styles["chapter_label"]))
    story.append(Paragraph("Quickstart: How to Use<br/>Document OS Every Day", styles["chapter_title"]))
    story.append(HRFlowable(width=2*inch, thickness=2, color=C["accent"],
                             spaceAfter=20, spaceBefore=8, hAlign="CENTER"))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph(
        "Using Document OS requires zero technical wizardry. When you converse with your Antigravity agent, "
        "the system automatically detects when you are dealing with files. Here are the 5 most common everyday "
        "scenarios and how to prompt your agent:",
        styles["body"]
    ))
    story.append(Spacer(1, 6))

    use_case_table = make_table(
        ["What You Want to Do", "What You Prompt", "What Document OS Does"],
        [
            ["<b>Read &amp; Summarize a PDF</b>",
             '<i>"Read the 2024 Annual Report and summarize key revenue figures."</i>',
             "Checks if PDF is digital or scanned, extracts tables cleanly."],
            ["<b>Edit an Excel Spreadsheet</b>",
             '<i>"Update Q3 projections with 5% increase. Keep formulas intact."</i>',
             "Loads workbook with formula preservation. Runs automated QA."],
            ["<b>Convert Formats Safely</b>",
             '<i>"Convert this Word proposal into a presentation-ready PDF."</i>',
             "Uses headless LibreOffice for 100% fidelity conversion."],
            ["<b>Create a Slide Deck</b>",
             '<i>"Turn these notes into a 5-slide PowerPoint in 16:9 layout."</i>',
             "Builds slides with word wrap, applies master templates."],
            ["<b>Extract from Scanned Images</b>",
             '<i>"Extract vendor name, date, and total from this receipt."</i>',
             "Applies contrast sharpening, deskewing, then OCR extraction."],
        ],
        [1.5 * inch, 2.5 * inch, 3.0 * inch],
        styles,
    )
    story.append(use_case_table)

    # Pipeline infographic if available
    pipeline_path = Path("docs/assets/pipeline_infographic.jpg")
    if pipeline_path.exists():
        story.append(Spacer(1, 10))
        story.append(Paragraph("The Automated Safety Pipeline", styles["h3"]))
        story.append(Image(str(pipeline_path), width=7.0 * inch, height=3.0 * inch))

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 3: 5-Stage Pipeline
    # ============================================================
    story.append(Spacer(1, 2.0 * inch))
    story.append(Paragraph("CHAPTER 3", styles["chapter_label"]))
    story.append(Paragraph("The 5-Stage Safety Pipeline", styles["chapter_title"]))
    story.append(HRFlowable(width=2*inch, thickness=2, color=C["accent"],
                             spaceAfter=20, spaceBefore=8, hAlign="CENTER"))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph(
        "To ensure zero accidental data loss, every document task passes through a rigorous 5-stage engineering "
        "pipeline. Each stage is systematically checked before returning results to you:",
        styles["body"]
    ))

    pipeline_table = make_table(
        ["Stage", "Action", "Tool / Helper", "Quality Objective"],
        [
            ["<b>1. Triage</b>", "Preflight structural analysis", "<code>inspect_doc.py</code>",
             "Determines if PDF is digital or scanned. Counts sheets and formulas. Checks slide aspect ratios."],
            ["<b>2. Route</b>", "Specialist protocol selection", "<code>document-router</code>",
             "Selects the exact safe library (openpyxl with formula-protect, pdfplumber for grids, python-docx for styles)."],
            ["<b>3. Execute</b>", "Deterministic processing", "<code>extract_doc.py</code><br/><code>convert_doc.py</code>",
             "Carries out the operation using pre-tested tools rather than hallucinated code."],
            ["<b>4. Render</b>", "Visual preview generation", "<code>render_doc.py</code>",
             "Converts pages to high-res PNG images so the agent can visually verify layout."],
            ["<b>5. QA Audit</b>", "Integrity &amp; error check", "<code>qa_doc.py</code>",
             "Scans for broken formulas (#REF!, #DIV/0!), confirms files open cleanly."],
        ],
        [0.85 * inch, 1.3 * inch, 1.45 * inch, 3.4 * inch],
        styles,
    )
    story.append(pipeline_table)
    story.append(Spacer(1, 10))

    story.append(make_callout(
        "The 5-stage pipeline runs automatically — you never need to invoke these tools manually. "
        "Your Antigravity agent's Document Router skill triggers each stage in the correct order based "
        "on the file type and your request.",
        "HOW IT WORKS", styles, "success"
    ))

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 4: Workspace & Deployment
    # ============================================================
    story.append(Spacer(1, 2.0 * inch))
    story.append(Paragraph("CHAPTER 4", styles["chapter_label"]))
    story.append(Paragraph("Understanding Your Workspace<br/>&amp; Global Deployment", styles["chapter_title"]))
    story.append(HRFlowable(width=2*inch, thickness=2, color=C["accent"],
                             spaceAfter=20, spaceBefore=8, hAlign="CENTER"))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph(
        "Document OS is installed in two complementary locations for total flexibility:",
        styles["body"]
    ))
    story.append(Paragraph(
        '• <b>Local Workspace</b> (<code>.agents/plugins/document-os/</code>): '
        'Ready to run in your current project. Commit to Git so your entire team shares the same document rules.',
        styles["bullet"]
    ))
    story.append(Paragraph(
        '• <b>Global Deployment</b> (<code>~/.gemini/config/plugins/document-os/</code>): '
        'Installed into your Antigravity user profile. Every project automatically enjoys Document OS superpowers.',
        styles["bullet"]
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Cross-Harness Freedom", styles["h2"]))
    story.append(Paragraph(
        "You are never locked into a single AI tool! Document OS adheres to open Agent Skills standards. "
        "Run the included exporter to deploy across all your development environments:",
        styles["body"]
    ))
    story.append(Paragraph(
        '<code>.\\export_cross_harness.ps1 -Target All</code>',
        styles["code"]
    ))
    story.append(Paragraph(
        "This bridges your Document OS skills into <b>Claude Code</b>, <b>OpenCode CLI</b>, and <b>Cursor</b>.",
        styles["body"]
    ))

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 5: CLI Cheat Sheet
    # ============================================================
    story.append(Spacer(1, 2.0 * inch))
    story.append(Paragraph("CHAPTER 5", styles["chapter_label"]))
    story.append(Paragraph("Quick Reference<br/>CLI Command Cheat Sheet", styles["chapter_title"]))
    story.append(HRFlowable(width=2*inch, thickness=2, color=C["accent"],
                             spaceAfter=20, spaceBefore=8, hAlign="CENTER"))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph(
        "For power users, automated scripts, or terminal workflows, execute CLI tools directly:",
        styles["body"]
    ))

    cli_table = make_table(
        ["Command", "What It Does", "Output / Benefit"],
        [
            ["<code>python inspect_doc.py &lt;file&gt;</code>",
             "Analyzes any document format.", "Returns JSON with page count, sheet names, formula count."],
            ["<code>python extract_doc.py &lt;file&gt; --type tables</code>",
             "Pulls tabular data from files.", "Outputs clean Markdown tables for reports."],
            ["<code>python convert_doc.py input.docx output.pdf</code>",
             "Headless cross-format conversion.", "Vector-perfect without font degradation."],
            ["<code>python render_doc.py deck.pptx --outdir ./previews</code>",
             "Renders slides/pages as PNGs.", "Vision models can visually QA alignment."],
            ["<code>python ocr_doc.py scan.png --output text.txt</code>",
             "Tesseract OCR with image sharpening.", "Extracts text from low-contrast scans."],
            ["<code>python qa_doc.py model.xlsx</code>",
             "Safety audit for broken formulas.", "Asserts 0 errors (#REF!, #DIV/0!) and integrity."],
        ],
        [2.2 * inch, 2.2 * inch, 2.6 * inch],
        styles,
    )
    story.append(cli_table)

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 6: Zero Data Loss Guarantee
    # ============================================================
    story.append(Spacer(1, 2.0 * inch))
    story.append(Paragraph("CHAPTER 6", styles["chapter_label"]))
    story.append(Paragraph("The Zero Unintentional<br/>Data Loss Guarantee", styles["chapter_title"]))
    story.append(HRFlowable(width=2*inch, thickness=2, color=C["accent"],
                             spaceAfter=20, spaceBefore=8, hAlign="CENTER"))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph(
        "Every developer's greatest fear is an AI agent running a destructive command and permanently "
        "deleting work. Document OS implements three strict behavioral safeguards:",
        styles["body"]
    ))
    story.append(Paragraph(
        '1.&nbsp;&nbsp;<b>Read-Only by Default</b>: The agent never modifies an original file in place without '
        'creating a versioned duplicate (e.g., <code>report_v2.docx</code>) unless you explicitly request it.',
        styles["bullet_num"]
    ))
    story.append(Paragraph(
        '2.&nbsp;&nbsp;<b>Formula Protection</b>: If an Excel file contains formulas, the agent is strictly '
        'forbidden from replacing them with static numbers.',
        styles["bullet_num"]
    ))
    story.append(Paragraph(
        '3.&nbsp;&nbsp;<b>Mandatory Self-Audit</b>: The agent cannot report a task as "Complete" until '
        '<code>qa_doc.py</code> validates the resulting file is 100% corruption-free.',
        styles["bullet_num"]
    ))

    story.append(Spacer(1, 12))
    story.append(make_callout(
        "These safety guarantees are encoded as agent rules in <code>GEMINI.md</code>, "
        "<code>AGENTS.md</code>, and <code>document-safety.md</code>. They are enforced "
        "automatically — you don't need to remember or configure them.",
        "SAFETY GUARANTEE", styles, "warning"
    ))

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 7: Cross-Harness
    # ============================================================
    story.append(Spacer(1, 2.0 * inch))
    story.append(Paragraph("CHAPTER 7", styles["chapter_label"]))
    story.append(Paragraph("Cross-Harness Freedom:<br/>Claude Code, OpenCode, Cursor", styles["chapter_title"]))
    story.append(HRFlowable(width=2*inch, thickness=2, color=C["accent"],
                             spaceAfter=20, spaceBefore=8, hAlign="CENTER"))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph(
        "Document OS is built on open standards that work across multiple AI agent platforms:",
        styles["body"]
    ))

    compat_table = make_table(
        ["Platform", "Installation Path", "Export Command"],
        [
            ["<b>Google Antigravity</b>", "<code>.agents/plugins/document-os/</code>", "Native — no export needed"],
            ["<b>Claude Code</b>", "<code>~/.claude/skills/document-os/</code>",
             "<code>.\\export_cross_harness.ps1 -Target ClaudeCode</code>"],
            ["<b>OpenCode CLI</b>", "<code>~/.config/opencode/skills/</code>",
             "<code>.\\export_cross_harness.ps1 -Target OpenCode</code>"],
            ["<b>Cursor</b>", "<code>.cursor/skills/document-os/</code>",
             "<code>.\\export_cross_harness.ps1 -Target Cursor</code>"],
        ],
        [1.4 * inch, 2.6 * inch, 3.0 * inch],
        styles,
    )
    story.append(compat_table)

    story.append(PageBreak())

    # ============================================================
    # CHAPTER 8: Brand Identity & Styling
    # ============================================================
    story.append(Spacer(1, 2.0 * inch))
    story.append(Paragraph("CHAPTER 8", styles["chapter_label"]))
    story.append(Paragraph("Brand Identity &amp;<br/>Professional Document Styling", styles["chapter_title"]))
    story.append(HRFlowable(width=2*inch, thickness=2, color=C["accent"],
                             spaceAfter=20, spaceBefore=8, hAlign="CENTER"))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph(
        "Document OS v3.0 introduces a built-in <b>Brand Identity Skill</b> that enforces consistent visual "
        "standards across all generated documents and web pages. The brand system includes:",
        styles["body"]
    ))
    story.append(Paragraph("• <b>Color Palette</b>: Royal Blue (#1A3A8F), Golden Yellow (#FFC107), Deep Navy (#0D1B4C)", styles["bullet"]))
    story.append(Paragraph("• <b>Typography</b>: Playfair Display for headings, Source Sans 3 for body text, JetBrains Mono for code", styles["bullet"]))
    story.append(Paragraph("• <b>Page Layout</b>: KDP-compliant margins, chapter opener formatting, running headers and footers", styles["bullet"]))
    story.append(Paragraph("• <b>Web Tokens</b>: CSS custom properties for consistent web page styling", styles["bullet"]))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "The brand tokens are stored in a machine-readable JSON file at "
        "<code>.agents/skills/brand-identity/resources/brand-tokens.json</code> "
        "and can be consumed by any script or template in the Document OS ecosystem.",
        styles["body"]
    ))

    story.append(Spacer(1, 8))
    story.append(make_callout(
        "This very guide was generated using the Brand Identity Skill and the professional PDF engine "
        "in <code>build_professional_pdf.py</code>. Every element — from the chapter openers to the callout "
        "boxes to the table styling — follows the brand tokens defined in the skill.",
        "DOGFOODED", styles, "success"
    ))

    story.append(PageBreak())

    # ============================================================
    # ABOUT THE AUTHOR
    # ============================================================
    story.append(Spacer(1, 2.0 * inch))
    story.append(Paragraph("About the Author", styles["h1"]))
    story.append(accent_rule())
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph(
        '<b>Ekpo Otu, Ph.D.</b> is a Computer Professional, Full Stack Developer, '
        'Researcher, Author, and Lecturer with a passion for using computational technology '
        'to solve real-world problems. His work spans AI and machine learning, agentic systems, '
        'document engineering, and open-source tooling.',
        styles["body"]
    ))
    story.append(Spacer(1, 12))

    links_table = make_table(
        ["Platform", "Link"],
        [
            ["Author Bio &amp; Links", '<a href="https://linktr.ee/ekpootu" color="#1A3A8F">linktr.ee/ekpootu</a>'],
            ["GitHub", '<a href="https://github.com/ekpootu" color="#1A3A8F">github.com/ekpootu</a>'],
            ["Support This Project", '<a href="https://www.buymeacoffee.com/ekpootu" color="#1A3A8F">buymeacoffee.com/ekpootu</a>'],
        ],
        [2.0 * inch, 5.0 * inch],
        styles,
    )
    story.append(links_table)

    story.append(Spacer(1, 0.5 * inch))

    # Support box
    support_box = Table(
        [[
            Paragraph(
                '☕ <b>Support Open-Source Document Engineering</b><br/><br/>'
                'Document OS is completely free and open source under the MIT License. '
                'If this project saved your financial models, corporate decks, or client contracts '
                'from being shredded by an AI agent, consider fueling ongoing development!<br/><br/>'
                '<b><a href="https://www.buymeacoffee.com/ekpootu" color="#1A3A8F">'
                'buymeacoffee.com/ekpootu</a></b>',
                ParagraphStyle("support_text", fontName=fonts["body"],
                                fontSize=10, leading=16, textColor=C["body"],
                                alignment=TA_CENTER)
            )
        ]],
        colWidths=[6.0 * inch],
    )
    support_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF8E1")),
        ("BOX", (0, 0), (-1, -1), 1.5, C["accent"]),
        ("TOPPADDING", (0, 0), (-1, -1), 20),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
        ("LEFTPADDING", (0, 0), (-1, -1), 24),
        ("RIGHTPADDING", (0, 0), (-1, -1), 24),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    support_wrapper = Table([[support_box]], colWidths=[7.0 * inch])
    support_wrapper.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    story.append(support_wrapper)

    story.append(Spacer(1, 0.5 * inch))
    story.append(thin_rule())
    story.append(Paragraph(
        '<i>Antigravity Document Operating System (Document OS) • User Guide v3.0 • Licensed under MIT</i>',
        styles["footer_meta"]
    ))

    # --- Build ---
    def canvas_maker(*args, **kwargs):
        return ProfessionalCanvas(*args, fonts=fonts, **kwargs)

    doc.build(story, canvasmaker=canvas_maker)
    print(f"\n[OK] Successfully generated professional PDF: {output_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("  Antigravity Document OS — Professional PDF Builder v3")
    print("  Brand: Royal Blue • Golden Yellow • Deep Navy")
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
             Path("docs/Antigravity_Document_OS_Comprehensive_Guide_v3.pdf")
    build_guide(output, fonts, styles)


if __name__ == "__main__":
    main()
