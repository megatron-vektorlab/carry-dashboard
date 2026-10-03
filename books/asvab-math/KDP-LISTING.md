# KDP listing — ASVAB Math Workbook

Copy-paste values for the Amazon KDP "Paperback Details", "Content" and
"Rights & Pricing" pages. (Upute na hrvatskom su u `README.md`.)

## Paperback details

| Field | Value |
|---|---|
| Language | English |
| Book title | **ASVAB Math Workbook** |
| Subtitle | **1,000 Practice Problems with Step-by-Step Solutions** |
| Series | — (leave empty) |
| Edition number | 1 |
| Author | Ivan Sikuten *(must match `asvab/config.py` → cover and title page)* |
| Contributors | — |
| Publishing rights | I own the copyright and I hold necessary publishing rights |
| Primary audience | Sexually explicit: No · Reading age: 16 – 18+ (leave max empty) |
| Primary marketplace | Amazon.com |

### Description (paste into the HTML-capable description box)

```html
<b>Raise your AFQT with the math practice that actually moves scores: lots of realistic problems, every one solved step by step.</b>

<p>Arithmetic Reasoning and Mathematics Knowledge make up about half of your AFQT score&mdash;the number that decides whether you can enlist and which jobs you qualify for. There is no calculator on the ASVAB, and no formula sheet. What you need is practice: seeing each type of question often enough that you know the first step the moment you read it.</p>

<p>This workbook gives you <b>1,000 ASVAB-style math problems</b>, each with a complete, hand-worked solution.</p>

<h4>What's inside</h4>
<ul>
<li><b>A 30-question diagnostic test</b> that maps every question to a chapter, so you know exactly where to start.</li>
<li><b>27 focused chapters</b>: whole numbers, negatives, factors and primes, fractions, decimals, percents, ratios, exponents, roots, algebraic expressions, equations, inequalities, systems, polynomials, factoring and quadratics, angles, triangles, area, circles, volume, coordinate geometry, money and wages, interest and commission, distance-rate-time, work and mixtures, averages and probability, and measurement.</li>
<li><b>Key Concepts pages</b> for every chapter with rules, formulas, a worked example, a no-calculator tip, and the common traps test writers use.</li>
<li><b>750 topic drills</b> arranged from warm-up to test level to challenge.</li>
<li><b>4 full-length math practice tests</b> (30 Arithmetic Reasoning + 25 Mathematics Knowledge questions each, timed like the paper ASVAB) with bubble answer sheets.</li>
<li><b>Step-by-step solutions for all 1,000 problems</b>&mdash;plus <b>"Why not?" notes</b> that name the exact mistake behind each tempting wrong answer, so you learn from every miss.</li>
<li><b>Every answer verified</b>: each answer was computed exactly with computer algebra and confirmed by a second, independent calculation.</li>
<li>A one-page <b>formula sheet</b>, a <b>mental-math toolkit</b>, quick reference tables, a <b>glossary</b> of math terms, and a <b>progress tracker</b>.</li>
</ul>

<p>Whether you are heading to MEPS for the CAT-ASVAB, taking the paper test at school, or retesting for a better job, this workbook builds the speed and confidence to answer math questions without a calculator.</p>

<p><i>ASVAB is a registered trademark of the U.S. Department of Defense, which was not involved in the production of, and does not endorse, this book.</i></p>
```

### Keywords (7 boxes)

1. `asvab math practice test book`
2. `arithmetic reasoning practice questions`
3. `mathematics knowledge asvab prep`
4. `afqt study guide 2026`
5. `military entrance exam math workbook`
6. `asvab prep army navy air force marines`
7. `no calculator math word problems`

### Categories (pick 3)

1. Books › Test Preparation › Military  *(Study Aids › Armed Forces)*
2. Books › Science & Math › Mathematics › Study & Teaching
3. Books › Test Preparation › Study Guides

Low-content book: **No**. Large-print book: **No**.

## Content

| Field | Value |
|---|---|
| ISBN | Get a free KDP ISBN |
| Publication date | leave empty (= today) |
| Print options | Black & white interior, **white paper** |
| Trim size | **8.5 × 11 in** (21.59 × 27.94 cm) |
| Bleed settings | **No bleed** |
| Paperback cover finish | **Matte** |
| Manuscript | `output/ASVAB-Math-Workbook-interior.pdf` |
| Book cover | "Upload a cover you already have" → `output/ASVAB-Math-Workbook-cover.pdf` |
| AI-generated content | **Yes.** Text: *AI-generated* (problems, solutions and explanations were written by an AI model, answers verified with SymPy, reviewed by the publisher). Images: *AI-generated* (cover and diagrams were produced by AI-written code). |

The cover PDF's spine width is computed from the interior page count. If the
interior changes, rebuild the cover (`python -m asvab.cover`) before
uploading — KDP rejects a cover whose spine doesn't match.

## Rights & pricing

* Territories: all territories (worldwide rights).
* Royalty: 60 %.
* Suggested list price: **$19.99** (UK £15.99, EU €18.99, CA $26.99, AU $29.99).
  Comparable ASVAB math-only workbooks sell for $14–$30; the big all-subject
  guides (Kaplan, Mometrix, Trivium) for $25–$45.
* Royalty estimate (US): this build has **255 pages**. KDP's printing cost
  for a black-and-white 8.5 × 11 paperback is a fixed $1.00 plus $0.017 per
  page → **≈ $5.34 per copy**. Royalty = 60 % × $19.99 − $5.34 ≈ **$6.66 per
  sale** (at $17.99: ≈ $5.46). Confirm in KDP's pricing calculator, which is
  authoritative.
* Expanded distribution: optional (lower royalty, requires a higher list
  price; leave off at launch).

## Marketing images

`output/front-cover.png` (front cover, 1600 px wide) and three sample pages in
`output/marketing/` (Key Concepts, a practice page with figures, a solutions
page with "Why not?" notes) — use them for A+ Content and ads.

## After publishing

* **A+ Content** (free, under Marketing): add a comparison module showing a
  sample problem + solution page and the "Why not?" feature.
* **Author Central**: claim the book, add a short bio.
* **Sponsored Products ads**: start with manual keyword targeting on
  `asvab math`, `asvab arithmetic reasoning`, `asvab practice test`,
  `afqt math`, at a low daily budget ($3–$5/day), and cut keywords whose
  ACOS stays above ~60 % after two weeks.
* Ask early readers (recruiting-prep groups, JROTC instructors, friends) for
  honest reviews — never offer payment or free copies in exchange for
  reviews (Amazon policy).
