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
