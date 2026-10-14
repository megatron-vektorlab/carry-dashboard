// Kindle eBook cover: 1600 × 2560 px (ratio 1.6), rendered at 320 ppi from a 5 × 8 in page.
// Same design as the paperback front; texts adapted (no answer sheets in the eBook).
#let P = json("/build/ebook_cover_params.json")
#let navy = rgb("#16233b")
#let paper = rgb("#f4f1ea")
#let accent = rgb("#e0a526")
#let de-black = rgb("#1b1b1b")
#let de-red = rgb("#c8102e")
#let de-gold = rgb("#f2c230")

#set page(width: 5in, height: 8in, margin: 0pt, fill: navy)
#set text(font: "Source Sans 3", fill: white)
#let L = 0.38in
#let W = 5in - 2 * L

#place(top + left, dx: L, dy: 0.42in, block(width: W,
  text(size: 12pt, weight: "bold", tracking: 0.04em, fill: accent)[DEUTSCH – BOSNISCH / KROATISCH / SERBISCH]))
#place(top + left, dx: L, dy: 0.85in, block(width: W)[
  #set par(leading: 0.55em)
  #block(below: 8pt, text(size: 36pt, weight: "bold")[Einbürgerungstest])
  #text(size: 25pt, weight: "semibold")[& Leben in Deutschland]
])
#let stripe-y = 2.35in
#for (i, c) in (de-black, de-red, de-gold).enumerate() {
  place(top + left, dy: stripe-y + i * 0.05in, rect(width: 5in, height: 0.05in, fill: c))
}
#place(top + left, dx: L, dy: stripe-y + 0.42in, block(width: W)[
  #set par(leading: 0.45em)
  #text(size: 21pt, weight: "bold")[Jede Frage verstehen –\ in Ihrer Sprache]
  #v(0.12in)
  #text(size: 16pt, weight: "semibold", style: "italic", fill: accent)[Razumijte svako pitanje\ na svom jeziku]
])
#place(top + left, dx: L, dy: 4.42in, block(width: W, stroke: 1.2pt + accent, radius: 6pt, inset: 11pt)[
  #text(size: 10.5pt, weight: "semibold", fill: accent)[DIE PRÜFUNG · ISPIT]
  #v(2pt)
  #text(size: 13pt)[33 Fragen · 60 Minuten \ Einbürgerung: 17 richtig · LiD: 15 richtig]
])
#let badge(big, small) = box(width: 1.36in, height: 1.0in, radius: 6pt, fill: paper, inset: 6pt,
  align(center + horizon)[#text(fill: navy, size: 18pt, weight: "bold", big)\ #text(fill: navy, size: 8.6pt, small)])
#place(top + left, dx: L, dy: 5.58in,
  grid(columns: 3, column-gutter: 0.1in,
    badge("460", "alle Fragen ·\nalle 16 Bundesländer"),
    badge("Erklärt", "jede richtige Antwort ·\nsvaki odgovor objašnjen"),
    badge("10", "Probetests\nmit Lösungen"),
  ))
#place(top + left, dx: L, dy: 6.9in, text(size: 15pt, weight: "semibold", P.author))
#place(top + left, dx: L, dy: 7.25in, block(width: W)[
  #text(size: 10pt, fill: paper)[BAMF-Fragenkatalog · #P.stand]
  #linebreak()
  #text(size: 9pt, fill: rgb("#aab4c8"))[Keine offizielle Publikation des BAMF]
])
#if P.draft {
  place(center + horizon, rotate(-30deg, text(size: 54pt, weight: "bold", fill: rgb(255, 255, 255, 60), "NACRT · ENTWURF")))
}
