"""Inspect a locally rendered ZAR-001 MP4 via FFprobe, without re-rendering."""

import argparse
from pathlib import Path

from musnim.video_qa import VideoQAError, assess_media, inspect_with_ffprobe

ROOT = Path(__file__).resolve().parents[1]
VIDEO_ROOT = ROOT / "media" / "videos" / "zarathustra_pitagorico"


def recent_render() -> Path:
    """Select the most recently written MP4 from Manim's quality folders."""
    files = list(VIDEO_ROOT.glob("*/ZarathustraPitagorico.mp4"))
    if not files:
        raise VideoQAError(
            f"No hay un render en {VIDEO_ROOT}. Ejecuta render_musnim.ps1."
        )
    return max(files, key=lambda path: path.stat().st_mtime)


def main() -> None:
    parser = argparse.ArgumentParser(description="QA técnico audiovisual ZAR-001")
    parser.add_argument(
        "--video",
        type=Path,
        help="Ruta concreta al MP4 (por defecto, el render más reciente)",
    )
    args = parser.parse_args()

    try:
        target = args.video if args.video is not None else recent_render()
        results = assess_media(inspect_with_ffprobe(target))
    except VideoQAError as error:
        raise SystemExit(f"QA ERROR: {error}") from error

    print("Archivo:", target)
    print("Duración:", results["duration_seconds"], "s")
    print("Resolución:", results["width"], "x", results["height"])
    print("Fotogramas por segundo:", results["fps"])
    print("Códec de video:", results["video_codec"])
    print("Códec de audio:", results["audio_codec"])
    print("OK: el MP4 contiene video y audio y presenta duración coherente.")
    print("Pendiente: revisar visualmente la tipografía y la partitura.")


if __name__ == "__main__":
    main()
