# ASVAB Math Workbook — 1,000 zadataka s rješenjima korak po korak

Knjiga za Amazon KDP (paperback, engleski, 8.5 × 11", crno-bijeli tisak).
Svi zadaci se generiraju iz Python predložaka: **sympy računa svaki odgovor
egzaktno**, a druga, neovisna metoda ga još jednom provjerava; tekst
zadataka, objašnjenja korak po korak i „Why not?” bilješke za svaki krivi
odgovor napisao je Claude u predlošcima.

## Gotove datoteke (`output/`)

| Datoteka | Za što |
|---|---|
| `ASVAB-Math-Workbook-interior.pdf` | unutrašnjost knjige — upload na KDP („Manuscript”) |
| `ASVAB-Math-Workbook-cover.pdf` | korice (stražnja + hrbat + prednja, s bleedom) — upload na KDP („Book cover”) |
| `front-cover.png` | prednja korica za oglase, društvene mreže, A+ sadržaj |
| `qa-report.txt` | statistika: 1.000 zadataka, raspored točnih slova A–D, razine, sekcije |
| `answer-ledger.csv` | popis svih 1.000 zadataka s točnim odgovorom (za kontrolu) |

Tekstovi za KDP obrazac (naslov, opis, ključne riječi, kategorije, cijena,
AI-izjava): **`KDP-LISTING.md`**.

## Sadržaj knjige

1. Uvod: *How to Use This Book*, *The ASVAB Math Subtests* (format CAT i
   papirnatog testa, AFQT), *Test-Day Strategies* + *Mental Math Toolkit*
2. **Dijagnostički test** (30 zadataka) s tablicom „pitanje → poglavlje” i
   planom učenja
3. **27 poglavlja** u 4 dijela (Number Skills, Algebra, Geometry, Word
   Problems); svako ima *Key Concepts* (pravila, formule, riješeni primjer,
   savjet bez kalkulatora, česte zamke), vježbu (zagrijavanje → razina
   testa → izazov) i *Answers & Explanations* (ključ + rješenje svakog
   zadatka)
4. **4 probna testa** u formatu papirnatog ASVAB-a (30 AR + 25 MK), s listom
   za odgovore, ključem s oznakom poglavlja i bodovnom tablicom
5. *Formula Sheet* (1 stranica), *Quick Reference Tables*, *Glossary*,
   *Progress Tracker*

Ukupno: 750 zadataka u poglavljima + 30 dijagnostičkih + 4 × 55 u testovima
= **1.000**.

## Kako objaviti na KDP-u (korak po korak)

1. kdp.amazon.com → **+ Create** → **Paperback**.
2. *Paperback Details*: kopirajte polja iz `KDP-LISTING.md` (naslov,
   podnaslov, autor, opis, 7 ključnih riječi, 3 kategorije).
3. *Paperback Content*: besplatni KDP ISBN · **Black & white interior,
   white paper** · trim **8.5 x 11 in** · **No bleed** · **Matte** ·
   Manuscript = `output/ASVAB-Math-Workbook-interior.pdf` · Cover = „Upload
   a cover you already have” → `output/ASVAB-Math-Workbook-cover.pdf`.
4. Na pitanje o AI sadržaju odgovorite **Yes** (tekst i slike su nastali uz
   AI) — to je obavezno i ne prikazuje se kupcima.
5. **Launch Previewer** — pregledajte nekoliko stranica, posebno hrbat
   korica.
6. *Rights & Pricing*: 60 % royalty, cijena **$19.99** (prijedlog).
7. Prije objave naručite **proof copy** (probni primjerak) i pregledajte ga
   u ruci.

## Promjene i ponovna izrada

```bash
cd books/asvab-math
python3.12 -m venv .venv && .venv/bin/pip install sympy pillow   # jednom
# potreban je TeX Live (pdflatex) s paketima: latex-extra, fonts-extra, pictures

.venv/bin/python -m asvab.selftest all -q   # stres-test svih predložaka
.venv/bin/python -m asvab.build             # svih 1.000 zadataka → PDF
.venv/bin/python -m asvab.cover             # korice (hrbat po broju stranica)
.venv/bin/python -m asvab.audit             # lektorska automatska provjera
```

* Autor, naslov, godina: `asvab/config.py` (pa ponovno `build` i `cover`).
  Ime autora mora biti isto na koricama, naslovnoj stranici i u KDP obrascu.
* `SEED` u `config.py` mijenja sve brojeve u zadacima (npr. za 2. izdanje);
  svi odgovori se ponovno provjeravaju.
* Poglavlja su u `asvab/chapters/chNN_*.py`; pravila pisanja predložaka su u
  `AUTHORING.md`.

## Kako je osigurana točnost

* Odgovor svakog zadatka računa sympy egzaktno (racionalni brojevi, bez
  zaokruživanja); generator odbija svaki zadatak u kojem se pojavi float.
* Svaki predložak daje i **neovisnu provjeru** (drugi put do istog
  rezultata, uvrštavanje u jednadžbu, brute-force, enumeracija
  vjerojatnosti) — ako se ne slažu, zadatak se ne može generirati.
* Četiri ponuđena odgovora moraju biti međusobno različita i po vrijednosti
  i po zapisu; krivi odgovori dolaze iz stvarnih tipičnih grešaka i svaki ima
  objašnjenje.
* `selftest` za svaki predložak generira stotine varijanti i provjerava sve
  gore navedeno + LaTeX sintaksu; `audit` traži gramatičke greške i
  provjerava da se konačni odgovor pojavljuje u koracima rješenja.
* **Dva kruga slijepe provjere**: neovisni AI recenzenti riješili su svih
  1.000 zadataka bez ključa i usporedili s ključem — u oba kruga **1.000/1.000
  podudaranja, nijedan pogrešan odgovor**. Nađene sitnice (netočne „why not”
  bilješke, realističnost konteksta, stil, ponavljanja između testova) su
  ispravljene.
* Probni testovi imaju jednak omjer težine, ravnomjerno raspoređena slova
  A–D (bez nizova od 4 ista) i ne ponavljaju isti scenarij između testova.

## Brojke ove verzije

255 stranica · 1.000 zadataka (750 + 30 + 220) · 79 slika · točni odgovori
A/B/C/D = 255/275/256/214 · trošak tiska ≈ $5,34 · prijedlog cijene $19.99 →
≈ $6,66 po prodanom primjerku.
