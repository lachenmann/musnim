"""Actual LilyPond 2.26 → SVG integration check for ZAR-001.

Musical chronology is supplied by naturmotiv_events.json. LilyPond's SVG DOM
order describes graphics and can differ from the chronological note order.
"""
import json
from pathlib import Path

from musnim import (
    LilyPondError, LilyPondRenderer, semantic_note_ids, validate_note_coverage,
)

ROOT = Path(__file__).resolve().parents[1]
SCORE_DIR = ROOT / "projects" / "ZAR-001" / "score"
SCORE = SCORE_DIR / "naturmotiv_reduccion.ly"
EVENTS = SCORE_DIR / "naturmotiv_events.json"
OUTPUT = ROOT / "projects" / "ZAR-001" / "_build" / "lilypond"


def main() -> None:
    score_events = json.loads(EVENTS.read_text(encoding="utf-8"))["events"]
    expected = tuple(event["id"] for event in score_events)
    svg = LilyPondRenderer().render_svg(SCORE, OUTPUT)
    observed = semantic_note_ids(svg)

    print(f"SVG generado: {svg}")
    print(f"Orden gráfico SVG: {observed}")
    print(f"Orden musical de la reducción: {expected}")
    try:
        validate_note_coverage(expected, observed)
    except LilyPondError as error:
        raise SystemExit(f"ERROR: {error}") from error

    print("OK: LilyPond 2.26 → SVG con todas las notas identificadas.")
    print("La cronología musical proviene del manifiesto de eventos, no del DOM SVG.")


if __name__ == "__main__":
    main()
