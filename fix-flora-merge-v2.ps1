# fix-flora-merge-v2.ps1
# Поправя предишния опит — добавя 9-те Flora имота в manifest-а
# с правилен subfolder prefix.

$ErrorActionPreference = "Stop"
$base = "D:\ClaudeCodeFirst\scraped-images\yavor"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Fix Flora merge v2 — добавяме 9-те имота" -ForegroundColor Cyan
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

# Започваме от backup-а (чистия 619 entries преди page-2 scrape-а)
$backupPath = Join-Path $base "_manifest-v2-backup.json"
$manifestPath = Join-Path $base "_manifest.json"

Write-Host "`n[1/4] Чета backup-а (619 entries преди новия scrape)..." -ForegroundColor Yellow
$backup = Get-Content $backupPath -Raw | ConvertFrom-Json
Write-Host "   Backup: $($backup.Count) entries" -ForegroundColor Gray

# Текущият manifest има 365 entries — много от тях са същите като backup
# Но има и нови entries за 9-те Flora имота с грешен subfolder
Write-Host "`n[2/4] Чета новия scrape manifest..." -ForegroundColor Yellow
$current = Get-Content $manifestPath -Raw | ConvertFrom-Json
Write-Host "   Current: $($current.Count) entries" -ForegroundColor Gray

# Извличаме само entries за новите 9 имота — те имат subfolder без префикс
Write-Host "`n[3/4] Извличам entries за новите 9 имота..." -ForegroundColor Yellow
$newEntries = @()
foreach ($entry in $current) {
    if ($newProps -contains $entry.subfolder) {
        # Поправяме subfolder-а
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
Write-Host "   Намерени entries за нови имоти: $($newEntries.Count)" -ForegroundColor Cyan

# Per-property breakdown
$grouped = $newEntries | Group-Object -Property subfolder
foreach ($g in $grouped) {
    $shortName = $g.Name -replace "apartamenti-v-komplex-flora/", ""
    Write-Host "     $shortName : $($g.Count)" -ForegroundColor Gray
}

# Финален merge — backup + new entries (вече с правилен subfolder)
Write-Host "`n[4/4] Финален merge..." -ForegroundColor Yellow
$merged = @($backup) + @($newEntries)

Write-Host "   Финален manifest: $($merged.Count) entries" -ForegroundColor Cyan
Write-Host "     Стари (от backup): $($backup.Count)" -ForegroundColor Gray
Write-Host "     Нови (Flora page 2): $($newEntries.Count)" -ForegroundColor Gray

# Записваме
$mergedJson = $merged | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText($manifestPath, $mergedJson, [System.Text.Encoding]::UTF8)

Write-Host "`n================================================" -ForegroundColor Green
Write-Host "  ✅ Готово!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Сега пусни upload:" -ForegroundColor Yellow
Write-Host "  python tools\scrape-and-upload-images.py --client-id yavor --upload-only --by-page" -ForegroundColor White
Write-Host ""
Write-Host "Cloudinary няма да дублира — ще качи само новите снимки." -ForegroundColor Gray
