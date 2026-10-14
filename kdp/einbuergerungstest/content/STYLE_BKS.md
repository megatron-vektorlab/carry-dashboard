# Style guide: DE–BKS edition (translations, explanations, Merksätze)

Readers: adults from Bosnia, Croatia, Serbia, Montenegro who live in Germany, speak German at
A2–B1 and prepare for the "Leben in Deutschland" test or the Einbürgerungstest. Many are older
or not used to legal vocabulary. Explanations must be clear, short, calm and factual.

## Language
- Croatian standard, **ijekavica, latinica**, but prefer words that Bosnian and Serbian readers
  use too (e.g. "opozicija", "podjela vlasti", "stranka"). No purist neologisms.
- Use the locked terms in `content/glossary_bks.json` **exactly**. When an explanation first
  mentions an institution, you may add the German name in parentheses: "Bundesrat (savezno vijeće pokrajina)".
- German gender pairs ("Bürgerinnen/Bürger", "sie/er") → use the generic masculine in BKS
  ("građani", "on") unless the question is specifically about women. The book states this once
  in the introduction.
- Typography: „…" quotes, "…" for the German trailing ellipsis, "%" with a space ("5 %").

## Fields to produce for each item
```json
{
  "id": "G-001",
  "q_bks": "translation of question_de",
  "options_bks": ["translation of option 1", "…2", "…3", "…4"],
  "expl_bks": "explanation (30–60 words)",
  "merksatz_de": "short German sentence (max. 12 words)"
}
```

### q_bks / options_bks
- Faithful, natural translation. Keep the **same order** as `options_de`.
- Never add hints that reveal the answer. Keep options that look alike in German distinguishable
  in BKS; for official titles/offices keep the German term in parentheses, e.g.
  "vladajući gradonačelnik (Regierender Bürgermeister)", "ministar predsjednik (Ministerpräsident)".
- Options that are only "Bild 1"… → "Slika 1"…; options that are only "1"… "4" → keep "1"… "4".
- A trailing German "…" in the question stays "…" in BKS; complete the sentence naturally so
  that each option continues it grammatically where possible.
- Photo credits (e.g. "© Deutscher Bundestag/…") and source captions are NOT translated; drop
  them from q_bks.

### expl_bks (the most important field)
- 30–60 words, 2–4 short sentences. Explain **why the correct option (`correct_option_de`) is
  right**, in plain words, with one concrete detail that helps memory (article of the Grundgesetz,
  year, example from daily life). If a wrong option is a common trap, you may say in one short
  clause why it is wrong.
- The explanation must support ONLY the option at `correct_index`. Never state or imply that
  another option is correct. Never contradict the answer key, even if you think the key is
  debatable — then write a neutral explanation and add the id to your final notes.
- If `image_note_bks` is present, start the explanation with that note (you may shorten it
  slightly but keep every fact), then add context.
- Facts only: no opinions, no politics of the day, no names of **current** office holders, no
  numbers that change often (population, current ministers). Historical names and dates are fine.
- No legal advice, no promises ("s ovim ćete sigurno proći" — forbidden).
- Never use the words "službeni/službeno" about this book, and never "BAMF preporučuje".

### merksatz_de
- One simple German sentence, A2–B1, **max. 12 words**, that states the correct fact so it is
  easy to remember. Must be true on its own. Examples:
  - "Meinungsfreiheit: Man darf die Regierung offen kritisieren."
  - "Man hat bei der Bundestagswahl zwei Stimmen."
  - "Die Landeshauptstadt von Bayern ist München."
- Do not start every Merksatz the same way. No "offiziell", "amtlich".

## Examples (quality bar)

```json
[
 {
  "id": "G-001",
  "q_bks": "U Njemačkoj ljudi smiju otvoreno govoriti protiv vlade jer …",
  "options_bks": ["ovdje vrijedi sloboda vjeroispovijesti.", "ljudi plaćaju poreze.", "ljudi imaju biračko pravo.", "ovdje vrijedi sloboda mišljenja."],
  "expl_bks": "Sloboda mišljenja jedno je od temeljnih prava iz Temeljnog zakona (članak 5.). Svatko smije javno reći ili napisati svoje mišljenje i kritizirati vladu, a zbog toga ne smije biti kažnjen. Granice postoje samo kod kaznenih djela, na primjer uvrede ili poticanja na mržnju.",
  "merksatz_de": "Meinungsfreiheit: Man darf die Regierung offen kritisieren."
 },
 {
  "id": "G-130",
  "q_bks": "Koji bi glasački listić bio valjan na izborima za Bundestag?",
  "options_bks": ["1", "2", "3", "4"],
  "expl_bks": "Valjan je listić s točno jednim križićem u lijevom stupcu (prvi glas, kandidat) i točno jednim križićem u desnom stupcu (drugi glas, stranka). Dva križića u istom stupcu čine taj glas nevaljanim.",
  "merksatz_de": "Bei der Bundestagswahl hat man eine Erst- und eine Zweitstimme."
 },
 {
  "id": "BE-09",
  "q_bks": "Kako se zove šef vlade u Berlinu?",
  "options_bks": ["ministar predsjednik (Ministerpräsident)", "gradonačelnik (Oberbürgermeister)", "predsjednik Senata (Präsident des Senates)", "vladajući gradonačelnik (Regierender Bürgermeister)"],
  "expl_bks": "Berlin je istodobno grad i savezna pokrajina. Njegovu vladu čini Senat, a na čelu Senata je vladajući gradonačelnik (Regierender Bürgermeister). Naziv „Ministerpräsident” koristi se u većini drugih pokrajina, a „Präsident des Senates” u Bremenu.",
  "merksatz_de": "Berlin wird vom Regierenden Bürgermeister regiert."
 }
]
```
