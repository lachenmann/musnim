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
