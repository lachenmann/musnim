# Render reproducible del grabado LilyPond sin reutilizar segmentos de Manim.
# Preserva automáticamente la versión anterior del MP4 para compararla.
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $repo

$python = Join-Path $repo '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) {
    throw "Falta el entorno Python de Musnim: $python"
}

$video = Join-Path $repo 'media\videos\score_drawing_demo\480p15\AnimatedScoreDrawingDemo.mp4'
$backupDir = Join-Path (Split-Path -Parent $repo) 'Musnim-renders'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

if (Test-Path -LiteralPath $video) {
    $timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
    $backup = Join-Path $backupDir "M3_Dibujo_antes_del_render_limpio_$timestamp.mp4"
    Copy-Item -LiteralPath $video -Destination $backup -ErrorAction Stop
    Write-Host "Copia anterior conservada: $backup" -ForegroundColor Cyan
}

Write-Host 'Renderizando M3.1 con caché deshabilitada...' -ForegroundColor Cyan
& $python -m manim --disable_caching -ql 'projects/ZAR-001/scenes/score_drawing_demo.py' AnimatedScoreDrawingDemo
if ($LASTEXITCODE -ne 0) {
    throw "Error en render sin caché: código $LASTEXITCODE"
}

Write-Host 'Comprobando video y audio de la versión recién creada...' -ForegroundColor Cyan
& $python '.\scripts\qa_score_drawing_video.py'
if ($LASTEXITCODE -ne 0) {
    throw "El control audiovisual falló: código $LASTEXITCODE"
}

Write-Host 'Render limpio M3.1 completado; pendiente revisión visual del MP4.' -ForegroundColor Green
