# Actualización independiente de LilyPond para uso general en C:.
# Preserva MUSNIM_LILYPOND, el repositorio de D: y las versiones anteriores.
param(
    [ValidatePattern('^\d+\.\d+\.\d+$')]
    [string]$Version = '2.26.0'
)
$ErrorActionPreference = 'Stop'

$root = Join-Path $env:LOCALAPPDATA 'Programs\LilyPond'
$install = Join-Path $root "lilypond-$Version"
$archive = Join-Path $env:TEMP "lilypond-$Version-mingw-x86_64.zip"
$url = "https://gitlab.com/lilypond/lilypond/-/releases/v$Version/downloads/lilypond-$Version-mingw-x86_64.zip"

New-Item -ItemType Directory -Force -Path $install | Out-Null
$found = @(Get-ChildItem -LiteralPath $install -Filter 'lilypond.exe' -File -Recurse -ErrorAction SilentlyContinue)

if ($found.Count -eq 0) {
    if (-not (Test-Path -LiteralPath $archive)) {
        $partial = "$archive.partial"
        try {
            Write-Host 'Descargando el paquete oficial de LilyPond...' -ForegroundColor Cyan
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
    Expand-Archive -LiteralPath $archive -DestinationPath $install -Force
    $found = @(Get-ChildItem -LiteralPath $install -Filter 'lilypond.exe' -File -Recurse -ErrorAction SilentlyContinue)
}

if ($found.Count -ne 1) {
    throw "Se esperaba un único ejecutable lilypond.exe; encontrados: $($found.Count)"
}
$exe = $found[0].FullName
$versionOutput = (& $exe --version 2>&1 | Out-String)
if ($LASTEXITCODE -ne 0 -or $versionOutput -notmatch [regex]::Escape($Version)) {
    throw "LilyPond no coincide con la versión solicitada: $versionOutput"
}

# Solo actualizamos el PATH de USUARIO para el LilyPond general de C:.
# Nunca modificamos MUSNIM_LILYPOND, que debe señalar al LilyPond de D:.
$bin = (Split-Path -Parent $exe).TrimEnd('\')
$prefix = ([IO.Path]::GetFullPath($root).TrimEnd('\') + '\')
$userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
$remaining = @(
    foreach ($item in ($userPath -split ';')) {
        $value = $item.Trim()
        if (-not $value) { continue }
        $expanded = [Environment]::ExpandEnvironmentVariables($value)
        try {
            $normalized = [IO.Path]::GetFullPath($expanded).TrimEnd('\')
        }
        catch {
            $normalized = $expanded.TrimEnd('\')
        }
        $inGeneralLilyPond = $normalized.StartsWith(
            $prefix, [StringComparison]::OrdinalIgnoreCase
        )
        $versionedBin = $normalized -match '\\lilypond-\d+\.\d+\.\d+\\bin$'
        if ($inGeneralLilyPond -and $versionedBin) { continue }
        if ($normalized.Equals($bin, [StringComparison]::OrdinalIgnoreCase)) { continue }
        $value
    }
)
$newUserPath = (@($bin) + $remaining) -join ';'
[Environment]::SetEnvironmentVariable('Path', $newUserPath, 'User')

Write-Host $versionOutput.Trim()
Write-Host "LilyPond general instalado en: $exe" -ForegroundColor Green
Write-Host 'PATH de usuario actualizado para usar LilyPond de C:.'
Write-Host 'MUSNIM_LILYPOND no se ha modificado.'
Write-Host 'Abre una nueva terminal para comprobar: lilypond --version'
