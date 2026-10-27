"""Diagnose the real LilyPond SVG identities and Manim notehead geometry."""
from pathlib import Path

from musnim import LilyPondRenderer
from musnim.semantic_notes import matched_svg_notes
from musnim.semantic_mobject import SemanticScore

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "projects" / "ZAR-001" / "score"


def main() -> None:
    svg = LilyPondRenderer().render_svg(
        SCORE / "naturmotiv_reduccion.ly",
        ROOT / "projects" / "ZAR-001" / "_build" / "lilypond",
    )
    linked = matched_svg_notes(svg, SCORE / "naturmotiv_events.json")
    score = SemanticScore(svg)
    score.scale_to_fit_width(8.4)
    print("SVG de LilyPond:", svg)
    print("Orden musical:", [event.id for event, _ in linked])
    for event, ref in linked:
        note = score.note(event.id)
        x, y, _ = note.get_center()
        print(
            f"{event.id} {event.pitch}: SVG id={ref.svg_id}, "
            f"tag={ref.tag}, onset={event.onset_beats:g}, "
            f"duration={event.duration_beats:g}, "
            f"center=({x:.3f},{y:.3f}), "
            f"width={note.width:.3f}, height={note.height:.3f}"
        )
        if note.width <= 0 or note.height <= 0:
            raise SystemExit(f"Geometría vacía para {event.id}")
        if note.width >= score.width * 0.5:
            raise SystemExit(
                f"La geometría seleccionada es demasiado grande "
                f"para una nota individual: {event.id}"
            )
    print("OK: tres cabezas de nota accesibles por identidad musical.")


if __name__ == "__main__":
    main()
