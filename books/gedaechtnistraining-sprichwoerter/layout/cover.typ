// Full-wrap paperback cover: back | spine | front.  Data: build/cover/cover.json (gt/cover.py).
#let C = json("/build/cover/cover.json")
#let inch = 1in
#let B = C.bleed * inch
#let TW = C.trim_w * inch
#let TH = C.trim_h * inch
#let SP = C.spine * inch
#let W = C.width * inch
#let H = C.height * inch
#let spine-x = B + TW
#let fx = B + TW + SP

// palette: deep petrol, warm cream, sunflower yellow, brick red
#let petrol = rgb("#174652")
#let deep = rgb("#0F313A")
#let cream = rgb("#FBF3E1")
#let sun = rgb("#F2B33D")
#let brick = rgb("#C4553A")
#let ink = rgb("#1B1B1B")

#set page(width: W, height: H, margin: 0pt, fill: petrol)
#set text(font: "Atkinson Hyperlegible Next", lang: "de")
#show regex("[0-9]+"): set text(font: "Source Sans 3")

#let serif = "Libre Baskerville"
#let at(x, y, body) = place(top + left, dx: x, dy: y, body)

// Speech bubble with a tail at the lower left.
#let bubble(w, h, fill: cream, body) = box(width: w, height: h + 0.45in, {
  place(top + left, rect(width: w, height: h, radius: 0.35in, fill: fill))
  place(top + left, polygon(fill: fill, (0.8in, h - 2pt), (1.55in, h - 2pt), (0.55in, h + 0.45in)))
  place(top + left, box(width: w, height: h, align(center + horizon, body)))
})
#let lbox(ch, filled: false, s: 0.5in) = box(width: s, height: s * 1.15, stroke: 2.2pt + petrol, fill: white,
  align(center + horizon, text(size: 30pt, weight: "bold", fill: petrol, if filled { ch } else { "" })))
#let badge(t) = box(fill: sun, radius: 0.18in, inset: (x: 0.16in, y: 0.09in), text(size: 17pt, weight: "bold", fill: deep, t))

// ================= FRONT =================
#at(fx, 0pt, rect(width: TW + B, height: H, fill: petrol))
#at(fx, B + 0.55in, box(width: TW, align(center, text(size: 19pt, weight: "bold", tracking: 2.5pt, fill: sun)[GEDÄCHTNISTRAINING IN GROSSDRUCK])))
#at(fx, B + 1.05in, box(width: TW, align(center, {
  set par(leading: 0.3em)
  text(font: serif, size: 47pt, weight: "bold", fill: cream)[Sprichwörter und \ Redewendungen]
  v(-0.12in)
  text(font: serif, size: 34pt, weight: "bold", fill: sun)[für Senioren]
})))
// the speech bubble: a proverb with letter boxes
#at(fx + 0.95in, B + 4.15in, bubble(TW - 1.9in, 2.1in, {
  set par(leading: 0.5em)
  text(size: 30pt, fill: deep)[Morgenstund hat]
  v(0.1in)
  box(lbox("G", filled: true) + lbox("") + lbox("") + lbox(""))
  h(0.15in)
  text(size: 30pt, fill: deep)[im Mund]
}))
#at(fx, B + 7.15in, box(width: TW, align(center, {
  set par(leading: 0.45em)
  text(size: 25pt, weight: "bold", fill: cream)[#C.front_lines.at(1)]
  v(0.06in)
  text(size: 20pt, fill: cream)[mit Lösungen und Gesprächsimpulsen \ für Betreuung, Pflegeheim und Tagespflege]
})))
#at(fx, B + 8.95in, box(width: TW, align(center, C.badges.map(badge).join(h(0.14in)))))
#at(fx, B + 10.25in, box(width: TW, align(center, text(size: 19pt, fill: cream)[Band #C.volume #h(0.12in) · #h(0.12in) #C.author])))

// ================= SPINE =================
#at(spine-x, 0pt, rect(width: SP, height: H, fill: deep))
#if C.spine_text {
  at(spine-x, B, box(width: SP, height: TH, align(center + horizon,
    rotate(90deg, reflow: true, text(size: if SP > 0.5in { 17pt } else { 14pt }, fill: cream)[
      #text(weight: "bold")[Sprichwörter und Redewendungen für Senioren] #h(0.25in) · #h(0.25in) Band #C.volume #h(0.25in) · #h(0.25in) #C.author]))))
}

// ================= BACK =================
#at(0pt, 0pt, rect(width: B + TW, height: H, fill: cream))
#let bx = B + 0.6in
#let bw = TW - 1.2in
#at(bx, B + 0.6in, box(width: bw, {
  set par(leading: 0.55em, justify: false)
  text(font: serif, size: 26pt, weight: "bold", fill: petrol, C.back_headline)
  v(0.12in)
  text(size: 16.5pt, fill: ink, C.blurb)
}))
#at(bx, B + 3.35in, box(width: bw * 0.56, {
  set par(leading: 0.45em)
  for b in C.bullets {
    block(below: 0.11in, grid(columns: (0.24in, 1fr), text(size: 16pt, fill: brick)[■], text(size: 15.5pt, fill: ink, b)))
  }
}))
// a small look into the book: worksheet 1
#at(bx + bw * 0.6, B + 3.25in, rotate(3deg, box(stroke: 1.5pt + petrol, fill: white, inset: 0pt,
  image(C.sample, width: bw * 0.4))))
#at(bx, B + 7.3in, box(width: bw * 0.62, {
  set par(leading: 0.5em)
  text(size: 14pt, fill: ink)[Für Betreuungskräfte, Alltagsbegleiter, Ergotherapie, Tagespflege, Seniorengruppen und für Angehörige zu Hause. Kopiererlaubnis für die eigene Einrichtung oder Gruppe.]
}))
// barcode area (KDP): lower right, keep empty and white
#at(B + TW - 0.25in - 2.1in, B + TH - 0.25in - 1.3in, rect(width: 2.1in, height: 1.3in, fill: white))
