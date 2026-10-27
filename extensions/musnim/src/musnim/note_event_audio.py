"""Monophonic schematic note playback driven by the score-event manifest.

This first laboratory treats one score beat as an explicit number of seconds.
Intervals are represented as exact ratios; synthesis is audio teaching material
rather than a recorded or reconstructed Strauss performance.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isfinite
from pathlib import Path
import wave

import numpy as np

from .audio import BASE_C4_HZ
from .engraving import LilyPondError
from .semantic_notes import NoteEvent

# The first scene only covers the three pitches in the Naturmotiv.
_PITCH_RATIOS = {
    "C4": Fraction(1),
    "G4": Fraction(3, 2),
    "C5": Fraction(2),
}


@dataclass(frozen=True)
class ScheduledNote:
    event: NoteEvent
    start_seconds: float
    duration_seconds: float
    frequency_hz: float

    @property
    def end_seconds(self) -> float:
        return self.start_seconds + self.duration_seconds


def make_note_schedule(
    events: tuple[NoteEvent, ...],
    *,
    lead_in_seconds: float = 8.0,
    seconds_per_beat: float = 3.0,
) -> tuple[ScheduledNote, ...]:
    """Produce a time-and-frequency contract for one monophonic scene."""
    if (
        not isfinite(lead_in_seconds) or lead_in_seconds < 0
        or not isfinite(seconds_per_beat) or seconds_per_beat <= 0
    ):
        raise LilyPondError("Parámetros temporales del calendario inválidos")
    if not events:
        raise LilyPondError("Se requiere al menos una nota para la demostración")

    result: list[ScheduledNote] = []
    for event in events:
        ratio = _PITCH_RATIOS.get(event.pitch)
        if ratio is None:
            raise LilyPondError(f"Altura fuera del piloto: {event.pitch}")
        start = lead_in_seconds + event.onset_beats * seconds_per_beat
        duration = event.duration_beats * seconds_per_beat
        if duration <= 0 or not isfinite(start) or not isfinite(duration):
            raise LilyPondError(f"Duración inválida de {event.id}")
        if result and start < result[-1].end_seconds - 1e-7:
            raise LilyPondError(
                f"El piloto es monofónico: eventos superpuestos en {event.id}"
            )
        result.append(
            ScheduledNote(
                event=event,
                start_seconds=start,
                duration_seconds=duration,
                frequency_hz=BASE_C4_HZ * float(ratio),
            )
        )
    return tuple(result)


def synthesize_scheduled_notes(
    destination: str | Path,
    schedule: tuple[ScheduledNote, ...],
    *,
    sample_rate: int = 22050,
    include_low_c_intro: bool = True,
) -> Path:
    """Render a deterministic 16-bit WAV using the exact event schedule."""
    if sample_rate < 8000:
        raise ValueError("Sample rate must be at least 8000 Hz")
    if not schedule:
        raise ValueError("The event schedule must contain notes")
    duration_seconds = max(note.end_seconds for note in schedule)
    total_samples = int(round(duration_seconds * sample_rate))
    samples = np.zeros(total_samples, dtype=np.float64)

    def add_tone(start: float, length: float, frequency: float, gain: float):
        low = int(round(start * sample_rate))
        high = min(total_samples, int(round((start + length) * sample_rate)))
        if high <= low:
            return
        t = np.arange(high - low, dtype=np.float64) / sample_rate
        # A brief release makes successive tones meet without clicks.
        envelope = np.minimum.reduce((
            np.ones_like(t),
            t / 0.07,
            np.maximum(0.0, (length - t) / 0.14),
        ))
        partials = np.zeros_like(t)
        for k, weight in ((1, 1.0), (2, 0.22), (3, 0.09), (4, 0.04)):
            partials += weight * np.sin(2 * np.pi * frequency * k * t)
        samples[low:high] += gain * envelope * partials

    if include_low_c_intro and duration_seconds >= 8.0:
        add_tone(1.0, 6.0, BASE_C4_HZ / 2.0, 0.22)

    for note in schedule:
        add_tone(
            note.start_seconds, note.duration_seconds, note.frequency_hz, 0.28
        )

    peak = max(float(np.max(np.abs(samples))), 1.0)
    pcm = np.asarray(samples / peak * 32766, dtype="<i2")
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(sample_rate)
        audio.writeframes(pcm.tobytes())
    return path
