#import "/layout/book.typ": *
#let D = json("/build/book/data.json")

#pagebreak()
#metadata(none) <sec-index>
#chapter-title("Index of Verses", sub: "In Bible order. The number is the puzzle number, not the page.")
#let order = D.book_order
#let sorted = D.puzzles.sorted(key: p => (order.position(b => b == p.book), p.chapter, p.verse))
#columns(2, gutter: 0.35in)[
  #for p in sorted [
    #block(breakable: false, spacing: 0.55em)[#p.ref #box(width: 1fr, repeat[ .]) #h(2pt) No.~*#p.num*]
  ]
]

#pagebreak()
#metadata(none) <sec-progress>
#chapter-title("My Progress", sub: "Check off each puzzle when you solve it")
#grid(columns: (1fr,) * 8, row-gutter: 0.1in, column-gutter: 0.06in,
  ..D.puzzles.map(p => box(width: 100%, height: 0.36in, stroke: 1pt + ink, radius: 3pt, inset: (left: 5pt),
    align(left + horizon, text(size: 16pt)[#p.num]))))

#pagebreak()
#metadata(none) <sec-remember>
#chapter-title("Verses I Want to Remember")
#ruled-lines()

#if D.at("pad_page", default: false) {
  pagebreak()
  chapter-title("Notes")
  ruled-lines()
}
