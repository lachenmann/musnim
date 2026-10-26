# Instalación de LilyPond 2.26.0 desde el paquete oficial para Windows.
# Todos los archivos se guardan en D:, fuera del repositorio Git.
param([string]$InstallRoot = "D:\Proyectos\.tools\lilypond-2.26.0")
$ErrorActionPreference = 'Stop'

$url = 'https://gitlab.com/lilypond/lilypond/-/releases/v2.26.0/downloads/lilypond-2.26.0-mingw-x86_64.zip'
$archive = Join-Path $InstallRoot 'lilypond-2.26.0-mingw-x86_64.zip'
New-Item -ItemType Directory -Force -Path $InstallRoot | Out-Null

$found = @(Get-ChildItem -LiteralPath $InstallRoot -Filter 'lilypond.exe' -File -Recurse -ErrorAction SilentlyContinue)
if ($found.Count -eq 0) {
    if (-not (Test-Path -LiteralPath $archive)) {
        $partial = "$archive.partial"
        try {
            Write-Host 'Descargando LilyPond 2.26.0 desde GitLab oficial...' -ForegroundColor Cyan
            Invoke-WebRequest -Uri $url -OutFile $partial -UseBasicParsing
            if ((Get-Item -LiteralPath $partial).Length -lt 100000) {
                throw 'La descarga parece incompleta.'
            }
            Move-Item -LiteralPath $partial -Destination $archive -Force
        }
        finally {
            if (Test-Path -LiteralPath $partial) {
                Remove-Item -LiteralPath $partial -Force
            }
        }
    }
    Write-Host 'Extrayendo el paquete en D:...' -ForegroundColor Cyan
    Expand-Archive -LiteralPath $archive -DestinationPath $InstallRoot -Force
    $found = @(Get-ChildItem -LiteralPath $InstallRoot -Filter 'lilypond.exe' -File -Recurse -ErrorAction SilentlyContinue)
}
if ($found.Count -ne 1) {
    throw "Se esperaba un lilypond.exe en $InstallRoot; encontrados: $($found.Count)"
}

$exe = $found[0].FullName
$versionText = (& $exe --version 2>&1 | Out-String)
if ($LASTEXITCODE -ne 0 -or $versionText -notmatch '2\.26\.0') {
    throw "No se pudo verificar LilyPond 2.26.0: $versionText"
}

# El motor Musnim acepta MUSNIM_LILYPOND incluso si LilyPond no está en PATH.
$env:MUSNIM_LILYPOND = $exe
[Environment]::SetEnvironmentVariable('MUSNIM_LILYPOND', $exe, 'User')

Write-Host $versionText.Trim()
Write-Host "LilyPond disponible en: $exe" -ForegroundColor Green
Write-Host 'Siguiente paso, en una nueva terminal:'
Write-Host '  cd D:\Proyectos\musnim'
Write-Host '  .\.venv\Scripts\python.exe scripts\verify_lilypond.py'
