\version "2.26.0"
\pointAndClickOff
\header {
  title = "Also sprach Zarathustra — Naturmotiv"
  subtitle = "Reducción didáctica de alturas (ritmo esquemático)"
  composer = "Richard Strauss (1896)"
  tagline = ##f
}
\paper {
  #(set-paper-size "a5landscape")
  indent = 0\mm
  ragged-right = ##t
  system-system-spacing.basic-distance = #15
}
\score {
  \new Staff \with { instrumentName = "Motivo Do–Sol–Do" } {
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
