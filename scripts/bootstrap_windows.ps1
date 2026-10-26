# Bootstrap Windows del fork de Manim + la extensión Musnim.
param([switch]$Render)
$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
$root = (Get-Location).Path

if (-not (Test-Path 'manim')) {
    throw 'Se requiere un clon verdadero del fork Manim Community.'
}
if (-not (Test-Path 'extensions/musnim/pyproject.toml')) {
    throw 'No se encontró la extensión Musnim.'
}
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw 'Instala uv desde https://docs.astral.sh/uv/getting-started/installation/.'
}

Write-Host '== Musnim: Python 3.12 ==' -ForegroundColor Cyan
& uv python install 3.12
if ($LASTEXITCODE -ne 0) { throw 'Error al instalar Python' }
& uv sync --python 3.12
if ($LASTEXITCODE -ne 0) { throw 'Error uv sync en el fork Manim' }

$py = Join-Path $root '.venv\Scripts\python.exe'
if (-not (Test-Path $py)) { throw "No se encontró $py" }

# --no-deps preserva el Manim editable del fork, en lugar de reemplazarlo
# por el paquete publicado en PyPI.
& uv pip install --python $py --no-deps -e '.\extensions\musnim'
if ($LASTEXITCODE -ne 0) { throw 'Error al instalar Musnim' }

Write-Host '== Musnim: pruebas ==' -ForegroundColor Cyan
& $py -m pytest -c 'extensions/musnim/pyproject.toml' 'extensions/musnim/tests' -q
if ($LASTEXITCODE -ne 0) { throw 'Las pruebas no aprobaron' }

$missing = @()
foreach ($name in @('latex', 'dvisvgm', 'ffmpeg')) {
    if (Get-Command $name -ErrorAction SilentlyContinue) {
        Write-Host "${name}: OK"
    } else {
        $missing += $name
        Write-Warning "${name}: pendiente"
    }
}
if ((Get-Command 'lilypond' -ErrorAction SilentlyContinue) -or
    ($env:MUSNIM_LILYPOND -and (Test-Path $env:MUSNIM_LILYPOND))) {
    Write-Host 'lilypond: OK'
} else {
    $missing += 'lilypond'
    Write-Warning 'lilypond: pendiente'
}

if ($Render) {
    if ($missing.Count -gt 0) {
        throw "Render pendiente por dependencias: $($missing -join ', ')"
    }
    & $py -m manim -ql 'projects/ZAR-001/scenes/zarathustra_pitagorico.py' ZarathustraPitagorico
    if ($LASTEXITCODE -ne 0) { throw 'Error al renderizar ZAR-001' }
}
Write-Host 'Bootstrap Musnim completado.' -ForegroundColor Green
