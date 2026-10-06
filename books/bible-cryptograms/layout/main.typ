#import "book.typ": *

#let D = json("/build/book/data.json")
#let R = D.release

#show: setup

// Draft watermark while data/release.json is incomplete.
#set page(background: if R.draft {
  rotate(-35deg, text(size: 64pt, fill: luma(88%), weight: "bold")[DRAFT · NOT FOR SALE])
})

// ================= FRONT MATTER =================
#set page(header: none, footer: none)

// Title page
#v(1.6in)
#align(center, text(font: display, size: 26pt, weight: "semibold", tracking: 4pt, fill: soft)[LARGE PRINT])
#v(0.05in)
#align(center, text(font: display, size: 60pt, weight: "bold")[Bible \ Cryptograms])
#v(0.2in)
#rule-ornament(width: 3.2in)
#v(0.25in)
#align(center, text(font: serif, size: 20pt)[#D.subtitle])
#v(0.2in)
#align(center, text(font: serif, size: 17pt, fill: soft)[Volume 1 · King James Version])
#v(1fr)
#align(center, text(font: serif, size: 20pt)[#D.author])
#v(0.5in)
#pagebreak()

// Copyright page
#include "/content/copyright.typ"
#pagebreak()

#include "/content/gift.typ"
#pagebreak()

// Contents
#set page(footer: plain-footer)
#chapter-title("Contents")
#include "/content/contents.typ"
#pagebreak()

#include "/content/front.typ"

// ================= PUZZLES =================
#for (ti, t) in D.themes.enumerate() {
  pagebreak()
  set page(header: none, footer: none)
  theme-opener(num: ti + 1, name: t.name, intro: t.intro, first: t.first, last: t.last)
  [#metadata(t.name) #label("part-" + str(ti + 1))]
  set page(header: context {
    set text(size: 16pt, fill: soft)
    if calc.even(here().page()) [#t.name #h(1fr)] else [#h(1fr) #t.name]
  }, footer: plain-footer)
  for p in D.puzzles.filter(p => p.theme == t.name) {
    let ws = p.words.map(w => word(..w.map(c => if c.at(2) { cell(c.at(0), c.at(1)) } else { pcell(c.at(0)) })))
    let n = p.given_list.len()
    let note = if n == 0 [No letters given: this one is all yours.] else if n == 1 [One letter is already filled in for you.] else [#n letters are already filled in for you.]
    pagebreak()
    [#metadata(p.num) #label("puzzle-" + str(p.num))]
    puzzle(num: p.num, level: p.level, level-name: p.level_name, words: ws, counts: p.counts, given: p.given, given-note: note,
      hint-label: label("hint-" + str(p.num)), sol-label: label("sol-" + str(p.num)))
  }
}

// ================= HINTS & SOLUTIONS =================
#pagebreak()
#set page(header: none, footer: plain-footer)
#include "/content/hints.typ"

#pagebreak()
#include "/content/solutions.typ"

#include "/content/back.typ"
