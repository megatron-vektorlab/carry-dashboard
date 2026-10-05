# Cozy Mystery Logic Puzzles for Beginners (Thimble Harbor Puzzle School, knjiga 1)

Potpuno nova verzija knjige *Logic Puzzles for Complete Beginners*: 100 logičkih
zagonetki (mrežnih „tko je što“ i „tko laže“) u velikom tisku, s pričom o
izmišljenom gradiću Thimble Harbor, mentoricom Adom Quill, šest lekcija sa
slikama mreže, tri razine savjeta za svaku zagonetku i objašnjenim rješenjima.

## Gotove datoteke za KDP

| Datoteka | Što je |
|---|---|
| `output/Cozy-Mystery-Logic-Puzzles-interior.pdf` | unutrašnjost knjige (8,5 × 11 in, crno-bijelo, bez bleeda) |
| `output/Cozy-Mystery-Logic-Puzzles-cover.pdf` | omot (prednja + hrbat + stražnja strana), hrbat izračunat za točan broj stranica |
| `output/front-cover.png` | prednja korica za oglase / A+ sadržaj |
| `output/marketing/*.png` | primjeri stranica (lekcija, zagonetka, savjeti, rješenje) |
| `KDP-LISTING.md` | sve vrijednosti za KDP (naslov, opis, ključne riječi, kategorije, cijena, AI-izjava) |

**Knjiga ima 321 stranicu** (8,5 × 11 in, veliki tisak), hrbat 0,723 in. Trošak tiska na KDP-u je
oko 6,46 $; uz preporučenu cijenu **16,99 $** zarada je oko **3,73 $ po primjerku** (uz 15,99 $ oko 3,13 $).
Sve vrijednosti za KDP su u `KDP-LISTING.md`.

**Prije objave odlučite:** ime autora (sada „Ivan Sikuten“, mijenja se u `lp/config.py`, zatim ponovno
izraditi knjigu i omot) i provjerite na Amazonu da naziv serije/grada nije zauzet. Preporučujem naručiti
jedan tiskani probni primjerak prije puštanja u prodaju.

## Što je drugačije od stare verzije

- **Priča i svijet**: gradić Thimble Harbor, 12 stalnih likova, sezona od proljeća do zime i završni
  slučaj „The Lighthouse Affair“ (pet povezanih zagonetki i završna dedukcija).
- **Prava progresija težine**: od ★ do ★★★★★; zagonetke s 5 zvjezdica zahtijevaju jedan korak
  „Pretpostavimo…“ (u staroj verziji nijedna zagonetka nije bila zaista teška).
- **Klasična „stepenasta“ mreža** na svakoj zagonetki, velike ćelije, deblje linije (KDP-sigurno).
- **Savjeti u tri koraka** (+ „Stuck halfway?“ za ★★★★ i ★★★★★), u zasebnim odjeljcima da se ništa ne otkrije slučajno;
  na dnu svake zagonetke piše na kojim su stranicama savjeti i rješenje.
- **Rješenja**: najprije tablica odgovora, zatim ključna ideja i kratko obrazloženje, pa „što se zapravo dogodilo“.
- **Veliki tisak**: sav tekst za čitanje je 16 pt (Atkinson Hyperlegible), naslovi Libre Caslon; svi fontovi ugrađeni.
- Karta grada, popis likova, praćenje napretka, prazne mreže, pojmovnik izraza iz tragova, česte greške, „napravi svoju zagonetku“, certifikat.

## Kako je provjereno

- Svaka zagonetka ima **točno jedno rješenje** (iscrpna provjera svih mogućih mreža, do 1,7 milijuna po zagonetki).
- Svaku zagonetku je riješio i „ljudski“ rješavač koji koristi samo tehnike iz lekcija; težina (zvjezdice) proizlazi iz toga.
- Tragove je jezično dotjerao jedan agent, a zatim ih je **drugi agent „naslijepo“ preveo natrag u logiku**
  (bez uvida u izvorne tragove); računalo je usporedilo oba značenja na svim mogućim mrežama.
- Savjete i rješenja je pregledao zaseban „kritički urednik“ u odnosu na tragove, rješenje i zapis rješavanja.
- `python -m lp.qa`: fontovi ugrađeni, nema teksta manjeg od 16 pt (osim podnožja), svaka zagonetka stane na svoje stranice.

## Ponovna izrada (ako nešto mijenjate)

```bash
cd books/logic-puzzles
python3 -m venv .venv && .venv/bin/pip install pillow numpy pymupdf
.venv/bin/python -m lp.themecheck all      # provjera tema
.venv/bin/python -m lp.build_puzzles       # zagonetke -> data/puzzles (determinističko)
.venv/bin/python -m lp.lessons             # primjeri za lekcije
.venv/bin/python -m lp.check_writing --back  # provjera tekstova
.venv/bin/python -m lp.book                # unutrašnjost -> build/book/interior.pdf
.venv/bin/python -m lp.cover               # omot prema broju stranica
.venv/bin/python -m lp.qa                  # provjere za tisak
```

Tekstovi: `content/*.md` (pismo, upute, lekcije, uvodi poglavlja, završne stranice),
`data/writing/NNN.json` (tragovi, savjeti, rješenja), `lp/themes/*.py` (priče i kategorije),
`story/bible.md` (priručnik priče). Ime autora: `lp/config.py`.
