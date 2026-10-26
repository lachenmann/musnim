import pytest

from musnim.video_qa import VideoQAError, assess_media


@pytest.fixture
def good_probe():
    return {
        "format": {"duration": "79.000000"},
        "streams": [
            {
                "codec_type": "video",
                "codec_name": "h264",
                "width": 854,
                "height": 480,
                "avg_frame_rate": "15/1",
            },
            {"codec_type": "audio", "codec_name": "aac"},
        ],
    }


def test_accepts_79_second_av_render(good_probe):
    results = assess_media(good_probe)
    assert results["duration_seconds"] == 79
    assert results["width"] == 854
    assert results["height"] == 480
    assert results["audio_codec"] == "aac"


def test_rejects_missing_audio(good_probe):
    good_probe["streams"] = good_probe["streams"][:1]
    with pytest.raises(VideoQAError, match="requieren duración, video y audio"):
        assess_media(good_probe)


def test_rejects_incorrect_duration(good_probe):
    good_probe["format"]["duration"] = "50.0"
    with pytest.raises(VideoQAError, match="Duración"):
        assess_media(good_probe)


def test_rejects_invalid_frame_rate(good_probe):
    good_probe["streams"][0]["avg_frame_rate"] = "0/0"
    with pytest.raises(VideoQAError, match="requieren duración, video y audio"):
        assess_media(good_probe)


def test_rejects_insufficient_resolution(good_probe):
    good_probe["streams"][0]["width"] = 320
    with pytest.raises(VideoQAError, match="Resolución insuficiente"):
        assess_media(good_probe)


def test_semantic_demo_duration_validation(good_probe):
    good_probe["format"]["duration"] = "19.066667"
    accepted = assess_media(
        good_probe, expected_duration=19.0, tolerance=1.0,
    )
    assert accepted["duration_seconds"] == 19.067


def test_semantic_demo_rejects_main_movie_duration(good_probe):
    with pytest.raises(VideoQAError, match="Duración"):
        assess_media(good_probe, expected_duration=19.0, tolerance=1.0)
