// "Tko je tko u njemačkoj državi" as a picture for the eBook (the same chart as in print).
#set page(width: 5in, height: auto, margin: 0.12in, fill: white)
#set text(font: "Source Sans 3", size: 11pt, lang: "hr")
#let ink = black
#let soft = luma(90)
#let org(t, s) = block(width: 100%, stroke: 1pt + ink, radius: 1.2mm, inset: 2.4mm,
  [#text(weight: "bold", lang: "de", t) #linebreak() #text(size: 9.5pt, s)])
#let arrow(t) = align(center, text(size: 9.5pt, fill: soft)[↓ #t])
#grid(columns: (1fr, 1fr), column-gutter: 4mm, row-gutter: 1.8mm,
  org("Wahlberechtigte", "birači – za Bundestag od 18 godina"), org("Wahlberechtigte im Land", "birači u pokrajini"),
  arrow("biraju svake 4 godine"), arrow("biraju"),
  org("Bundestag", "savezni parlament: zakoni, proračun, kontrola vlade"), org("Landtag", "pokrajinski parlament"),
  arrow("bira kancelara (na prijedlog predsjednika)"), arrow("bira šefa pokrajinske vlade"),
  org("Bundesregierung", "kancelar + ministri; ministre imenuje savezni predsjednik na prijedlog kancelara"), org("Landesregierung", "pokrajinska vlada"),
  [], arrow("šalje svoje članove"),
  [], org("Bundesrat", "pokrajine sudjeluju u saveznim zakonima"),
)
#v(2.5mm)
#grid(columns: (1fr, 1fr), column-gutter: 4mm, row-gutter: 1.8mm,
  org("Bundesversammlung", "zastupnici Bundestaga + jednako toliko predstavnika pokrajina"), org("Bundesverfassungsgericht", "Savezni ustavni sud: čuva Temeljni zakon"),
  arrow("bira na 5 godina"), align(center, text(size: 9.5pt, fill: soft)[↑ suce biraju Bundestag i Bundesrat, pola-pola]),
  org("Bundespräsident", "šef države: potpisuje zakone, imenuje kancelara i ministre"), [],
)
