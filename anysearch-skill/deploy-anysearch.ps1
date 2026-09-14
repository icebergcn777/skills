# deploy-anysearch.ps1 - Deploy AnySearch Skill to Claude Code CLI + Codex
# Usage: powershell -ExecutionPolicy Bypass -File D:\Claude_Code\skills\anysearch-skill\deploy-anysearch.ps1
# Source: D:\Claude_Code\skills\anysearch-skill  (v3.0.1)
# NOTE: ASCII-only on purpose - Windows PowerShell 5.1 reads .ps1 as ANSI/GBK.

$ErrorActionPreference = "Stop"

$src = "D:\Claude_Code\skills\anysearch-skill"

if (-not (Test-Path (Join-Path $src "SKILL.md"))) {
    Write-Host "[ERROR] SKILL.md not found at $src" -ForegroundColor Red
    exit 1
}

$targets = @(
    @{ Name = "Claude Code CLI"; Path = (Join-Path $env:USERPROFILE ".claude\skills\anysearch") },
    @{ Name = "Codex (shared)";  Path = (Join-Path $env:USERPROFILE ".agents\skills\anysearch") }
)

foreach ($t in $targets) {
    $dest = $t.Path
    if (Test-Path $dest) {
        Write-Host "[REPLACE] $($t.Name): $dest" -ForegroundColor Yellow
        Remove-Item $dest -Recurse -Force
    }
    Copy-Item $src $dest -Recurse -Force
    if (Test-Path (Join-Path $dest "SKILL.md")) {
        Write-Host "[OK] $($t.Name) -> $dest" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] $($t.Name)" -ForegroundColor Red
    }
}

# ---- Runtime detection (Python > Node.js > PowerShell) ----
Write-Host "`n-- Runtime detection --" -ForegroundColor Cyan
$runtime = $null
$cmd = $null

# Python (preferred)
$pyOk = $false
try {
    $pyVer = (python --version 2>&1).ToString()
    if ($pyVer -match "\d+\.\d+") {
        python -c "import requests" 2>$null
        if ($LASTEXITCODE -eq 0) {
            $pyOk = $true
            $runtime = "Python"
            $cmd = "python `"$src\scripts\anysearch_cli.py`""
            Write-Host "[OK] Python detected: $pyVer (requests OK)" -ForegroundColor Green
        } else {
            Write-Host "[WARN] Python found but missing 'requests', trying Node.js" -ForegroundColor Yellow
        }
    }
} catch {}

# Node.js
if (-not $pyOk) {
    try {
        $nodeVer = (node --version 2>&1).ToString()
        if ($LASTEXITCODE -eq 0 -and $nodeVer -match "v\d+") {
            $runtime = "Node.js"
            $cmd = "node `"$src\scripts\anysearch_cli.js`""
            Write-Host "[OK] Node.js detected: $nodeVer" -ForegroundColor Green
        }
    } catch {}
}

# PowerShell fallback
if (-not $runtime) {
    $runtime = "PowerShell"
    $cmd = "powershell -ExecutionPolicy Bypass -File `"$src\scripts\anysearch_cli.ps1`""
    Write-Host "[OK] PowerShell fallback" -ForegroundColor Green
}

# ---- Write runtime.conf ----
$confBase = Join-Path $env:USERPROFILE ".claude\skills\anysearch"
$conf = Join-Path $confBase "runtime.conf"
if (-not (Test-Path $confBase)) { New-Item -ItemType Directory -Path $confBase -Force | Out-Null }
"Runtime: $runtime" | Set-Content $conf -Encoding UTF8
"Command: $cmd" | Add-Content $conf -Encoding UTF8
Write-Host "[OK] runtime.conf written to $conf" -ForegroundColor Green
Get-Content $conf

# ---- Entry test (doc command, local only, no network) ----
Write-Host "`n-- Entry test (doc) --" -ForegroundColor Cyan
$docCmd = ($cmd + " doc")
try {
    $docOut = Invoke-Expression $docCmd 2>&1 | Select-Object -First 5
    Write-Host $docOut
    Write-Host "[OK] CLI runs" -ForegroundColor Green
} catch {
    Write-Host "[WARN] doc test failed. Run manually: $docCmd" -ForegroundColor Yellow
}

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "Deploy complete."
Write-Host "  Claude Code CLI: $env:USERPROFILE\.claude\skills\anysearch"
Write-Host "  Codex (shared):  $env:USERPROFILE\.agents\skills\anysearch"
Write-Host ""
Write-Host "Optional: configure an API key for higher rate limits (anonymous works too):"
Write-Host "  1. Visit https://anysearch.com/console/api-keys to create a free key"
Write-Host "  2. Edit ~/.claude/skills/anysearch/.env and set ANYSEARCH_API_KEY=<key>"
Write-Host ""
Write-Host "Verify a real search:"
Write-Host "  python $src\scripts\anysearch_cli.py search `"hello world`" --max_results 1"
Read-Host "`nPress Enter to exit"
