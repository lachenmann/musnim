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

## Seguimiento del segundo render (26-10-2026)

QA automatizada del MP4 de segunda iteración: **79,04 s, 1280×720, 30 fps,
H.264/AAC**, resultado OK en el PC del usuario. El archivo generado
se encuentra en `media/videos/zarathustra_pitagorico/720p30/`.

**Pendiente:** comparar fotogramas 12, 22 y 42 segundos con el primer
corte, escuchar la pista y comprobar si desaparecieron los solapes y
las advertencias de texto SVG. La superación del QA técnico no cierra
los hallazgos visuales P1/P2.

## Auditoría comparada del segundo MP4 HD (26-10-2026)

Se comparó directamente el segundo video (79,04 s, 1280×720, 30 fps,
H.264/AAC) con el primer corte en los segundos 7,5; 10; 12; 14; 16;
19,5; 20,5; 22; 25; 26,5; 27,5; 32,5; 35; 39; 42; 45; 49; 52;
55; 59; 61; 65,5; 68; 71,5; 74; 76 y 78.

- [x] Las etiquetas Do–Sol–Do y la leyenda están separadas (12 s).
- [x] El pentagrama sale antes de iniciar la fórmula 2:3:4 (22 s).
- [x] Las expresiones matemáticas estables son legibles (35, 39, 42, 49 s).
- [x] Líneas de pentagrama, clave y notas muestran mayor contraste.
- [ ] Los fundidos simultáneos entre fórmulas producen doble exposición
  breve cerca de 27,5; 32,5; 65,5 y 71,5 segundos.
- [ ] Los nombres de las notas deben anclarse en el futuro a sus propios
  `data-musnim-id` para animación individual y alineación precisa (M3).
- [ ] Comprobar en los logs reales la ausencia de advertencias
  `Unsupported element type: svgelements.Text`; el MP4 no conserva
  la salida completa de la consola de Manim.

Las pistas sonoras decodificadas de ambos MP4 son idénticas
muestra por muestra: se conserva la secuencia sintética y sus ataques.
Se comprobaron picos aproximados de Do 262 Hz, Sol 392 Hz,
Do agudo 523 Hz, Mi 327 Hz y Mi bemol 314 Hz.

### Tercera iteración de código, pendiente de render

`CueClock.exchange` completa primero la salida de una fórmula y
después la entrada de su sucesora, conservando la duración total
de cada transición. Se aplica a los nueve intercambios de la escena.
La prueba de regresión AST confirma el uso del nuevo patrón.

**Estado:** el cambio de código se ha registrado; los defectos de
doble exposición se considerarán cerrados después de inspeccionar
un tercer MP4 real.

## Tercer render ejecutado — validación visual pendiente (26-10-2026)

El tercer MP4 fue renderizado por Manim en Windows tras el cambio
`CueClock.exchange` del commit `584ad0e7`. La consola informa
**42 animaciones**. La herramienta de QA ejecutada por el usuario
informa **79,164 s, 1280×720, 30,001 fps, H.264 + AAC, OK**.

El incremento de animaciones es coherente con las fases adicionales
de salida y entrada de las expresiones matemáticas, pero la eliminación
real de la doble exposición **todavía debe revisarse fotograma a
fotograma** en 27–28, 32–33, 65–66 y 71–72 s. La salida publicada
del render no contiene información suficiente para aprobar el resultado
visual; el archivo local se mantiene fuera del repositorio Git.
