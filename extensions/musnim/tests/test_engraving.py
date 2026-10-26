import subprocess
import pytest

from musnim.engraving import LilyPondRenderer, LilyPondError, semantic_note_ids


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
