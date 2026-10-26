# QA de video ZAR-001 — primer render en Windows

La primera escena se ha renderizado con Manim Community 0.22.0 en Windows
el 26 de octubre de 2026. La consola informó "Rendered ZarathustraPitagorico",
"Played 30 animations" y el MP4 en resolución 480p15.

## Comprobación técnica

Desde D:\Proyectos\musnim:

    .\.venv\Scripts\python.exe .\scripts\qa_zar001_video.py

El verificador consulta FFprobe (normalmente incluido con FFmpeg) y exige:
duración de 79 ± 2 segundos, resolución de al menos 640×360, 10 fps
o más y presencia de una pista de audio. Comprueba que el contenedor
sea reproducible a nivel de metadatos, no escucha ni mira su contenido.

## Revisión visual y sonora manual

Abrir en Windows:

    Start-Process 'D:\Proyectos\musnim\media\videos\zarathustra_pitagorico\480p15\ZarathustraPitagorico.mp4'

Revisar el tramo con el pentagrama (aproximadamente 8–20 s), el motivo
Do–Sol–Do, las ecuaciones y el paso entre sonoridades mayor y menor.
Confirmar que el audio es audible a lo largo del clip y que su comienzo
está sincronizado con el primer gesto visual previsto.

## Hallazgo de compatibilidad SVG

En el primer render se registraron advertencias de Manim:
"Unsupported element type: <class 'svgelements.svgelements.Text'>".

Manim 0.22.0 aún carece de conversión SVG <text> a VMobject.
Esto puede provocar que elementos tipográficos del grabado LilyPond
desaparezcan al importarlo mediante SVGMobject. Por tanto, aunque
el MP4 existe, hay que inspeccionar el pentagrama para comprobar qué
aparece y qué falta.

Opciones de solución para un futuro PR de M1:
- convertir texto SVG a trazados vectoriales en una etapa de
  preprocesamiento, preservando los atributos data-musnim-id;
- separar el pentagrama de la tipografía y reconstruir títulos y
  etiquetas con los objetos Text de Manim.

Se necesita una comparación visual del MP4 real con el SVG de origen
antes de decidir una conversión automática. Mantener LilyPond como
autoridad del grabado y el manifiesto de eventos como cronología musical.

Documentación de referencia:
- https://docs.manim.community/en/stable/reference/manim.mobject.svg.svg_mobject.SVGMobject.html
- https://lilypond.org/doc/v2.26/Documentation/notation/alternative-output-formats

## Segunda iteración después de la revisión visual

Se incorporó un refactor de composición al PR #1: partitura LilyPond
centrada en una sección separada, anotaciones con franjas propias,
fórmulas MathTex después de retirar el pentagrama y transiciones por
fundido. Es una propuesta **pendiente de validación en video**, no un
resultado garantizado por las pruebas Python.

Para producir una vista de revisión a 720p30 desde PowerShell:

    cd D:\Proyectos\musnim
    git pull --ff-only origin feature/ZAR-001-bootstrap
    powershell -ExecutionPolicy Bypass -File .\scripts\render_musnim.ps1
    .\.venv\Scripts\python.exe .\scripts\qa_zar001_video.py

El script QA selecciona el MP4 más reciente dentro de las carpetas de
calidad de Manim. Para analizar un video concreto puede utilizarse:

    .\.venv\Scripts\python.exe .\scripts\qa_zar001_video.py --video "RUTA_AL_MP4"

Revisar especialmente 8–20, 21–27 y 39–55 s del nuevo render.

## Segundo corte HD: resultado técnico confirmado en Windows (26-10-2026)

El usuario ejecutó `scripts/qa_zar001_video.py` sobre el nuevo render y
compartió los resultados:

- Archivo: `media/videos/zarathustra_pitagorico/720p30/ZarathustraPitagorico.mp4`.
- Duración: **79,04 segundos**.
- Resolución: **1280 × 720**.
- Fotogramas por segundo: **30,0**.
- Códecs: **H.264** (video), **AAC** (audio).
- Resultado del verificador: **OK**, video y audio presentes y duración coherente.

Esta evidencia valida técnicamente el segundo render. La presencia de
una pista de audio demuestra que fue multiplexada en el archivo; la
sincronización fina y el contenido auditivo requieren inspección directa.
La revisión visual de los solapes, la tipografía, el pentagrama y las
transiciones permanece **pendiente** hasta recibir o inspeccionar el MP4
HD real. Conservar abierto el Issue #4 y el PR #1 en borrador.

## Tercer corte HD: resultado técnico informado por el usuario (26-10-2026)

El tercer render basado en `CueClock.exchange` finalizó en Windows:

- Manim Community 0.22.0: `Rendered ZarathustraPitagorico`.
- Total: **42 animaciones** procesadas.
- Archivo: `media/videos/zarathustra_pitagorico/720p30/ZarathustraPitagorico.mp4`.
- Inspección con `qa_zar001_video.py`: **79,164 segundos**,
  **1280 × 720**, **30,001 fps**, video **H.264** y audio **AAC**.
- Mensaje: `OK: el MP4 contiene video y audio y presenta duración coherente.`
- Advertencia de FFmpeg `Some options were not used`: no bloqueó el
  resultado audiovisual.

**Alcance de esta evidencia:** confirma creación del contenedor, parámetros
del archivo y presencia de las pistas. La ausencia de superposición de
fórmulas, calidad del texto SVG, inteligibilidad del audio y sincronización
musical fina exigen una inspección del tercer MP4 real.

La duración difiere ligeramente del valor nominal de 79,0 s; queda
dentro de la tolerancia ya documentada de ±2 s. Conservar los renders
anteriores para realizar comparaciones reproducibles.

## Verificación independiente del tercer MP4 aportado (26-10-2026)

Tras recibir el archivo real, FFprobe confirmó **79,163737 s, 1280×720,
30 fps, H.264, AAC estéreo 48 kHz, 2375 fotogramas**. La pista sonora
decodificada a PCM mono de 48 kHz tiene **3 793 920 muestras** y su
SHA-256 coincide exactamente con las versiones 1 y 2:

`4d1fa61bcc26e701995c96ae98a985cb08927d5c344850d3835ba23f645f876c`.

La verificación visual muestra que las transiciones de fórmula son
secuenciales y carecen de doble exposición. Para el detalle por segundo,
consultar `VIDEO_REVIEW_2026-10-26.md`.
