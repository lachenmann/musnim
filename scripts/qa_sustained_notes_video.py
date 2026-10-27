"""Check technical characteristics of the 20-second sustained-note demo."""
from pathlib import Path

from musnim.video_qa import VideoQAError, inspect_with_ffprobe, assess_media

ROOT = Path(__file__).resolve().parents[1]
FILE = (
    ROOT / "media" / "videos" / "semantic_notes_sustain_demo"
    / "480p15" / "SemanticNotesSustainDemo.mp4"
)


def main():
    try:
        result = assess_media(
            inspect_with_ffprobe(FILE), expected_duration=20.0, tolerance=1.0
        )
    except VideoQAError as error:
        raise SystemExit(f"M3 SUSTAIN QA ERROR: {error}") from error
    print("Archivo:", FILE)
    print("Duración:", result["duration_seconds"], "s")
    print("Resolución:", result["width"], "x", result["height"])
    print("Frecuencia:", result["fps"], "fps")
    print("Video:", result["video_codec"], "Audio:", result["audio_codec"])
    print("OK: MP4 de 20 segundos con pistas de video y audio.")
    print("Pendiente: observar color de cada cabeza durante todo su sonido.")


if __name__ == "__main__":
    main()
