"""Chapter 13 - Systems of Equations."""
import sympy as sp

from ..core import (R, Q, Problem, need, num, frac, m, F, tx, dec_raw, int_raw,
                    frac_raw, money, text, unit, person, soldier, choose,
                    template, x, y)

NUM = 13
TITLE = "Systems of Equations"
PART = 2

INTRO = r"""
A \emph{system of equations} is two equations that share the same
variables. Its solution is the pair $(x, y)$ that makes \emph{both}
equations true at the same time. On the ASVAB you solve systems by
elimination or by substitution, and you set them up yourself in word
problems with two unknowns.

\begin{concept}{Elimination: add or subtract the equations}
Line the equations up and add (or subtract) them so one variable cancels.
\[ \begin{array}{r@{\;}c@{\;}l} x + y &=& 10 \\ x - y &=& 4 \\ \hline 2x &=& 14 \end{array}
\qquad\Rightarrow\qquad x = 7,\ \ y = 10 - 7 = 3 \]
If nothing cancels right away, first multiply one equation (\emph{every}
term, including the number on the right) so that a pair of coefficients
match or are opposites.
\end{concept}

\begin{concept}{Substitution}
When one equation is already solved for a variable, such as $y = 2x - 1$,
replace that variable in the other equation, \emph{in parentheses}:
$3x + 2y = 19$ becomes $3x + 2(2x - 1) = 19$, so $7x - 2 = 19$ and $x = 3$.
Then $y = 2(3) - 1 = 5$.
\end{concept}

\begin{concept}{Setting up word problems}
Two unknowns need two equations: usually one counts the \emph{items} and
one adds up their \emph{value}. For $200$ tickets, adults \$12 and children
\$5, total \$1{,}560:
\[ a + c = 200 \qquad 12a + 5c = 1{,}560 \]
\end{concept}

\begin{example}{Worked example}
Solve the ticket system above for the number of adult tickets.

\textbf{Solution.} From the first equation, $c = 200 - a$. Substitute:
$12a + 5(200 - a) = 1{,}560$, so $12a + 1{,}000 - 5a = 1{,}560$, which gives
$7a = 560$ and $a = 80$. (Then $c = 120$. Check: $960 + 600 = 1{,}560$.)
\end{example}

\begin{tip}
Read what is asked. If the question wants $x + y$, try adding or
subtracting the equations first: you may get $x + y$ directly. You can
also backsolve: a choice is correct only if it works in \emph{both}
equations.
\end{tip}

\begin{trap}
\begin{itemize}
\item Answering with the wrong variable ($y$ when the question asks for $x$).
\item Subtracting equations but changing the sign of only the first term.
\item Multiplying one side of an equation but not the other side.
\item Dropping the parentheses in substitution: $3x - (2x - 1)$ is
  $3x - 2x + 1$.
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


def _subst(vals, *terms):
    """Substitute values into (coef, var) terms: '2(3) - 4(-1)'."""
    out = ""
    for c, v in terms:
        c = Q(c)
        if c == 0:
            continue
        X = vals[v] if v else None
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


def _eq(a, b, c):
    return f"{_lin((a, 'x'), (b, 'y'))} = {tx(c)}"


def _system_tex(e1, e2):
    return (f"\\[ \\begin{{aligned}} {_eq(*e1).replace(' = ', ' &= ')} \\\\ "
            f"{_eq(*e2).replace(' = ', ' &= ')} \\end{{aligned}} \\]")


def _brute(e1, e2, lim=60):
    """All integer solutions in a box: the independent check."""
    out = []
    for X in range(-lim, lim + 1):
        for Y in range(-lim, lim + 1):
            if e1[0] * X + e1[1] * Y == e1[2] and e2[0] * X + e2[1] * Y == e2[2]:
                out.append((X, Y))
    return out


def _partial(eq, keep, kv):
    """Left side of eq with the variable `keep` replaced by its value kv."""
    out = ""
    for c, v in ((eq[0], "x"), (eq[1], "y")):
        if c == 0:
            continue
        if v == keep:
            body = f"{tx(abs(c))}({tx(kv)})" if abs(c) != 1 else (tx(kv) if (kv >= 0 or not out) and c > 0 else f"({tx(kv)})")
        else:
            body = v if abs(c) == 1 else f"{tx(abs(c))}{v}"
        if not out:
            out = ("-" if c < 0 else "") + body
        else:
            out += (" - " if c < 0 else " + ") + body
    return out


def _elim_steps(e1, e2, X, Y):
    """Elimination steps; returns (steps, first var found, its coef, rhs, k, op)."""
    a1, b1, c1 = e1
    a2, b2, c2 = e2
    plans = []
    for var, p1, p2 in (("y", b1, b2), ("x", a1, a2)):
        for k in (1, 2, 3, 4, 5):
            if p1 == -k * p2:
                plans.append((k, var, "add"))
            elif p1 == k * p2:
                plans.append((k, var, "sub"))
    need(plans)
    k, var, op = min(plans, key=lambda t: (t[0], t[2] != "add", t[1] != "y"))
    steps = []
    A2, B2, C2 = k * a2, k * b2, k * c2
    if k > 1:
        steps.append(f"Multiply \\emph{{every}} term of the second equation by {m(k)} so the "
                     f"{m(var)}-terms will cancel: {m(_eq(A2, B2, C2))}.")
    if op == "add":
        na, nb, nc = a1 + A2, b1 + B2, c1 + C2
        steps.append(f"Add the equations. The {m(var)}-terms cancel: {m(_eq(na, nb, nc))}.")
    else:
        na, nb, nc = a1 - A2, b1 - B2, c1 - C2
        steps.append(f"Subtract the {'new ' if k > 1 else ''}second equation from the first "
                     f"(subtract \\emph{{every}} term). The {m(var)}-terms cancel: {m(_eq(na, nb, nc))}.")
    keep = "x" if var == "y" else "y"
    coef = na if keep == "x" else nb
    kv = X if keep == "x" else Y
    if coef != 1:
        steps.append(f"Divide both sides by {m(tx(coef))}: {m(f'{keep} = {F(tx(nc), tx(coef))} = {tx(kv)}')}.")
    other = "y" if keep == "x" else "x"
    oval = Y if other == "y" else X
    idx = 1 if other == "y" else 0
    use = e1 if abs(e1[idx]) <= abs(e2[idx]) else e2
    oc = use[idx]
    kc = use[1 - idx]
    rest = use[2] - kc * kv
    txt = (f"Substitute {m(f'{keep} = {tx(kv)}')} into {m(_eq(*use))}: "
           f"{m(f'{_partial(use, keep, kv)} = {tx(use[2])}')}, so {m(f'{_lin((oc, other))} = {tx(rest)}')}")
    if oc != 1:
        txt += f" and {m(f'{other} = {tx(oval)}')}"
    steps.append(txt + ".")
    return steps, keep, coef, nc, k, op


def _par(v):
    return f"({tx(v)})" if Q(v) < 0 else tx(v)


# --------------------------------------------------------------------------
# templates
# --------------------------------------------------------------------------

def _pick_system(rng, lvl):
    if lvl == 1:
        X = rng.randint(1, 15)
        Y = rng.randint(-5, 12)
        need(X != Y and X + Y != 0)
        e1 = (1, 1, X + Y)
        e2 = (1, -1, X - Y) if rng.random() < 0.6 else (rng.choice([2, 3]), -1, 0)
        if e2[2] == 0:
            e2 = (e2[0], -1, e2[0] * X - Y)
    elif lvl == 2:
        X = rng.randint(-6, 12)
        Y = rng.randint(-6, 12)
        need(X != Y and X != 0 and Y != 0)
        b = rng.choice([1, 1, 2, 3])
        a1, a2 = rng.sample([1, 2, 3, 4, 5], 2)
        b2 = rng.choice([b, -b])
        e1 = (a1, b, a1 * X + b * Y)
        e2 = (a2, b2, a2 * X + b2 * Y)
        if rng.random() < 0.5:
            e1, e2 = e2, e1
    else:
        X = rng.randint(-6, 10)
        Y = rng.randint(-6, 10)
        need(X != Y and X != 0 and Y != 0)
        b2 = rng.choice([1, -1, 2, -2])
        k = rng.choice([2, 3])
        b1 = rng.choice([1, -1]) * k * abs(b2)
        a1 = rng.randint(1, 5)
        a2 = rng.randint(1, 5)
        need(a1 * b2 - a2 * b1 != 0 and a1 != a2 and a1 % a2 != 0 and a2 % a1 != 0)
        e1 = (a1, b1, a1 * X + b1 * Y)
        e2 = (a2, b2, a2 * X + b2 * Y)
    need(e1[0] * e2[1] - e1[1] * e2[0] != 0)
    return e1, e2, Q(X), Q(Y)


@template("MK")
def elimination(rng, lvl):
    e1, e2, X, Y = _pick_system(rng, lvl)
    asks = ["x", "y"] + (["x + y"] if lvl >= 2 else []) + (["x - y"] if lvl == 3 else [])
    ask = rng.choice(asks)
    val = {"x": X, "y": Y, "x + y": X + Y, "x - y": X - Y}[ask]
    steps, first, coef, rhs, k, op = _elim_steps(e1, e2, X, Y)
    if ask in ("x + y", "x - y"):
        steps.append(f"The question asks for {m(ask)}: {m(f'{tx(X)} {ask[2]} {_par(Y)} = {tx(val)}')}.")
    wrong = []
    names = {"x": X, "y": Y, "x + y": X + Y, "x - y": X - Y}
    for nm, v in names.items():
        if nm != ask:
            wrong.append((v, f"gives the value of {m(nm)}, not {m(ask)}"))
    if coef not in (1, -1) and ask == first:
        wrong.insert(1, (rhs, f"forgets to divide by {m(tx(coef))}"))
    if k > 1 and ask == first:
        a1, b1, c1 = e1
        a2, b2, c2 = e2
        bad_rhs = c1 + c2 if op == "add" else c1 - c2
        wrong.insert(1, (Q(bad_rhs) / coef, f"multiplies the left side of the second equation by {m(k)} but not the right side"))
    wrong.append((-val, "makes a sign error"))
    sol = sp.solve([sp.Eq(e1[0] * x + e1[1] * y, e1[2]), sp.Eq(e2[0] * x + e2[1] * y, e2[2])], [x, y])
    bx = _brute(e1, e2)
    need(len(bx) == 1)
    BX, BY = bx[0]
    chk = {"x": BX, "y": BY, "x + y": BX + BY, "x - y": BX - BY}[ask]
    stem = choose(rng,
                  f"If {m(_eq(*e1))} and {m(_eq(*e2))}, what is the value of {m(ask)}?",
                  f"What is the value of {m(ask)} in the solution of this system?" + _system_tex(e1, e2),
                  f"Solve the system below. What is the value of {m(ask)}?" + _system_tex(e1, e2))
    return Problem(
        stem=stem,
        answer=val,
        fmt=frac,
        wrong=wrong,
        steps=steps,
        check=Q(chk),
        verify=lambda v: sol[x] == X and sol[y] == Y and v == {"x": sol[x], "y": sol[y], "x + y": sol[x] + sol[y],
                                                                "x - y": sol[x] - sol[y]}[ask],
        near=lambda r: [val + d for d in (1, -1, 2, -2, 3, -3)],
        neg_ok=True,
    )


@template("MK")
def substitution(rng, lvl):
    X = Q(rng.randint(-5, 9))
    mm = rng.choice([v for v in range(-4, 5) if v != 0])
    kk = rng.choice([v for v in range(-9, 10) if v != 0])
    Y = mm * X + kk
    a = rng.randint(1, 6)
    b = rng.choice([1, 2, 3, -1, -2])
    c = a * X + b * Y
    need(X != 0 and Y != 0 and X != Y and a + b * mm != 0)
    ask = rng.choice(["x", "y"])
    first = f"y = {_lin((mm, 'x'), (kk, ''))}"
    second = _eq(a, b, c)
    inner = _lin((mm, "x"), (kk, ""))
    if b == 1:
        sub = f"{_lin((a, 'x'))} + ({inner})"
    elif b == -1:
        sub = f"{_lin((a, 'x'))} - ({inner})"
    else:
        sub = f"{_lin((a, 'x'))} {'+' if b > 0 else '-'} {abs(b)}({inner})"
    expanded = _lin((a, "x"), (b * mm, "x"), (b * kk, ""))
    combined = _lin((a + b * mm, "x"), (b * kk, ""))
    steps = [f"The first equation tells you what {m('y')} equals. Replace {m('y')} in the second equation "
             f"with {m(f'({inner})')}: {m(f'{sub} = {tx(c)}')}.",
             f"Distribute{' the minus sign' if b == -1 else ''}: {m(f'{expanded} = {tx(c)}')}, "
             f"so {m(f'{combined} = {tx(c)}')}.",
             f"Solve: {m(f'{_lin((a + b * mm, "x"))} = {tx(c - b * kk)}')}"
             + (f", so {m(f'x = {tx(X)}')}." if a + b * mm != 1 else ".")]
    if ask == "y":
        steps.append(f"Now use the first equation: {m(f'y = {_subst({"x": X}, (mm, "x"), (kk, ""))} = {tx(Y)}')}.")
    # mistakes
    xw1 = Q(c - kk) / (a + b * mm)            # distributes b only to the x-term
    xw2 = Q(c + b * kk) / (a + b * mm)        # sign error on the constant
    wrong = []
    if ask == "x":
        wrong.append((Y, f"gives the value of {m('y')}, not {m('x')}"))
        if b != 1:
            wrong.append((xw1, f"multiplies only {m(_lin((mm, 'x')))} by {m(b)}, not {m(tx(kk))}"))
        wrong.append((xw2, f"makes a sign error with the {m(tx(b * kk))}"))
        wrong.append((-X, "makes a sign error"))
    else:
        wrong.append((X, f"gives the value of {m('x')}, not {m('y')}"))
        if b != 1:
            wrong.append((mm * xw1 + kk, f"multiplies only {m(_lin((mm, 'x')))} by {m(b)}, not {m(tx(kk))}"))
        wrong.append((mm * xw2 + kk, f"makes a sign error with the {m(tx(b * kk))}"))
        wrong.append((X + Y, f"gives {m('x + y')}"))
    bx = _brute((-mm, 1, kk), (a, b, c))
    need(len(bx) == 1)
    return Problem(
        stem=choose(rng,
                    f"If {m(first)} and {m(second)}, what is the value of {m(ask)}?",
                    f"Solve the system for {m(ask)}:" + f"\\[ \\begin{{aligned}} {first.replace(' = ', ' &= ')} \\\\ "
                    f"{second.replace(' = ', ' &= ')} \\end{{aligned}} \\]"),
        answer=X if ask == "x" else Y,
        fmt=frac,
        wrong=wrong,
        steps=steps,
        check=Q(bx[0][0] if ask == "x" else bx[0][1]),
        verify=lambda v: (a * X + b * (mm * X + kk) == c) and v == (X if ask == "x" else mm * X + kk),
        near=lambda r: [(X if ask == "x" else Y) + d for d in (1, -1, 2, -2, 3, -3)],
        neg_ok=True,
    )


@template("MK")
def check_solution(rng, lvl):
    X, Y = rng.randint(-3, 9), rng.randint(-3, 9)
    need(X != Y and (X, Y) != (0, 0))
    form = rng.randint(0, 2)
    if form == 0:
        e1, e2 = (1, 2, X + 2 * Y), (1, -1, X - Y)
    elif form == 1:
        a = rng.choice([2, 3])
        e1, e2 = (a, 1, a * X + Y), (1, -1, X - Y)
    else:
        a, b = rng.choice([(1, 2), (2, 1), (1, 3), (3, 1)])
        e1, e2 = (1, 1, X + Y), (a, -b, a * X - b * Y)
    need(e1[0] * e2[1] - e1[1] * e2[0] != 0)
    ok1 = lambda p: e1[0] * p[0] + e1[1] * p[1] == e1[2]
    ok2 = lambda p: e2[0] * p[0] + e2[1] * p[1] == e2[2]
    pair = lambda p: f"$({p[0]}, {p[1]})$"
    cands = []
    if not (ok1((Y, X)) and ok2((Y, X))):
        cands.append(((Y, X), "swaps the values of $x$ and $y$"))
    for t in (1, -1, 2, -2, 3):
        p1 = (X + t, (e1[2] - e1[0] * (X + t)) // e1[1])
        if ok1(p1) and not ok2(p1):
            cands.append((p1, "works in the first equation but not the second"))
            break
    for t in (1, -1, 2, -2, 3):
        if (e2[2] - e2[0] * (X + t)) % e2[1]:
            continue
        p2 = (X + t, (e2[2] - e2[0] * (X + t)) // e2[1])
        if ok2(p2) and not ok1(p2):
            cands.append((p2, "works in the second equation but not the first"))
            break
    cands.append(((X, -Y) if Y else (-X, Y), "makes a sign error"))
    wrong, seen = [], {(X, Y)}
    for p, why in cands:
        if p in seen or (ok1(p) and ok2(p)):
            continue
        seen.add(p)
        wrong.append((pair(p), why))
    need(len(wrong) >= 3)
    vals = {"x": X, "y": Y}
    steps = [f"A solution must make \\emph{{both}} equations true. Test {pair((X, Y))}, that is, "
             f"{m(f'x = {X}')} and {m(f'y = {Y}')}.",
             f"First equation: {m(f'{_subst(vals, (e1[0], "x"), (e1[1], "y"))} = {e1[2]}')}. \\checkmark",
             f"Second equation: {m(f'{_subst(vals, (e2[0], "x"), (e2[1], "y"))} = {e2[2]}')}. \\checkmark"]
    bx = _brute(e1, e2)
    return Problem(
        stem=choose(rng,
                    f"Which ordered pair $(x, y)$ is the solution of this system?" + _system_tex(e1, e2),
                    f"Which ordered pair $(x, y)$ satisfies both {m(_eq(*e1))} and {m(_eq(*e2))}?"),
        answer=pair((X, Y)),
        fmt=text,
        wrong=wrong,
        steps=steps,
        tip=(f"You can also solve it directly: adding the equations cancels {m('y')}." if e1[1] == -e2[1] else None),
        verify=lambda s: s == pair((X, Y)) and bx == [(X, Y)],
    )


@template("MK")
def sum_trick(rng, lvl):
    X, Y = rng.randint(-4, 12), rng.randint(-4, 12)
    a, b = rng.sample([1, 2, 3, 4, 5], 2)
    need(X != Y and abs(a - b) >= 1 and (X, Y) != (0, 0))
    e1 = (a, b, a * X + b * Y)
    e2 = (b, a, b * X + a * Y)
    ask = rng.choice(["x + y", "x + y", "x - y"])
    if ask == "x + y":
        s, val = a + b, X + Y
        tot = e1[2] + e2[2]
        steps = [f"Look at the coefficients: they are swapped. Add the two equations: "
                 f"{m(f'{s}x + {s}y = {tot}')}.",
                 f"Every term has a factor of {m(s)}, so divide by {m(s)}: {m(f'x + y = {F(tot, s)} = {val}')}."]
        wrong = [(Q(tot), f"forgets to divide by {m(s)}"),
                 (Q(X), f"gives the value of {m('x')}, not {m('x + y')}"),
                 (Q(Y), f"gives the value of {m('y')}, not {m('x + y')}"),
                 (Q(X - Y), f"gives {m('x - y')} instead")]
    else:
        s, val = a - b, X - Y
        tot = e1[2] - e2[2]
        steps = [f"Look at the coefficients: they are swapped. Subtract the second equation from the first: "
                 f"{m(f'{_lin((s, "x"), (-s, "y"))} = {tot}')}.",
                 (f"Divide by {m(s)}: {m(f'x - y = {F(tot, s)} = {val}')}." if s != 1 else
                  f"That is {m(f'x - y = {val}')} already.")]
        wrong = [(Q(X + Y), f"adds the equations, which gives {m('x + y')}"),
                 (Q(X), f"gives the value of {m('x')}"),
                 (Q(Y), f"gives the value of {m('y')}")]
        if s not in (1, -1):
            wrong.insert(0, (Q(tot), f"forgets to divide by {m(s)}"))
    bx = _brute(e1, e2)
    need(len(bx) == 1)
    chk = bx[0][0] + bx[0][1] if ask == "x + y" else bx[0][0] - bx[0][1]
    return Problem(
        stem=f"If {m(_eq(*e1))} and {m(_eq(*e2))}, what is the value of {m(ask)}?",
        answer=Q(val),
        fmt=frac,
        wrong=wrong,
        steps=steps,
        tip=f"No need to find {m('x')} and {m('y')} separately (they are {m(X)} and {m(Y)}).",
        check=Q(chk),
        near=lambda r: [Q(val + d) for d in (1, -1, 2, -2, 3, -3)],
        neg_ok=True,
    )


# ---- word problems -------------------------------------------------------------

def _mo(v):
    v = Q(v)
    return r"\$" + (int_raw(v) if v.is_integer else dec_raw(v, places=2))


def _mr(v):
    v = Q(v)
    return int_raw(v) if v.is_integer else dec_raw(v, places=2)


@template("AR")
def tickets(rng, lvl):
    # level 2: admission tickets; level 3: meals and merchandise (keeps a chapter from repeating a scene)
    ctx = rng.randint(0, 4) if lvl <= 2 else rng.randint(5, 9)
    if ctx == 0:
        hi, lo, N = rng.randint(10, 18), rng.randint(4, 8), rng.randrange(80, 300, 10)
        H, L = ("adult", "adult tickets"), ("student", "student tickets")
        stem = (f"A high school band sold {num(N)} tickets to its spring concert. Adult tickets cost {{HI}} and "
                f"student tickets cost {{LO}}. The band collected {{T}}. How many {{ASK}} were sold?")
    elif ctx == 1:
        hi, lo, N = rng.randint(8, 15), rng.randint(3, 6), rng.randrange(100, 400, 10)
        H, L = ("adult", "adult tickets"), ("child", "child tickets")
        stem = (f"For Family Day on base, {num(N)} barbecue tickets were sold. Adult tickets cost {{HI}} and child "
                f"tickets cost {{LO}}. Ticket sales totaled {{T}}. How many {{ASK}} were sold?")
    elif ctx == 2:
        hi, lo, N = rng.randint(12, 20), rng.randint(5, 9), rng.randrange(60, 250, 5)
        H, L = ("adult", "adult tickets"), ("child", "child tickets")
        stem = (f"A museum sold {num(N)} tickets on Saturday. Adult tickets cost {{HI}} and child tickets cost "
                f"{{LO}}. The museum took in {{T}}. How many {{ASK}} were sold?")
    elif ctx == 3:
        hi, lo, N = rng.randint(25, 45), rng.randint(15, 22), rng.randrange(100, 400, 10)
        H, L = ("adult", "adult passes"), ("child", "child passes")
        stem = (f"A water park sold {num(N)} day passes on Saturday. Adult passes cost {{HI}} and child passes cost "
                f"{{LO}}. Pass sales were {{T}}. How many {{ASK}} were sold?")
    elif ctx == 4:
        hi, lo, N = rng.randint(9, 14), rng.randint(5, 7), rng.randrange(60, 200, 4)
        H, L = ("evening", "evening tickets"), ("matinee", "matinee tickets")
        stem = (f"The base movie theater sold {num(N)} tickets on Sunday. Evening tickets cost {{HI}} and matinee "
                f"tickets cost {{LO}}. The theater took in {{T}}. How many {{ASK}} were sold?")
    elif ctx == 5:
        hi, lo, N = rng.randint(18, 30), rng.randint(10, 16), rng.randrange(40, 160, 4)
        H, L = ("steak", "steak dinners"), ("chicken", "chicken dinners")
        stem = (f"A fundraiser sold {num(N)} dinners: steak dinners for {{HI}} each and chicken dinners for "
                f"{{LO}} each. It took in {{T}}. How many {{ASK}} were sold?")
    elif ctx == 6:
        hi, lo, N = rng.randint(15, 25), rng.randint(6, 12), rng.randrange(30, 120, 2)
        H, L = ("T-shirt", "T-shirts"), ("cap", "caps")
        stem = (f"A unit's booth at a 5K race sold {num(N)} items, all T-shirts and caps. T-shirts cost {{HI}} "
                f"and caps cost {{LO}}. Sales came to {{T}}. How many {{ASK}} were sold?")
    elif ctx == 7:
        hi, lo, N = rng.randint(30, 60), rng.randint(15, 28), rng.randrange(20, 60, 2)
        H, L = ("soldier", "soldier seats"), ("family", "family-member seats")
        stem = (f"A charter bus to a football game carried {N} passengers. Soldiers paid {{HI}} each and family "
                f"members paid {{LO}} each, for a total of {{T}}. How many {{ASK}} were sold?")
    elif ctx == 8:
        hi, lo, N = rng.randint(9, 14), rng.randint(4, 7), rng.randrange(40, 150, 2)
        H, L = ("large", "large pizzas"), ("small", "small pizzas")
        stem = (f"For a company party, the dining facility ordered {num(N)} pizzas. Large pizzas cost {{HI}} each "
                f"and small pizzas cost {{LO}} each. The bill was {{T}}. How many {{ASK}} were ordered?")
    else:
        hi, lo, N = rng.randint(20, 35), rng.randint(8, 15), rng.randrange(30, 100, 2)
        H, L = ("hoodie", "hoodies"), ("mug", "mugs")
        stem = (f"A school store sold {num(N)} hoodies and mugs during spirit week. Hoodies cost {{HI}} and mugs "
                f"cost {{LO}}. Sales totaled {{T}}. How many {{ASK}} were sold?")
    need(hi - lo >= 2)
    A = rng.randint(max(3, N // 6), N - max(3, N // 6))
    C = N - A
    T = hi * A + lo * C
    need(A != C)
    ask_hi = rng.random() < 0.5
    ans = A if ask_hi else C
    more = lvl >= 3
    if more:
        big, small_ = (H[1], L[1]) if A > C else (L[1], H[1])
        stem = (stem.replace("How many {ASK} were sold?", f"How many more {big} than {small_} were sold?")
                .replace("How many {ASK} were ordered?", f"How many more {big} than {small_} were ordered?"))
        ans = abs(A - C)
    stem = (stem.replace("{HI}", _mo(hi)).replace("{LO}", _mo(lo)).replace("{T}", _mo(T))
            .replace("{ASK}", H[1] if ask_hi else L[1]))
    v1 = H[0][0].lower()
    steps = [f"Let {m(v1)} be the number of {H[1]}. The rest are {L[1]}: {m(f'{N} - {v1}')}.",
             f"Add up the money: {m(f'{hi}{v1} + {lo}({N} - {v1}) = {int_raw(T)}')}.",
             f"Distribute and combine: {m(f'{hi}{v1} + {int_raw(lo * N)} - {lo}{v1} = {int_raw(T)}')}, so "
             f"{m(f'{_lin((hi - lo, v1))} + {int_raw(lo * N)} = {int_raw(T)}')}.",
             f"Subtract {m(int_raw(lo * N))}: {m(f'{_lin((hi - lo, v1))} = {int_raw(T - lo * N)}')}. "
             f"Divide by {m(hi - lo)}: {m(f'{v1} = {A}')}."]
    if more:
        steps.append(f"So there were {m(f'{N} - {A} = {C}')} {L[1]}. The question asks how many more: "
                     f"{m(f'{max(A, C)} - {min(A, C)} = {ans}')}.")
    elif not ask_hi:
        steps.append(f"The question asks for {L[1]}: {m(f'{N} - {A} = {C}')}.")
    steps.append(f"Check: {m(f'{hi}({A}) + {lo}({C}) = {int_raw(hi * A)} + {int_raw(lo * C)} = {int_raw(T)}')}. \\checkmark")
    if more:
        hits = [a_ for a_ in range(0, N + 1) if hi * a_ + lo * (N - a_) == T]
        need(len(hits) == 1)
        return Problem(stem=stem, answer=Q(ans), fmt=num, steps=steps, section="AR",
                       wrong=[(Q(max(A, C)), f"gives the number of {big}, not the difference"),
                              (Q(min(A, C)), f"gives the number of {small_}, not the difference"),
                              (Q(ans + 2), None)],
                       check=Q(abs(hits[0] - (N - hits[0]))),
                       near=lambda r: [Q(ans + d) for d in (-4, 4, -2, 2, 6) if ans + d > 0])
    wrong = [(Q(C if ask_hi else A), f"gives the number of {L[1] if ask_hi else H[1]}"),
             (Q(N) / 2, "assumes the two kinds were sold in equal numbers")]
    if ask_hi:
        wrong.append((Q(T - lo * N) / hi, f"divides by {_mo(hi)} instead of by the price difference {_mo(hi - lo)}"))
    else:
        wrong.append((Q(hi * N - T) / lo, f"divides by {_mo(lo)} instead of by the price difference {_mo(hi - lo)}"))
    wrong.append((Q(T) / (hi + lo), "divides the total by the sum of the two prices"))
    hits = [a_ for a_ in range(0, N + 1) if hi * a_ + lo * (N - a_) == T]
    need(len(hits) == 1)
    return Problem(stem=stem, answer=Q(ans), fmt=num, wrong=wrong, steps=steps,
                   check=Q(hits[0] if ask_hi else N - hits[0]), section="AR",
                   near=lambda r: [Q(ans + d) for d in (-10, 10, -5, 5, -2, 2) if ans + d > 0])


@template("AR")
def coins(rng, lvl):
    kind = rng.randint(0, 3)
    if kind == 0:
        big, small, bn, sn = 25, 10, "quarters", "dimes"
        N = rng.randint(12, 60)
    elif kind == 1:
        big, small, bn, sn = 10, 5, "dimes", "nickels"
        N = rng.randint(12, 60)
    elif kind == 2:
        big, small, bn, sn = 1000, 500, "\\$10 bills", "\\$5 bills"
        N = rng.randint(8, 40)
    else:
        big, small, bn, sn = 2000, 500, "\\$20 bills", "\\$5 bills"
        N = rng.randint(8, 30)
    B = rng.randint(2, N - 2)
    S = N - B
    need(B != S)
    V = big * B + small * S           # cents
    ask_big = rng.random() < 0.5
    ans = B if ask_big else S
    who = person(rng)
    if kind <= 1:
        stem = choose(rng,
                      f"A jar holds {N} coins, all {bn} and {sn}. The coins are worth {money(R(V, 100))} in all. "
                      f"How many {bn if ask_big else sn} are in the jar?",
                      f"{who.name} has {N} coins, all {bn} and {sn}, worth a total of {money(R(V, 100))}. "
                      f"How many {bn if ask_big else sn} does {who.he} have?")
        unit_word = "cents"
        bv, sv, Vt = big, small, V
        lead = (f"Work in cents so there are no decimals: a {bn[:-1]} is {m(big)} cents, a {sn[:-1]} is "
                f"{m(small)} cents, and {money(R(V, 100))} is {m(int_raw(V))} cents.")
    else:
        stem = choose(rng,
                      f"A cash drawer holds {N} bills, all {bn} and {sn}, worth {money(V // 100)} in all. "
                      f"How many {bn if ask_big else sn} are in the drawer?",
                      f"After a unit fundraiser, {soldier(rng)} counted {N} bills, all {bn} and {sn}, worth "
                      f"{money(V // 100)}. How many {bn if ask_big else sn} were there?")
        unit_word = "dollars"
        bv, sv, Vt = big // 100, small // 100, V // 100
        lead = f"Each {bn[:-1]} is worth {m(bv)} dollars and each {sn[:-1]} is worth {m(sv)} dollars."
    v1 = "b"
    steps = [lead,
             f"Let {m(v1)} be the number of {bn}; then there are {m(f'{N} - {v1}')} {sn}. Total value: "
             f"{m(f'{bv}{v1} + {sv}({N} - {v1}) = {int_raw(Vt)}')}.",
             f"Distribute: {m(f'{bv}{v1} + {int_raw(sv * N)} - {sv}{v1} = {int_raw(Vt)}')}, so "
             f"{m(f'{bv - sv}{v1} = {int_raw(Vt)} - {int_raw(sv * N)} = {int_raw(Vt - sv * N)}')}.",
             f"Divide by {m(bv - sv)}: {m(f'{v1} = {B}')}."]
    if not ask_big:
        steps.append(f"The question asks for {sn}: {m(f'{N} - {B} = {S}')}.")
    wrong = [(Q(S if ask_big else B), f"gives the number of {sn if ask_big else bn}"),
             (Q(N) / 2, "assumes there are equally many of each")]
    if ask_big:
        wrong.append((Q(Vt - sv * N) / bv, f"divides by {m(bv)} instead of by the difference {m(bv - sv)}"))
    else:
        wrong.append((Q(bv * N - Vt) / sv, f"divides by {m(sv)} instead of by the difference {m(bv - sv)}"))
    wrong.append((Q(Vt) / bv if ask_big else Q(Vt) / sv,
                  f"divides the total value by the value of one {'coin' if kind <= 1 else 'bill'}"))
    hits = [b_ for b_ in range(0, N + 1) if bv * b_ + sv * (N - b_) == Vt]
    need(len(hits) == 1)
    return Problem(stem=stem, answer=Q(ans), fmt=num, wrong=wrong, steps=steps,
                   check=Q(hits[0] if ask_big else N - hits[0]), section="AR",
                   near=lambda r: [Q(ans + d) for d in (-4, 4, -2, 2, -1, 1) if ans + d > 0])


@template("AR")
def sum_diff(rng, lvl):
    ask_large = rng.random() < 0.5 if lvl > 1 else rng.random() < 0.7
    who = person(rng)
    ctx = rng.randint(0, 6) if lvl > 1 else -1
    lo_s, hi_s, lo_d, hi_d = {-1: (3, 40, 2, 20), 0: (6, 25, 2, 12), 1: (8, 40, 2, 30),
                              2: (8, 35, 2, 15), 3: (5, 12, 2, 6), 4: (10, 60, 2, 20),
                              5: (12, 50, 2, 16), 6: (3, 9, 2, 4)}[ctx]
    S_small = rng.randint(lo_s, hi_s)
    D = rng.randint(lo_d, hi_d)
    Lg = S_small + D
    S = S_small + Lg
    if lvl == 1:
        stem = (f"The sum of two numbers is {S}, and their difference is {D}. What is the "
                f"{'larger' if ask_large else 'smaller'} number?")
        L_name, S_name = "the larger number", "the smaller number"
        unit_w = ""
    else:
        if ctx == 0:
            stem = (f"A {S}-foot rope is cut into two pieces. One piece is {D} feet longer than the other. "
                    f"How long is the {'longer' if ask_large else 'shorter'} piece?")
            L_name, S_name, unit_w = "the longer piece", "the shorter piece", " feet"
        elif ctx == 1:
            o = person(rng, exclude=[who])
            stem = (f"{who.name} is {D} years older than {o.name}. The sum of their ages is {S}. "
                    f"How old is {who.name if ask_large else o.name}?")
            L_name, S_name, unit_w = f"{who.name}'s age", f"{o.name}'s age", " years"
        elif ctx == 2:
            stem = (f"Two squads collected {S} bags of litter during a base cleanup. The first squad collected "
                    f"{D} more bags than the second. How many bags did the {'first' if ask_large else 'second'} "
                    f"squad collect?")
            L_name, S_name, unit_w = "the first squad's bags", "the second squad's bags", " bags"
        elif ctx == 4:
            stem = (f"Two recruiters signed up {S} recruits last quarter. One recruiter signed up {D} more than "
                    f"the other. How many recruits did the {'more' if ask_large else 'less'} successful recruiter sign up?")
            L_name, S_name, unit_w = "the larger count", "the smaller count", " recruits"
        elif ctx == 5:
            stem = (f"Two water trailers hold a total of {S * 10} gallons. One holds {D * 10} gallons more than the "
                    f"other. How many gallons does the {'larger' if ask_large else 'smaller'} trailer hold?")
            L_name, S_name, unit_w = "the larger trailer's gallons", "the smaller trailer's gallons", " gallons"
            S_small, D, Lg, S = S_small * 10, D * 10, Lg * 10, S * 10
        elif ctx == 6:
            stem = (f"A {S}-foot board is cut into two pieces. One piece is {D} feet longer than the other. "
                    f"How long is the {'longer' if ask_large else 'shorter'} piece?")
            L_name, S_name, unit_w = "the longer piece", "the shorter piece", " feet"
        else:
            stem = (f"On a two-day ruck march, a platoon covered {S} miles. It marched {D} more miles on the "
                    f"first day than on the second. How many miles did it march on the "
                    f"{'first' if ask_large else 'second'} day?")
            L_name, S_name, unit_w = "the first day's miles", "the second day's miles", " miles"
    steps = [f"Let {m('L')} be {L_name} and {m('s')} be {S_name}. Then {m(f'L + s = {S}')} and {m(f'L - s = {D}')}.",
             f"Add the two equations; {m('s')} cancels: {m(f'2L = {S + D}')}, so {m(f'L = {Lg}')}.",
             (f"Then {m(f's = {S} - {Lg} = {S_small}')}." if not ask_large else
              f"Check: the other is {m(f'{S} - {Lg} = {S_small}')}, and {m(f'{Lg} - {S_small} = {D}')}. \\checkmark")]
    ans = Lg if ask_large else S_small
    wrong = [(Q(S_small if ask_large else Lg), f"gives {S_name if ask_large else L_name} instead"),
             (Q(S) / 2, "splits the total evenly and ignores the difference"),
             (Q(S + D) if ask_large else Q(S - D), "forgets to divide by 2"),
             (Q(S - D) if ask_large else Q(S + D) / 2, None)]
    hits = [(a_, S - a_) for a_ in range(0, S + 1) if a_ - (S - a_) == D]
    need(len(hits) == 1)
    return Problem(stem=stem, answer=Q(ans), fmt=num, wrong=wrong, steps=steps,
                   check=Q(hits[0][0] if ask_large else hits[0][1]), section="AR",
                   near=lambda r: [Q(ans + d) for d in (-3, 3, -2, 2, -4, 4) if ans + d > 0])


_MIX = [
    # place, (cheap, verb, price range), (dear, verb, price range), product, variable
    ("A coffee shop", ("house coffee", "costs", (4, 7)), ("premium coffee", "costs", (10, 14)), "a coffee blend", "h"),
    ("A grocery store", ("peanuts", "cost", (2, 4)), ("cashews", "cost", (7, 10)), "trail mix", "p"),
    ("A candy shop", ("hard candy", "costs", (2, 5)), ("chocolates", "cost", (8, 12)), "a candy mix", "h"),
    ("The dining facility on base", ("regular coffee", "costs", (4, 6)), ("dark-roast coffee", "costs", (9, 12)),
     "a coffee blend", "r"),
    ("A tea shop", ("black tea", "costs", (6, 9)), ("green tea", "costs", (12, 16)), "a tea blend", "b"),
    ("A feed store", ("cracked corn", "costs", (1, 2)), ("sunflower seeds", "cost", (4, 6)), "a bird-feed mix", "c"),
    ("The post exchange", ("pretzels", "cost", (2, 4)), ("mixed nuts", "cost", (8, 11)), "a snack mix", "p"),
    ("A garden center", ("basic grass seed", "costs", (2, 4)), ("shade grass seed", "costs", (6, 9)),
     "a lawn-seed mix", "g"),
]


@template("AR")
def mixture(rng, lvl):
    place, (cheap, v1, r1), (dear, v2, r2), what, var = rng.choice(_MIX)
    p1, p2 = rng.randint(*r1), rng.randint(*r2)
    W = rng.choice([10, 12, 15, 16, 20, 24, 25, 30, 40, 50])
    a = rng.randint(2, W - 2)          # pounds of the cheap one
    b = W - a
    total = p1 * a + p2 * b
    need(total % W == 0 and a != b)
    p = total // W
    need(p1 < p < p2)
    ask_cheap = rng.random() < 0.6
    ans = a if ask_cheap else b
    stem = (f"{place} mixes {cheap} that {v1} {_mo(p1)} per pound with {dear} that {v2} {_mo(p2)} per pound "
            f"to make {W} pounds of {what} that sells for {_mo(p)} per pound. How many pounds of "
            f"{cheap if ask_cheap else dear} are in the mix?")
    steps = [f"Let {m(var)} be the pounds of {cheap}; then {m(f'{W} - {var}')} pounds are {dear}.",
             f"The value of the mix is {m(f'{W} \\times {p} = {total}')} dollars, so "
             f"{m(f'{p1}{var} + {p2}({W} - {var}) = {total}')}.",
             f"Distribute and combine: {m(f'{p1}{var} + {p2 * W} - {p2}{var} = {total}')}, so "
             f"{m(f'-{p2 - p1}{var} + {p2 * W} = {total}')}.",
             f"Subtract {m(p2 * W)}: {m(f'-{p2 - p1}{var} = {total - p2 * W}')}. Divide by {m(-(p2 - p1))}: "
             f"{m(f'{var} = {a}')} pounds of {cheap}."]
    if not ask_cheap:
        steps.append(f"The question asks for {dear}: {m(f'{W} - {a} = {b}')} pounds.")
    wrong = [(Q(b if ask_cheap else a), f"gives the pounds of {dear if ask_cheap else cheap}"),
             (Q(W) / 2, "assumes equal amounts of each"),
             (Q(p2 * W - total) / p1 if ask_cheap else Q(total - p1 * W) / p2,
              f"divides by {_mo(p1 if ask_cheap else p2)} instead of by the price difference {_mo(p2 - p1)}")]
    hits = [c_ for c_ in range(0, W + 1) if p1 * c_ + p2 * (W - c_) == p * W]
    need(len(hits) == 1)
    closer = cheap if p - p1 < p2 - p else dear
    return Problem(stem=stem, answer=Q(ans), fmt=unit(num, "pound"), wrong=wrong, steps=steps,
                   check=Q(hits[0] if ask_cheap else W - hits[0]), section="AR",
                   tip=(f"Sense check: the mix price {_mo(p)} is closer to the price of {closer}, so the mix "
                        f"must contain more {closer}." if p - p1 != p2 - p else None),
                   near=lambda r: [Q(ans + d) for d in (-3, 3, -2, 2, -1, 1) if 0 < ans + d < W])


PLAN = [
    # (template, level, count)  -- easy -> hard; 25 problems
    (elimination, 1, 3),
    (check_solution, 1, 3),
    (sum_diff, 1, 2),
    (elimination, 2, 3),
    (substitution, 2, 2),
    (tickets, 2, 2),
    (coins, 2, 1),
    (sum_diff, 2, 2),
    (elimination, 3, 2),
    (sum_trick, 3, 2),
    (mixture, 3, 2),
    (tickets, 3, 1),
]
