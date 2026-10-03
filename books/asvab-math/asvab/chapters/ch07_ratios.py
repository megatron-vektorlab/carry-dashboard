"""Chapter 7 - Ratios & Proportions."""
from fractions import Fraction
from math import gcd

import sympy as sp

from ..core import (R, Q, Problem, need, num, dec, frac, mixed, money, unit, m, F,
                    tx, dec_raw, int_raw, frac_raw, mixed_raw, person, choose,
                    template, x, y)

NUM = 7
TITLE = r"Ratios \& Proportions"
PART = 1

INTRO = r"""
A \emph{ratio} compares two quantities; a \emph{proportion} says that two
ratios are equal. Together they handle recipes, maps, mixtures, unit rates,
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
one cup makes $8$ cookies, so $40$ cookies need $40 \div 8 = 5$ cups. Smaller
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


def _rt(*terms) -> str:
    """Raw ratio text 3:4 or 2:3:5 (no simplification)."""
    return ":".join(int_raw(t) for t in terms)


def _coprime_pair(rng, lo, hi):
    while True:
        p, q = rng.randint(lo, hi), rng.randint(lo, hi)
        if p != q and gcd(p, q) == 1:
            return p, q


def _fr(v) -> Fraction:
    v = sp.Rational(Q(v))
    return Fraction(int(v.p), int(v.q))


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
    ("In a training class, {A} students passed the first exam and {B} did not.",
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
            verify=lambda v: _fr(v) == Fraction(P, S),
        )

    big, bigs, small, smalls, f, slip, brange, srange = rng.choice(_UNITS)
    a = rng.choice(list(brange))
    b = rng.choice(list(srange))
    need(b % f != 0)
    big_first = rng.random() < 0.6
    A_conv = a * f
    P, S = (A_conv, b) if big_first else (b, A_conv)
    ans = R(P, S)
    need(max(ans.p, ans.q) <= 20 and ans != 1)
    a_txt = f"{num(a)} {big if a == 1 else bigs}"
    b_txt = f"{num(b)} {small if b == 1 else smalls}"
    first, second = (a_txt, b_txt) if big_first else (b_txt, a_txt)
    wrong = [
        (R(a, b) if big_first else R(b, a), f"forgets to change {bigs} to {smalls} before comparing"),
        (1 / ans, "reverses the order of the ratio"),
    ]
    if slip:
        wrong.append((R(a * slip, b) if big_first else R(b, a * slip),
                      f"uses {slip} {smalls} in {'an' if big == 'hour' else 'a'} {big} instead of {f}"))
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
            f"Now compare {smalls} to {smalls}, in the order asked: {m(_rt(P, S))}.",
            _gcf_step(P, S),
        ],
        check=sp.Rational(a * f, b) if big_first else sp.Rational(b, a * f),
        verify=lambda v: _fr(v) == (Fraction(A_conv, b) if big_first else Fraction(b, A_conv)),
    )


@template("MK")
def solve_proportion(rng, lvl):
    # level 1: x/a = c/d ; level 2: a/x = c/d.  The unknown is always a whole number.
    p, q = _coprime_pair(rng, 1, 9)
    need(q >= 2)
    s, t = rng.sample(range(2, 9), 2)
    if lvl == 1:
        a, xv, c, d = q * s, p * s, p * t, q * t
        need(a <= 48 and c <= 60 and d <= 72 and xv > 1)
        if rng.random() < 0.6:
            stem_eq = f"{F('x', a)} = {F(c, d)}"
        else:
            stem_eq = f"{F(c, d)} = {F('x', a)}"
        cross = a * c
        g = gcd(c, d)
        tip = None
        if g > 1 and d // g == 1:
            tip = (f"Simplify first: {m(F(c, d) + ' = ' + str(c // g))}, so {m(F('x', a) + f' = {c // g}')} "
                   f"and {m(f'x = {a} \\times {c // g} = {xv}')}.")
        elif g > 1 and d // g == a:
            tip = (f"Simplify first: {m(F(c, d) + ' = ' + F(c // g, d // g))}, so "
                   f"{m(F('x', a) + ' = ' + F(c // g, a))} and {m(f'x = {c // g}')}.")
        elif g > 1:
            tip = (f"Simplify {m(F(c, d))} to {m(F(c // g, d // g))} first to work with smaller numbers: "
                   f"{m(f'{d // g}x = {a} \\times {c // g} = {a * c // g}')}.")
        return Problem(
            stem=choose(rng, f"Solve for {m('x')}: {m(stem_eq)}",
                        f"If {m(stem_eq)}, what is the value of {m('x')}?"),
            answer=Q(xv),
            fmt=num,
            wrong=[w for w in [
                (Q(a * c), f"multiplies {a} by {c} but forgets to divide by {d}"),
                (Q(c + a - d), f"adds the difference of the denominators ({m(f'{a} - {d}')}) instead of scaling"),
                (R(a * d, c), f"cross-multiplies the wrong pair: {m(f'{a} \\times {d} \\div {c}')}"),
            ] if w[0] > 0],
            steps=[
                f"Cross-multiply: {m(f'{d} \\times x = {a} \\times {c}')}, so {m(f'{d}x = {int_raw(cross)}')}.",
                f"Divide both sides by {d}: {m(f'x = {int_raw(cross)} \\div {d} = {int_raw(xv)}')}.",
            ],
            tip=tip,
            check=sp.solve(sp.Eq(x / a, R(c, d)), x)[0],
            verify=lambda v: Fraction(int(v), a) == Fraction(c, d),
        )

    a, xv, c, d = p * s, q * s, p * t, q * t
    need(a <= 40 and c <= 60 and d <= 72 and xv > 1 and a != c)
    stem_eq = f"{F(a, 'x')} = {F(c, d)}"
    cross = a * d
    return Problem(
        stem=choose(rng, f"Solve for {m('x')}: {m(stem_eq)}",
                    f"If {m(stem_eq)}, what is the value of {m('x')}?"),
        answer=Q(xv),
        fmt=num,
        wrong=[w for w in [
            (R(a * c, d), f"solves as if {m('x')} were on top, giving {m(f'{a} \\times {c} \\div {d}')}"),
            (Q(a * d), f"multiplies {a} by {d} but forgets to divide by {c}"),
            (Q(d + a - c), "adds the difference of the numerators instead of scaling"),
        ] if w[0] > 0],
        steps=[
            f"Cross-multiply: {m(f'{c} \\times x = {a} \\times {d}')}, so {m(f'{c}x = {int_raw(cross)}')}.",
            f"Divide both sides by {c}: {m(f'x = {int_raw(cross)} \\div {c} = {int_raw(xv)}')}.",
            f"Check: {m(F(a, xv))} and {m(F(c, d))} both simplify to {m(frac_raw(R(a, xv)))}. \\checkmark",
        ],
        check=sp.solve(sp.Eq(R(a) / x, R(c, d)), x)[0],
        verify=lambda v: Fraction(a, int(v)) == Fraction(c, d),
    )


_GROUPS = [
    # (setting with {r}, first group, second group, question with {g})
    ("The ratio of boys to girls in a class is {r}.", "boys", "girls",
     "What fraction of the students in the class are {g}?"),
    ("A jar holds only quarters and dimes, in the ratio {r} (quarters to dimes).",
     "quarters", "dimes", "What fraction of the coins in the jar are {g}?"),
    ("At a recruiting station, the ratio of Army enlistees to Navy enlistees this week is {r}, "
     "and no one enlisted in any other branch.", "Army enlistees", "Navy enlistees",
     "What fraction of this week's enlistees are {g}?"),
    ("A bag holds only red and green marbles, in the ratio {r} (red to green).",
     "red", "green", "What fraction of the marbles are {g}?"),
    ("In an Army company, the ratio of officers to enlisted soldiers is {r}.",
     "officers", "enlisted soldiers", "What fraction of the company are {g}?"),
    ("A team's ratio of wins to losses this season is {r}, and it has had no ties.",
     "wins", "losses", "What fraction of its games this season were {g}?"),
    ("In a survey, everyone chose either coffee or tea, and the ratio of coffee drinkers to tea "
     "drinkers was {r}.", "coffee drinkers", "tea drinkers",
     "What fraction of the people surveyed were {g}?"),
    ("A battalion's vehicles are all trucks or trailers, in the ratio {r} (trucks to trailers).",
     "trucks", "trailers", "What fraction of the vehicles are {g}?"),
]


@template("MK")
def part_of_whole(rng, lvl):
    p, q = _coprime_pair(rng, 1, 9)
    need(p + q <= 13)
    setting, g1, g2, ask = rng.choice(_GROUPS)
    if g1 == "officers":
        need(p == 1 and q >= 5)
    ask_first = rng.random() < 0.6
    part, other, gname = (p, q, g1) if ask_first else (q, p, g2)
    ans = R(part, p + q)
    return Problem(
        stem=setting.format(r=m(_rt(p, q))) + " " + ask.format(g=gname),
        answer=ans,
        fmt=frac,
        wrong=[w for w in [
            (R(part, other), f"uses the ratio {m(_rt(part, other))} as if it were the fraction of the total"),
            (R(other, p + q), "is the fraction for the other group"),
            (R(1, p + q), "is the size of just one part, not the whole group's share"),
            (R(part, p * q), "multiplies the terms of the ratio instead of adding them to get the total"),
            (R(other, part), "flips the ratio"),
        ] if w[0] < 1 or w[1].startswith("uses the ratio")],
        steps=[
            f"Think in parts: the whole group is {m(f'{p} + {q} = {p + q}')} equal parts.",
            f"The {gname} are {part} of those {p + q} parts, so the fraction is {m(frac_raw(ans))}.",
        ],
        check=Fraction(part, p + q),
        near=lambda r: [R(k, p + q) for k in range(1, p + q) if k != part]
                       + [R(k, other + 1) for k in range(1, other + 1)],
    )


_TOTALS = [
    # (setting with {T} and {r}, first group, second group, verb, totals range)
    ("A recruiting station signed up {T} recruits last month, all for either the Army or the Navy. "
     "The ratio of Army recruits to Navy recruits was {r}.", "Army recruits", "Navy recruits", "were", range(20, 200)),
    ("A parking lot holds {T} vehicles, all cars or trucks. The ratio of cars to trucks is {r}.",
     "cars", "trucks", "are", range(20, 300)),
    ("A softball team played {T} games and had no ties. The ratio of wins to losses was {r}.",
     "wins", "losses", "were", range(12, 60)),
    ("A battalion sent {T} soldiers to two training courses. The ratio of soldiers in the driving "
     "course to soldiers in the first-aid course was {r}.", "soldiers in the driving course",
     "soldiers in the first-aid course", "were", range(30, 240)),
    ("A fruit stand sold {T} pieces of fruit on Saturday, all apples or oranges. The ratio of "
     "apples to oranges sold was {r}.", "apples", "oranges", "were sold", range(30, 300)),
    ("A school club has {T} members, and every member is a junior or a senior. The ratio of "
     "juniors to seniors is {r}.", "juniors", "seniors", "are in the club", range(15, 80)),
    ("A company surveyed {T} soldiers about PT. Each soldier chose morning PT or evening PT, and "
     "the ratio of morning to evening choices was {r}.", "soldiers", "soldiers", "chose __", range(40, 240)),
    ("A bookstore sold {T} books last week, all paperbacks or hardcovers. The ratio of paperbacks "
     "to hardcovers sold was {r}.", "paperbacks", "hardcovers", "were sold", range(40, 400)),
]


@template("AR")
def ratio_total(rng, lvl):
    p, q = _coprime_pair(rng, 1, 9)
    setting, n1, n2, verb, trange = rng.choice(_TOTALS)
    s = p + q
    T = rng.choice([t for t in trange if t % s == 0] or [0])
    one = T // s
    need(one >= 2)
    ask_first = rng.random() < 0.5
    part, other, name, oname = (p, q, n1, n2) if ask_first else (q, p, n2, n1)
    ans = part * one
    if verb in ("were", "are"):
        question = f" How many {name} {verb} there?"
    elif verb == "chose __":
        question = f" How many soldiers chose {'morning' if ask_first else 'evening'} PT?"
        name = f"soldiers who chose {'morning' if ask_first else 'evening'} PT"
        oname = f"soldiers who chose {'evening' if ask_first else 'morning'} PT"
    else:
        question = f" How many {name} {verb}?"
    return Problem(
        stem=setting.format(T=num(T), r=m(_rt(p, q))) + question,
        answer=Q(ans),
        fmt=num,
        wrong=[
            (Q(other * one), f"is the number of {oname}"),
            (R(T * part, other) if part < other else Q(-1),
             f"treats the ratio as the fraction {m(F(part, other))} of the total"),
            (Q(one), "stops after finding the size of one part"),
            (R(T, part), None),
        ],
        steps=[
            f"Add the terms of the ratio to get the number of equal parts: {m(f'{p} + {q} = {s}')}.",
            f"Find the size of one part: {m(f'{int_raw(T)} \\div {s} = {one}')}.",
            f"The {name} make up {_parts(part)}: {m(f'{part} \\times {one} = {int_raw(ans)}')}.",
        ],
        tip=(f"Check: {m(f'{int_raw(ans)} + {int_raw(other * one)} = {int_raw(T)}')}, and "
             f"{m(_rt(p * one, q * one))} simplifies to {m(_rt(p, q))}."),
        check=Fraction(T * part, s),
        verify=lambda v: Fraction(int(v), T - int(v)) == Fraction(part, other),
    )


_RECIPES = [
    dict(stem="A cookie recipe uses {a} of flour to make {b} cookies. How many cups of flour are "
              "needed to make {c} cookies?",
         unit=("cup", "cups"), per="cookies", a=[1, 2, 3, 4], b=[12, 16, 18, 24, 30, 36],
         c=range(12, 91, 2), fmt=mixed, small=True),
    dict(stem="A mess hall recipe uses {a} of rice to feed {b} soldiers. How many pounds of rice "
              "are needed to feed {c} soldiers?",
         unit=("pound", "pounds"), per="soldiers", a=range(3, 13), b=[20, 25, 30, 40, 50],
         c=range(50, 301, 5), fmt=dec, small=False),
    dict(stem="A pancake recipe calls for {a} to make {b} pancakes. How many eggs are needed to "
              "make {c} pancakes?",
         unit=("egg", "eggs"), per="pancakes", a=[2, 3, 4], b=[8, 10, 12, 15, 16],
         c=range(16, 61), fmt=num, small=True),
    dict(stem="The label on a bag of lawn fertilizer says to use {a} for every {b} square feet of "
              "lawn. How many pounds are needed for {c} square feet?",
         unit=("pound", "pounds"), per="square feet", a=[2, 3, 4, 5, 6], b=[500, 1000],
         c=range(1250, 6001, 250), fmt=dec, small=False),
    dict(stem="A field kitchen brews {a} of coffee for every {b} soldiers. How many gallons "
              "should it brew for {c} soldiers?",
         unit=("gallon", "gallons"), per="soldiers", a=[2, 3, 4, 5], b=[20, 25, 30, 40],
         c=range(60, 241, 5), fmt=dec, small=False),
    dict(stem="A painter used {a} of paint to cover {b} square feet of fence. At the same rate, "
              "how many gallons are needed to cover {c} square feet?",
         unit=("gallon", "gallons"), per="square feet", a=[2, 3, 4], b=[600, 700, 800],
         c=range(900, 2801, 50), fmt=dec, small=False),
    dict(stem="A concrete mix uses {a} of cement for every {b} bags of sand. How many bags of "
              "cement are needed for {c} bags of sand?",
         unit=("bag", "bags"), per="bags of sand", a=[1, 2, 3], b=[3, 4, 5],
         c=range(9, 41), fmt=num, small=True),
]


_FRAC_RECIPES = [
    # (stem with {a} {b} {c}, unit sing/pl, per-noun, amounts a)
    ("A recipe that serves {b} people uses {a} of sugar. How many cups of sugar are needed to "
     "serve {c} people?", ("cup", "cups"), ("person", "people"), [R(1, 2), R(2, 3), R(3, 4), R(3, 2), R(5, 4)]),
    ("A pancake recipe uses {a} of milk to make {b} pancakes. How many cups of milk are needed "
     "to make {c} pancakes?", ("cup", "cups"), ("pancake", "pancakes"), [R(2, 3), R(3, 4), R(3, 2), R(5, 4)]),
    ("A chili recipe that makes {b} servings uses {a} of ground beef. How many pounds of ground "
     "beef are needed to make {c} servings?", ("pound", "pounds"), ("serving", "servings"),
     [R(3, 2), R(5, 2), R(9, 4), R(2)]),
    ("A field kitchen's oatmeal recipe uses {a} of oats for every {b} soldiers. How many cups "
     "of oats are needed for {c} soldiers?", ("cup", "cups"), ("soldier", "soldiers"), [R(3, 4), R(3, 2), R(5, 2), R(2)]),
]


def _parts(k) -> str:
    return f"{k} part" if k == 1 else f"{k} parts"


@template("AR")
def recipe_scale(rng, lvl):
    if lvl == 3:
        stem_t, (one, many), (per1, per), avals = rng.choice(_FRAC_RECIPES)
        a = rng.choice(avals)
        b = rng.choice([4, 6, 8, 12])
        c = rng.choice([v for v in range(2, 41) if v != b])
        need(c > b or rng.random() < 0.25)
        scale = R(c, b)
        ans = a * scale
        need(not scale.is_integer and ans.q in (1, 2, 3, 4) and ans <= 8 and ans != a)
        need(not ans.is_integer or rng.random() < 0.3)
        amt = lambda v: f"{m(mixed_raw(v))} {one if v == 1 else many}"
        raw_p, raw_q = a.p * scale.p, a.q * scale.q
        chain = f"{mixed_raw(a)} \\times {frac_raw(scale)}"
        if a.q != 1 and a > 1:
            chain += f" = {frac_raw(a)} \\times {frac_raw(scale)}"
        raw = F(int_raw(raw_p), int_raw(raw_q)) if raw_q != 1 else int_raw(raw_p)
        chain += f" = {raw}"
        if mixed_raw(ans) != raw:
            chain += f" = {mixed_raw(ans)}"
        wrong = [
            (a * R(b, c), f"multiplies by {m(F(b, c))} instead of {m(F(c, b))}"),
            (Q(a * c), f"multiplies by {num(c)} but forgets to divide by {num(b)}"),
            (ans - a if c > b else a - ans, "finds only the change in the amount" if c > b else
             "finds how much less is needed, not the new amount"),
        ]
        if c > b:
            wrong.append((a + (c - b), f"adds {c - b} (the number of extra {per}) instead of scaling"))
        wrong.append((ans + R(1, 2), None))
        wrong.append((ans - R(1, 4), None))
        return Problem(
            stem=stem_t.format(a=amt(a), b=num(b), c=num(c)),
            answer=ans,
            fmt=mixed,
            wrong=wrong,
            steps=[
                f"Find the scale factor: {num(c)} {per} is "
                f"{m(F(c, b) + ('' if gcd(b, c) == 1 else ' = ' + frac_raw(scale)))} "
                + (f"times as many as {num(b)} {per}." if c > b else f"of {num(b)} {per}."),
                f"Multiply the amount by that factor: {m(chain)} {one if ans == 1 else many}.",
            ],
            tip=(f"Unit rate: each {per1} needs {m(f'{frac_raw(a)} \\div {b} = {frac_raw(a / b)}')} "
                 f"{one}, and {m(f'{c} \\times {frac_raw(a / b)} = {mixed_raw(ans)}')} {many}."),
            check=_fr(a) / b * c,
            verify=lambda v: _fr(v) / c == _fr(a) / b,
        )

    ctx = rng.choice(_RECIPES)
    one, many = ctx["unit"]
    a = rng.choice(list(ctx["a"]))
    b = rng.choice(ctx["b"])
    c = rng.choice(list(ctx["c"]))
    need(c > b)
    ans = R(a * c, b)
    fmt = ctx["fmt"]
    need(ans.q in (1, 2))
    if fmt is num:
        need(ans.is_integer)
    show = (lambda v: mixed_raw(v)) if fmt is mixed else (lambda v: dec_raw(v))
    cross = a * c
    if ans.is_integer:
        last = f"x = {int_raw(cross)} \\div {int_raw(b)} = {int_raw(ans)}"
    elif fmt is mixed:
        last = f"x = {F(int_raw(cross), int_raw(b))} = {mixed_raw(ans)}"
    else:
        last = f"x = {int_raw(cross)} \\div {int_raw(b)} = {dec_raw(ans)}"
    wrong = [
        (ans - a, f"finds only the extra amount needed and forgets the original {m(show(a))} {many if a != 1 else one}"),
        (R(a * b, c), "sets up the proportion upside down"),
    ]
    if ctx["small"]:
        wrong.append((Q(a + c - b), f"adds the {c - b} extra {ctx['per']} instead of scaling"))
    wrong.append((Q(a * c), f"multiplies by {num(c)} but forgets to divide by {num(b)}"))
    wrong.append((ans + a, None))
    unit_rate = R(b, a)
    tip = None
    if unit_rate.is_integer and unit_rate > 1 and a > 1:
        tip = (f"Unit rate: 1 {one} is enough for {m(int_raw(unit_rate))} {ctx['per']}, so "
               f"{m(f'{int_raw(c)} \\div {int_raw(unit_rate)} = {show(ans)}')} {many}.")
    return Problem(
        stem=ctx["stem"].format(a=f"{m(show(a))} {one if a == 1 else many}", b=num(b), c=num(c)),
        answer=ans,
        fmt=fmt,
        wrong=wrong,
        steps=[
            f"Set up a proportion with the same order on both sides ({many} over {ctx['per']}): "
            f"{m(F(int_raw(a), int_raw(b)) + ' = ' + F('x', int_raw(c)))}.",
            f"Cross-multiply: {m(f'{int_raw(b)}x = {int_raw(a)} \\times {int_raw(c)} = {int_raw(cross)}')}.",
            f"Divide by {num(b)}: {m(last)} {many}.",
        ],
        tip=tip,
        check=Fraction(a, b) * c,
        verify=lambda v: _fr(v) / c == Fraction(a, b),
    )


_MAPS = [
    # (stem with {s} and {d}, real unit (sing, pl), scales, max real value)
    ("On a road map, 1 inch represents {s} miles. Two towns are {d} inches apart on the map. "
     "What is the actual distance between the towns?", ("mile", "miles"), [10, 20, 25, 30, 40, 50, 60], 600),
    ("On a map of an Army training area, 1 inch represents {s} miles. Two checkpoints are {d} "
     "inches apart on the map. How far apart are the checkpoints on the ground?",
     ("mile", "miles"), [2, 3, 4], 40),
    ("A model of a Coast Guard patrol boat is built to a scale of 1 inch = {s} feet. The model is "
     "{d} inches long. How long is the actual boat?", ("foot", "feet"), [6, 8, 10, 12], 120),
    ("A floor plan is drawn to a scale of 1 inch = {s} feet. A wall measures {d} inches on the "
     "plan. How long is the actual wall?", ("foot", "feet"), [2, 4, 6, 8], 60),
]


@template("AR")
def map_scale(rng, lvl):
    if lvl == 2:
        if rng.random() < 0.3:
            # blueprint with a fractional scale such as 1/4 inch = 1 foot
            k = rng.choice([2, 4])
            whole = rng.randint(2, 9)
            part = rng.choice([R(1, 4), R(1, 2), R(3, 4)] if k == 4 else [R(1, 2)])
            d = whole + part
            ans = d * k
            need(ans.is_integer)
            thing = rng.choice(["wall", "room", "deck", "garage", "hallway"])
            return Problem(
                stem=(f"A blueprint uses the scale {m(F(1, k))} inch = 1 foot. A {thing} is "
                      f"{m(mixed_raw(d))} inches long on the blueprint. How long is the actual "
                      f"{thing}, in feet?"),
                answer=ans,
                fmt=dec,
                wrong=[
                    (d / k, f"multiplies by {m(F(1, k))} instead of dividing by it"),
                    (Q(whole * k), f"ignores the {m(frac_raw(part))} inch"),
                    (d + k, None),
                    (ans / 2 if k == 4 else ans * 2, None),
                    (ans * 10, "misplaces the decimal point in the product"),
                ],
                steps=[
                    f"Each {m(F(1, k))} inch stands for 1 foot, so each whole inch stands for {k} feet.",
                    f"Multiply: {m(f'{mixed_raw(d)} \\times {k} = {int_raw(ans)}')} feet "
                    f"({m(f'{whole} \\times {k} = {whole * k}')} and {m(f'{frac_raw(part)} \\times {k} = {int_raw(part * k)}')}).",
                ],
                check=_fr(d) / Fraction(1, k),
                verify=lambda v: v / k == d,
            )
        stem_t, (one, many), scales, top = rng.choice(_MAPS)
        where = "plan" if "floor plan" in stem_t else "model" if "model" in stem_t else "map"
        s = rng.choice(scales)
        whole = rng.randint(2, 9)
        part = rng.choice([Q(0), R(1, 4), R(1, 2), R(3, 4)])
        d = Q(whole) + part
        ans = d * s
        need(ans.is_integer or ans.q == 2)
        need(ans <= top)
        need(part != 0 or rng.random() < 0.25)
        wrong = [
            (d / s, "divides by the scale instead of multiplying"),
            (Q(d + s), "adds the scale instead of multiplying"),
        ]
        if part:
            wrong.append((Q(whole * s), f"ignores the {m(frac_raw(part))} inch"))
            wrong.append((ans * 10, "misplaces the decimal point in the product"))
        wrong.append((ans * 2, None))
        if part:
            work = (f"Split it up: {m(f'{whole} \\times {s} = {whole * s}')} and "
                    f"{m(f'{frac_raw(part)} \\times {s} = {dec_raw(part * s)}')}, so the total is "
                    f"{m(f'{whole * s} + {dec_raw(part * s)} = {dec_raw(ans)}')} {many}.")
        else:
            work = f"{m(f'{whole} \\times {s} = {dec_raw(ans)}')} {many}."
        return Problem(
            stem=stem_t.format(s=num(s), d=m(mixed_raw(d))),
            answer=ans,
            fmt=unit(dec, one, many),
            wrong=wrong,
            steps=[
                f"Each inch on the {where} stands for {num(s)} {many}, so multiply the measurement by {num(s)}.",
                work,
            ],
            check=_fr(d) * s,
        )

    # level 3: a scale that is not "1 inch = ..." (work backward), or area on a floor plan
    if rng.random() < 0.5:
        u = rng.choice([2, 3])                     # u inches = v miles
        v = rng.choice([5, 15, 25, 35, 45, 75, 125])
        need(gcd(u, v) == 1)
        k = rng.randint(3, 12)
        actual = v * k
        ans = Q(u * k)
        need(ans <= 16 and 40 <= actual <= 900)
        place = rng.choice(["two cities", "two Army posts", "two airports", "two state capitals",
                            "two Air Force bases"])
        return Problem(
            stem=(f"On a map, {u} inches represent {num(v)} miles. The actual distance between "
                  f"{place} is {num(actual)} miles. How far apart are they on the map?"),
            answer=ans,
            fmt=unit(num, "inch", "inches"),
            wrong=[
                (Q(k), f"divides {num(actual)} by {num(v)} but forgets that the scale uses {u} inches, not 1"),
                (R(actual, u), f"divides the distance by {u} instead of using the whole scale"),
                (Q(k + u), None),
                (Q(u * k + u), None),
            ],
            steps=[
                f"Set up a proportion, inches over miles: {m(F(u, int_raw(v)) + ' = ' + F('x', int_raw(actual)))}.",
                f"Cross-multiply: {m(f'{int_raw(v)}x = {u} \\times {int_raw(actual)} = {int_raw(u * actual)}')}.",
                f"Divide: {m(f'x = {int_raw(u * actual)} \\div {int_raw(v)} = {int_raw(ans)}')} inches.",
            ],
            tip=(f"Or count how many {num(v)}-mile chunks fit: {m(f'{int_raw(actual)} \\div {v} = {k}')}; "
                 f"each chunk is {u} inches on the map, so {m(f'{k} \\times {u} = {int_raw(ans)}')}."),
            check=Fraction(u, v) * actual,
        )
    s = rng.choice([2, 3, 4, 5, 6, 8])             # 1 inch = s feet
    L, W = sorted(rng.sample(range(2, 8), 2), reverse=True)
    need(L * s <= 40 and W * s <= 30)
    ans = Q(L * s * W * s)
    room = rng.choice(["A bedroom", "A garage", "An office", "A storage room", "A classroom",
                       "A barracks dayroom"])
    return Problem(
        stem=(f"On a floor plan, 1 inch represents {num(s)} feet. {room} measures {num(L)} inches "
              f"by {num(W)} inches on the plan. What is the actual area of the room, in square feet?"),
        answer=ans,
        fmt=num,
        wrong=[
            (Q(L * W * s), f"multiplies the plan's area by {s} instead of converting each side"),
            (Q(2 * (L * s + W * s)), "finds the perimeter instead of the area"),
            (Q(L * W), "gives the area on the plan, in square inches"),
            (Q(L * s + W * s), None),
            (ans * s, f"converts the sides and then multiplies the area by {s} again"),
            (ans + L * s, None),
        ],
        steps=[
            f"Convert each side to feet: {m(f'{L} \\times {s} = {L * s}')} feet and "
            f"{m(f'{W} \\times {s} = {W * s}')} feet.",
            f"Area = length {m(r'\times')} width: {m(f'{L * s} \\times {W * s} = {int_raw(ans)}')} square feet.",
        ],
        tip=(f"Areas scale by the \\emph{{square}} of the scale: the plan's {m(f'{L * W}')} square "
             f"inches times {m(f'{s}^2 = {s * s}')} gives {m(int_raw(ans))}."),
        check=Fraction(L * W) * s ** 2,
    )


@template("AR")
def unit_rate(rng, lvl):
    kind = rng.choice(["mpg", "meat", "wage", "typing", "convoy", "pump"])
    p = person(rng)
    money_like = kind in ("meat", "wage")
    if kind == "mpg":
        rate, n = rng.randint(14, 36), rng.randint(8, 22)
        vehicle = rng.choice(["A pickup truck", "A delivery van", "A sedan", "An Army truck", "A minivan"])
        stem = (f"{vehicle} traveled {num(rate * n)} miles on {num(n)} gallons of gas. How many miles "
                f"per gallon did it get?")
        per = "miles per gallon"
    elif kind == "meat":
        rate, n = R(rng.choice(range(13, 27)), 4), rng.choice([2, 3, 4, 5, 6, 8])
        item = rng.choice(["ground beef", "chicken breast", "deli turkey", "salmon"])
        stem = f"At a grocery store, {num(n)} pounds of {item} cost {money(rate * n)}. What is the cost per pound?"
        per = "per pound"
    elif kind == "wage":
        rate, n = R(rng.choice(range(24, 51)), 2), rng.choice([4, 6, 8, 10, 12, 20, 25, 30])
        stem = f"{p.name} earned {money(rate * n)} for {num(n)} hours of work. How much did {p.he} earn per hour?"
        per = "per hour"
    elif kind == "typing":
        rate, n = rng.randint(30, 80), rng.randint(3, 12)
        stem = (f"{p.name} typed a {num(rate * n)}-word report in {num(n)} minutes. How many words "
                f"per minute did {p.he} type?")
        per = "words per minute"
    elif kind == "convoy":
        rate, n = rng.randint(30, 55), rng.randint(2, 8)
        stem = (f"A supply convoy traveled {num(rate * n)} miles in {num(n)} hours. What was its "
                f"average speed, in miles per hour?")
        per = "miles per hour"
    else:
        rate, n = rng.choice(range(15, 95, 5)), rng.randint(4, 15)
        stem = (f"A pump removes {num(rate * n)} gallons of water from a flooded basement in {num(n)} "
                f"minutes. How many gallons per minute does it pump?")
        per = "gallons per minute"
    rate = Q(rate)
    total = rate * n
    step = R(1, 2) if money_like else 1
    wrong = [(rate * 10, "misplaces the decimal point when dividing"),
             (rate / 10, "misplaces the decimal point when dividing"),
             (rate + step, None), (rate - step, None), (rate + 2 * step, None),
             (rate - 2 * step, None)]
    result = f"{money(rate)} {per}" if money_like else f"{num(rate)} {per}"
    return Problem(
        stem=stem,
        answer=rate,
        fmt=money if money_like else dec,
        wrong=wrong,
        steps=[
            f"\\emph{{Per}} means ``for each one,'' so divide the total by the number of units: "
            f"{m(f'{dec_raw(total)} \\div {n} = {dec_raw(rate)}')}.",
            f"The unit rate is {result}.",
        ],
        tip=f"Check by multiplying back: {m(f'{dec_raw(rate)} \\times {n} = {dec_raw(total)}')}.",
        check=_fr(total) / n,
        verify=lambda v: v * n == total,
    )


@template("MK")
def direct_variation(rng, lvl):
    k = rng.choice([R(v) for v in range(2, 10)] + [R(v, 2) for v in (3, 5, 7, 9)]
                   + [R(v, 3) for v in (2, 4, 5)])
    x1 = rng.randint(2, 12)
    y1 = k * x1
    need(y1.is_integer)
    phr = choose(rng, f"{m('y')} varies directly with {m('x')}",
                 f"{m('y')} varies directly as {m('x')}",
                 f"{m('y')} is directly proportional to {m('x')}")
    k_step = f"Find {m('k')} by dividing: {m(f'k = \\frac{{y}}{{x}} = {F(int_raw(y1), x1)} = {tx(k)}')}."
    if lvl == 2:
        x2 = rng.randint(2, 20)
        need(x2 != x1)
        y2 = k * x2
        need(y2.is_integer)
        return Problem(
            stem=(f"If {phr}, and {m(f'y = {int_raw(y1)}')} when {m(f'x = {x1}')}, what is the value "
                  f"of {m('y')} when {m(f'x = {x2}')}?"),
            answer=y2,
            fmt=dec,
            wrong=[
                (y1 + (x2 - x1), f"adds the change in {m('x')} instead of multiplying by the constant"),
                (R(y1 * x1, x2), "uses inverse variation (constant product) instead of direct variation"),
                (k, f"stops after finding the constant {m('k')}"),
                (y1 * x2, f"forgets to divide by {x1}"),
            ],
            steps=[
                f"Direct variation means {m('y = kx')}, where {m('k')} is a constant.",
                k_step,
                f"Use it: {m(f'y = {tx(k)} \\times {x2} = {int_raw(y2)}')}.",
            ],
            check=sp.solve(sp.Eq(R(y1, x1), y / x2), y)[0],
            verify=lambda v: v * x1 == y1 * x2,
        )

    need(not k.is_integer)
    if rng.random() < 0.6:
        x2 = rng.randint(2, 30)
        y2 = k * x2
        need(y2.is_integer and x2 != x1 and y2 != y1)
        return Problem(
            stem=(f"If {phr}, and {m(f'y = {int_raw(y1)}')} when {m(f'x = {x1}')}, what is the value "
                  f"of {m('x')} when {m(f'y = {int_raw(y2)}')}?"),
            answer=Q(x2),
            fmt=dec,
            wrong=[
                (y2 * k, f"multiplies by {m('k')} instead of dividing by it"),
                (R(x1 * y1, y2), "uses inverse variation instead of direct variation"),
                (x1 + (y2 - y1), f"adds the change in {m('y')} instead of scaling"),
            ],
            steps=[
                f"Direct variation means {m('y = kx')}. " + k_step,
                f"Now solve {m(f'{int_raw(y2)} = {tx(k)}x')}: divide by {m(tx(k))}, which is the same as "
                f"multiplying by {m(tx(1 / k))}: {m(f'x = {int_raw(y2)} \\times {tx(1 / k)} = {x2}')}.",
            ],
            tip=(f"Or use a proportion: {m(F(int_raw(y1), x1) + ' = ' + F(int_raw(y2), 'x'))}, so "
                 f"{m(f'{int_raw(y1)}x = {int_raw(x1 * y2)}')} and {m(f'x = {x2}')}."),
            check=sp.solve(sp.Eq(R(y1, x1), R(y2) / x), x)[0],
            verify=lambda v: Fraction(int(y2), int(v)) == Fraction(int(y1), x1),
        )

    def eq(c):
        return m(f"y = {tx(c)}x")
    ksym = sp.Symbol("k")
    return Problem(
        stem=(f"If {phr}, and {m(f'y = {int_raw(y1)}')} when {m(f'x = {x1}')}, which equation "
              f"relates {m('x')} and {m('y')}?"),
        answer=eq(k),
        fmt=lambda s: s,
        wrong=[
            (eq(1 / k), f"divides {m('x')} by {m('y')} instead of {m('y')} by {m('x')}"),
            (m(f"y = x {'+' if y1 > x1 else '-'} {int_raw(abs(y1 - x1))}"),
             "describes a constant difference, not a constant ratio"),
            (m(f"y = {F(int_raw(x1 * y1), 'x')}"), "describes inverse variation"),
            (eq(k + 1), None),
        ],
        steps=[
            f"Direct variation has the form {m('y = kx')}.",
            k_step,
            f"So the equation is {eq(k)}. Check: {m(f'{tx(k)} \\times {x1} = {int_raw(y1)}')}. \\checkmark",
        ],
        check=m(f"y = {tx(sp.solve(sp.Eq(y1, ksym * x1), ksym)[0])}x"),
    )


_THREE = [
    dict(kind="angle", stem="The angles of a triangle are in the ratio {r}. What is the measure "
                            "of the {which} angle?", names=None, unit="degrees"),
    dict(kind="concrete", stem="A concrete mix is made of cement, sand, and gravel in the ratio "
                               "{r} by weight. How many pounds of {which} are in {T} pounds of the mix?",
         names=("cement", "sand", "gravel"), unit="pounds"),
    dict(kind="money", stem="Three partners split a profit of {T} in the ratio {r}. How much does "
                            "the partner with the {which} share receive?", names=None, unit="dollars",
         diff="Three partners split a profit of {T} in the ratio {r}. How much more does the partner "
              "with the largest share receive than the partner with the smallest share?"),
    dict(kind="water", stem="A supply sergeant divides {T} cases of bottled water among Alpha, Bravo, "
                            "and Charlie platoons in the ratio {r}. How many cases does {which} "
                            "platoon receive?", names=("Alpha", "Bravo", "Charlie"), unit="cases"),
    dict(kind="money", stem="Three employees share a {T} bonus in the ratio {r}, based on hours "
                            "worked. How much is the {which} share?", names=None, unit="dollars",
         diff="Three employees share a {T} bonus in the ratio {r}, based on hours worked. How much "
              "larger is the largest share than the smallest share?"),
]


@template("AR")
def divide_in_ratio(rng, lvl):
    ctx = rng.choice(_THREE)
    kind = ctx["kind"]
    while True:
        rs = [rng.randint(1, 7) for _ in range(3)]
        if len(set(rs)) == 3 and gcd(gcd(rs[0], rs[1]), rs[2]) == 1:
            break
    if kind == "concrete":
        rs.sort()
    s = sum(rs)
    T = {"angle": 180, "concrete": rng.choice(range(60, 1201, 30)),
         "water": rng.choice(range(48, 481, 12))}.get(kind) or rng.choice(range(600, 12001, 300))
    need(T % s == 0)
    one = T // s
    shares = [r * one for r in rs]
    Tt = money(T) if kind == "money" else num(T)
    r_txt = m(_rt(*rs))
    parts_step = ((f"The three angles of a triangle add up to {m('180^\\circ')}. " if kind == "angle" else "")
                  + f"Add the terms of the ratio: {m(f'{rs[0]} + {rs[1]} + {rs[2]} = {s}')} equal parts.")
    one_step = f"One part is {m(f'{int_raw(T)} \\div {s} = {int_raw(one)}')} {ctx['unit']}."
    fmt = {"money": money, "angle": (lambda v: m(int_raw(v) + r"^\circ"))}.get(kind, num)

    if "diff" in ctx and rng.random() < 0.4:
        hi, lo = max(rs), min(rs)
        ans = Q((hi - lo) * one)
        return Problem(
            stem=ctx["diff"].format(T=Tt, r=r_txt),
            answer=ans,
            fmt=money,
            wrong=[
                (Q(hi * one), "is the largest share, not the difference"),
                (Q(lo * one), "is the smallest share, not the difference"),
                (Q(one), "is the size of one part"),
                (Q((hi - lo) * one * 2), None),
            ],
            steps=[
                parts_step,
                one_step,
                f"The largest share is {_parts(hi)} and the smallest is {_parts(lo)}, a difference of "
                f"{m(f'{hi} - {lo} = {hi - lo}')} parts: {m(f'{hi - lo} \\times {int_raw(one)} = {int_raw(ans)}')} dollars.",
            ],
            check=Fraction(T, s) * (hi - lo),
        )

    if ctx["names"]:
        idx = rng.randrange(3)
        which = ctx["names"][idx]

        def label(i):
            nm = ctx["names"][i]
            return {"concrete": f"is the amount of {nm}", "water": f"is {nm} platoon's share"}[kind]
    else:
        idx = rng.choice([rs.index(max(rs)), rs.index(min(rs))])
        which = "largest" if rs[idx] == max(rs) else "smallest"

        def label(i):
            size = "largest" if rs[i] == max(rs) else "smallest" if rs[i] == min(rs) else "middle"
            return f"is the {size} angle" if kind == "angle" else f"is the {size} share"
    ans = Q(shares[idx])
    others = [i for i in range(3) if i != idx]
    calc = m(f"{rs[idx]} \\times {int_raw(one)} = {int_raw(ans)}" + ("^\\circ" if kind == "angle" else ""))
    who = {"angle": f"The {which} angle", "concrete": f"The {which}",
           "water": f"{which} platoon's share"}.get(kind, f"The {which} share")
    last_step = (f"{who} is {_parts(rs[idx])}: {calc}" + ("." if kind == "angle" else f" {ctx['unit']}."))
    return Problem(
        stem=ctx["stem"].format(r=r_txt, T=Tt, which=which),
        answer=ans,
        fmt=fmt,
        wrong=[
            (Q(shares[others[0]]), label(others[0])),
            (Q(shares[others[1]]), label(others[1])),
            (R(T, 3), "splits the total evenly three ways"),
            (Q(one), "is the size of one part"),
        ],
        steps=[
            parts_step,
            one_step,
            last_step,
        ],
        tip=f"Check: {m(' + '.join(int_raw(v) for v in shares) + ' = ' + int_raw(T))}.",
        check=Fraction(T * rs[idx], s),
    )


_DIFFS = [
    dict(setting="In a school club, the ratio of boys to girls is {r}. There are {d} more girls than boys.",
         order="small-big", small="boys", big="girls",
         q_total="How many members are in the club?", q_small="How many boys are in the club?",
         q_big="How many girls are in the club?"),
    dict(setting="At a recruiting event, the ratio of applicants who passed the fitness test to those "
                 "who did not pass was {r}. The number who passed was {d} more than the number who did not.",
         order="big-small", small="applicants who did not pass", big="applicants who passed",
         q_total="How many applicants took the test?", q_small="How many applicants did not pass?",
         q_big="How many applicants passed?"),
    dict(setting="An animal shelter has only dogs and cats, in the ratio {r} (cats to dogs). The shelter "
                 "has {d} more dogs than cats.",
         order="small-big", small="cats", big="dogs",
         q_total="How many animals are in the shelter?", q_small="How many cats are in the shelter?",
         q_big="How many dogs are in the shelter?"),
    dict(setting="A theater sold adult and child tickets in the ratio {r}. It sold {d} more child "
                 "tickets than adult tickets.",
         order="small-big", small="adult tickets", big="child tickets",
         q_total="How many tickets did it sell in all?", q_small="How many adult tickets did it sell?",
         q_big="How many child tickets did it sell?"),
    dict(setting="A motor pool has only Humvees and trucks, in the ratio {r} (Humvees to trucks). "
                 "There are {d} more trucks than Humvees.",
         order="small-big", small="Humvees", big="trucks",
         q_total="How many vehicles are in the motor pool?", q_small="How many Humvees are there?",
         q_big="How many trucks are there?"),
]


@template("AR")
def ratio_difference(rng, lvl):
    ctx = rng.choice(_DIFFS)
    p, q = _coprime_pair(rng, 1, 11)
    lo, hi = min(p, q), max(p, q)
    need(hi - lo >= 2)
    one = rng.randint(2, 12)
    d = (hi - lo) * one
    r_txt = m(_rt(lo, hi) if ctx["order"] == "small-big" else _rt(hi, lo))
    stem = ctx["setting"].format(r=r_txt, d=num(d))
    ask = rng.choice(["total", "big", "small"])
    total = (lo + hi) * one
    one_note = f"treats the difference of {num(d)} as one part, but it is {hi - lo} parts"
    if ask == "total":
        ans = Q(total)
        stem += " " + ctx["q_total"]
        last = (f"The total is {m(f'{lo} + {hi} = {lo + hi}')} parts: "
                f"{m(f'{lo + hi} \\times {one} = {int_raw(total)}')}.")
        wrong = [
            (Q(d * (lo + hi)), one_note),
            (Q(hi * one), f"is the number of {ctx['big']} only"),
            (Q(lo * one), f"is the number of {ctx['small']} only"),
            (Q(lo + hi + d), None),
        ]
    elif ask == "big":
        ans = Q(hi * one)
        stem += " " + ctx["q_big"]
        last = f"The {ctx['big']} are {_parts(hi)}: {m(f'{hi} \\times {one} = {int_raw(ans)}')}."
        wrong = [
            (Q(d * hi), one_note),
            (Q(lo * one), f"is the number of {ctx['small']}"),
            (Q(total), "is the total, not one group"),
            (Q(hi + d), None),
        ]
    else:
        ans = Q(lo * one)
        stem += " " + ctx["q_small"]
        last = f"The {ctx['small']} are {_parts(lo)}: {m(f'{lo} \\times {one} = {int_raw(ans)}')}."
        wrong = [
            (Q(d * lo), one_note),
            (Q(hi * one), f"is the number of {ctx['big']}"),
            (Q(total), "is the total, not one group"),
            (Q(one), "is the size of one part"),
        ]
    return Problem(
        stem=stem,
        answer=ans,
        fmt=num,
        wrong=wrong,
        steps=[
            f"In parts, the {ctx['big']} are {_parts(hi)} and the {ctx['small']} are {_parts(lo)}, so the "
            f"difference is {m(f'{hi} - {lo} = {hi - lo}')} parts.",
            f"Those {hi - lo} parts equal {num(d)}, so one part is {m(f'{int_raw(d)} \\div {hi - lo} = {one}')}.",
            last,
        ],
        tip=(f"Check: {m(f'{int_raw(hi * one)} - {int_raw(lo * one)} = {int_raw(d)}')}, and "
             f"{m(_rt(lo * one, hi * one))} simplifies to {m(_rt(lo, hi))}."),
        check=Fraction(d, hi - lo) * {"total": hi + lo, "big": hi, "small": lo}[ask],
    )


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
