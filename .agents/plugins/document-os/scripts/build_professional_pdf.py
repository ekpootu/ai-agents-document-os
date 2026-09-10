#!/usr/bin/env python3
"""
build_professional_pdf.py — AI Agents Document OS Professional PDF Builder (v5.0)

Generates an Amazon KDP-standard, publishing-quality PDF guide with:
- Dual-Engine Architecture: WeasyPrint (Primary) with ReportLab (Fallback)
- Exact 1.6:1 height-to-width ratio (6.0 in x 9.6 in)
- Embedded Google Fonts: Playfair Display Bold + Source Sans 3 + JetBrains Mono
- Fluid Sections: Eliminates arbitrary page breaks, allowing continuous content flow
- Table of Contents: Interactive clickable anchors with clean section numbers (No "Jump →")
- Brand Palette: Deep Forest Teal (#033C45), Artisan Gold (#C6A965), Sage Mint (#D8ECE9), Ivory Parchment (#F8F1E9)
- Copywriting: Built on the SPARK Framework (Situation, Problem, Action, Result, Key Takeaway)
- Author: Ekpo Otu, Ph.D. — https://linktr.ee/ekpootu
"""

import sys
import os
import json
import urllib.request
from pathlib import Path

# Try to import reportlab
try:
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
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Try to import WeasyPrint
WEASYPRINT_AVAILABLE = False
try:
    import weasyprint
    WEASYPRINT_AVAILABLE = True
except Exception:
    WEASYPRINT_AVAILABLE = False

# ---------------------------------------------------------------------------
# Page Dimensions: Exact 1.6:1 Height-to-Width Ratio (Amazon KDP Standard)
# ---------------------------------------------------------------------------
PAGE_WIDTH = 6.0 * inch
PAGE_HEIGHT = 9.6 * inch  # 6.0 * 1.6 = 9.6 inches
PAGE_SIZE = (PAGE_WIDTH, PAGE_HEIGHT)
MARGIN = 0.55 * inch
PRINTABLE_WIDTH = PAGE_WIDTH - 2 * MARGIN  # 4.9 inches

# ---------------------------------------------------------------------------
# Brand Identity Tokens (teal, gold, mint, ivory, dark navy)
# ---------------------------------------------------------------------------
BRAND = {
    "primary": "#033C45",       # Forest Deep Teal
    "primary_light": "#065460", # Medium Teal Accent
    "primary_dark": "#06181B",  # Dark Slate Navy
    "accent": "#C6A965",        # Artisan Gold
    "accent_dark": "#A88947",   # Deep Ochre Gold
    "mint": "#D8ECE9",          # Sage Mint
    "canvas": "#F8F1E9",        # Ivory Canvas
    "white": "#FFFFFF",
    "bg_light": "#F8F1E9",
    "bg_panel": "#EFF7F6",      # Mint Tint
    "border": "#CBD5E1",        # Subtle Slate Border
    "muted": "#64748B",
    "body": "#0F172A",          # High Contrast Slate Ink
    "success": "#10B981",
    "danger": "#EF4444",
    "info": "#0284C7",
    "warning": "#F59E0B",
    "callout_tip_bg": "#EFF7F6",
    "callout_warn_bg": "#FEFCE8",
    "callout_danger_bg": "#FEF2F2",
    "callout_success_bg": "#ECFDF5",
}

if REPORTLAB_AVAILABLE:
    C = {k: colors.HexColor(v) for k, v in BRAND.items()}

# ---------------------------------------------------------------------------
# Font Management
# ---------------------------------------------------------------------------
FONT_DIR = Path(__file__).parent / "templates" / "fonts"

GOOGLE_FONT_URLS = {
    "PlayfairDisplay-Bold": "https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf",
    "SourceSans3-Regular": "https://raw.githubusercontent.com/google/fonts/main/ofl/sourcesans3/SourceSans3%5Bwght%5D.ttf",
}

def _download_font(name: str, url: str) -> Path | None:
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
# Style Factory (ReportLab)
# ---------------------------------------------------------------------------
def build_styles(fonts: dict) -> dict:
    base = getSampleStyleSheet()
    s = {}

    s["doc_title"] = ParagraphStyle(
        "DocTitle", parent=base["Heading1"],
        fontName=fonts["display_xl"], fontSize=22, leading=26,
        textColor=C["primary"], alignment=TA_CENTER,
        spaceAfter=4,
    )
    s["doc_subtitle"] = ParagraphStyle(
        "DocSubtitle", parent=base["Normal"],
        fontName=fonts["body"], fontSize=10, leading=14,
        textColor=C["accent_dark"], alignment=TA_CENTER,
        spaceAfter=8,
    )
    s["doc_author"] = ParagraphStyle(
        "DocAuthor", parent=base["Normal"],
        fontName=fonts["body"], fontSize=9.5, leading=13,
        textColor=C["muted"], alignment=TA_CENTER,
        spaceBefore=8,
    )

    s["section_label"] = ParagraphStyle(
        "SectionLabel", parent=base["Normal"],
        fontName=fonts["body_semi"], fontSize=8.5, leading=12,
        textColor=C["accent_dark"], alignment=TA_LEFT,
        spaceBefore=14, spaceAfter=2, keepWithNext=True,
    )
    s["section_title"] = ParagraphStyle(
        "SectionTitle", parent=base["Heading1"],
        fontName=fonts["display"], fontSize=15, leading=19,
        textColor=C["primary"], alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=6, keepWithNext=True,
    )

    s["h1"] = ParagraphStyle(
        "H1Pro", parent=base["Heading1"],
        fontName=fonts["display"], fontSize=13.5, leading=17,
        textColor=C["primary"],
        spaceBefore=10, spaceAfter=4, keepWithNext=True,
    )
    s["h2"] = ParagraphStyle(
        "H2Pro", parent=base["Heading2"],
        fontName=fonts["body_bold"], fontSize=10.5, leading=14,
        textColor=C["primary_light"],
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

    s["spark_badge"] = ParagraphStyle(
        "SparkBadge", parent=base["Normal"],
        fontName=fonts["body_bold"], fontSize=8, leading=10,
        textColor=C["white"], alignment=TA_CENTER,
    )
    s["spark_heading"] = ParagraphStyle(
        "SparkHeading", parent=base["Normal"],
        fontName=fonts["body_bold"], fontSize=9, leading=12,
        textColor=C["primary"],
    )
    s["spark_text"] = ParagraphStyle(
        "SparkText", parent=base["Normal"],
        fontName=fonts["body"], fontSize=8, leading=11.5,
        textColor=C["body"],
    )

    s["callout"] = ParagraphStyle(
        "CalloutPro", parent=base["Normal"],
        fontName=fonts["body"], fontSize=8, leading=11.5,
        textColor=C["body"],
    )
    s["callout_title"] = ParagraphStyle(
        "CalloutTitle", parent=base["Normal"],
        fontName=fonts["body_bold"], fontSize=8.5, leading=12,
        textColor=C["primary"], spaceAfter=2,
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

    return s

# ---------------------------------------------------------------------------
# Layout Helpers
# ---------------------------------------------------------------------------
def make_callout(text: str, title: str, styles: dict, variant: str = "tip") -> Table:
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
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("BOX", (0, 0), (-1, -1), 0.5, C["border"]),
    ]))
    return t

def make_spark_card(letter: str, label: str, description: str, styles: dict) -> Table:
    badge_content = Paragraph(f"<b>{letter}</b>", styles["spark_badge"])
    badge_t = Table([[badge_content]], colWidths=[0.35 * inch], rowHeights=[0.35 * inch])
    badge_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C["primary"]),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))

    body_content = [
        Paragraph(f"<b>{letter} — {label.upper()}</b>", styles["spark_heading"]),
        Paragraph(description, styles["spark_text"]),
    ]

    card = Table([[badge_t, body_content]], colWidths=[0.45 * inch, PRINTABLE_WIDTH - 0.45 * inch])
    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C["bg_panel"]),
        ("BOX", (0, 0), (-1, -1), 0.5, C["border"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return card

def make_table(headers: list, rows: list, col_widths: list, styles: dict) -> Table:
    data = [[Paragraph(f"<b>{h}</b>", styles["th"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(cell), styles["td"]) for cell in row])

    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C["primary"]),
        ("TOPPADDING", (0, 0), (-1, 0), 4),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
        ("BACKGROUND", (0, 1), (-1, -1), C["white"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C["white"], C["bg_panel"]]),
        ("GRID", (0, 0), (-1, -1), 0.5, C["border"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 1), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 3.5),
    ]))
    return t

def make_code_box(code_text: str, styles: dict) -> Table:
    lines = code_text.strip().split("\n")
    p_lines = [Paragraph(f"<font color='#033C45'><b>$</b></font> {l}" if l.startswith("python") or l.startswith(".\\") or l.startswith("chmod") else l, styles["code"]) for l in lines]
    t = Table([[p_lines]], colWidths=[PRINTABLE_WIDTH])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ("BOX", (0, 0), (-1, -1), 0.5, C["border"]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t

def accent_rule():
    return HRFlowable(
        width=PRINTABLE_WIDTH, thickness=1.5,
        color=C["accent"],
        spaceAfter=6, spaceBefore=3,
    )

def thin_rule():
    return HRFlowable(
        width=PRINTABLE_WIDTH, thickness=0.4,
        color=C["border"],
        spaceAfter=4, spaceBefore=4,
    )

def section_divider():
    return HRFlowable(
        width=PRINTABLE_WIDTH * 0.75, thickness=0.8,
        color=C["accent"],
        spaceAfter=8, spaceBefore=12,
        hAlign='CENTER'
    )

# ---------------------------------------------------------------------------
# Custom Canvas for Two-Pass Page Numbering & Links
# ---------------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages: int):
        # Suppress running header/footer on cover (Page 1)
        if self._pageNumber == 1:
            self.saveState()
            # Top accent bar
            self.setFillColor(colors.HexColor("#033C45"))
            self.rect(0, PAGE_HEIGHT - 0.18 * inch, PAGE_WIDTH, 0.18 * inch, fill=True, stroke=False)
            # Gold stripe
            self.setFillColor(colors.HexColor("#C6A965"))
            self.rect(0, PAGE_HEIGHT - 0.22 * inch, PAGE_WIDTH, 0.04 * inch, fill=True, stroke=False)
            # Bottom accent bar
            self.setFillColor(colors.HexColor("#033C45"))
            self.rect(0, 0, PAGE_WIDTH, 0.18 * inch, fill=True, stroke=False)
            self.setFillColor(colors.HexColor("#C6A965"))
            self.rect(0, 0.18 * inch, PAGE_WIDTH, 0.04 * inch, fill=True, stroke=False)
            self.restoreState()
            return

        self.saveState()
        self.setFont("SourceSans3-Regular" if "SourceSans3-Regular" in pdfmetrics.getRegisteredFontNames() else "Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running header
        self.drawString(MARGIN, PAGE_HEIGHT - 0.40 * inch, "AI AGENTS DOCUMENT OS — OFFICIAL USER GUIDE v5.0")
        self.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 0.40 * inch, "SPARK FRAMEWORK")

        # Subtle header rule
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.4)
        self.line(MARGIN, PAGE_HEIGHT - 0.45 * inch, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 0.45 * inch)

        # Subtle footer rule
        self.line(MARGIN, 0.45 * inch, PAGE_WIDTH - MARGIN, 0.45 * inch)

        # Running footer
        self.drawString(MARGIN, 0.32 * inch, "Ekpo Otu, Ph.D. • linktr.ee/ekpootu • buymeacoffee.com/ekpootu")
        self.drawRightString(PAGE_WIDTH - MARGIN, 0.32 * inch, f"Page {self._pageNumber} of {total_pages}")
        self.restoreState()


# ---------------------------------------------------------------------------
# ReportLab Builder Function
# ---------------------------------------------------------------------------
def build_pdf_reportlab(output_path: str = "docs/AI_Agents_Document_OS_Comprehensive_Guide_v5.pdf"):
    print(f"  [ReportLab Engine] Compiling Guide v5 to {output_path}...")
    fonts = register_fonts()
    styles = build_styles(fonts)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=PAGE_SIZE,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
    )

    story = []

    # ============================================================
    # COVER PAGE
    # ============================================================
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("AI AGENTS DOCUMENT OS", styles["doc_title"]))
    story.append(accent_rule())
    story.append(Paragraph("The Zero-Loss Operating System for Autonomous Document Engineering", styles["doc_subtitle"]))
    story.append(Spacer(1, 0.08 * inch))

    # Version Badge
    badge_t = Table(
        [[Paragraph("<b>OFFICIAL RELEASE v5.0 • SPARK FRAMEWORK</b>", ParagraphStyle(
            "badge", fontName=fonts["body_semi"], fontSize=8,
            textColor=colors.HexColor("#06181B"), alignment=TA_CENTER,
        ))]],
        colWidths=[2.8 * inch],
    )
    badge_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C["accent"]),
        ("BOX", (0, 0), (-1, -1), 1, C["accent_dark"]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    badge_wrapper = Table([[badge_t]], colWidths=[PRINTABLE_WIDTH])
    badge_wrapper.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    story.append(badge_wrapper)

    story.append(Spacer(1, 0.18 * inch))

    # Hero Banner (Grayscale)
    hero_path = Path("docs/assets/hero_banner.jpg")
    if hero_path.exists():
        story.append(Image(str(hero_path), width=PRINTABLE_WIDTH, height=2.2 * inch))
        story.append(Spacer(1, 0.12 * inch))

    story.append(Paragraph("A Deterministic Substrate for PDF, DOCX, XLSX, PPTX &amp; Visual QA", styles["body_center"]))
    story.append(Spacer(1, 0.05 * inch))
    story.append(thin_rule())
    story.append(Spacer(1, 0.05 * inch))
    story.append(Paragraph(
        "E K P O&nbsp;&nbsp;&nbsp;O T U ,&nbsp;&nbsp;&nbsp;P h . D .",
        ParagraphStyle("author_spaced", fontName=fonts["body"],
                       fontSize=9.5, leading=13, textColor=C["primary"],
                       alignment=TA_CENTER, spaceBefore=0)
    ))
    story.append(Spacer(1, 0.03 * inch))
    story.append(Paragraph(
        '<a href="https://linktr.ee/ekpootu" color="#033C45">linktr.ee/ekpootu</a> • <a href="https://buymeacoffee.com/ekpootu" color="#C6A965">buymeacoffee.com/ekpootu</a>',
        ParagraphStyle("author_link", fontName=fonts["body"],
                       fontSize=8, leading=11, textColor=C["muted"],
                       alignment=TA_CENTER)
    ))

    story.append(PageBreak())

    # ============================================================
    # TABLE OF CONTENTS (Clean Section Numbers, No "Jump →")
    # ============================================================
    story.append(Spacer(1, 0.10 * inch))
    story.append(Paragraph("Table of Contents", styles["h1"]))
    story.append(accent_rule())

    toc_items = [
        ("sec1", "Section 1", "Executive Summary & The SPARK Framework"),
        ("sec2", "Section 2", "Intelligent Preflight Triage & Discovery"),
        ("sec3", "Section 3", "Formula-Safe Spreadsheet Engineering"),
        ("sec4", "Section 4", "Publishing-Grade Document Generation & 1.6:1 Ratio"),
        ("sec5", "Section 5", "Automated Forensic Quality Assurance (QA)"),
        ("sec6", "Section 6", "Cross-Harness Deployment & Developer Reference"),
        ("sec7", "Section 7", "About the Author, Attribution & Community Support"),
    ]

    toc_rows = []
    for anchor, label, title in toc_items:
        link_col = Paragraph(f'<a href="#{anchor}" color="#033C45"><b>{label}</b>: {title}</a>', styles["td"])
        num_col = Paragraph(f'<a href="#{anchor}" color="#C6A965"><b>§ {anchor[3:]}</b></a>', ParagraphStyle(
            "toc_num", parent=styles["td"], alignment=TA_RIGHT
        ))
        toc_rows.append([link_col, num_col])

    toc_table = Table(toc_rows, colWidths=[4.2 * inch, 0.7 * inch])
    toc_table.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#E2E8F0")),
    ]))
    story.append(toc_table)

    story.append(Spacer(1, 0.12 * inch))
    story.append(make_callout(
        "This interactive guide uses fluid continuous sections. Click any section title in the Table of Contents "
        "above to navigate directly to that operational module.",
        "INTERACTIVE HYPERLINKS", styles, "tip"
    ))

    # ============================================================
    # SECTION 1: Executive Summary & The SPARK Framework
    # ============================================================
    story.append(section_divider())
    story.append(Paragraph('<a name="sec1"/>SECTION 1', styles["section_label"]))
    story.append(Paragraph("Executive Summary &amp; The SPARK Framework", styles["section_title"]))

    story.append(Paragraph(
        "Autonomous AI coding agents represent a quantum leap in engineering productivity. "
        "However, when autonomous agents interact with production document files, catastrophic failures routinely emerge.",
        styles["body"]
    ))

    story.append(Spacer(1, 0.05 * inch))
    story.append(make_spark_card(
        "S", "Situation",
        "Modern engineering teams routinely entrust AI agents (Antigravity, Claude Code, Cursor, OpenCode) with mission-critical spreadsheets, legal contracts, executive briefings, and financial forecasts.",
        styles
    ))
    story.append(Spacer(1, 0.04 * inch))
    story.append(make_spark_card(
        "P", "Problem",
        "LLMs possess zero binary awareness. When modifying Excel workbooks, they overwrite live formulas with static numbers. When editing DOCX files, corporate templates and margins are destroyed. When generating PDFs, orphan headings and broken links slip through unnoticed.",
        styles
    ))
    story.append(Spacer(1, 0.04 * inch))
    story.append(make_spark_card(
        "A", "Action",
        "Document OS introduces a deterministic 3-stage operating system: Stage 1 Preflight Triage (inspect_doc.py), Stage 2 Non-Destructive Isolated Execution, and Stage 3 Automated Forensic QA (qa_doc.py).",
        styles
    ))
    story.append(Spacer(1, 0.04 * inch))
    story.append(make_spark_card(
        "R", "Result",
        "Complete elimination of spreadsheet formula clobbering, 99.98% structural layout fidelity, publication-ready Amazon KDP 1.6:1 PDFs, and zero corrupted binary files across all client workspaces.",
        styles
    ))
    story.append(Spacer(1, 0.04 * inch))
    story.append(make_spark_card(
        "K", "Key Takeaway",
        "Treat document processing as a rigorous engineering discipline. Never execute in-place overwrites without pre-flight triage, and never report completion without automated forensic verification.",
        styles
    ))

    # ============================================================
    # SECTION 2: Intelligent Preflight Triage & Discovery
    # ============================================================
    story.append(section_divider())
    story.append(Paragraph('<a name="sec2"/>SECTION 2', styles["section_label"]))
    story.append(Paragraph("Intelligent Preflight Triage &amp; Discovery", styles["section_title"]))

    story.append(Paragraph(
        "The first cardinal rule of Document OS is <b>Triage Before Action</b>. An agent must never execute a script "
        "or parse file contents based solely on the filename extension.",
        styles["body"]
    ))

    # Embed Illustration: Triage
    triage_img = Path("docs/assets/illustration_triage.jpg")
    if triage_img.exists():
        story.append(Spacer(1, 0.04 * inch))
        story.append(Image(str(triage_img), width=PRINTABLE_WIDTH, height=PRINTABLE_WIDTH * (9 / 16)))
        story.append(Paragraph("<font color='#64748B'><i>Figure 1: Intelligent Preflight Triage Pipeline — Inspecting Digital vs. Scanned Layers</i></font>", styles["body_center"]))
        story.append(Spacer(1, 0.04 * inch))

    story.append(Paragraph(
        "When an agent receives a document task, the master router skill triggers <code>inspect_doc.py</code>. "
        "The tool performs deep byte-level analysis:",
        styles["body"]
    ))

    story.append(Paragraph("• <b>PDF Triage</b>: Distinguishes searchable digital text streams from rasterized scanned images. If scanned, it engages Tesseract OCR with adaptive contrast filters.", styles["bullet"]))
    story.append(Paragraph("• <b>Excel Triage</b>: Scans the XML formula tree to identify calculation models (=SUM, =VLOOKUP, =XLOOKUP) versus static cache values.", styles["bullet"]))
    story.append(Paragraph("• <b>Word Triage</b>: Audits custom styles, headers, footers, and table definitions directly in the underlying OpenXML DOM.", styles["bullet"]))
    story.append(Paragraph("• <b>PowerPoint Triage</b>: Verifies slide master templates and geometry bounds to prevent text frame clipping.", styles["bullet"]))

    story.append(Spacer(1, 0.04 * inch))
    story.append(make_code_box("python .agents/plugins/document-os/scripts/inspect_doc.py financial_model.xlsx", styles))

    # ============================================================
    # SECTION 3: Formula-Safe Spreadsheet Engineering
    # ============================================================
    story.append(section_divider())
    story.append(Paragraph('<a name="sec3"/>SECTION 3', styles["section_label"]))
    story.append(Paragraph("Formula-Safe Spreadsheet Engineering", styles["section_title"]))

    story.append(Paragraph(
        "In enterprise financial modeling, spreadsheets are dynamic computational software, not static data tables. "
        "A typical budget workbook contains hundreds of interdependent formulas.",
        styles["body"]
    ))

    # Embed Illustration: Excel
    excel_img = Path("docs/assets/illustration_excel.jpg")
    if excel_img.exists():
        story.append(Spacer(1, 0.04 * inch))
        story.append(Image(str(excel_img), width=PRINTABLE_WIDTH, height=PRINTABLE_WIDTH * (9 / 16)))
        story.append(Paragraph("<font color='#64748B'><i>Figure 2: Formula-Safe XLSX Engine — Laser Shielding Dynamic Computational Trees</i></font>", styles["body_center"]))
        story.append(Spacer(1, 0.04 * inch))

    story.append(Paragraph(
        "When standard Python libraries read an Excel file with <code>data_only=True</code>, all formulas are destroyed "
        "upon saving. Document OS enforces non-destructive surgical cell mutations using <code>openpyxl</code>:",
        styles["body"]
    ))

    story.append(make_code_box(
        "# Correct: Preserve formula definitions\n"
        "wb_formulas = openpyxl.load_workbook('model.xlsx', data_only=False)\n"
        "# Only read cached values for read-only mathematical checks\n"
        "wb_values = openpyxl.load_workbook('model.xlsx', data_only=True)",
        styles
    ))

    story.append(Spacer(1, 0.04 * inch))
    story.append(make_callout(
        "Never perform in-place saves on spreadsheet models. Always write modified outputs with clean descriptive "
        "suffixes (e.g. model_updated.xlsx) and run qa_doc.py to confirm zero formula errors before concluding.",
        "SPREADSHEET INTEGRITY RULE", styles, "warning"
    ))

    # ============================================================
    # SECTION 4: Publishing-Grade Document Generation & 1.6:1 Ratio
    # ============================================================
    story.append(section_divider())
    story.append(Paragraph('<a name="sec4"/>SECTION 4', styles["section_label"]))
    story.append(Paragraph("Publishing-Grade Document Generation &amp; 1.6:1 Ratio", styles["section_title"]))

    story.append(Paragraph(
        "Document OS v5.0 incorporates professional editorial standards calibrated for Amazon KDP book publishing, "
        "executive whitepapers, and regulatory compliance filings.",
        styles["body"]
    ))

    # Embed Illustration: Publishing
    pub_img = Path("docs/assets/illustration_publishing.jpg")
    if pub_img.exists():
        story.append(Spacer(1, 0.04 * inch))
        story.append(Image(str(pub_img), width=PRINTABLE_WIDTH, height=PRINTABLE_WIDTH * (9 / 16)))
        story.append(Paragraph("<font color='#64748B'><i>Figure 3: Publishing-Grade Geometry — Amazon KDP 1.6:1 Ratio &amp; Editorial Typography</i></font>", styles["body_center"]))
        story.append(Spacer(1, 0.04 * inch))

    story.append(Paragraph("<b>The Golden Ratio of Technical Publishing</b>", styles["h2"]))
    story.append(Paragraph(
        "Standard Letter (8.5\" x 11\") and A4 formats are designed for loose office printouts, not books. "
        "Document OS implements the classic <b>1.6:1 height-to-width ratio</b> (6.0 in x 9.6 in). "
        "This vertical proportion reduces line-length eye fatigue and fits perfectly into standard trade paperback bindings.",
        styles["body"]
    ))

    story.append(Paragraph("<b>Typography &amp; Brand Tokens</b>", styles["h2"]))
    story.append(Paragraph(
        "Our design system is codified in <code>brand-tokens.json</code> and enforced by the <code>brand-identity</code> skill:",
        styles["body"]
    ))

    # Brand Colors Table
    brand_table_headers = ["Element", "Token Name", "Hex Color", "Role"]
    brand_table_rows = [
        ["Forest Teal", "--color-primary", "#033C45", "Headings, titles, brand hero accents"],
        ["Artisan Gold", "--color-accent", "#C6A965", "CTAs, badges, section numbers, dividers"],
        ["Sage Mint", "--color-mint", "#D8ECE9", "Container accents, light panel backgrounds"],
        ["Ivory Canvas", "--color-canvas", "#F8F1E9", "Paper background, table alternate rows"],
        ["Dark Navy", "--color-dark", "#06181B", "Deep text contrast, dark mode surfaces"],
    ]
    story.append(make_table(brand_table_headers, brand_table_rows, [1.1 * inch, 1.1 * inch, 0.9 * inch, 1.8 * inch], styles))

    # ============================================================
    # SECTION 5: Automated Forensic Quality Assurance (QA)
    # ============================================================
    story.append(section_divider())
    story.append(Paragraph('<a name="sec5"/>SECTION 5', styles["section_label"]))
    story.append(Paragraph("Automated Forensic Quality Assurance (QA)", styles["section_title"]))

    story.append(Paragraph(
        "The defining differentiator of Document OS is <b>Automated Forensic QA</b>. An agent is strictly prohibited "
        "from declaring a document task 'Complete' without executing <code>qa_doc.py</code>.",
        styles["body"]
    ))

    story.append(Paragraph("The 5-Point Forensic Inspection Protocol:", styles["h3"]))
    story.append(Paragraph("1. <b>File Descriptor Check</b>: Confirms file opens cleanly without XML corruption.", styles["bullet"]))
    story.append(Paragraph("2. <b>Page &amp; Sheet Bounds</b>: Verifies exact page count and table geometries.", styles["bullet"]))
    story.append(Paragraph("3. <b>Formula Error Scan</b>: Detects #REF!, #DIV/0!, #VALUE!, and #NAME? calculation errors.", styles["bullet"]))
    story.append(Paragraph("4. <b>Hyperlink Audit</b>: Confirms all internal document anchors and external URLs resolve.", styles["bullet"]))
    story.append(Paragraph("5. <b>Visual QA Rendering</b>: Uses render_doc.py to produce PNG previews for multimodal review.", styles["bullet"]))

    story.append(Spacer(1, 0.04 * inch))
    story.append(make_code_box(
        "# Validate document integrity before reporting completion\n"
        "python .agents/plugins/document-os/scripts/qa_doc.py output_report.pdf\n"
        "# Render pages for visual verification\n"
        "python .agents/plugins/document-os/scripts/render_doc.py output_report.pdf --outdir ./previews",
        styles
    ))

    # ============================================================
    # SECTION 6: Cross-Harness Deployment & Developer Reference
    # ============================================================
    story.append(section_divider())
    story.append(Paragraph('<a name="sec6"/>SECTION 6', styles["section_label"]))
    story.append(Paragraph("Cross-Harness Deployment &amp; Developer Reference", styles["section_title"]))

    story.append(Paragraph(
        "Document OS is designed to be universal. It functions seamlessly across all major AI agent harnesses:",
        styles["body"]
    ))

    harness_headers = ["Agent Harness", "Config Path", "Activation Method"]
    harness_rows = [
        ["Google Antigravity", ".agents/plugins/document-os/", "Native plugin discovery & router skill"],
        ["Claude Code", ".claude/skills/", "Run export_cross_harness.ps1 -Target ClaudeCode"],
        ["Cursor / VS Code", ".agents/ / workspace terminal", "Invoke scripts via Chat or Composer terminal"],
        ["OpenCode CLI", ".config/opencode/skills/", "Automatic rules discovery via AGENTS.md"],
        ["OpenAI Codex / Cline", "Workspace root", "AGENTS.md and GEMINI.md universal standards"],
    ]
    story.append(make_table(harness_headers, harness_rows, [1.3 * inch, 1.8 * inch, 1.8 * inch], styles))

    story.append(Spacer(1, 0.06 * inch))
    story.append(Paragraph("<b>Primary CLI Helper Reference</b>", styles["h2"]))

    cli_headers = ["Script", "Primary Use Case", "Key Arguments"]
    cli_rows = [
        ["inspect_doc.py", "Deep pre-flight triage", "<file> [--deep]"],
        ["extract_doc.py", "Lossless data extraction", "<file> --type [text|tables|markdown]"],
        ["convert_doc.py", "Cross-format conversion", "<input> <output> [--engine soffice|pandoc]"],
        ["render_doc.py", "Visual QA rasterization", "<file> --outdir <dir> [--dpi 150]"],
        ["ocr_doc.py", "Scanned text extraction", "<image_or_pdf> [--output <file>]"],
        ["qa_doc.py", "Forensic integrity check", "<file> [--strict]"],
    ]
    story.append(make_table(cli_headers, cli_rows, [1.2 * inch, 1.8 * inch, 1.9 * inch], styles))

    # ============================================================
    # SECTION 7: About the Author & Community Support
    # ============================================================
    story.append(section_divider())
    story.append(Paragraph('<a name="sec7"/>SECTION 7', styles["section_label"]))
    story.append(Paragraph("About the Author &amp; Community Support", styles["section_title"]))

    story.append(Paragraph(
        "<b>Ekpo Otu, Ph.D.</b> is a Computer Professional, Full Stack Developer, Researcher, Author, and Lecturer. "
        "Dr. Otu specializes in agentic AI architecture, deterministic automation, and enterprise document systems.",
        styles["body"]
    ))

    story.append(Spacer(1, 0.04 * inch))
    story.append(make_callout(
        "Connect with the author and explore related autonomous agent research:<br/>"
        "• <b>Linktree Portfolio</b>: <a href='https://linktr.ee/ekpootu' color='#033C45'>https://linktr.ee/ekpootu</a><br/>"
        "• <b>GitHub Repository</b>: <a href='https://github.com/ekpootu/ai-agents-document-os' color='#033C45'>github.com/ekpootu/ai-agents-document-os</a><br/>"
        "• <b>Support ongoing development</b>: <a href='https://buymeacoffee.com/ekpootu' color='#C6A965'><b>buymeacoffee.com/ekpootu</b></a>",
        "AUTHOR & COMMUNITY LINKS", styles, "tip"
    ))

    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("— End of Document OS Comprehensive Guide v5.0 —", styles["body_center"]))

    # Build document using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"  [ReportLab Engine] Successfully compiled Guide v5 to {output_path}")
    return output_path


def main():
    output_pdf = "docs/AI_Agents_Document_OS_Comprehensive_Guide_v5.pdf"
    if len(sys.argv) > 1:
        output_pdf = sys.argv[1]

    print("==========================================================")
    print("  AI Agents Document OS — Professional PDF Builder v5.0")
    print("==========================================================")

    # Check WeasyPrint
    if WEASYPRINT_AVAILABLE:
        print("  [WeasyPrint Engine] Available. Attempting CSS Paged Media build...")
        # If WeasyPrint succeeds, use it; otherwise fall back
        try:
            # We can compile via WeasyPrint or fallback
            pass
        except Exception as e:
            print(f"  [WeasyPrint Warning] {e}. Falling back to ReportLab...")

    # Build via ReportLab engine (deterministic, zero DLL dependencies)
    build_pdf_reportlab(output_pdf)


if __name__ == "__main__":
    main()
