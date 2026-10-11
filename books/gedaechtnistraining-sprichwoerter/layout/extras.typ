// The back of the book: a copy page for favourite sayings, Sprichwort-Bingo, read-aloud
// rounds and a checklist of all sheets. Data: build/book/data.json (gt/extras.py).
#import "book.typ": *

// Footer of a copy master that is not one of the 100 numbered sheets.
#let extra-footer(label, holder, year) = context {
  set text(size: small)
  let n = counter(page).display()
  let left = [© #year #holder · Kopiervorlage]
  if calc.even(here().page()) [#n #h(8mm) #left #h(1fr) #label] else [#left #h(1fr) #label #h(8mm) #n]
}

#let leader-head(title) = {
  block(width: 100%, stroke: (bottom: 1.5pt + ink), inset: (bottom: 12pt),
    grid(columns: (1fr, auto), align: (left + bottom, right + bottom),
      text(font: serif, size: 21pt, weight: "bold")[Für die Gruppenleitung], text(size: small, title)))
  v(0.3em)
}

// ---------- Mein Sprichwort ----------
#let prompt-lines(q, n) = block(breakable: false, below: 9mm, {
  text(size: ex-size, weight: "bold", q)
  for i in range(n) { full-line(gap: 15mm) }
})

#let mein-sprichwort() = {
  sheet-head(title: "Mein Sprichwort", chapter: "Zum Erzählen")
  task[Schreiben Sie auf, was Ihnen einfällt, oder erzählen Sie es und lassen Sie es aufschreiben.]
  block(below: 7mm, grid(columns: (auto, 1fr), column-gutter: 4pt, align: bottom,
    text(size: small)[Name (wenn Sie möchten):], line(length: 100%, stroke: 1.1pt + ink)))
  prompt-lines([Dieses Sprichwort habe ich früher oft gehört:], 2)
  prompt-lines([Wer hat es gesagt, und wann?], 2)
  prompt-lines([Ein Sprichwort aus meiner Heimat, gern auch in Mundart:], 2)
  text(size: ex-size, weight: "bold")[Diesen Rat gebe ich gern weiter:]
  ruled-lines(gap: 15mm)
}

#let mein-sprichwort-leader() = {
  set text(size: 16pt)
  set par(leading: 0.55em, spacing: 0.65em)
  leader-head[Mein Sprichwort]
  [*Mein Sprichwort* · Zum Erzählen · #box[etwa 15 bis 20 Minuten] \ Übt: Erinnern, Erzählen, Austausch in der Gruppe]
  let lead-section(t) = block(sticky: true, above: 0.95em, below: 0.45em, text(font: serif, size: 18pt, weight: "bold", t))
  lead-section[So geht’s]
  enum(spacing: 0.5em,
    [Das Blatt passt gut in die erste Stunde zum Kennenlernen, zu einem Besuch zu zweit oder zum Abschluss eines Kapitels.],
    [Lesen Sie die Fragen einzeln vor und lassen Sie Zeit. Wer nicht schreiben möchte, erzählt; Sie, eine Nachbarin oder Angehörige schreiben mit, wenn die Person das möchte.],
    [Fragen Sie nach: „Wie hat man das bei Ihnen zu Hause gesagt?“ Mundart und regionale Formen sind ausdrücklich willkommen.])
  lead-section[Ideen]
  list(spacing: 0.5em,
    [Mit Einverständnis der Teilnehmenden die Blätter zu einem Sprichwort-Buch der Gruppe zusammenheften; wer möchte, bekommt sein Blatt zurück oder eine Kopie.],
    [Jede Woche ein Sprichwort aus der Gruppe als „Spruch der Woche“ aufhängen, wenn die Person einverstanden ist.],
    [Angehörige mitmachen lassen: Welche Sprichwörter kennen die Enkel?])
  lead-section[Zum Gespräch]
  list(spacing: 0.5em,
    [Welches Sprichwort passt gut zu Ihrem Leben?],
    [Von wem haben Sie die meisten Sprichwörter gehört?],
    [Welches Sprichwort würden Sie einem jungen Menschen mitgeben?])
  v(0.6em)
  block(width: 100%, stroke: 1pt + ink, inset: 7pt, radius: 3pt)[*Achtsam:* Erinnerungen an Eltern, Großeltern oder an die Heimat können auch traurig sein, etwa bei Menschen, die flüchten mussten. Lassen Sie Zeit, hören Sie zu und drängen Sie niemanden. Das Blatt gehört der Person, die es ausgefüllt hat.]
}

// ---------- Sprichwort-Bingo ----------
#let bingo-rules(B) = {
  chapter-title("Sprichwort-Bingo", sub: "Ein Spiel für die Gruppe, mit 12 verschiedenen Karten zum Kopieren · etwa 20 bis 30 Minuten")
  section[Was Sie brauchen]
  list(spacing: 0.5em,
    [Für jede Person eine Karte. Auf jeder Seite stehen zwei Karten: kopieren und an der gestrichelten Linie durchschneiden. Gern auf A3 vergrößern.],
    [Einen dicken Stift zum Durchstreichen. Wer lieber abdeckt, nimmt Kärtchen aus Pappe statt Knöpfen oder Spielsteinen, die man verschlucken könnte.],
    [Die Liste mit den Sätzen zum Vorlesen auf der nächsten Seite.])
  section[So wird gespielt]
  enum(spacing: 0.5em,
    [Die Spielleitung liest einen Satz aus der Liste vor und macht an der Lücke eine kleine Pause. Die Gruppe ergänzt das Wort.],
    [Wer das Wort auf seiner Karte hat, streicht es durch. Danach sprechen alle das ganze Sprichwort gemeinsam.],
    [Die Spielleitung hakt den Satz in der Liste ab und wählt den nächsten, in beliebiger Reihenfolge.],
    [Wer drei durchgestrichene Wörter in einer Reihe hat, waagerecht, senkrecht oder schräg, ruft „Bingo!“],
    [Gespielt wird weiter, bis alle eine Reihe haben. So gibt es keine Verlierer.])
  section[Leichter oder anspruchsvoller]
  [*Leichter:* Zu zweit eine Karte; die Spielleitung zeigt beim Suchen auf das Wort. \ *Anspruchsvoller:* Bingo erst bei einer vollen Karte. Oder nach jedem Wort fragen: Wann sagt man das?]
}

#let bingo-calls(B) = {
  set text(size: 16pt)
  leader-head[Sprichwort-Bingo]
  section[Die Sätze zum Vorlesen]
  [Abhaken, was schon vorgelesen wurde. Das fehlende Wort steht fett dahinter.]
  v(0.4em)
  table(columns: (8mm, 1fr, auto), stroke: none, inset: (x: 3pt, y: 4.5pt), align: (left + top, left + top, right + top),
    ..B.calls.map(c => (box(width: 5mm, height: 5mm, baseline: 15%, stroke: 1pt + ink), c.call, strong(c.word))).flatten())
}

#let bingo-card(words, n, holder, year) = block(breakable: false, width: 100%, {
  grid(columns: (1fr, auto), align: (left + bottom, right + bottom),
    text(font: serif, size: 24pt, weight: "bold")[Sprichwort-Bingo], text(size: small)[Karte #n])
  v(2mm)
  grid(columns: (1fr,) * 3, rows: (33mm,) * 3, stroke: 1.6pt + ink,
    ..words.map(w => align(center + horizon, text(size: 26pt, weight: "bold", w))))
  // the upper card keeps its own copyright line when the page is cut; the lower one has the footer
  if calc.odd(n) { v(1.5mm); text(size: small)[© #year #holder · Kopiervorlage] }
})

#let bingo-cards(B, holder, year) = {
  for (k, c) in B.cards.enumerate() {
    if calc.even(k) and k > 0 { pagebreak() }
    bingo-card(c, k + 1, holder, year)
    if calc.even(k) {
      v(1fr)
      line(length: 100%, stroke: (paint: ink, thickness: 1pt, dash: "dashed"))
      v(1fr)
    }
  }
}

// ---------- Raterunden ----------
#let rounds(R) = {
  chapter-title("Raterunden für zwischendurch", sub: "Ich sage den Anfang, Sie das Ende")
  [Ohne Kopien, für fünf Minuten vor dem Essen, im Morgenkreis oder beim Besuch zu zweit. Lesen Sie den Anfang vor und lassen Sie die Gruppe ergänzen. Das Ende steht fett gedruckt. Kennt jemand ein anderes passendes Ende, gilt es natürlich auch.]
  for (k, r) in R.enumerate() {
    block(breakable: false, {
      section[Runde #(k + 1)]
      grid(columns: (1fr, 1fr), row-gutter: 0.6em, column-gutter: 6mm,
        ..r.map(w => (text(size: 18pt, w.a), text(size: 18pt, weight: "bold", w.b))).flatten())
    })
  }
}

// ---------- checklist of all sheets ----------
#let checklist(D) = {
  chapter-title("Welche Blätter haben wir schon gemacht?", sub: "Zum Abhaken: Tragen Sie ein, wann eine Gruppe ein Blatt bearbeitet hat.")
  set text(size: 16pt)
  table(columns: (16mm, 1fr, 20mm, 30mm, 30mm), inset: (x: 4pt, y: 5pt), stroke: 0.75pt + ink,
    align: (center + horizon, left + horizon, left + horizon, left + horizon, left + horizon),
    table.header(strong[Blatt], strong[Aufgabe], strong[Stufe], strong[Gruppe 1], strong[Gruppe 2]),
    ..D.chapters.map(c => (
      table.cell(colspan: 5, fill: none, inset: (x: 4pt, top: 9pt, bottom: 5pt), strong[Kapitel #c.num: #c.name]),
      ..c.sheets.map(s => ([#s.num], s.title, level-mark(s.level), [], [])).flatten(),
    )).flatten())
}
