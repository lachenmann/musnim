"""Nineteen-second proof of note-by-note LilyPond highlighting.

This scene uses the original synthesized audio and schematic timing.
It is separate from the approved 79-second ZAR-001 video.
"""
from pathlib import Path

from manim import (
    Scene, Text, MathTex, FadeIn, FadeOut, Indicate,
    GOLD_C, GREY_B, WHITE, UP, DOWN,
)

from musnim import LilyPondRenderer
from musnim.audio import synthesize_demonstration
from musnim.semantic_mobject import SemanticScore
from musnim.semantic_notes import matched_svg_notes

PROJECT = Path(__file__).resolve().parents[1]
NOTE_NAMES = {"C4": "Do", "G4": "Sol", "C5": "Do'"}


class SemanticNotesDemo(Scene):
    """Highlight the three staff noteheads at 8, 11 and 14 seconds."""

    def construct(self):
        self.camera.background_color = "#101826"
        folder = PROJECT / "score"
        svg = LilyPondRenderer().render_svg(
            folder / "naturmotiv_reduccion.ly",
            PROJECT / "_build" / "lilypond",
        )
        notes = matched_svg_notes(svg, folder / "naturmotiv_events.json")
        staff = SemanticScore(svg)
        staff.scale_to_fit_width(8.4).move_to(UP * 0.55)
        staff.set_color(WHITE)
        staff.set_stroke(color=WHITE, width=1.0, opacity=1.0)

        title = Text(
            "Do · Sol · Do' — una nota cada vez",
            font_size=29, color=GOLD_C,
        ).to_edge(UP, buff=0.4)
        notice = Text(
            "Reducción didáctica · tiempos esquemáticos",
            font_size=20, color=GREY_B,
        ).to_edge(DOWN, buff=0.4)
        formula = MathTex("2:3:4", font_size=55, color=GOLD_C)
        formula.move_to(DOWN * 1.60)

        audio = synthesize_demonstration(
            PROJECT / "audio" / "semantic_notes_demo.wav",
            duration=19.0,
        )
        self.add_sound(str(audio))
        self.play(
            FadeIn(title), FadeIn(staff), FadeIn(notice), run_time=1.5
        )
        elapsed = 1.5
        self.wait(8.0 - elapsed)
        elapsed = 8.0

        for event, ref in notes:
            onset = 8.0 + 3.0 * event.onset_beats
            if onset > elapsed:
                self.wait(onset - elapsed)
                elapsed = onset

            note = staff.note(event.id)
            label = Text(
                NOTE_NAMES.get(event.pitch, event.pitch),
                font_size=26, color=GOLD_C,
            )
            label.move_to([
                note.get_center()[0],
                staff.get_bottom()[1] - 0.48,
                0,
            ])
            self.play(
                Indicate(note, color=GOLD_C, scale_factor=1.2),
                FadeIn(label),
                run_time=1.3,
            )
            elapsed += 1.3
            self.play(FadeOut(label), run_time=0.3)
            elapsed += 0.3

        self.play(FadeIn(formula), run_time=1.0)
        elapsed += 1.0
        if elapsed < 19.0:
            self.wait(19.0 - elapsed)
