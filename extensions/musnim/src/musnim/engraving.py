"""LilyPond-to-SVG compilation and semantic score identifiers.

Note-id extraction is independent of Manim's SVG submobject ordering.
Actual LilyPond output and note-by-note selection need integration tests.
"""

from dataclasses import dataclass
from pathlib import Path
import hashlib
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET


class LilyPondError(RuntimeError):
    """Failed engraving or SVG validation."""


def _locate_lilypond(explicit: str | None) -> str:
    executable = explicit or os.environ.get("MUSNIM_LILYPOND") or shutil.which("lilypond")
    if not executable:
        raise LilyPondError(
            "LilyPond no está disponible. Instala LilyPond 2.26 y configura "
            "MUSNIM_LILYPOND, o añade lilypond al PATH."
        )
    return str(executable)


@dataclass(frozen=True)
class LilyPondRenderer:
    executable: str | None = None
    timeout_seconds: int = 120

    def render_svg(self, source: str | Path, destination: str | Path) -> Path:
        score = Path(source).resolve()
        if not score.is_file() or score.suffix != ".ly":
            raise LilyPondError(f"Fuente LilyPond inválida: {score}")
        output_dir = Path(destination).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        executable = _locate_lilypond(self.executable)
        checksum = hashlib.sha256(score.read_bytes()).hexdigest()[:12]
        base = output_dir / f"{score.stem}-{checksum}"
        expected = base.with_suffix(".svg")
        if expected.is_file() and expected.stat().st_size:
            return expected
        command = [
            executable, "-fsvg", "-dcrop", "-dno-point-and-click",
            "-o", str(base), str(score),
        ]
        try:
            result = subprocess.run(
                command, capture_output=True, text=True,
                timeout=self.timeout_seconds, check=False,
            )
        except (FileNotFoundError, OSError, subprocess.TimeoutExpired) as error:
            raise LilyPondError(f"Fallo al ejecutar LilyPond: {error}") from error
        if result.returncode:
            raise LilyPondError(
                f"LilyPond devolvió {result.returncode}:\n{result.stderr[-4000:]}"
            )
        candidates = [
            base.with_suffix(".cropped.svg"), expected,
            *sorted(output_dir.glob(base.name + "-*.svg")),
        ]
        for candidate in candidates:
            if candidate.is_file() and candidate.stat().st_size:
                return candidate
        raise LilyPondError("LilyPond terminó sin generar SVG")


def semantic_note_ids(svg_path: str | Path) -> tuple[str, ...]:
    """Read distinct data-musnim-id attributes in an actual SVG document."""
    path = Path(svg_path)
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as error:
        raise LilyPondError(f"SVG ilegible: {path}") from error
    ids = [
        item.attrib["data-musnim-id"]
        for item in root.iter()
        if "data-musnim-id" in item.attrib
    ]
    if len(ids) != len(set(ids)):
        raise LilyPondError("El SVG contiene identificadores semánticos repetidos")
    return tuple(ids)


def validate_note_coverage(
    expected_in_score_order: tuple[str, ...] | list[str],
    observed_in_svg_order: tuple[str, ...] | list[str],
) -> tuple[str, ...]:
    """Validate 1:1 semantic coverage, preserving the independent score order.

    LilyPond may emit SVG groups in graphical rather than musical order.
    Matching IDs establishes coverage, while musical events own chronology.
    """
    expected = tuple(expected_in_score_order)
    observed = tuple(observed_in_svg_order)
    if (
        any(not isinstance(value, str) or not value for value in expected)
        or len(expected) != len(set(expected))
    ):
        raise LilyPondError("La partitura contiene IDs semánticos inválidos o repetidos")
    if (
        any(not isinstance(value, str) or not value for value in observed)
        or len(observed) != len(set(observed))
    ):
        raise LilyPondError("El SVG contiene IDs semánticos inválidos o repetidos")

    missing = sorted(set(expected) - set(observed))
    extra = sorted(set(observed) - set(expected))
    if missing or extra:
        raise LilyPondError(
            f"IDs ausentes en SVG: {missing}; IDs inesperados en SVG: {extra}"
        )
    return expected
