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
