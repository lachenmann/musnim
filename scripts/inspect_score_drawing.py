"""Validate LilyPond 2.26 SVG grob roles and Manim geometry before rendering."""
from pathlib import Path
from collections import Counter
from xml.etree import ElementTree as ET

from musnim import LilyPondRenderer
from musnim.score_layers import read_score_layers
from musnim.score_drawing_mobject import DrawingScore
from musnim.semantic_notes import matched_svg_notes

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "projects" / "ZAR-001" / "score"
OUTPUT = ROOT / "projects" / "ZAR-001" / "_build" / "lilypond"


def main():
    svg = LilyPondRenderer().render_svg(SCORE / "naturmotiv_drawing.ly", OUTPUT)
    layers = read_score_layers(svg)
    print("SVG:", svg)
    print("Etiquetas musicales LilyPond:")
    for part in layers:
        print(f"  rol={part.role}, svg-id={part.svg_id}, owner={part.owner}")

    required = [
        ("staff", None),
        ("clef", None),
        ("meter", None),
        ("stem", "c-1"),
        ("stem", "g-1"),
        ("stem", "c-2"),
        ("barline", None),
    ]
    available = Counter((part.role, part.owner) for part in layers)
    missing = [
        (role, owner) for role, owner in required
        if available[(role, owner)] != 1
    ]
    if missing:
        root = ET.parse(svg).getroot()
        groups = [
            node for node in root.iter()
            if node.tag.rsplit("}", 1)[-1] == "g"
        ]
        print("DIAGNÓSTICO SVG (etiquetas de grupos):")
        print("  elementos SVG:", Counter(
            node.tag.rsplit("}", 1)[-1] for node in root.iter()
        ).most_common(8))
        print("  primeros IDs de grupos:", [
            node.attrib.get("id") for node in groups
            if node.attrib.get("id")
        ][:25])
        print("  roles encontrados:", dict(available))
        print("  roles ausentes/ambiguos:", missing)
        raise SystemExit(
            "Faltan etiquetas estructurales de LilyPond. "
            "Copia la salida del diagnóstico y conserva el SVG indicado."
        )

    score = DrawingScore(svg)
    score.scale_to_fit_width(8.4)
    for role, owner in required:
        graphic = score.layer(role, owner=owner)
        x, y, _ = graphic.get_center()
        print(
            f"  {role}/{owner}: center=({x:.3f},{y:.3f}) "
            f"size={graphic.width:.3f}x{graphic.height:.3f}"
        )
        if graphic.width <= 0 or graphic.height <= 0:
            raise SystemExit(f"Geometría vacía: {role}/{owner}")

    for event, _ in matched_svg_notes(svg, SCORE / "naturmotiv_events.json"):
        head = score.note(event.id)
        print(
            f"  notehead/{event.id}: "
            f"size={head.width:.3f}x{head.height:.3f}"
        )
        if head.width <= 0 or head.height <= 0:
            raise SystemExit(f"Cabeza de nota vacía: {event.id}")
    print(
        "OK: pentagrama, clave, compás, plicas, cabezas "
        "y barra final animables por separado."
    )


if __name__ == "__main__":
    main()
