// The back of every worksheet: notes for the group leader, solutions, hints, prompts.
#import "book.typ": *

#let lead-section(t) = block(sticky: true, above: 0.95em, below: 0.45em, text(font: serif, size: 18pt, weight: "bold", t))

// A solution line; accepted variants go before the closing full stop:
// "Wo gehobelt wird, da fallen Späne (auch: Wo gehobelt wird, fallen Späne)."
#let sol-line(x) = {
  let v = x.at("variants", default: ())
  let after = x.after
  let end = ""
  if v.len() > 0 and after.len() > 0 and after.last() in (".", "!", "?") {
    end = after.last()
    after = after.slice(0, after.len() - 1)
  }
  [#x.before#strong(x.word)#after]
  if v.len() > 0 [ (auch: #v.join(" / "))#end]
}

#let render-leader(L) = {
  set text(size: 16pt)
  set par(leading: 0.55em, spacing: 0.65em)
  block(width: 100%, stroke: (bottom: 1.5pt + ink), inset: (bottom: 12pt),
    grid(columns: (1fr, auto), align: (left + bottom, right + bottom),
      text(font: serif, size: 21pt, weight: "bold")[Für die Gruppenleitung],
      [Blatt #L.num #h(4pt) #level-mark(L.level)]))
  v(0.3em)
  // title, chapter and time on one line if they fit, otherwise the time on a line of its own
  layout(size => {
    let first = [*#L.title* · #L.chapter · etwa #L.minutes Minuten]
    if measure(first).width <= size.width [#first \ Übt: #L.trains]
    else [*#L.title* · #L.chapter \ etwa #L.minutes Minuten · Übt: #L.trains]
  })
  lead-section[So geht’s]
  enum(..L.steps, spacing: 0.5em)
  lead-section(if L.solution.len() == 1 [Lösung] else [Lösungen])
  if L.solution.len() == 1 { sol-line(L.solution.at(0)) }
  else if L.solution.len() > 1 and L.at("sol_cols", default: 1) == 2 {
    // short solutions (word search): two columns
    grid(columns: (1fr, 1fr), column-gutter: 6mm, row-gutter: 0.45em,
      ..L.solution.enumerate().map(((i, x)) => [#(i + 1). #sol-line(x)]))
  }
  else if L.solution.len() > 1 { enum(..L.solution.map(sol-line), spacing: 0.45em) }
  let hints = L.at("hints", default: ())
  if hints.len() > 0 {
    lead-section(L.at("hints_title", default: "Hilfen, wenn ein Wort nicht einfällt"))
    if L.at("hints_intro", default: "") != "" [#L.hints_intro \ ]
    if L.at("hints_plain", default: false) { hints.join(linebreak()) }
    else if hints.len() == 1 { hints.at(0) }
    // a number never stands apart from its hint, and no line starts with the dot
    else [#hints.enumerate().map(((i, h)) => [#(i + 1).~#h]).join([~· ])]
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
