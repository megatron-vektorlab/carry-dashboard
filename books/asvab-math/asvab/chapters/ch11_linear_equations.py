"""Chapter 11 - Linear Equations."""
from fractions import Fraction

import sympy as sp

from ..core import (R, Q, Problem, need, frac, dec, m, F, tx, dec_raw,
                    int_raw, frac_raw, text, unit, person, soldier, choose,
                    template, x, y, n)

NUM = 11
TITLE = "Linear Equations"
PART = 2

INTRO = r"""
An \emph{equation} says that two expressions are equal. To \emph{solve} it,
find the value of the variable that makes both sides equal. The golden rule:
\textbf{whatever you do to one side, do to the other side}, so the two sides
stay balanced.

\begin{concept}{Undo operations in reverse order}
Get the variable alone by undoing what was done to it, last operation first:
addition $\leftrightarrow$ subtraction, multiplication $\leftrightarrow$
division.
\[ 3x - 7 = 11 \;\Rightarrow\; 3x = 18 \;\Rightarrow\; x = 6 \]
(add $7$ to both sides, then divide both sides by $3$). \textbf{Check} by
substituting: $3(6) - 7 = 18 - 7 = 11$. \checkmark
\end{concept}

\begin{concept}{Clean up first}
\begin{itemize}
\item \textbf{Parentheses:} distribute to \emph{every} term inside:
  $4(x - 2) = 4x - 8$ and $-2(x + 5) = -2x - 10$.
\item \textbf{Variables on both sides:} add or subtract to move all the
  $x$-terms to one side and all the plain numbers to the other.
\item \textbf{Fractions:} multiply \emph{every} term by the least common
  denominator (LCD). \textbf{Decimals:} multiply every term by $10$ or $100$.
\item \textbf{Formulas:} to solve $d = rt$ for $t$, treat the other letters
  like numbers and divide: $t = \frac{d}{r}$.
\end{itemize}
\end{concept}

\begin{concept}{Translating words into equations}
\begin{tabular}{@{}ll@{}}
is, equals, gives, the result is & $=$ \\
more than, increased by, sum, plus & $+$ \\
less than, decreased by, difference & $-$ \\
times, twice, tripled, product & $\times$ \\
consecutive integers & $n,\ n+1,\ n+2,\ \ldots$ \\
consecutive even (or odd) integers & $n,\ n+2,\ n+4,\ \ldots$ \\
\end{tabular}

\smallskip
Careful: ``$5$ less than $x$'' is $x - 5$, \emph{not} $5 - x$.
\end{concept}

\begin{example}{Worked example}
Solve $2(x + 3) = 5x - 9$.

\textbf{Solution.} Distribute: $2x + 6 = 5x - 9$. Subtract $2x$ from both
sides: $6 = 3x - 9$. Add $9$ to both sides: $15 = 3x$. Divide by $3$:
$x = 5$. Check: $2(5 + 3) = 16$ and $5(5) - 9 = 16$. \checkmark
\end{example}

\begin{tip}
Multiple choice lets you \emph{backsolve}: plug each choice into the
equation; the one that makes both sides equal is the answer. When $x$-terms
are on both sides, move them toward the side with the larger
$x$-coefficient so that coefficient stays positive.
\end{tip}

\begin{trap}
\begin{itemize}
\item Distributing to only the first term: $3(x + 4)$ is $3x + 12$, not
  $3x + 4$.
\item Moving a term across the equal sign without changing its sign.
\item Answering $x$ when the question asks for something else, such as
  $2x + 1$.
\item Reversing ``less than'': ``$7$ less than $3n$'' is $3n - 7$.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# private helpers
# --------------------------------------------------------------------------

def _lin(*terms):
    """Signed sum of (coef, var) terms: (3, 'x'), (-7, '') -> '3x - 7'."""
    out = ""
    for c, v in terms:
        c = Q(c)
        if c == 0:
            continue
        mag = abs(c)
        body = v if (v and mag == 1) else frac_raw(mag) + v
        if not out:
            out = ("-" if c < 0 else "") + body
        else:
            out += (" - " if c < 0 else " + ") + body
    return out or "0"


def _p(v):
    """Value in parentheses when negative: -3 -> '(-3)'."""
    return f"({tx(v)})" if Q(v) < 0 else tx(v)


def _plus(v):
    """' + 5' or ' - 5' to append a constant term."""
    v = Q(v)
    return f" - {tx(-v)}" if v < 0 else f" + {tx(v)}"


def _solve(lhs, rhs, var=x):
    sols = sp.solve(sp.Eq(lhs, rhs), var)
    need(len(sols) == 1)
    return sols[0]


def _const_step(b, lhs_tex, rhs, var_side="left"):
    """Step that removes the constant b from the side holding the x-term."""
    new = Q(rhs) - b
    if b > 0:
        return (f"Undo the addition: subtract {m(tx(b))} from both sides. "
                f"{m(f'{lhs_tex} = {tx(rhs)} - {tx(b)} = {tx(new)}')}.")
    return (f"Undo the subtraction: add {m(tx(-b))} to both sides. "
            f"{m(f'{lhs_tex} = {tx(rhs)} + {tx(-b)} = {tx(new)}')}.")


def _div_step(a, top, var="x"):
    return (f"Undo the multiplication: divide both sides by {m(tx(a))}. "
            f"{m(f'{var} = {F(tx(top), tx(a))} = {tx(Q(top) / a)}')}.")


def _ask(rng, eq):
    return choose(rng,
                  f"Solve for $x$: {m(eq)}.",
                  f"What value of $x$ makes {m(eq)} true?",
                  f"If {m(eq)}, what is the value of $x$?")


# --------------------------------------------------------------------------
# templates
# --------------------------------------------------------------------------

@template("MK")
def basic_eq(rng, lvl):
    if lvl == 1:
        kind = rng.choice(["add", "sub", "mul", "div", "two", "two"])
        X = Q(rng.randint(2, 15))
    else:
        kind = rng.choice(["two", "two", "rev"])
        X = Q(rng.choice([v for v in range(-12, 13) if v not in (-1, 0, 1)]))
    tip = None
    if kind == "add":
        A = rng.randint(2, 30)
        B = X + A
        eq, holds = f"x + {A} = {tx(B)}", (lambda v: v + A == B)
        wrong = [(B + A, f"adds {m(A)} to both sides instead of subtracting it"),
                 (A - B, "subtracts in the wrong order")]
        steps = [f"The equation adds {m(A)} to {m('x')}. Undo that by subtracting {m(A)} "
                 f"from both sides: {m(f'x = {tx(B)} - {A} = {tx(X)}')}.",
                 f"Check: {m(f'{tx(X)} + {A} = {tx(B)}')}. \\checkmark"]
    elif kind == "sub":
        A = rng.randint(2, 30)
        B = X - A
        need(B != 0)
        eq, holds = f"x - {A} = {tx(B)}", (lambda v: v - A == B)
        wrong = [(B - A, f"subtracts {m(A)} from both sides instead of adding it"),
                 (A - B, None)]
        steps = [f"The equation subtracts {m(A)} from {m('x')}. Undo that by adding {m(A)} "
                 f"to both sides: {m(f'x = {tx(B)} + {A} = {tx(X)}')}.",
                 f"Check: {m(f'{tx(X)} - {A} = {tx(B)}')}. \\checkmark"]
    elif kind == "mul":
        A = rng.randint(2, 12)
        B = A * X
        eq, holds = f"{A}x = {tx(B)}", (lambda v: A * v == B)
        wrong = [(B - A, f"subtracts {m(A)} instead of dividing by it"),
                 (A * B, f"multiplies by {m(A)} instead of dividing"),
                 (B + A, f"adds {m(A)} instead of dividing by it")]
        steps = [f"{m(f'{A}x')} means {m(A)} times {m('x')}. Undo the multiplication by "
                 f"dividing both sides by {m(A)}.",
                 f"{m(f'x = {tx(B)} \\div {A} = {tx(X)}')}."]
    elif kind == "div":
        A = rng.randint(2, 9)
        B = Q(rng.randint(2, 15))
        X = A * B
        eq, holds = f"\\frac{{x}}{{{A}}} = {tx(B)}", (lambda v: v / A == B)
        wrong = [(B / A, f"divides by {m(A)} instead of multiplying"),
                 (B + A, f"adds {m(A)} instead of multiplying by it"),
                 (B - A, f"subtracts {m(A)} instead of multiplying by it")]
        steps = [f"{m(eq.split(' =')[0])} means {m('x')} divided by {m(A)}. Undo the division "
                 f"by multiplying both sides by {m(A)}.",
                 f"{m(f'x = {tx(B)} \\times {A} = {tx(X)}')}."]
    elif kind == "two":
        if lvl == 1:
            A, Bc = rng.randint(2, 9), rng.randint(1, 20)
        else:
            A = rng.choice([v for v in range(-9, 10) if abs(v) >= 2])
            Bc = rng.choice([v for v in range(-25, 26) if v != 0])
        C = A * X + Bc
        need(C != 0)
        eq = f"{_lin((A, 'x'), (Bc, ''))} = {tx(C)}"
        holds = lambda v: A * v + Bc == C
        moved = "subtracting it" if Bc > 0 else "adding it"
        wrong = [((C + Bc) / Q(A), f"moves {m(tx(Bc))} to the other side without changing its sign"),
                 (C - Bc, f"forgets to divide by {m(A)}"),
                 (Q(C) / A - Bc, f"divides both sides by {m(A)} but forgets to divide {m(tx(Bc))} too")]
        if A < 0:
            wrong.insert(0, (-X, f"divides by {m(-A)} instead of {m(A)}"))
        steps = [_const_step(Bc, f"{_lin((A, 'x'))}", C),
                 _div_step(A, C - Bc),
                 f"Check: {m(f'{A}{_p(X)}{_plus(Bc)} = {tx(A * X)}{_plus(Bc)} = {tx(C)}')}. \\checkmark"]
    else:  # rev: D - Ax = C
        A = rng.randint(2, 9)
        D = rng.randint(5, 30)
        C = D - A * X
        need(C != 0)
        eq = f"{D} - {A}x = {tx(C)}"
        holds = lambda v: D - A * v == C
        wrong = [(-X, f"divides by {m(A)} instead of {m(-A)}"),
                 ((C + D) / Q(-A), f"adds {m(D)} to both sides instead of subtracting it"),
                 (C - D, f"forgets to divide by {m(-A)}")]
        steps = [f"Undo the {m(D)}: subtract {m(D)} from both sides. "
                 f"{m(f'-{A}x = {tx(C)} - {D} = {tx(C - D)}')}.",
                 f"The {m('x')}-term is {m(f'-{A}x')}, so divide both sides by {m(-A)}: "
                 f"{m(f'x = {F(tx(C - D), -A)} = {tx(X)}')}.",
                 f"Check: {m(f'{D} - {A}{_p(X)} = {D}{_plus(-A * X)} = {tx(C)}')}. \\checkmark"]
        tip = "Dividing by a negative number changes the sign of the result."
    return Problem(
        stem=_ask(rng, eq),
        answer=X,
        fmt=frac,
        wrong=wrong,
        steps=steps,
        tip=tip,
        verify=holds,
        check=_solve_from(holds),
        neg_ok=True,
    )


def _solve_from(holds):
    """Independent check by brute force: the unique integer in [-200, 200]
    (or multiple of 1/12) that satisfies the equation."""
    hits = [Q(k) for k in range(-200, 201) if holds(Q(k))]
    need(len(hits) == 1)
    return hits[0]


@template("MK")
def both_sides(rng, lvl):
    X = Q(rng.choice([v for v in range(-9, 13) if v != 0]))
    if lvl <= 2:
        c = rng.randint(1, 7)
        a = c + rng.randint(1, 6)
    else:
        a = rng.choice([v for v in range(-6, 9) if v != 0])
        c = rng.choice([v for v in range(-6, 10) if v != 0])
        need(abs(a - c) >= 2 and (a < 0 or c < 0 or a < c))
    b = rng.choice([v for v in range(-15, 16) if v != 0])
    d = a * X + b - c * X
    need(d != 0 and d != b)
    left = _lin((a, "x"), (b, "")) if (lvl <= 2 or rng.random() < 0.5) else _lin((b, ""), (a, "x"))
    right = _lin((c, "x"), (d, ""))
    eq = f"{left} = {right}"
    if a > c:
        k = a - c
        move = (f"Get the {m('x')}-terms on the left: "
                + (f"subtract {m(f'{_lin((c, "x"))}')} from" if c > 0 else f"add {m(_lin((-c, 'x')))} to")
                + f" both sides. {m(f'{_lin((k, "x"), (b, ""))} = {tx(d)}')}.")
        steps = [move, _const_step(b, _lin((k, "x")), d), _div_step(k, d - b)]
    else:
        k = c - a
        move = (f"Get the {m('x')}-terms on the right, where the coefficient is larger: "
                + (f"subtract {m(_lin((a, 'x')))} from" if a > 0 else f"add {m(_lin((-a, 'x')))} to")
                + f" both sides. {m(f'{tx(b)} = {_lin((k, "x"), (d, ""))}')}.")
        if d > 0:
            mv = (f"Subtract {m(tx(d))} from both sides: "
                  f"{m(f'{tx(b)} - {tx(d)} = {_lin((k, "x"))}')}, so {m(f'{tx(b - d)} = {_lin((k, "x"))}')}.")
        else:
            mv = (f"Add {m(tx(-d))} to both sides: "
                  f"{m(f'{tx(b)} + {tx(-d)} = {_lin((k, "x"))}')}, so {m(f'{tx(b - d)} = {_lin((k, "x"))}')}.")
        steps = [move, mv, _div_step(k, b - d)]
    steps.append(f"Check: both sides equal {m(tx(a * X + b))} when {m(f'x = {tx(X)}')}. \\checkmark")
    wrong = [(-X, "makes a sign error when moving the terms"),
             (Q(d + b) / (a - c), f"moves {m(tx(b))} across without changing its sign")]
    if a + c != 0:
        wrong.insert(0, (Q(d - b) / (a + c), "adds the $x$-terms instead of subtracting one from the other"))
    if abs(a - c) != 1:
        wrong.append((Q(abs(d - b)) * (1 if X > 0 else -1), f"forgets to divide by {m(abs(a - c))}"))
    return Problem(
        stem=_ask(rng, eq),
        answer=X,
        fmt=frac,
        wrong=wrong,
        steps=steps,
        verify=lambda v: a * v + b == c * v + d,
        check=_solve(a * x + b, c * x + d),
        neg_ok=True,
    )


@template("MK")
def distribute(rng, lvl):
    X = Q(rng.choice([v for v in range(-6, 13) if v != 0]))
    if lvl <= 2:
        a = rng.randint(2, 7)
        b = rng.choice([v for v in range(-9, 10) if v != 0])
        c = rng.choice([0, 0] + [v for v in range(-15, 16) if v != 0])
        d = a * (X + b) + c
        need(d != 0)
        eq = f"{a}({_lin((1, 'x'), (b, ''))}){_plus(c) if c else ''} = {tx(d)}"
        K = a * b + c
        steps = [f"Distribute {m(a)} to \\emph{{both}} terms in the parentheses: "
                 f"{m(f'{a} \\cdot x = {a}x')} and {m(f'{a} \\cdot {_p(b)} = {tx(a * b)}')}. "
                 f"The equation becomes {m(f'{_lin((a, "x"), (a * b, ""))}{_plus(c) if c else ""} = {tx(d)}')}."]
        if c:
            steps.append(f"Combine the plain numbers: {m(f'{tx(a * b)}{_plus(c)} = {tx(K)}')}, "
                         f"so {m(f'{_lin((a, "x"), (K, ""))} = {tx(d)}')}.")
        if K != 0:
            steps.append(_const_step(K, f"{a}x", d))
        steps.append(_div_step(a, d - K))
        wrong = [(Q(d - c - b) / a, f"multiplies only the {m('x')} by {m(a)}, not the {m(tx(b))}"),
                 (Q(d - K) * 1, f"forgets to divide by {m(a)}"),
                 (Q(d - c + a * b) / a, f"makes a sign error with {m(tx(a * b))}")]
        tip = (f"Shortcut: divide both sides by {m(a)} first: {m(f'{_lin((1, "x"), (b, ""))} = {tx(Q(d) / a)}')}."
               if c == 0 and Q(d) % a == 0 else None)
        holds = lambda v: a * (v + b) + c == d
        chk = _solve(a * (x + b) + c, d)
    elif rng.random() < 0.6:
        # a(x - b) - c(x + e) = f : the minus-sign trap
        c = rng.randint(2, 5)
        a = c + rng.randint(1, 4)
        b, e = rng.randint(1, 9), rng.randint(1, 9)
        f = a * (X - b) - c * (X + e)
        need(f != 0)
        k = a - c
        eq = f"{a}(x - {b}) - {c}(x + {e}) = {tx(f)}"
        K = -a * b - c * e
        steps = [f"Distribute each number to both terms in its parentheses. The {m(f'-{c}')} multiplies "
                 f"\\emph{{both}} {m('x')} and {m(e)}: {m(f'-{c}(x + {e}) = -{c}x - {c * e}')}.",
                 f"So {m(f'{a}x - {a * b} - {c}x - {c * e} = {tx(f)}')}.",
                 f"Combine like terms: {m(f'{_lin((k, "x"), (K, ""))} = {tx(f)}')}.",
                 _const_step(K, _lin((k, "x")), f),
                 _div_step(k, f - K)]
        wrong = [(Q(f + a * b - c * e) / k, f"writes {m(f'+{c * e}')} instead of {m(f'-{c * e}')} "
                                            f"(does not distribute the minus sign)"),
                 (Q(f + a * b + c * e) / (a + c), f"adds {m(f'{a}x')} and {m(f'{c}x')} instead of subtracting"),
                 (Q(f + b + e) / k, f"multiplies only the {m('x')}-terms, not the numbers in parentheses")]
        tip = None
        holds = lambda v: a * (v - b) - c * (v + e) == f
        chk = _solve(a * (x - b) - c * (x + e), f)
    else:
        # a(x + b) = c(x + e), a > c
        c = rng.randint(2, 5)
        a = c + rng.randint(1, 4)
        b = rng.choice([v for v in range(-9, 10) if v != 0])
        e = rng.choice([v for v in range(-9, 10) if v not in (0, b)])
        k = a - c
        need((c * e - a * b) % k == 0)
        X = Q(c * e - a * b) / k
        need(X != 0 and abs(X) <= 20)
        eq = f"{a}({_lin((1, 'x'), (b, ''))}) = {c}({_lin((1, 'x'), (e, ''))})"
        steps = [f"Distribute on both sides: {m(f'{_lin((a, "x"), (a * b, ""))} = {_lin((c, "x"), (c * e, ""))}')}.",
                 f"Subtract {m(f'{c}x')} from both sides: {m(f'{_lin((k, "x"), (a * b, ""))} = {tx(c * e)}')}.",
                 _const_step(a * b, _lin((k, "x")), c * e),
                 _div_step(k, c * e - a * b)]
        wrong = [(Q(e - b) / k, "multiplies only the $x$-terms, not the numbers in parentheses"),
                 (-X, "makes a sign error when moving the terms"),
                 (Q(c * e - a * b) / (a + c), "adds the $x$-terms instead of subtracting")]
        tip = None
        holds = lambda v: a * (v + b) == c * (v + e)
        chk = _solve(a * (x + b), c * (x + e))
    return Problem(
        stem=_ask(rng, eq),
        answer=X,
        fmt=frac,
        wrong=wrong,
        steps=steps,
        tip=tip,
        verify=holds,
        check=chk,
        neg_ok=True,
    )


@template("MK")
def fraction_eq(rng, lvl):
    tip = None
    if lvl == 1:
        a = rng.randint(2, 9)
        k = Q(rng.randint(1, 12))
        X = a * k
        b = rng.randint(1, 15)
        plus = rng.random() < 0.6
        c = k + b if plus else k - b
        need(c > 0)
        sb = b if plus else -b
        eq = f"\\frac{{x}}{{{a}}}{_plus(sb)} = {tx(c)}"
        steps = [_const_step(sb, f"\\frac{{x}}{{{a}}}", c),
                 f"Undo the division: multiply both sides by {m(a)}. {m(f'x = {tx(k)} \\times {a} = {tx(X)}')}.",
                 f"Check: {m(f'\\frac{{{tx(X)}}}{{{a}}}{_plus(sb)} = {tx(k)}{_plus(sb)} = {tx(c)}')}. \\checkmark"]
        wrong = [((c - sb) / Q(a), f"divides by {m(a)} instead of multiplying"),
                 (a * c - sb, f"multiplies {m(tx(c))} by {m(a)} but forgets to multiply {m(tx(sb))}"),
                 (a * (c + sb), f"moves {m(tx(sb))} across without changing its sign"),
                 (c - sb, f"forgets to multiply by {m(a)}")]
        holds = lambda v: v / a + sb == c
        chk = _solve(x / a + sb, c)
    elif lvl == 2:
        if rng.random() < 0.5:
            # (k x)/a = c  with gcd(k, a) = 1
            a = rng.randint(2, 9)
            kk = rng.randint(2, 7)
            need(sp.gcd(a, kk) == 1)
            X = Q(kk * rng.randint(1, 12) * 0 + a * rng.randint(1, 8))
            need((kk * X) % a == 0)
            c = kk * X / a
            eq = f"\\frac{{{kk}x}}{{{a}}} = {tx(c)}"
            steps = [f"Undo the division first: multiply both sides by {m(a)}. "
                     f"{m(f'{kk}x = {tx(c)} \\times {a} = {tx(c * a)}')}.",
                     f"Undo the multiplication: divide both sides by {m(kk)}. "
                     f"{m(f'x = {F(tx(c * a), kk)} = {tx(X)}')}."]
            wrong = [(c * kk / a, f"multiplies by {m(F(kk, a))} instead of by its reciprocal {m(F(a, kk))}"),
                     (c * a, f"forgets to divide by {m(kk)}"),
                     (c / kk, f"forgets to multiply by {m(a)}")]
            tip = f"Multiplying by the reciprocal does both steps at once: {m(f'x = {tx(c)} \\cdot {F(a, kk)} = {tx(X)}')}."
            holds = lambda v: kk * v / a == c
            chk = _solve(kk * x / a, c)
        else:
            # (x + b)/a = c
            a = rng.randint(2, 9)
            b = rng.choice([v for v in range(-12, 13) if v != 0])
            c = Q(rng.choice([v for v in range(-8, 13) if v != 0]))
            X = a * c - b
            need(X != 0)
            eq = f"\\frac{{{_lin((1, 'x'), (b, ''))}}}{{{a}}} = {tx(c)}"
            steps = [f"Undo the division first: multiply both sides by {m(a)}. "
                     f"{m(f'{_lin((1, "x"), (b, ""))} = {tx(c)} \\times {a} = {tx(a * c)}')}.",
                     _const_step(b, "x", a * c).replace("Undo the addition", "Now undo the addition")
                     .replace("Undo the subtraction", "Now undo the subtraction")]
            wrong = [(a * c + b, f"moves {m(tx(b))} across without changing its sign"),
                     (c - b, f"forgets to multiply by {m(a)}"),
                     (a * (c - b), f"subtracts {m(tx(b))} from {m(tx(c))} before multiplying by {m(a)}")]
            holds = lambda v: (v + b) / a == c
            chk = _solve((x + b) / a, c)
    else:
        # x/p +- x/q = r
        p, q = sorted(rng.sample([2, 3, 4, 5, 6, 8, 10], 2))
        L = sp.ilcm(p, q)
        plus = rng.random() < 0.65
        S = L // p + L // q if plus else L // p - L // q
        r = Q(rng.randint(1, 12))
        X = r * L / S
        need(X.is_integer and 0 < X <= 150)
        sgn = "+" if plus else "-"
        eq = f"\\frac{{x}}{{{p}}} {sgn} \\frac{{x}}{{{q}}} = {tx(r)}"
        steps = [f"Clear the fractions: multiply \\emph{{every}} term by the LCD of {m(p)} and {m(q)}, "
                 f"which is {m(L)}.",
                 f"{m(f'{L} \\cdot \\frac{{x}}{{{p}}} = {_lin((L // p, "x"))}')}, "
                 f"{m(f'{L} \\cdot \\frac{{x}}{{{q}}} = {_lin((L // q, "x"))}')}, and "
                 f"{m(f'{L} \\cdot {tx(r)} = {tx(L * r)}')}. So {m(f'{_lin((L // p, "x"))} {sgn} {_lin((L // q, "x"))} = {tx(L * r)}')}.",
                 f"Combine like terms: {m(f'{_lin((S, "x"))} = {tx(L * r)}')}."]
        if S != 1:
            steps.append(f"Divide by {m(S)}: {m(f'x = {F(tx(L * r), S)} = {tx(X)}')}.")
        steps.append(f"Check: {m(f'\\frac{{{tx(X)}}}{{{p}}} {sgn} \\frac{{{tx(X)}}}{{{q}}} = {tx(X / p)} {sgn} {tx(X / q)} = {tx(r)}')}. \\checkmark")
        wrong = [(r * (p + q) if plus else r * (q - p),
                  f"{'adds' if plus else 'subtracts'} the denominators, as if the result were "
                  f"{m(f'\\frac{{x}}{{{p + q if plus else q - p}}}')}"),
                 (r / S, f"forgets to multiply the right side by {m(L)}"),
                 (r * p * q, None)]
        if plus:
            wrong.append((r * (p + q) / 2, f"treats the sum as {m(f'\\frac{{2x}}{{{p + q}}}')}"))
        holds = lambda v: (v / p + v / q if plus else v / p - v / q) == r
        chk = Q(Fraction(int(r) * L, S))
    return Problem(
        stem=_ask(rng, eq),
        answer=X,
        fmt=frac,
        wrong=wrong,
        steps=steps,
        tip=tip,
        verify=holds,
        check=chk,
        neg_ok=True,
    )


@template("MK")
def decimal_eq(rng, lvl):
    a = R(rng.choice([2, 3, 4, 5, 6, 8, 12, 15, 25, 35]), 10)
    X = Q(rng.randint(2, 24))
    if lvl >= 3 and rng.random() < 0.5:
        b = R(rng.choice([v for v in range(-95, 96, 5) if v != 0]), 100)
    else:
        b = R(rng.choice([v for v in range(-45, 46) if v != 0 and v % 10 != 0] + [10, 20, -10]), 10)
    c = a * X + b
    need(c > 0)
    scale = 100 if any((v * 10).q != 1 for v in (a, b, c)) else 10
    A, B, C = a * scale, b * scale, c * scale
    eq = f"{dec_raw(a)}x{' - ' if b < 0 else ' + '}{dec_raw(abs(b))} = {dec_raw(c)}"
    steps = [f"Clear the decimals: multiply \\emph{{every}} term by {m(scale)}. "
             f"{m(f'{_lin((A, "x"), (B, ""))} = {tx(C)}')}.",
             _const_step(B, _lin((A, "x")), C),
             f"Divide both sides by {m(A)}: {m(f'x = {F(tx(C - B), A)} = {tx(X)}')}."]
    wrong = [(X * 10, "slips the decimal point"),
             ((c + b) / a, f"moves {m(dec_raw(b))} across without changing its sign"),
             (c - b, f"forgets to divide by {m(dec_raw(a))}"),
             (X / 10, "slips the decimal point")]
    return Problem(
        stem=_ask(rng, eq),
        answer=X,
        fmt=dec,
        wrong=wrong,
        steps=steps,
        tip=(f"You can also work with the decimals directly: {m(f'{dec_raw(a)}x = {dec_raw(c - b)}')}, "
             f"and {m(f'{dec_raw(c - b)} \\div {dec_raw(a)} = {tx(X)}')}."),
        verify=lambda v: a * v + b == c,
        check=Q(Fraction(int(C - B), int(A))),
        neg_ok=True,
    )


# ---- literal equations ----------------------------------------------------

def _yfmt(v):
    e = sp.expand(Q(v))
    return m("y = " + _lin((e.coeff(x), "x"), (e.subs(x, 0), "")))


_A, _b, _h, _P, _l, _w, _d, _r, _t, _I, _V, _Fh, _C, _m, _M, _D, _a, _c, _u, _v = sp.symbols(
    "A b h P l w d r t I V F C m M D a c u v")
_b1, _b2 = sp.symbols("b_1 b_2")

# (intro, formula tex, sympy equation, solve-for symbol, its tex,
#  answer tex, answer expr, [(wrong tex, wrong expr, why), ...])
_FORMULAS = [
    ("The area of a triangle is", r"A = \frac{1}{2}bh", sp.Eq(_A, _b * _h / 2), _h, "h",
     r"h = \frac{2A}{b}", 2 * _A / _b,
     [(r"h = \frac{A}{2b}", _A / (2 * _b), "divides by 2 instead of multiplying by 2"),
      (r"h = \frac{Ab}{2}", _A * _b / 2, "multiplies by $b$ instead of dividing by $b$"),
      (r"h = 2A - b", 2 * _A - _b, "subtracts $b$ instead of dividing by it")]),
    ("The perimeter of a rectangle is", r"P = 2l + 2w", sp.Eq(_P, 2 * _l + 2 * _w), _w, "w",
     r"w = \frac{P - 2l}{2}", (_P - 2 * _l) / 2,
     [(r"w = P - 2l", _P - 2 * _l, "forgets to divide by 2"),
      (r"w = \frac{P + 2l}{2}", (_P + 2 * _l) / 2, "adds $2l$ instead of subtracting it"),
      (r"w = \frac{P}{2} - 2l", _P / 2 - 2 * _l, "divides only $P$ by 2, not $2l$")]),
    ("Distance traveled is", r"d = rt", sp.Eq(_d, _r * _t), _t, "t",
     r"t = \frac{d}{r}", _d / _r,
     [(r"t = dr", _d * _r, "multiplies by $r$ instead of dividing"),
      (r"t = \frac{r}{d}", _r / _d, "divides in the wrong order"),
      (r"t = d - r", _d - _r, "subtracts $r$ instead of dividing by it")]),
    ("Simple interest is", r"I = Prt", sp.Eq(_I, _P * _r * _t), _r, "r",
     r"r = \frac{I}{Pt}", _I / (_P * _t),
     [(r"r = IPt", _I * _P * _t, "multiplies by $Pt$ instead of dividing"),
      (r"r = \frac{Pt}{I}", _P * _t / _I, "divides in the wrong order"),
      (r"r = I - Pt", _I - _P * _t, "subtracts $Pt$ instead of dividing by it")]),
    ("The volume of a box is", r"V = lwh", sp.Eq(_V, _l * _w * _h), _h, "h",
     r"h = \frac{V}{lw}", _V / (_l * _w),
     [(r"h = Vlw", _V * _l * _w, "multiplies by $lw$ instead of dividing"),
      (r"h = \frac{lw}{V}", _l * _w / _V, "divides in the wrong order"),
      (r"h = V - lw", _V - _l * _w, "subtracts $lw$ instead of dividing by it")]),
    ("Temperature conversion uses", r"F = \frac{9}{5}C + 32", sp.Eq(_Fh, R(9, 5) * _C + 32), _C, "C",
     r"C = \frac{5}{9}(F - 32)", R(5, 9) * (_Fh - 32),
     [(r"C = \frac{5}{9}F - 32", R(5, 9) * _Fh - 32, "multiplies by $\\frac{5}{9}$ before subtracting 32"),
      (r"C = \frac{9}{5}(F - 32)", R(9, 5) * (_Fh - 32), "multiplies by $\\frac{9}{5}$ instead of its reciprocal"),
      (r"C = \frac{5}{9}(F + 32)", R(5, 9) * (_Fh + 32), "adds 32 instead of subtracting it")]),
    ("The equation of a line is", r"y = mx + b", sp.Eq(y, _m * x + _b), x, "x",
     r"x = \frac{y - b}{m}", (y - _b) / _m,
     [(r"x = \frac{y + b}{m}", (y + _b) / _m, "adds $b$ instead of subtracting it"),
      (r"x = \frac{y}{m} - b", y / _m - _b, "divides only $y$ by $m$, not $b$"),
      (r"x = m(y - b)", _m * (y - _b), "multiplies by $m$ instead of dividing")]),
    ("The circumference of a circle is", r"C = 2\pi r", sp.Eq(_C, 2 * sp.pi * _r), _r, "r",
     r"r = \frac{C}{2\pi}", _C / (2 * sp.pi),
     [(r"r = 2\pi C", 2 * sp.pi * _C, "multiplies by $2\\pi$ instead of dividing"),
      (r"r = \frac{C}{\pi}", _C / sp.pi, "divides by $\\pi$ but forgets the 2"),
      (r"r = C - 2\pi", _C - 2 * sp.pi, "subtracts $2\\pi$ instead of dividing by it")]),
    ("The perimeter of a triangle is", r"P = a + b + c", sp.Eq(_P, _a + _b + _c), _c, "c",
     r"c = P - a - b", _P - _a - _b,
     [(r"c = P + a + b", _P + _a + _b, "adds $a$ and $b$ instead of subtracting them"),
      (r"c = P - a + b", _P - _a + _b, "subtracts $a$ but adds $b$"),
      (r"c = a + b - P", _a + _b - _P, "subtracts in the wrong order")]),
    ("Final speed is", r"v = u + at", sp.Eq(_v, _u + _a * _t), _t, "t",
     r"t = \frac{v - u}{a}", (_v - _u) / _a,
     [(r"t = \frac{v + u}{a}", (_v + _u) / _a, "adds $u$ instead of subtracting it"),
      (r"t = \frac{v}{a} - u", _v / _a - _u, "divides only $v$ by $a$, not $u$"),
      (r"t = a(v - u)", _a * (_v - _u), "multiplies by $a$ instead of dividing")]),
    ("The area of a trapezoid is", r"A = \frac{1}{2}(b_1 + b_2)h", sp.Eq(_A, (_b1 + _b2) * _h / 2), _h, "h",
     r"h = \frac{2A}{b_1 + b_2}", 2 * _A / (_b1 + _b2),
     [(r"h = \frac{A}{2(b_1 + b_2)}", _A / (2 * (_b1 + _b2)), "divides by 2 instead of multiplying by 2"),
      (r"h = 2A - b_1 - b_2", 2 * _A - _b1 - _b2, "subtracts the bases instead of dividing by their sum"),
      (r"h = \frac{2A}{b_1} + b_2", 2 * _A / _b1 + _b2, "divides by $b_1$ only, not by the whole sum")]),
    ("The area of a rectangle is", r"A = lw", sp.Eq(_A, _l * _w), _l, "l",
     r"l = \frac{A}{w}", _A / _w,
     [(r"l = Aw", _A * _w, "multiplies by $w$ instead of dividing"),
      (r"l = \frac{w}{A}", _w / _A, "divides in the wrong order"),
      (r"l = A - w", _A - _w, "subtracts $w$ instead of dividing by it")]),
    ("Density is", r"D = \frac{M}{V}", sp.Eq(_D, _M / _V), _M, "M",
     r"M = DV", _D * _V,
     [(r"M = \frac{D}{V}", _D / _V, "divides by $V$ instead of multiplying"),
      (r"M = \frac{V}{D}", _V / _D, "divides in the wrong order"),
      (r"M = D + V", _D + _V, "adds $V$ instead of multiplying by it")]),
    ("The perimeter of a rectangle is", r"P = 2l + 2w", sp.Eq(_P, 2 * _l + 2 * _w), _l, "l",
     r"l = \frac{P - 2w}{2}", (_P - 2 * _w) / 2,
     [(r"l = P - 2w", _P - 2 * _w, "forgets to divide by 2"),
      (r"l = \frac{P + 2w}{2}", (_P + 2 * _w) / 2, "adds $2w$ instead of subtracting it"),
      (r"l = \frac{P}{2} - 2w", _P / 2 - 2 * _w, "divides only $P$ by 2, not $2w$")]),
    ("Distance traveled is", r"d = rt", sp.Eq(_d, _r * _t), _r, "r",
     r"r = \frac{d}{t}", _d / _t,
     [(r"r = dt", _d * _t, "multiplies by $t$ instead of dividing"),
      (r"r = \frac{t}{d}", _t / _d, "divides in the wrong order"),
      (r"r = d - t", _d - _t, "subtracts $t$ instead of dividing by it")]),
]


def _formula_problem(rng):
    intro, ftex, eq, var, vtex, atex, aexpr, wrongs = rng.choice(_FORMULAS)
    sols = sp.solve(eq, var)
    ok_ans = len(sols) == 1 and sp.simplify(sols[0] - aexpr) == 0
    for _, wexpr, _ in wrongs:
        need(sp.simplify(wexpr - aexpr) != 0, "equivalent distractor")
    stem = choose(rng,
                  f"{intro} ${ftex}$. Which equation gives ${vtex}$ in terms of the other variables?",
                  f"Solve the formula ${ftex}$ for ${vtex}$.",
                  f"{intro} ${ftex}$. Solve this formula for ${vtex}$.")
    # step text: describe the inverse operations by hand for each formula
    other = atex.split("=", 1)[1].strip()
    steps = [f"Treat every letter except ${vtex}$ as if it were a number. Undo what is being done "
             f"to ${vtex}$, in reverse order, doing the same thing to both sides.",
             _FORMULA_STEPS[ftex + "|" + vtex],
             f"So ${atex}$."]
    return Problem(
        stem=stem,
        answer=f"${atex}$",
        fmt=text,
        wrong=[(f"${t}$", why) for t, _, why in wrongs],
        steps=steps,
        verify=lambda s: ok_ans and s == f"${atex}$",
        tip=f"Check with easy numbers: pick values for the other letters, find ${vtex}$, and see that the original formula holds.",
    )


_FORMULA_STEPS = {
    r"A = \frac{1}{2}bh|h": r"Multiply both sides by 2 to clear the fraction: $2A = bh$. Then divide both sides by $b$: $\frac{2A}{b} = h$.",
    r"P = 2l + 2w|w": r"Subtract $2l$ from both sides: $P - 2l = 2w$. Then divide both sides by 2: $\frac{P - 2l}{2} = w$.",
    r"P = 2l + 2w|l": r"Subtract $2w$ from both sides: $P - 2w = 2l$. Then divide both sides by 2: $\frac{P - 2w}{2} = l$.",
    r"d = rt|t": r"$t$ is multiplied by $r$, so divide both sides by $r$: $\frac{d}{r} = t$.",
    r"d = rt|r": r"$r$ is multiplied by $t$, so divide both sides by $t$: $\frac{d}{t} = r$.",
    r"I = Prt|r": r"$r$ is multiplied by $P$ and by $t$, so divide both sides by $Pt$: $\frac{I}{Pt} = r$.",
    r"V = lwh|h": r"$h$ is multiplied by $l$ and by $w$, so divide both sides by $lw$: $\frac{V}{lw} = h$.",
    r"F = \frac{9}{5}C + 32|C": r"Subtract 32 from both sides: $F - 32 = \frac{9}{5}C$. Then multiply both sides by the reciprocal $\frac{5}{9}$: $\frac{5}{9}(F - 32) = C$.",
    r"y = mx + b|x": r"Subtract $b$ from both sides: $y - b = mx$. Then divide both sides by $m$: $\frac{y - b}{m} = x$.",
    r"C = 2\pi r|r": r"$r$ is multiplied by $2\pi$, so divide both sides by $2\pi$: $\frac{C}{2\pi} = r$.",
    r"P = a + b + c|c": r"Subtract $a$ and subtract $b$ from both sides: $P - a - b = c$.",
    r"v = u + at|t": r"Subtract $u$ from both sides: $v - u = at$. Then divide both sides by $a$: $\frac{v - u}{a} = t$.",
    r"A = \frac{1}{2}(b_1 + b_2)h|h": r"Multiply both sides by 2: $2A = (b_1 + b_2)h$. Then divide both sides by the whole sum $(b_1 + b_2)$: $\frac{2A}{b_1 + b_2} = h$.",
    r"A = lw|l": r"$l$ is multiplied by $w$, so divide both sides by $w$: $\frac{A}{w} = l$.",
    r"D = \frac{M}{V}|M": r"$M$ is divided by $V$, so multiply both sides by $V$: $DV = M$.",
}


@template("MK")
def literal_eq(rng, lvl):
    if lvl >= 3 and rng.random() < 0.5:
        return _formula_problem(rng)
    # numeric: ax + by = c  ->  y = mm x + kk
    bb = rng.choice([-1, -2, -3, -4, -5, 2, 3, 4, 5])
    if lvl <= 2:
        mm = Q(rng.choice([v for v in range(-5, 6) if v != 0]))
        aa = -bb * mm
    else:
        aa = rng.choice([v for v in range(-9, 10) if v != 0])
        need(aa % bb != 0)
        mm = Q(-aa) / bb
    kk = Q(rng.choice([v for v in range(-8, 9) if v != 0]))
    cc = bb * kk
    eq = f"{_lin((aa, 'x'), (bb, 'y'))} = {tx(cc)}"
    ans = mm * x + kk
    wrong = [(-mm * x + kk, f"does not change the sign of {m(_lin((aa, 'x')))} when moving it to the other side"),
             (kk - aa * x, f"divides only {m(tx(cc))} by {m(bb)}, not the {m('x')}-term")]
    if bb < 0:
        wrong.append((-mm * x - kk, f"divides by {m(-bb)} instead of {m(bb)}"))
    if abs(bb) != 1:
        wrong.append((cc - aa * x, f"forgets to divide by {m(bb)}"))
    wrong.append((mm * x - kk, "makes a sign error with the constant"))
    by = _lin((bb, "y"))
    steps = [("Move the {0}-term to the right side: ".format(m("x"))
              + (f"subtract {m(_lin((aa, 'x')))} from" if aa > 0 else f"add {m(_lin((-aa, 'x')))} to")
              + f" both sides. {m(f'{by} = {_lin((-aa, "x"), (cc, ""))}')}.")]
    if bb != 1:
        steps.append(f"Divide \\emph{{every}} term by {m(bb)}: "
                     f"{m(f'y = {F(_lin((-aa, "x")), bb)} + {F(tx(cc), bb)}')}.")
    steps.append(f"Simplify: {m(f'y = {_lin((mm, "x"), (kk, ""))}')}.")
    sol = sp.solve(sp.Eq(aa * x + bb * y, cc), y)
    return Problem(
        stem=choose(rng, f"Solve {m(eq)} for $y$.",
                    f"Which equation is the same as {m(eq)}, solved for $y$?",
                    f"If {m(eq)}, which of the following expresses $y$ in terms of $x$?"),
        answer=ans,
        fmt=_yfmt,
        wrong=wrong,
        steps=steps,
        check=sol[0] if len(sol) == 1 else None,
        verify=lambda v: all(aa * t + bb * Q(v).subs(x, t) == cc for t in (-3, 0, 2, 7)),
    )


# ---- reading the question ---------------------------------------------------

@template("MK")
def expression_value(rng, lvl):
    if lvl <= 2:
        a = rng.choice([v for v in range(-6, 8) if abs(v) >= 2])
        X = Q(rng.choice([v for v in range(-8, 11) if v not in (0, 1)]))
        b = rng.choice([v for v in range(-15, 16) if v != 0])
        c = a * X + b
        p = rng.randint(2, 5)
        q = rng.choice([v for v in range(-9, 10) if v != 0])
        target = _lin((p, "x"), (q, ""))
        ans = p * X + q
        need(ans != X)
        eq = f"{_lin((a, 'x'), (b, ''))} = {tx(c)}"
        Xw = (c + b) / Q(a)
        wrong = [(X, f"gives the value of {m('x')}, not of {m(target)}"),
                 (p * X, f"forgets the {m(tx(q))} in {m(target)}"),
                 (p * Xw + q, f"moves {m(tx(b))} across without changing its sign when solving")]
        steps = [f"First solve for {m('x')}. " + _const_step(b, _lin((a, "x")), c),
                 _div_step(a, c - b),
                 f"The question asks for {m(target)}, not {m('x')}. Substitute: "
                 f"{m(f'{p}{_p(X)}{_plus(q)} = {tx(p * X)}{_plus(q)} = {tx(ans)}')}."]
        stem = choose(rng, f"If {m(eq)}, what is the value of {m(target)}?",
                      f"If {m(eq)}, then {m(target)} equals")
        if stem.endswith("equals"):
            stem += " which of the following?"
        return Problem(stem=stem, answer=ans, fmt=frac, wrong=wrong, steps=steps,
                       check=(p * _solve(a * x + b, c) + q), neg_ok=True,
                       tip="Always reread the question before choosing: finding $x$ is only part of the job.")
    # level 3: scale the whole expression instead of solving
    if rng.random() < 0.5:
        a = rng.choice([2, 3, 4, 5, 6])
        bb = rng.choice([v for v in range(-9, 10) if v != 0])
        k = rng.choice([2, 3, 4])
        c = Q(rng.choice([v for v in range(-12, 15) if v not in (0, 1, -1)]))
        need(c != k and c * k != c + k)
        given = _lin((a, "x"), (bb, "y"))
        target = _lin((k * a, "x"), (k * bb, "y"))
        ans = k * c
        steps = [f"You cannot find {m('x')} and {m('y')} separately, and you don't need to. "
                 f"Compare the expressions: every coefficient in {m(target)} is {m(k)} times the one in {m(given)}.",
                 f"So {m(f'{target} = {k}({given})')}.",
                 f"Therefore {m(f'{target} = {k} \\times {_p(c)} = {tx(ans)}')}."]
        wrong = [(c, f"gives the value of {m(given)}, not of {m(target)}"),
                 (c + k, f"adds {m(k)} instead of multiplying by {m(k)}"),
                 (ans + k, None), (ans - k, None)]
        chk = (k * a * x + k * bb * y).subs(y, (c - a * x) / bb)
        return Problem(stem=f"If {m(f'{given} = {tx(c)}')}, what is the value of {m(target)}?",
                       answer=ans, fmt=frac, wrong=wrong, steps=steps,
                       check=sp.simplify(chk), neg_ok=True)
    # one variable, target is a fraction or multiple of the left side
    g = rng.choice([2, 3])
    a0 = rng.randint(1, 4)
    b0 = rng.choice([v for v in range(-9, 10) if v != 0])
    X = Q(rng.choice([v for v in range(-6, 10) if v not in (0, 1)]))
    big = rng.random() < 0.5    # given small, ask big (or the reverse)
    sa, sb = (a0, b0) if big else (g * a0, g * b0)
    ta, tb = (g * a0, g * b0) if big else (a0, b0)
    c = sa * X + sb
    ans = ta * X + tb
    need(len({c, ans, X}) == 3 and ans != 0)
    given, target = _lin((sa, "x"), (sb, "")), _lin((ta, "x"), (tb, ""))
    if big:
        steps = [f"Notice that {m(target)} is exactly {m(g)} times {m(given)}: "
                 f"{m(f'{g}({given}) = {target}')}.",
                 f"So {m(f'{target} = {g} \\times {_p(c)} = {tx(ans)}')}. No need to find {m('x')}."]
        wrong = [(c, f"gives the value of {m(given)}"), (X, f"gives the value of {m('x')}"),
                 (Q(c) / g, f"divides by {m(g)} instead of multiplying")]
    else:
        steps = [f"Notice that {m(target)} is exactly {m(F(1, g))} of {m(given)}: "
                 f"{m(f'{given} = {g}({target})')}.",
                 f"So {m(f'{target} = {tx(c)} \\div {g} = {tx(ans)}')}. No need to find {m('x')}."]
        wrong = [(c, f"gives the value of {m(given)}"), (X, f"gives the value of {m('x')}"),
                 (g * c, f"multiplies by {m(g)} instead of dividing")]
    steps.append(f"Check by solving: {m(f'x = {tx(X)}')}, and {m(f'{ta}{_p(X)}{_plus(tb)} = {tx(ans)}')}. \\checkmark"
                 if ta != 1 else
                 f"Check by solving: {m(f'x = {tx(X)}')}, and {m(f'{tx(X)}{_plus(tb)} = {tx(ans)}')}. \\checkmark")
    return Problem(stem=f"If {m(f'{given} = {tx(c)}')}, what is the value of {m(target)}?",
                   answer=ans, fmt=frac, wrong=wrong, steps=steps,
                   check=ta * _solve(sa * x + sb, c) + tb, neg_ok=True)


# ---- words to equations -------------------------------------------------------

_MULT_WORD = {2: "doubled", 3: "tripled", 4: "quadrupled"}
_TIMES_WORD = {2: "twice", 3: "three times", 4: "four times", 5: "five times",
               6: "six times", 7: "seven times", 8: "eight times", 9: "nine times"}


def _sentence(rng, lvl):
    """A word sentence about 'a number' n.

    Returns (sentence, (tex, lhs, rhs), [(tex, lhs, rhs, why)], procedure,
    solution, note).  procedure(v) evaluates the words literally for v.
    """
    k = rng.randint(2, 9)
    c = rng.randint(2, 15)
    kinds = (["more", "less", "tripled", "subfrom"] if lvl == 1
             else ["sum", "diff", "subfrom", "quot", "decthen", "less"])
    kind = rng.choice(kinds)
    if kind == "tripled":
        k = rng.choice([2, 3, 4])
    N = rng.randint(2, 15)
    K = _TIMES_WORD[k]
    if kind == "more":
        t = k * N + c
        s = f"{c} more than {K} a number is {t}"
        ans = (f"{k}n + {c}", k * n + c)
        wr = [(f"{k}(n + {c})", k * (n + c), f"adds {c} before multiplying by {k}"),
              (f"{k}n - {c}", k * n - c, "subtracts instead of adding"),
              (f"{c}n + {k}", c * n + k, "mixes up which number multiplies $n$")]
        proc = lambda v: k * v + c
        note = f"``{K.capitalize()} a number'' is ${k}n$. ``{c} more than'' that means add {c}: ${k}n + {c}$."
    elif kind in ("less", "subfrom", "diff", "tripled"):
        t = k * N - c
        need(t > 0)
        if kind == "less":
            s = f"{c} less than {K} a number is {t}"
            note = (f"``{K.capitalize()} a number'' is ${k}n$. ``{c} less than'' that means take {c} away "
                    f"\\emph{{from}} ${k}n$: ${k}n - {c}$, not ${c} - {k}n$.")
        elif kind == "subfrom":
            s = f"{c} subtracted from {K} a number gives {t}"
            note = (f"``{c} subtracted from ${k}n$'' means start with ${k}n$ and take {c} away: "
                    f"${k}n - {c}$, not ${c} - {k}n$.")
        elif kind == "diff":
            s = f"the difference between {K} a number and {c} is {t}"
            note = (f"``The difference between $A$ and $B$'' means $A - B$, in that order. "
                    f"Here $A = {k}n$ and $B = {c}$: ${k}n - {c}$.")
        else:
            s = f"a number {_MULT_WORD[k]} and then decreased by {c} is {t}"
            note = (f"``{_MULT_WORD[k].capitalize()}'' means multiplied by {k}: ${k}n$. "
                    f"Then ``decreased by {c}'' means subtract {c}: ${k}n - {c}$.")
        ans = (f"{k}n - {c}", k * n - c)
        wr = [(f"{c} - {k}n", c - k * n, "subtracts in the wrong order"),
              (f"{k}(n - {c})", k * (n - c), f"subtracts {c} before multiplying by {k}"),
              (f"{k}n + {c}", k * n + c, "adds instead of subtracting")]
        if kind == "tripled":
            wr.append((f"n + {k} - {c}", n + k - c, f"adds {k} instead of multiplying by {k}"))
        proc = lambda v: k * v - c
    elif kind == "sum":
        t = k * (N + c)
        s = f"{K} the sum of a number and {c} is {t}"
        ans = (f"{k}(n + {c})", k * (n + c))
        wr = [(f"{k}n + {c}", k * n + c, f"multiplies only the number by {k}, not the whole sum"),
              (f"{k} + n + {c}", k + n + c, f"adds {k} instead of multiplying by it"),
              (f"\\frac{{n + {c}}}{{{k}}}", (n + c) / k, f"divides by {k} instead of multiplying")]
        proc = lambda v: k * (v + c)
        note = (f"``The sum of a number and {c}'' is $n + {c}$. ``{K.capitalize()} the sum'' multiplies the "
                f"\\emph{{whole}} sum, so it needs parentheses: ${k}(n + {c})$.")
    elif kind == "decthen":
        need(N > c)
        t = k * (N - c)
        s = f"when a number is decreased by {c} and the result is multiplied by {k}, the answer is {t}"
        ans = (f"{k}(n - {c})", k * (n - c))
        wr = [(f"{k}n - {c}", k * n - c, f"multiplies before subtracting {c}"),
              (f"{k}({c} - n)", k * (c - n), "subtracts in the wrong order"),
              (f"\\frac{{n - {c}}}{{{k}}}", (n - c) / k, f"divides by {k} instead of multiplying")]
        proc = lambda v: k * (v - c)
        note = (f"First the number is decreased: $n - {c}$. Then that whole result is multiplied by {k}, "
                f"so it needs parentheses: ${k}(n - {c})$.")
    else:  # quot
        t = N + c
        N = k * N
        s = f"a number divided by {k}, plus {c}, equals {t}"
        ans = (f"\\frac{{n}}{{{k}}} + {c}", n / k + c)
        wr = [(f"\\frac{{{k}}}{{n}} + {c}", k / n + c, "divides in the wrong order"),
              (f"\\frac{{n + {c}}}{{{k}}}", (n + c) / k, f"adds {c} before dividing"),
              (f"{k}n + {c}", k * n + c, f"multiplies by {k} instead of dividing")]
        proc = lambda v: R(v, k) + c
        note = f"``A number divided by {k}'' is $\\frac{{n}}{{{k}}}$. Then add {c}: $\\frac{{n}}{{{k}}} + {c}$."
    return s, ans, t, wr, proc, N, note


@template("MK")
def translate(rng, lvl):
    s, (atex, alhs), t, wr, proc, N, note = _sentence(rng, lvl)
    ans_tex = f"${atex} = {t}$"
    # independent check: the left side matches the words, read literally
    good = all(sp.sympify(alhs).subs(n, v) == proc(v) for v in (1, 2, 5, 12))
    ans_sol = sp.solve(sp.Eq(alhs, t), n)
    wrong = []
    for wtex, wlhs, why in wr:
        ws = sp.solve(sp.Eq(wlhs, t), n)
        if ws and ws != ans_sol:      # not an equivalent equation
            wrong.append((f"${wtex} = {t}$", why))
    need(len(wrong) >= 3)
    sentence = s[0].upper() + s[1:]
    return Problem(
        stem=choose(rng,
                    f"Let $n$ be a number. Which equation means ``{sentence}''?",
                    f"``{sentence}.'' If $n$ stands for the number, which equation represents this sentence?"),
        answer=ans_tex,
        fmt=text,
        wrong=wrong,
        steps=["Translate piece by piece. Let $n$ be the number; ``is,'' ``gives,'' and ``equals'' "
               "all become ``$=$.''",
               note,
               f"The equation is {ans_tex}."],
        tip=f"Check with the solution: {m(f'n = {N}')} makes {ans_tex} true.",
        verify=lambda v: good and v == ans_tex and ans_sol == [N],
    )


@template("AR")
def number_puzzle(rng, lvl):
    k = rng.randint(2, 6) if lvl == 1 else rng.randint(2, 9)
    c = rng.randint(2, 20)
    N = rng.randint(2, 20) if lvl == 1 else rng.randint(3, 30)
    kinds = ["plus", "minus", "story_plus", "story_minus"] if lvl == 1 else ["sum", "quot", "minus", "story_minus", "both"]
    kind = rng.choice(kinds)
    who = person(rng)
    if kind == "plus":
        t = k * N + c
        stem = choose(rng, f"When {c} is added to {_TIMES_WORD[k]} a number, the result is {t}. What is the number?",
                      f"{c} more than {_TIMES_WORD[k]} a number is {t}. What is the number?")
        eq, A, B = f"{k}n + {c} = {t}", k, c
        wrong = [((t + c) / Q(k), f"adds {c} instead of subtracting it"),
                 (Q(t - c), f"forgets to divide by {k}"),
                 (Q(t) / k - c, f"divides {t} by {k} but forgets to divide {c}")]
    elif kind == "minus":
        t = k * N - c
        need(t > 0)
        stem = choose(rng, f"A number is multiplied by {k}, and then {c} is subtracted. The result is {t}. What is the number?",
                      f"If {c} is subtracted from {_TIMES_WORD[k]} a number, the result is {t}. What is the number?")
        eq, A, B = f"{k}n - {c} = {t}", k, -c
        wrong = [((t - c) / Q(k), f"subtracts {c} instead of adding it"),
                 (Q(t + c), f"forgets to divide by {k}"),
                 (Q(t) / k + c, f"divides {t} by {k} but forgets to divide {c}")]
    elif kind == "story_plus":
        t = k * N + c
        if rng.random() < 0.5:
            stem = (f"{who.name} did some push-ups on Monday. On Tuesday {who.he} did {c} more than "
                    f"{_TIMES_WORD[k]} as many, for a total of {t} push-ups on Tuesday. "
                    f"How many push-ups did {who.he} do on Monday?")
        else:
            stem = (f"A supply sergeant ordered some boxes of batteries in March. In April the order was "
                    f"{c} boxes more than {_TIMES_WORD[k]} the March order, or {t} boxes. "
                    f"How many boxes were ordered in March?")
        eq, A, B = f"{k}n + {c} = {t}", k, c
        wrong = [((t + c) / Q(k), f"adds {c} instead of subtracting it"),
                 (Q(t - c), f"forgets to divide by {k}"),
                 (Q(t) / k - c, f"divides {t} by {k} but forgets to divide {c}")]
    elif kind == "story_minus":
        t = k * N - c
        need(t > 0)
        stem = choose(rng,
                      f"{who.name} had some money saved. After {who.he} {_MULT_WORD.get(k, f'multiplied it by {k}') if k in _MULT_WORD else f'multiplied it by {k}'} "
                      f"the amount and then spent \\${c}, {who.he} had \\${t} left. How many dollars did {who.he} start with?",
                      f"A platoon ran a number of miles in week 1. In week 2 it ran {c} miles less than "
                      f"{_TIMES_WORD[k]} the week-1 distance, for a total of {t} miles. How many miles did it run in week 1?")
        eq, A, B = f"{k}n - {c} = {t}", k, -c
        wrong = [((t - c) / Q(k), f"subtracts {c} instead of adding it"),
                 (Q(t + c), f"forgets to divide by {k}"),
                 (Q(t) / k + c, f"divides {t} by {k} but forgets to divide {c}")]
    elif kind == "sum":
        t = k * (N + c)
        stem = f"{_TIMES_WORD[k].capitalize()} the sum of a number and {c} is {t}. What is the number?"
        steps = [f"Let $n$ be the number. The sum comes first, so it goes in parentheses: {m(f'{k}(n + {c}) = {t}')}.",
                 f"Divide both sides by {m(k)}: {m(f'n + {c} = {t // k}')}.",
                 f"Subtract {m(c)}: {m(f'n = {t // k} - {c} = {N}')}."]
        wrong = [(Q(t - c) / k, f"writes {m(f'{k}n + {c}')}, multiplying only the number by {k}"),
                 (Q(t // k + c), f"adds {c} instead of subtracting it"),
                 (Q(t // k), f"forgets to subtract {c}")]
        return Problem(stem=stem, answer=Q(N), fmt=frac, wrong=wrong, steps=steps,
                       verify=lambda v: k * (v + c) == t, check=_solve(k * (n + c), t, n),
                       section="AR")
    elif kind == "quot":
        t = N + c
        stem = f"When a number is divided by {k} and then {c} is added, the result is {t}. What is the number?"
        steps = [f"Let $n$ be the number: {m(f'\\frac{{n}}{{{k}}} + {c} = {t}')}.",
                 f"Subtract {m(c)} from both sides: {m(f'\\frac{{n}}{{{k}}} = {N}')}.",
                 f"Multiply both sides by {m(k)}: {m(f'n = {N} \\times {k} = {N * k}')}."]
        wrong = [(Q(N), f"forgets to multiply by {k} at the end"),
                 (Q(t * k - c), f"multiplies {t} by {k} but forgets to multiply {c}"),
                 (Q((t + c) * k), f"adds {c} instead of subtracting it")]
        return Problem(stem=stem, answer=Q(N * k), fmt=frac, wrong=wrong, steps=steps,
                       verify=lambda v: v / k + c == t, check=_solve(n / k + c, t, n),
                       section="AR")
    else:  # both: k n + c = j n + d  ("the same result")
        j = rng.randint(1, k - 1) if k > 2 else 1
        d = (k - j) * N + c
        stem = (f"Adding {c} to {_TIMES_WORD[k]} a number gives the same result as adding {d} to "
                f"{'the number' if j == 1 else _TIMES_WORD[j] + ' the number'}. What is the number?")
        jn = "n" if j == 1 else f"{j}n"
        steps = [f"Let $n$ be the number: {m(f'{k}n + {c} = {jn} + {d}')}.",
                 f"Subtract {m(jn)} from both sides: {m(f'{_lin((k - j, "n"))} + {c} = {d}')}.",
                 f"Subtract {m(c)}: {m(f'{_lin((k - j, "n"))} = {d - c}')}."
                 + (f" Divide by {m(k - j)}: {m(f'n = {N}')}." if k - j != 1 else "")]
        wrong = [(Q(d - c) / (k + j), "adds the $n$-terms instead of subtracting"),
                 (Q(d + c) / (k - j), f"adds {c} instead of subtracting it"),
                 (Q(d - c), f"forgets to divide by {k - j}") if k - j != 1 else (Q(d + c), None)]
        return Problem(stem=stem, answer=Q(N), fmt=frac, wrong=wrong, steps=steps,
                       verify=lambda v: k * v + c == j * v + d, check=_solve(k * n + c, j * n + d, n),
                       section="AR")
    steps = [f"Let $n$ be the unknown number and write the sentence as an equation: {m(eq)}.",
             _const_step(B, f"{k}n", t),
             f"Divide both sides by {m(k)}: {m(f'n = {F(t - B, k)} = {N}')}."]
    return Problem(stem=stem, answer=Q(N), fmt=frac, wrong=wrong, steps=steps,
                   verify=lambda v: A * v + B == t, check=_solve(A * n + B, t, n),
                   section="AR")


@template("AR")
def consecutive(rng, lvl):
    if lvl <= 2:
        step, count = 1, rng.choice([2, 3, 3])
        kind = "integers"
    else:
        step, count = 2, rng.choice([2, 3, 3, 4])
        kind = rng.choice(["even", "odd"])
    N = rng.randint(5, 60)
    if kind == "even" and N % 2:
        N += 1
    if kind == "odd" and N % 2 == 0:
        N += 1
    vals = [N + step * i for i in range(count)]
    S = sum(vals)
    which = rng.choice(["smallest", "largest"] + (["middle"] if count == 3 else []))
    ans = {"smallest": vals[0], "largest": vals[-1], "middle": vals[1] if count == 3 else None}[which]
    word = {"integers": "consecutive integers", "even": "consecutive even integers",
            "odd": "consecutive odd integers"}[kind]
    count_w = {2: "two", 3: "three", 4: "four"}[count]
    ctx = rng.random()
    if kind == "integers" and count == 2 and ctx < 0.5:
        stem = (f"A book is open to two facing pages. The sum of the two page numbers is {S}. "
                f"What is the {'larger' if which == 'largest' else 'smaller'} page number?")
    elif kind != "integers" and ctx < 0.4:
        stem = (f"The barracks rooms on one side of a hallway are numbered with {word}. "
                f"The numbers on {count_w} rooms in a row add up to {S}. What is the "
                f"{which if count > 2 else ('larger' if which == 'largest' else 'smaller')} room number?")
    else:
        stem = (f"The sum of {count_w} {word} is {S}. What is the "
                f"{which if count > 2 else ('larger' if which == 'largest' else 'smaller')} of these integers?")
    terms = ", ".join(_lin((1, "n"), (step * i, "")) for i in range(count))
    total = step * count * (count - 1) // 2
    steps = [f"Let $n$ be the smallest. {word.capitalize()} go up by {m(step)}, so the numbers are {m(terms)}.",
             f"Add them: {m(f'{count}n + {total} = {S}')}.",
             f"Subtract {m(total)}: {m(f'{count}n = {S - total}')}. Divide by {m(count)}: {m(f'n = {N}')}."]
    if which != "smallest":
        steps.append(f"The numbers are {', '.join(m(v) for v in vals)}. The {which if count > 2 else ('larger' if which == 'largest' else 'smaller')} is {m(ans)}.")
    else:
        steps.append(f"Check: {m(' + '.join(str(v) for v in vals) + f' = {S}')}. \\checkmark")
    wrong = []
    for i, v in enumerate(vals):
        if v != ans:
            wrong.append((Q(v), "is one of the other integers in the list"))
    if step == 2:
        wrong.append((Q(ans + (1 if which != "smallest" else -1)) if which != "smallest" else Q(N + 1),
                      "counts by 1 instead of by 2"))
    if Q(S) / count != ans and (Q(S) / count).is_integer:
        wrong.append((Q(S) / count, "divides the sum by the number of integers and stops"))
    # brute-force check
    hits = [k for k in range(-200, 400) if sum(k + step * i for i in range(count)) == S
            and (kind == "integers" or k % 2 == (0 if kind == "even" else 1))]
    need(len(hits) == 1)
    chk = {"smallest": hits[0], "largest": hits[0] + step * (count - 1), "middle": hits[0] + step}[which]
    return Problem(stem=stem, answer=Q(ans), fmt=frac, wrong=wrong, steps=steps,
                   check=Q(chk), section="AR")


@template("AR")
def cost_equation(rng, lvl):
    who = person(rng)
    ctx = rng.choice(["plumber", "taxi", "gym", "range", "tow", "truck"])
    if ctx == "plumber":
        fee, rate, k = rng.randrange(40, 95, 5), rng.randrange(35, 100, 5), rng.randint(2, 8)
        u, U = "hour", "hours"
        stem = (f"A plumber charges a {{FEE}} service fee plus {{RATE}} per hour. {who.name}'s bill was {{T}}. "
                f"How many hours did the plumber work?")
    elif ctx == "taxi":
        fee, rate, k = R(rng.randrange(250, 450, 25), 100), R(rng.randrange(150, 325, 25), 100), rng.randint(3, 18)
        u, U = "mile", "miles"
        stem = (f"A taxi charges {{FEE}} to start the ride plus {{RATE}} per mile. "
                f"{who.name}'s ride cost {{T}}. How many miles long was the ride?")
    elif ctx == "gym":
        fee, rate, k = rng.randrange(25, 105, 5), rng.randrange(15, 50, 5), rng.randint(3, 12)
        u, U = "month", "months"
        stem = (f"A gym charges a one-time sign-up fee of {{FEE}} plus {{RATE}} per month. "
                f"{who.name} has paid {{T}} in all. For how many months has {who.he} been a member?")
    elif ctx == "range":
        fee, rate, k = rng.randrange(100, 425, 25), rng.randrange(5, 21), rng.randint(12, 40)
        u, U = "soldier", "soldiers"
        stem = (f"{soldier(rng)} reserved a training range for a {{FEE}} flat fee plus {{RATE}} per soldier "
                f"for ammunition. The total bill was {{T}}. How many soldiers trained?")
    elif ctx == "tow":
        fee, rate, k = rng.randrange(50, 130, 5), rng.choice([3, 4, 5, 6]), rng.randint(8, 40)
        u, U = "mile", "miles"
        stem = (f"A towing service charges {{FEE}} to hook up a vehicle plus {{RATE}} per mile. "
                f"Towing a disabled truck back to base cost {{T}}. How many miles was it towed?")
    else:
        fee, rate, k = rng.randrange(20, 45, 5), R(rng.choice([50, 60, 75, 80]), 100), rng.choice(range(20, 160, 10))
        u, U = "mile", "miles"
        stem = (f"A moving truck rents for {{FEE}} per day plus {{RATE}} per mile. {who.name} rented the truck "
                f"for one day and paid {{T}}. How many miles did {who.he} drive?")
    fee, rate = Q(fee), Q(rate)
    T = fee + rate * k
    mo = lambda v: (r"\$" + dec_raw(v, places=2)) if not Q(v).is_integer else (r"\$" + int_raw(v))
    stem = stem.replace("{FEE}", mo(fee)).replace("{RATE}", mo(rate)).replace("{T}", mo(T))
    mr = lambda v: dec_raw(v, places=2) if not Q(v).is_integer else int_raw(v)
    var = u[0]
    steps = [f"Let {m(var)} be the number of {U}. The total is the fixed fee plus "
             f"{mo(rate)} for each {u}: {m(f'{mr(fee)} + {mr(rate)}{var} = {mr(T)}')}.",
             f"Subtract the fee from both sides: {m(f'{mr(rate)}{var} = {mr(T)} - {mr(fee)} = {mr(T - fee)}')}.",
             f"Divide by the rate: {m(f'{var} = {mr(T - fee)} \\div {mr(rate)} = {int_raw(k)}')} {U}."]
    wrong = [(T / rate, "ignores the fixed fee"),
             ((T + fee) / rate, "adds the fee instead of subtracting it"),
             (T - fee, "forgets to divide by the rate"),
             (Q(k + 1), None), (Q(k - 1), None)]
    hits = [h for h in range(0, 1000) if fee + rate * h == T]
    return Problem(stem=stem, answer=Q(k), fmt=unit(dec, u), wrong=wrong, steps=steps,
                   check=Q(hits[0]) if len(hits) == 1 else None,
                   verify=lambda v: fee + rate * v == T, section="AR")


PLAN = [
    # (template, level, count)  -- easy -> hard; 25 problems
    (basic_eq, 1, 3),
    (translate, 1, 2),
    (fraction_eq, 1, 1),
    (number_puzzle, 1, 2),
    (basic_eq, 2, 1),
    (both_sides, 2, 2),
    (distribute, 2, 1),
    (decimal_eq, 2, 1),
    (literal_eq, 2, 1),
    (expression_value, 2, 1),
    (cost_equation, 2, 2),
    (consecutive, 2, 1),
    (distribute, 3, 1),
    (fraction_eq, 3, 1),
    (literal_eq, 3, 1),
    (expression_value, 3, 1),
    (both_sides, 3, 1),
    (consecutive, 3, 1),
    (translate, 3, 1),
]
