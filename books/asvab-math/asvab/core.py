"""Core of the ASVAB math workbook generator.

Every problem is produced by a *template*: a function ``template(rng, lvl)``
that returns a :class:`Problem`.  The template computes the answer with sympy
(exact rationals, never floats), supplies wrong answers that come from real,
named mistakes, writes the step-by-step solution, and gives an independent
``check`` (the same answer reached by a different route) and/or a ``verify``
predicate (e.g. substitute the answer back into the equation).

:func:`finalize` turns a Problem into a 4-choice question (A-D), validating
everything on the way; any failure raises :class:`Reject` so the caller can
draw new numbers.
"""
from __future__ import annotations

import itertools
import random
import re
from dataclasses import dataclass, field
from typing import Any, Callable

import sympy as sp

R = sp.Rational
x, y, z, a, b, n = sp.symbols("x y z a b n")


class Reject(Exception):
    """Raised when generated numbers are unusable (ugly, ambiguous, ...)."""


# --------------------------------------------------------------------------
# exact-number helpers
# --------------------------------------------------------------------------

def Q(v) -> sp.Expr:
    """Exact sympy number. Floats are forbidden: they hide rounding errors."""
    if isinstance(v, float):
        raise TypeError(f"float {v!r} used; build exact values with R(p, q)")
    return sp.sympify(v)


def is_int(v) -> bool:
    v = Q(v)
    return bool(v.is_number and v.is_integer)


def need(cond, msg="numbers rejected"):
    """Template guard: ``need(answer > 0)`` -> retry with new numbers if false."""
    if not cond:
        raise Reject(msg)


def _terminating(v: sp.Rational, max_places: int) -> int:
    """Number of decimal places of a terminating decimal, else Reject."""
    q = v.q
    for p in (2, 5):
        while q % p == 0:
            q //= p
    if q != 1:
        raise Reject(f"{v} is not a terminating decimal")
    places = 0
    w = abs(v)
    while not (w * 10**places).is_integer:
        places += 1
        if places > max_places:
            raise Reject(f"{v} needs more than {max_places} decimal places")
    return places


def _group(int_str: str) -> str:
    """'1234567' -> '1{,}234{,}567' (safe in text and math mode)."""
    s = int_str
    if len(s) <= 3:
        return s
    parts = []
    while s:
        parts.append(s[-3:])
        s = s[:-3]
    return "{,}".join(reversed(parts))


def dec_raw(v, places: int | None = None, max_places: int = 4) -> str:
    """Exact decimal string of a rational (raw LaTeX, no $)."""
    v = Q(v)
    if not v.is_rational:
        raise Reject(f"{v} is not rational")
    v = sp.Rational(v)
    p = _terminating(v, max_places) if places is None else places
    if places is not None and not (v * 10**places).is_integer:
        raise Reject(f"{v} does not fit {places} places")
    sign = "-" if v < 0 else ""
    w = abs(v)
    scaled = int(w * 10**p)
    ip, fp = divmod(scaled, 10**p)
    s = _group(str(ip))
    if p:
        s += "." + str(fp).rjust(p, "0")
    return sign + s


def int_raw(v) -> str:
    v = Q(v)
    if not is_int(v):
        raise Reject(f"{v} is not an integer")
    v = int(v)
    return ("-" if v < 0 else "") + _group(str(abs(v)))


def frac_raw(v) -> str:
    """Rational as LaTeX: 3, -\\frac{3}{4}."""
    v = Q(v)
    if not v.is_rational:
        raise Reject(f"{v} is not rational")
    v = sp.Rational(v)
    if v.q == 1:
        return int_raw(v)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{_group(str(abs(v.p)))}}}{{{v.q}}}"


def mixed_raw(v) -> str:
    """Rational as a mixed number: 2\\frac{1}{3}; proper fractions unchanged."""
    v = sp.Rational(Q(v))
    if v.q == 1 or abs(v) < 1:
        return frac_raw(v)
    sign = "-" if v < 0 else ""
    w = abs(v)
    whole = w.p // w.q
    rest = w - whole
    return rf"{sign}{_group(str(whole))}\frac{{{rest.p}}}{{{rest.q}}}"


def m(s) -> str:
    """Wrap raw LaTeX in inline math."""
    return f"${s}$"


def F(p, q) -> str:
    """Raw \\frac{p}{q} with no simplification (for showing work)."""
    return rf"\frac{{{p}}}{{{q}}}"


def tx(v) -> str:
    """Raw LaTeX for any exact value/expression (rationals as fractions)."""
    v = Q(v)
    if v.is_number and v.is_rational:
        return frac_raw(v)
    return latex(v)


def latex(e) -> str:
    s = sp.latex(Q(e))
    # sympy writes "5 x"; tighten coefficients so it reads like a textbook
    import re
    s = re.sub(r"(\d) (?=[a-z\\(])", r"\1", s)
    s = re.sub(r"\\left\(", "(", s)
    s = re.sub(r"\\right\)", ")", s)
    return s


# --------------------------------------------------------------------------
# answer formatters: value -> LaTeX shown as a choice (text mode)
# Each may define .group(values) to format all four choices consistently.
# --------------------------------------------------------------------------

def num(v) -> str:
    return m(int_raw(v))


def dec(v) -> str:
    return m(dec_raw(v))


def frac(v) -> str:
    return m(frac_raw(v))


def mixed(v) -> str:
    return m(mixed_raw(v))


def pct(v) -> str:
    return m(dec_raw(v) + r"\%")


def expr(v) -> str:
    V = Q(v)
    if V.is_number and V.is_integer:
        return m(int_raw(V))
    return m(latex(V))


def money(v) -> str:
    v = Q(v)
    return _money(v, cents=not is_int(v))


def _money(v, cents: bool) -> str:
    v = Q(v)
    sign = "-" if v < 0 else ""
    s = dec_raw(abs(v), places=2) if cents else int_raw(abs(v))
    return rf"{sign}\${s}"


def _money_group(values):
    cents = any(not is_int(v) for v in values)
    return [_money(v, cents) for v in values]


money.group = _money_group


def dec_group(values):
    """Decimals with a common number of places (0.5 vs 0.25 -> 0.50, 0.25)."""
    places = max(_terminating(sp.Rational(Q(v)), 4) for v in values)
    return [m(dec_raw(v, places=places)) for v in values]


def money_cents(v) -> str:
    """Always two decimals: $12.00."""
    return _money(v, True)


def unit(fmt: Callable, singular: str, plural: str | None = None, space=True):
    """Formatter with a unit: unit(num, 'mile') -> '$12$ miles'."""
    plural = plural or singular + "s"

    def f(v):
        word = singular if Q(v) == 1 else plural
        return f"{fmt(v)}{'~' if space else ''}{word}"

    if hasattr(fmt, "group"):
        def g(values):
            return [f"{s}{'~' if space else ''}{singular if Q(v) == 1 else plural}"
                    for s, v in zip(fmt.group(values), values)]
        f.group = g
    return f


def sq_unit(fmt: Callable, u: str, power=2):
    """'$48$ sq ft' style: unit(num, 'ft') -> $48\\text{ ft}^2$."""
    def f(v):
        inner = fmt(v)[1:-1]
        return m(rf"{inner}\text{{ {u}}}^{power}")
    return f


def text(v) -> str:
    """For answers that are already LaTeX/text strings."""
    return str(v)


# --------------------------------------------------------------------------
# the Problem object
# --------------------------------------------------------------------------

@dataclass
class Problem:
    stem: str                          # LaTeX text of the question
    answer: Any                        # exact value (sympy) or string
    steps: list[str]                   # solution, one LaTeX paragraph per step
    wrong: list = field(default_factory=list)
    # each wrong item: (value, why) or (value, why, tex) — "why" completes the
    # sentence "Choice (B) ..." e.g. "is the discount, not the sale price."
    fmt: Callable = num
    check: Any = None                  # same answer by an independent route
    verify: Callable | None = None     # predicate on the answer
    figure: str | None = None          # TikZ code (no tikzpicture wrapper)
    tip: str | None = None             # optional shortcut / strategy note
    section: str = "MK"                # "AR" (word problems) or "MK"
    near: Callable | None = None       # rng -> plausible filler value
    sort: bool | None = None           # sort numeric choices ascending (default yes)
    neg_ok: bool = False               # allow negative distractors for a positive answer

    # filled in by finalize()
    choices: list = field(default_factory=list)   # [(tex, why|None)]
    key: int = -1                                   # index of correct choice
    level: int = 1
    template: str = ""
    chapter: int = 0


def same(u, v) -> bool:
    if isinstance(u, str) or isinstance(v, str):
        return str(u) == str(v)
    if isinstance(u, (tuple, list)) or isinstance(v, (tuple, list)):
        if not (isinstance(u, (tuple, list)) and isinstance(v, (tuple, list))):
            return False
        return len(u) == len(v) and all(same(p, q) for p, q in zip(u, v))
    try:
        U, V = sp.sympify(u), sp.sympify(v)
        if isinstance(U, sp.core.relational.Relational) or isinstance(V, sp.core.relational.Relational):
            return U == V
        if U.is_Rational and V.is_Rational:
            return U == V
        d = U - V
        if d.is_number:
            # fast numeric screen; exact simplify only when it is (nearly) zero
            if abs(sp.N(d, 40)) > sp.Float(10) ** -25:
                return False
            return sp.simplify(d) == 0
        syms = sorted(d.free_symbols, key=str)
        for pt in (R(3, 7), R(-5, 11), R(13, 3)):
            if d.subs({s_: pt + i for i, s_ in enumerate(syms)}) != 0:
                return False
        return sp.simplify(d) == 0
    except Exception:  # pragma: no cover - exotic types
        return u == v


def _is_real_num(v) -> bool:
    if isinstance(v, (str, tuple, list)):
        return False
    try:
        V = sp.sympify(v)
    except Exception:
        return False
    return bool(V.is_number and V.is_real)


def _fmt_all(fmt, values):
    if hasattr(fmt, "group"):
        return fmt.group(values)
    return [fmt(v) for v in values]


def _nice_step(v) -> sp.Rational:
    """A 'round' step size comparable to |v| for filler distractors."""
    v = abs(Q(v))
    if v == 0:
        return R(1)
    for s in (R(1, 100), R(1, 20), R(1, 10), R(1, 4), R(1, 2), 1, 2, 5, 10, 20, 25,
              50, 100, 200, 250, 500, 1000, 5000, 10000):
        if v <= 12 * s:
            return R(s)
    return R(10) ** (len(str(int(v))) - 2)


def _default_near(answer, rng: random.Random):
    """Plausible numbers near the answer, same 'shape' (int / sign / denominator)."""
    A = Q(answer)
    out = []
    if A.is_rational and not A.is_integer:
        Aq = sp.Rational(A)
        d = Aq.q
        for k in (1, 2, 3, -1, -2, -3):
            out.append(Aq + R(k, d))
        out += [1 / Aq if Aq != 0 else Aq + 1, Aq * 2, Aq / 2]
    else:
        st = _nice_step(A)
        for k in (1, 2, 3, 4, -1, -2, -3, -4):
            out.append(A + k * st)
        out += [A * 2, A / 2]
    if A > 0:
        out = [v for v in out if Q(v) > 0]
    rng.shuffle(out)
    return out


_ARTICLE = re.compile(r"(?<![\w\\])([Aa]) ((?:\\\$|\$)*)(\d[\d{},]*)")


def _an_number(digits: str) -> bool:
    """True if the number is read with a vowel sound: 8.., 11, 18, 11,000, 18,500."""
    d = digits.replace("{,}", ",").rstrip(",")
    if d.startswith("8"):
        return True
    head = d.split(",")[0]
    return head in ("11", "18")


def fix_articles(text: str) -> str:
    """'a 11-foot board' -> 'an 11-foot board', 'a $8 fee' -> 'an $8 fee'."""
    def sub(mm):
        art, pre, dig = mm.groups()
        if _an_number(dig):
            art = "An" if art == "A" else "an"
        return f"{art} {pre}{dig}"
    return _ARTICLE.sub(sub, text)


def finalize(p: Problem, rng: random.Random, target: int) -> Problem:
    """Validate a raw Problem and build its 4 answer choices.

    ``target`` is the preferred 0-based position of the correct answer (used
    to balance A/B/C/D across a chapter).  Raises Reject on any defect.
    """
    if not p.stem.strip() or not p.steps:
        raise ValueError("problem without stem or steps")
    for v in [p.answer, p.check] + [w[0] for w in p.wrong]:
        if isinstance(v, float):
            raise TypeError("float in problem values")
    if p.check is None and p.verify is None:
        raise ValueError("problem has neither check nor verify")
    if p.check is not None and not same(p.answer, p.check):
        raise AssertionError(f"answer {p.answer} != independent check {p.check}\n{p.stem}")
    if p.verify is not None and not p.verify(p.answer):
        raise AssertionError(f"answer {p.answer} fails verification\n{p.stem}")

    ans_tex = _fmt_all(p.fmt, [p.answer])[0]

    # candidate distractors: (value, why, tex|None)
    cands = []
    for w in p.wrong:
        val, why = w[0], w[1]
        t = w[2] if len(w) > 2 else None
        cands.append((val, why, t))
    near = p.near(rng) if p.near else (_default_near(p.answer, rng) if _is_real_num(p.answer) else [])
    for v in near:
        cands.append((v, None, None))

    pos_answer = _is_real_num(p.answer) and Q(p.answer) >= 0

    def ok(val, t, chosen):
        if same(val, p.answer):
            return False
        if pos_answer and not p.neg_ok and _is_real_num(val) and Q(val) < 0:
            return False
        try:
            tt = t if t is not None else _fmt_all(p.fmt, [val])[0]
        except Reject:
            return False
        if tt == ans_tex:
            return False
        for cv, _, ct in chosen:
            if ct == tt or same(cv, val):
                return False
        return True

    pool = []
    for val, why, t in cands:
        if ok(val, t, pool):
            tt = t if t is not None else _fmt_all(p.fmt, [val])[0]
            pool.append((val, why, tt))
    if len(pool) < 3:
        raise Reject("fewer than 3 distinct distractors")

    numeric = _is_real_num(p.answer) and all(_is_real_num(v) for v, _, _ in pool)
    do_sort = numeric if p.sort is None else (p.sort and numeric)

    explained = [c for c in pool if c[1]]
    plain = [c for c in pool if not c[1]]
    ordered = explained + plain
    ANS = (p.answer, None, ans_tex, True)

    if do_sort:
        A = Q(p.answer)
        best = None
        # keep at least one explained trap, then hit the target slot (to
        # balance A-D), then prefer still more explained traps
        for combo in itertools.combinations(ordered[:10], 3):
            sc = sum(1 for c in combo if c[1])
            below = sum(1 for c in combo if Q(c[0]) < A)
            key = (min(sc, 1), below == target, sc)
            if best is None or key > best[0]:
                best = (key, combo)
        vals = [c + (False,) for c in best[1]] + [ANS]
        vals.sort(key=lambda c: Q(c[0]))
    else:
        chosen = [c + (False,) for c in ordered[:3]]
        rng.shuffle(chosen)
        vals = chosen[:target] + [ANS] + chosen[target:]

    # consistent formatting across the four choices (money cents, decimals)
    texs = [c[2] for c in vals]
    if hasattr(p.fmt, "group") and all(len(w) < 3 or w[2] is None for w in p.wrong):
        texs = p.fmt.group([c[0] for c in vals])
    if len(set(texs)) != 4:
        raise Reject("choices collide after formatting")
    p.choices = [(t, None if c[3] else c[1]) for t, c in zip(texs, vals)]
    p.key = [i for i, c in enumerate(vals) if c[3]][0]

    p.stem = fix_articles(p.stem)
    p.steps = [fix_articles(t) for t in p.steps]
    p.tip = fix_articles(p.tip) if p.tip else p.tip
    blob = " ".join([p.stem, *p.steps, *(t for t, _ in p.choices)])
    bad = re.search(r"(?<![A-Za-z])(nan|zoo|None)(?![A-Za-z])|oo\}|\\infty", blob)
    if bad:
        raise Reject(f"bad token {bad.group(0)!r} in text")
    return p


# --------------------------------------------------------------------------
# word-problem flavour
# --------------------------------------------------------------------------

PEOPLE = [
    ("Maria", "she", "her", "her"), ("James", "he", "him", "his"),
    ("Aisha", "she", "her", "her"), ("Carlos", "he", "him", "his"),
    ("Mei", "she", "her", "her"), ("Tyrone", "he", "him", "his"),
    ("Priya", "she", "her", "her"), ("Ethan", "he", "him", "his"),
    ("Sofia", "she", "her", "her"), ("Malik", "he", "him", "his"),
    ("Hannah", "she", "her", "her"), ("Diego", "he", "him", "his"),
    ("Grace", "she", "her", "her"), ("Kevin", "he", "him", "his"),
    ("Leila", "she", "her", "her"), ("Marcus", "he", "him", "his"),
    ("Nora", "she", "her", "her"), ("Andre", "he", "him", "his"),
    ("Rosa", "she", "her", "her"), ("Jamal", "he", "him", "his"),
    ("Emily", "she", "her", "her"), ("Luis", "he", "him", "his"),
    ("Keisha", "she", "her", "her"), ("Ryan", "he", "him", "his"),
    ("Ana", "she", "her", "her"), ("Omar", "he", "him", "his"),
    ("Tasha", "she", "her", "her"), ("Brandon", "he", "him", "his"),
    ("Yuki", "she", "her", "her"), ("Derek", "he", "him", "his"),
    ("Jasmine", "she", "her", "her"), ("Victor", "he", "him", "his"),
]

RANKS = ["Private", "Specialist", "Corporal", "Sergeant", "Airman", "Seaman",
         "Lance Corporal", "Petty Officer"]


@dataclass
class Person:
    name: str
    he: str
    him: str
    his: str

    @property
    def He(self):
        return self.he.capitalize()

    @property
    def His(self):
        return self.his.capitalize()

    def __str__(self):
        return self.name


def person(rng: random.Random, exclude=()) -> Person:
    opts = [p for p in PEOPLE if p[0] not in {str(e) for e in exclude}]
    return Person(*rng.choice(opts))


def people(rng: random.Random, k: int) -> list[Person]:
    return [Person(*p) for p in rng.sample(PEOPLE, k)]


def soldier(rng: random.Random) -> str:
    """'Sergeant Ruiz' style name for military-flavoured problems."""
    last = rng.choice(["Ruiz", "Chen", "Walker", "Okafor", "Patel", "Novak",
                       "Brooks", "Kim", "Santos", "Reyes", "Jensen", "Haddad",
                       "Lopez", "Nguyen", "Carter", "Murphy"])
    return f"{rng.choice(RANKS)} {last}"


def choose(rng: random.Random, *options):
    """Pick one of several phrasings: choose(rng, 'a', 'b', 'c')."""
    return rng.choice(options)


def template(section: str = "MK"):
    """Mark a function as a problem template for the 'AR' or 'MK' subtest."""
    if section not in ("AR", "MK"):
        raise ValueError(section)

    def deco(fn):
        fn.section = section
        return fn
    return deco
