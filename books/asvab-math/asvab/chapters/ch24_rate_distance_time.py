"""Chapter 24 - Rate, Distance & Time (word problems)."""
import functools
import math
from fractions import Fraction

from ..core import (R, Q, Problem, Person, need, num, dec, money, pct, m, F, unit, text,
                    dec_raw, int_raw, frac_raw, mixed_raw, person, choose, template)

NUM = 24
TITLE = r"Rate, Distance \& Time"
PART = 4

INTRO = r"""
Anything that moves at a steady rate (a car, a convoy, a runner, a printer
turning out pages) follows one formula. The skill is in setting it up with
matching units and in knowing which rates to add, subtract, or leave alone.

\begin{concept}{The distance formula}
\[ d = r \times t \qquad r = \frac{d}{t} \qquad t = \frac{d}{r} \]
$d$ = distance, $r$ = rate (speed), $t$ = time. The units must match: with a
speed in miles per hour, the time must be in \emph{hours}. The same formula
works for any rate: $\text{amount} = \text{rate} \times \text{time}$ (words
typed, pages printed, gallons used).
\end{concept}

\begin{concept}{Minutes and hours}
Divide minutes by 60 to get hours: 15 min $= \frac14$ h $= 0.25$ h,
20 min $= \frac13$ h, 30 min $= 0.5$ h, 45 min $= 0.75$ h.
Going the other way, multiply by 60: $0.4$ h $= 24$ min.
Beware: 2.5 hours is 2 hours \emph{30} minutes, not 2 hours 50 minutes.
\end{concept}

\begin{concept}{Two movers}
\begin{itemize}
\item Moving \textbf{toward} each other or in \textbf{opposite} directions: the
  gap changes at the \emph{sum} of the speeds.
\item Moving in the \textbf{same} direction (one catching up): the gap changes at
  the \emph{difference} of the speeds.
\item \textbf{Average speed} $= \dfrac{\text{total distance}}{\text{total time}}$.
  It is \emph{not} the average of the speeds unless the times are equal.
\end{itemize}
\end{concept}

\begin{example}{Worked example}
A convoy drives 120 miles to a range at 40 mph and returns at 60 mph. What is
its average speed for the round trip?

\textbf{Solution.} Out: $120 \div 40 = 3$ hours. Back: $120 \div 60 = 2$ hours.
Total: 240 miles in 5 hours, so the average speed is $240 \div 5 = 48$ mph,
not 50 mph: the convoy spends more time at the slower speed.
\end{example}

\begin{tip}
For pace and speed, use 60: a pace of 8 minutes per mile is
$60 \div 8 = 7.5$ mph, and 10 mph is $60 \div 10 = 6$ minutes per mile.
\end{tip}

\begin{trap}
\begin{itemize}
\item Multiplying a speed in miles per hour by a time in \emph{minutes}.
\item Writing 45 minutes as 0.45 hour (it is 0.75 hour).
\item Averaging two speeds instead of dividing total distance by total time.
\item Adding speeds when one vehicle chases another (subtract them).
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
_ARMY = ["Private", "Private First Class", "Specialist", "Corporal", "Sergeant", "Staff Sergeant"]
_GROUND = _ARMY + ["Lance Corporal", "Lieutenant"]          # drive Humvees, lead convoys
_PILOT = ["Chief Warrant Officer", "Warrant Officer", "Captain", "Lieutenant"]


def _trooper(rng, ranks=None):
    """Rank + last name (vehicle drivers and convoy leaders get Army/Marine
    ground ranks by default)."""
    he, him, his = rng.choice([("he", "him", "his"), ("she", "her", "her")])
    return Person(f"{rng.choice(ranks or _GROUND)} {rng.choice(_LAST)}", he, him, his)


def _art(word):
    return "an" if word[0] in "aeiouAEIO" else "a"


def _cap(s):
    return s[0].upper() + s[1:]


def _d(v):
    """Exact number as a raw decimal string (integers stay integers)."""
    return dec_raw(Q(v))


def _hrs(t):
    """Hours as text: 3 -> '3 hours', 1 -> '1 hour', 2.5 -> '2.5 hours'."""
    return f"{_d(t)} hour{'' if Q(t) == 1 else 's'}"


def _hw(t):
    """'hour' or 'hours' to follow the number t."""
    return "hour" if Q(t) == 1 else "hours"


def _mi(d):
    """'1 mile', '12 miles' (plain text)."""
    return f"{int_raw(d)} mile{'' if Q(d) == 1 else 's'}"


def _hm(t):
    """Hours -> 'h hours m minutes' wording (t in hours, whole minutes)."""
    mins = Q(t) * 60
    assert mins.is_integer
    h, mm = divmod(int(mins), 60)
    parts = []
    if h:
        parts.append(f"{h} hour{'s' if h != 1 else ''}")
    if mm:
        parts.append(f"{mm} minute{'s' if mm != 1 else ''}")
    return " ".join(parts) if parts else "0 minutes"


def _near_like(ans):
    """Filler distractors with the same shape (whole numbers stay whole,
    halves stay halves) and a round spacing."""
    A = Q(ans)
    nice = next((Q(s) for s in (R(1, 10), R(1, 4), R(1, 2), 1, 2, 5, 10, 20, 25, 50, 100, 200, 500, 1000)
                 if abs(A) <= 12 * Q(s)), Q(1000))
    if A.is_integer:
        step = max(nice, Q(1))
    else:
        unit_ = R(1, sp_q(A))
        step = max(unit_, (nice / unit_).floor() * unit_)

    def f(rng):
        out = [A + k * step for k in (1, 2, 3, -1, -2, -3)]
        out = [v for v in out if v > 0]
        rng.shuffle(out)
        return out
    return f


def sp_q(v):
    return Q(v).q


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
    @functools.wraps(fn)
    def wrapper(rng, lvl, **kw):
        p = fn(rng, lvl, **kw)
        if p.near is None and not isinstance(p.answer, str):
            p.near = _near_like(p.answer)
        return p
    return wrapper


def _clock(mins):
    """Minutes after midnight -> '9:05 a.m.'"""
    mins = int(mins) % (24 * 60)
    h, mm = divmod(mins, 60)
    suf = "a.m." if h < 12 else "p.m."
    h12 = h % 12 or 12
    return f"{h12}:{mm:02d} {suf}"


_MI = unit(num, "mile")
_MID = unit(dec, "mile")
_MPH = unit(dec, "mph", "mph")
_HR = unit(dec, "hour")
_MIN = unit(num, "minute")
_GAL = unit(dec, "gallon")


# --------------------------------------------------------------------------
# 1. d = rt: distance, rate or time (L1)
# --------------------------------------------------------------------------

_MOVERS = [
    # (subject, how-far question, speed question, noun, speed lo, hi, step, hours, military)
    ("{B} drives", "How far does {he} drive?", "What is {his} average speed?", "trip",
     40, 70, 1, [2, 3, 4, 5, 6], False),
    ("A supply convoy travels", "How far does the convoy travel?", "What is the convoy's average speed?",
     "trip", 25, 50, 1, [2, 3, 4, 5, 6], True),
    ("A freight train travels", "How far does the train travel?", "What is the train's average speed?",
     "trip", 35, 60, 5, [3, 4, 5, 6, 8], False),
    ("{B} rides a bicycle", "How far does {he} ride?", "What is {his} average speed?", "ride",
     8, 18, 1, [2, 3, 4], False),
    ("A platoon marches", "How far does the platoon march?", "What is the platoon's average speed?",
     "march", 3, 4, 1, [2, 3, 4, 5, 6], True),
    ("A Black Hawk helicopter flies", "How far does the helicopter fly?",
     "What is the helicopter's average speed?", "flight", 120, 160, 10, [2, 3], True),
    ("A passenger jet flies", "How far does the jet fly?", "What is the jet's average speed?", "flight",
     400, 550, 25, [2, 3, 4, 5], False),
    ("A charter bus travels", "How far does the bus travel?", "What is the bus's average speed?", "trip",
     45, 65, 5, [3, 4, 5, 6], False),
    ("A tractor-trailer travels", "How far does the truck travel?", "What is the truck's average speed?",
     "trip", 50, 65, 1, [3, 4, 5, 6, 7], False),
    ("{T} drives a Humvee", "How far does {the} drive?", "What is {thes} average speed?", "drive",
     30, 55, 1, [2, 3, 4, 5], True),
    ("A cargo ship sails", "How far does the ship sail?", "What is the ship's average speed?", "voyage",
     15, 25, 1, [6, 8, 10, 12, 24], False),
    ("{B} jogs", "How far does {he} jog?", "What is {his} average speed?", "run", 5, 7, 1, [1, 2], False),
]


@template("AR")
@_fill
def drt_basic(rng, lvl, part=None):
    subj, qfar, qrate, noun, lo, hi, st, hours, mil = _pick(rng, _MOVERS, part)
    B, T = person(rng), _trooper(rng)
    r = rng.choice(range(lo, hi + 1, st))
    t = rng.choice(hours)
    d = r * t
    need(d >= 4)
    kw = dict(B=B, he=B.he, his=B.his, T=T, the=T.he, thes=T.his)
    S = subj.format(**kw)
    kind = rng.choice(["d", "r", "t"])
    if kind == "d":
        stem = f"{S} at an average speed of {r} miles per hour for {_hrs(t)}. {qfar.format(**kw)}"
        return Problem(
            stem=stem, answer=Q(d), fmt=_MI, section="AR",
            wrong=[(Q(r + t), "adds the speed and the time instead of multiplying"),
                   (Q(r) / t if (Q(r) / t).is_integer else Q(r * (t + 1)), "divides the speed by the time instead of multiplying"
                    if (Q(r) / t).is_integer else None)],
            steps=[f"Use {m('d = r \\times t')}: distance {m('=')} speed {m('\\times')} time.",
                   f"{m(f'd = {r} \\times {t} = {int_raw(d)}')} miles."],
            verify=lambda v: v / t == r,
        )
    if kind == "r":
        stem = f"{S} {int_raw(d) if d < 1000 else num(d)} miles in {_hrs(t)}. {qrate.format(**kw)}"
        return Problem(
            stem=stem, answer=Q(r), fmt=_MPH, section="AR",
            wrong=[(Q(d * t), "multiplies the distance by the time instead of dividing"),
                   (Q(d - t), "subtracts the time from the distance")],
            steps=[f"Use {m('r = d \\div t')}: speed {m('=')} distance {m('\\div')} time.",
                   f"{m(f'r = {int_raw(d)} \\div {t} = {r}')} miles per hour."],
            verify=lambda v: v * t == d,
        )
    need(r % 5 == 0 or r < 20)          # divide by a friendly speed in a warm-up
    stem = (f"{S} {int_raw(d) if d < 1000 else num(d)} miles at an average speed of {r} miles per hour. "
            f"How many hours does the {noun} take?")
    return Problem(
        stem=stem, answer=Q(t), fmt=_HR, section="AR",
        wrong=[(R(r, d), "divides the speed by the distance instead of the distance by the speed"),
               (Q(d - r), "subtracts the speed from the distance")],
        steps=[f"Use {m('t = d \\div r')}: time {m('=')} distance {m('\\div')} speed.",
               f"{m(f't = {int_raw(d)} \\div {r} = {t}')} {_hw(t)}."],
        verify=lambda v: v * r == d,
        near=lambda g: [Q(t + k) for k in (1, 2, -1, 3) if t + k > 0],
    )


# --------------------------------------------------------------------------
# 2. minutes and hours (L1, L2)
# --------------------------------------------------------------------------

_MIN_MOVERS = [
    # (sentence with {r} speed and {T} time phrase, noun, speed choices, military)
    ("{B} drives at {r} miles per hour for {T}.", "{he} drive", [40, 45, 48, 50, 54, 60, 66, 72], False),
    ("The supply convoy {R} is driving in travels at {r} miles per hour for {T}.", "the convoy travel",
     [24, 30, 32, 36, 40, 42, 45, 48, 50], True),
    ("A helicopter flies at {r} miles per hour for {T}.", "the helicopter fly", [120, 132, 144, 150, 160],
     True),
    ("{B} rides a train that travels at {r} miles per hour for {T}.", "the train travel", [36, 42, 48, 54, 60, 66, 72, 80], False),
    ("{B} rides a bicycle at {r} miles per hour for {T}.", "{he} ride", [10, 12, 14, 15, 16, 18], False),
    ("{B} rides a scooter at {r} miles per hour for {T}.", "{he} ride", [15, 18, 20, 24, 25], False),
    ("A city bus averages {r} miles per hour for {T}.", "the bus travel", [18, 20, 24, 30], False),
    ("{B} jogs at {r} miles per hour for {T}.", "{he} jog", [5, 6, 8, 9, 10], False),
]


@template("AR")
@_fill
def minutes_hours(rng, lvl, part=None):
    B = person(rng)
    if lvl == 1:
        st, who, speeds, mil = _pick(rng, _MIN_MOVERS, part)
        r = rng.choice(speeds)
        mins = rng.choice([10, 12, 15, 20, 30, 40, 45, 50])
        t = R(mins, 60)
        d = r * t
        need(d.is_integer)
        kw = dict(B=B, he=B.he, R=_trooper(rng))
        stem = st.format(r=r, T=f"{mins} minutes", **kw) + f" How many miles does {who.format(**kw)}?"
        wrong = [(Q(r * mins), "uses the minutes as if they were hours"),
                 (Q(r), "gives the distance for a full hour"),
                 (r * R(mins, 100), f"treats {mins} minutes as {m(dec_raw(R(mins, 100)))} hour")]
        return Problem(
            stem=stem, answer=d, fmt=_MID, section="AR", wrong=wrong,
            steps=[f"Change the time to hours: {m(f'{mins} \\text{{ min}} = {F(mins, 60)} = {frac_raw(t)}')} hour.",
                   f"Distance: {m(f'{r} \\times {frac_raw(t)} = {int_raw(d)}')} miles."],
            tip=(f"Or think per minute: {r} miles per hour is {m(f'{r} \\div 60 = {_d(R(r, 60))}')} "
                 f"mile{'s' if R(r, 60) > 1 else ''} per minute, and {m(f'{_d(R(r, 60))} \\times {mins} = {int_raw(d)}')}."
                 if R(r, 60).q in (1, 2, 4, 5, 10) else None),
            check=Fraction(r) * mins / 60,
        )
    v = _pick(rng, [0, 1, 2], part)
    if v == 0:
        # hours and minutes -> distance
        st, who, speeds, mil = rng.choice(_MIN_MOVERS)
        r = rng.choice(speeds)
        h = rng.choice([1, 2, 3])
        mins = rng.choice([15, 20, 30, 40, 45])
        t = h + R(mins, 60)
        d = r * t
        need(d.is_integer)
        kw = dict(B=B, he=B.he, R=_trooper(rng))
        stem = (st.format(r=r, T=f"{h} hour{'s' if h > 1 else ''} {mins} minutes", **kw)
                + f" How many miles does {who.format(**kw)}?")
        misread = r * (h + R(mins, 100))
        return Problem(
            stem=stem, answer=d, fmt=_MID, section="AR",
            wrong=[(misread, f"treats {h} hour{'s' if h > 1 else ''} {mins} minutes as "
                             f"{m(dec_raw(h + R(mins, 100)))} hours"),
                   (Q(r * h), "leaves out the extra minutes"),
                   (Q(r * (h + 1)), "rounds the time up to a whole hour")],
            steps=[f"Change the minutes to hours: {m(f'{mins} \\text{{ min}} = {F(mins, 60)} = {frac_raw(R(mins, 60))}')} hour, "
                   f"so the time is {m(mixed_raw(t))} hours.",
                   f"Distance: {m(f'{r} \\times {mixed_raw(t)} = {r} \\times {h} + {r} \\times {frac_raw(R(mins, 60))} = {int_raw(r * h)} + {_d(r * R(mins, 60))} = {_d(d)}')} miles."],
            check=Fraction(r) * (h * 60 + mins) / 60,
        )
    if v == 1:
        # distance in minutes -> speed in mph
        ctx = rng.choice([
            ("{B} drives {d} miles on the interstate in {mins} minutes.", "{his} average speed", [48, 54, 60, 66, 72]),
            ("A train covers {d} miles in {mins} minutes.", "the train's average speed", [42, 48, 54, 60, 72]),
            ("A convoy covers {d} miles of highway in {mins} minutes.", "the convoy's average speed", [30, 36, 42, 45, 48]),
            ("{B} cycles {d} miles in {mins} minutes.", "{his} average speed", [9, 10, 12, 15, 18]),
        ])
        st, what, speeds = ctx
        r = rng.choice(speeds)
        mins = rng.choice([10, 12, 15, 20, 30, 40, 45])
        d = r * R(mins, 60)
        need(d.is_integer and d > 1)
        stem = (st.format(B=B, d=int_raw(d), mins=mins) + f" What is {what.format(his=B.his)} in miles per hour?")
        return Problem(
            stem=stem, answer=Q(r), fmt=_MPH, section="AR",
            wrong=[(d / mins, "gives miles per minute, not miles per hour"),
                   (d * 100 / mins, f"treats {mins} minutes as {m(dec_raw(R(mins, 100)))} hour"),
                   (d * mins, "multiplies the distance by the minutes")],
            steps=[f"Change the time to hours: {m(f'{mins} \\text{{ min}} = {F(mins, 60)} = {frac_raw(R(mins, 60))}')} hour.",
                   f"Speed: {m(f'{int_raw(d)} \\div {frac_raw(R(mins, 60))} = {int_raw(d)} \\times {frac_raw(R(60, mins))} = {r}')} miles per hour."],
            tip=f"Or scale up to an hour: {mins} minutes goes into 60 minutes {m(_d(R(60, mins)))} times, and "
                f"{m(f'{int_raw(d)} \\times {_d(R(60, mins))} = {r}')}." if R(60, mins).is_integer else None,
            verify=lambda v: v * mins / 60 == d,
        )
    # distance and speed -> minutes
    ctx = rng.choice([
        ("{B} lives {d} miles from work and drives at an average of {r} miles per hour.", "the drive",
         [30, 36, 40, 45, 48, 60]),
        ("A medevac helicopter flies {d} miles to a field hospital at {r} miles per hour.", "the flight",
         [120, 144, 150, 180]),
        ("A shuttle bus travels {d} miles between two gates of a large base at {r} miles per hour.", "the trip",
         [20, 24, 30, 36]),
        ("{B} rides a bicycle {d} miles to school at {r} miles per hour.", "the ride", [8, 9, 10, 12, 15]),
    ])
    st, noun, speeds = ctx
    r = rng.choice(speeds)
    mins = rng.choice([10, 15, 20, 25, 30, 40, 45, 50])
    d = r * R(mins, 60)
    need(d.is_integer and d > 1)
    th = R(mins, 60)
    stem = st.format(B=B, d=int_raw(d), r=r) + f" How many minutes does {noun} take?"
    wrong = []
    if (Q(r) / d).is_integer:
        wrong.append((Q(r) / d, "divides the speed by the distance"))
    misread = int(th * 100)                     # 1/4 h -> 0.25 -> "25 minutes"
    if misread != mins and misread < 100:
        shown = dec_raw(th) if (th * 100).is_integer else f"0.{misread:02d}"
        wrong.append((Q(misread), f"reads {m(shown)} hour as {misread} minutes"))
    if (Q(r) * 60 / d).is_integer:
        wrong.append((Q(r) * 60 / d, "divides the speed by the distance before multiplying by 60"))
    return Problem(
        stem=stem, answer=Q(mins), fmt=_MIN, section="AR", wrong=wrong,
        steps=[f"Time in hours: {m(f't = d \\div r = {int_raw(d)} \\div {r} = {F(int_raw(d), r)} = {frac_raw(th)}')} hour.",
               f"Change to minutes: {m(f'{frac_raw(th)} \\times 60 = {mins}')} minutes."],
        verify=lambda v: r * v / 60 == d,
    )


# --------------------------------------------------------------------------
# 3. fuel: miles per gallon, gallons, cost
# --------------------------------------------------------------------------

_VEHICLES = [
    # (name, mpg lo, hi, gallons lo, hi, fuel, military)
    ("car", 24, 38, 8, 15, "gas", False),
    ("pickup truck", 15, 22, 10, 24, "gas", False),
    ("motorcycle", 40, 55, 3, 5, "gas", False),
    ("delivery van", 14, 20, 12, 25, "gas", False),
    ("Humvee", 8, 14, 10, 25, "diesel", True),
    ("school bus", 6, 10, 20, 50, "diesel", False),
]


@template("AR")
@_fill
def fuel(rng, lvl, part=None):
    name, mlo, mhi, glo, ghi, fuel_, mil = _pick(rng, _VEHICLES, part)
    B = _trooper(rng) if mil else person(rng)
    mpg = rng.randint(mlo, mhi)
    if lvl == 1:
        g = rng.randint(glo, ghi)
        miles = mpg * g
        if mil:
            stem = (f"During a field exercise, {_art(name)} {name} used {g} gallons of diesel to travel "
                    f"{num(miles)} miles. How many miles per gallon did it get?")
        elif name == "school bus":
            stem = (f"On a field trip, a school bus used {g} gallons of diesel to travel {num(miles)} miles. How "
                    f"many miles per gallon did it get?")
        else:
            stem = (f"{B}'s {name} used {g} gallons of gas to travel {num(miles)} miles. How many miles per "
                    f"gallon did it get?")
        return Problem(
            stem=stem, answer=Q(mpg), fmt=num, section="AR",
            wrong=[(Q(miles - g), "subtracts the gallons from the miles")],
            steps=[f"Miles per gallon {m('=')} miles {m('\\div')} gallons.",
                   f"{m(f'{int_raw(miles)} \\div {g} = {mpg}')} miles per gallon."],
            tip=f"Check: {m(f'{mpg} \\times {g} = {int_raw(miles)}')}.",
            verify=lambda v: v * g == miles,
            near=lambda gg: [Q(mpg + k) for k in gg.sample([-4, -3, -2, -1, 1, 2, 3, 4, 5], 6) if mpg + k > 0],
        )
    price = R(rng.randint(60, 90) * 5, 100)          # $3.00 - $4.50 a gallon
    if lvl == 2:
        if mil and rng.random() < 0.6:
            n = rng.choice([4, 5, 6, 8, 10])
            g = rng.randint(4, 15)
            miles = mpg * g
            stem = (f"A convoy of {n} {name}s will drive {num(miles)} miles to a training area. Each {name} gets "
                    f"{mpg} miles per gallon of diesel. How many gallons of fuel will the whole convoy use?")
            total = n * g
            return Problem(
                stem=stem, answer=Q(total), fmt=_GAL, section="AR",
                wrong=[(Q(g), f"finds the fuel for one {name} only"),
                       (R(miles, mpg * n), f"divides by the number of {name}s instead of multiplying"),
                       (Q(miles * n), "forgets to divide by the miles per gallon")],
                steps=[f"Fuel for one {name}: {m(f'{int_raw(miles)} \\div {mpg} = {g}')} gallons.",
                       f"For all {n}: {m(f'{n} \\times {g} = {total}')} gallons."],
                verify=lambda v: v * mpg == n * miles,
                near=lambda gg: [Q(total + k * n) for k in (1, 2, -1, -2, 3) if total + k * n > 0],
            )
        g = rng.randint(4, 16)
        miles = mpg * g
        cost = g * price
        if mil:
            stem = (f"{_cap(_art(name))} {name} gets {mpg} miles per gallon of diesel, and diesel costs "
                    f"{money(price)} per gallon. How much will the fuel cost for a supply run of {num(miles)} miles?")
        elif name == "school bus":
            stem = (f"A school bus gets {mpg} miles per gallon of diesel, and diesel costs {money(price)} per "
                    f"gallon. How much will the fuel cost for a field trip of {num(miles)} miles?")
        else:
            trip = rng.choice(["a trip to visit family", "a road trip", "a drive to the beach",
                               "a drive to a job interview"])
            stem = (f"{B}'s {name} gets {mpg} miles per gallon. Gas costs {money(price)} per gallon. How much "
                    f"will gas cost for {trip} of {num(miles)} miles?")
        return Problem(
            stem=stem, answer=cost, fmt=money, section="AR",
            wrong=[(Q(g), "gives the number of gallons, not the cost"),
                   (mpg * price, "multiplies the miles per gallon by the price"),
                   (miles * price, "multiplies the miles by the price per gallon")],
            steps=[f"Gallons needed: {m(f'{int_raw(miles)} \\div {mpg} = {g}')} gallons.",
                   f"Cost: {m(f'{g} \\times {money(price)} = {money(cost)}')}."],
            check=Fraction(miles, mpg) * Fraction(price.p, price.q),
        )
    # level 3: compare two vehicles
    a = rng.choice([24, 25, 28, 30, 32, 35, 36, 40])
    b = rng.choice([12, 14, 15, 16, 18, 20])
    need(a > b + 6)
    L = a * b // math.gcd(a, b)
    k = rng.choice([1, 2, 3, 4, 5, 6])
    miles = L * k
    need(150 <= miles <= 900)
    ga, gb = R(miles, a), R(miles, b)
    saved = (gb - ga) * price
    if rng.random() < 0.3:
        B2 = _trooper(rng, _RANKS)
        stem = f"{B2} is driving {num(miles)} miles to a new duty station"
    else:
        B2 = person(rng)
        stem = f"For a trip of {num(miles)} miles, {B2}"
    stem += ((" can" if stem.startswith("For") else " and can")
             + f" take either a car that gets {a} miles per gallon or a truck that gets {b} miles per "
               f"gallon. Gas costs {money(price)} per gallon. How much will {B2.he} save on gas by taking the car?")
    wrong = [((a - b) * price, "subtracts the miles per gallon and multiplies by the price"),
             (gb * price, "is the cost for the truck, not the savings"),
             (ga * price, "is the cost for the car, not the savings")]
    if (Q(miles) / (a - b)).is_integer:
        wrong.append((Q(miles) / (a - b) * price, "divides the distance by the difference in miles per gallon"))
    return Problem(
        stem=stem, answer=saved, fmt=money, section="AR", wrong=wrong,
        steps=[f"Gas for the truck: {m(f'{int_raw(miles)} \\div {b} = {_d(gb)}')} gallons. "
               f"Gas for the car: {m(f'{int_raw(miles)} \\div {a} = {_d(ga)}')} gallons.",
               f"Gallons saved: {m(f'{_d(gb)} - {_d(ga)} = {_d(gb - ga)}')}.",
               f"Money saved: {m(f'{_d(gb - ga)} \\times {money(price)} = {money(saved)}')}."],
        check=Fraction(miles) * (Fraction(1, b) - Fraction(1, a)) * Fraction(price.p, price.q),
    )


# --------------------------------------------------------------------------
# 4. other rates: words, pages, items (L1, L2)
# --------------------------------------------------------------------------

_WORK = [
    # (rate sentence, amount unit (plural), per, rate choices, time choices (in "per" units), military,
    #  question for amount, question for time)
    ("{B} types {r} words per minute.", "words", "minute", [40, 45, 50, 55, 60, 65, 70, 75, 80],
     [10, 12, 15, 20, 25, 30], False,
     "How many words can {he} type in {t} minutes?", "How many minutes will it take {him} to type a {a}-word report?"),
    ("An office printer prints {r} pages per minute.", "pages", "minute", [15, 18, 20, 24, 25, 30, 35, 40],
     [3, 4, 5, 6, 8, 12], False,
     "How many pages can it print in {t} minutes?", "How many minutes will it take to print {a} pages?"),
    ("{B} reads about {r} pages per hour.", "pages", "hour", [20, 24, 25, 30, 35, 40, 45],
     [2, 3, 4, 5], False,
     "How many pages can {he} read in {t} hours?", "How many hours will it take {him} to read a {a}-page book?"),
    ("Working steadily, a soldier can fill {r} sandbags per hour.", "sandbags", "hour", [20, 24, 25, 30, 35, 40],
     [2, 3, 4, 5, 6], True,
     "How many sandbags can the soldier fill in {t} hours?", "How many hours will it take to fill {a} sandbags?"),
    ("A field kitchen crew can make {r} sandwiches per hour.", "sandwiches", "hour", [40, 45, 50, 60, 75, 80],
     [2, 3, 4, 5], True,
     "How many sandwiches can the crew make in {t} hours?", "How many hours will it take to make {a} sandwiches?"),
    ("A bottling machine fills {r} bottles per minute.", "bottles", "minute", [45, 48, 50, 60, 75, 80, 90],
     [10, 12, 15, 20, 30], False,
     "How many bottles can it fill in {t} minutes?", "How many minutes will it take to fill {a} bottles?"),
    ("A recruiter makes about {r} phone calls per hour.", "calls", "hour", [12, 15, 16, 18, 20, 24],
     [2, 3, 4, 5, 6], True,
     "How many calls can the recruiter make in {t} hours?", "How many hours will it take to make {a} calls?"),
    ("At a packing job, {B} assembles {r} boxes per hour.", "boxes", "hour", [30, 35, 40, 45, 50, 60],
     [3, 4, 5, 6, 8], False,
     "How many boxes can {he} assemble in {t} hours?", "How many hours will it take {him} to assemble {a} boxes?"),
    ("A conveyor belt at a warehouse moves {r} packages per minute.", "packages", "minute",
     [12, 15, 18, 20, 24, 25], [10, 15, 20, 30, 45], False,
     "How many packages does it move in {t} minutes?", "How many minutes will it take to move {a} packages?"),
]


@template("AR")
@_fill
def work_rate(rng, lvl, part=None):
    st, things, per, rates, times, mil, q_amt, q_time = _pick(rng, _WORK, part)
    B = person(rng)
    r = rng.choice(rates)
    if lvl == 1:
        t = rng.choice(times)
        a = r * t
        kw = dict(B=B, he=B.he, him=B.him, t=t, a=int_raw(a), r=r)
        if rng.random() < 0.5:
            stem = st.format(**kw) + " " + q_amt.format(**kw)
            return Problem(
                stem=stem, answer=Q(a), fmt=num, section="AR",
                wrong=[(Q(r + t), f"adds the rate and the time instead of multiplying")],
                steps=[f"Amount {m('=')} rate {m('\\times')} time.",
                       f"{m(f'{r} \\times {t} = {int_raw(a)}')} {things}."],
                verify=lambda v: v / t == r,
            )
        stem = st.format(**kw) + " " + q_time.format(**kw)
        return Problem(
            stem=stem, answer=Q(t), fmt=unit(num, per), section="AR",
            wrong=[(Q(a - r), "subtracts the rate from the total")],
            steps=[f"Time {m('=')} amount {m('\\div')} rate.",
                   f"{m(f'{int_raw(a)} \\div {r} = {t}')} {per}s."],
            tip=f"Check: {m(f'{r} \\times {t} = {int_raw(a)}')} {things}.",
            verify=lambda v: v * r == a,
            near=lambda g: [Q(t + k) for k in g.sample([-3, -2, -1, 1, 2, 3, 5], 6) if t + k > 0],
        )
    # level 2: rate per hour, time in minutes (or the other way)
    ctx = rng.choice([
        ("A bottling machine fills {r} bottles per hour.", "bottles", [1200, 1500, 1800, 2400, 3000, 3600],
         "How many bottles does it fill in {mins} minutes?"),
        ("A printing press turns out {r} flyers per hour.", "flyers", [600, 900, 1200, 1500, 1800, 2400],
         "How many flyers does it print in {mins} minutes?"),
        ("A team of soldiers can fill {r} sandbags per hour.", "sandbags", [120, 150, 180, 240, 300],
         "How many sandbags can the team fill in {mins} minutes?"),
        ("A fuel pump on a tanker truck delivers {r} gallons per hour.", "gallons", [600, 900, 1200, 1800, 2400],
         "How many gallons does it deliver in {mins} minutes?"),
        ("{B} can stuff {r} envelopes per hour.", "envelopes", [120, 180, 240, 300, 360],
         "How many envelopes can {he} stuff in {mins} minutes?"),
        ("A water purification unit at a field camp produces {r} gallons of drinking water per hour.", "gallons",
         [600, 900, 1200, 1500, 1800, 3000], "How many gallons does it produce in {mins} minutes?"),
        ("A cafeteria line serves {r} meals per hour.", "meals", [180, 240, 300, 360, 420],
         "How many meals does it serve in {mins} minutes?"),
        ("A data clerk enters {r} records per hour.", "records", [60, 90, 120, 150, 180],
         "How many records can the clerk enter in {mins} minutes?"),
    ])
    st, things, rs, q = ctx
    r = rng.choice(rs)
    mins = rng.choice([10, 15, 20, 25, 30, 40, 45, 50])
    a = r * R(mins, 60)
    need(a.is_integer)
    stem = st.format(r=num(r), B=B) + " " + q.format(mins=mins, he=B.he)
    wrong = [(Q(r * mins), "uses the minutes as if they were hours"),
             (R(r, mins), "divides the hourly rate by the minutes"),
             (r * R(mins, 100), f"treats {mins} minutes as {m(dec_raw(R(mins, 100)))} hour")]
    return Problem(
        stem=stem, answer=a, fmt=num, section="AR",
        wrong=[w for w in wrong if Q(w[0]).is_integer],
        steps=[f"Change the time to hours: {m(f'{mins} \\text{{ min}} = {F(mins, 60)} = {frac_raw(R(mins, 60))}')} hour.",
               f"Amount: {m(f'{int_raw(r)} \\times {frac_raw(R(mins, 60))} = {int_raw(a)}')} {things}."],
        tip=f"Or find the rate per minute: {m(f'{int_raw(r)} \\div 60 = {_d(R(r, 60))}')}, and "
            f"{m(f'{_d(R(r, 60))} \\times {mins} = {int_raw(a)}')}." if R(r, 60).is_integer else None,
        check=Fraction(r * mins, 60),
    )


# --------------------------------------------------------------------------
# 5. two movers: toward each other, opposite or same direction (L2)
# --------------------------------------------------------------------------

_PAIRS = [
    # (two things, speed lo, hi, step, military)
    ("two supply trucks", 40, 60, 5, True),
    ("two trains", 45, 70, 5, False),
    ("two cars", 45, 65, 5, False),
    ("two buses", 40, 60, 5, False),
    ("two cyclists", 10, 18, 1, False),
    ("two Humvees", 30, 50, 5, True),
]


@template("AR")
@_fill
def two_movers(rng, lvl, part=None):
    things, lo, hi, st, mil = _pick(rng, _PAIRS, part)
    r1, r2 = sorted(rng.sample(range(lo, hi + 1, st), 2))
    kind = rng.choice(["toward", "toward", "opposite", "same"])
    place = ("the base" if mil else "a town" if "cyclists" not in things else "a park")
    if kind == "toward":
        t = rng.choice([R(1, 2), Q(1), R(3, 2), Q(2), R(5, 2), Q(3), Q(4)])
        D = (r1 + r2) * t
        need(D.is_integer and D >= 10)
        route = ("on parallel tracks" if "train" in things else "on the same trail" if "cyclist" in things
                 else "on the same road")
        stem = (f"{_cap(things)} start {int_raw(D)} miles apart and travel toward each other {route}. "
                f"One goes {r1} miles per hour and the other goes {r2} miles per hour. In how many hours will "
                f"they meet?")
        wrong = [(D / (r2 - r1), "subtracts the speeds, but the two are closing the gap together"),
                 (2 * t, "divides by the average of the two speeds instead of their sum"),
                 (D / r2, "uses only one speed"),
                 (D / r1, "uses only one speed")]
        return Problem(
            stem=stem, answer=t, fmt=_HR, section="AR",
            wrong=[w for w in wrong if (Q(w[0]) * 10).is_integer and w[0] != t],
            steps=[f"Moving toward each other, the gap closes at the sum of the speeds: "
                   f"{m(f'{r1} + {r2} = {r1 + r2}')} miles per hour.",
                   f"Time to close {int_raw(D)} miles: {m(f'{int_raw(D)} \\div {r1 + r2} = {_d(t)}')} {_hw(t)}."],
            tip=f"Check: in {_hrs(t)} they cover {m(f'{_d(r1 * t)} + {_d(r2 * t)} = {int_raw(D)}')} miles.",
            verify=lambda v: (r1 + r2) * v == D,
        )
    t = rng.choice([2, 3, 4, 5]) if "cyclists" not in things else rng.choice([2, 3])
    if kind == "opposite":
        ans = (r1 + r2) * t
        stem = (f"{_cap(things)} leave {place} at the same time and travel in opposite directions. One goes "
                f"{r1} miles per hour and the other goes {r2} miles per hour. How far apart are they after "
                f"{t} hours?")
        return Problem(
            stem=stem, answer=Q(ans), fmt=_MI, section="AR",
            wrong=[(Q((r2 - r1) * t), "subtracts the speeds, but the two are moving apart in opposite directions"),
                   (Q(r2 * t), "gives only the faster one's distance"),
                   (Q(r1 + r2), f"forgets to multiply by the {t} hours")],
            steps=[f"Moving in opposite directions, the gap grows at the sum of the speeds: "
                   f"{m(f'{r1} + {r2} = {r1 + r2}')} miles per hour.",
                   f"After {t} hours: {m(f'{r1 + r2} \\times {t} = {ans}')} miles."],
            verify=lambda v: v == r1 * t + r2 * t,
        )
    ans = (r2 - r1) * t
    stem = (f"{_cap(things)} leave {place} at the same time and travel in the same direction "
            f"{'on parallel tracks' if 'train' in things else 'on the same road'}. "
            f"One goes {r1} miles per hour and the other goes {r2} miles per hour. How far apart are they after "
            f"{t} hours?")
    return Problem(
        stem=stem, answer=Q(ans), fmt=_MI, section="AR",
        wrong=[(Q((r1 + r2) * t), "adds the speeds, but the two travel in the same direction"),
               (Q(r2 * t), "gives the faster one's distance, not the distance between them"),
               (Q(r2 - r1), f"forgets to multiply by the {t} hours")],
        steps=[f"In the same direction, the faster one pulls ahead at the difference of the speeds: "
               f"{m(f'{r2} - {r1} = {r2 - r1}')} miles per hour.",
               f"After {t} hours: {m(f'{r2 - r1} \\times {t} = {ans}')} miles apart."],
        verify=lambda v: v == r2 * t - r1 * t,
    )


# --------------------------------------------------------------------------
# 6. pace and speed (L2)
# --------------------------------------------------------------------------

_RUNS = [
    # (prefix, verb (3rd person), verb (base), distance in miles, total minutes for the speed question,
    #  speeds (mph) for the time question, ranks or None for civilians)
    ("On the Army fitness test, ", "runs", "run", 2, [12, 15, 16, 20, 24], [6, R(15, 2), 8, 10], _ARMY),
    ("On the Navy fitness test, ", "runs", "run", R(3, 2), [9, 10, 12, 15, 18], [6, R(15, 2), 9, 10],
     ["Seaman", "Petty Officer"]),
    ("On a Marine Corps fitness test, ", "runs", "run", 3, [18, 20, 24, 30], [6, R(15, 2), 9, 10],
     ["Lance Corporal", "Corporal", "Sergeant"]),
    ("", "jogs", "jog", 4, [30, 32, 40, 48], [5, 6, 8], None),
    ("", "runs", "run", 5, [40, 50, 60], [6, R(15, 2), 10], None),
    ("", "walks", "walk", 3, [45, 54, 60], [3, 4], None),
]


@template("AR")
@_fill
def pace_speed(rng, lvl, part=None):
    pre, verbs, verb, d, totals, speeds, ranks = _pick(rng, _RUNS, part)
    B = _trooper(rng, ranks) if ranks else person(rng)
    who = f"{pre}{B}" if pre else f"{B}"
    if rng.random() < 0.55:
        T = rng.choice(totals)
        speed = Q(d) * 60 / T
        pace = Q(T) / d
        need((speed * 10).is_integer)
        stem = f"{who} {verbs} {_d(d)} miles in {T} minutes. What is {B.his} average speed in miles per hour?"
        wrong = [(pace, "gives the pace in minutes per mile, not the speed"),
                 (Q(d) / T, "gives miles per minute, not miles per hour"),
                 (Q(d) * T, "multiplies the distance by the time")]
        return Problem(
            stem=stem, answer=speed, fmt=_MPH, section="AR",
            wrong=[w for w in wrong if (Q(w[0]) * 1000).is_integer],
            steps=[f"Change the time to hours: {m(f'{T} \\text{{ min}} = {F(T, 60)} = {frac_raw(R(T, 60))}')} hour.",
                   f"Speed: {m(f'{_d(d)} \\div {frac_raw(R(T, 60))} = {_d(d)} \\times {frac_raw(R(60, T))} = {_d(speed)}')} miles per hour."],
            tip=(f"Or: the pace is {m(f'{T} \\div {_d(d)} = {_d(pace)}')} minutes per mile, and "
                 f"{m(f'60 \\div {_d(pace)} = {_d(speed)}')} mph." if (pace * 10).is_integer else None),
            verify=lambda v: v * T / 60 == d,
        )
    speed = Q(rng.choice(speeds))
    T = Q(d) * 60 / speed
    need(T.is_integer)
    stem = (f"{who} {verbs} at a steady {_d(speed)} miles per hour. How many minutes does it take {B.him} to "
            f"{verb} {_d(d)} miles?")
    th = Q(d) / speed
    wrong = []
    if (speed / d).is_integer:
        wrong.append((speed / d, "divides the speed by the distance"))
    misread = int(th * 100)
    if th < 1 and misread != T:
        shown = dec_raw(th) if (th * 100).is_integer else f"0.{misread:02d}"
        wrong.append((Q(misread), f"reads {m(shown)} hour as {misread} minutes"))
    wrong.append((Q(60) / speed * 1 if (Q(60) / speed).is_integer and Q(60) / speed != T else speed * d,
                  "finds the minutes for one mile only" if (Q(60) / speed).is_integer and Q(60) / speed != T
                  else "multiplies the speed by the distance"))
    return Problem(
        stem=stem, answer=T, fmt=_MIN, section="AR",
        wrong=[w for w in wrong if Q(w[0]).is_integer],
        steps=[f"Time in hours: {m(f'{_d(d)} \\div {_d(speed)} = {frac_raw(th)}')} hour.",
               f"Change to minutes: {m(f'{frac_raw(th)} \\times 60 = {int_raw(T)}')} minutes."],
        tip=(f"Or: at {_d(speed)} mph one mile takes {m(f'60 \\div {_d(speed)} = {_d(60 / speed)}')} minutes, and "
             f"{m(f'{_d(d)} \\times {_d(60 / speed)} = {int_raw(T)}')}." if ((60 / speed) * 10).is_integer else None),
        verify=lambda v: speed * v / 60 == d,
    )


# --------------------------------------------------------------------------
# 7. two-leg trips (L2 total time, L3 average speed)
# --------------------------------------------------------------------------

_LEGS = [
    # (stem, leg-1 speeds, leg-2 speeds, military)
    ("{B} drives {d1} miles on the highway at {r1} miles per hour, then {d2} miles on country roads at "
     "{r2} miles per hour.", [55, 60, 65, 70], [30, 35, 40, 45], False),
    ("A convoy travels {d1} miles on paved road at {r1} miles per hour, then {d2} miles on a dirt road at "
     "{r2} miles per hour.", [40, 45, 50], [15, 20, 25], True),
    ("{B} bikes {d1} miles on a flat trail at {r1} miles per hour, then {d2} miles uphill at {r2} miles per "
     "hour.", [14, 15, 16, 18], [6, 8, 9, 10], False),
    ("A delivery truck travels {d1} miles on the interstate at {r1} miles per hour, then {d2} miles in "
     "city traffic at {r2} miles per hour.", [60, 65, 70], [20, 25, 30], False),
    ("On a training exercise, a squad marches {d1} miles at {r1} miles per hour, then {d2} miles through "
     "rough terrain at {r2} miles per hour.", [3, 4], [2], True),
    ("{B} runs {d1} miles at {r1} miles per hour, then walks {d2} miles at {r2} miles per hour.",
     [6, 8, 10], [3, 4], False),
    ("{T} drives a Humvee {d1} miles on a paved road at {r1} miles per hour, then {d2} miles on a desert "
     "track at {r2} miles per hour.", [40, 45, 50, 55], [10, 12, 15, 20], True),
    ("A bus travels {d1} miles on the highway at {r1} miles per hour, then {d2} miles through town at {r2} "
     "miles per hour.", [50, 55, 60, 65], [20, 24, 25, 30], False),
]


@template("AR")
@_fill
def two_leg(rng, lvl, part=None):
    st, s1, s2, mil = _pick(rng, _LEGS, part)
    B = person(rng)
    r1, r2 = rng.choice(s1), rng.choice(s2)
    t1 = rng.choice([R(1, 2), Q(1), R(3, 2), Q(2), R(5, 2), Q(3)])
    t2 = rng.choice([R(1, 2), Q(1), R(3, 2), Q(2)])
    d1, d2 = r1 * t1, r2 * t2
    need(d1.is_integer and d2.is_integer and t1 != t2)
    T = t1 + t2
    D = d1 + d2
    stem0 = st.format(B=B, T=_trooper(rng), d1=int_raw(d1), d2=int_raw(d2), r1=r1, r2=r2).replace(" 1 miles", " 1 mile")
    legs = [f"First part: {m(f'{int_raw(d1)} \\div {r1} = {_d(t1)}')} hour{'s' if t1 != 1 else ''}.",
            f"Second part: {m(f'{int_raw(d2)} \\div {r2} = {_d(t2)}')} hour{'s' if t2 != 1 else ''}."]
    if lvl == 2:
        stem = stem0 + " How many hours does the whole trip take?"
        wrong = [(D / R(r1 + r2, 2), "divides the total distance by the average of the two speeds"),
                 (D / r1, "uses the first speed for the whole trip"),
                 (t1, "finds the time for the first part only"),
                 (D / r2, "uses the second speed for the whole trip")]
        return Problem(
            stem=stem, answer=T, fmt=_HR, section="AR",
            wrong=[w for w in wrong if (Q(w[0]) * 100).is_integer],
            steps=legs + [f"Total: {m(f'{_d(t1)} + {_d(t2)} = {_d(T)}')} hours."],
            verify=lambda v: v == Fraction(int(d1), r1) + Fraction(int(d2), r2),
        )
    avg = D / T
    need((avg * 10).is_integer and avg != R(r1 + r2, 2))
    stem = stem0 + " What is the average speed for the whole trip?"
    return Problem(
        stem=stem, answer=avg, fmt=_MPH, section="AR",
        wrong=[(R(r1 + r2, 2), "averages the two speeds, but more time is spent at one of them"),
               (Q(r1 + r2), "adds the two speeds"),
               (D / t1, "divides the total distance by the first part's time only"),
               (D / t2, "divides the total distance by the second part's time only")],
        steps=legs + [f"Total distance: {m(f'{int_raw(d1)} + {int_raw(d2)} = {int_raw(D)}')} miles. "
                      f"Total time: {m(f'{_d(t1)} + {_d(t2)} = {_d(T)}')} hours.",
                      f"Average speed: {m(f'{int_raw(D)} \\div {_d(T)} = {_d(avg)}')} miles per hour."],
        check=Fraction(int(D)) / (Fraction(int(d1), r1) + Fraction(int(d2), r2)),
    )


# --------------------------------------------------------------------------
# 8. round-trip average speed (L3)
# --------------------------------------------------------------------------

_ROUND = [
    # (stem with {d} {a} {b}, speed choices, military, longest one-way distance)
    ("A convoy drives {d} miles to a training range at {a} miles per hour and returns on the same road at "
     "{b} miles per hour.", [20, 24, 30, 36, 40, 45, 48, 60], True, 180),
    ("{B} drives {d} miles to visit a friend at {a} miles per hour and drives home at {b} miles per hour.",
     [30, 40, 45, 48, 50, 60, 72, 75], False, 300),
    ("{T} flies a supply helicopter {d} miles to an outpost at {a} miles per hour and flies back at {b} "
     "miles per hour.", [100, 120, 125, 150, 180, 200], True, 450),
    ("{B} rides a bicycle {d} miles to a lake at {a} miles per hour and rides back at {b} miles per hour.",
     [8, 9, 10, 12, 15, 16, 18, 20, 24], False, 60),
    ("{T} leads a convoy {d} miles to a training range at {a} miles per hour. On the way back, the convoy "
     "travels the same road at {b} miles per hour.", [20, 24, 30, 36, 40, 45, 48, 60], True, 180),
    ("{B} drives {d} miles to a job site at {a} miles per hour in morning traffic and drives back at {b} miles "
     "per hour in the evening.", [30, 36, 40, 45, 50, 60], False, 120),
    ("A medical helicopter flies {d} miles to a rural hospital at {a} miles per hour and flies back at {b} "
     "miles per hour.", [100, 120, 125, 150, 180, 200], False, 300),
    ("A boat travels {d} miles upstream at {a} miles per hour and returns downstream at {b} miles per hour.",
     [6, 8, 9, 10, 12, 15, 18, 20, 24], False, 60),
    ("A Humvee patrol drives {d} miles to a checkpoint at {a} miles per hour and returns at {b} miles per "
     "hour.", [20, 24, 30, 36, 40, 45, 60], True, 120),
    ("A tow truck drives {d} miles to a breakdown at {a} miles per hour and tows the car back at {b} miles "
     "per hour.", [30, 36, 40, 45, 48, 60], False, 120),
]


@template("AR")
@_fill
def round_trip(rng, lvl, part=None):
    st, speeds, mil, dmax = _pick(rng, _ROUND, part)
    B = person(rng)
    combos = []
    for a in speeds:
        for b in speeds:
            if a == b or ("upstream" in st and a > b):
                continue
            L = a * b // math.gcd(a, b)
            for d in range(L, dmax + 1, L):
                avg = R(2 * a * b, a + b)
                if R(d, a) + R(d, b) <= 12 and (avg * 10).is_integer and d >= 6:
                    combos.append((a, b, d))
    need(combos)
    a, b, d = rng.choice(combos)
    t1, t2 = R(d, a), R(d, b)
    avg = 2 * d / (t1 + t2)
    stem = (st.format(B=B, T=_trooper(rng, _PILOT if "flies" in st else _GROUND), d=d, a=a, b=b)
            + choose(rng, " What is the average speed for the whole round trip?",
                     " What is the average speed for the round trip?"))
    return Problem(
        stem=stem, answer=avg, fmt=_MPH, section="AR",
        wrong=[(R(a + b, 2), "averages the two speeds, but more time is spent at the slower speed"),
               (d / (t1 + t2), "uses the one-way distance instead of the round-trip distance"),
               (Q(a + b), "adds the two speeds")],
        steps=[f"Time going: {m(f'{d} \\div {a} = {_d(t1)}')} {_hw(t1)}. Time returning: "
               f"{m(f'{d} \\div {b} = {_d(t2)}')} {_hw(t2)}.",
               f"Total distance: {m(f'2 \\times {d} = {2 * d}')} miles. Total time: "
               f"{m(f'{_d(t1)} + {_d(t2)} = {_d(t1 + t2)}')} {_hw(t1 + t2)}.",
               f"Average speed: {m(f'{2 * d} \\div {_d(t1 + t2)} = {_d(avg)}')} miles per hour."],
        tip=f"Shortcut for equal distances: {m(f'2ab \\div (a + b) = 2 \\times {a} \\times {b} \\div {a + b} = {_d(avg)}')}.",
        check=Fraction(2 * a * b, a + b),
    )


# --------------------------------------------------------------------------
# 9. catching up (L3)
# --------------------------------------------------------------------------

_CHASE = [
    # (stem with {r1} {r2} {h}, slow range, fast range, military, chaser)
    ("A supply convoy leaves the base traveling {r1} miles per hour. {h} later, {T} leaves the base in a repair "
     "truck on the same road at {r2} miles per hour to catch up.", (25, 40), (45, 60), True, "the repair truck"),
    ("A freight train leaves a station at {r1} miles per hour. {h} later, {B} boards a passenger train that "
     "leaves the same station on a parallel track at {r2} miles per hour.", (35, 50), (60, 80), False,
     "the passenger train"),
    ("A platoon starts a road march at {r1} miles per hour. {h} later, {T} follows the same route in a Humvee "
     "carrying water at {r2} miles per hour.", (3, 4), (15, 30), True, "the Humvee"),
    ("{B} leaves home on a bicycle at {r1} miles per hour. {h} later, {his} sister follows on a scooter at "
     "{r2} miles per hour.", (8, 12), (15, 24), False, "the sister"),
    ("A cargo ship leaves port at {r1} miles per hour. {h} later, a supply boat leaves the same port on the "
     "same course at {r2} miles per hour.", (12, 18), (20, 32), False, "the supply boat"),
    ("A moving truck leaves {B}'s old house at {r1} miles per hour. {h} later, {B} follows the same route in "
     "{his} car at {r2} miles per hour.", (45, 55), (60, 72), False, "the car"),
]


@template("AR")
@_fill
def catch_up(rng, lvl, part=None):
    st, (slo, shi), (flo, fhi), mil, chaser = _pick(rng, _CHASE, part)
    B = person(rng)
    r1 = rng.randint(slo, shi)
    h = rng.choice([R(1, 2), Q(1), R(3, 2), Q(2)])
    head = r1 * h
    need(head.is_integer)
    fast = [x for x in range(flo, fhi + 1) if (head / (x - r1) * 4).is_integer and head / (x - r1) <= 6]
    need(fast)
    r2 = rng.choice(fast)
    t = head / (r2 - r1)
    hw = {R(1, 2): "Half an hour", Q(1): "One hour", R(3, 2): "An hour and a half", Q(2): "Two hours"}[h]
    stem = st.format(B=B, T=_trooper(rng), his=B.his, r1=r1, r2=r2, h=hw)
    ask_dist = rng.random() < 0.35
    if ask_dist:
        stem += f" How far from the start will {chaser} catch up?"
        dist = r2 * t
        need((dist * 10).is_integer)
        return Problem(
            stem=stem, answer=dist, fmt=_MID, section="AR",
            wrong=[(head, "is the head start, not the meeting point"),
                   (r1 * t, f"uses the slower speed for the time {chaser} drives"),
                   (r2 * (t + h), f"counts {chaser}'s time from when the first one left")],
            steps=[f"Head start: {m(f'{r1} \\times {_d(h)} = {int_raw(head)}')} miles.",
                   f"The gap closes at {m(f'{r2} - {r1} = {r2 - r1}')} miles per hour, so it takes "
                   f"{m(f'{int_raw(head)} \\div {r2 - r1} = {_d(t)}')} {_hw(t)}.",
                   f"Distance from the start: {m(f'{r2} \\times {_d(t)} = {_d(dist)}')} miles."],
            tip=f"Check: the slower one has gone {m(f'{r1} \\times {_d(t + h)} = {_d(r1 * (t + h))}')} miles too.",
            verify=lambda v: v == r1 * (t + h),
        )
    stem += f" How many hours after {chaser} leaves will it catch up?".replace("the sister leaves will it", "the sister leaves will she")
    wrong = [(t + h, "counts the time from when the first one left"),
             (head / (r1 + r2), "adds the speeds, but the gap closes at the difference of the speeds"),
             (head / r2, "divides the head start by the faster speed instead of the difference")]
    return Problem(
        stem=stem, answer=t, fmt=_HR, section="AR",
        wrong=[w for w in wrong if (Q(w[0]) * 100).is_integer],
        steps=[f"Head start: in {_hrs(h)} the first one goes {m(f'{r1} \\times {_d(h)} = {int_raw(head)}')} miles.",
               f"The gap closes at the difference of the speeds: {m(f'{r2} - {r1} = {r2 - r1}')} miles per hour.",
               f"Time to close it: {m(f'{int_raw(head)} \\div {r2 - r1} = {_d(t)}')} {_hw(t)}."],
        tip=f"Check: in {_hrs(t)} the chaser goes {m(f'{r2} \\times {_d(t)} = {_d(r2 * t)}')} miles, and the first one "
            f"has gone {m(f'{r1} \\times {_d(t + h)} = {_d(r1 * (t + h))}')} miles.",
        verify=lambda v: r2 * v == r1 * (v + h),
    )


# --------------------------------------------------------------------------
# 10. feet per second <-> miles per hour (L3)
# --------------------------------------------------------------------------

_FPS = [
    # (stem start with {v}, mph values (multiples of 15), military)
    ("A car is traveling at {v} on the highway.", [45, 60, 75], False),
    ("A delivery truck drives at {v}.", [30, 45, 60], False),
    ("A pitcher throws a fastball at {v}.", [75, 90], False),
    ("A skydiver in free fall drops at about {v}.", [105, 120], True),
    ("A paratrooper's open parachute slows the fall to about {v}.", [15], True),
    ("A Black Hawk helicopter cruises at {v}.", [135, 150], True),
    ("A tank crosses open ground at {v}.", [30, 45], True),
    ("A sprinter reaches a top speed of {v}.", [15, 30], False),
    ("A cheetah can run at {v}.", [60, 75], False),
    ("A racehorse gallops at {v}.", [30, 45], False),
    ("A roller coaster reaches a top speed of {v}.", [60, 75, 90], False),
    ("A speedboat cruises at {v}.", [45, 60], False),
    ("{B} drives through a school zone at {v}.", [15], False),
    ("{B} pitches a softball at {v}.", [45, 60], False),
    ("{B} rides a motorcycle at {v}.", [45, 60, 75], False),
    ("{B} sprints at {v} near the end of a race.", [15], False),
    ("{T}'s Humvee travels at {v} on a gravel road.", [30, 45], True),
    ("{T} drives a cargo truck at {v} on the highway.", [45, 60], True),
]

_FPS_Q = {True: [" How many feet per second is this?", " What is this speed in feet per second?"],
          False: [" How many miles per hour is this?", " What is this speed in miles per hour?"]}


_KNOWN = [(15, 22), (30, 44), (45, 66), (60, 88), (75, 110), (90, 132)]   # mph, feet per second


def _ratio_raw(k):
    return frac_raw(k) if k.q == 3 else _d(k)


@template("AR")
@_fill
def fps_mph(rng, lvl, part=None):
    st, mphs, mil = _pick(rng, _FPS, part)
    mph = rng.choice(mphs)
    B, T = person(rng), _trooper(rng)
    fps = mph * R(22, 15)
    need(fps.is_integer)
    pairs = [(km, kf) for km, kf in _KNOWN
             if km != mph and R(mph, km).q in (1, 2, 3, 4) and R(mph, km) <= 10]
    full = rng.random() < 0.4 or not pairs
    to_fps = rng.random() < 0.5
    if full:
        conv = "(1 mile = 5,280 feet and 1 hour = 3,600 seconds.)"
    else:
        km, kf = rng.choice(pairs)
        k = R(mph, km)
        conv = f"({km} miles per hour is the same as {kf} feet per second.)"
        same_pair = (f"Compare with the known pair: {m(f'{mph} \\div {km} = {_ratio_raw(k)}')}, so the speed is "
                     f"{m(_ratio_raw(k))} times {km} mph" if to_fps else
                     f"Compare with the known pair: {m(f'{int_raw(fps)} \\div {kf} = {_ratio_raw(k)}')}, so the "
                     f"speed is {m(_ratio_raw(k))} times {kf} feet per second")
    if to_fps:
        stem = (st.format(v=f"{mph} miles per hour", B=B, T=T) + rng.choice(_FPS_Q[True]) + " " + conv)
        if full:
            steps = [f"Change miles to feet: {m(f'{mph} \\times 5{{,}}280 = {int_raw(mph * 5280)}')} feet per hour.",
                     f"Change hours to seconds: {m(f'{int_raw(mph * 5280)} \\div 3{{,}}600 = {int_raw(fps)}')} feet per second."]
            tip = (f"Simplify first: {m('5{,}280 \\div 3{,}600 = \\frac{22}{15}')}, so "
                   f"{m(f'{mph} \\times \\frac{{22}}{{15}} = {int_raw(fps)}')}.")
            wrong = [(Q(mph * 88), "changes hours to minutes but not to seconds, which gives feet per minute"),
                     (Q(mph * 5280), "changes miles to feet but never changes hours to seconds")]
        else:
            steps = [same_pair + ".",
                     f"Feet per second: {m(f'{_ratio_raw(k)} \\times {kf} = {int_raw(fps)}')}."]
            tip = (f"Check with 15 mph {m('=')} 22 feet per second: {m(f'{mph} = {mph // 15} \\times 15')}, and "
                   f"{m(f'{mph // 15} \\times 22 = {int_raw(fps)}')}." if mph > 15 else None)
            wrong = [(Q(mph + kf - km), f"adds the difference {m(f'{kf} - {km} = {kf - km}')} instead of "
                                        f"multiplying by {m(_ratio_raw(k))}")]
            inv = Q(kf) / k
            if inv.is_integer and inv != fps:
                wrong.append((inv, f"divides by {m(_ratio_raw(k))} instead of multiplying"))
        return Problem(
            stem=stem, answer=fps, fmt=num, section="AR", wrong=wrong, steps=steps, tip=tip,
            verify=lambda v: v * 3600 == mph * 5280,
            near=lambda g: [fps + d for d in g.sample([-22, -11, -8, -4, 4, 8, 11, 22], 6) if fps + d > 0],
        )
    stem = (st.format(v=f"{int_raw(fps)} feet per second", B=B, T=T) + rng.choice(_FPS_Q[False]) + " " + conv)
    if full:
        steps = [f"Feet per hour: {m(f'{int_raw(fps)} \\times 3{{,}}600 = {int_raw(fps * 3600)}')}.",
                 f"Miles per hour: {m(f'{int_raw(fps * 3600)} \\div 5{{,}}280 = {mph}')}."]
        tip = (f"Simplify first: {m('3{,}600 \\div 5{,}280 = \\frac{15}{22}')}, so "
               f"{m(f'{int_raw(fps)} \\times \\frac{{15}}{{22}} = {mph}')}.")
        wrong = [(fps * R(22, 15), "turns the conversion upside down (multiplies by 5,280 and divides by 3,600)"),
                 (fps * 3600, "changes seconds to hours but never changes feet to miles"),
                 (fps * 60 / 5280, "changes seconds to minutes but not to hours")]
    else:
        steps = [same_pair + ".",
                 f"Miles per hour: {m(f'{_ratio_raw(k)} \\times {km} = {mph}')}."]
        tip = None
        wrong = [(fps - (kf - km), f"subtracts the difference {m(f'{kf} - {km} = {kf - km}')} instead of "
                                   f"multiplying by {m(_ratio_raw(k))}")]
        inv = Q(km) / k
        if inv.is_integer and inv != mph:
            wrong.append((inv, f"divides by {m(_ratio_raw(k))} instead of multiplying"))
    return Problem(
        stem=stem, answer=Q(mph), fmt=_MPH, section="AR", wrong=wrong, steps=steps, tip=tip,
        verify=lambda v: v * 5280 == fps * 3600,
        near=lambda g: [Q(mph + d) for d in g.sample([-15, -10, -5, 5, 10, 15, 20], 6) if mph + d > 0],
    )


# --------------------------------------------------------------------------
# 11. clock time of arrival (L2, L3)
# --------------------------------------------------------------------------

_TRIPS = [
    # (stem start, speed choices, military)
    ("{B} leaves home at {t0} and drives {d} miles at an average speed of {r} miles per hour.", [40, 48, 50, 60, 64, 70], False),
    ("A convoy leaves the motor pool at {t0} and travels {d} miles to a training area at {r} miles per hour.",
     [30, 40, 45, 48, 50], True),
    ("A charter bus carrying new recruits leaves the processing station at {t0} and travels {d} miles to the "
     "training base at {r} miles per hour.", [50, 55, 60, 65], True),
    ("A train leaves the station at {t0} and travels {d} miles at {r} miles per hour.", [48, 50, 60, 64, 80], False),
    ("A tour bus leaves the hotel at {t0} and travels {d} miles to a national park at {r} miles per hour.",
     [40, 45, 48, 50, 60], False),
    ("{B} leaves for the airport at {t0} and drives {d} miles at an average speed of {r} miles per hour.",
     [40, 45, 48, 50, 60, 64], False),
]


_TRIPS3 = [
    # two legs and a stop; the destination is named only at the end of the trip
    ("{B} leaves home at {t0} and drives {d1} miles at {r1} miles per hour. {He} stops for {stop} minutes to eat "
     "lunch, then drives another {d2} miles at {r2} miles per hour to {his} cousin's house. At what time does "
     "{he} arrive at {his} cousin's house?", [40, 48, 50, 60, 64], False),
    ("A convoy leaves the motor pool at {t0} and travels {d1} miles at {r1} miles per hour. It halts for {stop} "
     "minutes to refuel, then travels another {d2} miles at {r2} miles per hour to the training area. At what "
     "time does the convoy reach the training area?", [30, 40, 45, 48, 50], True),
    ("A charter bus carrying new recruits leaves the processing station at {t0} and travels {d1} miles at {r1} "
     "miles per hour. It makes a {stop}-minute rest stop, then travels another {d2} miles at {r2} miles per "
     "hour to the training base. At what time does it arrive at the base?", [50, 55, 60, 65], True),
    ("A train leaves the first station at {t0} and travels {d1} miles at {r1} miles per hour. It waits {stop} "
     "minutes at a second station, then travels another {d2} miles at {r2} miles per hour to the end of the "
     "line. At what time does it reach the end of the line?", [48, 50, 60, 64, 80], False),
    ("A tour bus leaves the hotel at {t0} and travels {d1} miles at {r1} miles per hour. It makes a {stop}-minute "
     "stop, then travels another {d2} miles at {r2} miles per hour to a national park. At what time does it "
     "arrive at the park?", [40, 45, 48, 50, 60], False),
    ("{B} leaves for the airport at {t0} and drives {d1} miles on the highway at {r1} miles per hour. {He} "
     "stops {stop} minutes for gas, then drives the last {d2} miles to the airport at {r2} miles per hour. At "
     "what time does {he} reach the airport?", [40, 45, 48, 50, 60, 64], False),
]


def _clock_min(s):
    """'11:05 a.m.' -> minutes after midnight (sort key for clock-time choices)."""
    hm, suf = s.split()
    h, mm = map(int, hm.split(":"))
    return (h % 12 + (12 if suf == "p.m." else 0)) * 60 + mm


@template("AR")
@_fill
def arrival_time(rng, lvl, part=None):
    st, speeds, mil = _pick(rng, _TRIPS, part)
    B = person(rng)
    r = rng.choice(speeds)
    start = rng.choice(range(5 * 60, 11 * 60 + 1, 15)) + rng.choice([0, 0, 5, 10])
    if lvl == 2:
        frac_h = rng.choice([R(1, 4), R(1, 2), R(1, 5), R(2, 5), R(3, 4), R(1, 3)])
        th = rng.choice([1, 2, 3, 4]) + frac_h
        d = r * th
        need(d.is_integer and d >= 20)
        mins = int(th * 60)
        end = start + mins
        stem = st.format(B=B, t0=_clock(start), d=int_raw(d), r=r) + " At what time does it arrive?"
        stem = stem.replace("At what time does it arrive?", f"At what time does {B.he} arrive?" if "{B}" in st else
                            "At what time does it arrive?")
        whole = int(th)
        wrong = [(_clock(start + whole * 60), "leaves out the part of an hour")]
        misread = int(frac_h * 100)                 # 2.25 h read as 2 h 25 min
        if misread < 60 and misread != int(frac_h * 60):
            shown = dec_raw(th) if (th * 100).is_integer else f"{whole}.{misread:02d}"
            wrong.append((_clock(start + whole * 60 + misread),
                          f"reads {m(shown)} hours as {whole} hour{'s' if whole > 1 else ''} {misread} minutes"))
        fill = [60, -30, 30, -60, -15, 15, 45, -45]
        rng.shuffle(fill)
        wrong += [(_clock(end + f), None) for f in fill]
        wrong = [w for w in wrong if w[0] != _clock(end)]
        return Problem(
            stem=stem, answer=_clock(end), fmt=text, section="AR", wrong=wrong, order=_clock_min,
            steps=[f"Travel time: {m(f'{int_raw(d)} \\div {r} = {mixed_raw(th)}')} hours.",
                   f"Change the fraction of an hour to minutes: {m(f'{frac_raw(frac_h)} \\times 60 = {int(frac_h * 60)}')} "
                   f"minutes, so the trip takes {_hm(th)}.",
                   f"Add to the start time: {_clock(start)} plus {_hm(th)} is {_clock(end)}"],
            check=_clock(start + (Fraction(int(d), r) * 60)),
        )
    # level 3: two legs with a rest stop
    st3, speeds3, mil3 = _pick(rng, _TRIPS3, part)
    r1 = rng.choice(speeds3)
    r2 = rng.choice([v for v in speeds3 if v != r1])
    t1 = rng.choice([1, 2, R(3, 2), R(5, 2), 3])
    t2 = rng.choice([R(1, 2), 1, R(3, 2), R(3, 4), R(5, 4)])
    d1, d2 = r1 * t1, r2 * t2
    need(Q(d1).is_integer and Q(d2).is_integer)
    stop = rng.choice([15, 20, 30, 45])
    total = int((t1 + t2) * 60) + stop
    end = start + total
    stem = st3.format(B=B, He=B.He, he=B.he, his=B.his, t0=_clock(start), d1=int_raw(d1), r1=r1,
                      d2=int_raw(d2), r2=r2, stop=stop)
    wrong = [(_clock(end - stop), f"forgets the {stop}-minute stop"),
             ]
    one_speed = Q(d1 + d2) / r1 * 60          # minutes if the first speed is used for both legs
    if one_speed.is_integer and one_speed != total - stop:
        wrong.append((_clock(start + int(one_speed) + stop), "uses the first speed for the whole trip"))
    fill = [60, -30, 15, -60, 30, -15, 45]
    rng.shuffle(fill)
    wrong += [(_clock(end + f), None) for f in fill]
    wrong = [w for w in wrong if w[0] != _clock(end)]
    return Problem(
        stem=stem, answer=_clock(end), fmt=text, section="AR", wrong=wrong, order=_clock_min,
        steps=[f"First part: {m(f'{int_raw(d1)} \\div {r1} = {_d(t1)}')} {_hw(t1)}"
               + ("" if Q(t1).is_integer else f" ({_hm(t1)})")
               + f". Second part: {m(f'{int_raw(d2)} \\div {r2} = {_d(t2)}')} {_hw(t2)}"
               + ("" if Q(t2).is_integer else f" ({_hm(t2)})") + ".",
               f"Total time: {_hm(t1)} {m('+')} {_hm(t2)} {m('+')} {stop} minutes {m('=')} {_hm(R(total, 60))}.",
               f"Add to the start time: {_clock(start)} plus {_hm(R(total, 60))} is {_clock(end)}"],
        check=_clock(start + int(Fraction(int(d1), r1) * 60 + Fraction(int(d2), r2) * 60) + stop),
    )


# --------------------------------------------------------------------------

_DRT = _variants(drt_basic, 4)
_MH1, _MH2, _MH3 = _variants(minutes_hours, 3)
_FU = _variants(fuel, 3)
_WR = _variants(work_rate, 3)
_TM = _variants(two_movers, 3)
_PS = _variants(pace_speed, 3)
_TL = _variants(two_leg, 2)
_AT = _variants(arrival_time, 2)
_RT = _variants(round_trip, 3)
_CU = _variants(catch_up, 3)
_FPSV = _variants(fps_mph, 2)

PLAN = [
    # level 1 (12)
    *[(v, 1, 1) for v in _DRT],
    *[(v, 1, 1) for v in _variants(minutes_hours, 2)],
    *[(v, 1, 1) for v in _FU],
    *[(v, 1, 1) for v in _WR],
    # level 2 (16)
    (_MH1, 2, 1), (_MH2, 2, 1), (_MH3, 2, 1),
    *[(v, 2, 1) for v in _TM],
    *[(v, 2, 1) for v in _FU[:2]],
    *[(v, 2, 1) for v in _PS],
    *[(v, 2, 1) for v in _TL],
    *[(v, 2, 1) for v in _AT],
    (work_rate, 2, 1),
    # level 3 (12)
    *[(v, 3, 1) for v in _RT],
    *[(v, 3, 1) for v in _CU],
    *[(v, 3, 1) for v in _FPSV],
    *[(v, 3, 1) for v in _TL],
    (fuel, 3, 1),
    (arrival_time, 3, 1),
]
