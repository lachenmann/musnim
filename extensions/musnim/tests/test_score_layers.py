"""Score layer metadata is independent of XML shape-order variations."""
from pathlib import Path

import pytest

from musnim.engraving import LilyPondError
from musnim.score_layers import read_score_layers, require_score_layer


def svg(tmp_path, source):
    path = tmp_path / "score.svg"
    path.write_text(source, encoding="utf-8")
    return path


@pytest.mark.parametrize("reverse", [False, True])
def test_resolves_graphic_roles_and_note_stems_by_owner(tmp_path, reverse):
    elements = [
        '<g id="line-group" data-musnim-role="staff"><path d="M0 0L4 0"/></g>',
        '<g id="clef" data-musnim-role="clef"><path d="M0 0L1 2"/></g>',
        '<g id="stem-g" data-musnim-role="stem" data-musnim-owner="g-1">'
        '<path d="M0 0L1 0"/></g>',
        '<g id="stem-c" data-musnim-role="stem" data-musnim-owner="c-1">'
        '<path d="M0 0L1 0"/></g>',
        '<g id="meter" data-musnim-role="meter"><path d="M1 0L1 2"/></g>',
        '<g id="bar" data-musnim-role="barline"><path d="M2 0L2 2"/></g>',
    ]
    if reverse:
        elements.reverse()
    layers = read_score_layers(svg(tmp_path, "<svg>"+"".join(elements)+"</svg>"))
    assert require_score_layer(layers, "staff").svg_id == "line-group"
    assert require_score_layer(layers, "clef").svg_id == "clef"
    assert require_score_layer(layers, "meter").svg_id == "meter"
    assert require_score_layer(layers, "barline").svg_id == "bar"
    assert require_score_layer(layers, "stem", owner="c-1").svg_id == "stem-c"
    assert require_score_layer(layers, "stem", owner="g-1").svg_id == "stem-g"


def test_missing_required_role_raises_explanation(tmp_path):
    layers = read_score_layers(svg(tmp_path, '<svg/>'))
    with pytest.raises(LilyPondError, match="exactamente un"):
        require_score_layer(layers, "staff")


def test_repeated_graphical_id_rejected(tmp_path):
    document = '<svg><g data-musnim-role="clef" id="same"/>' + (
        '<g data-musnim-role="staff" id="same"/></svg>'
    )
    with pytest.raises(LilyPondError, match="duplicado"):
        read_score_layers(svg(tmp_path, document))


def test_duplicate_role_is_ambiguous(tmp_path):
    document = (
        '<svg><g data-musnim-role="staff" id="a"/>'
        '<g data-musnim-role="staff" id="b"/></svg>'
    )
    with pytest.raises(LilyPondError, match="exactamente un"):
        require_score_layer(read_score_layers(svg(tmp_path, document)), "staff")


def test_missing_id_rejected(tmp_path):
    with pytest.raises(LilyPondError, match="sin id"):
        read_score_layers(svg(tmp_path, '<svg><g data-musnim-role="clef"/></svg>'))


def test_drawing_lilypond_file_has_all_expected_markers():
    import re

    root = Path(__file__).resolve().parents[3]
    score = (
        root / "projects" / "ZAR-001" / "score" / "naturmotiv_drawing.ly"
    ).read_text(encoding="utf-8")
    for grob in ("StaffSymbol", "Clef", "TimeSignature", "Stem", "BarLine"):
        assert f"{grob}.output-attributes" in score

    roles = re.findall(r'\(data-musnim-role \. "([^"]+)"\)', score)
    assert sorted(roles) == sorted(
        ["staff", "clef", "meter", "stem", "stem", "stem", "barline"]
    )
    owners = re.findall(r'\(data-musnim-owner \. "([^"]+)"\)', score)
    assert owners == ["c-1", "g-1", "c-2"]
    ids = re.findall(r'\(data-musnim-id \. "([^"]+)"\)', score)
    assert ids == ["c-1", "g-1", "c-2"]
