# Writing clues, hints and solutions

The engine has generated every puzzle in `data/puzzles/NNN.json`. Your job is
to turn each one into finished book text in `data/writing/NNN.json`. Read
`story/bible.md` (voice, cast, season) and `content/lessons.md` (the
techniques and their names, as the reader learns them) before you start.

## What is in a puzzle file

- `title`, `story`, `question` (may be null), `answer`, `stars`, `chapter`
- `state.cats`: the categories and their values, in grid order
- `texts`: the generator's clue sentences, numbered 1, 2, 3... in this order
- `table`: the solution, one row per person
- `trace`: the solver's step-by-step reasoning in plain English. Every line is
  true. Lines marked `"trivial": true` are bookkeeping. A `"kind": "suppose"`
  line has a `chain` (what follows from the supposition) and a `result`.
- liar puzzles (`"kind": "liars"`): `names`, `texts` (one statement per
  person, in order), `rule_text`, `culprit`, `cases` (each suspect tested:
  truth value of every statement, how many are true, whether it fits)

## What you write

```json
{
  "no": 12,
  "clues": ["...", "..."],
  "hints": ["Where to look", "What to notice", "The key step", "Stuck halfway (4-5 stars only)"],
  "solution": {
    "key_idea": "One sentence: the turning point of this puzzle.",
    "steps": ["3 to 8 sentences (up to 10 for 5 stars)..."],
    "epilogue": "One or two sentences: what really happened."
  },
  "tip": "Chapters 1-3 only: one short sentence from Ada, or null.",
  "answer_line": "Only for puzzles with a question: one short sentence, e.g. 'Teddy borrowed the spare key.'"
}
```

### Clues (grid puzzles only; liar statements are never changed)

Rewrite each generated sentence so the set reads like a person wrote it, in
the puzzle's world. **The meaning must stay exactly the same**: a separate
checker will translate your sentence back into logic without seeing the
original, and the computer compares the two on every possible grid.

- Same number of clues, same order. Never merge, split, drop or add clues.
- Keep every name and value spelled exactly as in the grid.
- Do not add information. "Gus came later than Rosa" must not become "Gus
  came right after Rosa" or "Gus came last".
- Do not lose information. "Of Nell and the 9 a.m. visitor, one baked the fig
  pie and the other the plum pie" also says Nell is not the 9 a.m. visitor.
  Keep the "one ... the other" shape, or an equally exact one.
- "Either A or B" stays a choice of exactly those two. "Neither A nor B"
  stays two no's. Comparisons keep their direction and their "exactly N".
- Vary the sentence shapes. Natural is good: "Whoever brought the fig jam
  used the tin." "The tin held the fig jam." Fancy is not: no puns that blur
  the meaning, no clue that needs outside knowledge.
- A sentence that already reads well may stay as it is.

### Hints: a ladder, aimed at the key step

1. **Where to look.** A question or a pointer to a specific clue, row or
   column: "Look at the 9 a.m. column. Who could possibly be first?" Not
   "start with clue 1" unless clue 1 really is the place to start. Give no
   marks away.
2. **What to notice.** Name the technique and apply it to that place: "Clue 4
   and clue 6 both talk about the tin. Put them together."
3. **The key step.** The turning point, stated as a deduction: "So the tin
   cannot be Rosa's: she was first, and the tin came later. That leaves only
   Mabel for the tin." For 5-star puzzles this is the Suppose: say which
   square to test and why it fails.
4. **Stuck halfway?** (4 and 5 stars only.) A deduction from the middle of
   the solve, for a reader who has made progress and stalled.

Each hint is 1 or 2 sentences: aim for 15 to 25 words, never more than 35
(the book is large print, and every word costs space). Every hint must be
true, and must follow from the clues (and, for hints 3 and 4, from the steps
before them in the trace). Use clue numbers.

Choose the key step from the trace: the first non-trivial line that unlocks
the rest (often the first comparison or pair deduction, or the Suppose).

### Solution

- **key_idea**: one sentence (at most 25 words) naming the turning point ("Clues 2 and 5 both
  limit the skiff, so it must be Gus's.").
- **steps**: the reasoning in order, in plain sentences of at most 25 words:
  3 to 5 sentences for 1-2 stars, 4 to 6 for 3 stars, 5 to 8 for 4-5 stars. Cite clue numbers. Summarize bookkeeping ("The rest of
  the grid fills in by elimination.") rather than listing every X. Every
  sentence must be true and must follow from the clues and the sentences
  before it. Follow the trace's logic; you may reorder only where the logic
  allows.
- For 5-star puzzles, include the Suppose: "Suppose Gus came at 9 a.m. Then
  ... But then ... So Gus did not come at 9 a.m."
- For liar puzzles: test the suspects (you may use the "opposites" shortcut
  when two statements contradict), and say which suspect fits the rule.
- **epilogue**: 1 or 2 sentences (at most 35 words), past tense, in the puzzle's world: what
  really happened, consistent with the answer table and the story. For
  whodunits name the culprit and give a gentle, forgivable reason. Keep to the
  bible's threads; never reveal the finale's secret before the finale.

### Voice and style

- Second person for hints ("Look at..."), plain past tense for epilogues.
  Ada's voice is warm, wry and precise; short sentences; no exclamation
  marks. Use "partner" at most once in a whole puzzle's writing, and rarely.
- US spelling. No emoji, no symbols for marks: write "X" and "dot".
- Large print matters: keep sentences short.

### Check your work

    cd /home/user/carry-dashboard/books/logic-puzzles
    .venv/bin/python -m lp.check_writing 12 13 14

must print `0 problems`. It checks counts, lengths, clue numbers and typos.
It cannot check meaning, so re-read every clue against the generated one.
