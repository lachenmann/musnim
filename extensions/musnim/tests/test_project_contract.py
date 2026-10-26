"""First laboratory checks that do not require the renderer."""
import json
from pathlib import Path
import re

from musnim.audio import SOUND_EVENTS

REPO = Path(__file__).resolve().parents[3]
PROJECT = REPO / "projects" / "ZAR-001"


def test_cues_monotonic_and_end_at_79_seconds():
    data = json.loads((PROJECT / "cues.json").read_text(encoding="utf-8"))
    times = [cue["time"] for cue in data["cues"]]
    assert times == sorted(times)
    assert len(times) == len(set(times))
    assert times[0] == 0
    assert times[-1] == 79


def test_synthetic_events_inside_prototype_duration():
    for start, duration, volume, ratios in SOUND_EVENTS:
        assert 0 <= start and 0 < duration and start + duration <= 79
        assert volume > 0
        assert all(ratio > 0 for ratio in ratios)


def test_lilypond_source_has_three_semantic_note_tags():
    score = (PROJECT / "score" / "naturmotiv_reduccion.ly").read_text(
        encoding="utf-8")
    identifiers = re.findall(r'data-musnim-id\s*\.\s*"([^"]+)"', score)
    assert identifiers == ["c-1", "g-1", "c-2"]
    assert r'\version "2.24.4"' in score


def test_score_provenance_disclaims_exact_rhythm():
    note = (PROJECT / "README.md").read_text(encoding="utf-8").lower()
    assert "reducción" in note and "compases 1–21" in note
