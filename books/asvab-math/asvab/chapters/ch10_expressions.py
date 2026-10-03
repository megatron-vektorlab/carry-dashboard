"""Chapter 10 - Algebraic Expressions."""
import re
from fractions import Fraction

import sympy as sp

from ..core import (R, Q, Problem, need, num, dec, money, m, F, tx, dec_raw,
                    int_raw, frac_raw, person, soldier, choose, template)

NUM = 10
TITLE = "Algebraic Expressions"
PART = 2

INTRO = r"""
An \emph{algebraic expression} combines numbers and letters (variables) with
operations, such as $3x + 5$ or $2a^2 - 3b$. This chapter covers the four
skills the test checks most: plugging in values, combining like terms,
distributing, and turning words into expressions.

\begin{concept}{Vocabulary}
In $4x^2 - 7x + 9$ there are three \emph{terms}. The number in front of a
variable is its \emph{coefficient} ($4$ and $-7$); $9$ is the
\emph{constant}. \emph{Like terms} have exactly the same variable part:
$5x$ and $-2x$ are like terms, but $5x$ and $5x^2$ are not, and neither are
$3x$ and $3y$.
\end{concept}

\begin{concept}{Evaluating: substitute, then follow the order of operations}
Replace each variable with its value \emph{in parentheses}, then do powers,
then multiplication, then addition and subtraction. For $a = -2$ and $b = 4$:
\[ 2a^2 - 3b = 2(-2)^2 - 3(4) = 2(4) - 12 = 8 - 12 = -4. \]
Note that $(-2)^2 = 4$, but $-x^2$ with $x = 2$ is $-(2^2) = -4$.
\end{concept}

\begin{concept}{Simplifying}
\begin{itemize}
\item Combine like terms by adding their coefficients:
  $5x + 3y - 2x + 7y = 3x + 10y$.
\item Distribute: multiply \emph{every} term inside the parentheses, signs
  included. $-2(x + 5) = -2x - 10$ and $-(x - 4) = -x + 4$.
\end{itemize}
\end{concept}

\begin{concept}{Words into symbols}
\begin{tabular}{@{}ll@{}}
sum, more than, increased by & $+$\\
difference, less than, decreased by & $-$\\
product, times, twice & $\times$\\
quotient, divided by, half of & $\div$
\end{tabular}

``$5$ less than twice a number'' is $2n - 5$: \emph{less than} reverses the
order, so it is \emph{not} $5 - 2n$.
\end{concept}

\begin{example}{Worked example}
Simplify $3(2x - 4) - 2(x + 5)$.

\textbf{Solution.} Distribute each number: $3(2x - 4) = 6x - 12$ and
$-2(x + 5) = -2x - 10$. Combine like terms:
$6x - 2x = 4x$ and $-12 - 10 = -22$. The result is $4x - 22$.
\end{example}

\begin{tip}
Check a simplification by plugging in an easy number. With $x = 1$:
$3(2 - 4) - 2(1 + 5) = -6 - 12 = -18$, and $4(1) - 22 = -18$ too.
\end{tip}

\begin{trap}
\begin{itemize}
\item Squaring a negative without parentheses: $(-3)^2 = 9$, not $-9$.
\item Distributing a minus sign to only the first term:
  $-2(x + 5)$ is $-2x - 10$, not $-2x + 10$.
\item Combining unlike terms: $3x + 4y$ cannot become $7xy$.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# private helpers
# --------------------------------------------------------------------------

def _py(v: str) -> str:
    """'x^2' -> 'x**2', 'xy' -> 'x*y' (for sympy)."""
    v = v.replace("^", "**").replace("{", "").replace("}", "")
    return re.sub(r"([a-z])(?=[a-z])", r"\1*", v)


def _lin(terms) -> str:
    """[(4, 'x'), (-22, '')] -> '4x - 22'. Terms are shown in the order given."""
    out = []
    for c, v in terms:
        c = Q(c)
        if c == 0:
            continue
        mag = abs(c)
        body = ("" if (mag == 1 and v) else tx(mag)) + v
        if not out:
            out.append(("-" if c < 0 else "") + body)
        else:
            out.append(("- " if c < 0 else "+ ") + body)
    return " ".join(out) if out else "0"


def _sym(terms):
    return sum((Q(c) * (sp.sympify(_py(v)) if v else 1) for c, v in terms), sp.Integer(0))


def _choices(ans_sym, wrongs):
    """wrongs: [(tex, sympy, why)] -> [(choice text, why)], dropping any that equal the answer."""
    out, seen = [], [ans_sym]
    for t, s, why in wrongs:
        if any(sp.simplify(s - u) == 0 for u in seen):
            continue
        seen.append(s)
        out.append((m(t), why))
    return out


def _p(v) -> str:
    """Value in parentheses for substitution: (−2), (4)."""
    return f"({int_raw(v)})"


def _signed(vals) -> str:
    """[8, -12, 15] -> '8 - 12 + 15'."""
    s = int_raw(vals[0])
    for v in vals[1:]:
        s += (" - " if v < 0 else " + ") + int_raw(abs(v))
    return s


# monomial terms for evaluate_expr: (coef, ((var, power), ...))
def _term_tex(c, fac, first):
    body = "".join(v + (f"^{p}" if p > 1 else "") for v, p in fac)
    mag = abs(c)
    coef = "" if (mag == 1 and fac) else int_raw(mag)
    sign = ("-" if c < 0 else "") if first else ("- " if c < 0 else "+ ")
    return sign + coef + body


def _expr_tex(terms):
    return " ".join(_term_tex(c, fac, i == 0) for i, (c, fac) in enumerate(terms))


def _term_val(c, fac, vals, mistake=None):
    """Value of one term; mistake alters how it is computed."""
    v = Fraction(c)
    for var, p in fac:
        x = vals[var]
        if mistake == "negsq" and x < 0 and p % 2 == 0:
            v *= -(abs(x) ** p)
        elif mistake == "coefsq" and p == 2 and abs(c) != 1:
            v = Fraction(c) ** 2 * x ** 2 if len(fac) == 1 else v * x ** p
        else:
            v *= Fraction(x) ** p
    if mistake == "negprod":
        v = -v
    return v


# --------------------------------------------------------------------------
# templates
# --------------------------------------------------------------------------

_L1_SHAPES = ["ax+b", "ax-b", "x2+b", "ax+by", "a(x+b)"]
_L2_SHAPES = ["ca2-db", "x2-dx", "cx2+dx", "a2-b2", "dx-ey"]
_L3_SHAPES = ["-x2-dx+e", "cab-b2", "a2-2ab", "cx2-dxy"]


@template("MK")
def evaluate_expr(rng, lvl):
    if lvl == 1:
        shape = rng.choice(_L1_SHAPES)
        a, b = rng.randint(2, 9), rng.randint(1, 15)
        xv, yv = rng.randint(2, 9), rng.randint(2, 9)
        if shape == "a(x+b)":
            ans = Q(a * (xv + b))
            tex = f"{a}(x + {b})"
            vals_t = f"{m(f'x = {xv}')}"
            wrong = [
                (Q(a * xv + b), f"multiplies only {m('x')} by {a}, not the whole sum"),
                (Q(a + xv + b), f"adds {a} instead of multiplying"),
                (Q(a * xv * b), None),
                (Q(a * (xv + b) + a), None),
            ]
            steps = [
                f"Substitute {m(f'x = {xv}')}: {m(f'{a}({xv} + {b})')}.",
                f"Parentheses first: {m(f'{xv} + {b} = {xv + b}')}. Then multiply: {m(f'{a} \\times {xv + b} = {int_raw(ans)}')}.",
            ]
            sym = a * (sp.Symbol("x") + b)
            subs = {sp.Symbol("x"): xv}
        else:
            if shape == "ax+b":
                terms = [(a, (("x", 1),)), (b, ())]
            elif shape == "ax-b":
                need(a * xv > b)
                terms = [(a, (("x", 1),)), (-b, ())]
            elif shape == "x2+b":
                terms = [(1, (("x", 2),)), (b, ())]
            else:
                c = rng.randint(2, 9)
                need(c != a)
                terms = [(a, (("x", 1),)), (c, (("y", 1),))]
            vals = {"x": xv, "y": yv}
            tex = _expr_tex(terms)
            ans = Q(sum(_term_val(c, f, vals) for c, f in terms))
            vals_t = f"{m(f'x = {xv}')}" + (f" and {m(f'y = {yv}')}" if shape == "ax+by" else "")
            wrong = []
            if shape in ("ax+b", "ax-b"):
                sgn = 1 if shape == "ax+b" else -1
                wrong += [
                    (Q(10 * a + xv + sgn * b), f"reads {m(f'{a}x')} as the two-digit number {m(f'{a}{xv}')}"),
                    (Q(a + xv + sgn * b), f"adds {a} and {xv} instead of multiplying"),
                    (Q(a * (xv + sgn * b)), f"{'adds' if sgn > 0 else 'subtracts'} before multiplying"),
                    (Q(a * xv - sgn * b), None),
                ]
            elif shape == "x2+b":
                wrong += [
                    (Q(2 * xv + b), f"multiplies {xv} by 2 instead of squaring it"),
                    (Q((xv + b) ** 2), "adds before squaring"),
                    (Q(xv * xv - b), None),
                    (Q(xv + b), None),
                ]
            else:
                wrong += [
                    (Q(a * yv + c * xv), f"swaps the values of {m('x')} and {m('y')}"),
                    (Q(a + xv + c + yv), "adds the numbers instead of multiplying"),
                    (Q((a + c) * (xv + yv)), None),
                    (Q(a * xv * c * yv), None),
                ]
            sym = _sym([(c, "".join(v + (f"^{p}" if p > 1 else "") for v, p in f)) for c, f in terms])
            subs = {sp.Symbol("x"): xv, sp.Symbol("y"): yv}
            sub_txt = " ".join(
                (("-" if c < 0 else "") if i == 0 else ("- " if c < 0 else "+ "))
                + ("" if (abs(c) == 1 and f) else int_raw(abs(c)))
                + "".join(_p(vals[v]) + (f"^{p}" if p > 1 else "") for v, p in f)
                for i, (c, f) in enumerate(terms))
            parts = [int(_term_val(c, f, vals)) for c, f in terms]
            steps = [
                f"Substitute {vals_t}: {m(sub_txt)}.",
                f"{'Find the power, then multiply' if shape == 'x2+b' else 'Multiply first'}: {m(_signed(parts))}.",
                f"Then add or subtract: {m(f'{_signed(parts)} = {int_raw(ans)}')}.",
            ]
        return Problem(
            stem=choose(rng, f"What is the value of {m(tex)} when {vals_t}?",
                        f"If {vals_t}, what is the value of {m(tex)}?",
                        f"Evaluate {m(tex)} for {vals_t}."),
            answer=ans,
            fmt=num,
            wrong=wrong,
            steps=steps,
            check=sym.subs(subs),
        )

    # levels 2 and 3: negative values
    shape = rng.choice(_L2_SHAPES if lvl == 2 else _L3_SHAPES)
    c, d, e = rng.randint(2, 5), rng.randint(2, 7), rng.randint(1, 12)
    neg = lambda: -rng.randint(1, 5)
    pos = lambda: rng.randint(2, 6)
    if shape == "ca2-db":
        terms, vals = [(c, (("a", 2),)), (-d, (("b", 1),))], {"a": neg(), "b": pos()}
        need(vals["a"] != -1)
    elif shape == "x2-dx":
        terms, vals = [(1, (("x", 2),)), (-d, (("x", 1),))], {"x": neg()}
    elif shape == "cx2+dx":
        terms, vals = [(c, (("x", 2),)), (d, (("x", 1),))], {"x": neg()}
    elif shape == "a2-b2":
        terms, vals = [(1, (("a", 2),)), (-1, (("b", 2),))], {"a": pos(), "b": neg()}
        need(abs(vals["b"]) != vals["a"])
    elif shape == "dx-ey":
        terms, vals = [(d, (("x", 1),)), (-c, (("y", 1),))], {"x": pos(), "y": neg()}
    elif shape == "-x2-dx+e":
        terms, vals = [(-1, (("x", 2),)), (-d, (("x", 1),)), (e, ())], {"x": neg()}
        need(vals["x"] != -1)
    elif shape == "cab-b2":
        terms, vals = [(c, (("a", 1), ("b", 1))), (-1, (("b", 2),))], {"a": neg(), "b": neg()}
    elif shape == "a2-2ab":
        terms, vals = [(1, (("a", 2),)), (-2, (("a", 1), ("b", 1)))], {"a": pos(), "b": neg()}
    else:
        terms, vals = [(c, (("x", 2),)), (-d, (("x", 1), ("y", 1)))], {"x": neg(), "y": pos()}
    tex = _expr_tex(terms)
    parts = [_term_val(cc, f, vals) for cc, f in terms]
    ans = Q(sum(parts))
    wrong = []

    def alt(kind, why, which=None):
        tot = Fraction(0)
        hit = False
        for i, (cc, f) in enumerate(terms):
            use = kind if (which is None or which == i) else None
            v_ok = _term_val(cc, f, vals)
            v_bad = _term_val(cc, f, vals, use)
            if v_bad != v_ok:
                hit = True
            tot += v_bad
        if hit:
            wrong.append((Q(tot), why))

    negvars = [v for v in vals if vals[v] < 0]
    for v in negvars:
        if any(var == v and p == 2 for _, f in terms for var, p in f):
            alt("negsq", f"treats {m(f'({vals[v]})^2')} as {m(int_raw(-(vals[v] ** 2)))}")
            break
    for i, (cc, f) in enumerate(terms):
        if abs(cc) != 1 and len(f) == 1 and f[0][1] == 2:
            alt("coefsq", f"squares {m(f'{abs(cc)}{f[0][0]}')} instead of only {m(f[0][0])}", which=i)
    for i, (cc, f) in enumerate(terms):
        odd_neg = sum(1 for var, p in f if vals[var] < 0 and p % 2 == 1)
        if cc < 0 and odd_neg % 2 == 1:
            alt("negprod", "forgets that a negative times a negative is positive", which=i)
            break
    for i, (cc, f) in enumerate(terms):
        if cc == -1 and len(f) == 1 and f[0][1] == 2:
            alt("negprod", f"reads {m(f'-{f[0][0]}^2')} as {m(f'(-{f[0][0]})^2')}; the exponent applies only to {m(f[0][0])}",
                which=i)
    wrong.append((ans + 2 * abs(parts[-1]) if parts[-1] else ans + 4, None))
    wrong.append((-ans if ans != 0 else Q(1), None))

    vals_t = " and ".join(m(f"{v} = {int_raw(vals[v])}") for v in sorted(vals))
    sub_txt = " ".join(
        (("-" if cc < 0 else "") if i == 0 else ("- " if cc < 0 else "+ "))
        + ("" if (abs(cc) == 1 and f) else int_raw(abs(cc)))
        + "".join(_p(vals[v]) + (f"^{p}" if p > 1 else "") for v, p in f)
        for i, (cc, f) in enumerate(terms))
    powers = []
    for v in sorted(vals):
        for _, f in terms:
            for var, p in f:
                if var == v and p > 1:
                    t = f"({int_raw(vals[v])})^{p} = {int_raw(vals[v] ** p)}"
                    if t not in powers:
                        powers.append(t)
    steps = [f"Substitute, putting each value in parentheses: {m(sub_txt)}."]
    if powers:
        steps.append("Powers first: " + ", ".join(m(t) for t in powers) + ".")
    steps.append(f"Multiply each term (watch the signs): {m(_signed([int(v) for v in parts]))}.")
    steps.append(f"Add and subtract from left to right: {m(f'{_signed([int(v) for v in parts])} = {int_raw(ans)}')}.")
    syms = {v: sp.Symbol(v) for v in vals}
    sym = sum(cc * sp.Mul(*[syms[var] ** p for var, p in f]) for cc, f in terms)
    return Problem(
        stem=choose(rng, f"What is the value of {m(tex)} when {vals_t}?",
                    f"If {vals_t}, what is the value of {m(tex)}?",
                    f"Evaluate {m(tex)} for {vals_t}."),
        answer=ans,
        fmt=num,
        neg_ok=True,
        wrong=wrong,
        steps=steps,
        check=sym.subs({syms[v]: vals[v] for v in vals}),
    )


@template("MK")
def combine_like(rng, lvl):
    if lvl == 1:
        u, w = rng.choice([("x", "y"), ("a", "b"), ("m", "n"), ("x", "y")])
        p1, p2 = rng.randint(2, 9), rng.choice([-1, 1]) * rng.randint(1, 9)
        q1, q2 = rng.randint(1, 9), rng.choice([-1, 1]) * rng.randint(1, 9)
        need(p1 + p2 != 0 and q1 + q2 != 0 and (p2 < 0 or q2 < 0))
        order = [(p1, u), (q1, w), (p2, u), (q2, w)]
        tex = _lin(order)
        ans_terms = [(p1 + p2, u), (q1 + q2, w)]
        ans_sym = _sym(ans_terms)
        wrongs = []
        if p2 < 0:
            wrongs.append((_lin([(p1 - p2, u), (q1 + q2, w)]), _sym([(p1 - p2, u), (q1 + q2, w)]),
                           f"ignores the minus sign in front of {m(_lin([(abs(p2), u)]))}"))
        if q2 < 0:
            wrongs.append((_lin([(p1 + p2, u), (q1 - q2, w)]), _sym([(p1 + p2, u), (q1 - q2, w)]),
                           f"ignores the minus sign in front of {m(_lin([(abs(q2), w)]))}"))
        tot = p1 + p2 + q1 + q2
        if tot != 0:
            wrongs.append((_lin([(tot, u + w)]), _sym([(tot, u + w)]),
                           f"combines unlike terms; {m(u)}-terms and {m(w)}-terms cannot be added together"))
        wrongs.append((_lin([(p1 + q1, u), (p2 + q2, w)]), _sym([(p1 + q1, u), (p2 + q2, w)]),
                       "adds terms by their position instead of by their variable"))
        wrongs.append((_lin([(p1 + p2 + 1, u), (q1 + q2, w)]), _sym([(p1 + p2 + 1, u), (q1 + q2, w)]), None))
        steps = [
            f"Group the like terms: {m(u)}-terms {m(_lin([(p1, u), (p2, u)]))} and {m(w)}-terms {m(_lin([(q1, w), (q2, w)]))}.",
            f"Add the coefficients: {m(f'{p1} {"+" if p2 > 0 else "-"} {abs(p2)} = {p1 + p2}')} and "
            f"{m(f'{q1} {"+" if q2 > 0 else "-"} {abs(q2)} = {q1 + q2}')}.",
            f"The simplified expression is {m(_lin(ans_terms))}.",
        ]
        X, Y = sp.Symbol(u), sp.Symbol(w)
        check_expr = sp.expand(p1 * X + q1 * Y + p2 * X + q2 * Y)
        check_tex = m(_lin([(check_expr.coeff(X), u), (check_expr.coeff(Y), w)]))
    else:
        A, B = rng.randint(2, 7), rng.randint(1, 8)
        C, D = rng.choice([-1, 1]) * rng.randint(1, 6), rng.choice([-1, 1]) * rng.randint(1, 8)
        E = rng.choice([-1, 1]) * rng.randint(1, 9)
        need(A + C != 0 and B + D != 0 and (C < 0 or D < 0) and A + C != 1)
        order = [(A, "x^2"), (B, "x"), (C, "x^2"), (D, "x"), (E, "")]
        tex = _lin(order)
        ans_terms = [(A + C, "x^2"), (B + D, "x"), (E, "")]
        ans_sym = _sym(ans_terms)
        wrongs = []
        allx2 = A + B + C + D
        if allx2 != 0:
            wrongs.append((_lin([(allx2, "x^2"), (E, "")]), _sym([(allx2, "x^2"), (E, "")]),
                           f"treats {m('x^2')} and {m('x')} as like terms"))
        if C < 0:
            wrongs.append((_lin([(A - C, "x^2"), (B + D, "x"), (E, "")]), _sym([(A - C, "x^2"), (B + D, "x"), (E, "")]),
                           f"ignores the minus sign in front of {m(_lin([(abs(C), 'x^2')]))}"))
        if D < 0:
            wrongs.append((_lin([(A + C, "x^2"), (B - D, "x"), (E, "")]), _sym([(A + C, "x^2"), (B - D, "x"), (E, "")]),
                           f"ignores the minus sign in front of {m(_lin([(abs(D), 'x')]))}"))
        wrongs.append((_lin([(A + C, "x^3"), (B + D, "x"), (E, "")]), _sym([(A + C, "x^3"), (B + D, "x"), (E, "")]),
                       "adds the exponents when combining like terms"))
        wrongs.append((_lin([(A + C, "x^2"), (B + D + E, "x")]), _sym([(A + C, "x^2"), (B + D + E, "x")]),
                       f"adds the constant {m(int_raw(E))} to the {m('x')}-terms"))
        steps = [
            f"Like terms have the same variable part. The {m('x^2')}-terms are {m(_lin([(A, 'x^2'), (C, 'x^2')]))}; "
            f"the {m('x')}-terms are {m(_lin([(B, 'x'), (D, 'x')]))}; the constant is {m(int_raw(E))}.",
            f"Add the coefficients: {m(f'{A} {"+" if C > 0 else "-"} {abs(C)} = {A + C}')} and "
            f"{m(f'{B} {"+" if D > 0 else "-"} {abs(D)} = {B + D}')}. The exponent stays the same.",
            f"The simplified expression is {m(_lin(ans_terms))}.",
        ]
        X = sp.Symbol("x")
        ce = sp.Poly(sp.expand(A * X ** 2 + B * X + C * X ** 2 + D * X + E), X)
        check_tex = m(_lin([(ce.coeff_monomial(X ** 2), "x^2"), (ce.coeff_monomial(X), "x"), (ce.coeff_monomial(1), "")]))
    return Problem(
        stem=choose(rng, f"Simplify: {m(tex)}", f"Which expression is equivalent to {m(tex)}?",
                    f"Combine like terms: {m(tex)}"),
        answer=m(_lin(ans_terms)),
        fmt=lambda s: s,
        wrong=_choices(ans_sym, wrongs),
        steps=steps,
        check=check_tex,
    )


@template("MK")
def distribute(rng, lvl):
    X = sp.Symbol("x")
    if lvl == 2:
        a, d = rng.randint(2, 6), rng.randint(2, 6)
        b, e = rng.randint(1, 5), rng.randint(1, 5)
        c, f = rng.choice([-1, 1]) * rng.randint(1, 9), rng.choice([-1, 1]) * rng.randint(1, 9)
        need(a * b != d * e)
        p1 = _lin([(b, "x"), (c, "")])
        p2 = _lin([(e, "x"), (f, "")])
        tex = f"{a}({p1}) - {d}({p2})"
        X1, K1 = a * b - d * e, a * c - d * f
        ans_terms = [(X1, "x"), (K1, "")]
        wrongs = [
            (_lin([(X1, "x"), (a * c + d * f, "")]), X1 * X + a * c + d * f,
             f"multiplies {m(int_raw(f))} by {m(d)} instead of {m(-d)}; the minus sign goes to every term"),
            (_lin([(X1, "x"), (c - f, "")]), X1 * X + c - f,
             "multiplies only the first term in each set of parentheses"),
            (_lin([(a * b + d * e, "x"), (a * c + d * f, "")]), (a * b + d * e) * X + a * c + d * f,
             "adds the second product instead of subtracting it"),
            (_lin([(X1, "x"), (a * c - f, "")]), X1 * X + a * c - f,
             f"forgets to multiply {m(int_raw(f))} by {d}"),
        ]
        steps = [
            f"Distribute {a}: {m(f'{a}({p1}) = {_lin([(a * b, "x"), (a * c, "")])}')}.",
            f"Distribute {m(-d)} (the minus sign comes with it): {m(f'-{d}({p2}) = {_lin([(-d * e, "x"), (-d * f, "")])}')}.",
            f"Combine like terms: {m(f'{a * b}x {"-" if d * e > 0 else "+"} {d * e}x = {_lin([(X1, "x")])}')} and "
            f"{m(f'{_signed([a * c, -d * f])} = {int_raw(K1)}')}. The result is {m(_lin(ans_terms))}.",
        ]
        sym_check = sp.expand(a * (b * X + c) - d * (e * X + f))
    else:
        kind = rng.choice(["const-minus", "bare-minus", "x-times"])
        if kind == "const-minus":
            k, d = rng.randint(5, 20), rng.randint(2, 6)
            e, f = rng.randint(1, 4), rng.choice([-1, 1]) * rng.randint(1, 9)
            need(k != d)
            p2 = _lin([(e, "x"), (f, "")])
            tex = f"{k} - {d}({p2})"
            X1, K1 = -d * e, k - d * f
            ans_terms = [(X1, "x"), (K1, "")]
            wrongs = [
                (_lin([((k - d) * e, "x"), ((k - d) * f, "")]), (k - d) * (e * X + f),
                 f"subtracts {m(f'{k} - {d}')} first; multiplication comes before subtraction"),
                (_lin([(X1, "x"), (k + d * f, "")]), X1 * X + k + d * f,
                 f"multiplies {m(int_raw(f))} by {m(d)} instead of {m(-d)}"),
                (_lin([(d * e, "x"), (k + d * f, "")]), d * e * X + k + d * f,
                 "adds the product instead of subtracting it"),
                (_lin([(X1, "x"), (k - f, "")]), X1 * X + k - f,
                 f"forgets to multiply {m(int_raw(f))} by {d}"),
            ]
            steps = [
                f"Multiplication comes before subtraction, so distribute {m(-d)} first: "
                f"{m(f'-{d}({p2}) = {_lin([(-d * e, "x"), (-d * f, "")])}')}.",
                f"Now the expression is {m(f'{k} ' + _lin([(-d * e, 'x'), (-d * f, '')]).replace('-', '- ', 1) if True else '')}"
                .replace(f"{k} - ", f"{k} - ") + ".",
                f"Combine the constants: {m(f'{_signed([k, -d * f])} = {int_raw(K1)}')}. The result is "
                f"{m(_lin(ans_terms))}.",
            ]
            sym_check = sp.expand(k - d * (e * X + f))
        elif kind == "bare-minus":
            a = rng.randint(2, 6)
            b, c = rng.randint(1, 5), rng.choice([-1, 1]) * rng.randint(1, 9)
            e, f = rng.randint(1, 5), rng.choice([-1, 1]) * rng.randint(1, 9)
            need(a * b != e)
            p1, p2 = _lin([(b, "x"), (c, "")]), _lin([(e, "x"), (f, "")])
            tex = f"{a}({p1}) - ({p2})"
            X1, K1 = a * b - e, a * c - f
            ans_terms = [(X1, "x"), (K1, "")]
            wrongs = [
                (_lin([(X1, "x"), (a * c + f, "")]), X1 * X + a * c + f,
                 "changes the sign of only the first term inside the second parentheses"),
                (_lin([(a * b + e, "x"), (a * c + f, "")]), (a * b + e) * X + a * c + f,
                 "drops the parentheses without changing any signs"),
                (_lin([(X1, "x"), (c - f, "")]), X1 * X + c - f,
                 f"multiplies only {m(_lin([(b, 'x')]))} by {a}"),
                (_lin([(X1 + 1, "x"), (K1, "")]), (X1 + 1) * X + K1, None),
            ]
            steps = [
                f"Distribute {a}: {m(f'{a}({p1}) = {_lin([(a * b, "x"), (a * c, "")])}')}.",
                f"A minus sign in front of parentheses means multiply by {m('-1')}: "
                f"{m(f'-({p2}) = {_lin([(-e, "x"), (-f, "")])}')}. \\emph{{Both}} signs change.",
                f"Combine like terms: {m(_lin(ans_terms))}.",
            ]
            sym_check = sp.expand(a * (b * X + c) - (e * X + f))
        else:
            c = rng.choice([-1, 1]) * rng.randint(1, 9)
            d = rng.randint(2, 6)
            f = rng.choice([-1, 1]) * rng.randint(1, 9)
            need(c != d)
            p1, p2 = _lin([(1, "x"), (c, "")]), _lin([(1, "x"), (f, "")])
            tex = f"x({p1}) - {d}({p2})"
            ans_terms = [(1, "x^2"), (c - d, "x"), (-d * f, "")]
            wrongs = [
                (_lin([(1, "x^2"), (c - d, "x"), (d * f, "")]), X ** 2 + (c - d) * X + d * f,
                 f"multiplies {m(int_raw(f))} by {m(d)} instead of {m(-d)}"),
                (_lin([(2 + c - d, "x"), (-d * f, "")]), (2 + c - d) * X - d * f,
                 f"writes {m('x \\cdot x')} as {m('2x')} instead of {m('x^2')}"),
                (_lin([(1, "x^2"), (c + d, "x"), (-d * f, "")]), X ** 2 + (c + d) * X - d * f,
                 f"adds {m(f'{d}x')} instead of subtracting it"),
                (_lin([(1, "x^2"), (c - d, "x"), (f, "")]), X ** 2 + (c - d) * X + f,
                 f"forgets to multiply {m(int_raw(f))} by {m(-d)}"),
            ]
            steps = [
                f"Distribute {m('x')}: {m(f'x({p1}) = {_lin([(1, "x^2"), (c, "x")])}')}.",
                f"Distribute {m(-d)}: {m(f'-{d}({p2}) = {_lin([(-d, "x"), (-d * f, "")])}')}.",
                f"Combine the {m('x')}-terms: {m(f'{_lin([(c, "x"), (-d, "x")])} = {_lin([(c - d, "x")])}')}. "
                f"The result is {m(_lin(ans_terms))}.",
            ]
            sym_check = sp.expand(X * (X + c) - d * (X + f))
    ans_sym = _sym(ans_terms)
    need(sp.expand(ans_sym - sym_check) == 0)
    P = sp.Poly(sym_check, X)
    check_tex = m(_lin([(P.coeff_monomial(X ** 2), "x^2"), (P.coeff_monomial(X), "x"), (P.coeff_monomial(1), "")]))
    return Problem(
        stem=choose(rng, f"Simplify: {m(tex)}", f"Which expression is equivalent to {m(tex)}?",
                    f"Which of the following is equal to {m(tex)}?"),
        answer=m(_lin(ans_terms)),
        fmt=lambda s: s,
        wrong=_choices(ans_sym, wrongs),
        steps=steps,
        tip=f"Check with {m('x = 1')}: the original and {m(_lin(ans_terms))} both equal "
            f"{m(int_raw(sym_check.subs(X, 1)))}.",
        check=check_tex,
    )


# phrase bank: (words with {k}/{j}, answer tex, answer sympy-able, semantic, [(wrong tex, sympy, why)])
def _phrases(k, j, lvl):
    n = sp.Symbol("n")
    if lvl == 1:
        return [
            (f"{k} more than a number", f"n + {k}", n + k, lambda v: v + k,
             [(f"{k}n", k * n, "multiplies instead of adding"),
              (f"n - {k}", n - k, "subtracts instead of adding"),
              (f"{k} - n", k - n, None)]),
            (f"{k} less than a number", f"n - {k}", n - k, lambda v: v - k,
             [(f"{k} - n", k - n, "reverses the order; \\emph{less than} means subtract from the number"),
              (f"n + {k}", n + k, "adds instead of subtracting"),
              (f"{k}n", k * n, None)]),
            (f"a number decreased by {k}", f"n - {k}", n - k, lambda v: v - k,
             [(f"{k} - n", k - n, "reverses the order of the subtraction"),
              (f"n + {k}", n + k, "adds instead of subtracting"),
              (f"{k}n", k * n, None)]),
            (f"the product of {k} and a number", f"{k}n", k * n, lambda v: k * v,
             [(f"n + {k}", n + k, "adds instead of multiplying"),
              (f"\\frac{{n}}{{{k}}}", n / k, "divides instead of multiplying"),
              (f"n - {k}", n - k, None)]),
            (f"the quotient of a number and {k}", f"\\frac{{n}}{{{k}}}", n / k, lambda v: Fraction(v, k),
             [(f"\\frac{{{k}}}{{n}}", k / n, "reverses the order of the division"),
              (f"{k}n", k * n, "multiplies instead of dividing"),
              (f"n - {k}", n - k, None)]),
            (f"{k} times a number, increased by {j}", f"{k}n + {j}", k * n + j, lambda v: k * v + j,
             [(f"{k}(n + {j})", k * (n + j), "adds before multiplying"),
              (f"{j}n + {k}", j * n + k, "swaps the two numbers"),
              (f"{k + j}n", (k + j) * n, None)]),
        ]
    return [
        (f"{j} less than {k} times a number", f"{k}n - {j}", k * n - j, lambda v: k * v - j,
         [(f"{j} - {k}n", j - k * n, "reverses the order; \\emph{less than} means subtract from the other amount"),
          (f"{k}(n - {j})", k * (n - j), "subtracts before multiplying"),
          (f"{j}n - {k}", j * n - k, "swaps the two numbers")]),
        (f"{k} times the sum of a number and {j}", f"{k}(n + {j})", k * (n + j), lambda v: k * (v + j),
         [(f"{k}n + {j}", k * n + j, "multiplies only the number, not the whole sum"),
          (f"{k} + n + {j}", k + n + j, "adds instead of multiplying"),
          (f"{k}n + {j}n", k * n + j * n, None)]),
        (f"the sum of {k} times a number and {j}", f"{k}n + {j}", k * n + j, lambda v: k * v + j,
         [(f"{k}(n + {j})", k * (n + j), "multiplies the whole sum by the number; only the number is multiplied"),
          (f"{k} + {j}n", k + j * n, "attaches the variable to the wrong number"),
          (f"{k + j}n", (k + j) * n, None)]),
        (f"{k} times the difference of a number and {j}", f"{k}(n - {j})", k * (n - j), lambda v: k * (v - j),
         [(f"{k}n - {j}", k * n - j, "multiplies only the number, not the whole difference"),
          (f"{k}({j} - n)", k * (j - n), "reverses the order of the difference"),
          (f"{k} - n - {j}", k - n - j, None)]),
        (f"{j} subtracted from twice a number", f"2n - {j}", 2 * n - j, lambda v: 2 * v - j,
         [(f"{j} - 2n", j - 2 * n, "reverses the order; \\emph{subtracted from} means take it away from the other amount"),
          (f"2(n - {j})", 2 * (n - j), "subtracts before doubling"),
          (f"n^2 - {j}", n ** 2 - j, "reads \\emph{twice} as squaring")]),
        (f"half of a number, decreased by {j}", f"\\frac{{n}}{{2}} - {j}", n / 2 - j, lambda v: Fraction(v, 2) - j,
         [(f"\\frac{{n - {j}}}{{2}}", (n - j) / 2, "subtracts before taking half"),
          (f"2n - {j}", 2 * n - j, "doubles instead of halving"),
          (f"{j} - \\frac{{n}}{{2}}", j - n / 2, "reverses the order of the subtraction")]),
        (f"the square of a number, increased by {j}", f"n^2 + {j}", n ** 2 + j, lambda v: v * v + j,
         [(f"(n + {j})^2", (n + j) ** 2, "adds before squaring"),
          (f"2n + {j}", 2 * n + j, "doubles the number instead of squaring it"),
          (f"{j}n^2", j * n ** 2, None)]),
    ]


@template("MK")
def translate(rng, lvl):
    k = rng.randint(3, 12)
    j = rng.randint(2, 15)
    need(k != j)
    bank = _phrases(k, j, lvl)
    words, ans_t, ans_s, sem, wr = rng.choice(bank)
    n = sp.Symbol("n")
    wrong = _choices(ans_s, wr + [(f"{k}n + {j + 1}" if lvl == 2 else f"n + {k + 1}",
                                   (k * n + j + 1) if lvl == 2 else n + k + 1, None)])
    lead = "Five less than" if False else words[0].upper() + words[1:]
    return Problem(
        stem=choose(rng, f"Which expression means ``{words}''?",
                    f"If {m('n')} stands for a number, which expression represents ``{words}''?",
                    f"Translate into an expression: ``{words}.''"),
        answer=m(ans_t),
        fmt=lambda s: s,
        wrong=wrong,
        steps=_translate_steps(words, ans_t, k, j),
        verify=lambda s: s == m(ans_t) and all(ans_s.subs(n, v) == sem(v) for v in range(1, 8)),
    )


def _translate_steps(words, ans_t, k, j):
    hints = {
        "more than": "\\emph{more than} means add",
        "less than": "\\emph{less than} means subtract, and the order flips: the amount after \\emph{than} comes first",
        "decreased by": "\\emph{decreased by} means subtract, in the order written",
        "product": "\\emph{product} means multiply",
        "quotient": "\\emph{quotient} means divide, in the order written",
        "increased by": "\\emph{increased by} means add",
        "sum of a number": "\\emph{the sum of a number and} groups those two together first, so use parentheses",
        "difference of a number": "\\emph{the difference of a number and} groups those two together first, so use parentheses",
        "sum of": "\\emph{the sum of A and B} means A + B",
        "subtracted from": "\\emph{A subtracted from B} means B - A: the order flips",
        "twice": "\\emph{twice} means 2 times",
        "half of": "\\emph{half of a number} means divide it by 2",
        "square of": "\\emph{the square of a number} means the number to the second power",
    }
    used = [h for key, h in hints.items() if key in words]
    # keep the specific "sum of a number" hint and drop the generic one
    if any("sum of a number" in key for key in hints if key in words):
        used = [h for h in used if not h.startswith("\\emph{the sum of A")]
    out = ["Translate the key words: " + "; ".join(used[:3]) + "."]
    out.append(f"Let {m('n')} be the number. The expression is {m(ans_t)}.")
    return out


_SHOP = [
    # (stem, price p range, price q range, items)
    ("Shirts cost {p} each and hats cost {q} each. Which expression gives the total cost, in dollars, "
     "of {X} shirts and {Y} hats?", (10, 25), (6, 15)),
    ("At a movie theater, adult tickets cost {p} and child tickets cost {q}. Which expression gives the "
     "total cost, in dollars, of {X} adult tickets and {Y} child tickets?", (9, 15), (5, 9)),
    ("A unit store sells T-shirts for {p} and pairs of socks for {q}. Which expression gives the total "
     "cost, in dollars, of {X} T-shirts and {Y} pairs of socks?", (8, 16), (2, 6)),
    ("Notebooks cost {p} each and pens cost {q} each. Which expression gives the total cost, in "
     "dollars, of {X} notebooks and {Y} pens?", (3, 8), (1, 3)),
]

_RATE = [
    ("A taxi charges {a} to start a ride plus {b} for each mile. Which expression gives the cost, "
     "in dollars, of a ride that is {M} miles long?", (3, 6), (2, 4), "m"),
    ("A phone plan costs {a} per month plus {b} for each gigabyte of data used. Which expression "
     "gives the cost, in dollars, of one month in which {M} gigabytes are used?", (25, 45), (5, 15), "g"),
    ("A plumber charges {a} for a house call plus {b} per hour of work. Which expression gives the "
     "charge, in dollars, for a job that takes {M} hours?", (40, 90), (45, 95), "h"),
    ("A gym charges a {a} sign-up fee plus {b} per month. Which expression gives the total cost, in "
     "dollars, of a membership for {M} months?", (25, 75), (20, 45), "t"),
]

_COUNT = [
    ("A supply sergeant has {M} full cases of MREs with {a} meals in each case, plus {b} loose meals. "
     "Which expression gives the total number of meals?", (12, 12), (3, 11), "c"),
    ("A warehouse worker stacks {M} pallets with {a} boxes on each pallet and then adds {b} more boxes. "
     "Which expression gives the total number of boxes?", (20, 48), (3, 15), "p"),
    ("A recruit does {a} push-ups every morning for {M} days, plus {b} extra push-ups on the last "
     "day. Which expression gives the total number of push-ups?", (20, 60), (5, 25), "d"),
]


@template("AR")
def word_expression(rng, lvl):
    if lvl == 3:
        return _word_l3(rng)
    kind = rng.choice(["shop", "rate", "count"])
    if kind == "shop":
        stem_t, (plo, phi), (qlo, qhi) = rng.choice(_SHOP)
        p, q = rng.randint(plo, phi), rng.randint(qlo, qhi)
        need(p != q)
        X, Y = sp.symbols("x y")
        ans_t, ans_s = f"{p}x + {q}y", p * X + q * Y
        wr = [
            (f"{q}x + {p}y", q * X + p * Y, "matches each price with the wrong item"),
            (f"{p + q}(x + y)", (p + q) * (X + Y), "charges both prices for every item"),
            (f"{p + q}xy", (p + q) * X * Y, "combines unlike terms"),
            (f"x + y + {p + q}", X + Y + p + q, "adds the prices instead of multiplying them by the number of items"),
        ]
        stem = stem_t.format(p=money(p), q=money(q), X=m("x"), Y=m("y"))
        steps = [
            f"Each shirt-type item costs {money(p)}, so {m('x')} of them cost {m(f'{p}x')} dollars."
            .replace("shirt-type item", "item of the first kind"),
            f"{m('y')} of the second item cost {m(f'{q}y')} dollars.",
            f"Add the two costs: {m(ans_t)}.",
        ]
        sem = lambda xv, yv: sum([p] * xv) + sum([q] * yv)
        verify = lambda s: s == m(ans_t) and all(ans_s.subs({X: a, Y: b}) == sem(a, b) for a in range(4) for b in range(4))
    elif kind == "rate":
        stem_t, (alo, ahi), (blo, bhi), v = rng.choice(_RATE)
        a, b = rng.randint(alo, ahi), rng.randint(blo, bhi)
        need(a != b)
        V = sp.Symbol(v)
        ans_t, ans_s = f"{a} + {b}{v}", a + b * V
        wr = [
            (f"{a + b}{v}", (a + b) * V, f"charges the one-time {money(a)} for every unit too"),
            (f"{a}{v} + {b}", a * V + b, "swaps the one-time charge and the rate"),
            (f"{b}({a} + {v})", b * (a + V), None),
            (f"{a} + {b} + {v}", a + b + V, f"adds {m(v)} instead of multiplying it by {money(b)}"),
        ]
        stem = stem_t.format(a=money(a), b=money(b), M=m(v))
        steps = [
            f"The {money(a)} is charged once, no matter what.",
            f"The {money(b)} is charged for each unit, so {m(v)} units cost {m(f'{b}{v}')} dollars.",
            f"Total: {m(ans_t)}.",
        ]
        sem = lambda t: a + sum([b] * t)
        verify = lambda s: s == m(ans_t) and all(ans_s.subs(V, t) == sem(t) for t in range(6))
    else:
        stem_t, (alo, ahi), (blo, bhi), v = rng.choice(_COUNT)
        a, b = rng.randint(alo, ahi), rng.randint(blo, bhi)
        need(a != b)
        V = sp.Symbol(v)
        ans_t, ans_s = f"{a}{v} + {b}", a * V + b
        wr = [
            (f"{a}({v} + {b})", a * (V + b), f"multiplies the {b} extra by {a} too"),
            (f"{b}{v} + {a}", b * V + a, "swaps the two numbers"),
            (f"{a + b}{v}", (a + b) * V, f"multiplies the {b} extra by {m(v)} too"),
            (f"{v} + {a + b}", V + a + b, f"adds {a} instead of multiplying it by {m(v)}"),
        ]
        stem = stem_t.format(a=num(a), b=num(b), M=m(v))
        steps = [
            f"{m(v)} groups of {a} make {m(f'{a}{v}')}.",
            f"Add the {b} extra: {m(ans_t)}.",
        ]
        sem = lambda t: sum([a] * t) + b
        verify = lambda s: s == m(ans_t) and all(ans_s.subs(V, t) == sem(t) for t in range(6))
    return Problem(
        stem=stem,
        answer=m(ans_t),
        fmt=lambda s: s,
        wrong=_choices(ans_s, wr),
        steps=steps,
        verify=verify,
    )


def _word_l3(rng):
    kind = rng.choice(["left", "rental", "perim"])
    if kind == "left":
        p = person(rng)
        total = rng.choice(range(40, 201, 10))
        q = rng.randint(3, 15)
        item = rng.choice(["a shirt", "a book", "a ticket", "a pizza", "a phone case"])
        X = sp.Symbol("x")
        ans_t, ans_s = f"{total} - {q}x", total - q * X
        wr = [
            (f"{q}x - {total}", q * X - total, "subtracts in the wrong order"),
            (f"{total - q}x", (total - q) * X, "subtracts the price from the starting amount first"),
            (f"{total} + {q}x", total + q * X, "adds the cost instead of subtracting it"),
            (f"{q}({total} - x)", q * (total - X), None),
        ]
        thing = item.split(" ", 1)[1]
        stem = (f"{p.name} has {money(total)}. {p.He} buys {m('x')} items that cost {money(q)} each. "
                f"Which expression gives the amount of money, in dollars, {p.he} has left?")
        steps = [f"The items cost {m(f'{q}x')} dollars in all.",
                 f"Subtract that from the starting amount: {m(ans_t)}."]
        sem = lambda t: total - sum([q] * t)
        verify = lambda s: s == m(ans_t) and all(ans_s.subs(X, t) == sem(t) for t in range(5))
    elif kind == "rental":
        a, b = rng.randint(25, 60), R(rng.randint(1, 9), 4)
        need(b.q != 1)
        D, M = sp.symbols("d m")
        bt = dec_raw(b, places=2)
        ans_t, ans_s = f"{a}d + {bt}m", a * D + b * M
        wr = [
            (f"{a}m + {bt}d", a * M + b * D, "matches each rate with the wrong quantity"),
            (f"{a} + {bt}m", a + b * M, f"charges the daily rate only once instead of {m('d')} times"),
            (f"({a} + {bt})dm", (a + b) * D * M, "multiplies everything together"),
            (f"{a}d + {bt}", a * D + b, f"forgets to multiply the mileage rate by {m('m')}"),
        ]
        stem = (f"A rental truck costs {money(a)} per day plus {money(b)} per mile. Which expression gives "
                f"the cost, in dollars, of renting the truck for {m('d')} days and driving it {m('m')} miles?")
        steps = [f"Daily charges: {m(f'{a}d')} dollars.",
                 f"Mileage charges: {m(f'{bt}m')} dollars.",
                 f"Total: {m(ans_t)}."]
        verify = lambda s: s == m(ans_t) and all(ans_s.subs({D: d_, M: m_}) == a * d_ + b * m_ for d_ in range(3) for m_ in (0, 4, 10))
    else:
        c = rng.randint(2, 9)
        two = rng.choice([2, 3])
        W = sp.Symbol("w")
        length = two * W + c
        ans_s = sp.expand(2 * length + 2 * W)
        A, B = ans_s.coeff(W), ans_s.subs(W, 0)
        ans_t = _lin([(A, "w"), (B, "")])
        wr = [
            (_lin([(two + 1, "w"), (c, "")]), (two + 1) * W + c, "adds one length and one width instead of all four sides"),
            (_lin([(A, "w"), (c, "")]), A * W + c, f"doubles the {m('w')}-terms but not the {c}"),
            (_lin([(2 * two, "w"), (2 * c, "")]), 2 * two * W + 2 * c, "counts the two lengths but forgets the two widths"),
            (_lin([(two, "w^2"), (c, "w")]), two * W ** 2 + c * W, "finds the area instead of the perimeter"),
        ]
        stem = (f"The length of a rectangle is {c} more than {('twice' if two == 2 else 'three times')} its width, "
                f"{m('w')}. Which expression gives the perimeter of the rectangle?")
        steps = [f"The length is {m(f'{two}w + {c}')}.",
                 f"Perimeter = 2(length) + 2(width) = {m(f'2({two}w + {c}) + 2w')}.",
                 f"Distribute and combine: {m(f'{2 * two}w + {2 * c} + 2w = {ans_t}')}."]
        verify = lambda s: s == m(ans_t) and all(ans_s.subs(W, t) == 2 * (two * t + c) + 2 * t for t in range(1, 6))
    return Problem(
        stem=stem,
        answer=m(ans_t),
        fmt=lambda s: s,
        wrong=_choices(ans_s, wr),
        steps=steps,
        verify=verify,
        section="AR",
    )


@template("MK")
def evaluate_formula(rng, lvl):
    if lvl == 1:
        kind = rng.choice(["perim", "tri", "dist"])
        if kind == "perim":
            l, w = rng.randint(5, 30), rng.randint(2, 20)
            need(l > w)
            ans = Q(2 * l + 2 * w)
            stem = (f"The perimeter of a rectangle is given by {m('P = 2l + 2w')}. What is {m('P')} when "
                    f"{m(f'l = {l}')} and {m(f'w = {w}')}?")
            wrong = [
                (Q(l + w), "adds one length and one width only"),
                (Q(l * w), "finds the area instead of the perimeter"),
                (Q(2 * l + w), "doubles only the length"),
                (Q(2 * (l * w)), None),
            ]
            steps = [f"Substitute: {m(f'P = 2({l}) + 2({w})')}.",
                     f"Multiply, then add: {m(f'{2 * l} + {2 * w} = {int_raw(ans)}')}."]
            check = (2 * sp.Symbol("l") + 2 * sp.Symbol("w")).subs({sp.Symbol("l"): l, sp.Symbol("w"): w})
        elif kind == "tri":
            b, h = rng.randint(3, 20), rng.randint(2, 16)
            need((b * h) % 2 == 0 and b != h)
            ans = R(b * h, 2)
            stem = (f"The area of a triangle is {m('A = \\frac{1}{2}bh')}. What is {m('A')} when "
                    f"{m(f'b = {b}')} and {m(f'h = {h}')}?")
            wrong = [
                (Q(b * h), f"forgets to multiply by {m('\\frac{1}{2}')}"),
                (R(b + h, 2), "adds the base and height instead of multiplying"),
                (Q(2 * b * h), f"multiplies by 2 instead of by {m('\\frac{1}{2}')}"),
                (ans + b, None),
            ]
            steps = [f"Substitute: {m(f'A = \\frac{{1}}{{2}}({b})({h})')}.",
                     f"Multiply: {m(f'{b} \\times {h} = {b * h}')}, and half of {num(b * h)} is {num(ans)}."]
            check = sp.Rational(1, 2) * b * h
        else:
            r = rng.choice(range(30, 66, 5))
            t = rng.choice([R(v, 2) for v in range(3, 15)])
            ans = r * t
            need(ans.is_integer or ans.q == 2)
            stem = (f"Distance traveled is given by {m('d = rt')}, where {m('r')} is the rate in miles per hour "
                    f"and {m('t')} is the time in hours. What is {m('d')} when {m(f'r = {r}')} and "
                    f"{m(f't = {dec_raw(t)}')}?")
            wrong = [
                (r + t, "adds the rate and time instead of multiplying"),
                (r / t, "divides the rate by the time"),
                (r * (t.p // t.q) if t.q != 1 else r * t + r, f"ignores the half hour" if t.q != 1 else None),
                (ans * 10, None),
            ]
            whole = t.p // t.q
            steps = [f"Substitute: {m(f'd = {r} \\times {dec_raw(t)}')}.",
                     (f"Multiply: {m(f'{r} \\times {whole} = {r * whole}')} and half of {r} is {m(dec_raw(R(r, 2)))}; "
                      f"{m(f'{r * whole} + {dec_raw(R(r, 2))} = {dec_raw(ans)}')} miles." if t.q == 2 else
                      f"Multiply: {m(f'{r} \\times {dec_raw(t)} = {dec_raw(ans)}')} miles.")]
            check = sp.Integer(r) * t
        return Problem(stem=stem, answer=ans, fmt=dec, wrong=wrong, steps=steps, check=check)

    # level 2: temperature conversion
    if rng.random() < 0.55:
        Cv = rng.choice(range(-10, 41, 5))
        need(Cv != 0)
        ans = R(9, 5) * Cv + 32
        stem = (f"The formula {m('F = \\frac{9}{5}C + 32')} converts a Celsius temperature {m('C')} to "
                f"Fahrenheit. What is {m(f'{Cv}^\\circ')}C in degrees Fahrenheit?")
        wrong = [
            (R(9, 5) * Cv, "forgets to add 32"),
            (R(9, 5) * (Cv + 32), "adds 32 before multiplying"),
            (Q(Cv + 32), f"ignores the {m('\\frac{9}{5}')}"),
            (R(5, 9) * Cv + 32, f"uses {m('\\frac{5}{9}')} instead of {m('\\frac{9}{5}')}"),
        ]
        steps = [
            f"Substitute {m(f'C = {Cv}')}: {m(f'F = \\frac{{9}}{{5}}({Cv}) + 32')}.",
            f"Multiply first: {m(f'{Cv} \\div 5 = {Cv // 5}')}, and {m(f'{Cv // 5} \\times 9 = {9 * Cv // 5}')}.",
            f"Then add: {m(f'{9 * Cv // 5} + 32 = {int_raw(ans)}')}. The temperature is {m(f'{int_raw(ans)}^\\circ')}F.",
        ]
        check = sp.solve(sp.Eq(sp.Symbol("C"), R(5, 9) * (sp.Symbol("F") - 32)).subs(sp.Symbol("C"), Cv), sp.Symbol("F"))[0]
    else:
        k = rng.choice([v for v in range(-4, 9) if v != 0])
        Fv = 32 + 9 * k
        ans = Q(5 * k)
        stem = (f"The formula {m('C = \\frac{5}{9}(F - 32)')} converts a Fahrenheit temperature {m('F')} to "
                f"Celsius. What is {m(f'{Fv}^\\circ')}F in degrees Celsius?")
        wrong = [
            (Q(Fv - 32), f"forgets to multiply by {m('\\frac{5}{9}')}"),
            (R(9, 5) * (Fv - 32), f"uses {m('\\frac{9}{5}')} instead of {m('\\frac{5}{9}')}"),
            (R(5, 9) * Fv - 32, "multiplies before subtracting 32; the parentheses come first"),
            (R(5, 9) * (Fv + 32), "adds 32 instead of subtracting it"),
        ]
        steps = [
            f"Parentheses first: {m(f'{Fv} - 32 = {Fv - 32}')}.",
            f"Multiply by {m('\\frac{5}{9}')}: {m(f'{Fv - 32} \\div 9 = {k}')}, and {m(f'{k} \\times 5 = {5 * k}')}.",
            f"The temperature is {m(f'{5 * k}^\\circ')}C.",
        ]
        check = sp.Rational(5, 9) * (Fv - 32)
    return Problem(stem=stem, answer=ans, fmt=dec, neg_ok=True, wrong=wrong, steps=steps, check=check)


@template("MK")
def formula_solve(rng, lvl):
    kind = rng.choice(["perim", "temp", "tri", "box"])
    if kind == "perim":
        l, w = rng.randint(6, 30), rng.randint(2, 20)
        need(l > w)
        P = 2 * l + 2 * w
        ans = Q(w)
        stem = (f"The perimeter of a rectangle is {m('P = 2l + 2w')}. If {m(f'P = {P}')} and {m(f'l = {l}')}, "
                f"what is {m('w')}?")
        wrong = [
            (Q(2 * w), "forgets to divide by 2"),
            (Q(P - l), f"subtracts {m('l')} only once and stops"),
            (R(P - l, 2), f"subtracts {m('l')} only once before dividing by 2"),
            (R(P, 2), f"divides {m('P')} by 2 and forgets to subtract the length"),
        ]
        steps = [f"Substitute: {m(f'{P} = 2({l}) + 2w')}, so {m(f'{P} = {2 * l} + 2w')}.",
                 f"Subtract {2 * l}: {m(f'2w = {P - 2 * l}')}.",
                 f"Divide by 2: {m(f'w = {w}')}."]
        W = sp.Symbol("w")
        check = sp.solve(sp.Eq(P, 2 * l + 2 * W), W)[0]
    elif kind == "temp":
        k = rng.choice([v for v in range(-2, 9) if v != 0])
        Cv = 5 * k
        Fv = 9 * k + 32
        ans = Q(Cv)
        stem = (f"The formula {m('F = \\frac{9}{5}C + 32')} relates Fahrenheit and Celsius temperatures. "
                f"If {m(f'F = {Fv}')}, what is {m('C')}?")
        wrong = [
            (R(9, 5) * Fv + 32, f"substitutes {Fv} for {m('C')} instead of {m('F')}"),
            (Q(Fv - 32), f"subtracts 32 but forgets to multiply by {m('\\frac{5}{9}')}"),
            (R(9, 5) * (Fv - 32), f"multiplies by {m('\\frac{9}{5}')} instead of {m('\\frac{5}{9}')}"),
            (R(5, 9) * Fv - 32, "multiplies before subtracting 32"),
        ]
        steps = [f"Substitute: {m(f'{Fv} = \\frac{{9}}{{5}}C + 32')}.",
                 f"Subtract 32: {m(f'{Fv - 32} = \\frac{{9}}{{5}}C')}.",
                 f"Multiply by {m('\\frac{5}{9}')}: {m(f'C = {Fv - 32} \\times \\frac{{5}}{{9}} = {Cv}')}."]
        Cs = sp.Symbol("C")
        check = sp.solve(sp.Eq(Fv, R(9, 5) * Cs + 32), Cs)[0]
    elif kind == "tri":
        b, h = rng.randint(4, 20), rng.randint(3, 16)
        need((b * h) % 2 == 0 and b != h)
        A = b * h // 2
        ans = Q(h)
        stem = (f"The area of a triangle is {m('A = \\frac{1}{2}bh')}. If {m(f'A = {A}')} and {m(f'b = {b}')}, "
                f"what is {m('h')}?")
        wrong = [
            (R(A, b), f"divides by {b} but forgets the {m('\\frac{1}{2}')}"),
            (Q(2 * A * b), f"multiplies by {b} instead of dividing"),
            (R(A, 2 * b), f"divides by 2 instead of multiplying by 2"),
            (Q(A - b), None),
        ]
        steps = [f"Substitute: {m(f'{A} = \\frac{{1}}{{2}}({b})h')}, so {m(f'{A} = {int_raw(R(b, 2)) if b % 2 == 0 else dec_raw(R(b, 2))}h')}.",
                 f"Divide by {m(int_raw(R(b, 2)) if b % 2 == 0 else dec_raw(R(b, 2)))}: {m(f'h = {h}')}.",
                 f"Check: {m(f'\\frac{{1}}{{2}} \\times {b} \\times {h} = {A}')}. \\checkmark"]
        Hs = sp.Symbol("h")
        check = sp.solve(sp.Eq(A, R(1, 2) * b * Hs), Hs)[0]
    else:
        l, w, h = rng.randint(2, 12), rng.randint(2, 10), rng.randint(2, 10)
        V = l * w * h
        ans = Q(h)
        stem = (f"The volume of a box is {m('V = lwh')}. If {m(f'V = {V}')}, {m(f'l = {l}')}, and "
                f"{m(f'w = {w}')}, what is {m('h')}?")
        wrong = [
            (Q(V - l * w), "subtracts instead of dividing"),
            (Q(V - l - w), f"subtracts {m('l')} and {m('w')} instead of dividing"),
            (R(V, l + w), f"divides by {m('l + w')} instead of {m('l \\times w')}"),
            (Q(V * l * w), "multiplies instead of dividing"),
        ]
        steps = [f"Substitute: {m(f'{V} = {l} \\times {w} \\times h')}, so {m(f'{V} = {l * w}h')}.",
                 f"Divide by {l * w}: {m(f'h = {V} \\div {l * w} = {h}')}."]
        Hs = sp.Symbol("h")
        check = sp.solve(sp.Eq(V, l * w * Hs), Hs)[0]
    return Problem(stem=stem, answer=ans, fmt=dec, neg_ok=kind == "temp", wrong=wrong, steps=steps,
                   check=check)


@template("MK")
def perimeter_expression(rng, lvl):
    W = sp.Symbol("x")
    if rng.random() < 0.6:
        a, b = rng.randint(2, 5), rng.randint(1, 9)
        c, d = rng.randint(1, 4), rng.choice([-1, 1]) * rng.randint(1, 6)
        need(a != c and b + d > 0)
        L_t, W_t = _lin([(a, "x"), (b, "")]), _lin([(c, "x"), (d, "")])
        ans_s = sp.expand(2 * (a * W + b) + 2 * (c * W + d))
        A_, B_ = 2 * (a + c), 2 * (b + d)
        ans_t = _lin([(A_, "x"), (B_, "")])
        wr = [
            (_lin([(a + c, "x"), (b + d, "")]), (a + c) * W + b + d, "adds one length and one width only"),
            (_lin([(A_, "x"), (b + d, "")]), A_ * W + b + d, "doubles the x-terms but not the constants"),
            (_lin([(a * c, "x^2"), (a * d + b * c, "x"), (b * d, "")]), sp.expand((a * W + b) * (c * W + d)),
             "multiplies the length by the width, which gives the area"),
            (_lin([(A_, "x"), (B_ + 2, "")]), A_ * W + B_ + 2, None),
        ]
        stem = (f"A rectangle has a length of {m(L_t)} and a width of {m(W_t)}. Which expression represents "
                f"its perimeter?")
        steps = [
            f"Perimeter = 2(length) + 2(width) = {m(f'2({L_t}) + 2({W_t})')}.",
            f"Distribute: {m(f'{_lin([(2 * a, "x"), (2 * b, "")])} + {_lin([(2 * c, "x"), (2 * d, "")])}')}.",
            f"Combine like terms: {m(ans_t)}.",
        ]
    else:
        s = [(rng.randint(1, 4), rng.choice([-1, 1]) * rng.randint(1, 8)) for _ in range(3)]
        need(len({t[0] for t in s}) > 1 and all(t[0] * 5 + t[1] > 0 for t in s))
        texs = [_lin([(p, "x"), (q, "")]) for p, q in s]
        A_, B_ = sum(p for p, _ in s), sum(q for _, q in s)
        ans_s = A_ * W + B_
        ans_t = _lin([(A_, "x"), (B_, "")])
        wr = [
            (_lin([(A_, "x"), (sum(abs(q) for _, q in s), "")]), A_ * W + sum(abs(q) for _, q in s),
             "adds every constant, ignoring the minus signs") if any(q < 0 for _, q in s) else
            (_lin([(A_ + 1, "x"), (B_, "")]), (A_ + 1) * W + B_, None),
            (_lin([(A_ + B_, "x")]), (A_ + B_) * W, "combines unlike terms"),
            (_lin([(2 * A_, "x"), (2 * B_, "")]), 2 * A_ * W + 2 * B_, "doubles the sum, as if the figure were a rectangle"),
            (_lin([(A_, "x"), (B_ - 1, "")]), A_ * W + B_ - 1, None),
        ]
        stem = (f"The sides of a triangle have lengths {m(texs[0])}, {m(texs[1])}, and {m(texs[2])}. "
                f"Which expression represents the perimeter of the triangle?")
        steps = [
            "The perimeter is the sum of the three sides.",
            f"Add the {m('x')}-terms: {m(f'{s[0][0]} + {s[1][0]} + {s[2][0]} = {A_}')}. Add the constants: "
            f"{m(f'{_signed([q for _, q in s])} = {int_raw(B_)}')}.",
            f"The perimeter is {m(ans_t)}.",
        ]
    P = sp.Poly(ans_s, W)
    return Problem(
        stem=stem,
        answer=m(ans_t),
        fmt=lambda t: t,
        wrong=_choices(ans_s, wr),
        steps=steps,
        check=m(_lin([(P.coeff_monomial(W), "x"), (P.coeff_monomial(1), "")])),
    )


PLAN = [
    # (template, level, count)  -- easy -> hard; 25 problems
    (evaluate_expr, 1, 2),
    (combine_like, 1, 2),
    (translate, 1, 2),
    (evaluate_formula, 1, 2),
    (evaluate_expr, 2, 2),
    (combine_like, 2, 1),
    (distribute, 2, 2),
    (translate, 2, 2),
    (word_expression, 2, 2),
    (evaluate_formula, 2, 1),
    (distribute, 3, 2),
    (evaluate_expr, 3, 2),
    (formula_solve, 3, 1),
    (perimeter_expression, 3, 1),
    (word_expression, 3, 1),
]
