\version "2.26.0"
\pointAndClickOff
% Experimental layers for animated engraving in Musnim.
% Do-Sol-Do: schematic pitches and rhythms; not a literal Strauss transcript.
\header {
  title = ##f
  subtitle = ##f
  composer = ##f
  tagline = ##f
}
\paper {
  #(set-paper-size "a5landscape")
  indent = 0\mm
  ragged-right = ##t
}
\score {
  % Grobs at the start of a Staff need their metadata from context creation.
  % A \once override inside the music may arrive after the initial grob.
  \new Staff \with {
    \override StaffSymbol.output-attributes =
      #'((id . "draw-staff") (data-musnim-role . "staff"))
    \override Clef.output-attributes =
      #'((id . "draw-clef") (data-musnim-role . "clef"))
    \override TimeSignature.output-attributes =
      #'((id . "draw-meter") (data-musnim-role . "meter"))
    \override BarLine.output-attributes =
      #'((id . "draw-barline") (data-musnim-role . "barline"))
  } {
    \clef treble
    \time 4/4

    \once \override Stem.output-attributes =
      #'((id . "draw-stem-c4") (data-musnim-role . "stem")
         (data-musnim-owner . "c-1"))
    \once \override NoteHead.output-attributes =
      #'((id . "draw-head-c4") (data-musnim-id . "c-1"))
    c'4

    \once \override Stem.output-attributes =
      #'((id . "draw-stem-g4") (data-musnim-role . "stem")
         (data-musnim-owner . "g-1"))
    \once \override NoteHead.output-attributes =
      #'((id . "draw-head-g4") (data-musnim-id . "g-1"))
    g'4

    \once \override Stem.output-attributes =
      #'((id . "draw-stem-c5") (data-musnim-role . "stem")
         (data-musnim-owner . "c-2"))
    \once \override NoteHead.output-attributes =
      #'((id . "draw-head-c5") (data-musnim-id . "c-2"))
    c''2

    \bar "||"
  }
  \layout { }
}
