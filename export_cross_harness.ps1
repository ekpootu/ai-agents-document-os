<#
.SYNOPSIS
    Exports Antigravity Document OS skills to other Agent Harnesses (Claude Code, OpenCode CLI, Cursor).

.PARAMETER Target
    Destination agent harness: ClaudeCode, OpenCode, Universal, or GlobalAntigravity.
#>

[CmdletBinding()]
param(
    [ValidateSet("ClaudeCode", "OpenCode", "Universal", "GlobalAntigravity", "All")]
    [string]$Target = "All"
)

$WorkspaceRoot = $PSScriptRoot
$SkillsSource = Join-Path $WorkspaceRoot ".agents\plugins\document-os\skills"

Write-Host "Exporting Document OS Skills to Target: $Target..." -ForegroundColor Cyan

function Copy-SkillsTo {
    param([string]$DestinationPath, [string]$PlatformName)
    Write-Host "Exporting to $PlatformName ($DestinationPath)..." -ForegroundColor Yellow
    if (-not (Test-Path $DestinationPath)) {
        New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
    }
    Copy-Item -Path "$SkillsSource\*" -Destination $DestinationPath -Recurse -Force
    Write-Host "Successfully exported skills to $PlatformName." -ForegroundColor Green
}

if ($Target -in @("ClaudeCode", "All")) {
    $ClaudeSkills = Join-Path $HOME ".claude\skills"
    Copy-SkillsTo $ClaudeSkills "Claude Code (Global)"
    $LocalClaude = Join-Path $WorkspaceRoot ".claude\skills"
    Copy-SkillsTo $LocalClaude "Claude Code (Local Workspace)"
}

if ($Target -in @("OpenCode", "All")) {
    $OpenCodeSkills = Join-Path $HOME ".config\opencode\skills"
    Copy-SkillsTo $OpenCodeSkills "OpenCode CLI"
}

if ($Target -in @("GlobalAntigravity", "All")) {
    $GlobalAntigravity = Join-Path $HOME ".gemini\config\plugins\document-os\skills"
    Copy-SkillsTo $GlobalAntigravity "Antigravity (Global)"
}

Write-Host "`nExport process completed successfully." -ForegroundColor Cyan
