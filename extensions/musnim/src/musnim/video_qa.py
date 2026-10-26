"""Technical verification of rendered audiovisual files for Musnim.

Validates container, duration and streams using FFprobe, distributed with
FFmpeg. This checks technical presence, not visual fidelity or synchronization.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
import shutil
import subprocess


class VideoQAError(RuntimeError):
    """A render is missing required audiovisual characteristics."""


def inspect_with_ffprobe(video: str | Path) -> dict:
    """Read the container metadata through the local FFprobe executable."""
    path = Path(video)
    if not path.is_file() or path.stat().st_size == 0:
        raise VideoQAError(f"MP4 inexistente o vacío: {path}")
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        ffmpeg = shutil.which("ffmpeg")
        if ffmpeg:
            sibling = Path(ffmpeg).with_name(
                "ffprobe.exe" if Path(ffmpeg).suffix.lower() == ".exe" else "ffprobe"
            )
            if sibling.is_file():
                ffprobe = str(sibling)
    if not ffprobe:
        raise VideoQAError("FFprobe no está disponible. Añade ffprobe.exe al PATH.")
    try:
        result = subprocess.run(
            [
                ffprobe, "-v", "error",
                "-show_entries",
                "stream=codec_type,codec_name,width,height,avg_frame_rate",
                "-show_entries", "format=duration",
                "-of", "json", str(path),
            ],
            capture_output=True, text=True, check=False, timeout=45,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise VideoQAError(f"Error ejecutando FFprobe: {exc}") from exc
    if result.returncode != 0:
        raise VideoQAError(f"FFprobe falló: {result.stderr[-1600:]}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise VideoQAError("FFprobe devolvió una respuesta ilegible") from exc


def assess_media(
    data: dict,
    expected_duration: float = 79.0,
    tolerance: float = 2.0,
) -> dict:
    """Validate fundamental properties and return an inspectable report."""
    try:
        duration = float(data["format"]["duration"])
        streams = data["streams"]
        video = next(s for s in streams if s.get("codec_type") == "video")
        audio = next(s for s in streams if s.get("codec_type") == "audio")
        width = int(video["width"])
        height = int(video["height"])
        fps = float(Fraction(video["avg_frame_rate"]))
    except (KeyError, TypeError, ValueError, ZeroDivisionError, StopIteration) as exc:
        raise VideoQAError(
            "Metadatos incompletos: se requieren duración, video y audio"
        ) from exc

    if abs(duration - expected_duration) > tolerance:
        raise VideoQAError(
            f"Duración {duration:.2f}s fuera de {expected_duration}±{tolerance}s"
        )
    if width < 640 or height < 360:
        raise VideoQAError(f"Resolución insuficiente para la prueba: {width}×{height}")
    if fps < 10:
        raise VideoQAError(f"Frecuencia de imagen insuficiente: {fps:g} fps")

    return {
        "duration_seconds": round(duration, 3),
        "width": width,
        "height": height,
        "fps": round(fps, 3),
        "video_codec": video.get("codec_name", "desconocido"),
        "audio_codec": audio.get("codec_name", "desconocido"),
    }
