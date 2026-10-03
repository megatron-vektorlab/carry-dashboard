"""Chapter 25 - Work Rates & Mixtures (Part IV word problems)."""
import functools
import math
from fractions import Fraction

import sympy as sp

from ..core import (R, Q, Problem, Reject, need, num, dec, pct, money, unit, m, F,
                    dec_raw, int_raw, frac_raw, mixed_raw, people, soldier,
                    template, x as X)

NUM = 25
TITLE = r"Work Rates \& Mixtures"
PART = 4

INTRO = r"""
Work and mixture problems look different, but both are about \emph{rates and
totals}: how much of a job gets done each hour, or how much of an ingredient
is in each gallon. Set up the totals carefully and the arithmetic stays short.

\begin{concept}{Work rates}
If a job takes $t$ hours, the worker does $\frac{1}{t}$ of the job per hour.
\begin{itemize}
\item Working together, \textbf{rates add}: $\frac{1}{a} + \frac{1}{b} =
  \frac{1}{T}$, where $T$ is the time together. Then flip: time $= 1 \div
  \text{rate}$.
\item Two-worker shortcut (product over sum): $T = \dfrac{a \times b}{a + b}$.
  For $3$~h and $6$~h: $\frac{18}{9} = 2$~h.
\item A drain or a leak works against you: \textbf{subtract} its rate.
\item To find one worker's time from the time together, subtract rates:
  $\frac{1}{b} = \frac{1}{T} - \frac{1}{a}$.
\end{itemize}
\end{concept}

\begin{concept}{Equal workers: worker-hours}
Total work $=$ number of workers $\times$ time. If 6 workers need 8 days, the
job is $6 \times 8 = 48$ worker-days, so 4 workers need $48 \div 4 = 12$ days.
\emph{More} workers means \emph{less} time (an inverse proportion).
\end{concept}

\begin{concept}{Mixtures}
\[ \text{amount of pure ingredient} = \text{percent} \times \text{total amount} \]
\begin{itemize}
\item When two mixtures are combined, the pure amounts add and the totals add.
\item Adding water raises the total but does \emph{not} change the pure amount.
\item Price mixtures work the same way: total cost $\div$ total pounds $=$
  price per pound.
\end{itemize}
\end{concept}

\begin{example}{Worked example}
How many liters of a 50\% antifreeze solution must be added to 10 liters of a
20\% solution to make a 30\% solution?

\textbf{Solution.} Let $x$ be the liters of 50\% solution. The pure antifreeze
going in equals the pure antifreeze in the mixture:
$0.20(10) + 0.50x = 0.30(10 + x)$, so $2 + 0.5x = 3 + 0.3x$. Then $0.2x = 1$
and $x = 5$ liters. \emph{Check:} $2 + 2.5 = 4.5$ liters of antifreeze in
$15$ liters, and $4.5 \div 15 = 0.30 = 30\%$.
\end{example}

\begin{tip}
Sanity checks save points. Two workers together must be \emph{faster} than
the faster one alone (3~h and 6~h together: less than 3~h). A mixture's percent
or price must land \emph{between} the two ingredients, closer to the one you
use more of.
\end{tip}

\begin{trap}
\begin{itemize}
\item Averaging or adding the times: 3~h and 6~h together is 2~h, not
  4.5~h or 9~h.
\item Treating workers as a direct proportion: fewer workers need \emph{more}
  time, not less.
\item Taking the simple average of two percents or prices when the amounts
  are different.
\item Answering with the final amount when the question asks how much
  water (or how much of one ingredient) to \emph{add}.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# private helpers
# --------------------------------------------------------------------------

def _plural(word, v):
    return word if Q(v) == 1 else word + "s"


def _dur_text(v, base):
    """Time value in hours (base='hour') or minutes -> '2 hours 24 minutes'."""
    v = sp.Rational(Q(v))
    mins = v * 60 if base == "hour" else v
    need(mins.is_integer and mins > 0, "time is not a whole number of minutes")
    mins = int(mins)
    h, mm = divmod(mins, 60) if base == "hour" else (0, mins)
    parts = []
    if h:
        parts.append(f"{m(int_raw(h))}~{_plural('hour', h)}")
    if mm:
        parts.append(f"{m(int_raw(mm))}~{_plural('minute', mm)}")
    return " ".join(parts)


def _hours(v):
    return _dur_text(v, "hour")


def _minutes(v):
    return _dur_text(v, "minute")


def _rate_sum_raw(times, L):
    """'\\frac{1}{3} + \\frac{1}{6} = \\frac{2}{6} + \\frac{1}{6} = \\frac{3}{6} = \\frac{1}{2}'."""
    s = sum(L // t for t in times)
    out = " + ".join(F(1, t) for t in times) + " = " + " + ".join(F(L // t, L) for t in times)
    out += " = " + F(s, L)
    if math.gcd(s, L) != 1:
        out += " = " + frac_raw(R(s, L))
    return out


def _flip_steps(T, base, who="they"):
    """Steps that turn a combined rate 1/T into a time T (with minutes)."""
    T = sp.Rational(T)
    rate = 1 / T
    u = base
    first = (f"Time $=$ 1 job $\\div$ rate: "
             f"{m('1 \\div ' + frac_raw(rate) + ' = ' + frac_raw(T) + (' = ' + mixed_raw(T) if T.q != 1 and T > 1 else ''))}"
             f" {_plural(u, T)}.")
    if T.q == 1 or base == "minute":
        return [first]
    whole = T.p // T.q
    part = T - whole
    mins = part * 60
    return [first,
            f"Change the fraction of an hour to minutes: "
            f"{m(frac_raw(part) + ' \\times 60 = ' + int_raw(mins))} minutes. "
            f"So {who} need {_hours(T)}."]


_LAST = ["Ruiz", "Chen", "Walker", "Okafor", "Patel", "Novak", "Brooks", "Kim", "Santos",
         "Reyes", "Jensen", "Haddad", "Lopez", "Nguyen", "Carter", "Murphy"]
_BRANCH_RANKS = [["Private", "Specialist", "Corporal", "Sergeant"],
                 ["Private", "Lance Corporal", "Corporal", "Sergeant"]]


def _squadmates(rng, k=2):
    """k soldiers from the same branch with different last names."""
    ranks = rng.choice(_BRANCH_RANKS)
    return [f"{rng.choice(ranks)} {last}" for last in rng.sample(_LAST, k)]


def _near(ans, step=None, money_=False):
    """Plausible filler values around the answer (no silly x10 values)."""
    A = Q(ans)

    def f(rng):
        st = step
        if st is None:
            if money_:
                st = R(1, 4) if A < 10 else R(1, 2)
            elif A.is_integer:
                st = next(s_ for lim, s_ in ((12, 1), (30, 2), (80, 5), (200, 10), (600, 25),
                                              (10 ** 9, 100)) if A <= lim)
            else:
                st = R(1, sp.Rational(A).q)
        out = [A + k_ * st for k_ in (1, 2, 3, -1, -2, -3)]
        out = [v for v in out if v > 0]
        rng.shuffle(out)
        return out
    return f


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


def _cap(t):
    return t[0].upper() + t[1:]


def _pairs(lo, hi, cond):
    return [(a, b) for a in range(lo, hi + 1) for b in range(a + 1, hi + 1) if cond(a, b)]


def _friendly_T(T):
    T = sp.Rational(T)
    return T.q in (1, 2, 3, 4, 5, 6) and (T * 60).is_integer


# --------------------------------------------------------------------------
# work rates
# --------------------------------------------------------------------------

_TOGETHER = {
    # key: (base unit, lo, hi)
    "paint": ("hour", 8, 30),
    "pump": ("hour", 2, 15),
    "sandbag": ("hour", 2, 12),
    "clerk": ("hour", 2, 12),
    "plow": ("hour", 2, 12),
    "mow": ("minute", 20, 90),
    "print": ("minute", 10, 60),
    "unload": ("minute", 20, 90),
}


def _together_stem(rng, key, t1, t2):
    """Stem for two workers + labels used in the solution."""
    if key == "paint":
        p1, p2 = people(rng, 2)
        return (f"{p1} can paint the outside of a house in {num(t1)} hours. {p2} can paint "
                f"the same house in {num(t2)} hours. If they work together, how long will it "
                f"take them to paint the house?", p1.name, p2.name)
    if key == "pump":
        return (f"One pump can empty a flooded basement in {num(t1)} hours. A second pump can "
                f"empty it in {num(t2)} hours. How long will it take to empty the basement if "
                f"both pumps run at the same time?", "the first pump", "the second pump")
    if key == "sandbag":
        s1, s2 = _squadmates(rng)
        return (f"Working alone, {s1} can fill the sandbags for a fighting position in "
                f"{num(t1)} hours. {s2} needs {num(t2)} hours to do the same job alone. "
                f"How long will the job take if they work together?", s1, s2)
    if key == "clerk":
        return (f"At a recruiting station, one clerk can enter a stack of enlistment forms into "
                f"the computer in {num(t1)} hours. A second clerk can enter the same stack in "
                f"{num(t2)} hours. How long will it take the two clerks working together?",
                "the first clerk", "the second clerk")
    if key == "plow":
        return (f"One snowplow can clear a shopping-center parking lot in {num(t1)} hours. A "
                f"second plow can clear it in {num(t2)} hours. How long will the job take if "
                f"both plows work at the same time?", "the first plow", "the second plow")
    if key == "mow":
        p1, p2 = people(rng, 2)
        return (f"{p1} can mow a large lawn in {num(t1)} minutes, and {p2} can mow it in "
                f"{num(t2)} minutes. If they use two mowers and work together, how long will "
                f"it take them to mow the lawn?", p1.name, p2.name)
    if key == "print":
        return (f"An older printer can print the programs for a graduation ceremony in "
                f"{num(max(t1, t2))} minutes. A newer printer can print them in "
                f"{num(min(t1, t2))} minutes. If the two printers share the job, how long "
                f"will it take?", "the older printer", "the newer printer")
    if key == "unload":
        return (f"First squad can unload a supply truck in {num(t1)} minutes. Second squad can "
                f"unload the same truck in {num(t2)} minutes. How long will it take if both "
                f"squads work together?", "first squad", "second squad")
    raise KeyError(key)


@template("AR")
@_retrying
def work_together(rng, lvl):
    if lvl == 3:
        return _three_workers(rng)
    key = _fresh(rng, list(_TOGETHER), "together")
    base, lo, hi = _TOGETHER[key]
    if lvl == 1:
        cond = lambda a, b: (a * b) % (a + b) == 0 and math.lcm(a, b) <= 60  # noqa: E731
    elif base == "hour":
        cond = lambda a, b: (math.lcm(a, b) <= 60 and (a * b) % (a + b) != 0  # noqa: E731
                             and _friendly_T(R(a * b, a + b)))
    else:
        cond = lambda a, b: (a * b) % (a + b) == 0 and 60 < math.lcm(a, b) <= 180  # noqa: E731
    pairs = _pairs(lo, hi, cond)
    need(pairs)
    a, b = rng.choice(pairs)
    t1, t2 = (a, b) if (key == "print" or rng.random() < 0.5) else (b, a)
    stem, lab1, lab2 = _together_stem(rng, key, t1, t2)
    if key == "print":
        lab1, lab2 = ("the newer printer", "the older printer")
        t1, t2 = a, b
    T = R(a * b, a + b)
    L = math.lcm(a, b)
    fmt = _hours if base == "hour" else _minutes
    u = base
    steps = [
        f"Turn each time into a rate (the part of the job done in one {u}): "
        f"{lab1} does {m(F(1, t1))} of the job per {u}, and {lab2} does {m(F(1, t2))}.",
        f"Add the rates (common denominator {L}): {m(_rate_sum_raw([t1, t2], L))} "
        f"of the job per {u}.",
    ] + _flip_steps(T, base)
    tip = ((f"Product over sum: {m(F(f'{a} \\times {b}', f'{a} + {b}') + ' = ' + F(a * b, a + b) + ' = ' + mixed_raw(T))}. "
            if a * b <= 300 else "")
           + f"The answer must be less than the faster time, {num(a)} {_plural(u, a)}.")
    return Problem(
        stem=stem,
        answer=T,
        fmt=fmt,
        section="AR",
        wrong=[
            (R(a + b, 2), "averages the two times"),
            (Q(a + b), "adds the two times instead of adding the two rates"),
            (R(a, 2), "halves the faster time, as if both worked as fast as the faster one"),
            (R(a + b, 4), "halves the average of the two times"),
            (1 / T, "stops at the combined rate and forgets to flip it into a time"),
            (Q(b - a), "subtracts the two times"),
        ],
        steps=steps,
        tip=tip,
        check=sp.solve(sp.Eq(X / a + X / b, 1), X)[0],
        verify=lambda t: Fraction(int(sp.Rational(t).p), int(sp.Rational(t).q)) * (Fraction(1, a) + Fraction(1, b)) == 1,
    )


def _three_workers(rng):
    key = _fresh(rng, ["paint", "pump", "sandbag", "fuel"], "three")
    hi = {"paint": 30, "pump": 15, "sandbag": 15, "fuel": 24}[key]
    lo = 6 if key == "paint" else 2
    triples = [(a, b, c) for a in range(lo, hi + 1) for b in range(a + 1, hi + 1)
               for c in range(b + 1, hi + 1)
               if math.lcm(a, b, c) <= 60 and _friendly_T(R(a * b * c, a * b + b * c + a * c))]
    need(triples)
    a, b, c = rng.choice(triples)
    T = 1 / (R(1, a) + R(1, b) + R(1, c))
    L = math.lcm(a, b, c)
    order = [a, b, c]
    rng.shuffle(order)
    t1, t2, t3 = order
    if key == "paint":
        p1, p2, p3 = people(rng, 3)
        stem = (f"Working alone, {p1} can paint the outside of a house in {num(t1)} hours, {p2} "
                f"in {num(t2)} hours, and {p3} in {num(t3)} hours. How long will the job take "
                f"if all three paint together?")
    elif key == "pump":
        stem = (f"Three pumps are set up to empty a flooded basement. Working alone, they would "
                f"take {num(t1)} hours, {num(t2)} hours, and {num(t3)} hours. How long will it "
                f"take to empty the basement with all three pumps running?")
    elif key == "sandbag":
        stem = (f"Three squads are filling sandbags for a checkpoint. Working alone, first squad "
                f"would finish in {num(t1)} hours, second squad in {num(t2)} hours, and third "
                f"squad in {num(t3)} hours. How long will it take if all three squads work "
                f"together?")
    else:
        stem = (f"At a forward operating base, a large fuel bladder can be filled by any of three "
                f"pumps. Working alone, the pumps would take {num(t1)} hours, {num(t2)} hours, "
                f"and {num(t3)} hours. How long will it take to fill the bladder if all three "
                f"pumps run at once?")
    steps = [
        f"Each rate is 1 job divided by the time alone: {m(F(1, t1))}, {m(F(1, t2))}, and "
        f"{m(F(1, t3))} of the job per hour.",
        f"Add the three rates (common denominator {L}): {m(_rate_sum_raw([t1, t2, t3], L))} "
        f"of the job per hour.",
    ] + _flip_steps(T, "hour")
    return Problem(
        stem=stem,
        answer=T,
        fmt=_hours,
        section="AR",
        wrong=[
            (R(a + b + c, 3), "averages the three times"),
            (Q(a + b + c), "adds the three times instead of adding the rates"),
            (R(a, 3), "divides the fastest time by 3, as if all three were that fast"),
            (R(a * b, a + b), "leaves out the slowest worker"),
            (1 / T, "stops at the combined rate and forgets to flip it into a time"),
        ],
        steps=steps,
        tip=f"Check: the answer must be less than the fastest time alone, {num(a)} hours.",
        check=sp.solve(sp.Eq(X / a + X / b + X / c, 1), X)[0],
    )


@template("AR")
@_retrying
def work_find_one(rng, lvl):
    if lvl >= 3:
        return _speed_ratio(rng)
    pairs = _pairs(2, 24, lambda a, b: (a * b) % (a + b) == 0 and a * b // (a + b) >= 2
                   and math.lcm(a, b) <= 72)
    a, b = rng.choice(pairs)          # a faster, b slower
    T = a * b // (a + b)
    known_fast = rng.random() < 0.5
    known, ans = (a, b) if known_fast else (b, a)
    key = _fresh(rng, ["fence", "rifles", "pond", "fuel", "envelopes", "inventory"], "findone")
    if key == "fence":
        p1, p2 = people(rng, 2)
        stem = (f"Working together, {p1} and {p2} can paint a fence in {num(T)} hours. Working "
                f"alone, {p1} can paint it in {num(known)} hours. How long would it take {p2} "
                f"to paint the fence alone?")
        lk, lu = p1.name, p2.name
    elif key == "rifles":
        s1, s2 = _squadmates(rng)
        stem = (f"Working together, {s1} and {s2} can clean all of the squad's rifles in "
                f"{num(T)} hours. {s1} could do the job alone in {num(known)} hours. How long "
                f"would it take {s2} working alone?")
        lk, lu = s1, s2
    elif key == "pond":
        big = known_fast
        stem = (f"Two pumps working together can drain a pond in {num(T)} hours. The "
                f"{'larger' if big else 'smaller'} pump alone would take {num(known)} hours. "
                f"How long would the {'smaller' if big else 'larger'} pump take alone?")
        lk, lu = (("the larger pump", "the smaller pump") if big
                  else ("the smaller pump", "the larger pump"))
    elif key == "fuel":
        stem = (f"Two fuel pumps working together can fill the storage tanks at a forward "
                f"operating base in {num(T)} hours. One of the pumps alone would take "
                f"{num(known)} hours. How long would the other pump take alone?")
        lk, lu = "the first pump", "the other pump"
    elif key == "envelopes":
        p1, p2 = people(rng, 2)
        stem = (f"{p1} and {p2} are stuffing envelopes for a charity mailing. Together they "
                f"can finish in {num(T)} hours. Alone, {p1} would need {num(known)} hours. "
                f"How many hours would {p2} need alone?")
        lk, lu = p1.name, p2.name
    else:
        stem = (f"Two supply clerks can inventory a warehouse together in {num(T)} hours. "
                f"Working alone, the first clerk needs {num(known)} hours. How long would the "
                f"second clerk need working alone?")
        lk, lu = "the first clerk", "the second clerk"
    L = math.lcm(T, known)
    diff = L // T - L // known
    rate_raw = F(1, T) + " - " + F(1, known) + " = " + F(L // T, L) + " - " + F(L // known, L) \
        + " = " + F(diff, L) + (" = " + frac_raw(R(diff, L)) if math.gcd(diff, L) != 1 else "")
    return Problem(
        stem=stem,
        answer=Q(ans),
        fmt=unit(num, "hour"),
        section="AR",
        wrong=[
            (Q(abs(known - T)), "subtracts the times instead of the rates"),
            (Q(2 * T), "assumes the two work at the same speed"),
            (R(known * T, known + T), "uses the product-over-sum shortcut, which is for combining two workers"),
            (Q(known + T), "adds the two times"),
        ],
        steps=[
            f"Rates: together they do {m(F(1, T))} of the job per hour, and {lk} alone does "
            f"{m(F(1, known))} of the job per hour.",
            f"{_cap(lu)}'s rate is the difference: {m(rate_raw)} of the job per hour.",
            f"Doing {m(frac_raw(R(1, ans)))} of the job each hour, {lu} needs {num(ans)} hours alone.",
        ],
        tip=(f"Check: {m(F(1, known) + ' + ' + F(1, ans) + ' = ' + frac_raw(R(1, T)))}, the "
             f"rate together. \\checkmark"),
        near=_near(ans),
        verify=lambda v: R(1, known) + 1 / Q(v) == R(1, T),
        check=sp.solve(sp.Eq(R(1, known) + 1 / X, R(1, T)), X)[0],
    )


def _speed_ratio(rng):
    k = rng.choice([2, 2, 3, 3, 4])
    word = {2: "twice", 3: "three times", 4: "four times"}[k]
    T = rng.randint(2, 10)
    slow = (k + 1) * T
    fast = R((k + 1) * T, k)
    need(_friendly_T(fast) and slow <= 48)
    ask_fast = rng.random() < 0.5
    key = _fresh(rng, ["recruit", "mower", "pump", "forklift", "printer", "crew"], "speed")
    if key == "recruit":
        s = soldier(rng)
        lf, ls = s, "the recruit"
        stem = (f"{s} can fill sandbags {word} as fast as a new recruit. Working together, "
                f"they can fill the sandbags for a bunker in {num(T)} hours. How long would it "
                f"take {s if ask_fast else 'the recruit'} to do the job alone?")
    elif key == "mower":
        lf, ls = "the riding mower", "the push mower"
        stem = (f"A riding mower cuts grass {word} as fast as a push mower. Using both mowers "
                f"at the same time, two groundskeepers, one on each mower, can mow a park in {num(T)} hours. How long "
                f"would it take using only the {'riding' if ask_fast else 'push'} mower?")
    elif key == "pump":
        lf, ls = "the new pump", "the old pump"
        stem = (f"A new pump moves water {word} as fast as an old pump. Running together, the "
                f"two pumps can fill a water tank in {num(T)} hours. How long would the "
                f"{'new' if ask_fast else 'old'} pump take to fill the tank alone?")
    elif key == "forklift":
        lf, ls = "the experienced driver", "the trainee"
        stem = (f"At a supply depot, an experienced forklift driver works {word} as fast as a "
                f"trainee. Together they can unload a cargo container in {num(T)} hours. How "
                f"long would it take the {'experienced driver' if ask_fast else 'trainee'} "
                f"working alone?")
    elif key == "printer":
        lf, ls = "the new copier", "the old copier"
        stem = (f"A print shop's new copier works {word} as fast as its old copier. Running "
                f"together, the two copiers can finish a large order in {num(T)} hours. How long "
                f"would the order take on the {'new' if ask_fast else 'old'} copier alone?")
    else:
        lf, ls = "the large crew", "the small crew"
        stem = (f"A large landscaping crew works {word} as fast as a small crew. Together the two "
                f"crews can plant all the trees in a new park in {num(T)} hours. How long would "
                f"the {'large' if ask_fast else 'small'} crew take working alone?")
    ans = fast if ask_fast else Q(slow)
    other = Q(slow) if ask_fast else fast
    steps = [
        f"Let {ls} do {m('r')} of the job per hour. Then {lf} does {m(f'{k}r')}, and together "
        f"they do {m(f'r + {k}r = {k + 1}r')} per hour.",
        f"Together they finish in {num(T)} hours, so {m(f'{k + 1}r = {F(1, T)}')} and "
        f"{m(f'r = {F(1, (k + 1) * T)}')}. So {ls} alone needs {num(slow)} hours.",
    ]
    if ask_fast:
        frac_word = {2: "half", 3: "one third", 4: "one fourth"}[k]
        steps.append(f"Working {word} as fast, {lf} needs {frac_word} of that time: "
                     f"{m(f'{slow} \\div {k} = ' + mixed_raw(fast))} hours"
                     + (f", which is {_hours(fast)}." if not fast.is_integer else "."))
    return Problem(
        stem=stem,
        answer=ans,
        fmt=_hours,
        section="AR",
        wrong=[
            (other, f"is the time for {ls if ask_fast else lf}, not the one asked about"),
            (Q(2 * T), "assumes the two work at the same speed"),
            (Q(k * T) if ask_fast else R(T, k), "only multiplies or divides the time together by the speed ratio"),
            (Q(T), "gives the time for both working together"),
        ],
        steps=steps,
        tip=f"Check: rates {m(frac_raw(1 / fast) + ' + ' + frac_raw(R(1, slow)) + ' = ' + F(1, T))} of the job per hour. \\checkmark",
        near=_near(ans),
        verify=lambda v: (Q(v) == fast) if ask_fast else (Q(v) == slow),
        check=(sp.solve(sp.Eq(T / X + T * k / X, 1), X)[0] / (k if ask_fast else 1)),
    )


_FILL = {
    # key: (base, a lo, a hi, b hi)
    "pool": ("hour", 2, 12, 24),
    "tank": ("hour", 2, 12, 24),
    "cistern": ("hour", 2, 12, 24),
    "tub": ("minute", 6, 20, 40),
    "trailer": ("minute", 10, 30, 60),
    "sink": ("minute", 2, 8, 20),
    "kiddie": ("minute", 10, 30, 90),
}


def _fill_stem(key, a, b):
    """(stem, filler label, drain label, container word)."""
    return {
        "pool": (f"A fill pipe can fill an empty swimming pool in {num(a)} hours. The pool's "
                 f"drain can empty a full pool in {num(b)} hours. The pool is empty, and by "
                 f"mistake the drain is left open while the pipe fills the pool. How long will "
                 f"it take to fill the pool?", "the pipe", "the drain", "pool"),
        "tank": (f"A pump can fill an empty water tank at a base camp in {num(a)} hours. The "
                 f"tank has a leak that would empty a full tank in {num(b)} hours. If the "
                 f"pump fills the empty tank while it leaks, how long will it take to fill?",
                 "the pump", "the leak", "tank"),
        "cistern": (f"A pump can fill an empty fuel bladder at a forward operating base in "
                    f"{num(a)} hours. A damaged valve would let a full bladder drain in "
                    f"{num(b)} hours. If the valve is not fixed, how long will it take the pump "
                    f"to fill the empty bladder?", "the pump", "the valve", "bladder"),
        "tub": (f"A bathtub faucet can fill the tub in {num(a)} minutes. With the plug "
                f"pulled, the drain empties a full tub in {num(b)} minutes. If the faucet is "
                f"turned on with the plug pulled, how long will it take to fill the tub?",
                "the faucet", "the drain", "tub"),
        "trailer": (f"A hose can fill an empty water trailer in {num(a)} minutes. A loose valve "
                    f"would let a full trailer drain in {num(b)} minutes. If the valve is not "
                    f"fixed, how long will it take the hose to fill the empty trailer?",
                    "the hose", "the valve", "trailer"),
        "sink": (f"A kitchen faucet fills a large sink in {num(a)} minutes. The drain, if left "
                 f"open, empties a full sink in {num(b)} minutes. If the drain is left open, how "
                 f"long will it take the faucet to fill the empty sink?",
                 "the faucet", "the drain", "sink"),
        "kiddie": (f"A garden hose can fill a backyard wading pool in {num(a)} minutes. The pool "
                   f"has a small hole that would let a full pool drain in {num(b)} minutes. How "
                   f"long will it take the hose to fill the empty pool?",
                   "the hose", "the hole", "pool"),
    }[key]


@template("AR")
@_retrying
def fill_and_drain(rng, lvl):
    if lvl >= 3:
        return _two_in_one_out(rng)
    key = _fresh(rng, list(_FILL), "fill")
    base, lo, hi, bhi = _FILL[key]
    u = base
    fmt = _hours if base == "hour" else _minutes
    pairs = [(a, b) for a in range(lo, hi + 1) for b in range(a + 1, bhi + 1)
             if (a * b) % (b - a) == 0 and a * b // (b - a) <= (24 if base == "hour" else 90)
             and math.lcm(a, b) <= 72]
    a, b = rng.choice(pairs)
    T = R(a * b, b - a)
    L = math.lcm(a, b)
    stem, lf, ld, cont = _fill_stem(key, a, b)
    net = L // a - L // b
    steps = [
        f"Rates: {lf} fills {m(F(1, a))} of the {cont} per {u}, and {ld} empties "
        f"{m(F(1, b))} of it per {u}.",
        f"{_cap(ld)} works against {lf}, so \\emph{{subtract}}: "
        f"{m(F(1, a) + ' - ' + F(1, b) + ' = ' + F(L // a, L) + ' - ' + F(L // b, L) + ' = ' + F(net, L) + (' = ' + frac_raw(R(net, L)) if math.gcd(net, L) != 1 else ''))} "
        f"of the {cont} per {u}.",
        f"Time $=$ 1 {cont} $\\div$ rate $=$ {m('1 \\div ' + frac_raw(1 / T) + ' = ' + int_raw(T))} {_plural(u, T)}.",
    ]
    wrong = [
        (R(a * b, a + b), f"adds {ld}'s rate instead of subtracting it"),
        (Q(b - a), "subtracts the two times"),
        (Q(a), f"ignores {ld}"),
        (Q(a + b), "adds the two times"),
        (1 / T, "stops at the net rate and forgets to flip it into a time"),
    ]
    return Problem(stem=stem, answer=T, fmt=fmt, section="AR", wrong=wrong, steps=steps,
                   near=_near(T),
                   tip=(f"Shortcut for fill and drain: {m(F(f'{a} \\times {b}', f'{b} - {a}') + ' = ' + F(a * b, b - a) + ' = ' + int_raw(T))}."
                        if a * b <= 300 else None),
                   check=sp.solve(sp.Eq(X / a - X / b, 1), X)[0])


def _two_in_one_out(rng):
    trip = [(a, b, c) for a in range(2, 16) for b in range(a + 1, 21) for c in range(2, 31)
            if c not in (a, b) and math.lcm(a, b, c) <= 72
            and R(1, a) + R(1, b) - R(1, c) > 0
            and (1 / (R(1, a) + R(1, b) - R(1, c))).is_integer
            and 1 / (R(1, a) + R(1, b) - R(1, c)) <= 30]
    a, b, c = rng.choice(trip)
    T = 1 / (R(1, a) + R(1, b) - R(1, c))
    L = math.lcm(a, b, c)
    i1, i2 = (a, b) if rng.random() < 0.5 else (b, a)
    key = _fresh(rng, ["fuel", "pool", "farm", "reservoir", "ship"], "fill3")
    stem = {
        "fuel": (f"Two pumps are filling an empty fuel bladder at a forward operating base. Alone, "
                 f"one pump would fill it in {num(i1)} hours and the other in {num(i2)} hours. A "
                 f"damaged valve leaks fuel and would empty a full bladder in {num(c)} hours. With "
                 f"both pumps running and the valve leaking, how long will it take to fill the "
                 f"bladder?"),
        "pool": (f"A swimming pool has two fill pipes. One alone can fill the empty pool in "
                 f"{num(i1)} hours, and the other alone in {num(i2)} hours. The drain can empty a "
                 f"full pool in {num(c)} hours. If both pipes are on and the drain is open, how "
                 f"long will it take to fill the empty pool?"),
        "farm": (f"Two pipes feed a water tank on a farm. One pipe alone fills the empty tank in "
                 f"{num(i1)} hours, and the other alone in {num(i2)} hours. An outlet pipe used for "
                 f"irrigation drains a full tank in {num(c)} hours. With all three pipes open, how "
                 f"long will it take to fill the empty tank?"),
        "reservoir": (f"Two pumps fill a water storage tank at a base camp. Working alone, they would "
                      f"take {num(i1)} hours and {num(i2)} hours. Meanwhile, the camp uses water at "
                      f"a rate that would empty a full tank in {num(c)} hours. Starting with an empty "
                      f"tank, how long will it take to fill it?"),
        "ship": (f"A ship's ballast tank can be filled by either of two pumps: one alone takes "
                 f"{num(i1)} hours and the other {num(i2)} hours. A stuck valve lets water out and "
                 f"would empty a full tank in {num(c)} hours. With both pumps on, how long will it "
                 f"take to fill the empty tank?"),
    }[key]
    net = L // i1 + L // i2 - L // c
    ins, out, cont = {"fuel": ("pumps", "leak", "bladder"), "pool": ("fill pipes", "drain", "pool"),
                      "farm": ("feed pipes", "outlet pipe", "tank"),
                      "reservoir": ("pumps", "camp's water use", "tank"),
                      "ship": ("pumps", "stuck valve", "tank")}[key]
    steps = [
        f"Rates per hour: the {ins} add {m(F(1, i1))} and {m(F(1, i2))} of the {cont}; "
        f"the {out} takes away {m(F(1, c))}.",
        f"Net rate (common denominator {L}): "
        f"{m(F(1, i1) + ' + ' + F(1, i2) + ' - ' + F(1, c) + ' = ' + F(L // i1, L) + ' + ' + F(L // i2, L) + ' - ' + F(L // c, L) + ' = ' + F(net, L) + (' = ' + frac_raw(R(net, L)) if math.gcd(net, L) != 1 else ''))} "
        f"of the {cont} per hour.",
        f"Time $=$ 1 {cont} $\\div$ rate $=$ {m('1 \\div ' + frac_raw(1 / T) + ' = ' + int_raw(T))} hours.",
    ]
    return Problem(
        stem=stem, answer=T, fmt=_hours, section="AR",
        wrong=[
            (R(a * b, a + b), f"ignores the {out}"),
            (1 / (R(1, a) + R(1, b) + R(1, c)), f"adds the {out}'s rate instead of subtracting it"
             if not out.endswith("use") else f"adds the rate of the {out} instead of subtracting it"),
            (R(a + b, 2), f"averages the two fill times and ignores the {out}"),
            (1 / T, "stops at the net rate and forgets to flip it into a time"),
            (Q(a + b + c), "adds the three times"),
        ],
        steps=steps,
        near=_near(T),
        check=sp.solve(sp.Eq(X / a + X / b - X / c, 1), X)[0],
    )


# --------------------------------------------------------------------------
# equal workers (worker-hours)
# --------------------------------------------------------------------------

_CREW = [
    # (key, worker word, unit, workers range, time range, military)
    ("sandbag", "soldiers", "hour", (4, 16), (2, 12)),
    ("barracks", "recruits", "hour", (4, 20), (2, 8)),
    ("painters", "painters", "day", (2, 10), (4, 30)),
    ("roofers", "roofers", "day", (2, 8), (3, 15)),
    ("pickers", "pickers", "day", (4, 20), (3, 15)),
    ("movers", "movers", "hour", (2, 8), (2, 10)),
    ("mechanics", "mechanics", "day", (3, 12), (4, 20)),
    ("volunteers", "volunteers", "hour", (6, 30), (2, 10)),
    ("supply", "soldiers", "hour", (4, 20), (2, 12)),
    ("landscapers", "landscapers", "day", (2, 10), (3, 15)),
]


def _crew_stem(key, w, t, u):
    us = _plural(u, t)
    return {
        "sandbag": f"A detail of {num(w)} soldiers can fill all the sandbags for a checkpoint in {num(t)} {us}.",
        "barracks": f"Working together, {num(w)} recruits can clean their barracks in {num(t)} {us}.",
        "painters": f"A crew of {num(w)} painters can paint an apartment building in {num(t)} {us}.",
        "roofers": f"A crew of {num(w)} roofers can put a new roof on a warehouse in {num(t)} {us}.",
        "pickers": f"A team of {num(w)} pickers can harvest an apple orchard in {num(t)} {us}.",
        "movers": f"A crew of {num(w)} movers can load a moving truck in {num(t)} {us}.",
        "mechanics": f"A team of {num(w)} mechanics can service all of a battalion's trucks in {num(t)} {us}.",
        "volunteers": f"A group of {num(w)} volunteers can pack the boxes for a food drive in {num(t)} {us}.",
        "supply": f"A detail of {num(w)} soldiers can unload and stack a shipment of supplies in {num(t)} {us}.",
        "landscapers": f"A crew of {num(w)} landscapers can plant the trees for a new park in {num(t)} {us}.",
    }[key]


@template("AR")
@_retrying
def equal_workers(rng, lvl):
    key, wword, u, (wlo, whi), (tlo, thi) = _fresh(rng, _CREW, "crew")
    w1 = rng.randint(wlo, whi)
    t1 = rng.randint(tlo, thi)
    total = w1 * t1
    first = _crew_stem(key, w1, t1, u)
    us = u + "s"
    if lvl == 1:
        w2 = rng.randint(wlo, whi)
        need(w2 != w1 and total % w2 == 0)
        t2 = total // w2
        need(tlo // 2 <= t2 <= thi * 2 and t2 != t1)
        stem = (f"{first} At the same rate, how many {us} would it take {num(w2)} {wword} "
                f"to do the job?")
        direct = R(t1 * w2, w1)
        wrong = [
            (direct, "sets up a direct proportion; more workers should take less time, not more"
             if w2 > w1 else "sets up a direct proportion; fewer workers should take more time, not less"),
            (Q(total), f"gives the total number of worker-{us}, not the time"),
            (Q(t1 + (w1 - w2)), f"changes the time by one {u} for each worker added or removed"),
            (Q(t1), "assumes the time does not change"),
        ]
        steps = [
            f"Find the total amount of work in worker-{us}: "
            f"{m(f'{w1} \\times {t1} = {int_raw(total)}')} worker-{us}.",
            f"Share that work among {num(w2)} {wword}: "
            f"{m(f'{int_raw(total)} \\div {w2} = {int_raw(t2)}')} {_plural(u, t2)}.",
        ]
        tip = (f"{'More' if w2 > w1 else 'Fewer'} workers means {'less' if w2 > w1 else 'more'} "
               f"time, so the answer must be {'less' if w2 > w1 else 'more'} than {num(t1)} {_plural(u, t1)}.")
        return Problem(stem=stem, answer=Q(t2), fmt=unit(num, u), section="AR", wrong=wrong,
                       steps=steps, tip=tip, near=_near(t2), verify=lambda v: Q(v) * w2 == w1 * t1,
                       check=sp.solve(sp.Eq(w1 * t1, w2 * X), X)[0])
    # level 2: how many workers (or how many more) are needed to finish in t2
    t2 = rng.randint(max(1, tlo // 2), thi)
    need(t2 < t1 and total % t2 == 0)
    w2 = total // t2
    need(w2 <= max(whi, 2 * w1) and w2 <= 3 * w1 and w2 - w1 >= 2)
    more = rng.random() < 0.5
    q = (f"How many \\emph{{more}} {wword} are needed to finish the job in {num(t2)} {_plural(u, t2)}?"
         if more else
         f"How many {wword} working at the same rate are needed to finish the job in "
         f"{num(t2)} {_plural(u, t2)}?")
    stem = f"{first} {q}"
    ans = Q(w2 - w1) if more else Q(w2)
    wrong = [
        (R(w1 * t2, t1) - (w1 if more else 0), "sets up a direct proportion; less time needs more workers, not fewer"),
        (Q(total), f"gives the total number of worker-{us}, not the number of workers"),
        (Q(w1 + (t1 - t2)) - (w1 if more else 0), f"adds one worker for each {u} saved"),
    ]
    if more:
        wrong.insert(0, (Q(w2), "is the total number of workers needed, not how many more"))
    steps = [
        f"Total work: {m(f'{w1} \\times {t1} = {int_raw(total)}')} worker-{us}.",
        f"To finish in {num(t2)} {_plural(u, t2)}: "
        f"{m(f'{int_raw(total)} \\div {t2} = {int_raw(w2)}')} {wword} are needed.",
    ]
    if more:
        steps.append(f"There are already {num(w1)} {wword}, so "
                     f"{m(f'{int_raw(w2)} - {w1} = {int_raw(w2 - w1)}')} more are needed.")
    return Problem(stem=stem, answer=ans, fmt=num, section="AR", wrong=wrong, steps=steps,
                   near=_near(ans),
                   verify=lambda v: (Q(v) + (w1 if more else 0)) * t2 == total,
                   check=sp.solve(sp.Eq(w1 * t1, (X + (w1 if more else 0)) * t2), X)[0])


@template("AR")
@_retrying
def crew_changes(rng, lvl):
    key = _fresh(rng, ["mre", "berm", "house", "camp", "road"], "changes")
    if key in ("mre", "camp"):
        n1 = rng.choice(range(20, 121, 5) if key == "mre" else range(30, 151, 10))
        d1 = rng.randint(10, 40)
        k = rng.randint(2, d1 // 2)
        arrive = rng.random() < 0.6
        ch = rng.choice(range(5, n1 // 2 + 1, 5))
    else:
        n1 = {"berm": rng.choice(range(12, 41, 4)), "house": rng.randint(4, 12),
              "road": rng.randint(6, 30)}[key]
        d1 = rng.randint(10, 30) if key == "house" else rng.randint(8, 40)
        k = rng.randint(2, d1 // 2)
        arrive = rng.random() < 0.6
        ch = rng.randint(2, max(2, n1 // 2))
    n2 = n1 + ch if arrive else n1 - ch
    rest_work = n1 * (d1 - k)
    need(n2 > 0 and rest_work % n2 == 0)
    rem = rest_work // n2
    need(rem != d1 - k and rem >= 2)
    ask_total = rng.random() < 0.35
    ans = Q(k + rem) if ask_total else Q(rem)
    if key == "mre":
        s1 = (f"A remote outpost has enough MREs (meals) to feed {num(n1)} soldiers for "
              f"{num(d1)} days. After {num(k)} days, {num(ch)} "
              f"{'more soldiers arrive' if arrive else 'soldiers are sent home'}.")
        q = ("How many more days will the remaining MREs last?" if not ask_total else
             "In all, counting from the first day, how many days will the MREs last?")
        unit_w, job = "soldier-days", "food"
    elif key == "camp":
        s1 = (f"A summer camp has enough food to feed {num(n1)} campers for {num(d1)} days. "
              f"After {num(k)} days, {num(ch)} {'more campers arrive' if arrive else 'campers go home'}.")
        q = ("How many more days will the remaining food last?" if not ask_total else
             "In all, counting from the first day, how many days will the food last?")
        unit_w, job = "camper-days", "food"
    elif key == "berm":
        s1 = (f"A platoon of {num(n1)} soldiers can build a sandbag wall around a command post "
              f"in {num(d1)} days. After {num(k)} days of work, {num(ch)} "
              f"{'more soldiers join the job' if arrive else 'soldiers are reassigned'}.")
        q = ("How many more days will it take to finish the wall?" if not ask_total else
             "How many days in all will the job take?")
        unit_w, job = "soldier-days", "work"
    elif key == "house":
        s1 = (f"A crew of {num(n1)} workers can frame a house in {num(d1)} days. After "
              f"{num(k)} days, {num(ch)} {'more workers join the crew' if arrive else 'workers leave for another job'}.")
        q = ("How many more days will it take to finish?" if not ask_total else
             "How many days in all will the job take?")
        unit_w, job = "worker-days", "work"
    else:
        s1 = (f"A road crew of {num(n1)} workers can repave a road in {num(d1)} days. After "
              f"{num(k)} days, {num(ch)} {'more workers join the crew' if arrive else 'workers are moved to another project'}.")
        q = ("How many more days will it take to finish the road?" if not ask_total else
             "How many days in all will the job take?")
        unit_w, job = "worker-days", "work"
    stem = s1 + " " + q
    who = {"mre": "soldiers", "camp": "campers", "berm": "soldiers"}.get(key, "workers")
    steps = [
        f"After {num(k)} days, the original {num(n1)} {who} still had {num(d1 - k)} days' worth "
        f"of {job} left: {m(f'{n1} \\times {d1 - k} = {int_raw(rest_work)}')} {unit_w}.",
        f"Now there are {m(f'{n1} {"+" if arrive else "-"} {ch} = {n2}')} {who}, so the rest "
        f"takes {m(f'{int_raw(rest_work)} \\div {n2} = {rem}')} days.",
    ]
    if ask_total:
        steps.append(f"Add the days already passed: {m(f'{k} + {rem} = {k + rem}')} days in all.")
    wrong = [
        (Q(d1 - k) + (k if ask_total else 0), f"ignores the {'new arrivals' if arrive else 'smaller group'}"),
        (R(n1 * d1, n2) + (k if ask_total else 0),
         (f"forgets the food already eaten in the first {num(k)} days (gives the new group the full supply)"
          if key in ("mre", "camp") else
          f"forgets the work already done in the first {num(k)} days (gives the new crew the whole job)")),
        (R((d1 - k) * n2, n1) + (k if ask_total else 0), "sets up a direct proportion instead of an inverse one"),
    ]
    if ask_total:
        wrong.append((Q(rem), "gives only the days after the change, not the total"))
    else:
        wrong.append((Q(k + rem), "gives the total number of days, not the days remaining"))
    return Problem(stem=stem, answer=ans, fmt=unit(num, "day"), section="AR", wrong=wrong,
                   steps=steps, near=_near(ans),
                   verify=lambda v: n1 * k + n2 * (Q(v) - (k if ask_total else 0)) == n1 * d1,
                   check=sp.solve(sp.Eq(n1 * k + n2 * (X - (k if ask_total else 0)), n1 * d1), X)[0])


# --------------------------------------------------------------------------
# mixtures
# --------------------------------------------------------------------------

_SOLUTE = [
    # key, unit, totals, percents, pure word, rest word, military
    ("radiator", "quart", list(range(8, 21)), [30, 40, 50, 60], "antifreeze", "water"),
    ("brass", "pound", list(range(100, 401, 20)), [65, 70], "copper", "zinc"),
    ("punch", "ounce", [32, 48, 64, 96, 128], [5, 10, 15, 20, 25], "real fruit juice", "water and sweetener"),
    ("cleaner", "gallon", list(range(2, 13)), [10, 20, 25, 40, 50], "concentrate", "water"),
    ("fuel", "gallon", list(range(10, 26)), [10, 15], "ethanol", "gasoline"),
    ("medic", "milliliter", list(range(200, 1001, 100)), [5, 10, 20], "bleach", "water"),
]


def _solute_stem(key, V, P, A, ask_pct):
    if not ask_pct:
        return {
            "radiator": f"A car's radiator holds {num(V)} quarts of coolant that is {pct(P)} antifreeze and the rest water. How many quarts of pure antifreeze are in the radiator?",
            "brass": f"Brass rifle casings are {pct(P)} copper by weight; the rest is zinc. The recycling bin at a firing range holds {num(V)} pounds of brass casings. How many pounds of copper do the casings contain?",
            "punch": f"A {num(V)}-ounce bottle of fruit punch is {pct(P)} real fruit juice. How many ounces of real fruit juice does the bottle contain?",
            "cleaner": f"For a barracks cleanup, a soldier mixes {num(V)} gallons of floor-cleaning solution that is {pct(P)} concentrate and the rest water. How many gallons of concentrate are in the solution?",
            "fuel": f"Gasoline sold as E{P} is {pct(P)} ethanol. How many gallons of ethanol are in a full {num(V)}-gallon tank of E{P} gasoline?",
            "medic": f"A medic mixes {num(V)} milliliters of a cleaning solution that is {pct(P)} bleach and the rest water. How many milliliters of bleach are in the solution?",
        }[key]
    return {
        "radiator": f"A car's radiator holds {num(V)} quarts of coolant. The coolant contains {dec(A)} quarts of pure antifreeze, and the rest is water. What percent of the coolant is antifreeze?",
        "brass": f"A {num(V)}-pound load of brass casings collected at a firing range contains {dec(A)} pounds of copper. What percent of the brass is copper?",
        "punch": f"A {num(V)}-ounce bottle of fruit punch contains {dec(A)} ounces of real fruit juice. What percent of the punch is real juice?",
        "cleaner": f"A soldier mixes {num(V)} gallons of floor-cleaning solution using {dec(A)} gallons of concentrate and the rest water. What percent of the solution is concentrate?",
        "medic": f"A medic's {num(V)}-milliliter cleaning solution contains {dec(A)} milliliters of bleach. What percent of the solution is bleach?",
    }[key]


@template("AR")
@_retrying
def solute_amount(rng, lvl):
    key, u, Vs, Ps, pure, rest = _fresh(rng, _SOLUTE, "solute")
    V = rng.choice(Vs)
    P = rng.choice(Ps)
    A = R(P, 100) * V
    need((A * 10).is_integer and A > 0)
    ask_pct = key != "fuel" and rng.random() < 0.4
    stem = _solute_stem(key, V, P, A, ask_pct)
    up = u + "s"
    if not ask_pct:
        return Problem(
            stem=stem, answer=A, fmt=unit(dec, u), section="AR",
            wrong=[
                (V - A, f"is the amount of {rest}, not {pure}"),
                (A * 10, "moves the decimal point only one place when changing the percent"),
                (A / 10, "moves the decimal point three places when changing the percent"),
                (Q(P), "uses the percent as if it were the amount"),
            ],
            steps=[
                f"Amount of {pure} $=$ percent $\\times$ total. Change the percent to a decimal: "
                f"{m(f'{P}\\% = {dec_raw(R(P, 100))}')}.",
                f"Multiply: {m(f'{dec_raw(R(P, 100))} \\times {int_raw(V)} = {dec_raw(A)}')} {up}.",
            ],
            check=Fraction(V * P, 100),
            verify=lambda v: Q(v) / V == R(P, 100),
        )
    return Problem(
        stem=stem, answer=Q(P), fmt=pct, section="AR",
        wrong=[
            (Q(100 - P), f"is the percent that is {rest}"),
            (A / (V - A) * 100, f"compares the {pure} to the {rest} instead of to the whole"),
            (Q(V) / A * 100, "divides the whole by the part"),
            (A, "gives the amount, not the percent"),
        ],
        steps=[
            f"Percent $=$ part $\\div$ whole: {m(F(dec_raw(A), int_raw(V)))}.",
            f"Divide and change to a percent: {m(F(dec_raw(A), int_raw(V)) + ' = ' + dec_raw(R(P, 100)) + ' = ' + str(P) + r'\%')}.",
        ],
        verify=lambda v: Q(v) * V / 100 == A,
    )


_SOLN = {
    # key: (unit, amounts, percents, pure word, who, description of a p% solution)
    "coolant": ("quart", list(range(2, 13)), [20, 25, 30, 40, 50, 60, 70, 75, 80, 90],
                "antifreeze", "A mechanic", lambda p: f"a {pct(p)} antifreeze solution"),
    "motorpool": ("gallon", list(range(2, 21)), [20, 25, 30, 40, 50, 60, 70, 75, 80, 90],
                  "antifreeze", "A motor pool mechanic",
                  lambda p: f"coolant that is {pct(p)} antifreeze"),
    "lab": ("liter", list(range(1, 13)), [5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90],
            "acid", "A lab technician", lambda p: f"a {pct(p)} acid solution"),
    "alcohol": ("milliliter", list(range(100, 801, 50)), [30, 40, 50, 60, 70, 80, 90],
                "alcohol", "A medic at an aid station", lambda p: f"a {pct(p)} alcohol solution"),
    "fertilizer": ("gallon", list(range(2, 21)), [5, 10, 15, 20, 25, 30, 40, 50],
                   "fertilizer", "A gardener", lambda p: f"a {pct(p)} fertilizer solution"),
    "punch": ("gallon", list(range(1, 11)), [10, 20, 25, 30, 40, 50],
              "fruit juice", "A cafeteria worker", lambda p: f"a punch that is {pct(p)} fruit juice"),
}


@template("AR")
@_retrying
def mix_two_solutions(rng, lvl):
    key = _fresh(rng, list(_SOLN), "soln")
    u, amounts, pcts, pure, who, desc = _SOLN[key]

    def D(p):
        return f"pure {pure}" if p == 100 else desc(p)

    us = u + "s"
    if lvl <= 2:
        x1, x2 = rng.sample(amounts, 2)
        p1, p2 = rng.sample(pcts + ([100] if key == "punch" else []), 2)
        pure_tot = R(p1 * x1 + p2 * x2, 100)
        c = R(p1 * x1 + p2 * x2, x1 + x2)
        need(c.is_integer and c != R(p1 + p2, 2))
        need((R(p1 * x1, 100) * 10).is_integer and (R(p2 * x2, 100) * 10).is_integer)
        stem = (f"{who} mixes {num(x1)} {_plural(u, x1)} of {D(p1)} with {num(x2)} "
                f"{_plural(u, x2)} of {D(p2)}. What percent of the mixture is {pure}?")
        a1, a2 = R(p1 * x1, 100), R(p2 * x2, 100)
        return Problem(
            stem=stem, answer=c, fmt=pct, section="AR",
            wrong=[
                (R(p1 + p2, 2), "averages the two percents without weighting by the amounts"),
                (R(p1 * x2 + p2 * x1, x1 + x2), "weights each percent by the wrong amount"),
                (Q(p1 + p2), "adds the two percents"),
                (pure_tot, f"gives the amount of pure {pure}, not the percent"),
            ],
            steps=[
                f"Pure {pure} in each: {m(f'{dec_raw(R(p1, 100))} \\times {int_raw(x1)} = {dec_raw(a1)}')} and "
                f"{m(f'{dec_raw(R(p2, 100))} \\times {int_raw(x2)} = {dec_raw(a2)}')} {us}.",
                f"Totals: {m(f'{dec_raw(a1)} + {dec_raw(a2)} = {dec_raw(pure_tot)}')} {us} of {pure} in "
                f"{m(f'{int_raw(x1)} + {int_raw(x2)} = {int_raw(x1 + x2)}')} {us} of mixture.",
                f"Percent: {m(F(dec_raw(pure_tot), int_raw(x1 + x2)) + ' = ' + dec_raw(c / 100) + ' = ' + int_raw(c) + r'\%')}.",
            ],
            tip=f"Check: {pct(c)} is between {pct(min(p1, p2))} and {pct(max(p1, p2))}, closer to the percent of the larger amount.",
            near=_near(c, step=5 if c % 5 == 0 else 2),
            check=Fraction(p1 * x1 + p2 * x2, x1 + x2),
        )
    # level 3: how much of the second solution to add to reach the target
    x1 = rng.choice(amounts)
    p1, p2 = rng.sample(pcts + ([100] if key in ("coolant", "motorpool", "lab", "punch") else []), 2)
    lo_, hi_ = min(p1, p2), max(p1, p2)
    need(hi_ - lo_ >= 10)
    c = rng.choice(range(lo_ + 5, hi_, 5))
    y = R(x1 * (c - p1), p2 - c)
    need(y.is_integer and 0 < y <= 2 * max(amounts) and y != x1 and y <= 4 * x1)
    stem = (f"{who} has {num(x1)} {_plural(u, x1)} of {D(p1)}. How many {us} of "
            f"{D(p2)} must be added to make a mixture that is {pct(c)} {pure}?")
    d1, d2 = abs(c - p1), abs(p2 - c)
    p1d, p2d, cd = dec_raw(R(p1, 100)), dec_raw(R(p2, 100)), dec_raw(R(c, 100))
    p2y = "y" if p2 == 100 else f"{p2d}y"
    steps = [
        f"Let {m('y')} be the {us} added. The pure {pure} going in must equal the pure "
        f"{pure} in the mixture: {m(f'{p1d}({int_raw(x1)}) + {p2y} = {cd}({int_raw(x1)} + y)')}.",
        f"Multiply out: {m(f'{dec_raw(R(p1 * x1, 100))} + {p2y} = {dec_raw(R(c * x1, 100))} + {cd}y')}.",
        (f"Collect the {m('y')} terms: {m(f'{dec_raw(R(p2 - c, 100))}y = {dec_raw(R(x1 * (c - p1), 100))}')}"
         if p2 > c else
         f"Collect the {m('y')} terms: {m(f'{dec_raw(R(p1 * x1 - c * x1, 100))} = {dec_raw(R(c - p2, 100))}y')}")
        + f", so {m(f'y = {int_raw(y)}')} {_plural(u, y)}.",
    ]
    return Problem(
        stem=stem, answer=y, fmt=unit(num, u), section="AR",
        wrong=[
            (R(x1 * d2, d1), "swaps the two differences"),
            (x1 + y, "gives the total amount of the mixture, not the amount added"),
            (Q(x1), "assumes equal amounts of the two solutions"),
            (R(x1 * d1, p2) if p2 > c else R(x1 * d1, c),
             "forgets that the added solution also counts toward the new total" if p2 > c
             else "treats the added solution as if it were plain water"),
        ],
        steps=steps,
        tip=(f"Balance shortcut: {D(p1)} is {d1} points from {pct(c)} and {D(p2)} is {d2} points "
             f"away, so {m(f'{int_raw(x1)} \\times {d1} = y \\times {d2}')}, which gives "
             f"{m(f'y = {int_raw(y)}')}."),
        near=_near(y),
        verify=lambda v: Fraction(p1 * x1 + p2 * int(v), 100) == Fraction(c, 100) * (x1 + int(v)),
        check=sp.solve(sp.Eq(R(p1, 100) * x1 + R(p2, 100) * X, R(c, 100) * (x1 + X)), X)[0],
    )


@template("AR")
@_retrying
def concentration_change(rng, lvl):
    if lvl <= 2:
        key = _fresh(rng, ["fertilizer", "acid", "bleach", "juice", "antifreeze"], "dilute")
        u = {"fertilizer": "gallon", "acid": "liter", "bleach": "liter", "juice": "gallon",
             "antifreeze": "gallon"}[key]
        V = rng.randint(1, 5) if key == "bleach" else rng.randint(2, 12) if key == "acid" else rng.randint(2, 20)
        if key == "bleach":
            p = rng.choice([10, 15, 20, 25])
            q = rng.choice([2, 4, 5])
        elif key == "antifreeze":
            p = rng.choice([60, 75, 80, 90, 100])
            q = rng.choice([40, 50])
        else:
            p = rng.choice([20, 25, 30, 40, 50, 60, 75, 80])
            q = rng.choice([5, 10, 15, 20, 25, 30, 40, 50, 60])
        need(q < p)
        final = R(V * p, q)
        water = final - V
        need(water.is_integer and water > 0 and water <= 6 * V)
        P = R(V * p, 100)
        need((P * 10).is_integer)
        stem = {
            "fertilizer": f"A gardener has {num(V)} gallons of a {pct(p)} fertilizer solution. How many gallons of water must be added to make a {pct(q)} solution?",
            "acid": f"A chemistry teacher has {num(V)} liters of a {pct(p)} acid solution. How many liters of water must be added to dilute it to a {pct(q)} solution?",
            "bleach": f"A medic has {num(V)} {_plural('liter', V)} of a {pct(p)} disinfectant solution but needs a weaker {pct(q)} solution to clean equipment. How many liters of water should be added?",
            "juice": f"A dining facility has {num(V)} gallons of a drink that is {pct(p)} juice. How many gallons of water must be added so that the drink is {pct(q)} juice?",
            "antifreeze": (f"A motor pool has {num(V)} gallons of pure antifreeze." if p == 100 else
                           f"A motor pool has {num(V)} gallons of coolant that is {pct(p)} antifreeze.")
                          + f" The truck manual calls for coolant that is {pct(q)} antifreeze. How many gallons of water must be added?",
        }[key]
        pure = {"fertilizer": "fertilizer", "acid": "acid", "bleach": "disinfectant", "juice": "juice",
                "antifreeze": "antifreeze"}[key]
        us = u + "s"
        return Problem(
            stem=stem, answer=water, fmt=unit(num, u), section="AR",
            wrong=[
                (final, "is the final amount of the mixture, not the water added"),
                (R(V * q, p), f"makes two slips: flips the percents ({m(F(q, p))} instead of {m(F(p, q))}) "
                 "and stops at the total instead of finding the water added"),
                (R(V * (p - q), 100), "takes the drop in percent of the original amount"),
                (V - R(V * q, p), f"flips the percents ({m(F(q, p))} instead of {m(F(p, q))}), then "
                 "subtracts that amount from the starting amount"),
                (P, f"is the amount of pure {pure}, not the water to add"),
                (V - P, "is the water already in the solution, not the water to add"),
            ],
            near=_near(water),
            steps=[
                (f"Pure {pure} now: all {num(V)} {us}. " if p == 100 else
                 f"Pure {pure} now: {m(f'{dec_raw(R(p, 100))} \\times {int_raw(V)} = {dec_raw(P)}')} {us}. ")
                + "Adding water does not change this amount.",
                f"In the new mixture these {dec(P)} {us} must be {pct(q)} of the total: "
                f"{m(f'{dec_raw(P)} \\div {dec_raw(R(q, 100))} = {int_raw(final)}')} {us} in all.",
                f"Water to add: {m(f'{int_raw(final)} - {int_raw(V)} = {int_raw(water)}')} {_plural(u, water)}.",
            ],
            verify=lambda w: R(V * p, 100) == R(q, 100) * (V + Q(w)),
            check=sp.solve(sp.Eq(R(p, 100) * V, R(q, 100) * (V + X)), X)[0],
        )
    kind = _fresh(rng, ["evaporate", "pure"], "conc3", keep=1)
    if kind == "evaporate":
        key = _fresh(rng, ["salt", "juice", "syrup"], "evap")
        V = rng.choice(range(10, 201, 10))
        p = rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
        q = rng.choice([4, 5, 6, 8, 10, 12, 15, 16, 20, 24, 25, 30, 40, 48, 50, 60])
        need(q > p and q <= 4 * p)
        final = R(V * p, q)
        gone = V - final
        need(final.is_integer and gone.is_integer and gone > 0)
        P = R(V * p, 100)
        need((P * 10).is_integer)
        u = {"salt": "liter", "juice": "gallon", "syrup": "gallon"}[key]
        pure = {"salt": "salt", "juice": "juice solids", "syrup": "sugar"}[key]
        stem = {
            "salt": f"A tank holds {num(V)} liters of salt water that is {pct(p)} salt. How many liters of water must evaporate to leave a solution that is {pct(q)} salt?",
            "juice": f"A juice plant starts with {num(V)} gallons of juice that is {pct(p)} juice solids. How many gallons of water must be removed to make a concentrate that is {pct(q)} solids?",
            "syrup": f"A cook has {num(V)} gallons of sugar syrup that is {pct(p)} sugar. How many gallons of water must be boiled off to make the syrup {pct(q)} sugar?",
        }[key]
        us = u + "s"
        return Problem(
            stem=stem, answer=gone, fmt=unit(num, u), section="AR",
            wrong=[
                (final, "is the amount left after evaporating, not the amount removed"),
                (R(V * (q - p), 100), "takes the rise in percent of the original amount"),
                (R(V * (q - p), p), "divides by the old percent instead of the new one"),
                (R(V * q, p), f"makes two slips: flips the percents ({m(F(q, p))} instead of {m(F(p, q))}) "
                 "and stops at the total instead of finding the water removed"),
            ],
            near=_near(gone),
            steps=[
                f"Pure {pure}: {m(f'{dec_raw(R(p, 100))} \\times {int_raw(V)} = {dec_raw(P)}')} {us}. "
                f"Removing water does not change this amount.",
                f"After evaporating, {dec(P)} {us} must be {pct(q)} of the total: "
                f"{m(f'{dec_raw(P)} \\div {dec_raw(R(q, 100))} = {int_raw(final)}')} {us} left.",
                f"Water removed: {m(f'{int_raw(V)} - {int_raw(final)} = {int_raw(gone)}')} {_plural(u, gone)}.",
            ],
            verify=lambda w: R(V * p, 100) == R(q, 100) * (V - Q(w)),
            check=sp.solve(sp.Eq(R(p, 100) * V, R(q, 100) * (V - X)), X)[0],
        )
    # add pure ingredient to strengthen
    key = _fresh(rng, ["winter", "lab", "garden"], "purectx")
    V = rng.randint(4, 30)
    p = rng.choice([10, 20, 25, 30, 40, 50])
    q = rng.choice([20, 25, 30, 40, 50, 60, 75])
    need(q > p)
    add = R(V * (q - p), 100 - q)
    need(add.is_integer and add > 0)
    need((V * (q - p)) % 100 == 0 or rng.random() < 0.25)
    u = {"winter": "gallon", "lab": "liter", "garden": "gallon"}[key]
    pure = {"winter": "antifreeze", "lab": "acid", "garden": "fertilizer"}[key]
    stem = {
        "winter": f"Before winter, a motor pool has {num(V)} gallons of coolant that is {pct(p)} antifreeze. How many gallons of pure antifreeze must be added to make coolant that is {pct(q)} antifreeze?",
        "lab": f"A lab has {num(V)} liters of a {pct(p)} acid solution. How many liters of pure acid must be added to make a {pct(q)} acid solution?",
        "garden": f"A greenhouse worker has {num(V)} gallons of a {pct(p)} fertilizer solution. How many gallons of pure fertilizer must be added to make a {pct(q)} solution?",
    }[key]
    us = u + "s"
    P = R(V * p, 100)
    pd, qd = dec_raw(R(p, 100)), dec_raw(R(q, 100))
    return Problem(
        stem=stem, answer=add, fmt=unit(num, u), section="AR",
        wrong=[
            (R(V * (q - p), 100), f"forgets that the added {pure} also raises the total amount "
             f"(solves {m(f'{pd}({int_raw(V)}) + y = {qd}({int_raw(V)})')})"),
            (R(V * (q - p), q), f"divides by the target percent ({pct(q)}) instead of by the share that is "
             f"not {pure} ({pct(100 - q)})"),
            (V + add, "gives the total amount of the new mixture"),
            (R(V * (q - p), p), None),
        ],
        near=_near(add),
        steps=[
            f"Let {m('y')} be the {us} of pure {pure} added (pure means {m('100\\%')}). Pure {pure} "
            f"before and after: {m(f'{pd}({int_raw(V)}) + y = {qd}({int_raw(V)} + y)')}.",
            f"Multiply out: {m(f'{dec_raw(P)} + y = {dec_raw(R(q * V, 100))} + {qd}y')}.",
            f"Collect terms: {m(f'{dec_raw(R(100 - q, 100))}y = {dec_raw(R(V * (q - p), 100))}')}, so "
            f"{m(f'y = {int_raw(add)}')} {_plural(u, add)}.",
        ],
        verify=lambda w: R(V * p, 100) + Q(w) == R(q, 100) * (V + Q(w)),
        check=sp.solve(sp.Eq(R(p, 100) * V + X, R(q, 100) * (V + X)), X)[0],
    )


_GOODS = [
    # key, item A, item B, price range A, price range B, amount range, unit
    ("coffee", "Colombian coffee", "Kona blend coffee", (6, 10), (12, 20), (2, 20)),
    ("nuts", "peanuts", "cashews", (3, 5), (9, 14), (4, 30)),
    ("candy", "gummy bears", "chocolate drops", (3, 5), (6, 9), (2, 20)),
    ("seed", "rye grass seed", "bluegrass seed", (2, 4), (5, 8), (10, 60)),
    ("beef", "80\\%-lean ground beef", "93\\%-lean ground beef", (3, 5), (6, 8), (20, 80)),
    ("trail", "raisins", "almonds", (2, 4), (7, 10), (5, 40)),
]


def _goods_who(key):
    return {
        "coffee": "A coffee shop", "nuts": "A grocery store", "candy": "A candy store",
        "seed": "A garden center", "beef": "A base dining facility",
        "trail": "The base exchange",
    }[key]


@template("AR")
@_retrying
def mix_prices(rng, lvl):
    key, A, B, (alo, ahi), (blo, bhi), (wlo, whi) = _fresh(rng, _GOODS, "goods")
    who = _goods_who(key)
    halves = lvl == 2 and rng.random() < 0.4
    pa = Q(rng.randint(alo, ahi)) + (R(1, 2) if halves and rng.random() < 0.5 else 0)
    pb = Q(rng.randint(blo, bhi)) + (R(1, 2) if halves and rng.random() < 0.5 else 0)
    if lvl <= 2:
        wa, wb = rng.randint(wlo, whi), rng.randint(wlo, whi)
        need(wa != wb)
        cost = pa * wa + pb * wb
        price = cost / (wa + wb)
        need((price * 20).is_integer and price != (pa + pb) / 2)
        stem = (f"{who} mixes {num(wa)} pounds of {A} costing {money(pa)} per pound with "
                f"{num(wb)} pounds of {B} costing {money(pb)} per pound. What is the cost per "
                f"pound of the mixture?")
        cents = not (pa.is_integer and pb.is_integer)

        def d(v):
            return dec_raw(v, 2) if cents else int_raw(v)
        return Problem(
            stem=stem, answer=price, fmt=money, section="AR",
            wrong=[
                ((pa + pb) / 2, "averages the two prices without weighting by the pounds"),
                ((pa * wb + pb * wa) / (wa + wb), "weights each price by the wrong number of pounds"),
                (cost, "is the total cost of the mixture, not the price per pound"),
                (cost / 2, "divides the total cost by 2 instead of by the total pounds"),
            ],
            steps=[
                f"Cost of each part: {m(f'{wa} \\times {d(pa)} = {d(pa * wa)}')} and "
                f"{m(f'{wb} \\times {d(pb)} = {d(pb * wb)}')} dollars.",
                f"Totals: {money(cost)} for {m(f'{wa} + {wb} = {wa + wb}')} pounds.",
                f"Price per pound: {m(f'{d(cost)} \\div {wa + wb} = {dec_raw(price, 2)}')}, "
                f"or {money(price)} per pound.",
            ],
            tip=f"Check: {money(price)} is between {money(pa)} and {money(pb)}, closer to the price of the item with more pounds.",
            near=_near(price, money_=True),
            check=Fraction(int(cost * 2), 2 * (wa + wb)) if (cost * 2).is_integer else cost / (wa + wb),
        )
    # level 3: how many pounds of one item are needed for a target price
    need(pb - pa >= 2)
    t = Q(rng.randint(int(pa) + 1, int(pb) - 1))
    known_cheap = rng.random() < 0.5
    K = rng.randint(wlo, whi)
    if known_cheap:
        pk, pu, kn, un = pa, pb, A, B
    else:
        pk, pu, kn, un = pb, pa, B, A
    y = R(K * abs(pk - t), abs(t - pu))
    need(y.is_integer and y != K and 2 <= y <= min(3 * whi, 3 * K))
    stem = (f"{who} has {num(K)} pounds of {kn} priced at {money(pk)} per pound. How many "
            f"pounds of {un} priced at {money(pu)} per pound must be mixed in to make a blend "
            f"worth {money(t)} per pound?")
    lhs_k = pk * K
    steps = [
        f"Let {m('y')} be the pounds of {un}. The money must balance: "
        f"{m(f'{int_raw(pk)}({K}) + {int_raw(pu)}y = {int_raw(t)}({K} + y)')}.",
        f"Multiply out: {m(f'{int_raw(lhs_k)} + {int_raw(pu)}y = {int_raw(t * K)} + {int_raw(t)}y')}.",
    ]
    if pu > t:
        cy = "y" if pu - t == 1 else f"{int_raw(pu - t)}y"
        steps.append(f"Collect terms: {m(f'{int_raw(pu)}y - {int_raw(t)}y = {int_raw(t * K)} - {int_raw(lhs_k)}')}, "
                     f"so {m(f'{cy} = {int_raw(t * K - lhs_k)}')}"
                     + (f" and {m(f'y = {int_raw(y)}')} pounds." if pu - t != 1 else " pounds."))
    else:
        cy = "y" if t - pu == 1 else f"{int_raw(t - pu)}y"
        steps.append(f"Collect terms: {m(f'{int_raw(lhs_k)} - {int_raw(t * K)} = {int_raw(t)}y - {int_raw(pu)}y')}, "
                     + (f"so {m(f'{int_raw(lhs_k - t * K)} = {cy}')} and {m(f'y = {int_raw(y)}')} pounds."
                        if t - pu != 1 else f"so {m(f'y = {int_raw(y)}')} pounds."))
    return Problem(
        stem=stem, answer=y, fmt=unit(num, "pound"), section="AR",
        wrong=[
            (Q(K), "assumes equal amounts, which only works if the target is halfway between the prices"),
            (R(K * abs(t - pu), abs(pk - t)), "swaps the two price differences"),
            (y + K, "gives the total weight of the blend"),
            (Q(abs(pk - t) * K), None),
        ],
        steps=steps,
        near=_near(y),
        tip=(f"Balance shortcut: each pound of {kn} is {money(abs(pk - t))} away from {money(t)}, "
             f"each pound of {un} is {money(abs(pu - t))} away; the totals must match: "
             f"{m(f'{K} \\times {int_raw(abs(pk - t))} = {int_raw(y)} \\times {int_raw(abs(pu - t))}')}."),
        verify=lambda v: pk * K + pu * Q(v) == t * (K + Q(v)),
        check=sp.solve(sp.Eq(pk * K + pu * X, t * (K + X)), X)[0],
    )


# --------------------------------------------------------------------------
# ratio mixes
# --------------------------------------------------------------------------

_RATIO_CTX = [
    # key, ingredient names, ratios, unit singular, unit plural, product name
    ("concrete", ["cement", "sand", "gravel"], [(1, 2, 3), (1, 2, 4), (1, 3, 4)],
     "cubic foot", "cubic feet", "concrete mix"),
    ("bronze", ["copper", "tin"], [(9, 1), (4, 1), (7, 1)], "pound", "pounds", "bronze"),
    ("paint", ["tan paint", "green paint"], [(3, 1), (5, 1), (3, 2), (4, 1)],
     "gallon", "gallons", "mixed paint"),
    ("lemonade", ["lemonade concentrate", "water"], [(1, 4), (1, 5), (1, 3), (2, 7)],
     "cup", "cups", "lemonade"),
    ("trail", ["peanuts", "raisins", "chocolate chips"], [(3, 2, 1), (4, 3, 1), (5, 3, 2)],
     "pound", "pounds", "trail mix"),
]


def _ratio_intro(key, names, ratio):
    rr = " : ".join(str(r) for r in ratio)
    nn = ", ".join(names[:-1]) + (", and " if len(names) > 2 else " and ") + names[-1]
    return {
        "concrete": f"Combat engineers mix concrete for a bunker floor using {nn} in the ratio {m(rr)} by volume.",
        "bronze": f"A foundry makes bronze from {nn} in the ratio {m(rr)} by weight.",
        "paint": f"To touch up vehicles, a motor pool mixes {nn} in the ratio {m(rr)}.",
        "lemonade": f"A recipe for lemonade mixes {nn} in the ratio {m(rr)}.",
        "trail": f"For ruck-march snack packs, a unit mixes {nn} in the ratio {m(rr)} by weight.",
    }[key]


def _is(name):
    return "are" if name.endswith("s") else "is"


def _parts(r):
    return "part" if r == 1 else "parts"


@template("AR")
@_retrying
def ratio_mix(rng, lvl):
    if lvl >= 2 and rng.random() < 0.45:
        return _two_stroke(rng)
    key, names, ratios, us_, up_, prod = _fresh(rng, _RATIO_CTX, "ratio")
    ratio = rng.choice(ratios)
    S = sum(ratio)
    i = rng.randrange(len(ratio))
    ri = ratio[i]
    intro = _ratio_intro(key, names, ratio)

    def u(v):
        return us_ if v == 1 else up_

    Name = names[i][0].upper() + names[i][1:]
    if lvl == 1:
        k = rng.randint(2, 12 if S <= 6 else 8)
        T = S * k
        ans = ri * k
        stem = f"{intro} How many {up_} of {names[i]} are in {num(T)} {up_} of {prod}?"
        others = S - ri
        wrong = [
            (Q(T - ans), f"is the amount of everything except the {names[i]}"),
            (R(T, len(ratio)), "splits the mix into equal amounts"),
        ]
        if ri > 1:
            wrong.append((R(T, ri), f"divides the total by the {names[i]}'s {ri} parts instead of by all {S} parts"
                          if not names[i].endswith("s") else
                          f"divides the total by {ri} (the parts for {names[i]}) instead of by all {S} parts"))
            wrong.append((Q(k), "is the size of just one part"))
        if R(T * ri, others) != T:
            wrong.append((R(T * ri, others), "divides by the other parts instead of by the total parts"))
        last = (f"{Name} {_is(names[i])} 1 part, so the answer is {num(k)} {u(k)}." if ri == 1 else
                f"{Name} {_is(names[i])} {ri} parts: {m(f'{ri} \\times {k} = {ans}')} {u(ans)}.")
        return Problem(
            stem=stem, answer=Q(ans), fmt=unit(num, us_, up_), section="AR",
            wrong=wrong,
            steps=[
                f"Add the parts: {m(' + '.join(str(r) for r in ratio) + f' = {S}')} parts in all.",
                f"Find the size of one part: {m(f'{int_raw(T)} \\div {S} = {k}')} {u(k)}.",
                last,
            ],
            near=_near(ans),
            check=Fraction(T * ri, S),
        )
    # level 2: given one ingredient, find another ingredient or the total
    j = rng.choice([j for j in range(len(ratio)) if j != i] + ["total"])
    k = rng.randint(2, 10)
    have = ri * k
    rj = S if j == "total" else ratio[j]
    ans = rj * k
    if j == "total":
        what = f"How many {up_} of {prod} can be made"
        last = f"The whole batch is {S} parts: {m(f'{S} \\times {k} = {ans}')} {u(ans)}."
    else:
        what = f"How many {up_} of {names[j]} are needed"
        Nj = names[j][0].upper() + names[j][1:]
        last = f"{Nj} {_is(names[j])} {rj} {_parts(rj)}: {m(f'{rj} \\times {k} = {ans}')} {u(ans)}."
    stem = f"{intro} {what} if {num(have)} {u(have)} of {names[i]} {'is' if have == 1 else 'are'} used?"
    first = (f"{Name} {_is(names[i])} 1 part, so one part is {num(k)} {u(k)}." if ri == 1 else
             f"{Name} {_is(names[i])} {ri} parts, so one part is "
             f"{m(f'{have} \\div {ri} = {k}')} {u(k)}.")
    wrong = [
        (Q(have * rj), "multiplies by the number of parts without first finding the size of one part"),
        (Q(have + rj - ri), "adds or subtracts the difference in parts instead of scaling by the size of one part"),
    ]
    if j != "total":
        wrong.append((Q(S * k), f"gives the total amount of {prod}"))
        wrong.append((R(have * ri, rj), "flips the ratio"))
    else:
        wrong.append((Q(S * k - have), f"leaves out the {names[i]}"))
    return Problem(
        stem=stem, answer=Q(ans), fmt=unit(num, us_, up_), section="AR",
        wrong=wrong,
        steps=[first, last],
        near=_near(ans),
        check=Fraction(have, ri) * rj,
    )


def _two_stroke(rng):
    ratio = rng.choice([32, 40, 50])
    gal = Q(rng.choice([R(5, 4), R(5, 2), 5, 1, 2, 3, 4, R(3, 2)]))
    oz = gal * 128
    oil = oz / ratio
    need(oil.is_integer)
    eq = _fresh(rng, ["chainsaw", "generator", "outboard"], "stroke")
    what = {"chainsaw": "An engineer platoon's chainsaws run on",
            "generator": "A small two-stroke generator runs on",
            "outboard": "A boat's outboard motor runs on"}[eq]
    gtxt = m(mixed_raw(gal))
    stem = (f"{what} gasoline mixed with oil in the ratio {m(f'{ratio} : 1')} (gasoline to oil). "
            f"How many fluid ounces of oil should be mixed with {gtxt} "
            f"{'gallon' if gal == 1 else 'gallons'} of gasoline? (1 gallon $=$ 128 fluid ounces)")
    return Problem(
        stem=stem, answer=oil, fmt=unit(num, "fluid ounce"), section="AR",
        wrong=[
            (gal * 32 / ratio, "uses 32 ounces in a gallon (that is a quart)"),
            (gal * ratio, "makes two slips: multiplies the gallons by the ratio instead of dividing, "
             "and skips the change to ounces"),
            (oz / ratio * 2, None),
            (oz / ratio / 2, None),
        ],
        near=_near(oil),
        steps=[
            f"Change gallons to fluid ounces: {m(f'{mixed_raw(gal)} \\times 128 = {int_raw(oz)}')} fluid ounces of gasoline.",
            f"The oil is {m(F(1, ratio))} of the gasoline amount: "
            f"{m(f'{int_raw(oz)} \\div {ratio} = {int_raw(oil)}')} fluid ounces.",
        ],
        check=Fraction(int(gal * 4), 4) * 128 / ratio if (gal * 4).is_integer else oil,
    )


PLAN = [
    # level 1: warm-ups (10)
    (work_together, 1, 3),
    (solute_amount, 1, 3),
    (equal_workers, 1, 2),
    (ratio_mix, 1, 2),
    # level 2: test level (14)
    (work_together, 2, 2),
    (work_find_one, 2, 2),
    (fill_and_drain, 2, 2),
    (equal_workers, 2, 2),
    (mix_two_solutions, 2, 2),
    (concentration_change, 2, 1),
    (mix_prices, 2, 2),
    (ratio_mix, 2, 1),
    # level 3: challenge (11)
    (work_together, 3, 1),
    (work_find_one, 3, 1),
    (fill_and_drain, 3, 1),
    (crew_changes, 3, 2),
    (mix_two_solutions, 3, 2),
    (concentration_change, 3, 2),
    (mix_prices, 3, 2),
]
