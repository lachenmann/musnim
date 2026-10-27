"""Manim musical score with separately selectable LilyPond graphic layers."""
from pathlib import Path

from .engraving import LilyPondError
from .score_layers import read_score_layers, require_score_layer
from .semantic_mobject import SemanticScore


class DrawingScore(SemanticScore):
    """A score whose staff, clef, meter, stems, and barline can be animated.

    Each SVG graphical ID resolves to its actual VMobjects, including
    their parent transformations. The entire score remains LilyPond-made.
    """

    def __init__(self, file_name: str | Path, **kwargs):
        self.score_layers = read_score_layers(file_name)
        super().__init__(file_name, **kwargs)

    def layer(self, role: str, *, owner: str | None = None):
        """Find an individual engraved component by its LilyPond metadata."""
        ref = require_score_layer(self.score_layers, role, owner=owner)
        graphic_id = ref.svg_id
        group = self.id_to_vgroup_dict.get(graphic_id)
        if group is not None and len(group.get_all_points()) > 0:
            return group

        shape = self._shapes_by_svg_id.get(graphic_id)
        if shape is not None and shape.has_points():
            return shape
        raise LilyPondError(
            f"Elemento {role} (owner={owner}) sin geometría "
            f"Manim: SVG id={graphic_id}. Ejecuta "
            "scripts/inspect_score_drawing.py."
        )
