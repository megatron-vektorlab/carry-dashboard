// KDP paperback full-wrap cover: bleed + back + spine + front + bleed.
// Spine width = pages × 0.002252 in (white paper, B&W interior). Values come from build/cover_params.json.
#let P = json("/build/cover_params.json")
#let bleed = 0.125in
#let trim-w = 6.69in
#let trim-h = 9.61in
#let spine = P.spine_in * 1in
#let W = bleed * 2 + trim-w * 2 + spine
#let H = bleed * 2 + trim-h

#let navy = rgb("#16233b")
#let paper = rgb("#f4f1ea")
#let accent = rgb("#e0a526")
#let de-black = rgb("#1b1b1b")
#let de-red = rgb("#c8102e")
#let de-gold = rgb("#f2c230")

#set page(width: W, height: H, margin: 0pt)
#set text(font: "Source Sans 3", fill: white)

// background
#place(top + left, rect(width: W, height: H, fill: navy))

// thin tricolour rule across the whole wrap, 1/3 from the top
#let stripe-y = bleed + 2.05in
#for (i, c) in (de-black, de-red, de-gold).enumerate() {
  place(top + left, dx: 0pt, dy: stripe-y + i * 0.045in, rect(width: W, height: 0.045in, fill: c))
}

// ---------- FRONT ----------
#let fx = bleed + trim-w + spine
#place(top + left, dx: fx + 0.45in, dy: bleed + 0.55in, block(width: trim-w - 0.9in)[
  #text(size: 13.5pt, weight: "bold", tracking: 0.05em, fill: accent)[DEUTSCH – BOSNISCH / KROATISCH / SERBISCH]
])
#place(top + left, dx: fx + 0.45in, dy: bleed + 1.0in, block(width: trim-w - 0.9in)[
  #set par(leading: 0.62em)
  #block(below: 9pt, text(size: 33pt, weight: "bold")[Einbürgerungstest])
  #block(text(size: 24pt, weight: "semibold")[& Leben in Deutschland])
])
#place(top + left, dx: fx + 0.45in, dy: stripe-y + 0.45in, block(width: trim-w - 0.9in)[
  #set par(leading: 0.45em)
  #text(size: 19pt, weight: "bold")[Jede Frage verstehen –\ in Ihrer Sprache]
  #v(0.12in)
  #text(size: 15pt, weight: "semibold", style: "italic", fill: accent)[Razumijte svako pitanje na svom jeziku]
  #v(0.14in)
  #text(size: 12pt)[Alle 460 Fragen mit Übersetzung, Erklärung und Bildern · \ 10 vollständige Prüfungssimulationen]
])

#place(top + left, dx: fx + 0.45in, dy: bleed + 4.55in, block(width: trim-w - 0.9in, stroke: 1pt + accent, radius: 6pt, inset: 12pt)[
  #text(size: 10pt, weight: "semibold", fill: accent)[DIE PRÜFUNG · ISPIT]
  #v(2pt)
  #text(size: 12.5pt)[33 Fragen · 60 Minuten · Einbürgerung: 17 richtig · LiD-Test: 15 richtig]
  #v(1pt)
  #text(size: 10pt, style: "italic", fill: paper)[33 pitanja · 60 minuta · naturalizacija: 17 točnih · test LiD: 15 točnih]
])
#let badge(big, small) = box(width: 1.72in, height: 0.95in, radius: 6pt, fill: paper, inset: 7pt,
  align(center + horizon)[#text(fill: navy, size: 18pt, weight: "bold", big)\ #text(fill: navy, size: 8.3pt, small)])
#place(top + left, dx: fx + 0.45in, dy: bleed + 6.35in,
  grid(columns: 3, column-gutter: 0.17in,
    badge("300 + 160", "allgemeine Fragen +\nalle 16 Bundesländer"),
    badge("Erklärt", "jede richtige Antwort ·\nsvaki odgovor objašnjen"),
    badge("30 + 3", "10 Prüfungssimulationen\nmit Antwortbogen"),
  ))
#place(top + left, dx: fx + 0.45in, dy: bleed + trim-h - 1.05in, block(width: trim-w - 0.9in)[
  #text(size: 9pt, fill: paper)[BAMF-Fragenkatalog · Stand: #P.stand]
  #linebreak()
  #text(size: 7.5pt, fill: rgb("#aab4c8"))[Keine offizielle Publikation des BAMF]
])

#if P.draft {
  place(center + horizon, rotate(-30deg, text(size: 70pt, weight: "bold", fill: rgb(255, 255, 255, 60), "NACRT · ENTWURF")))
}

// ---------- SPINE ----------
#if P.spine_in >= 0.25 {
  place(top + left, dx: bleed + trim-w, dy: 0pt, rect(width: spine, height: H, fill: navy))
  place(top + left, dx: bleed + trim-w + spine / 2, dy: H / 2,
    place(center + horizon, rotate(90deg, reflow: true,
      text(size: 11pt, weight: "semibold")[Einbürgerungstest & Leben in Deutschland #h(8pt) #text(fill: accent)[Deutsch – BKS]])))
}

// ---------- BACK ----------
#let bx = bleed + 0.45in
#place(top + left, dx: bx, dy: bleed + 0.55in, block(width: trim-w - 0.9in)[
  #set par(leading: 0.55em, justify: false)
  #text(size: 15pt, weight: "bold")[Gut vorbereitet zum Test „Leben in Deutschland“ und zum Einbürgerungstest]
  #v(0.1in)
  #text(size: 9.6pt)[Alle 460 Fragen des BAMF-Fragenkatalogs – 300 allgemeine Fragen und die Fragen aller 16 Bundesländer. Jede Frage auf Deutsch, wie in der Prüfung, mit Übersetzung ins Bosnische/Kroatische/Serbische.]
])
#place(top + left, dx: bx, dy: stripe-y + 0.4in, block(width: trim-w - 0.9in)[
  #set par(leading: 0.55em, justify: false)
  #set text(size: 10pt)
  - Richtige Antwort markiert und in einfachen Worten erklärt
  - Merksatz auf Deutsch zu jeder Frage
  - Wappen, Karten und Stimmzettel der Bildfragen abgedruckt
  - 10 vollständige Prüfungssimulationen (30 + 3 Fragen) mit Antwortbogen
  - Lernplan für 14 und 30 Tage, Fehlerliste, Themenregister
  - Glossar Deutsch – BKS
  #v(0.18in)
  #text(size: 10.5pt, style: "italic", fill: paper)[Sva 460 pitanja za test naturalizacije i test „Život u Njemačkoj”: njemački original, prijevod, označen točan odgovor, kratko objašnjenje, slike iz kataloga i 10 potpunih probnih testova.]
  #v(0.18in)
  #text(size: 7.8pt, fill: rgb("#aab4c8"))[Keine offizielle Publikation des Bundesamts für Migration und Flüchtlinge. Fragen und Antworten: BAMF-Gesamtfragenkatalog, unverändert wiedergegeben. Übersetzungen und Erklärungen mit KI-Unterstützung erstellt; #P.check_note]
])
// KDP barcode area (bottom right of back cover): keep empty, 2 × 1.2 in, plus margin
#place(top + left, dx: bleed + trim-w - 0.25in - 2in, dy: bleed + trim-h - 0.25in - 1.2in,
  rect(width: 2in, height: 1.2in, fill: white))
#place(top + left, dx: bx, dy: bleed + trim-h - 0.62in, text(size: 9pt, weight: "semibold", fill: paper, P.imprint))
