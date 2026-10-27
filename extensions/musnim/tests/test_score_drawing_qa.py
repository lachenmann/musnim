"""Validate expected metadata for the score-writing video independently."""
import ast
from pathlib import Path

import pytest

from musnim.video_qa import VideoQAError, assess_media

ROOT = Path(__file__).resolve().parents[3]


def test_score_drawing_clip_duration():
    probe = {
        "format": {"duration": "20.03333"},
        "streams": [
            {
                "codec_type": "video", "codec_name": "h264",
                "width": 854, "height": 480,
                "avg_frame_rate": "15/1",
            },
            {"codec_type": "audio", "codec_name": "aac"},
        ],
    }
    result = assess_media(
        probe, expected_duration=20, tolerance=1.0,
    )
    assert result["duration_seconds"] == 20.033
    probe["format"]["duration"] = "79.04"
    with pytest.raises(VideoQAError, match="Duración"):
        assess_media(probe, expected_duration=20, tolerance=1.0)


def test_diagnostic_and_qa_scripts_are_valid_python():
    for name in ("inspect_score_drawing.py", "qa_score_drawing_video.py"):
        path = ROOT / "scripts" / name
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
