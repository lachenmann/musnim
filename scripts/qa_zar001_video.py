"""Inspect the first locally rendered ZAR-001 MP4 without re-rendering it."""

from pathlib import Path

from musnim.video_qa import VideoQAError, assess_media, inspect_with_ffprobe

ROOT = Path(__file__).resolve().parents[1]
VIDEO = (
    ROOT / "media" / "videos" / "zarathustra_pitagorico"
    / "480p15" / "ZarathustraPitagorico.mp4"
)


def main() -> None:
    try:
        results = assess_media(inspect_with_ffprobe(VIDEO))
    except VideoQAError as error:
        raise SystemExit(f"QA ERROR: {error}") from error
    print("Archivo:", VIDEO)
    print("Duración:", results["duration_seconds"], "s")
    print("Resolución:", results["width"], "x", results["height"])
    print("Fotogramas por segundo:", results["fps"])
    print("Códec de video:", results["video_codec"])
    print("Códec de audio:", results["audio_codec"])
    print("OK: el MP4 contiene video y audio y presenta una duración coherente.")
    print("Pendiente: revisar a vista y oído la partitura y sincronización.")


if __name__ == "__main__":
    main()
