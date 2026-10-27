"""M3 laboratory: LilyPond musical symbols drawn progressively with Manim.

The experiment renders a schematic C4-G4-C5 reduction, not a verified
orchestral transcription of Strauss's opening measures. Original synthesized
notes and highlighted drawings share an event schedule (8, 11, 14–20 s).
"""
from pathlib import Path

from manim import (
    Scene, Create, DrawBorderThenFill, Write,
    GOLD_C, GREY_B, WHITE, UP, DOWN, Text, MathTex,
)

from musnim import LilyPondRenderer
from musnim.note_event_audio import make_note_schedule, synthesize_scheduled_notes
from musnim.score_drawing_mobject import DrawingScore
from musnim.semantic_notes import matched_svg_notes

PROJECT = Path(__file__).resolve().parents[1]
SCORES = PROJECT / "score"
PITCH_NAMES = {"C4": "Do", "G4": "Sol", "C5": "Do'"}

INTRO_SECONDS = 8.0
SECONDS_PER_BEAT = 3.0
NOTE_APPEAR_SECONDS = 0.65
NOTE_COLOR_SECONDS = 0.20
NOTE_RELEASE_SECONDS = 0.25


class AnimatedScoreDrawingDemo(Scene):
    """Write staff/clef/meter first, then draw notes as they sound."""

    def construct(self):
        self.camera.background_color = "#101826"
        svg = LilyPondRenderer().render_svg(
            SCORES / "naturmotiv_drawing.ly", PROJECT / "_build" / "lilypond"
        )
        event_map = matched_svg_notes(
            svg, SCORES / "naturmotiv_events.json"
        )
        schedule = make_note_schedule(
            tuple(event for event, _ in event_map),
            lead_in_seconds=INTRO_SECONDS,
            seconds_per_beat=SECONDS_PER_BEAT,
        )

        score = DrawingScore(svg)
        score.scale_to_fit_width(8.4)
        score.move_to(UP * 0.50)
        score.set_color(WHITE)
        score.set_stroke(color=WHITE, width=1.0, opacity=1.0)

        heading = Text(
            "Cómo se escribe una consonancia",
            font_size=31, color=GOLD_C,
        ).to_edge(UP, buff=0.35)
        context = Text(
            "Grabado LilyPond · animación vectorial Manim",
            font_size=20, color=GREY_B,
        ).to_edge(DOWN, buff=0.30)

        frequency_ratio = MathTex(
            r"f_C:f_G:f_{C^\prime}=2:3:4",
            font_size=44, color=GOLD_C,
        )
        if frequency_ratio.width > 9:
            frequency_ratio.scale_to_fit_width(9)
        # Keep the equation in its own lower band beneath pitch labels.
        frequency_ratio.move_to(DOWN * 2.48)

        wav = synthesize_scheduled_notes(
            PROJECT / "audio" / "score_drawing_20s.wav", schedule
        )
        self.add_sound(str(wav))

        elapsed = 0.0

        def until(t: float):
            nonlocal elapsed
            if t < elapsed - 1e-7:
                raise ValueError(f"Evento visual anterior al tiempo actual: {t}")
            if t > elapsed:
                self.wait(t - elapsed)
                elapsed = t

        def animate(*animations, duration: float):
            nonlocal elapsed
            self.play(*animations, run_time=duration)
            elapsed += duration

        # Separate layers retain LilyPond's staff geometry and glyph contours.
        animate(Write(heading), duration=0.9)
        animate(
            Create(score.layer("staff"), lag_ratio=0.22),
            duration=2.4,
        )
        animate(
            DrawBorderThenFill(score.layer("clef")), duration=1.1
        )
        animate(
            DrawBorderThenFill(score.layer("meter")), duration=0.9
        )
        animate(Write(context), duration=0.7)
        until(INTRO_SECONDS)

        for i, note in enumerate(schedule):
            until(note.start_seconds)
            head = score.note(note.event.id)
            stem = score.layer("stem", owner=note.event.id)
            label = Text(
                PITCH_NAMES.get(note.event.pitch, note.event.pitch),
                font_size=24, color=GOLD_C,
            )
            label.move_to([
                head.get_center()[0],
                score.get_bottom()[1] - 0.47,
                0.0,
            ])

            animate(
                DrawBorderThenFill(head),
                Create(stem),
                Write(label),
                duration=NOTE_APPEAR_SECONDS,
            )
            animate(
                head.animate.set_color(GOLD_C),
                duration=NOTE_COLOR_SECONDS,
            )

            if i == len(schedule) - 1:
                until(16.8)
                animate(Write(frequency_ratio), duration=0.8)
                until(18.0)
                animate(Create(score.layer("barline")), duration=0.65)

            until(note.end_seconds - NOTE_RELEASE_SECONDS)
            animate(
                head.animate.set_color(WHITE),
                duration=NOTE_RELEASE_SECONDS,
            )
        until(schedule[-1].end_seconds)
