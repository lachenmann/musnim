"""Graphical layers in a LilyPond SVG, independent of the SVG node order.

LilyPond provides SVG groups for musical grobs through output-attributes.
A note uses data-musnim-id; other grobs use data-musnim-role and may
declare an owner that connects a stem to its particular note event.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET

from .engraving import LilyPondError


@dataclass(frozen=True)
class ScoreGraphic:
    """A selectable LilyPond engraved element."""

    role: str
    svg_id: str
    owner: str | None = None


def read_score_layers(source: str | Path) -> tuple[ScoreGraphic, ...]:
    """Collect grob roles and ids from an SVG document.

    Graphic traversal order is returned for inspection, but the animation
    sequence must choose layers by role and musical-event identifiers.
    """
    try:
        root = ET.parse(source).getroot()
    except (ET.ParseError, OSError) as error:
        raise LilyPondError(f"No se puede leer SVG de capas: {source}") from error

    result: list[ScoreGraphic] = []
    known_ids: set[str] = set()
    for element in root.iter():
        role = element.attrib.get("data-musnim-role")
        if role is None:
            continue
        graphic_id = element.attrib.get("id")
        if not role or not graphic_id:
            raise LilyPondError(
                f"Grob sin id o data-musnim-role: {element.tag}"
            )
        if graphic_id in known_ids:
            raise LilyPondError(f"ID gráfico duplicado: {graphic_id}")
        owner = element.attrib.get("data-musnim-owner")
        if owner is not None and not owner:
            raise LilyPondError(f"Propietario musical vacío: {graphic_id}")
        result.append(ScoreGraphic(role, graphic_id, owner))
        known_ids.add(graphic_id)
    return tuple(result)


def require_score_layer(
    layers: tuple[ScoreGraphic, ...],
    role: str,
    *,
    owner: str | None = None,
) -> ScoreGraphic:
    """Return exactly one layer matching the semantic role and owner."""
    matches = [
        part for part in layers
        if part.role == role and (owner is None or part.owner == owner)
    ]
    if len(matches) != 1:
        raise LilyPondError(
            f"Se esperaba exactamente un elemento SVG para "
            f"{role} (owner={owner!r}); encontrados: {len(matches)}"
        )
    return matches[0]
