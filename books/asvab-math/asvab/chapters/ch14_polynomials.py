"""Chapter 14 - Polynomials & Exponent Rules."""
from fractions import Fraction

import sympy as sp

from ..core import (R, Q, Problem, need, num, m, F, tx, latex, text, frac_raw,
                    choose, template, x, y)

NUM = 14
TITLE = r"Polynomials \& Exponent Rules"
PART = 2

INTRO = r"""
A \emph{polynomial} is a sum of terms such as $3x^2$, $-5x$, and $7$. Each
term has a \emph{coefficient} (the number in front) and a variable part.
\emph{Like terms} have exactly the same variable part: $x^2$ and $4x^2$ are
like terms; $x^2$ and $x^3$ are not.

\begin{concept}{Exponent rules}
{\renewcommand{\arraystretch}{1.9}\begin{tabular}{@{}ll@{\qquad}ll@{}}
$x^a \cdot x^b = x^{a+b}$ & add exponents & $x^0 = 1$ & ($x \ne 0$) \\
$\dfrac{x^a}{x^b} = x^{a-b}$ & subtract exponents & $x^{-a} = \dfrac{1}{x^a}$ & negative exponent \\
$(x^a)^b = x^{ab}$ & multiply exponents & $(xy)^a = x^a y^a$ & every factor \\
\end{tabular}}

\smallskip
A variable with no exponent has exponent $1$: $x = x^1$.
\end{concept}

\begin{concept}{Adding, subtracting, and vocabulary}
Add or subtract polynomials by combining like terms: add the
\emph{coefficients} and keep the exponent ($2x^2 + 5x^2 = 7x^2$). To subtract,
distribute the minus sign to \emph{every} term:
$-(x^2 - 4x + 1) = -x^2 + 4x - 1$.

The \emph{degree} is the highest exponent; the \emph{leading coefficient}
is the coefficient of that term. In $5x^3 - 2x^7 + x$ the degree is $7$
and the leading coefficient is $-2$.
\end{concept}

\begin{concept}{Multiplying}
Multiply every term by every term. For two binomials use FOIL (First,
Outer, Inner, Last):
\[ (x + 3)(x - 5) = x^2 - 5x + 3x - 15 = x^2 - 2x - 15 \]
Special products worth memorizing:
\[ (a + b)^2 = a^2 + 2ab + b^2 \quad (a - b)^2 = a^2 - 2ab + b^2 \quad (a + b)(a - b) = a^2 - b^2 \]
\end{concept}

\begin{example}{Worked example}
Simplify $(2x^3y)^2 \cdot 3xy^4$.

\textbf{Solution.} Square every factor: $(2x^3y)^2 = 2^2 x^{3 \cdot 2} y^2 = 4x^6y^2$.
Then multiply coefficients and add exponents:
$4x^6y^2 \cdot 3xy^4 = 12x^{6+1}y^{2+4} = 12x^7y^6$.
\end{example}

\begin{tip}
Check with a number. Put $x = 2$ (and $y = 1$) into the original
expression and into your answer: the two values must match. It takes
seconds and catches most sign and exponent slips.
\end{tip}

\begin{trap}
\begin{itemize}
\item $(x + 4)^2$ is \emph{not} $x^2 + 16$: the middle term $8x$ is missing.
\item $(2x^3)^2$ is $4x^6$, not $2x^6$: the coefficient is squared too.
\item Adding exponents when you add like terms: $x^2 + x^2 = 2x^2$, not $x^4$.
\item Forgetting to change \emph{every} sign when subtracting a polynomial.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# private helpers
# --------------------------------------------------------------------------

_PTS = [(-3, 2), (-1, -2), (2, 3), (5, -1), (3, 1)]


def _numcheck(f, v):
    """Independent check: evaluate the original expression with plain
    fractions at several points and compare with the sympy answer."""
    e = sp.sympify(v)
    for t, u in _PTS:
        want = f(Fraction(t), Fraction(u))
        got = e.subs({x: t, y: u})
        if Q(got) != Q(sp.Rational(want.numerator, want.denominator)):
            return False
    return True


def _mono(c, px, py=0):
    """Monomial as a sympy expression."""
    return Q(c) * x**px * y**py


def _poly_tex(e):
    """Polynomial in x in descending order (sympy's latex can reorder)."""
    P = sp.Poly(sp.expand(e), x)
    terms = []
    for (k,), c in sorted(P.terms(), key=lambda t: -t[0][0]):
        terms.append((c, "" if k == 0 else ("x" if k == 1 else f"x^{{{k}}}")))
    out = ""
    for c, v in terms:
        if c == 0:
            continue
        mag = abs(c)
        body = v if (v and mag == 1) else frac_raw(mag) + v
        out = (("-" if c < 0 else "") + body) if not out else out + (" - " if c < 0 else " + ") + body
    return out or "0"


def _pfmt(v):
    """Choice formatter for polynomials in x: descending order."""
    return m(_poly_tex(v))


def _bin(p, a):
    """(px + a) as LaTeX, e.g. '2x - 3'."""
    out = ("x" if p == 1 else ("-x" if p == -1 else f"{p}x"))
    return out + (f" + {a}" if a > 0 else f" - {-a}" if a < 0 else "")


def _par(v):
    return f"({tx(v)})" if Q(v) < 0 else tx(v)


def _xp(k, var="x"):
    return var if k == 1 else f"{var}^{{{k}}}"


def _mtex(c, px, py=0):
    """Monomial LaTeX with exponents written the textbook way."""
    s = ""
    if c == -1:
        s = "-"
    elif c != 1:
        s = tx(c)
    if px:
        s += _xp(px)
    if py:
        s += _xp(py, "y")
    return s or "1"


def _efmt(v):
    """Choice formatter for monomials and rational expressions."""
    return m(latex(v))


def _choice_problem(stem, ans, wrong, steps, f, fmt=_efmt, tip=None):
    """Problem whose choices are LaTeX strings built from sympy expressions.

    The answer is verified against the original expression with plain
    fractions (_numcheck), and every distractor is checked to be a
    *different* expression (sp.cancel of the difference is not 0), so no
    equivalent form can appear as a wrong choice.  String choices keep the
    comparisons in finalize() literal and fast.
    """
    ans_tex = fmt(ans)
    ok = _numcheck(f, ans)
    out, seen = [], {ans_tex}
    for item in wrong:
        val, why = item[0], item[1]
        if sp.cancel(sp.together(sp.sympify(val) - ans)) == 0:
            continue
        t = fmt(val)
        if t in seen:
            continue
        seen.add(t)
        out.append((t, why))
    need(len(out) >= 3)
    return Problem(stem=stem, answer=ans_tex, fmt=text, wrong=out, steps=steps, tip=tip,
                   verify=lambda s_: ok and s_ == ans_tex)


# --------------------------------------------------------------------------
# templates
# --------------------------------------------------------------------------

def _rand_quad(rng, lead_pos=True):
    a = rng.randint(1, 7) * (1 if lead_pos or rng.random() < 0.5 else -1)
    b = rng.choice([v for v in range(-9, 10) if v != 0])
    c = rng.choice([v for v in range(-12, 13) if v != 0])
    return a, b, c


@template("MK")
def add_sub_poly(rng, lvl):
    a1, b1, c1 = _rand_quad(rng)
    a2, b2, c2 = _rand_quad(rng)
    need(a1 != a2 and (a1, b1, c1) != (a2, b2, c2))
    P = a1 * x**2 + b1 * x + c1
    Qp = a2 * x**2 + b2 * x + c2
    Pt, Qt = _poly_tex(P), _poly_tex(Qp)
    if lvl == 1:
        ans = sp.expand(P + Qp)
        need(all(ans.coeff(x, k) != 0 for k in (0, 1, 2)))
        stem = choose(rng, f"Simplify: {m(f'({Pt}) + ({Qt})')}",
                      f"What is the sum of {m(Pt)} and {m(Qt)}?")
        wrong = [((a1 + a2) * x**4 + (b1 + b2) * x**2 + (c1 + c2), "adds the exponents as well as the coefficients"),
                 ((a1 + a2) * x**2 + (b1 - b2) * x + (c1 + c2), "subtracts the $x$-terms instead of adding them"),
                 ((a1 + a2 + b1 + b2) * x**2 + (c1 + c2), "combines unlike terms ($x^2$-terms with $x$-terms)"),
                 ((a1 + a2) * x**2 + (b1 + b2) * x + (c1 - c2), "subtracts the constants instead of adding them")]
        steps = [f"Group like terms: {m(f'({a1} + {_par(a2)})x^{{2}} + ({b1} + {_par(b2)})x + ({c1} + {_par(c2)})')}.",
                 f"Add the coefficients and keep each exponent: {m(_poly_tex(ans))}."]
        f = lambda t, u: (a1 * t**2 + b1 * t + c1) + (a2 * t**2 + b2 * t + c2)
    else:
        rev = rng.random() < 0.4      # "Subtract Q from P" order trap
        ans = sp.expand(P - Qp)
        need(all(ans.coeff(x, k) != 0 for k in (0, 1, 2)))
        if rev:
            stem = f"Subtract {m(Qt)} from {m(Pt)}."
        else:
            stem = choose(rng, f"Simplify: {m(f'({Pt}) - ({Qt})')}",
                          f"What is {m(f'({Pt}) - ({Qt})')}?")
        neg = _poly_tex(-Qp)
        wrong = [((a1 - a2) * x**2 + (b1 + b2) * x + (c1 + c2), "changes the sign of only the first term of the second polynomial"),
                 (sp.expand(P + Qp), "adds the polynomials instead of subtracting"),
                 ((a1 - a2) * x**2 + (b1 - b2) * x + (c1 + c2), "forgets to change the sign of the last term")]
        if rev:
            wrong.insert(0, (sp.expand(Qp - P), f"subtracts in the wrong order: ``subtract $A$ from $B$'' means $B - A$"))
        else:
            wrong.append((sp.expand(Qp - P), "subtracts in the wrong order"))
        steps = ([f"``Subtract {m(Qt)} from {m(Pt)}'' means {m(f'({Pt}) - ({Qt})')}."] if rev else []) + [
            f"Distribute the minus sign to \\emph{{every}} term of the second polynomial: "
            f"{m(f'-({Qt}) = {neg}')}.",
            f"Combine like terms: {m(f'({a1} - {_par(a2)})x^{{2}} + ({b1} - {_par(b2)})x + ({c1} - {_par(c2)}) = {_poly_tex(ans)}')}."]
        f = lambda t, u: (a1 * t**2 + b1 * t + c1) - (a2 * t**2 + b2 * t + c2)
    return _choice_problem(stem, ans, wrong, steps, f, fmt=_pfmt)


@template("MK")
def mult_monomials(rng, lvl):
    a, b = rng.randint(2, 9), rng.randint(2, 9)
    if lvl >= 2:
        a *= rng.choice([1, -1])
        b *= rng.choice([1, -1])
    p, r = rng.randint(1, 6), rng.randint(1, 6)
    if lvl == 1:
        q = s = 0
    else:
        q, s = rng.randint(1, 5), rng.randint(1, 5)
        need(q == 1 or s == 1 or p == 1 or r == 1)     # an invisible exponent 1 to notice
    need(p * r != p + r)
    A = _mtex(a, p, q)
    B = _mtex(b, r, s)
    ans = _mono(a * b, p + r, q + s)
    stem = choose(rng, f"Simplify: {m(f'({A})({B})')}", f"What is the product of {m(A)} and {m(B)}?")
    wrong = [(_mono(a * b, p * r, q * s if q * s else q + s), "multiplies the exponents instead of adding them"),
             (_mono(a + b, p + r, q + s), "adds the coefficients instead of multiplying them")]
    if lvl == 1:
        wrong.append((_mono(a + b, p * r), "adds the coefficients and multiplies the exponents"))
        wrong.append((_mono(a * b, max(p, r)), "keeps only the larger exponent"))
    else:
        ones = [v for v, e in (("x", p), ("y", q), ("x", r), ("y", s)) if e == 1]
        if q == 1 or s == 1:
            wrong.append((_mono(a * b, p + r, q + s - 1), "treats a $y$ with no exponent as $y^0$ instead of $y^1$"))
        if p == 1 or r == 1:
            wrong.append((_mono(a * b, p + r - 1, q + s), "treats an $x$ with no exponent as $x^0$ instead of $x^1$"))
        wrong.append((_mono(-a * b, p + r, q + s), "makes a sign error multiplying the coefficients"))
    steps = [f"Multiply the coefficients: {m(f'{_par(a)} \\cdot {_par(b)} = {a * b}')}.",
             f"Multiply like bases by \\emph{{adding}} exponents: {m(f'x^{{{p}}} \\cdot x^{{{r}}} = x^{{{p}+{r}}} = {_xp(p + r)}')}"
             + (f" and {m(f'y^{{{q}}} \\cdot y^{{{s}}} = y^{{{q}+{s}}} = {_xp(q + s, "y")}')}" if lvl >= 2 else "")
             + (" (a letter with no exponent has exponent 1)" if 1 in (p, r, q, s) else "") + ".",
             f"So the product is {m(_mtex(a * b, p + r, q + s))}."]
    f = lambda t, u: (a * t**p * u**q) * (b * t**r * u**s)
    return _choice_problem(stem, ans, wrong, steps, f)


@template("MK")
def quotient_rule(rng, lvl):
    b = rng.randint(2, 6)
    k = rng.randint(2, 6)
    a = b * k
    r = rng.randint(1, 4)
    p = r + rng.randint(1, 6)
    if lvl == 1:
        q = s = 0
    else:
        s = rng.randint(1, 4)
        q = s + rng.randint(0, 4)
        a *= rng.choice([1, -1])
    need(Fraction(p, r).denominator != 1 or p // r != p - r)
    ans = _mono(Q(a) / b, p - r, q - s)
    top, bot = _mtex(a, p, q), _mtex(b, r, s)
    stem = choose(rng, f"Simplify: {m(F(top, bot))}", f"Simplify {m(F(top, bot))}. Assume $x \\ne 0$"
                  + (" and $y \\ne 0$." if lvl >= 2 else "."))
    wrong = [(_mono(Q(a) / b, p + r, q + s), "adds the exponents instead of subtracting"),
             (_mono(a - b, p - r, q - s), "subtracts the coefficients instead of dividing")]
    if r > 1 and p % r == 0 and p // r != p - r:
        wrong.append((_mono(Q(a) / b, p // r, q - s), "divides the exponents instead of subtracting"))
    if lvl >= 2:
        if q == s:
            wrong.insert(0, (_mono(Q(a) / b, p - r, 1), f"keeps a {m('y')}, but {m(F(_xp(q, 'y'), _xp(s, 'y')))} is $y^0 = 1$"))
        else:
            wrong.append((_mono(Q(a) / b, p - r, q), f"forgets to divide the {m('y')} part"))
    wrong.append((_mono(Q(a) / b * (1 if lvl == 1 else -1), p - r + (1 if lvl == 1 else 0), q - s), None))
    xs = f"{F(_xp(p), _xp(r))} = x^{{{p}-{r}}} = {_xp(p - r)}"
    ys = f"{F(_xp(q, 'y'), _xp(s, 'y'))} = y^{{{q}-{s}}} = " + (_xp(q - s, "y") if q > s else "y^0 = 1")
    steps = [f"Divide the coefficients: {m(f'{tx(a)} \\div {b} = {tx(Q(a) / b)}')}.",
             f"Divide like bases by \\emph{{subtracting}} exponents: {m(xs)}"
             + (f" and {m(ys)}" if lvl >= 2 else "") + ".",
             f"So the result is {m(_mtex(Q(a) / b, p - r, q - s))}."]
    f = lambda t, u: Fraction(a) * t**p * u**q / (b * t**r * u**s)
    return _choice_problem(stem, ans, wrong, steps, f)


@template("MK")
def power_rule(rng, lvl):
    if lvl >= 3 and rng.random() < 0.5:
        return _power_product(rng)
    if lvl <= 2:
        c = rng.randint(2, 6)
        p = rng.randint(1, 6)
        q = rng.choice([0, 0, 1, 2, 3])
        k = 2 if c > 3 else rng.choice([2, 2, 3])
        sign = rng.choice([1, 1, -1]) if k == 2 else 1
    else:
        c = rng.randint(2, 4)
        p = rng.randint(1, 4)
        q = rng.randint(1, 3)
        k = rng.choice([2, 3])
        sign = rng.choice([1, -1])
    need(p + k != p * k)
    base = _mtex(sign * c, p, q)
    ans = _mono((sign * c)**k, p * k, q * k)
    stem = choose(rng, f"Simplify: {m(f'({base})^{{{k}}}')}", f"What is {m(f'({base})^{{{k}}}')}?")
    wrong = [(_mono(sign * c, p * k, q * k), f"forgets to raise the coefficient {m(sign * c)} to the power"),
             (_mono((sign * c)**k, p + k, q + k if q else 0), "adds the exponents instead of multiplying"),
             (_mono(sign * c * k, p * k, q * k), f"multiplies the coefficient by {m(k)} instead of raising it to the power {m(k)}")]
    if sign < 0 and k % 2 == 1:
        wrong.insert(0, (_mono(c**k, p * k, q * k), "loses the negative sign: a negative number to an odd power stays negative"))
    if sign < 0 and k % 2 == 0:
        wrong.insert(0, (_mono(-(c**k), p * k, q * k), "keeps the negative sign, but a negative number squared is positive"))
    steps = [f"Raise \\emph{{every}} factor inside the parentheses to the power {m(k)}.",
             f"Coefficient: {m(f'{_par(sign * c)}^{{{k}}} = {(sign * c)**k}')}. Variables: multiply exponents, "
             f"{m(f'({_xp(p)})^{{{k}}} = x^{{{p * k}}}')}"
             + (f" and {m(f'({_xp(q, "y")})^{{{k}}} = y^{{{q * k}}}')}" if q else "") + ".",
             f"So the result is {m(_mtex((sign * c)**k, p * k, q * k))}."]
    f = lambda t, u: (sign * c * t**p * u**q)**k
    return _choice_problem(stem, ans, wrong, steps, f)


def _power_product(rng):
    """(c x^p y^q)^k times another monomial: power first, then multiply."""
    c, d = rng.randint(2, 4), rng.randint(2, 6)
    p, r = rng.randint(1, 4), rng.randint(1, 4)
    q, s_ = rng.randint(0, 3), rng.randint(0, 3)
    k = rng.choice([2, 2, 3]) if c == 2 else 2
    need(q + s_ > 0 and p * k != p + k and (c, p, q) != (d, r, s_))
    A, B = _mtex(c, p, q), _mtex(d, r, s_)
    given = f"({A})^{{{k}}} \\cdot {B}"
    ans = _mono(c**k * d, p * k + r, q * k + s_)
    stem = choose(rng, f"Simplify: {m(given)}", f"Which expression is equal to {m(given)}?")
    wrong = [(_mono(c * d, p * k + r, q * k + s_), f"forgets to raise the coefficient {m(c)} to the power {m(k)}"),
             (_mono(c**k * d, p + k + r, (q + k if q else 0) + s_), "adds the exponents inside the power instead of multiplying"),
             (_mono(c**k * d, p * k * r, q * k * s_ if q * s_ else q * k + s_), "multiplies the exponents when multiplying the monomials"),
             (_mono(c**k + d, p * k + r, q * k + s_), "adds the coefficients at the end instead of multiplying")]
    pw = _mtex(c**k, p * k, q * k)
    steps = [f"Do the power first. Raise every factor to the power {m(k)}: {m(f'({A})^{{{k}}} = {pw}')}.",
             f"Now multiply: coefficients {m(f'{c**k} \\cdot {d} = {c**k * d}')}; add exponents of like bases, "
             f"{m(f'x^{{{p * k}}} \\cdot {_xp(r)} = {_xp(p * k + r)}')}"
             + (f" and {m(f'{_xp(q * k, "y")} \\cdot {_xp(s_, "y")} = {_xp(q * k + s_, "y")}')}" if q and s_ else
                f"; the {m(_xp(q * k + s_, 'y'))} has no partner, so it stays as it is") + ".",
             f"So the result is {m(_mtex(c**k * d, p * k + r, q * k + s_))}."]
    f = lambda t, u: (c * t**p * u**q)**k * (d * t**r * u**s_)
    return _choice_problem(stem, ans, wrong, steps, f)


@template("MK")
def foil(rng, lvl):
    if lvl <= 2:
        p = q = 1
    else:
        p, q = rng.randint(2, 5), rng.randint(1, 4)
    a = rng.choice([v for v in range(-9, 10) if v != 0])
    b = rng.choice([v for v in range(-9, 10) if v != 0])
    need(p * b + q * a != 0 and (p, a) != (q, b))
    ans = sp.expand((p * x + a) * (q * x + b))
    need(ans.coeff(x, 1) != 0)
    L1, L2 = _bin(p, a), _bin(q, b)
    stem = choose(rng, f"Multiply: {m(f'({L1})({L2})')}", f"Which expression is equal to {m(f'({L1})({L2})')}?",
                  f"Expand and simplify {m(f'({L1})({L2})')}.")
    first, outer, inner, last = p * q * x**2, p * b * x, a * q * x, a * b
    wrong = [(p * q * x**2 + a * b, "multiplies only the First and Last terms and leaves out the middle"),
             (p * q * x**2 - (p * b + q * a) * x + a * b, "gets the sign of the middle term wrong"),
             (p * q * x**2 + (p * b + q * a) * x - a * b, "gets the sign of the last term wrong")]
    if p == q == 1:
        wrong.append((x**2 + a * b * x + (a + b), "mixes up the sum and the product of the numbers"))
    else:
        wrong.append((p * q * x**2 + (p * a + q * b) * x + a * b, "pairs the wrong terms for the Outer and Inner products"))
        wrong.append(((p + q) * x**2 + (p * b + q * a) * x + a * b, "adds the First terms instead of multiplying them"))
    steps = [f"Use FOIL. First: {m(f'{_xp1(p)} \\cdot {_xp1(q)} = {_poly_tex(first)}')}. "
             f"Outer: {m(f'{_xp1(p)} \\cdot {_par(b)} = {_poly_tex(outer)}')}. "
             f"Inner: {m(f'{_par(a)} \\cdot {_xp1(q)} = {_poly_tex(inner)}')}. "
             f"Last: {m(f'{_par(a)} \\cdot {_par(b)} = {a * b}')}.",
             f"Add them and combine the two middle terms: "
             f"{m(f'{_poly_tex(first)} {_sgn_term(outer)} {_sgn_term(inner)} {_sgn_c(a * b)} = {_poly_tex(ans)}')}."]
    f = lambda t, u: (p * t + a) * (q * t + b)
    return _choice_problem(stem, ans, wrong, steps, f, fmt=_pfmt)


def _xp1(p):
    return "x" if p == 1 else f"{p}x"


def _sgn_term(e):
    t = _poly_tex(e)
    return f"- {t[1:]}" if t.startswith("-") else f"+ {t}"


def _sgn_c(c):
    return f"- {-c}" if c < 0 else f"+ {c}"


@template("MK")
def special_products(rng, lvl):
    kind = rng.choice(["sq+", "sq-", "conj"])
    p = rng.choice([1, 1, 1, 2, 3]) if lvl <= 2 else rng.randint(2, 6)
    a = rng.randint(1, 12) if lvl <= 2 else rng.randint(1, 9)
    P = p * x
    if kind == "sq+":
        expr_tex = f"({_bin(p, a)})^{{2}}"
        ans = sp.expand((P + a)**2)
        wrong = [(p**2 * x**2 + a**2, f"squares each term but leaves out the middle term {m(_poly_tex(2 * p * a * x))}"),
                 (p**2 * x**2 + p * a * x + a**2, "forgets to double the middle term"),
                 (p * x**2 + 2 * p * a * x + a**2, f"does not square the coefficient {m(p)}") if p > 1 else
                 (x**2 + 2 * a * x + 2 * a, f"doubles {m(a)} instead of squaring it"),
                 (p**2 * x**2 + 2 * p * a * x + 2 * a, f"doubles {m(a)} instead of squaring it")]
        f = lambda t, u: (p * t + a)**2
        pattern = r"(A + B)^2 = A^2 + 2AB + B^2"
        mid = f"2({_xp1(p)})({a}) = {_poly_tex(2 * p * a * x)}"
    elif kind == "sq-":
        expr_tex = f"({_bin(p, -a)})^{{2}}"
        ans = sp.expand((P - a)**2)
        wrong = [(p**2 * x**2 - a**2, "squares each term, leaves out the middle term, and makes the last term negative"),
                 (p**2 * x**2 + a**2, f"squares each term but leaves out the middle term {m(_poly_tex(-2 * p * a * x))}"),
                 (p**2 * x**2 - 2 * p * a * x - a**2, f"makes the last term negative, but {m(f'(-{a})^{{2}} = {a * a}')}"),
                 (p**2 * x**2 + 2 * p * a * x + a**2, "gets the sign of the middle term wrong")]
        f = lambda t, u: (p * t - a)**2
        pattern = r"(A - B)^2 = A^2 - 2AB + B^2"
        mid = f"2({_xp1(p)})({a}) = {_poly_tex(2 * p * a * x)}"
    else:
        expr_tex = choose(rng, f"({_bin(p, a)})({_bin(p, -a)})", f"({_bin(p, -a)})({_bin(p, a)})")
        ans = sp.expand((P + a) * (P - a))
        wrong = [(p**2 * x**2 + a**2, "makes the last term positive, but a positive times a negative is negative"),
                 (p**2 * x**2 - 2 * p * a * x - a**2,
                  f"gets the sign of one middle product wrong ({m(_poly_tex(-p * a * x))} instead of "
                  f"{m(_poly_tex(p * a * x))}), so the middle terms add to {m(_poly_tex(-2 * p * a * x))} instead of canceling"),
                 (p**2 * x**2 - 2 * p * a * x + a**2, "treats it like a perfect square"),
                 (p * x**2 - a**2, f"does not square the coefficient {m(p)}") if p > 1 else (x**2 - 2 * a, f"doubles {m(a)} instead of squaring it")]
        f = lambda t, u: (p * t + a) * (p * t - a)
        pattern = r"(A + B)(A - B) = A^2 - B^2"
        mid = None
    stem = choose(rng, f"Multiply: {m(expr_tex)}", f"Which expression is equal to {m(expr_tex)}?",
                  f"Expand {m(expr_tex)}.")
    A_ = _xp1(p)
    if mid:
        sg = "-" if kind == "sq-" else ""
        midv = _poly_tex((-1 if kind == "sq-" else 1) * 2 * p * a * x)
        steps = [f"Use the pattern {m(pattern)} with {m(f'A = {A_}')} and {m(f'B = {a}')}.",
                 f"{m(f'A^2 = ({A_})^{{2}} = {_poly_tex(p * p * x**2)}')}, "
                 f"{m(f'{sg}2AB = {sg}2({A_})({a}) = {midv}')}, and {m(f'B^2 = {a}^{{2}} = {a * a}')}.",
                 f"So {m(f'{expr_tex} = {_poly_tex(ans)}')}."]
    else:
        steps = [f"This is a sum times a difference of the same two terms, so use {m(pattern)} "
                 f"with {m(f'A = {A_}')} and {m(f'B = {a}')}.",
                 f"The middle terms cancel ({m(f'+{_poly_tex(p * a * x)}')} and {m(f'-{_poly_tex(p * a * x)}')}), leaving "
                 f"{m(f'({A_})^{{2}} - {a}^{{2}} = {_poly_tex(ans)}')}."]
    return _choice_problem(stem, ans, wrong, steps, f, fmt=_pfmt,
                           tip="Check with $x = 1$: the original and your answer must give the same number.")


@template("MK")
def poly_vocab(rng, lvl):
    k = rng.choice([3, 3, 4])
    exps = rng.sample(range(0, 9), k)
    need(max(exps) != exps[0] and max(exps) >= 2)
    coefs = [rng.choice([v for v in range(-9, 10) if v not in (0,)]) for _ in exps]
    lead = coefs[exps.index(max(exps))]
    need(lead not in (1, -1) and coefs[0] != lead)
    terms = []
    for c, e in zip(coefs, exps):
        terms.append((c, "" if e == 0 else ("x" if e == 1 else f"x^{{{e}}}")))
    out = ""
    for c, v in terms:
        mag = abs(c)
        body = v if (v and mag == 1) else str(mag) + v
        out = (("-" if c < 0 else "") + body) if not out else out + (" - " if c < 0 else " + ") + body
    poly = sum(c * x**e for c, e in zip(coefs, exps))
    P = sp.Poly(poly, x)
    ask = rng.choice(["degree", "lead"])
    if ask == "degree":
        ans = max(exps)
        wrong = [(Q(exps[0]), "gives the exponent of the first term written, not the highest exponent"),
                 (Q(k), "counts the terms"),
                 (Q(sum(exps)), "adds all the exponents"),
                 (Q(lead), "gives the leading coefficient instead of the degree"),
                 (Q(max(coefs)), "gives the largest coefficient instead of the largest exponent")]
        steps = [f"The degree is the \\emph{{highest}} exponent, no matter where the term is written.",
                 f"The exponents are {', '.join(m(e) for e in exps)}. The highest is {m(ans)}."]
        chk = P.degree()
        stem = f"What is the degree of the polynomial {m(out)}?"
    else:
        ans = lead
        wrong = [(Q(coefs[0]), "takes the coefficient of the first term written"),
                 (Q(max(exps)), "gives the degree instead of the coefficient"),
                 (Q(-lead), "has the wrong sign; the sign is part of the coefficient"),
                 (Q(max(coefs, key=abs)) if max(coefs, key=abs) != lead else Q(coefs[-1]), "picks the coefficient with the largest size")]
        steps = [f"Rewrite in standard form (highest exponent first): {m(_poly_tex(poly))}.",
                 f"The leading coefficient is the number in front of the highest-power term, {m(_mtex(lead, max(exps)))}: "
                 f"it is {m(ans)}, sign included."]
        chk = P.LC()
        stem = f"What is the leading coefficient of {m(out)}?"
    return Problem(stem=stem, answer=Q(ans), fmt=num, wrong=wrong, steps=steps,
                   check=Q(chk), neg_ok=True, near=lambda r: [])


@template("MK")
def divide_by_monomial(rng, lvl):
    d = rng.randint(2, 6)
    k = rng.choice([1, 1, 2]) if lvl >= 3 else 1
    A = d * rng.randint(1, 6)
    B = d * rng.choice([v for v in range(-6, 7) if v != 0])
    C = d * rng.choice([v for v in range(-6, 7) if v != 0])
    top = A * x**(k + 2) + B * x**(k + 1) + C * x**k
    ans = sp.expand(top / (d * x**k))
    div = _mtex(d, k)
    stem = choose(rng, f"Simplify: {m(F(_poly_tex(top), div))}",
                  f"Divide {m(_poly_tex(top))} by {m(div)}. (Assume $x \\ne 0$.)")
    wrong = [(Q(A) / d * x**(k + 2) + Q(B) / d * x**(k + 1) + Q(C) / d * x**k,
              "divides the coefficients but forgets to subtract the exponents"),
             (Q(A) / d * x**2 + Q(B) / d * x, f"drops the last term, but {m(F(_mtex(C, k), div))} is {m(tx(Q(C) / d))}, not 0"),
             (Q(A) / d * x**2 + Q(B) / d * x + Q(C) / d * x, f"leaves an {m('x')} on the last term"),
             (Q(A) / d * x**2 + B * x + C, f"divides only the first term by {m(div)}")]
    steps = [f"Divide \\emph{{each}} term of the top by {m(div)}.",
             f"{m(f'{F(_mtex(A, k + 2), div)} = {_mtex(Q(A) / d, 2)}')}, "
             f"{m(f'{F(_mtex(B, k + 1), div)} = {_mtex(Q(B) / d, 1)}')}, and "
             f"{m(f'{F(_mtex(C, k), div)} = {tx(Q(C) / d)}')}.",
             f"So the result is {m(_poly_tex(ans))}."]
    f = lambda t, u: (A * t**(k + 2) + B * t**(k + 1) + C * t**k) / (d * t**k)
    return _choice_problem(stem, ans, wrong, steps, f, fmt=_pfmt)


@template("MK")
def binomial_trinomial(rng, lvl):
    a = rng.choice([v for v in range(-6, 7) if v != 0])
    b = rng.choice([v for v in range(-6, 7) if v != 0])
    c = rng.choice([v for v in range(-9, 10) if v != 0])
    ans = sp.expand((x + a) * (x**2 + b * x + c))
    need(all(ans.coeff(x, k) != 0 for k in range(4)))
    L1, L2 = _bin(1, a), _poly_tex(x**2 + b * x + c)
    part1 = sp.expand(x * (x**2 + b * x + c))
    part2 = sp.expand(a * (x**2 + b * x + c))
    steps = [f"Multiply each term of {m(f'({L1})')} by every term of {m(f'({L2})')}.",
             f"{m(f'x({L2}) = {_poly_tex(part1)}')}.",
             f"{m(f'{_par(a)}({L2}) = {_poly_tex(part2)}')}.",
             f"Add and combine like terms: {m(f'{_poly_tex(part1)} {_sgn_poly(part2)} = {_poly_tex(ans)}')}."]
    if rng.random() < 0.5:
        stem = choose(rng, f"Multiply: {m(f'({L1})({L2})')}", f"Which expression is equal to {m(f'({L1})({L2})')}?")
        wrong = [(x**3 + b * x**2 + c * x + a * c, f"multiplies {m(a)} by only {m(c)}, the last term of the trinomial"),
                 (sp.expand(ans - 2 * a * b * x), "makes a sign error combining the $x$-terms"),
                 (x**3 + (a + b) * x**2 + a * c, "drops the $x$-terms"),
                 (sp.expand(ans - 2 * a * x**2), "makes a sign error combining the $x^2$-terms")]
        f = lambda t, u: (t + a) * (t**2 + b * t + c)
        return _choice_problem(stem, ans, wrong, steps, f, fmt=_pfmt)
    which = rng.choice([1, 2])
    co = ans.coeff(x, which)
    term = "x" if which == 1 else "x^2"
    stem = f"When {m(f'({L1})({L2})')} is multiplied out and simplified, what is the coefficient of {m(term)}?"
    if which == 2:
        wrong = [(Q(b), f"uses only the {m('x^2')}-term from {m(f'x({L2})')}"),
                 (Q(a), f"uses only the {m('x^2')}-term from {m(f'{_par(a)}({L2})')}"),
                 (Q(a * b), "multiplies the numbers instead of adding the like terms"),
                 (Q(b - a), "subtracts instead of adding the like terms")]
    else:
        wrong = [(Q(c), f"uses only the {m('x')}-term from {m(f'x({L2})')}"),
                 (Q(a * b), f"uses only the {m('x')}-term from {m(f'{_par(a)}({L2})')}"),
                 (Q(a * c), "gives the constant term instead"),
                 (Q(c - a * b), "subtracts instead of adding the like terms")]
    return Problem(stem=stem, answer=Q(co), fmt=num, wrong=wrong, steps=steps,
                   check=Q(sp.Poly((x + a) * (x**2 + b * x + c), x).coeff_monomial(x**which)),
                   neg_ok=True)


def _sgn_poly(e):
    t = _poly_tex(e)
    return f"- {t[1:]}" if t.startswith("-") else f"+ {t}"


@template("MK")
def negative_exponents(rng, lvl):
    kind = rng.choice(["single", "quot", "prod"])
    if kind == "single":
        c = rng.randint(2, 9)
        k = rng.randint(1, 5)
        ans = Q(c) / x**k
        given = f"{c}x^{{-{k}}}"
        stem = choose(rng, f"Which expression is equal to {m(given)}?", f"Rewrite {m(given)} using only positive exponents.")
        wrong = [(1 / (c * x**k), f"moves the coefficient {m(c)} to the bottom too, but the exponent belongs only to {m('x')}"),
                 (-c * x**k, "treats the negative exponent as a negative number"),
                 (c * x**k, "just drops the negative sign"),
                 (Q(1) / (c * x)**k if k > 1 else -Q(c) / x**k, None)]
        steps = [f"A negative exponent means ``one over'': {m(f'x^{{-{k}}} = {F(1, _xp(k))}')}.",
                 f"The exponent applies only to {m('x')}, not to the {m(c)}: {m(f'{given} = {c} \\cdot {F(1, _xp(k))} = {F(c, _xp(k))}')}."]
        f = lambda t, u: c * t**(-k)
    elif kind == "quot":
        p, q = rng.randint(1, 5), rng.randint(1, 5)
        r, s = rng.randint(1, 5), rng.randint(1, 5)
        top = f"{_xp(p)}y^{{-{q}}}"
        bot = f"x^{{-{r}}}{_xp(s, 'y')}"
        ans = x**(p + r) / y**(q + s)
        stem = choose(rng, f"Simplify {m(F(top, bot))} and write the answer with positive exponents.",
                      f"Which expression is equal to {m(F(top, bot))}?")
        wrong = [(x**(p - r) * y**(q - s), "ignores the negative signs and just subtracts the exponents"),
                 (y**(q + s) / x**(p + r), "puts the variables on the wrong sides of the fraction bar"),
                 (x**(p + r) * y**(q + s), "drops the negative sign on the $y$-exponent"),
                 (x**(p * r) / y**(q * s), "multiplies the exponents instead of subtracting")]
        steps = [f"Subtract exponents of like bases (top minus bottom). For {m('x')}: "
                 f"{m(f'{p} - ({-r}) = {p + r}')}, so {m(_xp(p + r))}.",
                 f"For {m('y')}: {m(f'{-q} - {s} = {-(q + s)}')}, so {m(f'y^{{{-(q + s)}}} = {F(1, _xp(q + s, "y"))}')}.",
                 f"Together: {m(F(_xp(p + r), _xp(q + s, 'y')))}."]
        f = lambda t, u: (t**p * u**(-q)) / (t**(-r) * u**s)
    else:
        a, b = rng.randint(2, 6), rng.randint(2, 6)
        mexp = rng.randint(2, 7)
        nexp = rng.randint(1, 6)
        need(nexp != mexp)
        e = nexp - mexp
        ans = a * b * x**e
        given = f"({a}x^{{-{mexp}}})({b}{_xp(nexp)})"
        stem = choose(rng, f"Simplify {m(given)} and write the answer with positive exponents.",
                      f"Which expression is equal to {m(given)}?")
        wrong = [(a * b * x**(-mexp * nexp), "multiplies the exponents instead of adding them"),
                 (a * b * x**(nexp + mexp), "ignores the negative sign on the exponent"),
                 ((a + b) * x**e, "adds the coefficients instead of multiplying them"),
                 (Q(a * b) * x**(-e) if e != 0 else a * b * x, "subtracts the exponents in the wrong order")]
        res = (f"{_xp(e)}" if e > 0 else F(1, _xp(-e)))
        steps = [f"Multiply the coefficients: {m(f'{a} \\cdot {b} = {a * b}')}.",
                 f"Add the exponents: {m(f'x^{{-{mexp}}} \\cdot x^{{{nexp}}} = x^{{-{mexp} + {nexp}}} = x^{{{e}}}')}"
                 + (f", and {m(f'x^{{{e}}} = {F(1, _xp(-e))}')}" if e < 0 else "") + ".",
                 f"So the product is {m(_mtex(a * b, e) if e > 0 else F(a * b, _xp(-e)))}."]
        f = lambda t, u: (a * t**(-mexp)) * (b * t**nexp)
    return _choice_problem(stem, ans, wrong, steps, f)


PLAN = [
    # (template, level, count)  -- easy -> hard; 25 problems
    (add_sub_poly, 1, 2),
    (mult_monomials, 1, 2),
    (quotient_rule, 1, 2),
    (poly_vocab, 1, 2),
    (add_sub_poly, 2, 2),
    (power_rule, 2, 2),
    (foil, 2, 2),
    (special_products, 2, 2),
    (divide_by_monomial, 2, 1),
    (mult_monomials, 2, 1),
    (power_rule, 3, 1),
    (foil, 3, 1),
    (special_products, 3, 1),
    (binomial_trinomial, 3, 2),
    (negative_exponents, 3, 2),
]
