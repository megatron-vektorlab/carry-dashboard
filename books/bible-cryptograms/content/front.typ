#import "/layout/book.typ": *
#let D = json("/build/book/data.json")
#let E = D.example

#include "/content/welcome.typ"
#pagebreak()
#include "/content/howto.typ"
#pagebreak()
#include "/content/tips.typ"
