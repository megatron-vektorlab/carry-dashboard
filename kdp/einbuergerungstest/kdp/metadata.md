# KDP – podaci za unos (izdanje DE–BKS, meki uvez)

> Postupak objave korak po korak: `kdp/objava_korak_po_korak.md`. Pravila računa: jedan KDP račun po osobi; najviše 2 nova naslova tjedno po formatu (od 21. 9. 2026.).

> Sve s oznakom **[provjeriti]** potvrdite u KDP-u prije objave.

## Osnovno
| Polje | Vrijednost |
|---|---|
| Jezik knjige | **Njemački** (Deutsch). Hrvatski/bosanski/srpski vjerojatno nije KDP-ov podržani jezik; njemački tekst je izvornik i čini veći dio knjige. [provjeriti na stranici „Book Supported Languages”] |
| Naslov | Einbürgerungstest & Leben in Deutschland |
| Podnaslov | Deutsch – Bosnisch/Kroatisch/Serbisch: Alle 460 Fragen mit Übersetzung, Erklärung und Bildern (oba dijela stoje na naslovnici) |
| Serija | Einbürgerungstest zweisprachig (svezak: Deutsch–BKS) |
| Izdanje | 1 |
| Autor / suradnici | Ime izdavača ili urednika (**ne** navoditi BAMF). Uloga „Übersetzer” za odgovornog urednika. |
| Opis | vidi dolje |
| Publishing rights | „I own the copyright…” za prijevode, objašnjenja i dizajn; pitanja su javno službeno djelo (§ 5 Abs. 2 UrhG) i to je navedeno u impresumu. |
| Primarno tržište | Amazon.de (zatim .at; .com nije ciljano) |
| Format | Meki uvez, 6,69 × 9,61 in (17 × 24,4 cm), crno-bijeli tisak, bijeli papir, bez „bleeda”, mat naslovnica |
| ISBN | Besplatni KDP ISBN (impresum tada glasi „Independently published”) ili vlastiti ISBN |
| Cijena | Prijedlog **16,99 €** (Amazon.de): knjiga sada ima ~311 stranica. Honorar ≈ 60 % × (16,99 / 1,07) − trošak tiska (≈ 1,00 € + 0,012 € po stranici ≈ 4,7 €) ≈ 4,8 €. Pri 14,99 € honorar bi bio ≈ 3,7 €. [provjeriti u KDP kalkulatoru] |

## Prijava AI-ja (obavezno)
- **Text: AI-generated → Yes** (prijevodi, objašnjenja, Merksätze). Opis alata: „Claude (Anthropic)”. Ljudsku lekturu upišite tek kad je stvarno obavljena.
- **Translations: AI-generated → Yes.**
- **Images: No** – slike u knjizi preuzete su iz BAMF-ova kataloga (nisu nastale AI-jem), naslovnica je tipografska. Ako ste u nedoumici, označite „Yes” – prijava nije javna.

## Ključne riječi (7 polja, do 50 znakova)
1. einbürgerungstest kroatisch
2. leben in deutschland test bosnisch serbisch
3. einbürgerungstest fragen antworten übersetzung
4. test leben in deutschland buch 2026
5. einbürgerung vorbereitung zweisprachig
6. test za državljanstvo njemačka
7. einbürgerungstest alle bundesländer probetest

## Kategorije (3) [provjeriti u KDP-ovu stablu kategorija]
- Bücher › Schule & Lernen › Deutsch als Fremdsprache
- Bücher › Fachbücher › Recht › (Ausländer- / Staatsangehörigkeitsrecht)
- Bücher › Sprachen lernen › Kroatisch / Serbisch / Bosnisch

## Opis (Amazon, njemački + BKS)
```html
<b>Alle 460 Fragen zum Test „Leben in Deutschland“ und zum Einbürgerungstest – auf Deutsch, mit Übersetzung ins Bosnische/Kroatische/Serbische.</b>
<br><br>
Die Prüfung ist auf Deutsch. Dieses Buch hilft Ihnen, jede Frage wirklich zu verstehen:
<ul>
<li>Alle 300 allgemeinen Fragen und die 10 Fragen jedes der 16 Bundesländer</li>
<li>Jede Frage und jede Antwort mit Übersetzung</li>
<li>Die richtige Antwort markiert und in einfachen Worten erklärt</li>
<li>Ein kurzer Merksatz auf Deutsch zu jeder Frage</li>
<li>10 vollständige Prüfungssimulationen (30 + 3 Fragen) mit Antwortbogen und Lösungen</li>
<li>Wappen, Karten und Stimmzettel der Bildfragen abgedruckt</li>
<li>Lernplan für 14 und 30 Tage, Fehlerliste, Themenregister, Glossar Deutsch – BKS</li>
</ul>
<b>Sva pitanja za test naturalizacije i test „Život u Njemačkoj”</b> – njemački original, prijevod, označen točan odgovor, kratko objašnjenje i 10 probnih testova s rješenjima.
<br><br>
<i>Keine offizielle Publikation des BAMF. Fragen und Antworten: BAMF-Gesamtfragenkatalog, unverändert wiedergegeben. Maßgeblich ist der aktuelle Katalog auf bamf.de.</i>
```

## A+ sadržaj (prijedlog)
1. Slika jedne stranice s pitanjem (izrezak iz `out/interior_de-bks.pdf`, npr. pitanje 1) s natpisom „So ist jede Frage aufgebaut”.
2. Stranica probnog testa + stranica s rješenjima.
3. Traka „33 Fragen · 60 Minuten · ab 17 richtig bestanden”.

## E-knjiga (Kindle eBook)
Datoteke: `out/ebook_de-bks.epub` (manuskript) i `out/ebook_cover_de-bks.jpg` (naslovnica 1600 × 2560 px).
U KDP-u: **+ Create → Kindle eBook**, isti naslov, podnaslov, autor, serija i izdanje kao meki uvez – tada
Amazon obje verzije spaja na jednoj stranici proizvoda (inače: KDP podrška → „Link print and Kindle”).

| Polje | Vrijednost |
|---|---|
| Jezik | **Njemački** (kao meki uvez) |
| ISBN | Nije potreban (Amazon dodjeljuje ASIN); ne upisujte ISBN mekog uveza |
| Manuskript | EPUB (`out/ebook_de-bks.epub`); EPUBCheck: 0 grešaka. Nakon učitavanja otvorite **Launch Previewer** i pregledajte slikovna pitanja, tablice i poveznice |
| Naslovnica | „Upload a cover you already have” → `out/ebook_cover_de-bks.jpg` |
| DRM | Po izboru (ne može se kasnije promijeniti). Bez DRM-a kupci mogu čitati i na drugim uređajima |
| Prijava AI-ja | Ista kao za meki uvez (tekst i prijevodi: AI-generated → Yes; slike: No) |
| Ključne riječi, kategorije | Iste kao za meki uvez; kategorije birajte u stablu „Kindle-Shop” [provjeriti] |
| KDP Select | Po izboru: 90 dana ekskluzivno na Amazonu (vrijedi samo za e-knjigu, ne za meki uvez), zauzvrat Kindle Unlimited (plaćanje po pročitanim stranicama) i promocije. Ako e-knjigu prodajete **samo na Amazonu**, prijedlog je **uključiti** – ekskluzivnost tada ništa ne košta [vaša odluka] |
| Cijena | Prijedlog **7,99 €** (Amazon.de) – opcija honorara **70 %** (dopuštena za 2,99–9,99 €) [provjeriti] |
| Honorar (procjena) | 7,99 € s 7 % PDV-a = 7,47 € neto; trošak dostave ≈ 0,12 €/MB × ~3,3 MB ≈ 0,40 €; 70 % × (7,47 − 0,40) ≈ **4,95 €** po prodaji. KDP prikazuje stvarnu veličinu datoteke nakon pretvorbe [provjeriti] |
| Pravilo cijene | Za 70 % e-knjiga mora biti barem 20 % jeftinija od mekog uveza (16,99 € → najviše 13,59 €); 7,99 € to ispunjava |

### Opis e-knjige (zamjena za popis u opisu mekog uveza)
```html
<li>10 vollständige Prüfungssimulationen (30 + 3 Fragen) mit Lösungen – jede Lösung führt per Klick zur Frage mit Erklärung</li>
<li>Wappen, Karten und Stimmzettel der Bildfragen enthalten</li>
<li>Lernplan für 14 und 30 Tage, Themenregister und Zeitleiste mit anklickbaren Fragenummern, Glossar Deutsch – BKS</li>
```
Ostatak opisa (naslov, uvod, prve četiri točke, BKS dio, napomena o BAMF-u) isti je kao za meki uvez.
