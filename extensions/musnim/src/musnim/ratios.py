"""Exact ideal acoustic ratios; orchestral tuning requires empirical study."""

from fractions import Fraction
from math import log2
from types import MappingProxyType


def cents(ratio: Fraction) -> float:
    """Logarithmic size of a positive frequency ratio in cents."""
    if ratio <= 0:
        raise ValueError("La razón de frecuencias debe ser positiva")
    return 1200 * log2(float(ratio))


def reduce_octave(ratio: Fraction) -> Fraction:
    """Place a positive frequency ratio in [1, 2)."""
    if ratio <= 0:
        raise ValueError("La razón de frecuencias debe ser positiva")
    while ratio < 1:
        ratio *= 2
    while ratio >= 2:
        ratio /= 2
    return ratio


def fifth_chain(steps: int) -> Fraction:
    """Pure fifths, octave reduced. E = 81/64; E flat = 32/27."""
    if not isinstance(steps, int) or isinstance(steps, bool):
        raise TypeError("steps debe ser un entero")
    return reduce_octave(Fraction(3, 2) ** steps)


def monochord_frequency_ratios() -> tuple[Fraction, Fraction, Fraction]:
    """Do–Sol–Do' normalized to its first tone."""
    return (Fraction(1), Fraction(3, 2), Fraction(2))


PYTHAGOREAN = MappingProxyType({
    "fifth": Fraction(3, 2), "octave": Fraction(2),
    "major_third": fifth_chain(4), "minor_third": fifth_chain(-3),
})
JUST = MappingProxyType({
    "fifth": Fraction(3, 2), "octave": Fraction(2),
    "major_third": Fraction(5, 4), "minor_third": Fraction(6, 5),
})


def syntonic_comma() -> Fraction:
    """Pythagorean major third divided by the just major third: 81/80."""
    return PYTHAGOREAN["major_third"] / JUST["major_third"]
