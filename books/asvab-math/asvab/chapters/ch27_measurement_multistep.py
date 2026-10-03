"""Chapter 27 - Measurement, Units & Multi-Step Problems (Part IV word problems)."""
import datetime
import functools
import math
from fractions import Fraction

import sympy as sp

from ..core import (R, Q, Problem, Reject, need, num, dec, money, unit, text, m,
                    dec_raw, int_raw, frac_raw, mixed_raw, person, template,
                    x as X)

NUM = 27
TITLE = r"Measurement, Units \& Multi-Step Problems"
PART = 4

INTRO = r"""
Many Arithmetic Reasoning questions are easy arithmetic wrapped in units:
feet and inches, quarts and gallons, a 24-hour clock. The rule that saves
you: \textbf{convert first, then calculate}, and write down each step.

\begin{concept}{US customary units (memorize these)}
\begin{tabular}{@{}lll@{}}
\textbf{Length} & \textbf{Capacity} & \textbf{Weight and time}\\
12 inches $=$ 1 foot & 8 fluid ounces $=$ 1 cup & 16 ounces $=$ 1 pound\\
3 feet $=$ 1 yard & 2 cups $=$ 1 pint & 2{,}000 pounds $=$ 1 ton\\
36 inches $=$ 1 yard & 2 pints $=$ 1 quart & 60 minutes $=$ 1 hour\\
5{,}280 feet $=$ 1 mile & 4 quarts $=$ 1 gallon & 7 days $=$ 1 week\\
\end{tabular}

\smallskip
Big unit $\to$ small unit: \textbf{multiply}. Small unit $\to$ big unit:
\textbf{divide}. (There are \emph{more} inches than feet, so the number gets bigger.)
\end{concept}

\begin{concept}{Metric units}
kilo $=$ 1{,}000 \quad centi $=$ $\frac{1}{100}$ \quad milli $=$ $\frac{1}{1{,}000}$.
So 1~km $=$ 1{,}000~m, 1~m $=$ 100~cm $=$ 1{,}000~mm, 1~kg $=$ 1{,}000~g,
1~L $=$ 1{,}000~mL. Converting is just moving the decimal point:
$2.5$~km $= 2{,}500$~m. US--metric factors (such as 1~mile $\approx$ 1.6~km)
are given in the problem.
\end{concept}

\begin{concept}{Military (24-hour) time and elapsed time}
Hours run from 0000 (midnight) to 2359. For p.m. times add 12 to the hour:
3:45 p.m. $=$ 1545. To find elapsed time, subtract hours and minutes
separately, and when you borrow an hour, it is worth \textbf{60} minutes,
not 100. Across midnight: time until 2400, plus time after 0000.
\end{concept}

\begin{example}{Worked example}
A convoy leaves at 0745 and arrives at 1420. How long is the trip?

\textbf{Solution.} 20 minutes minus 45 minutes won't go, so borrow 1 hour:
14:20 becomes 13 hours 80 minutes. Then $13 - 7 = 6$ hours and
$80 - 45 = 35$ minutes. The trip takes 6 hours 35 minutes.
\end{example}

\begin{tip}
Decide how to round from the question. ``How many trips (boxes, tents) are
\emph{needed}?'' rounds \emph{up}: 75 soldiers in 6-person tents need 13 tents.
``How many \emph{full} pieces (or items you can afford)?'' rounds \emph{down}.
\end{tip}

\begin{trap}
\begin{itemize}
\item Subtracting clock times like ordinary numbers: $1420 - 0745 = 675$ is not
  6 hours 75 minutes.
\item Fence posts: a 60-foot fence with posts every 6 feet needs
  $60 \div 6 + 1 = 11$ posts (one at each end). Cutting a board into 5 pieces
  takes only 4 cuts.
\item ``$\frac13$ of the \emph{remainder}'' is a fraction of what is left, not of
  the original amount.
\item Using the wrong conversion factor (3 feet in a yard, but 12 inches in a foot).
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# private helpers
# --------------------------------------------------------------------------

_RECENT: dict = {}
_FROZEN: list = []


def _fresh(rng, options, tag, keep=3):
    """rng.choice that avoids the last few picks for this tag, so a practice set does not
    tell the same story twice in a row (deterministic for a fixed call sequence).  Inside a
    @_retrying template the pick is frozen while the numbers are redrawn."""
    if _FROZEN and tag in _FROZEN[-1]:
        return _FROZEN[-1][tag]
    recent = _RECENT.setdefault(tag, [])
    pool = [o for o in options if o not in recent] or list(options)
    pick = rng.choice(pool)
    recent.append(pick)
    del recent[:-min(keep, len(options) - 1)]
    if _FROZEN:
        _FROZEN[-1][tag] = pick
    return pick


def _retrying(fn, tries=300):
    """Redraw numbers inside one call (same story) until the template accepts them."""
    @functools.wraps(fn)
    def wrapper(rng, lvl):
        _FROZEN.append({})
        try:
            for _ in range(tries):
                try:
                    return fn(rng, lvl)
                except Reject:
                    continue
            raise Reject(f"{fn.__name__}: no usable numbers")
        finally:
            _FROZEN.pop()
    return wrapper


_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
          "ten", "eleven", "twelve"]
_LAST = ["Ruiz", "Chen", "Walker", "Okafor", "Patel", "Novak", "Brooks", "Kim", "Santos",
         "Reyes", "Jensen", "Haddad", "Lopez", "Nguyen", "Carter", "Murphy"]


def _army(rng):
    return f"{rng.choice(['Private', 'Specialist', 'Corporal', 'Sergeant', 'Staff Sergeant'])} {rng.choice(_LAST)}"


def _tidy(t):
    """'... 4:50 p.m.. The' -> '... 4:50 p.m. The' (a.m./p.m. already end in a period)."""
    return t.replace("a.m..", "a.m.").replace("p.m..", "p.m.") if t else t


def _Prob(**kw):
    kw["stem"] = _tidy(kw["stem"])
    kw["steps"] = [_tidy(t) for t in kw["steps"]]
    if kw.get("tip"):
        kw["tip"] = _tidy(kw["tip"])
    return Problem(**kw)


def _pl(word, v, plural=None):
    return word if Q(v) == 1 else (plural or word + "s")


def _near(ans, step=None):
    """Plausible fillers around a numeric answer (no silly x10 values)."""
    A = Q(ans)

    def f(rng):
        st = step
        if st is None:
            if A.is_integer:
                st = next(s_ for lim, s_ in ((12, 1), (30, 2), (80, 5), (200, 10), (600, 25),
                                              (3000, 100), (10 ** 9, 1000)) if A <= lim)
            else:
                st = R(1, sp.Rational(A).q)
        out = [A + k * st for k in (1, 2, 3, -1, -2, -3)]
        out = [v for v in out if v > 0]
        rng.shuffle(out)
        return out
    return f


def _short(v, places=2):
    """True if v is a decimal with at most `places` places (keeps distractors readable)."""
    v = sp.Rational(Q(v))
    return (v * 10 ** places).is_integer


def _hm_text(mins):
    """Minutes -> '7 hours 45 minutes' (text with math digits)."""
    mins = Q(mins)
    need(mins.is_integer and mins > 0, "bad duration")
    h, mm = divmod(int(mins), 60)
    parts = []
    if h:
        parts.append(f"{m(int_raw(h))}~{_pl('hour', h)}")
    if mm:
        parts.append(f"{m(int_raw(mm))}~{_pl('minute', mm)}")
    return " ".join(parts)


def _dur(v):
    """Formatter: duration in minutes."""
    return _hm_text(v)


def _clock12_raw(v):
    """Minutes after midnight -> '7:45 a.m.' (text)."""
    v = Q(v)
    need(v.is_integer and 0 <= v < 1440, "bad clock time")
    h, mm = divmod(int(v), 60)
    suf = "a.m." if h < 12 else "p.m."
    h12 = h % 12 or 12
    return f"${h12}{{:}}{mm:02d}$~{suf}"


def _clock12(v):
    return _clock12_raw(v)


def _clock24_raw(v):
    v = Q(v)
    need(v.is_integer and 0 <= v < 1440, "bad clock time")
    h, mm = divmod(int(v), 60)
    return f"${h:02d}{mm:02d}$"


def _clock24(v):
    return _clock24_raw(v)


# --------------------------------------------------------------------------
# unit conversions
# --------------------------------------------------------------------------

_LEN = {
    # (from, to): factor (multiply when going big -> small)
    ("yard", "foot"): 3, ("foot", "inch"): 12, ("yard", "inch"): 36, ("mile", "foot"): 5280,
}
_LEN_PL = {"yard": "yards", "foot": "feet", "inch": "inches", "mile": "miles"}


def _lu(u, v):
    return u if Q(v) == 1 else _LEN_PL[u]


@template("AR")
@_retrying
def us_length(rng, lvl):
    if lvl >= 2:
        return _length_two_step(rng)
    key = _fresh(rng, ["fence", "plywood", "run", "rope", "field", "room", "range", "trail"], "len1")
    p = person(rng)
    if key == "fence":
        big, small, a = "yard", "foot", rng.randint(8, 120)
        stem = f"{p} buys a roll of fencing that is {num(a)} yards long. How many feet of fencing is that?"
        down = True
    elif key == "plywood":
        big, small, a = "foot", "inch", rng.randint(3, 24)
        stem = f"{p} needs a piece of trim {num(a)} feet long. How many inches long is the trim?"
        down = True
    elif key == "run":
        big, small = "mile", "foot"
        a = rng.choice([R(1, 2), 1, R(3, 2), 2, R(5, 2), 3, 4, 5])
        stem = (f"{_army(rng)}'s morning run is {m(mixed_raw(a))} {_lu('mile', a)}. How many feet "
                f"is that?")
        down = True
    elif key == "rope":
        big, small = "foot", "inch"
        a = 12 * rng.randint(2, 30)
        stem = f"{p} has a rope that is {num(a)} inches long. How long is the rope in feet?"
        down = False
    elif key == "field":
        big, small = "yard", "inch"
        a = rng.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 100])
        stem = f"{p} marks off a sprint course {num(a)} yards long. How many inches long is the course?"
        down = True
    elif key == "room":
        big, small = "yard", "foot"
        a = 3 * rng.randint(5, 30)
        stem = (f"A hallway in the office building where {p} works is {num(a)} feet long. How many "
                f"yards of carpet runner are needed to cover its length?")
        down = False
    elif key == "range":
        big, small = "yard", "foot"
        a = rng.choice(range(25, 501, 25))
        stem = (f"On a rifle range, a target is {num(a)} yards from the firing line. How many feet "
                f"away is the target?")
        down = True
    else:
        big, small = "mile", "foot"
        a = rng.choice([2640, 5280, 7920, 10560, 13200, 15840, 21120, 26400])
        stem = f"{p} hikes a trail that is {num(a)} feet long. How many miles long is the trail?"
        down = False
    f = _LEN[(big, small)]
    ans = Q(a) * f if down else Q(a) / f
    need(ans.is_integer or (ans * 2).is_integer)
    other = {3: 12, 12: 3, 36: 12, 5280: 1760}[f]
    other_why = (f"uses 1,760 (the number of yards in a mile) instead of 5,280" if f == 5280 else
                 f"uses {other} instead of {f} {_LEN_PL[small]} in a {big}")
    to, frm = (small, big) if down else (big, small)
    fmt = unit(dec, to, _LEN_PL[to])
    if down:
        wrong = [(Q(a) * other, other_why)]
        if _short(Q(a) / f):
            wrong.append((Q(a) / f, "divides instead of multiplying"))
        if f < 100:
            wrong.append((Q(a) + f, f"adds {f} instead of multiplying by it"))
        step = (f"1 {big} $=$ {num(f)} {_LEN_PL[small]}. Going from a big unit to a small unit, "
                f"multiply: {m(f'{mixed_raw(a)} \\times {int_raw(f)} = {int_raw(ans)}')} {_lu(small, ans)}.")
    else:
        wrong = [(Q(a) * f, "multiplies instead of dividing")]
        if _short(Q(a) / other):
            wrong.append((Q(a) / other, other_why))
        if f < 100:
            wrong.append((Q(a) - f, f"subtracts {f} instead of dividing by it"))
        step = (f"1 {big} $=$ {num(f)} {_LEN_PL[small]}. Going from a small unit to a big unit, "
                f"divide: {m(f'{int_raw(a)} \\div {int_raw(f)} = {dec_raw(ans)}')} {_lu(big, ans)}.")
    return _Prob(
        stem=stem, answer=ans, fmt=fmt, section="AR", wrong=wrong,
        steps=[step],
        tip=("Check the size: inches are smaller than feet, so there should be more of them."
             if small == "inch" and down else None),
        near=_near(ans),
        check=Fraction(int(sp.Rational(a).p) * (f if down else 1), int(sp.Rational(a).q) * (1 if down else f)),
    )


def _length_two_step(rng):
    key = _fresh(rng, ["boards", "fence_cost", "ribbon", "laps"], "len2")
    if key == "boards":
        k = rng.randint(4, 16)
        L = rng.choice([18, 24, 30, 32, 36, 40, 42, 45, 48, 54, 60])
        tot = k * L
        ans = R(tot, 12)
        need((ans * 2).is_integer)
        p = person(rng)
        stem = (f"{p} is building shelves and needs {_WORDS[k] if k <= 12 else num(k)} boards, each "
                f"{num(L)} inches long. How many feet of board does {p.he} need in all?")
        wrong = [
            (Q(tot), "gives the total in inches, not feet"),
            (R(tot, 36), "divides by 36, which changes inches to yards"),
            (R(L, 12), "gives the length of one board in feet"),
            (R(tot, 10), "divides by 10 instead of 12"),
        ]
        steps = [
            f"Total length in inches: {m(f'{k} \\times {L} = {int_raw(tot)}')} inches.",
            f"Change inches to feet (12 inches $=$ 1 foot): {m(f'{int_raw(tot)} \\div 12 = {dec_raw(ans)}')} feet.",
        ]
        return _Prob(stem=stem, answer=ans, fmt=unit(dec, "foot", "feet"), section="AR",
                       wrong=wrong, steps=steps, near=_near(ans, step=R(1, 2) if not ans.is_integer else None),
                       check=Fraction(k * L, 12))
    if key == "fence_cost":
        L = 3 * rng.randint(10, 80)
        price = rng.choice([2, 3, 4, 5, 6, 8, 9, 12, 15])
        yd = L // 3
        ans = Q(yd * price)
        what = rng.choice(["garden", "dog run", "storage yard on a base", "playground"])
        stem = (f"Fencing costs {money(price)} per yard. How much will it cost to buy fencing for "
                f"{num(L)} feet of a {what}?")
        wrong = [
            (Q(L * price), "forgets to change feet to yards"),
            (Q(yd), "gives the number of yards, not the cost"),
            (R(L * price, 12), "divides by 12 instead of 3"),
            (Q(L * price * 3), "multiplies by 3 instead of dividing"),
        ]
        steps = [
            f"Change feet to yards (3 feet $=$ 1 yard): {m(f'{int_raw(L)} \\div 3 = {yd}')} yards.",
            f"Multiply by the price per yard: {m(f'{yd} \\times {price} = {int_raw(ans)}')}, so {money(ans)}.",
        ]
        return _Prob(stem=stem, answer=ans, fmt=money, section="AR", wrong=wrong, steps=steps,
                       near=_near(ans), check=Fraction(L, 3) * price)
    if key == "ribbon":
        yd = rng.randint(2, 12)
        piece = rng.choice([4, 6, 9, 12, 18])
        tot = 36 * yd
        ans = R(tot, piece)
        need(ans.is_integer)
        stem = (f"A roll holds {num(yd)} yards of ribbon. How many pieces {num(piece)} inches long can "
                f"be cut from it?")
        wrong = [
            (R(yd * 12, piece), "uses 12 inches in a yard instead of 36"),
            (Q(tot), "gives the length in inches, not the number of pieces"),
            (R(yd * 3, piece) if (R(yd * 3, piece)).is_integer else Q(yd * piece), "forgets to change yards to inches"),
        ]
        steps = [
            f"Change yards to inches (36 inches $=$ 1 yard): {m(f'{yd} \\times 36 = {int_raw(tot)}')} inches.",
            f"Divide by the length of one piece: {m(f'{int_raw(tot)} \\div {piece} = {int_raw(ans)}')} pieces.",
        ]
        return _Prob(stem=stem, answer=ans, fmt=num, section="AR", wrong=wrong, steps=steps,
                       near=_near(ans), check=Fraction(36 * yd, piece))
    lap = rng.choice([440, 220, 880])
    miles = rng.choice([1, 2, 3])
    ans = Q(1760 * miles // lap)
    stem = (f"A running track on base is {num(lap)} yards around. How many laps must a soldier run "
            f"to cover {m(str(miles))} {_pl('mile', miles)}? (1 mile $=$ 1{{,}}760 yards)")
    wrong = [
        (R(5280 * miles, lap), "uses feet in a mile with a track measured in yards"),
        (Q(1760 * miles), "gives the distance in yards, not the number of laps"),
        (R(1000 * miles, lap) if (R(1000 * miles, lap) * 2).is_integer else ans + 2, None),
    ]
    steps = [
        f"Distance in yards: {m(f'{miles} \\times 1{{,}}760 = {int_raw(1760 * miles)}')} yards.",
        f"Divide by one lap: {m(f'{int_raw(1760 * miles)} \\div {lap} = {int_raw(ans)}')} laps.",
    ]
    return _Prob(stem=stem, answer=ans, fmt=num, section="AR", wrong=wrong, steps=steps,
                   near=_near(ans), check=Fraction(1760 * miles, lap))


_CAP = {
    # unit: size in fluid ounces (capacity) or ounces (weight)
    "gallon": 128, "quart": 32, "pint": 16, "cup": 8, "fluid ounce": 1,
    "ton": 32000, "pound": 16, "ounce": 1,
}
_CAP_PL = {"gallon": "gallons", "quart": "quarts", "pint": "pints", "cup": "cups",
           "fluid ounce": "fluid ounces", "ton": "tons", "pound": "pounds", "ounce": "ounces"}


def _cu(u, v):
    return u if Q(v) == 1 else _CAP_PL[u]


@template("AR")
@_retrying
def capacity_weight(rng, lvl):
    if lvl >= 2:
        return _capacity_two_step(rng)
    key = _fresh(rng, ["broth", "jug", "milk", "flour", "truck", "package", "punch", "canteen"], "cap1")
    p = person(rng)
    if key == "broth":
        big, small, a = "quart", "cup", rng.randint(2, 16)
        stem = f"{p}'s soup recipe calls for {num(a)} quarts of broth. How many cups of broth is that?"
    elif key == "jug":
        big, small, a = "gallon", "quart", rng.randint(2, 25)
        stem = f"{p} fills a water jug that holds {num(a)} gallons. How many quarts does the jug hold?"
    elif key == "milk":
        big, small, a = "gallon", "pint", rng.randint(2, 40)
        stem = (f"The dining facility on a base uses {num(a)} gallons of milk at breakfast. How many "
                f"pints is that?")
    elif key == "flour":
        big, small, a = "pound", "ounce", rng.randint(2, 25)
        stem = f"{p} buys a bag of flour that weighs {num(a)} pounds. How many ounces does it weigh?"
    elif key == "truck":
        big, small = "ton", "pound"
        a = rng.choice([R(1, 2), R(3, 4), 1, R(5, 4), R(3, 2), 2, R(5, 2), 3, 5])
        stem = (f"A military truck is rated to carry {m(mixed_raw(a))} {_cu('ton', a)} of cargo. "
                f"How many pounds is that?")
    elif key == "package":
        big, small = "pound", "ounce"
        a = 8 * rng.randint(3, 30)
        stem = f"{p} mails a package that weighs {num(a)} ounces. How many pounds does it weigh?"
    elif key == "punch":
        big, small = "gallon", "cup"
        a = 8 * rng.randint(2, 16)
        stem = f"{p}'s party punch recipe makes {num(a)} cups. How many gallons of punch is that?"
    else:
        big, small = "quart", "pint"
        a = 2 * rng.randint(3, 30)
        stem = (f"A squad fills {num(a)} one-pint water bottles. How many quarts of water do they "
                f"use?")
    down = key not in ("package", "punch", "canteen")
    f = _CAP[big] // _CAP[small] if big != "ton" else 2000
    ans = Q(a) * f if down else Q(a) / f
    need(ans.is_integer or (ans * 2).is_integer)
    to = small if down else big
    fmt = unit(dec, to, _CAP_PL[to])
    wrong_factor = {("quart", "cup"): 2, ("gallon", "quart"): 2, ("gallon", "pint"): 4,
                    ("pound", "ounce"): 12, ("ton", "pound"): 1000, ("gallon", "cup"): 8,
                    ("quart", "pint"): 4}[(big, small)]
    facts = {("quart", "cup"): "1 quart $=$ 2 pints $=$ 4 cups",
             ("gallon", "quart"): "1 gallon $=$ 4 quarts",
             ("gallon", "pint"): "1 gallon $=$ 4 quarts $=$ 8 pints",
             ("pound", "ounce"): "1 pound $=$ 16 ounces",
             ("ton", "pound"): "1 ton $=$ 2{,}000 pounds",
             ("gallon", "cup"): "1 gallon $=$ 4 quarts $=$ 16 cups",
             ("quart", "pint"): "1 quart $=$ 2 pints"}[(big, small)]
    if down:
        wrong = [
            (Q(a) * wrong_factor, f"uses {wrong_factor} {_CAP_PL[small]} in a {big} instead of {f}"),
            (Q(a) + f, f"adds {f} instead of multiplying by it"),
        ]
        if _short(Q(a) / f):
            wrong.append((Q(a) / f, "divides instead of multiplying"))
        step = (f"{facts}. From a big unit to a small unit, multiply: "
                f"{m(f'{mixed_raw(a)} \\times {int_raw(f)} = {dec_raw(ans)}')} {_cu(small, ans)}.")
    else:
        wrong = [
            (Q(a) * f, "multiplies instead of dividing"),
            (Q(a) - f, f"subtracts {f} instead of dividing by it"),
        ]
        if _short(Q(a) / wrong_factor):
            wrong.append((Q(a) / wrong_factor, f"uses {wrong_factor} {_CAP_PL[small]} in a {big} instead of {f}"))
        step = (f"{facts}. From a small unit to a big unit, divide: "
                f"{m(f'{int_raw(a)} \\div {int_raw(f)} = {dec_raw(ans)}')} {_cu(big, ans)}.")
    return _Prob(stem=stem, answer=ans, fmt=fmt, section="AR", wrong=wrong, steps=[step],
                   near=_near(ans), check=Fraction(int(sp.Rational(a).p), int(sp.Rational(a).q)) * (f if down else Fraction(1, f)))


def _capacity_two_step(rng):
    key = _fresh(rng, ["canteens", "cooler", "patties", "crates", "buffalo"], "cap2")
    if key == "canteens":
        g = rng.randint(2, 12)
        c = rng.choice([5, 5, 3, 2])
        stem = (f"{_army(rng)}'s squad has {_WORDS[g]} full {c}-gallon water cans. Each canteen holds "
                f"1 quart. How many canteens can the squad fill?")
        ans = Q(g * c * 4)
        wrong = [
            (Q(g * c), "forgets to change gallons to quarts"),
            (Q(g * c * 2), "uses 2 quarts in a gallon instead of 4"),
            (Q(g * 4), f"leaves out the {c} gallons in each can"),
            (Q(g * c * 8), "changes gallons to pints instead of quarts"),
        ]
        steps = [f"Total water: {m(f'{g} \\times {c} = {g * c}')} gallons.",
                 f"1 gallon $=$ 4 quarts: {m(f'{g * c} \\times 4 = {int_raw(ans)}')} quarts, so "
                 f"{num(ans)} canteens."]
        check = Fraction(g * c * 128, 32)
    elif key == "buffalo":
        g = rng.choice(range(100, 501, 25))
        stem = (f"A water trailer at {_army(rng)}'s field site holds {num(g)} gallons. How many "
                f"1-quart canteens can be filled from a full trailer?")
        ans = Q(4 * g)
        wrong = [
            (Q(2 * g), "uses 2 quarts in a gallon instead of 4"),
            (Q(8 * g), "changes gallons to pints instead of quarts"),
            (Q(g), "forgets to convert gallons to quarts"),
            (R(g, 4), "divides by 4 instead of multiplying"),
        ]
        steps = [f"1 gallon $=$ 4 quarts, so the trailer holds "
                 f"{m(f'{int_raw(g)} \\times 4 = {int_raw(ans)}')} quarts.",
                 f"Each canteen takes 1 quart, so {num(ans)} canteens can be filled."]
        check = Fraction(g * 128, 32)
    elif key == "cooler":
        g = rng.randint(2, 12)
        cup = rng.choice([8, 16, 4])
        p = person(rng)
        stem = (f"{p} fills a cooler with {num(g)} gallons of sports drink for a team. How many "
                f"{num(cup)}-ounce cups can be filled from it? (1 gallon $=$ 128 fluid ounces)")
        ans = R(128 * g, cup)
        wrong = [
            (R(32 * g, cup), "uses 32 ounces in a gallon (that is a quart)"),
            (Q(128 * g), "gives the number of ounces, not the number of cups"),
            (R(128, cup), "finds the cups in only one gallon"),
            (R(128 * g, cup) * 2, None),
        ]
        steps = [f"Change gallons to ounces: {m(f'{g} \\times 128 = {int_raw(128 * g)}')} fluid ounces.",
                 f"Divide by the size of a cup: {m(f'{int_raw(128 * g)} \\div {cup} = {int_raw(ans)}')} cups."]
        check = Fraction(128 * g, cup)
    elif key == "patties":
        w = rng.randint(3, 40)
        oz = rng.choice([4, 8, 6])
        need((16 * w) % oz == 0)
        stem = (f"{_army(rng)}, a cook at the dining facility, makes hamburger patties that weigh "
                f"{num(oz)} ounces each. How many patties can be made from {num(w)} pounds of ground beef?")
        ans = R(16 * w, oz)
        wrong = [
            (R(w, oz) if (R(w, oz) * 4).is_integer else R(10 * w, oz), "forgets to change pounds to ounces"),
            (R(12 * w, oz), "uses 12 ounces in a pound instead of 16"),
            (Q(16 * w), "gives the number of ounces, not the number of patties"),
            (Q(w * oz), "multiplies the pounds by the patty size"),
        ]
        steps = [f"Change pounds to ounces (16 ounces $=$ 1 pound): {m(f'{w} \\times 16 = {16 * w}')} ounces.",
                 f"Divide by the weight of one patty: {m(f'{16 * w} \\div {oz} = {int_raw(ans)}')} patties."]
        check = Fraction(16 * w, oz)
    else:
        t = Q(rng.choice([R(1, 2), R(3, 4), 1, R(5, 4), R(3, 2), 2, R(5, 2), 3, 4, 5]))
        c = rng.choice([40, 50, 60, 75, 80, 100, 125, 150, 200, 250])
        lb = t * 2000
        ans = lb / c
        need(ans.is_integer)
        stem = (f"A truck can carry {m(mixed_raw(t))} {_cu('ton', t)} of cargo. Each crate of "
                f"{rng.choice(['supplies', 'tools', 'rations', 'spare parts'])} weighs {num(c)} pounds. "
                f"What is the greatest number of crates the truck can carry?")
        wrong = [
            (t * 1000 / c, "uses 1,000 pounds in a ton instead of 2,000"),
            (lb, "gives the weight limit in pounds, not the number of crates"),
            (lb / c * 2, None),
            (lb / c / 2 if (lb / c / 2).is_integer else lb / c + 4, None),
        ]
        steps = [f"Change tons to pounds (1 ton $=$ 2{{,}}000 pounds): "
                 f"{m(f'{mixed_raw(t)} \\times 2{{,}}000 = {int_raw(lb)}')} pounds.",
                 f"Divide by the weight of one crate: {m(f'{int_raw(lb)} \\div {c} = {int_raw(ans)}')} crates."]
        check = Fraction(int(t * 4) * 500, c)
    return _Prob(stem=stem, answer=ans, fmt=num, section="AR", wrong=wrong, steps=steps,
                   near=_near(ans), check=check)


_METRIC = {
    # (big, small): factor
    ("kilometer", "meter"): 1000, ("meter", "centimeter"): 100, ("centimeter", "millimeter"): 10,
    ("meter", "millimeter"): 1000, ("kilogram", "gram"): 1000, ("liter", "milliliter"): 1000,
}


@template("AR")
@_retrying
def metric_convert(rng, lvl):
    if lvl >= 2:
        return _metric_two_step(rng)
    key = _fresh(rng, ["race", "patrol", "ruck", "bottle", "board", "bolt", "canteen", "flour"], "met1")
    if key == "race":
        big, small, down = "kilometer", "meter", True
        a = rng.choice([R(5), R(10), R(3, 2), R(5, 2), R(21, 2), R(15, 2)])
        stem = f"A charity race is {m(dec_raw(a))} kilometers long. How many meters is that?"
    elif key == "patrol":
        big, small, down = "kilometer", "meter", True
        a = R(rng.randint(12, 95), 10)
        stem = f"A foot patrol covers {m(dec_raw(a))} kilometers. How many meters is that?"
    elif key == "ruck":
        big, small, down = "kilogram", "gram", False
        a = rng.choice(range(1500, 30001, 500))
        stem = f"A soldier's rucksack weighs {num(a)} grams. How many kilograms is that?"
    elif key == "bottle":
        big, small, down = "liter", "milliliter", True
        a = rng.choice([R(1, 2), R(3, 4), R(1, 4), R(3, 2), R(2), R(5, 2)])
        stem = f"A bottle of water holds {m(dec_raw(a))} liters. How many milliliters is that?"
    elif key == "board":
        big, small, down = "meter", "centimeter", False
        a = rng.randint(120, 480)
        stem = f"A board is {num(a)} centimeters long. How many meters long is it?"
    elif key == "bolt":
        big, small, down = "centimeter", "millimeter", False
        a = rng.randint(15, 95)
        stem = f"A bolt is {num(a)} millimeters long. How many centimeters long is it?"
    elif key == "canteen":
        big, small, down = "liter", "milliliter", False
        a = rng.choice(range(250, 4001, 250))
        stem = f"A hydration pack holds {num(a)} milliliters of water. How many liters is that?"
    else:
        big, small, down = "kilogram", "gram", True
        a = R(rng.randint(5, 50), 10)
        stem = f"A bag of flour has a mass of {m(dec_raw(a))} kilograms. How many grams is that?"
    f = _METRIC[(big, small)]
    a = Q(a)
    ans = a * f if down else a / f
    wf = {1000: 100, 100: 1000, 10: 100}[f]
    to = small if down else big
    fmt = unit(dec, to)
    if down:
        wrong = [
            (a * wf, f"uses {num(wf)} instead of {num(f)}"),
            (a / f, "divides instead of multiplying"),
            (a * f * 10, "moves the decimal point one place too far"),
        ]
        step = (f"1 {big} $=$ {num(f)} {small}s. Multiply by {num(f)} (move the decimal point "
                f"{len(str(f)) - 1} {_pl('place', len(str(f)) - 1)} to the right): {m(f'{dec_raw(a)} \\times {int_raw(f)} = {dec_raw(ans)}')} {_pl(small, ans)}.")
    else:
        wrong = [
            (a / wf, f"uses {num(wf)} instead of {num(f)}"),
            (a * f, "multiplies instead of dividing"),
            (a / f / 10, "moves the decimal point one place too far"),
        ]
        step = (f"1 {big} $=$ {num(f)} {small}s. Divide by {num(f)} (move the decimal point "
                f"{len(str(f)) - 1} {_pl('place', len(str(f)) - 1)} to the left): {m(f'{int_raw(a)} \\div {int_raw(f)} = {dec_raw(ans)}')} {_pl(big, ans)}.")
    return _Prob(stem=stem, answer=ans, fmt=fmt, section="AR", wrong=wrong, steps=[step],
                   near=_near(ans, step=R(1, 10) if not ans.is_integer else None),
                   check=Fraction(int(a.p), int(a.q)) * (f if down else Fraction(1, f)))


def _metric_two_step(rng):
    key = _fresh(rng, ["saline", "wire", "rice", "laps", "sugar"], "met2")
    if key == "saline":
        L = rng.choice([1, 2, 3, 4, R(1, 2), R(3, 2), R(5, 2), R(3, 4)])
        dose = rng.choice([50, 100, 125, 150, 200, 250, 500])
        tot = Q(L) * 1000
        ans = tot / dose
        need(ans.is_integer and ans > 1)
        s_ = _army(rng)
        stem = (f"{s_}, a medic, has {m(dec_raw(L))} {_pl('liter', L)} of saline solution. Each dose is "
                f"{num(dose)} milliliters. How many doses can {s_.split()[-1]} give?")
        wrong = [(Q(L) * 100 / dose if (Q(L) * 100 / dose).is_integer else ans * 10, "uses 100 milliliters in a liter instead of 1,000"),
                 (tot, "gives the number of milliliters, not doses"),
                 (ans * 10, "moves the decimal point one place too far")]
        steps = [f"Change liters to milliliters: {m(f'{dec_raw(L)} \\times 1{{,}}000 = {int_raw(tot)}')} milliliters.",
                 f"Divide by one dose: {m(f'{int_raw(tot)} \\div {dose} = {int_raw(ans)}')} doses."]
        check = Fraction(int(Q(L).p) * 1000, int(Q(L).q) * dose)
    elif key == "wire":
        L = rng.randint(3, 80)
        piece = rng.choice([20, 25, 40, 50, 60, 75, 80])
        tot = 100 * L
        ans = R(tot, piece)
        need(ans.is_integer)
        stem = (f"{person(rng)} has a roll of wire {num(L)} meters long. How many pieces "
                f"{num(piece)} centimeters long can be cut from it?")
        wrong = [(R(1000 * L, piece) if (R(1000 * L, piece)).is_integer else ans * 10, "uses 1,000 centimeters in a meter instead of 100"),
                 (Q(tot), "gives the length in centimeters, not the number of pieces"),
                 (ans / 10 if (ans / 10).is_integer else ans + 5, None)]
        steps = [f"Change meters to centimeters: {m(f'{L} \\times 100 = {int_raw(tot)}')} centimeters.",
                 f"Divide by one piece: {m(f'{int_raw(tot)} \\div {piece} = {int_raw(ans)}')} pieces."]
        check = Fraction(L * 100, piece)
    elif key == "rice":
        kg = rng.choice([1, 2, 3, 4, 5, 10, R(3, 2), R(5, 2)])
        g = rng.choice([50, 75, 80, 100, 125, 150, 200, 250])
        tot = Q(kg) * 1000
        ans = tot / g
        need(ans.is_integer)
        stem = (f"{person(rng)} divides a {m(dec_raw(kg))}-kilogram bag of rice into servings of "
                f"{num(g)} grams. How many servings does the bag hold?")
        wrong = [(Q(kg) * 100 / g if (Q(kg) * 100 / g).is_integer else ans / 10 if (ans / 10).is_integer else ans + 10,
                  "uses 100 grams in a kilogram instead of 1,000"),
                 (tot, "gives the number of grams, not servings"),
                 (ans * 10, "moves the decimal point one place too far")]
        steps = [f"Change kilograms to grams: {m(f'{dec_raw(kg)} \\times 1{{,}}000 = {int_raw(tot)}')} grams.",
                 f"Divide by one serving: {m(f'{int_raw(tot)} \\div {g} = {int_raw(ans)}')} servings."]
        check = Fraction(int(Q(kg).p) * 1000, int(Q(kg).q) * g)
    elif key == "laps":
        km = rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
        lap = rng.choice([200, 250, 400, 500])
        tot = 1000 * km
        ans = R(tot, lap)
        need(ans.is_integer)
        pp = person(rng)
        stem = (f"A track is {num(lap)} meters around. How many laps does {pp} need to run to "
                f"complete {m(str(km))} kilometers?")
        wrong = [(R(100 * km, lap) if (R(100 * km, lap) * 2).is_integer else ans * 10, "uses 100 meters in a kilometer instead of 1,000"),
                 (Q(tot), "gives the distance in meters, not the number of laps"),
                 (ans * 10, "moves the decimal point one place too far")]
        steps = [f"Change kilometers to meters: {m(f'{km} \\times 1{{,}}000 = {int_raw(tot)}')} meters.",
                 f"Divide by one lap: {m(f'{int_raw(tot)} \\div {lap} = {int_raw(ans)}')} laps."]
        check = Fraction(km * 1000, lap)
    else:
        kg = rng.choice([1, 2, R(3, 2), R(5, 2), R(6, 5), R(12, 5)])
        g = rng.choice([100, 150, 200, 250, 300, 400])
        tot = Q(kg) * 1000
        ans = tot / g
        need(ans.is_integer and ans > 2)
        stem = (f"{person(rng)}'s cookie recipe uses {num(g)} grams of sugar per batch. How many "
                f"batches can be made with a {m(dec_raw(kg))}-kilogram bag of sugar?")
        wrong = [(tot, "gives the number of grams, not batches"),
                 (ans * 10, "moves the decimal point one place too far"),
                 (Q(kg) * 100 / g if (Q(kg) * 100 / g * 10).is_integer else ans + 3, "uses 100 grams in a kilogram instead of 1,000")]
        steps = [f"Change kilograms to grams: {m(f'{dec_raw(kg)} \\times 1{{,}}000 = {int_raw(tot)}')} grams.",
                 f"Divide by one batch: {m(f'{int_raw(tot)} \\div {g} = {int_raw(ans)}')} batches."]
        check = Fraction(int(Q(kg).p) * 1000, int(Q(kg).q) * g)
    return _Prob(stem=stem, answer=Q(ans), fmt=dec, section="AR", wrong=wrong, steps=steps,
                   near=_near(ans), verify=lambda v: Q(v).is_integer and Q(v) > 0,
                   check=check)


@template("AR")
@_retrying
def us_metric(rng, lvl):
    key = _fresh(rng, ["km_mi", "mi_km", "kg_lb", "lb_kg", "in_cm", "gal_l", "speed"], "usm")
    if key == "km_mi":
        km = rng.choice([4, 8, 12, 16, 20, 24, 32, 40, 48, 10])
        ans = R(km * 10, 16)
        what = rng.choice([("A convoy route on a military map is", "long"),
                           ("A cross-country race is", "long"),
                           ("A road march covers", "")])
        stem = (f"{what[0]} {num(km)} kilometers{(' ' + what[1]) if what[1] else ''}. About how many "
                f"miles is that? (1 mile $\\approx$ 1.6 kilometers)")
        fmt = unit(dec, "mile")
        wrong = [(Q(km) * R(16, 10), "multiplies by 1.6 instead of dividing"),
                 ]
        steps = [f"A mile is longer than a kilometer, so there are fewer miles. Divide by 1.6: "
                 f"{m(f'{km} \\div 1.6')}.",
                 f"Clear the decimal: {m(f'{km * 10} \\div 16 = {dec_raw(ans)}')} miles."]
        check = Fraction(km * 10, 16)
    elif key == "mi_km":
        mi = rng.choice([3, 5, 10, 15, 20, 25, 30, 50, 6, 12])
        ans = Q(mi) * R(16, 10)
        stem = (f"A truck's trip odometer shows {num(mi)} miles. About how many kilometers is that? "
                f"(1 mile $\\approx$ 1.6 kilometers)")
        fmt = unit(dec, "kilometer")
        wrong = [(R(mi * 10, 16), "divides by 1.6 instead of multiplying"),
                 (Q(mi) + R(16, 10), "adds 1.6 instead of multiplying"),
                 ]
        steps = [f"Each mile is about 1.6 kilometers, so multiply: "
                 f"{m(f'{mi} \\times 1.6 = {dec_raw(ans)}')} kilometers."]
        check = Fraction(mi * 16, 10)
    elif key == "kg_lb":
        kg = rng.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
        ans = Q(kg) * R(22, 10)
        thing = rng.choice(["rucksack", "box of ammunition", "bag of cement", "duffel bag"])
        stem = (f"A {thing} has a mass of {num(kg)} kilograms. About how many pounds does it weigh? "
                f"(1 kilogram $\\approx$ 2.2 pounds)")
        fmt = unit(dec, "pound")
        wrong = [(R(kg * 10, 22), "divides by 2.2 instead of multiplying"),
                 (Q(kg) + R(22, 10), "adds 2.2 instead of multiplying")]
        steps = [f"Each kilogram is about 2.2 pounds, so multiply: "
                 f"{m(f'{kg} \\times 2.2 = {dec_raw(ans)}')} pounds."]
        check = Fraction(kg * 22, 10)
    elif key == "lb_kg":
        lb = 11 * rng.randint(4, 20)
        ans = R(lb * 10, 22)
        p = person(rng)
        stem = (f"{p}'s luggage weighs {num(lb)} pounds. About how many kilograms is that? "
                f"(1 kilogram $\\approx$ 2.2 pounds)")
        fmt = unit(dec, "kilogram")
        wrong = [(Q(lb) * R(22, 10), "multiplies by 2.2 instead of dividing"),
                 (Q(lb) - R(22, 10), "subtracts 2.2 instead of dividing")]
        steps = [f"A kilogram is heavier than a pound, so there are fewer kilograms. Divide by 2.2: "
                 f"{m(f'{lb} \\div 2.2 = {lb * 10} \\div 22 = {dec_raw(ans)}')} kilograms."]
        check = Fraction(lb * 10, 22)
    elif key == "in_cm":
        inch = rng.choice([2, 4, 5, 6, 8, 10, 12, 20, 24, 30])
        ans = Q(inch) * R(254, 100)
        thing = rng.choice(["picture frame", "board", "laptop screen", "pipe"])
        stem = (f"A {thing} is {num(inch)} inches long. How many centimeters is that? "
                f"(1 inch $=$ 2.54 centimeters)")
        fmt = unit(dec, "centimeter")
        wrong = [(Q(inch) + R(254, 100), "adds 2.54 instead of multiplying")]
        if _short(R(inch * 100, 254)):
            wrong.append((R(inch * 100, 254), "divides by 2.54 instead of multiplying"))
        steps = [f"Each inch is 2.54 centimeters, so multiply: "
                 f"{m(f'{inch} \\times 2.54 = {dec_raw(ans)}')} centimeters."]
        check = Fraction(inch * 254, 100)
    elif key == "gal_l":
        thing, gal = rng.choice([("The fuel tank of a Humvee", 25), ("A water can", 5),
                                 ("A car's gas tank", rng.choice([10, 12, 14, 15, 16, 18, 20])),
                                 ("A fuel drum", 55), ("A pickup truck's gas tank", rng.choice([20, 24, 26, 30])),
                                 ("A rain barrel", rng.choice([40, 50, 60]))])
        ans = Q(gal) * R(38, 10)
        stem = (f"{thing} holds {num(gal)} gallons. About how many liters is that? "
                f"(1 gallon $\\approx$ 3.8 liters)")
        fmt = unit(dec, "liter")
        wrong = [(Q(gal) + R(38, 10), "adds 3.8 instead of multiplying")]
        if _short(R(gal * 10, 38)):
            wrong.append((R(gal * 10, 38), "divides by 3.8 instead of multiplying"))
        steps = [f"Each gallon is about 3.8 liters, so multiply: "
                 f"{m(f'{gal} \\times 3.8 = {dec_raw(ans)}')} liters."]
        check = Fraction(gal * 38, 10)
    else:
        kmh = rng.choice([40, 48, 56, 64, 72, 80, 88, 96, 100, 120])
        ans = R(kmh * 10, 16)
        stem = (f"The speed limit on a road overseas is {num(kmh)} kilometers per hour. About how "
                f"many miles per hour is that? (1 mile $\\approx$ 1.6 kilometers)")
        fmt = unit(dec, "mile per hour", "miles per hour")
        wrong = [(Q(kmh) * R(16, 10), "multiplies by 1.6 instead of dividing"),
                 ]
        steps = [f"Fewer miles than kilometers, so divide by 1.6: "
                 f"{m(f'{kmh} \\div 1.6 = {kmh * 10} \\div 16 = {dec_raw(ans)}')} miles per hour."]
        check = Fraction(kmh * 10, 16)
    need((ans * 100).is_integer)
    # error-based decimal slips; fillers stay far from the answer ("about" questions)
    wrong.append((ans * 10, "moves the decimal point one place too far to the right"))
    if _short(ans / 10):
        wrong.append((ans / 10, "moves the decimal point one place too far to the left"))
    wrong = [w for w in wrong if _short(w[0]) and Q(w[0]) > 0]

    def far(rng_):
        out = [v for v in (ans * 2, ans / 2, ans * R(3, 2), ans * R(2, 3)) if _short(v)]
        rng_.shuffle(out)
        return out
    return _Prob(stem=stem, answer=ans, fmt=fmt, section="AR", wrong=wrong, steps=steps,
                 near=far, check=check)


# --------------------------------------------------------------------------
# time
# --------------------------------------------------------------------------

def _borrow_trap(start, end):
    """Elapsed time when clock times are subtracted like ordinary numbers (borrow 100)."""
    hs, ms = divmod(start, 60)
    he, me = divmod(end, 60)
    diff = (he * 100 + me) - (hs * 100 + ms)
    h, mm = divmod(diff, 100)
    return 60 * h + mm   # e.g. 675 -> 6 h 75 min -> 7 h 15 min


def _borrow_why(start, end, civilian=False):
    """Exact description of the 'subtract clock times like ordinary numbers' slip."""
    hs, ms = divmod(start, 60)
    he, me = divmod(end, 60)
    a_, b_ = f"{hs:02d}{ms:02d}", f"{he:02d}{me:02d}"
    diff = (he * 100 + me) - (hs * 100 + ms)
    h, mm = divmod(diff, 100)
    head = (f"writes the times as {m(a_)} and {m(b_)} and subtracts them like ordinary numbers"
            if civilian else f"subtracts {m(b_)} $-$ {m(a_)} like ordinary numbers")
    read = f"reads {m(str(diff))} as {h} hours {mm} minutes"
    if mm >= 60:
        read += f", which it rewrites as {h + 1} hours {mm - 60} minutes"
    return f"{head} and {read}"


@template("AR")
@_retrying
def elapsed_time(rng, lvl):
    kind = _fresh(rng, ["elapsed", "end"], "el_kind", keep=1)
    if kind == "elapsed":
        key = _fresh(rng, ["shift", "flight", "drive", "game", "class"], "el")
        lo, hi = {"shift": (6 * 60, 10 * 60), "flight": (6 * 60, 14 * 60), "drive": (7 * 60, 13 * 60),
                  "game": (11 * 60, 18 * 60), "class": (8 * 60, 12 * 60)}[key]
        start = rng.randrange(lo, hi, 5)
        dur = rng.randrange(75, 9 * 60, 5) if key in ("shift", "drive", "flight") else rng.randrange(75, 4 * 60, 5)
        end = start + dur
        need(end < 22 * 60 and start % 60 > end % 60 and start < 12 * 60 <= end)
        p = person(rng)
        stem = {
            "shift": f"{p}'s work shift starts at {_clock12_raw(start)} and ends at {_clock12_raw(end)}. How long is the shift?",
            "flight": f"A flight leaves at {_clock12_raw(start)} and lands at {_clock12_raw(end)} (same time zone). How long is the flight?",
            "drive": f"{p} starts driving to visit family at {_clock12_raw(start)} and arrives at {_clock12_raw(end)}. How long is the drive?",
            "game": f"A baseball doubleheader starts at {_clock12_raw(start)} and ends at {_clock12_raw(end)}. How long does it last?",
            "class": f"A weekend first-aid class runs from {_clock12_raw(start)} to {_clock12_raw(end)}. How long is the class?",
        }[key]
        noon = 12 * 60
        before, after = noon - start, end - noon
        trap_noon = abs((end % 720) - start)   # treats 4:15 as if it came before 7:45
        wrong = [
            (Q(_borrow_trap(start, end)), _borrow_why(start, end, civilian=True)),
            (Q(trap_noon), "forgets that the clock starts over at 12 noon"),
            (Q(60 * (end // 60 - start // 60)), "counts only the change in the hour"),
        ]
        steps = [
            f"From {_clock12_raw(start)} to 12 noon is {_hm_text(before)}.",
            f"From 12 noon to {_clock12_raw(end)} is {_hm_text(after) if after else 'no time'}.",
            f"Add: {_hm_text(before)} $+$ {_hm_text(after)} $=$ {_hm_text(dur)}"
            + (f" (since {m(f'{(before % 60) + (after % 60)}')} minutes $=$ 1~hour {m(str((before % 60) + (after % 60) - 60))}~minutes)." if (before % 60) + (after % 60) >= 60 else "."),
        ]
        return _Prob(stem=stem, answer=Q(dur), fmt=_dur, section="AR", wrong=wrong, steps=steps,
                       near=_near(dur, step=15),
                       check=Q((datetime.datetime(2026, 1, 1, end // 60, end % 60)
                                - datetime.datetime(2026, 1, 1, start // 60, start % 60)).seconds // 60))
    key = _fresh(rng, ["movie", "bake", "hike", "meeting"], "end")
    (slo, shi), (dlo, dhi) = {"movie": ((13 * 60, 21 * 60 + 30), (90, 195)),
                              "bake": ((8 * 60, 14 * 60), (150, 330)),
                              "hike": ((6 * 60, 12 * 60), (90, 360)),
                              "meeting": ((8 * 60, 15 * 60), (65, 200))}[key]
    start = rng.randrange(slo, shi, 5)
    dur = rng.randrange(dlo, dhi, 5)
    end = start + dur
    need(end < 24 * 60 and (start % 60) + (dur % 60) >= 60)
    p = person(rng)
    stem = {
        "movie": f"A movie starts at {_clock12_raw(start)} and runs {_hm_text(dur)}. At what time does it end?",
        "bake": f"{p} puts a turkey in the oven at {_clock12_raw(start)}. It needs to cook for {_hm_text(dur)}. At what time will it be done?",
        "hike": f"{p} starts a hike at {_clock12_raw(start)} and hikes for {_hm_text(dur)}. At what time does {p.he} finish?",
        "meeting": f"A training meeting begins at {_clock12_raw(start)} and lasts {_hm_text(dur)}. At what time does it end?",
    }[key]
    h, mm = divmod(dur, 60)
    sh, sm = divmod(start, 60)
    wrong = [
        (Q(end - 60), "forgets to carry the extra hour from the minutes"),
        (Q(start + 60 * h), "adds only the hours"),
        (Q(start - dur) if start - dur >= 0 else Q(end + 60), "subtracts instead of adding" if start - dur >= 0 else None),
    ]
    if (start < 12 * 60) != (end < 12 * 60):
        wrong.append((Q(end - 720) if end >= 720 else Q(end + 720), "uses the wrong a.m. or p.m."))
    total_m = sm + mm
    steps = [
        f"Add the minutes: {m(f'{sm} + {mm} = {total_m}')} minutes, which is 1~hour "
        f"{m(str(total_m - 60))}~minutes. Write down {m(str(total_m - 60))} minutes and carry 1 hour.",
        f"Add the hours: {m(f'{sh % 12 or 12} + {h} + 1 = {sh % 12 + h + 1 if sh % 12 else 12 + h + 1}')}"
        + (f", and past 12 the clock starts over." if (sh % 12 or 12) + h + 1 > 12 else "."),
        f"The time is {_clock12_raw(end)}.",
    ]
    return _Prob(stem=stem, answer=Q(end), fmt=_clock12, section="AR", wrong=wrong, steps=steps,
                   near=_near(end, step=10),
                   check=Q((datetime.datetime(2026, 1, 1, sh, sm) + datetime.timedelta(minutes=dur)).hour * 60
                           + (datetime.datetime(2026, 1, 1, sh, sm) + datetime.timedelta(minutes=dur)).minute))


def _mil(v):
    """'1320' raw (inside math)."""
    h, mm = divmod(int(v), 60)
    return f"{h:02d}{mm:02d}"


@template("AR")
@_retrying
def military_time(rng, lvl):
    if lvl <= 2:
        kind = _fresh(rng, ["elapsed", "elapsed", "convert_add"], "mil2", keep=1)
        if kind == "elapsed":
            key = _fresh(rng, ["convoy", "range", "flight", "watch"], "mil_el")
            start = rng.randrange(4 * 60, 14 * 60, 5)
            end = rng.randrange(start + 90, min(start + 12 * 60, 23 * 60 + 55), 5)
            need(start % 60 > end % 60)
            stem = {
                "convoy": f"A supply convoy departs at {m(_mil(start))} and arrives at {m(_mil(end))}. How long is the trip?",
                "range": f"Range training starts at {m(_mil(start))} and ends at {m(_mil(end))}. How long does the training last?",
                "flight": f"A military transport flight takes off at {m(_mil(start))} and lands at {m(_mil(end))} (same time zone). How long is the flight?",
                "watch": f"A Navy cook works in the ship's galley from {m(_mil(start))} to {m(_mil(end))}. How long is the cook's shift?",
            }[key]
            dur = end - start
            sh, sm = divmod(start, 60)
            eh, em = divmod(end, 60)
            wrong = [
                (Q(_borrow_trap(start, end)), _borrow_why(start, end)),
                (Q(60 * (eh - sh) + (sm - em)), "subtracts the smaller number of minutes from the larger instead of borrowing"),
                (Q(dur + 60), "borrows the hour but forgets to take it away from the hours"),
                (Q(60 * (eh - 1 - sh) + (sm - em)), "borrows an hour but forgets to add the 60 minutes"),
            ]
            steps = [
                f"{m(str(em))} minutes minus {m(str(sm))} minutes won't go, so borrow 1 hour: "
                f"{m(_mil(end))} becomes {m(str(eh - 1))} hours {m(str(em + 60))} minutes.",
                f"Subtract: {m(f'{eh - 1} - {sh} = {eh - 1 - sh}')} hours and "
                f"{m(f'{em + 60} - {sm} = {em + 60 - sm}')} minutes.",
                f"The time is {_hm_text(dur)}.",
            ]
            return _Prob(stem=stem, answer=Q(dur), fmt=_dur, section="AR", wrong=wrong, steps=steps,
                           near=_near(dur, step=10),
                           check=Q((datetime.datetime(2026, 1, 1, eh, em) - datetime.datetime(2026, 1, 1, sh, sm)).seconds // 60))
        # standard p.m. time + duration -> military end time
        start = rng.randrange(13 * 60 + 5, 17 * 60 + 30, 5)
        dur = rng.randrange(2 * 60, 8 * 60, 5)
        end = start + dur
        need(end < 24 * 60 and (start % 60) + (dur % 60) >= 60)
        s_ = _army(rng)
        stem = (f"{s_} begins guard duty at {_clock12_raw(start)}. The shift lasts {_hm_text(dur)}. "
                f"At what time does the shift end, in military time?")
        sh, sm = divmod(start, 60)
        h, mm = divmod(dur, 60)
        wrong = [
            (Q(end - 720), "forgets to change the p.m. time to 24-hour time"),
            (Q(end - 60), "forgets to carry the extra hour from the minutes"),
            (Q(start + 60 * h), "adds only the hours"),
        ]
        steps = [
            f"Change to military time: {_clock12_raw(start)} is {m(f'{sh - 12} + 12 = {sh}')} hours, so {m(_mil(start))}.",
            f"Add the minutes: {m(f'{sm} + {mm} = {sm + mm}')} minutes $=$ 1~hour {m(str(sm + mm - 60))}~minutes.",
            f"Add the hours: {m(f'{sh} + {h} + 1 = {sh + h + 1}')}. The shift ends at {m(_mil(end))}.",
        ]
        return _Prob(stem=stem, answer=Q(end), fmt=_clock24, section="AR", wrong=wrong, steps=steps,
                       near=_near(end, step=15), check=Q((start + dur) % 1440))
    # level 3: across midnight
    kind = _fresh(rng, ["overnight", "arrival"], "mil3", keep=1)
    if kind == "overnight":
        start = rng.randrange(20 * 60, 23 * 60 + 55, 5)
        end = rng.randrange(3 * 60, 8 * 60, 5)
        need((24 * 60 - start) % 60 != 0 and end % 60 != 0)
        key = _fresh(rng, ["guard", "watch", "drive", "fireguard"], "night")
        stem = {
            "guard": f"A soldier pulls guard duty from {m(_mil(start))} until {m(_mil(end))} the next morning. How long is the guard shift?",
            "watch": f"A sailor works a night security shift at the pier from {m(_mil(start))} to {m(_mil(end))} the next morning. How long is the shift?",
            "drive": f"A convoy leaves at {m(_mil(start))} and reaches its destination at {m(_mil(end))} the next morning. How long is the drive?",
            "fireguard": f"A night-shift nurse at a military hospital works from {m(_mil(start))} to {m(_mil(end))} the next morning. How long is the shift?",
        }[key]
        before = 24 * 60 - start
        dur = before + end
        sh, sm = divmod(start, 60)
        wrong = [
            (Q(start - end), f"subtracts {m(_mil(end))} from {m(_mil(start))} instead of going past midnight"),
            (Q(dur + 40) if sm > 40 else None, f"borrows 100 minutes instead of 60 when counting up to midnight "
             f"({m('2400')} $-$ {m(_mil(start))} read as {_hm_text(before + 40)})"),
            (Q(24 * 60 - dur), "finds the rest of the 24 hours instead of the time on duty"),
            (Q(end), "counts only the time after midnight"),
            (Q(dur - 60), None),
        ]
        wrong = [w for w in wrong if w[0] is not None]
        steps = [
            f"From {m(_mil(start))} to midnight ({m('2400')}): {_hm_text(before)}.",
            f"From midnight to {m(_mil(end))}: {_hm_text(end)}.",
            f"Add: {_hm_text(before)} $+$ {_hm_text(end)} $=$ {_hm_text(dur)}.",
        ]
        return _Prob(stem=stem, answer=Q(dur), fmt=_dur, section="AR", wrong=wrong, steps=steps,
                       near=_near(dur, step=15),
                       check=Q((datetime.datetime(2026, 1, 2, end // 60, end % 60)
                                - datetime.datetime(2026, 1, 1, sh, sm)).seconds // 60))
    start = rng.randrange(18 * 60, 23 * 60 + 55, 5)
    dur = rng.randrange(4 * 60, 11 * 60, 5)
    end = (start + dur) % 1440
    need(start + dur >= 1440 and (start % 60) + (dur % 60) >= 60)
    key = _fresh(rng, ["flight", "convoy", "ship"], "arr")
    stem = {
        "flight": f"A flight carrying troops leaves at {m(_mil(start))} and the flight takes {_hm_text(dur)}. At what time (in military time, same time zone) does it land?",
        "convoy": f"A convoy leaves at {m(_mil(start))} for a drive that takes {_hm_text(dur)}. At what military time will it arrive?",
        "ship": f"A ship's crew starts loading cargo at {m(_mil(start))}, and the job takes {_hm_text(dur)}. At what military time will the loading be finished?",
    }[key]
    sh, sm = divmod(start, 60)
    h, mm = divmod(dur, 60)
    wrong = [
        (Q(end - 60) if end >= 60 else Q(end + 1380), "forgets to carry the extra hour from the minutes"),
        (Q((start + dur - 720) % 1440), "subtracts 12 hours instead of 24 after passing midnight"),
        (Q((start + 60 * h) % 1440), "adds only the hours"),
        (Q((end + 60) % 1440), None),
    ]
    tot_h = sh + h + 1
    steps = [
        f"Add the minutes: {m(f'{sm} + {mm} = {sm + mm}')} minutes $=$ 1~hour {m(str(sm + mm - 60))}~minutes.",
        f"Add the hours: {m(f'{sh} + {h} + 1 = {tot_h}')}. Past midnight, subtract 24: {m(f'{tot_h} - 24 = {tot_h - 24}')}.",
        f"The answer is {m(_mil(end))} the next day.",
    ]
    return _Prob(stem=stem, answer=Q(end), fmt=_clock24, section="AR", wrong=wrong, steps=steps,
                   near=_near(end, step=30),
                   check=Q(((datetime.datetime(2026, 1, 1, sh, sm) + datetime.timedelta(minutes=dur)).hour * 60
                            + (datetime.datetime(2026, 1, 1, sh, sm) + datetime.timedelta(minutes=dur)).minute)))


# --------------------------------------------------------------------------
# mixed units
# --------------------------------------------------------------------------

_MIX = {
    # key: (factor, big abbrev, small abbrev, big word, small word)
    "ftin": (12, "ft", "in", "feet", "inches"),
    "lboz": (16, "lb", "oz", "pounds", "ounces"),
    "hrmin": (60, "hr", "min", "hours", "minutes"),
    "galqt": (4, "gal", "qt", "gallons", "quarts"),
    "ydft": (3, "yd", "ft", "yards", "feet"),
}


def _mixfmt(key):
    f, B, S, _, _ = _MIX[key]

    def fmt(v):
        v = Q(v)
        need(v.is_integer and v > 0, "bad mixed value")
        b, s_ = divmod(int(v), f)
        parts = []
        if b:
            parts.append(f"{m(int_raw(b))}~{B}")
        if s_:
            parts.append(f"{m(int_raw(s_))}~{S}")
        return " ".join(parts)
    return fmt


@template("AR")
@_retrying
def mixed_units(rng, lvl):
    key = _fresh(rng, list(_MIX), "mix")
    f, B, S, Bw, Sw = _MIX[key]
    fmt = _mixfmt(key)
    sub = lvl >= 2
    if key == "ftin":
        b1, b2 = rng.randint(3, 12), rng.randint(1, 8)
    elif key == "lboz":
        b1, b2 = rng.randint(2, 30), rng.randint(1, 15)
    elif key == "hrmin":
        b1, b2 = rng.randint(1, 6), rng.randint(1, 4)
    elif key == "galqt":
        b1, b2 = rng.randint(2, 20), rng.randint(1, 12)
    else:
        b1, b2 = rng.randint(3, 20), rng.randint(1, 10)
    s1, s2 = rng.randrange(1, f), rng.randrange(1, f)
    v1, v2 = b1 * f + s1, b2 * f + s2
    p = person(rng)
    if not sub:
        need(s1 + s2 > f)
        if f > 10:
            need(s1 + s2 >= 10)
        ans = v1 + v2
        stem = {
            "ftin": f"{p} lays two boards end to end. One is {fmt(v1)} long and the other is {fmt(v2)} long. What is their total length?",
            "lboz": f"{p} mails two packages. One weighs {fmt(v1)} and the other weighs {fmt(v2)}. What is their total weight?",
            "hrmin": f"A ruck march has two legs. The first takes {fmt(v1)} and the second takes {fmt(v2)}. What is the total time?",
            "galqt": f"A motor pool has two partly full drums of motor oil. One holds {fmt(v1)} and the other holds {fmt(v2)}. How much oil is there in all?",
            "ydft": f"{p} has two pieces of rope. One is {fmt(v1)} long and the other is {fmt(v2)} long. What is their total length?",
        }[key]
        ss = s1 + s2
        carry, rem = divmod(ss, f)
        wrong = [
            (Q(ans - f), f"changes {ss} {S} to {rem} {S} but forgets to add 1 to the {Bw}"),
        ]
        if f in (12, 16) and ss >= 10 and ss % 10 < f:
            wrong.append((Q((b1 + b2 + ss // 10) * f + ss % 10), f"regroups 10 {Sw} as 1 {B} instead of {f}"))
        wrong.append((Q(ans + f), f"adds 1 {B} for the extra {Sw} but does not take {f} {S} away"))
        steps = [
            f"Add the {Sw}: {m(f'{s1} + {s2} = {ss}')} {S}. Since {m(f'{f}')} {S} $=$ 1 {B}, "
            f"{m(str(ss))} {S} $=$ 1 {B} {m(str(rem))} {S}.",
            f"Add the {Bw}: {m(f'{b1} + {b2} + 1 = {b1 + b2 + 1}')} {B}.",
            f"Total: {fmt(ans)}.",
        ]
        return _Prob(stem=stem, answer=Q(ans), fmt=fmt, section="AR", wrong=wrong, steps=steps,
                       near=_near(ans, step=1 if f < 10 else 2), check=Q(v1 + v2))
    need(b1 > b2 and s1 < s2)
    ans = v1 - v2
    stem = {
        "ftin": f"{p} has a board that is {fmt(v1)} long and cuts off a piece {fmt(v2)} long. How long is the board that is left?",
        "lboz": f"A box of supplies weighs {fmt(v1)}. After {p} removes {fmt(v2)} of supplies, how much does the box weigh?",
        "hrmin": f"A training exercise is scheduled to last {fmt(v1)}. After {fmt(v2)}, how much time is left?",
        "galqt": f"A water tank held {fmt(v1)} of water. A squad used {fmt(v2)}. How much water is left?",
        "ydft": f"A roll of fabric holds {fmt(v1)}. {p} cuts off {fmt(v2)}. How much fabric is left on the roll?",
    }[key]
    if key == "lboz":
        stem = stem.replace("weighs", "weighs", 1)
    sw = s1 + f - s2
    wrong = [
        (Q((b1 - b2) * f + (s2 - s1)), f"subtracts the smaller number of {Sw} from the larger instead of borrowing"),
        (Q(ans + f), f"borrows 1 {B} but forgets to take it away from the {Bw}"),
    ]
    bw = 100 if f == 60 else 10
    if f > 10 and s1 + bw - s2 >= 0:
        wrong.append((Q((b1 - 1 - b2) * f + (s1 + bw - s2)), f"borrows {bw} {Sw} instead of {f}"))
    wrong.append((Q(ans - f) if ans - f > 0 else Q(ans + 2 * f), None))
    steps = [
        f"You can't take {m(str(s2))} {S} from {m(str(s1))} {S}, so borrow 1 {B}: "
        f"{fmt(v1)} becomes {m(str(b1 - 1))} {B} {m(str(s1 + f))} {S}.",
        f"Subtract: {m(f'{s1 + f} - {s2} = {sw}')} {S} and {m(f'{b1 - 1} - {b2} = {b1 - 1 - b2}')} {B}.",
        f"What is left: {fmt(ans)}.",
    ]
    return _Prob(stem=stem, answer=Q(ans), fmt=fmt, section="AR", wrong=wrong, steps=steps,
                   near=_near(ans, step=1 if f < 10 else 2), check=Q(v1 - v2))


# --------------------------------------------------------------------------
# rounding in context
# --------------------------------------------------------------------------

@template("AR")
@_retrying
def round_up_down(rng, lvl):
    if lvl >= 3:
        return _round_cost(rng)
    up = _fresh(rng, [True, False], "updown", keep=1)
    if lvl == 1:
        if up:
            key = _fresh(rng, ["eggs", "ammo", "pallets", "seeds", "rafts"], "up1")
            per, total = {"eggs": (12, rng.randint(100, 900)),
                          "ammo": (rng.choice([200, 250, 400]), rng.randint(900, 5000)),
                          "pallets": (rng.choice([30, 40, 48]), rng.randint(200, 1500)),
                          "seeds": (rng.choice([15, 20, 25]), rng.randint(60, 400)),
                          "rafts": (rng.choice([6, 8]), rng.randint(20, 90))}[key]
            # (stem, container plural, item plural, leftover phrase)
            stem, cont, items, left = {
                "eggs": (f"A farm packs eggs in cartons of {num(per)}. How many cartons are needed to pack {num(total)} eggs?",
                         "cartons", "eggs", "without a carton"),
                "ammo": (f"Each ammunition can holds {num(per)} rounds. How many cans are needed for {num(total)} rounds of training ammunition?",
                         "cans", "rounds", "without a can"),
                "pallets": (f"Each pallet holds {num(per)} cases of MREs. How many pallets are needed to ship {num(total)} cases?",
                            "pallets", "cases", "off the pallets"),
                "seeds": (f"One packet of seeds plants {num(per)} feet of garden row. How many packets does {person(rng)} need to plant {num(total)} feet of rows?",
                          "packets", "feet of row", "unplanted"),
                "rafts": (f"Each rubber raft holds {num(per)} soldiers for a river-crossing exercise. How many rafts are needed for {num(total)} soldiers?",
                          "rafts", "soldiers", "without a raft"),
            }[key]
        else:
            key = _fresh(rng, ["tickets", "shelf", "truck", "rope", "shirts"], "down1")
            per, total = {"tickets": (rng.choice([7, 8, 9, 12, 15]), rng.randint(40, 150)),
                          "shelf": (rng.choice([2, 3]), rng.randint(25, 60)),
                          "truck": (rng.choice([120, 140, 150, 160, 180]), rng.choice([2000, 2500, 3000, 4000, 5000])),
                          "rope": (rng.choice([6, 8, 12, 15]), rng.choice([50, 75, 100, 150])),
                          "shirts": (rng.choice([12, 14, 18, 22]), rng.randint(50, 150))}[key]
            # (stem, items counted, singular item, leftover unit)
            stem, cont, one, items = {
                "tickets": (f"Movie tickets cost {money(per)} each. How many tickets can be bought with {money(total)}?",
                            "tickets", "ticket", "dollars"),
                "shelf": (f"A shelf is {num(total)} inches long. How many binders, each {num(per)} inches thick, can stand on it?",
                          "binders", "binder", "inches"),
                "truck": (f"A trailer can safely carry {num(total)} pounds. Each crate weighs {num(per)} pounds. What is the greatest number of crates it can carry?",
                          "crates", "crate", "pounds"),
                "rope": (f"A {num(total)}-foot coil of rope is cut into {num(per)}-foot pieces for a training course. How many full pieces can be cut?",
                         "pieces", "piece", "feet"),
                "shirts": (f"{person(rng)} has {money(total)} to spend on T-shirts that cost {money(per)} each. How many shirts can be bought?",
                           "shirts", "shirt", "dollars"),
            }[key]
        q, r = divmod(total, per)
        need(r != 0 and q >= 2)
        ans = q + 1 if up else q
        exact = R(total, per)
        if up:
            wrong = [(Q(q), f"rounds down, which leaves {r} {items} {left}")]
            last = (f"{m(str(q))} {cont} take care of only {m(f'{q} \\times {per} = {int_raw(q * per)}')} {items}, "
                    f"leaving {m(str(r))} {items} {left}. One more is needed: {m(f'{q} + 1 = {q + 1}')} {cont}.")
        else:
            wrong = [(Q(q + 1), f"rounds up, but there is not enough for another {one}")]
            amt = (money(r) if items == "dollars" else f"{m(str(r))} {items}")
            last = (f"The {amt} left over {'is' if items == 'dollars' else 'are'} not enough for another {one}, "
                    f"so the answer is {m(str(q))} {cont}.")
        wrong += [
            (Q(r), f"gives the leftover {items}, not the number of {cont}"),
            (Q(q + r), "adds the remainder to the quotient"),
        ]
        if (exact * 10).is_integer:
            wrong.append((exact, "gives the exact quotient, which is not a whole number"))
        steps = [
            f"Divide: {m(f'{int_raw(total)} \\div {per}')} is {m(str(q))} with a remainder of {m(str(r))}.",
            last,
        ]
        return _Prob(stem=stem, answer=Q(ans), fmt=num, section="AR", wrong=wrong, steps=steps,
                     near=_near(ans), check=Q(math.ceil(Fraction(total, per)) if up else total // per))
    # level 2: with a unit conversion
    key = _fresh(rng, ["board", "bottle", "water", "milk", "sand"], "round2")
    wrong_conv = None
    if key == "board":
        ft = rng.randint(6, 20)
        piece = rng.choice([7, 9, 10, 11, 14, 15, 16, 18, 20, 22])
        total, per, up = 12 * ft, piece, False
        stem = (f"{person(rng)} cuts a {num(ft)}-foot board into pieces {num(piece)} inches long. "
                f"How many full pieces can be cut?")
        conv = f"Change feet to inches: {m(f'{ft} \\times 12 = {total}')} inches."
        if ft >= piece:
            wrong_conv = (Q(ft // piece), "forgets to change feet to inches")
        cont, one, items = "pieces", "piece", "inches"
        last = lambda q, r: (f"Only full pieces count: the {m(str(r))} inches left are too short for "  # noqa: E731
                             f"another piece, so {m(str(q))} pieces.")
    elif key == "bottle":
        L = rng.choice([1, 2, 3, 4])
        cup = rng.choice([150, 175, 200, 225, 300, 350, 400, 450])
        total, per, up = 1000 * L, cup, False
        stem = (f"{person(rng)} pours juice from a {num(L)}-liter bottle into {num(cup)}-milliliter "
                f"cups. How many cups can be filled completely?")
        conv = f"Change liters to milliliters: {m(f'{L} \\times 1{{,}}000 = {int_raw(total)}')} milliliters."
        if 100 * L >= cup:
            wrong_conv = (Q(100 * L // cup), "uses 100 milliliters in a liter instead of 1,000")
        cont, one, items = "cups", "cup", "milliliters"
        last = lambda q, r: (f"Only completely filled cups count: the {m(str(r))} milliliters left will "  # noqa: E731
                             f"not fill another cup, so {m(str(q))} cups.")
    elif key == "water":
        gal = rng.choice([5, 10, 15, 20, 25, 30, 40, 50])
        qt = rng.choice([3, 6, 7, 9])
        total, per, up = 4 * gal, qt, False
        stem = (f"In the field, each soldier needs {num(qt)} quarts of water per day. How many soldiers can "
                f"a full {num(gal)}-gallon water tank supply for one day?")
        conv = f"Change gallons to quarts: {m(f'{gal} \\times 4 = {total}')} quarts."
        if 2 * gal >= qt:
            wrong_conv = (Q(2 * gal // qt), "uses 2 quarts in a gallon instead of 4")
        cont, one, items = "soldiers", "soldier", "quarts"
        last = lambda q, r: (f"The {m(str(r))} quarts left are not enough for another soldier's day, so "  # noqa: E731
                             f"{m(str(q))} soldiers.")
    elif key == "milk":
        batches = rng.randint(5, 16)
        cups = rng.choice([2, 3, 5])
        total, per, up = batches * cups, 8, True
        stem = (f"{person(rng)}'s pancake recipe uses {num(cups)} cups of milk per batch, and "
                f"{num(batches)} batches are needed for a fundraiser breakfast. How many half-gallon "
                f"cartons of milk must be bought? (1 half gallon $=$ 8 cups)")
        conv = f"Total milk: {m(f'{batches} \\times {cups} = {total}')} cups."
        wrong_conv = (Q(math.ceil(Fraction(total, 16))), "uses 16 cups per carton (that is a full gallon)")
        cont, one, items = "cartons", "carton", "cups"
        last = lambda q, r: (f"{m(str(q))} cartons hold only {m(f'{q} \\times 8 = {8 * q}')} cups, which is "  # noqa: E731
                             f"{m(str(r))} cups short, so buy {m(str(q + 1))} cartons.")
    else:
        tons = rng.choice([1, 2, 3, 4, 5])
        bag = rng.choice([30, 35, 40, 45, 60, 70, 80, 90])
        total, per, up = 2000 * tons, bag, True
        stem = (f"Engineers need {num(tons)} {_pl('ton', tons)} of sand for sandbags. The sand comes in {num(bag)}-pound "
                f"bags. How many bags must they order?")
        conv = f"Change tons to pounds: {m(f'{tons} \\times 2{{,}}000 = {int_raw(total)}')} pounds."
        wrong_conv = (Q(math.ceil(Fraction(1000 * tons, bag))), "uses 1,000 pounds in a ton instead of 2,000")
        cont, one, items = "bags", "bag", "pounds"
        last = lambda q, r: (f"{m(str(q))} bags hold only {m(f'{q} \\times {per} = {int_raw(q * per)}')} pounds, "  # noqa: E731
                             f"which is {m(str(r))} pounds short, so order {m(str(q + 1))} bags.")
    q, r = divmod(total, per)
    need(r != 0 and q >= 2)
    ans = q + 1 if up else q
    wrong = [
        (Q(q) if up else Q(q + 1), f"rounds down, which leaves {r} {items} short" if up
         else f"rounds up, but there is not enough for another {one}"),
        (Q(r), f"gives the leftover {items}, not the number of {cont}"),
    ]
    if wrong_conv is not None:
        wrong.insert(1, wrong_conv)
    steps = [
        conv,
        f"Divide: {m(f'{int_raw(total)} \\div {per}')} is {m(str(q))} with a remainder of {m(str(r))}.",
        last(q, r),
    ]
    return _Prob(stem=stem, answer=Q(ans), fmt=num, section="AR", wrong=wrong, steps=steps,
                 near=_near(ans), check=Q(math.ceil(Fraction(total, per)) if up else total // per))


def _round_cost(rng):
    key = _fresh(rng, ["paint", "tile", "fence", "sod"], "round3")
    if key == "paint":
        cover = rng.choice([300, 350, 400])
        area = rng.randint(8, 40) * 50
        price = rng.choice([25, 28, 32, 35, 38, 42])
        stem = (f"One gallon of paint covers {num(cover)} square feet. Paint is sold only in whole "
                f"gallons at {money(price)} per gallon. How much will it cost to paint {num(area)} "
                f"square feet of walls?")
        unit_w = "gallons"
    elif key == "tile":
        cover = rng.choice([10, 12, 15, 20])
        area = rng.randint(40, 300)
        price = rng.choice([24, 30, 36, 45])
        stem = (f"Floor tile is sold in boxes that each cover {num(cover)} square feet, at {money(price)} "
                f"per box. How much will enough tile cost to cover a {num(area)}-square-foot floor?")
        unit_w = "boxes"
    elif key == "fence":
        cover = rng.choice([25, 50])
        area = rng.randint(60, 400)
        price = rng.choice([30, 45, 60, 75])
        stem = (f"Wire fencing comes in {num(cover)}-foot rolls that cost {money(price)} each. How much "
                f"will it cost to buy enough rolls to fence {num(area)} feet?")
        unit_w = "rolls"
    else:
        cover = rng.choice([10, 16, 20])
        area = rng.randint(50, 400)
        price = rng.choice([5, 6, 8, 9])
        stem = (f"Each roll of sod covers {num(cover)} square feet and costs {money(price)}. How much "
                f"will it cost to buy enough rolls to cover a {num(area)}-square-foot yard?")
        unit_w = "rolls"
    q, r = divmod(area, cover)
    need(r != 0 and q >= 2)
    n_ = q + 1
    ans = Q(n_ * price)
    wrong = [
        (Q(q * price), f"rounds the number of {unit_w} down, which is not enough"),
        (Q((q + 2) * price), None),
        (Q(n_ * price + price), None),
    ]
    if R(area * price, cover).is_integer:
        wrong.insert(1, (R(area * price, cover), f"pays for part of a {'box' if unit_w == 'boxes' else unit_w[:-1]}, which is not sold"))
    one = {"gallons": "gallon", "boxes": "box", "rolls": "roll"}[unit_w]
    area_u = "feet" if key == "fence" else "square feet"
    steps = [
        f"Each {one} covers {num(cover)} {area_u}: "
        f"{m(f'{int_raw(area)} \\div {cover}')} is {m(str(q))} with a remainder of {m(str(r))}.",
        f"{m(str(q))} {unit_w} would cover only {m(f'{q} \\times {cover} = {int_raw(q * cover)}')} {area_u}, "
        f"which is not quite enough, so buy {m(str(n_))} {unit_w}.",
        f"Cost: {m(f'{n_} \\times {price} = {int_raw(ans)}')}, so {money(ans)}.",
    ]
    return _Prob(stem=stem, answer=ans, fmt=money, section="AR", wrong=wrong, steps=steps,
                   near=_near(ans), check=Q(math.ceil(Fraction(area, cover)) * price))


# --------------------------------------------------------------------------
# multi-step reasoning
# --------------------------------------------------------------------------

_FRACS = [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (1, 6), (1, 8), (3, 8)]


@template("AR")
@_retrying
def fraction_remainder(rng, lvl):
    key = _fresh(rng, ["paycheck", "convoy", "fuel", "recruits", "water", "prize"], "fracrem")
    f1 = R(*rng.choice(_FRACS))
    f2 = R(*rng.choice(_FRACS))
    need(f1 != f2 or rng.random() < 0.2)
    rest1 = 1 - f1
    left_frac = rest1 * (1 - f2)
    p = person(rng)
    fr1, fr2 = m(frac_raw(f1)), m(frac_raw(f2))
    if lvl >= 3:
        # reverse: amount left is known, find the original
        left = rng.choice({"paycheck": range(200, 1601, 50), "convoy": range(20, 301, 10),
                           "fuel": range(6, 61, 2), "recruits": range(20, 241, 4),
                           "water": range(10, 301, 5), "prize": range(100, 2001, 50)}[key])
        T = left / left_frac
        need(T.is_integer and (T * f1).is_integer and (T * rest1 * f2).is_integer)
        need(T <= {"paycheck": 6000, "convoy": 600, "fuel": 120, "recruits": 300,
                   "water": 600, "prize": 10000}[key])
        stem = {
            "paycheck": f"{p} spent {fr1} of {p.his} paycheck on rent and then {fr2} of what was left on groceries. {p.He} had {money(left)} left. How much was the paycheck?",
            "convoy": f"On the first day a convoy drove {fr1} of its route, and on the second day it drove {fr2} of the remaining distance. It still has {num(left)} miles to go. How long is the whole route?",
            "fuel": f"A generator used {fr1} of a tank of fuel on Monday and {fr2} of the remaining fuel on Tuesday. {num(left)} gallons are left. How many gallons does a full tank hold?",
            "recruits": f"Of the recruits who started a training course, {fr1} were sent to other units in the first week, and {fr2} of the rest were sent away in the second week. {num(left)} recruits remain. How many recruits started the course?",
            "water": f"A water tank was full. Soldiers used {fr1} of the water in the morning and {fr2} of what was left in the afternoon. {num(left)} gallons remain. How many gallons does the tank hold?",
            "prize": f"{p} won a cash prize. {p.He} spent {fr1} of it on a car repair and saved {fr2} of the rest. {p.He} has {money(left)} left to spend. How much was the prize?",
        }[key]
        fmt = money if key in ("paycheck", "prize") else num
        wrong = [
            (left / (1 - f1 - f2) if f1 + f2 < 1 else None, "subtracts both fractions from the whole amount"),
            (left * (1 + f1) * (1 + f2), "increases the amount by each fraction instead of dividing"),
            (left / rest1, "undoes only the first step"),
            (left + left * (f1 + f2), "adds the fractions of the amount left"),
        ]
        wrong = [w_ for w_ in wrong if w_[0] is not None]
        need(sum(1 for w_ in wrong if Q(w_[0]).is_integer and Q(w_[0]) != T) >= 2)
        lf = frac_raw(left_frac)
        steps = [
            f"After the first step, {m(f'1 - {frac_raw(f1)} = {frac_raw(rest1)}')} of the whole is left.",
            f"The second step uses {fr2} of that, leaving {m(f'1 - {frac_raw(f2)} = {frac_raw(1 - f2)}')} of it: "
            f"{m(f'{frac_raw(rest1)} \\times {frac_raw(1 - f2)} = {lf}')} of the whole.",
            f"So {m(lf)} of the whole is {num(left) if fmt is num else money(left)}: "
            f"{m(f'{int_raw(left)} \\div {lf} = {int_raw(T)}')}.",
        ]
        return _Prob(stem=stem, answer=T, fmt=fmt, section="AR", wrong=wrong, steps=steps,
                       near=_near(T), verify=lambda v: Q(v) * left_frac == left,
                       check=sp.solve(sp.Eq(X * (1 - f1) * (1 - f2), left), X)[0])
    T = rng.choice({"paycheck": range(1200, 4801, 60), "convoy": range(120, 601, 12),
                    "fuel": range(24, 121, 4), "recruits": range(60, 301, 12),
                    "water": range(100, 601, 20), "prize": range(600, 4801, 60)}[key])
    first = T * f1
    rest = T - first
    second = rest * f2
    left = rest - second
    need(first.is_integer and second.is_integer and left > 0)
    ask_left = rng.random() < 0.65
    stem = {
        "paycheck": f"{p} earns {money(T)} a month. {p.He} spends {fr1} of it on rent and {fr2} of the remainder on food. ",
        "convoy": f"A convoy must travel {num(T)} miles. On the first day it covers {fr1} of the distance, and on the second day it covers {fr2} of the remaining distance. ",
        "fuel": f"A truck starts with {num(T)} gallons of fuel. It uses {fr1} of the fuel on the first day and {fr2} of what is left on the second day. ",
        "recruits": f"A training company starts with {num(T)} recruits. In the first month, {fr1} of them are moved to another company, and in the second month, {fr2} of the remaining recruits are moved. ",
        "water": f"A water tank holds {num(T)} gallons. Soldiers use {fr1} of the water in the morning and {fr2} of what is left in the afternoon. ",
        "prize": f"{p} wins {money(T)}. {p.He} spends {fr1} of it on a car repair and saves {fr2} of the rest. ",
    }[key]
    q_left = {"paycheck": f"How much does {p.he} have left for other expenses?",
              "convoy": "How many miles are left to travel?",
              "fuel": "How many gallons are left?",
              "recruits": "How many recruits remain?",
              "water": "How many gallons are left?",
              "prize": f"How much money does {p.he} have left to spend?"}[key]
    q_second = {"paycheck": f"How much does {p.he} spend on food?",
                "convoy": "How many miles does it cover on the second day?",
                "fuel": "How many gallons does it use on the second day?",
                "recruits": "How many recruits are moved in the second month?",
                "water": "How many gallons are used in the afternoon?",
                "prize": f"How much does {p.he} save?"}[key]
    stem += q_left if ask_left else q_second
    fmt = money if key in ("paycheck", "prize") else num
    ans = left if ask_left else second
    first_n, second_n, left_n = {
        "paycheck": ("rent", "amount spent on food", "amount left"),
        "convoy": ("miles driven on the first day", "miles driven on the second day", "miles left"),
        "fuel": ("fuel used on the first day", "fuel used on the second day", "fuel left"),
        "recruits": ("recruits moved in the first month", "recruits moved in the second month",
                     "recruits who remain"),
        "water": ("water used in the morning", "water used in the afternoon", "water left"),
        "prize": ("cost of the car repair", "amount saved", "amount left to spend"),
    }[key]
    asked = left_n if ask_left else second_n
    wrong = [
        (rest, f"stops after the first step (gives what is left after the {first_n})"
         if key not in ("paycheck", "prize") else "stops after the first step"),
        (second if ask_left else left, f"gives the {second_n if ask_left else left_n}, not the {asked}"),
        (first, f"gives the {first_n}, not the {asked}"),
    ]
    if ask_left and f1 + f2 < 1:
        wrong.insert(0, (T * (1 - f1 - f2), "takes both fractions of the original amount instead of the remainder"))
    elif not ask_left:
        wrong.insert(0, (T * f2, "takes the fraction of the original amount instead of the remainder"))
    steps = [
        f"First step: {m(f'{frac_raw(f1)} \\times {int_raw(T)} = {int_raw(first)}')}. "
        f"Remainder: {m(f'{int_raw(T)} - {int_raw(first)} = {int_raw(rest)}')}.",
        f"Second step: {fr2} of the \\emph{{remainder}}: {m(f'{frac_raw(f2)} \\times {int_raw(rest)} = {int_raw(second)}')}.",
    ]
    if ask_left:
        steps.append(f"Left: {m(f'{int_raw(rest)} - {int_raw(second)} = {int_raw(left)}')}.")
    return _Prob(stem=stem, answer=ans, fmt=fmt, section="AR", wrong=wrong, steps=steps,
                   near=_near(ans),
                   check=(Fraction(T) * (1 - Fraction(f1.p, f1.q)) * ((1 - Fraction(f2.p, f2.q)) if ask_left else Fraction(f2.p, f2.q))))


@template("AR")
@_retrying
def age_problem(rng, lvl):
    p = person(rng)
    if lvl <= 2:
        kind = _fresh(rng, ["sumdiff", "past", "future"], "age2")
        if kind == "sumdiff":
            rel = _fresh(rng, ["brother", "sister", "cousin"], "agerel")
            young = rng.randint(8, 30)
            d = rng.randint(2, 12)
            old = young + d
            S = old + young
            stem = (f"{p} is {num(d)} years older than {p.his} {rel}. The sum of their ages is {num(S)}. "
                    f"How old is {p}?")
            wrong = [
                (Q(young), f"gives the {rel}'s age"),
                (Q(S - d), "subtracts the difference but forgets to divide by 2"),
                (R(S, 2), "splits the sum evenly, ignoring the difference"),
                (Q(S + d), None),
            ]
            steps = [
                f"Take away the difference to make the ages equal: {m(f'{S} - {d} = {S - d}')}.",
                f"Split it in half to get the {rel}'s age: {m(f'{S - d} \\div 2 = {young}')}.",
                f"{p} is {num(d)} years older: {m(f'{young} + {d} = {old}')}.",
            ]
            ans = old
            verify = lambda v: Q(v) + (Q(v) - d) == S  # noqa: E731
            check = Q([a_ for a_ in range(1, 150) if a_ + (a_ - d) == S][0])
        elif kind == "past":
            k = rng.choice([2, 3])
            t = rng.randint(2, 10)
            y_now = rng.randint(t + 3, 35)
            x_now = k * (y_now - t) + t
            need(18 <= x_now - y_now <= 45 and x_now <= 80)
            rel = rng.choice(["daughter", "son", "nephew", "niece"])
            stem = (f"{num(t)} years ago, {p} was {'twice' if k == 2 else 'three times'} as old as "
                    f"{p.his} {rel} was then. The {rel} is {num(y_now)} now. How old is {p} now?")
            stem = _cap_num(stem)
            wrong = [
                (Q(k * y_now), f"multiplies the {rel}'s age today instead of {t} years ago"),
                (Q(k * (y_now - t)), f"gives {p}'s age {t} years ago, not now"),
                (Q(k * y_now + t), None),
                (Q(k * (y_now - t) - t), f"subtracts the {t} years instead of adding them back"),
            ]
            steps = [
                f"{t} years ago the {rel} was {m(f'{y_now} - {t} = {y_now - t}')}.",
                f"Then {p} was {m(f'{k} \\times {y_now - t} = {k * (y_now - t)}')}.",
                f"Add the {t} years back: {m(f'{k * (y_now - t)} + {t} = {x_now}')}.",
            ]
            ans = x_now
            verify = lambda v: Q(v) - t == k * (y_now - t)  # noqa: E731
            check = Q([a_ for a_ in range(1, 150) if a_ - t == k * (y_now - t)][0])
        else:
            k = rng.choice([2, 3])
            t = rng.randint(2, 10)
            y_now = rng.randint(2, 15)
            x_now = k * (y_now + t) - t
            need(x_now - y_now >= 18)
            rel = rng.choice(["daughter", "son"])
            stem = (f"In {num(t)} years, {p} will be {'twice' if k == 2 else 'three times'} as old as "
                    f"{p.his} {rel} will be then. The {rel} is {num(y_now)} now. How old is {p} now?")
            wrong = [
                (Q(k * y_now), f"multiplies the {rel}'s age today instead of in {t} years"),
                (Q(k * (y_now + t)), f"gives {p}'s age in {t} years, not now"),
                (Q(k * (y_now + t) + t), f"adds the {t} years instead of subtracting them"),
                (Q(k * y_now + t), None),
            ]
            steps = [
                f"In {t} years the {rel} will be {m(f'{y_now} + {t} = {y_now + t}')}.",
                f"Then {p} will be {m(f'{k} \\times {y_now + t} = {k * (y_now + t)}')}.",
                f"Today {p} is {t} years younger than that: {m(f'{k * (y_now + t)} - {t} = {x_now}')}.",
            ]
            ans = x_now
            verify = lambda v: Q(v) + t == k * (y_now + t)  # noqa: E731
            check = Q([a_ for a_ in range(1, 150) if a_ + t == k * (y_now + t)][0])
        return _Prob(stem=stem, answer=Q(ans), fmt=num, section="AR", wrong=wrong, steps=steps,
                       near=_near(ans), verify=verify, check=check)
    # level 3: two conditions -> solve for both ages
    kind = _fresh(rng, ["ratio_future", "sum_future", "ratio_past"], "age3")
    if kind == "ratio_future":
        k1, k2 = rng.choice([(3, 2), (4, 3), (4, 2), (5, 3), (3, 2)])
        t = rng.randint(4, 15)
        num_ = t * (k2 - 1)
        need(num_ % (k1 - k2) == 0)
        y = num_ // (k1 - k2)
        x_ = k1 * y
        need(4 <= y <= 20 and 22 <= x_ <= 55 and x_ - y >= 18)
        rel = rng.choice(["son", "daughter"])
        stem = (f"{p} is {_times(k1)} as old as {p.his} {rel}. In {num(t)} years, {p} will be "
                f"{_times(k2)} as old as the {rel}. How old is {p} now?")
        wrong = [
            (Q(y), f"gives the {rel}'s age"),
            (Q(x_ + t), f"gives {p}'s age in {t} years"),
            (Q(k2 * y), f"uses the second ratio for today's ages"),
            (Q(y + t), None),
        ]
        steps = [
            f"Let the {rel} be {m('a')} years old; then {p} is {m(f'{k1}a')}.",
            f"In {t} years: {m(f'{k1}a + {t} = {k2}(a + {t})')}, so {m(f'{k1}a + {t} = {k2}a + {k2 * t}')}.",
            f"Then {m(f'{_ca(k1 - k2)} = {k2 * t - t}')}, so {m(f'a = {y}')} and {p} is {m(f'{k1} \\times {y} = {x_}')}.",
        ]
        verify = lambda v: Q(v) % k1 == 0 and Q(v) + t == k2 * (Q(v) / k1 + t)  # noqa: E731
        sols = [(xx, yy) for yy in range(1, 60) for xx in range(1, 120) if xx == k1 * yy and xx + t == k2 * (yy + t)]
        check = Q(sols[0][0])
    elif kind == "sum_future":
        y = rng.randint(5, 15)
        k = rng.choice([2, 3])
        t = rng.randint(2, 10)
        x_ = k * (y + t) - t
        need(x_ - y >= 20 and x_ <= 70)
        S = x_ + y
        rel = rng.choice(["son", "daughter"])
        stem = (f"The sum of the ages of {p} and {p.his} {rel} is {num(S)}. In {num(t)} years, {p} will "
                f"be {_times(k)} as old as the {rel}. How old is {p} now?")
        wrong = [
            (Q(y), f"gives the {rel}'s age"),
            (Q(x_ + t), f"gives {p}'s age in {t} years"),
            (R(S, 2), "splits the sum in half"),
            (Q(k * y), None),
        ]
        steps = [
            f"Let the {rel} be {m('a')}; then {p} is {m(f'{S} - a')}.",
            f"In {t} years: {m(f'{S} - a + {t} = {k}(a + {t})')}, so {m(f'{S + t} - a = {k}a + {k * t}')}.",
            f"Then {m(f'{S + t - k * t} = {k + 1}a')}, so {m(f'a = {y}')}, and {p} is {m(f'{S} - {y} = {x_}')}.",
        ]
        verify = lambda v: (Q(v) + t) == k * (S - Q(v) + t)  # noqa: E731
        sols = [xx for xx in range(1, S) if xx + t == k * (S - xx + t)]
        check = Q(sols[0])
    else:
        k1, k2 = rng.choice([(2, 3), (2, 4), (3, 5), (2, 5)])
        t = rng.randint(3, 10)
        # now: x = k1*y ; t years ago: x - t = k2*(y - t)  -> y = t(k2-1)/(k2-k1)
        num_ = t * (k2 - 1)
        need(num_ % (k2 - k1) == 0)
        y = num_ // (k2 - k1)
        x_ = k1 * y
        need(y - t >= 2 and 22 <= x_ <= 75 and x_ - y >= 18)
        rel = rng.choice(["son", "daughter", "nephew"])
        stem = (f"{p} is {_times(k1)} as old as {p.his} {rel}. {_cap(_WORDS[t]) if t <= 12 else num(t)} "
                f"years ago, {p} was {_times(k2)} as old as the {rel}. How old is {p} now?")
        wrong = [
            (Q(y), f"gives the {rel}'s age"),
            (Q(x_ - t), f"gives {p}'s age {t} years ago"),
            (Q(k2 * y), "uses the second ratio for today's ages"),
            (Q(x_ + t), None),
        ]
        steps = [
            f"Let the {rel} be {m('a')} years old; then {p} is {m(f'{k1}a')}.",
            f"{t} years ago: {m(f'{k1}a - {t} = {k2}(a - {t})')}, so {m(f'{k1}a - {t} = {k2}a - {k2 * t}')}.",
            f"Then {m(f'{k2 * t - t} = {_ca(k2 - k1)}')}, so {m(f'a = {y}')} and {p} is {m(f'{k1} \\times {y} = {x_}')}.",
        ]
        verify = lambda v: Q(v) % k1 == 0 and Q(v) - t == k2 * (Q(v) / k1 - t)  # noqa: E731
        sols = [xx for yy in range(1, 60) for xx in [k1 * yy] if xx - t == k2 * (yy - t)]
        check = Q(sols[0])
    return _Prob(stem=stem, answer=Q(x_), fmt=num, section="AR", wrong=wrong, steps=steps,
                   near=_near(x_), verify=verify, check=check)


def _ca(c, v="a"):
    """'3a', but 'a' for a coefficient of 1."""
    return v if c == 1 else f"{c}{v}"


def _times(k):
    return {2: "twice", 3: "three times", 4: "four times", 5: "five times"}[k]


def _cap(s):
    return s[0].upper() + s[1:]


def _cap_num(s):
    """Sentences must not start with a math digit: '$4$ years ago' -> 'Four years ago'."""
    if s.startswith("$"):
        end = s.index("$", 1)
        n_ = int(s[1:end])
        if n_ < len(_WORDS):
            return _cap(_WORDS[n_]) + s[end + 1:]
    return s


@template("AR")
@_retrying
def fence_posts(rng, lvl):
    if lvl <= 2:
        kind = _fresh(rng, ["straight", "inclusive", "cuts"], "fence2")
    else:
        kind = _fresh(rng, ["loop", "both_sides", "cut_time", "clock"], "fence3")
    if kind == "straight":
        key = _fresh(rng, ["fence", "flags", "trees", "lights"], "straight")
        d = {"fence": rng.choice([4, 5, 6, 8, 10]), "flags": rng.choice([5, 10, 20]),
             "trees": rng.choice([10, 12, 15, 20]), "lights": rng.choice([25, 40, 50])}[key]
        n_gaps = rng.randint(6, 25)
        L = d * n_gaps
        stem = {
            "fence": f"A straight fence is {num(L)} feet long. There is a post every {num(d)} feet, including one at each end. How many posts are there?",
            "flags": f"For a parade, flags are placed every {num(d)} yards along a straight {num(L)}-yard route, with a flag at the start and one at the end. How many flags are used?",
            "trees": f"Trees are planted every {num(d)} feet along one side of a straight {num(L)}-foot sidewalk, with a tree at each end. How many trees are planted?",
            "lights": f"Light poles stand every {num(d)} meters along a straight {num(L)}-meter road on a base, with a pole at each end. How many light poles are there?",
        }[key]
        ans = n_gaps + 1
        wrong = [
            (Q(n_gaps), "counts the spaces between posts, not the posts"),
            (Q(n_gaps - 1), "leaves out the posts at both ends"),
            (Q(n_gaps + 2), None),
        ]
        steps = [
            f"Number of spaces: {m(f'{int_raw(L)} \\div {d} = {n_gaps}')}.",
            f"A straight line with a post at each end has one more post than spaces: "
            f"{m(f'{n_gaps} + 1 = {ans}')}.",
        ]
        tip = "Picture a short case: a 10-foot fence with posts every 5 feet has posts at 0, 5, and 10, which is 3 posts for 2 spaces."
        check = Q(len(range(0, L + 1, d)))
    elif kind == "inclusive":
        key = _fresh(rng, ["pages", "leave", "seats", "tickets"], "incl")
        a_ = rng.randint(3, 120)
        b_ = a_ + rng.randint(8, 80)
        if key == "leave":
            a_ = rng.randint(1, 12)
            b_ = a_ + rng.randint(6, 17)
            month = rng.choice(["June", "July", "August", "March", "October"])
            stem = (f"A soldier is on leave from {month} {a_} through {month} {b_}, counting both days. "
                    f"How many days of leave is that?")
        else:
            pp = person(rng)
            stem = {
                "pages": f"{pp} read pages {num(a_)} through {num(b_)} of a manual, including both of those pages. How many pages did {pp.he} read?",
                "seats": f"In a stadium row, seats are numbered in order. A group bought seats {num(a_)} through {num(b_)}. How many seats did they buy?",
                "tickets": f"Raffle tickets numbered {num(a_)} through {num(b_)} were sold. How many tickets were sold?",
            }[key]
        ans = b_ - a_ + 1
        wrong = [
            (Q(b_ - a_), "subtracts but forgets to count the first one"),
            (Q(b_ - a_ - 1), "leaves out both ends"),
            (Q(b_ - a_ + 2), None),
        ]
        steps = [
            f"Subtract: {m(f'{b_} - {a_} = {b_ - a_}')}. This counts the steps from the first to the last.",
            f"Both ends are included, so add 1: {m(f'{b_ - a_} + 1 = {ans}')}.",
        ]
        tip = "Check with a small case: pages 3 through 5 are pages 3, 4, 5, which is 3 pages, not 5 $-$ 3 $=$ 2."
        check = Q(len(range(a_, b_ + 1)))
    elif kind == "cuts":
        key = _fresh(rng, ["log", "pipe", "rope"], "cuts")
        piece = rng.choice([2, 3, 4, 5, 6])
        n_p = rng.randint(3, 10)
        L = piece * n_p
        stem = {
            "log": f"A {num(L)}-foot log is cut into {num(piece)}-foot pieces. How many cuts are needed?",
            "pipe": f"A plumber cuts a {num(L)}-foot pipe into equal pieces {num(piece)} feet long. How many cuts does the plumber make?",
            "rope": f"A {num(L)}-foot rope is cut into pieces {num(piece)} feet long for a rope bridge. How many cuts are made?",
        }[key]
        ans = n_p - 1
        wrong = [
            (Q(n_p), "gives the number of pieces, not the number of cuts"),
            (Q(n_p + 1), None),
            (Q(L // 2) if L // 2 not in (n_p, n_p - 1) else Q(n_p + 2), None),
        ]
        steps = [
            f"Number of pieces: {m(f'{L} \\div {piece} = {n_p}')}.",
            f"The last piece needs no cut of its own, so cuts $=$ pieces $- 1$: {m(f'{n_p} - 1 = {ans}')}.",
        ]
        tip = "One cut makes 2 pieces, two cuts make 3 pieces: always one fewer cut than pieces."
        check = Q(len([c for c in range(piece, L, piece)]))
    elif kind == "loop":
        key = _fresh(rng, ["field", "garden", "lot"], "loop")
        d = rng.choice([5, 8, 10, 12, 15, 20])
        a_, b_ = d * rng.randint(3, 12), d * rng.randint(2, 10)
        need(a_ != b_)
        P = 2 * (a_ + b_)
        stem = {
            "field": f"A rectangular training field is {num(a_)} feet long and {num(b_)} feet wide. Fence posts are placed every {num(d)} feet all the way around, with a post at each corner. How many posts are needed?",
            "garden": f"A rectangular garden is {num(a_)} feet by {num(b_)} feet. Stakes are placed every {num(d)} feet around its edge, including the corners. How many stakes are used?",
            "lot": f"A rectangular parking lot measures {num(a_)} feet by {num(b_)} feet. Lights are placed every {num(d)} feet around the edge, including one at each corner. How many lights are needed?",
        }[key]
        ans = P // d
        wrong = [
            (Q(ans + 1), "adds 1 as if it were a straight fence; around a closed loop the first and last posts are the same"),
            (Q(ans + 4), "adds an extra post at each corner"),
            (Q((a_ + b_) // d), "uses only two sides instead of the whole perimeter"),
            (Q(ans - 4), "leaves out the corner posts"),
        ]
        steps = [
            f"Perimeter: {m(f'2 \\times ({a_} + {b_}) = {int_raw(P)}')} feet.",
            f"Around a closed loop, posts $=$ spaces: {m(f'{int_raw(P)} \\div {d} = {ans}')}.",
        ]
        tip = "A loop has no loose end, so you do not add 1."
        pts = {(x_, 0) for x_ in range(0, a_ + 1, d)} | {(x_, b_) for x_ in range(0, a_ + 1, d)} | \
              {(0, y_) for y_ in range(0, b_ + 1, d)} | {(a_, y_) for y_ in range(0, b_ + 1, d)}
        check = Q(len(pts))
    elif kind == "both_sides":
        d = rng.choice([10, 15, 20, 25, 30, 50])
        n_gaps = rng.randint(5, 20)
        L = d * n_gaps
        stem = (f"Trees are planted on \\emph{{both}} sides of a straight {num(L)}-foot road, one every "
                f"{num(d)} feet, with a tree at each end on each side. How many trees are planted?")
        ans = 2 * (n_gaps + 1)
        wrong = [
            (Q(2 * n_gaps), "forgets the extra tree at the end of each side"),
            (Q(n_gaps + 1), "counts only one side of the road"),
            (Q(2 * n_gaps + 1), "adds only one extra tree for both sides"),
            (Q(2 * (n_gaps + 2)), None),
        ]
        steps = [
            f"Spaces on one side: {m(f'{int_raw(L)} \\div {d} = {n_gaps}')}, so one side has "
            f"{m(f'{n_gaps} + 1 = {n_gaps + 1}')} trees.",
            f"Two sides: {m(f'2 \\times {n_gaps + 1} = {ans}')} trees.",
        ]
        tip = None
        check = Q(2 * len(range(0, L + 1, d)))
    elif kind == "cut_time":
        piece = rng.choice([2, 3, 4, 5])
        n_p = rng.randint(4, 10)
        L = piece * n_p
        t = rng.choice([2, 3, 4, 5, 6])
        need(t not in (n_p - 1, n_p, piece))   # keep the numbers in the notes distinct
        key = _fresh(rng, ["log", "beam"], "cut_time")
        stem = ({"log": f"It takes {num(t)} minutes to make one cut through a log. How long will it take to cut a {num(L)}-foot log into {num(piece)}-foot pieces?",
                 "beam": f"A saw takes {num(t)} minutes to cut through a steel beam. How long will it take to cut a {num(L)}-foot beam into {num(n_p)} equal pieces?"}[key])
        ans = (n_p - 1) * t
        wrong = [
            (Q(n_p * t), "multiplies by the number of pieces instead of the number of cuts"),
            (Q((n_p + 1) * t), None),
            (Q(n_p - 1), "gives the number of cuts, not the time"),
            (Q(L * t), "multiplies the length by the time per cut"),
        ]
        steps = [
            f"Pieces: {num(n_p)}" + (f" ({m(f'{L} \\div {piece} = {n_p}')})" if key == "log" else "") +
            f". Cuts $=$ pieces $- 1$ $=$ {m(str(n_p - 1))}.",
            f"Time: {m(f'{n_p - 1} \\times {t} = {ans}')} minutes.",
        ]
        tip = None
        check = Q(len(range(piece, L, piece)) * t)
        return _Prob(stem=stem, answer=Q(ans), fmt=unit(num, "minute"), section="AR", wrong=wrong,
                       steps=steps, near=_near(ans), check=check)
    else:
        a_ = rng.choice([3, 4, 5, 6])
        sec = rng.choice([2, 3, 4, 6])
        span = (a_ - 1) * sec
        b_ = rng.choice([c for c in (6, 8, 9, 10, 12) if c > a_])
        ans = (b_ - 1) * sec
        stem = (f"A clock tower strikes {num(a_)} times at {a_} o'clock, and it takes {num(span)} seconds "
                f"from the first strike to the last. At the same pace, how many seconds does it take "
                f"to strike {num(b_)} times at {b_} o'clock?")
        wrong = [
            (R(span * b_, a_), "sets up a simple proportion with the number of strikes"),
            (Q(b_ * sec), "counts the strikes instead of the gaps between them"),
            (Q(span * 2) if span * 2 != ans else Q(ans + sec * 2), None),
        ]
        steps = [
            f"{num(a_)} strikes have {m(f'{a_} - 1 = {a_ - 1}')} gaps, so each gap is "
            f"{m(f'{span} \\div {a_ - 1} = {sec}')} seconds.",
            f"{num(b_)} strikes have {m(f'{b_} - 1 = {b_ - 1}')} gaps: {m(f'{b_ - 1} \\times {sec} = {ans}')} seconds.",
        ]
        tip = None
        check = Q(sec * len(range(1, b_)))
        return _Prob(stem=stem, answer=Q(ans), fmt=unit(num, "second"), section="AR", wrong=wrong,
                       steps=steps, near=_near(ans), check=check)
    return _Prob(stem=stem, answer=Q(ans), fmt=num, section="AR", wrong=wrong, steps=steps,
                   tip=tip, near=_near(ans), check=check)


_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


@template("AR")
@_retrying
def day_of_week(rng, lvl):
    kind = _fresh(rng, ["after", "day_n", "month", "ago"], "dow")
    d0 = rng.randrange(7)
    base = datetime.date(2024, 1, 1) + datetime.timedelta(days=d0)   # 2024-01-01 was a Monday
    if kind == "after":
        N = rng.randint(20, 200)
        need(N % 7 not in (0,))
        ans_i = (d0 + N) % 7
        ctx = _fresh(rng, ["today", "orders", "pay"], "after_ctx")
        stem = {
            "today": f"Today is {_DAYS[d0]}. What day of the week will it be {num(N)} days from today?",
            "orders": f"A soldier receives orders on a {_DAYS[d0]} to report in {num(N)} days. On what day of the week must the soldier report?",
            "pay": f"{person(rng)} starts a {num(N)}-day savings challenge on a {_DAYS[d0]}. The challenge ends {num(N)} days later. On what day of the week does it end?",
        }[ctx]
        q, r = divmod(N, 7)
        wrong = [
            (_DAYS[(ans_i + 1) % 7], "counts one day too many"),
            (_DAYS[(ans_i - 1) % 7], "counts one day too few"),
            (_DAYS[(d0 - r) % 7], "counts backward instead of forward"),
            (_DAYS[(d0 + q) % 7], f"moves ahead {q} days (the number of weeks) instead of {r}"),
        ]
        steps = [
            f"Every 7 days the day of the week repeats. {m(f'{N} \\div 7 = {q}')} weeks with "
            f"{m(str(r))} {_pl('day', r)} left over.",
            f"After {q} full weeks it is {_DAYS[d0]} again. Count {r} more {_pl('day', r)}: "
            + ", ".join(_DAYS[(d0 + i) % 7] for i in range(1, r + 1)) + ".",
        ]
        check = _DAYS[(base + datetime.timedelta(days=N)).weekday()]
    elif kind == "day_n":
        N = rng.randint(20, 180)
        need((N - 1) % 7 != 0)
        ans_i = (d0 + N - 1) % 7
        ctx = _fresh(rng, ["deploy", "course", "diet"], "dayn_ctx")
        stem = {
            "deploy": f"A deployment begins on a {_DAYS[d0]}, which is day 1. On what day of the week is day {num(N)} of the deployment?",
            "course": f"A training course starts on a {_DAYS[d0]} (day 1) and runs every day without a break. On what day of the week is day {num(N)}?",
            "diet": f"{person(rng)} starts a fitness plan on a {_DAYS[d0]}, which counts as day 1. On what day of the week is day {num(N)}?",
        }[ctx]
        q, r = divmod(N - 1, 7)
        wrong = [
            (_DAYS[(d0 + N) % 7], f"counts {N} days after day 1, but day {N} is only {N - 1} days later"),
            (_DAYS[(ans_i - 1) % 7], "counts one day too few"),
            (_DAYS[(d0 - r) % 7], "counts backward instead of forward"),
            (_DAYS[(ans_i + 2) % 7], None),
        ]
        steps = [
            f"Day {num(N)} is {m(f'{N} - 1 = {N - 1}')} days after day 1.",
            f"{m(f'{N - 1} \\div 7 = {q}')} weeks with {m(str(r))} {_pl('day', r)} left over, so move "
            f"{r} {_pl('day', r)} past {_DAYS[d0]}: {_DAYS[ans_i]}.",
        ]
        check = _DAYS[(base + datetime.timedelta(days=N - 1)).weekday()]
    elif kind == "month":
        a_ = rng.randint(1, 12)
        b_ = a_ + rng.randint(9, 28)
        need(b_ <= 31 and (b_ - a_) % 7 != 0)
        month = rng.choice(["March", "May", "July", "August", "October", "December"])
        ans_i = (d0 + b_ - a_) % 7
        stem = (f"{month} {a_} is a {_DAYS[d0]}. On what day of the week is {month} {b_}?")
        q, r = divmod(b_ - a_, 7)
        wrong = [
            (_DAYS[(ans_i + 1) % 7], "counts one day too many"),
            (_DAYS[(ans_i - 1) % 7], "counts one day too few"),
            (_DAYS[(d0 - r) % 7], "counts backward instead of forward"),
            (_DAYS[(d0 + b_) % 7], f"counts {b_} days instead of the {b_ - a_} days between the dates"),
        ]
        steps = [
            f"{month} {b_} is {m(f'{b_} - {a_} = {b_ - a_}')} days after {month} {a_}.",
            f"{m(f'{b_ - a_} \\div 7 = {q}')} weeks with {m(str(r))} {_pl('day', r)} left over: "
            f"{r} {_pl('day', r)} after {_DAYS[d0]} is {_DAYS[ans_i]}.",
        ]
        check = _DAYS[(base + datetime.timedelta(days=b_ - a_)).weekday()]
    else:
        N = rng.randint(15, 120)
        need(N % 7 != 0)
        ans_i = (d0 - N) % 7
        pp = person(rng)
        stem = (f"Today is {_DAYS[d0]}. {pp} enlisted exactly {num(N)} days ago. On what day "
                f"of the week did {pp.he} enlist?")
        q, r = divmod(N, 7)
        wrong = [
            (_DAYS[(d0 + r) % 7], "counts forward instead of backward"),
            (_DAYS[(ans_i + 1) % 7], "counts one day too few"),
            (_DAYS[(ans_i - 1) % 7], "counts one day too many"),
            (_DAYS[(d0 - q) % 7], f"moves back {q} days (the number of weeks) instead of {r}"),
        ]
        steps = [
            f"{m(f'{N} \\div 7 = {q}')} weeks with {m(str(r))} {_pl('day', r)} left over. "
            f"{q} weeks ago was also a {_DAYS[d0]}.",
            f"Go back {r} more {_pl('day', r)}: "
            + ", ".join(_DAYS[(d0 - i) % 7] for i in range(1, r + 1)) + ".",
        ]
        check = _DAYS[(base - datetime.timedelta(days=N)).weekday()]
    ans = _DAYS[ans_i]
    seen_ = {ans}
    wl = []
    for w in wrong:
        if w[0] not in seen_:
            seen_.add(w[0])
            wl.append(w)
    return _Prob(stem=stem, answer=ans, fmt=text, section="AR", wrong=wl, steps=steps,
                   check=check, sort=False)


PLAN = [
    # level 1: warm-ups (10)
    (us_length, 1, 2),
    (capacity_weight, 1, 2),
    (metric_convert, 1, 2),
    (elapsed_time, 1, 2),
    (mixed_units, 1, 1),
    (round_up_down, 1, 1),
    # level 2: test level (14)
    (us_length, 2, 1),
    (capacity_weight, 2, 1),
    (metric_convert, 2, 1),
    (us_metric, 2, 2),
    (military_time, 2, 2),
    (mixed_units, 2, 2),
    (round_up_down, 2, 2),
    (fraction_remainder, 2, 1),
    (fence_posts, 2, 1),
    (age_problem, 2, 1),
    # level 3: challenge (11)
    (fence_posts, 3, 2),
    (day_of_week, 3, 2),
    (age_problem, 3, 2),
    (fraction_remainder, 3, 2),
    (military_time, 3, 2),
    (round_up_down, 3, 1),
]
