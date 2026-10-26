# Arquitectura Musnim v0.1

                Manim Community (fork actualizable)
                           |
                 extensions/musnim
                  /       |       \
              ratios   engraving   audio
                  \       |       /
                    projects/ZAR-001
                         |
                  LilyPond + MathTex
                         |
                    render Manim

## Contratos técnicos

1. Las razones acústicas son Fraction exactas.
2. Las partituras usan LilyPond y producen SVG vectorial.
3. Cada nota animable deberá conservar un ID semántico estable:
   data-musnim-id. El orden de los elementos en el árbol SVG describe el
   grabado y puede diferir del orden musical. El contrato temporal inicial
   está en projects/ZAR-001/score/naturmotiv_events.json (IDs, alturas,
   inicios y duraciones). validate_note_coverage verifica igualdad exacta
   de IDs y preserva el orden musical. La selección geométrica por ID
   se implementará y comprobará en el siguiente hito; el prototipo
   todavía importa el SVG entero.
4. cues.json define tiempos del prototipo, independientes de los
   tiempos de interpretación de una grabación específica.
5. Las grabaciones externas requieren autorización o régimen
   de uso comprobado antes de incorporarlas al código.
6. Windows, macOS y Linux son plataformas objetivo. La CI de M0
   prueba lógica Python, con integración gráfica prevista en M1.

## Decisiones

Se reserva el núcleo de Manim original para facilitar la sincronización
desde upstream. El código propio se concentra en extensions/musnim,
projects/ZAR-001 y docs/musnim.

La afinación pitagórica 3-límite y la entonación justa 5-límite
son modelos que el video compara con precisión, sin atribuir
sus proporciones exactas a una ejecución orquestal.

## Trabajo pendiente

- Fijar LilyPond estable 2.26.0 como referencia y probar su salida SVG efectiva.
- Animar noteheads seleccionados por identificadores semánticos.
- Cotejar compases 1–21 de la partitura de Joseph Aibl.
- Construir eventos musicales tipados y relaciones partitura/tiempo.
- Primer MP4 de prueba producido en Windows (480p15; 30 animaciones).
- Auditar visualmente los nodos SVG `<text>` omitidos por Manim 0.22.0.
- Probar el render en macOS y Linux.
