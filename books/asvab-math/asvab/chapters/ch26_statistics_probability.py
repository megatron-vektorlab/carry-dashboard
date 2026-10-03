"""Chapter 26 - Averages, Statistics & Probability (Part IV word problems)."""
import functools
import itertools
import math
from fractions import Fraction

import sympy as sp

from ..core import (R, Q, Problem, Reject, need, num, dec, frac, money, unit, m, F,
                    dec_raw, int_raw, frac_raw, person, template,
                    x as X)

NUM = 26
TITLE = r"Averages, Statistics \& Probability"
PART = 4

INTRO = r"""
Averages and probability questions are short, but they hide traps: the wrong
count in a division, a list that was never put in order, or two chances
that were added when they should have been multiplied. Work with
\emph{totals} and \emph{counts}, and these problems become simple arithmetic.

\begin{concept}{Mean, median, mode, range}
\begin{itemize}
\item \textbf{Mean} (average) $=$ sum of the values $\div$ number of values.
\item \textbf{Median} $=$ the middle value \emph{after} putting the list in order.
  With an even number of values, average the two middle ones.
\item \textbf{Mode} $=$ the value that appears most often.
  \textbf{Range} $=$ largest value $-$ smallest value.
\end{itemize}
\end{concept}

\begin{concept}{Think in totals}
\[ \text{sum} = \text{mean} \times \text{number of values} \]
To find a missing score, a new average, or the average of two groups, turn
every average into a total first, do the adding or subtracting with totals,
then divide by the new count. Two groups of different sizes: add the two
totals and divide by the total number of people.
\end{concept}

\begin{concept}{Probability and counting}
\begin{itemize}
\item $P(\text{event}) = \dfrac{\text{number of favorable outcomes}}{\text{total number of outcomes}}$,
  a number from $0$ to $1$. \quad $P(\text{not } A) = 1 - P(A)$.
\item Independent events (``and''): \textbf{multiply}. A coin and a die:
  $P(\text{heads and } 6) = \frac12 \times \frac16 = \frac{1}{12}$.
\item Without replacement, the second draw has one fewer item in the bag.
\item Counting principle: multiply the number of choices at each step.
  Ordering $n$ things: $n \times (n-1) \times \cdots \times 1$.
  Choosing a group of 2 when order doesn't matter: $\frac{n(n-1)}{2}$.
\item Expected count $=$ probability $\times$ number of tries.
\end{itemize}
\end{concept}

\begin{example}{Worked example}
Maria scored 82, 88, and 91 on three tests. What must she score on the fourth
test to average 88 on all four?

\textbf{Solution.} For an average of 88 on 4 tests she needs a total of
$4 \times 88 = 352$ points. She has $82 + 88 + 91 = 261$. She needs
$352 - 261 = 91$ on the fourth test.
\end{example}

\begin{tip}
Check probability answers for size: a probability can never be more than 1,
and ``not'' events are usually the larger ones. For averages, the answer must
lie between the smallest and largest values.
\end{tip}

\begin{trap}
\begin{itemize}
\item Finding the median without first putting the numbers in order.
\item Averaging two averages when the groups have different sizes.
\item Answering with the target average when the question asks what score is
  \emph{needed}.
\item Adding probabilities for ``and'' events, or forgetting that a drawn item
  is not put back.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# private helpers
# --------------------------------------------------------------------------

def _lst(vals):
    """'$78$, $85$, and $92$' for running text."""
    vals = [int_raw(v) for v in vals]
    if len(vals) == 2:
        return f"${vals[0]}$ and ${vals[1]}$"
    return ", ".join(f"${v}$" for v in vals[:-1]) + f", and ${vals[-1]}$"


def _mlist(vals):
    """'$78$, $85$, $92$' for data sets (breakable between values)."""
    return ", ".join(f"${int_raw(v)}$" for v in vals)


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


def _sum_raw(vals):
    return " + ".join(int_raw(v) for v in vals)


def _median(vals):
    s = sorted(vals)
    k = len(s)
    return Q(s[k // 2]) if k % 2 else R(s[k // 2 - 1] + s[k // 2], 2)


def _near(ans, step=None):
    """Plausible fillers around a whole-number or decimal answer."""
    A = Q(ans)

    def f(rng):
        st = step
        if st is None:
            if A.is_integer:
                st = next(s_ for lim, s_ in ((12, 1), (30, 2), (80, 3), (200, 5), (600, 25),
                                              (10 ** 9, 100)) if A <= lim)
            else:
                st = R(1, sp.Rational(A).q)
        out = [A + k * st for k in (1, 2, 3, -1, -2, -3)]
        out = [v for v in out if v > 0]
        rng.shuffle(out)
        return out
    return f


def _near_prob(ans):
    """Fillers for a probability: same denominator, strictly between 0 and 1."""
    A = sp.Rational(Q(ans))

    def f(rng):
        d = A.q
        out = [A + R(k, d) for k in (1, 2, 3, -1, -2, -3)]
        out += [A / 2, 2 * A, 1 - A]
        out = [v for v in out if 0 < v < 1]
        rng.shuffle(out)
        return out
    return f


def _pfrac_steps(fav, total, what="favorable outcomes"):
    """'P = 7/20' with reduction shown when needed."""
    raw = F(int_raw(fav), int_raw(total))
    g = math.gcd(fav, total)
    if g != 1:
        raw += " = " + frac_raw(R(fav, total))
    return raw


def _cap(s):
    return s[0].upper() + s[1:]


_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
          "ten", "eleven", "twelve"]


def _w(n):
    """Small counts as words in running text ('four tests')."""
    return _WORDS[n] if 0 <= n < len(_WORDS) else num(n)


def _ordinal(n):
    return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")


_LAST = ["Ruiz", "Chen", "Walker", "Okafor", "Patel", "Novak", "Brooks", "Kim", "Santos",
         "Reyes", "Jensen", "Haddad", "Lopez", "Nguyen", "Carter", "Murphy"]


def _army(rng):
    """Army-style name for squad/platoon contexts ('Sergeant Kim')."""
    return f"{rng.choice(['Private', 'Specialist', 'Corporal', 'Sergeant', 'Staff Sergeant'])} {rng.choice(_LAST)}"


# --------------------------------------------------------------------------
# averages
# --------------------------------------------------------------------------

_MEAN_CTX = [
    # key, count range, value range
    ("scores", (4, 6), (65, 99)),
    ("pushups", (4, 6), (30, 75)),
    ("temps", (5, 7), (60, 95)),
    ("groceries", (4, 5), (60, 150)),
    ("ruck", (4, 6), (75, 105)),
    ("hours", (4, 6), (20, 45)),
    ("recruits", (5, 6), (6, 30)),
    ("miles", (5, 7), (2, 9)),
]


def _mean_stem(rng, key, vals, ask="mean"):
    n = len(vals)
    p = person(rng)
    word = {"mean": "mean (average)", "median": "median", "mode": "mode", "range": "range"}[ask]
    data = _lst(vals) if ask == "mean" else _mlist(vals)
    if key == "scores":
        return (f"{p} scored {data} on {_w(n)} practice tests." if ask == "mean" else
                f"{p}'s scores on {_w(n)} practice tests were {data}.") + \
            f" What is the {word} of {p.his} scores?"
    if key == "pushups":
        return (f"During a PT session, {_w(n)} soldiers did the following numbers of push-ups in two "
                f"minutes: {data}. What is the {word} number of push-ups?")
    if key == "temps":
        return (f"The daily high temperatures at a training base for {_w(n)} days were {data} "
                f"degrees Fahrenheit. What is the {word} of these temperatures?")
    if key == "groceries":
        if ask == "mean":
            data = ", ".join(money(v) for v in vals[:-1]) + f", and {money(vals[-1])}"
        return (f"{p} spent {data} on groceries over {_w(n)} weeks. What is the {word} amount "
                f"{p.he} spent per week?")
    if key == "ruck":
        return (f"A recruit's times on {_w(n)} six-mile ruck marches were {data} minutes. "
                f"What is the {word} of these times?")
    if key == "hours":
        return (f"Over {_w(n)} weeks, {p} worked {data} hours at a part-time job. What is the "
                f"{word} number of hours {p.he} worked per week?")
    if key == "recruits":
        return (f"A recruiting station enlisted {data} recruits in {_w(n)} months. What is the "
                f"{word} number of recruits per month?")
    return (f"During {_w(n)} days of training, a soldier ran {data} miles. What is the {word} "
            f"distance per day?")


def _vals_fmt(key):
    if key == "groceries":
        return money
    if key in ("ruck",):
        return unit(num, "minute")
    if key == "miles":
        return unit(num, "mile")
    return num


@template("AR")
@_retrying
def mean_basic(rng, lvl):
    key, (nlo, nhi), (vlo, vhi) = _fresh(rng, _MEAN_CTX, "mean")
    n = rng.randint(nlo, nhi)
    vals = [rng.randint(vlo, vhi) for _ in range(n)]
    S = sum(vals)
    need(S % n == 0 and len(set(vals)) >= n - 1)
    mean = Q(S // n)
    med = _median(vals)
    stem = _mean_stem(rng, key, vals, "mean")
    wrong = [
        (R(S, n - 1), "divides by one less than the number of values"),
        (Q(S), "is the total, not the average"),
        (R(max(vals) + min(vals), 2), "averages only the highest and lowest values"),
        (R(S, n + 1), "divides by one more than the number of values"),
    ]
    if med != mean:
        wrong.insert(0, (med, "is the median (the middle value), not the mean"))
    return Problem(
        stem=stem, answer=mean, fmt=_vals_fmt(key), section="AR",
        wrong=wrong,
        steps=[
            f"Add the {n} values: {m(_sum_raw(vals) + ' = ' + int_raw(S))}.",
            f"Divide by the number of values, {n}: {m(f'{int_raw(S)} \\div {n} = {int_raw(mean)}')}.",
        ],
        tip=f"Check: the mean must be between the smallest value ({num(min(vals))}) and the largest ({num(max(vals))}).",
        near=_near(mean),
        check=Fraction(sum(vals), len(vals)),
    )


_NEED_CTX = [
    # key, number of known values (k), value range, max allowed, target range
    ("tests", (3, 4), (68, 96), 100, (78, 92)),
    ("bowling", (3, 4), (120, 210), 300, (150, 190)),
    ("pushups", (3, 4), (35, 70), 90, (45, 65)),
    ("marks", (3, 4), (26, 39), 40, (30, 36)),
    ("miles", (3, 5), (8, 20), 30, (12, 18)),
    ("sales", (3, 4), (6, 25), 40, (12, 20)),
]


def _need_stem(rng, key, vals, target, more=1):
    p = person(rng)
    k = len(vals)
    tot = k + more
    nxt = "the next test" if more == 1 else "each of the next two tests"
    if key == "tests":
        return (f"{p} scored {_lst(vals)} on {_w(k)} math tests. What score does {p.he} need on "
                f"{nxt} to average {num(target)} on all {_w(tot)} tests?" if more == 1 else
                f"{p} scored {_lst(vals)} on {_w(k)} math tests. {p.He} wants to average "
                f"{num(target)} on all {_w(tot)} tests. If {p.he} earns the same score on each of "
                f"the next two tests, what score does {p.he} need on each one?")
    if key == "bowling":
        return (f"{p} bowled {_lst(vals)} in {_w(k)} games. What score does {p.he} need in the next "
                f"game to average {num(target)} for all {_w(tot)} games?" if more == 1 else
                f"{p} bowled {_lst(vals)} in {_w(k)} games. If {p.he} bowls the same score in each "
                f"of the next two games, what must that score be for {p.him} to average "
                f"{num(target)} for all {_w(tot)} games?")
    if key == "pushups":
        s = _army(rng)
        return (f"On {_w(k)} practice fitness tests, {s} did {_lst(vals)} push-ups. How many "
                f"push-ups must {s.split()[-1]} do on the next test to average {num(target)} "
                f"over all {_w(tot)} tests?" if more == 1 else
                f"On {_w(k)} practice fitness tests, {s} did {_lst(vals)} push-ups. To average "
                f"{num(target)} over {_w(tot)} tests, how many push-ups must {s.split()[-1]} do on "
                f"each of the next two tests, if both are the same?")
    if key == "marks":
        s = _army(rng)
        return (f"On a rifle range, {s} hit {_lst(vals)} targets out of 40 on {_w(k)} practice "
                f"rounds. How many hits does {s.split()[-1]} need on the next round to average "
                f"{num(target)} hits over all {_w(tot)} rounds?" if more == 1 else
                f"On a rifle range, {s} hit {_lst(vals)} targets out of 40 on {_w(k)} practice "
                f"rounds. To average {num(target)} hits over {_w(tot)} rounds, how many hits does "
                f"{s.split()[-1]} need on each of the next two rounds, if both are the same?")
    if key == "miles":
        return (f"While training for a marathon, {p} ran {_lst(vals)} miles in the first {_w(k)} "
                f"weeks. How many miles must {p.he} run in the next week to average "
                f"{num(target)} miles per week over {_w(tot)} weeks?" if more == 1 else
                f"While training for a marathon, {p} ran {_lst(vals)} miles in the first {_w(k)} "
                f"weeks. If {p.he} runs the same distance in each of the next two weeks, how "
                f"many miles must that be to average {num(target)} miles per week over {_w(tot)} weeks?")
    return (f"A salesperson sold {_lst(vals)} cars in the first {_w(k)} months of the year. How "
            f"many cars must the salesperson sell next month to average {num(target)} cars per "
            f"month over {_w(tot)} months?" if more == 1 else
            f"A salesperson sold {_lst(vals)} cars in the first {_w(k)} months of the year. If "
            f"the salesperson sells the same number in each of the next two months, how many "
            f"must that be to average {num(target)} cars per month over {_w(tot)} months?")


@template("AR")
@_retrying
def score_needed(rng, lvl):
    key, (klo, khi), (vlo, vhi), vmax, (tlo, thi) = _fresh(rng, _NEED_CTX, "need")
    k = rng.randint(klo, khi)
    vals = [rng.randint(vlo, vhi) for _ in range(k)]
    target = rng.randint(tlo, thi)
    S = sum(vals)
    more = 1 if lvl <= 2 else 2
    tot = k + more
    total_needed = target * tot
    rest = total_needed - S
    need(rest % more == 0)
    ans = rest // more
    need(vlo <= ans <= vmax and ans != target and abs(ans - target) >= 2)
    stem = _need_stem(rng, key, vals, target, more)
    cur_mean = R(S, k)
    wrong = [
        (Q(target), "is the target average, not the score needed"),
        (2 * target - cur_mean, "makes up the shortfall for only one test, not for all of them"),
        ((target + cur_mean) / 2, "averages the target with the current average"),
    ]
    if more == 2:
        u1 = {"tests": "test", "bowling": "game", "pushups": "test", "marks": "round",
              "miles": "week", "sales": "month"}[key]
        wrong.append((Q(rest), f"is the total for the next two {u1}s, not the amount for each"))
        wrong.append((Q(target * (k + 1) - S), f"plans for only one more {u1} instead of two"))
    steps = [
        f"To average {num(target)} over {tot} {'tests' if key in ('tests', 'pushups') else 'tries'}"
        .replace("tries", {"bowling": "games", "marks": "rounds", "miles": "weeks",
                           "sales": "months"}.get(key, "tries")) +
        f", the total must be {m(f'{target} \\times {tot} = {int_raw(total_needed)}')}.",
        f"The total so far is {m(_sum_raw(vals) + ' = ' + int_raw(S))}.",
    ]
    if more == 1:
        steps.append(f"Subtract: {m(f'{int_raw(total_needed)} - {int_raw(S)} = {int_raw(ans)}')}.")
    else:
        steps.append(f"The next two must add up to {m(f'{int_raw(total_needed)} - {int_raw(S)} = {int_raw(rest)}')}, "
                     f"so each one is {m(f'{int_raw(rest)} \\div 2 = {int_raw(ans)}')}.")
    return Problem(
        stem=stem, answer=Q(ans), fmt=num, section="AR",
        wrong=wrong,
        steps=steps,
        tip=(f"Check: {m(f'{_sum_raw(vals)} + {int_raw(ans)}' + (f' + {int_raw(ans)}' if more == 2 else '') + f' = {int_raw(total_needed)}')}, "
             f"and {m(f'{int_raw(total_needed)} \\div {tot} = {target}')}. \\checkmark"),
        near=_near(ans),
        verify=lambda v: Fraction(S + more * int(v), tot) == target,
        check=sp.solve(sp.Eq((S + more * X) / tot, target), X)[0],
    )


_AVG_CTX = [
    # key, n range, avg range, new value range
    ("weights", (6, 12), (150, 190), (120, 240)),
    ("ages", (8, 15), (20, 30), (17, 50)),
    ("class", (15, 30), (70, 90), (40, 100)),
    ("prices", (4, 8), (8, 30), (2, 60)),
    ("heights", (8, 12), (68, 74), (64, 82)),
]


@template("AR")
@_retrying
def average_change(rng, lvl):
    if lvl >= 3:
        return _missing_value(rng)
    key, (nlo, nhi), (alo, ahi), (vlo, vhi) = _fresh(rng, _AVG_CTX, "avg")
    n = rng.randint(nlo, nhi)
    A = rng.randint(alo, ahi)
    v = rng.randint(vlo, vhi)
    add = rng.random() < 0.6
    T = n * A
    n2 = n + 1 if add else n - 1
    newT = T + v if add else T - v
    need(newT % n2 == 0)
    ans = newT // n2
    need(ans != A and abs(v - A) >= 3)
    if key == "weights":
        s = _army(rng)
        stem = (f"The average weight of the {n} soldiers in a squad is {num(A)} pounds. "
                + (f"{s}, who weighs {num(v)} pounds, joins the squad. " if add else
                   f"{s}, who weighs {num(v)} pounds, transfers out of the squad. ")
                + "What is the new average weight of the squad?")
        fmt = unit(num, "pound")
    elif key == "ages":
        stem = (f"The average age of the {n} players on a softball team is {num(A)} years. "
                + (f"A new player who is {num(v)} years old joins the team. " if add else
                   f"A {num(v)}-year-old player leaves the team. ")
                + "What is the new average age of the players?")
        fmt = num
    elif key == "class":
        stem = (f"The average score of the {n} students who took a test is {num(A)}. "
                + (f"A student who missed the test takes it later and scores {num(v)}. "
                   "What is the new class average?" if add else
                   f"One student's score of {num(v)} is removed because the student was in the "
                   "wrong class. What is the average of the remaining scores?"))
        fmt = num
    elif key == "prices":
        p = person(rng)
        stem = (f"The average price of the {n} items in {p}'s shopping cart is {money(A)}. "
                + (f"{p.He} adds one more item that costs {money(v)}. " if add else
                   f"{p.He} puts back one item that costs {money(v)}. ")
                + "What is the new average price of the items in the cart?")
        fmt = money
    else:
        stem = (f"The average height of the {n} players on a basketball team is {num(A)} inches. "
                + (f"A player who is {num(v)} inches tall joins the team. " if add else
                   f"A player who is {num(v)} inches tall leaves the team. ")
                + "What is the new average height?")
        fmt = unit(num, "inch", "inches")
    op = "+" if add else "-"
    wrong = [
        (R(A + v, 2) if add else 2 * A - Q(v), "averages the old average with the new value" if add
         else "subtracts the value from twice the average"),
        (R(newT, n), f"divides by the old count, {n}, instead of {n2}"),
        (Q(A), "assumes the average does not change"),
        ((Q(A) + R(v, n2)) if add else (Q(A) - R(v, n2)),
         "adds the new value divided by the new count to the old average" if add else
         "subtracts the value divided by the new count from the old average"),
    ]
    return Problem(
        stem=stem, answer=Q(ans), fmt=fmt, section="AR",
        wrong=wrong,
        steps=[
            f"Turn the average into a total: {m(f'{n} \\times {int_raw(A)} = {int_raw(T)}')}.",
            f"{'Add' if add else 'Subtract'} the value: {m(f'{int_raw(T)} {op} {int_raw(v)} = {int_raw(newT)}')}.",
            f"Divide by the new count, {m(f'{n} {op} 1 = {n2}')}: {m(f'{int_raw(newT)} \\div {n2} = {int_raw(ans)}')}.",
        ],
        near=_near(ans),
        verify=lambda w: Q(w) * n2 == newT,
        check=Fraction(n * A + (v if add else -v), n2),
    )


def _missing_value(rng):
    kind = _fresh(rng, ["dropped", "added"], "missing", keep=1)
    if kind == "dropped":
        key = _fresh(rng, ["quiz", "range", "bowling"], "dropped")
        n = rng.randint(6, 12)
        A = rng.randint(70, 85) if key != "bowling" else rng.randint(140, 180)
        A2 = A + rng.randint(1, 4)
        v = n * A - (n - 1) * A2
        need(0 < v < A - 5 and (key != "range" or v <= 50))
        if key == "range":
            A = rng.randint(30, 44)
            A2 = A + rng.randint(1, 3)
            v = n * A - (n - 1) * A2
            need(10 <= v < A - 3 and A2 <= 48)
        s = _army(rng)
        p = person(rng)
        stem = {
            "quiz": (f"{p}'s average on {n} quizzes is {num(A)}. The teacher drops {p.his} lowest "
                     f"quiz score, and the average of the other {n - 1} quizzes is {num(A2)}. "
                     f"What was the score that was dropped?"),
            "range": (f"{s}'s average score on {n} rifle-qualification tables is {num(A)} out of "
                      f"50. If {s.split()[-1]}'s lowest score is thrown out, the average of the "
                      f"other {n - 1} is {num(A2)}. What was the lowest score?"),
            "bowling": (f"{p}'s average for {n} bowling games is {num(A)}. Without {p.his} worst "
                        f"game, the average of the other {n - 1} games is {num(A2)}. What did "
                        f"{p.he} score in the worst game?"),
        }[key]
        T1, T2 = n * A, (n - 1) * A2
        return Problem(
            stem=stem, answer=Q(v), fmt=num, section="AR",
            wrong=[
                (Q(A - (A2 - A)), "assumes the dropped score was as far below the average as the average went up"),
                (Q(n * A2 - n * A), f"uses {n} scores instead of {n - 1} for the new total"),
                (Q(A2 - A), "gives the change in the average, not the dropped score"),
                (Q(2 * A - A2), "subtracts the new average from twice the old one"),
            ],
            steps=[
                f"Total of all {n}: {m(f'{n} \\times {A} = {int_raw(T1)}')}.",
                f"Total of the other {n - 1}: {m(f'{n - 1} \\times {A2} = {int_raw(T2)}')}.",
                f"The dropped score is the difference: {m(f'{int_raw(T1)} - {int_raw(T2)} = {v}')}.",
            ],
            near=_near(v),
            verify=lambda w: Fraction(n * A - int(w), n - 1) == A2,
            check=sp.solve(sp.Eq((n * A - X) / (n - 1), A2), X)[0],
        )
    # a value is added and the average changes
    key = _fresh(rng, ["recruits", "donations", "temps"], "added")
    n = rng.randint(4, 9)
    A = {"recruits": rng.randint(15, 30), "donations": rng.randint(20, 60),
         "temps": rng.randint(55, 80)}[key]
    A2 = A + rng.choice([-3, -2, -1, 1, 2, 3, 4])
    v = (n + 1) * A2 - n * A
    need(v > 0 and v != A2 and abs(v - A) >= 4)
    stem = {
        "recruits": (f"Over {n} weeks, a recruiting office averaged {num(A)} new enlistments per "
                     f"week. After one more week, the average for all {n + 1} weeks is "
                     f"{num(A2)}. How many people enlisted in that last week?"),
        "donations": (f"A food drive collected an average of {num(A)} cans per day for {n} days. "
                      f"After one more day, the average for all {n + 1} days is {num(A2)} cans. "
                      f"How many cans were collected on the last day?"),
        "temps": (f"The average high temperature for the first {n} days of a training exercise "
                  f"was {num(A)} degrees. Including the next day, the average for all {n + 1} days "
                  f"is {num(A2)} degrees. What was the high temperature on that day?"),
    }[key]
    T1, T2 = n * A, (n + 1) * A2
    return Problem(
        stem=stem, answer=Q(v), fmt=num, section="AR",
        wrong=[
            (Q(A2), "is the new average, not the new value"),
            (Q(A2 + (A2 - A)), "adds the change in the average to the new average"),
            (Q(n * A2 - n * A + A), None),
            (Q(T2), f"is the total for all {n + 1}, not the last value"),
            (Q(abs(A2 - A)), "gives the change in the average"),
        ],
        steps=[
            f"Total for the first {n}: {m(f'{n} \\times {A} = {int_raw(T1)}')}.",
            f"Total for all {n + 1}: {m(f'{n + 1} \\times {A2} = {int_raw(T2)}')}.",
            f"The new value is the difference: {m(f'{int_raw(T2)} - {int_raw(T1)} = {v}')}.",
        ],
        near=_near(v),
        verify=lambda w: Fraction(n * A + int(w), n + 1) == A2,
        check=sp.solve(sp.Eq((n * A + X) / (n + 1), A2), X)[0],
    )


_SPREAD_CTX = [
    # key, value range, odd sizes, even sizes
    ("scores", (60, 99)),
    ("pushups", (25, 75)),
    ("temps", (55, 95)),
    ("recruits", (5, 30)),
    ("heights", (64, 78)),
    ("ages", (18, 29)),
    ("run", (13, 20)),
]


def _spread_stem(rng, key, vals, ask):
    word = {"median": "median", "mode": "mode", "range": "range"}[ask]
    data = _mlist(vals)
    n = len(vals)
    if key == "scores":
        return f"The scores of {_w(n)} students on a quiz were {data}. What is the {word} of the scores?"
    if key == "pushups":
        return (f"In a PT test, the soldiers of a squad did these numbers of push-ups: {data}. "
                f"What is the {word} of the data?")
    if key == "temps":
        return (f"The daily high temperatures (in degrees Fahrenheit) for {_w(n)} days were {data}. "
                f"What is the {word} of the temperatures?")
    if key == "recruits":
        return (f"The numbers of recruits who enlisted at a recruiting station in each of {_w(n)} "
                f"months were {data}. What is the {word}?")
    if key == "heights":
        return (f"The heights, in inches, of the {_w(n)} players on a basketball team are {data}. "
                f"What is the {word} of their heights?")
    if key == "ages":
        return (f"The ages of the {_w(n)} recruits in a training group are {data}. What is the "
                f"{word} of their ages?")
    return (f"The times, in minutes, of {_w(n)} soldiers on a two-mile run were {data}. What is "
            f"the {word} of the times?")


@template("AR")
@_retrying
def center_spread(rng, lvl):
    key, (vlo, vhi) = _fresh(rng, _SPREAD_CTX, "spread")
    if lvl >= 2:
        n = rng.choice([6, 6, 8])
        vals = [rng.randint(vlo, vhi) for _ in range(n)]
        s = sorted(vals)
        need(len(set(vals)) >= n - 1)
        a_, b_ = s[n // 2 - 1], s[n // 2]
        need(b_ - a_ >= 1)
        med = R(a_ + b_, 2)
        unsorted_mid = R(vals[n // 2 - 1] + vals[n // 2], 2)
        need(unsorted_mid != med)
        mean = R(sum(vals), n)
        stem = _spread_stem(rng, key, vals, "median")
        wrong = [
            (Q(a_), "uses only one of the two middle values"),
            (Q(b_), "uses only one of the two middle values"),
            (unsorted_mid, "averages the two middle numbers without putting the list in order first"),
        ]
        if (mean * 10).is_integer:
            wrong.append((mean, "is the mean, not the median"))
        return Problem(
            stem=stem, answer=med, fmt=dec, section="AR",
            wrong=wrong,
            steps=[
                f"Put the {n} values in order: {_mlist(s)}.",
                f"With an even number of values, the median is the average of the two middle ones "
                f"(the {_ordinal(n // 2)} and {_ordinal(n // 2 + 1)}): "
                f"{m(f'({a_} + {b_}) \\div 2 = {a_ + b_} \\div 2 = {dec_raw(med)}')}.",
            ],
            near=_near(med, step=R(1, 2)),
            check=Fraction(a_ + b_, 2),
        )
    ask = rng.choice(["median", "median", "mode", "range"])
    n = rng.choice([5, 7])
    if ask == "mode":
        n = rng.choice([6, 7, 8])
        base = rng.sample(range(vlo, vhi + 1), n - 1)
        mode_v = rng.choice(base)
        vals = base + [mode_v]
        if rng.random() < 0.3 and n >= 7:
            vals = vals[:-2] + [mode_v, mode_v]
            need(vals.count(mode_v) == 3 and len(set(vals)) == n - 2)
        rng.shuffle(vals)
        cnt = vals.count(mode_v)
        med = _median(vals)
        mean = R(sum(vals), n)
        stem = _spread_stem(rng, key, vals, "mode")
        return Problem(
            stem=stem, answer=Q(mode_v), fmt=num, section="AR",
            wrong=[
                (Q(cnt), "gives how many times the mode appears, not the mode itself"),
                (med, "is the median, not the mode"),
                (mean, "is the mean, not the mode"),
                (Q(max(vals)), "gives the largest value, not the most frequent one"),
                (Q(max(vals) - min(vals)), "is the range, not the mode"),
            ],
            steps=[
                f"Put the values in order to spot repeats: {_mlist(sorted(vals))}.",
                f"The value {num(mode_v)} appears {'twice' if cnt == 2 else 'three times'}, more than any other value, so the "
                f"mode is {num(mode_v)}.",
            ],
            near=_near(mode_v),
            check=Q(max(set(vals), key=vals.count)),
        )
    vals = rng.sample(range(vlo, vhi + 1), n)
    s = sorted(vals)
    if ask == "median":
        med = Q(s[n // 2])
        need(Q(vals[n // 2]) != med)
        mean = R(sum(vals), n)
        stem = _spread_stem(rng, key, vals, "median")
        return Problem(
            stem=stem, answer=med, fmt=num, section="AR",
            wrong=[
                (Q(vals[n // 2]), "takes the middle number of the list without putting it in order first"),
                (mean, "is the mean, not the median"),
                (Q(s[n // 2 + 1]), None),
                (Q(s[-1] - s[0]), "is the range, not the median"),
            ],
            steps=[
                f"Put the {n} values in order: {_mlist(s)}.",
                f"The middle value is the {_ordinal(n // 2 + 1)} one ({n // 2} values on each side), so "
                f"the median is {num(med)}.",
            ],
            near=_near(med),
            check=Q(sorted(vals)[len(vals) // 2]),
        )
    rng_ = s[-1] - s[0]
    need(vals[-1] - vals[0] != rng_ and vals[-1] != s[-1] or vals[0] != s[0])
    stem = _spread_stem(rng, key, vals, "range")
    wrong = [
        (Q(s[-1]), "gives the largest value, not the range"),
        (Q(abs(vals[-1] - vals[0])), "subtracts the first value listed from the last one listed"),
        (_median(vals), "is the median, not the range"),
        (Q(s[-1] - s[1]), None),
    ]
    return Problem(
        stem=stem, answer=Q(rng_), fmt=num, section="AR",
        wrong=wrong,
        steps=[
            f"Find the largest and smallest values: the largest is {num(s[-1])} and the smallest "
            f"is {num(s[0])}.",
            f"Range $=$ largest $-$ smallest $=$ {m(f'{s[-1]} - {s[0]} = {rng_}')}.",
        ],
        near=_near(rng_),
        check=Q(max(vals) - min(vals)),
    )


_WAVG_CTX = ["platoons", "classes", "games", "shifts", "flights"]


@template("AR")
@_retrying
def weighted_average(rng, lvl):
    if lvl >= 3:
        return _weighted_reverse(rng)
    key = _fresh(rng, _WAVG_CTX, "wavg")
    if key == "platoons":
        n1, n2 = rng.randint(20, 40), rng.randint(20, 40)
        a1, a2 = rng.randint(70, 95), rng.randint(70, 95)
        stem = (f"On a fitness test, the {num(n1)} soldiers of 1st Platoon averaged {num(a1)} "
                f"points and the {num(n2)} soldiers of 2nd Platoon averaged {num(a2)} points. What "
                f"is the average score of all the soldiers in the two platoons?")
        fmt, who = num, "soldiers"
    elif key == "classes":
        n1, n2 = rng.randint(15, 35), rng.randint(15, 35)
        a1, a2 = rng.randint(65, 95), rng.randint(65, 95)
        stem = (f"In one class, {num(n1)} students averaged {num(a1)} on a test. In another class, "
                f"{num(n2)} students averaged {num(a2)} on the same test. What is the average score "
                f"of all the students in both classes?")
        fmt, who = num, "students"
    elif key == "games":
        n1, n2 = rng.randint(4, 12), rng.randint(4, 12)
        a1, a2 = rng.randint(8, 25), rng.randint(8, 25)
        p = person(rng)
        stem = (f"{p} averaged {num(a1)} points per game in {p.his} first {num(n1)} basketball "
                f"games and {num(a2)} points per game in the next {num(n2)} games. What was "
                f"{p.his} average for all the games?")
        fmt, who = num, "games"
    elif key == "shifts":
        n1, n2 = rng.randint(4, 15), rng.randint(4, 15)
        a1, a2 = rng.randint(14, 22), rng.randint(16, 26)
        stem = (f"A warehouse has {num(n1)} day-shift workers who earn an average of {money(a1)} per "
                f"hour and {num(n2)} night-shift workers who earn an average of {money(a2)} per "
                f"hour. What is the average hourly pay of all these workers?")
        fmt, who = money, "workers"
    else:
        n1, n2 = rng.randint(10, 30), rng.randint(10, 30)
        a1, a2 = rng.randint(14, 19), rng.randint(14, 19)
        stem = (f"On a two-mile run, the {num(n1)} airmen in A Flight averaged {num(a1)} minutes "
                f"and the {num(n2)} airmen in B Flight averaged {num(a2)} minutes. What was the "
                f"average time for all the airmen?")
        fmt, who = unit(num, "minute"), "airmen"
    need(n1 != n2 and abs(a1 - a2) >= 2)
    T1, T2 = n1 * a1, n2 * a2
    ans = R(T1 + T2, n1 + n2)
    need(ans.is_integer and ans != R(a1 + a2, 2))
    return Problem(
        stem=stem, answer=ans, fmt=fmt, section="AR",
        wrong=[
            (R(a1 + a2, 2), "averages the two averages without weighting by group size"),
            (R(n1 * a2 + n2 * a1, n1 + n2), "weights each average by the other group's size"),
            (Q(T1 + T2), "is the combined total, not the average"),
            (R(T1 + T2, 2), "divides the combined total by 2 instead of by the number of " + who),
        ],
        steps=[
            f"Turn each average into a total: {m(f'{n1} \\times {a1} = {int_raw(T1)}')} and "
            f"{m(f'{n2} \\times {a2} = {int_raw(T2)}')}.",
            f"Add the totals and the counts: {m(f'{int_raw(T1)} + {int_raw(T2)} = {int_raw(T1 + T2)}')} "
            f"for {m(f'{n1} + {n2} = {n1 + n2}')} {who}.",
            f"Divide: {m(f'{int_raw(T1 + T2)} \\div {n1 + n2} = {int_raw(ans)}')}.",
        ],
        tip=f"Check: the answer is closer to the average of the larger group ({num(max(n1, n2))} {who}).",
        near=_near(ans),
        check=Fraction(n1 * a1 + n2 * a2, n1 + n2),
    )


def _weighted_reverse(rng):
    kind = _fresh(rng, ["group", "grade"], "wrev", keep=1)
    if kind == "group":
        key = _fresh(rng, ["class", "company", "team"], "wgroup")
        n1 = rng.randint(8, 20)
        n2 = rng.randint(6, 20)
        a1 = rng.randint(70, 90) if key != "team" else rng.randint(160, 190)
        c = a1 + rng.choice([-4, -3, -2, 2, 3, 4]) if key != "team" else a1 + rng.choice([-6, -4, 4, 6])
        T = (n1 + n2) * c
        rest = T - n1 * a1
        need(rest % n2 == 0)
        a2 = rest // n2
        need(abs(a2 - a1) >= 3 and (a2 <= 100 if key != "team" else 140 <= a2 <= 220)
             and a2 != 2 * c - a1)
        stem = {
            "class": (f"In a class of {num(n1 + n2)} students, the {num(n1)} boys averaged {num(a1)} on a "
                      f"test, and the whole class averaged {num(c)}. What was the average score of the "
                      f"girls?"),
            "company": (f"A company of {num(n1 + n2)} soldiers took a fitness test. The {num(n1)} soldiers "
                        f"of the first group averaged {num(a1)} points, and the whole company averaged "
                        f"{num(c)} points. What was the average score of the other {num(n2)} soldiers?"),
            "team": (f"A bowling league has {num(n1 + n2)} members. The {num(n1)} members of the morning "
                     f"group average {num(a1)}, and the whole league averages {num(c)}. What is the "
                     f"average of the evening group?"),
        }[key]
        other = {"class": "girls", "company": "other soldiers", "team": "evening group"}[key]
        have = "has" if key == "team" else "have"
        return Problem(
            stem=stem, answer=Q(a2), fmt=num, section="AR",
            wrong=[
                (Q(2 * c - a1), "assumes the two groups are the same size"),
                (Q(rest), f"is the total for the {other}, not their average"),
                (Q(c), "gives the average of the whole group"),
                (R(T - a1, n2), "subtracts the first group's average instead of its total"),
            ],
            steps=[
                f"Total for everyone: {m(f'{n1 + n2} \\times {c} = {int_raw(T)}')}.",
                f"Total for the first group: {m(f'{n1} \\times {a1} = {int_raw(n1 * a1)}')}.",
                f"The {other} {have} {m(f'{int_raw(T)} - {int_raw(n1 * a1)} = {int_raw(rest)}')} points in "
                f"all, so their average is {m(f'{int_raw(rest)} \\div {n2} = {a2}')}.",
            ],
            near=_near(a2),
            verify=lambda v: Fraction(n1 * a1 + n2 * int(v), n1 + n2) == c,
            check=sp.solve(sp.Eq((n1 * a1 + n2 * X) / (n1 + n2), c), X)[0],
        )
    # course grade with weights
    wt, wf = rng.choice([(60, 40), (70, 30), (75, 25), (50, 50), (80, 20)])
    avg = rng.randint(70, 92)
    goal = rng.randint(75, 92)
    final = R(goal * 100 - wt * avg, wf)
    need(final.is_integer and 60 <= final <= 100 and final != goal and abs(final - goal) >= 3)
    p = person(rng)
    school = rng.choice([("a technical training course", "class"),
                         ("an Army mechanic course", "course"),
                         ("a community college course", "course")])
    stem = (f"In {school[0]}, the unit tests count for {m(f'{wt}\\%')} of the final grade and the "
            f"final exam counts for {m(f'{wf}\\%')}. {p} has a test average of {num(avg)}. What "
            f"score does {p.he} need on the final exam to earn a final grade of {num(goal)}?")
    part = R(wt * avg, 100)
    wd, fd = dec_raw(R(wt, 100)), dec_raw(R(wf, 100))
    return Problem(
        stem=stem, answer=final, fmt=num, section="AR",
        wrong=[
            (Q(goal), "is the final grade wanted, not the exam score needed"),
            (Q(2 * goal - avg), "treats the tests and the final as if they counted equally"),
            (Q(goal) - part, "forgets to divide by the final exam's weight"),
            (Q(goal + (goal - avg)), None),
        ],
        steps=[
            f"The tests contribute {m(f'{wd} \\times {avg} = {dec_raw(part)}')} points to the grade.",
            f"The final must contribute {m(f'{goal} - {dec_raw(part)} = {dec_raw(goal - part)}')} points.",
            f"The final counts {m(f'{wf}\\%')}, so the exam score is "
            f"{m(f'{dec_raw(goal - part)} \\div {fd} = {int_raw(final)}')}.",
        ],
        tip=f"Check: {m(f'{wd}({avg}) + {fd}({int_raw(final)}) = {dec_raw(part)} + {dec_raw(R(wf, 100) * final)} = {goal}')}. \\checkmark",
        near=_near(final),
        verify=lambda v: R(wt * avg + wf * Q(v), 100) == goal,
        check=sp.solve(sp.Eq(R(wt, 100) * avg + R(wf, 100) * X, goal), X)[0],
    )


# --------------------------------------------------------------------------
# probability
# --------------------------------------------------------------------------

def _bag(rng, lvl):
    """A container of colored/labeled items: (intro text, names, counts, noun)."""
    key = _fresh(rng, ["marbles", "mre", "roster", "socks", "candy", "ammo"], "bag")
    if key == "marbles":
        names = rng.sample(["red", "blue", "green", "yellow", "white"], 3)
        counts = [rng.randint(2, 12) for _ in names]
        txt = (f"A bag holds {_and_list([f'{num(c)} {nm}' for nm, c in zip(names, counts)])} marbles.")
        return txt, names, counts, "marble", key
    if key == "mre":
        names = ["chili mac", "beef stew", "vegetarian", "chicken"]
        while True:
            counts = [rng.randint(1, 5) for _ in names]
            if sum(counts) == 12:
                break
        txt = (f"A case of 12 MREs (meals) holds {_and_list([f'{num(c)} {nm}' for nm, c in zip(names, counts)])} "
               f"meals. A soldier grabs one meal without looking.")
        return txt, names, counts, "meal", key
    if key == "roster":
        names = ["privates", "specialists", "corporals"]
        counts = [rng.randint(3, 12), rng.randint(3, 10), rng.randint(2, 6)]
        txt = (f"For a weekend duty assignment, the names of {num(counts[0])} privates, "
               f"{num(counts[1])} specialists, and {num(counts[2])} corporals are put in a helmet, "
               f"and one name is drawn at random.")
        return txt, names, counts, "name", key
    if key == "socks":
        names = rng.sample(["black", "white", "gray", "blue"], 3)
        counts = [rng.choice([2, 4, 6, 8, 10]) for _ in names]
        txt = f"A drawer holds {_and_list([f'{num(c)} {nm}' for nm, c in zip(names, counts)])} socks."
        return txt, names, counts, "sock", key
    if key == "candy":
        names = rng.sample(["cherry", "lemon", "grape", "orange", "lime"], 3)
        counts = [rng.randint(3, 15) for _ in names]
        txt = (f"A jar contains {_and_list([f'{num(c)} {nm}' for nm, c in zip(names, counts)])} "
               f"hard candies.")
        return txt, names, counts, "candy", key
    names = ["tracer", "standard"]
    counts = [rng.randint(2, 8), rng.randint(10, 30)]
    txt = (f"A box holds {num(counts[0])} tracer rounds and {num(counts[1])} standard rounds "
           f"of training ammunition.")
    return txt, names, counts, "round", key


def _and_list(items):
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + ", and " + items[-1]


def _pick_q(key, noun, name):
    if key == "mre":
        return f"What is the probability that the meal is {name}?"
    if key == "roster":
        return f"What is the probability that the name drawn is one of the {name}?"
    if key == "ammo":
        return f"If one round is taken at random, what is the probability that it is a {name} round?"
    return f"If one {noun} is picked at random, what is the probability that it is {name}?"


@template("AR")
@_retrying
def simple_prob(rng, lvl):
    kind = _fresh(rng, ["bag", "cards", "raffle"], "sp", keep=1)
    if kind == "bag":
        txt, names, counts, noun, key = _bag(rng, lvl)
        i = rng.randrange(len(names))
        fav, total = counts[i], sum(counts)
        need(len(set(counts)) == len(counts) and fav < total)
        ans = R(fav, total)
        stem = f"{txt} {_pick_q(key, noun, names[i])}"
        items = [nm for nm, c in zip(names, counts) for _ in range(c)]
        steps = [
            f"Count all the {noun}{'s' if noun != 'candy' else ''}: "
            f"{m(' + '.join(str(c) for c in counts) + f' = {total}')}.".replace("candys", "candies"),
            f"Favorable outcomes: {fav}. Probability $=$ {m(_pfrac_steps(fav, total))}.",
        ]
        steps[0] = steps[0].replace("candy:", "candies:")
        wrong = [
            (R(fav, total - fav), "compares the favorable outcomes to the unfavorable ones instead of to the total"),
            (R(1, len(names)), "assumes each kind is equally likely"),
            (1 - ans, f"is the probability of \\emph{{not}} getting {names[i]}"),
            (R(1, total) if fav > 1 else R(1, fav), "counts only one of the favorable items" if fav > 1 else None),
        ]
        check = Fraction(sum(1 for it in items if it == names[i]), len(items))
    elif kind == "cards":
        N = rng.choice([10, 12, 15, 20, 24, 25, 30])
        k = rng.choice([3, 4, 5, 6])
        sub = rng.choice(["mult", "greater"])
        if sub == "mult":
            fav = N // k
            cond = f"a multiple of {k}"
            how = (f"The multiples of {k} from 1 to {N} are "
                   f"{m(', '.join(str(k * j) for j in range(1, fav + 1)))}: {fav} cards.")
            items = [c for c in range(1, N + 1) if c % k == 0]
        else:
            t = rng.randint(N // 2, N - 2)
            fav = N - t
            cond = f"greater than {t}"
            how = f"The numbers greater than {t} are {t + 1} through {N}: {m(f'{N} - {t} = {fav}')} cards."
            items = [c for c in range(1, N + 1) if c > t]
        need(1 < fav < N)
        ans = R(fav, N)
        stem = (f"Cards numbered 1 through {N} are placed in a box, and one card is drawn at random. "
                f"What is the probability that the number on the card is {cond}?")
        steps = [how, f"There are {N} cards in all, so the probability is {m(_pfrac_steps(fav, N))}."]
        wrong = [
            (R(fav, N - fav), "compares the favorable cards to the unfavorable ones instead of to all the cards"),
            (1 - ans, "is the probability that the card is \\emph{not} " + cond),
            (R(fav + 1, N), "miscounts the favorable cards by one"),
            (R(fav - 1, N) if fav > 1 else R(fav, N + 1), "miscounts the favorable cards by one"),
            (R(1, k) if sub == "mult" else R(t, N), None),
        ]
        check = Fraction(len(items), N)
    else:
        sold = rng.choice([100, 120, 150, 200, 240, 250, 300, 400, 500])
        mine = rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25])
        need(mine < sold // 4)
        ans = R(mine, sold)
        p = person(rng)
        org = rng.choice(["a school fundraiser", "the base's holiday party", "a fire department benefit"])
        stem = (f"For a raffle at {org}, {num(sold)} tickets are sold and one winning ticket is drawn. "
                f"{p} bought {num(mine)} tickets. What is the probability that {p.he} wins?")
        steps = [
            f"Favorable outcomes: {p.his} {mine} tickets. Total outcomes: {num(sold)} tickets.",
            f"Probability $=$ {m(_pfrac_steps(mine, sold))}.",
        ]
        wrong = [
            (R(mine, sold - mine), "compares the tickets bought to the tickets not bought instead of to all tickets"),
            (R(1, sold), "uses only one ticket"),
            (1 - ans, "is the probability of \\emph{not} winning"),
            (R(1, mine), None),
        ]
        check = Fraction(len([t for t in range(sold) if t < mine]), sold)
    return Problem(stem=stem, answer=ans, fmt=frac, section="AR", wrong=wrong, steps=steps,
                   near=_near_prob(ans), check=check)


@template("AR")
@_retrying
def prob_complement(rng, lvl):
    kind = _fresh(rng, ["bag", "vehicles", "die", "raffle"], "comp")
    if kind == "bag":
        txt, names, counts, noun, key = _bag(rng, lvl)
        need(len(names) >= 3)
        i = rng.randrange(len(names))
        two = rng.random() < 0.4
        j = (i + 1) % len(names)
        bad = counts[i] + (counts[j] if two else 0)
        total = sum(counts)
        fav = total - bad
        need(len(set(counts)) == len(counts) and 0 < fav < total)
        excl = (f"{names[i]} or {names[j]}" if two else names[i])
        if key == "roster":
            q = (f"What is the probability that the name drawn is \\emph{{not}} one of the "
                 f"{names[i]}" + (f" or {names[j]}?" if two else "?"))
        elif key == "mre":
            q = (f"What is the probability that the meal is \\emph{{neither}} {names[i]} nor {names[j]}?"
                 if two else f"What is the probability that the meal is \\emph{{not}} {names[i]}?")
        else:
            nn = noun if key != "ammo" else "round"
            q = (f"If one {nn} is picked at random, what is the probability that it is "
                 + (f"\\emph{{neither}} {names[i]} nor {names[j]}?" if two else f"\\emph{{not}} {names[i]}?"))
        stem = f"{txt} {q}"
        items = [nm for nm, c in zip(names, counts) for _ in range(c)]
        ex = {names[i]} | ({names[j]} if two else set())
        check = Fraction(sum(1 for it in items if it not in ex), len(items))
        ans = R(fav, total)
        steps = [
            f"Total: {m(' + '.join(str(c) for c in counts) + f' = {total}')}. "
            f"The ones that are {excl}: {m(f'{counts[i]} + {counts[j]} = {bad}') if two else num(bad)}.",
            f"The rest, {m(f'{total} - {bad} = {fav}')}, are favorable. Probability $=$ "
            f"{m(_pfrac_steps(fav, total))}.",
        ]
        tip = f"Or use $1 - P$: {m(f'1 - {F(bad, total)} = {F(fav, total)}')}."
        wrong = [
            (R(bad, total), "is the probability of the event happening, not of it \\emph{not} happening"),
            (R(fav, bad), "compares favorable to unfavorable instead of to the total"),
            (R(counts[j], total) if two else R(len(names) - 1, len(names)),
             "leaves out one of the excluded kinds" if two else "assumes each kind is equally likely"),
        ]
    elif kind == "vehicles":
        total = rng.choice([20, 24, 30, 36, 40, 45, 48, 50, 60])
        bad = rng.randint(2, total // 3)
        fav = total - bad
        stem = (f"A motor pool has {num(total)} vehicles, and {num(bad)} of them are down for "
                f"maintenance. If one vehicle is picked at random for a convoy, what is the "
                f"probability that it is \\emph{{not}} down for maintenance?")
        ans = R(fav, total)
        steps = [f"Vehicles not in maintenance: {m(f'{total} - {bad} = {fav}')}.",
                 f"Probability $=$ {m(_pfrac_steps(fav, total))}."]
        tip = None
        wrong = [
            (R(bad, total), "is the probability that the vehicle \\emph{is} down for maintenance"),
            (R(fav, bad), "compares good vehicles to broken ones instead of to the total"),
            (R(bad, fav), None),
        ]
        check = Fraction(sum(1 for v in range(total) if v >= bad), total)
    elif kind == "die":
        t = rng.choice([2, 3, 4, 5])
        cond = rng.choice(["greater", "less"])
        if cond == "greater":
            bad = 6 - t
            desc = f"greater than {t}"
            good = [f for f in range(1, 7) if not f > t]
        else:
            bad = t - 1
            desc = f"less than {t}"
            good = [f for f in range(1, 7) if not f < t]
        need(0 < bad < 6)
        fav = 6 - bad
        stem = (f"A fair six-sided die is rolled once. What is the probability that the number "
                f"rolled is \\emph{{not}} {desc}?")
        ans = R(fav, 6)
        bads = [f for f in range(1, 7) if f not in good]
        steps = [f"The outcomes that are {desc}: {m(', '.join(map(str, bads)))} ({bad} of them).",
                 f"The other {fav} outcomes are favorable: {m(_pfrac_steps(fav, 6))}."]
        tip = None
        wrong = [
            (R(bad, 6), f"is the probability that the number \\emph{{is}} {desc}"),
            (R(fav, bad) if fav < bad else R(bad, fav), "compares favorable to unfavorable outcomes"),
            (R(1, 6), "counts only one outcome"),
        ]
        check = Fraction(len(good), 6)
    else:
        sold = rng.choice([100, 120, 150, 200, 250, 300, 400, 500])
        mine = rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25])
        need(mine < sold // 4)
        p = person(rng)
        stem = (f"At a charity raffle, {num(sold)} tickets are sold and one winning ticket is drawn. "
                f"{p} bought {num(mine)} tickets. What is the probability that {p.he} does "
                f"\\emph{{not}} win?")
        fav = sold - mine
        ans = R(fav, sold)
        steps = [f"Tickets {p.he} did not buy: {m(f'{int_raw(sold)} - {mine} = {int_raw(fav)}')}.",
                 f"Probability $=$ {m(_pfrac_steps(fav, sold))}."]
        tip = None
        wrong = [
            (R(mine, sold), f"is the probability that {p.he} \\emph{{does}} win"),
            (1 - R(1, sold), "subtracts only one ticket"),
            (R(mine, fav), "compares the tickets bought to the tickets not bought"),
        ]
        check = Fraction(len([t for t in range(sold) if t >= mine]), sold)
    return Problem(stem=stem, answer=ans, fmt=frac, section="AR", wrong=wrong, steps=steps,
                   tip=tip, near=_near_prob(ans), check=check)


@template("AR")
@_retrying
def independent_events(rng, lvl):
    kind = _fresh(rng, ["coin_die", "two_dice", "spinner_die", "replace", "shots", "radios"], "indep")
    if kind in ("coin_die", "two_dice", "spinner_die"):
        die_t = rng.choice([("even", lambda f: f % 2 == 0), ("odd", lambda f: f % 2 == 1),
                            ("greater than 4", lambda f: f > 4), ("less than 3", lambda f: f < 3),
                            ("a 6", lambda f: f == 6), ("a 1 or a 2", lambda f: f in (1, 2)),
                            ("a multiple of 3", lambda f: f % 3 == 0)])
        if kind == "coin_die":
            side = rng.choice(["heads", "tails"])
            stem = (f"A coin is tossed and a six-sided die is rolled. What is the probability of "
                    f"getting {side} on the coin and {'an' if die_t[0] in ('even', 'odd') else ''}"
                    f"{' ' if die_t[0] in ('even', 'odd') else ''}{die_t[0]}"
                    f"{' number' if die_t[0] in ('even', 'odd') else ''} on the die?")
            stem = stem.replace("and  ", "and ")
            first = (R(1, 2), "the coin", 1, 2, f"{side}")
            outs = list(itertools.product(["heads", "tails"], range(1, 7)))
            ok = sum(1 for c, f in outs if c == side and die_t[1](f))
            check = Fraction(ok, len(outs))
        elif kind == "two_dice":
            t2 = rng.choice([("even", lambda f: f % 2 == 0), ("greater than 3", lambda f: f > 3),
                             ("a 6", lambda f: f == 6), ("less than 5", lambda f: f < 5)])
            stem = (f"Two six-sided dice, one red and one blue, are rolled. What is the probability "
                    f"that the red die shows {'an even number' if t2[0] == 'even' else t2[0]} and the "
                    f"blue die shows {'an even number' if die_t[0] == 'even' else 'an odd number' if die_t[0] == 'odd' else die_t[0]}?")
            c1 = sum(1 for f in range(1, 7) if t2[1](f))
            first = (R(c1, 6), "the red die", c1, 6, t2[0])
            outs = list(itertools.product(range(1, 7), range(1, 7)))
            ok = sum(1 for a_, b_ in outs if t2[1](a_) and die_t[1](b_))
            check = Fraction(ok, len(outs))
        else:
            secs = rng.choice([4, 5, 8])
            colors = {4: ["red", "blue", "green", "yellow"],
                      5: ["red", "blue", "green", "yellow", "white"],
                      8: ["red", "blue", "green", "yellow", "white", "black", "orange", "purple"]}[secs]
            col = rng.choice(colors)
            stem = (f"A spinner has {secs} equal sections, each a different color, one of them {col}. "
                    f"The spinner is spun once and a six-sided die is rolled once. What is the "
                    f"probability that the spinner lands on {col} and the die shows "
                    f"{'an even number' if die_t[0] == 'even' else 'an odd number' if die_t[0] == 'odd' else die_t[0]}?")
            first = (R(1, secs), "the spinner", 1, secs, col)
            outs = list(itertools.product(range(secs), range(1, 7)))
            ok = sum(1 for s_, f in outs if s_ == 0 and die_t[1](f))
            check = Fraction(ok, len(outs))
        c2 = sum(1 for f in range(1, 7) if die_t[1](f))
        p1, p2 = first[0], R(c2, 6)
        ans = p1 * p2
        steps = [
            f"P({first[4]} on {first[1]}) $=$ {m(_pfrac_steps(first[2], first[3]))}. "
            f"P(die) $=$ {m(_pfrac_steps(c2, 6))}.",
            f"The two results do not affect each other, so multiply: "
            f"{m(f'{frac_raw(p1)} \\times {frac_raw(p2)} = {frac_raw(ans)}')}.",
        ]
        wrong = [
            (p1 + p2 if p1 + p2 < 1 else None, "adds the probabilities instead of multiplying them"),
            (R(first[2] + c2, first[3] + 6), "adds the counts instead of multiplying them"),
            (p2, "ignores the first event"),
            (p1, "ignores the die"),
            (R(1, first[3] * 6) if first[2] * c2 > 1 else None, "counts only one favorable combination"),
        ]
        wrong = [w for w in wrong if w[0] is not None]
    elif kind == "replace":
        txt, names, counts, noun, key = _bag(rng, lvl)
        need(key in ("marbles", "candy", "socks"))
        i, j = rng.sample(range(len(names)), 2)
        total = sum(counts)
        same_ = rng.random() < 0.35
        if same_:
            j = i
        p1, p2 = R(counts[i], total), R(counts[j], total)
        ans = p1 * p2
        nn = noun + ("s" if noun != "candy" else "")
        stem = (f"{txt} One {noun} is picked at random, its color is noted, and it is put back. Then "
                f"a second {noun} is picked. What is the probability that "
                + (f"both are {names[i]}?" if same_ else f"the first is {names[i]} and the second is {names[j]}?"))
        steps = [
            f"There are {m(' + '.join(str(c) for c in counts) + f' = {total}')} {nn}. Because the first "
            f"one is put back, the total is {total} for both picks.",
            f"Multiply: {m(f'{F(counts[i], total)} \\times {F(counts[j], total)} = {F(counts[i] * counts[j], total * total)}' + (' = ' + frac_raw(ans) if math.gcd(counts[i] * counts[j], total * total) != 1 else ''))}.",
        ]
        wrong = [
            (p1 + p2 if p1 + p2 < 1 else None, "adds the probabilities instead of multiplying them"),
            (R(counts[i] * (counts[j] - (1 if same_ else 0)), total * (total - 1)) if counts[j] > 1 else None,
             "treats the draws as if the first item were not put back"),
            (p1, "stops after the first pick"),
            (R(counts[i] * counts[j], 2 * total), None),
        ]
        wrong = [w for w in wrong if w[0] is not None]
        items = [nm for nm, c in zip(names, counts) for _ in range(c)]
        outs = list(itertools.product(items, items))
        check = Fraction(sum(1 for a_, b_ in outs if a_ == names[i] and b_ == names[j]), len(outs))
    else:
        num_, den = rng.choice([(3, 4), (4, 5), (9, 10), (2, 3), (5, 6), (7, 10), (3, 5)])
        p = R(num_, den)
        if kind == "shots":
            s = _army(rng)
            k = rng.choice([2, 2, 3]) if den <= 5 else 2
            stem = (f"{s} hits a target {m(frac_raw(p))} of the time. If each shot is independent, "
                    f"what is the probability that {s.split()[-1]} hits the target on "
                    f"{'both' if k == 2 else 'all three'} of the next {k} shots?")
        else:
            k = 2
            stem = (f"A patrol carries two radios. Each radio works independently with probability "
                    f"{m(frac_raw(p))}. What is the probability that \\emph{{both}} radios work?")
        ans = p ** k
        steps = [
            f"Each {'shot' if kind == 'shots' else 'radio'} has probability {m(frac_raw(p))}, and the "
            f"events are independent, so multiply.",
            f"{m(' \\times '.join([frac_raw(p)] * k) + f' = {F(num_ ** k, den ** k)}')}.",
        ]
        wrong = [
            (p, f"gives the probability for only one {'shot' if kind == 'shots' else 'radio'}"),
            (k * p if k * p < 1 else None, "adds the probabilities instead of multiplying them"),
            (R(num_ * k, den ** k), "multiplies the denominators but not the numerators"),
            (1 - (1 - p) ** k, "finds the probability of at least one, not all"),
        ]
        wrong = [w for w in wrong if w[0] is not None]
        outs = list(itertools.product(range(den), repeat=k))
        check = Fraction(sum(1 for o in outs if all(v < num_ for v in o)), len(outs))
    need(0 < ans < 1)
    return Problem(stem=stem, answer=ans, fmt=frac, section="AR", wrong=wrong, steps=steps,
                   near=_near_prob(ans), check=check)


@template("AR")
@_retrying
def without_replacement(rng, lvl):
    key = _fresh(rng, ["marbles", "roster", "batteries", "donuts", "raffle"], "wor")
    if key == "marbles":
        c1, c2 = rng.sample(["red", "blue", "green", "white"], 2)
        a_, b_ = rng.randint(2, 8), rng.randint(2, 8)
        setup = f"A bag holds {num(a_)} {c1} marbles and {num(b_)} {c2} marbles."
        draw = "Two marbles are drawn at random, one after the other, without being put back."
        A, B, noun = c1, c2, "marbles"
        As, Ap, Bs, Bp, it_s = f"{c1} marble", f"{c1} marbles", f"{c2} marble", f"{c2} marbles", "marble"
    elif key == "roster":
        a_, b_ = rng.randint(2, 7), rng.randint(3, 9)
        setup = (f"A squad has {num(a_)} privates and {num(b_)} specialists. The squad leader puts "
                 f"all of their names in a helmet.")
        draw = "Two names are drawn at random for weekend guard duty."
        A, B, noun = "privates", "specialists", "names"
        As, Ap, Bs, Bp, it_s = "private", "privates", "specialist", "specialists", "name"
    elif key == "batteries":
        a_, b_ = rng.randint(2, 4), rng.randint(5, 10)
        setup = f"A box of {num(a_ + b_)} radio batteries contains {num(a_)} dead batteries."
        draw = "Two batteries are taken from the box at random."
        A, B, noun = "dead", "good", "batteries"
        As, Ap, Bs, Bp, it_s = "dead battery", "dead batteries", "good battery", "good batteries", "battery"
    elif key == "donuts":
        a_, b_ = rng.randint(3, 7), rng.randint(3, 9)
        setup = f"A box contains {num(a_)} glazed donuts and {num(b_)} chocolate donuts."
        draw = "Two donuts are taken at random, one after the other."
        A, B, noun = "glazed", "chocolate", "donuts"
        As, Ap, Bs, Bp, it_s = "glazed donut", "glazed donuts", "chocolate donut", "chocolate donuts", "donut"
    else:
        a_, b_ = rng.randint(2, 6), rng.randint(4, 10)
        setup = (f"The {num(a_ + b_)} finalists in a base raffle include {num(a_)} soldiers from "
                 f"Alpha Company; the rest are from other companies.")
        draw = "Two different winners are drawn at random."
        A, B, noun = "Alpha Company soldiers", "other soldiers", "names"
        As, Ap, Bs, Bp, it_s = ("Alpha Company soldier", "Alpha Company soldiers", "soldier from another company",
                                "soldiers from other companies", "name")
    n = a_ + b_
    ask = rng.choice(["both_a", "both_a", "a_then_b", "one_each"])
    items = ["A"] * a_ + ["B"] * b_
    pairs = list(itertools.permutations(range(n), 2))
    if ask == "both_a":
        q = {"marbles": f"What is the probability that both marbles are {A}?",
             "roster": "What is the probability that both names are privates?",
             "batteries": "What is the probability that both batteries are dead?",
             "donuts": "What is the probability that both donuts are glazed?",
             "raffle": "What is the probability that both winners are from Alpha Company?"}[key]
        ans = R(a_ * (a_ - 1), n * (n - 1))
        ok = sum(1 for i, j in pairs if items[i] == "A" and items[j] == "A")
        steps = [
            f"First pick: {m(F(a_, n))}. After one {As} is taken, {a_ - 1} of the {n - 1} {noun} "
            f"left {'is' if a_ - 1 == 1 else 'are'} {'a ' + As if a_ - 1 == 1 else Ap}: {m(F(a_ - 1, n - 1))}.",
            f"Multiply: {m(f'{F(a_, n)} \\times {F(a_ - 1, n - 1)} = {F(a_ * (a_ - 1), n * (n - 1))}' + (' = ' + frac_raw(ans) if math.gcd(a_ * (a_ - 1), n * (n - 1)) != 1 else ''))}.",
        ]
        wrong = [
            (R(a_ * a_, n * n), "puts the first one back (uses the same counts for both picks)"),
            (R(a_ * a_, n * (n - 1)), f"forgets to remove the first one from the count of {Ap}"),
            (R(a_ * (a_ - 1), n * n), "lowers the count of the kind picked but not the total"),
            (R(a_, n) + R(a_ - 1, n - 1) if R(a_, n) + R(a_ - 1, n - 1) < 1 else None,
             "adds the two probabilities instead of multiplying"),
        ]
    elif ask == "a_then_b":
        q = {"marbles": f"What is the probability that the first marble is {A} and the second is {B}?",
             "roster": "What is the probability that the first name is a private and the second is a specialist?",
             "batteries": "What is the probability that the first battery is dead and the second is good?",
             "donuts": "What is the probability that the first donut is glazed and the second is chocolate?",
             "raffle": "What is the probability that the first winner is from Alpha Company and the second is not?"}[key]
        ans = R(a_ * b_, n * (n - 1))
        ok = sum(1 for i, j in pairs if items[i] == "A" and items[j] == "B")
        steps = [
            f"First pick: {m(F(a_, n))}. After one {As} is taken, {n - 1} {noun} are left, and all "
            f"{b_} {Bp} are still there: {m(F(b_, n - 1))}.",
            f"Multiply: {m(f'{F(a_, n)} \\times {F(b_, n - 1)} = {F(a_ * b_, n * (n - 1))}' + (' = ' + frac_raw(ans) if math.gcd(a_ * b_, n * (n - 1)) != 1 else ''))}.",
        ]
        wrong = [
            (R(a_ * b_, n * n), "puts the first one back (uses the same total for both picks)"),
            (R(a_ * (b_ - 1), n * (n - 1)), f"wrongly removes one of the {Bp} before the second pick"),
            (2 * ans if 2 * ans < 1 else None, "counts both orders, but the order is fixed here"),
            (R(a_, n) + R(b_, n - 1) if R(a_, n) + R(b_, n - 1) < 1 else None,
             "adds the two probabilities instead of multiplying"),
        ]
    else:
        q = {"marbles": f"What is the probability of getting one {A} marble and one {B} marble, in either order?",
             "roster": "What is the probability that one name is a private and the other is a specialist?",
             "batteries": "What is the probability that exactly one of the two batteries is dead?",
             "donuts": "What is the probability of getting one glazed donut and one chocolate donut?",
             "raffle": "What is the probability that exactly one of the two winners is from Alpha Company?"}[key]
        ans = R(2 * a_ * b_, n * (n - 1))
        ok = sum(1 for i, j in pairs if {items[i], items[j]} == {"A", "B"})
        one = R(a_ * b_, n * (n - 1))
        steps = [
            f"One order, {As} first and then {Bs}: {m(f'{F(a_, n)} \\times {F(b_, n - 1)} = {F(a_ * b_, n * (n - 1))}')}.",
            f"The other order, {Bs} first and then {As}: {m(f'{F(b_, n)} \\times {F(a_, n - 1)} = {F(a_ * b_, n * (n - 1))}')}.",
            f"Add the two orders: {m(f'2 \\times {F(a_ * b_, n * (n - 1))} = {F(2 * a_ * b_, n * (n - 1))}' + (' = ' + frac_raw(ans) if math.gcd(2 * a_ * b_, n * (n - 1)) != 1 else ''))}.",
        ]
        wrong = [
            (one, "counts only one order"),
            (R(2 * a_ * b_, n * n), "puts the first one back (uses the same total for both picks)"),
            (R(a_ * b_, n * n), "counts only one order and puts the first one back"),
        ]
    need(0 < ans < 1)
    wrong = [w for w in wrong if w[0] is not None]
    return Problem(stem=f"{setup} {draw} {q}", answer=ans, fmt=frac, section="AR", wrong=wrong,
                   steps=steps, near=_near_prob(ans), check=Fraction(ok, len(pairs)))


# --------------------------------------------------------------------------
# counting
# --------------------------------------------------------------------------

@template("AR")
@_retrying
def counting(rng, lvl):
    if lvl >= 2:
        return _codes(rng)
    key = _fresh(rng, ["outfit", "dfac", "routes", "pizza", "sundae", "car"], "count")
    if key == "outfit":
        a_, b_, c_ = rng.randint(3, 7), rng.randint(2, 5), rng.randint(2, 4)
        p = person(rng)
        stem = (f"{p} packed {num(a_)} shirts, {num(b_)} pairs of pants, and {num(c_)} pairs of "
                f"shoes for a trip. How many different outfits of one shirt, one pair of pants, and "
                f"one pair of shoes can {p.he} make?")
        stages = [(a_, "shirts"), (b_, "pants"), (c_, "shoes")]
    elif key == "dfac":
        a_, b_, c_ = rng.randint(2, 5), rng.randint(3, 6), rng.randint(2, 4)
        stem = (f"The dining facility on a base offers {num(a_)} main dishes, {num(b_)} side dishes, "
                f"and {num(c_)} desserts. A meal is one main dish, one side, and one dessert. How "
                f"many different meals are possible?")
        stages = [(a_, "main dishes"), (b_, "sides"), (c_, "desserts")]
    elif key == "routes":
        a_, b_ = rng.randint(2, 5), rng.randint(2, 6)
        c_ = None
        stem = (f"A convoy can take {num(a_)} different roads from the base to a checkpoint and "
                f"{num(b_)} different roads from the checkpoint to the training area. How many "
                f"different routes are there from the base to the training area through the "
                f"checkpoint?")
        stages = [(a_, "first-leg roads"), (b_, "second-leg roads")]
    elif key == "pizza":
        a_, b_, c_ = rng.randint(3, 4), rng.randint(2, 3), rng.randint(5, 10)
        stem = (f"A pizza shop offers {num(a_)} sizes, {num(b_)} kinds of crust, and {num(c_)} "
                f"toppings. How many different one-topping pizzas can be ordered?")
        stages = [(a_, "sizes"), (b_, "crusts"), (c_, "toppings")]
    elif key == "sundae":
        a_, b_, c_ = rng.randint(4, 12), rng.randint(2, 5), rng.randint(2, 4)
        stem = (f"An ice cream stand has {num(a_)} flavors, {num(b_)} sauces, and {num(c_)} "
                f"toppings. How many different sundaes can be made with one flavor, one sauce, and "
                f"one topping?")
        stages = [(a_, "flavors"), (b_, "sauces"), (c_, "toppings")]
    else:
        a_, b_, c_ = rng.randint(3, 8), rng.randint(2, 4), rng.randint(2, 3)
        stem = (f"A new pickup truck comes in {num(a_)} colors, {num(b_)} cab styles, and {num(c_)} "
                f"engine sizes. How many different versions of the truck are possible?")
        stages = [(a_, "colors"), (b_, "cab styles"), (c_, "engines")]
    counts = [c for c, _ in stages]
    ans = math.prod(counts)
    wrong = [
        (Q(sum(counts)), "adds the choices instead of multiplying them"),
        (Q(counts[0] * counts[1]) if len(counts) == 3 else Q(counts[0] * counts[1] * 2), "leaves out one of the choices"
         if len(counts) == 3 else None),
        (Q(max(counts) ** len(counts)), None),
    ]
    if len(counts) == 3:
        wrong.append((Q(counts[1] * counts[2]), "leaves out one of the choices"))
    return Problem(
        stem=stem, answer=Q(ans), fmt=num, section="AR",
        wrong=wrong,
        steps=[
            "Each choice can be paired with every other choice, so multiply the number of options "
            "at each step (the counting principle).",
            f"{m(' \\times '.join(str(c) for c in counts) + f' = {int_raw(ans)}')}.",
        ],
        near=_near(ans),
        check=Q(len(list(itertools.product(*[range(c) for c in counts])))),
    )


def _codes(rng):
    key = _fresh(rng, ["lock", "dials", "pin", "id", "plate", "callsign"], "codes")
    p = person(rng)
    if key == "lock":
        d = rng.choice([3, 4])
        first0 = rng.random() < 0.5
        stem = (f"{p}'s footlocker has a combination lock with a {d}-digit code. Each digit can be "
                f"any number from 0 to 9, and digits may repeat"
                + (", but the first digit cannot be 0." if first0 else ".")
                + " How many different codes are possible?")
        counts = ([9] if first0 else [10]) + [10] * (d - 1)
        wrong = [
            (Q(10 ** d), "forgets that the first digit cannot be 0") if first0 else
            (Q(math.perm(10, d)), "does not let the digits repeat"),
            (Q(sum(counts)), "adds the choices instead of multiplying them"),
            (Q(9 ** d), "leaves out the digit 0 in every position") if first0 else
            (Q(9 * 10 ** (d - 1)), "assumes the first digit cannot be 0"),
        ]
    elif key == "dials":
        d = rng.choice([3, 4, 5])
        k = rng.choice([4, 5, 6, 8])
        need(k ** d <= 5000)
        item = rng.choice(["bike lock", "gym locker lock", "toolbox lock", "luggage lock"])
        stem = (f"{p}'s {item} has {d} dials, and each dial shows the numbers 1 through {k}. "
                f"How many different settings of the dials are possible?")
        counts = [k] * d
        wrong = [
            (Q(k * d), "multiplies the number of dials by the numbers on each dial"),
            (Q(math.perm(k, d)) if k >= d else Q(k ** (d - 1)), "does not let the numbers repeat"
             if k >= d else "leaves out one dial"),
            (Q(d ** k), "switches the roles of the dials and the numbers"),
            (Q(k ** (d - 1)), "leaves out one dial"),
        ]
    elif key == "pin":
        d = rng.choice([3, 4])
        lo = rng.choice([0, 1])
        k = 10 - lo
        stem = (f"{p} is choosing a {d}-digit PIN using the digits {lo} through 9. No digit can be "
                f"used more than once. How many different PINs are possible?")
        counts = list(range(k, k - d, -1))
        wrong = [
            (Q(k ** d), "lets the digits repeat"),
            (Q(sum(counts)), "adds the choices instead of multiplying them"),
            (Q(math.prod(counts[:-1])), f"stops after {d - 1} digits"),
            (Q(math.comb(k, d)), "ignores the order of the digits"),
        ]
    elif key == "id":
        L_ = rng.randint(3, 8)
        dd = rng.choice([2, 3])
        s_ = _army(rng)
        stem = (f"{s_} is assigning ID codes to the soldiers in a training company. Each code is "
                f"one letter from A to {'ABCDEFGH'[L_ - 1]} followed by {dd} digits (0 to 9, repeats "
                f"allowed). How many different ID codes are possible?")
        counts = [L_] + [10] * dd
        wrong = [
            (Q(L_ + 10 * dd), "adds the choices instead of multiplying them"),
            (Q(L_ * 10), "counts only one digit"),
            (Q(L_ * math.perm(10, dd)), "does not let the digits repeat"),
            (Q(L_ * 9 ** dd), "leaves out the digit 0"),
        ]
    elif key == "plate":
        L_ = rng.choice([2, 3])
        dd = rng.choice([1, 2])
        stem = (f"A town's parking permits each have {L_} letters (A to Z, repeats allowed) "
                f"followed by {'one digit' if dd == 1 else 'two digits'} from 1 to 9. How many "
                f"different permit numbers are possible?")
        counts = [26] * L_ + [9] * dd
        wrong = [
            (Q(26 * L_ + 9 * dd), "adds the choices instead of multiplying them"),
            (Q(26 ** L_ * 10 ** dd), "uses 10 digits instead of 9"),
            (Q(math.perm(26, L_) * 9 ** dd), "does not let the letters repeat"),
            (Q(26 * 9 ** dd), "counts only one letter"),
        ]
    else:
        k = rng.choice([3, 4, 5, 6])
        dd = rng.choice([1, 2])
        unit_ = rng.choice(["platoon", "company", "battalion"])
        stem = (f"A {unit_} makes radio call signs from two letters followed by "
                f"{'one digit' if dd == 1 else 'two digits'}. The letters must come from the first "
                f"{k} letters of the alphabet (repeats allowed), and each digit can be 0 to 9. "
                f"How many call signs are possible?")
        counts = [k, k] + [10] * dd
        wrong = [
            (Q(2 * k + 10 * dd), "adds the choices instead of multiplying them"),
            (Q(k * (k - 1) * 10 ** dd), "does not let the letters repeat"),
            (Q(k * 10 ** dd), "counts only one letter"),
        ]
    ans = math.prod(counts)
    return Problem(
        stem=stem, answer=Q(ans), fmt=num, section="AR",
        wrong=wrong,
        steps=[
            "Count the choices for each position: "
            + ", ".join(f"{c}" for c in counts) + ".",
            f"Multiply (counting principle): {m(' \\times '.join(str(c) for c in counts) + f' = {int_raw(ans)}')}.",
        ],
        near=_near(ans),
        check=Q(len(list(itertools.product(*[range(c) for c in counts])))),
    )


@template("AR")
@_retrying
def arrangements(rng, lvl):
    kind = (_fresh(rng, ["line", "officers"], "arr2", keep=1) if lvl <= 2 else _fresh(rng, ["three", "fixed"], "arr3", keep=1))
    p = person(rng)
    if kind == "line":
        n = rng.randint(4, 6)
        key = _fresh(rng, ["photo", "books", "runners", "trucks", "errands", "posters"], "line")
        W = _cap(_WORDS[n])
        stem = {
            "photo": f"{p} is taking a photo of {n} soldiers standing in a line. In how many different orders can the {n} soldiers line up?",
            "books": f"{p} has {n} different books to arrange on a shelf. In how many different orders can the books be arranged?",
            "runners": f"{W} runners, including {p}, finish a race with no ties. How many different orders of finish are possible?",
            "trucks": f"A convoy has {n} trucks. In how many different orders can the trucks line up on the road?",
            "errands": f"{p} has {n} errands to run on Saturday. In how many different orders can {p.he} do them?",
            "posters": f"{p} wants to hang {n} different posters side by side on a wall. In how many different orders can {p.he} hang them?",
        }[key]
        ans = math.factorial(n)
        wrong = [
            (Q(sum(range(1, n + 1))), "adds the choices instead of multiplying them"),
            (Q(n * n), None),
            (Q(n * (n - 1)), "fills only the first two places"),
            (Q(n ** n), "lets the same item fill more than one place"),
        ]
        counts = list(range(n, 0, -1))
        steps = [
            f"First place: {n} choices; second place: {n - 1} (one is used); and so on down to 1.",
            f"Multiply: {m(' \\times '.join(map(str, counts)) + f' = {int_raw(ans)}')}.",
        ]
        check = Q(len(list(itertools.permutations(range(n)))))
    elif kind == "officers":
        n = rng.randint(5, 15)
        key = _fresh(rng, ["club", "squad", "council", "team"], "officers")
        roles = {"club": ("president", "vice president"), "squad": ("team leader", "assistant team leader"),
                 "council": ("chair", "secretary"), "team": ("captain", "co-captain")}[key]
        who = {"club": f"{p}'s hiking club has {n} members.",
               "squad": f"{_army(rng)} has {n} soldiers in the section.",
               "council": f"A student council has {n} members, including {p}.",
               "team": f"{p}'s volleyball team has {n} players."}[key]
        stem = (f"{who} One person will be chosen as {roles[0]} and a different person as "
                f"{roles[1]}. In how many ways can the two positions be filled?")
        ans = n * (n - 1)
        wrong = [
            (Q(n * n), "lets the same person hold both positions"),
            (Q(math.comb(n, 2)), "ignores the difference between the two positions"),
            (Q(2 * n), None),
            (Q(n + n - 1), "adds the choices instead of multiplying them"),
        ]
        steps = [
            f"{_cap(roles[0])}: {n} choices. {_cap(roles[1])}: {n - 1} choices (anyone except the {roles[0]}).",
            f"Multiply: {m(f'{n} \\times {n - 1} = {ans}')}.",
        ]
        check = Q(len(list(itertools.permutations(range(n), 2))))
    elif kind == "three":
        n = rng.randint(5, 12)
        key = _fresh(rng, ["medals", "crew", "officers", "awards"], "three")
        W = _cap(_WORDS[n])
        stem = {
            "medals": f"{W} runners, including {p}, are in a race. In how many different ways can the gold, silver, and bronze medals be awarded (no ties)?",
            "crew": f"From a squad of {n} soldiers, {_army(rng)} will choose a driver, a gunner, and a radio operator. In how many ways can the three jobs be filled if no one does two jobs?",
            "officers": f"{p}'s club of {n} members will elect a president, a vice president, and a treasurer. No one can hold two offices. How many different results are possible?",
            "awards": f"A science fair has {n} projects, including {p}'s. In how many ways can the judges award first, second, and third place?",
        }[key]
        ans = n * (n - 1) * (n - 2)
        wrong = [
            (Q(n ** 3), "lets the same one fill more than one position"),
            (Q(math.comb(n, 3)), "counts groups of three instead of ordered positions"),
            (Q(n * (n - 1)), "fills only two of the three positions"),
            (Q(3 * n), None),
        ]
        steps = [
            f"First position: {n} choices; second: {n - 1}; third: {n - 2} (no one can repeat).",
            f"Multiply: {m(f'{n} \\times {n - 1} \\times {n - 2} = {int_raw(ans)}')}.",
        ]
        check = Q(len(list(itertools.permutations(range(n), 3))))
    else:
        n = rng.randint(4, 7)
        key = _fresh(rng, ["photo", "speech", "lineup"], "fixed")
        W = _cap(_WORDS[n])
        stem = {
            "photo": f"{W} friends, including {p}, line up for a photo. {p} must stand at the left end. How many different line-ups are possible?",
            "speech": f"{W} students, including {p}, will give speeches one at a time. {p} must speak last. In how many different orders can the speeches be given?",
            "lineup": f"{W} soldiers, including {p}, march in single file. {p}, the squad leader, must be first. In how many different orders can the soldiers march?",
        }[key]
        ans = math.factorial(n - 1)
        wrong = [
            (Q(math.factorial(n)), f"ignores the rule about {p}"),
            (Q(n - 1), "counts only the choices for one position"),
            (Q((n - 1) ** (n - 1)), "lets the same person fill more than one place"),
            (Q(math.factorial(n) - 1), None),
        ]
        rest = list(range(n - 1, 0, -1))
        steps = [
            f"{p}'s place is fixed, so only the other {n - 1} people need to be arranged.",
            f"{m(' \\times '.join(map(str, rest)) + f' = {int_raw(ans)}')}.",
        ]
        perms = itertools.permutations(range(n))
        check = Q(sum(1 for pp in perms if (pp[-1] == 0 if key == "speech" else pp[0] == 0)))
    return Problem(stem=stem, answer=Q(ans), fmt=num, section="AR", wrong=wrong, steps=steps,
                   near=_near(ans), check=check)


@template("AR")
@_retrying
def combinations(rng, lvl):
    kind = _fresh(rng, ["pick2", "handshake", "games", "pick3"], "comb")
    p = person(rng)
    if kind == "pick3":
        n = rng.randint(5, 9)
        key = _fresh(rng, ["toppings", "detail", "books", "classes"], "pick3")
        stem = {
            "toppings": f"At a sandwich shop, {p} may choose any 3 different toppings from a list of {n}. How many different groups of 3 toppings are possible?",
            "detail": f"{_army(rng)} must choose 3 soldiers from a team of {n} for a work detail. How many different groups of 3 can be chosen?",
            "books": f"{p} must read 3 of the {n} books on a summer reading list. How many different groups of 3 books can {p.he} choose?",
            "classes": f"{p} must pick 3 of the {n} elective classes offered next semester. How many different sets of 3 classes are possible?",
        }[key]
        ans = math.comb(n, 3)
        P3 = n * (n - 1) * (n - 2)
        wrong = [
            (Q(P3), "counts each group several times (order does not matter here)"),
            (Q(3 * n), None),
            (Q(math.comb(n, 2)), "picks only 2"),
            (Q(P3 // 2), "divides by 2 instead of by 6"),
        ]
        steps = [
            f"If order mattered: {m(f'{n} \\times {n - 1} \\times {n - 2} = {P3}')}.",
            f"Each group of 3 can be ordered in {m('3 \\times 2 \\times 1 = 6')} ways, and all of these "
            f"are the same group. Divide: {m(f'{P3} \\div 6 = {ans}')}.",
        ]
        check = Q(len(list(itertools.combinations(range(n), 3))))
    else:
        n = rng.randint(5, 14)
        if kind == "pick2":
            key = _fresh(rng, ["detail", "reps", "books", "pizza"], "pick2")
            stem = {
                "detail": f"{_army(rng)} must pick 2 soldiers from a squad of {n} to go on a supply run. How many different pairs can be chosen?",
                "reps": f"{p}'s class of {n} students will choose 2 students to represent it at a meeting. How many different pairs of students are possible?",
                "books": f"{p} wants to take 2 of {p.his} {n} favorite books on vacation. How many different pairs of books can {p.he} choose?",
                "pizza": f"A pizza shop has {n} toppings, and {p} wants a pizza with 2 different toppings. How many different pairs of toppings can {p.he} choose?",
            }[key]
        elif kind == "handshake":
            stem = (f"At a meeting, {p} and the other {n - 1} people each shake hands once with every "
                    f"other person. How many handshakes take place?")
        else:
            sport = rng.choice(["softball", "basketball", "soccer", "volleyball"])
            stem = (f"In a {sport} league of {n} teams, each team plays every other team exactly "
                    f"once. How many games are played in all?")
        ans = math.comb(n, 2)
        wrong = [
            (Q(n * (n - 1)), "counts each pair twice"),
            (Q(n * n), None),
            (Q(2 * n), None),
            (Q((n - 1) * (n - 2) // 2), "leaves one person out"),
        ]
        steps = [
            f"Each of the {n} can be paired with {n - 1} others: {m(f'{n} \\times {n - 1} = {n * (n - 1)}')}.",
            f"That counts every pair twice (A with B and B with A), so divide by 2: "
            f"{m(f'{n * (n - 1)} \\div 2 = {ans}')}.",
        ]
        check = Q(len(list(itertools.combinations(range(n), 2))))
    return Problem(stem=stem, answer=Q(ans), fmt=num, section="AR", wrong=wrong, steps=steps,
                   near=_near(ans), check=check)


@template("AR")
@_retrying
def expected_count(rng, lvl):
    if lvl <= 1:
        key = _fresh(rng, ["bulbs", "freethrows", "targets", "survey"], "exp1")
        if key == "bulbs":
            p = rng.choice([2, 3, 4, 5])
            N = rng.choice([200, 300, 400, 500, 600, 800, 1000])
            stem = (f"A factory finds that {m(f'{p}\\%')} of the light bulbs it makes are defective. "
                    f"In a shipment of {num(N)} bulbs, how many would you expect to be defective?")
            other = "not defective"
        elif key == "freethrows":
            p = rng.choice([60, 70, 75, 80, 90])
            N = rng.choice([20, 30, 40, 50, 60])
            nm = person(rng)
            stem = (f"{nm} makes {m(f'{p}\\%')} of {nm.his} free throws. If {nm.he} shoots {num(N)} "
                    f"free throws, how many would you expect {nm.him} to make?")
            other = "missed"
        elif key == "targets":
            p = rng.choice([70, 75, 80, 85, 90, 95])
            N = rng.choice([20, 40, 60, 80, 100])
            s = _army(rng)
            stem = (f"On the range, {s} hits {m(f'{p}\\%')} of the targets on average. Out of "
                    f"{num(N)} targets, how many hits should {s.split()[-1]} expect?")
            other = "misses"
        else:
            p = rng.choice([10, 15, 20, 25, 30, 35, 40])
            N = rng.choice([200, 300, 400, 500, 600, 800])
            stem = (f"A survey found that {m(f'{p}\\%')} of high school seniors plan to join the "
                    f"military. In a group of {num(N)} seniors, how many would you expect to plan "
                    f"to join?")
            other = "not planning to join"
        ans = R(p * N, 100)
        need(ans.is_integer)
        return Problem(
            stem=stem, answer=ans, fmt=num, section="AR",
            wrong=[
                (N - ans, f"is the expected number {other}"),
                (ans * 10, "moves the decimal point only one place"),
                (Q(p), "uses the percent as the count"),
                (ans / 10 if (ans / 10).is_integer else ans + 10, None),
            ],
            steps=[
                f"Expected count $=$ probability $\\times$ number of tries: "
                f"{m(f'{dec_raw(R(p, 100))} \\times {int_raw(N)} = {int_raw(ans)}')}.",
            ],
            near=_near(ans),
            check=Fraction(p * N, 100),
        )
    kind = _fresh(rng, ["die", "spinner", "graduates", "defect_good"], "exp2")
    if kind == "die":
        t = rng.choice([("a 6", 1), ("an even number", 3), ("a number greater than 4", 2),
                        ("a 1 or a 2", 2), ("a multiple of 3", 2)])
        N = rng.choice(range(60, 601, 30))
        pp = person(rng)
        stem = (f"For a game, {pp} rolls a fair six-sided die {num(N)} times. About how many times "
                f"should {pp.he} expect to roll {t[0]}?")
        prob = R(t[1], 6)
        ans = prob * N
        steps = [f"P({t[0]}) $=$ {m(_pfrac_steps(t[1], 6))}.",
                 f"Expected count: {m(f'{frac_raw(prob)} \\times {int_raw(N)} = {int_raw(ans)}')}."]
        wrong = [
            (N - ans, f"is the expected number of rolls that are \\emph{{not}} {t[0]}"),
            (Q(N // 2), "assumes each roll is a 50-50 chance"),
        ]
        if t[1] > 1:
            wrong += [(R(N, t[1]), "divides by the number of favorable outcomes"),
                      (Q(N // 6), "counts only one favorable outcome out of six")]
        check = Fraction(t[1] * N, 6)
    elif kind == "spinner":
        secs = rng.choice([4, 5, 8, 10])
        k = rng.randint(1, secs // 2)
        N = rng.choice(range(40, 401, 20))
        prob = R(k, secs)
        ans = prob * N
        need(ans.is_integer)
        stem = (f"A spinner has {secs} equal sections, and {k} of them {'is' if k == 1 else 'are'} red. "
                f"If the spinner is spun {num(N)} times, about how many times should it land on red?")
        steps = [f"P(red) $=$ {m(_pfrac_steps(k, secs))}.",
                 f"Expected count: {m(f'{frac_raw(prob)} \\times {int_raw(N)} = {int_raw(ans)}')}."]
        wrong = [
            (N - ans, "is the expected number of spins that do \\emph{not} land on red"),
            (R(N, secs), "counts only one red section"),
        ]
        if k > 1:
            wrong.append((R(N, k), "divides by the number of red sections"))
        check = Fraction(k * N, secs)
    elif kind == "graduates":
        p = rng.choice([2, 4, 5, 6, 8, 10, 12, 15])
        N = rng.choice(range(200, 1601, 50))
        ans = N - R(p * N, 100)
        need(ans.is_integer)
        where = rng.choice(["a basic training battalion", "an Air Force training squadron",
                            "a Navy boot camp division", "a police academy"])
        stem = (f"At {where}, about {m(f'{p}\\%')} of recruits do not complete "
                f"training. If {num(N)} recruits start, about how many would you expect to "
                f"graduate?")
        steps = [f"If {m(f'{p}\\%')} do not finish, then {m(f'100\\% - {p}\\% = {100 - p}\\%')} graduate.",
                 f"Expected graduates: {m(f'{dec_raw(R(100 - p, 100))} \\times {int_raw(N)} = {int_raw(ans)}')}."]
        wrong = [
            (R(p * N, 100), "is the number expected \\emph{not} to graduate"),
            (Q(N - p), "subtracts the percent as if it were a number of recruits"),
            (N - R(p * N, 10), "moves the decimal point only one place"),
        ]
        check = Fraction(N * (100 - p), 100)
    else:
        p = rng.choice([1, 2, 3, 4, 5])
        N = rng.choice(range(300, 3001, 100))
        ans = N - R(p * N, 100)
        need(ans.is_integer)
        thing = rng.choice(["bolts", "phone chargers", "light bulbs", "water bottles", "batteries"])
        stem = (f"A machine makes {thing}, and {m(f'{p}\\%')} of them are defective. Out of "
                f"{num(N)} {thing}, how many would you expect to be \\emph{{good}}?")
        steps = [f"Good {thing}: {m(f'100\\% - {p}\\% = {100 - p}\\%')}.",
                 f"Expected good {thing}: {m(f'{dec_raw(R(100 - p, 100))} \\times {int_raw(N)} = {int_raw(ans)}')}."]
        wrong = [
            (R(p * N, 100), "is the number expected to be defective"),
            (Q(N - p), f"subtracts the percent as if it were a number of {thing}"),
            (N - R(p * N, 10), "moves the decimal point only one place"),
        ]
        check = Fraction(N * (100 - p), 100)
    return Problem(stem=stem, answer=ans, fmt=num, section="AR", wrong=wrong, steps=steps,
                   near=_near(ans), check=check)


PLAN = [
    # level 1: warm-ups (12)
    (mean_basic, 1, 3),
    (center_spread, 1, 3),
    (simple_prob, 1, 3),
    (counting, 1, 2),
    (expected_count, 1, 1),
    # level 2: test level (16)
    (score_needed, 2, 3),
    (average_change, 2, 2),
    (center_spread, 2, 2),
    (weighted_average, 2, 2),
    (prob_complement, 2, 2),
    (independent_events, 2, 2),
    (expected_count, 2, 1),
    (arrangements, 2, 1),
    (counting, 2, 1),
    # level 3: challenge (12)
    (score_needed, 3, 1),
    (average_change, 3, 2),
    (weighted_average, 3, 2),
    (without_replacement, 3, 3),
    (arrangements, 3, 2),
    (combinations, 3, 2),
]
