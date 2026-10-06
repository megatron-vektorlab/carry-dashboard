#import "/layout/book.typ": *
#let D = json("/build/book/data.json")
#let pairs(ls) = ls.map(h => h.at(0) + " = " + h.at(1)).join(", ")

#metadata(none) <sec-hints>
#chapter-title("Hints", sub: "Three gentle steps for every puzzle")
Every puzzle has three hints, each in its own section so you never see more than you want. Take one hint, go back to the puzzle, and enjoy the rest of it yourself.

How to read a letter hint: *Y = E* means that the code letter *Y* stands for the real letter *E*. Write E on the line above every Y in the puzzle, and in the *Real* box under Y in the code key.

#let pg(l) = context counter(page).at(l).first()
#table(columns: (auto, 1fr, auto), stroke: none, inset: (x: 0pt, y: 4pt), column-gutter: 12pt,
  [*Hint 1*], [The book of the Bible, and one more letter.], [page #pg(<hints-1>)],
  [*Hint 2*], [Two more letters.], [page #pg(<hints-2>)],
  [*Hint 3*], [The longest word and where it is (word 7 means the seventh word of the puzzle), and the full reference, so you can look the verse up in your own Bible.], [page #pg(<hints-3>)],
)

#metadata(none) <hints-1>
#set page(header: context { if locate(<hints-1>).page() != here().page() { set text(size: 16pt); if calc.even(here().page()) [Hint 1 · The book and one letter #h(1fr)] else [#h(1fr) Hint 1 · The book and one letter] } })
#section("Hint 1 · The book and one letter")
#v(4pt)
#columns(2, gutter: 0.35in)[
  #for p in D.puzzles [
    #block(breakable: false, spacing: 0.6em)[#metadata(p.num) #label("hint-" + str(p.num))*#p.num.* #h(3pt) #p.hints.at("1").book · #pairs(p.hints.at("1").letters)]
  ]
]

#pagebreak()
#set page(header: context { if locate(<hints-2>).page() != here().page() { set text(size: 16pt); if calc.even(here().page()) [Hint 2 · Two more letters #h(1fr)] else [#h(1fr) Hint 2 · Two more letters] } })
#metadata(none) <hints-2>
#section("Hint 2 · Two more letters")
#v(4pt)
#columns(3, gutter: 0.3in)[
  #for p in D.puzzles [
    #block(breakable: false, spacing: 0.6em)[#metadata(p.num) #label("hint2-" + str(p.num))*#p.num.* #h(3pt) #pairs(p.hints.at("2").letters)]
  ]
]

#pagebreak()
#set page(header: context { if locate(<hints-3>).page() != here().page() { set text(size: 16pt); if calc.even(here().page()) [Hint 3 · The longest word and the reference #h(1fr)] else [#h(1fr) Hint 3 · The longest word and the reference] } })
#metadata(none) <hints-3>
#section("Hint 3 · The longest word and the reference")
#v(4pt)
#columns(2, gutter: 0.35in)[
  #for p in D.puzzles [
    #block(breakable: false, spacing: 0.6em)[#metadata(p.num) #label("hint3-" + str(p.num))*#p.num.* #h(3pt) word #p.hints.at("3").position: #p.hints.at("3").word \ #h(1.2em) #p.ref]
  ]
]
