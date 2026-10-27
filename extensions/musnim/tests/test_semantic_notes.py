"""Unit checks for stable SVG identities and score time ordering."""
import json

import pytest

from musnim.engraving import LilyPondError
from musnim.semantic_notes import (
    matched_svg_notes, read_note_events, read_svg_note_refs,
)


def fixture_svg(tmp_path, text):
    p = tmp_path / "notes.svg"
    p.write_text(text, encoding="utf-8")
    return p


def fixture_events(tmp_path, notes):
    p = tmp_path / "events.json"
    p.write_text(json.dumps({"events": notes}), encoding="utf-8")
    return p


def events():
    return [
        {"id": "c-1", "pitch": "C4", "onset_beats": 0, "duration_beats": 1},
        {"id": "g-1", "pitch": "G4", "onset_beats": 1, "duration_beats": 1},
        {"id": "c-2", "pitch": "C5", "onset_beats": 2, "duration_beats": 2},
    ]


@pytest.mark.parametrize("reverse_dom", [False, True])
def test_svg_ids_independent_of_dom_order(tmp_path, reverse_dom):
    order = ["g-1", "c-2", "c-1"]
    if reverse_dom:
        order.reverse()
    ids = {"c-1": "head-c4", "g-1": "head-g4", "c-2": "head-c5"}
    xml = "<svg>" + "".join(
        f'<g data-musnim-id="{i}" id="{ids[i]}">'
        '<path d="M0 0L2 0Z"/></g>' for i in order
    ) + "</svg>"
    svg = fixture_svg(tmp_path, xml)
    manifest = fixture_events(tmp_path, events())
    refs = read_svg_note_refs(svg)
    assert set(refs) == {"c-1", "g-1", "c-2"}
    linked = matched_svg_notes(svg, manifest)
    assert [x.id for x, _ in linked] == ["c-1", "g-1", "c-2"]
    assert [x.svg_id for _, x in linked] == [
        "head-c4", "head-g4", "head-c5"
    ]


def test_ids_on_inline_svg_paths(tmp_path):
    svg = fixture_svg(
        tmp_path,
        '<svg><path id="head-c4" data-musnim-id="c-1"'
        ' d="M0 0L1 0L1 1Z"/></svg>',
    )
    assert read_svg_note_refs(svg)["c-1"].tag == "path"


def test_duplicate_ids_are_invalid(tmp_path):
    svg = fixture_svg(
        tmp_path,
        '<svg><g id="a" data-musnim-id="c-1"/>'
        '<g id="b" data-musnim-id="c-1"/></svg>',
    )
    with pytest.raises(LilyPondError, match="repetido"):
        read_svg_note_refs(svg)


def test_note_svg_id_required(tmp_path):
    svg = fixture_svg(tmp_path, '<svg><g data-musnim-id="c-1"/></svg>')
    with pytest.raises(LilyPondError, match="carece"):
        read_svg_note_refs(svg)


def test_manifest_with_missing_svg_note(tmp_path):
    svg = fixture_svg(
        tmp_path, '<svg><g id="c4" data-musnim-id="c-1"/></svg>'
    )
    with pytest.raises(LilyPondError, match="IDs ausentes"):
        matched_svg_notes(svg, fixture_events(tmp_path, events()))


def test_manifest_duplicate_event_ids(tmp_path):
    e = events()
    e[1]["id"] = "c-1"
    with pytest.raises(LilyPondError, match="inválidos"):
        read_note_events(fixture_events(tmp_path, e))


def test_negative_or_nonfinite_time_rejected(tmp_path):
    e = events()
    e[0]["duration_beats"] = -1
    with pytest.raises(LilyPondError, match="Tiempo inválido"):
        read_note_events(fixture_events(tmp_path, e))


def test_out_of_order_events_rejected(tmp_path):
    e = events()
    e[0]["onset_beats"] = 2
    e[1]["onset_beats"] = 1
    with pytest.raises(LilyPondError, match="ordenarse"):
        read_note_events(fixture_events(tmp_path, e))



def test_experimental_scene_parses_without_rendering():
    """CI validates scene syntax without depending on Manim/FFmpeg binaries."""
    import ast
    from pathlib import Path

    root = Path(__file__).resolve().parents[3]
    scene = root / "projects" / "ZAR-001" / "scenes" / "semantic_notes_demo.py"
    diagnostic = root / "scripts" / "inspect_semantic_notes.py"
    ast.parse(scene.read_text(encoding="utf-8"), filename=str(scene))
    ast.parse(diagnostic.read_text(encoding="utf-8"), filename=str(diagnostic))
    assert "class SemanticNotesDemo" in scene.read_text(encoding="utf-8")
