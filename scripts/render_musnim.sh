#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m manim -ql projects/ZAR-001/scenes/zarathustra_pitagorico.py ZarathustraPitagorico
