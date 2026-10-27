"""Lightweight source-level checks for the distinct sustain experiment."""
import ast
from pathlib import Path

from musnim.note_event_audio import make_note_schedule
from musnim.semantic_notes import read_note_events


PROJECT = Path(__file__).resolve().parents[3] / "projects" / "ZAR-001"


def test_sustain_scene_parses_and_uses_one_audio_visual_schedule():
    path = PROJECT / "scenes" / "semantic_notes_sustain_demo.py"
    source = path.read_text(encoding="utf-8")
    ast.parse(source, filename=str(path))
    assert "make_note_schedule(" in source
    assert "synthesize_scheduled_notes(" in source
    assert "notehead.animate.set_color(GOLD_C)" in source
    assert "wait_until(event.end_seconds - RELEASE_FADE_SECONDS)" in source
    assert 'wait_until(17.0)' in source


def test_manifest_horizon_is_twenty_seconds():
    notes = read_note_events(PROJECT / "score" / "naturmotiv_events.json")
    schedule = make_note_schedule(notes)
    assert schedule[-1].end_seconds == 20.0
    assert all(
        schedule[i].start_seconds >= schedule[i - 1].end_seconds
        for i in range(1, len(schedule))
    )
