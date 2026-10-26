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
   data-musnim-id. La selección geométrica por ID se implementará
   y comprobará en el siguiente hito; el prototipo importa el SVG entero.
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

- Probar LilyPond 2.26 con su salida SVG efectiva.
- Animar noteheads seleccionados por identificadores semánticos.
- Cotejar compases 1–21 de la partitura de Joseph Aibl.
- Construir eventos musicales tipados y relaciones partitura/tiempo.
- Renderizar video de prueba en los tres sistemas.
