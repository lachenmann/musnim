# Musnim extension (pre-alpha)

Musnim adds exact acoustic ratios, original demonstrational audio, and LilyPond
SVG score engraving to the Manim Community fork.

Install into the fork's Python environment:

    python -m pip install --no-deps -e extensions/musnim

Run Python-only checks:

    python -m pytest -c extensions/musnim/pyproject.toml extensions/musnim/tests -q

LilyPond is needed for SVG engraving and Manim + LaTeX for video rendering.
See ../../README_MUSNIM.md and ../../docs/musnim/ARCHITECTURE.md.
