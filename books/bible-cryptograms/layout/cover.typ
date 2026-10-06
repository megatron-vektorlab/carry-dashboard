// Full-wrap paperback cover: back | spine | front.  Data: build/cover/cover.json (bc/cover.py).
#let C = json("/build/cover/cover.json")
#let inch = 1in
#let B = C.bleed * inch
#let TW = C.trim_w * inch
#let TH = C.trim_h * inch
#let SP = C.spine * inch
#let W = C.width * inch
#let H = C.height * inch
#let back-x = B
#let spine-x = B + TW
#let front-x = B + TW + SP

#set page(width: W, height: H, margin: 0pt, fill: rgb("#1D2B4F"))
#set text(font: "Atkinson Hyperlegible Next")
// Atkinson draws a slashed zero; numbers on the cover use Libre Baskerville.
#show regex("[0-9]+"): set text(font: "Libre Baskerville", number-type: "lining")

// ---------- palette ----------
#let navy = rgb("#1D2B4F")
#let lead = rgb("#0E1730")
#let gold = rgb("#E8B84A")
#let cream = rgb("#FFF6E0")
#let ruby = rgb("#B8293D")
#let sapph = rgb("#2F6DB5")
#let emer = rgb("#2E8B57")
#let amber = rgb("#E07B2E")
#let viol = rgb("#6A4C9C")
#let sky = rgb("#7FB8DA")

// ---------- helpers ----------
#let arcpts(cx, cy, r, a0, a1, steps: 8) = range(steps + 1).map(i => {
  let a = a0 + (a1 - a0) * i / steps
  (cx + r * calc.cos(a), cy + r * calc.sin(a))
})
#let ring(cx, cy, ra, rb, n, colors, off: 0deg, sw: 2pt) = {
  for k in range(n) {
    let a0 = off + 360deg * k / n
    let a1 = off + 360deg * (k + 1) / n
    place(top + left, polygon(fill: colors.at(calc.rem(k, colors.len())), stroke: sw + lead,
      ..(arcpts(cx, cy, rb, a0, a1) + arcpts(cx, cy, ra, a1, a0))))
  }
}
#let pill(body, fill, h: 0.66in) = box(fill: fill, radius: h / 2, inset: (x: 0.34in), height: h, align(horizon, body))

#let rose-window(cx, cy, r) = {
  let k = r / 2.75in
  place(top + left, dx: cx - r, dy: cy - r, circle(radius: r, fill: lead))
  ring(cx, cy, 2.05in * k, 2.6in * k, 24, (ruby, sapph, gold, sapph, emer, sapph), off: -90deg)
  ring(cx, cy, 1.25in * k, 2.05in * k, 12, (sky, viol, amber, viol), off: -75deg)
  ring(cx, cy, 0.62in * k, 1.25in * k, 8, (ruby, sapph), off: -67.5deg)
  place(top + left, dx: cx - 0.62in * k, dy: cy - 0.62in * k, circle(radius: 0.62in * k, fill: gold, stroke: 2pt + lead))
  place(top + left, dx: cx - 0.09in * k, dy: cy - 0.46in * k, rect(width: 0.18in * k, height: 0.92in * k, fill: cream))
  place(top + left, dx: cx - 0.32in * k, dy: cy - 0.24in * k, rect(width: 0.64in * k, height: 0.18in * k, fill: cream))
  place(top + left, dx: cx - 2.62in * k, dy: cy - 2.62in * k, circle(radius: 2.62in * k, fill: none, stroke: 6pt * k + gold))
}

// Cream letter tiles with the code letter underneath, like a puzzle line.
#let tiles(word, code, tw: 0.53in, th: 0.9in, gap: 0.05in, size: 48pt, code-size: 17pt) = stack(dir: ltr, spacing: gap,
  ..word.clusters().enumerate().map(((i, ch)) => stack(spacing: 0.09in,
    box(width: tw, height: th, fill: cream, radius: 0.06in,
      align(center + horizon, text(size: size, weight: "bold", fill: lead, ch))),
    box(width: tw, align(center, text(size: code-size, weight: "bold", fill: gold.transparentize(15%), code.clusters().at(i)))))))

// ================= FRONT =================
#let fx = front-x
#let fcx = fx + TW / 2
#place(top + left, dx: fx + 0.65in, dy: B + 0.65in, rect(width: TW - 1.3in, height: TH - 1.3in, stroke: 2pt + gold, radius: 0.14in))
#place(top + left, dx: fx, dy: B + 0.92in, box(width: TW, align(center,
  pill(text(size: 34pt, weight: "bold", fill: navy, tracking: 3pt)[LARGE PRINT], gold))))
#place(top + left, dx: fx, dy: B + 1.75in, box(width: TW, align(center,
  text(font: "Cinzel", weight: "bold", size: 100pt, fill: cream)[BIBLE])))
#place(top + left, dx: fx, dy: B + 3.2in, box(width: TW, align(center, tiles("CRYPTOGRAMS", C.tile_code))))
#place(top + left, dx: fx, dy: B + 4.72in, box(width: TW, align(center, {
  set par(leading: 0.45em)
  text(font: "Libre Baskerville", style: "italic", size: 23pt, fill: cream)[#C.front_line.at(0) \ #C.front_line.at(1)]
})))
#place(top + left, dx: fx, dy: B + 5.7in, box(width: TW, align(center,
  text(size: 18pt, weight: "bold", fill: gold)[ONE PUZZLE PER PAGE #h(6pt) · #h(6pt) HINTS #h(6pt) · #h(6pt) SOLUTIONS])))
#rose-window(fcx, B + 8.05in, 1.75in)
// count seal
#place(top + left, dx: fx + 5.55in, dy: B + 7.95in, circle(radius: 0.9in, fill: cream, stroke: 4pt + gold,
  align(center + horizon, stack(spacing: 0.08in,
    text(font: "Libre Baskerville", size: 44pt, weight: "bold", fill: navy)[#C.count],
    text(size: 16pt, weight: "bold", fill: navy, tracking: 1pt)[PUZZLES]))))
#place(top + left, dx: fx, dy: B + 9.88in, box(width: TW, align(center,
  text(font: "Libre Baskerville", size: 21pt, fill: cream, tracking: 2.5pt)[#upper(C.author)])))

// ================= SPINE =================
#if C.spine_text {
  place(top + left, dx: spine-x, dy: B, box(width: SP, height: TH, align(center + horizon,
    rotate(90deg, reflow: true, box(width: TH - 1in, height: SP - 0.14in, align(center + horizon,
      text(size: calc.min(22pt, (SP - 0.18in) / 1in * 72pt * 0.95), fill: cream, weight: "bold", tracking: 1pt)[
        #text(font: "Cinzel")[LARGE PRINT BIBLE CRYPTOGRAMS] #h(0.35in) #text(fill: gold)[VOL. 1] #h(0.35in) #text(font: "Libre Baskerville", weight: "regular")[#upper(C.author.split(" ").last())]]))))))
}

// ================= BACK =================
#let bx = back-x
#place(top + left, dx: bx + 0.9in, dy: B + 0.9in, block(width: TW - 1.8in, {
  set text(fill: cream, size: 17pt)
  set par(leading: 0.5em, spacing: 0.8em)
  text(font: "Libre Baskerville", size: 26pt, weight: "bold", fill: gold)[#C.back_headline]
  v(0.06in)
  C.blurb
  v(0.12in)
  // sample puzzle card
  block(width: 100%, fill: cream, radius: 0.1in, inset: 0.16in, {
    set text(fill: lead)
    text(size: 16pt, weight: "bold")[Try one: #C.sample_level_name · given letters in bold]
    v(0.04in)
    let cw = 0.30in
    let cell(c, g) = box(width: cw, stack(dir: ttb, spacing: 0.02in,
      box(width: cw - 4pt, height: 0.34in, stroke: (bottom: 1.2pt + lead),
        align(center + bottom, pad(bottom: 2pt, text(size: 20pt, weight: "bold", g)))),
      box(width: cw, height: 0.27in, align(center + horizon, text(size: 20pt, c)))))
    let pcell(c) = box(width: 0.15in, stack(dir: ttb, spacing: 0.02in,
      box(height: 0.34in),
      box(height: 0.27in, align(center + horizon, text(size: 20pt, c)))))
    let ws = C.sample_words.map(w => box(w.map(c => if c.at(2) { cell(c.at(0), c.at(1)) } else { pcell(c.at(0)) }).join()))
    par(leading: 0.1in, ws.join(h(0.2in, weak: true)))
    v(0.02in)
    text(size: 16pt)[This is puzzle #C.sample_num inside. The verse is in the solutions.]
  })
  v(0.14in)
  for b in C.bullets [
    #grid(columns: (0.32in, 1fr), align: (left + top, left + top), text(fill: gold, weight: "bold", size: 20pt)[•], b)
    #v(0.02in)
  ]
}))
// barcode zone: keep empty (KDP prints the barcode here)
#place(top + left, dx: bx + TW - 0.25in - 2.25in, dy: B + TH - 0.25in - 1.45in,
  rect(width: 2.25in, height: 1.45in, fill: white))
#place(top + left, dx: bx + 0.9in, dy: B + TH - 1.35in, block(width: 4.6in, {
  set text(fill: cream, size: 16pt)
  text(font: "Libre Baskerville", style: "italic")[#C.epigraph]
}))
