"""Chapter 22 - Money: Shopping, Discounts, Tax & Wages (word problems)."""
import functools
from fractions import Fraction

from ..core import (R, Q, F, Problem, Person, need, num, money, money_cents, pct, m,
                    text, unit, dec_raw, int_raw, frac_raw, person, choose, template)

NUM = 22
TITLE = r"Money: Shopping, Discounts, Tax \& Wages"
PART = 4

INTRO = r"""
Money problems are the most common word problems on the Arithmetic Reasoning
test. They use only a handful of ideas (add up a bill, take a percent off,
add a percent on, figure out pay), but they chain two or three of them
together. Label every number you write with what it means, and always
re-read what the question actually asks for.

\begin{concept}{Shopping}
\begin{itemize}
\item \textbf{Total cost} $=$ quantity $\times$ price for each item, added up.
  \textbf{Change} $=$ amount paid $-$ total cost.
\item \textbf{Sale price:} subtract the discount, or multiply by the percent
  you still pay. $25\%$ off means you pay $75\%$: $0.75 \times \$80 = \$60$.
\item \textbf{Sales tax:} add the tax on. A $6\%$ tax means you pay $106\%$:
  $1.06 \times \$50 = \$53$.
\item \textbf{Discount and tax together:} take the discount first, then
  figure the tax on the \emph{sale} price.
\item \textbf{Unit price} $=$ price $\div$ number of units. The
  \emph{better buy} is the one with the lower unit price.
\end{itemize}
\end{concept}

\begin{concept}{Wages and paychecks}
Hourly pay $=$ hours $\times$ rate. \textbf{Overtime} at
``time-and-a-half'' pays $1.5\times$ the regular rate, but \emph{only} for
the hours over 40 in a week. A salary is split evenly over the paychecks in
a year:
\begin{center}\small
\begin{tabular}{@{}lc@{}}
\toprule
Paid \dots & Paychecks per year\\
\midrule
weekly & 52\\
every two weeks (biweekly) & 26\\
twice a month (semimonthly) & 24\\
monthly & 12\\
\bottomrule
\end{tabular}
\end{center}
A full-time year is $40 \times 52 = 2{,}080$ hours.
\end{concept}

\begin{concept}{Rounding to fit the situation}
``How many can you buy?'' rounds \emph{down}: you cannot buy part of an
item. ``How many weeks until you can afford it?'' rounds \emph{up}: after a
partial week you are still short.
\end{concept}

\begin{example}{Worked example}
Kevin earns \$18 per hour and gets time-and-a-half for hours over 40. Last
week he worked 46 hours. How much did he earn?

\textbf{Solution.} Regular pay: $40 \times \$18 = \$720$. Overtime rate:
$1.5 \times \$18 = \$27$ per hour, and $46 - 40 = 6$ overtime hours earn
$6 \times \$27 = \$162$. Total: $\$720 + \$162 = \$882$.
\end{example}

\begin{tip}
Build percents from $10\%$ (move the decimal point one place left). For
\$64: $10\% = \$6.40$, so $5\% = \$3.20$, $15\% = \$9.60$, and
$20\% = \$12.80$. To multiply by $1.5$, add half: $1.5 \times \$18 = \$18 + \$9 = \$27$.
\end{tip}

\begin{trap}
\begin{itemize}
\item Stopping a step early: giving the discount instead of the sale price,
  or the tax instead of the total.
\item Paying time-and-a-half for \emph{all} the hours instead of only the
  hours over 40.
\item Reading ``every two weeks'' as twice a month: that is 26 paychecks a
  year, not 24.
\item Figuring the tax on the original price when the item is on sale.
\end{itemize}
\end{trap}
"""

# --------------------------------------------------------------------------
# private helpers
# --------------------------------------------------------------------------

_LAST = ["Ruiz", "Chen", "Walker", "Okafor", "Patel", "Novak", "Brooks", "Kim",
         "Santos", "Reyes", "Jensen", "Haddad", "Lopez", "Nguyen", "Carter", "Murphy"]
_RANKS = ["Private", "Specialist", "Corporal", "Sergeant", "Airman",
          "Lance Corporal", "Petty Officer", "Seaman"]


def _trooper(rng, ranks=None):
    """Rank + last name, with pronouns (last names fit either gender)."""
    he, him, his = rng.choice([("he", "him", "his"), ("she", "her", "her")])
    return Person(f"{rng.choice(ranks or _RANKS)} {rng.choice(_LAST)}", he, him, his)


def _art(word):
    return "an" if word[0] in "aeiouAEIO" else "a"


def _cap(s):
    return s[0].upper() + s[1:]


def _price(rng, lo, hi, cents=(0, 25, 49, 50, 75, 95, 99)):
    """A shelf price between lo and hi dollars with a realistic cents ending."""
    return Q(rng.randint(lo, hi - 1)) + R(rng.choice(cents), 100)


def _cents(v):
    """Exact value in whole cents (an int) - used for independent checks."""
    c = Fraction(str(Q(v))) * 100
    assert c.denominator == 1
    return int(c)


def _pdec(p):
    """Percent p as a decimal string: 6 -> 0.06, 7.5 -> 0.075."""
    return dec_raw(Q(p) / 100)


def is_whole(v):
    return Q(v).is_integer


def _hc(c):
    """Exact money value from integer cents."""
    return R(c, 100)


def _near_money(ans):
    """Filler distractors with the same shape as a money answer (whole dollars
    stay whole, cents keep their cents), spaced by a round step."""
    A = Q(ans)
    step = next(R(x) for x in (R(1, 100), R(1, 20), R(1, 4), 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000)
                if abs(A) <= 12 * Q(x))

    def f(rng):
        out = [A + k * step for k in (1, 2, 3, -1, -2, -3)]
        out = [v for v in out if v > 0]
        rng.shuffle(out)
        return out
    return f


def _near_count(ans):
    A = Q(ans)

    def f(rng):
        out = [A + k for k in (1, 2, 3, 4, -1, -2, -3, -4) if A + k > 0]
        rng.shuffle(out)
        return out
    return f


def _pick(rng, seq, part):
    """rng.choice(seq), or - for a template variant - only from slice k of n."""
    if part is None:
        return rng.choice(seq)
    k, n = part
    return rng.choice(seq[k::n])


def _variants(fn, n):
    """Split a template into n variants that draw from disjoint slices of its
    contexts, so the copies used in one practice set never share a context."""
    out = []
    for k in range(n):
        def g(rng, lvl, _k=k):
            return fn(rng, lvl, part=(_k, n))
        g.__name__ = g.__qualname__ = f"{fn.__name__}_{'abcd'[k]}"
        g.__module__ = fn.__module__
        g.section = fn.section
        out.append(g)
    return out


def _fill(fn):
    """Give a template same-shape filler distractors (no odd 10x or /10 values)."""
    @functools.wraps(fn)
    def wrapper(rng, lvl, **kw):
        p = fn(rng, lvl, **kw)
        if p.near is None and not isinstance(p.answer, str):
            p.near = _near_money(p.answer) if p.fmt is money else _near_count(p.answer)
        return p
    return wrapper


# --------------------------------------------------------------------------
# 1. total cost and change
# --------------------------------------------------------------------------

_SHOPS = [
    ("At the base exchange, {B} buys {L}.", True, [
        ("pair of boot socks", "pairs of boot socks", 7, 14),
        ("PT shirt", "PT shirts", 12, 22),
        ("reflective belt", "reflective belts", 5, 10),
        ("tin of boot polish", "tins of boot polish", 4, 7),
        ("bottle of sunscreen", "bottles of sunscreen", 6, 12),
        ("phone charger", "phone chargers", 12, 25)]),
    ("Before a field exercise, {B} stops at the base exchange and buys {L}.", True, [
        ("headlamp", "headlamps", 15, 30),
        ("pack of AA batteries", "packs of AA batteries", 6, 12),
        ("package of baby wipes", "packages of baby wipes", 3, 7),
        ("bottle of foot powder", "bottles of foot powder", 4, 8),
        ("box of energy bars", "boxes of energy bars", 6, 12),
        ("bottle of insect repellent", "bottles of insect repellent", 5, 10)]),
    ("At a grocery store, {B} buys {L}.", False, [
        ("gallon of milk", "gallons of milk", 3, 5),
        ("loaf of bread", "loaves of bread", 2, 5),
        ("box of cereal", "boxes of cereal", 3, 6),
        ("bag of apples", "bags of apples", 3, 7),
        ("jar of salsa", "jars of salsa", 3, 6),
        ("bag of coffee", "bags of coffee", 7, 13)]),
    ("At a hardware store, {B} buys {L}.", False, [
        ("box of screws", "boxes of screws", 4, 9),
        ("roll of duct tape", "rolls of duct tape", 5, 9),
        ("paintbrush", "paintbrushes", 6, 14),
        ("tape measure", "tape measures", 8, 18),
        ("pair of work gloves", "pairs of work gloves", 7, 15),
        ("can of spray paint", "cans of spray paint", 5, 9)]),
    ("Shopping for school supplies, {B} buys {L}.", False, [
        ("notebook", "notebooks", 2, 5),
        ("pack of pens", "packs of pens", 3, 8),
        ("binder", "binders", 4, 9),
        ("calculator", "calculators", 10, 20),
        ("pack of index cards", "packs of index cards", 2, 4),
        ("set of highlighters", "sets of highlighters", 4, 8)]),
    ("At a sporting-goods store, {B} buys {L}.", False, [
        ("basketball", "basketballs", 20, 35),
        ("water bottle", "water bottles", 8, 15),
        ("jump rope", "jump ropes", 6, 12),
        ("pair of gym shorts", "pairs of gym shorts", 15, 28),
        ("can of tennis balls", "cans of tennis balls", 3, 6),
        ("yoga mat", "yoga mats", 15, 30)]),
]


@template("AR")
@_fill
def change_due(rng, lvl, part=None):
    fmt_s, mil, items = _pick(rng, _SHOPS, part)
    B = _trooper(rng) if mil else person(rng)
    (n1, pl1, lo1, hi1), (n2, pl2, lo2, hi2) = rng.sample(items, 2)
    a, b = _price(rng, lo1, hi1), _price(rng, lo2, hi2)
    if lvl == 1:
        q1 = q2 = 1
    else:
        q1, q2 = rng.choice([2, 3, 4]), rng.choice([1, 2, 3])
    total = q1 * a + q2 * b
    need(total < 98 and not is_whole(total))
    bills = [v for v in (10, 20, 50, 100) if v > total + 1]
    bill = Q(bills[0] if len(bills) == 1 or rng.random() < 0.7 else bills[1])
    change = bill - total

    def part(q, n, pl, p):
        return f"{_art(n)} {n} for {money(p)}" if q == 1 else f"{q} {pl} at {money(p)} each"

    lst = f"{part(q1, n1, pl1, a)} and {part(q2, n2, pl2, b)}"
    stem = (fmt_s.format(B=B, L=lst)
            + f" {B.He} pays with a {money(bill)} bill. "
            + choose(rng, f"How much change should {B.he} receive?",
                     f"How much change does {B.he} get back?"))
    steps = []
    if lvl == 1:
        steps.append(f"Add the prices to find the total cost: {m(f'{money(a)} + {money(b)} = {money(total)}')}.")
    else:
        c1 = m(f"{q1} \\times {money(a)} = {money(q1 * a)}")
        c2 = (f"the {n2} costs {money(b)}" if q2 == 1
              else m(f"{q2} \\times {money(b)} = {money(q2 * b)}"))
        steps.append(f"Find the cost of each kind of item: {c1}, and {c2}.")
        steps.append(f"Add to get the total cost: {m(f'{money(q1 * a)} + {money(q2 * b)} = {money(total)}')}.")
    steps.append(f"Subtract the total from the amount paid: "
                 f"{m(f'{money_cents(bill)} - {money(total)} = {money(change)}')}.")
    rounded = q1 * a.ceiling() + q2 * b.ceiling()
    wrong = [
        (total, "is the total cost, not the change"),
        (change + 1, "forgets to borrow a dollar when subtracting the cents"),
        (bill - rounded, "rounds each price up to a whole dollar instead of using the exact prices"),
    ]
    if lvl == 1:
        wrong.append((bill - a, f"leaves out the price of the {n2}"))
    else:
        wrong.append((bill - a - b, "prices only one of each item and ignores the quantities"))
        if q2 > 1:
            wrong.append((bill - q1 * a - b, f"counts only one of the {pl2}"))
    return Problem(
        stem=stem, answer=change, fmt=money, section="AR", wrong=wrong, steps=steps,
        tip=(f"Check by counting up: {m(f'{money(total)} + {money(change)} = {money_cents(bill)}')}."
             if lvl == 1 else None),
        check=_hc(_cents(bill) - q1 * _cents(a) - q2 * _cents(b)),
        verify=lambda v: v + q1 * a + q2 * b == bill,
    )


# --------------------------------------------------------------------------
# 2. sale price after a discount
# --------------------------------------------------------------------------

_SALE = [
    # (item, lo, hi, step, military)
    ("pair of hiking boots", 80, 180, 5, False),
    ("winter coat", 80, 220, 5, False),
    ("pair of running shoes", 60, 150, 5, False),
    ("bicycle", 150, 480, 10, False),
    ("microwave oven", 60, 160, 5, False),
    ("set of wireless earbuds", 40, 160, 5, False),
    ("desk chair", 80, 240, 5, False),
    ("pair of tactical sunglasses", 60, 160, 5, True),
    ("hydration backpack", 40, 100, 5, True),
    ("smartwatch", 180, 400, 10, True),
    ("gaming headset", 60, 150, 5, False),
]


@template("AR")
@_fill
def sale_price(rng, lvl, part=None):
    item, lo, hi, st, mil = _pick(rng, _SALE, part)
    P = Q(rng.choice(range(lo, hi + 1, st)))
    p = rng.choice([10, 15, 20, 25, 30, 35, 40, 50])
    disc = P * p / 100
    sale = P - disc
    if mil:
        T = _trooper(rng)
        stem = (f"The base exchange is having {_art_n(p)} {pct(p)}-off sale. {T} buys {_art(item)} {item} "
                f"that regularly costs {money(P)}. How much does {T.he} pay? "
                f"(There is no sales tax at the exchange.)")
    else:
        B = person(rng)
        stem = choose(
            rng,
            f"{_cap(_art(item))} {item} regularly sells for {money(P)}. This week it is on sale for "
            f"{pct(p)} off. What is the sale price?",
            f"{B} wants to buy {_art(item)} {item} that normally costs {money(P)}. The store is taking "
            f"{pct(p)} off the price this weekend. How much will the {item} cost on sale?",
            f"A store marks down {_art(item)} {item} from its regular price of {money(P)} by {pct(p)}. "
            f"What is the new price?")
    return Problem(
        stem=stem, answer=sale, fmt=money, section="AR",
        wrong=[
            (disc, "is the amount of the discount, not the sale price"),
            (P - p, "subtracts the percent as if it were dollars"),
            (P + disc, "adds the discount instead of subtracting it"),
            (P - disc / 10, "moves the decimal point one place too far when finding the discount"),
        ],
        steps=[
            f"Find the discount: {m(f'{p}\\% \\text{{ of }} {money(P)} = {_pdec(p)} \\times {int_raw(P)} = {money(disc)}')}.",
            f"Subtract it from the regular price: {m(f'{money(P)} - {money(disc)} = {money(sale)}')}.",
        ],
        tip=(f"Shortcut: {pct(p)} off means you pay {m(f'100\\% - {p}\\% = {100 - p}\\%')}, and "
             f"{m(f'{_pdec(100 - p)} \\times {money(P)} = {money(sale)}')}."),
        check=P * (100 - p) / 100,
    )


# --------------------------------------------------------------------------
# 3. sales tax
# --------------------------------------------------------------------------

_TAX_ONE = [
    # (item, lo, hi, step)
    ("pair of jeans", 30, 70, 2),
    ("coffee maker", 30, 90, 5),
    ("printer", 60, 200, 5),
    ("car battery", 90, 200, 5),
    ("television", 200, 700, 10),
    ("laptop", 300, 900, 10),
    ("lawn mower", 150, 400, 10),
    ("pair of work boots", 60, 160, 5),
]

_TAX_MULTI = [
    # (singular, plural, lo, hi) items bought several at a time; second item single
    (("can of paint", "cans of paint", 25, 45), ("paint roller", "paint rollers", 8, 15)),
    (("tire", "tires", 80, 160), ("set of wiper blades", "sets of wiper blades", 15, 30)),
    (("pair of jeans", "pairs of jeans", 25, 50), ("belt", "belts", 15, 30)),
    (("video game", "video games", 30, 60), ("controller", "controllers", 40, 70)),
    (("houseplant", "houseplants", 8, 20), ("bag of potting soil", "bags of potting soil", 6, 12)),
    (("bag of mulch", "bags of mulch", 4, 8), ("garden hose", "garden hoses", 20, 40)),
]


@template("AR")
@_fill
def sales_tax(rng, lvl, part=None):
    t = rng.choice([4, 5, 6, 7, 8] if lvl == 1 else [5, 6, 7, 8, R(15, 2)])
    mil = rng.random() < 0.35
    B = _trooper(rng) if mil else person(rng)
    where = (choose(rng, "at a store off base", "in town on a weekend pass") if mil
             else choose(rng, "at a local store", "online", "at a department store"))
    if lvl == 1:
        item, lo, hi, st = _pick(rng, _TAX_ONE, part)
        sub = Q(rng.choice(range(lo, hi + 1, st)))
        stem = (f"{B} buys {_art(item)} {item} {where} for {money(sub)}. The sales tax rate is {pct(t)}. "
                f"What is the total cost, including tax?")
        first = []
        q1 = a = b = None
    else:
        (n1, pl1, lo1, hi1), (n2, pl2, lo2, hi2) = rng.choice(_TAX_MULTI)
        q1 = rng.choice([2, 3, 4])
        a = _price(rng, lo1, hi1, cents=(0, 50, 0, 0))
        b = _price(rng, lo2, hi2, cents=(0, 50, 0, 0))
        sub = q1 * a + b
        stem = (f"{B} buys {q1} {pl1} at {money(a)} each and {_art(n2)} {n2} for {money(b)} {where}. "
                f"The sales tax rate is {pct(t)}. What is the total cost, including tax?")
        first = [f"Find the cost before tax: {m(f'{q1} \\times {money(a)} + {money(b)} = {money(q1 * a)} + {money(b)} = {money(sub)}')}."]
    tax = sub * Q(t) / 100
    need((tax * 100).is_integer)
    total = sub + tax
    wrong = [
        (tax, "is the tax alone, not the total cost"),
        (sub + t, "adds the tax rate as if it were dollars"),
        (sub + tax * 10, "moves the decimal point only one place when finding the tax"),
        (sub - tax, "subtracts the tax instead of adding it"),
    ]
    if lvl > 1:
        wrong += [
            (sub, "forgets to add the tax"),
            ((a + b) * (100 + Q(t)) / 100, "prices only one of each item and ignores the quantity"),
        ]
    return Problem(
        stem=stem, answer=total, fmt=money, section="AR", wrong=wrong,
        steps=first + [
            f"Find the tax: {m(f'{dec_raw(t)}\\% \\text{{ of }} {money(sub)} = {_pdec(t)} \\times {dec_raw(sub)} = {money(tax)}')}.",
            f"Add the tax to the price: {m(f'{money(sub)} + {money(tax)} = {money(total)}')}.",
        ],
        tip=(f"In one step: with tax you pay {m(f'{dec_raw(100 + Q(t))}\\%')}, so multiply by "
             f"{m(dec_raw(1 + Q(t) / 100))}." if lvl == 1 else None),
        check=_hc(_cents(sub) * (100 + Q(t)) / 100),
    )


# --------------------------------------------------------------------------
# 4. discount, then tax on the sale price (level 3)
# --------------------------------------------------------------------------

_BIG = [
    # (item, lo, hi, step)
    ("television", 300, 900, 10),
    ("laptop", 400, 1200, 20),
    ("recliner", 300, 800, 10),
    ("set of four tires", 400, 900, 20),
    ("mattress", 400, 1200, 20),
    ("mountain bike", 300, 900, 10),
    ("gaming console", 300, 600, 10),
    ("dishwasher", 400, 900, 10),
]


@template("AR")
@_fill
def discount_tax(rng, lvl, part=None):
    item, lo, hi, st = _pick(rng, _BIG, part)
    P = Q(rng.choice(range(lo, hi + 1, st)))
    d = rng.choice([10, 15, 20, 25, 30, 40])
    t = rng.choice([5, 6, 7, 8])
    disc = P * d / 100
    sale = P - disc
    need(sale.is_integer)
    tax = sale * t / 100
    total = sale + tax
    v = _pick(rng, [0, 1, 2], part)
    if v == 0:
        T = _trooper(rng)
        stem = (f"{T} is furnishing an apartment off base. {_cap(_art(item))} {item} that regularly "
                f"costs {money(P)} is on sale for {pct(d)} off. A sales tax of {pct(t)} is charged on the "
                f"sale price. How much does {T.he} pay in all?")
    elif v == 1:
        stem = (f"{_cap(_art(item))} {item} is priced at {money(P)}. It is on sale for {pct(d)} off, and "
                f"{_art_n(t)} {pct(t)} sales tax is charged on the sale price. What is the total cost?")
    else:
        B = person(rng)
        stem = (f"{B} buys {_art(item)} {item} during {_art_n(d)} {pct(d)}-off sale. The regular price is "
                f"{money(P)}, and {pct(t)} sales tax is added to the sale price. How much does {B.he} "
                f"pay, including tax?")
    return Problem(
        stem=stem, answer=total, fmt=money, section="AR",
        wrong=[
            (sale, "forgets to add the sales tax"),
            (P - disc + P * t / 100, "figures the tax on the regular price instead of the sale price"),
            (P * (100 + t) / 100, "adds the tax but forgets the discount"),
            (sale - tax, "subtracts the tax instead of adding it"),
        ],
        steps=[
            f"Find the discount: {m(f'{_pdec(d)} \\times {money(P)} = {money(disc)}')}.",
            f"Sale price: {m(f'{money(P)} - {money(disc)} = {money(sale)}')}.",
            f"Tax on the \\emph{{sale}} price: {m(f'{_pdec(t)} \\times {money(sale)} = {money(tax)}')}.",
            f"Total: {m(f'{money(sale)} + {money(tax)} = {money(total)}')}.",
        ],
        tip=(f"Or chain the multipliers: {m(f'{money(P)} \\times {_pdec(100 - d)} \\times {dec_raw(R(100 + t, 100))} = {money(total)}')}."),
        check=_hc(_cents(P) * (100 - d) * (100 + t) / 10000),
    )


# --------------------------------------------------------------------------
# 5. unit price - two packages (level 2)
# --------------------------------------------------------------------------

_PRODUCTS = [
    # (kind, "X come(s)", noun after "of", pkg, unit, unit_pl, sizes, u_lo, u_hi (cents), military)
    ("wt", "peanut butter comes", "peanut butter", "jar", "ounce", "ounces", [12, 16, 18, 28, 40], 10, 24, False),
    ("wt", "cereal comes", "cereal", "box", "ounce", "ounces", [10, 12, 14, 18, 24], 16, 36, False),
    ("wt", "coffee comes", "coffee", "bag", "ounce", "ounces", [12, 16, 24, 32, 40], 28, 60, False),
    ("wt", "laundry detergent comes", "laundry detergent", "bottle", "ounce", "ounces", [50, 64, 100, 150], 8, 18, False),
    ("wt", "rice comes", "rice", "bag", "pound", "pounds", [2, 5, 10, 20], 80, 180, False),
    ("wt", "dog food comes", "dog food", "bag", "pound", "pounds", [5, 15, 30, 40], 80, 200, False),
    ("ct", "sports drinks come", "sports drinks", "pack", "bottle", "bottles", [6, 8, 12, 24], 50, 125, True),
    ("ct", "AA batteries come", "AA batteries", "pack", "battery", "batteries", [4, 8, 12, 24], 40, 125, True),
    ("ct", "protein bars come", "protein bars", "box", "bar", "bars", [6, 10, 12, 15, 20], 75, 200, True),
    ("ct", "bottled water comes", "bottles of water", "case", "bottle", "bottles", [12, 24, 32, 40], 15, 40, False),
]


def _art_n(k):
    """Article before a number: 'an 18-ounce', 'an 8-pack', 'a 16-ounce'."""
    return "an" if str(k).startswith("8") or k in (11, 18) else "a"


def _desc(kind, product, pkg, unit_, s):
    if kind == "wt":
        return f"{_art_n(s)} {s}-{unit_} {pkg} of {product}"
    return f"{_art(pkg)} {pkg} of {s} {product}"


def _short(kind, pkg, unit_, s):
    return f"the {s}-{unit_} {pkg}" if kind == "wt" else f"the {pkg} of {s}"


def _place(rng, mil):
    if mil:
        return choose(rng, "At the base commissary", "At the base exchange")
    return choose(rng, "At a grocery store", "At a supermarket", "At a warehouse store", "Online")


@template("AR")
@_fill
def unit_price(rng, lvl, part=None):
    kind, _subj, product, pkg, u_, upl, sizes, ulo, uhi, mil = _pick(rng, _PRODUCTS, part)
    s1, s2 = sorted(rng.sample(sizes, 2))
    u1 = rng.randint(ulo, uhi)
    gap = rng.randint(1, max(2, (uhi - ulo) // 6))
    u2 = u1 - gap if rng.random() < 0.75 else u1 + gap     # bigger is usually cheaper
    need(ulo <= u2 <= uhi)
    U1, U2 = R(u1, 100), R(u2, 100)
    P1, P2 = U1 * s1, U2 * s2
    need(P1 != P2)
    best, worse = min(U1, U2), max(U1, U2)
    d1, d2 = _desc(kind, product, pkg, u_, s1), _desc(kind, product, pkg, u_, s2)
    bd = _short(kind, pkg, u_, s1 if U1 < U2 else s2)
    place = _place(rng, mil)
    B = _trooper(rng) if mil else person(rng)
    stem = (f"{place}, {d1} costs {money(P1)}, and {d2} costs {money(P2)}. "
            + choose(rng, f"What is the price per {u_} of the better buy?",
                     f"{B} wants the better buy, so {B.he} compares the prices per {u_}. "
                     f"What is the lower price per {u_}?"))
    return Problem(
        stem=stem, answer=best, fmt=money, section="AR",
        wrong=[
            (worse, f"is the price per {u_} of the worse buy"),
            (best - (worse - best) if best > worse - best else worse + (worse - best), None),
            (worse - best, f"is the difference between the two prices per {u_}"),
            (abs(P2 - P1), f"compares the total prices instead of the prices per {u_}"),
        ],
        steps=[
            f"Divide each price by its number of {upl}. Smaller size: {m(f'{money(P1)} \\div {s1} = {money_cents(U1)}')} per {u_}.",
            f"Larger size: {m(f'{money(P2)} \\div {s2} = {money_cents(U2)}')} per {u_}.",
            f"The better buy is the one with the lower price per {u_}: {bd}, at {money_cents(best)} per {u_}.",
        ],
        check=R(min(u1, u2), 100),
        verify=lambda v: v * (s1 if U1 < U2 else s2) == (P1 if U1 < U2 else P2),
    )


# --------------------------------------------------------------------------
# 6. best buy among three sizes (level 3, text answer)
# --------------------------------------------------------------------------

@template("AR")
@_fill
def best_buy(rng, lvl, part=None):
    kind, subj, product, pkg, u_, upl, sizes, ulo, uhi, mil = _pick(rng, _PRODUCTS[::-1], part)
    need(len(sizes) >= 3)
    ss = sorted(rng.sample(sizes, 3))
    lowu, *others = sorted(rng.sample(range(ulo, uhi + 1), 3))
    need(others[-1] - lowu <= max(4, (uhi - ulo) // 3))
    ib = rng.choices([0, 1, 2], weights=[25, 35, 40])[0]   # bigger is a bit more often the best buy
    rng.shuffle(others)
    us = others[:ib] + [lowu] + others[ib:]
    Us = [R(u, 100) for u in us]
    Ps = [U * s for U, s in zip(Us, ss)]
    need(len(set(Ps)) == 3)
    names = [_short(kind, pkg, u_, s) for s in ss]
    descs = [_desc(kind, product, pkg, u_, s) for s in ss]
    place = _place(rng, mil)
    stem = (f"{place}, {subj} in three sizes: {descs[0]} for {money(Ps[0])}, {descs[1]} for "
            f"{money(Ps[1])}, and {descs[2]} for {money(Ps[2])}. Which size is the best buy?")
    cheapest_tag = min(range(3), key=lambda i: Ps[i])
    wrong = []
    for i in range(3):
        if i == ib:
            continue
        lead = ("has the lowest price tag, but it costs" if i == cheapest_tag
                else "is the largest size, but it costs" if i == 2 else "costs")
        wrong.append((names[i], f"{lead} {money_cents(Us[i])} per {u_}, more than {money_cents(Us[ib])}"))
    wrong.append((f"All three cost the same per {u_}",
                  f"is not true: the prices per {u_} are {money_cents(Us[0])}, {money_cents(Us[1])}, "
                  f"and {money_cents(Us[2])}"))
    # independent route: compare by cross-multiplying (no division)
    def cheaper(i, j):
        return Ps[i] * ss[j] < Ps[j] * ss[i]
    chk = [i for i in range(3) if all(cheaper(i, j) for j in range(3) if j != i)]
    need(len(chk) == 1)
    return Problem(
        stem=stem, answer=names[ib], fmt=text, section="AR", wrong=wrong,
        steps=[
            f"Find each price per {u_} (price {m('\\div')} number of {upl}): "
            + "; ".join(m(f"{money(Ps[i])} \\div {ss[i]} = {money_cents(Us[i])}") for i in range(3)) + ".",
            f"The lowest price per {u_} is {money_cents(Us[ib])}, so {names[ib]} is the best buy.",
        ],
        tip=("The biggest package is not always the best deal, so always compare unit prices."
             if ib != 2 else None),
        check=names[chk[0]],
    )


# --------------------------------------------------------------------------
# 7. overtime pay
# --------------------------------------------------------------------------

_JOBS = [
    # (phrase, rate lo, rate hi, military-flavored)
    ("a warehouse worker", 16, 22, False),
    ("a line cook", 14, 19, False),
    ("a security guard", 15, 22, False),
    ("a delivery driver", 17, 24, False),
    ("a hotel desk clerk", 14, 18, False),
    ("a civilian mechanic at the base motor pool", 20, 28, True),
    ("a contractor at the base dining facility", 14, 18, True),
    ("a forklift operator at an Army supply depot", 18, 24, True),
]


@template("AR")
@_fill
def overtime(rng, lvl, part=None):
    job, lo, hi, mil = _pick(rng, _JOBS, part)
    B = person(rng)
    r = Q(rng.randint(lo, hi))
    ot = r * R(3, 2)
    v = 0 if lvl == 2 else (rng.choice([1, 1, 2]) if part is None else _pick(rng, [1, 2], part))
    if v in (0, 2):
        h = rng.choice([42, 43, 44, 45, 46, 47, 48, 50])
    else:
        per_day, days, sat = rng.choice([(9, 5, 0), (10, 5, 0), (9, 5, 4), (9, 5, 6), (8, 5, 5),
                                         (8, 5, 6), (8, 5, 8), (10, 4, 6), (10, 5, 4), (11, 4, 0)])
        h = per_day * days + sat
        need(h > 40)
    k = h - 40
    reg = 40 * r
    otp = k * ot
    pay = reg + otp
    intro = (f"{B} works as {job} and earns {money(r)} per hour, with time-and-a-half for every hour "
             f"over 40 in a week.")
    if v == 0:
        stem = intro + f" Last week {B.he} worked {h} hours. How much did {B.he} earn last week?"
    elif v == 1:
        dayword = {4: "Monday through Thursday", 5: "Monday through Friday"}[days]
        sat_txt = f" and {sat} hours on Saturday" if sat else ""
        stem = (intro + f" Last week {B.he} worked {per_day} hours a day {dayword}{sat_txt}. "
                f"How much did {B.he} earn for the week?")
    else:
        stem = (intro + f" Last week {B.his} pay was {money(pay)}. How many hours did {B.he} work "
                f"last week?")
    split = (f"Only hours over 40 are overtime: {m(f'{h} - 40 = {k}')} overtime hours.")
    ot_line = (f"Overtime rate: {m(f'1.5 \\times {money(r)} = {money(ot)}')} per hour.")
    if v in (0, 1):
        steps = []
        if v == 1:
            hrs = (f"{per_day} \\times {days} + {sat} = {h}" if sat else f"{per_day} \\times {days} = {h}")
            steps.append(f"Total hours: {m(hrs)} hours.")
        steps += [
            split,
            f"Regular pay: {m(f'40 \\times {money(r)} = {money(reg)}')}. {ot_line}",
            f"Overtime pay: {m(f'{k} \\times {money(ot)} = {money(otp)}')}.",
            f"Total: {m(f'{money(reg)} + {money(otp)} = {money(pay)}')}.",
        ]
        wrong = [
            (h * ot, "pays time-and-a-half for all the hours, not just the hours over 40"),
            (h * r, "pays every hour at the regular rate"),
            (reg + k * 2 * r, "pays double time instead of time-and-a-half"),
            (otp, "is the overtime pay only"),
            (reg + k * r / 2, "pays the overtime hours only the extra half rate"),
        ]
        return Problem(stem=stem, answer=pay, fmt=money, section="AR", wrong=wrong, steps=steps,
                       check=h * r + k * r / 2)
    # v == 2: reverse - find the hours
    steps = [
        f"Pay for the first 40 hours: {m(f'40 \\times {money(r)} = {money(reg)}')}.",
        f"The rest of the pay is overtime: {m(f'{money(pay)} - {money(reg)} = {money(otp)}')}.",
        f"{ot_line} Overtime hours: {m(f'{money(otp)} \\div {money(ot)} = {k}')}.",
        f"Total hours: {m(f'40 + {k} = {h}')} hours.",
    ]
    wrong = [
        (k, "gives only the overtime hours, not the total"),
        (40 + otp / r, "divides the overtime pay by the regular rate instead of the overtime rate"),
        (pay / r, "divides the whole paycheck by the regular rate"),
        (pay / ot, "divides the whole paycheck by the overtime rate"),
    ]
    return Problem(stem=stem, answer=Q(h), fmt=unit(num, "hour"), section="AR",
                   wrong=[(w, y) for w, y in wrong if Q(w).is_integer], steps=steps,
                   near=lambda g: [Q(h + d) for d in g.sample([-3, -2, -1, 1, 2, 3, 4, 5], 6)],
                   verify=lambda H: 40 * r + (H - 40) * ot == pay,
                   check=next(H for H in range(41, 80) if 40 * r + (H - 40) * ot == pay))


# --------------------------------------------------------------------------
# 8. paycheck from an annual salary
# --------------------------------------------------------------------------

_CIV_JOBS = [
    ("a medical assistant", 34000, 46000), ("a bank teller", 31000, 40000),
    ("an electrician's apprentice", 36000, 50000), ("an office manager", 42000, 62000),
    ("a police officer", 48000, 65000), ("a truck driver", 50000, 68000),
    ("a dental assistant", 38000, 50000),
]

_MIL_PAY = [
    # (ranks, annual lo, annual hi)
    (["Private", "Airman", "Seaman"], 24000, 30000),
    (["Specialist", "Lance Corporal", "Airman First Class"], 28000, 36000),
    (["Corporal", "Sergeant", "Petty Officer"], 34000, 46000),
    (["Staff Sergeant", "Technical Sergeant"], 42000, 54000),
]

_FREQ = {
    26: ("every two weeks", "biweekly (every two weeks)"),
    24: ("twice a month", "twice a month, on the 15th and on the last day of the month"),
    52: ("every week", "weekly"),
}

_FREQ_STEP = {
    26: "Every two weeks means {m1} paychecks a year (\\emph{{not}} 24).",
    24: "Twice a month means {m1} paychecks a year.",
    52: "Paid every week means 52 paychecks a year.",
}


@template("AR")
@_fill
def paycheck(rng, lvl, part=None):
    mil = rng.random() < (0.4 if lvl == 2 else 0.35) if part is None else bool(_pick(rng, [0, 1], part))
    if mil:
        ranks, lo, hi = rng.choice(_MIL_PAY)
        T = _trooper(rng, ranks)
        P = 24
    else:
        job, lo, hi = rng.choice(_CIV_JOBS)
        T = person(rng)
        P = rng.choice([26, 26, 24, 52])
    # paycheck sizes chosen so the classic wrong divisions also come out to whole cents
    stepc = 325 if (P == 24 and rng.random() < 0.6) else (150 if P in (26, 52) else 50)
    c = Q(rng.choice(range(-(-lo // P // stepc) * stepc, hi // P + 1, stepc) or [0]))
    S = c * P
    need(c > 0 and lo <= S <= hi)
    m1 = {26: m("52 \\div 2 = 26"), 24: m("12 \\times 2 = 24"), 52: ""}[P]
    count_step = _FREQ_STEP[P].format(m1=m1)
    div_step = f"Divide the yearly pay by the number of paychecks: {m(f'{money(S)} \\div {P} = {money(c)}')}."
    if mil:
        intro = (f"{T}'s yearly base pay is {money(S)}. Service members are paid twice a month, on the "
                 f"1st and the 15th.")
    else:
        intro = (f"{T} works as {job} for a salary of {money(S)} a year and is paid "
                 f"{rng.choice(_FREQ[P])}.")
    month = (S / 12, "divides by 12, which gives one month's pay")
    if P == 26:
        wrong_base = [(S / 24, "uses 24 paychecks, but every two weeks gives 26 paychecks a year"),
                      month,
                      (S / 52, "divides by 52, the number of weeks, not the number of paychecks")]
    elif P == 24:
        wrong_base = [(S / 26, "uses 26 paychecks, but twice a month gives 24 paychecks a year"),
                      month,
                      (S / 52, "divides by 52, the number of weeks, not the number of paychecks")]
    else:
        wrong_base = [month,
                      (S / 26, "divides by 26, but weekly pay means 52 paychecks"),
                      (S / 24, "divides by 24, but weekly pay means 52 paychecks")]
    if lvl == 2:
        stem = intro + " How much is each paycheck before taxes and other deductions?"
        return Problem(stem=stem, answer=c, fmt=money, section="AR", wrong=wrong_base,
                       steps=[count_step, div_step],
                       tip=f"Check: {m(f'{P} \\times {money(c)} = {money(S)}')}.",
                       verify=lambda v: v * P == S)
    if mil:
        # base pay + monthly housing allowance, both split over two paychecks
        H = Q(rng.choice(range(1200, 2401, 50)))
        hh = H / 2
        ans = c + hh
        stem = (intro + f" {T.He} also receives a housing allowance of {money(H)} per month, which is "
                f"split evenly between the two paychecks. How much does each paycheck include for base pay "
                f"and housing together?")
        return Problem(
            stem=stem, answer=ans, fmt=money, section="AR",
            wrong=[(c + H, "adds a whole month of housing allowance to each paycheck"),
                   (c, "leaves out the housing allowance"),
                   (S / 12 + H, "gives the total for a month, not for one paycheck"),
                   (S / 12 + hh, "divides the yearly pay by 12 instead of 24")],
            steps=[count_step + " " + div_step.replace("Divide the yearly pay", "Base pay per paycheck: divide the yearly pay"),
                   f"Housing per paycheck: {m(f'{money(H)} \\div 2 = {money(hh)}')}.",
                   f"Add: {m(f'{money(c)} + {money(hh)} = {money(ans)}')}."],
            check=(S / 12 + H) / 2)
    w = rng.choice([15, 20, 25])
    held = c * w / 100
    take = c - held
    need((held * 100).is_integer)
    stem = (intro + f" Of each paycheck, {pct(w)} is withheld for taxes. How much does {T.he} take home "
            f"from each paycheck?")
    return Problem(
        stem=stem, answer=take, fmt=money, section="AR",
        wrong=[(c, "forgets to subtract the taxes withheld"),
               (held, "is the amount withheld, not the take-home pay"),
               (S / 12 * (100 - w) / 100, "divides by 12 months instead of the number of paychecks"),
               (S / (24 if P == 26 else 26) * (100 - w) / 100,
                "uses the wrong number of paychecks per year" if P != 52 else None)],
        steps=[count_step, div_step,
               f"Taxes withheld: {m(f'{_pdec(w)} \\times {money(c)} = {money(held)}')}.",
               f"Take-home pay: {m(f'{money(c)} - {money(held)} = {money(take)}')}."],
        check=S * (100 - w) / (100 * P))


# --------------------------------------------------------------------------
# 9. budget shares (fractions of a paycheck)
# --------------------------------------------------------------------------

_RENT = [R(1, 4), R(1, 3), R(3, 10), R(2, 5)]
_SAVE = [R(1, 10), R(1, 5), R(1, 4), R(1, 6)]
_SMALL = [R(1, 6), R(1, 8), R(1, 10), R(1, 5)]
_HOME = [R(1, 4), R(1, 3), R(1, 5)]


@template("AR")
@_fill
def budget_share(rng, lvl, part=None):
    mil = rng.random() < 0.4
    B = _trooper(rng) if mil else person(rng)
    # (verb, phrase, noun for "the amount ...", realistic fractions of the whole pay)
    if mil:
        T = Q(rng.choice(range(1800, 3601, 60)))
        who = f"{B}'s take-home pay is {money(T)} a month."
        uses = [("sends", "home to {his} family", "sent home", _HOME),
                ("puts", "into savings", "saved", _SAVE),
                ("pays", "toward a car loan", "paid on the car loan", _SMALL)]
    else:
        T = Q(rng.choice(range(1800, 4801, 60)))
        who = f"{B} takes home {money(T)} a month."
        uses = [("spends", "on rent", "spent on rent", _RENT),
                ("puts", "into savings", "saved", _SAVE),
                ("spends", "on groceries", "spent on groceries", _SMALL),
                ("pays", "toward a car loan", "paid on the car loan", _SMALL)]
    (v1, w1, n1, fs1), (v2, w2, n2, fs2) = rng.sample(uses, 2)
    if lvl == 3 and not mil:
        (v1, w1, n1, fs1) = uses[0]            # rent comes off the top first
        (v2, w2, n2, fs2) = rng.choice(uses[1:])
    w1, w2 = w1.format(his=B.his), w2.format(his=B.his)
    f1 = rng.choice(fs1)
    p1 = T * f1
    need(p1.is_integer)
    fr1 = m(frac_raw(f1))
    if lvl == 1:
        ask_left = rng.random() < 0.5 if part is None else bool(_pick(rng, [0, 1], part))
        left = T - p1
        one = T / f1.q
        find = (f"{fr1} of the pay: {m(f'{money(T)} \\div {f1.q} = {money(one)}')}"
                + (f", and {m(f'{f1.p} \\times {money(one)} = {money(p1)}')}" if f1.p > 1 else ""))
        if ask_left:
            stem = who + f" {B.He} {v1} {fr1} of it {w1}. How much of the month's pay is left?"
            wrong = [(p1, f"is the amount {n1}, not the amount left")]
            if f1.p > 1:
                wrong.append((T - one, f"subtracts only {m(frac_raw(R(1, f1.q)))} of the pay"))
            return Problem(
                stem=stem, answer=left, fmt=money, section="AR", wrong=wrong,
                steps=[f"Find {find}. That is the amount {n1}.",
                       f"Subtract it from the pay: {m(f'{money(T)} - {money(p1)} = {money(left)}')}."],
                tip=(f"Or: {m(f'1 - {frac_raw(f1)} = {frac_raw(1 - f1)}')} of the pay is left, and "
                     f"{m(f'{frac_raw(1 - f1)} \\times {money(T)} = {money(left)}')}."),
                check=Fraction(int(T)) * (1 - Fraction(f1.p, f1.q)))
        stem = who + f" {B.He} {v1} {fr1} of it {w1}. How much does {B.he} {v1.rstrip('s')} {w1} each month?"
        wrong = [(T - p1, f"is the amount left over, not the amount {n1}")]
        if f1.p > 1:
            wrong.append((one, f"finds only {m(frac_raw(R(1, f1.q)))} of the pay and forgets to multiply by {f1.p}"))
        steps = [f"\\emph{{Of}} means multiply: {m(f'{frac_raw(f1)} \\times {money(T)}')}. "
                 f"To find {fr1} of an amount, divide by {f1.q}"
                 + (f" and then multiply by {f1.p}." if f1.p > 1 else "."),
                 f"{m(f'{money(T)} \\div {f1.q} = {money(one)}')}"
                 + (f", and {m(f'{f1.p} \\times {money(one)} = {money(p1)}')}." if f1.p > 1 else ".")]
        return Problem(
            stem=stem, answer=p1, fmt=money, section="AR", wrong=wrong, steps=steps,
            tip=(f"Check: {m(f'{f1.q} \\times {money(p1)} = {money(T)}')}." if f1.p == 1 else None),
            check=Fraction(int(T)) * Fraction(f1.p, f1.q))
    if lvl == 2:
        f2 = rng.choice(fs2)
        need(f1 != f2 and f1 + f2 < R(3, 4))
        p2 = T * f2
        need(p2.is_integer)
        left = T - p1 - p2
        fr2 = m(frac_raw(f2))
        stem = (who + f" {B.He} {v1} {fr1} of it {w1} and {v2} {fr2} of it {w2}. "
                f"How much is left each month for everything else?")
        bad = R(f1.p + f2.p, f1.q + f2.q)
        return Problem(
            stem=stem, answer=left, fmt=money, section="AR",
            wrong=[(p1 + p2, "is the total of the two amounts, not what is left"),
                   (T - p1, f"subtracts only the amount {n1}"),
                   (T - p2, f"subtracts only the amount {n2}"),
                   (T * (1 - bad), "adds the fractions by adding the tops and the bottoms")],
            steps=[f"Amount {n1}: {m(f'{frac_raw(f1)} \\times {money(T)} = {money(p1)}')}.",
                   f"Amount {n2}: {m(f'{frac_raw(f2)} \\times {money(T)} = {money(p2)}')}.",
                   f"What is left: {m(f'{money(T)} - {money(p1)} - {money(p2)} = {money(left)}')}."],
            check=T * (1 - f1 - f2))
    # level 3: a fraction of what is left
    f2 = rng.choice(fs2 + [R(1, 3), R(1, 2)] if "sav" in n2 else fs2 + [R(1, 4)])
    rest1 = T - p1
    p2 = rest1 * f2
    need(p2.is_integer and T * f2 != p2)
    left = rest1 - p2
    ask_left = rng.random() < 0.5
    fr2 = m(frac_raw(f2))
    stem = (who + f" {B.He} {v1} {fr1} of the pay {w1}, and then {v2} {fr2} of what is left {w2}. "
            + ("How much money remains after both?" if ask_left
               else f"How much money does {B.he} {v2.rstrip('s')} {w2}?"))
    wrong_left = [(T - p1 - T * f2, f"takes {fr2} of the whole pay instead of {fr2} of what is left"),
                  (p2, f"is the amount {n2}, not the amount remaining"),
                  (rest1, f"stops after the amount {n1}"),
                  (T * (1 - f1 - f2) if (T * (1 - f1 - f2)) > 0 else T * f2 / 2, None)]
    wrong_part = [(T * f2, f"takes {fr2} of the whole pay instead of {fr2} of what is left"),
                  (left, "is the amount remaining, not the amount asked for"),
                  (rest1, f"is what is left after the amount {n1}, before the second step"),
                  (p1, f"is the amount {n1}")]
    steps = [f"First amount ({n1}): {m(f'{frac_raw(f1)} \\times {money(T)} = {money(p1)}')}.",
             f"What is left: {m(f'{money(T)} - {money(p1)} = {money(rest1)}')}.",
             f"Second amount is {fr2} of \\emph{{that}}: {m(f'{frac_raw(f2)} \\times {money(rest1)} = {money(p2)}')}."]
    if ask_left:
        steps.append(f"Remaining: {m(f'{money(rest1)} - {money(p2)} = {money(left)}')}.")
    return Problem(
        stem=stem, answer=left if ask_left else p2, fmt=money, section="AR",
        wrong=wrong_left if ask_left else wrong_part, steps=steps,
        check=(T * (1 - f1) * (1 - f2)) if ask_left else T * (1 - f1) * f2)


# --------------------------------------------------------------------------
# 10. splitting a bill with a tip
# --------------------------------------------------------------------------

_WORD = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 8: "Eight"}


@template("AR")
@_fill
def split_bill(rng, lvl, part=None):
    t = rng.choice([15, 18, 20])
    v = _pick(rng, list(range(8)), part)
    if v == 0:
        n = rng.choice([3, 4, 5])
        Bl = Q(rng.choice(range(60, 181, 2))) + R(rng.choice([0, 0, 50]), 100)
        P = person(rng)
        stem = (f"After {P}'s graduation from basic training, {P.he} and {n - 1} family members go out to "
                f"dinner. The bill is {money(Bl)}. They add {_art_n(t)} {pct(t)} tip and split the total evenly among "
                f"the {n} of them. How much does each person pay?")
        who = "person"
    elif v == 1:
        n = rng.choice([4, 5, 6, 8])
        Bl = Q(rng.choice(range(40, 101, 2)))
        stem = (f"A squad of {n} soldiers orders pizza for a movie night. The order costs {money(Bl)}, and "
                f"they give the driver {_art_n(t)} {pct(t)} tip. If they split the cost evenly, how much does each "
                f"soldier pay?")
        who = "soldier"
    elif v == 2:
        n = rng.choice([2, 3, 4])
        Bl = Q(rng.choice(range(30, 121, 2))) + R(rng.choice([0, 50]), 100)
        stem = (f"{_WORD[n]} friends eat lunch together. The bill comes to {money(Bl)} before the tip. They "
                f"leave {_art_n(t)} {pct(t)} tip and share the total equally. How much does each friend pay?")
        who = "friend"
    elif v == 3:
        n = rng.choice([4, 5, 6])
        Bl = Q(rng.choice(range(80, 201, 4)))
        stem = (f"{_WORD[n]} coworkers celebrate a birthday at a restaurant. "
                f"The food costs {money(Bl)}, and they add {_art_n(t)} {pct(t)} tip. If they divide the total cost "
                f"equally, what is each coworker's share?")
        who = "coworker"
    elif v == 5:
        n = rng.choice([3, 4, 5])
        Bl = Q(rng.choice(range(90, 241, 5)))
        stem = (f"On their first weekend pass, {n} Marines eat at a steakhouse. The check comes to "
                f"{money(Bl)}, and they add {_art_n(t)} {pct(t)} tip. If they split the total evenly, how much does "
                f"each Marine pay?")
        who = "Marine"
    elif v == 6:
        n = rng.choice([2, 3, 4])
        Bl = Q(rng.choice(range(30, 91, 2))) + R(rng.choice([0, 50]), 100)
        stem = (f"{_WORD[n]} roommates order takeout. The food costs {money(Bl)}, and they add {_art_n(t)} {pct(t)} "
                f"tip for the delivery driver. They split the total equally. What is each roommate's share?")
        who = "roommate"
    elif v == 7:
        n = rng.choice([4, 5, 6])
        Bl = Q(rng.choice(range(60, 161, 4)))
        stem = (f"After a bowling league night, the {n} members of a team share a meal. The bill is "
                f"{money(Bl)}, and they leave {_art_n(t)} {pct(t)} tip. If they split the total evenly, how much does "
                f"each team member pay?")
        who = "team member"
    else:
        n = rng.choice([3, 4, 5, 6])
        Bl = Q(rng.choice(range(60, 151, 2)))
        stem = (f"After a long hike, {n} friends eat at a diner near the trailhead. The bill is "
                f"{money(Bl)}, and they leave {_art_n(t)} {pct(t)} tip. They split the total evenly. How much does "
                f"each friend pay?")
        who = "friend"
    tip = Bl * t / 100
    total = Bl + tip
    each = total / n
    need((each * 100).is_integer and (tip * 100).is_integer)
    return Problem(
        stem=stem, answer=each, fmt=money, section="AR",
        wrong=[(Bl / n, "forgets to add the tip"),
               (total, f"is the total for the whole group, not one {who}'s share"),
               (Bl / n + tip, f"adds the whole tip to one {who}'s share"),
               (tip / n, f"is one {who}'s share of the tip only")],
        steps=[f"Find the tip: {m(f'{_pdec(t)} \\times {money(Bl)} = {money(tip)}')}.",
               f"Total with tip: {m(f'{money(Bl)} + {money(tip)} = {money(total)}')}.",
               f"Split it {n} ways: {m(f'{money(total)} \\div {n} = {money(each)}')}."],
        check=_hc(_cents(Bl) * (100 + t) / 100) / n,
        verify=lambda v: v * n * 100 == Bl * (100 + t),
    )


# --------------------------------------------------------------------------
# 11. weeks needed to reach a savings goal (round up)
# --------------------------------------------------------------------------

_GOALS = [
    # (thing, G lo, G hi, G step, S lo, S hi, w lo, w hi, military)
    ("a down payment on a used car", 1500, 4000, 100, 200, 1200, 75, 250, False),
    ("a new laptop", 600, 1400, 50, 50, 300, 25, 80, False),
    ("a motorcycle", 3000, 7000, 250, 500, 2000, 100, 300, False),
    ("a new phone", 700, 1200, 50, 50, 300, 25, 75, False),
    ("a gaming computer", 900, 2000, 100, 100, 500, 40, 120, False),
    ("a plane ticket home for holiday leave", 400, 900, 25, 50, 300, 30, 80, True),
    ("the security deposit and first month's rent on an apartment off base", 1800, 3600, 100, 300,
     1200, 75, 200, True),
    ("a used truck to drive at the next duty station", 3000, 8000, 250, 500, 2500, 100, 300, True),
]


@template("AR")
@_fill
def savings_weeks(rng, lvl, part=None):
    thing, glo, ghi, gst, slo, shi, wlo, whi, mil = _pick(rng, _GOALS, part)
    B = _trooper(rng) if mil else person(rng)
    G = rng.choice(range(glo, ghi + 1, gst))
    S = rng.choice(range(slo, shi + 1, 10 if shi <= 500 else 50))
    w = rng.choice(range(wlo, whi + 1, 25 if wlo >= 75 else 5))
    rem = G - S
    need(rem > 0 and rem % w != 0)
    q = rem // w
    weeks = q + 1
    need(4 <= weeks <= 40)
    short = rem - q * w
    stem = (f"{B} is saving for {thing}, which costs {money(G)}. {B.He} has already saved {money(S)} and "
            f"can save {money(w)} a week. How many weeks will it take {B.him} to have enough money?")
    stem = stem.replace("the next duty station", f"{B.his} next duty station")
    smart = lambda k: -(-k // w)   # ceiling division
    wk = unit(num, "week")
    return Problem(
        stem=stem, answer=Q(weeks), fmt=wk, section="AR",
        wrong=[(q, f"rounds down, but after {q} weeks {B.he} is still {money(short)} short"),
               (smart(G), f"ignores the {money(S)} already saved"),
               (smart(G + S), "adds the money already saved to the price instead of subtracting it")],
        steps=[f"Money still needed: {m(f'{money(G)} - {money(S)} = {money(rem)}')}.",
               f"Divide by the weekly savings: {m(f'{int_raw(rem)} \\div {w}')} is {q} with "
               f"{int_raw(short)} left over. After {q} weeks {B.he} has saved "
               f"{m(f'{q} \\times {money(w)} = {money(q * w)}')}, still {money(short)} short.",
               f"So {B.he} needs one more week: {m(f'{q} + 1 = {weeks}')} weeks."],
        check=next(k for k in range(1, 200) if S + k * w >= G),
        verify=lambda v: S + v * w >= G and S + (v - 1) * w < G,
    )


# --------------------------------------------------------------------------
# 12. how many items a budget buys (round down)
# --------------------------------------------------------------------------

_BUY1 = [
    # (stem with {B} {M} {C}, item plural, budget range, step, cost choices)
    ("A squad leader has {M} to buy sports drinks for a long day on the range. Each bottle costs {C}. "
     "What is the greatest number of bottles the squad leader can buy?", "bottles", 25, 60, 1,
     [R(5, 4), R(3, 2), R(7, 4), R(9, 4), R(5, 2)]),
    ("{B} has {M} on a transit card. Each bus ride costs {C}. How many rides can {B.he} pay for?",
     "rides", 20, 45, 1, [R(9, 4), R(5, 2), R(11, 4)]),
    ("A coach has {M} to spend on new soccer balls that cost {C} each. How many soccer balls can the "
     "coach buy?", "soccer balls", 100, 250, 5, [Q(14), Q(16), Q(18), Q(22), Q(24)]),
    ("A unit's morale fund has {M} to spend on large pizzas for a platoon party. Each pizza costs {C}. "
     "What is the greatest number of pizzas the unit can buy?", "pizzas", 100, 300, 5,
     [Q(12), Q(13), Q(14), Q(15), Q(16), Q(17)]),
    ("A teacher has {M} to buy calculators for her classroom. Each calculator costs {C}. How many "
     "calculators can she buy?", "calculators", 100, 300, 5, [Q(12), Q(14), Q(16), Q(18)]),
    ("{B} has {M} to spend on paperback books for a long summer trip. Each book costs {C}. How many books "
     "can {B.he} buy?", "books", 40, 90, 1, [Q(7), Q(8), Q(9), Q(11), Q(12)]),
    ("A recruiter has {M} to spend on T-shirts to give away at a high school career fair. Each T-shirt "
     "costs {C}. How many T-shirts can the recruiter buy?", "T-shirts", 150, 400, 5,
     [Q(6), Q(7), Q(8), Q(9), R(13, 2), R(15, 2)]),
    ("A softball coach has {M} to buy caps for the team. Each cap costs {C}. How many caps can the coach "
     "buy?", "caps", 60, 150, 1, [Q(6), Q(7), R(13, 2), R(15, 2), R(17, 2)]),
    ("A school club has {M} to spend on movie tickets for a field trip. Each ticket costs {C}. How many "
     "tickets can the club buy?", "tickets", 80, 200, 5, [Q(9), Q(11), Q(12), R(19, 2), R(21, 2), R(25, 2)]),
]

_BUY2 = [
    # (stem with {M} total, {F} fixed cost, {C} each, {X} fixed item), plural
    ("The platoon has {M} for a barbecue. After spending {F} on charcoal and paper plates, it will spend "
     "the rest on packs of hamburger patties at {C} each. How many packs can it buy?", "packs", 200, 400, 10,
     (25, 60, 5), [Q(12), Q(14), Q(16), Q(18)]),
    ("{B} has {M} to spend at a county fair. Admission is {F}, and each ride ticket costs {C}. After "
     "paying admission, how many ride tickets can {B.he} buy?", "tickets", 40, 80, 5, (8, 15, 1),
     [R(5, 2), Q(3), R(7, 2), Q(4)]),
    ("An office manager has {M} to spend on printer ink. There is a {F} shipping charge on the order, "
     "and each ink cartridge costs {C}. How many cartridges can she order?", "cartridges", 200, 400, 10,
     (10, 20, 5), [Q(22), Q(24), Q(26), Q(28)]),
    ("{B} has {M} for a new fishing setup. {B.He} buys a rod and reel for {F} and wants to spend the rest "
     "on lures that cost {C} each. How many lures can {B.he} buy?", "lures", 100, 160, 10, (45, 80, 5),
     [Q(4), Q(6), Q(7), R(9, 2), R(11, 2)]),
    ("A squad has {M} to spend before a field exercise. It buys a {F} first-aid kit and spends the rest on "
     "boxes of hand warmers at {C} each. How many boxes can it buy?", "boxes", 80, 150, 5, (20, 35, 5),
     [Q(6), Q(7), Q(8), Q(9)]),
]


@template("AR")
@_fill
def items_budget(rng, lvl, part=None):
    B = person(rng)
    if lvl == 1:
        st, pl, lo, hi, step, costs = _pick(rng, _BUY1, part)
        M = Q(rng.choice(range(lo, hi + 1, step)))
        C = rng.choice(costs)
        F = Q(0)
    else:
        st, pl, lo, hi, step, (flo, fhi, fst), costs = rng.choice(_BUY2)
        M = Q(rng.choice(range(lo, hi + 1, step)))
        F = Q(rng.choice(range(flo, fhi + 1, fst)))
        C = rng.choice(costs)
    avail = M - F
    need(avail % C != 0)
    k = int(avail // C)
    need(3 <= k <= 60)
    stem = st.format(B=B, M=money(M), C=money(C), F=money(F))
    left = avail - k * C
    steps = []
    if lvl > 1:
        steps.append(f"First take out the fixed cost: {m(f'{money(M)} - {money(F)} = {money(avail)}')} "
                     f"is left to spend.")
    steps += [
        f"Divide by the price of one: {m(f'{money(avail)} \\div {money(C)}')} is {k} with some money left "
        f"over, because {m(f'{k} \\times {money(C)} = {money(k * C)}')}.",
        f"One more would cost {m(f'{money((k + 1) * C)}')}, which is more than {money(avail)}. "
        f"Round \\emph{{down}}: {k} {pl}.",
    ]
    wrong = [(k + 1, f"rounds up, but {k + 1} {pl} would cost {money((k + 1) * C)}")]
    if not C.is_integer and int(avail // C.ceiling()) < k:
        wrong.append((int(avail // C.ceiling()), f"rounds the price up to {money(C.ceiling())} before dividing"))
    if lvl > 1:
        wrong += [(int(M // C), f"forgets to subtract the {money(F)} first"),
                  (int((M + F) // C), f"adds the {money(F)} instead of subtracting it")]
        if "shipping" in st:
            wrong.append((int(M // (C + F)), f"adds the {money(F)} shipping to the cost of each of the {pl} "
                                             f"instead of paying it once"))
    return Problem(
        stem=stem, answer=Q(k), fmt=num, section="AR", wrong=wrong, steps=steps,
        tip=f"Left over: {m(f'{money(avail)} - {money(k * C)} = {money(left)}')}, not enough for one more.",
        check=max(j for j in range(0, 200) if j * C <= avail),
    )


# --------------------------------------------------------------------------
# 13. bulk vs single price
# --------------------------------------------------------------------------

_BULK = [
    # (product, unit, unit_pl, pkg, case sizes, single prices (cents), where, military)
    ("sports drinks cost", "bottle", "bottles", "case", [12, 24], [99, 119, 125, 129, 149],
     "At the base commissary", True),
    ("bottled water costs", "bottle", "bottles", "case", [24, 32], [50, 75, 89, 99], "At a grocery store", False),
    ("printer paper costs", "ream", "reams", "box", [5, 8, 10], [599, 649, 699, 799, 899],
     "At an office-supply store", False),
    ("motor oil costs", "quart", "quarts", "case", [6, 12], [699, 749, 799, 899, 999],
     "At the motor pool's parts supplier", True),
    ("energy bars cost", "bar", "bars", "box", [12, 18, 24], [129, 149, 175, 199, 225], "At a sporting-goods store", False),
    ("paper towels cost", "roll", "rolls", "pack", [6, 12], [149, 179, 199, 229, 249], "At a warehouse store", False),
]


@template("AR")
@_fill
def bulk_savings(rng, lvl, part=None):
    product, u_, upl, pkg, ks, singles, where, mil = rng.choice(_BULK)
    k = rng.choice(ks)
    s = rng.choice(singles)
    uc = rng.randint(s * 60 // 100, s * 90 // 100)      # price per unit inside the case, in cents
    S1, C = R(s, 100), R(uc * k, 100)
    if lvl == 2:
        sav = k * S1 - C
        stem = (f"{where}, {product} {money(S1)} per {u_}, or {money(C)} for a {pkg} of {k}. How much "
                f"is saved by buying a {pkg} of {k} instead of {k} single {upl}?")
        return Problem(
            stem=stem, answer=sav, fmt=money, section="AR",
            wrong=[(S1 - C / k, f"is the savings on one {u_}, not on the whole {pkg}"),
                   (k * S1, f"is the cost of {k} single {upl}, not the savings"),
                   (C / k, f"is the price per {u_} in the {pkg}")],
            steps=[f"Cost of {k} single {upl}: {m(f'{k} \\times {money(S1)} = {money(k * S1)}')}.",
                   f"Savings: {m(f'{money(k * S1)} - {money(C)} = {money(sav)}')}."],
            check=_hc((s - uc) * k))
    j = rng.choice([1, 2, 3])
    r = rng.randint(1, k - 1)
    N = j * k + r
    cost = j * C + r * S1
    need(cost < (j + 1) * C)
    buyer = (choose(rng, "A supply sergeant", "A unit's supply clerk") if mil
             else choose(rng, "A youth-league coach", "An office manager", "A camp director"))
    stem = (f"{where}, {product} {money(S1)} per {u_}, or {money(C)} for a {pkg} of {k}. "
            f"{buyer} needs {N} {upl}. The plan is to buy as many full {pkg}s as possible and the rest "
            f"as single {upl}. What is the total cost?")
    wrong = [(N * S1, f"buys every {u_} singly"),
             ((j + 1) * C, f"buys one more full {pkg} instead of {r} single {upl}"),
             (j * C, f"forgets the {r} single {upl}")]
    frac_cost = Q(N) * C / k
    if (frac_cost * 100).is_integer:
        wrong.append((frac_cost, f"pays for part of a {pkg} at the {pkg} price, but stores sell whole {pkg}s"))
    return Problem(
        stem=stem, answer=cost, fmt=money, section="AR", wrong=wrong,
        steps=[f"Full {pkg}s: {m(f'{N} \\div {k}')} is {j} with {r} left over, so buy {j} "
               f"{pkg}{'s' if j > 1 else ''} and {r} single {upl if r > 1 else u_}.",
               f"{_cap(pkg)}s: {m(f'{j} \\times {money(C)} = {money(j * C)}')}. Singles: "
               f"{m(f'{r} \\times {money(S1)} = {money(r * S1)}')}.",
               f"Total: {m(f'{money(j * C)} + {money(r * S1)} = {money(cost)}')}."],
        check=_hc(j * uc * k + r * s))


# --------------------------------------------------------------------------
# 14. hourly job vs salaried job (level 3)
# --------------------------------------------------------------------------

@template("AR")
@_fill
def hourly_vs_salary(rng, lvl, part=None):
    r = rng.choice([Q(16), Q(17), Q(18), Q(19), Q(20), Q(21), Q(22), Q(23), Q(24),
                    R(33, 2), R(37, 2), R(39, 2), R(41, 2), R(45, 2)])
    A = r * 2080
    # the salary works out to a whole number of quarters per hour more or less than Job A
    dh = rng.choice([R(1, 4), R(1, 2), R(3, 4), Q(1), R(5, 4), R(3, 2), Q(2)]) * rng.choice([1, -1])
    S = (r + dh) * 2080
    diff = abs(A - S)
    mil = rng.random() < 0.5 if part is None else bool(_pick(rng, [0, 1], part))
    if mil:
        T = _trooper(rng, ["Sergeant", "Specialist", "Corporal", "Staff Sergeant"])
        intro = (f"{T} is leaving the Army after four years and has two civilian job offers.")
    else:
        T = person(rng)
        intro = f"{T} has two job offers."
    stem = (intro + f" Job A pays {money(r)} per hour, and Job B pays a salary of {money(S)} a year. "
            f"At either job {T.he} would work 40 hours a week, 52 weeks a year. How much more per year "
            f"does the better-paying job pay?")
    better = "A" if A > S else "B"
    return Problem(
        stem=stem, answer=diff, fmt=money, section="AR",
        wrong=[(A, "is Job A's yearly pay, not the difference"),
               (abs(r * 40 * 48 - S), "assumes 4 weeks in every month (48 weeks), but a year has 52 weeks"),
               (abs(r * 2000 - S), "uses 2,000 hours a year instead of 2,080"),
               (abs(dh) * 40, "is the difference for one week, not for a year"),
               (abs(dh), "is the difference in pay per hour, not per year")],
        steps=[f"Hours in a year: {m('40 \\times 52 = 2{,}080')} hours.",
               f"Job A per year: {m(f'2{{,}}080 \\times {money(r)} = {money(A)}')}."
               + (f" (Think {m(f'2{{,}}080 \\times {int_raw(r.floor())} = {money(2080 * r.floor())}')} plus "
                  f"{m(f'2{{,}}080 \\times 0.50 = \\$1{{,}}040')}.)" if not r.is_integer else ""),
               f"Compare with Job B's {money(S)}: {m(f'{money(max(A, S))} - {money(min(A, S))} = {money(diff)}')}. "
               f"Job {better} pays {money(diff)} more."],
        check=abs(sum(r * 40 for _ in range(52)) - S),
    )


# --------------------------------------------------------------------------

PLAN = [
    # level 1 (12)
    *[(v, 1, 1) for v in _variants(change_due, 3)],
    *[(v, 1, 1) for v in _variants(sale_price, 3)],
    *[(v, 1, 1) for v in _variants(sales_tax, 2)],
    *[(v, 1, 1) for v in _variants(items_budget, 2)],
    *[(v, 1, 1) for v in _variants(budget_share, 2)],
    # level 2 (16)
    *[(v, 2, 1) for v in _variants(change_due, 2)],
    *[(v, 2, 1) for v in _variants(unit_price, 2)],
    (sales_tax, 2, 1),
    *[(v, 2, 1) for v in _variants(overtime, 2)],
    *[(v, 2, 1) for v in _variants(paycheck, 2)],
    *[(v, 2, 1) for v in _variants(split_bill, 2)],
    *[(v, 2, 1) for v in _variants(savings_weeks, 2)],
    (budget_share, 2, 1),
    (items_budget, 2, 1),
    (bulk_savings, 2, 1),
    # level 3 (12)
    *[(v, 3, 1) for v in _variants(discount_tax, 3)],
    *[(v, 3, 1) for v in _variants(overtime, 2)],
    *[(v, 3, 1) for v in _variants(best_buy, 2)],
    (budget_share, 3, 1),
    (paycheck, 3, 1),
    *[(v, 3, 1) for v in _variants(hourly_vs_salary, 2)],
    (bulk_savings, 3, 1),
]
