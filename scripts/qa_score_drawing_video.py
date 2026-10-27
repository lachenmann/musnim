"""Technical QA for the experimental 20-second progressive score drawing."""
from pathlib import Path

from musnim.video_qa import VideoQAError, assess_media, inspect_with_ffprobe

ROOT = Path(__file__).resolve().parents[1]
MOVIE = (
    ROOT / "media" / "videos" / "score_drawing_demo"
    / "480p15" / "AnimatedScoreDrawingDemo.mp4"
)


def main():
    try:
        result = assess_media(
            inspect_with_ffprobe(MOVIE),
            expected_duration=20.0,
            tolerance=1.0,
        )
    except VideoQAError as error:
        raise SystemExit(f"DRAWING QA ERROR: {error}") from error
    print("MP4:", MOVIE)
    print("Duración:", result["duration_seconds"], "s")
    print("Resolución:", result["width"], "x", result["height"])
    print("Frecuencia:", result["fps"], "fps")
    print("Video:", result["video_codec"], "Audio:", result["audio_codec"])
    print("OK: el clip tiene video, audio y una duración próxima a 20 s.")
    print("Pendiente: inspeccionar trazado, glyphs y nota-sincronización.")


if __name__ == "__main__":
    main()
