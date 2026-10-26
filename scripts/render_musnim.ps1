$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
$py = '.\.venv\Scripts\python.exe'
& $py -m manim -ql 'projects/ZAR-001/scenes/zarathustra_pitagorico.py' ZarathustraPitagorico
if ($LASTEXITCODE -ne 0) { throw 'Render fallido' }
