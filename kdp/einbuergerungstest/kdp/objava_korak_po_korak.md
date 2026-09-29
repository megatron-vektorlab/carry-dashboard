# Objava na KDP-u – korak po korak

Vodič za meki uvez *Einbürgerungstest & Leben in Deutschland (DE–BKS)*. Vrijednosti u okvirima
kopirajte izravno u KDP. Stanje pravila: 29. 9. 2026.

## 0. Pravila računa (važno prije početka)

- **Jedan KDP račun po osobi.** KDP-ovi uvjeti (t. 4.2): „You may maintain only one account at a time”.
  Drugi račun smije se otvoriti samo uz pisano dopuštenje Amazona. Duplikati se gase.
  Različita autorska imena (pseudonimi) vodite unutar **istog** računa – njihov broj nije ograničen.
- **Ukupan broj knjiga nije ograničen**, ali od 21. 9. 2026. smijete stvoriti najviše
  **2 nova naslova tjedno po formatu**: 2 e-knjige, 2 meka uveza i 2 tvrda uveza. Brojač se vraća
  na nulu nedjeljom u 00:00 UTC.
  - Svaki format i svako jezično izdanje je zaseban naslov (ukrajinsko izdanje = novi naslov).
  - Već objavljeni naslovi nisu pogođeni. Zamjena PDF-a u postojećem naslovu nije novi naslov;
    novo izdanje (nova ISBN oznaka) jest.
  - Prema izvještajima izdavača i nedovršeni nacrt vjerojatno troši mjesto. Zato **„+ Create”
    kliknite tek kad su konačni PDF-ovi spremni.**

## 1. Tko što radi

| Korak | Vi | Claude |
|---|---|---|
| Prijava u Amazon/KDP, dvofaktorska potvrda | ✔ | – |
| Porezni intervju (W-8BEN), bankovni račun, provjera identiteta | ✔ | objašnjava |
| Usporedba sa službenim BAMF PDF-om, lektura | ✔ | priprema popise za provjeru |
| Konačni PDF-ovi bez vodenog žiga (nakon što upišete podatke) | – | ✔ |
| Unos polja u KDP | ✔ (kopiranje iz ovog vodiča) | priprema sve vrijednosti |
| Izjave o pravima i o upotrebi AI-ja | ✔ (to je Vaša izjava) | preporuka ispod |
| Probni primjerak i završni klik „Publish” | ✔ | pregled probnog tiska po fotografijama |

## 2. Jednokratno: KDP račun (≈ 30–45 min)

1. Otvorite **kdp.amazon.com** i prijavite se Amazon računom (ili napravite novi).
2. **Your Account → Author/Publisher Information:** ime i adresa kao u banci i poreznim podacima.
3. **Getting Paid:** bankovni račun (IBAN, BIC). KDP pokazuje koji su načini isplate podržani za Hrvatsku.
4. **Tax Information (porezni intervju):**
   - fizička osoba (Individual), niste US osoba → obrazac **W-8BEN**;
   - država: Hrvatska; porezni broj (Foreign TIN): **OIB**;
   - ugovor o izbjegavanju dvostrukog oporezivanja SAD–Hrvatska još **nije na snazi** (upućen
     Senatu 14. 9. 2026.) → na prodaju kupcima u SAD-u zadržava se 30 %. Prodaja na Amazon.de
     nema američki porez.
   - Za hrvatsku stranu (prijava prihoda, eventualno PDV ID) pitajte računovođu.
5. Ako KDP zatraži provjeru identiteta, pošaljite traženi dokument.

## 3. Prije unosa: dovršite knjigu

Upišite podatke u `kdp/release.json` (ili ih pošaljite meni), a ja složim konačne PDF-ove bez
vodenog žiga, s ispravnom debljinom hrpta:

- [ ] `catalog_stand` – datum „Stand” sa službenog BAMF PDF-a; `catalog_compared_on` – kada ste usporedili
- [ ] `human_proofread_by`, `human_proofread_date` – tek nakon stvarne lekture
- [ ] `publisher`, `address`, `email` – podaci za impresum (GPSR); `edition_date` – npr. „listopad 2026.”
- [ ] **ISBN** – odaberite jednu mogućnost:
  - **besplatni KDP ISBN** (najjednostavnije; kao nakladnik piše „Independently published”), ili
  - **vlastiti ISBN iz Hrvatske:** Hrvatski ured za ISBN (NSK Zagreb) dodjeljuje ga besplatno, ali
    tada NSK-u u roku 30 dana od tiska dostavljate obvezne primjerke. Kao nakladnik tada piše Vaše ime.
- [ ] Odluka o slikama grbova (`images: true/false`), vidi README → Pravne napomene

## 4. Unos knjige: Bookshelf → **+ Create → Paperback**

### 4.1 Paperback Details

**Language:** `German`

**Book Title:**
```
Einbürgerungstest & Leben in Deutschland
```
**Subtitle** (oba dijela stoje na naslovnici, pa se podaci i naslovnica podudaraju):
```
Deutsch – Bosnisch/Kroatisch/Serbisch: Alle 460 Fragen mit Übersetzung, Erklärung und Bildern
```
**Series:** preskočite za prvo izdanje (dodajte kad izađe drugi jezik).
**Edition Number:** `1`

**Author:** Vaše ime ili pseudonim (nikad „BAMF”). **Contributors:** isto ime s ulogom `Translator`.

**Description:** kopirajte HTML iz `kdp/metadata.md` (odjeljak „Opis”).

**Publishing Rights:** to je Vaša izjava. Preporuka:
- „**I own the copyright and I hold the necessary publishing rights**” – knjiga je novo djelo
  (prijevod, objašnjenja, testovi, dodaci). Novi sadržaj čini više od polovice knjige, a izvor
  pitanja naveden je u impresumu.
- Ako niste sigurni, pitajte KDP podršku prije objave. Za knjige s javnim sadržajem uobičajeno je
  pravilo: ako novi sadržaj čini manje od 50 %, bira se „This is a public domain work”.

**Primary Audience:** Sexually explicit – `No`; dob čitatelja – ostavite prazno.
**Primary Marketplace:** `Amazon.de`
**Categories (3)** i **Keywords (7):** iz `kdp/metadata.md`.
**Low-content book:** `No` · **Large-print book:** `No`

### 4.2 Paperback Content

**ISBN:** prema odluci iz točke 3. · **Publication Date:** ostavite prazno.

**Print Options:**
- Ink and Paper Type: `Black & white interior with white paper`
- Trim Size: `6.69 x 9.61 in (17 x 24.41 cm)` (pod „Select a different size”)
- Bleed Settings: `No Bleed`
- Paperback cover finish: `Matte`

**Manuscript:** učitajte `out/interior_de-bks.pdf` (konačni, bez vodenog žiga).
**Book Cover:** „Upload a cover you already have” → `out/cover_de-bks.pdf`
(naslovnica mora biti složena za isti broj stranica kao unutrašnjost; ja ih slažem zajedno).

**AI-Generated Content** (ovisno o sučelju, na ovoj ili prethodnoj stranici):
- Text: `Yes` → alat: `Claude (Anthropic)`; opseg: prijevodi, objašnjenja, Merksätze
- Translations: `Yes`
- Images: `No` – slike su iz BAMF-ova kataloga, naslovnica je tipografska. U nedoumici odaberite
  `Yes`; prijava nije javna.

**Book Preview:** „Launch Previewer” → provjerite da nema grešaka, da je tekst hrpta unutar hrpta i
da su slike i list za odgovore uredni → „Approve”.

**Probni primjerak:** prije objave kliknite **„Request printed proof”** i naručite 1–2 primjerka
(imaju oznaku „Not for resale”). Pošaljite mi fotografije nekoliko stranica: provjerit ću čitljivost
slika u sivim tonovima i margine.

### 4.3 Paperback Rights & Pricing

- Territories: `All territories (worldwide rights)`
- Primary marketplace: `Amazon.de`, cijena **`16,99 €`**. KDP odmah prikazuje honorar
  (očekivano ≈ 4,8 €); ostala tržišta preuzimaju preračunatu cijenu ili ih postavite ručno.
- Expanded Distribution: `No` (za sada)
- Potvrdite uvjete i kliknite **„Publish Your Paperback Book”** – to radite Vi.
  KDP pregledava knjigu do 72 sata i javlja e-mailom kad je dostupna.

## 5. Nakon objave

- **A+ sadržaj** (Marketing → A+ Content Manager): iz konačnog PDF-a složit ću slike 970 × 600 px –
  stranicu s pitanjem, probni test s listom za odgovore i stranicu „Moja pokrajina”.
- **Author Central** (Amazon.de): autorska stranica povezana s knjigom.
- **Ažuriranja:** pitanja o dužnosnicima (G-072, G-075) mijenjaju se najkasnije u ožujku 2027.
  Zamjena PDF-a u postojećem naslovu ne troši mjesto za nove naslove.
- **E-knjiga:** odluka poslije. Zbog javnog sadržaja moguć je niži honorar (35 %) i nema KDP Selecta,
  a prijelom sa slikama treba prilagoditi.
- **Sljedeća jezična izdanja:** najviše 2 nova meka uveza tjedno.
