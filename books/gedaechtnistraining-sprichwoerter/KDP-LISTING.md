# KDP unos: Sprichwörter und Redewendungen für Senioren (Band 1)

Vrijednosti za kopiranje u Amazon KDP: „Paperback Details”, „Paperback Content” i „Rights & Pricing”.
Upute za cijeli postupak su u `README.md`.
Datoteku stvara `python3 -m gt.build` iz predloška `content/kdp_listing.tmpl.md`. Mijenjajte predložak, ne ovu datoteku.

## Paperback Details

| Polje | Vrijednost |
|---|---|
| Language | **German** |
| Book Title | **Sprichwörter und Redewendungen für Senioren** |
| Subtitle | **Gedächtnistraining in Großdruck: 100 Kopiervorlagen in A4 mit Lösungen und Gesprächsimpulsen** |
| Series | **Gedächtnistraining für Senioren in Großdruck**, broj **1** (polje „Series” → „Add series”; na naslovnici i u knjizi piše „Band 1”) |
| Edition Number | 1 |
| Author | Ivan Sikuten *(mora odgovarati naslovnici i naslovnoj stranici)* |
| Contributors | ništa |
| Publishing Rights | **I own the copyright and I hold the necessary publishing rights** |
| Primary Audience | Sexually explicit: No · Reading age: ostaviti prazno (odrasli) |
| Primary Marketplace | **Amazon.de** |
| Low-content book | **No** |
| Large-print book | **Yes**: sav tekst u knjizi ima najmanje 16 pt (`python3 -m gt.qa` to provjerava) |

Naslov i podnaslov zajedno imaju 135 znakova (KDP dopušta do 200).

### Description (Beschreibung)

KDP-ov uređivač opisa je „rich text”. Zalijepite tekst i provjerite pregled; ako se oznake poput `<b>` vide doslovno, koristite gumbe alatne trake.

```html
<b>100 Kopiervorlagen in A4 rund um bekannte Sprichwörter und Redewendungen – für die Gruppenstunde, zu zweit oder allein.</b>

<p>„Morgenstund hat Gold im Mund“, „Da liegt der Hund begraben“: Sprichwörter und Redewendungen sitzen tief im Gedächtnis. Sie wecken Erinnerungen und bringen Menschen zum Lachen und ins Gespräch. Dieses Buch macht daraus 100 abwechslungsreiche Arbeitsblätter in drei Stufen, mit allem, was die Gruppenleitung braucht.</p>

<h4>Das steckt im Buch</h4>
<ul>
<li><b>100 Arbeitsblätter in 10 Themen:</b> Tiere, Körper, Essen & Trinken, Haus, Hof & Garten, Wetter, Natur & Jahreszeiten, Arbeit & Fleiß, Geld & Glück, Reden & Schweigen, Familie & Freundschaft sowie Zeit & Lebensweisheiten.</li>
<li><b>Echtes A4-Format:</b> jedes Blatt eine Kopiervorlage auf einer rechten Seite, mit breitem Innenrand zum Kopieren, gern auch auf A3 vergrößert.</li>
<li><b>Auf der Rückseite jedes Blattes:</b> die Lösungen mit gängigen Varianten, Hilfen, wenn ein Wort nicht einfällt, Fragen zum Gespräch und Ideen, wie die Aufgabe leichter oder anspruchsvoller wird.</li>
<li><b>Drei Stufen:</b> von „Wörter zur Auswahl“ bis „frei ergänzen“. Jedes Blatt der ersten und zweiten Stufe beginnt mit einem gelösten Beispiel.</li>
<li><b>11 Aufgabenarten:</b> Was fehlt?, Das richtige Wort, Was gehört zusammen?, Vorlesegeschichten, Da stimmt was nicht!, Was bedeutet das?, Wortsalat, Wie geht es weiter?, Erste Buchstaben, Wann sagt man das? und Wörter suchen.</li>
<li><b>Großdruck:</b> Aufgaben in 20 Punkt, nichts kleiner als 16 Punkt, klare serifenlose Schrift, reines Schwarz auf Weiß, keine grauen Flächen.</li>
<li><b>Zu jedem Kapitel:</b> eine Aufwärmrunde zum Vorlesen, Gesprächsfragen, Bewegungsideen und Vorschläge zum Mitbringen.</li>
<li><b>Hinweise für die Gruppenleitung</b>, ein Beispiel für eine Stunde von 45 Minuten und ein Verzeichnis aller 357 Sprichwörter und Redewendungen von A bis Z.</li>
<li><b>Kopiererlaubnis</b> für die eigene Einrichtung oder Gruppe.</li>
</ul>

<p>Für Betreuungskräfte und Alltagsbegleiter, Ergotherapie, Tagespflege, Seniorengruppen und für Angehörige, die zu Hause gemeinsam rätseln möchten. Auch für Menschen mit beginnender Demenz geeignet: ohne Leistungsdruck und mit vielen Erfolgserlebnissen.</p>
```

Riječ „Demenz” stoji samo u opisu, ne u knjizi ni na naslovnici. Recenzenti konkurentskih knjiga žale se kada je otisnuta u knjizi. Opis ne obećava nikakav zdravstveni učinak (njemački HWG): nema „gegen Demenz”, „vorbeugen” ni „wissenschaftlich bewiesen”.

### Keywords (7 polja)

Riječi iz naslova i podnaslova (Sprichwörter, Redewendungen, Senioren, Gedächtnistraining, Großdruck, Kopiervorlagen …) Amazon ionako indeksira, pa polja nose druge pojmove:

1. `sprichwörter ergänzen rätsel gruppe`
2. `redewendungen bedeutung gedächtnisspiel`
3. `rätselbuch senioren große schrift a4`
4. `demenz beschäftigung arbeitsblätter`
5. `betreuungskraft alltagsbegleiter aktivierung`
6. `seniorenbeschäftigung tagespflege ideen`
7. `geschenk oma opa gehirnjogging`

Nema zaštićenih imena ni imena konkurenata. „Herkunft” je namjerno izostavljen jer knjiga ne objašnjava podrijetlo izreka.

### Categories (3)

U KDP-ovom izborniku kategorija potražite (nazivi su iz istraživanja; točan njemački put provjerite u izborniku):

1. **Gedächtnistraining** (Ratgeber)
2. **Geriatrie** ili **Gerontologische Pflege** (Medizin › Pflege)
3. **Sprichwörter** (Sprachwissenschaft / Nachschlagewerke; manja konkurencija, realna šansa za oznaku „Bestseller” u kategoriji)

Alternative: Alzheimer, Ergotherapie.

## Paperback Content

| Polje | Vrijednost |
|---|---|
| ISBN | **Get a free KDP ISBN** (najjednostavnije; izdavač tada glasi „Independently published”). Alternativa: kao hrvatski izdavač možete besplatno dobiti ISBN od Nacionalne i sveučilišne knjižnice (NSK). Odlučite prije prvog slanja, jer se ISBN poslije ne može promijeniti. |
| Publication Date | ostaviti prazno (= danas) |
| Print Options | **Black & white interior**, **white paper** |
| Trim Size | **A4: 21 × 29,7 cm (8,27 × 11,69 in)** (u izborniku „Select a different size”) |
| Bleed Settings | **No bleed** |
| Paperback cover finish | **Matte** (manje odsjaja za slabovidne čitatelje) |
| Manuscript | `output/Sprichwoerter-Redewendungen-Senioren-interior.pdf` |
| Book Cover | „Upload a cover you already have” → `output/Sprichwoerter-Redewendungen-Senioren-cover.pdf` |
| AI-Generated Content | **Yes.** Texts: *Some sections, with minimal or no editing*. Napisao ih je AI model (Claude): upute, objašnjenja značenja, pomoć, pitanja za razgovor, 10 priča, uvodi poglavlja i tekstovi korica. Ako ih sami preradite, promijenite u „with extensive editing”. Images: *One or a few AI-generated images, with minimal or no editing* (naslovnicu i grafike nacrtao je kod koji je napisala umjetna inteligencija). Translations: *None*. Same poslovice i izreke su narodna predaja; vježbe je složio deterministički program. |

Širina hrpta izračunata je iz broja stranica unutrašnjosti (240 stranica, hrbat 0.5405 in). Ako se unutrašnjost promijeni, ponovno izgradite sve naredbom `python3 -m gt.build` prije učitavanja. KDP odbija naslovnicu čiji hrbat ne odgovara.

## Rights & Pricing

* Territories: **All territories (worldwide rights)**.
* Royalty: **60 %**.
* Preporučena cijena na Amazon.de: **18,99 €** s PDV-om. KDP traži cijenu **bez PDV-a**, a stopa ovisi o tome kako Amazon razvrsta knjigu:
  * uz 7 % (obična knjiga): unesite **17,75 €**;
  * uz 19 % (knjige s vježbama mogu biti razvrstane kao „activity books”): unesite **15,96 €**.
  * Na zaslonu s cijenama KDP prikazuje procijenjenu stopu PDV-a; prema njoj odaberite iznos.
* **Fiksna cijena knjige (Buchpreisbindung)** vrijedi u Njemačkoj i Austriji: ista cijena svugdje, bez popusta (ni za domove), a vlastite primjerke krajnjim kupcima u DE/AT prodajete samo po punoj cijeni. Promjena cijene je dopuštena ako vrijedi za sve kanale. Tako možete početi sa 16,99 € radi prvih recenzija, a cijenu poslije podići.
* Procjena honorara (Amazon.de): 240 stranica, tisak = 0,75 € + 0,016 € × 240 = **4,59 €**.
  * Honorar = 60 % × 17,75 € − 4,59 € ≈ **6,06 € po prodanom primjerku** (uz 19 % PDV-a: ≈ 4,99 €).
  * Mjerodavan je KDP-ov kalkulator.
* Ostale trgovine: KDP preračunava cijene. Za Amazon.com predložite oko 19,99 $ (tisak $5.08).
* Expanded Distribution: isključeno (honorar bi bio gotovo nula).

## Slike za marketing

`output/front-cover.png` (naslovnica) i ogledne stranice u `output/marketing/`:
* jedan radni list s primjerom,
* stranica za voditelja,
* početak poglavlja,
* jedna priča.

Koristite ih za A+ Content i oglase.

## Nakon objave

* Najprije naručite tiskani probni primjerak (proof copy). Na običnom uredskom fotokopirnom stroju provjerite kopiraju li se listovi čisto i ne nestaje li tekst u pregibu.
* Sponsored Products oglasi: počnite s 3–5 € dnevno. Primjeri pojmova: `sprichwörter für senioren`, `sprichwörter und redewendungen für senioren`, `gedächtnistraining für senioren`, `beschäftigung für senioren im pflegeheim`.
* Molite prve čitatelje za iskrene recenzije. Nikada ne nudite novac ni besplatne primjerke u zamjenu za recenziju (Amazonova pravila).
