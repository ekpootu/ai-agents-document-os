---
name: document-qa
description: >-
  Quality assurance, structural integrity verification, and validation skill for
  all generated or modified documents (.pdf, .docx, .xlsx, .pptx, .png, .jpg).
  Scans for file corruption, broken formulas, truncated text, and rendering defects.
  Use immediately after modifying or creating any document.
---

# Document Quality Assurance (Document QA)

The **Document QA Skill** is the defensive validation checkpoint for Antigravity. It ensures that no corrupt, misformatted, or broken document is ever returned to the user.

---

## The QA Verification Protocol

Whenever a file is created, modified, or converted, execute `qa_doc.py`:
```powershell
python .agents/plugins/document-os/scripts/qa_doc.py "<filepath>"
```

The script evaluates:

### 1. Structural File Integrity
- Does the file open cleanly without raising zip corruption or parsing errors?
- Does the internal OOXML XML tree validate?
- Are mandatory sections present (e.g. `word/document.xml`, `xl/workbook.xml`, `ppt/presentation.xml`)?

### 2. Format-Specific Quality Checks

#### PDF Quality Checklist
- [ ] File header is valid (`%PDF-1.x`).
- [ ] Document contains at least 1 page and EOF marker is present.
- [ ] Text extraction yields expected characters (or page images exist if scanned).
- [ ] Embedded fonts are resolved without fallback corruption.

#### DOCX Quality Checklist
- [ ] All paragraphs and runs have valid XML tags.
- [ ] Tables have consistent column counts across all rows.
- [ ] Document contains non-empty body text.
- [ ] File opens in Word / LibreOffice without prompting for "Repair".

#### XLSX Quality Checklist
- [ ] All sheet names are unique and non-empty.
- [ ] **Formula Integrity**: Zero `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#N/A` errors detected.
- [ ] Cell references stay within worksheet boundaries.
- [ ] Number formats (dates, percentages, currencies) remain applied.

#### PPTX Quality Checklist
- [ ] Presentation has at least 1 slide.
- [ ] No slide contains overlapping text boxes with identical coordinates.
- [ ] Text frames do not overflow the slide dimension boundary (`13.33 x 7.5` inches).
- [ ] Images have valid aspect ratios and positive dimensions.

### 3. Acceptance Reporting Format
When reporting completion to the user, include this QA block:
```markdown
### Document QA Verification Report
- **File**: `quarterly_report.xlsx`
- **Status**: PASSED (100% Structural & Formula Integrity)
- **Sheets Verified**: `Summary` (42 rows, 6 formulas), `Data` (1,200 rows)
- **Formula Error Scan**: 0 errors detected (0 `#REF!`, 0 `#VALUE!`)
- **Render Check**: Clean
```
