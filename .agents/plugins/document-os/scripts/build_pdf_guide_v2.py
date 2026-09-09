#!/usr/bin/env python3
"""
build_pdf_guide_v2.py - Enhanced, Beginner-Friendly Document OS Guide Builder
Generates Antigravity_Document_OS_Comprehensive_Guide_v2.pdf with embedded infographics,
wrapped table cells (fixing margin overflow), beginner "How to Use" tutorials, and two-pass page numbering.
"""
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, Image, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas that computes total page count dynamically for Page X of Y footers."""
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

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Draw running header on pages > 1
        if self._pageNumber > 1:
            self.drawString(0.75 * inch, 10.4 * inch, "Antigravity Document Operating System (Document OS) — User Manual")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(0.75 * inch, 10.3 * inch, 7.75 * inch, 10.3 * inch)

        # Running footer on all pages
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(7.75 * inch, 0.45 * inch, footer_text)
        self.drawString(0.75 * inch, 0.45 * inch, "Confidential & Open Source • Powered by Antigravity AI Engine")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(0.75 * inch, 0.6 * inch, 7.75 * inch, 0.6 * inch)
        self.restoreState()

def create_guide_v2(output_pdf_path: Path):
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 8.5 x 11 inches. Margins: 0.75in. Printable width: 7.0 inches.
    doc = SimpleDocTemplate(
        str(output_pdf_path),
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    styles = getSampleStyleSheet()
    
    # Brand Palette
    c_primary = colors.HexColor("#0F172A")    # Slate 900
    c_secondary = colors.HexColor("#1E3A8A")  # Blue 900
    c_accent = colors.HexColor("#0284C7")     # Sky 600
    c_teal = colors.HexColor("#0D9488")       # Teal 600
    c_body = colors.HexColor("#334155")       # Slate 700
    c_bg_light = colors.HexColor("#F8FAFC")   # Slate 50
    c_callout_bg = colors.HexColor("#F0F9FF") # Sky 50
    c_border = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=c_primary,
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        spaceAfter=12
    )
    h1_style = ParagraphStyle(
        'H1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_secondary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_teal,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=c_body,
        spaceAfter=6
    )
    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4
    )
    code_inline = ParagraphStyle(
        'CodeInline',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#991B1B"),
        backColor=colors.HexColor("#FEF2F2")
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_body
    )
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )
    callout_text = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#0369A1")
    )

    def make_callout(text: str, title: str = "PRO TIP FOR BEGINNERS"):
        content = [
            Paragraph(f"<b>{title}:</b> {text}", callout_text)
        ]
        box = Table([[content]], colWidths=[7.0 * inch])
        box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), c_callout_bg),
            ('LINEBEFORE', (0, 0), (0, -1), 3, c_accent),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ]))
        return box

    story = []

    # ================= PAGE 1 =================
    # Title & Banner
    story.append(Paragraph("Antigravity Document Operating System (Document OS)", title_style))
    story.append(Paragraph("Complete Beginner-Friendly Guide & Practical Operational Manual (v2.0)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceAfter=8))

    # Hero Banner Image
    hero_img_path = Path("docs/assets/hero_banner.jpg")
    if hero_img_path.exists():
        # Printable width is 7.0 inches. 16:9 ratio -> height ~3.93 inches. Let's scale to 6.8 x 3.6
        img = Image(str(hero_img_path), width=7.0 * inch, height=3.5 * inch)
        story.append(img)
        story.append(Spacer(1, 8))

    # Welcome Section (Novice Friendly)
    story.append(Paragraph("Welcome! What is the Document Operating System?", h1_style))
    story.append(Paragraph(
        "If you have ever asked an AI assistant to <i>'read this PDF'</i>, <i>'edit this spreadsheet'</i>, or <i>'fix this PowerPoint presentation'</i>, "
        "you might have noticed that things often go wrong. Standard AI agents frequently hallucinate missing information, accidentally erase "
        "vital mathematical formulas in Excel, break document margins, or deliver files that won't even open.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Document OS is your AI agent's reliable co-pilot.</b> Think of it as an automated safety suite, forensic reader, and quality inspector all in one. "
        "It gives your Antigravity agent the specialized knowledge and precision tools needed to work with real documents without making mistakes or deleting your data.",
        body_style
    ))

    story.append(make_callout(
        "You do not need to memorize complex terminal commands or write Python code! You simply talk to your Antigravity agent in plain English. Document OS works automatically behind the scenes to safeguard your documents.",
        "NOVICE FRIENDLY"
    ))

    story.append(PageBreak())

    # ================= PAGE 2 =================
    story.append(Paragraph("1. Quickstart: How to Use Document OS Everyday", h1_style))
    story.append(Paragraph(
        "Using Document OS requires zero technical wizardry. When you converse with your Antigravity agent, the system automatically detects "
        "when you are dealing with files. Here are the 5 most common everyday scenarios and how to prompt your agent:",
        body_style
    ))

    # Real-World Scenario Examples in a Clean Table
    use_cases = [
        [
            Paragraph("<b>What You Want to Do</b>", table_header),
            Paragraph("<b>What You Prompt Your Agent (Plain English)</b>", table_header),
            Paragraph("<b>What Document OS Does Automatically Behind the Scenes</b>", table_header)
        ],
        [
            Paragraph("<b>Read & Summarize a PDF</b>", table_cell),
            Paragraph("<i>\"Read the attached 2024_Annual_Report.pdf and summarize the key revenue figures and executive milestones.\"</i>", table_cell),
            Paragraph("Automatically checks if the PDF is digital text or scanned imagery. Extracts tables cleanly without confusing columns.", table_cell)
        ],
        [
            Paragraph("<b>Edit an Excel Spreadsheet</b>", table_cell),
            Paragraph("<i>\"Update the Q3 projections in Financials.xlsx with a 5% increase in ad spend. Make sure all formulas stay intact.\"</i>", table_cell),
            Paragraph("Loads the workbook with formula preservation. Modifies numbers without overwriting =SUM() or =VLOOKUP(). Runs automated QA.", table_cell)
        ],
        [
            Paragraph("<b>Convert Formats Safely</b>", table_cell),
            Paragraph("<i>\"Convert this Word proposal Proposal_v1.docx into a presentation-ready PDF for my client meeting.\"</i>", table_cell),
            Paragraph("Invokes headless LibreOffice engine to convert vectors and fonts at 100% fidelity without misaligning margins.", table_cell)
        ],
        [
            Paragraph("<b>Create a Slide Deck</b>", table_cell),
            Paragraph("<i>\"Turn these meeting notes into a clean 5-slide PowerPoint deck using standard 16:9 widescreen layout.\"</i>", table_cell),
            Paragraph("Builds slides adhering to master templates, applies word wrap so text never overflows borders, and renders previews to verify.", table_cell)
        ],
        [
            Paragraph("<b>Extract from Scanned Receipts/Images</b>", table_cell),
            Paragraph("<i>\"Extract the vendor name, date, and itemized total from this scanned receipt invoice_scan.jpg.\"</i>", table_cell),
            Paragraph("Applies digital contrast sharpening and deskewing, then runs OCR engine to copy verbatim numbers accurately.", table_cell)
        ]
    ]

    use_cases_table = Table(use_cases, colWidths=[1.6 * inch, 2.5 * inch, 2.9 * inch])
    use_cases_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('BACKGROUND', (0, 1), (-1, -1), c_bg_light),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(use_cases_table)
    story.append(Spacer(1, 10))

    # Visual Workflow Infographic
    pipeline_img_path = Path("docs/assets/pipeline_infographic.jpg")
    if pipeline_img_path.exists():
        story.append(Paragraph("Visualizing the Automated Safety Pipeline", h2_style))
        img2 = Image(str(pipeline_img_path), width=7.0 * inch, height=3.2 * inch)
        story.append(img2)
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # ================= PAGE 3 =================
    story.append(Paragraph("2. The 5-Stage Safety Pipeline (Fixed Text Wrapping)", h1_style))
    story.append(Paragraph(
        "To ensure zero accidental data loss, every single document task passes through a 5-stage engineering pipeline. "
        "Notice that all objectives are systematically checked before returning results to you:",
        body_style
    ))

    # Fully Wrapped 5-Stage Lifecycle Table (Precisely 7.0 inches total)
    lifecycle_data_v2 = [
        [
            Paragraph("<b>Stage</b>", table_header),
            Paragraph("<b>Action</b>", table_header),
            Paragraph("<b>Tool / Helper</b>", table_header),
            Paragraph("<b>Verification & Quality Objective</b>", table_header)
        ],
        [
            Paragraph("<b>1. Triage</b>", table_cell),
            Paragraph("Preflight structural analysis", table_cell),
            Paragraph("<code>inspect_doc.py</code>", table_cell),
            Paragraph("Determines if PDF is digital text or scanned raster. Counts sheets and formulas in Excel. Checks slide aspect ratio (16:9 vs 4:3).", table_cell)
        ],
        [
            Paragraph("<b>2. Route</b>", table_cell),
            Paragraph("Specialist protocol selection", table_cell),
            Paragraph("<code>document-router</code>", table_cell),
            Paragraph("Selects the exact safe library (e.g. <i>openpyxl</i> with formula-protect, <i>pdfplumber</i> for grids, <i>python-docx</i> for styles).", table_cell)
        ],
        [
            Paragraph("<b>3. Execute</b>", table_cell),
            Paragraph("Deterministic processing", table_cell),
            Paragraph("<code>extract_doc.py</code><br/><code>convert_doc.py</code>", table_cell),
            Paragraph("Carries out the requested read, write, or conversion using pre-tested tools rather than hallucinated code.", table_cell)
        ],
        [
            Paragraph("<b>4. Render</b>", table_cell),
            Paragraph("Visual preview generation", table_cell),
            Paragraph("<code>render_doc.py</code>", table_cell),
            Paragraph("Converts slides or pages into high-resolution PNG preview images so the agent can visually review layout and spacing.", table_cell)
        ],
        [
            Paragraph("<b>5. QA Audit</b>", table_cell),
            Paragraph("Integrity & error check", table_cell),
            Paragraph("<code>qa_doc.py</code>", table_cell),
            Paragraph("Audits the completed file. Scans Excel for broken formula tokens (<b>#REF!</b>, <b>#DIV/0!</b>), confirms Word opens cleanly, and reports QA status.", table_cell)
        ]
    ]

    t_lifecycle_v2 = Table(lifecycle_data_v2, colWidths=[0.9 * inch, 1.4 * inch, 1.5 * inch, 3.2 * inch])
    t_lifecycle_v2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('BACKGROUND', (0, 1), (-1, -1), c_bg_light),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_lifecycle_v2)
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. Understanding Your Workspace & Global Deployment", h1_style))
    story.append(Paragraph(
        "Document OS is installed in two complementary locations to give you total flexibility:",
        body_style
    ))
    story.append(Paragraph("• <b>Local Workspace (<code>.agents/plugins/document-os/</code>)</b>: Ready to run in your current project folder. You can commit this to Git so your entire engineering team shares the exact same document rules.", bullet_style))
    story.append(Paragraph("• <b>Global Deployment (<code>~/.gemini/config/plugins/document-os/</code>)</b>: Installed directly into your personal Antigravity user profile. Every folder or project you ever open in Antigravity automatically enjoys Document OS superpowers!", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Cross-Harness Freedom (Claude Code, OpenCode CLI, Cursor)", h2_style))
    story.append(Paragraph(
        "You are never locked into a single AI tool! Document OS adheres to open Agent Skills standards. Run the included exporter:",
        body_style
    ))
    story.append(Paragraph("<code>.\\export_cross_harness.ps1 -Target All</code>", code_inline))
    story.append(Paragraph(
        "This instantly bridges your Document OS skills into <b>Claude Code</b> (<code>~/.claude/skills/</code>) and <b>OpenCode CLI</b> (<code>~/.config/opencode/skills/</code>).",
        body_style
    ))

    story.append(PageBreak())

    # ================= PAGE 4 =================
    story.append(Paragraph("4. Quick Reference CLI Command Cheat Sheet", h1_style))
    story.append(Paragraph(
        "For power users, automated scripts, or terminal workflows, you can also execute the Document OS CLI tools directly:",
        body_style
    ))

    cli_rows = [
        [
            Paragraph("<b>Command & Syntax</b>", table_header),
            Paragraph("<b>What It Does</b>", table_header),
            Paragraph("<b>Sample Output / Benefit</b>", table_header)
        ],
        [
            Paragraph("<code>python inspect_doc.py &lt;file&gt;</code>", table_cell),
            Paragraph("Analyzes any document format (PDF, DOCX, XLSX, PPTX, Image).", table_cell),
            Paragraph("Returns JSON with page count, sheet names, formula count, and scanned status.", table_cell)
        ],
        [
            Paragraph("<code>python extract_doc.py &lt;file&gt; --type tables</code>", table_cell),
            Paragraph("Pulls tabular data out of PDFs, Word files, or spreadsheets.", table_cell),
            Paragraph("Outputs pure Markdown tables ready to paste into reports or prompts.", table_cell)
        ],
        [
            Paragraph("<code>python convert_doc.py input.docx output.pdf</code>", table_cell),
            Paragraph("Converts documents using headless LibreOffice or Pandoc.", table_cell),
            Paragraph("Vector-perfect conversion without misalignment or font degradation.", table_cell)
        ],
        [
            Paragraph("<code>python render_doc.py presentation.pptx --outdir ./previews</code>", table_cell),
            Paragraph("Renders slide decks or PDF pages as crisp PNG images.", table_cell),
            Paragraph("Allows multi-modal vision models to visually QA alignment.", table_cell)
        ],
        [
            Paragraph("<code>python ocr_doc.py scan.png --output text.txt</code>", table_cell),
            Paragraph("Runs high-accuracy Tesseract OCR with automatic image sharpening.", table_cell),
            Paragraph("Extracts text from receipts, invoices, and low-contrast scanned scans.", table_cell)
        ],
        [
            Paragraph("<code>python qa_doc.py financial_model.xlsx</code>", table_cell),
            Paragraph("Performs safety audit and scans for broken formula errors.", table_cell),
            Paragraph("Asserts 0 formula errors (#REF!, #DIV/0!) and checks file integrity.", table_cell)
        ]
    ]

    t_cli = Table(cli_rows, colWidths=[2.3 * inch, 2.3 * inch, 2.4 * inch])
    t_cli.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('BACKGROUND', (0, 1), (-1, -1), c_bg_light),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_cli)
    story.append(Spacer(1, 12))

    story.append(Paragraph("5. The Zero Unintentional Data Loss Guarantee", h1_style))
    story.append(Paragraph(
        "Every developer's greatest fear is an AI agent running a destructive command and permanently deleting work. "
        "Document OS implements three strict behavioral safeguards encoded in <code>GEMINI.md</code> and <code>document-safety.md</code>:",
        body_style
    ))
    story.append(Paragraph("1. <b>Read-Only by Default</b>: The agent will never modify an original file in place without creating a versioned duplicate (e.g. <code>report_v2.docx</code>) unless you explicitly type: <i>'Overwrite the original file'</i>.", bullet_style))
    story.append(Paragraph("2. <b>Formula Protection</b>: If an Excel file contains formulas, the agent is strictly forbidden from replacing them with static numbers.", bullet_style))
    story.append(Paragraph("3. <b>Mandatory Self-Audit</b>: The agent cannot report a task as 'Complete' until <code>qa_doc.py</code> validates that the resulting file is 100% free of corruption.", bullet_style))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceAfter=8))
    story.append(Paragraph(
        "<i>Antigravity Document Operating System (Document OS) • User Guide v2.0 • Licensed under MIT</i>",
        ParagraphStyle('FooterMeta', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, textColor=colors.gray, alignment=1)
    ))

    # Build PDF with dynamic NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated v2 PDF guide at: {output_pdf_path}")

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/Antigravity_Document_OS_Comprehensive_Guide_v2.pdf")
    create_guide_v2(target)
