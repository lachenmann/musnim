# Musnim — Instalación en Windows (PowerShell)

El fork está en https://github.com/lachenmann/musnim.
La ubicación recomendada de desarrollo es `D:\Proyectos\musnim`, con
entorno virtual `.venv` dentro del propio repositorio.

## Clonar directamente en D: (instalación nueva)

    New-Item -ItemType Directory -Force 'D:\Proyectos' | Out-Null
    Set-Location 'D:\Proyectos'
    git clone --branch feature/ZAR-001-bootstrap https://github.com/lachenmann/musnim.git
    Set-Location 'D:\Proyectos\musnim'
    git remote add upstream https://github.com/ManimCommunity/manim.git

## Trasladar un clon que ya existe en C: a D:

Este método conserva las ramas, los commits, la carpeta oculta `.git`,
los remotos `origin` y `upstream`, y cualquier trabajo local. Utiliza
`robocopy` para copiar entre volúmenes, conservando la copia de C:
hasta verificar que la de D: funciona.

    Set-Location $HOME
    $source = Join-Path $HOME 'Proyectos\musnim'
    $destination = 'D:\Proyectos\musnim'
    if (-not (Test-Path $source)) { throw "No existe $source" }
    if (Test-Path $destination) { throw "El destino ya existe: $destination" }
    New-Item -ItemType Directory -Force 'D:\Proyectos' | Out-Null
    robocopy $source $destination /E /COPY:DAT /DCOPY:DAT /R:2 /W:2 /NP
    if ($LASTEXITCODE -ge 8) { throw "Robocopy falló: $LASTEXITCODE" }
    Set-Location $destination
    git status -sb
    git remote -v
    git pull --ff-only origin feature/ZAR-001-bootstrap

Después de comprobar el clon de D:, puedes eliminar el clon de C:
manualmente. Evita borrar C: antes de revisar los cambios locales.

## Actualizar la rama existente

    Set-Location 'D:\Proyectos\musnim'
    git switch feature/ZAR-001-bootstrap
    git pull --ff-only origin feature/ZAR-001-bootstrap

## Instalar dependencias Python

Instala `uv` desde https://docs.astral.sh/uv/getting-started/installation/
o mediante:

    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

Para dejar también las descargas de Python y la caché de uv en D:,
configura estas variables en la sesión actual *antes* del bootstrap:

    $env:UV_CACHE_DIR = 'D:\Proyectos\.uv-cache'
    $env:UV_PYTHON_INSTALL_DIR = 'D:\Proyectos\.uv-python'

Abre otra ventana de PowerShell si acabas de instalar `uv`, repite
estas dos asignaciones y ejecuta:

    Set-Location 'D:\Proyectos\musnim'
    powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap_windows.ps1

El script instala el entorno de Manim, instala Musnim en modo editable,
ejecuta las pruebas y comprueba herramientas externas. Requiere conexión
a Internet durante la primera instalación.

## Herramientas de producción audiovisual

- LilyPond: https://lilypond.org/
- MiKTeX: https://miktex.org/download
- FFmpeg: https://ffmpeg.org/download.html

Comprueba:

    & $env:MUSNIM_LILYPOND --version
    latex --version
    dvisvgm --version
    ffmpeg -version

En Windows puede ser necesario configurar `MUSNIM_LILYPOND` con la ruta
completa a `lilypond.exe` cuando está fuera del `PATH`. Una vez
instaladas las herramientas:

    powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap_windows.ps1 -Render

El primer render es una prueba de integración. Si falla, registra
mensajes completos para corregir la compatibilidad real de SVG y Manim.

## LilyPond 2.26.0 (versión estable canónica de Musnim)

La versión estable fijada para el desarrollo inicial es 2.26.0.
La anterior 2.24.4 instalada en C: puede permanecer como respaldo,
sin necesidad de desinstalarla ni modificar su directorio.

El script descarga el ZIP oficial Windows x86_64 desde GitLab,
lo instala en `D:\Proyectos\.tools\lilypond-2.26.0`,
comprueba la versión y registra el ejecutable en
`MUSNIM_LILYPOND` (variable de usuario). Los scripts de Musnim
utilizan ese ejecutable incluso cuando la versión antigua está en PATH.

    Set-Location 'D:\Proyectos\musnim'
    git pull --ff-only origin feature/ZAR-001-bootstrap
    powershell -ExecutionPolicy Bypass -File .\scripts\install_lilypond_windows.ps1

Si GitLab falla, descargar LilyPond 2.26.0 para Windows x86_64 desde:
https://lilypond.org/download.es.html

El archivo fuente `projects/ZAR-001/score/naturmotiv_reduccion.ly`
declara `\version "2.26.0"` de forma reproducible.
Para comparar con partituras antiguas, puede usarse
`convert-ly` en una rama de trabajo; conservar siempre el original.

## Primera integración real de grabado

Abre una NUEVA ventana de PowerShell, para que Windows lea la nueva
variable MUSNIM_LILYPOND:

    cd D:\Proyectos\musnim
    .\.venv\Scripts\python.exe scripts\verify_lilypond.py

Esto valida LilyPond real, salida SVG y los identificadores de cabeza
de nota Do–Sol–Do. Si aprueba, intenta la escena audiovisual:

    powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap_windows.ps1 -Render

Si el render detecta diferencias en el SVG o la escena, conserva los
mensajes del error y corrige el código desde el PR #1. La verificación
de grabado real es un hito posterior a las 16 pruebas unitarias.
