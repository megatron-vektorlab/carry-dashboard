"""Chapter 12 - Inequalities."""
import math
from fractions import Fraction

import sympy as sp

from ..core import (R, Q, Problem, need, num, frac, m, F, tx, dec_raw, int_raw,
                    frac_raw, mixed_raw, text, unit, person, soldier, choose, template)

NUM = 12
TITLE = "Inequalities"
PART = 2

INTRO = r"""
An \emph{inequality} compares two quantities that need not be equal. Its
solution is usually a whole range of numbers, not a single value. You solve
it almost exactly like an equation, with \textbf{one} extra rule.

\begin{concept}{Symbols and the number line}
\begin{tabular}{@{}lll@{}}
$x < 3$ & $x$ is less than $3$ & open circle at $3$, shade left \\
$x > 3$ & $x$ is greater than $3$ & open circle at $3$, shade right \\
$x \le 3$ & $x$ is at most $3$ (no more than $3$) & closed dot at $3$, shade left \\
$x \ge 3$ & $x$ is at least $3$ (no less than $3$) & closed dot at $3$, shade right \\
\end{tabular}

\smallskip
\begin{center}
\begin{tikzpicture}[scale=0.55]
\draw[-{Stealth}] (-5.6,0) -- (5.6,0);
\foreach \t in {-5,...,5} \draw (\t,0.12) -- (\t,-0.12) node[below] {\scriptsize $\t$};
\draw[line width=2.2pt] (-2,0) -- (5.4,0);
\draw[fill=white, thick] (-2,0) circle (0.17);
\node[above] at (1.5,0.2) {\small $x > -2$};
\end{tikzpicture}
\end{center}
\end{concept}

\begin{concept}{Solving: one extra rule}
Add or subtract any number on both sides, and multiply or divide both sides
by a \emph{positive} number, exactly as with equations. But when you
\textbf{multiply or divide both sides by a negative number, flip the
inequality sign}:
\[ -2x < 6 \;\Rightarrow\; x > -3 \]
\emph{Compound} inequalities have three parts; do the same thing to all
three: $-3 < 2x + 1 \le 9 \Rightarrow -4 < 2x \le 8 \Rightarrow -2 < x \le 4$.
\end{concept}

\begin{concept}{Absolute value}
$|x - 3|$ is the distance between $x$ and $3$ on the number line.
\begin{itemize}
\item $|x - 3| < 5$: within $5$ of $3$, so $-2 < x < 8$ (one ``between'' piece).
\item $|x - 3| > 5$: more than $5$ away, so $x < -2$ or $x > 8$ (two pieces).
\end{itemize}
\end{concept}

\begin{example}{Worked example}
Solve $5 - 3x \ge 17$.

\textbf{Solution.} Subtract $5$ from both sides: $-3x \ge 12$. Divide both
sides by $-3$ and \emph{flip} the sign: $x \le -4$. Check with $x = -5$:
$5 - 3(-5) = 20$, and $20 \ge 17$. \checkmark
\end{example}

\begin{tip}
Test a point. Pick an easy number in your answer (such as $0$, if it is
included) and substitute it into the \emph{original} inequality. If it
makes a true statement, the direction of your sign is right.
\end{tip}

\begin{trap}
\begin{itemize}
\item Forgetting to flip the sign after dividing by a negative number.
\item Flipping when you only \emph{subtracted} a number: $x - 5 > 2$ is
  simply $x > 7$.
\item Mixing up $<$ and $\le$: ``at least $10$'' includes $10$.
\item Rounding the wrong way in word problems: to earn \emph{at least} a
  goal, round the number of hours \emph{up}.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# private helpers
# --------------------------------------------------------------------------

_TEX = {"<": "<", ">": ">", "le": r"\le", "ge": r"\ge"}
_FLIP = {"<": ">", ">": "<", "le": "ge", "ge": "le"}
_STRICT = {"<": "le", "le": "<", ">": "ge", "ge": ">"}     # toggle the endpoint
_WORD = {"<": "less than", ">": "greater than", "le": "less than or equal to",
         "ge": "greater than or equal to"}


def _holds(op, u, v):
    """Independent numeric meaning of each symbol."""
    if op == "<":
        return u < v
    if op == ">":
        return u > v
    if op == "le":
        return u <= v
    return u >= v


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


def _subst(X, *terms):
    """Substitute X into (coef, var) terms in the written order: '3(5) - 4'."""
    out = ""
    for c, v in terms:
        c = Q(c)
        if c == 0:
            continue
        if v and abs(c) != 1:
            body = f"{tx(abs(c))}({tx(X)})"
        elif v:
            first = not out and c > 0
            body = tx(X) if (Q(X) >= 0 or first) else f"({tx(X)})"
        else:
            body = tx(abs(c))
        if not out:
            out = ("-" if c < 0 else "") + body
        else:
            out += (" - " if c < 0 else " + ") + body
    return out


def _ray(op, bound, var="x"):
    """(LaTeX choice, predicate) for 'x op bound'."""
    b = Q(bound)
    return (f"${var} {_TEX[op]} {tx(b)}$", lambda t: _holds(op, t, b))


def _between(lo, lo_op, hi, hi_op, var="x"):
    """lo (< or le) x (< or le) hi."""
    lo, hi = Q(lo), Q(hi)
    return (f"${tx(lo)} {_TEX[lo_op]} {var} {_TEX[hi_op]} {tx(hi)}$",
            lambda t: _holds(lo_op, lo, t) and _holds(hi_op, t, hi))


def _outside(lo, lo_op, hi, hi_op, var="x"):
    """x (< or le) lo  or  x (> or ge) hi."""
    lo, hi = Q(lo), Q(hi)
    return (f"${var} {_TEX[lo_op]} {tx(lo)}$ or ${var} {_TEX[hi_op]} {tx(hi)}$",
            lambda t: _holds(lo_op, t, lo) or _holds(hi_op, t, hi))


def _grid(*marks):
    """Test points: quarters from -60 to 60 plus every endpoint and its neighbours."""
    pts = {Fraction(k, 4) for k in range(-240, 241)}
    for b in marks:
        b = Fraction(int(sp.numer(Q(b))), int(sp.denom(Q(b))))
        pts |= {b, b - Fraction(1, 100), b + Fraction(1, 100)}
    return sorted(pts)


def _agree(p, q, grid):
    return all(bool(p(t)) == bool(q(t)) for t in grid)


def _keep_wrong(cands, orig, grid, ans_tex):
    """Drop distractors that are the same set as the answer (or repeat)."""
    out, seen = [], {ans_tex}
    for (tex, pred), why in cands:
        if tex in seen or _agree(pred, orig, grid):
            continue
        seen.add(tex)
        out.append((tex, why))
    return out


def _div_text(a, op):
    """Words for dividing both sides of an inequality by a."""
    if a > 0:
        return f"Divide both sides by {m(tx(a))}. Dividing by a positive number keeps the sign the same"
    return (f"Divide both sides by {m(tx(a))}. Dividing by a \\emph{{negative}} number flips the sign: "
            f"{m(_TEX[op])} becomes {m(_TEX[_FLIP[op]])}")


def _const_text(b, lhs_tex, op, rhs):
    new = Q(rhs) - b
    if b > 0:
        return (f"Subtract {m(tx(b))} from both sides (adding or subtracting never changes the sign): "
                f"{m(f'{lhs_tex} {_TEX[op]} {tx(rhs)} - {tx(b)}')}, so {m(f'{lhs_tex} {_TEX[op]} {tx(new)}')}.")
    return (f"Add {m(tx(-b))} to both sides (adding or subtracting never changes the sign): "
            f"{m(f'{lhs_tex} {_TEX[op]} {tx(rhs)} + {tx(-b)}')}, so {m(f'{lhs_tex} {_TEX[op]} {tx(new)}')}.")


def _ask(rng, ineq):
    return choose(rng,
                  f"Solve the inequality {m(ineq)}.",
                  f"Which of the following is the solution of {m(ineq)}?",
                  f"Which inequality describes all values of $x$ that make {m(ineq)} true?")


# --------------------------------------------------------------------------
# templates
# --------------------------------------------------------------------------

@template("MK")
def solve_ineq(rng, lvl):
    op = rng.choice(["<", ">", "le", "ge"])
    B = Q(rng.choice([v for v in range(-9, 13) if v != 0]))      # the boundary
    if lvl == 1:
        kind = rng.choice(["add", "mul", "two", "two"])
    else:
        kind = rng.choice(["neg", "neg", "rev"])
    if kind == "add":
        a = rng.choice([v for v in range(-15, 16) if v not in (0,)])
        c = B + a
        ineq = f"{_lin((1, 'x'), (a, ''))} {_TEX[op]} {tx(c)}"
        orig = lambda t: _holds(op, t + a, c)
        steps = [_const_text(a, "x", op, c)]
        cands = [(_ray(op, c + a), f"{'adds' if a > 0 else 'subtracts'} {m(abs(a))} instead of "
                                   f"{'subtracting' if a > 0 else 'adding'} it"),
                 (_ray(_FLIP[op], B), "flips the sign, but you flip only when multiplying or dividing by a negative number"),
                 (_ray(_STRICT[op], B), f"uses {m(_TEX[_STRICT[op]])} instead of {m(_TEX[op])}")]
        test_terms = [(1, "x"), (a, "")]
    elif kind == "mul":
        a = rng.randint(2, 9)
        c = a * B
        ineq = f"{a}x {_TEX[op]} {tx(c)}"
        orig = lambda t: _holds(op, a * t, c)
        steps = [_div_text(a, op) + f": {m(f'x {_TEX[op]} {F(tx(c), a)}')}, so {m(f'x {_TEX[op]} {tx(B)}')}."]
        cands = [(_ray(_FLIP[op], B), f"flips the sign, but {m(a)} is positive"),
                 (_ray(op, c - a), f"subtracts {m(a)} instead of dividing by it"),
                 (_ray(op, c * a), f"multiplies by {m(a)} instead of dividing"),
                 (_ray(_STRICT[op], B), f"uses {m(_TEX[_STRICT[op]])} instead of {m(_TEX[op])}")]
        test_terms = [(a, "x")]
    else:
        if kind == "two":
            a = rng.randint(2, 9)
        else:
            a = -rng.randint(2, 9)
        b = rng.choice([v for v in range(-20, 21) if v != 0])
        c = a * B + b
        rev = kind == "rev"
        ineq = (f"{tx(b)} - {-a}x {_TEX[op]} {tx(c)}" if rev
                else f"{_lin((a, 'x'), (b, ''))} {_TEX[op]} {tx(c)}")
        orig = lambda t: _holds(op, a * t + b, c)
        fop = op if a > 0 else _FLIP[op]
        steps = [_const_text(b, _lin((a, "x")), op, c),
                 _div_text(a, op) + f": {m(f'x {_TEX[fop]} {F(tx(c - b), tx(a))}')}, so {m(f'x {_TEX[fop]} {tx(B)}')}."]
        cands = []
        if a < 0:
            cands.append((_ray(op, B), f"forgets to flip the sign when dividing by {m(a)}"))
            cands.append((_ray(fop, -B), f"makes a sign error when dividing by {m(a)}"))
        else:
            cands.append((_ray(_FLIP[op], B), "flips the sign, but you flip only when dividing by a negative number"))
        cands += [(_ray(fop, Q(c + b) / a), f"moves {m(tx(b))} across without changing its sign"),
                  (_ray(fop, Q(c - b)), f"forgets to divide by {m(a)}"),
                  (_ray(_STRICT[fop], B), f"uses {m(_TEX[_STRICT[fop]])} instead of {m(_TEX[fop])}")]
        test_terms = [(b, ""), (a, "x")] if rev else [(a, "x"), (b, "")]
    ans_tex, ans_pred = _ray(_final_op(kind, op), B)
    grid = _grid(B, c)
    need(_agree(ans_pred, orig, grid))
    # a test point inside the solution (one unit past the boundary)
    fop = _final_op(kind, op)
    tpt = B + (1 if fop in (">", "ge") else -1)
    lhs_val = sum(Q(cf) * (tpt if v else 1) for cf, v in test_terms)
    steps.append(f"Check with a number in the answer, {m(f'x = {tx(tpt)}')}: "
                 f"{m(f'{_subst(tpt, *test_terms)} = {tx(lhs_val)}')}, and "
                 f"{m(f'{tx(lhs_val)} {_TEX[op]} {tx(c)}')} is true. \\checkmark")
    return Problem(
        stem=_ask(rng, ineq),
        answer=ans_tex,
        fmt=text,
        wrong=_keep_wrong(cands, orig, grid, ans_tex),
        steps=steps,
        verify=lambda s: s == ans_tex and _agree(ans_pred, orig, grid),
    )


def _final_op(kind, op):
    return _FLIP[op] if kind in ("neg", "rev") else op


@template("MK")
def both_sides_ineq(rng, lvl):
    op = rng.choice(["<", ">", "le", "ge"])
    B = Q(rng.choice([v for v in range(-9, 11) if v != 0]))
    c = rng.randint(1, 6)
    a = c + rng.randint(1, 5) if lvl <= 2 else c - rng.randint(2, 6)
    need(a != 0)
    b = rng.choice([v for v in range(-15, 16) if v != 0])
    d = (a - c) * B + b
    need(d != b)
    ineq = f"{_lin((a, 'x'), (b, ''))} {_TEX[op]} {_lin((c, 'x'), (d, ''))}"
    orig = lambda t: _holds(op, a * t + b, c * t + d)
    k = a - c
    fop = op if k > 0 else _FLIP[op]
    move = (f"Collect the {m('x')}-terms on the left: subtract {m(_lin((c, 'x')))} from both sides. "
            f"{m(f'{_lin((k, "x"), (b, ""))} {_TEX[op]} {tx(d)}')}.")
    steps = [move,
             _const_text(b, _lin((k, "x")), op, d),
             _div_text(k, op) + f": {m(f'x {_TEX[fop]} {F(tx(d - b), tx(k))}')}, so {m(f'x {_TEX[fop]} {tx(B)}')}."]
    if k == 1:
        steps.pop()
    cands = []
    if k < 0:
        cands.append((_ray(op, B), f"forgets to flip the sign when dividing by {m(k)}"))
        cands.append((_ray(fop, -B), f"makes a sign error when dividing by {m(k)}"))
    else:
        cands.append((_ray(_FLIP[op], B), "flips the sign, but no division by a negative number happened"))
    if a + c != 0:
        cands.append((_ray(fop, Q(d - b) / (a + c)), "adds the $x$-terms instead of subtracting"))
    cands += [(_ray(fop, Q(d + b) / k), f"moves {m(tx(b))} across without changing its sign"),
              (_ray(_STRICT[fop], B), f"uses {m(_TEX[_STRICT[fop]])} instead of {m(_TEX[fop])}")]
    ans_tex, ans_pred = _ray(fop, B)
    grid = _grid(B)
    tip = None
    if k < 0:
        tip = (f"To avoid dividing by a negative, collect the {m('x')}-terms on the right instead: "
               f"{m(f'{tx(b - d)} {_TEX[op]} {_lin((-k, "x"))}')}, so {m(f'{tx(B)} {_TEX[op]} x')}, "
               f"which means the same as {m(f'x {_TEX[fop]} {tx(B)}')}.")
    return Problem(
        stem=_ask(rng, ineq),
        answer=ans_tex,
        fmt=text,
        wrong=_keep_wrong(cands, orig, grid, ans_tex),
        steps=steps,
        tip=tip,
        verify=lambda s: s == ans_tex and _agree(ans_pred, orig, grid),
    )


@template("MK")
def compound(rng, lvl):
    lo_op, hi_op = rng.choice([("<", "le"), ("le", "<"), ("<", "<"), ("le", "le")])
    L = Q(rng.randint(-8, 3))
    H = L + rng.randint(3, 9)
    if lvl <= 2:
        a = rng.randint(2, 5)
        b = rng.choice([v for v in range(-9, 10) if v != 0])
        lo, hi = a * L + b, a * H + b
        mid = _lin((a, "x"), (b, ""))
        ineq = f"{tx(lo)} {_TEX[lo_op]} {mid} {_TEX[hi_op]} {tx(hi)}"
        orig = lambda t: _holds(lo_op, lo, a * t + b) and _holds(hi_op, a * t + b, hi)
        ans_tex, ans_pred = _between(L, lo_op, H, hi_op)
        sub = "Subtract" if b > 0 else "Add"
        steps = [f"Do the same thing to all three parts. {sub} {m(abs(b))} "
                 f"{'from' if b > 0 else 'to'} each part: {m(f'{tx(lo - b)} {_TEX[lo_op]} {a}x {_TEX[hi_op]} {tx(hi - b)}')}.",
                 f"Divide each part by {m(a)} (positive, so the signs stay the same): "
                 f"{m(f'{tx(L)} {_TEX[lo_op]} x {_TEX[hi_op]} {tx(H)}')}."]
        cands = [(_between(Q(lo - b), lo_op, H, hi_op), f"forgets to divide the left part by {m(a)}"),
                 (_between(L, hi_op, H, lo_op), "swaps which endpoint is included"),
                 (_between(Q(lo + b) / a, lo_op, Q(hi + b) / a, hi_op),
                  f"{'adds' if b > 0 else 'subtracts'} {m(abs(b))} instead of "
                  f"{'subtracting' if b > 0 else 'adding'} it"),
                 (_between(Q(lo) / a, lo_op, Q(hi) / a, hi_op), f"divides by {m(a)} without first removing the {m(tx(b))}")]
    else:
        a = -rng.randint(2, 4)
        b = rng.choice([v for v in range(-9, 10) if v != 0])
        # b + a x lies between lo and hi  <=>  x between L and H, endpoints swapped
        lo, hi = a * H + b, a * L + b          # a < 0 reverses the order
        mid = f"{tx(b)} - {-a}x"
        # the symbol at each end of x travels with its endpoint
        ineq = f"{tx(lo)} {_TEX[lo_op]} {mid} {_TEX[hi_op]} {tx(hi)}"
        orig = lambda t: _holds(lo_op, lo, a * t + b) and _holds(hi_op, a * t + b, hi)
        # lo  op1  b + a x  op2  hi   ->   (hi - b)/a  op2'  x  op1'  (lo - b)/a  read backwards
        ans_tex, ans_pred = _between(L, hi_op, H, lo_op)
        sub = "Subtract" if b > 0 else "Add"
        steps = [f"Do the same thing to all three parts. {sub} {m(abs(b))} "
                 f"{'from' if b > 0 else 'to'} each part: {m(f'{tx(lo - b)} {_TEX[lo_op]} {a}x {_TEX[hi_op]} {tx(hi - b)}')}.",
                 f"Divide each part by {m(a)}. Dividing by a negative number flips \\emph{{both}} signs: "
                 f"{m(f'{tx(H)} {_TEX[_FLIP[lo_op]]} x {_TEX[_FLIP[hi_op]]} {tx(L)}')}.",
                 f"Rewrite it with the smaller number on the left: {m(f'{tx(L)} {_TEX[hi_op]} x {_TEX[lo_op]} {tx(H)}')}."]
        cands = [(_between(L, lo_op, H, hi_op), "moves the numbers but leaves each symbol in its old place"),
                 (_between(-H, lo_op, -L, hi_op), f"forgets that dividing by {m(a)} changes the signs of the numbers"),
                 (_between(min(Q(lo + b) / a, Q(hi + b) / a), hi_op, max(Q(lo + b) / a, Q(hi + b) / a), lo_op),
                  f"{'adds' if b > 0 else 'subtracts'} {m(abs(b))} instead of {'subtracting' if b > 0 else 'adding'} it"),
                 (_outside(L, "<" if hi_op == "le" else "le", H, ">" if lo_op == "le" else "ge"),
                  "gives the numbers \\emph{outside} the answer")]
    grid = _grid(L, H, lo, hi)
    need(_agree(ans_pred, orig, grid))
    inside = L + 1 if L + 1 < H else (L + H) / 2
    mv = a * inside + b
    steps.append(f"Check with {m(f'x = {tx(inside)}')}: the middle is {m(f'{_subst(inside, *( [(a, "x"), (b, "")] if lvl <= 2 else [(b, ""), (a, "x")]))} = {tx(mv)}')}, "
                 f"and {m(f'{tx(lo)} {_TEX[lo_op]} {tx(mv)} {_TEX[hi_op]} {tx(hi)}')} is true. \\checkmark")
    return Problem(
        stem=_ask(rng, ineq),
        answer=ans_tex,
        fmt=text,
        wrong=_keep_wrong(cands, orig, grid, ans_tex),
        steps=steps,
        verify=lambda s: s == ans_tex and _agree(ans_pred, orig, grid),
    )


@template("MK")
def which_satisfies(rng, lvl):
    if lvl == 1 and rng.random() < 0.5:
        return _extreme_integer(rng)
    if lvl == 1:
        op = rng.choice(["<", ">", "le", "ge"])
        a = rng.randint(2, 6)
        b = rng.choice([v for v in range(-12, 13) if v != 0])
        B = Q(rng.randint(-4, 9))
        c = a * B + b
        expr_terms = [(a, "x"), (b, "")]
        ineq = f"{_lin(*expr_terms)} {_TEX[op]} {tx(c)}"
        ok = lambda t: _holds(op, a * t + b, c)
        up = op in (">", "ge")
        ans = B + rng.randint(1, 3) * (1 if up else -1)
        cands = [B - 1 * (1 if up else -1), B - 2 * (1 if up else -1), B - 3 * (1 if up else -1),
                 B - 4 * (1 if up else -1)]
        if op in ("<", ">"):
            cands.insert(0, B)
        cond = f"{_WORD[op]} {m(tx(c))}"
        steps = [f"Solve first. " + _const_text(b, f"{a}x", op, c),
                 f"Divide both sides by {m(a)} (positive, so the sign stays): {m(f'x {_TEX[op]} {tx(B)}')}.",
                 f"Only {m(tx(ans))} is {_WORD[op]} {m(tx(B))}. Check: {m(f'{_subst(ans, *expr_terms)} = {tx(a * ans + b)}')}, "
                 f"which is {cond}. \\checkmark"]
    else:
        lo_op, hi_op = rng.choice([("<", "le"), ("le", "<"), ("<", "<")])
        a = rng.randint(2, 5)
        b = rng.choice([v for v in range(-9, 10) if v != 0])
        L = Q(rng.randint(-8, 3))
        H = L + rng.randint(3, 7)
        lo, hi = a * L + b, a * H + b
        expr_terms = [(a, "x"), (b, "")]
        ineq = f"{tx(lo)} {_TEX[lo_op]} {_lin(*expr_terms)} {_TEX[hi_op]} {tx(hi)}"
        ok = lambda t: _holds(lo_op, lo, a * t + b) and _holds(hi_op, a * t + b, hi)
        inside = [v for v in range(int(L), int(H) + 1) if ok(Q(v))]
        ans = Q(rng.choice(inside))
        cands = [L - 1, H + 1, L - 2, H + 2, L - 3, H + 3]
        if lo_op == "<":
            cands.insert(0, L)
        if hi_op == "<":
            cands.insert(0, H)
        cond = f"between {m(tx(lo))} and {m(tx(hi))} as required"
        steps = [f"Solve first. {'Subtract' if b > 0 else 'Add'} {m(abs(b))} {'from' if b > 0 else 'to'} all three parts: "
                 f"{m(f'{tx(lo - b)} {_TEX[lo_op]} {a}x {_TEX[hi_op]} {tx(hi - b)}')}, then divide all three by {m(a)}: "
                 f"{m(f'{tx(L)} {_TEX[lo_op]} x {_TEX[hi_op]} {tx(H)}')}.",
                 f"Only {m(tx(ans))} is in this range. Check: {m(f'{_subst(ans, *expr_terms)} = {tx(a * ans + b)}')}, "
                 f"and {m(f'{tx(lo)} {_TEX[lo_op]} {tx(a * ans + b)} {_TEX[hi_op]} {tx(hi)}')}. \\checkmark"]
    wrong = []
    for v in cands:
        v = Q(v)
        if ok(v):
            continue
        val = a * v + b
        if lvl == 1:
            if val == c:
                why = f"makes the left side equal to {m(tx(c))}, but the inequality is strict"
            else:
                why = f"gives {m(f'{_subst(v, *expr_terms)} = {tx(val)}')}, which is not {_WORD[op]} {m(tx(c))}"
        else:
            if val in (lo, hi):
                why = f"makes the middle equal to {m(tx(val))}, but that end is not included"
            else:
                why = f"gives {m(f'{_subst(v, *expr_terms)} = {tx(val)}')}, which is outside the range"
        wrong.append((v, why))
    sols = [v for v in range(-60, 61) if ok(Q(v))]
    return Problem(
        stem=choose(rng, f"Which value of $x$ satisfies {m(ineq)}?",
                    f"Which of the following is a solution of {m(ineq)}?",
                    f"Which number makes {m(ineq)} true?"),
        answer=ans,
        fmt=frac,
        wrong=wrong,
        near=lambda r: [],
        steps=steps,
        verify=ok,
        check=ans if ans in sols else None,
        neg_ok=True,
    )


def _extreme_integer(rng):
    """Smallest (or largest) integer that satisfies a x + b op c."""
    op = rng.choice(["<", ">", "le", "ge"])
    a = rng.randint(2, 6)
    b = rng.choice([v for v in range(-12, 13) if v != 0])
    B = Q(rng.randint(-4, 9))
    c = a * B + b
    terms = [(a, "x"), (b, "")]
    ineq = f"{_lin(*terms)} {_TEX[op]} {tx(c)}"
    ok = lambda t: _holds(op, a * t + b, c)
    up = op in (">", "ge")
    word = "smallest" if up else "largest"
    ans = B if op in ("le", "ge") else (B + 1 if up else B - 1)
    sgn = 1 if up else -1
    wrong = []
    for v in (B - 2 * sgn, B - sgn, B, B + sgn, B + 2 * sgn, B + 3 * sgn):
        v = Q(v)
        if v == ans:
            continue
        val = a * v + b
        if ok(v):
            why = f"is a solution, but not the {word} one"
        elif val == c:
            why = f"makes the left side equal to {m(tx(c))}, but the inequality is strict"
        else:
            why = f"gives {m(f'{_subst(v, *terms)} = {tx(val)}')}, which is not {_WORD[op]} {m(tx(c))}"
        wrong.append((v, why))
    steps = ["Solve first. " + _const_text(b, f"{a}x", op, c),
             f"Divide both sides by {m(a)} (positive, so the sign stays): {m(f'x {_TEX[op]} {tx(B)}')}.",
             (f"{m(tx(B))} itself is allowed ({m(_TEX[op])}), so the {word} integer is {m(tx(ans))}."
              if op in ("le", "ge") else
              f"{m(tx(B))} itself is \\emph{{not}} allowed ({m(_TEX[op])}), so the {word} integer is {m(tx(ans))}.")]
    sols = [v for v in range(-60, 61) if ok(Q(v))]
    return Problem(
        stem=f"What is the {word} integer $x$ that satisfies {m(ineq)}?",
        answer=ans,
        fmt=frac,
        wrong=wrong,
        near=lambda r: [],
        steps=steps,
        verify=ok,
        check=Q(min(sols) if up else max(sols)),
        neg_ok=True,
    )


# phrase -> (symbol, meaning at the boundary K: does K, K-1, K+1 count?)
_PHRASES = {
    "ge": ["at least", "no less than", "a minimum of"],
    "le": ["at most", "no more than", "a maximum of"],
    ">": ["more than", "greater than"],
    "<": ["less than", "fewer than"],
}
_MEANS = {  # independent table: which of K-1, K, K+1 satisfy each phrase
    "at least": (False, True, True), "no less than": (False, True, True),
    "a minimum of": (False, True, True), "at most": (True, True, False),
    "no more than": (True, True, False), "a maximum of": (True, True, False),
    "more than": (False, False, True), "greater than": (False, False, True),
    "less than": (True, False, False), "fewer than": (True, False, False),
}


def _op_why(right, wrong):
    if _FLIP[right] == wrong:
        return "points the sign the wrong way"
    if _STRICT[right] == wrong:
        return ("includes the boundary number, which is not allowed" if right in ("<", ">")
                else "leaves out the boundary number, which is allowed")
    return "points the sign the wrong way and gets the boundary wrong"


@template("MK")
def translate_ineq(rng, lvl):
    op = rng.choice(["ge", "le", ">", "<"])
    phrase = rng.choice(_PHRASES[op])
    if lvl == 1:
        k = rng.randint(2, 9)
        c = rng.randint(2, 30)
        K = rng.randint(c + 1, c + 40)
        form = rng.choice(["plus", "times", "minus"])
        if form == "plus":
            words, lhs = f"A number $n$ increased by {c} is {phrase} {K}.", f"n + {c}"
            f = lambda v: v + c
        elif form == "minus":
            words, lhs = f"A number $n$ decreased by {c} is {phrase} {K}.", f"n - {c}"
            f = lambda v: v - c
        else:
            words, lhs = f"{_TIMESW[k].capitalize()} a number $n$ is {phrase} {K}.", f"{k}n"
            f = lambda v: k * v
        stem = choose(rng, f"Which inequality says: ``{words}''",
                      f"``{words}'' Which inequality represents this statement?")
        bad_expr = None
    else:
        stem, lhs, K, f, bad_expr, op, phrase = _context_ineq(rng)
    Kt = int_raw(K)
    ans_tex = f"${lhs} {_TEX[op]} {Kt}$"
    wrong = [(f"${lhs} {_TEX[w]} {Kt}$", _op_why(op, w)) for w in ("<", ">", "le", "ge") if w != op]
    if bad_expr:
        wrong.insert(1, (f"${bad_expr[0]} {_TEX[op]} {Kt}$", bad_expr[1]))
    # independent check: the symbol's meaning matches the phrase at K-1, K, K+1
    means = _MEANS[phrase]
    good = all(_holds(op, kk, K) == want for kk, want in zip((K - 1, K, K + 1), means))
    sym_word = {"ge": "is greater than or equal to", "le": "is less than or equal to",
                ">": "is greater than", "<": "is less than"}[op]
    incl = ("includes" if op in ("ge", "le") else "does not include")
    steps = [f"``{phrase.capitalize()} {Kt}'' means the quantity {sym_word} {Kt}: it {incl} {Kt} itself, "
             f"so the symbol is {m(_TEX[op])}.",
             f"The quantity is {m(lhs)}, so the inequality is {ans_tex}."]
    return Problem(
        stem=stem,
        answer=ans_tex,
        fmt=text,
        wrong=wrong,
        steps=steps,
        verify=lambda s: good and s == ans_tex,
    )


_TIMESW = {2: "twice", 3: "three times", 4: "four times", 5: "five times", 6: "six times",
           7: "seven times", 8: "eight times", 9: "nine times"}


def _context_ineq(rng):
    """Word situations: (stem, lhs tex, K, f, (bad lhs tex, why) | None, op, phrase)."""
    s = soldier(rng)
    who = person(rng)
    pick = rng.randint(0, 5)
    if pick == 0:
        have, K = rng.randrange(120, 200, 5), rng.choice([240, 250, 260, 270])
        op, phrase = "ge", rng.choice(["at least", "a minimum of"])
        stem = (f"{s} needs a total score of {phrase} {K} points on a fitness test. {s.split()[-1]} has already "
                f"earned {have} points on the first events. Which inequality shows the points $p$ that "
                f"{s.split()[-1]} still needs from the last event?")
        return stem, f"{have} + p", K, None, (f"{have}p", "multiplies instead of adding the points"), op, phrase
    if pick == 1:
        have, K = rng.randrange(300, 900, 25), rng.choice([2000, 2500, 3000])
        op, phrase = "le", rng.choice(["at most", "no more than", "a maximum of"])
        stem = (f"A trailer can carry {phrase} {int_raw(K)} pounds. It is already loaded with {have} pounds of gear. "
                f"Which inequality shows the additional weight $w$, in pounds, that can be loaded?")
        return stem, f"{have} + w", K, None, (f"{have}w", "multiplies instead of adding the weights"), op, phrase
    if pick == 2:
        price, K = rng.choice([3, 4, 5, 6, 8]), rng.choice([40, 50, 60, 75, 80])
        op, phrase = "le", rng.choice(["no more than", "at most"])
        stem = (f"{who.name} can spend {phrase} \\${K} on snacks for a road trip. Each snack pack costs \\${price}. "
                f"Which inequality shows the number of packs $n$ that {who.he} can buy?")
        return stem, f"{price}n", K, None, (f"n + {price}", f"adds {price} instead of multiplying"), op, phrase
    if pick == 3:
        per, K = rng.choice([15, 20, 25, 30]), rng.choice([300, 400, 500, 600])
        op, phrase = ">", "more than"
        stem = (f"A unit is selling raffle tickets for \\${per} each and wants to raise {phrase} \\${K}. "
                f"Which inequality shows the number of tickets $t$ the unit must sell?")
        return stem, f"{per}t", K, None, (f"t + {per}", f"adds {per} instead of multiplying"), op, phrase
    if pick == 4:
        used, K = rng.randint(3, 12), rng.choice([20, 24, 30])
        op, phrase = "<", "fewer than"
        stem = (f"A squad must finish a land-navigation course with {phrase} {K} total penalty points. It has "
                f"{used} penalty points so far. Which inequality shows the penalty points $p$ it can still get?")
        return stem, f"{used} + p", K, None, (f"{used}p", "multiplies instead of adding"), op, phrase
    rate, have, K = rng.choice([12, 14, 15, 16, 18]), rng.randrange(50, 200, 10), rng.choice([500, 600, 750, 800])
    op, phrase = "ge", rng.choice(["at least", "no less than"])
    stem = (f"{who.name} has \\${have} saved and earns \\${rate} per hour. {who.He} wants to have {phrase} \\${K}. "
            f"Which inequality shows the number of hours $h$ {who.he} must work?")
    return stem, f"{have} + {rate}h", K, None, (f"{rate}({have} + h)", f"multiplies the savings by {rate} too"), op, phrase


@template("MK")
def integer_count(rng, lvl):
    lo_op, hi_op = rng.choice([("<", "le"), ("le", "<"), ("<", "<"), ("le", "le")])
    if lvl == 1:
        L = rng.randint(-8, 2)
        H = L + rng.randint(3, 9)
        ineq = f"{L} {_TEX[lo_op]} x {_TEX[hi_op]} {H}"
        ok = lambda t: _holds(lo_op, L, t) and _holds(hi_op, t, H)
        steps = []
        Lx, Hx = L, H
    else:
        a = rng.randint(2, 4)
        b = rng.choice([v for v in range(-7, 8) if v != 0])
        Lx = rng.randint(-6, 1)
        Hx = Lx + rng.randint(3, 7)
        lo, hi = a * Lx + b, a * Hx + b
        ineq = f"{lo} {_TEX[lo_op]} {_lin((a, 'x'), (b, ''))} {_TEX[hi_op]} {hi}"
        ok = lambda t: _holds(lo_op, lo, a * t + b) and _holds(hi_op, a * t + b, hi)
        sub = "Subtract" if b > 0 else "Add"
        steps = [f"Solve first. {sub} {m(abs(b))} {'from' if b > 0 else 'to'} all three parts: "
                 f"{m(f'{lo - b} {_TEX[lo_op]} {a}x {_TEX[hi_op]} {hi - b}')}. Divide all three parts by {m(a)}: "
                 f"{m(f'{Lx} {_TEX[lo_op]} x {_TEX[hi_op]} {Hx}')}."]
    first = Lx if lo_op == "le" else Lx + 1
    last = Hx if hi_op == "le" else Hx - 1
    ans = last - first + 1
    listing = ", ".join(str(v) for v in range(first, last + 1))
    steps += [f"{m(tx(Lx))} {'is' if lo_op == 'le' else 'is not'} included ({m(_TEX[lo_op])}), and "
              f"{m(tx(Hx))} {'is' if hi_op == 'le' else 'is not'} included ({m(_TEX[hi_op])}). "
              f"So the integers run from {m(first)} to {m(last)}.",
              f"List them: {m(listing)}. That is {m(ans)} integers."]
    wrong = []
    span = Hx - Lx
    for v, why in ((span + 1, "counts both endpoints, but one or both are not included"),
                   (span - 1, "leaves out both endpoints"),
                   (span, f"just subtracts the endpoints, {m(f'{Hx} - ({Lx}) = {span}' if Lx < 0 else f'{Hx} - {Lx} = {span}')}, "
                          "without checking which ends are included"),
                   (ans + 1, None), (ans - 1, None)):
        if v != ans and v > 0:
            wrong.append((Q(v), why))
    if first < 0 < last:
        wrong.insert(0, (Q(ans - 1), "forgets to count $0$, which is an integer"))
    if lvl > 1:
        span0 = (hi - lo)
        wrong.append((Q(span0), "counts the integers before dividing by the coefficient of $x$"))
    count = sum(1 for t in range(-100, 101) if ok(Q(t)))
    near = lambda r: [Q(v) for v in (ans - 2, ans + 2, ans - 3, ans + 3) if v > 0]
    return Problem(
        near=near,
        stem=choose(rng, f"How many integers $x$ satisfy {m(ineq)}?",
                    f"How many integer values of $x$ make {m(ineq)} true?"),
        answer=Q(ans),
        fmt=num,
        wrong=wrong,
        steps=steps,
        check=Q(count),
        tip=f"Count from {m(first)} to {m(last)} with last $-$ first $+ 1$: {m(f'{last} - ({first}) + 1 = {ans}')}."
        if first < 0 else f"Count from {m(first)} to {m(last)} with last $-$ first $+ 1$: {m(f'{last} - {first} + 1 = {ans}')}.",
    )


@template("AR")
def ineq_word(rng, lvl):
    if lvl <= 2:
        return _min_or_max(rng)
    return rng.choice([_compare_plans, _average_needed, _min_or_max])(rng)


def _near_int(ans):
    return lambda r: [Q(ans + d) for d in (1, -1, 2, -2, 3, -3) if ans + d > 0]


def _mo(v):
    v = Q(v)
    return r"\$" + (int_raw(v) if v.is_integer else dec_raw(v, places=2))


def _min_or_max(rng):
    who = person(rng)
    ctx = rng.randint(0, 5)
    if ctx <= 2:  # reach at least a goal: round up
        if ctx == 0:
            have, rate, goal = rng.randrange(40, 300, 5), rng.choice([11, 12, 13, 14, 15, 16, 17, 18]), rng.randrange(400, 1200, 50)
            unit_s, unit_p = "hour", "hours"
            stem = (f"{who.name} has {_mo(have)} saved and earns {_mo(rate)} per hour at a part-time job. "
                    f"What is the least number of whole hours {who.he} must work to have at least {_mo(goal)}?")
        elif ctx == 1:
            have, rate, goal = rng.randrange(100, 600, 25), rng.choice([25, 30, 35, 40, 45, 60, 75]), rng.randrange(1000, 3000, 100)
            unit_s, unit_p = "week", "weeks"
            stem = (f"Before leaving for basic training, {who.name} has {_mo(have)} in the bank and deposits "
                    f"{_mo(rate)} every week. What is the fewest number of weeks until {who.he} has at least {_mo(goal)}?")
        else:
            have, rate, goal = rng.randrange(50, 400, 10), rng.choice([6, 8, 12, 15]), rng.randrange(500, 1500, 50)
            unit_s, unit_p = "T-shirt", "T-shirts"
            stem = (f"A unit's family readiness group has raised {_mo(have)}. It sells T-shirts for {_mo(rate)} each. "
                    f"What is the least number of T-shirts it must sell to reach at least {_mo(goal)}?")
        need(goal > have and (goal - have) % rate != 0)
        exact = Q(goal - have) / rate
        ans = math.ceil(exact)
        need(2 <= ans <= 150)
        var = unit_s[0].lower()
        steps = [f"Let {m(var)} be the number of {unit_p}. The total must be at least the goal: "
                 f"{m(f'{have} + {rate}{var} \\ge {goal}')}.",
                 f"Subtract {m(have)}: {m(f'{rate}{var} \\ge {goal - have}')}. Divide by {m(rate)}: "
                 f"{m(f'{var} \\ge {F(goal - have, rate)} = {mixed_raw(exact)}')}.",
                 f"{m(var)} must be a whole number at least that big, so round \\emph{{up}}: {m(ans)}. "
                 f"Check: {m(f'{have} + {rate}({ans - 1}) = {have + rate * (ans - 1)}')} is too little, but "
                 f"{m(f'{have} + {rate}({ans}) = {have + rate * ans}')} is enough."]
        wrong = [(Q(ans - 1), "rounds down, which falls just short of the goal"),
                 (Q(math.ceil(Q(goal) / rate)), f"ignores the {_mo(have)} already saved"),
                 (Q(math.ceil(Q(goal + have) / rate)), f"adds the {_mo(have)} instead of subtracting it"),
                 (Q(ans + 1), None)]
        alt = math.ceil(Q(goal) / (have + rate))
        if 3 * alt >= ans:
            wrong.insert(1, (Q(alt), f"divides {_mo(goal)} by {_mo(have)} $+$ {_mo(rate)} instead of subtracting first"))
        ok = lambda h: have + rate * h >= goal
        least = next(h for h in range(0, 1000) if ok(h))
        return Problem(stem=stem, answer=Q(ans), fmt=unit(num, unit_s), wrong=wrong, steps=steps,
                       check=Q(least), section="AR", near=_near_int(ans))
    # stay within a limit: round down
    if ctx == 3:
        base, per, cap = rng.randrange(150, 400, 10), rng.choice([35, 40, 45, 55, 60, 65, 70]), rng.choice([1500, 2000, 2500, 3000])
        unit_s, unit_p = "crate", "crates"
        stem = (f"A trailer can carry at most {num(cap)} pounds. It already holds {base} pounds of tools. "
                f"What is the greatest number of {per}-pound ammunition crates that can be added?")
        lead = f"{base} + {per}c \\le {int_raw(cap)}"
        var, lbl = "c", f"{base} pounds"
    elif ctx == 4:
        base, per, cap = rng.choice([25, 30, 35, 40, 45]), rng.choice([3, 4, 6, 7]), rng.choice([60, 70, 75, 80, 90, 100])
        unit_s, unit_p = "gigabyte", "gigabytes"
        stem = (f"{who.name}'s phone plan costs {_mo(base)} per month plus {_mo(per)} for each gigabyte of data. "
                f"{who.He} wants the monthly bill to be no more than {_mo(cap)}. What is the greatest whole number "
                f"of gigabytes {who.he} can use?")
        lead = f"{base} + {per}g \\le {cap}"
        var, lbl = "g", _mo(base)
    else:
        base, per, cap = rng.choice([180, 200, 220, 250]), rng.choice([150, 160, 170, 175, 180, 190]), rng.choice([1200, 1500, 1600, 2000])
        unit_s, unit_p = "passenger", "passengers"
        stem = (f"An elevator has a weight limit of {num(cap)} pounds. A {base}-pound cart of equipment is already "
                f"inside. If each passenger is counted as {per} pounds, what is the greatest number of passengers "
                f"who can ride with the cart?")
        lead = f"{base} + {per}p \\le {int_raw(cap)}"
        var, lbl = "p", f"{base} pounds"
    need((cap - base) % per != 0)
    exact = Q(cap - base) / per
    ans = math.floor(exact)
    need(2 <= ans <= 100)
    steps = [f"Let {m(var)} be the number of {unit_p}. The total must stay at or under the limit: {m(lead)}.",
             f"Subtract {m(base)}: {m(f'{per}{var} \\le {int_raw(cap - base)}')}. Divide by {m(per)}: "
             f"{m(f'{var} \\le {F(int_raw(cap - base), per)} = {mixed_raw(exact)}')}.",
             f"{m(var)} must be a whole number no bigger than that, so round \\emph{{down}}: {m(ans)}. "
             f"Check: {m(ans + 1)} would make {m(int_raw(base + per * (ans + 1)))}, over the limit."]
    wrong = [(Q(ans + 1), "rounds up, which goes over the limit"),
             (Q(math.floor(Q(cap) / per)), f"forgets the {lbl} already counted"),
             (Q(math.floor(Q(cap + base) / per)), "adds the starting amount instead of subtracting it"),
             (Q(ans - 1), None)]
    alt = math.floor(Q(cap) / (base + per))
    if 3 * alt >= ans:
        wrong.insert(1, (Q(alt), f"divides {m(int_raw(cap))} by {m(f'{int_raw(base)} + {per}')} instead of subtracting first"))
    ok = lambda h: base + per * h <= cap
    most = max(h for h in range(0, 1000) if ok(h))
    return Problem(stem=stem, answer=Q(ans), fmt=unit(num, unit_s), wrong=wrong, steps=steps,
                   check=Q(most), section="AR", near=_near_int(ans))


def _compare_plans(rng):
    who = person(rng)
    ctx = rng.randint(0, 2)
    if ctx == 0:
        fee, per, flat = rng.choice([0, 10, 15, 20]), rng.choice([5, 6, 7, 8, 9, 10, 12]), rng.choice([45, 50, 55, 60, 65, 70])
        stem = (f"A gym offers two options: pay {_mo(per)} per visit"
                + (f" plus a {_mo(fee)} monthly fee" if fee else "")
                + f", or pay {_mo(flat)} per month for unlimited visits. What is the greatest number of visits in "
                f"a month for which paying per visit costs \\emph{{less}} than the unlimited plan?")
        u, optA = "visit", "paying per visit"
    elif ctx == 1:
        fee, per, flat = rng.choice([20, 25, 30, 35]), R(rng.choice([10, 20, 25]), 100), rng.choice([45, 50, 55, 60])
        stem = (f"Car rental A costs {_mo(fee)} per day plus {_mo(per)} per mile. Car rental B costs {_mo(flat)} per "
                f"day with unlimited miles. For a one-day rental, what is the greatest whole number of miles for "
                f"which rental A costs less than rental B?")
        u, optA = "mile", "rental A"
    else:
        fee, per, flat = rng.choice([10, 15, 20]), R(rng.choice([5, 10, 20, 25]), 100), rng.choice([30, 35, 40, 45, 48])
        stem = (f"Phone plan A costs {_mo(fee)} per month plus {_mo(per)} per text message. Plan B costs {_mo(flat)} "
                f"per month with unlimited texts. What is the greatest number of texts in a month for which plan A "
                f"costs less than plan B?")
        u, optA = "text", "plan A"
    fee, per, flat = Q(fee), Q(per), Q(flat)
    need(flat > fee)
    exact = (flat - fee) / per
    ans = math.ceil(exact) - 1                  # strict inequality
    need(1 <= ans <= 400)
    var = u[0]
    lead = (f"{_mr(fee)} + {_mr(per)}{var} < {_mr(flat)}" if fee else f"{_mr(per)}{var} < {_mr(flat)}")
    steps = [f"Let {m(var)} be the number of {u}s. {optA[0].upper() + optA[1:]} costs less when {m(lead)}."]
    if fee:
        steps.append(f"Subtract {m(_mr(fee))}: {m(f'{_mr(per)}{var} < {_mr(flat - fee)}')}.")
    steps.append(f"Divide by {m(_mr(per))}: {m(f'{var} < {_mr(flat - fee)} \\div {_mr(per)} = {mixed_raw(exact)}')}"
                 + (f" (dividing by {m(_mr(per))} is the same as multiplying by {m(int_raw(1 / per))})."
                    if (1 / per).is_integer and not per.is_integer else "."))
    if Q(exact).is_integer:
        steps.append(f"At exactly {m(int_raw(exact))} {u}s the two plans cost the same, so the greatest whole number "
                     f"that is \\emph{{less}} is {m(ans)}.")
    else:
        steps.append(f"The greatest whole number below that is {m(ans)}.")
    wrong = [(Q(ans + 1), "is where the plans cost the same or more, not less") if Q(exact).is_integer
             else (Q(ans + 1), f"rounds up, which makes {optA} cost more"),
             (Q(math.floor(flat / per)), f"ignores the {_mo(fee)} fee") if fee
             else (Q(ans + 2), None),
             (Q(math.floor((flat + fee) / per)), "adds the fee instead of subtracting it") if fee else (Q(ans - 1), None),
             (Q(math.floor(flat / (fee + per))), f"adds the {_mo(fee)} fee to the price of each {u}")
             if fee and 3 * math.floor(flat / (fee + per)) >= ans else (Q(ans - 2), None),
             (Q(ans - 1), None)]
    ok = lambda k: fee + per * k < flat
    most = max(k for k in range(0, 1000) if ok(k))
    return Problem(stem=stem, answer=Q(ans), fmt=unit(num, u), wrong=wrong, steps=steps,
                   check=Q(most), section="AR", near=_near_int(ans))


def _mr(v):
    v = Q(v)
    return int_raw(v) if v.is_integer else dec_raw(v, places=2)


_W = {3: "three", 4: "four", 5: "five"}


def _average_needed(rng):
    who = person(rng)
    k = rng.choice([3, 4])
    target = rng.choice([75, 80, 85, 88, 90])
    scores = [rng.randint(68, 98) for _ in range(k)]
    total_needed = target * (k + 1)
    ans = total_needed - sum(scores)
    need(60 <= ans <= 100 and ans != target)
    lst = ", ".join(str(s_) for s_ in scores[:-1]) + f", and {scores[-1]}"
    ctx = rng.choice(["test", "range"])
    if ctx == "test":
        stem = (f"{who.name} scored {lst} on {_W[k]} tests. What is the lowest score {who.he} can get on the next test "
                f"to have an average of at least {target} on all {_W[k + 1]} tests?")
    else:
        stem = (f"{soldier(rng)} fired qualification scores of {lst} in {_W[k]} rounds at the range. What is the lowest "
                f"score needed in the next round for an average of at least {target} over all {_W[k + 1]} rounds?")
    S = sum(scores)
    steps = [f"An average of at least {m(target)} over {m(k + 1)} scores means a total of at least "
             f"{m(f'{target} \\times {k + 1} = {total_needed}')}.",
             f"The first {m(k)} scores add up to {m(' + '.join(str(s_) for s_ in scores) + f' = {S}')}.",
             f"The next score {m('s')} must satisfy {m(f'{S} + s \\ge {total_needed}')}, so "
             f"{m(f's \\ge {total_needed} - {S} = {ans}')}."]
    wrong = [(Q(target), "assumes the next score only needs to equal the target average"),
             (Q(total_needed - S - target) if total_needed - S - target > 0 else Q(ans + 3), None),
             (Q(ans - 2), None),
             (Q(target * k - S + target + 5), None)]
    least = next(v for v in range(0, 1000) if Q(S + v) / (k + 1) >= target)
    return Problem(stem=stem, answer=Q(ans), fmt=num, wrong=wrong, steps=steps,
                   check=Q(least), section="AR", near=_near_int(ans))


@template("MK")
def abs_ineq(rng, lvl):
    c = rng.choice([v for v in range(-6, 8) if v != 0])
    r = rng.randint(2, 8)
    a = 1 if rng.random() < 0.7 else 2
    if a == 2:
        need((c + r) % 2 == 0 and (c - r) % 2 == 0 and c % 2 == 0)
    kind = rng.choice(["<", "le", ">", "ge"])
    inside = _lin((a, "x"), (-c, ""))
    ineq = f"|{inside}| {_TEX[kind]} {r}"
    lo, hi = Q(c - r) / a, Q(c + r) / a
    orig = lambda t: _holds(kind, abs(a * t - c), r)
    if kind in ("<", "le"):
        op = kind
        ans_tex, ans_pred = _between(lo, op, hi, op)
        cands = [(_ray(op, hi), f"keeps only the positive case; the inside must also be greater than {m(f'-{r}')}"),
                 (_between(Q(-c - r) / a, op, Q(-c + r) / a, op), f"uses the wrong sign: {m(inside)} is zero when {m(f'x = {tx(Q(c) / a)}')}, not {m(f'x = {tx(Q(-c) / a)}')}"),
                 (_outside(lo, "<" if op == "le" else "le", hi, ">" if op == "le" else "ge"),
                  f"gives the ``outside'' set, which is for {m('>')}"),
                 (_between(lo, _STRICT[op], hi, _STRICT[op]), "gets the endpoints wrong")]
        steps = [f"{m(ineq)} means {m(inside)} is within {m(r)} of zero, so it is \\emph{{between}} "
                 f"{m(-r)} and {m(r)}: {m(f'{-r} {_TEX[op]} {inside} {_TEX[op]} {r}')}.",
                 f"{'Add' if c > 0 else 'Subtract'} {m(abs(c))} {'to' if c > 0 else 'from'} all three parts: "
                 f"{m(f'{-r + c} {_TEX[op]} {_lin((a, "x"))} {_TEX[op]} {r + c}')}."
                 + (f" Divide by 2: {m(f'{tx(lo)} {_TEX[op]} x {_TEX[op]} {tx(hi)}')}." if a == 2 else "")]
    else:
        op = kind
        low_op = "<" if op == ">" else "le"
        ans_tex, ans_pred = _outside(lo, low_op, hi, op)
        cands = [(_ray(op, hi), "keeps only the positive case; the inside can also be very negative"),
                 (_between(lo, "<" if op == "ge" else "le", hi, "<" if op == "ge" else "le"),
                  f"gives the ``between'' set, which is for {m('<')}"),
                 (_outside(Q(-c - r) / a, low_op, Q(-c + r) / a, op), f"uses the wrong sign: {m(inside)} is zero when {m(f'x = {tx(Q(c) / a)}')}, not {m(f'x = {tx(Q(-c) / a)}')}"),
                 (_outside(lo, _STRICT[low_op], hi, _STRICT[op]), "gets the endpoints wrong")]
        steps = [f"{m(ineq)} means {m(inside)} is \\emph{{more than}} {m(r)} away from zero"
                 + (" (or exactly that far)" if op == "ge" else "")
                 + f", so there are two pieces: {m(f'{inside} {_TEX[low_op]} {-r}')} or {m(f'{inside} {_TEX[op]} {r}')}.",
                 f"Solve each piece: {m(f'{_lin((a, "x"))} {_TEX[low_op]} {-r + c}')} or "
                 f"{m(f'{_lin((a, "x"))} {_TEX[op]} {r + c}')}."
                 + (f" Divide by 2: {m(f'x {_TEX[low_op]} {tx(lo)}')} or {m(f'x {_TEX[op]} {tx(hi)}')}." if a == 2 else "")]
    grid = _grid(lo, hi, -lo, -hi)
    need(_agree(ans_pred, orig, grid))
    test = (lo + hi) / 2 if kind in ("<", "le") else hi + 1
    steps.append(f"Check with {m(f'x = {tx(test)}')}: {m(f'|{_subst(test, (a, "x"), (-c, ""))}| = {tx(abs(a * test - c))}')}, "
                 f"and {m(f'{tx(abs(a * test - c))} {_TEX[kind]} {r}')} is true. \\checkmark")
    return Problem(
        stem=choose(rng, f"Which of the following is the solution of {m(ineq)}?",
                    f"Solve {m(ineq)}.",
                    f"Which describes all values of $x$ that satisfy {m(ineq)}?"),
        answer=ans_tex,
        fmt=text,
        wrong=_keep_wrong(cands, orig, grid, ans_tex),
        steps=steps,
        verify=lambda s: s == ans_tex and _agree(ans_pred, orig, grid),
    )


PLAN = [
    # (template, level, count)  -- easy -> hard; 25 problems
    (solve_ineq, 1, 3),
    (translate_ineq, 1, 2),
    (which_satisfies, 1, 2),
    (integer_count, 1, 1),
    (solve_ineq, 2, 2),
    (both_sides_ineq, 2, 2),
    (compound, 2, 2),
    (ineq_word, 2, 2),
    (which_satisfies, 2, 1),
    (translate_ineq, 2, 1),
    (compound, 3, 1),
    (both_sides_ineq, 3, 1),
    (abs_ineq, 3, 2),
    (ineq_word, 3, 2),
    (integer_count, 3, 1),
]
