# Sprichwörter und Redewendungen für Senioren, Band 1

Ideja br. 4 s popisa KDP ideja: „Gedächtnistraining für Senioren in Großdruck, Band 1:
Sprichwörter & Redensarten” za Amazon.de. Nakon istraživanja tržišta naslov je promijenjen u točan
Amazonov prijedlog pretrage: **„Sprichwörter und Redewendungen für Senioren”**.
- Podnaslov: „Gedächtnistraining in Großdruck: 100 Kopiervorlagen in A4 mit Lösungen und Gesprächsimpulsen”.
- Serija: „Gedächtnistraining für Senioren in Großdruck”, Band 1.

Knjiga ima 100 radnih listova (Kopiervorlagen) u formatu A4. Namijenjena je njegovateljima i
voditeljima aktivnosti u domovima za starije i dnevnim boravcima (Betreuungskräfte,
Alltagsbegleiter, radni terapeuti) te obiteljima koje rješavaju zajedno kod kuće.

⟨STANJE⟩

## Gotove datoteke za KDP (`output/`)

| Datoteka | Za što |
|---|---|
| `Sprichwoerter-Redewendungen-Senioren-interior.pdf` | unutrašnjost, upload na KDP („Manuscript”) |
| `Sprichwoerter-Redewendungen-Senioren-cover.pdf` | omot (stražnja strana + hrbat + prednja strana, s bleedom), upload („Book cover”) |
| `front-cover.png` | prednja korica za oglase i A+ sadržaj |
| `marketing/*.png` | primjeri stranica: radni list, stranica za voditelja, početak poglavlja, priča |
| `../KDP-LISTING.md` | sve vrijednosti za KDP obrazac: njemački opis, ključne riječi, kategorije, cijena, PDV, AI-izjava |

## Što je u knjizi

| Dio | Sadržaj |
|---|---|
| Uvod | naslovna stranica, impresum s **dozvolom za kopiranje** i napomenom da vježbe nisu test ni terapija, sadržaj, „Willkommen!” (kako je knjiga složena, 3 razine, rad sam / u dvoje / u grupi), upute za voditelja grupe (stav bez ocjenjivanja, pomoć u 5 koraka, izbor razine, praktični savjeti, kad se jave osjećaji, kopiranje), primjer sata od 45 minuta, pregled listova po razini i vrsti zadatka, stranica „Meine Lieblingssprichwörter” |
| **10 poglavlja × 10 listova** | Tiere · Körper · Essen & Trinken · Haus, Hof & Garten · Wetter, Natur & Jahreszeiten · Arbeit & Fleiß · Geld & Glück · Reden & Schweigen · Familie & Freundschaft · Zeit & Lebensweisheiten |
| Početak poglavlja | kratki uvod, zagrijavanje „Ich sage den Anfang, Sie das Ende” (8 poslovica za čitanje naglas), pitanja za razgovor, ideje za kretanje, predmeti koje se može donijeti, popis listova |
| Svaki list | **desna stranica** = radni list (Kopiervorlage), **poleđina** = stranica za voditelja: tijek, rješenja s inačicama, pomoć ako se riječ ne sjeti, 2–3 pitanja za razgovor, lakša/teža inačica, napomena ako tema može biti osjetljiva |
| Kazalo | sve upotrijebljene poslovice i izreke od A do Ž s brojevima listova |

**Razine** (oznaka ◆ / ◆◆ / ◆◆◆ u podnožju, bez riječi „lako/teško” na listu): 40 / 40 / 20 listova.
Razina 1 uvijek ima okvir s riječima ili izbor između dvije riječi.

**Vrste zadataka** (po poglavlju je redoslijed uvijek sličan):
- Was fehlt? (s okvirom riječi, s kućicama za slova ili slobodno);
- Das richtige Wort (zaokruživanje između 2 ili 3 riječi);
- Was gehört zusammen? (spajanje početka i kraja);
- Vorlesegeschichte (10 kratkih priča koje završavaju poslovicom);
- Da stimmt was nicht! (jedna riječ je zamijenjena, šaljivo);
- Was bedeutet das? / Wann sagt man das? (izbor značenja ili prikladne poslovice);
- Wortsalat, Wie geht es weiter?, Erste Buchstaben, Wörter suchen.

Namjerno nema anagrama ni križaljki: istraživanje stručne prakse ocjenjuje ih nepogodnima za tu skupinu.

**Krupni tisak:** zadaci su u 20 pt, a nigdje u knjizi nema teksta manjeg od 16 pt (ni u podnožju).
Pismo je Atkinson Hyperlegible Next, a za brojke Source Sans 3. Sve je čisto crno na bijelom,
bez sivih površina (dobro se kopira). Unutarnja margina od 22 mm omogućuje kopiranje bez gubitka teksta u pregibu.

## Kako je osigurana točnost

1. **Umjetna inteligencija nije izmislila nijednu izreku.**
   - Tri agenta su neovisno jedan o drugome sastavila popise poslovica i izreka.
   - U knjigu ulazi samo izreka koju su navela barem dva od tri agenta (ili jedan, ako je na znanstveno ispitanom popisu najpoznatijih izreka).
   - Izreka mora biti i **potvrđena u izvoru**: njemački Wiktionary, njemački Wikiquote, engleski Wiktionary, Baur/Chlosta i GfM popisi najpoznatijih poslovica, Hallsteinsdóttir 2006, Borchardt (1888/1895) ili Wander (1867).
   - ⟨WEB⟩ izreka koje nisu bile u preuzetim izvorima potvrđene su pojedinačnom provjerom na webu (DWDS, Duden, Wiktionary, Redensarten-Index). Poveznice su u `data/attested_web.json`.
   - Citati poznatih autora i neprovjerljive izreke su izbačeni.
2. **Crna lista** (`data/blacklist.txt`). Nema izreka:
   - opterećenih nacističkom prošlošću („Jedem das Seine”, „bis zur Vergasung”);
   - rasističkih i antisemitskih;
   - o tjelesnom kažnjavanju;
   - koje se rugaju pamćenju, razumijevanju ili starosti („nicht alle Tassen im Schrank”, „Was Hänschen nicht lernt …”, „hinter dem Mond leben”).
3. **Dva urednika.** Svaku izreku jedan agent je obogatio (točan oblik, značenje vlastitim riječima, ključna riječ, pogrešni odgovori, pomoć, situacija, pitanja), a drugi je neovisno provjerio.
4. **Strojne provjere** (`gt/finalize.py`, `gt/plan.py`):
   - pogrešni odgovori i šaljive zamjene ne smiju činiti stvarnu izreku;
   - pomoć ne smije otkriti riječ;
   - na istom listu ne smiju biti dvije izreke istog oblika („einen ___ haben”);
   - na istom listu ne smiju biti riječi istog korijena („Hund/Hunde”);
   - odgovor jednog zadatka ne smije se vidjeti u drugom zadatku;
   - osmosmjerka sadrži svaku riječ točno jednom i nema slučajnih ružnih riječi.
5. **Provjera PDF-a** (`python3 -m gt.qa`):
   - format A4, sav tekst najmanje 16 pt, sigurne margine, ugrađeni fontovi;
   - svaki list je na desnoj stranici, a njegova stranica za voditelja na poleđini;
   - svako rješenje stoji na stranici za voditelja;
   - riječ „Demenz” ne postoji u knjizi ni na korici;
   - brojevi na korici odgovaraju knjizi;
   - pravopis je provjeren njemačkim rječnikom (LibreOffice).
6. **Završni pregled** s 5 neovisnih recenzenata: ⟨PREGLED⟩

**Iskreno: što nije napravljeno.** Knjigu nije pregledao čovjek kojemu je njemački materinski
jezik, a listovi nisu isprobani u stvarnoj grupi. Prije objave preporučujem oboje (vidi popis dolje).

## Prije objave: Vaš popis

1. Naručite **probni primjerak** (proof copy). Probajte kopirati nekoliko listova na običnom uredskom stroju.
2. Ako možete, dajte knjigu na čitanje nekome kome je njemački materinski jezik, idealno nekome tko radi
   u skrbi za starije. Barem 10 listova isprobajte s grupom ili s jednom starijom osobom.
3. **ISBN:** besplatni KDP ISBN (najjednostavnije) ili besplatni ISBN od NSK kao hrvatski izdavač.
   Odlučite prije prvog slanja.
4. Na KDP-ovom zaslonu s cijenama provjerite stopu PDV-a (7 % ili 19 %) i prema `KDP-LISTING.md` unesite neto cijenu.
5. U Njemačkoj i Austriji vrijedi **fiksna cijena knjige** (Buchpreisbindung): nema popusta, ni za domove.
6. U AI-izjavi na KDP-u odgovorite istinito (tekst u `KDP-LISTING.md`).
7. KDP dopušta 2 nova naslova po formatu tjedno. Ova knjiga i biblijski kriptogrami mogu se poslati isti tjedan.

## Ponovna izgradnja

```bash
pip install typst pymupdf pyphen spylls fonttools
python3 -m gt.build        # plan → unutrašnjost → omot → QA → output/ → KDP-LISTING.md
```

Za `gt.corpus`, `gt.finalize` i pravopisnu provjeru potrebni su izvori u `sources_cache/` (nisu u gitu):
- `sources_cache/de_DE_frami.dic` i `.aff`, iz `github.com/LibreOffice/dictionaries` (de);
- `sources_cache/proverb_sources/`:
  - kaikki.org izvozi njemačkog i engleskog Wiktionaryja;
  - njemački Wikiquote „Deutsche Sprichwörter”;
  - ynsrc popisi;
  - Baur/Chlosta i Hallsteinsdóttir tablice;
  - Borchardt i Wander s archive.org.

IDS OWID popis namjerno se **ne** koristi: uvjeti korištenja traže pisanu dozvolu, a popis može biti zaštićen kao baza podataka.

## Struktura

| Put | Što |
|---|---|
| `gt/corpus.py` | konsenzus triju popisa + potvrda u izvorima + crna lista → `data/corpus_consensus.json` |
| `gt/attest.py` | provjera izreke u izvorima |
| `gt/finalize.py` | spaja obogaćivanje i ispravke drugog urednika, strojne provjere → `data/corpus.json`, `data/corpus_report.md` |
| `gt/plan.py` | raspored 100 listova (10 × 10), bez dvosmislenih odgovora → `data/sheets.json` |
| `gt/exercises.py`, `gt/wordsearch.py`, `gt/text.py` | generatori vježbi, osmosmjerka, slogovi i pravopis |
| `gt/leader.py`, `gt/book.py` | stranice za voditelja, slaganje unutrašnjosti (s automatskim skraćivanjem ako nešto ne stane) |
| `gt/cover.py`, `gt/qa.py`, `gt/listing.py`, `gt/build.py`, `gt/dump.py` | omot, provjere, KDP unos, cijela izgradnja, tekstualni ispis za recenzente |
| `layout/*.typ`, `content/*.typ` | Typst prijelom i njemački tekstovi uvoda |
| `data/chapters.json`, `data/stories.json` | uvodi poglavlja, pitanja, ideje za kretanje i 10 priča |

## Odluke iz istraživanja (sažetak)

- **A4 i 100 listova:** jedina knjiga takve vrste na Amazon.de u A4 formatu samo s poslovicama. Konkurencija su SingLiesel (A5) i Verlag an der Ruhr (€22,99).
- **Rješenje na poleđini lista:** recenzenti konkurentskih knjiga hvale princip „okreni stranicu”. List se može i izrezati bez gubitka rješenja drugog lista.
- **Bez riječi „Demenz” u knjizi i na korici.** Najčešća pritužba u recenzijama je da korisnici moraju prelijepiti tu riječ. Spominje se samo u opisu na Amazonu.
- **Bez zdravstvenih obećanja** (njemački HWG): nigdje „gegen Demenz”, „beugt vor”, „bewiesen”.
- **Dozvola za kopiranje** izričito dopušta kopije za sudionike i povećanje na A3 za jednu ustanovu ili vlastitu grupu. Zabranjuje prosljeđivanje drugim ustanovama, prodaju i digitalno širenje.
- **Cijena:** 18,99 € (KDP traži neto cijenu; vidi `KDP-LISTING.md`). Tisak 240 stranica A4 stoji 4,59 €, a honorar je oko 6 € uz 7 % PDV-a, odnosno oko 5 € uz 19 %.
