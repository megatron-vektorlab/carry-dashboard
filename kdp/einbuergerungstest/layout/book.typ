// Interior: Einbürgerungstest & Leben in Deutschland – Deutsch–BKS
// Trim 6.69 × 9.61 in (17 × 24.4 cm), black & white, no bleed.
#let data = json("/build/book_data.json")
#let M = data.meta

#let ink = black
#let grey = luma(95)
#let pale = luma(238)

#set document(title: M.title + " – " + M.languages)
#set text(font: "Source Sans 3", size: 9.4pt, lang: "de", hyphenate: true)
#set par(leading: 0.52em, justify: false)

#let section = state("section", "")
#set page(
  width: 6.69in, height: 9.61in,
  margin: (inside: 19mm, outside: 14mm, top: 18mm, bottom: 18mm),
  header: context {
    let p = here().page()
    let s = section.get()
    if s == "" { return }
    set text(size: 7.8pt, fill: grey)
    if calc.odd(p) { align(right, s) } else { align(left, M.title) }
    v(-2mm)
    line(length: 100%, stroke: 0.4pt + luma(170))
  },
  footer: context {
    let p = here().page()
    if section.get() == "" { return }
    set text(size: 8.5pt)
    if calc.odd(p) { align(right, str(counter(page).get().first())) } else { align(left, str(counter(page).get().first())) }
  },
)

#show heading.where(level: 1): it => {
  pagebreak(weak: true, to: "odd")
  v(18mm)
  block(text(size: 22pt, weight: "bold", it.body))
  v(6mm)
}
#show heading.where(level: 2): it => block(above: 1.4em, below: 0.8em, text(size: 13pt, weight: "bold", it.body))
#show heading.where(level: 3): it => block(above: 1.1em, below: 0.6em, text(size: 10.5pt, weight: "semibold", it.body))

// ---------- building blocks ----------
#let subtitle(body) = block(above: -3mm, below: 7mm, text(size: 14pt, style: "italic", lang: "hr", body))
#let bks(body) = text(style: "italic", fill: grey, size: 8.7pt, lang: "hr", body)

#let marker(o) = if o.correct {
  box(width: 4.2mm, height: 4.2mm, fill: ink, radius: 0.8mm, baseline: 1.05mm,
    align(center + horizon, text(fill: white, weight: "bold", size: 7.5pt, o.letter)))
} else {
  box(width: 4.2mm, height: 4.2mm, stroke: 0.6pt + ink, radius: 0.8mm, baseline: 1.05mm,
    align(center + horizon, text(size: 7.5pt, o.letter)))
}

#let question(q) = block(breakable: false, width: 100%, above: 4.2mm, below: 0mm)[
  #grid(columns: (9.5mm, 1fr), column-gutter: 1.5mm,
    align(left, box(inset: (x: 1.2mm, y: 0.9mm), stroke: 0.8pt + ink, radius: 1mm, text(weight: "bold", size: 8.4pt, q.label))),
    [
      #text(weight: "semibold", q.q_de)
      #linebreak()
      #bks(q.q_bks)
    ],
  )
  #v(1.2mm)
  #grid(columns: (9.5mm, 5.5mm, 1fr), column-gutter: 1.5mm, row-gutter: 1.6mm,
    ..q.options.map(o => (
      [], marker(o),
      [#if o.correct { text(weight: "bold", o.de) } else { o.de } #h(1.5mm) #bks(o.bks)],
    )).flatten()
  )
  #v(1.2mm)
  #pad(left: 11mm, block(width: 100%, fill: pale, inset: (x: 2.4mm, y: 1.8mm), radius: 1mm)[
    #set text(size: 8.5pt)
    #set par(leading: 0.48em)
    #text(lang: "hr")[*Objašnjenje:* #q.expl]
    #linebreak()
    *Merksatz:* #emph(q.merksatz)
  ])
]

// ---------- front matter ----------
#page(header: none, footer: none)[
  #v(55mm)
  #align(center)[
    #text(size: 20pt, weight: "bold", M.title)
    #v(3mm)
    #text(size: 13pt, M.languages)
  ]
]
#page(header: none, footer: none)[]

#page(header: none, footer: none)[
  #v(22mm)
  #align(center)[
    #text(size: 23pt, weight: "bold")[Einbürgerungstest\ & Leben in Deutschland]
    #v(5mm)
    #text(size: 13.5pt, weight: "semibold")[Deutsch – Bosnisch/Kroatisch/Serbisch]
    #v(9mm)
    #text(size: 11.5pt)[Alle 460 Fragen des BAMF-Fragenkatalogs\ (300 allgemeine Fragen + 10 Fragen je Bundesland)\ mit Übersetzung, Erklärungen, Merksätzen\ und 10 Probetests]
    #v(9mm)
    #text(size: 11pt, lang: "hr", style: "italic")[Sva pitanja iz kataloga za test naturalizacije\ i test „Život u Njemačkoj”\ s prijevodom, objašnjenjima i 10 probnih testova]
    #v(1fr)
    #text(size: 9pt)[Fragenkatalog: Stand des BAMF-Katalogs, abgerufen am #M.catalog_retrieved]
    #v(3mm)
    #text(size: 10pt, weight: "semibold", M.imprint)
  ]
  #v(10mm)
]

// Copyright / imprint page
#page(header: none, footer: none)[
  #set text(size: 7.8pt)
  #set par(leading: 0.5em)
  #v(1fr)
  *Hinweis:* Dieses Buch ist keine Veröffentlichung des Bundesamts für Migration und Flüchtlinge (BAMF) und steht in keiner Verbindung zum BAMF.

  *Quelle der Fragen und Antworten:* #M.catalog_source. Die Fragen, Antwortmöglichkeiten und richtigen Antworten sind unverändert wiedergegeben (§ 5 Abs. 2 UrhG); Schreibweise nur typografisch angepasst. Maßgeblich ist allein der aktuelle Fragenkatalog des BAMF (www.bamf.de).

  *Bildfragen:* Die Abbildungen des Katalogs sind in diesem Buch nicht enthalten. Das richtige Bild wird jeweils in Worten beschrieben. Alle Bilder finden Sie kostenlos im Online-Testcenter des BAMF.

  *Übersetzungen, Erklärungen und Merksätze:* erstellt mit Unterstützung durch künstliche Intelligenz und redaktionell geprüft. Redaktionelle Verantwortung: [NAME].

  Alle Angaben ohne Gewähr. Das Buch ersetzt keine Beratung durch die Einbürgerungsbehörde.

  © 2026 [VERLAG / NAME] (Übersetzungen, Erklärungen, Merksätze, Gestaltung). Alle Rechte vorbehalten.\
  Verantwortlich / Hersteller (GPSR): [NAME], [ANSCHRIFT], [E-MAIL]\
  Druck: siehe letzte Seite. ISBN: [ISBN oder KDP-ISBN]
  #v(6mm)
]

#outline(title: [Sadržaj / Inhalt], depth: 2, indent: 4mm)

// ---------- introduction ----------
#section.update("Uvod")
#set text(lang: "hr")
= Uvod

== O testu

Test *„Leben in Deutschland”* (Život u Njemačkoj) polaže se na kraju integracijskog tečaja, a *Einbürgerungstest* (test naturalizacije) prije stjecanja njemačkog državljanstva. Oba testa koriste *isti katalog od 310 pitanja*: 300 općih pitanja i 10 pitanja o saveznoj pokrajini u kojoj živite. Ova knjiga sadrži cijeli katalog: 300 općih pitanja i pitanja za *svih 16 pokrajina*.

- Test ima *33 pitanja*: 30 općih i 3 o Vašoj pokrajini.
- Za svako pitanje ponuđena su 4 odgovora; točan je uvijek samo jedan.
- Imate *60 minuta*.
- Za državljanstvo trebate najmanje *17 točnih odgovora*. Na kraju orijentacijskog tečaja 15 točnih odgovora znači da ste položili tečaj, a 17 da ste ujedno ispunili uvjet za naturalizaciju.
- Test se polaže *na njemačkom jeziku*. Zato u ovoj knjizi njemački tekst uvijek stoji prvi.
- Pristojba za Einbürgerungstest iznosi 25 €. Prijavljujete se u ispitnom centru, npr. u pučkom učilištu (Volkshochschule). Neke osobe su oslobođene testa (npr. nakon završene njemačke škole) – to provjerite u svom uredu za naturalizaciju.

== Kako koristiti ovu knjigu

Svako pitanje izgleda ovako:

- *Masno:* pitanje na njemačkom, točno kako je u katalogu. Ispod njega, u *kurzivu*: prijevod.
- Četiri odgovora označena s A–D. *Crni kvadratić i masna slova* označavaju točan odgovor. Iza svakog odgovora je prijevod.
- *Objašnjenje* kaže zašto je odgovor točan – razumijevanje se pamti bolje od napamet naučenih slova.
- *Merksatz* je kratka njemačka rečenica za pamćenje. Pročitajte je naglas.

*Savjeti za učenje:* učite 20 do 30 pitanja dnevno. Prekrijte odgovore papirom i prvo sami odgovorite. Pitanja na kojima ste pogriješili označite i ponovite ih sutradan. Na ispitu je redoslijed odgovora drugačiji, pa učite *sadržaj* točnog odgovora, a ne slovo. Kad prođete kroz sva pitanja, riješite *10 probnih testova* na kraju knjige – zajedno pokrivaju svih 300 općih pitanja.

== Napomene

- *Prijevod:* radi čitljivosti za osobe koristimo muški rod, koji se odnosi na oba spola. Nazivi njemačkih institucija ostaju na njemačkom, s objašnjenjem u zagradi. Tekst je pisan ijekavicom i latinicom.
- *Slikovna pitanja:* slike iz kataloga nisu otisnute u knjizi. Točna slika je uvijek opisana riječima. Sve slike možete besplatno pogledati u BAMF-ovu Online-Testcentru (oet.bamf.de).
- *Brojevi pitanja* odgovaraju brojevima u BAMF-ovu katalogu, pa pitanja lako pronađete i u aplikacijama.
- Prije ispita provjerite na www.bamf.de je li katalog promijenjen.

#set text(lang: "de")
== Vorwort (Deutsch)

Dieses Buch enthält alle 460 Fragen des Gesamtfragenkatalogs zum Test „Leben in Deutschland“ und zum Einbürgerungstest. Zu jeder Frage finden Sie die Übersetzung ins Bosnische/Kroatische/Serbische, die richtige Antwort, eine kurze Erklärung und einen Merksatz auf Deutsch. Am Ende stehen 10 Probetests mit je 30 allgemeinen Fragen und ein Lösungsschlüssel. Viel Erfolg!

// ---------- part 1: general questions ----------
#section.update("Allgemeine Fragen · Opća pitanja")
= Teil 1: 300 allgemeine Fragen
#subtitle[Dio 1: 300 općih pitanja]
#for q in data.general { question(q) }

// ---------- part 2: states ----------
#section.update("Bundesländer · Savezne pokrajine")
= Teil 2: Fragen zu den Bundesländern
#subtitle[Dio 2: Pitanja o saveznim pokrajinama]
#text(lang: "hr")[Na ispitu dobivate 3 pitanja o pokrajini u kojoj živite. Naučite 10 pitanja svoje pokrajine – ostale možete preskočiti.]
#for s in data.states {
  pagebreak(weak: true)
  [== #s.name]
  for q in s.questions { question(q) }
}

// ---------- part 3: practice tests ----------
#section.update("Probetests · Probni testovi")
= Teil 3: 10 Probetests
#subtitle[Dio 3: 10 probnih testova]
#text(lang: "hr")[Svaki test ima 30 općih pitanja, samo na njemačkom – kao na ispitu. Dodajte 3 pitanja svoje pokrajine iz Dijela 2. Imate 60 minuta; za prolaz trebate 17 od 33 točna odgovora. Rješenja su na kraju ovog dijela. Broj u zagradi je broj pitanja u katalogu.]

#for t in data.tests {
  pagebreak(weak: true)
  [== Probetest #t.n]
  set text(size: 9pt)
  for (i, q) in t.questions.enumerate() {
    block(breakable: false, above: 3mm, below: 0mm)[
      #grid(columns: (8mm, 1fr), column-gutter: 1mm,
        text(weight: "bold", str(i + 1) + "."),
        [
          #text(weight: "semibold", q.q_de) #text(fill: grey, size: 7.5pt)[(Nr. #q.num)]
          #if q.picture [#text(fill: grey, size: 7.5pt, lang: "hr")[– slikovno pitanje, vidi opis uz pitanje #q.num]]
          #v(0.6mm)
          #grid(columns: (1fr, 1fr), column-gutter: 3mm, row-gutter: 1.2mm,
            ..q.options.map(o => grid(columns: (4.6mm, 1fr), column-gutter: 0.6mm,
              box(width: 3.6mm, height: 3.6mm, stroke: 0.5pt, radius: 0.6mm, baseline: 0.7mm, align(center + horizon, text(size: 6.5pt, o.letter))),
              o.de))
          )
        ],
      )
    ]
  }
}

#pagebreak(weak: true)
== Lösungen · Rješenja
#set text(size: 8.6pt)
#for t in data.tests {
  block(breakable: false, above: 3mm)[
    *Probetest #t.n* #h(2mm) #text(fill: grey)[(Frage: Antwort — Nr. im Katalog)]
    #v(0.8mm)
    #grid(columns: (1fr,) * 6, column-gutter: 1mm, row-gutter: 1.1mm,
      ..t.questions.enumerate().map(((i, q)) => [*#(i + 1):* #q.answer #text(fill: grey, size: 7pt)[(#q.num)]])
    )
  ]
}

// ---------- part 4: glossary ----------
#set text(size: 9.4pt)
#section.update("Glossar · Pojmovnik")
= Glossar Deutsch – BKS
#subtitle[Pojmovnik njemački – BKS]
#set text(size: 8.6pt)
#columns(2, gutter: 6mm)[
  #for g in data.glossary {
    block(breakable: false, below: 1.6mm)[*#g.de* \ #text(lang: "hr", g.bks)]
  }
]
