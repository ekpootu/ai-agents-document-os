# PROMPT:

I am about to work with Google Antigravity CLI AI Agent Harness, and would love my workflow to be able to read and write from and to all documents format, including .pdf, .docx, .pptx, .png, .md, .jpg, .xlsx, etc) Can you tell me what Workspace/Project or Global Skill or skills, Rules, etc, that I will need to install, setup or configure? Search the web, including places like, [skills.sh](http://skills.sh/), agentskillshub.top, and other ai agents skills portals, and let me know.

# RESPONSE:

Yes. I searched the current **Google Antigravity documentation**, **`skills.sh`**, Agent Skills Hub, and several GitHub Agent-Skills repositories. The short version is:

> **You do not want one giant “read every file” skill.**
> 
> 
> You want a **document-processing stack** consisting of a global document-router skill + specialist format skills/tools + system utilities + a small set of rules/permissions.
> 

Antigravity is actually quite well suited to this because its current extensibility model supports **Skills, Rules, Plugins, MCP servers, hooks, and native file/shell tools**. 

One important caveat: there isn't a single magic package that gives perfect read/write fidelity for *every* conceivable document format. PDF, DOCX, XLSX and PPTX are structurally very different. Images additionally need OCR/vision tooling. The best architecture is therefore a **format router**.

## **1. The architecture I recommend**

I'd build your Antigravity environment like this:

```jsx
                         Google Antigravity CLI
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
             GLOBAL RULES                 GLOBAL SKILLS
          ~/.gemini/GEMINI.md          ~/.gemini/antigravity-cli/
                                             skills/
                    │                           │
                    │                  ┌────────┴─────────┐
                    │                  │                  │
                    │           document-router     specialist skills
                    │                  │           ┌─────┼─────┬─────┐
                    │                  │          PDF   DOCX XLSX PPTX
                    │                  │
                    │                  ├── images/OCR
                    │                  ├── Markdown
                    │                  ├── CSV/JSON
                    │                  └── conversion
                    │
                    └─────────────── MCP / tools
                                           │
                              ┌────────────┼────────────┐
                              │            │            │
                         LibreOffice    Pandoc      OCR/image
                              │            │            │
                           Office       conversion   processing

```

This is preferable to putting hundreds of instructions into **`GEMINI.md`**.

Antigravity itself recommends keeping Skills focused rather than making one enormous skill, and Skills can contain both instructions and supporting scripts/resources.

# **2. First: understand the Antigravity locations**

For the **Antigravity CLI**, the current documented locations are:

### **Global skills**

```
~/.gemini/antigravity-cli/skills/
```

These apply across your projects.

### **Workspace/project skills**

```
<project>/.agents/skills/
```

These belong to one project/repository. 

### **Global rules**

```
~/.gemini/GEMINI.md
```

### **Workspace rules/context**

```
<project>/GEMINI.md
<project>/AGENTS.md
<project>/.agents/rules/
```

Antigravity's Rules system supports global and workspace rules, including rules that are always active, manually activated, model-selected, or triggered by file globs. 

### **MCP**

Global:

```
~/.gemini/config/mcp_config.json
```

Workspace:

```
<project>/.agents/mcp_config.json
```

Antigravity CLI also has **`/mcp`** for managing MCP servers. 

### **Check what Antigravity currently sees**

Inside the CLI:

```
/skills
```

and:

```
/mcp
```

The CLI reference explicitly lists **`/skills`**, **`/mcp`**, **`/permissions`**, **`/agents`**, etc.

---

# **3. The most important skill: a document-processing/router skill**

I would make this your **core global skill**.

Something like:

```
~/.gemini/antigravity-cli/skills/document-processing/
├── SKILL.md
├── scripts/
│   ├── inspect_file.py
│   ├── extract_text.py
│   ├── extract_tables.py
│   ├── convert_document.py
│   ├── render_document.py
│   ├── ocr_document.py
│   └── validate_output.py
└── references/
    ├── pdf.md
    ├── docx.md
    ├── xlsx.md
    ├── pptx.md
    ├── images.md
    └── conversion-matrix.md
```

The skill should tell the agent:

1. Identify the file type.
2. Inspect before modifying.
3. Select the correct tool/library.
4. Never blindly convert formats.
5. Preserve the original.
6. Perform the operation.
7. Re-open/render the result.
8. Validate the result.
9. Report what was changed.

That last part is important.

For example:

> "Convert this PDF to Word."
> 

should **not** simply become:

```bash
pdf2docx input.pdf output.docx
```

The agent should inspect the PDF, determine whether it is text-based/scanned/table-heavy/layout-heavy, select an appropriate conversion strategy, convert it, render/check the DOCX and report any fidelity limitations.

---

# **4. There is already an excellent candidate skill**

I found a particularly relevant Agent Skill:

document-processing Agent Skill on GitHub

It is specifically designed for agentic document processing and covers:

- PDF
- DOCX
- XLSX
- PPTX
- OCR
- conversion
- tables
- charts
- forms
- mail merge
- presentations
- batch processing

It uses:

| **Format/task** | **Recommended tooling** |
| --- | --- |
| PDF | **`pypdf`** |
| PDF layout/tables | **`pdfplumber`** |
| PDF OCR | **`pytesseract`** + **`pdf2image`** |
| DOCX | **`python-docx`** |
| XLSX | **`openpyxl`** |
| PPTX | **`python-pptx`** |
| Conversion | **`pandoc`** |
| Office → PDF | LibreOffice |

The skill also has a preflight script that checks whether the required tooling is installed. 

**I would use this as one of your starting points rather than reinventing the entire document stack.**

---

# **5. DOCX — definitely install a dedicated skill**

For Word documents, I'd have a dedicated specialist.

I found this one on **`skills.sh`**:

DOCX Agent Skill on skills.sh

It handles:

- reading DOCX
- creating DOCX
- editing DOCX
- analyzing DOCX
- OOXML manipulation
- document structure

The installation shown by **`skills.sh`** is:

```bash
npx skills add https://github.com/answerzhao/agent-skills --skill docx
```

I'd also consider the larger document-processing skill above, rather than installing duplicate DOCX skills that could conflict.

# **6. PDF — make this a first-class skill**

PDF is actually several different problems:

```
PDF
├── text PDF
├── scanned PDF
├── form PDF
├── table-heavy PDF
├── image-heavy PDF
├── scientific PDF
├── PDF → DOCX
├── PDF → Markdown
├── PDF → images
├── PDF merging/splitting
└── PDF generation
```

Your stack should therefore include:

```
pypdf
pdfplumber
pdf2image
pytesseract
qpdf
poppler
```

Potentially:

```
pdf2docx
```

for PDF → DOCX.

The document-processing skill I found explicitly handles these workflows. 

---

# **7. XLSX — don't rely on generic file reading**

Excel is another one where a dedicated skill is worth having.

You want:

```
openpyxl
pandas
LibreOffice
```

Potentially:

```
xlsxwriter
```

for generating highly formatted spreadsheets.

The agent should understand that:

- formulas ≠ displayed values
- formatting matters
- merged cells matter
- hidden sheets matter
- charts matter
- named ranges matter
- tables matter
- pivot tables are special
- formulas need recalculation/validation

The document-processing skill I found specifically addresses XLSX formulas, charts and spreadsheets. 

There is also a collection of separate **`docx`**, **`xlsx`**, **`pptx`**, and **`pdf`** skills in another Agent Skills repository:

SherifEldeeb/agentskills

It explicitly organizes these as baseline document skills. 

---

# **8. PPTX — also deserves its own specialist**

For PowerPoint:

```
python-pptx
LibreOffice
PDF rendering
image rendering
```

I'd make the agent follow:

```
PPTX
 ↓
inspect slide dimensions/theme/layouts
 ↓
modify/create
 ↓
export to PDF
 ↓
render slides
 ↓
visually inspect
 ↓
validate
```

This is important because a syntactically valid **`.pptx`** can still be visually terrible.

The document-processing skill I found includes PPTX layouts, charts, media and speaker notes. 

---

# **9. PNG/JPG — add an image/OCR capability**

For:

```
.png
.jpg
.jpeg
.webp
.tiff
.bmp
```

you don't really need a separate "document" format library.

I'd give Antigravity:

```
Pillow
ImageMagick
Tesseract OCR
```

and potentially:

```
OpenCV
```

for more advanced image processing.

Your skill should distinguish:

```
image → understand
image → OCR
image → resize
image → convert
image → crop
image → annotate
image → extract metadata
image → embed into document
```

And, importantly, **visual understanding should use the model's vision capability where available**, rather than attempting to OCR everything.

---

# **10. Markdown should be treated as a native interchange format**

This is where I would make your architecture much more powerful.

Use Markdown as an **intermediate representation**.

For example:

```
PDF
 ↓
Markdown
 ↓
AI transformation
 ↓
DOCX
```

or:

```
DOCX
 ↓
Markdown
 ↓
AI analysis
 ↓
PPTX
```

or:

```
XLSX
 ↓
structured data
 ↓
Markdown report
 ↓
PDF
```

**`pandoc`** is extremely useful here.

Install:

```bash
pandoc
```

The document-processing skill explicitly recommends Pandoc for cross-format conversion. 

---

# **11. LibreOffice is probably the most important system dependency**

If you're serious about **read + write + conversion**, I'd install LibreOffice even if you don't normally use it interactively.

It gives your agent a powerful headless conversion engine:

```
DOCX → PDF
XLSX → PDF
PPTX → PDF
ODT → DOCX
ODS → XLSX
ODP → PPTX
etc.
```

Typical command:

```bash
soffice --headless --convert-to pdf file.docx
```

The document-processing skill specifically uses LibreOffice for Office → PDF conversion and identifies DOCX → PDF as a high-fidelity conversion path. 

---

# **12. I would install this base toolchain**

Assuming macOS/Linux:

### **Python packages**

```bash
python -m pip install \
  pypdf \
  pdfplumber \
  pdf2image \
  pdf2docx \
  pytesseract \
  python-docx \
  openpyxl \
  xlsxwriter \
  pandas \
  python-pptx \
  Pillow \
  opencv-python
```

### **System tools**

```
LibreOffice
Pandoc
Poppler
Tesseract
ImageMagick
qpdf
```

Depending on your OS, the installation commands differ.

This gives you a very strong local document-processing substrate.

---

# **13. Consider adding an OOXML specialist**

DOCX/XLSX/PPTX are all fundamentally related because modern Office documents are **OOXML packages**.

That means your agent can sometimes perform things that higher-level libraries cannot.

I found an interesting skill specifically for this:

Office OOXML Utilities skill on skills.sh

It provides utilities for:

- unpacking OOXML
- repacking OOXML
- validating OOXML
- converting through LibreOffice

That's useful as a **low-level recovery/repair skill**.

I would not make it the primary document interface, though.

Use:

```
python-docx
openpyxl
python-pptx
```

first.

Use OOXML manipulation when necessary.

---

# **14. There's another interesting document toolkit**

I also found:

memtomem/agent-skills-public

It contains individual tools/skills for:

```
pdf-parser
xlsx-parser
docx-parser
pptx-parser
hwp-toolkit
```

and produces structured output such as Markdown/JSON from the documents. 

That's interesting if your primary goal is **feeding documents into the agent**, rather than merely editing them.

---

# **15. Don't overlook HWP/HWPX and other formats**

You said "all documents."

If you really mean that, I'd eventually expand the router to:

```
PDF
DOCX
DOC
ODT
RTF
TXT
MD
HTML
EPUB
XLSX
XLS
ODS
CSV
TSV
PPTX
PPT
ODP
PNG
JPG
JPEG
WEBP
TIFF
BMP
SVG
JSON
XML
YAML
ZIP
```

and possibly:

```
HWP
HWPX
Pages
Numbers
Keynote
```

The latter three are considerably more awkward on Linux/macOS because Apple's proprietary formats don't have the same nice open tooling.

---

# **16. Your Global Rule should be small**

I would **not** dump a huge document manual into **`GEMINI.md`**.

Instead, something along these lines:

```markdown
# Document Handling

When working with files, treat document processing as a structured
read → understand → modify → validate workflow.

## General rules

- Never overwrite an original document unless explicitly requested.
- Identify the file format before processing it.
- Use the specialist document skill/tool appropriate to the format.
- Prefer native format manipulation over lossy conversion.
- Use Markdown/JSON as intermediate representations when useful.
- Preserve formatting, metadata, formulas, tables, images and structure
  whenever technically possible.
- For scanned documents, use OCR.
- For image-based documents, combine OCR with visual inspection.
- For generated Office documents, validate that the resulting file opens.
- For PDF/DOCX/PPTX visual layouts, render and inspect the result when
  layout matters.
- For spreadsheets, preserve formulas unless the user explicitly asks
  for values only.
- Never silently discard content during conversion.
- Report significant fidelity limitations.
- Keep source files unchanged by default.
```

That's the kind of thing I'd put in:

```
~/.gemini/GEMINI.md
```

Global Rules are specifically intended for persistent behavior like this.

# **17. Then make the actual intelligence a Skill**

Your global Skill should be much more detailed:

```
document-processing/
    SKILL.md
    scripts/
    references/
```

The Rule says:

> "Handle documents carefully."
> 

The Skill says:

> "Here's exactly how to handle PDF, DOCX, XLSX, PPTX, images, conversions, validation, OCR, etc."
> 

That's a very important distinction.

---

# **18. Add a "document triage" skill**

I would actually make this a separate skill:

```
document-triage/
```

Its job is to answer:

> **What is this file and what is the safest way to work with it?**
> 

For example:

```
report.pdf
   ↓
magic/file identification
   ↓
PDF?
   ↓
text-based or scanned?
   ↓
tables?
   ↓
forms?
   ↓
images?
   ↓
choose processing pipeline
```

For:

```
financials.xlsx
```

it might detect:

```
Workbook
├── 12 sheets
├── 8 formulas
├── 3 charts
├── 2 pivot tables
└── hidden sheet
```

Then select the appropriate processing strategy.

---

# **19. Add a "document QA" skill**

This is something I think is **more important than another format skill**.

Call it:

```
document-qa/
```

It should verify:

### **PDF**

- page count
- text presence
- images
- metadata
- corruption
- rendering

### **DOCX**

- file opens
- paragraphs preserved
- tables preserved
- images preserved
- styles preserved

### **XLSX**

- workbook opens
- sheets preserved
- formulas preserved
- formulas recalculated where necessary
- charts preserved

### **PPTX**

- slides preserved
- text isn't overflowing
- images aren't missing
- charts exist
- presentation renders

### **Images**

- dimensions
- format
- color profile
- corruption
- OCR result if relevant

This gives you a much more reliable agent.

---

# **20. MCP is optional — but potentially powerful**

Antigravity supports MCP specifically for connecting agents to local tools, file parsers and other services. 

I would **not immediately install five document MCP servers**, though.

For local documents, ordinary CLI tools + Python libraries + Skills are simpler and more reliable.

Use MCP when you want something like:

```
Antigravity
   ↓
MCP
   ↓
specialized document service
```

or:

```
Antigravity
   ↓
MCP
   ↓
Google Drive
```

or:

```
Antigravity
   ↓
MCP
   ↓
SharePoint
```

or:

```
Antigravity
   ↓
MCP
   ↓
document database/search index
```

That's where MCP becomes particularly valuable.

---

# **21. I would NOT install every skill you find on skills.sh**

There are already lots of overlapping document skills.

For example, **`skills.sh`** has separate DOCX and document-processing skills, while Agent Skills Hub indexes many different document parsers and Office tools. 

You can very easily end up with:

```
pdf skill #1
pdf skill #2
pdf skill #3
document skill #1
office skill #2
xlsx skill #4
...
```

and then the agent has competing instructions.

That's worse than having fewer, better-integrated skills.

I'd pick:

### **Tier 1 — core**

```
document-processing
document-triage
document-qa
```

### **Tier 2 — specialists**

```
pdf
docx
xlsx
pptx
image-ocr
```

### **Tier 3 — optional**

```
ooxml
conversion
google-drive
sharepoint
notion
research
```

---

# **22. There's an especially interesting "Office Mastery" skill**

I found this:

Office Mastery Agent Skill

It covers:

```
Word
Excel
PowerPoint
PDF
```

using Python libraries and MCP servers. 

It's another candidate I'd evaluate against the broader **`document-processing`** skill rather than blindly installing both.

---

# **23. Anthropic's document skills are worth studying too**

Interestingly, Anthropic's Agent Skills collection contains separate document skills for:

```
docx
pdf
pptx
xlsx
```

and these have become something of a reference implementation for the Agent Skills approach. 

[](https://www.google.com/s2/favicons?domain=https%3A%2F%2Fclaudeskillsgithub.com&sz=128)

Even though they're designed around Anthropic's ecosystem, the underlying Agent Skills structure is portable enough that they're useful **reference material for Antigravity**.

I would use them as design inspiration, not automatically install all of them.

---

# **24. Antigravity Plugins may eventually be the cleanest solution**

This is particularly interesting for your use case.

Antigravity Plugins can package:

```
skills
agents
rules
MCP servers
hooks
```

into a single unit. 

So eventually you could have:

```
document-superpowers/
├── plugin.json
├── skills/
│   ├── document-router/
│   ├── document-qa/
│   ├── pdf/
│   ├── docx/
│   ├── xlsx/
│   ├── pptx/
│   └── image-ocr/
├── agents/
│   └── document-specialist/
├── rules/
│   └── document-safety.md
├── hooks.json
└── mcp_config.json
```

Then install it as one Antigravity plugin.

That is probably where I would take your setup eventually.

---

# **25. Permissions matter enormously**

There's a potential trap here.

You are asking the agent to **write to arbitrary document formats**, which means it needs permission to execute things such as:

```
python
soffice
pandoc
tesseract
convert
qpdf
```

and write files.

Antigravity's permission system allows granular rules such as:

```
read_file(...)
write_file(...)
command(...)
mcp(...)
```

and defaults unconfigured actions to Ask. 

I would **not** simply enable:

```
command(*)
write_file(*)
```

globally.

Instead, allow the document-processing commands and your intended document directories.

For example conceptually:

```
ALLOW
  read_file(project/)
  write_file(project/documents/)
  command(python ...)
  command(soffice ...)
  command(pandoc ...)
  command(tesseract ...)

ASK
  network
  arbitrary shell
  destructive operations

DENY
  rm -rf
  ~/.ssh
  credentials
  .git/
```

Antigravity explicitly supports this sort of granular permission configuration. 

---

# **26. One thing I'd change from many existing skills**

A lot of document skills are designed around:

> "The user asks to manipulate a document."
> 

You want something slightly more ambitious:

> **"Documents are first-class objects in my agent environment."**
> 

That means your Skill should teach Antigravity to automatically recognize:

```
*.pdf
*.docx
*.doc
*.xlsx
*.xls
*.pptx
*.ppt
*.png
*.jpg
*.jpeg
*.webp
*.tiff
*.md
*.txt
*.csv
*.json
*.xml
*.html
...
```

and route them appropriately.

For example:

```
"Summarise this PDF"
       ↓
PDF triage
       ↓
text extraction
       ↓
OCR if necessary
       ↓
structured representation
       ↓
LLM analysis
```

Whereas:

```
"Fix the formatting in this Excel workbook"
       ↓
XLSX specialist
       ↓
openpyxl / LibreOffice
       ↓
modify
       ↓
recalculate/render
       ↓
QA
```

And:

```
"Turn these meeting notes into a PowerPoint"
       ↓
Markdown/text
       ↓
PPTX generation
       ↓
render slides
       ↓
visual QA
       ↓
final.pptx
```

---

# **27. My recommended final installation**

If this were **my Antigravity machine**, I'd start with:

```
GLOBAL
────────────────────────────────────────────

~/.gemini/GEMINI.md
    ↓
global document-handling rules

~/.gemini/antigravity-cli/skills/

    document-router/
    document-processing/
    document-qa/
    pdf/
    docx/
    xlsx/
    pptx/
    image-ocr/

SYSTEM
────────────────────────────────────────────

Python
pypdf
pdfplumber
pdf2image
pdf2docx
pytesseract
python-docx
openpyxl
xlsxwriter
pandas
python-pptx
Pillow
OpenCV

LibreOffice
Pandoc
Poppler
Tesseract
ImageMagick
qpdf

OPTIONAL
────────────────────────────────────────────

OOXML skill
Office Mastery skill
specialized parsers
Google Drive MCP
SharePoint MCP
other storage MCPs
```

---

# **28. One important current Antigravity detail**

There is a bit of documentation evolution happening right now.

The current Antigravity documentation says the newer model is moving toward **Agent Skills**, while Workflows are being deprecated in favor of Skills by **November 1, 2026**. 

So I would **not invest heavily in old Workflow-based document automation**.

Build this around:

```
Skills
+
Rules
+
Plugins
+
MCP
+
Hooks
```

instead.

---

# **29. My strongest recommendation**

Rather than having you install 15 random skills from portals, I'd build you a **single coherent "Universal Document Workspace" for Antigravity**.

Something like:

```
universal-document-workspace/
│
├── skills/
│   ├── document-router/
│   ├── document-processing/
│   ├── document-qa/
│   ├── pdf/
│   ├── docx/
│   ├── xlsx/
│   ├── pptx/
│   ├── image/
│   ├── ocr/
│   └── conversion/
│
├── agents/
│   └── document-specialist/
│
├── rules/
│   └── document-safety.md
│
├── scripts/
│   ├── inspect.py
│   ├── convert.py
│   ├── render.py
│   ├── extract.py
│   ├── ocr.py
│   └── validate.py
│
└── mcp/
    └── optional document servers
```

Then make it **globally available to every Antigravity project**.

The nice thing is that Antigravity's current plugin architecture is explicitly designed to package skills, agents, rules, MCP configuration and hooks together. 

### **In other words**

You don't really want:

> "Install a PDF skill."
> 

You want:

> **"Give my Antigravity agent a reliable document operating system."**
> 

That's a much better mental model for what you're trying to accomplish.

If you want, **I can take this one step further and actually design the complete Antigravity setup for you** — including the exact folder tree, **`GEMINI.md`**, **`.agents/rules`**, a master **`document-router/SKILL.md`**, recommended **`skills.sh`** installations, Python/system dependencies, permissions, QA workflow, and an install script you can run on your machine.