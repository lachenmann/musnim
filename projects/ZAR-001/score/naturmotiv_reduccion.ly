\version "2.26.0"
\pointAndClickOff
% Richard Strauss (1896), Also sprach Zarathustra — reduced pitch motif.
% Video presentation and bibliographic attribution use Manim Text objects.
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
  system-system-spacing.basic-distance = #15
}
\score {
  \new Staff {
    \clef treble
    \time 4/4
    \once \override NoteHead.output-attributes = #'((id . "zar-nature-01") (data-musnim-id . "c-1"))
    c'4
    \once \override NoteHead.output-attributes = #'((id . "zar-nature-02") (data-musnim-id . "g-1"))
    g'4
    \once \override NoteHead.output-attributes = #'((id . "zar-nature-03") (data-musnim-id . "c-2"))
    c''2
    \bar "||"
  }
  \layout { }
}
