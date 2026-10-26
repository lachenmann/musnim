# Checklist M0

- [x] Fork lachenmann/musnim creado desde Manim Community.
- [x] Rama feature/ZAR-001-bootstrap creada.
- [x] Código matemático, audio y grabado LilyPond incorporados.
- [x] ZAR-001 con reducción, cue sheet, guion y fuentes.
- [x] CI Python de Musnim en verde en Windows, macOS y Linux (26-10-2026).
- [x] LilyPond 2.26 instalado en D: y salida SVG con tres IDs confirmada por el usuario.
- [x] Verificación de cobertura de IDs independiente del orden DOM (LilyPond real 2.26.0 en Windows, 26-10-2026).
- [x] Manim + LaTeX + FFmpeg probados localmente: 30 animaciones, MP4 480p15 (26-10-2026).
- [x] Validar técnicamente el MP4 HD con `qa_zar001_video.py`: 79,04 s, 1280×720, 30 fps, H.264/AAC (26-10-2026).
- [x] Inspección visual de primer y segundo MP4: pentagrama y fórmulas legibles en segundo corte.
- [ ] Comprobar en el log de render ausencia de advertencias SVG de texto no soportado.
- [ ] Revisión de PR y merge hacia main.
- [ ] Notas Obsidian organizadas fuera del repo público.

## ZAR-001 — revisión del primer video

- [x] Inspección visual del MP4 real y análisis de audio (26-10-2026).
- [x] Hallazgos P1/P2 y primera refactorización de escena registrados.
- [x] Segundo render 720p30 comparado con el primero: solapes persistentes corregidos.
- [x] Tercer render generado y QA técnico aprobado en Windows: 42 animaciones, 79,164 s, 1280×720, ~30 fps, H.264/AAC (26-10-2026).
- [ ] Inspeccionar visualmente los fundidos secuenciales del tercer MP4 (27,5; 32,5; 65,5; 71,5 s).
- [ ] Comprobar ausencia de advertencias de texto SVG y audio íntegro.
- [x] Generar segundo corte de revisión a 720p30 (26-10-2026).
- [ ] Aprobar visual y musicalmente el segundo corte antes de solicitar 1080p.
