#import "/layout/book.typ": *
#let D = json("/build/book/data.json")

#metadata(none) <sec-solutions>
#chapter-title("Solutions", sub: "Every verse, word for word from the King James Version")
#columns(2, gutter: 0.32in)[
  #for p in D.puzzles [
    #block(breakable: false, spacing: 1.1em)[
      #metadata(p.num) #label("sol-" + str(p.num))
      #text(font: serif, weight: "bold", size: 16pt)[#p.num.] #h(4pt) #text(weight: "bold")[#p.ref] \
      #p.text
      #if p.reflection != "" [ \ *Reflect:* #p.reflection]
    ]
  ]
]
