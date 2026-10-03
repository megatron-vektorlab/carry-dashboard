# Chapter authoring guide — ASVAB Math Workbook

The book: **ASVAB Math Workbook — 1,000 Practice Problems with Step-by-Step
Solutions** (Arithmetic Reasoning + Mathematics Knowledge). US English, KDP
paperback, 8.5×11 in, black-and-white. Readers: mostly 17–25-year-olds
preparing to enlist; many are rusty at math. Calculators are **not allowed**
on the ASVAB, so every problem must be solvable by hand in about 1 minute
(MK) or 1–2 minutes (AR).

Every answer is computed by **sympy** (exact arithmetic) and double-checked
by an **independent route**; the step-by-step solutions and the "why not"
explanation for each wrong choice are written by us (the authors) in the
template code.

Read `asvab/core.py` and the reference chapter
`asvab/chapters/ch06_percents.py` before writing anything — copy their
conventions exactly.

## Files

* One module per chapter: `asvab/chapters/chNN_slug.py` (e.g. `ch07_ratios.py`).
* Do **not** edit `core.py`, `generate.py`, `render.py`, `selftest.py`,
  `preview.py`, `tex/preamble.tex`, or other chapters. If you need a helper,
  define it privately in your module (prefix `_`). Mention anything you think
  belongs in core in your final report.
* Do not commit or push; the editor integrates everything.

## Module contents

```python
NUM = 7                 # chapter number
TITLE = "Ratios & Proportions"
PART = 1                # 1 Number Skills, 2 Algebra, 3 Geometry, 4 Word Problems
INTRO = r"""..."""      # Key Concepts (LaTeX), see below
PLAN = [(template_fn, level, count), ...]   # easy -> hard
TEST = [(template_fn, level), ...]          # optional: entries suitable for
                                            # the full-length practice tests
```

`PLAN` counts must total **25** for chapters 1–21; chapter 22: 40,
23: 35, 24: 40, 25: 35, 26: 40, 27: 35. Split roughly 30 % level 1
(warm-up, one step), 40 % level 2 (typical ASVAB, two steps), 30 % level 3
(challenge, multi-step but still hand-solvable). Use **at least 6
different templates per chapter** (8–10 is better for 35–40 problem
chapters), and never more than 4 problems from one (template, level) pair.

If `TEST` is omitted, all PLAN entries with level ≥ 2 are used for the
diagnostic and the four practice tests. Exclude drill-only templates (e.g.
pure vocabulary) from `TEST` if they would look odd in a real test.

## Templates

```python
@template("AR")              # "AR" = word problem (Arithmetic Reasoning), else "MK"
def name(rng, lvl):          # rng: random.Random; lvl: 1, 2 or 3
    ...                      # draw numbers with rng ONLY (never `random.` module)
    need(cond)               # reject ugly/ambiguous draws -> generator retries
    return Problem(stem=..., answer=..., fmt=..., wrong=[...], steps=[...],
                   check=... or verify=..., tip=None, figure=None)
```

### Exactness

* **Never use floats.** Use ints, `R(p, q)` (sympy Rational) and `Q(v)`.
  `7 / 2` in Python is a float — write `R(7, 2)` or `Q(7) / 2`. `finalize`
  raises `TypeError` on floats.
* Answers: sympy numbers/expressions, or strings for non-numeric answers
  (then use `fmt=text` and give each wrong value as a LaTeX string).
* `check=` must reach the answer by a **different route** than the one used
  to compute `answer` (substitute back, brute force over integers,
  `fractions.Fraction`, a different formula, `sp.solve` vs. hand formula, …).
  `verify=lambda v: ...` is a predicate (e.g. the value satisfies the
  equation). Give at least one; give both when cheap. Copy-pasting the same
  formula into `check` is not a check.
* Make numbers **calculator-free**: small integers, friendly decimals
  (money to the cent, ≤ 2–3 decimal places), fractions with small
  denominators, perfect squares where roots appear, π answers left in terms
  of π (`8\pi`) unless the stem says "use 3.14" or "use 22/7". Use `need()`
  liberally.

### Formatters (`fmt=`)

`num` integer · `dec` decimal · `money` dollars (cents shown consistently
across the four choices) · `money_cents` · `frac` · `mixed` · `pct` ·
`expr` (sympy expression) · `text` (strings) · `unit(num, "mile")` ·
`sq_unit(num, "ft")` → ft². Raw helpers for building text: `m(raw)` wraps
in `$…$`; `int_raw`, `dec_raw`, `frac_raw`, `mixed_raw`, `tx`, `latex`,
`F(p, q)` (unsimplified `\frac`).

### Wrong answers (`wrong=`)

List of `(value, why)` — 3 to 6 candidates; the generator picks 3, sorts
numeric choices ascending, and balances the answer letter. Each wrong value
should come from a **real mistake** a student makes, and `why` completes the
sentence "Choice (B) …", lowercase, no final period:

* `"is the discount, not the sale price"`
* `"adds the two percents instead of applying them one after the other"`
* `"forgets to convert minutes to hours"`

Use `None` as `why` for plausible values that do not come from a named
mistake. For string answers give `(latex_string, why)`. The generator adds
near-miss fillers if you supply too few. Negative distractors are dropped
for non-negative answers unless you pass `neg_ok=True` (do so for
signed-number chapters).

### Steps (`steps=`)

Each step is one short paragraph (LaTeX, text mode), written like a patient
tutor: say *what* you do and *why* in a few words, then show the
arithmetic. 2–4 steps typically. Show every arithmetic result that a
student would need to write down; never skip from the setup to the answer.
State units. Do not write the answer letter (the renderer adds it).

Good: `"Find the time for each leg: $d \\div r = 120 \\div 40 = 3$ hours."`

`tip=` (optional, ≤ 2 lines): a shortcut, estimation trick, backsolving
idea, or "check" — only when it is genuinely useful. Don't add tips that
show messy arithmetic.

### Stems

* Plain, ASVAB-like wording, US units and spelling, dollars.
* Vary phrasing and context: for word problems give at least 3–5 contexts
  per template. Mix civilian contexts (shopping, jobs, travel, cooking,
  sports, home projects) with military ones (platoon, convoy, recruits,
  ruck march, PT test, base, deployment supplies) — about 1/3 military.
  Use `person(rng)` (gives `.name`, `.he/.him/.his`, `.He/.His`) and
  `soldier(rng)` ("Sergeant Ruiz").
* **Realistic magnitudes**: tie each item to a sensible range (a gallon of
  paint is $20–$80, not $260; a car travels 30–70 mph; a soldier's PT run is
  2 miles in 13–20 minutes). Give each context its own number ranges.
* Emphasize reversals with `\emph{not}`.
* Money in text: `money(12.5)` → `\$12.50` — always use the formatter.
  Numbers in text: `num(1250)` → `$1{,}250$`. Never put a bare `%` — use
  `\%` (or `pct()`).
* Avoid ambiguous stems; if a figure is "not drawn to scale", say so.

### Figures (geometry)

`figure=` takes TikZ code *without* the `tikzpicture` wrapper (or with it,
if you need options). Must fit a 3.3-inch column: keep it within about
6 cm × 4 cm (use `scale=`). Grayscale only (`black`, `gray`, `black!20`
fills). Label with `$…$`. Use `\small` for labels if needed. Example:

```python
figure=rf"""\draw[thick] (0,0) -- (4,0) -- (4,2.5) -- cycle;
\node[below] at (2,0) {{$8$}};
\node[right] at (4,1.25) {{$6$}};"""
```

(In f-strings, TikZ braces must be doubled.)

## INTRO (Key Concepts)

About one printed page (≤ 1.5): a 1–3 sentence opening, then 2–4
`concept` boxes (rules, formulas, vocabulary), one `example` box (a fully
worked ASVAB-style example), one `tip` box (no-calculator trick), one
`trap` box (2–4 bullet common mistakes). Environments:

```latex
\begin{concept}{Title} ... \end{concept}
\begin{example}{Worked example} ... \textbf{Solution.} ... \end{example}
\begin{tip} ... \end{tip}
\begin{trap} \begin{itemize} \item ... \end{itemize} \end{trap}
```

Use `\[ … \]` for displayed formulas, `itemize`/`enumerate` for lists,
`tabular` for small tables. No `\section` commands. Tone: clear, warm,
direct ("you"), no fluff, no claims about scores.

## Testing (mandatory before you finish)

```bash
cd books/asvab-math
.venv/bin/python -m asvab.selftest 7 -n 300        # must print OK
.venv/bin/python -m asvab.preview 7 --png          # must compile
```

Then **look at** the PNG pages (`build/preview_ch07-*.png`, use the Read
tool) and read every problem and solution on them as a student would.
Fix: wrong math, unclear wording, unrealistic numbers, choices that give
the answer away, layout problems (figure too big, overflow). Re-run both
commands after fixes. Also read the selftest samples (`selftest 7 -n 50`
without `-q`).

The selftest reports `keys={…}` — the distribution of the correct answer's
position; if one template has the answer almost always at the same letter
(e.g. A in >60 % of draws), add distractors on the other side of the
answer.
