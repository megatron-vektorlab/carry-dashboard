# Einbürgerungstest & Leben in Deutschland – dvojezično izdanje (DE–BKS)

Ideja br. 1 s popisa KDP ideja: dvojezični priručnik za njemački test naturalizacije i test
„Leben in Deutschland”. Prvo izdanje je **njemački – bosanski/hrvatski/srpski**: taj prijevod
vlasnik može sam lektorirati. Isti postupak zatim daje ukrajinsko, tursko i albansko izdanje
(nova mapa `content/<jezik>/`, isti katalog i prijelom).

## Što je gotovo

| Dio | Datoteka | Stanje |
|---|---|---|
| Katalog, 460 pitanja, provjeren iz 3 izvora | `data/catalog.json`, `data/crosscheck_report.md` | gotovo |
| Zaključani pojmovnik DE–BKS | `content/glossary_bks.json` | gotovo |
| Opisi 38 slikovnih pitanja | `content/image_notes_bks.json` | gotovo, provjereno prema slikama |
| Prijevodi, objašnjenja, Merksätze | `content/bks.json` | vidi `content/validation_report.md` i `content/review_report.md` |
| Unutrašnjost knjige (PDF za KDP) | `out/interior_de-bks.pdf` | složeno |
| Naslovnica s hrbtom (PDF za KDP) | `out/cover_de-bks.pdf` | složeno |
| KDP podaci (naslov, opis, ključne riječi, prijava AI-ja) | `kdp/metadata.md` | gotovo |

## Kako je osigurana točnost
1. **Katalog se ne generira.** Tekst pitanja i ključ odgovora dolaze iz tri neovisne javne kopije
   BAMF-ova kataloga (`data/sources.json`, s točnim commitima). Tekst mjerodavne kopije B izgrađen
   je iz BAMF-ova PDF-a 17. 9. 2026. Izvor A potvrđuje **svih 460** odgovora, a izvor C 443.
   Preostalih 17 neslaganja greške su u izvoru C (prazne opcije, ćirilično „е”, stariji tekst)
   i svaka je objašnjena u `data/resolutions.json`. Skripta prekida izgradnju ako se ijedan ključ ne slaže.
2. **Model ne dira njemački tekst ni ključ.** Claude piše samo prijevod, objašnjenje i Merksatz,
   uz zaključani ključ i pojmovnik.
3. **Automatska provjera** (`scripts/validate_content.py`): potpunost, 4 opcije, duljine,
   zabranjene riječi („offiziell”, „službeno”…), dosljednost pojmovnika, brojevi.
4. **Slijepa provjera:** zaseban agent koji ne vidi ključ odgovara na svako pitanje samo iz
   prijevoda te za svako objašnjenje kaže koju opciju podupire. Svako odstupanje od ključa
   pregledano je i ispravljeno (`content/review_report.md`).

## Ponovna izgradnja
```bash
pip install typst pymupdf
python3 scripts/build_catalog.py --a <A>/data/questions.json --b <B>/public/data/bamf/questions.json --c <C>/data/question.json
python3 scripts/validate_content.py
python3 scripts/build_book.py      # out/interior_de-bks.pdf
python3 scripts/build_cover.py     # out/cover_de-bks.pdf (debljina hrbta prema broju stranica)
```
Izvori A–C: vidi `data/sources.json` (javni GitHub repozitoriji).

## Prije objave – ljudski popis (obavezno)
- [ ] **Katalog:** preuzmite aktualni PDF s bamf.de i usporedite datum („Stand”) i nekoliko
      pitanja s `data/catalog.json`. Građevinsko okruženje nije moglo pristupiti bamf.de.
- [ ] **Lektura BKS-a:** pročitajte svih 460 prijevoda i objašnjenja. Prvo pitanja navedena
      u `content/review_report.md`.
- [ ] **Slikovna pitanja:** usporedite 38 opisa s BAMF-ovim slikama (Online-Testcenter).
- [ ] **Impresum:** u `layout/book.typ` i `scripts/build_cover.py` zamijenite `[VERLAG / NAME]`,
      `[NAME]`, `[ANSCHRIFT]`, `[E-MAIL]`, `[ISBN …]`. Podaci o proizvođaču su obavezni po GPSR-u.
- [ ] **KDP jezik:** provjerite podržava li KDP hrvatski/bosanski/srpski; u suprotnom je jezik knjige njemački.
- [ ] **Probni tisak:** naručite probni primjerak i provjerite margine, veličinu slova i hrbat.
- [ ] **Cijena:** provjerite honorar u KDP kalkulatoru s konačnim brojem stranica.
- [ ] **Konkurencija:** na Amazon.de provjerite postoji li već izdanje DE–BKS/Kroatisch.

## Pravne napomene (sažetak)
- Pitanja i odgovori: službeno djelo prema § 5 Abs. 2 UrhG. Preuzimaju se **neizmijenjeno**,
  uz navođenje izvora (§ 62, § 63). Mijenjaju se samo navodnici i znak „…”. Tipfeler iz izvornika
  (npr. „Niedersachen” u pitanju 201) ostaje.
- **Slike iz kataloga nisu otisnute:** dio su fotografije trećih strana (npr. „© Deutscher
  Bundestag/Achim Melde”), a uporaba grbova pokrajina je regulirana. Točna slika opisana je riječima.
- Na naslovnici i u impresumu stoji da knjiga **nije publikacija BAMF-a**. Riječ „offiziell”
  koristi se samo u toj negaciji.
- Prijava AI-ja na KDP-u je obavezna (vidi `kdp/metadata.md`). U impresumu stoji da su prijevodi
  i objašnjenja izrađeni uz pomoć umjetne inteligencije i redaktorski pregledani (čl. 50(4) Akta o umjetnoj inteligenciji).
- Font: Source Sans 3, SIL Open Font License (`layout/fonts/SourceSans3-LICENSE.md`).
