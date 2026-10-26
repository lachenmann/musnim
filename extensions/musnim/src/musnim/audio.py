"""Original teaching-tone synthesis; it does not imitate a Strauss recording."""

from fractions import Fraction
from pathlib import Path
import wave

import numpy as np

BASE_C4_HZ = 261.6255653005986
# Start time (s), duration (s), volume, frequency ratios relative to C4.
SOUND_EVENTS: tuple[tuple[float, float, float, tuple[Fraction, ...]], ...] = (
    (1., 6., .25, (Fraction(1, 2),)),
    (8., 3., .35, (Fraction(1),)),
    (11., 3., .35, (Fraction(3, 2),)),
    (14., 5., .35, (Fraction(2),)),
    (21., 7., .27, (Fraction(1), Fraction(3, 2), Fraction(2))),
    (33., 8., .24, (Fraction(1), Fraction(5, 4), Fraction(3, 2))),
    (45., 8., .24, (Fraction(1), Fraction(6, 5), Fraction(3, 2))),
    (59., 5., .22, (Fraction(1), Fraction(5, 4), Fraction(3, 2))),
    (65., 5., .22, (Fraction(1), Fraction(6, 5), Fraction(3, 2))),
    (71., 5., .25, (Fraction(1), Fraction(5, 4), Fraction(3, 2))),
)


def synthesize_demonstration(
    output: str | Path, duration: float = 79., rate: int = 22050
) -> Path:
    """Write deterministic, mono, 16-bit WAV samples."""
    if duration <= 0 or rate <= 0:
        raise ValueError("Duration and sample rate must be positive")
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    length = int(duration * rate)
    samples = np.zeros(length, dtype=np.float64)
    for start, event_duration, volume, ratios in SOUND_EVENTS:
        low = int(start * rate)
        high = min(length, int((start + event_duration) * rate))
        if low >= high:
            continue
        t = np.arange(high - low, dtype=np.float64) / rate
        attack = np.minimum(1.0, t / .09)
        release = np.minimum(1.0, (event_duration - t) / .14)
        envelope = np.clip(np.minimum(attack, release), 0., 1.)
        signal = np.zeros_like(t)
        for ratio in ratios:
            fundamental = BASE_C4_HZ * float(ratio)
            for harmonic, weight in ((1, 1.0), (2, .22), (3, .09), (4, .04)):
                signal += (weight / len(ratios)) * np.sin(
                    2 * np.pi * fundamental * harmonic * t
                )
        samples[low:high] += volume * signal * envelope
    peak = max(float(np.max(np.abs(samples))), 1.0)
    pcm = np.asarray(samples / peak * 32766, dtype="<i2")
    with wave.open(str(path), "wb") as sound:
        sound.setnchannels(1)
        sound.setsampwidth(2)
        sound.setframerate(rate)
        sound.writeframes(pcm.tobytes())
    return path
