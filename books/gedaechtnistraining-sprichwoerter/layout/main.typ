#import "book.typ": *
#import "sheet.typ": *
#import "leader.typ": *

#let D = json("/build/book/data.json")
#let R = D.release

#show: setup

#set page(background: if R.draft {
  rotate(-35deg, text(size: 60pt, fill: luma(85%), weight: "bold")[ENTWURF · NICHT ZUM VERKAUF])
})

// ================= TITLE =================
#set page(footer: none)
#v(30mm)
#align(center, text(size: 20pt, tracking: 2pt)[GEDÄCHTNISTRAINING IN GROSSDRUCK])
#v(10mm)
#align(center, text(font: serif, size: 40pt, weight: "bold")[Sprichwörter \ und Redewendungen \ für Senioren])
#v(8mm)
#align(center, line(length: 60mm, stroke: 1.5pt + ink))
#v(8mm)
#align(center, text(size: 20pt)[100 Kopiervorlagen in A4 \ mit Lösungen und Gesprächsimpulsen])
#v(6mm)
#align(center, text(size: 18pt)[für Betreuung, Pflegeheim und Tagespflege])
#v(1fr)
#align(center, text(size: 18pt)[Band #D.volume])
#v(4mm)
#align(center, text(size: 20pt)[#D.author])
#v(15mm)
#pagebreak()

#include "/content/impressum.typ"
#pagebreak()

// ================= CONTENTS =================
#set page(footer: plain-footer)
#chapter-title("Inhalt")
#{
  let entry(t, l) = grid(columns: (1fr, auto), column-gutter: 4mm, t, context counter(page).at(l).first())
  set par(spacing: 0.75em)
  entry([Willkommen!], <welcome>)
  entry([Hinweise für die Gruppenleitung], <leitung>)
  entry([So kann eine Stunde aussehen], <stunde>)
  entry([Die Blätter nach Stufe und Aufgabe], <overview>)
  v(0.5em)
  for c in D.chapters {
    entry([*Kapitel #c.num: #c.name* #h(3mm) Blatt #c.sheets.first().num–#c.sheets.last().num], label("chapter-" + str(c.num)))
  }
  v(0.5em)
  entry([Alle Sprichwörter und Redewendungen von A bis Z], <index>)
}
#pagebreak()

#[#metadata("welcome") <welcome>]
#include "/content/welcome.typ"
#pagebreak()
#[#metadata("leitung") <leitung>]
#include "/content/leitung.typ"
#pagebreak()
#[#metadata("stunde") <stunde>]
#include "/content/stunde.typ"
#pagebreak()

// Overview by level and by exercise type
#[#metadata("overview") <overview>]
#chapter-title("Die Blätter nach Stufe und Aufgabe")
#section[Nach Stufe]
#for lv in ("1", "2", "3") {
  block(below: 0.8em, grid(columns: (22mm, 1fr), level-mark(int(lv)), D.by_level.at(lv).map(str).join(", ")))
}
#section[Nach Aufgabe]
#for t in D.by_type {
  block(below: 0.6em, [*#t.name:* #t.nums.map(str).join(", ")])
}

// A left-hand page before chapter 1 would otherwise stay blank: a page for favourite sayings.
#pagebreak()
#context if calc.even(here().page()) {
  chapter-title("Meine Lieblingssprichwörter")
  [Welche Sprichwörter und Redewendungen haben Sie früher oft gehört, vielleicht von den Eltern, in der Schule oder bei der Arbeit? Schreiben Sie sie hier auf oder lassen Sie sie sich aufschreiben.]
  ruled-lines(gap: 15mm)
}

// ================= CHAPTERS =================
#for c in D.chapters {
  pagebreak(to: "odd")
  set page(footer: plain-footer)
  [#metadata(c.name) #label("chapter-" + str(c.num))]
  v(6mm)
  text(size: 20pt, tracking: 2pt)[KAPITEL #c.num]
  v(1mm)
  text(font: serif, size: 36pt, weight: "bold", c.name)
  v(1mm)
  line(length: 100%, stroke: 1.5pt + ink)
  v(3mm)
  text(size: 19pt, c.intro)
  v(4mm)
  section[Zum Aufwärmen: Ich sage den Anfang, Sie das Ende]
  text(size: small)[Lesen Sie den Anfang vor und lassen Sie die Gruppe ergänzen. Das Ende steht fett gedruckt.]
  v(2mm)
  grid(columns: (1fr, 1fr), row-gutter: 0.75em, column-gutter: 6mm,
    ..c.warmup.map(w => (text(size: 18pt, w.a), text(size: 18pt, weight: "bold", w.b))).flatten())
  pagebreak()
  // verso: around the theme
  section[Rund um das Thema: Zum Erzählen]
  list(..c.talk, spacing: 0.6em)
  section[In Bewegung]
  list(..c.move, spacing: 0.6em)
  section[Zum Mitbringen]
  list(..c.props, spacing: 0.6em)
  section[Die Blätter in diesem Kapitel]
  grid(columns: (26mm, 1fr, auto), row-gutter: 0.55em,
    ..c.sheets.map(s => ([Blatt #s.num], s.title, level-mark(s.level))).flatten())

  for u in D.units.filter(u => u.sheet.chapter == c.name) {
    let s = u.sheet
    pagebreak(to: "odd")
    set page(footer: sheet-footer(s.num, s.level, D.author, D.year))
    render-sheet(s)
    pagebreak()
    set page(footer: plain-footer)
    render-leader(u.leader)
  }
}

// ================= INDEX =================
#pagebreak(to: "odd")
#set page(footer: plain-footer)
#[#metadata("index") <index>]
#chapter-title("Alle Sprichwörter und Redewendungen von A bis Z", sub: "mit den Nummern der Blätter")
#columns(2, gutter: 8mm, {
  set par(leading: 0.45em, spacing: 0.55em, hanging-indent: 4mm)
  for e in D.index [#e.w #h(2mm) #text(weight: "bold", e.sheets.map(str).join(", ")) \ ]
})
#if D.pad_page {
  pagebreak()
  chapter-title("Notizen")
  ruled-lines()
}
