# M3 — Primer laboratorio de notas animables de LilyPond

Branch: feature/M3-semantic-notes.
Parent branch: feature/ZAR-001-bootstrap.
The 79-second approved third cut remains untouched.

## Representation contract

LilyPond 2.26 exports noteheads with a musical data-musnim-id
and a standard graphic id. The pure Python semantic_notes module joins
these two attributes with naturmotiv_events.json, preserving time order.
Manim 0.22 exposes id_to_vgroup_dict for SVG groups. SemanticScore,
a small SVGMobject subclass, also captures IDs on leaf shapes such as
paths; its mobjects retain the whole staff's transformations.

The first experiment uses a single voice and schematic note durations.
Polyphony will require explicit instrument and voice IDs, as well as
more general musical timing rules.

## Test on Windows with the existing D drive installation

    cd D:\Proyectos\musnim
    git fetch origin
    git switch -c feature/M3-semantic-notes --track origin/feature/M3-semantic-notes

First validate LilyPond IDs and their actual geometry in Manim:

    .\.venv\Scripts\python.exe .\scripts\inspect_semantic_notes.py

If all three noteheads have distinct centers and small positive dimensions,
render the independent 19-second video:

    .\.venv\Scripts\python.exe -m manim -ql projects/ZAR-001/scenes/semantic_notes_demo.py SemanticNotesDemo

Expected output relative to the repository:

    media/videos/semantic_notes_demo/480p15/SemanticNotesDemo.mp4

This proof-of-concept does not overwrite the 79-second Zarathustra movie.

## Acceptance

- All three events are matched to a graphic notehead by ID.
- The score order C4–G4–C5 is retained independently of SVG DOM order.
- Only the chosen notehead is highlighted on each event.
- Labels follow their own notehead positions.
- Synthetic audio attacks at 8, 11 and 14 seconds.
- Python unit tests pass on Windows, macOS and Linux.
- Review a real rendered movie before declaring end-to-end success.

Technical limitations: graphic ID preservation needs verification on the
actual SVG emitted by LilyPond and imported by Manim. The model is
currently single-voice; orchestral notes of Strauss measures 1–21 will
follow after the critical score transcription in Issue #3.

## Real Windows diagnostic — 2026-10-26

The user executed scripts/inspect_semantic_notes.py on the D: development
installation, using LilyPond 2.26.0 and Manim Community 0.22.0.

Observed SVG:
projects/ZAR-001/_build/lilypond/naturmotiv_reduccion-451326967fbe.svg

| Score event | SVG graphic ID | SVG tag | Onset/duration in beats | Manim center (x,y) | Width × height |
| --- | --- | --- | --- | --- | --- |
| c-1 (C4) | zar-nature-01 | g | 0 / 1 | (-0.290, -1.326) | 0.555 × 0.463 |
| g-1 (G4) | zar-nature-02 | g | 1 / 1 | (1.094, -0.475) | 0.555 × 0.463 |
| c-2 (C5) | zar-nature-03 | g | 2 / 2 | (2.452, 0.163) | 0.586 × 0.463 |

The diagnostic ended with:
OK: tres cabezas de nota accesibles por identidad musical.

All three objects have individual dimensions and coordinates. The actual
LilyPond symbols have SVG tag g, so group lookup through Manim's
id_to_vgroup_dict is sufficient for this initial example; the importer also
supports leaf shapes for future score layouts.

The event chronology follows the manifest, not the DOM order. This
validates semantic selection and geometry retrieval in Windows. It does
not yet establish temporal animation, label alignment, or audiovisual
render quality; those require inspection of SemanticNotesDemo.mp4.

### Next integration step

From the already-active feature/M3-semantic-notes branch:

    cd D:\Proyectos\musnim
    .\.venv\Scripts\python.exe -m manim -ql projects/ZAR-001/scenes/semantic_notes_demo.py SemanticNotesDemo

Review 8 s (C4), 11 s (G4), 14 s (C5), the alignment of each label,
and the final 2:3:4 formula. The approved 79-second ZAR-001 remains intact.


## M3 MP4 rendered in Windows — 2026-10-26

User execution confirmed that Manim Community 0.22.0 finished
SemanticNotesDemo successfully: "Rendered SemanticNotesDemo",
"Played 12 animations", and produced the MP4 in:

    media/videos/semantic_notes_demo/480p15/SemanticNotesDemo.mp4

The reported FFmpeg message "Some options were not used" did not stop
the renderer. The log established file creation; dimensions, duration,
presence of audio and alignment of highlighted notes still require
independent verification.

To inspect media container and stream properties (19 ± 1 seconds):

    cd D:\Proyectos\musnim
    git pull --ff-only origin feature/M3-semantic-notes
    .\.venv\Scripts\python.exe .\scripts\qa_semantic_notes_video.py

Open the MP4 from PowerShell:

    Start-Process "D:\Proyectos\musnim\media\videos\semantic_notes_demo\480p15\SemanticNotesDemo.mp4"

## Visual and musical acceptance gate

- [x] LilyPond SVG elements resolved to three individual Manim objects.
- [x] Manim rendered the 12-animation demonstration on Windows.
- [ ] FFprobe technical video/audio verification (run local QA script).
- [ ] Inspect 8–9.5 seconds: Do4 (c-1) is the selected head and audio C4.
- [ ] Inspect 11–12.5 seconds: G4 (g-1) is selected and audio G4.
- [ ] Inspect 14–15.5 seconds: Do5 (c-2) is selected and audio C5.
- [ ] Inspect independent labels align with the appropriate noteheads.
- [ ] Check the ending 2:3:4 expression is readable and uncrowded.
- [ ] Examine output warnings and verify color/stroke behavior.
- [ ] Review the uploaded movie before completing M3 or merging PR #6.

A metadata-only success means the video has the required streams and
rough duration. It cannot prove that the correct note is illuminated.


## First 19-second MP4 audited — 2026-10-26

The user uploaded SemanticNotesDemo.mp4 and the actual media was inspected.

- Duration: **19.029333 seconds**, H.264 854×480 at ~15 fps,
  AAC stereo, 48 kHz.
- C4 (c-1) highlighted at 8.3–9.0 s; audio fundamental
  measured around 261.5 Hz (audible 8–11 s).
- G4 (g-1) highlighted at 11.3–12.0 s; audio around
  392.6 Hz (audible 11–14 s).
- C5 (c-2) highlighted at 14.3–15.0 s; audio around
  523 Hz (audible 14–19 s).
- Each label sits under its corresponding LilyPond notehead,
  and the final MathTex ratio 2:3:4 is legible at ~16.6 s.
- The orange highlight affects only the selected notehead,
  leaving the other two notes white.
- An introductory low C around 131 Hz sounds between
  seconds 1 and 7 (the introductory pedal).

**Accepted:** correct note selection by semantic ID, attack order,
label alignment, and frequency correspondence.

**Identified limitation:** a highlighted note fades back to white
approximately 1.3 seconds after onset, while its sound continues.
The last half note (C5) occupies two beats in the LilyPond
reduction/manifest. At the explicitly chosen three seconds per beat,
its intended duration is six seconds (14–20 s), whereas the first
clip contains only five seconds of C5 (14–19 s).

The first video remains untouched as a verified attack experiment.
The event manifest is still schematic rather than an exact transcription
of Richard Strauss.

## Second sustained-note experiment (M3 v2) — pending render

New files:

- musnim.note_event_audio: deterministic WAV from the event manifest,
  mapping one beat to three seconds.
- semantic_notes_sustain_demo.py: highlights notes from their onset
  until their musical end, including the release interval.
- qa_sustained_notes_video.py: FFprobe test for the 20-second clip.
- Unit tests verify C4 = [8,11), G4 = [11,14),
  C5 = [14,20), and exactly 20 seconds of audio.

This new scene has its own output basename and preserves both the
original 19-second experiment and the 79-second Zarathustra v3 video.

Commands for Windows (working branch feature/M3-semantic-notes):

    cd D:\Proyectos\musnim
    git pull --ff-only origin feature/M3-semantic-notes
    .\.venv\Scripts\python.exe -m manim -ql projects/ZAR-001/scenes/semantic_notes_sustain_demo.py SemanticNotesSustainDemo
    .\.venv\Scripts\python.exe .\scripts\qa_sustained_notes_video.py

Expected video path:

    media/videos/semantic_notes_sustain_demo/480p15/SemanticNotesSustainDemo.mp4

Evaluate frames during full note durations, especially 9.5 s,
12.5 s, and 18.0 s, when notes are still sounding, and the
boundaries at 11, 14 and 20 s. Only an actual MP4 review can
complete the visual acceptance gate for this new design.
