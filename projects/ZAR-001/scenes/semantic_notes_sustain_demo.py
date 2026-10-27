"""Second M3 laboratory: note heads remain highlighted for their full sound.

Unlike the earlier 19-second attack experiment, this separate 20-second
scene uses a single explicit monophonic score timeline for sound and image.
The source score still has schematic durations, not Strauss's actual rhythm.
"""
from pathlib import Path

from manim import (
    Scene, Text, MathTex, FadeIn, FadeOut, GOLD_C, GREY_B, WHITE, UP, DOWN,
)

from musnim import LilyPondRenderer
from musnim.note_event_audio import make_note_schedule, synthesize_scheduled_notes
from musnim.semantic_notes import matched_svg_notes
from musnim.semantic_mobject import SemanticScore

PROJECT = Path(__file__).resolve().parents[1]
SCORE_DIR = PROJECT / "score"
PITCH_NAMES = {"C4": "Do", "G4": "Sol", "C5": "Do'"}

LEAD_IN_SECONDS = 8.0
SECONDS_PER_BEAT = 3.0
ATTACK_FADE_SECONDS = 0.2
RELEASE_FADE_SECONDS = 0.2


class SemanticNotesSustainDemo(Scene):
    """C4 8–11 s, G4 11–14 s, C5 14–20 s from one timeline."""

    def construct(self):
        self.camera.background_color = "#101826"

        svg = LilyPondRenderer().render_svg(
            SCORE_DIR / "naturmotiv_reduccion.ly",
            PROJECT / "_build" / "lilypond",
        )
        matched = matched_svg_notes(
            svg, SCORE_DIR / "naturmotiv_events.json"
        )
        schedule = make_note_schedule(
            tuple(event for event, _ in matched),
            lead_in_seconds=LEAD_IN_SECONDS,
            seconds_per_beat=SECONDS_PER_BEAT,
        )
        staff = SemanticScore(svg)
        staff.scale_to_fit_width(8.4).move_to(UP * 0.55)
        staff.set_color(WHITE)
        staff.set_stroke(color=WHITE, width=1.0, opacity=1.0)

        title = Text(
            "Do · Sol · Do' — duración de cada nota",
            font_size=29, color=GOLD_C,
        ).to_edge(UP, buff=0.4)
        note_scope = Text(
            "Reducción didáctica · tiempos esquemáticos",
            font_size=20, color=GREY_B,
        ).to_edge(DOWN, buff=0.4)
        formula = MathTex(r"2:3:4", font_size=55, color=GOLD_C)
        formula.move_to(DOWN * 1.60)

        wav = synthesize_scheduled_notes(
            PROJECT / "audio" / "semantic_notes_sustain.wav", schedule
        )
        self.add_sound(str(wav))

        self.play(
            FadeIn(title), FadeIn(staff), FadeIn(note_scope), run_time=1.5
        )
        elapsed = 1.5

        def wait_until(moment: float):
            nonlocal elapsed
            if moment > elapsed:
                self.wait(moment - elapsed)
                elapsed = moment

        for i, event in enumerate(schedule):
            wait_until(event.start_seconds)
            notehead = staff.note(event.event.id)
            pitch_name = PITCH_NAMES.get(event.event.pitch, event.event.pitch)
            label = Text(pitch_name, font_size=26, color=GOLD_C)
            label.move_to([
                notehead.get_center()[0],
                staff.get_bottom()[1] - 0.48,
                0.0,
            ])

            # The onset and color activation share the audio event's start.
            self.play(
                notehead.animate.set_color(GOLD_C),
                FadeIn(label),
                run_time=ATTACK_FADE_SECONDS,
            )
            elapsed += ATTACK_FADE_SECONDS

            # The formula enters during the sustained C5, keeping the note lit.
            if i == len(schedule) - 1:
                wait_until(17.0)
                self.play(FadeIn(formula), run_time=0.6)
                elapsed += 0.6

            wait_until(event.end_seconds - RELEASE_FADE_SECONDS)
            # The notehead returns to its original color at the audio release.
            self.play(
                notehead.animate.set_color(WHITE),
                FadeOut(label),
                run_time=RELEASE_FADE_SECONDS,
            )
            elapsed += RELEASE_FADE_SECONDS

        # The score and WAV now share exactly 20 seconds of event chronology.
        wait_until(schedule[-1].end_seconds)
