// Large Print Bible Cryptograms: page styles and building blocks.
// bc/book.py writes build/book/main.typ, which imports this file and fills in the data.

#let ink = luma(0%)
#let soft = luma(0%)       // all reading text is solid black (low-vision guidance: no grey text)
#let rule-grey = luma(55%) // hairlines only
#let faint = luma(75%)
#let paper-tint = luma(92%)

#let serif = "Libre Baskerville"
#let display = "Cormorant Garamond"
#let sans = "Atkinson Hyperlegible Next"

// Every word a reader reads is at least 16 pt (KDP large print).
#let body-size = 17pt
#let cipher-size = 21pt
#let answer-size = 21pt

// Letter cell geometry
#let cw = 0.31in         // width of one letter cell   (bc/layout.py must match)
#let pw = 0.15in         // width of a punctuation cell
#let ah = 0.37in         // height of the write-in space
#let ch = 0.28in         // height of the code letter
#let gap-word = 0.20in   // space between words
#let line-gap = 0.12in   // between one line of code letters and the next write-in line

#let setup(body) = {
  set document(title: "Large Print Bible Cryptograms", author: "Ivan Sikuten")
  set page(width: 8.5in, height: 11in,
    margin: (inside: 0.9in, outside: 0.45in, top: 0.72in, bottom: 0.7in),
    header-ascent: 0.16in, footer-descent: 0.18in)
  set text(font: sans, size: body-size, fill: ink, lang: "en", hyphenate: false)
  set par(leading: 0.62em, spacing: 0.95em, justify: false)
  set strong(delta: 300)
  // Atkinson draws a slashed zero, which a blind tester read as the letter O next to the
  // code key's O column; numbers use Source Sans 3 (plain zero, narrow lining figures).
  show regex("[0-9]+"): it => context {
    let f = text.font
    let first = if type(f) == array { f.first() } else { f }
    let name = if type(first) == str { first } else { first.name }
    if lower(name) == lower(sans) { text(font: "Source Sans 3", it) } else { it }
  }
  body
}

// ---------- ornaments (drawn, no images) ----------
#let cross-mark(size: 10pt, color: ink) = box(width: size * 0.7, height: size, {
  place(dx: size * 0.28, dy: 0pt, rect(width: size * 0.14, height: size, fill: color, stroke: none))
  place(dx: 0pt, dy: size * 0.26, rect(width: size * 0.7, height: size * 0.14, fill: color, stroke: none))
})

#let rule-ornament(width: 2.6in) = align(center, box(width: width, {
  grid(columns: (1fr, auto, 1fr), column-gutter: 8pt, align: horizon,
    line(length: 100%, stroke: 0.9pt + soft),
    cross-mark(size: 12pt, color: soft),
    line(length: 100%, stroke: 0.9pt + soft))
}))

#let star(filled, size: 15pt) = {
  let pts = range(10).map(i => {
    let r = if calc.even(i) { size / 2 } else { size * 0.21 }
    let a = -90deg + i * 36deg
    (size / 2 + r * calc.cos(a), size / 2 + r * calc.sin(a))
  })
  box(width: size, height: size, baseline: 15%,
    polygon(fill: if filled { ink } else { none }, stroke: 1pt + ink, ..pts))
}

#let stars(level, total: 4) = box(range(total).map(i => star(i < level)).join(h(3pt)))

// ---------- page furniture ----------
#let running(theme-name) = {
  set page(header: context {
    let p = here().page()
    set text(size: 16pt, fill: soft)
    if calc.even(p) [#theme-name #h(1fr)] else [#h(1fr) #theme-name]
  }, footer: context {
    set text(size: 16pt, fill: soft)
    let n = counter(page).display()
    if calc.even(here().page()) [#n #h(1fr)] else [#h(1fr) #n]
  })
}

#let plain-footer = context {
  set text(size: 16pt, fill: soft)
  let n = counter(page).display()
  if calc.even(here().page()) [#n #h(1fr)] else [#h(1fr) #n]
}

// ---------- the puzzle ----------
#let cell(c, g) = box(width: cw, stack(dir: ttb, spacing: 0.03in,
  box(width: cw - 7pt, height: ah, stroke: (bottom: 1.3pt + ink),
    align(center + bottom, pad(bottom: 3pt, text(size: answer-size, weight: "bold", g)))),
  box(width: cw, height: ch, align(center + horizon, text(size: cipher-size, c)))
))

// A cell whose letter was just found (worked example): the write-in space is boxed.
#let cell-new(c, g) = box(width: cw, stack(dir: ttb, spacing: 0.03in,
  box(width: cw - 4pt, height: ah, stroke: 1.6pt + ink, radius: 2pt,
    align(center + bottom, pad(bottom: 3pt, text(size: answer-size, weight: "bold", g)))),
  box(width: cw, height: ch, align(center + horizon, text(size: cipher-size, weight: "bold", c)))
))

// Punctuation is printed only in the code line: on the write-in line a comma would sit
// at the top of an empty space and look like an apostrophe (blind-test finding).
#let pcell(c) = box(width: pw, stack(dir: ttb, spacing: 0.03in,
  box(height: ah),
  box(height: ch, align(center + horizon, text(size: cipher-size, weight: "bold", if c == "'" { "\u{2019}" } else { c })))
))

#let word(..cells) = box(cells.pos().join())

#let cipher-block(words) = par(leading: line-gap, justify: false, words.join(h(gap-word, weak: true)))

// The code key: every code letter, how often it appears, and a space to write its real letter.
// wide: two bands (A-M, N-Z) with columns twice as wide, used whenever the page has room.
#let key-band(letters, counts, given) = {
  let sep = 0.9pt + rule-grey      // visible column rules keep two-digit counts apart
  let n = letters.len()
  let wide = n <= 13
  // The two-band key has row labels and roomy rows; the one-row key (long verses) gives the
  // label column's width to the 26 letter columns instead, so two-digit counts have room.
  let (hc, hu, hr) = if wide { (0.29in, 0.27in, 0.40in) } else { (0.27in, 0.25in, 0.36in) }
  let lab(t, h, bold: true) = if wide { (box(height: h, inset: (right: 5pt), align(right + horizon, text(size: 16pt, weight: if bold { "bold" } else { "regular" }, t))),) } else { () }
  grid(columns: (if wide { (auto,) } else { () }) + (1fr,) * n, row-gutter: 0pt,
    ..lab([Code], hc),
    ..letters.map(l => box(width: 100%, height: hc, stroke: (top: 1pt + ink, left: sep, right: sep),
      align(center + horizon, text(size: if wide { 18pt } else { 16pt }, weight: "bold", l)))),
    ..lab([Used], hu, bold: false),
    ..letters.map(l => box(width: 100%, height: hu, stroke: (left: sep, right: sep),
      align(center + horizon, text(size: 16pt, tracking: if wide { 0pt } else { -0.5pt },
        if counts.at(l, default: 0) > 0 { str(counts.at(l)) } else { "–" })))),
    ..lab([Real], hr),
    ..letters.map(l => box(width: 100%, height: hr, stroke: (bottom: 1pt + ink, top: 0.6pt + faint, left: sep, right: sep),
      align(center + horizon, text(size: 20pt, weight: "bold", given.at(l, default: ""))))),
  )
}

#let key-table(counts, given, wide: false) = {
  let letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".clusters()
  block(width: 100%, breakable: false, if wide {
    key-band(letters.slice(0, 13), counts, given)
    v(0.12in)
    key-band(letters.slice(13), counts, given)
  } else {
    key-band(letters, counts, given)
  })
}

// Ruled notes area filling the rest of the page.
#let notes-area() = block(width: 100%, height: 1fr, breakable: false, clip: true, layout(size => {
  let gap = 0.45in
  let n = calc.floor((size.height - 0.45in) / gap)
  if n >= 2 {
    text(size: 16pt, weight: "bold")[Notes]
    for i in range(n) { v(gap - 1pt, weak: false); line(length: 100%, stroke: 1pt + rule-grey) }
  }
}))

// Writing lines filling the rest of the page (never spills onto the next page).
#let ruled-lines(gap: 0.48in) = block(width: 100%, height: 1fr, breakable: false, clip: true, layout(size => {
  let n = calc.floor((size.height - 0.1in) / gap)
  for i in range(n) { v(gap - 1pt, weak: false); line(length: 100%, stroke: 1pt + rule-grey) }
}))

// One puzzle per page.
#let puzzle(num: 0, level: 1, level-name: "", words: (), counts: (:), given: (:), given-note: "",
            hint-label: none, hint2-label: none, hint3-label: none, sol-label: none, wide-key: false) = {
  let pg(l) = context counter(page).at(l).first()
  block(width: 100%, stroke: (top: 1.6pt + ink, bottom: 0.8pt + ink), inset: (x: 0pt, y: 5pt),
    grid(columns: (auto, auto, 1fr), column-gutter: 12pt, align: (left + horizon, left + horizon, right + horizon),
      text(font: serif, size: 22pt, weight: "bold")[Puzzle #num],
      [#stars(level) #h(4pt) #text(size: 16pt)[#level-name]],
      text(size: 16pt)[Answer p. #pg(sol-label)]))
  v(2pt)
  block(width: 100%, text(size: 16pt)[#given-note #h(1fr) Hints p. #pg(hint-label) · #pg(hint2-label) · #pg(hint3-label)])
  v(0.10in)
  cipher-block(words)
  v(0.22in)
  key-table(counts, given, wide: wide-key)
  v(0.25in)
  notes-area()
}

// ---------- theme opener ----------
#let theme-opener(num: 1, name: "", intro: [], verses: "", first: 0, last: 0) = {
  v(1.3in)
  align(center, text(font: display, size: 22pt, weight: "semibold", fill: soft, tracking: 3pt, upper("Part " + ("One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine").at(num - 1))))
  v(0.1in)
  align(center, text(font: display, size: 46pt, weight: "bold", name))
  v(0.15in)
  rule-ornament()
  v(0.35in)
  align(center, block(width: 5.6in, align(left, text(size: 17pt, intro))))
  v(0.3in)
  align(center, text(size: 16pt, fill: soft)[Puzzles #first–#last])
}

// ---------- headings for front/back matter ----------
#let chapter-title(t, sub: none) = {
  v(0.35in)
  text(font: serif, size: 30pt, weight: "bold", t)
  if sub != none { v(-0.05in); text(size: 17pt, fill: soft, sub) }
  v(0.05in)
  line(length: 100%, stroke: 1pt + soft)
  v(0.15in)
}

#let section(t) = block(sticky: true, above: 0.9em, below: 0.55em, text(font: serif, size: 20pt, weight: "bold", t))

// ---------- worked example ----------
#let example-state(E, state) = {
  let ws = E.cipher.split(" ").filter(w => w != "").map(w => word(..w.clusters().map(c => {
    if c.match(regex("[A-Z]")) != none {
      let g = state.known.at(c, default: "")
      if c in state.new { cell-new(c, g) } else { cell(c, g) }
    } else { pcell(c) }
  })))
  block(breakable: false, inset: (y: 4pt), cipher-block(ws))
}
