$ErrorActionPreference = "Stop"
$base = "D:\ClaudeCodeFirst\scraped-images\yavor"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Fix Flora merge v2 - add 9 missing properties" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

$newProps = @(
    "apartament-404-khotel-flora",
    "apartament-11-mailili-rezidns",
    "apartament-03-tiulip-rezidns",
    "studio-18-tiulip-rezidns",
    "studio-02-violet-rezidns",
    "studio-05-tiulip-rezidns",
    "studio-409-khotel-flora",
    "studio-703-khotel-flora",
    "dvoina-staia-18-mailili-rezidns"
)

$backupPath = Join-Path $base "_manifest-v2-backup.json"
$manifestPath = Join-Path $base "_manifest.json"

Write-Host "`n[1/4] Reading backup (619 entries from before page-2 scrape)..." -ForegroundColor Yellow
$backup = Get-Content $backupPath -Raw | ConvertFrom-Json
Write-Host "   Backup: $($backup.Count) entries" -ForegroundColor Gray

Write-Host "`n[2/4] Reading new scrape manifest..." -ForegroundColor Yellow
$current = Get-Content $manifestPath -Raw | ConvertFrom-Json
Write-Host "   Current: $($current.Count) entries" -ForegroundColor Gray

Write-Host "`n[3/4] Extracting entries for new 9 properties..." -ForegroundColor Yellow
$newEntries = @()
foreach ($entry in $current) {
    if ($newProps -contains $entry.subfolder) {
        $fixed = [PSCustomObject]@{
            filename = $entry.filename
            subfolder = "apartamenti-v-komplex-flora/$($entry.subfolder)"
            original_url = $entry.original_url
            alt = $entry.alt
            found_on = $entry.found_on
            size_bytes = $entry.size_bytes
            cloudinary_url = $null
        }
        $newEntries += $fixed
    }
}
Write-Host "   Found entries for new properties: $($newEntries.Count)" -ForegroundColor Cyan

$grouped = $newEntries | Group-Object -Property subfolder
foreach ($g in $grouped) {
    $shortName = $g.Name -replace "apartamenti-v-komplex-flora/", ""
    Write-Host "     $shortName : $($g.Count)" -ForegroundColor Gray
}

Write-Host "`n[4/4] Final merge..." -ForegroundColor Yellow
$merged = @($backup) + @($newEntries)

Write-Host "   Final manifest: $($merged.Count) entries" -ForegroundColor Cyan
Write-Host "     Old (from backup): $($backup.Count)" -ForegroundColor Gray
Write-Host "     New (Flora page 2): $($newEntries.Count)" -ForegroundColor Gray

$mergedJson = $merged | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText($manifestPath, $mergedJson, [System.Text.Encoding]::UTF8)

Write-Host "`n================================================" -ForegroundColor Green
Write-Host "  DONE!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Now run upload:" -ForegroundColor Yellow
Write-Host "  python tools\scrape-and-upload-images.py --client-id yavor --upload-only --by-page" -ForegroundColor White
