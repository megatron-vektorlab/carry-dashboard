# Einbürgerungstest & Leben in Deutschland – dvojezično izdanje (DE–BKS)

Ideja br. 1 s popisa KDP ideja: dvojezični priručnik za njemački test naturalizacije i test
„Leben in Deutschland”. Prvo izdanje je **njemački – bosanski/hrvatski/srpski**: taj prijevod
vlasnik može sam lektorirati. Isti postupak zatim daje ukrajinsko, tursko i albansko izdanje
(nova mapa `content/<jezik>/`, isti katalog i prijelom).

## Stanje

| Dio | Datoteka | Stanje |
|---|---|---|
| Katalog: 460 pitanja, provjereno iz 3 izvora | `data/catalog.json`, `data/crosscheck_report.md` | gotovo |
| Prijevodi, objašnjenja i Merksätze (460) | `content/bks.json` | gotovo: 0 grešaka; slijepa provjera + provjera preciznosti, sve ispravke primijenjene |
| Slike za 37 slikovnih pitanja (sivi tonovi) | `layout/images/`, `content/image_provenance.json` | gotovo; fotografije trećih strana izostavljene |
| Unutrašnjost (PDF), 311 str. | `out/interior_de-bks.pdf` | **konačno** (29. 9. 2026.) – bez ljudske lekture i bez usporedbe sa službenim PDF-om, što impresum navodi |
| Naslovnica s hrbtom (PDF) | `out/cover_de-bks.pdf` | **konačno**: 14,3304 × 9,86 in, hrbat 0,7004 in (vidi `out/build_info.json`) |
| KDP podaci | `kdp/metadata.md` | gotovo |

## Sadržaj knjige
- Uvod: o testu (33 pitanja, 60 min; **17** točnih za naturalizaciju, **15** za test LiD na kraju
  orijentacijskog tečaja), kako koristiti knjigu, **aktualnost i provjera** (datum izdanja,
  stanje kataloga, datum usporedbe, stvarno provedene provjere), slikovna pitanja s QR kodom.
- Prije početka: **Moja pokrajina** (stranice svih 16 pokrajina + raspored pitanja),
  **plan učenja 14 i 30 dana**, **Pazi na riječ** (nicht, kein, nur, darf, muss…), **Tko je tko
  u državi** (dijagram + tablica s brojevima pitanja), **vremenska crta**.
- Dio 1 i 2: 460 pitanja s prijevodom, označenim odgovorom, objašnjenjem, Merksatzom i slikama.
- Dio 3: **10 potpunih simulacija ispita** (30 općih + 3 pitanja pokrajine iz **Dodatka A**
  bez označenih odgovora), **list za odgovore 1–33** iza svakog testa, rješenja uključujući
  tablicu rješenja za pitanja pokrajina.
- Tablica pogrešaka (ponavljanje nakon 1, 3 i 7 dana), **tematsko kazalo** s brojevima pitanja, pojmovnik.

## Kako je osigurana točnost
1. **Katalog se ne generira.** Tekst i ključ odgovora dolaze iz tri neovisne javne kopije
   BAMF-ova kataloga (`data/sources.json`). Izvor A potvrđuje **svih 460** odgovora, izvor C 443;
   17 neslaganja greške su u izvoru C (`data/resolutions.json`). Izgradnja se prekida ako se
   ijedan ključ ne slaže.
2. **Model ne dira njemački tekst ni ključ.**
3. **Automatska provjera** (`scripts/validate_content.py`).
4. **Slijepa provjera** (`content/review_report.md`): 0 odstupanja od ključa na 424 pitanja bez slike;
   31 jezična/činjenična primjedba ispravljena.
5. **Provjera preciznosti** (`content/precision_report.md`, potaknuta vanjskom uredničkom recenzijom):
   66 nalaza u 57 pitanja (preširoka pravna pravila, savjeti, podaci koji zastarijevaju), npr.
   pitanje 130 (listić), prag od 5 % i pravilo tri izborna okruga, Widerspruch po pokrajinama,
   „javno” poricanje holokausta. Sve ispravke u `scripts/consistency.py`, zapis u `content/consistency_log.md`.

**Nije provedeno (mora vlasnik):** usporedba sa službenim BAMF PDF-om (bamf.de nije bio dostupan
iz okruženja za izradu) i ljudska lektura. Knjiga to otvoreno navodi dok se ne upiše u `kdp/release.json`.

## Izdanje: `kdp/release.json`
Dok je bilo koje obavezno polje prazno, svaka izgradnja je **nacrt**: vodeni žig „NACRT · ENTWURF”
na svakoj stranici i naslovnici, a impresum navodi što nedostaje. Upišite:
- `edition_date` (npr. „listopad 2026.”), `catalog_stand` (datum „Stand” sa službenog PDF-a),
  `catalog_compared_on` (kada ste usporedili), `human_proofread_by` + `human_proofread_date`
  (tek nakon stvarne lekture), `publisher`, `address`, `email` (GPSR), po želji `isbn`.
- `images: false` isključuje slike (tada ostaju samo opisi i QR kod).

## Ponovna izgradnja
```bash
pip install typst pymupdf pillow segno
python3 scripts/build_catalog.py --a <A>/data/questions.json --b <B>/public/data/bamf/questions.json --c <C>/data/question.json
python3 scripts/prepare_images.py --b <B>/public/data/bamf   # slike + provjera SHA-256 + QR
python3 scripts/consistency.py      # ujednačavanje + sve ispravke iz provjera
python3 scripts/validate_content.py
python3 scripts/build_book.py      # out/interior_de-bks.pdf
python3 scripts/build_cover.py     # out/cover_de-bks.pdf (hrbat prema broju stranica)
```

## Prije objave – ljudski popis (obavezno)
- [ ] **Katalog:** preuzmite aktualni PDF s bamf.de, upišite njegov „Stand” i datum usporedbe
      u `kdp/release.json`; usporedite barem pitanja o dužnosnicima (G-072, G-075) i nekoliko nasumičnih.
- [ ] **Lektura BKS-a:** svih 460 pitanja; prvo `content/translator_notes.md` i `content/precision_report.md`.
- [ ] **Slike:** odlučite o slikama (vidi pravne napomene); pregledajte ih u probnom tisku.
- [ ] **Impresum/GPSR:** izdavač, adresa, e-mail u `kdp/release.json`.
- [ ] **KDP jezik:** njemački; prijava AI-ja prema `kdp/metadata.md`.
- [ ] **Probni tisak:** slike u sivim tonovima, margine, list za odgovore, hrbat (~0,70 in).
- [ ] **Cijena:** KDP kalkulator s konačnim brojem stranica (prijedlog 16,99 €).
- [ ] **QR kod** vodi na BAMF-ovu stranicu kataloga; po mogućnosti zamijenite ga vlastitom
      kratkom poveznicom koju možete preusmjeriti ako BAMF promijeni adresu.

## Pravne napomene (sažetak – nije pravni savjet)
- Pitanja i odgovori: službeno djelo (§ 5 Abs. 2 UrhG), preuzeto **neizmijenjeno** uz navođenje izvora.
- **Slike:** crteži grbova, karata, listića i zastava iz BAMF-ova kataloga dio su službenog djela.
  Grbovi i zastave nisu zaštićeni autorskim pravom, ali je njihova *uporaba* regulirana (§ 124 OWiG,
  pokrajinski propisi): prikazani su samo kao predmet ispitnih pitanja, u knjizi jasno označenoj kao
  neslužbenoj. **Fotografije trećih strana** (npr. „© Deutscher Bundestag/Achim Melde”, pitanje 55) nisu
  otisnute – umjesto njih QR kod. Popis i kontrolni zbrojevi: `content/image_provenance.json`.
  Ako želite potpunu sigurnost, pravnik neka potvrdi uporabu grbova prije objave; isključenje je jedna postavka.
- Na naslovnici i u impresumu stoji da knjiga **nije publikacija BAMF-a**.
- Prijava AI-ja na KDP-u je obavezna. Tvrdnje o provjerama u knjizi odgovaraju stvarno provedenima.
- Font: Source Sans 3, SIL Open Font License (`layout/fonts/SourceSans3-LICENSE.md`).
