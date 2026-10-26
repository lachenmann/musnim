"""ZAR-001: animated study of the Naturmotiv, with original synthetic audio.

The LilyPond score is a schematic pitch reduction, not a transcription of
Strauss's original rhythm, orchestration, or all measures 1–21.
"""
from pathlib import Path

from manim import (
    Scene, Text, MathTex, SVGMobject, VGroup, Line, FadeIn, FadeOut,
    Write, Transform, Indicate, UP, DOWN, LEFT, RIGHT,
    BLUE_C, GOLD_C, GREEN_C, WHITE, GREY_B,
)
from musnim import LilyPondRenderer
from musnim.audio import synthesize_demonstration

PROJECT = Path(__file__).resolve().parents[1]


class CueClock:
    """Schedule animation events on a simple elapsed-seconds timeline."""

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


def ratio_card(latex: str, explanation: str, color=WHITE) -> VGroup:
    formula = MathTex(latex, font_size=56, color=color)
    caption = Text(explanation, font_size=23, color=GREY_B)
    if caption.width > 11.3:
        caption.scale_to_fit_width(11.3)
    return VGroup(formula, caption).arrange(DOWN, buff=.35).move_to(DOWN)


def ratio_lines() -> VGroup:
    lines = VGroup()
    for index, (name, length, color) in enumerate([
        ("Do: 1", 3.0, BLUE_C),
        ("Sol: 3/2", 4.5, GOLD_C),
        ("Do': 2", 6.0, GREEN_C),
    ]):
        y = -1.05 - index * .6
        line = Line(
            LEFT * 2.75 + UP * y,
            LEFT * 2.75 + RIGHT * length + UP * y,
            color=color,
            stroke_width=12,
        )
        label = Text(name, font_size=22, color=color).next_to(
            line, LEFT, buff=.25)
        lines.add(line, label)
    return lines.move_to(DOWN * .7)


class ZarathustraPitagorico(Scene):
    """First conceptual scene: pitched intervals and ideal tuning models."""

    def construct(self):
        self.camera.background_color = "#111925"
        clock = CueClock(self)
        sound = synthesize_demonstration(
            PROJECT / "audio" / "demostracion_ratios.wav")
        self.add_sound(str(sound))

        title = Text("ZARATHUSTRA", font_size=65, color=WHITE).to_edge(
            UP, buff=.7)
        subtitle = Text(
            "El amanecer de las proporciones",
            font_size=31, color=GOLD_C,
        ).next_to(title, DOWN, buff=.4)
        credit = Text(
            "Strauss · Also sprach Zarathustra · Introducción (1896)",
            font_size=22, color=GREY_B,
        ).to_edge(DOWN, buff=.5)
        clock.play(FadeIn(title), duration=2)
        clock.play(FadeIn(subtitle), FadeIn(credit), duration=1.4)
        clock.until(7)

        source = PROJECT / "score" / "naturmotiv_reduccion.ly"
        svg = LilyPondRenderer().render_svg(
            source, PROJECT / "_build" / "lilypond")
        staff = SVGMobject(str(svg))
        staff.scale_to_fit_width(11.3)
        staff.set_color(WHITE)
        staff.move_to(UP * .8)
        provenance = Text(
            "Reducción didáctica de alturas — ritmo esquemático",
            font_size=21, color=GREY_B,
        ).next_to(staff, DOWN, buff=.22)
        clock.play(FadeOut(title), FadeOut(subtitle), duration=.7)
        clock.play(FadeIn(staff), FadeIn(provenance), duration=1.6)
        clock.until(11)

        notes = Text(
            "Do  —  Sol  —  Do'",
            font_size=43, color=GOLD_C,
        ).move_to(DOWN * 1.75)
        clock.play(Write(notes), duration=2.1)
        clock.play(Indicate(staff, color=GOLD_C, scale_factor=1.015),
                   duration=1.5)
        clock.until(20)

        relation = ratio_card(
            r"f_C:f_G:f_{C^\prime}=2:3:4",
            "Tres armónicos consecutivos: 2, 3 y 4",
            color=GOLD_C,
        )
        clock.play(
            FadeOut(notes), FadeOut(provenance),
            Transform(staff, staff.copy().scale(.75).to_edge(UP, buff=1)),
            duration=1,
        )
        bars = ratio_lines().scale(.65).to_edge(DOWN, buff=.9)
        relation.move_to(UP * .3)
        clock.play(FadeIn(relation), FadeIn(bars), duration=1.5)
        clock.until(27)

        fifth = ratio_card(
            r"\frac{f_G}{f_C}=\frac32\qquad\frac{f_{C^\prime}}{f_C}=2",
            "Quinta pura y octava",
            color=GREEN_C,
        )
        clock.play(Transform(relation, fifth), FadeOut(bars), duration=1.8)
        clock.until(32)

        major = ratio_card(
            r"f_C:f_E:f_G=4:5:6",
            "La tercera mayor justa incorpora el armónico 5",
            color=GOLD_C,
        )
        clock.play(Transform(relation, major), duration=1.5)
        clock.until(39)

        comparison = ratio_card(
            r"\frac{81}{64}\neq\frac54\qquad"
            r"\frac{81/64}{5/4}=\frac{81}{80}",
            "La coma sintónica distingue ambas terceras mayores",
            color=GOLD_C,
        )
        clock.play(Transform(relation, comparison), duration=1.8)
        clock.until(44)

        minor = ratio_card(
            r"f_C:f_{E^\flat}:f_G=10:12:15",
            "Tríada menor en afinación justa",
            color=BLUE_C,
        )
        clock.play(Transform(relation, minor), duration=1.5)
        clock.until(51)

        lower_thirds = ratio_card(
            r"\frac{32}{27}\neq\frac65",
            "Tercera menor pitagórica y tercera menor justa",
            color=BLUE_C,
        )
        clock.play(Transform(relation, lower_thirds), duration=1.5)
        clock.until(56)

        motif = Text(
            "Retornos del motivo: cc. 5–6 · 9–10 · 13–14",
            font_size=29, color=GOLD_C,
        ).move_to(UP)
        major_return = ratio_card(
            r"4:5:6", "Do mayor justo · experimento auditivo", GOLD_C)
        minor_return = ratio_card(
            r"10:12:15", "Do menor justo · experimento auditivo", BLUE_C)
        clock.play(
            FadeOut(staff), FadeIn(motif),
            Transform(relation, major_return), duration=1.4,
        )
        clock.until(65)
        clock.play(Transform(relation, minor_return), duration=1.4)
        clock.until(71)
        clock.play(Transform(relation, major_return), duration=1.4)
        clock.until(75)

        disclaimer = Text(
            "Afinación ideal · audio sintético propio · transcripción integral pendiente",
            font_size=19, color=GREY_B,
        ).to_edge(DOWN, buff=.45)
        if disclaimer.width > 12:
            disclaimer.scale_to_fit_width(12)
        clock.play(
            FadeOut(relation), FadeOut(motif),
            Transform(credit, disclaimer), duration=1.5,
        )
        clock.until(79)
