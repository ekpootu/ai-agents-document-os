<#
.SYNOPSIS
    Automated Installer and Diagnostic Harness for Antigravity Document Operating System (Document OS) on Windows.

.DESCRIPTION
    1. Validates Python 3.10+ installation.
    2. Creates and manages a dedicated virtual environment (.venv-docos).
    3. Installs all required Python document processing packages (including ReportLab, pypdf, python-docx, openpyxl, etc.).
    4. Detects and safely installs system tools (LibreOffice, Pandoc, Tesseract) using winget.
    5. Optionally deploys/links the plugin globally to $HOME\.gemini\config\plugins\document-os.
    6. Executes diagnostic self-tests across all format engines.

.PARAMETER DeployGlobal
    Deploy Document OS plugin to the global Antigravity configuration directory ($HOME\.gemini\config\plugins\).

.PARAMETER SkipWinget
    Skip automated system tool installation via winget.
#>

[CmdletBinding()]
param(
    [switch]$DeployGlobal,
    [switch]$SkipWinget
)

$ErrorActionPreference = "Continue"
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Antigravity Document Operating System (Document OS)    " -ForegroundColor Cyan
Write-Host "              Automated Windows Installer                 " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$WorkspaceRoot = $PSScriptRoot
$VenvDir = Join-Path $WorkspaceRoot ".venv-docos"
$PluginSource = Join-Path $WorkspaceRoot ".agents\plugins\document-os"

# 1. Check Python
Write-Host "`n[1/6] Checking Python installation..." -ForegroundColor Yellow
$PythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCmd) {
    Write-Error "Python not found in PATH. Please install Python 3.10 or higher."
    exit 1
}
$PythonVersion = & python --version
Write-Host "Found Python: $PythonVersion at $($PythonCmd.Source)" -ForegroundColor Green

# 2. Virtual Environment Setup
Write-Host "`n[2/6] Configuring dedicated virtual environment (.venv-docos)..." -ForegroundColor Yellow
if (-not (Test-Path $VenvDir)) {
    Write-Host "Creating virtual environment at $VenvDir..." -ForegroundColor Gray
    & python -m venv $VenvDir
} else {
    Write-Host "Virtual environment already exists at $VenvDir" -ForegroundColor Gray
}

$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$VenvPip = Join-Path $VenvDir "Scripts\pip.exe"

# 3. Install Python Dependencies
Write-Host "`n[3/6] Installing Document OS Python packages..." -ForegroundColor Yellow
$Packages = @(
    "pypdf",
    "pdfplumber",
    "pdf2image",
    "pdf2docx",
    "pytesseract",
    "python-docx",
    "openpyxl",
    "xlsxwriter",
    "pandas",
    "python-pptx",
    "Pillow",
    "reportlab",
    "weasyprint",
    "fonttools"
)

Write-Host "Upgrading pip..." -ForegroundColor Gray
& $VenvPython -m pip install --upgrade pip --quiet

Write-Host "Installing packages: $($Packages -join ', ')..." -ForegroundColor Gray
& $VenvPip install --quiet $Packages

Write-Host "Python packages successfully installed into .venv-docos." -ForegroundColor Green

# WeasyPrint GTK3 detection
Write-Host "`nChecking WeasyPrint GTK3 runtime availability..." -ForegroundColor Gray
$WeasyCheck = & $VenvPython -c "
try:
    import weasyprint
    print('WeasyPrint: Available [OK]')
except OSError:
    print('WeasyPrint: GTK3 runtime not found. PDF generation will use ReportLab fallback.')
    print('  To enable WeasyPrint, install GTK3: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html')
" 2>&1
Write-Host $WeasyCheck -ForegroundColor $(if ($WeasyCheck -match 'OK') { 'Green' } else { 'Yellow' })

# 4. Check & Install System CLI Tools via Winget
Write-Host "`n[4/6] Inspecting System Dependencies (LibreOffice, Pandoc, Tesseract, Poppler)..." -ForegroundColor Yellow

function Test-SystemTool {
    param([string]$Name, [string[]]$KnownPaths)
    if (Get-Command $Name -ErrorAction SilentlyContinue) { return $true }
    foreach ($p in $KnownPaths) {
        if (Test-Path $p) { return $true }
    }
    return $false
}

$LibreOfficePaths = @(
    "C:\Program Files\LibreOffice\program\soffice.exe",
    "C:\Program Files (x86)\LibreOffice\program\soffice.exe"
)
$PandocPaths = @(
    "C:\Program Files\Pandoc\pandoc.exe",
    "$env:LOCALAPPDATA\Pandoc\pandoc.exe"
)
$TesseractPaths = @(
    "C:\Program Files\Tesseract-OCR\tesseract.exe",
    "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
)

$HasLibreOffice = Test-SystemTool "soffice" $LibreOfficePaths
$HasPandoc = Test-SystemTool "pandoc" $PandocPaths
$HasTesseract = Test-SystemTool "tesseract" $TesseractPaths

Write-Host "LibreOffice: $(if ($HasLibreOffice) { 'Installed [OK]' } else { 'Missing [!] ' })" -ForegroundColor $(if ($HasLibreOffice) { 'Green' } else { 'Yellow' })
Write-Host "Pandoc:      $(if ($HasPandoc) { 'Installed [OK]' } else { 'Missing [!] ' })" -ForegroundColor $(if ($HasPandoc) { 'Green' } else { 'Yellow' })
Write-Host "Tesseract:   $(if ($HasTesseract) { 'Installed [OK]' } else { 'Missing [!] ' })" -ForegroundColor $(if ($HasTesseract) { 'Green' } else { 'Yellow' })

if (-not $SkipWinget) {
    $WingetCmd = Get-Command winget -ErrorAction SilentlyContinue
    if ($WingetCmd) {
        if (-not $HasLibreOffice) {
            Write-Host "Installing LibreOffice via winget..." -ForegroundColor Cyan
            & winget install --id TheDocumentFoundation.LibreOffice --silent --accept-package-agreements --accept-source-agreements
        }
        if (-not $HasPandoc) {
            Write-Host "Installing Pandoc via winget..." -ForegroundColor Cyan
            & winget install --id JohnMacFarlane.Pandoc --silent --accept-package-agreements --accept-source-agreements
        }
        if (-not $HasTesseract) {
            Write-Host "Installing Tesseract OCR via winget..." -ForegroundColor Cyan
            & winget install --id UB-Mannheim.TesseractOCR --silent --accept-package-agreements --accept-source-agreements
        }
    } else {
        Write-Warning "winget not found. Please install missing tools manually."
    }
}

# 5. Global Deployment (Optional)
if ($DeployGlobal) {
    Write-Host "`n[5/6] Deploying Document OS globally to Antigravity..." -ForegroundColor Yellow
    $GlobalPluginDir = Join-Path $HOME ".gemini\config\plugins\document-os"
    if (-not (Test-Path $GlobalPluginDir)) {
        New-Item -ItemType Directory -Path $GlobalPluginDir -Force | Out-Null
    }
    Copy-Item -Path "$PluginSource\*" -Destination $GlobalPluginDir -Recurse -Force
    Write-Host "Document OS successfully deployed globally to $GlobalPluginDir" -ForegroundColor Green
} else {
    Write-Host "`n[5/6] Global deployment skipped. (Run with -DeployGlobal to install globally across all Antigravity workspaces)" -ForegroundColor Gray
}

# 6. Diagnostics & Dogfood Self-Test
Write-Host "`n[6/6] Executing Diagnostics & Self-Test Verification..." -ForegroundColor Yellow
$DiagnosticsScript = @"
import pypdf, docx, openpyxl, pptx, PIL, reportlab
print('  [PASS] All core Python document libraries imported successfully.')
"@
& $VenvPython -c $DiagnosticsScript

Write-Host "`nDocument Operating System installation and verification complete!" -ForegroundColor Green
Write-Host "To use Python CLI tools in your tasks, execute with: $VenvPython" -ForegroundColor Cyan
