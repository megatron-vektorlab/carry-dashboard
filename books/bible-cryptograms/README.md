# Large Print Bible Cryptograms, Vol. 1 — 200 King James Verses of Comfort, Hope and Strength

Ideja br. 2 s popisa KDP ideja (26. 9. 2026.): biblijski kriptogrami krupnim tiskom, engleski,
King James Version. Na popisu je ova ideja bila preporučena kao prva za izradu jer se izrađuje
najbrže i stiže u božićnu sezonu.

Svaka zagonetka skriva jedan stih ili kratak odlomak. Šifru, provjere i prijelom radi kod.
**Model nikad ne tipka stih:** svaki stih se povlači po referenci iz pet zasebnih digitalnih
kopija KJV teksta, a koristi se tekst oko kojeg se kopije slažu.

## Gotove datoteke za KDP (`output/`)

| Datoteka | Za što |
|---|---|
| `Large-Print-Bible-Cryptograms-interior.pdf` | unutrašnjost knjige, upload na KDP („Manuscript”) |
| `Large-Print-Bible-Cryptograms-cover.pdf` | omot (stražnja strana + hrbat + prednja strana, s bleedom), upload na KDP („Book cover”) |
| `front-cover.png` | prednja korica za oglase i A+ sadržaj |
| `marketing/*.png` | primjeri stranica: zagonetka, riješeni primjer, savjeti, rješenja |
| `../KDP-LISTING.md` | sve vrijednosti za KDP obrazac: naslov, opis, ključne riječi, kategorije, cijena, AI-izjava, teritoriji |

Stanje: **knjiga je spremna za probni tisak** (6. 10. 2026.).
- Unutrašnjost ima 275 stranica, a omot hrbat od 0,619 in (bijeli papir).
- `python3 -m bc.qa` prolazi bez greške.
- Vodenog žiga nema, jer su podaci za impresum upisani.
- Prije objave: probni primjerak i Vaš popis ispod.

## Što je u knjizi

| Dio | Stranice |
|---|---|
| Uvod | naslov, impresum, stranica za posvetu („This Book Belongs To”), sadržaj, dobrodošlica |
| *How to Solve* | pravila, opis stranice, riješeni primjer u 5 koraka (Psalam 23,1) sa slikama, kratka metoda |
| *Tips for King James Verses* | učestalost slova i riječi izračunata iz cijelog KJV-a, uzorci (THAT/HATH, SHALL), stari oblici (THEE, UNTO, -ETH) |
| **7 dijelova, 200 zagonetki** | Comfort in Hard Times (32), Peace for an Anxious Heart (26), Hope That Does Not Fade (30), Strength & Courage (30), Faith & Trust (30), Love, Joy & Praise (30), Christmas: Good Tidings of Great Joy (22) |
| Savjeti | 3 zasebna odjeljka: (1) knjiga Biblije + jedno slovo, (2) još dva slova, (3) najduža riječ s položajem + referenca |
| Rješenja | stih doslovno, referenca i kratko razmišljanje („Reflect:”) |
| Završne stranice | kazalo stihova po redu biblijskih knjiga, tablica napretka, „Verses I Want to Remember” |

**Svaka zagonetka ima svoju stranicu:**
- broj, razina (Easy / Medium / Hard / Expert, sa zvjezdicama) i stranice savjeta i rješenja;
- kodna slova od 21 pt s crtom za upis iznad svakog slova;
- tablica ključa: kodno slovo, koliko se puta pojavljuje i polje za pravo slovo. Ako stih ima do 7 redaka, tablica je u dva reda sa širim stupcima;
- prostor za bilješke, ako ostane mjesta.

Svaki dio počinje lakim zagonetkama i postaje teži. Razine: 61 laka, 67 srednjih, 52 teške, 20 ekspertnih.

Svaki dio ima i kratki uvod.

**Dodatno:**
- Q i J nikad nisu kodna slova, jer se na slabijem vidu brkaju s O i I.
- Interpunkcija je samo u kodnom retku.

## Kako je osigurana točnost

1. **Tekst stihova.** Svaki stih se uspoređuje u 5 javno dostupnih kopija KJV teksta
   (popis s kontrolnim zbrojevima: `data/sources.json`). Uzima se tekst oko kojeg se kopije
   slažu, a stih ulazi u knjigu tek ako se barem 4 od 5 kopija slažu u svim slovima. Na cijeloj
   Bibliji svih 5 kopija slaže se u 96,9 % stihova.
2. **Šifra.** Za svaku zagonetku je nov ključ i nijedno slovo se ne šifrira samo u sebe.
   Kupci kod konkurencije upravo to najčešće kritiziraju.
3. **Jedinstveno rješenje.** Rješavač (`bc/cipher.py`) isprobava sve riječi iz KJV-a,
   13.406 različitih riječi. Zadana slova su odabrana tako da uz njih odgovara **točno jedno**
   čitanje. Strože od toga ne može: uzimaju se u obzir i besmislene kombinacije pravih riječi.
4. **Razina težine je izračunata.** Ekspertne zagonetke su rješive bez ijednog zadanog slova.
   Lake su rješive čistom dedukcijom (≥ 90 %, bez pogađanja).
5. **Provjera PDF-a** (`python3 -m bc.qa`):
   - nijedan tekst nije manji od 16 pt, pa je KDP-ova oznaka „Large print” istinita;
   - sve je unutar sigurnih margina i svi fontovi su ugrađeni;
   - svaka stranica sa zagonetkom sadrži točno ona kodna slova koja su u podacima;
   - svaki stih u rješenjima je doslovno točan;
   - svaka uputa „Hints p. / Answer p.” pokazuje na pravu stranicu;
   - hrbat omota odgovara broju stranica.
6. **Slijepo rješavanje.** 14 nasumično odabranih zagonetki (sve razine) riješilo je 7 neovisnih AI testera samo sa slike tiskane stranice, bez ključa i bez podataka. **Svih 14 je točno riješeno.** Doživljena težina raste po razinama.

Njihove primjedbe su ugrađene:
- izbačena su slova Q i J;
- ispravljen je zapis zadanih slova;
- brojevi u tablici ključa su jasniji;
- interpunkcija je samo u kodnom retku.

Nakon toga je 6 recenzenata (lektor, teolog, stručnjak za slabovidne, KDP marketing, provjera tvrdnji, odabir stihova) pregledalo cijelu knjigu. Ispravke su primijenjene.

To nije zamjena za ljudske testere.
7. **Tekstovi.** Uvode u dijelove i kratka razmišljanja uz svaki stih napisao je Claude.
   Svaki je provjerio zaseban recenzent u ulozi „iskusnog pastora i lektora”. Pazilo se:
   - je li tekst vjeran kontekstu stiha;
   - da nema konfesionalnih tvrdnji ni obećanja zdravlja i uspjeha;
   - na ton.

   Završni urednik je ujednačio stil.

**Što NIJE napravljeno (morate Vi ili netko koga zamolite):**
- ljudska lektura uvoda i razmišljanja; ako je moguće, neka tekst pogleda pastor ili voditelj
  biblijske skupine;
- da 3–5 čitatelja ciljne dobi riješi po nekoliko zagonetki na papiru, s probnim primjerkom;
- ocjene popularnosti stihova su urednička procjena, a ne podaci s interneta (alati za pretragu
  su bili blokirani).

## Prije objave — Vaš popis

- [ ] **Probni primjerak** (KDP → „Order proof copy”). Provjerite debljinu slova, olovku na
      papiru i kako izgleda tamnoplava naslovnica (mat).
- [ ] **Ujedinjeno Kraljevstvo:** u KDP-u kod „Territories” odaberite *Individual territories* i
      sve osim UK. U UK-u je KJV pod pravima Krune (izdavač Cambridge University Press), a njihovo
      besplatno dopuštenje vrijedi samo za nekomercijalnu upotrebu. Ako želite i UK, pošaljite
      upit na permissions@cambridge.org. Kad dopuštenje stigne, u `data/release.json` stavite
      `"uk_permission": true` i ponovno složite knjigu (impresum tada sadrži njihovu obaveznu rečenicu).
- [ ] **Impresum** (`data/release.json`): nakladnik Ivan Sikuten, Miškinova 4, Šašinovec, 10360 Sesvete, Croatia, ivansikuten@gmail.com. Podaci su preuzeti iz prethodne knjige.
      Ako želite drugu adresu (zbog privatnosti) ili ime, promijenite ih i ponovno složite knjigu.
- [ ] **Ograničenje KDP-a:** najviše 2 nova meka uveza tjedno. Ako su ovaj tjedan već dva iskorištena
      (npr. ASVAB i logičke zagonetke), pričekajte nedjelju 00:00 UTC.
- [ ] Cijena: preporuka je **13,99 $** (honorar oko 2,71 $ po primjerku).
  - Tisak 275 stranica 8,5×11 stoji 1,00 $ + 0,017 $ × 275 = 5,68 $.
  - Jeftinija opcija za početak: 12,99 $ (oko 2,10 $ po primjerku). Cijenu podignite nakon prvih recenzija.
  - Ispod 9,99 $ honorar pada na 50 %, pa tamo nikako.

## Objava na KDP-u — kratko

1. KDP → Bookshelf → **+ Create → Paperback** (tek kad ste spremni, jer i nacrt troši tjedno mjesto).
2. **Paperback Details:** sve vrijednosti iz `KDP-LISTING.md` (naslov, podnaslov, autor, opis, ključne
   riječi, kategorije, *Large print: Yes*, *Low-content: No*).
3. **Paperback Content:**
   - besplatni KDP ISBN;
   - 8.5 × 11 in, crno-bijelo, bijeli papir, bez bleeda, mat;
   - upload oba PDF-a iz `output/`;
   - AI-izjava prema `KDP-LISTING.md`;
   - **Launch Previewer**: provjerite hrbat i da nema upozorenja.
4. **Rights & Pricing:**
   - Individual territories, sve osim UK-a;
   - 60 %;
   - cijene iz `KDP-LISTING.md`;
   - Expanded Distribution isključen.
5. Naručite probni primjerak, pregledajte ga, pa **Publish**. Pregled na KDP-u traje do 72 sata.

Za božićnu sezonu: knjiga bi trebala biti „live” do kraja listopada ili početka studenoga. Oglasi
(Sponsored Products) idu od početka studenoga do otprilike 15. prosinca. Upute su u `KDP-LISTING.md`.

## Ponovna izrada (ako nešto mijenjate)

```bash
cd books/bible-cryptograms
pip install typst pymupdf
python3 -m bc.kjv download     # 5 kopija KJV teksta u sources_cache/ (ne ide u git)
python3 -m bc.stats            # statistika slova/riječi za stranicu savjeta
python3 -m bc.pool             # spaja popise kandidata u data/verse_pool.json
python3 -m bc.build --select   # odabir stihova -> zagonetke -> PDF -> omot -> QA -> output/ + KDP-LISTING.md
```

Gdje je što:

| Što | Gdje |
|---|---|
| Popisi kandidata | `data/verse_pool_agent.json`, `data/verse_pool_extra.json` |
| Isključeni stihovi | `bc/pool.py` (`EXCLUDE`) |
| Odabranih 200 | `data/selection.json`, izvještaj u `data/selection_report.md` |
| Zagonetke (ključ, zadana slova, savjeti, provjere) | `data/puzzles.json` |
| Uvodi i razmišljanja | `data/intros.json`, `data/reflections.json` |
| Tekstovi stranica | `content/*.typ` |
| Prijelom | `layout/book.typ`, `layout/main.typ`, `layout/cover.typ` |
| Naslov, tekstovi na naslovnici | `bc/config.py` |

Ako zamijenite jedan stih: promijenite izvor u `data/verse_pool_*.json` ili `EXCLUDE`, pa pokrenite
`python3 -m bc.pool && python3 -m bc.build --select`. Razmišljanje za novi stih treba napisati
u `data/reflections.json`, jer se ključ ondje veže uz referencu.

## Izvori i licencije

- **KJV tekst:** javno dobro u SAD-u, EU, Kanadi i Australiji; pet kopija s GitHuba
  (`data/sources.json`). U UK-u vrijedi pravo Krune, vidi gore.
- **Fontovi** (svi SIL Open Font License, licencije u `fonts/`):
  - Atkinson Hyperlegible Next (Braille Institute; čitljivost za slabovidne);
  - Libre Baskerville;
  - Cormorant Garamond;
  - Cinzel.
- **Naslovnica i ukrasi** nacrtani su kodom (vektorski oblici), bez fotografija i bez generatora slika.
