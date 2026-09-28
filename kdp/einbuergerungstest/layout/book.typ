// Interior: Einbürgerungstest & Leben in Deutschland – Deutsch–BKS
// Trim 6.69 × 9.61 in (17 × 24.4 cm), black & white, no bleed.
#let data = json("/build/book_data.json")
#let M = data.meta
#let R = M.release
#let pending = "[AUSSTEHEND]"
#let val(k) = if R.at(k, default: none) == none { pending } else { R.at(k) }

#let ink = black
#let grey = luma(45)      // translation: dark enough to read comfortably
#let soft = luma(110)
#let pale = luma(238)

// type sizes (readability pass)
#let s-de = 10pt
#let s-bks = 9.4pt
#let s-expl = 9.2pt
#let s-small = 8.2pt

#set document(title: M.title + " – " + M.languages)
#set text(font: "Source Sans 3", size: s-de, lang: "de", hyphenate: true)
#set par(leading: 0.56em, justify: false)

#let section = state("section", "")
#set page(
  width: 6.69in, height: 9.61in,
  margin: (inside: 19mm, outside: 14mm, top: 18mm, bottom: 18mm),
  background: if M.draft { rotate(-40deg, text(size: 64pt, weight: "bold", fill: luma(232), "NACRT · ENTWURF")) },
  header: context {
    let p = here().page()
    let s = section.get()
    if s == "" { return }
    set text(size: 7.8pt, fill: soft)
    if calc.odd(p) { align(right, s) } else { align(left, M.title) }
    v(-2mm)
    line(length: 100%, stroke: 0.4pt + luma(170))
  },
  footer: context {
    if section.get() == "" { return }
    set text(size: 8.5pt)
    let n = str(counter(page).get().first())
    if calc.odd(here().page()) { align(right, n) } else { align(left, n) }
  },
)

#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(14mm)
  block(text(size: 21pt, weight: "bold", it.body))
  v(4mm)
}
#show heading.where(level: 2): it => block(above: 1.4em, below: 0.8em, text(size: 13pt, weight: "bold", it.body))
#show heading.where(level: 3): it => block(above: 1.1em, below: 0.6em, text(size: 10.5pt, weight: "semibold", it.body))

// ---------- building blocks ----------
#let subtitle(body) = block(above: -2mm, below: 6mm, text(size: 13.5pt, style: "italic", lang: "hr", body))
#let bks(body) = text(style: "italic", fill: grey, size: s-bks, lang: "hr", body)
#let note(body) = block(width: 100%, stroke: 0.6pt + ink, radius: 1.2mm, inset: 2.6mm, text(lang: "hr", size: 9pt, body))

#let letterbox(l, filled: false, size: 4.4mm) = box(width: size, height: size, radius: 0.8mm, baseline: 1.1mm,
  fill: if filled { ink } else { none }, stroke: 0.6pt + ink,
  align(center + horizon, text(fill: if filled { white } else { ink }, weight: "bold", size: 7.5pt, l)))

#let single-width(id) = if id == "G-130" { 100mm } else if id == "G-176" { 46mm } else { 62mm }

#let pictures(q, small: false) = {
  if q.images == none { return }
  let im = q.images
  if im.layout == "row" {
    grid(columns: (1fr,) * 4, column-gutter: 3mm,
      ..im.files.enumerate().map(((i, f)) => align(center, stack(spacing: 1mm,
        image(f, height: if small { 15mm } else { 22mm }),
        text(size: 7.5pt, "Bild " + str(i + 1))))))
  } else {
    align(center, image(im.files.first(), width: if small { single-width(q.id) * 0.75 } else { single-width(q.id) }))
  }
}

#let photo-box(num) = block(width: 100%, fill: pale, inset: 2.4mm, radius: 1mm, text(lang: "hr", size: 8.8pt)[
  *Fotografija nije otisnuta* (autorska prava treće strane). Pogledajte je u BAMF-ovu katalogu, pitanje #num – QR kod je na stranici #context counter(page).at(<qr>).first().])

#let question(q) = block(breakable: false, width: 100%, above: 4.6mm, below: 0mm)[
  #grid(columns: (10mm, 1fr), column-gutter: 1.5mm,
    align(left, box(inset: (x: 1.2mm, y: 0.9mm), stroke: 0.8pt + ink, radius: 1mm, text(weight: "bold", size: 8.6pt, q.label))),
    [
      #text(weight: "semibold", q.q_de)
      #linebreak()
      #bks(q.q_bks)
    ],
  )
  #if q.images != none { v(1.5mm); pad(left: 11.5mm, pictures(q)) }
  #if q.photo_missing { v(1.2mm); pad(left: 11.5mm, photo-box(q.num)) }
  #v(1.4mm)
  #grid(columns: (11.5mm, 6mm, 1fr), column-gutter: 0mm, row-gutter: 1.8mm,
    ..q.options.map(o => (
      [], letterbox(o.letter, filled: o.correct),
      if o.stack [
        #(if o.correct { text(weight: "bold", o.de) } else { o.de })
        #if o.bks != "" [ \ #bks(o.bks)]
      ] else [
        #(if o.correct { text(weight: "bold", o.de) } else { o.de }) #h(1.5mm) #bks(o.bks)
      ],
    )).flatten()
  )
  #v(1.4mm)
  #pad(left: 11.5mm, block(width: 100%, fill: pale, inset: (x: 2.6mm, y: 2mm), radius: 1mm)[
    #set text(size: s-expl)
    #set par(leading: 0.52em)
    #text(lang: "hr")[*Objašnjenje:* #q.expl]
    #linebreak()
    *Merksatz:* #emph(q.merksatz)
  ])
]

// exam-style question (German only, empty boxes)
#let exam-question(no, q) = block(breakable: false, above: 3.2mm, below: 0mm)[
  #grid(columns: (8mm, 1fr), column-gutter: 1mm,
    text(weight: "bold", str(no) + "."),
    [
      #text(weight: "semibold", q.q_de) #text(fill: soft, size: 7.5pt)[(Nr. #q.label)]
      #if q.images != none { v(1mm); pictures(q, small: true) }
      #if q.photo_missing [ #text(fill: soft, size: 7.8pt, lang: "hr")[– fotografija nije otisnuta, vidi QR kod na početku Dijela 3] ]
      #v(0.8mm)
      #grid(columns: (1fr, 1fr), column-gutter: 3mm, row-gutter: 1.3mm,
        ..q.options.map(o => grid(columns: (5mm, 1fr), column-gutter: 0.6mm, letterbox(o.letter, size: 3.8mm), o.de)))
    ],
  )
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
    #text(size: 11.5pt)[Alle 460 Fragen des BAMF-Fragenkatalogs\ (300 allgemeine Fragen + 10 Fragen je Bundesland)\ mit Übersetzung, Erklärungen, Merksätzen\ und 10 vollständigen Probetests]
    #v(9mm)
    #text(size: 11pt, lang: "hr", style: "italic")[Razumijte svako pitanje na svom jeziku:\ sva pitanja s prijevodom, objašnjenjima\ i 10 potpunih probnih testova]
    #v(1fr)
    #text(size: 9pt)[#R.edition · #val("edition_date")\ Fragenkatalog: Stand #val("catalog_stand")]
    #v(3mm)
    #text(size: 10pt, weight: "semibold", val("publisher"))
  ]
  #v(10mm)
]

// Copyright / imprint page – every statement reflects the checks actually done (kdp/release.json)
#page(header: none, footer: none)[
  #set text(size: 7.8pt)
  #set par(leading: 0.5em)
  #v(1fr)
  #if M.draft [
    #block(stroke: 1pt + ink, inset: 2mm, width: 100%)[*ENTWURF – NICHT ZUR VERÖFFENTLICHUNG.* Fehlende Angaben: #M.missing_release.join(", ")]
    #v(2mm)
  ]
  *Hinweis:* Dieses Buch ist keine Veröffentlichung des Bundesamts für Migration und Flüchtlinge (BAMF) und steht in keiner Verbindung zum BAMF.

  *Ausgabe:* #R.edition, #val("edition_date").

  *Fragen und Antworten:* #M.catalog_source, Stand #val("catalog_stand"). Die Fragen, Antwortmöglichkeiten und richtigen Antworten sind unverändert wiedergegeben (§ 5 Abs. 2 UrhG); Schreibweise nur typografisch angepasst. Satzgrundlage: öffentliche Kopie des Katalogs, abgerufen am #R.public_copy_retrieved, abgeglichen mit zwei weiteren unabhängigen Kopien. Abgleich mit dem offiziellen BAMF-PDF: #val("catalog_compared_on"). Maßgeblich ist allein der aktuelle Katalog des BAMF.

  *Abbildungen:* Wappen, Karten, Stimmzettel und Flaggen stammen aus dem Fragenkatalog des BAMF (Graustufen). Sie werden nur als Gegenstand der Prüfungsfragen gezeigt. Ein Foto Dritter (Frage 55) ist nicht abgedruckt.

  *Übersetzungen, Erklärungen und Merksätze:* mit Unterstützung durch künstliche Intelligenz erstellt; automatisch und durch unabhängige KI-Gegenprüfungen kontrolliert. Menschliches Lektorat: #if R.human_proofread_by == none [ausstehend] else [#R.human_proofread_by, #R.human_proofread_date].

  Alle Angaben ohne Gewähr. Das Buch ersetzt keine Beratung durch die Einbürgerungsbehörde.

  © #val("publisher") (Übersetzungen, Erklärungen, Merksätze, Gestaltung). Alle Rechte vorbehalten.\
  Verantwortlich / Hersteller (GPSR): #val("publisher"), #val("address"), #val("email")\
  ISBN: #val("isbn")
  #v(6mm)
]

#outline(title: [Sadržaj / Inhalt], depth: 2, indent: 4mm)

// ---------- introduction ----------
#section.update("Uvod")
#set text(lang: "hr")
= Uvod

== O testu

Test *„Leben in Deutschland”* (Život u Njemačkoj, LiD) polaže se na kraju integracijskog tečaja, a *Einbürgerungstest* (test naturalizacije) prije stjecanja njemačkog državljanstva. Oba testa koriste *isti katalog od 310 pitanja*: 300 općih pitanja i 10 pitanja o saveznoj pokrajini u kojoj živite. Ova knjiga sadrži cijeli katalog: 300 općih pitanja i pitanja za *svih 16 pokrajina*.

- Test ima *33 pitanja*: 30 općih i 3 o Vašoj pokrajini. Imate *60 minuta*.
- Za svako pitanje ponuđena su 4 odgovora; točan je uvijek samo jedan.
- *Koliko točnih odgovora trebate:*
  - *17 od 33* – dokaz znanja za *naturalizaciju* (Einbürgerungstest ili LiD s 17 točnih).
  - *15 od 33* – položen test *LiD na kraju orijentacijskog tečaja*.
- Test se polaže *na njemačkom jeziku*. Zato u ovoj knjizi njemački tekst uvijek stoji prvi.
- Pristojba za Einbürgerungstest iznosi 25 €. Prijavljujete se u ispitnom centru, npr. u pučkom učilištu (Volkshochschule). Neke osobe su oslobođene testa (npr. nakon završene njemačke škole) – to provjerite u svom uredu za naturalizaciju.

== Kako koristiti ovu knjigu

- *Masno:* pitanje na njemačkom, točno kako je u katalogu. Ispod njega, u *kurzivu*: prijevod.
- Četiri odgovora označena s A–D. *Crni kvadratić i masna slova* označavaju točan odgovor. Uz svaki odgovor je prijevod; kod dužih odgovora prijevod je u zasebnom redu.
- *Objašnjenje* kaže zašto je odgovor točan – razumijevanje se pamti bolje od napamet naučenih slova.
- *Merksatz* je kratka njemačka rečenica za pamćenje. Pročitajte je naglas.

Prije učenja pogledajte stranice *Moja pokrajina*, *Plan učenja*, *Pazi na riječ*, *Tko je tko u državi* i *Vremenska crta*. Na kraju knjige su *10 potpunih probnih testova* (30 + 3 pitanja, s listom za odgovore), *tablica pogrešaka* i *tematsko kazalo*.

== Aktualnost i provjera sadržaja

#table(columns: (auto, 1fr), stroke: 0.4pt + luma(160), inset: 1.8mm,
  [*Izdanje knjige*], [#R.edition, #val("edition_date")],
  [*Stanje službenog kataloga*], [#val("catalog_stand") (datum otisnut na BAMF-ovu PDF-u)],
  [*Posljednja usporedba sa službenim PDF-om*], [#val("catalog_compared_on")],
  [*Podloga za slog*], [javna kopija BAMF-ova kataloga preuzeta #R.public_copy_retrieved, uspoređena s još dvije neovisne kopije; ključ odgovora potvrđen za svih 460 pitanja],
  [*Provjere prijevoda i objašnjenja*], [automatska provjera; neovisne provjere drugim AI modelima (slijepo rješavanje bez ključa, provjera preciznosti); ljudska lektura: #if R.human_proofread_by == none [još nije provedena] else [#R.human_proofread_by, #R.human_proofread_date]],
)
Katalog se povremeno mijenja (npr. pitanja o aktualnim dužnosnicima). Prije ispita usporedite pitanja na www.bamf.de.

== Slikovna pitanja <qr>

#grid(columns: (1fr, 26mm), column-gutter: 4mm,
  [Grbovi, karte, glasački listići i zastave preuzeti su iz službenog kataloga i otisnuti u sivim tonovima. U ispitu su u boji – boje su opisane u objašnjenjima. *Jedna fotografija (pitanje 55)* zaštićena je autorskim pravom treće strane i nije otisnuta: pogledajte je u BAMF-ovu katalogu (QR kod desno ili #M.catalogue_url), a zatim potražite pitanje broj 55.],
  image("/layout/images/qr_catalogue.svg", width: 26mm),
)

== Napomene

- *Prijevod:* radi čitljivosti za osobe koristimo muški rod, koji se odnosi na oba spola. Nazivi njemačkih institucija ostaju na njemačkom, s objašnjenjem u zagradi. Tekst je pisan ijekavicom i latinicom.
- *Brojevi pitanja* odgovaraju brojevima u BAMF-ovu katalogu, pa pitanja lako pronađete i u aplikacijama.

#set text(lang: "de")
== Vorwort (Deutsch)

Dieses Buch enthält alle 460 Fragen des Gesamtfragenkatalogs zum Test „Leben in Deutschland“ und zum Einbürgerungstest. Zu jeder Frage finden Sie die Übersetzung ins Bosnische/Kroatische/Serbische, die richtige Antwort, eine kurze Erklärung und einen Merksatz auf Deutsch. Am Ende stehen 10 vollständige Probetests (30 allgemeine + 3 Landesfragen) mit Antwortbogen und Lösungen. Viel Erfolg!

// ---------- before you start ----------
#set text(lang: "hr")
#section.update("Prije početka · Vor dem Lernen")
= Prije početka

== Moja pokrajina

Na ispitu dobivate 3 pitanja o pokrajini u kojoj živite. *Označite svoju pokrajinu* i učite samo njezinih 10 pitanja.

#table(columns: (8mm, 1fr, 18mm), stroke: 0.4pt + luma(160), inset: 1.6mm,
  [], [*Pokrajina / Bundesland*], [*Stranica*],
  ..data.states.map(s => ([#box(width: 3.6mm, height: 3.6mm, stroke: 0.6pt)], [#s.name #text(fill: soft)[· #s.bks_name]], context [#counter(page).at(label("state-" + s.code)).first()])).flatten()
)

U svim pokrajinama pitanja slijede isti raspored:
#enum(..data.state_pattern.map(p => [#p]))

#pagebreak(weak: true)
== Plan učenja

#let plan14 = (
  ..range(10).map(i => ([#(i + 1).], [#(30 * i + 1)–#(30 * i + 30)], [pogreške od jučer])),
  ([11.], [pitanja moje pokrajine], [Probetest 1, 2]),
  ([12.], [–], [Probetest 3, 4, 5]),
  ([13.], [–], [Probetest 6, 7, 8]),
  ([14.], [–], [Probetest 9, 10 + označena pitanja]),
)
#let plan30 = (
  ..range(20).map(i => ([#(i + 1).], [#(15 * i + 1)–#(15 * i + 15)], [pogreške])),
  ([21.], [moja pokrajina], [pogreške]),
  ..range(8).map(i => ([#(22 + i).], [–], [Probetest #(i + 1)])),
  ([30.], [–], [Probetest 9, 10]),
)
Učite po planu i svaki dan ponovite pitanja na kojima ste pogriješili. Brojevi su brojevi općih pitanja.
#set text(size: 8.4pt)
#grid(columns: (1fr, 1fr), column-gutter: 5mm,
  [=== Plan za 14 dana
   #table(columns: (8mm, 17mm, 1fr), stroke: 0.4pt + luma(170), inset: 1.3mm, [*Dan*], [*Nova pitanja*], [*Ponavljanje · test*], ..plan14.flatten())],
  [=== Plan za 30 dana
   #table(columns: (8mm, 17mm, 1fr), stroke: 0.4pt + luma(170), inset: (x: 1.3mm, y: 0.9mm), [*Dan*], [*Nova pitanja*], [*Ponavljanje · test*], ..plan30.flatten())],
)
#set text(size: s-de)
Svako pogrešno pitanje upišite u *tablicu pogrešaka* na kraju knjige i ponovite ga nakon 1, 3 i 7 dana.

#pagebreak(weak: true)
== Pazi na riječ

Neke male riječi potpuno mijenjaju smisao pitanja. Brojevi su pitanja u kojima se riječ pojavljuje.

#set text(size: 9pt)
#table(columns: (27mm, 1fr), stroke: 0.4pt + luma(170), inset: 1.6mm,
  ..data.words.map(w => ([#text(lang: "de", weight: "bold", w.de)], [#w.bks #linebreak() #text(fill: soft, size: 7.8pt)[Pitanja: #w.nums.map(str).join(", ")]])).flatten()
)
#set text(size: s-de)

#pagebreak(weak: true)
== Tko je tko u njemačkoj državi

#let org(t, s) = block(width: 100%, stroke: 0.8pt + ink, radius: 1.2mm, inset: 2mm, [#text(weight: "bold", lang: "de", t) #linebreak() #text(size: 8.6pt, s)])
#let arrow(t) = align(center, text(size: 8.4pt, fill: soft)[↓ #t])
#grid(columns: (1fr, 1fr), column-gutter: 5mm, row-gutter: 1.6mm,
  org("Wahlberechtigte", "birači – za Bundestag od 18 godina"), org("Wahlberechtigte im Land", "birači u pokrajini"),
  arrow("biraju svake 4 godine"), arrow("biraju"),
  org("Bundestag", "savezni parlament: zakoni, proračun, kontrola vlade"), org("Landtag", "pokrajinski parlament"),
  arrow("bira kancelara (na prijedlog predsjednika)"), arrow("bira šefa pokrajinske vlade"),
  org("Bundesregierung", "kancelar + ministri; ministre imenuje savezni predsjednik na prijedlog kancelara"), org("Landesregierung", "pokrajinska vlada"),
  [], arrow("šalje svoje članove"),
  [], org("Bundesrat", "pokrajine sudjeluju u saveznim zakonima"),
)
#v(2mm)
#grid(columns: (1fr, 1fr), column-gutter: 5mm, row-gutter: 1.6mm,
  org("Bundesversammlung", "zastupnici Bundestaga + jednako toliko predstavnika pokrajina"), org("Bundesverfassungsgericht", "Savezni ustavni sud: čuva Temeljni zakon"),
  arrow("bira na 5 godina"), align(center, text(size: 8.4pt, fill: soft)[↑ suce biraju Bundestag i Bundesrat, pola-pola]),
  org("Bundespräsident", "šef države: potpisuje zakone, imenuje kancelara i ministre"), [],
)

#v(3mm)
#set text(size: 8.8pt)
#table(columns: (30mm, 1fr, 34mm), stroke: 0.4pt + luma(170), inset: 1.5mm,
  [*Institucija*], [*Što radi · tko je bira*], [*Pitanja*],
  ..data.institutions.map(i => ([#text(lang: "de", weight: "bold", i.name) \ #i.bks], [#i.does. #linebreak() _Bira:_ #i.who.], [#text(size: 7.8pt, i.nums.map(str).join(", "))])).flatten()
)
#set text(size: s-de)

#pagebreak(weak: true)
== Vremenska crta

#for e in data.timeline {
  block(breakable: false, above: 2.2mm, below: 0mm,
    grid(columns: (24mm, 1fr), column-gutter: 3mm,
      align(right, text(weight: "bold", e.year)),
      [#e.text #text(fill: soft, size: 7.8pt)[(pitanja #e.nums.map(str).join(", "))]]))
}

// ---------- part 1: general questions ----------
#set text(lang: "de")
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
  [#heading(level: 2, s.name)#label("state-" + s.code)]
  for q in s.questions { question(q) }
}

// ---------- part 3: full exam simulations ----------
#section.update("Probetests · Probni testovi")
= Teil 3: 10 Probetests
#subtitle[Dio 3: 10 potpunih probnih testova]
#set text(lang: "hr")
Svaki probni test izgleda kao pravi ispit: *33 pitanja, 60 minuta*, samo na njemačkom.

+ Pitanja *1–30* su opća pitanja (zajedno 10 testova pokrivaju svih 300 općih pitanja).
+ Pitanja *31–33* uzmite iz *Dodatka A* (pitanja o pokrajinama bez označenih odgovora): za svaki test naveden je koja tri pitanja Vaše pokrajine rješavate.
+ Odgovore upisujte u *list za odgovore* iza svakog testa, a ne u knjigu – tako test možete ponoviti.
+ Izmjerite vrijeme. Zatim provjerite rješenja na kraju ovog dijela.

#note[*Rezultat:* *17 ili više točnih* – ispunjen je uvjet znanja za naturalizaciju. *15 ili više* – položen je test LiD na kraju orijentacijskog tečaja. *Pitanje 55* prikazuje fotografiju koja u knjizi nije otisnuta – prije testa je pogledajte u BAMF-ovu katalogu (QR kod na stranici #context counter(page).at(<qr>).first()). Ostale slike su otisnute uz pitanja.]

#let fill-line(w) = box(width: w, height: 3mm, stroke: (bottom: 0.5pt))
#let answer-sheet(t) = page(header: none)[
  #set text(size: 9pt, lang: "hr")
  #text(size: 13pt, weight: "bold")[Probetest #t.n – list za odgovore]
  #h(1fr) #text(size: 9pt)[Datum: #fill-line(30mm)]
  #v(3mm)
  #let row(no, lab) = (text(weight: "bold", str(no)), text(size: 7.5pt, fill: soft, lab), ..("A", "B", "C", "D").map(l => letterbox(l, size: 4.6mm)))
  #let rows = range(33).map(i => if i < 30 { row(i + 1, "Nr. " + t.questions.at(i).label) } else { row(i + 1, "Land, Nr. " + str(t.state_nums.at(i - 30))) })
  #grid(columns: (1fr, 1fr), column-gutter: 8mm,
    table(columns: (7mm, 20mm, 7mm, 7mm, 7mm, 7mm), stroke: none, inset: (y: 1.45mm, x: 0.6mm), align: horizon, ..rows.slice(0, 17).flatten()),
    table(columns: (7mm, 20mm, 7mm, 7mm, 7mm, 7mm), stroke: none, inset: (y: 1.45mm, x: 0.6mm), align: horizon, ..rows.slice(17).flatten()),
  )
  #v(1fr)
  #block(width: 100%, stroke: 0.8pt, radius: 1.2mm, inset: 3mm)[
    *Točnih odgovora:* #fill-line(14mm) / 33 #h(8mm) *Vrijeme:* #fill-line(14mm) min (najviše 60)
    #v(1.5mm)
    ☐ 17 ili više: uvjet znanja za naturalizaciju ispunjen #h(4mm) ☐ 15 ili više: položen test LiD (orijentacijski tečaj)
  ]
]

#set text(lang: "de")
#for t in data.tests {
  pagebreak(weak: true)
  [== Probetest #t.n]
  set text(size: 9.2pt)
  for (i, q) in t.questions.enumerate() { exam-question(i + 1, q) }
  v(3mm)
  note[*Fragen 31–33:* Aus *Anhang A* die Fragen *#t.state_nums.map(str).join(", ")* Ihres Bundeslandes lösen. \ #text(style: "italic")[Pitanja 31–33: iz Dodatka A riješite pitanja *#t.state_nums.map(str).join(", ")* svoje pokrajine.]]
  answer-sheet(t)
}

// ---------- appendix A: state questions without answers ----------
= Anhang A: Landesfragen ohne Lösungen
#subtitle[Dodatak A: pitanja o pokrajinama za probne testove (bez rješenja)]
#for s in data.state_appendix {
  block(breakable: false, above: 5mm, below: 1mm, text(size: 11.5pt, weight: "bold", s.name))
  set text(size: 9pt)
  for q in s.questions { exam-question(q.num, q) }
}

// ---------- solutions ----------
#pagebreak(weak: true)
== Lösungen · Rješenja
#set text(size: 8.6pt)
#for t in data.tests {
  block(breakable: false, above: 3mm)[
    *Probetest #t.n* #h(2mm) #text(fill: soft)[(Frage: Antwort — Nr. im Katalog) · Fragen 31–33: Landesfragen #t.state_nums.map(str).join(", ") (Tabelle unten)]
    #v(0.8mm)
    #grid(columns: (1fr,) * 6, column-gutter: 1mm, row-gutter: 1.1mm,
      ..t.questions.enumerate().map(((i, q)) => [*#(i + 1):* #q.answer #text(fill: soft, size: 7pt)[(#q.label)]])
    )
  ]
}
#v(4mm)
=== Landesfragen · Pitanja o pokrajinama
#table(columns: (1fr,) + (6.5mm,) * 10, stroke: 0.4pt + luma(170), inset: 1.2mm, align: center,
  [*Bundesland*], ..range(10).map(i => [*#(i + 1)*]),
  ..data.state_key.map(s => (align(left, s.name), ..s.answers.map(a => [#a]))).flatten()
)

// ---------- mistakes log ----------
#set text(size: s-de, lang: "hr")
#section.update("Tablica pogrešaka · Fehlerliste")
= Tablica pogrešaka
#subtitle[Fehlerliste – ponavljanje nakon 1, 3 i 7 dana]
Upišite broj svakog pitanja na kojem ste pogriješili i zašto (riječ koju niste razumjeli, zamjena pojmova, niste znali). Kad pitanje ponovite, označite kvadratić.
#let blank = box(width: 3.8mm, height: 3.8mm, stroke: 0.6pt)
#for _ in range(2) {
  table(columns: (16mm, 1fr, 18mm, 12mm, 12mm, 12mm), stroke: 0.4pt + luma(150), inset: (y: 2.35mm, x: 1.2mm), align: horizon,
    [*Br. pitanja*], [*Zašto sam pogriješio/la*], [*Datum*], [*+1 dan*], [*+3 dana*], [*+7 dana*],
    ..range(24).map(_ => ([], [], [], align(center, blank), align(center, blank), align(center, blank))).flatten())
  pagebreak(weak: true)
}

// ---------- thematic index ----------
#section.update("Tematsko kazalo · Themenregister")
= Tematsko kazalo
#subtitle[Themenregister – ciljano ponavljanje po temama]
Griješite li često u nekoj temi, ponovite sva njezina pitanja. Brojevi su brojevi općih pitanja; pitanja o pokrajinama su u Dijelu 2.
#set text(size: 8.8pt)
#for tp in data.topics {
  block(breakable: false, above: 3mm)[
    *#tp.bks* #text(fill: soft, lang: "de")[· #tp.de] #text(fill: soft)[(#tp.nums.len() pitanja#if tp.state_count > 0 [ + #tp.state_count pitanja o pokrajinama])] \
    #text(size: 8pt, tp.nums.map(str).join(", "))
  ]
}

// ---------- glossary ----------
#set text(size: s-de)
#section.update("Glossar · Pojmovnik")
= Glossar Deutsch – BKS
#subtitle[Pojmovnik njemački – BKS]
#set text(size: 8.8pt)
#columns(2, gutter: 6mm)[
  #for g in data.glossary {
    block(breakable: false, below: 1.8mm)[#text(lang: "de", weight: "bold", g.de) \ #text(lang: "hr", g.bks)]
  }
]
