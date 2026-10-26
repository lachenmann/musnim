"""Stable musical event identities mapped onto LilyPond SVG identifiers.

The musical timeline is defined by the event manifest and independently
of the element order chosen by LilyPond in the SVG file.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from math import isfinite
from pathlib import Path
from xml.etree import ElementTree as ET

from .engraving import LilyPondError, validate_note_coverage


@dataclass(frozen=True)
class SVGNoteRef:
    musical_id: str
    svg_id: str
    tag: str


@dataclass(frozen=True)
class NoteEvent:
    id: str
    pitch: str
    onset_beats: float
    duration_beats: float


def read_svg_note_refs(source: str | Path) -> dict[str, SVGNoteRef]:
    """Map data-musnim-id to an ordinary SVG id regardless of DOM order."""
    try:
        root = ET.parse(source).getroot()
    except (ET.ParseError, OSError) as error:
        raise LilyPondError(f"SVG inválido: {source}") from error
    results: dict[str, SVGNoteRef] = {}
    graphic_ids: set[str] = set()
    for item in root.iter():
        musical_id = item.attrib.get("data-musnim-id")
        if musical_id is None:
            continue
        graphic_id = item.attrib.get("id")
        if not musical_id or not graphic_id:
            raise LilyPondError(
                "Una nota SVG carece de data-musnim-id o del atributo id: "
                f"{item.tag}"
            )
        if musical_id in results or graphic_id in graphic_ids:
            raise LilyPondError(
                f"Identificador musical o gráfico SVG repetido: "
                f"{musical_id}, {graphic_id}"
            )
        results[musical_id] = SVGNoteRef(
            musical_id=musical_id,
            svg_id=graphic_id,
            tag=item.tag.rsplit("}", 1)[-1],
        )
        graphic_ids.add(graphic_id)
    if not results:
        raise LilyPondError(
            "El SVG no contiene notas con identificador data-musnim-id"
        )
    return results


def read_note_events(source: str | Path) -> tuple[NoteEvent, ...]:
    """Parse a typed musical event stream in chronological order."""
    try:
        payload = json.loads(Path(source).read_text(encoding="utf-8"))
        raw_events = payload["events"]
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise LilyPondError(f"Manifiesto musical ilegible: {source}") from error
    if not isinstance(raw_events, list) or not raw_events:
        raise LilyPondError("El manifiesto musical debe contener eventos")
    events: list[NoteEvent] = []
    seen: set[str] = set()
    for raw in raw_events:
        try:
            identifier = raw["id"]
            pitch = raw["pitch"]
            onset = raw["onset_beats"]
            duration = raw["duration_beats"]
        except (TypeError, KeyError) as error:
            raise LilyPondError("Un evento musical está incompleto") from error
        if (
            not isinstance(identifier, str) or not identifier
            or not isinstance(pitch, str) or not pitch
            or identifier in seen
        ):
            raise LilyPondError(f"IDs o alturas inválidos: {identifier}")
        if (
            isinstance(onset, bool) or isinstance(duration, bool)
            or not isinstance(onset, (int, float))
            or not isinstance(duration, (int, float))
            or not isfinite(onset) or not isfinite(duration)
            or onset < 0 or duration <= 0
        ):
            raise LilyPondError(f"Tiempo inválido en nota: {identifier}")
        if events and onset < events[-1].onset_beats:
            raise LilyPondError("Los eventos deben ordenarse por inicio")
        events.append(NoteEvent(
            id=identifier, pitch=pitch,
            onset_beats=float(onset), duration_beats=float(duration),
        ))
        seen.add(identifier)
    return tuple(events)


def matched_svg_notes(
    svg: str | Path, manifest: str | Path
) -> tuple[tuple[NoteEvent, SVGNoteRef], ...]:
    """Join the graphical notes and score events in the score's chronology."""
    events = read_note_events(manifest)
    refs = read_svg_note_refs(svg)
    validate_note_coverage([event.id for event in events], list(refs))
    return tuple((event, refs[event.id]) for event in events)
