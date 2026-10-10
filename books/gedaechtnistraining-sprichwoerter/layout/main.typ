#import "book.typ": *
#import "sheet.typ": *
#import "leader.typ": *
#import "extras.typ": *

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
  entry([Mein Sprichwort: ein Blatt zum Erzählen], <mein>)
  entry([Sprichwort-Bingo mit 12 Karten], <bingo>)
  entry([Raterunden für zwischendurch], <rounds>)
  entry([Welche Blätter haben wir schon gemacht?], <checklist>)
  entry([Alle Sprichwörter und Redewendungen von A bis Z, mit Bedeutung], <index>)
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
  block(below: 0.55em, grid(columns: (22mm, 1fr), level-mark(int(lv)), D.by_level.at(lv).map(str).join(", ")))
}
#section[Nach Aufgabe]
#grid(columns: (66mm, 1fr), row-gutter: 0.5em, column-gutter: 3mm,
  ..D.by_type.map(t => (strong(t.name),
    t.levels.map(l => [#level-mark(l.level)#h(1.5mm)#l.nums.map(str).join(", ")]).join(h(4mm)))).flatten())

// A left-hand page before chapter 1 would otherwise stay blank.
#[#metadata("overview-end") <overview-end>]
#context if calc.odd(locate(<overview-end>).page()) {
  pagebreak()
  chapter-title("Notizen")
  ruled-lines()
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

// ================= EXTRAS =================
#pagebreak(to: "odd")
#set page(footer: extra-footer([Mein Sprichwort], D.author, D.year))
#[#metadata("mein") <mein>]
#mein-sprichwort()
#pagebreak()
#set page(footer: plain-footer)
#mein-sprichwort-leader()

#pagebreak(to: "odd")
#[#metadata("bingo") <bingo>]
#bingo-rules(D.bingo)
#pagebreak()
#bingo-calls(D.bingo)
#pagebreak()
#set page(footer: extra-footer([Sprichwort-Bingo], D.author, D.year))
#bingo-cards(D.bingo)

#pagebreak()
#set page(footer: plain-footer)
#[#metadata("rounds") <rounds>]
#rounds(D.rounds)

#pagebreak()
#set page(footer: extra-footer([Blatt-Übersicht], D.author, D.year))
#[#metadata("checklist") <checklist>]
#checklist(D)

// ================= INDEX =================
#pagebreak(to: "odd")
#set page(footer: plain-footer)
#[#metadata("index") <index>]
#chapter-title("Alle Sprichwörter und Redewendungen von A bis Z",
  sub: "mit ihrer Bedeutung und den Nummern der Blätter. In Klammern: Dort steht es nur zur Auswahl. Geordnet nach dem ersten wichtigen Wort; der, die, das, den, dem, ein, eine, einen, jemandem, jemanden, etwas und sich am Anfang zählen nicht.")
#columns(2, gutter: 7mm, {
  set par(leading: 0.42em)
  for e in D.index {
    let where = ()
    if e.sheets.len() > 0 { where.push(e.sheets.map(str).join(",\u{a0}")) }
    if e.also.len() > 0 { where.push("(" + e.also.map(str).join(",\u{a0}") + ")") }
    if e.chapters.len() > 0 { where.push("Aufwärmen\u{a0}Kapitel\u{a0}" + e.chapters.map(str).join(",\u{a0}")) }
    if e.extra.len() > 0 { where.push(e.extra.map(x => x.replace(" ", "\u{a0}")).join(", ")) }
    block(breakable: false, above: 0pt, below: 0.6em,
      par(hanging-indent: 4mm)[*#e.w* #h(1mm) #where.join(" · ") – #e.m])
  }
})
#if D.pad_page {
  pagebreak()
  chapter-title("Notizen")
  ruled-lines()
}
