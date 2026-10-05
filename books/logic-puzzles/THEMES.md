# Writing puzzle themes

Every one of the 100 puzzles has a theme: its title, its story setup, its
people and the things they are matched with, plus the sentence pieces the
generator uses to write the clues. Themes live in `lp/themes/chN.py` (or
`chNa.py` / `chNb.py` when a chapter is split) as a list called `THEMES`.

The puzzle logic (which clues, the unique solution, hints, solutions) is made
by the engine. A theme only supplies the world and the words.

Check your file after every edit:

    cd books/logic-puzzles
    .venv/bin/python -m lp.themecheck lp/themes/ch2.py -v

`-v` prints real clues generated from your templates. Read them: every one
must be a natural, grammatical English sentence. Fix templates until it
prints `OK` for every theme and the clues read well.

See `lp/plan.py` for what each slot needs (`.venv/bin/python -m lp.plan`
lists all 100 slots with size `n` x `k`, family and stars).

## Grid themes (all chapters except 4)

```python
THEMES = [
  {
    "slot": 12,                              # puzzle number 1-100
    "title": "The Swapped Jam Labels",       # unique in the book, max ~32 characters
    "story": "Three neighbors brought jam to the church supper, and the "
             "labels came off in the rain. Mrs. Pruitt needs to know whose is whose "
             "before the judging. Can you match each cook with a jam and a jar?",
    "entity": ["cook", "cooks"],             # singular, plural (used in a few clue forms)
    "cast": ["Hattie"],                      # recurring characters who appear (from the bible)
    "question": {                            # optional in ch. 1-5, REQUIRED in ch. 6-7
        "text": "Who left the lid off?",     # the payoff question, answered by the solution
        "cat": "Jar",                        # a category label
        "value": "mason jar",                # whoever has this value is the answer
    },
    "answer": "Lou",                         # optional: force who the answer is (finale needs it)
    "answer_has": {"Jam": "plum"},           # optional: also force the answer person's value in an
                                             # unordered category (so the story's motive holds)
    "cats": [
      {"label": "Cook", "kind": "name", "values": ["Hattie", "Ruben", "Lou"]},
      {"label": "Jam", "values": ["plum", "fig", "quince"],
       "ref": "the {v} jam's maker",                 # noun phrase: whoever has this value
       "pred": "made the {v} jam",                   # verb phrase, past tense
       "neg": "did not make the {v} jam",
       "either": "made either the {a} or the {b} jam",
       "nor": "made neither the {a} nor the {b} jam",
       "short": "the {v} jam"},                      # short label for explanations
      {"label": "Jar", "values": ["mason jar", "crock", "tin"], ...same keys...},
    ],
  },
]
```

Rules for the `cats` list:

- Exactly `k` categories: the names first (`"kind": "name"`), then `k - 1` more.
- Exactly `n` values in every category (the slot says `n`).
- Names: different first letters, not in alphabetical order, 3–7 letters,
  easy to pronounce, no two names that look alike (Ann/Anna). Use the
  bible's cast and name pool.
- Every grid label (names, values, number labels) at most 12 characters.
  Prefer one or two short words: "plum", "mason jar", "9 a.m.".
- Values of one category must be the same kind of thing (all jams, all jars).
- All verb phrases in one theme use the same tense (past is usual).
- Templates must work with ANY value of the category: "the {v} jam's maker"
  must read well for "plum", "fig" and "quince".
- `ref` is used as subject AND object ("Ruben is older than the fig jam's
  maker"), so it must be a noun phrase that names a person.
- Never put a period inside a template.

### Ordered categories (numbers, times, places in line)

Slots with `ordered = 1` need exactly one ordered category. It is a list of
evenly spaced numbers plus the words for comparing them:

```python
{"label": "Time", "ordered": True,
 "nums": [9, 10, 11, 12],                          # exactly n, evenly spaced
 "labels": ["9 a.m.", "10 a.m.", "11 a.m.", "noon"],  # optional display text, same length
 "ref": "the {x} arrival",       # {x} is the label
 "pred": "arrived at {x}", "neg": "did not arrive at {x}",
 "either": "arrived at either {a} or {b}", "nor": "arrived at neither {a} nor {b}",
 "short": "{x}",
 "more": "arrived later than {y}",            # bigger number than {y}
 "less": "arrived earlier than {y}",          # smaller number than {y}
 "dmore": "arrived exactly {d} after {y}",    # {d} becomes "2 hours"
 "dless": "arrived exactly {d} before {y}",
 "dunit": ["hour", "hours"],                  # unit for {d} (singular, plural)
 "dmore1": "arrived one hour after {y}",      # optional: the one-step case
 "dless1": "arrived one hour before {y}"}
```

The numbers' step is the unit: nums `[5, 10, 15, 20]` with `dunit
["dollar", "dollars"]` makes "exactly 10 dollars more". Bigger number =
`more`. For ages use `more` = "is older than {y}"; for prices "cost more
than {y}"; for times "arrived later than {y}".

Line-up slots (chapter 3, puzzles 31-38) use an ordered "place in line"
category and must also give:

```python
 "adj": "stood right next to {y}",
 "nadj": "did not stand next to {y}",
 "ends": "stood at one end of the line"       # used for "either first or last"
```

## Liar themes (chapter 4, puzzles 47-58)

```python
{"slot": 47, "title": "Who Ate the Last Scone?",
 "story": "Two sentences of setup ... Each of them says one thing. ...",
 "names": ["Bea", "Otto", "Juno"],          # 3 names for 47-50, 4 for 51-55, 5 for 56-58
 "did": "ate the last scone",               # past tense, completes "Otto ___."
 "didnt": "didn't eat the last scone",       # completes "Otto ___." and "I ___."
 "cast": ["Otto"]}
```

The generator writes the statements ("I didn't eat the last scone.",
"Either Bea or Juno ate the last scone.") and the rule ("Exactly one of
these statements is true." or "Only the culprit is fibbing.").

## Story setups

- 2–4 sentences, about 40–80 words. Warm, light, small-town; no violence,
  no murder, nothing gory. Low stakes early (mixed-up labels, a lost
  ribbon), bigger mysteries later (a missing heirloom, a sabotaged boat) —
  still bloodless and gift-safe.
- Give a reason to solve it and end with the task, usually a question:
  "Can you work out who brought which pie, and when each arrived?"
- Never give away clue information in the story.
- US spelling and US settings (dollars, a.m./p.m., Main Street).
- Vary openings. Do not start two stories in a chapter the same way.
