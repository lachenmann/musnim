# M3 — First individual-note audiovisual audit (2026-10-26)

Video source: SemanticNotesDemo.mp4 uploaded by the author.
Scenario: a 19-second schematic C4–G4–C5 reduction of
Also sprach Zarathustra. The source manuscript is LilyPond 2.26.0;
the graphics are imported into Manim 0.22.0 via SemanticScore.

## Real media characteristics

FFprobe reports MP4 duration 19.029333 s, size 481927 bytes,
video H.264 854×480 at about 15 fps, and AAC stereo audio at 48 kHz.

The first event occurs at t = 8 s. Before it, the soundtrack includes
a low C pedal (around 131 Hz, t = 1–7 s). The bass has no highlighted
notehead; its status is a teaching prelude rather than one of the
three semantic events.

## Observations per musical event

| ID | Written pitch | Attack time | Head illumination | Audio dominant frequency | Visual label |
| --- | --- | --- | --- | --- | --- |
| c-1 | C4 | 8 s | 8.3–9.0 s | 261.5 Hz approx. | Do |
| g-1 | G4 | 11 s | 11.3–12.0 s | 392.6 Hz approx. | Sol |
| c-2 | C5 | 14 s | 14.3–15.0 s | 523 Hz approx. | Do' |

Frame sampling indicates that the orange highlight is confined to
the target head at each attack. The other two noteheads remain white.
The labels sit horizontally beneath their corresponding heads,
and the MathTex formula 2:3:4 is displayed legibly around t = 16.6 s.

The color is reset approximately 1.3 seconds after the attack.
The audio persists over intervals 8–11, 11–14, and 14–19 seconds.
The first two intervals agree with the demonstrational beat mapping,
but their color does not remain for the whole note duration.
The final C5 ends at 19 seconds, although the manuscript half note
has duration two beats and the explicit model of three seconds per beat
would end it at 20 seconds.

The initial notehead emphasis and audio onset are synchronized at
the cue level. The visible color develops over the initial animation
rather than appearing at full saturation instantaneously.

## Decision and next experiment

**Accepted:** note identity, target-specific animation, legible note
labels, attack timing, and pitch correspondence in the 19-second clip.

**Open:** sustained color aligned with the complete note duration,
C5 six-second sustain, and musical event-driven audio generation.

To address these limitations without altering the first successful
demonstration, M3 v2 introduces note_event_audio.py and the separate
SemanticNotesSustainDemo (20 seconds). It generates audio and
visual transitions from the same event schedule.

M3 v2 code passing unit tests does not establish that the new rendered
video is visually or musically complete. Retain the PR in draft until
the second actual MP4 is inspected.
