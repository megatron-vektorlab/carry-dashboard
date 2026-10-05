# KDP listing — Cozy Mystery Logic Puzzles for Beginners

Copy-paste values for the Amazon KDP "Paperback Details", "Content" and
"Rights & Pricing" pages. (Upute na hrvatskom su u `README.md`.)

## Paperback details

| Field | Value |
|---|---|
| Language | English |
| Book title | **Cozy Mystery Logic Puzzles for Beginners** |
| Subtitle | **100 Large Print Whodunit Grid Puzzles from Easy to Expert, with Step-by-Step Lessons, 3 Hints per Puzzle, and Every Solution Explained** |
| Series | **The Thimble Harbor Puzzle School** — number **1** |
| Edition number | 1 |
| Author | Ivan Sikuten *(must match `lp/config.py` → cover and title page; change all three together if you use a pen name)* |
| Contributors | — |
| Publishing rights | I own the copyright and I hold necessary publishing rights |
| Primary audience | Sexually explicit: No · Reading age: leave empty (adult) or 12+ |
| Primary marketplace | Amazon.com |

Title + subtitle = 176 characters (KDP limit 200). The cover shows the same
title; the subtitle is shortened on the cover, which KDP allows.

### Description (paste into the HTML-capable description box)

```html
<b>The cozy mystery logic puzzle book that teaches you, so you never get stuck.</b>

<p>Welcome to Thimble Harbor, a small New England town with one ferry, one lighthouse, and far too many opinions about pie. Retired puzzle editor Ada Quill needs an apprentice for the Gazette's puzzle desk, and she will teach you everything, one clue at a time.</p>

<p>You start with swapped jam labels at the church supper and a goat loose in the pie tent. By winter you are ready for the Lighthouse Affair: the town's beloved 150-year-old Keeper's Lamp vanishes the night before the Lantern Festival, and five linked cases lead to one final question. Who took it?</p>

<h4>What's inside</h4>
<ul>
<li><b>100 logic grid puzzles</b> from one-star warm-ups to five-star whodunits, each with its own little story.</li>
<li><b>Six friendly lessons</b> with pictures of the grid, step by step: your first grid, the staircase grid, line-ups, truth-tellers and fibbers, clues that team up, and one careful "Suppose".</li>
<li><b>A three-step hint ladder for every puzzle</b> (plus a "Stuck halfway?" hint for the hardest ones), kept in separate sections so you never spoil the next step by accident.</li>
<li><b>Every solution explained</b> in plain words: the answer table first, then the key idea and the reasoning.</li>
<li><b>Large 16-point print</b> for every word you read, big grids with room to write, and a clean, uncluttered layout.</li>
<li>A town map, a puzzle tracker, blank grids, a clue-language cheat sheet, "common mistakes and quick repairs", and a certificate for the honorary detective who finishes the book.</li>
<li><b>Every puzzle checked by computer</b> to have exactly one solution, and every explanation checked against the clues.</li>
</ul>

<p>No murders and nothing gory: just mischief, muddles, and a whole town of neighbors who could use your help. A thoughtful gift for anyone who loves cozy mysteries, crosswords or sudoku and has always wanted to learn logic puzzles.</p>
```

### Keywords (7 boxes)

1. `logic puzzles for adults large print`
2. `cozy mystery puzzle book`
3. `logic grid puzzles for beginners`
4. `whodunit puzzles detective games`
5. `brain games for seniors large print`
6. `detective logic puzzles for adults`
7. `gift for puzzle lovers mystery fans`

### Categories (pick 3)

1. Books › Humor & Entertainment › Puzzles & Games › Logic & Brain Teasers
2. Books › Humor & Entertainment › Puzzles & Games › Puzzles
3. Books › Mystery, Thriller & Suspense › Mystery › Cozy *(or Large Print)*

Low-content book: **No**. Large-print book: **Yes** (every reading text is
16 pt; the QA script checks this).

## Content

| Field | Value |
|---|---|
| ISBN | Get a free KDP ISBN |
| Publication date | leave empty (= today) |
| Print options | Black & white interior, **white paper** |
| Trim size | **8.5 × 11 in** (21.59 × 27.94 cm) |
| Bleed settings | **No bleed** |
| Paperback cover finish | **Matte** |
| Manuscript | `output/Cozy-Mystery-Logic-Puzzles-interior.pdf` |
| Book cover | "Upload a cover you already have" → `output/Cozy-Mystery-Logic-Puzzles-cover.pdf` |
| AI-generated content | **Yes.** Text: *AI-generated* (puzzles were generated and verified by software; stories, hints, solutions and lessons were written by an AI model and checked by software and by the publisher). Images: *AI-generated* (cover, map and grids were drawn by AI-written code). |

The cover PDF's spine width is computed from the interior page count. If the
interior changes, rebuild the cover (`python -m lp.cover`) before uploading —
KDP rejects a cover whose spine doesn't match.

## Rights & pricing

* Territories: all territories (worldwide rights).
* Royalty: 60 %.
* Suggested list price: **$15.99** (UK £12.99, EU €14.99, CA $21.99, AU $24.99).
  Comparable large-print logic and cozy puzzle books sell for $9.99–$16.
* Royalty estimate (US): see the page count in `README.md`. Printing cost for
  black-and-white 8.5 × 11 is $1.00 + $0.017 per page (≈ $5.70 at 276 pages),
  so 60 % × $15.99 − $5.70 ≈ **$3.90 per sale** (at $14.99 ≈ $3.30). KDP's
  pricing calculator is authoritative.
* Expanded distribution: optional; leave off at launch.

## Marketing images

`output/front-cover.png` (front cover) and sample pages in
`output/marketing/` (a lesson page, a puzzle spread, the hint ladder and a
solution page) — use them for A+ Content and ads.

## After publishing

* **A+ Content** (free): show a lesson page with grid pictures, a puzzle page,
  a hint page and a solution, and the town map.
* **Sponsored Products ads**: start small ($3–$5/day) on `logic puzzles large
  print`, `cozy mystery puzzle book`, `logic grid puzzles` and competitor
  titles; cut keywords whose ACOS stays above ~60 % after two weeks.
* Ask early readers for honest reviews — never offer payment or free copies
  in exchange for reviews (Amazon policy).
