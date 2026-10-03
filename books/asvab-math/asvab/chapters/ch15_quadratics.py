"""Chapter 15 - Factoring & Quadratic Equations."""
import math
from fractions import Fraction

import sympy as sp

from ..core import (R, Q, Problem, need, num, frac, m, F, tx, frac_raw, int_raw,
                    text, choose, template, x, y)

NUM = 15
TITLE = r"Factoring \& Quadratic Equations"
PART = 2

INTRO = r"""
\emph{Factoring} is multiplication in reverse: it rewrites a sum as a
product. It is also the fastest way to solve a \emph{quadratic equation}
(an equation with an $x^2$ term) without a calculator.

\begin{concept}{Factoring patterns}
\begin{itemize}
\item \textbf{Greatest common factor (GCF) first:} $6x^2 + 9x = 3x(2x + 3)$.
\item \textbf{Trinomials} $x^2 + bx + c$: find two numbers that
  \emph{multiply} to $c$ and \emph{add} to $b$. For $x^2 + 7x + 12$: $3 \cdot 4 = 12$
  and $3 + 4 = 7$, so $(x + 3)(x + 4)$.
\item \textbf{Difference of squares:} $a^2 - b^2 = (a + b)(a - b)$, so
  $x^2 - 49 = (x + 7)(x - 7)$.
\item \textbf{Perfect squares:} $x^2 + 10x + 25 = (x + 5)^2$.
\item \textbf{Leading coefficient not 1:} try factor pairs and check the
  middle term with FOIL: $2x^2 + 7x + 3 = (2x + 1)(x + 3)$.
\end{itemize}
\end{concept}

\begin{concept}{Solving quadratic equations}
\begin{enumerate}
\item Move everything to one side so the other side is $0$.
\item Factor, then set \emph{each} factor equal to $0$ (a product is $0$
  only when one of its factors is $0$).
\end{enumerate}
If there is no $x$-term, take square roots and keep both signs:
$x^2 = 49$ gives $x = 7$ or $x = -7$. When factoring is hard, use the
quadratic formula for $ax^2 + bx + c = 0$:
\[ x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} \]
\end{concept}

\begin{concept}{Function notation}
$f(x) = x^2 - 3x + 2$ is a rule; $f(-2)$ means ``replace every $x$ with
$(-2)$'': $f(-2) = (-2)^2 - 3(-2) + 2 = 4 + 6 + 2 = 12$.
\end{concept}

\begin{example}{Worked example}
Solve $x^2 - 5x = 14$.

\textbf{Solution.} Subtract $14$: $x^2 - 5x - 14 = 0$. Two numbers that
multiply to $-14$ and add to $-5$ are $-7$ and $2$, so $(x - 7)(x + 2) = 0$.
Then $x - 7 = 0$ or $x + 2 = 0$: $x = 7$ or $x = -2$.
Check: $49 - 35 = 14$ and $4 + 10 = 14$. \checkmark
\end{example}

\begin{tip}
To find the pair for $x^2 + bx + c$, list the factor pairs of $c$. If $c$
is positive, both numbers have the sign of $b$; if $c$ is negative, the
signs differ and the larger number takes the sign of $b$.
\end{tip}

\begin{trap}
\begin{itemize}
\item $(x + 3)(x - 5) = 0$ gives $x = -3$ or $x = 5$: use the
  \emph{opposites} of the numbers in the factors.
\item Forgetting the negative root of $x^2 = 49$.
\item $x(x - 3) = 10$ does \emph{not} mean $x = 10$ or $x - 3 = 10$; you need
  $0$ on one side first.
\item $(-3)^2 = 9$, but $-3^2 = -9$: keep the parentheses when you substitute.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# private helpers
# --------------------------------------------------------------------------

def _bin(p, q, v="x"):
    """p v + q as LaTeX: _bin(2, -3) -> '2x - 3'."""
    lead = v if p == 1 else ("-" + v if p == -1 else f"{p}{v}")
    if q == 0:
        return lead
    q = Q(q)
    return lead + (f" + {tx(q)}" if q > 0 else f" - {tx(-q)}")


def _vp(k, v="x"):
    return "" if k == 0 else (v if k == 1 else f"{v}^{{{k}}}")


def _fact_tex(factors, g=1, gx=0, v="x"):
    """g * v^gx * prod(p v + q), factors in a fixed order (equal factors squared)."""
    fs = sorted(factors, key=lambda f: (-f[0], f[1]))
    parts, i = [], 0
    while i < len(fs):
        j = i
        while j < len(fs) and fs[j] == fs[i]:
            j += 1
        parts.append(f"({_bin(*fs[i], v)})" + (f"^{{{j - i}}}" if j - i > 1 else ""))
        i = j
    front = "-" if g == -1 else ("" if g == 1 else str(g))
    return front + _vp(gx, v) + "".join(parts)


def _fact_expr(factors, g=1, gx=0, v=x):
    e = Q(g) * v**gx
    for p, q in factors:
        e *= (p * v + q)
    return e


def _poly_tex(e, v=x, vname="x"):
    """Polynomial in v, descending order."""
    P = sp.Poly(sp.expand(e), v)
    out = ""
    for (k,), c in sorted(P.terms(), key=lambda t: -t[0][0]):
        if c == 0:
            continue
        body = _vp(k, vname)
        mag = abs(c)
        body = body if (body and mag == 1) else tx(mag) + body
        out = (("-" if c < 0 else "") + body) if not out else out + (" - " if c < 0 else " + ") + body
    return out or "0"


def _sol_tex(vals, v="x"):
    vals = sorted(set(Q(r) for r in vals))
    return " or ".join(f"${v} = {frac_raw(r)}$" for r in vals)


def _string_choices(ans_tex, ans_key, cands):
    """Keep distractors whose key (expanded polynomial / root set) differs
    from the answer's: no equivalent form can become a wrong choice."""
    out, seen = [], {ans_tex}
    for tex_, key, why in cands:
        if key == ans_key or tex_ in seen:
            continue
        seen.add(tex_)
        out.append((tex_, why))
    need(len(out) >= 3)
    return out


def _pairs(c):
    """Integer factor pairs (r, s) with r * s = c, r <= s."""
    out = []
    for r in range(-abs(c), abs(c) + 1):
        if r != 0 and c % r == 0 and r <= c // r:
            out.append((r, c // r))
    return out


def _roots_ok(coefs, roots):
    """Independent check: each root makes a x^2 + b x + c equal 0 (fractions)."""
    a, b, c = coefs
    for r in roots:
        r = Fraction(int(sp.numer(Q(r))), int(sp.denom(Q(r))))
        if a * r * r + b * r + c != 0:
            return False
    return True


def _plus(v):
    v = Q(v)
    return f" - {tx(-v)}" if v < 0 else f" + {tx(v)}"


# --------------------------------------------------------------------------
# templates
# --------------------------------------------------------------------------

@template("MK")
def factor_gcf(rng, lvl):
    if lvl >= 3:
        return _gcf_trinomial(rng)
    g = rng.randint(2, 9)
    gx = rng.choice([0, 1, 1, 2])
    p = rng.randint(1, 7)
    q = rng.choice([v for v in range(-9, 10) if v != 0])
    need(math.gcd(p, abs(q)) == 1 and (p, q) != (1, 1))
    orig = g * p * x**(gx + 1) + g * q * x**gx
    otex = _poly_tex(orig)
    if rng.random() < 0.35:
        # name the GCF itself
        t1, t2 = g * p * x**(gx + 1), g * q * x**gx
        ans = f"${g}{_vp(gx)}$"
        lcm = sp.ilcm(g * p, g * abs(q))
        cands = [(f"${g}{_vp(gx + 1)}$", None, "uses the higher power of $x$; the GCF takes the lower power"
                  if gx else "includes an $x$, but the second term has no $x$"),
                 (f"${lcm}{_vp(gx + 1)}$", None, "gives the least common multiple, not the greatest common factor"),
                 (f"${min(g * p, g * abs(q))}{_vp(gx)}$", None, "uses the smaller coefficient, which does not divide both terms")
                 if min(g * p, g * abs(q)) != g else (f"${g * 2}{_vp(gx)}$", None, None),
                 (f"${g}$" if gx else f"${g}x$", None, "is a common factor, but not the greatest" if gx else
                  "includes an $x$, but the second term has no $x$")]
        if g % 2 == 0 and g > 2:
            cands.append((f"${g // 2}{_vp(gx)}$", None, "is a common factor, but not the greatest"))
        cands = [(t, t, w) for t, _, w in cands]
        wrong = _string_choices(ans, ans, cands)
        steps = [f"Coefficients: the largest number that divides both {m(g * p)} and {m(abs(g * q))} is {m(g)}.",
                 (f"Variables: both terms contain {m(_vp(gx))}; use the \\emph{{lower}} power, {m(_vp(gx))}."
                  if gx else "Variables: the second term has no $x$, so the GCF has no $x$."),
                 f"So the GCF is {ans}. (Check: {m(f'{otex} = {g}{_vp(gx)}({_bin(p, q)})')}.)"]
        return Problem(stem=f"What is the greatest common factor of the terms of {m(otex)}?",
                       answer=ans, fmt=text, wrong=wrong, steps=steps,
                       verify=lambda s: s == ans and sp.gcd(sp.Poly(t1, x), sp.Poly(t2, x)).as_expr() == g * x**gx)
    ans_e = _fact_expr([(p, q)], g, gx)
    ans = f"${_fact_tex([(p, q)], g, gx)}$"
    key = sp.expand(ans_e)

    def c_(factors, gg, gxx, why, inner=None):
        if inner is not None:          # g x^gx (inner polynomial)
            e = gg * x**gxx * inner
            t = f"${gg}{_vp(gxx)}({_poly_tex(inner)})$"
        else:
            e = _fact_expr(factors, gg, gxx)
            t = f"${_fact_tex(factors, gg, gxx)}$"
        return (t, sp.expand(e), why)

    cands = [c_([(p, g * q)], g, gx, f"divides only the first term by {m(f'{g}{_vp(gx)}')}"),
             c_([(p, -q)], g, gx, "changes the sign of the second term"),
             c_(None, g, gx, "divides the coefficients but not the powers of $x$",
                inner=p * x**(gx + 1) + q * x**gx) if gx else
             c_([(p, q)], g, 1, "takes out an $x$, but the second term has no $x$"),
             c_([(p, q)], g, 0, f"leaves the {m(_vp(gx))} out of the GCF") if gx else
             c_([(g * p, q)], 1, 0, "does not take the GCF out of the first term"),
             c_([(p, q)], g, gx + 1, "takes out too high a power of $x$")]
    steps = [f"Find the GCF of the terms: the numbers {m(g * p)} and {m(abs(g * q))} share {m(g)}"
             + (f", and both terms contain {m(_vp(gx))}" if gx else ", and the second term has no $x$")
             + f". The GCF is {m(f'{g}{_vp(gx)}')}.",
             f"Divide each term by the GCF: {m(F(_poly_tex(g * p * x**(gx + 1)), f'{g}{_vp(gx)}') + ' = ' + _poly_tex(p * x))} "
             f"and {m(F(_poly_tex(g * q * x**gx), f'{g}{_vp(gx)}') + ' = ' + tx(q))}.",
             f"So {m(f'{otex} = {_fact_tex([(p, q)], g, gx)}')}. Check by multiplying back. \\checkmark"]
    ok = sp.expand(ans_e - orig) == 0 and all(
        g * t**gx * (p * t + q) == g * p * t**(gx + 1) + g * q * t**gx for t in (-3, 2, 5))
    return Problem(stem=choose(rng, f"Factor completely: {m(otex)}", f"Which is the completely factored form of {m(otex)}?"),
                   answer=ans, fmt=text, wrong=_string_choices(ans, key, cands), steps=steps,
                   verify=lambda s: s == ans and ok)


def _gcf_trinomial(rng):
    g = rng.randint(2, 5)
    p, q = rng.sample([v for v in range(-7, 8) if v != 0], 2)
    need(p + q != 0)
    orig = sp.expand(g * (x + p) * (x + q))
    otex = _poly_tex(orig)
    ans = f"${_fact_tex([(1, p), (1, q)], g)}$"
    key = orig
    cands = [(f"${_fact_tex([(1, p), (1, q)])}$", sp.expand((x + p) * (x + q)), "leaves out the common factor"),
             (f"${_fact_tex([(1, -p), (1, -q)], g)}$", sp.expand(g * (x - p) * (x - q)), "has the signs of both numbers backwards")]
    for r, s in _pairs(p * q):
        if r + s != p + q:
            cands.append((f"${_fact_tex([(1, r), (1, s)], g)}$", sp.expand(g * (x + r) * (x + s)),
                          f"uses numbers that multiply to {m(p * q)} but add to {m(r + s)}, not {m(p + q)}"))
    cands.append((f"${_fact_tex([(1, g * p), (1, g * q)])}$", sp.expand((x + g * p) * (x + g * q)),
                  f"factors the original numbers without first dividing out {m(g)}"))
    steps = [f"First take out the GCF, {m(g)}: {m(f'{otex} = {g}({_poly_tex(orig / g)})')}.",
             f"Now factor {m(_poly_tex(orig / g))}: find two numbers that multiply to {m(p * q)} and add to "
             f"{m(p + q)}. They are {m(p)} and {m(q)}.",
             f"So {m(f'{otex} = {_fact_tex([(1, p), (1, q)], g)}')}."]
    ok = all(g * (t + p) * (t + q) == orig.subs(x, t) for t in (-4, 1, 3, 7))
    return Problem(stem=choose(rng, f"Factor completely: {m(otex)}", f"Which is the completely factored form of {m(otex)}?"),
                   answer=ans, fmt=text, wrong=_string_choices(ans, key, cands[:6]), steps=steps,
                   verify=lambda s: s == ans and ok)


@template("MK")
def factor_trinomial(rng, lvl):
    if lvl <= 1:
        p, q = rng.sample(range(1, 13), 2)
        if rng.random() < 0.4:
            p, q = -p, -q
    else:
        p = rng.randint(1, 12)
        q = -rng.randint(1, 12)
        need(p + q != 0)
        if rng.random() < 0.5:
            p, q = -p, -q
    b, c = p + q, p * q
    need(abs(c) <= 100)
    orig = x**2 + b * x + c
    otex = _poly_tex(orig)
    key = sp.expand(orig)
    pair_note = (f"Two numbers that multiply to {m(c)} and add to {m(b)} are {m(p)} and {m(q)}: "
                 f"{m(f'{p} \\cdot {_par(q)} = {c}')} and {m(f'{p} + {_par(q)} = {b}')}.")
    if rng.random() < 0.3:
        # which binomial is a factor?
        r = rng.choice([p, q])
        ans = f"${_bin(1, r)}$"
        consts = [(-r, "has the wrong sign"),
                  (c, f"uses the constant term {m(c)} itself"),
                  (b, f"uses the coefficient {m(b)} itself")]
        for rr, ss in _pairs(c):
            if rr + ss != b:
                consts.append((rr, f"comes from {m(rr)} and {m(ss)}, which multiply to {m(c)} but add to {m(rr + ss)}"))
        # x + k is a factor exactly when x = -k makes the trinomial 0; keep only true non-factors
        good = [(f"${_bin(1, k)}$", f"${_bin(1, k)}$", why) for k, why in consts
                if k != 0 and k * k - b * k + c != 0]
        steps = [pair_note, f"So {m(f'{otex} = {_fact_tex([(1, p), (1, q)])}')}.",
                 f"The factors are {m(_bin(1, p))} and {m(_bin(1, q))}; only {ans} is among the choices."]
        return Problem(stem=f"Which of the following is a factor of {m(otex)}?",
                       answer=ans, fmt=text, wrong=_string_choices(ans, ans, good), steps=steps,
                       verify=lambda s: s == ans and sp.rem(orig, x + r, x) == 0)
    ans = f"${_fact_tex([(1, p), (1, q)])}$"
    cands = [(f"${_fact_tex([(1, -p), (1, -q)])}$", sp.expand((x - p) * (x - q)),
              "has both signs backwards" if c > 0 else f"has the signs switched, which makes the middle term {m(_poly_tex(-b * x))}")]
    for rr, ss in _pairs(c):
        if rr + ss != b:
            cands.append((f"${_fact_tex([(1, rr), (1, ss)])}$", sp.expand((x + rr) * (x + ss)),
                          f"uses {m(rr)} and {m(ss)}, which multiply to {m(c)} but add to {m(rr + ss)}, not {m(b)}"))
    for r0 in (1, 2, -1):
        s0 = b - r0
        if r0 * s0 != c and s0 != 0:
            cands.append((f"${_fact_tex([(1, r0), (1, s0)])}$", sp.expand((x + r0) * (x + s0)),
                          f"uses {m(r0)} and {m(s0)}, which add to {m(b)} but multiply to {m(r0 * s0)}, not {m(c)}"))
            break
    rng.shuffle(cands)
    cands.sort(key=lambda t: 0 if "backwards" in t[2] or "switched" in t[2] else 1)
    steps = [pair_note,
             f"So {m(f'{otex} = {_fact_tex([(1, p), (1, q)])}')}.",
             f"Check with FOIL: {m(f'x^{{2}} {_plus(q)}x {_plus(p)}x {_plus(c)} = {otex}')}. \\checkmark"
             .replace("+ 1x", "+ x").replace("- 1x", "- x")]
    ok = all((t + p) * (t + q) == t * t + b * t + c for t in (-5, 0, 3, 8)) and \
        sp.expand(sp.factor(orig) - (x + p) * (x + q)) == 0
    return Problem(stem=choose(rng, f"Factor: {m(otex)}", f"Which is the factored form of {m(otex)}?",
                               f"Which expression is equal to {m(otex)}?"),
                   answer=ans, fmt=text, wrong=_string_choices(ans, key, cands), steps=steps,
                   verify=lambda s: s == ans and ok)


def _par(v):
    return f"({tx(v)})" if Q(v) < 0 else tx(v)


@template("MK")
def special_factor(rng, lvl):
    vname = rng.choice(["x", "x", "x", "n", "t", "m"]) if lvl <= 2 else "x"
    V = sp.Symbol(vname)
    if lvl <= 2:
        kind = rng.choice(["dsq", "dsq", "psq", "psq-"])
        a, g = 1, 1
        k = rng.randint(2, 15) if kind == "dsq" else rng.randint(1, 12)
    else:
        kind = rng.choice(["dsq", "psq", "psq-", "gdsq"])
        a = rng.randint(2, 5) if kind != "gdsq" else 1
        g = rng.randint(2, 5) if kind == "gdsq" else 1
        k = rng.randint(1, 9)
        need(math.gcd(a, k) == 1)
    if kind in ("dsq", "gdsq"):
        orig = g * ((a * V)**2 - k * k)
        ans_f, gg = [(a, k), (a, -k)], g
        cands_raw = [([(a, -k), (a, -k)], g, "is a perfect square, not a difference of squares"),
                     ([(a, k), (a, k)], g, "is a perfect square, not a difference of squares")]
        if a > 1:
            cands_raw.append(([(a * a, k), (a * a, -k)], g, f"does not take the square root of {m(a * a)}"))
        if g > 1:
            cands_raw.append(([(a, k), (a, -k)], 1, f"leaves out the common factor {m(g)}"))
            cands_raw.append(([(a, k * k), (a, -1)], g, f"uses {m(k * k)} and {m(-1)}, which do not cancel the middle term"))
        else:
            cands_raw.append(([(a, k * k), (a, -1)] if a == 1 else [(a, k), (1, -k)], 1,
                              f"uses {m(k * k)} and {m(-1)}, which multiply to {m(-k * k)} but do not add to 0"
                              if a == 1 else "does not split the square evenly"))
        steps = ([f"First take out the common factor {m(g)}: {m(f'{_poly_tex(orig, V, vname)} = {g}({_poly_tex(orig / g, V, vname)})')}."]
                 if g > 1 else [])
        base = f"{_vp(1, vname) if a == 1 else f'{a}{vname}'}"
        steps += [f"{m(_poly_tex(orig / g, V, vname))} is a difference of squares: {m(f'({base})^{{2}} - {k}^{{2}}')}.",
                  f"Use {m('A^2 - B^2 = (A + B)(A - B)')}: {m(f'{_poly_tex(orig, V, vname)} = {_fact_tex(ans_f, g, 0, vname)}')}."]
    else:
        s = 1 if kind == "psq" else -1
        orig = (a * V + s * k)**2
        ans_f, gg = [(a, s * k), (a, s * k)], 1
        cands_raw = [([(a, k), (a, -k)], 1, "is a difference of squares, which has no middle term"),
                     ([(a, -s * k), (a, -s * k)], 1, "gets the sign wrong; the middle term tells you the sign"),
                     ([(a, s * k * k), (a, s)], 1, f"uses {m(k * k)} and 1, which multiply correctly but give the wrong middle term")
                     if a == 1 else ([(a * a, s * k), (1, s * k)], 1, f"does not take the square root of {m(a * a)}")]
        if a > 1:
            cands_raw.append(([(a * a, s * k * k), (1, s)], 1, None))
        sg = "-" if s < 0 else ""
        steps = [f"The first and last terms are perfect squares: {m(f'{_poly_tex(a * a * V**2, V, vname)} = ({_bin(a, 0, vname)})^{{2}}')} "
                 f"and {m(f'{k * k} = {k}^{{2}}')}.",
                 f"The middle term is {m(f'{sg}2({_bin(a, 0, vname)})({k}) = {_poly_tex(2 * s * a * k * V, V, vname)}')}, "
                 f"so it is a perfect square: {m(f'{_poly_tex(orig, V, vname)} = ({_bin(a, s * k, vname)})^{{2}}')}."]
    key = sp.expand(orig)
    ans = f"${_fact_tex(ans_f, gg, 0, vname)}$"
    cands = [(f"${_fact_tex(fs, g_, 0, vname)}$", sp.expand(_fact_expr(fs, g_, 0, V)), why) for fs, g_, why in cands_raw]
    otex = _poly_tex(orig, V, vname)
    ok = sp.expand(_fact_expr(ans_f, gg, 0, V) - orig) == 0 and \
        all(_fact_expr(ans_f, gg, 0, V).subs(V, t) == orig.subs(V, t) for t in (-2, 3, 7))
    return Problem(stem=choose(rng, f"Factor completely: {m(otex)}", f"Which is the factored form of {m(otex)}?",
                               f"Which expression is equal to {m(otex)}?"),
                   answer=ans, fmt=text, wrong=_string_choices(ans, key, cands), steps=steps,
                   verify=lambda s_: s_ == ans and ok)


@template("MK")
def solve_factored(rng, lvl):
    r1, r2 = rng.sample([v for v in range(-9, 10) if v != 0], 2)
    need(r1 + r2 != 0)
    b, c = -(r1 + r2), r1 * r2
    coefs = (1, b, c)
    ans = _sol_tex([r1, r2])
    key = frozenset([r1, r2])
    cands = [(_sol_tex([-r1, -r2]), frozenset([-r1, -r2]),
              "uses the numbers in the factors instead of their opposites")]
    if lvl == 1:
        if rng.random() < 0.3:
            r1 = 0
            r2 = rng.choice([v for v in range(-12, 13) if v != 0])
            eq = f"x({_bin(1, -r2)}) = 0"
            ans, key = _sol_tex([0, r2]), frozenset([0, r2])
            cands = [(_sol_tex([r2]), frozenset([r2]), "forgets that the factor $x$ gives the solution $x = 0$"),
                     (_sol_tex([0, -r2]), frozenset([0, -r2]), "uses the number in the factor instead of its opposite"),
                     (_sol_tex([-r2]), frozenset([-r2]), None),
                     (_sol_tex([1, r2]), frozenset([1, r2]), "sets the factor $x$ equal to 1 instead of 0")]
            coefs = (1, -r2, 0)
            steps = [f"A product is 0 only if one of its factors is 0, so set each factor equal to 0.",
                     f"{m('x = 0')} or {m(f'{_bin(1, -r2)} = 0')}, which gives {m(f'x = {r2}')}.",
                     f"The solutions are {ans}."]
        else:
            eq = f"({_bin(1, -r1)})({_bin(1, -r2)}) = 0"
            cands += [(_sol_tex([r1]), frozenset([r1]), "forgets the second factor"),
                      (_sol_tex([-r1, r2]), frozenset([-r1, r2]), "gets the sign of one solution wrong"),
                      (_sol_tex([r1, -r2]), frozenset([r1, -r2]), "gets the sign of one solution wrong")]
            steps = [f"A product is 0 only if one of its factors is 0, so set each factor equal to 0.",
                     f"{m(f'{_bin(1, -r1)} = 0')} gives {m(f'x = {r1}')}; {m(f'{_bin(1, -r2)} = 0')} gives {m(f'x = {r2}')}.",
                     f"The solutions are {ans}. (Notice they are the \\emph{{opposites}} of the numbers in the factors.)"]
        stem = choose(rng, f"What are the solutions of {m(eq)}?", f"Solve {m(eq)}.")
    else:
        if lvl == 2:
            eq = f"{_poly_tex(x**2 + b * x + c)} = 0"
            first = []
        else:
            form = rng.choice(["move", "move", "prod"])
            if form == "move":
                # x^2 + b x = -c   or   x^2 = -b x - c
                if rng.random() < 0.5:
                    eq = f"{_poly_tex(x**2 + b * x)} = {-c}"
                    first = [f"Get 0 on one side: {'subtract' if -c > 0 else 'add'} {m(abs(c))} "
                             f"{'from' if -c > 0 else 'to'} both sides: {m(f'{_poly_tex(x**2 + b * x + c)} = 0')}."]
                else:
                    eq = f"x^{{2}} = {_poly_tex(-b * x - c)}"
                    first = [f"Get 0 on one side: move every term to the left. {m(f'{_poly_tex(x**2 + b * x + c)} = 0')}."]
            else:
                # x (x + k) = d  with the trap of setting each factor equal to d
                k = b
                d = -c
                need(d != 0 and k != 0)
                eq = f"x({_bin(1, k)}) = {d}"
                first = [f"Multiply out the left side and get 0 on one side: {m(f'x^{{2}} {_plus(k)}x = {d}')}, so "
                         f"{m(f'{_poly_tex(x**2 + k * x - d)} = 0')}.".replace("+ 1x", "+ x").replace("- 1x", "- x")]
                cands.insert(0, (_sol_tex([d, d - k]), frozenset([d, d - k]),
                                 f"sets each factor equal to {m(d)}; that only works when the right side is 0"))
        pr = [(rr, ss) for rr, ss in _pairs(c) if rr + ss != -b]
        for rr, ss in pr[:2]:
            cands.append((_sol_tex([-rr, -ss]), frozenset([-rr, -ss]),
                          f"factors with {m(rr)} and {m(ss)}, which multiply to {m(c)} but do not add to {m(-(r1 + r2))}"))
        cands.append((_sol_tex([r1]), frozenset([r1]), "finds only one of the two solutions"))
        steps = first + [f"Factor: two numbers that multiply to {m(c)} and add to {m(b)} are {m(-r1)} and {m(-r2)}, so "
                         f"{m(f'({_bin(1, -r1)})({_bin(1, -r2)}) = 0')}.",
                         f"Set each factor equal to 0: {m(f'x = {r1}')} or {m(f'x = {r2}')}."]
        stem = choose(rng, f"What are the solutions of {m(eq)}?", f"Solve for $x$: {m(eq)}.",
                      f"Which values of $x$ satisfy {m(eq)}?")
    sols = set(sp.solve(sp.Eq(coefs[0] * x**2 + coefs[1] * x + coefs[2], 0), x))
    want = set(key)
    return Problem(stem=stem, answer=ans, fmt=text, wrong=_string_choices(ans, key, cands), steps=steps,
                   verify=lambda s: s == ans and _roots_ok(coefs, want) and sols == {Q(v) for v in want})


@template("MK")
def which_solution(rng, lvl):
    r1, r2 = rng.sample([v for v in range(-9, 10) if v != 0], 2)
    need(r1 + r2 != 0)
    b, c = -(r1 + r2), r1 * r2
    a = 1
    if lvl >= 3 and rng.random() < 0.5:
        a = rng.choice([2, 3])
    poly = a * (x**2 + b * x + c)
    eq = f"{_poly_tex(poly)} = 0"
    ans = rng.choice([r1, r2])
    other = r2 if ans == r1 else r1
    roots = {r1, r2}
    cands = [(-ans, "has the wrong sign: it is the number in a factor, not a solution"),
             (-other, "is the opposite of the other solution"),
             (c, "is the constant term, not a solution"),
             (b, f"is the coefficient of {m('x')}, not a solution")]
    wrong = []
    for v, why in cands:
        if v not in roots and v not in [w[0] for w in wrong] and v != ans:
            wrong.append((Q(v), why))
    steps = ([f"Divide every term by {m(a)}: {m(f'{_poly_tex(x**2 + b * x + c)} = 0')}."] if a > 1 else []) + [
        f"Factor: two numbers that multiply to {m(c)} and add to {m(b)} are {m(-r1)} and {m(-r2)}, so "
        f"{m(f'({_bin(1, -r1)})({_bin(1, -r2)}) = 0')}.",
        f"The solutions are {m(f'x = {r1}')} and {m(f'x = {r2}')}. Only {m(ans)} is among the choices.",
        (f"Check: {m(f'({ans})^{{2}} {_plus(b)}({ans}) {_plus(c)} = {ans * ans} {_plus(b * ans)} {_plus(c)} = 0')}. \\checkmark"
         .replace("+ 1(", "+ (").replace("- 1(", "- ("))]
    return Problem(stem=choose(rng, f"Which of the following is a solution of {m(eq)}?",
                               f"Which value of $x$ makes {m(eq)} true?"),
                   answer=Q(ans), fmt=frac, wrong=wrong, near=lambda r: [], steps=steps,
                   verify=lambda v: _roots_ok((a, a * b, a * c), [v]), neg_ok=True)


@template("MK")
def leading_coef(rng, lvl):
    a = rng.choice([2, 3, 5])
    p = rng.choice([v for v in range(-7, 8) if v != 0])
    q = rng.choice([v for v in range(-6, 7) if v != 0])
    need(math.gcd(a, abs(p)) == 1 and p != q)
    b, c = a * q + p, p * q
    need(b != 0 and abs(b) <= 20)
    orig = a * x**2 + b * x + c
    otex = _poly_tex(orig)
    if rng.random() < 0.5:
        ans = f"${_fact_tex([(a, p), (1, q)])}$"
        key = sp.expand(orig)
        cands = [(f"${_fact_tex([(a, q), (1, p)])}$", sp.expand((a * x + q) * (x + p)),
                  f"puts {m(p)} and {m(q)} in the wrong factors, so the middle term comes out {m(_poly_tex((a * p + q) * x))}"),
                 (f"${_fact_tex([(1, p), (1, q)])}$", sp.expand((x + p) * (x + q)), f"ignores the leading coefficient {m(a)}"),
                 (f"${_fact_tex([(a, -p), (1, -q)])}$", sp.expand((a * x - p) * (x - q)), "has the signs backwards"),
                 (f"${_fact_tex([(a, p), (a, q)])}$", sp.expand((a * x + p) * (a * x + q)), f"puts {m(a)} in both factors")]
        steps = [f"The first terms must multiply to {m(f'{a}x^{{2}}')}, so try {m(f'({a}x + \\underline{{\\ \\ }})(x + \\underline{{\\ \\ }})')}. "
                 f"The last numbers must multiply to {m(c)}.",
                 f"Test pairs until the Outer + Inner products give {m(_poly_tex(b * x))}: with {m(p)} and {m(q)}, "
                 f"{m(f'{a}x \\cdot {_par(q)} + {_par(p)} \\cdot x = {_poly_tex(a * q * x)} {_plus(p)}x = {_poly_tex(b * x)}')}."
                 .replace("+ 1x", "+ x").replace("- 1x", "- x"),
                 f"So {m(f'{otex} = {_fact_tex([(a, p), (1, q)])}')}."]
        ok = all((a * t + p) * (t + q) == a * t * t + b * t + c for t in (-3, 1, 4))
        return Problem(stem=choose(rng, f"Factor: {m(otex)}", f"Which is the factored form of {m(otex)}?"),
                       answer=ans, fmt=text, wrong=_string_choices(ans, key, cands), steps=steps,
                       verify=lambda s: s == ans and ok)
    r1, r2 = R(-p, a), Q(-q)
    ans = _sol_tex([r1, r2])
    key = frozenset([r1, r2])
    cands = [(_sol_tex([-r1, -r2]), frozenset([-r1, -r2]), "uses the numbers in the factors instead of their opposites"),
             (_sol_tex([Q(-p), r2]), frozenset([Q(-p), r2]), f"forgets to divide by {m(a)} when solving {m(f'{_bin(a, p)} = 0')}"),
             (_sol_tex([R(-q, a), Q(-p)]), frozenset([R(-q, a), Q(-p)]), f"puts {m(p)} and {m(q)} in the wrong factors"),
             (_sol_tex([r1]), frozenset([r1]), "finds only one of the two solutions")]
    steps = [f"Factor: {m(f'{otex} = {_fact_tex([(a, p), (1, q)])}')} (check the middle term: "
             f"{m(f'{_poly_tex(a * q * x)} {_plus(p)}x = {_poly_tex(b * x)}')}).".replace("+ 1x", "+ x").replace("- 1x", "- x"),
             f"Set each factor equal to 0: {m(f'{_bin(a, p)} = 0')} gives {m(f'x = {frac_raw(r1)}')}; "
             f"{m(f'{_bin(1, q)} = 0')} gives {m(f'x = {tx(r2)}')}.",
             f"The solutions are {ans}."]
    sols = set(sp.solve(sp.Eq(orig, 0), x))
    return Problem(stem=choose(rng, f"What are the solutions of {m(f'{otex} = 0')}?", f"Solve for $x$: {m(f'{otex} = 0')}."),
                   answer=ans, fmt=text, wrong=_string_choices(ans, key, cands), steps=steps,
                   verify=lambda s: s == ans and _roots_ok((a, b, c), [r1, r2]) and sols == {r1, r2})


@template("MK")
def square_root_eq(rng, lvl):
    nn = rng.randint(2, 13)
    k = nn * nn
    if lvl <= 1:
        v = rng.choice(["x", "x", "n", "t", "y"])
        form = rng.choice(["eq", "zero", "plus", "minus"])
        if form == "eq":
            eq, steps0 = f"{v}^{{2}} = {k}", []
        elif form == "zero":
            eq, steps0 = f"{v}^{{2}} - {k} = 0", [f"Add {m(k)} to both sides: {m(f'{v}^{{2}} = {k}')}."]
        elif form == "plus":
            cst = rng.randint(1, 30)
            eq, steps0 = f"{v}^{{2}} + {cst} = {k + cst}", [f"Subtract {m(cst)} from both sides: {m(f'{v}^{{2}} = {k}')}."]
        else:
            cst = rng.randint(1, k - 1)
            eq, steps0 = f"{v}^{{2}} - {cst} = {k - cst}", [f"Add {m(cst)} to both sides: {m(f'{v}^{{2}} = {k}')}."]
        coefs = (1, 0, -k)
        roots = [nn, -nn]
        ans, key = _sol_tex(roots, v), frozenset(roots)
        cands = [(_sol_tex([nn], v), frozenset([nn]), "forgets the negative solution"),
                 (_sol_tex([k, -k], v), frozenset([k, -k]), "forgets to take the square root")]
        if k % 2 == 0 and k // 2 != nn:
            cands.append((_sol_tex([k // 2, -(k // 2)], v), frozenset([k // 2, -(k // 2)]), "divides by 2 instead of taking the square root"))
        cands.append((_sol_tex([nn + 1, -(nn + 1)], v), frozenset([nn + 1, -(nn + 1)]), None))
        steps = steps0 + [f"Take the square root of both sides and keep \\emph{{both}} signs: {m(f'{v} = {nn}')} or {m(f'{v} = -{nn}')}, "
                          f"because {m(f'{nn}^{{2}} = {k}')} and {m(f'(-{nn})^{{2}} = {k}')}."]
        sols = set(sp.solve(sp.Eq(x**2 - k, 0), x))
        return Problem(stem=choose(rng, f"What are the solutions of {m(eq)}?", f"Solve for ${v}$: {m(eq)}."),
                       answer=ans, fmt=text, wrong=_string_choices(ans, key, cands), steps=steps,
                       verify=lambda s_: s_ == ans and _roots_ok(coefs, roots) and sols == {Q(r) for r in roots})
    form = rng.choice(["ax", "axc", "shift"])
    if form in ("ax", "axc"):
        a = rng.randint(2, 5)
        cst = 0 if form == "ax" else rng.choice([v for v in range(-20, 21) if v != 0])
        d = a * k + cst
        eq = f"{a}x^{{2}}{_plus(cst) if cst else ''} = {d}"
        coefs = (a, 0, cst - d)
        roots = [nn, -nn]
        steps = ([f"{'Subtract' if cst > 0 else 'Add'} {m(abs(cst))} {'from' if cst > 0 else 'to'} both sides: "
                  f"{m(f'{a}x^{{2}} = {a * k}')}."] if cst else []) + \
            [f"Divide both sides by {m(a)}: {m(f'x^{{2}} = {k}')}.",
             f"Take the square root and keep both signs: {m(f'x = {nn}')} or {m(f'x = -{nn}')}."]
        cands = [(_sol_tex([nn]), frozenset([nn]), "forgets the negative solution")]
        if cst:
            w = Q(d + cst) / a
            if w > 0 and sp.sqrt(w).is_rational:
                s_ = sp.sqrt(w)
                cands.append((_sol_tex([s_, -s_]), frozenset([s_, -s_]), f"moves {m(tx(cst))} across without changing its sign"))
        w2 = Q(d - cst)
        if sp.sqrt(w2).is_rational and w2 != k:
            cands.append((_sol_tex([sp.sqrt(w2), -sp.sqrt(w2)]), frozenset([sp.sqrt(w2), -sp.sqrt(w2)]),
                          f"forgets to divide by {m(a)}"))
        cands.append((_sol_tex([k, -k]), frozenset([k, -k]), "forgets to take the square root"))
        if (a * nn) != k:
            cands.append((_sol_tex([a * nn, -a * nn]), frozenset([a * nn, -a * nn]), None))
    else:
        h = rng.choice([v for v in range(-9, 10) if v != 0])
        nn = rng.randint(2, 9)
        k = nn * nn
        need(abs(h) != nn)
        eq = f"({_bin(1, -h)})^{{2}} = {k}"
        roots = [h + nn, h - nn]
        coefs = (1, -2 * h, h * h - k)
        steps = [f"Take the square root of both sides, keeping both signs: {m(f'{_bin(1, -h)} = {nn}')} or "
                 f"{m(f'{_bin(1, -h)} = -{nn}')}.",
                 f"{'Add' if h > 0 else 'Subtract'} {m(abs(h))} {'to' if h > 0 else 'from'} both sides: "
                 f"{m(f'x = {h + nn}')} or {m(f'x = {h - nn}')}."]
        cands = [(_sol_tex([h + nn]), frozenset([h + nn]), "forgets the negative square root"),
                 (_sol_tex([nn, -nn]), frozenset([nn, -nn]), f"forgets to {'add' if h > 0 else 'subtract'} {m(abs(h))}"),
                 (_sol_tex([-h + nn, -h - nn]), frozenset([-h + nn, -h - nn]), f"uses the wrong sign for {m(abs(h))}"),
                 (_sol_tex([h + k, h - k]), frozenset([h + k, h - k]), "forgets to take the square root")]
    ans, key = _sol_tex(roots), frozenset(roots)
    sols = set(sp.solve(sp.Eq(coefs[0] * x**2 + coefs[1] * x + coefs[2], 0), x))
    return Problem(stem=choose(rng, f"What are the solutions of {m(eq)}?", f"Solve for $x$: {m(eq)}."),
                   answer=ans, fmt=text, wrong=_string_choices(ans, key, cands), steps=steps,
                   verify=lambda s: s == ans and _roots_ok(coefs, roots) and sols == {Q(r) for r in roots})


@template("MK")
def quadratic_formula(rng, lvl):
    a1, a2 = rng.choice([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (1, 4), (1, 5), (1, 6), (2, 2)])
    p = rng.choice([v for v in range(-7, 8) if v != 0])
    q = rng.choice([v for v in range(-7, 8) if v != 0])
    a, b, c = a1 * a2, a1 * q + a2 * p, p * q
    need(b != 0 and math.gcd(math.gcd(a, abs(b)), abs(c)) == 1 and abs(b) <= 16 and abs(c) <= 30)
    D = b * b - 4 * a * c
    s = math.isqrt(D)
    need(s * s == D and s > 0)
    r_plus, r_minus = R(-b + s, 2 * a), R(-b - s, 2 * a)
    ans, key = _sol_tex([r_plus, r_minus]), frozenset([r_plus, r_minus])
    otex = _poly_tex(a * x**2 + b * x + c)
    cands = [(_sol_tex([-r_plus, -r_minus]), frozenset([-r_plus, -r_minus]), f"uses {m(tx(b))} instead of {m(tx(-b))} in the formula"),
             (_sol_tex([2 * r_plus, 2 * r_minus]), frozenset([2 * r_plus, 2 * r_minus]), f"divides by {m(a)} instead of by {m(f'2a = {2 * a}')}")
             if a != 1 else (_sol_tex([r_plus / 2, r_minus / 2]), frozenset([r_plus / 2, r_minus / 2]), "divides by 4 instead of by 2"),
             (_sol_tex([r_plus]), frozenset([r_plus]), "uses only the $+$ sign of $\\pm$")]
    D2 = b * b + 4 * a * c
    s2 = math.isqrt(abs(D2))
    if D2 > 0 and s2 * s2 == D2:
        w1, w2 = R(-b + s2, 2 * a), R(-b - s2, 2 * a)
        cands.insert(1, (_sol_tex([w1, w2]), frozenset([w1, w2]), "adds $4ac$ instead of subtracting it"))
    w1, w2 = Q(-b) + R(s, 2 * a), Q(-b) - R(s, 2 * a)
    cands.append((_sol_tex([w1, w2]), frozenset([w1, w2]), "divides only the square root by $2a$, not the $-b$"))
    steps = [f"Here {m(f'a = {a}')}, {m(f'b = {b}')}, {m(f'c = {c}')}.",
             f"Compute {m('b^2 - 4ac')}: {m(f'{_par(b)}^{{2}} - 4({a})({c}) = {b * b} {_plus(-4 * a * c)} = {D}')}, "
             f"and {m(f'\\sqrt{{{D}}} = {s}')}.",
             f"{m(f'x = {F(f"{tx(-b)} \\pm {s}", 2 * a)}')}: either {m(f'x = {F(f"{tx(-b)} + {s}", 2 * a)} = {frac_raw(r_plus)}')} "
             f"or {m(f'x = {F(f"{tx(-b)} - {s}", 2 * a)} = {frac_raw(r_minus)}')}."]
    sols = set(sp.solve(sp.Eq(a * x**2 + b * x + c, 0), x))
    return Problem(stem=choose(rng, f"Use the quadratic formula to solve {m(f'{otex} = 0')}.",
                               f"What are the solutions of {m(f'{otex} = 0')}?"),
                   answer=ans, fmt=text, wrong=_string_choices(ans, key, cands), steps=steps,
                   tip=f"You can check by factoring: {m(f'{otex} = {_fact_tex([(a1, p), (a2, q)])}')}.",
                   verify=lambda v: v == ans and _roots_ok((a, b, c), [r_plus, r_minus]) and sols == {r_plus, r_minus})


@template("MK")
def function_eval(rng, lvl):
    fname = rng.choice(["f", "f", "g", "h"])
    if lvl <= 1:
        a = 1
        b = rng.choice([v for v in range(-6, 7) if v != 0])
        c = rng.randint(-9, 9)
        t = rng.choice([v for v in range(-5, 6) if v not in (0, 1)])
    else:
        a = rng.choice([2, 3, -1, -2])
        b = rng.choice([v for v in range(-7, 8) if v != 0])
        c = rng.randint(-9, 9)
        t = rng.choice([-5, -4, -3, -2, -1, 2, 3, 4])
    poly = a * x**2 + b * x + c
    ftex = _poly_tex(poly)
    val = a * t * t + b * t + c
    sq = f"({t})^{{2}}" if t < 0 else f"{t}^{{2}}"
    if a == 1:
        a_part = sq
    elif a == -1:
        a_part = f"-({t})^{{2}}"
    else:
        a_part = f"{a}({t})^{{2}}"
    b_part = f"{_plus(b)}({t})".replace("+ 1(", "+ (").replace("- 1(", "- (")
    c_part = _plus(c) if c else ""
    sub = f"{a_part} {b_part}{c_part}"
    nums = f"{a * t * t} {_plus(b * t)}{c_part}"
    wrong = [(Q(-a * t * t + b * t + c), f"treats {m(sq)} as {m(-t * t)}") if t < 0 else
             (Q(a * 2 * t + b * t + c), f"doubles {m(t)} instead of squaring it"),
             (Q(a * t * t - b * t + c), f"makes a sign error with {m(_poly_tex(b * x))}"),
             (Q(a * t * t + b * (-t) + c) if t < 0 else Q(a * t * t + b * t - c), "substitutes the wrong sign" if t < 0
              else "makes a sign error with the constant")]
    if a not in (1, -1):
        wrong.insert(1, (Q((a * t)**2 + b * t + c), f"squares {m(f'{a}({t})')} instead of squaring only {m(t)}"))
    steps = [f"Replace every {m('x')} with {m(f'({t})')}: {m(f'{fname}({t}) = {sub}')}.",
             f"Square first (order of operations): {m(f'{sq} = {t * t}')}"
             + (f", then multiply: {m(f'{a} \\cdot {t * t} = {a * t * t}')}" if a not in (1, -1) else "")
             + f". So {m(f'{fname}({t}) = {nums}')}.",
             f"Combine: {m(f'{fname}({t}) = {val}')}."]
    fr = Fraction(a) * t * t + b * t + c
    return Problem(stem=choose(rng, f"If {m(f'{fname}(x) = {ftex}')}, what is {m(f'{fname}({t})')}?",
                               f"Given {m(f'{fname}(x) = {ftex}')}, find {m(f'{fname}({t})')}."),
                   answer=Q(val), fmt=num, wrong=wrong, steps=steps,
                   check=poly.subs(x, t), verify=lambda v: Q(v) == Q(int(fr)), neg_ok=True)


PLAN = [
    # (template, level, count)  -- easy -> hard; 25 problems
    (factor_gcf, 1, 2),
    (factor_trinomial, 1, 2),
    (solve_factored, 1, 2),
    (square_root_eq, 1, 1),
    (function_eval, 1, 1),
    (factor_trinomial, 2, 2),
    (special_factor, 2, 2),
    (solve_factored, 2, 2),
    (which_solution, 2, 2),
    (square_root_eq, 2, 1),
    (function_eval, 2, 1),
    (leading_coef, 3, 2),
    (quadratic_formula, 3, 2),
    (special_factor, 3, 1),
    (factor_gcf, 3, 1),
    (solve_factored, 3, 1),
]
