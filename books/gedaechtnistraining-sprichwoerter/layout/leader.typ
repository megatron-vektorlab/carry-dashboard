// The back of every worksheet: notes for the group leader, solutions, hints, prompts.
#import "book.typ": *

#let lead-section(t) = block(sticky: true, above: 1.1em, below: 0.5em, text(font: serif, size: 19pt, weight: "bold", t))

#let sol-line(x) = {
  [#x.before#strong(x.word)#x.after]
  if x.at("variants", default: ()).len() > 0 [ (auch: #x.variants.join(" / "))]
}

#let render-leader(L) = {
  set text(size: 17pt)
  set par(leading: 0.6em, spacing: 0.7em)
  block(width: 100%, stroke: (bottom: 1.5pt + ink), inset: (bottom: 6pt),
    grid(columns: (1fr, auto), align: (left + bottom, right + bottom),
      text(font: serif, size: 21pt, weight: "bold")[Für die Gruppenleitung],
      [Blatt #L.num #h(4pt) #level-mark(L.level)]))
  v(0.3em)
  [*#L.title* · #L.chapter · etwa #L.minutes Minuten \ Übt: #L.trains]
  lead-section[So geht’s]
  enum(..L.steps, spacing: 0.5em)
  lead-section[Lösungen]
  if L.solution.len() > 0 {
    enum(..L.solution.map(sol-line), spacing: 0.45em)
  }
  if L.at("hints", default: ()).len() > 0 {
    lead-section[Hilfen, wenn ein Wort nicht einfällt]
    [#L.hints.enumerate().map(((i, h)) => [#(i + 1). #h]).join([ · ])]
  }
  lead-section[Zum Gespräch]
  list(..L.prompts, spacing: 0.5em)
  if L.at("easier", default: "") != "" or L.at("harder", default: "") != "" {
    lead-section[Leichter oder anspruchsvoller]
    if L.easier != "" [*Leichter:* #L.easier \ ]
    if L.harder != "" [*Anspruchsvoller:* #L.harder]
  }
  if L.at("note", default: "") != "" {
    v(0.6em)
    block(width: 100%, stroke: 1pt + ink, inset: 7pt, radius: 3pt)[*Achtsam:* #L.note]
  }
}
