"""Source-level and timing checks for the experimental writing scene."""
import ast
from pathlib import Path

from musnim.note_event_audio import make_note_schedule
from musnim.semantic_notes import read_note_events


ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "projects" / "ZAR-001"


def test_animation_scene_parses_and_uses_engraved_components():
    path = PROJECT / "scenes" / "score_drawing_demo.py"
    script = path.read_text(encoding="utf-8")
    ast.parse(script, filename=str(path))
    required = [
        'Create(score.layer("staff")',
        'DrawBorderThenFill(score.layer("clef"))',
        'DrawBorderThenFill(score.layer("meter"))',
        'Create(score.layer("barline"))',
        'DrawBorderThenFill(head)',
        'Create(stem)',
        'Write(frequency_ratio)',
        'head.animate.set_color(GOLD_C)',
        'head.animate.set_color(WHITE)',
    ]
    for snippet in required:
        assert snippet in script


def test_drawing_scene_uses_music_events_for_audio_and_graphic_onsets():
    p = PROJECT / "scenes" / "score_drawing_demo.py"
    src = p.read_text(encoding="utf-8")
    assert "make_note_schedule(" in src
    assert "synthesize_scheduled_notes(" in src
    assert "until(note.start_seconds)" in src
    assert "until(note.end_seconds - NOTE_RELEASE_SECONDS)" in src
    notes = read_note_events(PROJECT / "score" / "naturmotiv_events.json")
    schedule = make_note_schedule(notes)
    assert [(n.start_seconds, n.end_seconds) for n in schedule] == [
        (8.0, 11.0), (11.0, 14.0), (14.0, 20.0)
    ]


def test_drawing_diagnostic_parses_without_native_graphics():
    path = ROOT / "scripts" / "inspect_score_drawing.py"
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_mathematical_caption_uses_dedicated_lower_band():
    """Prevent the formula/label collision observed in video v1."""
    source = (PROJECT / "scenes" / "score_drawing_demo.py").read_text(
        encoding="utf-8"
    )
    assert "frequency_ratio.move_to(DOWN * 2.48)" in source
    assert "frequency_ratio.move_to(DOWN * 1.68)" not in source
