"""ZAR-001 — First audiovisual laboratory: proportional hearing.

LilyPond is the sole notation/engraving engine. MathTex is used for
mathematical statements, and the audio consists of original synthesized
teaching tones. This is a schematic pitch reduction, not an orchestral
transcription of measures 1–21 of Strauss.
"""
from pathlib import Path

from manim import (
    Scene, Text, MathTex, SVGMobject, VGroup, Line,
    FadeIn, FadeOut, Indicate, UP, DOWN, LEFT, RIGHT,
    BLUE_C, GOLD_C, GREEN_C, WHITE, GREY_B,
)

from musnim import LilyPondRenderer
from musnim.audio import synthesize_demonstration

PROJECT = Path(__file__).resolve().parents[1]


class CueClock:
    """Schedule scene actions on a predictable timeline in seconds."""

    def __init__(self, scene: Scene):
        self.scene = scene
        self.time = 0.0

    def until(self, at: float):
        if at < self.time - 1e-8:
            raise ValueError(f"Retroactive cue: {at} < {self.time}")
        if at > self.time:
            self.scene.wait(at - self.time)
            self.time = at

    def play(self, *animations, duration: float = 1.0):
        self.scene.play(*animations, run_time=duration)
        self.time += duration


def heading(text: str) -> Text:
    """Persistent chapter title occupying only the top band of the frame."""
    result = Text(text, font_size=32, color=GOLD_C)
    if result.width > 11.8:
        result.scale_to_fit_width(11.8)
    return result.to_edge(UP, buff=0.40)


def math_card(
    latex: str,
    explanation: str,
    color=WHITE,
    *,
    secondary_latex: str | None = None,
    y: float = 0.25,
) -> VGroup:
    """A formula region with its own reserved space and explanatory caption."""
    primary = MathTex(latex, font_size=63, color=color)
    if primary.width > 10.7:
        primary.scale_to_fit_width(10.7)
    elements = [primary]

    if secondary_latex:
        secondary = MathTex(secondary_latex, font_size=49, color=color)
        if secondary.width > 10.7:
            secondary.scale_to_fit_width(10.7)
        elements.append(secondary)

    caption = Text(explanation, font_size=24, color=GREY_B)
    if caption.width > 10.7:
        caption.scale_to_fit_width(10.7)
    elements.append(caption)
    return VGroup(*elements).arrange(DOWN, buff=0.40).move_to(UP * y)


def ratio_bars() -> VGroup:
    """Normalized relative frequencies C : G : C' = 1 : 3/2 : 2."""
    group = VGroup()
    for i, (label, ratio, color) in enumerate([
        ("Do · 1", 1.0, BLUE_C),
        ("Sol · 3/2", 1.5, GOLD_C),
        ("Do' · 2", 2.0, GREEN_C),
    ]):
        y = -1.48 - i * 0.48
        note_label = Text(label, font_size=21, color=color)
        note_label.move_to(LEFT * 3.4 + UP * y)
        bar = Line(
            LEFT * 2.2 + UP * y,
            LEFT * 2.2 + RIGHT * (1.85 * ratio) + UP * y,
            color=color,
            stroke_width=10,
        )
        group.add(note_label, bar)
    return group


class ZarathustraPitagorico(Scene):
    """An analytical teaching scene with separated music and math bands."""

    def construct(self):
        self.camera.background_color = "#101826"
        clock = CueClock(self)

        audio = synthesize_demonstration(
            PROJECT / "audio" / "demostracion_ratios.wav"
        )
        self.add_sound(str(audio))

        title = Text("ZARATHUSTRA", font_size=67, color=WHITE)
        title.move_to(UP * 1.15)
        subtitle = Text(
            "El amanecer de las proporciones", font_size=32, color=GOLD_C
        ).next_to(title, DOWN, buff=0.35)
        credit = Text(
            "Strauss · Also sprach Zarathustra · Introducción (1896)",
            font_size=20,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.30)

        clock.play(FadeIn(title), duration=1.8)
        clock.play(FadeIn(subtitle), FadeIn(credit), duration=1.2)
        clock.until(7.0)

        # Musical region: the score and its annotations occupy distinct bands.
        score_source = PROJECT / "score" / "naturmotiv_reduccion.ly"
        svg = LilyPondRenderer().render_svg(
            score_source, PROJECT / "_build" / "lilypond"
        )
        score = SVGMobject(str(svg))
        score.scale_to_fit_width(8.4)
        score.set_color(WHITE)
        # Explicit stroke makes thin staff lines legible on the dark canvas.
        score.set_stroke(color=WHITE, width=1.0, opacity=1.0)
        score.move_to(UP * 1.08)

        score_title = heading("El motivo de la naturaleza")
        score_caption = Text(
            "Reducción didáctica de alturas · ritmo esquemático",
            font_size=22,
            color=GREY_B,
        ).move_to(DOWN * 1.95)
        notes = Text(
            "Do    ·    Sol    ·    Do'",
            font_size=36,
            color=GOLD_C,
        ).move_to(DOWN * 1.1)

        clock.play(FadeOut(title), FadeOut(subtitle), duration=0.65)
        clock.play(FadeIn(score_title), FadeIn(score), duration=1.0)
        clock.play(FadeIn(score_caption), duration=0.4)
        clock.until(11.0)
        clock.play(FadeIn(notes), duration=0.9)
        clock.until(14.0)
        clock.play(
            Indicate(score, color=GOLD_C, scale_factor=1.025),
            duration=1.1,
        )
        clock.until(20.0)

        # Mathematical region begins when the staff exits the frame.
        clock.play(
            FadeOut(score), FadeOut(score_title),
            FadeOut(score_caption), FadeOut(notes),
            duration=0.8,
        )
        analysis_title = heading("La consonancia como proporción")
        current = math_card(
            r"f_C:f_G:f_{C^\prime}=2:3:4",
            "Los armónicos segundo, tercero y cuarto",
            GOLD_C,
            y=1.10,
        )
        bars = ratio_bars()
        clock.play(FadeIn(analysis_title), FadeIn(current), duration=1.0)
        clock.play(FadeIn(bars), duration=0.6)
        clock.until(27.0)

        fifth = math_card(
            r"\frac{f_G}{f_C}=\frac32\qquad"
            r"\frac{f_{C^\prime}}{f_C}=2",
            "Quinta pura y octava",
            GREEN_C,
        )
        clock.play(
            FadeOut(current), FadeIn(fifth), FadeOut(bars), duration=1.2
        )
        current = fifth
        clock.until(32.0)

        major = math_card(
            r"f_C:f_E:f_G=4:5:6",
            "La tercera mayor justa introduce el armónico quinto",
            GOLD_C,
        )
        clock.play(FadeOut(current), FadeIn(major), duration=1.2)
        current = major
        clock.until(39.0)

        comma = math_card(
            r"\frac{81}{64}\neq\frac54",
            "La diferencia entre ambas terceras es la coma sintónica",
            GOLD_C,
            secondary_latex=r"\frac{81/64}{5/4}=\frac{81}{80}",
        )
        clock.play(FadeOut(current), FadeIn(comma), duration=1.2)
        current = comma
        clock.until(44.0)

        minor = math_card(
            r"f_C:f_{E^\flat}:f_G=10:12:15",
            "Tríada menor en afinación justa",
            BLUE_C,
        )
        clock.play(FadeOut(current), FadeIn(minor), duration=1.2)
        current = minor
        clock.until(51.0)

        lower_thirds = math_card(
            r"\frac{32}{27}\neq\frac65",
            "Tercera menor pitagórica y tercera menor justa",
            BLUE_C,
        )
        clock.play(
            FadeOut(current), FadeIn(lower_thirds), duration=1.2
        )
        current = lower_thirds
        clock.until(56.0)

        return_title = heading("Retornos del motivo · cc. 5–6, 9–10 y 13–14")
        major_return = math_card(
            r"4:5:6",
            "Do mayor justo · experimento auditivo",
            GOLD_C,
        )
        clock.play(
            FadeOut(analysis_title), FadeIn(return_title),
            FadeOut(current), FadeIn(major_return),
            duration=1.2,
        )
        current = major_return
        clock.until(65.0)

        minor_return = math_card(
            r"10:12:15",
            "Do menor justo · experimento auditivo",
            BLUE_C,
        )
        clock.play(
            FadeOut(current), FadeIn(minor_return), duration=1.2
        )
        current = minor_return
        clock.until(71.0)

        major_return = math_card(
            r"4:5:6",
            "Do mayor justo · experimento auditivo",
            GOLD_C,
        )
        clock.play(
            FadeOut(current), FadeIn(major_return), duration=1.2
        )
        current = major_return
        clock.until(75.0)

        closing = Text(
            "Afinación ideal · audio original · partitura integral en estudio",
            font_size=23,
            color=GREY_B,
        )
        if closing.width > 11:
            closing.scale_to_fit_width(11)
        closing.move_to(UP * 0.3)
        clock.play(
            FadeOut(return_title), FadeOut(current), FadeIn(closing),
            duration=1.3,
        )
        clock.until(79.0)
