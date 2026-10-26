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
    assert r'\version "2.26.0"' in score


def test_score_provenance_disclaims_exact_rhythm():
    note = (PROJECT / "README.md").read_text(encoding="utf-8").lower()
    assert "reducción" in note and "compases 1–21" in note



def test_musical_event_order_is_a_separate_contract_from_svg():
    data = json.loads(
        (PROJECT / "score" / "naturmotiv_events.json").read_text(encoding="utf-8")
    )
    events = data["events"]
    assert data["schema"] == "musnim.note-events.v0.1"
    assert [(event["id"], event["pitch"]) for event in events] == [
        ("c-1", "C4"), ("g-1", "G4"), ("c-2", "C5"),
    ]
    assert [event["onset_beats"] for event in events] == [0, 1, 2]
    assert [event["duration_beats"] for event in events] == [1, 1, 2]
    source = (PROJECT / "score" / "naturmotiv_reduccion.ly").read_text(
        encoding="utf-8"
    )
    ids_in_lilypond = re.findall(
        r'data-musnim-id\s*\.\s*"([^"]+)"', source
    )
    assert ids_in_lilypond == [event["id"] for event in events]



def test_scene_sources_parse_and_keep_score_separate():
    import ast

    scene_file = PROJECT / "scenes" / "zarathustra_pitagorico.py"
    scene_text = scene_file.read_text(encoding="utf-8")
    ast.parse(scene_text, filename=str(scene_file))

    # The staff must disappear before analytical formulas occupy the frame.
    assert "FadeOut(score)" in scene_text
    assert "math_card(" in scene_text
    assert "score.scale_to_fit_width(8.4)" in scene_text
    # Abrupt changes between unrelated MathTex formula structures are avoided.
    assert "Transform(current" not in scene_text


def test_lilypond_score_delegates_editorial_text_to_manim():
    score = (PROJECT / "score" / "naturmotiv_reduccion.ly").read_text(
        encoding="utf-8"
    )
    assert r"\version " + '"2.26.0"' in score
    assert "title = ##f" in score
    assert "subtitle = ##f" in score
    assert "composer = ##f" in score
    assert 'instrumentName = "' not in score



def test_formula_exchanges_are_sequential_in_scene():
    """Regression for 720p ghosting at 27–28, 32–33 and 65–72 seconds."""
    import ast

    scene_file = PROJECT / "scenes" / "zarathustra_pitagorico.py"
    scene_text = scene_file.read_text(encoding="utf-8")
    parsed = ast.parse(scene_text, filename=str(scene_file))
    clock_class = next(
        node for node in parsed.body
        if isinstance(node, ast.ClassDef) and node.name == "CueClock"
    )
    exchange = next(
        node for node in clock_class.body
        if isinstance(node, ast.FunctionDef) and node.name == "exchange"
    )
    assert exchange is not None
    assert "duration * 0.4" in scene_text
    assert "duration * 0.6" in scene_text
    assert scene_text.count("clock.exchange(") == 9
    assert "FadeOut(current), FadeIn(" not in scene_text
