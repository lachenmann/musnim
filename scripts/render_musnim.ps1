param(
    [ValidateSet('low', 'medium')]
    [string]$Quality = 'medium'
)
$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))

$py = '.\.venv\Scripts\python.exe'
$flag = if ($Quality -eq 'low') { '-ql' } else { '-qm' }
& $py -m manim $flag 'projects/ZAR-001/scenes/zarathustra_pitagorico.py' ZarathustraPitagorico
if ($LASTEXITCODE -ne 0) {
    throw "Error al renderizar ZAR-001 en calidad $Quality"
}
Write-Host "Render ZAR-001 completado ($Quality)." -ForegroundColor Green
