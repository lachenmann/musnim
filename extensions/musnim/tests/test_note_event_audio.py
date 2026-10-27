"""A single timeline must govern both note highlighting and note sound."""
from pathlib import Path
import wave

import pytest

from musnim.engraving import LilyPondError
from musnim.note_event_audio import make_note_schedule, synthesize_scheduled_notes
from musnim.semantic_notes import NoteEvent


def score_events():
    return (
        NoteEvent(id="c-1", pitch="C4", onset_beats=0, duration_beats=1),
        NoteEvent(id="g-1", pitch="G4", onset_beats=1, duration_beats=1),
        NoteEvent(id="c-2", pitch="C5", onset_beats=2, duration_beats=2),
    )


def test_one_timeline_defines_attack_and_release():
    notes = make_note_schedule(score_events())
    assert [(e.start_seconds, e.end_seconds) for e in notes] == [
        (8.0, 11.0), (11.0, 14.0), (14.0, 20.0),
    ]
    assert [note.event.id for note in notes] == ["c-1", "g-1", "c-2"]
    assert [n.frequency_hz for n in notes] == pytest.approx(
        [261.6255653, 392.438348, 523.2511306], abs=0.01
    )


def test_wav_duration_follows_score_event_timing(tmp_path):
    path = synthesize_scheduled_notes(
        tmp_path / "scheduled.wav",
        make_note_schedule(score_events()),
        sample_rate=8000,
    )
    with wave.open(str(path), "rb") as stream:
        assert stream.getnchannels() == 1
        assert stream.getsampwidth() == 2
        assert stream.getframerate() == 8000
        assert stream.getnframes() == 20 * 8000


def test_rejects_pitch_outside_initial_trio():
    events = (NoteEvent("n", "F4", 0, 1),)
    with pytest.raises(LilyPondError, match="fuera del piloto"):
        make_note_schedule(events)


def test_rejects_musical_overlap_in_monophonic_pilot():
    events = (
        NoteEvent("a", "C4", 0, 2),
        NoteEvent("b", "G4", 1, 1),
    )
    with pytest.raises(LilyPondError, match="monofónico"):
        make_note_schedule(events)


def test_rejects_negative_or_zero_timing_parameters():
    with pytest.raises(LilyPondError, match="temporales"):
        make_note_schedule(score_events(), seconds_per_beat=0)
    with pytest.raises(LilyPondError, match="temporales"):
        make_note_schedule(score_events(), lead_in_seconds=-3)
