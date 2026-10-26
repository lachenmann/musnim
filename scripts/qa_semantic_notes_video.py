"""Validate the 19-second M3 LilyPond note-by-note demonstration MP4.

FFprobe proves technical stream presence and duration, not correct note
highlighting or audio/video alignment; inspect the actual movie for those.
"""

from argparse import ArgumentParser
from pathlib import Path

from musnim.video_qa import VideoQAError, assess_media, inspect_with_ffprobe

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VIDEO = (
    ROOT / "media" / "videos" / "semantic_notes_demo"
    / "480p15" / "SemanticNotesDemo.mp4"
)


def main() -> None:
    parser = ArgumentParser(description="M3 semantic score audiovisual smoke test")
    parser.add_argument(
        "--video", type=Path, default=DEFAULT_VIDEO,
        help="MP4 path (default: the 480p15 SemanticNotesDemo render)",
    )
    args = parser.parse_args()
    try:
        properties = assess_media(
            inspect_with_ffprobe(args.video),
            expected_duration=19.0,
            tolerance=1.0,
        )
    except VideoQAError as error:
        raise SystemExit(f"M3 QA ERROR: {error}") from error

    print(f"Archivo: {args.video}")
    print(f"Duración: {properties['duration_seconds']} s")
    print(f"Resolución: {properties['width']} x {properties['height']}")
    print(f"Fotogramas por segundo: {properties['fps']}")
    print(f"Códec de video: {properties['video_codec']}")
    print(f"Códec de audio: {properties['audio_codec']}")
    print("OK: M3 MP4 contiene imagen, audio y duración coherente (19 s).")
    print(
        "Pendiente: examinar visualmente Do4 (8 s), Sol4 (11 s), "
        "Do5 (14 s) y comprobar sincronización a oído."
    )


if __name__ == "__main__":
    main()
