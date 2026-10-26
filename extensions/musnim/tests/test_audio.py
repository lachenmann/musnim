import wave

from musnim.audio import synthesize_demonstration


def test_original_sound_can_be_written(tmp_path):
    path = synthesize_demonstration(tmp_path / "demo.wav", duration=2, rate=8000)
    with wave.open(str(path), "rb") as sound:
        assert sound.getnchannels() == 1
        assert sound.getsampwidth() == 2
        assert sound.getframerate() == 8000
        assert sound.getnframes() == 16000
