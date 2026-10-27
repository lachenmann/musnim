"""Selectable LilyPond notehead graphics imported through Manim 0.22.

This module requires Manim and is imported only during graphical work.
"""
from pathlib import Path

from manim import SVGMobject

from .engraving import LilyPondError
from .semantic_notes import read_svg_note_refs


class SemanticScore(SVGMobject):
    """Imported complete score with individual notehead identities.

    Manim maps group ids via id_to_vgroup_dict. We additionally capture
    shape ids (such as a notehead id on a path). The ordinary SVG cache
    is disabled, ensuring the saved shapes belong to this exact score
    instance and follow its transformations.
    """

    def __init__(self, file_name: str | Path, **kwargs):
        self.note_refs = read_svg_note_refs(file_name)
        self._shapes_by_svg_id = {}
        kwargs.pop("use_svg_cache", None)
        super().__init__(
            file_name=file_name, use_svg_cache=False, **kwargs
        )

    def get_mob_from_shape_element(self, shape):
        mob = super().get_mob_from_shape_element(shape)
        if mob is not None:
            svg_id = getattr(shape, "values", {}).get("id")
            if svg_id:
                self._shapes_by_svg_id[str(svg_id)] = mob
        return mob

    def note(self, musical_id: str):
        """Return a geometry object attached to the given musical event."""
        if musical_id not in self.note_refs:
            raise LilyPondError(f"Nota musical desconocida: {musical_id}")
        graphic_id = self.note_refs[musical_id].svg_id

        shape = self._shapes_by_svg_id.get(graphic_id)
        if shape is not None and shape.has_points():
            return shape

        group = self.id_to_vgroup_dict.get(graphic_id)
        if group is not None and group.get_all_points().size:
            return group

        raise LilyPondError(
            f"Geometría Manim ausente: nota {musical_id}, "
            f"svg-id {graphic_id}; ejecutar inspect_semantic_notes.py"
        )
