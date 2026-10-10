// Gedächtnistraining Sprichwörter: page styles and worksheet building blocks.
// Data: build/book/data.json (gt/book.py). All reading text is at least 16 pt (KDP large print).

#let ink = luma(0%)
#let rule-grey = luma(45%)
#let faint = luma(80%)

#let serif = "Libre Baskerville"
#let sans = "Atkinson Hyperlegible Next"
#let digits = "Source Sans 3"

#let body-size = 18pt
#let ex-size = 20pt        // exercise text
#let small = 16pt          // the smallest size in the book

#let setup(body) = {
  set document(title: "Gedächtnistraining für Senioren in Großdruck: Sprichwörter & Redensarten", author: "Ivan Sikuten")
  set page(paper: "a4",
    margin: (inside: 22mm, outside: 15mm, top: 15mm, bottom: 19mm),
    header-ascent: 4mm, footer-descent: 4mm)
  set text(font: sans, size: body-size, fill: ink, lang: "de", hyphenate: false)
  set par(leading: 0.6em, spacing: 0.9em, justify: false)
  set strong(delta: 300)
  // Atkinson draws a slashed zero; numbers use Source Sans 3 (plain zero).
  show regex("[0-9]+"): it => context {
    let f = text.font
    let first = if type(f) == array { f.first() } else { f }
    let name = if type(first) == str { first } else { first.name }
    if lower(name) == lower(sans) { text(font: digits, it) } else { it }
  }
  body
}

#let plain-footer = context {
  set text(size: small)
  let n = counter(page).display()
  if calc.even(here().page()) [#n #h(1fr)] else [#h(1fr) #n]
}

// ---------- level marker: one to three diamonds (a neutral symbol, no "easy"/"hard") ----------
#let diamond(size: 11pt) = box(width: size, height: size, baseline: 10%,
  polygon(fill: ink, stroke: none, (size / 2, 0pt), (size, size / 2), (size / 2, size), (0pt, size / 2)))
#let level-mark(level) = box(range(level).map(i => diamond()).join(h(2pt)))

// ---------- headings ----------
#let chapter-title(t, sub: none) = {
  v(4mm)
  text(font: serif, size: 28pt, weight: "bold", t)
  if sub != none { v(-1mm); text(size: body-size, sub) }
  v(1mm)
  line(length: 100%, stroke: 1pt + ink)
  v(3mm)
}
#let section(t) = block(sticky: true, above: 1em, below: 0.5em, text(font: serif, size: 21pt, weight: "bold", t))

// ---------- worksheet frame ----------
#let sheet-head(num: 0, title: "", level: 1, chapter: "") = {
  block(width: 100%, stroke: (bottom: 1.5pt + ink), inset: (x: 0pt, top: 0pt, bottom: 6pt),
    grid(columns: (1fr, auto), column-gutter: 10pt, align: (left + bottom, right + bottom),
      text(font: serif, size: 26pt, weight: "bold", title),
      text(size: small, chapter)))
}

// Footer of a Kopiervorlage: copyright, sheet number, level symbol.
#let sheet-footer(num, level, holder, year) = context {
  set text(size: small)
  let n = counter(page).display()
  let left = [© #year #holder · Kopiervorlage]
  let right = [Blatt #num #h(6pt) #level-mark(level)]
  if calc.even(here().page()) [#n #h(8mm) #left #h(1fr) #right] else [#left #h(1fr) #right #h(8mm) #n]
}

#let example-box(body) = block(width: 100%, stroke: (paint: ink, thickness: 1.2pt, dash: "dashed"), radius: 4pt,
  inset: (x: 10pt, y: 8pt), above: 0.2em, below: 0.9em, breakable: false,
  grid(columns: (auto, 1fr), column-gutter: 10pt, align: (left + top, left + top),
    text(size: small, weight: "bold")[Beispiel:], body))
#let answer(t) = text(weight: "bold", t)

#let task(body) = block(width: 100%, above: 0.7em, below: 0.9em, text(size: 19pt, weight: "bold", body))

// A box of words to choose from.
#let word-bank(words, title: "Diese Wörter fehlen:") = block(width: 100%, stroke: 1.4pt + ink, radius: 4pt, inset: (x: 10pt, y: 8pt), below: 1em, {
  text(size: small, weight: "bold", title)
  v(-0.3em)
  set par(leading: 0.9em)
  text(size: ex-size, words.join(h(1fr, weak: false) + "  " ))
})

#let bank-grid(words, cols: 4, title: "Diese Wörter fehlen:") = block(width: 100%, stroke: 1.4pt + ink, radius: 4pt, inset: (x: 10pt, y: 8pt), below: 1em, breakable: false, {
  text(size: small, weight: "bold", title)
  v(0.1em)
  grid(columns: (1fr,) * cols, row-gutter: 0.55em, ..words.map(w => text(size: ex-size, w)))
})

// A line to write on, filling the rest of the row.
#let wline(width: 1fr) = box(width: width, height: 0.9em, baseline: 0.2em, stroke: (bottom: 1.1pt + ink))
#let full-line(gap: 13mm) = block(width: 100%, height: gap, above: 0pt, below: 0pt, align(bottom, line(length: 100%, stroke: 1.1pt + ink)))

// Numbered item: number in a fixed column.
#let item(n, body) = grid(columns: (11mm, 1fr), align: (left + top, left + top), text(size: ex-size, weight: "bold")[#n.], body)

// Writing lines filling the rest of the page (never spills onto the next page).
#let ruled-lines(gap: 13mm) = block(width: 100%, height: 1fr, breakable: false, clip: true, layout(size => {
  let n = calc.floor((size.height - 2mm) / gap)
  for i in range(n) { v(gap - 1pt, weak: false); line(length: 100%, stroke: 1pt + rule-grey) }
}))

// The worksheet being set (for overflow reports).
#let current-sheet = state("current-sheet", 0)

// Items spread evenly over the rest of the page (never onto the next one). If they do not
// fit, a metadata mark <overflow> with the sheet number is left for gt/book.py to find.
#let spread(blocks) = block(width: 100%, height: 1fr, breakable: false, layout(size => {
  let total = blocks.map(b => measure(block(width: size.width, b)).height).sum(default: 0pt)
  if total > size.height { context [#metadata(current-sheet.get()) <overflow>] }
  for b in blocks { b; v(1fr) }
}))

// ---------- pieces ----------
#let gap-line(n: 8) = box(width: n * 0.62em + 0.5em, height: 0.9em, baseline: 0.2em, stroke: (bottom: 1.1pt + ink))
// One box per letter; the first letter may be printed in its box.
#let letter-boxes(n, first: "") = box(baseline: 0.25em, stack(dir: ltr, spacing: 0pt,
  ..range(n).map(i => box(width: 0.8em, height: 1.1em, stroke: 1.1pt + ink,
    align(center + horizon, text(weight: "bold", if i == 0 { first } else { "" }))))))
#let joined(before, mid, after) = {
  let tight = after == "" or after.starts-with(",") or after.starts-with(".") or after.starts-with("!") or after.starts-with("?")
  [#before#if before != "" [ ]#mid#if not tight [ ]#after]
}
#let blanked(it) = {
  let g = if it.at("boxes", default: 0) > 0 { letter-boxes(it.boxes, first: it.at("first", default: "")) } else { gap-line(n: it.at("gap", default: 8)) }
  joined(it.parts.at(0), g, it.parts.at(1))
}
#let filled(parts, word) = joined(parts.at(0), box(stroke: (bottom: 1.1pt + ink), inset: (x: 3pt, bottom: 2pt), answer(word)), parts.at(1))
#let tile(w) = box(stroke: 1.2pt + ink, radius: 3pt, inset: (x: 6pt, y: 5pt), text(size: ex-size, w))
#let tickbox = box(width: 9mm, height: 9mm, baseline: 25%, stroke: 1.4pt + ink, radius: 1.5pt)
#let wordchoice(w) = box(inset: (x: 7pt, y: 4pt), text(size: ex-size, w))
#let circled(w) = box(stroke: 1.6pt + ink, radius: 50%, inset: (x: 7pt, y: 4pt), text(size: ex-size, weight: "bold", w))
#let wline(width: 1fr) = box(width: width, height: 0.9em, baseline: 0.2em, stroke: (bottom: 1.1pt + ink))
#let write-line(lead: none, gap: 15mm) = block(width: 100%, height: gap, above: 0pt, below: 0pt, align(bottom,
  grid(columns: (auto, 1fr), column-gutter: 4pt, align: bottom,
    if lead == none or lead == "" { [] } else { text(size: ex-size, lead) }, line(length: 100%, stroke: 1.1pt + ink))))

// ---------- exercise types (participant page) ----------
#let ex-gaps(s) = {
  if s.example != none { example-box(text(size: ex-size, filled(s.example.parts, s.example.answer))) }
  spread(s.items.enumerate().map(((i, it)) =>
    block(breakable: false, item(i + 1, par(leading: 1.0em, text(size: ex-size, blanked(it)))))))
}

#let ex-circle(s) = {
  let row(it, ans: none) = {
    par(leading: 1.0em, text(size: ex-size, joined(it.parts.at(0), gap-line(n: 6), it.parts.at(1))))
    v(0.15em)
    pad(left: 6mm, it.options.map(o => if ans == o { circled(o) } else { wordchoice(o) }).join(h(14mm)))
  }
  if s.example != none { example-box(row(s.example, ans: s.example.answer)) }
  spread(s.items.enumerate().map(((i, it)) => block(breakable: false, item(i + 1, row(it)))))
}

#let dotm = box(baseline: -20%, circle(radius: 2.2mm, fill: ink))
#let ex-match(s) = {
  let letters = "ABCDEFGHIJ".clusters()
  let cols = if s.at("wide_right", default: false) { (11mm, 0.8fr, 6mm, 24mm, 6mm, 9mm, 1.2fr) } else { (11mm, 1fr, 6mm, 32mm, 6mm, 9mm, 1fr) }
  spread(s.left.enumerate().map(((i, l)) => grid(columns: cols,
    align: (left + horizon, left + horizon, center + horizon, left, center + horizon, left + horizon, left + horizon),
    text(size: ex-size, weight: "bold")[#(i + 1).],
    text(size: ex-size, l), dotm, [], dotm,
    text(size: ex-size, weight: "bold")[#letters.at(i)],
    text(size: ex-size, s.right.at(i)))))
}

#let ex-complete(s) = {
  if s.example != none {
    example-box({ text(size: ex-size, s.example.start); linebreak(); text(size: ex-size, answer(s.example.answer)) })
  }
  spread(s.items.enumerate().map(((i, it)) => block(breakable: false, item(i + 1, {
    text(size: ex-size, it.start)
    write-line(lead: it.at("hint", default: ""))
  }))))
}

#let ex-scramble(s) = {
  if s.example != none {
    example-box({ par(leading: 0.9em, s.example.tiles.map(tile).join(h(7pt))); v(0.2em); text(size: ex-size, answer(s.example.answer)) })
  }
  spread(s.items.enumerate().map(((i, it)) => block(breakable: false, item(i + 1, {
    par(leading: 0.9em, it.tiles.map(tile).join(h(7pt)))
    write-line(lead: it.at("first", default: ""))
  }))))
}

#let ex-wrong(s) = {
  if s.example != none {
    let parts = s.example.shown.split(s.example.wrong)
    example-box({
      text(size: ex-size)[#parts.at(0)#strike(stroke: 2pt, s.example.wrong)#parts.slice(1).join(s.example.wrong)]
      linebreak()
      text(size: small)[Richtig heißt es: ]
      text(size: ex-size, answer(s.example.answer))
    })
  }
  spread(s.items.enumerate().map(((i, it)) => block(breakable: false, item(i + 1, {
    text(size: ex-size, it.shown)
    v(0.3em)
    grid(columns: (auto, 1fr), column-gutter: 6pt, align: bottom, text(size: small)[Richtig heißt es:], box(width: 70mm, wline()))
  }))))
}

#let stub(w) = box([#text(size: ex-size, weight: "bold", w.first)#box(width: (w.len - 1) * 0.55em + 0.2em, height: 0.9em, baseline: 0.2em, stroke: (bottom: 1.1pt + ink))#w.at("punct", default: "")])
#let ex-firstletters(s) = spread(s.items.enumerate().map(((i, it)) =>
  block(breakable: false, item(i + 1, {
    par(leading: 1.1em, it.stubs.map(stub).join(h(0.55em)))
    write-line()
  }))))

#let options-block(opts) = {
  for (k, o) in opts.enumerate() {
    block(above: 0.55em, below: 0pt, grid(columns: (12mm, 8mm, 1fr), align: (left + horizon, left + horizon, left + horizon),
      tickbox, text(size: ex-size, weight: "bold")[#("abc".clusters().at(k)))], text(size: ex-size, o)))
  }
}
#let ex-choice(s) = spread(s.items.enumerate().map(((i, it)) =>
  block(breakable: false, item(i + 1, {
    text(size: ex-size, weight: "bold", it.phrase)
    options-block(it.options)
  }))))

#let ex-situation(s) = spread(s.items.enumerate().map(((i, it)) =>
  block(breakable: false, item(i + 1, {
    text(size: ex-size, it.phrase)
    options-block(it.options)
  }))))

// Word search grid.
#let ws-grid(grid-rows, cell: 15mm, size: 24pt) = {
  let n = grid-rows.len()
  align(center, box(stroke: 1.6pt + ink, grid(columns: (cell,) * n, rows: (cell,) * n, stroke: 0.8pt + rule-grey,
    ..grid-rows.flatten().map(ch => align(center + horizon, text(size: size, weight: "bold", ch))))))
}
#let ex-wordsearch(s) = {
  bank-grid(s.words, cols: 4, title: "Diese Wörter sind versteckt:")
  v(1fr)
  ws-grid(s.grid)
  v(1fr)
}

// Read-aloud story: paragraphs, then the last sentence with a gap and three words to circle.
#let ex-story(s) = {
  set par(leading: 0.95em, spacing: 1.2em)
  for p in s.paragraphs { par(text(size: ex-size, p)) }
  v(0.6em)
  block(width: 100%, stroke: 1.4pt + ink, radius: 4pt, inset: 10pt, breakable: false, {
    par(leading: 1.0em, text(size: ex-size, joined(s.parts.at(0), gap-line(n: 7), s.parts.at(1))))
    v(0.3em)
    align(center, s.options.map(o => wordchoice(o)).join(h(16mm)))
  })
  v(1fr)
}
