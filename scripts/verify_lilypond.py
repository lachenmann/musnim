"""Real LilyPond 2.24+ -> SVG -> note identifiers smoke test for ZAR-001.

Requires MUSNIM_LILYPOND to reference lilypond.exe, or lilypond in PATH.
Unlike the unit tests, this checks the actual external engraving engine.
"""
from pathlib import Path

from musnim import LilyPondRenderer, semantic_note_ids

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "projects" / "ZAR-001" / "score" / "naturmotiv_reduccion.ly"
OUTPUT = ROOT / "projects" / "ZAR-001" / "_build" / "lilypond"


def main() -> None:
    svg = LilyPondRenderer().render_svg(SCORE, OUTPUT)
    actual = semantic_note_ids(svg)
    expected = ("c-1", "g-1", "c-2")
    print(f"SVG generado: {svg}")
    print(f"Identificadores SVG encontrados: {actual}")
    if actual != expected:
        raise SystemExit(
            f"ERROR: identificadores de nota inesperados. "
            f"Esperados: {expected}; obtenidos: {actual}"
        )
    print("OK: LilyPond -> SVG con IDs semánticos Do-Sol-Do.")


if __name__ == "__main__":
    main()
