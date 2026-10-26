# Musnim — Motor abierto de animación musical

Estado: prealfa 0.1.0a0 · Primer proyecto ZAR-001 · 26-10-2026.

Musnim es una bifurcación de Manim Community Edition orientada a la
representación musical. Conserva la base original y el vínculo con
ManimCommunity/manim para recibir mejoras del proyecto original.

La primera etapa incorpora herramientas musicales en extensions/musnim,
con una arquitectura modular. LilyPond genera partituras SVG; LaTeX a través
de Manim MathTex presenta modelos matemáticos y proporciones. Python
genera la animación, cálculos racionales y sonido demostrativo.

Plataformas objetivo: Windows, macOS y Linux.

## ZAR-001: El amanecer de las proporciones

Primera película de prueba, dedicada a los compases iniciales de
Also sprach Zarathustra, op. 30, de Richard Strauss.

El prototipo presenta el motivo Do–Sol–Do, las relaciones 2:3:4,
las terceras pitagóricas y justas, y una comparación auditiva de las
tríadas mayor y menor. Se mantiene una distinción explícita entre
modelos de afinación y el sonido real de la orquesta.

La partitura LilyPond actual es una reducción esquemática de alturas.
La transcripción crítica de los compases 1–21, el render real en Manim,
la sincronización con grabación autorizada y la animación semántica
de notas siguen siendo hitos separados.

## Carpetas Musnim

- extensions/musnim: librería Python con razones, audio y SVG LilyPond.
- projects/ZAR-001: fuente LilyPond, escenas, cues, guion y fuentes.
- docs/musnim: arquitectura, hoja de ruta y guía de Windows.
- scripts: preparación del entorno y comandos de render.
- .github/workflows: pruebas unitarias multiplataforma.

Leer docs/musnim/WINDOWS_SETUP.md para preparar el fork en Windows.

La biblioteca Obsidian personal y los PDFs protegidos están fuera
del repositorio público. Se conservan todas las licencias de Manim
Community; el código nuevo Musnim usa licencia MIT propia.
