from fractions import Fraction
import pytest

from musnim.ratios import (
    cents, fifth_chain, reduce_octave, monochord_frequency_ratios,
    PYTHAGOREAN, JUST, syntonic_comma,
)


def test_motif_in_the_harmonic_series():
    assert monochord_frequency_ratios() == (
        Fraction(1), Fraction(3, 2), Fraction(2))
    assert tuple(x * 2 for x in monochord_frequency_ratios()) == (2, 3, 4)


def test_pythagorean_major_third():
    assert fifth_chain(4) == Fraction(81, 64)
    assert PYTHAGOREAN["major_third"] == Fraction(81, 64)


def test_pythagorean_minor_third():
    assert fifth_chain(-3) == Fraction(32, 27)
    assert PYTHAGOREAN["minor_third"] == Fraction(32, 27)


def test_just_triads_and_comma():
    assert JUST["major_third"] == Fraction(5, 4)
    assert JUST["minor_third"] == Fraction(6, 5)
    assert syntonic_comma() == Fraction(81, 80)


def test_cents_exact_octave_and_fifth():
    assert cents(Fraction(2)) == pytest.approx(1200)
    assert cents(Fraction(3, 2)) == pytest.approx(701.9550, abs=1e-4)
    assert cents(syntonic_comma()) == pytest.approx(21.5063, abs=1e-4)


def test_octave_reduction_invariant_under_power_of_two():
    for n in range(-8, 9):
        assert reduce_octave(Fraction(3, 2) * Fraction(2) ** n) == Fraction(3, 2)


def test_invalid_ratios():
    for ratio in (Fraction(0), Fraction(-1)):
        with pytest.raises(ValueError):
            cents(ratio)
        with pytest.raises(ValueError):
            reduce_octave(ratio)
    with pytest.raises(TypeError):
        fifth_chain(3.5)
