# Musnim — Instalación en Windows (PowerShell)

El fork es https://github.com/lachenmann/musnim.

## Clonar

Instala Git para Windows, abre PowerShell y ejecuta:

    New-Item -ItemType Directory -Force "$HOME\Proyectos" | Out-Null
    cd "$HOME\Proyectos"
    git clone https://github.com/lachenmann/musnim.git
    cd musnim
    git remote add upstream https://github.com/ManimCommunity/manim.git
    git fetch origin
    git switch feature/ZAR-001-bootstrap

Si upstream ya existe, consulta git remote -v y consérvalo.

## Instalar dependencias Python

Instala uv desde https://docs.astral.sh/uv/getting-started/installation/
o mediante:

    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

Abre otra ventana de PowerShell, vuelve al directorio del repo y ejecuta:

    powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap_windows.ps1

El script instala el entorno Python de Manim y la extensión Musnim
en modo editable, ejecuta las pruebas Python y comprueba herramientas
externas. Necesita conexión a Internet durante la primera instalación.

## Herramientas de producción audiovisual

- LilyPond: https://lilypond.org/
- MiKTeX: https://miktex.org/download
- FFmpeg: https://ffmpeg.org/download.html

Comprueba:

    lilypond --version
    latex --version
    dvisvgm --version
    ffmpeg -version

En Windows puede ser necesario configurar MUSNIM_LILYPOND con la ruta
completa a lilypond.exe cuando está fuera del PATH. Cuando las cuatro
herramientas estén presentes, ejecuta:

    powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap_windows.ps1 -Render

El prototipo es una prueba de integración inicial: si falla,
guardar las trazas para corregir la compatibilidad de SVG y Manim.
