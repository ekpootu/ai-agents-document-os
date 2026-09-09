#!/usr/bin/env python3
"""
build_pdf_guide.py - Official Document OS User Guide PDF Builder
Dogfoods ReportLab Platypus engine to compile an authoritative, beautifully styled PDF user manual.
"""
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable

def create_guide(output_pdf_path: Path):
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_pdf_path),
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    styles = getSampleStyleSheet()
    
    # Custom color palette
    primary_color = colors.HexColor("#1A365D")   # Deep navy
    secondary_color = colors.HexColor("#2B6CB0") # Vibrant blue
    accent_color = colors.HexColor("#319795")    # Teal accent
    dark_neutral = colors.HexColor("#2D3748")    # Charcoal body text
    light_bg = colors.HexColor("#F7FAFC")        # Soft grey background
    border_color = colors.HexColor("#E2E8F0")

    # Custom typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=primary_color,
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=secondary_color,
        spaceAfter=15
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=dark_neutral,
        spaceAfter=8
    )
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#742A2A"),
        backColor=colors.HexColor("#FFF5F5"),
        spaceBefore=4,
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    story = []

    # Title & Metadata Banner
    story.append(Paragraph("Antigravity Document Operating System", title_style))
    story.append(Paragraph("The Engineering Standard for Autonomous Document Operations Across Agent Harnesses", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=primary_color, spaceAfter=15))

    # Executive Overview
    story.append(Paragraph("1. Executive Architecture Overview", h1_style))
    story.append(Paragraph(
        "Modern LLM agents frequently fail when interacting with real-world documents. Common failure modes include "
        "destructive in-place overwrites, stripping live spreadsheet formulas into dead text, destroying multi-column "
        "layouts in Word documents, and overflowing PowerPoint slide boundaries. The <b>Antigravity Document Operating System (Document OS)</b> "
        "replaces impromptu code hallucination with a deterministic, multi-stage engineering substrate.",
        body_style
    ))
    story.append(Paragraph(
        "Rather than installing disjointed standalone skills from assorted portals, Document OS packages a master format router, "
        "format-specific procedural protocols, safety rules, and battle-tested local Python CLI utilities into a unified, portable architecture.",
        body_style
    ))

    # Lifecycle Table
    story.append(Paragraph("The 5-Stage Document Lifecycle", h2_style))
    lifecycle_data = [
        ["Stage", "Action", "Tool / Script", "Verification Objective"],
        ["1. Triage", "Preflight structure analysis", "inspect_doc.py", "Identify MIME, digital vs. scanned layers, sheets, formulas"],
        ["2. Route", "Format protocol selection", "document-router", "Select optimal toolchain (PDF, DOCX, XLSX, PPTX, OCR)"],
        ["3. Execute", "Deterministic processing", "extract / convert_doc", "Execute Python library or headless LibreOffice/Pandoc engine"],
        ["4. Render", "Visual verification preview", "render_doc.py", "Generate high-resolution PNG previews for multi-modal review"],
        ["5. QA", "Structural integrity check", "qa_doc.py", "Scan formula errors (#REF!), validate OOXML tree, confirm page bounds"]
    ]
    t = Table(lifecycle_data, colWidths=[1.1*inch, 1.6*inch, 1.7*inch, 2.6*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('BACKGROUND', (0, 1), (-1, -1), light_bg),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    # How to Use: Workspace vs Global
    story.append(Paragraph("2. Deployment & Usage Models", h1_style))
    story.append(Paragraph(
        "Document OS is designed for dual deployment: it can run isolated within a specific project repository or installed "
        "globally across your machine for every Antigravity project.",
        body_style
    ))

    story.append(Paragraph("A. Workspace Deployment (.agents/)", h2_style))
    story.append(Paragraph(
        "When stored in <code>.agents/plugins/document-os/</code> and accompanied by a root <code>GEMINI.md</code>, "
        "the agent automatically discovers the plugin and rules upon launching within the directory. This enables team "
        "collaboration by checking Document OS directly into your project's Git repository.",
        body_style
    ))
    story.append(Paragraph("Command line invocation example:", body_style))
    story.append(Paragraph("python .agents/plugins/document-os/scripts/inspect_doc.py financial_model.xlsx", code_style))

    story.append(Paragraph("B. Global Deployment (~/.gemini/config/)", h2_style))
    story.append(Paragraph(
        "To make Document OS available to <i>any</i> folder or repository opened in Antigravity, deploy it to your global "
        "configuration directory. Run the automated PowerShell installer with the global deployment flag:",
        body_style
    ))
    story.append(Paragraph(".\\install_document_os.ps1 -DeployGlobal", code_style))
    story.append(Paragraph(
        "This copies the plugin to <code>$HOME\\.gemini\\config\\plugins\\document-os\\</code>, making the skills and rules "
        "universally available across every agent session on your workstation.",
        body_style
    ))

    story.append(PageBreak())

    # Format Specific Protocols
    story.append(Paragraph("3. Format Engineering Protocols", h1_style))
    
    story.append(Paragraph("Portable Document Format (PDF)", h2_style))
    story.append(Paragraph("• <b>Digital PDFs</b>: Extract structural text streams with <code>pypdf</code>. Extract grid tables with <code>pdfplumber</code>.", bullet_style))
    story.append(Paragraph("• <b>Scanned PDFs</b>: Render pages to 300 DPI raster images, apply Otsu contrast thresholding, and run Tesseract OCR.", bullet_style))
    story.append(Paragraph("• <b>Generation</b>: Use programmatic Flowables via ReportLab (avoid manual string concatenation).", bullet_style))

    story.append(Paragraph("Microsoft Word (DOCX)", h2_style))
    story.append(Paragraph("• <b>Semantic Styles</b>: Modify runs and paragraphs using Word styles rather than ad-hoc inline font styling.", bullet_style))
    story.append(Paragraph("• <b>Structural Preservation</b>: Retain section properties (headers, footers, margins) during in-place edits.", bullet_style))
    story.append(Paragraph("• <b>Conversions</b>: Headless LibreOffice provides 100% vector-faithful DOCX &rarr; PDF rendering.", bullet_style))

    story.append(Paragraph("Microsoft Excel (XLSX)", h2_style))
    story.append(Paragraph("• <b>The Cardinal Rule</b>: Never clobber live calculation formulas (e.g. <code>=SUM()</code>) with static scalar values.", bullet_style))
    story.append(Paragraph("• <b>Multi-Sheet Integrity</b>: Inspect all sheets before queries. Check formula graphs for downstream dependencies.", bullet_style))
    story.append(Paragraph("• <b>Automated Formula Error Scan</b>: <code>qa_doc.py</code> scans for <code>#REF!</code>, <code>#VALUE!</code>, and <code>#DIV/0!</code> tokens.", bullet_style))

    story.append(Paragraph("Microsoft PowerPoint (PPTX)", h2_style))
    story.append(Paragraph("• <b>Slide Master Layouts</b>: Inherit from standard master slide archetypes (16:9 widescreen default).", bullet_style))
    story.append(Paragraph("• <b>Overflow Defense</b>: Enforce bounding box constraints and word wrap to prevent clipped bullet points.", bullet_style))
    story.append(Paragraph("• <b>Visual QA</b>: Automatically export slides to PDF and render to PNGs for vision-model layout validation.", bullet_style))

    story.append(Spacer(1, 10))

    # Cross Harness Portability
    story.append(Paragraph("4. Cross-Harness Portability", h1_style))
    story.append(Paragraph(
        "Document OS strictly follows the open <b>Agent Skills Standard</b> (YAML frontmatter + progressive markdown). "
        "The underlying Python CLI utilities are 100% standalone and platform-agnostic. Use the cross-harness exporter:",
        body_style
    ))
    story.append(Paragraph(".\\export_cross_harness.ps1 -Target ClaudeCode", code_style))
    story.append(Paragraph(".\\export_cross_harness.ps1 -Target OpenCode", code_style))

    portability_data = [
        ["Agent Harness", "Standard Customization Path", "Integration Method"],
        ["Google Antigravity", ".agents/plugins/ or ~/.gemini/config/plugins/", "Native Plugin discovery & progressive disclosure"],
        ["Claude Code", ".claude/skills/ or ~/.claude/skills/", "Agent Skills directory export"],
        ["OpenCode CLI / Cursor", ".skills/ or ~/.config/opencode/skills/", "Universal symlink & standalone CLI tool access"]
    ]
    t2 = Table(portability_data, colWidths=[1.8*inch, 2.8*inch, 2.4*inch])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), secondary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('BACKGROUND', (0, 1), (-1, -1), light_bg),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t2)

    story.append(Spacer(1, 15))

    # CLI Helper Reference
    story.append(Paragraph("5. CLI Helper Command Cheat Sheet", h1_style))
    cli_data = [
        ["Script", "Key Arguments", "Purpose"],
        ["inspect_doc.py", "<file>", "Returns structured JSON metadata, page counts, scanned vs text"],
        ["extract_doc.py", "<file> --type text|tables|images", "Extracts raw text, Markdown tables, or embedded images"],
        ["convert_doc.py", "<input> <output_or_ext>", "Headless conversion via LibreOffice, Pandoc, or pdf2docx"],
        ["render_doc.py", "<file> --outdir <dir>", "Renders PDF pages / Office slides to high-res PNGs"],
        ["ocr_doc.py", "<file> --lang eng --psm 3", "Runs Tesseract OCR with adaptive contrast enhancement"],
        ["qa_doc.py", "<file>", "Validates structural integrity, formula syntax, and exit codes"]
    ]
    t3 = Table(cli_data, colWidths=[1.4*inch, 2.6*inch, 3.0*inch])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('BACKGROUND', (0, 1), (-1, -1), light_bg),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t3)

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceAfter=10))
    story.append(Paragraph(
        "<i>Antigravity Document Operating System • Published under MIT License • Open Source Agent Infrastructure</i>",
        ParagraphStyle('FooterNotice', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, textColor=colors.gray, alignment=1)
    ))

    doc.build(story)
    print(f"Successfully generated official PDF guide at: {output_pdf_path}")

if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/Antigravity_Document_OS_Comprehensive_Guide.pdf")
    create_guide(out)
