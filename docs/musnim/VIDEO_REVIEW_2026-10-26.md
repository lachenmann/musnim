# ZAR-001 — Primera auditoría del MP4 real (2026-10-26)

Estado: primer render **terminado**, 30 animaciones; calidad editorial **en revisión**.

Archivo observado: video subido por el usuario, originalmente
`D:\Proyectos\musnim\media\videos\zarathustra_pitagorico\480p15\ZarathustraPitagorico.mp4`.
El video no se agrega al repositorio Git.

## Inspección técnica (FFprobe + decodificación local)

- Contenedor MP4: **79,040 segundos**, 1 871 384 bytes.
- Video: H.264, 854×480, ~15 fps (relación 16:9).
- Audio: AAC, estéreo, 48 kHz. El volumen registrado confirma señal audible
  durante los ejemplos; presenta silencios en las transiciones, entre otros
  19–21, 29–32, 41–45, 53–59 y 76–79 segundos.
- Los principales picos espectrales verifican la síntesis: Do grave
  ~130,8 Hz al comienzo; Do ~261,6 Hz, Sol ~392 Hz, Do agudo ~523,3 Hz;
  tríada mayor con Mi ~327 Hz y menor con Mi bemol ~314 Hz.
- Las razones acústicas del video corresponden a modelos didácticos
  ideales, sin atribuir afinación pura exacta a una interpretación orquestal.

## Defectos visuales comprobados por fotograma

1. **Mayor (P1):** 12–20 s, el texto "Do · Sol · Do" intersecta la
   leyenda "Reducción didáctica de alturas — ritmo esquemático".
2. **Mayor (P1):** ~21–27 s, la fórmula `f_C:f_G:f_C'=2:3:4`
   se superpone al pentagrama y al subtítulo; las barras aparecen demasiado
   próximas al crédito inferior.
3. **Mayor (P1):** líneas del pentagrama con contraste insuficiente sobre
   fondo azul oscuro; clef y figuras son muy grandes respecto del cuadro.
4. **Moderado (P2):** ~39–55 s, fórmulas superpuestas a figuras o muy próximas
   a notas; la transición entre fórmulas genera instantes visualmente
   confusos. Reemplazar morphs de grupos heterogéneos por fundidos.
5. **Moderado (P2):** LilyPond emite SVG `<text>` que
   `SVGMobject` de Manim 0.22.0 omite ("Unsupported element type").
   Generar un SVG de pentagrama sin textos editoriales; incorporar
   títulos, créditos y anotaciones con Manim Text por separado.
6. **Menor (P3):** primeros ensayos a 480p15 limitan la legibilidad; después
   de corregir la composición, pasar a 720p30 y finalmente 1080p.

## Refactor propuesto en PR #1

- Espacios independientes: título superior; partitura central en su segmento;
  etiquetas y advertencia en franjas inferiores; luego escena matemática
  con pentagrama ausente para evitar solapes.
- Mantener LilyPond como autoridad del grabado y los IDs semánticos
  `data-musnim-id`; los metadatos de eventos establecen el orden musical.
- Usar `FadeOut` y `FadeIn` entre expresiones de estructura distinta.
- El siguiente MP4 se debe volver a inspeccionar: las correcciones
  aquí incluidas son propuestas implementadas en código, todavía pendientes
  de validación mediante render en el PC del usuario.

## Siguiente criterio de aceptación

Render renovado en Windows, QA de FFprobe, revisión de los segundos 8–27,
39–55 y 75–79, y confirmación de que desaparecieron los avisos por texto SVG.
