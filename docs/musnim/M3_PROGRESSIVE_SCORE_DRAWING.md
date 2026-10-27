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

- [x] El SVG LilyPond 2.26 contiene roles de StaffSymbol, Clef,
      TimeSignature, Stem y BarLine, e IDs de las tres NoteHead (Windows 26-10-2026).
- [x] Manim importa geometría individual para los siete grupos
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

## Primer ensayo de integración y corrección (26-10-2026)

La ejecución real de `inspect_score_drawing.py` en Windows generó el SVG
`naturmotiv_drawing-ecbba5f275b1.cropped.svg`. LilyPond 2.26.0
entregó estos metadatos de capa:

- `stem / g-1` (`draw-stem-g4`)
- `stem / c-2` (`draw-stem-c5`)
- `stem / c-1` (`draw-stem-c4`)

El diagnóstico se detuvo correctamente: `staff` carecía de grupo
identificado en el SVG (0 elementos). El resto de roles estructurales
también faltaba en el inventario, por lo que el render completo de
`AnimatedScoreDrawingDemo` seguía bloqueado.

### Causa y cambio propuesto

Las plicas se constituyen al procesar las notas y recibieron sus
`\once \override`. El pentagrama `StaffSymbol` y otros grobs
iniciales nacen durante la creación del contexto `Staff`.
LilyPond documenta que los atributos de StaffSymbol deben configurarse
antes de iniciar el pentagrama.

Se trasladaron los atributos de `StaffSymbol`, `Clef`,
`TimeSignature` y `BarLine` a `\new Staff \with { ... }`,
manteniendo las plicas y cabezas de nota en la secuencia musical.
Ahora `inspect_score_drawing.py` también muestra un inventario
compacto de grupos del SVG si falta una capa, para distinguir
la ausencia de etiqueta de un problema de geometría Manim.

**Estado:** modificación de código y pruebas sintácticas integradas;
el resultado con el SVG LilyPond real debe verificarse nuevamente
en Windows antes de declarar la solución completa.

    cd D:\Proyectos\musnim
    git pull --ff-only origin feature/M3-score-drawing
    .\.venv\Scripts\python.exe .\scripts\inspect_score_drawing.py

Si los siete roles se detectan y se validan las tres cabezas de nota,
renderizar con el comando de la sección anterior. Conservar la salida
completa de errores si algún símbolo sigue ausente.

## Segundo ensayo real: diez componentes reconocidos (26-10-2026)

El usuario ejecutó la versión corregida de `inspect_score_drawing.py`
en Windows, desde `D:\Proyectos\musnim`. LilyPond 2.26 generó el
SVG `naturmotiv_drawing-79685e214f5a.cropped.svg` y el diagnóstico
terminó con **OK**.

| Rol / nota | ID gráfico | Centro Manim (x, y) | Tamaño (ancho × alto) |
| --- | --- | --- | --- |
| Pentagrama | draw-staff | (-0.011, -0.049) | 8.379 × 1.703 |
| Clave | draw-clef | (-3.330, 0.001) | 1.095 × 3.114 |
| Compás | draw-meter | (-1.773, -0.050) | 0.737 × 0.894 |
| Plica Do4 | draw-stem-c4 | (-0.040, -0.542) | 0.055 × 1.410 |
| Plica Sol4 | draw-stem-g4 | (1.344, 0.309) | 0.055 × 1.410 |
| Plica Do5 | draw-stem-c5 | (2.187, -0.637) | 0.055 × 1.379 |
| Barra final | draw-barline | (4.055, -0.049) | 0.289 × 1.703 |
| Cabeza Do4 | c-1 | disponible | 0.555 × 0.463 |
| Cabeza Sol4 | g-1 | disponible | 0.555 × 0.463 |
| Cabeza Do5 | c-2 | disponible | 0.586 × 0.463 |

**Conclusión de integración:** el traslado de los atributos de los
grobs iniciales al bloque `\new Staff \with { ... }` permitió
identificar efectivamente todos los roles, con geometrías positivas
y separadas. Las plicas y cabezas siguen enlazadas a los eventos
musicales de Do–Sol–Do.

**Pendiente:** las dimensiones y los IDs demuestran acceso individual
a la geometría; queda por comprobar cómo se dibujan en movimiento.
El siguiente control es generar el MP4 de `AnimatedScoreDrawingDemo`,
inspeccionando pentagrama, clave, compás, notas, plicas, barra y audio.

    cd D:\Proyectos\musnim
    .\.venv\Scripts\python.exe -m manim -ql projects/ZAR-001/scenes/score_drawing_demo.py AnimatedScoreDrawingDemo
    .\.venv\Scripts\python.exe .\scripts\qa_score_drawing_video.py

Conservar el PR #7 en borrador hasta revisar el MP4 real.


## Primera generación real del video 20 s (26-10-2026)

El usuario ejecutó en Windows la escena `AnimatedScoreDrawingDemo`
con Manim Community 0.22.0, a partir de la misma partitura LilyPond
que había superado el diagnóstico estructural de diez componentes.

- **22 animaciones** procesadas.
- Archivo resultante: `media/videos/score_drawing_demo/480p15/AnimatedScoreDrawingDemo.mp4`.
- Verificación con `qa_score_drawing_video.py` completada con **OK**.
- Duración: **20,032 segundos**.
- Resolución: **854 × 480**, **15 fps**.
- Códecs: **H.264** (imagen) y **AAC** (audio).
- El mensaje de FFmpeg `Some options were not used` fue una advertencia
  no bloqueante. En el fragmento del log enviado no aparecen
  advertencias de tipos de elementos SVG no admitidos.

**Conclusión:** el flujo de grabado por componentes superó la
integración real de ejecución y los controles técnicos de contenedor
en Windows. La inspección visual de las animaciones, el contorno de los
glifos y el alineamiento entre notas y sonido continúa pendiente,
por lo que el PR #7 debe permanecer en borrador.

### Próxima comprobación

Abrir o adjuntar el video generado:

    Start-Process "D:\Proyectos\musnim\media\videos\score_drawing_demo\480p15\AnimatedScoreDrawingDemo.mp4"

Revisar los primeros segundos para comprobar que el pentagrama se
traza con las cinco líneas, que la clave y el compás se dibujan
correctamente y que cada plica acompaña a su nota. Revisar
especialmente los segundos 8, 11, 14, 17 y 19 en sincronía con
la pista sintética. Los criterios relativos a apariencia y
sincronización quedarán pendientes hasta examinar el MP4 real.

## Auditoría del primer MP4 por fotogramas — 26-10-2026

Se recibió y revisó directamente AnimatedScoreDrawingDemo.mp4 generado en
Windows. FFprobe confirmó 20,032 s, 854×480, 15 fps, 300 fotogramas,
H.264 y AAC estéreo a 48 kHz.

### Hallazgos aprobados

- [x] Se trazan progresivamente las cinco líneas del pentagrama (≈1–3,3 s).
- [x] La clave de sol y el indicador de compás se construyen por etapas.
- [x] Las tres cabezas y sus plicas se dibujan individualmente.
- [x] La barra final se añade alrededor de 18 s.
- [x] Los rótulos de Do, Sol y Do' se alinean con las respectivas notas.
- [x] El resaltado de las notas se mantiene durante los sonidos.
- [x] La pista contiene Do grave ≈131 Hz (introducción), Do4 ≈262 Hz
      entre 8–11 s, Sol4 ≈392 Hz entre 11–14 s y Do5 ≈523 Hz
      entre 14–20 s, según el calendario didáctico.

### Ajustes de maquetación detectados

1. **P1, 17–20 s:** la ecuación f_C:f_G:f_C'=2:3:4 compartía la
   misma franja que los nombres de las notas, dificultando su lectura.
   El segundo código desplaza la ecuación de DOWN*1.68 a DOWN*2.48
   unidades de Manim, manteniendo intactos los eventos y la duración.
2. **P2, ≈4–5 s:** el compás 4/4 aparecía como C, la notación usual
   de compás común. Para mostrar explícitamente 4/4 en esta explicación,
   se añadió el comando LilyPond `\numericTimeSignature` antes
   de `\time 4/4`, preservando el rol gráfico `draw-meter`.

Los cambios están en el commit `b48698d0` del PR #7, junto con
dos pruebas de regresión. **La corrección visual todavía requiere
un segundo render y la inspección del nuevo MP4.** La partitura
sigue siendo una reducción didáctica; el análisis orquestal exacto
de los primeros 21 compases de Strauss corresponde al Issue #3.

### Repetir el control en el PC

    cd D:\Proyectos\musnim
    git pull --ff-only origin feature/M3-score-drawing
    .\.venv\Scripts\python.exe .\scripts\inspect_score_drawing.py
    .\.venv\Scripts\python.exe -m manim -ql projects/ZAR-001/scenes/score_drawing_demo.py AnimatedScoreDrawingDemo
    .\.venv\Scripts\python.exe .\scripts\qa_score_drawing_video.py

Conservar la primera versión del MP4 antes de volver a renderizar.
El control de SVG debe aprobar antes de intentar el segundo video.
