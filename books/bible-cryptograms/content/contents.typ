#import "/layout/book.typ": *
#let D = json("/build/book/data.json")
#let pg(l) = context counter(page).at(l).first()
#let row(t, l, bold: false) = block(spacing: 0.62em)[#if bold [*#t*] else [#t] #box(width: 1fr, repeat[ .]) #h(2pt) #pg(l)]

#row("Welcome", <sec-welcome>)
#row("How to Solve a Cryptogram", <sec-howto>)
#row("Tips for King James Verses", <sec-tips>)
#v(0.3em)
#for (ti, t) in D.themes.enumerate() [
  #row([Part #(ti + 1): #t.name], label("part-" + str(ti + 1)), bold: true)
]
#v(0.3em)
#row("Hints", <sec-hints>)
#row("Solutions", <sec-solutions>)
#row("Index of Verses", <sec-index>)
#row("My Progress", <sec-progress>)
#row("Verses I Want to Remember", <sec-remember>)
