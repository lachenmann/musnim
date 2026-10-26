# ZAR-001 — El amanecer de las proporciones

Primer laboratorio audiovisual de Musnim, dedicado al motivo Do–Sol–Do
de Also sprach Zarathustra, op. 30, de Richard Strauss.

La notación es LilyPond, el análisis matemático usa LaTeX mediante
MathTex y el diseño visual utiliza Manim Community.

## Estado de las fuentes

La partitura de score/naturmotiv_reduccion.ly es una reducción didáctica de
alturas con ritmo esquemático. La transcripción orquestal de los
compases 1–21, sus instrumentos transpositores y la sincronización con
una interpretación musical requieren un cotejo documental posterior.
Las razones de afinación expuestas son modelos ideales.

`score/naturmotiv_events.json` define el orden musical de Do–Sol–Do
(IDs, alturas, inicios y duraciones esquemáticos). LilyPond genera el SVG
con un orden interno de nodos independiente, comprobado por presencia
exacta de IDs. Un orden del DOM diferente al musical es una propiedad
admisible del grabado, y no modifica la cronología de la reducción.

## Render

Con dependencias externas instaladas y la extensión importable:

    python -m manim -ql projects/ZAR-001/scenes/zarathustra_pitagorico.py ZarathustraPitagorico

La salida del prototipo tiene 79 segundos y usa audio sintético original.
No hay en este proyecto grabaciones comerciales ni PDF bibliográficos.

## Primer render efectivo (Windows, 26-10-2026)

Manim Community 0.22.0 completó 30 animaciones a 480p15 y creó
`media/videos/zarathustra_pitagorico/480p15/ZarathustraPitagorico.mp4`.
El registro confirma generación del archivo; la verificación independiente
de su pista sonora, duración efectiva y aspecto visual sigue pendiente.
Ejecutar `python scripts/qa_zar001_video.py` y consultar
`docs/musnim/VIDEO_QA.md`. Manim advirtió que ciertos nodos SVG
`<text>` de LilyPond no son soportados; el pentagrama necesita
inspección visual antes de aprobar el primer corte.

## Corrección de maquetación — segunda iteración

La primera inspección del MP4 480p15 reveló solapes de fórmula, pentagrama
y anotaciones. La nueva escena separa las franjas tipográfica, musical
y matemática, utiliza fundidos entre expresiones y reserva el texto
editorial a los objetos Text de Manim. Pendiente de verificar visualmente
con el siguiente render. Informe: `docs/musnim/VIDEO_REVIEW_2026-10-26.md`.

## Revisión comparada del segundo MP4 HD

El segundo corte resuelve las colisiones persistentes entre partitura,
etiquetas y fórmulas. El audio original permanece idéntico al del primer
render. Se registró `CueClock.exchange` para suprimir la doble exposición
transitoria de fórmulas mediante dos fases secuenciales. **La corrección
necesita un tercer render de validación** antes de aprobarse visualmente.
Informe: `docs/musnim/VIDEO_REVIEW_2026-10-26.md`.

## Tercer corte auditado: aprobación técnica (26-10-2026)

El tercer MP4 de 79,164 s (720p, 30 fps, H.264/AAC) se inspeccionó
fotograma a fotograma en los cruces de fórmula. Se resolvió el defecto
de doble exposición de expresiones mediante `CueClock.exchange`.
La pista de audio es idéntica al PCM de los dos cortes anteriores.
Quedan abiertas la inspección de logs SVG y la animación individual
según IDs de LilyPond. Ver `docs/musnim/VIDEO_REVIEW_2026-10-26.md`.
