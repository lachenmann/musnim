import subprocess
import pytest

from musnim.engraving import LilyPondRenderer, LilyPondError, semantic_note_ids, validate_note_coverage


def test_extract_semantic_note_identifiers(tmp_path):
    svg = tmp_path / "score.svg"
    svg.write_text("""<svg xmlns="http://www.w3.org/2000/svg">
       <g data-musnim-id="c-1"><path d="M0 0"/></g>
       <g data-musnim-id="g-1"><path d="M0 1"/></g>
    </svg>""", encoding="utf-8")
    assert semantic_note_ids(svg) == ("c-1", "g-1")


def test_duplicated_semantic_note_id_rejected(tmp_path):
    svg = tmp_path / "score.svg"
    svg.write_text('<svg><g data-musnim-id="x"/><g data-musnim-id="x"/></svg>')
    with pytest.raises(LilyPondError, match="repetidos"):
        semantic_note_ids(svg)


def test_render_reports_failed_executable(tmp_path, monkeypatch):
    score = tmp_path / "a.ly"
    score.write_text('\\version "2.26.0"\n\\score { c4 }', encoding="utf-8")
    monkeypatch.setattr(
        "musnim.engraving.subprocess.run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args, 3, stdout="", stderr="bad input"
        ),
    )
    with pytest.raises(LilyPondError, match="devolvió 3"):
        LilyPondRenderer(executable="fake-lilypond").render_svg(
            score, tmp_path / "out"
        )


def test_invalid_file_rejected(tmp_path):
    with pytest.raises(LilyPondError, match="Fuente LilyPond inválida"):
        LilyPondRenderer().render_svg(tmp_path / "missing.ly", tmp_path)



def test_lilypond_svg_dom_order_is_independent_of_musical_time(tmp_path):
    """Regression: real 2.26 SVG yielded g-1, c-2, c-1 on Windows."""
    svg = tmp_path / "reordered.svg"
    svg.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<g data-musnim-id="g-1"/>'
        '<g data-musnim-id="c-2"/>'
        '<g data-musnim-id="c-1"/>'
        '</svg>',
        encoding="utf-8",
    )
    observed_dom_order = semantic_note_ids(svg)
    assert observed_dom_order == ("g-1", "c-2", "c-1")
    assert validate_note_coverage(
        ("c-1", "g-1", "c-2"), observed_dom_order
    ) == ("c-1", "g-1", "c-2")


def test_coverage_rejects_missing_or_unexpected_ids():
    with pytest.raises(LilyPondError, match="IDs ausentes"):
        validate_note_coverage(("c-1", "g-1", "c-2"), ("c-1", "g-1"))
    with pytest.raises(LilyPondError, match="IDs inesperados"):
        validate_note_coverage(("c-1",), ("c-1", "x"))


def test_coverage_rejects_duplicated_score_ids():
    with pytest.raises(LilyPondError, match="repetidos"):
        validate_note_coverage(("c-1", "c-1"), ("c-1",))
