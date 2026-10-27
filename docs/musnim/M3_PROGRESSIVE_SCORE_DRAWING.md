# M3 — Grabado musical dibujado progresivamente

Estado: PROTOTIPO EXPERIMENTAL, pendiente de validación real en Windows.
Rama: feature/M3-score-drawing, basada en feature/M3-semantic-notes.
Destino del PR: feature/M3-semantic-notes (PR #6).

## Objetivo

Construir animaciones en que la partitura aparezca como los objetos
geométricos de Manim, preservando a LilyPond como autoridad gráfica.

- Create: trazado del pentagrama, plicas y barra de compás.
- DrawBorderThenFill: contornos y rellenos de clave, indicación de compás
  y cabezas de nota.
- Write: títulos, nombres de las notas y MathTex para proporciones.
- Los objetos de LilyPond pueden posteriormente recibir Indicate,
  Transform, FadeIn, FadeOut y animaciones de color.

En el primer prototipo, los elementos se presentan en el orden:
título → líneas del pentagrama → clave de sol → indicación 4/4 →
Do4 + plica → Sol4 + plica → Do5 + plica → proporción 2:3:4 →
barra final. Los tres sonidos tienen un calendario compartido con
el color de sus notas: C4 8–11 s, G4 11–14 s y C5 14–20 s.

La duración y el ritmo de la partitura son didácticos. Los compases
orquestales 1–21 de Strauss se encuentran pendientes de cotejo (Issue #3).

## Cómo funciona

LilyPond puede asignar atributos a los grobs mediante
output-attributes. El archivo naturmotiv_drawing.ly utiliza:

- StaffSymbol -> data-musnim-role="staff"
- Clef -> data-musnim-role="clef"
- TimeSignature -> data-musnim-role="meter"
- Stem -> data-musnim-role="stem", data-musnim-owner="<ID musical>"
- NoteHead -> data-musnim-id="<ID musical>"
- BarLine -> data-musnim-role="barline"

Cada elemento también conserva un ID SVG estable. Un nuevo lector puro,
musnim.score_layers, valida la estructura XML. DrawingScore, subclase
de SemanticScore, accede a los elementos vectoriales importados por Manim
mediante id_to_vgroup_dict o IDs de formas individuales. El orden del
DOM SVG permanece independiente del orden musical.

## Requisitos y primera prueba en Windows

Conservar por separado los MP4 ZAR-001 y las escenas anteriores de M3.
Para entrar en la rama del experimento desde la rama actual M3:

    cd D:\Proyectos\musnim
    git status --short
    git fetch origin
    git switch --track origin/feature/M3-score-drawing

Si la rama ya existe localmente, usar git switch feature/M3-score-drawing
y git pull --ff-only origin feature/M3-score-drawing.

PRIMER CONTROL OBLIGATORIO: comprobar que el SVG real contiene grupos
válidos y que Manim los interpreta como objetos individuales:

    .\.venv\Scripts\python.exe .\scripts\inspect_score_drawing.py

Esperado: pantallazo de IDs para staff, clef, meter, tres stems, barline
y tres cabezas de nota, todos con geometría de dimensiones positivas.

SEGUNDO CONTROL, solamente después del diagnóstico correcto:

    .\.venv\Scripts\python.exe -m manim -ql projects/ZAR-001/scenes/score_drawing_demo.py AnimatedScoreDrawingDemo

    .\.venv\Scripts\python.exe .\scripts\qa_score_drawing_video.py

Archivo de salida (20 s nominales):

    media/videos/score_drawing_demo/480p15/AnimatedScoreDrawingDemo.mp4

Se recomienda revisar a 1–6 s la construcción del pentagrama,
clave y compás; a 8, 11 y 14 s las notas; a 17–20 s la proporción
y el cierre.

## Criterios de aceptación

- [ ] El SVG LilyPond 2.26 contiene roles de StaffSymbol, Clef,
      TimeSignature, Stem y BarLine y un ID para cada NoteHead.
- [ ] Manim importa geometría individual para los ocho grupos
      Staff/Clef/Meter/Stem×3/BarLine y tres NoteHeads.
- [ ] El pentagrama se traza progresivamente, conservando grosor,
      separación y contornos legibles.
- [ ] Los signos musicales se dibujan con Create o DrawBorderThenFill.
- [ ] Las notas coinciden con el audio sintetizado y se mantienen
      iluminadas según el calendario de eventos.
- [ ] No se omiten símbolos de LilyPond ni aparecen grupos ajenos.
- [ ] El MP4 supera el QA de imagen, audio y duración.
- [ ] Validar en Windows y probar la portabilidad del flujo a macOS/Linux.
- [ ] Revisar el video real antes de incorporar el componente al motor
      principal de Musnim.

## Problemas previstos y controles

LilyPond organiza los grobs en su estructura gráfica propia. Por eso
no se debe animar usando índices posicionales de submobjects: utilizar
IDs y roles explícitos. Un SVG puede contener glifos tipográficos
representados por nodos <text>, actualmente ignorados por Manim 0.22.
La prueba de geometría permite detectar si un símbolo de clave o
compás necesita conversión vectorial o un tratamiento específico.

El contexto de la partitura está reducido a una voz y tres alturas.
El próximo contrato deberá admitir clefs variables, instrumentos,
alteraciones, ligaduras, barras, articulaciones, dinámicas,
multi-staff y polifonía temporal.

Fuentes técnicas:
https://lilypond.org/doc/v2.26/Documentation/notation/alternative-output-formats
https://docs.manim.community/en/stable/_modules/manim/animation/creation.html
https://docs.manim.community/en/stable/reference/manim.mobject.svg.svg_mobject.SVGMobject.html
