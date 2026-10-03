"""Chapter 7 - Ratios & Proportions."""
from fractions import Fraction
from math import gcd

import sympy as sp

from ..core import (R, Q, Problem, need, num, dec, frac, mixed, money, m, F, tx,
                    dec_raw, int_raw, frac_raw, mixed_raw, person, soldier,
                    choose, template, x, y)

NUM = 7
TITLE = "Ratios & Proportions"
PART = 1

INTRO = r"""
A \emph{ratio} compares two quantities; a \emph{proportion} says that two
ratios are equal. Together they handle recipes, maps, mixtures, unit prices,
and every ``how many of each'' question on the test.

\begin{concept}{Writing and simplifying ratios}
The ratio of $a$ to $b$ can be written $a:b$, ``$a$ to $b$,'' or
$\frac{a}{b}$. \textbf{Order matters}: the first quantity named goes first.
\begin{itemize}
\item Simplify a ratio like a fraction: divide both terms by their greatest
  common factor. $18:24 = 3:4$ (divide both by $6$).
\item Put both amounts in the \emph{same unit} first: $2$ feet to $8$ inches
  is $24$ inches to $8$ inches, so the ratio is $24:8 = 3:1$.
\end{itemize}
\end{concept}

\begin{concept}{Ratios as parts of a whole}
If the ratio of boys to girls is $3:5$, think of the group as $3 + 5 = 8$
equal \emph{parts}: boys are $\frac{3}{8}$ of the group and girls are
$\frac{5}{8}$. With $40$ people, one part is $40 \div 8 = 5$, so there are
$3 \times 5 = 15$ boys and $5 \times 5 = 25$ girls.
\end{concept}

\begin{concept}{Proportions, unit rates, and direct variation}
\begin{itemize}
\item In a proportion $\frac{a}{b} = \frac{c}{d}$ the \emph{cross products}
  are equal: $a \times d = b \times c$. To solve $\frac{x}{12} = \frac{15}{36}$,
  write $36x = 12 \times 15 = 180$, so $x = 180 \div 36 = 5$.
\item A \emph{unit rate} compares to one unit: $300$ miles on $12$ gallons
  is $300 \div 12 = 25$ miles per gallon.
\item ``$y$ varies directly with $x$'' means $y = kx$: the ratio
  $\frac{y}{x}$ is always the same number $k$.
\end{itemize}
\end{concept}

\begin{example}{Worked example}
A cookie recipe uses $3$ cups of flour to make $24$ cookies. How many cups of
flour are needed to make $40$ cookies?

\textbf{Solution.} Keep the same order in both ratios (cups over cookies):
$\frac{3}{24} = \frac{x}{40}$. Cross-multiply: $24x = 3 \times 40 = 120$.
Divide: $x = 120 \div 24 = 5$ cups.
\end{example}

\begin{tip}
Simplify before you multiply. In the example, $\frac{3}{24} = \frac{1}{8}$:
one cup makes $8$ cookies, so $40$ cookies need $40 \div 8 = 5$ cups. Small
numbers mean fewer mistakes.
\end{tip}

\begin{trap}
\begin{itemize}
\item Reversing the order: ``girls to boys'' is $5:3$, not $3:5$.
\item Treating the ratio $3:5$ as the fraction $\frac{3}{5}$ of the
  \emph{total}; the total has $3 + 5 = 8$ parts.
\item Adding instead of scaling: going from $24$ to $40$ cookies does
  \emph{not} mean adding $16$ cups of flour.
\item Comparing amounts in different units (feet with inches, hours with
  minutes) without converting first.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# private helpers
# --------------------------------------------------------------------------

def _ratio(v) -> str:
    """Positive rational p/q shown as the ratio $p:q$ in lowest terms."""
    v = sp.Rational(Q(v))
    need(v > 0)
    return m(f"{int_raw(v.p)}:{int_raw(v.q)}")


def _rt(p, q) -> str:
    """Raw ratio text p:q (no simplification)."""
    return f"{int_raw(p)}:{int_raw(q)}"


def _qty(v, one: str, many: str) -> str:
    """'$3$ cups', '$1$ cup', '$2\\frac{1}{2}$ cups' (mixed numbers)."""
    word = one if Q(v) == 1 else many
    return f"{m(mixed_raw(v))} {word}"


def _coprime_pair(rng, lo, hi):
    while True:
        p, q = rng.randint(lo, hi), rng.randint(lo, hi)
        if p != q and gcd(p, q) == 1:
            return p, q


def _gcf_step(A, B) -> str:
    g = gcd(A, B)
    if g == 1:
        return (f"{num(A)} and {num(B)} have no common factor other than 1, so "
                f"{m(_rt(A, B))} is already in simplest form.")
    return (f"Divide both terms by their greatest common factor, {num(g)}: "
            f"{m(f'{int_raw(A)} \\div {g} = {int_raw(A // g)}')} and "
            f"{m(f'{int_raw(B)} \\div {g} = {int_raw(B // g)}')}. "
            f"The ratio is {m(_rt(A // g, B // g))}.")


# --------------------------------------------------------------------------
# templates
# --------------------------------------------------------------------------

_PAIRS = [
    # (setting with {A} and {B}, name of first group, name of second group)
    ("A box holds {A} red pens and {B} blue pens.", "red pens", "blue pens"),
    ("A basketball team won {A} games and lost {B} games this season. There were no ties.",
     "wins", "losses"),
    ("A recruiting office signed up {A} recruits for the Army and {B} recruits for the Navy last month.",
     "Army recruits", "Navy recruits"),
    ("A motor pool has {A} trucks and {B} Humvees.", "trucks", "Humvees"),
    ("A garden has {A} tomato plants and {B} pepper plants.", "tomato plants", "pepper plants"),
    ("On a ruck march, a squad covered {A} miles on paved roads and {B} miles on dirt trails.",
     "paved miles", "trail miles"),
    ("A used-car lot has {A} sedans and {B} pickup trucks for sale.", "sedans", "pickup trucks"),
    ("A training class has {A} students who passed the first exam and {B} who did not.",
     "students who passed", "students who did not pass"),
]

_UNITS = [
    # big unit (sing, pl), small unit (sing, pl), factor, slip factor, big range, small values
    ("foot", "feet", "inch", "inches", 12, 10, range(1, 6), range(2, 31)),
    ("yard", "yards", "foot", "feet", 3, None, range(1, 9), range(1, 21)),
    ("hour", "hours", "minute", "minutes", 60, 100, range(1, 5), range(5, 56, 5)),
    ("pound", "pounds", "ounce", "ounces", 16, None, range(1, 6), range(2, 15)),
    ("gallon", "gallons", "quart", "quarts", 4, None, range(1, 7), range(1, 16)),
    ("minute", "minutes", "second", "seconds", 60, 100, range(1, 5), range(10, 51, 5)),
]


@template("MK")
def simplify_ratio(rng, lvl):
    if lvl == 1:
        p, q = _coprime_pair(rng, 1, 9)
        g = rng.randint(2, 12)
        A, B = g * p, g * q
        need(A <= 90 and B <= 90)
        setting, n1, n2 = rng.choice(_PAIRS)
        swap = rng.random() < 0.4
        first, second = (n2, n1) if swap else (n1, n2)
        P, S = (B, A) if swap else (A, B)
        ans = R(P, S)
        return Problem(
            stem=(setting.format(A=num(A), B=num(B))
                  + f" What is the ratio of {first} to {second}, in simplest form?"),
            answer=ans,
            fmt=_ratio,
            wrong=[
                (R(S, P), f"reverses the order; the question asks for {first} to {second}"),
                (R(P, P + S), f"compares the {first} to the total instead of to the {second}"),
                (R(S, P + S), f"compares the {second} to the total"),
            ],
            steps=[
                f"Write the amounts in the order asked, {first} first: {m(_rt(P, S))}.",
                _gcf_step(P, S),
            ],
            check=sp.Rational(P, S),
            verify=lambda v: Fraction(int(v.p), int(v.q)) == Fraction(P, S),
        )

    big, bigs, small, smalls, f, slip, brange, srange = rng.choice(_UNITS)
    a = rng.choice(list(brange))
    b = rng.choice(list(srange))
    need(b % f != 0)                      # the small amount is not a whole number of big units
    big_first = rng.random() < 0.6
    A_conv = a * f
    P, S = (A_conv, b) if big_first else (b, A_conv)
    ans = R(P, S)
    need(max(ans.p, ans.q) <= 20 and ans != 1)
    a_txt = f"{num(a)} {big if a == 1 else bigs}"
    b_txt = f"{num(b)} {small if b == 1 else smalls}"
    first, second = (a_txt, b_txt) if big_first else (b_txt, a_txt)
    raw = R(a, b) if big_first else R(b, a)
    wrong = [
        (raw, f"forgets to change {bigs} to {smalls} before comparing"),
        (1 / ans, "reverses the order of the ratio"),
    ]
    if slip:
        s_val = R(a * slip, b) if big_first else R(b, a * slip)
        wrong.append((s_val, f"uses {slip} {smalls} in a {big} instead of {f}"))
    wrong.append((R(a, b * f) if big_first else R(b * f, a),
                  f"multiplies the {smalls} by {f} instead of the {bigs}"))
    return Problem(
        stem=choose(rng,
                    f"What is the ratio of {first} to {second}, in simplest form?",
                    f"Written in simplest form, what is the ratio of {first} to {second}?"),
        answer=ans,
        fmt=_ratio,
        wrong=wrong,
        steps=[
            f"Both amounts must be in the same unit. Change {bigs} to {smalls}: "
            f"{m(f'{a} \\times {f} = {int_raw(A_conv)}')} {smalls}.",
            f"Now compare {smalls} to {smalls}: {m(_rt(P, S))}.",
            _gcf_step(P, S),
        ],
        check=sp.Rational(a * f, b) if big_first else sp.Rational(b, a * f),
        verify=lambda v: Fraction(int(v.p), int(v.q)) == (Fraction(A_conv, b) if big_first else Fraction(b, A_conv)),
    )


@template("MK")
def solve_proportion(rng, lvl):
    # x/a = c/d (level 1) or a/x = c/d (level 2); the unknown is always an integer
    p, q = _coprime_pair(rng, 1, 9)
    s, t = rng.sample(range(2, 9), 2)
    if lvl == 1:
        a, xv, c, d = q * s, p * s, p * t, q * t
        need(a <= 48 and c <= 60 and d <= 72 and xv > 1)
        form = rng.choice(["x/a", "c/d first"])
        if form == "x/a":
            stem_eq = f"{F('x', a)} = {F(c, d)}"
        else:
            stem_eq = f"{F(c, d)} = {F('x', a)}"
        cross = a * c
        wrong = [
            (a * c, f"multiplies {a} by {c} but forgets to divide by {d}"),
            (c + a - d, f"adds the difference of the denominators ({m(f'{a} - {d}')}) instead of scaling"),
            (R(a * d, c), f"cross-multiplies the wrong pair: {m(f'{a} \\times {d} \\div {c}')}"),
            (R(c * d, a), None),
        ]
        steps = [
            f"Cross-multiply: {m(f'{d} \\times x = {a} \\times {c}')}, so {m(f'{d}x = {int_raw(cross)}')}.",
            f"Divide both sides by {d}: {m(f'x = {int_raw(cross)} \\div {d} = {int_raw(xv)}')}.",
        ]
        g = gcd(c, d)
        tip = None
        if g > 1 and d // g == a:
            tip = (f"Simplify first: {m(F(c, d) + ' = ' + F(c // g, d // g))}, so "
                   f"{m(F('x', a) + ' = ' + F(c // g, a))} and {m(f'x = {c // g}')}.")
        elif g > 1:
            tip = (f"Simplify {m(F(c, d))} to {m(F(c // g, d // g))} first; the numbers get smaller: "
                   f"{m(f'{d // g}x = {a} \\times {c // g}')}.")
        return Problem(
            stem=choose(rng, f"Solve for {m('x')}: {m(stem_eq)}",
                        f"If {m(stem_eq)}, what is the value of {m('x')}?"),
            answer=Q(xv),
            fmt=num,
            wrong=wrong,
            steps=steps,
            tip=tip,
            check=sp.solve(sp.Eq(x / a, R(c, d)), x)[0],
            verify=lambda v: Fraction(int(v), a) == Fraction(c, d),
        )

    # level 2: the unknown is in the denominator
    a, xv, c, d = p * s, q * s, p * t, q * t
    need(a <= 40 and c <= 60 and d <= 72 and xv > 1 and a != c)
    stem_eq = f"{F(a, 'x')} = {F(c, d)}"
    cross = a * d
    return Problem(
        stem=choose(rng, f"Solve for {m('x')}: {m(stem_eq)}",
                    f"If {m(stem_eq)}, what is the value of {m('x')}?"),
        answer=Q(xv),
        fmt=num,
        wrong=[
            (R(a * c, d), f"solves as if {m('x')} were on top, giving {m(f'{a} \\times {c} \\div {d}')}"),
            (Q(a * d), f"multiplies {a} by {d} but forgets to divide by {c}"),
            (d + a - c, "adds the difference of the numerators instead of scaling"),
            (R(c * d, a), None),
        ],
        steps=[
            f"Cross-multiply: {m(f'{c} \\times x = {a} \\times {d}')}, so {m(f'{c}x = {int_raw(cross)}')}.",
            f"Divide both sides by {c}: {m(f'x = {int_raw(cross)} \\div {c} = {int_raw(xv)}')}.",
            f"Check: {m(F(a, xv))} and {m(F(c, d))} both simplify to {m(frac_raw(R(a, xv)))}. \\checkmark",
        ],
        check=sp.solve(sp.Eq(R(a) / x, R(c, d)), x)[0],
        verify=lambda v: Fraction(a, int(v)) == Fraction(c, d),
    )


_GROUPS = [
    # (sentence with {p} and {q}, first group, second group, whole)
    ("The ratio of boys to girls in a class is {r}.", "boys", "girls", "the class"),
    ("In a parking lot, the ratio of cars to trucks is {r}. There are no other vehicles.",
     "cars", "trucks", "the vehicles"),
    ("At a recruiting station, the ratio of Army enlistees to Navy enlistees this week is {r}, "
     "and no one enlisted in any other branch.", "Army enlistees", "Navy enlistees", "the enlistees"),
    ("A bag holds only red and green marbles, in the ratio {r} (red to green).",
     "red marbles", "green marbles", "the marbles"),
    ("In a company, the ratio of officers to enlisted soldiers is {r}.",
     "officers", "enlisted soldiers", "the company"),
    ("A team's ratio of wins to losses is {r}, and it has had no ties.",
     "wins", "losses", "the games played"),
]


@template("MK")
def part_of_whole(rng, lvl):
    p, q = _coprime_pair(rng, 1, 9)
    need(p + q <= 13)
    setting, g1, g2, whole = rng.choice(_GROUPS)
    if g1 == "officers":
        need(p < q)
    ask_first = rng.random() < 0.6
    part, other, gname = (p, q, g1) if ask_first else (q, p, g2)
    ans = R(part, p + q)
    return Problem(
        stem=(setting.format(r=m(_rt(p, q)))
              + f" What fraction of {whole} {'are' if not whole.startswith('the games') else 'are'} {gname}?"),
        answer=ans,
        fmt=frac,
        wrong=[
            (R(part, other), f"uses the ratio {m(_rt(part, other))} as if it were the fraction of the total"),
            (R(other, p + q), f"is the fraction for the other group"),
            (R(other, part), "flips the ratio"),
        ],
        steps=[
            f"Think in parts: {m(f'{p} + {q} = {p + q}')} parts make up the whole group.",
            f"The {gname} are {part} of those {p + q} parts, so the fraction is {m(frac_raw(ans))}.",
        ],
        check=Fraction(part, p + q),
    )


_TOTALS = [
    # setting with {T} and {r}; names; military?
    ("A recruiting station signed up {T} recruits last month, all for either the Army or the Navy. "
     "The ratio of Army recruits to Navy recruits was {r}.", "Army recruits", "Navy recruits", range(20, 200)),
    ("A parking lot holds {T} vehicles, all cars or trucks. The ratio of cars to trucks is {r}.",
     "cars", "trucks", range(20, 300)),
    ("A softball team played {T} games and had no ties. The ratio of wins to losses was {r}.",
     "wins", "losses", range(12, 60)),
    ("A battalion sent {T} soldiers to two training courses, and the ratio of soldiers in the "
     "driving course to soldiers in the first-aid course was {r}.", "soldiers in the driving course",
     "soldiers in the first-aid course", range(30, 240)),
    ("A fruit stand sold {T} pieces of fruit on Saturday, all apples or oranges. The ratio of apples "
     "to oranges sold was {r}.", "apples", "oranges", range(30, 300)),
    ("A school club has {T} members. The ratio of juniors to seniors in the club is {r}, and every "
     "member is a junior or a senior.", "juniors", "seniors", range(15, 80)),
]


@template("AR")
def ratio_total(rng, lvl):
    p, q = _coprime_pair(rng, 1, 9)
    setting, n1, n2, trange = rng.choice(_TOTALS)
    s = p + q
    T = rng.choice([t for t in trange if t % s == 0])
    one = T // s
    need(one >= 2)
    ask_first = rng.random() < 0.5
    part, other, name, oname = (p, q, n1, n2) if ask_first else (q, p, n2, n1)
    ans = part * one
    return Problem(
        stem=setting.format(T=num(T), r=m(_rt(p, q))) + f" How many {name} were there?"
             .replace("were there", "are there" if "has" in setting or "holds" in setting else "were there"),
        answer=Q(ans),
        fmt=num,
        wrong=[
            (Q(other * one), f"is the number of {oname}"),
            (R(T * part, other), f"treats the ratio as the fraction {m(F(part, other))} of the total"),
            (Q(one), "stops after finding the size of one part"),
            (R(T, part), None),
        ],
        steps=[
            f"Add the terms of the ratio to get the number of equal parts: {m(f'{p} + {q} = {s}')}.",
            f"Find the size of one part: {m(f'{int_raw(T)} \\div {s} = {one}')}.",
            f"The {name} make up {part} parts: {m(f'{part} \\times {one} = {int_raw(ans)}')}.",
        ],
        tip=f"Check: {m(f'{int_raw(ans)} + {int_raw(other * one)} = {int_raw(T)}')}, and "
            f"{m(_rt(p * one, q * one))} simplifies to {m(_rt(p, q))}.",
        check=Fraction(T * part, s),
        verify=lambda v: Fraction(int(v), T - int(v)) == Fraction(part, other),
    )


_RECIPES = [
    # (stem with {a} {b} {c}, unit (sing, pl), a-values, b-values, c-step, c-range, fmt, military)
    ("A cookie recipe uses {a} of flour to make {b} cookies. How many cups of flour are needed to "
     "make {c} cookies?", ("cup", "cups"), [1, 2, 3, 4], [12, 16, 18, 24, 30, 36], 2, (12, 90), mixed),
    ("A mess hall recipe uses {a} of rice to feed {b} soldiers. How many pounds of rice are needed "
     "to feed {c} soldiers?", ("pound", "pounds"), range(3, 13), [20, 25, 30, 40, 50], 5, (50, 300), dec),
    ("A pancake recipe calls for {a} to make {b} pancakes. How many eggs are needed to make {c} "
     "pancakes?", ("egg", "eggs"), [2, 3, 4], [8, 10, 12, 15, 16], 1, (16, 60), num),
    ("The label on a bag of lawn fertilizer says to use {a} for every {b} square feet of lawn. "
     "How many pounds are needed for {c} square feet?", ("pound", "pounds"), [2, 3, 4, 5, 6],
     [500, 1000], 250, (1250, 6000), dec),
    ("A field kitchen brews {a} of coffee for every {b} soldiers. How many gallons should it "
     "brew for {c} soldiers?", ("gallon", "gallons"), [2, 3, 4, 5], [20, 25, 30, 40], 5, (60, 240), dec),
    ("A painter used {a} of paint to cover {b} square feet of fence. At the same rate, how many "
     "gallons are needed to cover {c} square feet?", ("gallon", "gallons"), [2, 3, 4],
     [600, 700, 800], 50, (900, 2800), dec),
    ("A concrete mix uses {a} of cement for every {b} bags of sand. How many bags of cement are "
     "needed for {c} bags of sand?", ("bag", "bags"), [1, 2, 3], [3, 4, 5], 1, (9, 40), num),
]


@template("AR")
def recipe_scale(rng, lvl):
    stem_t, (one, many), avals, bvals, cstep, (clo, chi), fmt = rng.choice(_RECIPES)
    a = rng.choice(list(avals))
    b = rng.choice(bvals)
    c = rng.choice(range(clo, chi + 1, cstep))
    need(c != b)
    ans = R(a * c, b)
    if lvl == 2:
        need(ans.q in (1, 2) and c > b and ans > a)
    else:
        need(ans.q in (2, 3, 4) and c > b)
        if fmt is dec:
            need(ans.q in (2, 4))
    if fmt is num:
        need(ans.is_integer)
    if fmt is mixed or lvl == 3:
        fmt = mixed
    unit_a = f"{m(mixed_raw(a))} {one if a == 1 else many}"
    stem = stem_t.format(a=unit_a, b=num(b), c=num(c))
    cross = a * c
    wrong = [
        (ans - a, f"finds only the extra amount needed and forgets the original {m(mixed_raw(a))}"),
        (R(a * b, c), "sets up the proportion upside down"),
        (Q(a + c - b), "adds the difference in quantity instead of scaling"),
        (R(a, b) * (c // b) if c // b > 0 else None, None),
    ]
    wrong = [w for w in wrong if w[0] is not None and Q(w[0]) > 0]
    unit_rate = R(b, a)
    tip = None
    if unit_rate.is_integer and unit_rate > 1:
        tip = (f"Unit rate: {m(mixed_raw(1))} {one} serves {m(int_raw(unit_rate))}, so divide: "
               f"{m(f'{int_raw(c)} \\div {int_raw(unit_rate)} = {mixed_raw(ans)}')}."
               .replace("serves", "covers" if "square feet" in stem else "is enough for"))
    return Problem(
        stem=stem,
        answer=ans,
        fmt=fmt,
        wrong=wrong,
        steps=[
            f"Set up a proportion with the same order on both sides ({many} over the other quantity): "
            f"{m(F(int_raw(a), int_raw(b)) + ' = ' + F('x', int_raw(c)))}.",
            f"Cross-multiply: {m(f'{int_raw(b)}x = {int_raw(a)} \\times {int_raw(c)} = {int_raw(cross)}')}.",
            f"Divide by {num(b)}: {m(f'x = {int_raw(cross)} \\div {int_raw(b)} = {mixed_raw(ans)}')} {many}."
            .replace(f"= {mixed_raw(ans)}", f"= {mixed_raw(ans)}" if ans.is_integer else
                     (f"= {F(int_raw(cross), int_raw(b))} = {mixed_raw(ans)}" if fmt is mixed
                      else f"= {dec_raw(ans)}")),
        ],
        tip=tip,
        check=Fraction(a, b) * c,
        verify=lambda v: Fraction(int(sp.Rational(v).p), int(sp.Rational(v).q)) / c == Fraction(a, b),
    )


_MAPS = [
    # (stem with {s} scale and {d} map distance, scale unit, real unit sing/pl, scales, blueprint?)
    ("On a road map, 1 inch represents {s} miles. Two towns are {d} inches apart on the map. "
     "What is the actual distance between the towns?", ("mile", "miles"), [10, 20, 25, 30, 40, 50, 60], "map"),
    ("On a land navigation map, 1 inch represents {s} miles. Two checkpoints are {d} inches apart "
     "on the map. How far apart are the checkpoints on the ground?", ("mile", "miles"), [2, 4], "map"),
    ("A model of a Navy destroyer is built to a scale of 1 inch = {s} feet. The model is {d} inches "
     "long. How long is the actual ship?", ("foot", "feet"), [8, 10, 12, 16, 20], "model"),
    ("A floor plan is drawn to a scale of 1 inch = {s} feet. A wall measures {d} inches on the "
     "plan. How long is the actual wall?", ("foot", "feet"), [2, 4, 6, 8], "plan"),
]


@template("AR")
def map_scale(rng, lvl):
    if lvl == 2:
        if rng.random() < 0.3:
            # blueprint with a fractional scale: 1/4 inch = 1 foot
            k = rng.choice([2, 4])              # 1/k inch = 1 foot
            whole = rng.randint(2, 9)
            part = rng.choice([R(1, 4), R(1, 2), R(3, 4)] if k == 4 else [R(1, 2)])
            d = whole + part
            ans = d * k
            need(ans.is_integer)
            thing = rng.choice(["wall", "room", "deck", "garage", "barracks hallway"])
            return Problem(
                stem=(f"A blueprint uses the scale {m(F(1, k))} inch = 1 foot. A {thing} is "
                      f"{m(mixed_raw(d))} inches long on the blueprint. How long is the actual {thing}, in feet?"),
                answer=ans,
                fmt=num,
                wrong=[
                    (d / k, f"multiplies by {m(F(1, k))} instead of finding how many {m(F(1, k))}-inch pieces fit"),
                    (Q(whole * k), f"ignores the {m(frac_raw(part))} inch"),
                    (d + k, None),
                    (ans / 2 if k == 4 else ans * 2, None),
                ],
                steps=[
                    f"Each {m(F(1, k))} inch on the blueprint stands for 1 foot, so each full inch stands for {k} feet.",
                    f"Multiply: {m(f'{mixed_raw(d)} \\times {k} = {int_raw(ans)}')} feet.",
                ],
                tip=f"{m(f'{whole} \\times {k} = {whole * k}')} and {m(f'{frac_raw(part)} \\times {k} = {int_raw(part * k)}')}; together {int_raw(ans)} feet.",
                check=Fraction(int(d.p), int(d.q)) / Fraction(1, k),
                verify=lambda v: v / k == d,
            )
        stem_t, (one, many), scales, kind = rng.choice(_MAPS)
        s = rng.choice(scales)
        whole = rng.randint(2, 9)
        part = rng.choice([0, R(1, 4), R(1, 2), R(3, 4)])
        d = whole + part
        ans = d * s
        need(ans.is_integer or ans.q == 2)
        need(part != 0 or rng.random() < 0.25)
        wrong = [
            (d / s, "divides by the scale instead of multiplying"),
            (Q(d + s), "adds the scale instead of multiplying"),
        ]
        if part:
            wrong.append((Q(whole * s), f"ignores the {m(frac_raw(part))} inch"))
        wrong.append((ans * 2, None))
        return Problem(
            stem=stem_t.format(s=num(s), d=m(mixed_raw(d))),
            answer=ans,
            fmt=unit(dec, one, many),
            wrong=wrong,
            steps=[
                f"Each inch stands for {num(s)} {many}, so multiply the measurement by {num(s)}.",
                (f"{m(f'{mixed_raw(d)} \\times {s} = {dec_raw(ans)}')} {many}." if not part else
                 f"Split it up: {m(f'{whole} \\times {s} = {whole * s}')} and "
                 f"{m(f'{frac_raw(part)} \\times {s} = {dec_raw(part * s)}')}; "
                 f"{m(f'{whole * s} + {dec_raw(part * s)} = {dec_raw(ans)}')} {many}."),
            ],
            check=Fraction(int(d.p), int(d.q)) * s,
        )

    # level 3: a scale that is not "1 inch = ..." (work backward), or area on a floor plan
    if rng.random() < 0.5:
        u = rng.choice([2, 3])                     # u inches = v miles
        v = rng.choice([5, 15, 25, 35, 45, 75, 125])
        need(gcd(u, v) == 1)
        k = rng.randint(3, 12)
        actual = v * k
        ans = Q(u * k)
        place = rng.choice(["two cities", "two Army posts", "a lake and a campground",
                            "two airports", "two exits on a highway"])
        return Problem(
            stem=(f"On a map, {u} inches represent {num(v)} miles. The actual distance between "
                  f"{place} is {num(actual)} miles. How far apart are they on the map?"),
            answer=ans,
            fmt=unit(num, "inch", "inches"),
            wrong=[
                (Q(k), f"divides {num(actual)} by {num(v)} but forgets that the scale uses {u} inches, not 1"),
                (R(actual * v, u), None),
                (R(actual, u), f"divides the distance by {u} instead of using the whole scale"),
                (Q(k + u), None),
                (Q(u * k + u), None),
            ],
            steps=[
                f"Set up a proportion, inches over miles: {m(F(u, int_raw(v)) + ' = ' + F('x', int_raw(actual)))}.",
                f"Cross-multiply: {m(f'{int_raw(v)}x = {u} \\times {int_raw(actual)} = {int_raw(u * actual)}')}.",
                f"Divide: {m(f'x = {int_raw(u * actual)} \\div {int_raw(v)} = {int_raw(ans)}')} inches.",
            ],
            tip=f"Or count how many {num(v)}-mile chunks fit: {m(f'{int_raw(actual)} \\div {v} = {k}')}; each chunk is {u} inches, so {m(f'{k} \\times {u} = {int_raw(ans)}')}.",
            check=Fraction(u, v) * actual,
        )
    s = rng.choice([2, 3, 4, 5, 6, 8])             # 1 inch = s feet
    L, W = rng.sample(range(2, 8), 2)
    L, W = max(L, W), min(L, W)
    need(L * s <= 40 and W * s <= 30)
    ans = Q(L * s * W * s)
    room = rng.choice(["a bedroom", "a garage", "an office", "a storage room", "a classroom", "a dayroom in the barracks"])
    return Problem(
        stem=(f"On a floor plan, 1 inch represents {num(s)} feet. {room[0].upper() + room[1:]} measures "
              f"{num(L)} inches by {num(W)} inches on the plan. What is the actual area of the room, in square feet?"),
        answer=ans,
        fmt=num,
        wrong=[
            (Q(L * W * s), f"multiplies the plan's area by {s} instead of converting each side"),
            (Q(2 * (L * s + W * s)), "finds the perimeter instead of the area"),
            (Q(L * W), "gives the area on the plan, in square inches"),
            (Q(L * s + W * s), None),
        ],
        steps=[
            f"Convert each side: {m(f'{L} \\times {s} = {L * s}')} feet and {m(f'{W} \\times {s} = {W * s}')} feet.",
            f"Area = length {m(r'\times')} width: {m(f'{L * s} \\times {W * s} = {int_raw(ans)}')} square feet.",
        ],
        tip=f"Areas scale by the square of the scale factor: the plan's {m(f'{L * W}')} square inches times {m(f'{s}^2 = {s * s}')}.",
        check=Fraction(L * W) * s ** 2,
    )


_RATES = [
    # (stem builder, answer fmt) -- values chosen so the rate is exact
    "mpg", "beef", "wage", "typing", "convoy", "pump",
]


@template("AR")
def unit_rate(rng, lvl):
    kind = rng.choice(_RATES)
    p = person(rng)
    if kind == "mpg":
        rate = rng.randint(14, 36)
        n = rng.randint(8, 22)
        total = rate * n
        vehicle = rng.choice(["A pickup truck", "A delivery van", "A sedan", "An Army truck", "A minivan"])
        stem = f"{vehicle} traveled {num(total)} miles on {num(n)} gallons of gas. How many miles per gallon did it get?"
        fmt, unit_w, money_like = num, "miles per gallon", False
    elif kind == "beef":
        rate = R(rng.choice(range(13, 27)), 4)     # $3.25 .. $6.50 per pound
        n = rng.choice([2, 3, 4, 5, 6, 8])
        total = rate * n
        item = rng.choice(["ground beef", "chicken breast", "deli turkey", "salmon"])
        stem = f"At a grocery store, {num(n)} pounds of {item} cost {money(total)}. What is the cost per pound?"
        fmt, unit_w, money_like = money, "dollars per pound", True
    elif kind == "wage":
        rate = R(rng.choice(range(24, 51)), 2)     # $12.00 .. $25.00 per hour
        n = rng.choice([4, 6, 8, 10, 12, 20, 25, 30])
        total = rate * n
        stem = f"{p.name} earned {money(total)} for {num(n)} hours of work. How much did {p.he} earn per hour?"
        fmt, unit_w, money_like = money, "dollars per hour", True
    elif kind == "typing":
        rate = rng.randint(30, 80)
        n = rng.randint(3, 12)
        total = rate * n
        stem = f"{p.name} typed a {num(total)}-word report in {num(n)} minutes. How many words per minute did {p.he} type?"
        fmt, unit_w, money_like = num, "words per minute", False
    elif kind == "convoy":
        rate = rng.randint(30, 55)
        n = rng.randint(2, 8)
        total = rate * n
        stem = f"A supply convoy traveled {num(total)} miles in {num(n)} hours. What was its average speed, in miles per hour?"
        fmt, unit_w, money_like = num, "miles per hour", False
    else:
        rate = rng.choice(range(15, 95, 5))
        n = rng.randint(4, 15)
        total = rate * n
        stem = f"A pump empties {num(total)} gallons of water from a flooded basement in {num(n)} minutes. How many gallons per minute does it pump?"
        fmt, unit_w, money_like = num, "gallons per minute", False
    rate = Q(rate)
    wrong = [
        (rate * 10, "misplaces the decimal point (or drops a digit) when dividing"),
        (rate + 1 if not money_like else rate + R(1, 2), None),
        (rate - 1 if not money_like else rate - R(1, 2), None),
        (rate + 2 if not money_like else rate + R(1, 4), None),
    ]
    if rate.is_integer and rate % 10 == 0:
        wrong[0] = (rate / 10, "misplaces a zero when dividing")
    return Problem(
        stem=stem,
        answer=rate,
        fmt=fmt,
        wrong=wrong,
        steps=[
            f"A rate \\emph{{per}} one unit means divide by the number of units: "
            f"{m(f'{dec_raw(total)} \\div {n} = {dec_raw(rate)}')}.",
            f"The unit rate is {m(dec_raw(rate) if not money_like else money(rate)[1:] if False else dec_raw(rate))} {unit_w}."
            .replace(f"{m(dec_raw(rate))} dollars", money(rate) if money_like else f"{m(dec_raw(rate))} dollars"),
        ],
        tip=f"Check by multiplying back: {m(f'{dec_raw(rate)} \\times {n} = {dec_raw(total)}')}.",
        check=Fraction(int(sp.Rational(total).p), int(sp.Rational(total).q)) / n,
        verify=lambda v: v * n == total,
    )


@template("MK")
def direct_variation(rng, lvl):
    k = rng.choice([R(v) for v in range(2, 10)] + [R(v, 2) for v in (3, 5, 7, 9)] + [R(v, 3) for v in (2, 4, 5)])
    x1 = rng.randint(2, 12)
    y1 = k * x1
    need(y1.is_integer)
    phr = choose(rng, f"{m('y')} varies directly with {m('x')}",
                 f"{m('y')} varies directly as {m('x')}",
                 f"{m('y')} is directly proportional to {m('x')}")
    if lvl == 2:
        x2 = rng.randint(2, 20)
        need(x2 != x1)
        y2 = k * x2
        need(y2.is_integer)
        return Problem(
            stem=(f"If {phr}, and {m(f'y = {int_raw(y1)}')} when {m(f'x = {x1}')}, what is the value of "
                  f"{m('y')} when {m(f'x = {x2}')}?"),
            answer=y2,
            fmt=dec,
            wrong=[
                (y1 + (x2 - x1), f"adds the change in {m('x')} instead of multiplying by the constant"),
                (R(y1 * x1, x2), "uses inverse variation (the product stays the same) instead of direct variation"),
                (k, f"stops after finding the constant {m('k')}"),
                (y1 * x2, f"forgets to divide by {x1}"),
            ],
            steps=[
                f"Direct variation means {m('y = kx')}, where {m('k')} stays the same.",
                f"Find {m('k')}: {m(f'k = \\frac{{y}}{{x}} = {F(int_raw(y1), x1)} = {tx(k)}')}.",
                f"Use it: {m(f'y = {tx(k)} \\times {x2} = {int_raw(y2)}')}.",
            ],
            check=sp.solve(sp.Eq(R(y1, x1), y / x2), y)[0],
            verify=lambda v: v * x1 == y1 * x2,
        )

    # level 3
    if rng.random() < 0.6:
        need(not k.is_integer)
        x2 = rng.randint(2, 30)
        y2 = k * x2
        need(y2.is_integer and x2 != x1 and y2 != y1)
        return Problem(
            stem=(f"If {phr}, and {m(f'y = {int_raw(y1)}')} when {m(f'x = {x1}')}, what is the value of "
                  f"{m('x')} when {m(f'y = {int_raw(y2)}')}?"),
            answer=Q(x2),
            fmt=dec,
            wrong=[
                (y2 * k, f"multiplies by {m('k')} instead of dividing by it"),
                (R(x1 * y1, y2), "uses inverse variation instead of direct variation"),
                (x1 + (y2 - y1), f"adds the change in {m('y')} instead of scaling"),
                (y2 * x1 / (y1 + x1), None),
            ],
            steps=[
                f"Direct variation means {m('y = kx')}. Find {m('k')}: {m(f'k = {F(int_raw(y1), x1)} = {tx(k)}')}.",
                f"Now {m(f'{int_raw(y2)} = {tx(k)}x')}. Divide by {m(tx(k))} (multiply by {m(tx(1 / k))}): "
                f"{m(f'x = {int_raw(y2)} \\times {tx(1 / k)} = {x2}')}.",
            ],
            tip=f"Or use a proportion: {m(F(int_raw(y1), x1) + ' = ' + F(int_raw(y2), 'x'))}, so {m(f'{int_raw(y1)}x = {int_raw(x1 * y2)}')} and {m(f'x = {x2}')}.",
            check=sp.solve(sp.Eq(R(y1, x1), R(y2) / x), x)[0],
            verify=lambda v: Fraction(int(y2), int(v)) == Fraction(int(y1), x1),
        )
    # which equation?
    need(not k.is_integer)
    eq = lambda c: m(f"y = {tx(c)}x")
    wr = [
        (eq(1 / k), f"divides {m('x')} by {m('y')} instead of {m('y')} by {m('x')}"),
        (m(f"y = x + {int_raw(y1 - x1)}"), "describes a constant difference, not a constant ratio")
        if y1 > x1 else (m(f"y = x - {int_raw(x1 - y1)}"), "describes a constant difference, not a constant ratio"),
        (m(f"y = {F(int_raw(x1 * y1), 'x')}"), "describes inverse variation"),
        (eq(k + 1), None),
    ]
    return Problem(
        stem=(f"If {phr}, and {m(f'y = {int_raw(y1)}')} when {m(f'x = {x1}')}, which equation "
              f"relates {m('x')} and {m('y')}?"),
        answer=eq(k),
        fmt=lambda s: s,
        wrong=wr,
        steps=[
            f"Direct variation has the form {m('y = kx')}.",
            f"Find {m('k')} by dividing: {m(f'k = \\frac{{y}}{{x}} = {F(int_raw(y1), x1)} = {tx(k)}')}.",
            f"So the equation is {eq(k)}. Check: {m(f'{tx(k)} \\times {x1} = {int_raw(y1)}')}. \\checkmark",
        ],
        check=m(f"y = {tx(sp.solve(sp.Eq(y1, sp.Symbol('k') * x1))[0])}x"),
    )


_THREE = [
    # (stem with {r} and {T}, total kind, names of the three shares, unit fmt)
    ("The angles of a triangle are in the ratio {r}. What is the measure of the {which} angle?",
     "angle", None),
    ("A concrete mix is made of cement, sand, and gravel in the ratio {r} by weight. How many pounds "
     "of {which} are in {T} pounds of the mix?", "concrete", ("cement", "sand", "gravel")),
    ("Three partners split a profit of {T} in the ratio {r}. How much does the partner with the "
     "{which} share receive?", "money", None),
    ("A supply sergeant divides {T} cases of bottled water among Alpha, Bravo, and Charlie platoons "
     "in the ratio {r}. How many cases does {which} platoon receive?", "water", ("Alpha", "Bravo", "Charlie")),
    ("Three employees share a {T} bonus in the ratio {r}, based on hours worked. How much is the "
     "{which} share?", "money", None),
]


@template("AR")
def divide_in_ratio(rng, lvl):
    stem_t, kind, names = rng.choice(_THREE)
    while True:
        rs = [rng.randint(1, 7) for _ in range(3)]
        if len(set(rs)) == 3 and gcd(gcd(rs[0], rs[1]), rs[2]) == 1:
            break
    if kind == "concrete":
        rs.sort()
    s = sum(rs)
    if kind == "angle":
        T = 180
        need(T % s == 0)
    elif kind == "concrete":
        T = rng.choice(range(60, 1201, 30))
    elif kind == "water":
        T = rng.choice(range(48, 481, 12))
    else:
        T = rng.choice(range(600, 12001, 300))
    need(T % s == 0)
    one = T // s
    shares = [r * one for r in rs]
    diff_q = kind in ("money",) and rng.random() < 0.35
    if diff_q:
        hi, lo = max(rs), min(rs)
        ans = Q((hi - lo) * one)
        fmt = money
        stem = (stem_t.split(" How")[0].format(T=money(T), r=m(_rt(rs[0], rs[1]) + ':' + int_raw(rs[2])))
                + " How much more does the partner with the largest share receive than the partner with the smallest share?"
                if "partners" in stem_t else
                stem_t.split(" How")[0].format(T=money(T), r=m(_rt(rs[0], rs[1]) + ':' + int_raw(rs[2])))
                + " How much more is the largest share than the smallest share?")
        return Problem(
            stem=stem,
            answer=ans,
            fmt=fmt,
            wrong=[
                (Q(hi * one), "is the largest share, not the difference"),
                (Q(lo * one), "is the smallest share, not the difference"),
                (Q(one), "is the size of one part"),
                (R(T * (hi - lo), hi + lo), None),
            ],
            steps=[
                f"Add the terms of the ratio: {m(f'{rs[0]} + {rs[1]} + {rs[2]} = {s}')} parts.",
                f"One part is {m(f'{int_raw(T)} \\div {s} = {int_raw(one)}')} dollars.",
                f"The largest share is {hi} parts and the smallest is {lo} parts, a difference of "
                f"{m(f'{hi} - {lo} = {hi - lo}')} parts: {m(f'{hi - lo} \\times {int_raw(one)} = {int_raw(ans)}')}.",
            ],
            check=Fraction(T, s) * (hi - lo),
        )
    if names:
        idx = rng.randrange(3)
        which = names[idx]
    else:
        idx = rng.choice([rs.index(max(rs)), rs.index(min(rs))])
        which = "largest" if rs[idx] == max(rs) else "smallest"
    ans = Q(shares[idx])
    r_txt = m(f"{rs[0]}:{rs[1]}:{rs[2]}")
    Tt = money(T) if kind == "money" else num(T)
    fmt = {"angle": unit(num, r"^\circ", r"^\circ", space=False), "money": money}.get(kind, num)
    if kind == "angle":
        fmt = lambda v: m(int_raw(v) + r"^\circ")
    others = [i for i in range(3) if i != idx]
    oname = (lambda i: names[i] if names else ("largest" if rs[i] == max(rs) else
                                                "smallest" if rs[i] == min(rs) else "middle"))
    wrong = [
        (Q(shares[others[0]]), f"is the {oname(others[0])} share" + (" platoon's share" if kind == "water" else "")),
        (Q(shares[others[1]]), f"is the {oname(others[1])} share" + (" platoon's share" if kind == "water" else "")),
        (R(T, 3), "splits the total evenly three ways"),
        (Q(one), "is the size of one part, not the share"),
        (R(T * rs[idx], sum(rs) - rs[idx]), None),
    ]
    wrong = [(v, w.replace(" share platoon's share", " platoon's share")) if w else (v, w) for v, w in wrong]
    unit_word = {"angle": "degrees", "money": "dollars", "concrete": "pounds", "water": "cases"}[kind]
    return Problem(
        stem=stem_t.format(r=r_txt, T=Tt, which=which),
        answer=ans,
        fmt=fmt,
        wrong=wrong,
        steps=[
            (f"The three angles always add up to {m('180^\\circ')}. " if kind == "angle" else "")
            + f"Add the terms of the ratio: {m(f'{rs[0]} + {rs[1]} + {rs[2]} = {s}')} equal parts.",
            f"One part is {m(f'{int_raw(T)} \\div {s} = {int_raw(one)}')} {unit_word}.",
            f"The {which}{' platoon' if kind == 'water' else ''} share is {rs[idx]} parts: "
            f"{m(f'{rs[idx]} \\times {int_raw(one)} = {int_raw(ans)}')} {unit_word}.",
        ],
        tip=f"Check: {m(' + '.join(int_raw(v) for v in shares) + ' = ' + int_raw(T))}.",
        check=Fraction(T * rs[idx], s),
    )


_DIFFS = [
    # (setting with {r} and {d}, first group, second group, whole noun, question about total)
    ("In a school club, the ratio of boys to girls is {r}. There are {d} more girls than boys.",
     "boys", "girls", "members are in the club"),
    ("At a recruiting event, the ratio of applicants who passed the fitness test to those who did "
     "not was {r}. {D} more applicants passed than did not.", "applicants who did not pass",
     "applicants who passed", "applicants took the test"),
    ("An animal shelter has only dogs and cats, in the ratio {r} (cats to dogs). The shelter has "
     "{d} more dogs than cats.", "cats", "dogs", "animals are in the shelter"),
    ("A theater sold adult and child tickets in the ratio {r}. It sold {d} more child tickets "
     "than adult tickets.", "adult tickets", "child tickets", "tickets did it sell in all"),
    ("A motor pool has Humvees and trucks in the ratio {r}. There are {d} more trucks than Humvees.",
     "Humvees", "trucks", "vehicles are in the motor pool"),
]


@template("AR")
def ratio_difference(rng, lvl):
    setting, small_name, big_name, total_q = rng.choice(_DIFFS)
    p, q = _coprime_pair(rng, 1, 11)
    lo, hi = min(p, q), max(p, q)
    need(hi - lo >= 2)
    one = rng.randint(2, 12)
    d = (hi - lo) * one
    passed = "passed" in setting
    r_txt = m(_rt(hi, lo)) if passed else m(_rt(lo, hi))
    stem = setting.format(r=r_txt, d=num(d), D=num(d))
    ask = rng.choice(["total", "big", "small"])
    total = (lo + hi) * one
    if ask == "total":
        ans = Q(total)
        stem += f" How many {total_q}?"
        last = f"The total is {lo} + {hi} = {lo + hi} parts: {m(f'{lo + hi} \\times {one} = {int_raw(total)}')}."
        wrong = [
            (Q(d * (lo + hi)), f"treats the difference of {num(d)} as one part, but it is {hi - lo} parts"),
            (Q(hi * one), f"is the number of {big_name} only"),
            (Q(lo * one), f"is the number of {small_name} only"),
            (Q(lo + hi + d), None),
        ]
    elif ask == "big":
        ans = Q(hi * one)
        stem += f" How many {big_name} are there?"
        last = f"The {big_name} are {hi} parts: {m(f'{hi} \\times {one} = {int_raw(ans)}')}."
        wrong = [
            (Q(d * hi), f"treats the difference of {num(d)} as one part, but it is {hi - lo} parts"),
            (Q(lo * one), f"is the number of {small_name}"),
            (Q(total), "is the total, not one group"),
            (Q(hi + d), None),
        ]
    else:
        ans = Q(lo * one)
        stem += f" How many {small_name} are there?"
        last = f"The {small_name} are {lo} parts: {m(f'{lo} \\times {one} = {int_raw(ans)}')}."
        wrong = [
            (Q(d * lo), f"treats the difference of {num(d)} as one part, but it is {hi - lo} parts"),
            (Q(hi * one), f"is the number of {big_name}"),
            (Q(total), "is the total, not one group"),
            (Q(one), "is the size of one part"),
        ]
    stem = stem.replace("are there? ", "are there?")
    return Problem(
        stem=stem,
        answer=ans,
        fmt=num,
        wrong=wrong,
        steps=[
            f"In parts, the {big_name} are {hi} parts and the {small_name} are {lo} parts, so the difference is "
            f"{m(f'{hi} - {lo} = {hi - lo}')} parts.",
            f"Those {hi - lo} parts equal {num(d)}, so one part is {m(f'{int_raw(d)} \\div {hi - lo} = {one}')}.",
            last,
        ],
        tip=f"Check: {m(f'{int_raw(hi * one)} - {int_raw(lo * one)} = {int_raw(d)}')}, and "
            f"{m(_rt(hi * one, lo * one))} simplifies to {m(_rt(hi, lo))}.",
        check=Fraction(d, hi - lo) * {"total": hi + lo, "big": hi, "small": lo}[ask],
    )


from ..core import unit  # noqa: E402  (used by map_scale / divide_in_ratio)


PLAN = [
    # (template, level, count)  -- easy -> hard; 25 problems
    (simplify_ratio, 1, 2),
    (part_of_whole, 1, 2),
    (solve_proportion, 1, 2),
    (unit_rate, 1, 2),
    (simplify_ratio, 2, 2),
    (solve_proportion, 2, 1),
    (ratio_total, 2, 2),
    (recipe_scale, 2, 2),
    (map_scale, 2, 2),
    (direct_variation, 2, 1),
    (divide_in_ratio, 3, 2),
    (ratio_difference, 3, 2),
    (map_scale, 3, 1),
    (direct_variation, 3, 1),
    (recipe_scale, 3, 1),
]
