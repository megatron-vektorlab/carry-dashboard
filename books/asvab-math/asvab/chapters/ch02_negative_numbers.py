"""Chapter 2 - Negative Numbers & Absolute Value."""
import sympy as sp

from ..core import (Q, Problem, need, num, text, m, int_raw, unit, person,
                    soldier, choose, template)

NUM = 2
TITLE = r"Negative Numbers \& Absolute Value"
PART = 1

INTRO = r"""
Negative numbers show up whenever something goes below a starting point:
temperatures below zero, depths below sea level, an overdrawn bank account.
A handful of sign rules covers every problem in this chapter.

\begin{concept}{The number line and absolute value}
Numbers increase to the right. Every negative number is less than $0$, and
the farther left, the smaller: $-9 < -4 < 0 < 3$.

The \emph{absolute value} $\lvert x \rvert$ is the distance from $0$, so it is never
negative: $\lvert -7 \rvert = 7$ and $\lvert 7 \rvert = 7$. The distance between two
numbers is the absolute value of their difference: from $-3$ to $5$ is
$\lvert 5 - (-3) \rvert = 8$.
\end{concept}

\begin{concept}{Adding and subtracting}
\begin{itemize}
\item \textbf{Same signs:} add the absolute values, keep the sign:
  $-6 + (-9) = -15$.
\item \textbf{Different signs:} subtract the absolute values, keep the sign
  of the number with the larger absolute value: $-11 + 4 = -7$.
\item \textbf{Subtracting} means adding the opposite:
  $5 - 8 = 5 + (-8) = -3$ and $-7 - (-12) = -7 + 12 = 5$.
\end{itemize}
\end{concept}

\begin{concept}{Multiplying and dividing}
Same signs give a positive answer; different signs give a negative answer:
$(-6)(-7) = 42$, \ $-48 \div 6 = -8$. With several factors, count the
negatives: an even number of them gives a positive product, an odd number a
negative one. Watch exponents: $(-3)^2 = (-3)(-3) = 9$, but
$-3^2 = -(3 \times 3) = -9$.
\end{concept}

\begin{example}{Worked example}
At 5 a.m. the temperature was $-8^\circ$F. By noon it was $13^\circ$F. How
many degrees did the temperature rise?

\textbf{Solution.} Rise $=$ new $-$ old $= 13 - (-8) = 13 + 8 = 21$ degrees.
On a number line: $8$ degrees up to $0$, then $13$ more.
\end{example}

\begin{tip}
For a change or a distance, think ``how far apart on the number line.'' If
the two numbers are on opposite sides of $0$, \emph{add} their absolute
values ($-8$ to $13$: $8 + 13 = 21$); if they are on the same side,
\emph{subtract} them.
\end{tip}

\begin{trap}
\begin{itemize}
\item Reading $-7 - (-12)$ as $-7 - 12$. Two negatives in a row make a plus.
\item Thinking $-12$ is greater than $-5$ because $12 > 5$.
\item Squaring before the sign: $-4^2 = -16$, while $(-4)^2 = 16$.
\item Keeping a negative sign inside absolute value bars: $\lvert 3 - 9 \rvert = 6$, not $-6$.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _r(v):
    """Raw signed integer (no parentheses)."""
    return int_raw(v)


def _p(v):
    """Raw signed integer, in parentheses when negative: (-7)."""
    v = Q(v)
    return f"({int_raw(v)})" if v < 0 else int_raw(v)


def _bars(s):
    """Turn |...| pairs into \\lvert ... \\rvert (correct spacing for |-7|)."""
    out, open_ = [], True
    for ch in s:
        if ch == "|":
            out.append(r"\lvert " if open_ else r"\rvert ")
            open_ = not open_
        else:
            out.append(ch)
    return "".join(out)


def _fix_bars(pr):
    pr.stem = _bars(pr.stem)
    pr.steps = [_bars(t) for t in pr.steps]
    pr.wrong = [(w[0], _bars(w[1]) if w[1] else w[1]) + tuple(w[2:]) for w in pr.wrong]
    return pr


def _mlist(vals):
    """Numbers as separate math pieces so the line can break: $-3$, $5$, and $8$."""
    return ", ".join(m(_r(v)) for v in vals)


def _sgn_word(v):
    return "positive" if v > 0 else "negative"


def _add_two(u, v):
    """One explained step for u + v (signed)."""
    u, v = Q(u), Q(v)
    s = u + v
    work = m(f"{_r(u)} + {_p(v)} = {_r(s)}")
    if u == 0 or v == 0:
        return f"{work}."
    if u > 0 and v > 0:
        return f"Add: {work}."
    if (u > 0) == (v > 0):
        return (f"Same signs: add the absolute values ({m(f'{_r(abs(u))} + {_r(abs(v))} = {_r(abs(s))}')}) "
                f"and keep the sign: {work}.")
    big = u if abs(u) > abs(v) else v
    if s == 0:
        return f"Opposites add to zero: {work}."
    return (f"Different signs: subtract the absolute values "
            f"({m(f'{_r(max(abs(u), abs(v)))} - {_r(min(abs(u), abs(v)))} = {_r(abs(s))}')}) and keep "
            f"the sign of {m(_r(big))}, which has the larger absolute value: {work}.")


def _deg(v):
    return m(int_raw(v) + r"^{\circ}\mathrm{F}")


def _signed_money(v):
    v = Q(v)
    body = r"\$" + int_raw(abs(v))
    return (m("-") + body) if v < 0 else body


_ft = unit(num, "ft", "ft")


def _near_int(v, offsets=(1, 2, 3, 4, 5)):
    def f(r):
        out = [Q(v) + d * s for d in offsets for s in (1, -1)]
        r.shuffle(out)
        return out
    return f


# --------------------------------------------------------------------------
# adding and subtracting
# --------------------------------------------------------------------------

@template("MK")
def add_sub(rng, lvl):
    if lvl == 1:
        form = rng.choice(["neg+pos", "pos-big", "neg-pos", "neg+neg"])
        a_, b_ = rng.randint(2, 15), rng.randint(2, 15)
        need(a_ != b_)
        if form == "neg+pos":
            first, op, second = -a_, "+", b_
        elif form == "pos-big":
            a_, b_ = min(a_, b_), max(a_, b_)
            first, op, second = a_, "-", b_
        elif form == "neg-pos":
            first, op, second = -a_, "-", b_
        else:
            first, op, second = -a_, "+", -b_
        terms = [(None, first), (op, second)]
    else:
        n_terms = rng.choice([2, 3, 3])
        first = rng.choice([-1, 1]) * rng.randint(2, 20)
        terms = [(None, first)]
        for _ in range(n_terms - 1):
            terms.append((rng.choice(["+", "-"]), rng.choice([-1, 1, -1]) * rng.randint(2, 20)))
        need(any(op == "-" and v < 0 for op, v in terms[1:]))     # at least one "- (-b)"
    # display
    disp = _r(terms[0][1]) + "".join(f" {op} {_p(v)}" for op, v in terms[1:])
    signed = [terms[0][1]] + [v if op == "+" else -v for op, v in terms[1:]]
    ans = sum(Q(v) for v in signed)
    need(ans != 0)
    # traps
    wrong = [(-ans, "has the right size but the wrong sign")]
    if any(op == "-" and v < 0 for op, v in terms[1:]):
        alt = [terms[0][1]] + [(-abs(v) if (op == "-" and v < 0) else (v if op == "+" else -v)) for op, v in terms[1:]]
        b_ = next(abs(v) for op, v in terms[1:] if op == "-" and v < 0)
        wrong.append((sum(Q(x) for x in alt),
                      f"subtracts {m(b_)} instead of adding it; subtracting a negative means adding"))
    if any(op == "+" and v < 0 for op, v in terms[1:]):
        alt = [terms[0][1]] + [(abs(v) if (op == "+" and v < 0) else (v if op == "+" else -v)) for op, v in terms[1:]]
        b_ = next(abs(v) for op, v in terms[1:] if op == "+" and v < 0)
        wrong.append((sum(Q(x) for x in alt),
                      f"adds {m(b_)} instead of subtracting it; adding a negative means subtracting"))
    if len(terms) == 2:
        u, (op, v) = terms[0][1], terms[1]
        if u < 0 and op == "-" and v > 0:
            wrong.append((-(Q(abs(u)) - v), f"treats {m(disp)} as {m(f'-({abs(u)} - {v})')}"))
        if u < 0 and op == "+" and v > 0:
            wrong.append((-(Q(abs(u)) + v), f"adds {m(abs(u))} and {m(v)} instead of finding their difference"))
        if u > 0 and op == "-" and v > u:
            wrong.append((Q(u + v), "adds the numbers instead of subtracting"))
    wrong.append((sum(Q(abs(x)) for x in signed), "ignores the signs and adds all the numbers"))
    # steps
    steps = []
    if any(op == "-" for op, _ in terms[1:]):
        rewritten = _r(signed[0]) + "".join(f" + {_p(v)}" for v in signed[1:])
        steps.append(f"Rewrite each subtraction as adding the opposite: {m(f'{disp} = {rewritten}')}.")
    run = Q(signed[0])
    for v in signed[1:]:
        steps.append(_add_two(run, v))
        run += v
    return Problem(
        stem=choose(rng, f"What is {m(disp)}?", f"Evaluate: {m(disp)}", f"Simplify: {m(disp)}"),
        answer=ans,
        fmt=num,
        wrong=wrong,
        steps=steps,
        check=sp.sympify(disp.replace("{,}", "")),
        neg_ok=True,
        near=_near_int(ans),
    )


# --------------------------------------------------------------------------
# multiplying and dividing
# --------------------------------------------------------------------------

def _neg_rule(k):
    return ("an even number of negative signs gives a positive answer" if k % 2 == 0
            else "an odd number of negative signs gives a negative answer")


@template("MK")
def mult_div(rng, lvl):
    if lvl == 1:
        a_, b_ = rng.randint(2, 12), rng.randint(2, 12)
        sa, sb = rng.choice([(-1, -1), (-1, 1), (1, -1), (-1, -1)])
        if rng.random() < 0.5:
            u, v = sa * a_, sb * b_
            ans = Q(u) * v
            disp = rf"{_p(u)} \times {_p(v)}" if rng.random() < 0.6 else f"{_p(u)}{_p(v)}"
            need(u < 0 or v < 0)
            word = "Multiply"
            wrong = [(Q(u + v), "adds the numbers instead of multiplying")]
        else:
            q = sa * a_
            v = sb * b_
            u = q * v
            ans = Q(q)
            disp = rf"{_r(u)} \div {_p(v)}"
            word = "Divide"
            wrong = [(Q(u + v) if abs(u + v) < 100 else Q(abs(a_) + abs(b_)), None)]
        same = (u < 0) == (v < 0)
        optex = r"\times" if word == "Multiply" else r"\div"
        wrong.insert(0, (-ans, f"uses the wrong sign: {'same' if same else 'different'} signs give a "
                               f"{'positive' if same else 'negative'} answer"))
        return Problem(
            stem=choose(rng, f"What is {m(disp)}?", f"Evaluate: {m(disp)}"),
            answer=ans,
            fmt=num,
            wrong=wrong,
            steps=[
                f"{word} the absolute values: "
                + m(f"{abs(u)} {optex} {abs(v)} = {abs(ans)}") + ".",
                f"The signs are {'the same' if same else 'different'}, so the answer is "
                f"{_sgn_word(ans)}: {m(f'{disp} = {_r(ans)}')}.",
            ],
            check=(sp.Integer(u) * v) if word == "Multiply" else sp.Rational(u, v),
            neg_ok=True,
            near=_near_int(ans, (1, 2, 4, 10)),
        )
    # level 2: three numbers, or a quotient times a number
    if rng.random() < 0.5:
        fs = [rng.choice([-1, 1]) * rng.randint(2, 6) for _ in range(3)]
        need(sum(1 for f in fs if f < 0) >= 2 or (sum(1 for f in fs if f < 0) == 1 and rng.random() < 0.4))
        ans = Q(fs[0]) * fs[1] * fs[2]
        disp = r" \times ".join(_p(f) for f in fs) if rng.random() < 0.5 else "".join(f"({_r(f)})" for f in fs)
        k = sum(1 for f in fs if f < 0)
        steps = [
            f"Count the negative factors: there {'is' if k == 1 else 'are'} {m(k)}, and "
            f"{_neg_rule(k)}.",
            "Multiply the absolute values: "
            + m(r" \times ".join(str(abs(f)) for f in fs) + f" = {abs(ans)}") + ".",
            f"So {m(f'{disp} = {_r(ans)}')}.",
        ]
        wrong = [(-ans, f"gets the sign wrong; {_neg_rule(k)}"),
                 (Q(sum(fs)), "adds the numbers instead of multiplying")]
        check = sp.Mul(*[sp.Integer(f) for f in fs])
    else:
        d = rng.choice([-1, 1]) * rng.randint(2, 9)
        q = rng.choice([-1, 1]) * rng.randint(2, 9)
        c = rng.choice([-1, 1]) * rng.randint(2, 6)
        top = q * d
        need(top < 0 or d < 0)
        ans = Q(q) * c
        disp = rf"({_r(top)} \div {_p(d)}) \times {_p(c)}"
        k = sum(1 for f in (top, d, c) if f < 0)
        steps = [
            f"Parentheses first: {m(rf'{_r(top)} \div {_p(d)} = {_r(q)}')} "
            f"({'same signs, positive' if (top < 0) == (d < 0) else 'different signs, negative'}).",
            f"Then multiply: {m(rf'{_p(q)} \times {_p(c)} = {_r(ans)}')} "
            f"({'same signs, positive' if (q < 0) == (c < 0) else 'different signs, negative'}).",
        ]
        wrong = [(-ans, "gets the sign wrong in one of the steps"),
                 (Q(top) / (Q(d) * c), "multiplies before dividing, ignoring the parentheses")]
        check = sp.Rational(top, d) * c
    return Problem(
        stem=choose(rng, f"What is {m(disp)}?", f"Evaluate: {m(disp)}"),
        answer=ans,
        fmt=num,
        wrong=wrong,
        steps=steps,
        check=check,
        neg_ok=True,
        near=_near_int(ans, (1, 2, 6, 10)),
    )


# --------------------------------------------------------------------------
# absolute value
# --------------------------------------------------------------------------

@template("MK")
def abs_value(rng, lvl):
    return _fix_bars(_abs_value(rng, lvl))


def _abs_value(rng, lvl):
    if lvl == 1:
        form = rng.choice(["sum", "diff_inside", "abs_minus"])
        if form == "sum":
            a_, b_ = -rng.randint(2, 15), rng.choice([-1, 1]) * rng.randint(2, 15)
            disp = f"|{_r(a_)}| + |{_r(b_)}|"
            ans = Q(abs(a_) + abs(b_))
            steps = [f"Absolute value is distance from zero: {m(f'|{_r(a_)}| = {abs(a_)}')} and "
                     f"{m(f'|{_r(b_)}| = {abs(b_)}')}.",
                     f"Add: {m(f'{abs(a_)} + {abs(b_)} = {ans}')}."]
            wrong = [(Q(a_ + b_), "adds the numbers inside the bars and keeps their signs"),
                     (-ans, "makes the answer negative; absolute values are never negative")]
            if b_ < 0:
                wrong.append((Q(abs(a_) - abs(b_)), None))
        elif form == "diff_inside":
            a_, b_ = rng.randint(-9, 9), rng.randint(-9, 12)
            need(a_ < b_ and a_ != 0)
            inner = a_ - b_
            disp = f"|{_r(a_)} - {_p(b_)}|"
            ans = Q(abs(inner))
            steps = [f"Work inside the bars first: {m(f'{_r(a_)} - {_p(b_)} = {_r(inner)}')}.",
                     f"Take the absolute value: {m(f'|{_r(inner)}| = {ans}')}."]
            wrong = [(Q(inner), "forgets to take the absolute value"),
                     (Q(abs(abs(a_) - abs(b_))), "subtracts the absolute values of the two numbers")
                     if (a_ < 0) != (b_ < 0) else (Q(abs(a_) + abs(b_)), "adds the absolute values")]
        else:
            a_, b_ = rng.randint(2, 15), rng.randint(2, 15)
            need(a_ != b_)
            a_neg, b_neg = rng.random() < 0.5, rng.random() < 0.7
            A, B = (-a_ if a_neg else a_), (-b_ if b_neg else b_)
            disp = f"|{_r(A)}| - |{_r(B)}|"
            ans = Q(a_ - b_)
            steps = [f"Find each absolute value: {m(f'|{_r(A)}| = {a_}')} and {m(f'|{_r(B)}| = {b_}')}.",
                     f"Subtract: {m(f'{a_} - {b_} = {_r(ans)}')}."]
            wrong = [(Q(A - B), "subtracts the numbers inside the bars and keeps their signs"),
                     (-ans, "has the right size but the wrong sign"),
                     (Q(a_ + b_), "adds the absolute values instead of subtracting")]
        return Problem(
            stem=choose(rng, f"What is the value of {m(disp)}?", f"Evaluate: {m(disp)}"),
            answer=ans,
            fmt=num,
            wrong=wrong,
            steps=steps,
            check=_abs_eval(disp),
            neg_ok=True,
            near=_near_int(ans),
        )
    if lvl == 2:
        a_, b_ = rng.randint(-9, 9), rng.randint(-9, 12)
        c_ = rng.randint(2, 12) * rng.choice([-1, 1, -1])
        need(a_ < b_ and a_ != 0 and b_ != 0)
        inner = a_ - b_
        if rng.random() < 0.5:
            disp = f"|{_r(a_)} - {_p(b_)}| - |{_r(c_)}|"
            ans = Q(abs(inner) - abs(c_))
            wrong = [(Q(inner - abs(c_)), f"treats {m(f'|{_r(a_)} - {_p(b_)}|')} as {m(_r(inner))} instead of {m(abs(inner))}"),
                     (Q(abs(inner) + abs(c_)), f"treats {m(f'-|{_r(c_)}|')} as {m(f'+{abs(c_)}')}"),
                     (-ans, "has the right size but the wrong sign")]
            last = f"Subtract: {m(f'{abs(inner)} - {abs(c_)} = {_r(ans)}')}."
        else:
            disp = f"|{_r(c_)}| \\times |{_r(a_)} - {_p(b_)}|"
            ans = Q(abs(inner) * abs(c_))
            wrong = [(Q(inner * c_) if inner * c_ != ans else Q(inner * abs(c_)),
                      "keeps the signs inside the bars instead of taking absolute values"),
                     (Q(abs(c_) + abs(inner)), "adds instead of multiplying"),
                     (-ans, "makes the answer negative; absolute values are never negative")]
            last = f"Multiply: {m(rf'{abs(c_)} \times {abs(inner)} = {ans}')}."
        steps = [
            f"Work inside the bars first: {m(f'{_r(a_)} - {_p(b_)} = {_r(inner)}')}, so "
            f"{m(f'|{_r(a_)} - {_p(b_)}| = |{_r(inner)}| = {abs(inner)}')}.",
            f"Also {m(f'|{_r(c_)}| = {abs(c_)}')}.",
            last,
        ]
        return Problem(
            stem=choose(rng, f"What is the value of {m(disp)}?", f"Evaluate: {m(disp)}"),
            answer=ans,
            fmt=num,
            wrong=wrong,
            steps=steps,
            check=_abs_eval(disp),
            neg_ok=True,
            near=_near_int(ans),
        )
    # level 3: substitute, then absolute values
    x_, y_ = -rng.randint(2, 12), rng.randint(2, 12)
    k = rng.randint(2, 5)
    if rng.random() < 0.5:
        expr_ = f"|{k}x - y| - |x|"
        inner = k * x_ - y_
        ans = Q(abs(inner) - abs(x_))
        wrong = [(Q(inner - x_), "keeps the signs instead of taking absolute values"),
                 (Q(abs(k * abs(x_) - y_) - abs(x_)), f"uses {m(abs(x_))} for {m('x')} inside the first bars"),
                 (Q(abs(inner) + abs(x_)), f"treats {m('-|x|')} as {m(f'+{abs(x_)}')}"),
                 (-ans, "has the right size but the wrong sign")]
        steps = [
            f"Substitute: {m(f'|{k}({_r(x_)}) - {y_}| - |{_r(x_)}|')}.",
            f"Inside the first bars: {m(f'{k}({_r(x_)}) - {y_} = {_r(k * x_)} - {y_} = {_r(inner)}')}, "
            f"and {m(f'|{_r(inner)}| = {abs(inner)}')}. Also {m(f'|{_r(x_)}| = {abs(x_)}')}.",
            f"Subtract: {m(f'{abs(inner)} - {abs(x_)} = {_r(ans)}')}.",
        ]
    else:
        expr_ = f"|x + y| - |x| - |y|"
        need(abs(x_) != y_)
        inner = x_ + y_
        ans = Q(abs(inner) - abs(x_) - abs(y_))
        wrong = [(Q(inner - x_ - y_), "keeps the signs instead of taking absolute values"),
                 (-ans, "has the right size but the wrong sign"),
                 (Q(abs(inner) + abs(x_) + abs(y_)), "adds the absolute values instead of subtracting")]
        steps = [
            f"Substitute: {m(f'|{_r(x_)} + {y_}| - |{_r(x_)}| - |{y_}|')}.",
            f"Inside the first bars: {m(f'{_r(x_)} + {y_} = {_r(inner)}')}, and "
            f"{m(f'|{_r(inner)}| = {abs(inner)}')}. Also {m(f'|{_r(x_)}| = {abs(x_)}')} and "
            f"{m(f'|{y_}| = {y_}')}.",
            f"Subtract from left to right: {m(f'{abs(inner)} - {abs(x_)} - {y_} = {_r(ans)}')}.",
        ]
    X, Y = sp.Integer(x_), sp.Integer(y_)
    chk = (sp.Abs(k * X - Y) - sp.Abs(X)) if "k" not in expr_ and expr_.startswith(f"|{k}x") else \
        (sp.Abs(X + Y) - sp.Abs(X) - sp.Abs(Y))
    return Problem(
        stem=choose(rng, f"If {m(f'x = {_r(x_)}')} and {m(f'y = {y_}')}, what is the value of {m(expr_)}?",
                    f"What is the value of {m(expr_)} when {m(f'x = {_r(x_)}')} and {m(f'y = {y_}')}?"),
        answer=ans,
        fmt=num,
        wrong=wrong,
        steps=steps,
        check=chk,
        neg_ok=True,
        near=_near_int(ans),
    )


def _abs_eval(disp):
    """Independent check: evaluate a displayed expression with sympy, |..| -> Abs(..)."""
    s = disp.replace(r"\times", "*").replace("{,}", "")
    out, open_ = "", True
    for ch in s:
        if ch == "|":
            out += "Abs(" if open_ else ")"
            open_ = not open_
        else:
            out += ch
    return sp.sympify(out)


# --------------------------------------------------------------------------
# ordering
# --------------------------------------------------------------------------

@template("MK")
def order_ints(rng, lvl):
    if lvl == 1:
        want = rng.choice(["greatest", "least"])
        if want == "greatest":
            vals = sorted(rng.sample(range(-20, 0), 4))           # all negative
            ans = vals[-1]
            most = vals[0]
            wrong = [(Q(most), f"has the largest absolute value, but it is the farthest left of {m(0)}")]
            wrong += [(Q(v), f"is farther left of {m(0)} than {m(_r(ans))}") for v in vals[1:-1]]
            steps = [f"All four numbers are negative. On a number line, the greatest one is the "
                     f"one farthest to the right, which is the one closest to {m(0)}.",
                     f"{m(_r(ans))} is closest to {m(0)}, so it is the greatest: "
                     f"{m(' < '.join(_r(v) for v in vals))}."]
        else:
            negs = sorted(rng.sample(range(-20, 0), 2))
            poss = rng.sample(range(0, 20), 2)
            vals = sorted(negs + poss)
            ans = vals[0]
            other_neg = negs[1]
            wrong = [(Q(other_neg), f"is negative, but closer to {m(0)} than {m(_r(ans))}")]
            for v in poss:
                wrong.append((Q(v), f"is not negative, so it is greater than any negative number"))
            steps = [f"The least number is the one farthest to the left on a number line.",
                     f"Of the two negative numbers, {m(_r(ans))} is farther from {m(0)} than "
                     f"{m(_r(other_neg))}, so {m(_r(ans))} is the least: "
                     f"{m(' < '.join(_r(v) for v in vals))}."]
        shown = rng.sample(vals, 4)
        return Problem(
            stem=choose(rng, f"Which of the numbers {_mlist(shown)} is the {want}?",
                        f"Of {_mlist(shown[:-1])}, and {m(_r(shown[-1]))}, which number is the {want}?"),
            answer=Q(ans),
            fmt=num,
            wrong=wrong,
            steps=steps,
            check=Q(max(vals) if want == "greatest" else min(vals)),
            sort=False,
            neg_ok=True,
            near=lambda r: [],
        )
    vals = rng.sample(range(-15, 0), 3) + rng.sample(range(1, 15), 2)
    need(len({abs(v) for v in vals}) == 5)
    asc = sorted(vals)
    by_abs = sorted(vals, key=abs)
    neg_rev = sorted([v for v in vals if v < 0], key=abs) + sorted(v for v in vals if v > 0)
    desc = asc[::-1]

    def show(lst):
        return m(", ".join(_r(v) for v in lst))
    wrong = [(show(by_abs), "orders the numbers by their distance from 0, ignoring the signs"),
             (show(neg_rev), "puts the negative numbers in the wrong order; for negatives, the "
                             "larger absolute value is the smaller number"),
             (show(desc), "lists the numbers from greatest to least")]
    need(len({show(asc)} | {w for w, _ in wrong}) == 4)
    shown = rng.sample(vals, 5)
    return Problem(
        stem=(f"Which list shows the numbers {_mlist(shown)} in order from least to greatest?"),
        answer=show(asc),
        fmt=text,
        wrong=wrong,
        steps=[
            "Negative numbers come first. Among them, the one farthest from 0 is the least: "
            f"{m(' < '.join(_r(v) for v in asc if v < 0))}.",
            f"Then the positive numbers: {m(' < '.join(_r(v) for v in asc if v > 0))}.",
            f"So the order is {show(asc)}.",
        ],
        verify=lambda s: s == show(sorted(vals, key=lambda v: (v > 0, v))),
    )


# --------------------------------------------------------------------------
# distance on a number line
# --------------------------------------------------------------------------

@template("MK")
def distance(rng, lvl):
    if lvl == 1:
        a_ = -rng.randint(2, 15)
        b_ = rng.randint(1, 15)
        if rng.random() < 0.3:
            b_ = -rng.randint(1, 15)
            need(b_ != a_)
        lo_, hi_ = min(a_, b_), max(a_, b_)
        need(hi_ - lo_ >= 3)
        ans = Q(hi_ - lo_)
        wrong = [(-ans, "subtracts in the wrong order; a distance is never negative")]
        if (a_ < 0) != (b_ < 0):
            wrong.append((Q(abs(abs(a_) - abs(b_))), "subtracts the absolute values; the points are on "
                                                     "opposite sides of 0, so the distances add"))
        else:
            wrong.append((Q(abs(a_) + abs(b_)), "adds the absolute values; both points are on the same "
                                                "side of 0, so subtract"))
        x1, x2 = rng.sample([a_, b_], 2)
        return Problem(
            stem=choose(rng, f"What is the distance between {m(_r(x1))} and {m(_r(x2))} on a number line?",
                        f"How many units apart are {m(_r(x1))} and {m(_r(x2))} on a number line?"),
            answer=ans,
            fmt=num,
            wrong=wrong,
            steps=[
                "Distance is the larger number minus the smaller number (or the absolute value of the difference).",
                f"{m(f'{_r(hi_)} - {_p(lo_)} = {_r(hi_)} + {abs(lo_)} = {ans}') if lo_ < 0 else m(f'{_r(hi_)} - {_r(lo_)} = {ans}')}"
                + (f", or count {m(abs(lo_))} units to {m(0)} and {m(hi_)} more." if (lo_ < 0 < hi_) else "."),
            ],
            check=sp.Abs(sp.Integer(a_) - b_),
            neg_ok=True,
            near=_near_int(ans),
        )
    # level 2: the point halfway between two numbers
    p_ = -rng.randint(2, 15)
    q_ = rng.randint(-10, 15)
    need(q_ > p_ + 3 and (p_ + q_) % 2 == 0 and q_ != 0 and p_ + q_ != 0)
    mid = Q(p_ + q_) / 2
    half = Q(q_ - p_) / 2
    x1, x2 = rng.sample([p_, q_], 2)
    return Problem(
        stem=choose(rng, f"What number is halfway between {m(_r(x1))} and {m(_r(x2))} on a number line?",
                    f"On a number line, point {m('M')} is halfway between {m(_r(x1))} and {m(_r(x2))}. "
                    f"What number is at {m('M')}?"),
        answer=mid,
        fmt=num,
        wrong=[(half, "is half the distance between the numbers, not the point halfway between them"),
               (-mid, "has the right size but the wrong sign"),
               (Q(q_ - p_), "is the distance between the numbers"),
               (Q(abs(p_) + abs(q_)) / 2 if (p_ < 0) != (q_ < 0) else Q(abs(p_) - abs(q_)) / 2,
                "ignores the negative sign when averaging")],
        steps=[
            f"The halfway point is the average of the two numbers: "
            f"{m(f'({_r(p_)} + {_p(q_)}) \\div 2')}.",
            f"{m(f'{_r(p_)} + {_p(q_)} = {_r(p_ + q_)}')}, and {m(f'{_r(p_ + q_)} \\div 2 = {_r(mid)}')}.",
            f"Check: {m(_r(mid))} is {m(half)} units from each number.",
        ],
        verify=lambda v: Q(v) - p_ == q_ - Q(v),
        check=sp.Rational(p_ + q_, 2),
        neg_ok=True,
        near=_near_int(mid),
    )


# --------------------------------------------------------------------------
# exponents with negatives, order of operations
# --------------------------------------------------------------------------

@template("MK")
def neg_powers(rng, lvl):
    form = rng.choice(["sq_sq", "cube_sq", "sub", "sub2"])
    if form == "sub2":
        k = rng.randint(2, 9)
        c = rng.randint(2, 15)
        x_, y_ = -k, -c
        ans = Q(-k ** 2 + c)
        X, Y = sp.Integer(x_), sp.Integer(y_)
        return Problem(
            stem=choose(rng, f"What is the value of {m('-x^2 - y')} when {m(f'x = {x_}')} and {m(f'y = {y_}')}?",
                        f"If {m(f'x = {x_}')} and {m(f'y = {y_}')}, what is {m('-x^2 - y')}?"),
            answer=ans,
            fmt=num,
            wrong=[(Q(k ** 2 + c), f"treats {m('-x^2')} as {m('(-x)^2')}, which is positive"),
                   (Q(-k ** 2 - c), f"subtracts {m(c)} instead of subtracting {m(-c)}; subtracting a negative means adding"),
                   (Q(k ** 2 - c), f"makes both mistakes: treats {m('-x^2')} as positive and subtracts {m(c)} "
                                  f"instead of adding it"),
                   (Q(2 * k + c), f"multiplies {m('x')} by 2 instead of squaring it: {m(f'-2({x_}) = {2 * k}')}")],
            steps=[f"Substitute, keeping negatives in parentheses: {m(f'-({x_})^2 - ({y_})')}.",
                   f"Square first: {m(f'({x_})^2 = {k ** 2}')}, so {m(f'-({x_})^2 = {-k ** 2}')}.",
                   f"Subtracting {m(y_)} means adding {m(c)}: {m(f'{-k ** 2} + {c} = {_r(ans)}')}."],
            check=-X ** 2 - Y,
            neg_ok=True,
            near=_near_int(ans, (1, 2, 4, 8)),
        )
    if form == "sq_sq":
        a_, b_ = rng.sample(range(2, 13), 2)
        disp = f"-{a_}^2 + ({-b_})^2"
        ans = Q(-a_ ** 2 + b_ ** 2)
        wrong = [(Q(a_ ** 2 + b_ ** 2), f"treats {m(f'-{a_}^2')} as {m(f'(-{a_})^2')}"),
                 (Q(-a_ ** 2 - b_ ** 2), f"treats {m(f'(-{b_})^2')} as {m(f'-{b_}^2')}"),
                 (Q(-2 * a_ - 2 * b_), "multiplies by 2 instead of squaring")]
        steps = [
            f"In {m(f'-{a_}^2')} the exponent applies only to {m(a_)}: "
            f"{m(f'-{a_}^2 = -({a_} \\times {a_}) = {-a_ ** 2}')}.",
            f"In {m(f'(-{b_})^2')} the parentheses include the sign: "
            f"{m(f'(-{b_})(-{b_}) = {b_ ** 2}')}.",
            f"Add: {m(f'{-a_ ** 2} + {b_ ** 2} = {_r(ans)}')}.",
        ]
        chk = -sp.Integer(a_) ** 2 + sp.Integer(-b_) ** 2
    elif form == "cube_sq":
        a_ = rng.randint(2, 5)
        b_ = rng.randint(2, 10)
        disp = f"(-{a_})^3 - (-{b_})^2"
        ans = Q((-a_) ** 3 - b_ ** 2)
        wrong = [(Q(a_ ** 3 - b_ ** 2), f"thinks {m(f'(-{a_})^3')} is positive; an odd power of a negative is negative"),
                 (Q((-a_) ** 3 + b_ ** 2), f"treats {m(f'(-{b_})^2')} as {m(f'-{b_ ** 2}')}"),
                 (Q(-3 * a_ + 2 * b_), f"multiplies by the exponents instead of using them as powers: "
                                       f"{m(rf'(-{a_}) \times 3 - (-{b_}) \times 2 = {-3 * a_ + 2 * b_}')}")]
        steps = [
            f"{m(f'(-{a_})^3 = (-{a_})(-{a_})(-{a_}) = {(-a_) ** 3}')}: three negative factors give a negative.",
            f"{m(f'(-{b_})^2 = (-{b_})(-{b_}) = {b_ ** 2}')}: two negative factors give a positive.",
            f"Subtract: {m(f'{(-a_) ** 3} - {b_ ** 2} = {_r(ans)}')}.",
        ]
        chk = sp.Integer(-a_) ** 3 - sp.Integer(-b_) ** 2
    else:
        k = rng.randint(2, 9)
        c = rng.randint(2, 9)
        need(k != c)
        disp = f"-x^2 + {c}x"
        x_ = -k
        ans = Q(-k ** 2 + c * x_)
        wrong = [(Q(k ** 2 + c * x_), f"squares {m(f'-{k}')} correctly but drops the minus sign in front of {m('x^2')}"),
                 (Q(-k ** 2 - c * x_), f"gets the sign of {m(f'{c}({x_})')} wrong"),
                 (Q(k ** 2 - c * x_), "makes both terms positive"),
                 (Q(2 * k + c * x_), f"multiplies {m('x')} by 2 instead of squaring it: {m(f'-2({x_}) = {2 * k}')}")]
        steps = [
            f"Substitute {m(x_)} for {m('x')}, keeping it in parentheses: {m(f'-({x_})^2 + {c}({x_})')}.",
            f"Square first: {m(f'({x_})^2 = {k ** 2}')}, so {m(f'-({x_})^2 = {-k ** 2}')}.",
            f"Multiply: {m(f'{c}({x_}) = {c * x_}')}.",
            f"Add: {m(f'{-k ** 2} + ({c * x_}) = {_r(ans)}')}.",
        ]
        X = sp.Integer(x_)
        chk = -X ** 2 + c * X
        return Problem(
            stem=f"What is the value of {m(disp)} when {m(f'x = {x_}')}?",
            answer=ans, fmt=num, wrong=wrong, steps=steps, check=chk, neg_ok=True,
            near=_near_int(ans, (1, 2, 4, 8)),
        )
    return Problem(
        stem=choose(rng, f"What is the value of {m(disp)}?", f"Evaluate: {m(disp)}", f"Simplify: {m(disp)}"),
        answer=ans, fmt=num, wrong=wrong, steps=steps, check=chk, neg_ok=True,
        near=_near_int(ans, (1, 2, 4, 8)),
    )


@template("MK")
def mixed_ops(rng, lvl):
    form = rng.choice(["div_minus_prod", "prod_paren_plus_div", "paren_prod_minus"])
    if form == "div_minus_prod":
        d = rng.randint(2, 6)
        q = -rng.randint(2, 9)
        a_ = q * d
        b_, c_ = -rng.randint(2, 6), rng.choice([-1, 1]) * rng.randint(2, 6)
        prod = b_ * c_
        ans = Q(q - prod)
        disp = rf"{_r(a_)} \div {d} - {_p(b_)} \times {_p(c_)}"
        wrong = [(Q(q + prod), f"gets the sign of {m(rf'{_p(b_)} \times {_p(c_)}')} wrong"),
                 (Q((q - b_) * c_), "works from left to right instead of multiplying before subtracting"),
                 (-ans, "has the right size but the wrong sign")]
        steps = [
            f"Divide first: {m(rf'{_r(a_)} \div {d} = {q}')} (different signs, negative).",
            f"Multiply: {m(rf'{_p(b_)} \times {_p(c_)} = {_r(prod)}')} "
            f"({'same signs, positive' if (b_ < 0) == (c_ < 0) else 'different signs, negative'}).",
            f"Subtract: {m(f'{q} - {_p(prod)} = {_r(ans)}')}"
            + (f" (subtracting a negative means adding {abs(prod)})." if prod < 0 else "."),
        ]
        chk = sp.Rational(a_, d) - sp.Integer(b_) * c_
    elif form == "prod_paren_plus_div":
        k = -rng.randint(2, 6)
        u, w = rng.randint(1, 6), rng.randint(7, 15)
        inner = u - w
        d = rng.choice([-1, 1]) * rng.randint(2, 5)
        q = rng.choice([-1, 1]) * rng.randint(2, 8)
        top = q * d
        need(top < 0 or d < 0)
        ans = Q(k * inner + q)
        disp = rf"{_r(k)} \times ({u} - {w}) + {_p(top)} \div {_p(d)}"
        wrong = [(Q(-k * inner + q), f"gets the sign of {m(rf'{_r(k)} \times {_p(inner)}')} wrong"),
                 (Q(k * inner - q), f"gets the sign of {m(rf'{_p(top)} \div {_p(d)}')} wrong"),
                 ((Q(k * inner + top) / d, f"adds {m(k * inner)} and {m(_p(top))} before dividing by {m(_p(d))}")
                  if (k * inner + top) % d == 0 else
                  (Q(k * inner + top), f"forgets to divide {m(_p(top))} by {m(_p(d))}"))]
        steps = [
            f"Parentheses first: {m(f'{u} - {w} = {inner}')}.",
            f"Multiply: {m(rf'{_r(k)} \times {_p(inner)} = {k * inner}')} (same signs, positive).",
            f"Divide: {m(rf'{_p(top)} \div {_p(d)} = {_r(q)}')} "
            f"({'same signs, positive' if (top < 0) == (d < 0) else 'different signs, negative'}).",
            f"Add: {m(f'{k * inner} + {_p(q)} = {_r(ans)}')}.",
        ]
        chk = sp.Integer(k) * (u - w) + sp.Rational(top, d)
    else:
        a_, b_ = rng.randint(-9, 4), rng.randint(5, 12)
        c_ = -rng.randint(2, 6)
        e_ = rng.choice([-1, 1]) * rng.randint(2, 15)
        inner = a_ - b_
        ans = Q(inner * c_ - e_)
        disp = rf"({_r(a_)} - {b_}) \times {_p(c_)} - {_p(e_)}"
        wrong = [(Q(-inner * c_ - e_), f"gets the sign of {m(rf'{_p(inner)} \times {_p(c_)}')} wrong"),
                 (Q(inner * c_ + e_), f"subtracts {m(abs(e_))} instead of adding it; subtracting a negative means adding"
                  if e_ < 0 else f"adds {m(e_)} instead of subtracting it"),
                 (Q(inner * (c_ - e_)), "subtracts before multiplying")]
        steps = [
            f"Parentheses first: {m(f'{_r(a_)} - {b_} = {inner}')}.",
            f"Multiply: {m(rf'{_p(inner)} \times {_p(c_)} = {inner * c_}')} (same signs, positive).",
            f"Subtract: {m(f'{inner * c_} - {_p(e_)} = {_r(ans)}')}"
            + (f" (subtracting a negative means adding {abs(e_)})." if e_ < 0 else "."),
        ]
        chk = (sp.Integer(a_) - b_) * c_ - sp.Integer(e_)
    need(abs(ans) <= 120)
    return Problem(
        stem=choose(rng, f"What is the value of {m(disp)}?", f"Evaluate: {m(disp)}"),
        answer=ans,
        fmt=num,
        wrong=wrong,
        steps=steps,
        check=chk,
        neg_ok=True,
        near=_near_int(ans, (1, 2, 4, 10)),
    )


# --------------------------------------------------------------------------
# word problems
# --------------------------------------------------------------------------

_PLACES_COLD = ["a town in northern Minnesota", "a ski resort", "a cold-weather training site in Alaska",
                "a farm in North Dakota", "a mountain base camp", "an Army post in upstate New York"]


@template("AR")
def temperature(rng, lvl):
    place = rng.choice(_PLACES_COLD)
    t1, t2 = rng.choice([("6 a.m.", "noon"), ("midnight", "9 a.m."), ("5 a.m.", "2 p.m."),
                         ("sunrise", "early afternoon")])
    if lvl == 1:
        if rng.random() < 0.5:
            start = -rng.randint(3, 18)
            rise = rng.randint(5, 25)
            end = start + rise
            need(end != 0 and end != -start)
            stem = (f"At {t1} the temperature at {place} was {_deg(start)}. By {t2} it had risen "
                    f"{m(rise)} degrees. What was the temperature at {t2}?")
            chk = sp.Integer(start) + rise
            wrong = [(Q(start - rise), "subtracts the rise instead of adding it"),
                     (Q(-end), "has the right size but the wrong sign"),
                     (Q(abs(start) + rise), "ignores the negative sign on the starting temperature")]
            steps = [f"A rise means add: {m(f'{_r(start)} + {rise}')}.",
                     _add_two(start, rise) + f" The temperature was {_deg(end)}."]
        else:
            start = rng.randint(2, 15)
            drop = rng.randint(start + 2, start + 20)
            end = start - drop
            t0 = rng.choice(["4 p.m.", "sunset", "6 p.m.", "noon"])
            stem = (f"At {t0} the temperature at {place} was {_deg(start)}. By midnight it had "
                    f"dropped {m(drop)} degrees. What was the temperature at midnight?")
            chk = sp.Integer(start) - drop
            wrong = [(Q(start + drop), "adds the drop instead of subtracting it"),
                     (Q(-end), "subtracts the smaller number from the larger and drops the negative sign"),
                     (Q(-(start + drop)), None)]
            steps = [f"A drop means subtract: {m(f'{start} - {drop}')}.",
                     f"{m(f'{start} - {drop} = {start} + ({-drop})')}. " + _add_two(start, -drop)
                     + f" The temperature was {_deg(end)}."]
        return Problem(stem=stem, answer=Q(end), fmt=_deg, wrong=wrong, steps=steps, check=chk,
                       neg_ok=True, near=_near_int(end, (1, 2, 3, 5)))
    # level 2: the change between two readings, or a steady drop over several hours
    if rng.random() < 0.5:
        low = -rng.randint(3, 20)
        high = rng.randint(2, 25)
        rise = high - low
        stem = (f"At {t1} the temperature at {place} was {_deg(low)}. At {t2} it was {_deg(high)}. "
                "By how many degrees did the temperature rise?")
        return Problem(
            stem=stem,
            answer=Q(rise),
            fmt=unit(num, "degree"),
            wrong=[(Q(high - abs(low)) if high != abs(low) else Q(rise + 2),
                    "subtracts the numbers as if both were positive"),
                   (Q(-rise), "subtracts in the wrong order"),
                   (Q(high), f"measures only from {m(0)} up to the final temperature")],
            steps=[
                f"Change {m('=')} final {m('-')} starting: {m(f'{high} - ({_r(low)})')}.",
                f"Subtracting a negative means adding: {m(f'{high} + {abs(low)} = {rise}')} degrees.",
            ],
            tip=f"On a number line: {m(abs(low))} degrees up to {m(0)}, then {m(high)} more.",
            check=sp.Integer(high) - low,
            neg_ok=True,
            near=_near_int(rise),
        )
    start = rng.randint(-5, 12)
    per = rng.randint(2, 5)
    hours = rng.randint(3, 8)
    end = start - per * hours
    need(end < 0 and end != -start)
    stem = (f"At 6 p.m. the temperature at {place} was {_deg(start)}. It then fell {m(per)} degrees "
            f"every hour for {m(hours)} hours. What was the temperature at the end of that time?")
    return Problem(
        stem=stem,
        answer=Q(end),
        fmt=_deg,
        wrong=[(Q(start + per * hours), "adds the drop instead of subtracting it"),
               (Q(start - per - hours) if start - per - hours != end else Q(end + 1),
                "subtracts the degrees and the hours separately instead of multiplying them"),
               (Q(-end), "has the right size but the wrong sign"),
               (Q(-per * hours), "forgets the starting temperature")],
        steps=[
            f"Total drop: {m(rf'{per} \times {hours} = {per * hours}')} degrees.",
            f"Subtract it from the starting temperature: {m(f'{_r(start)} - {per * hours} = {_r(end)}')}.",
            f"The temperature was {_deg(end)}.",
        ],
        check=sp.Integer(start) + sum([-per] * hours),
        neg_ok=True,
        near=_near_int(end, (1, 2, 3, 5)),
    )


@template("AR")
def elevation(rng, lvl):
    if lvl == 2:
        kind = rng.choice(["dive", "heli", "land"])
        if kind == "dive":
            p = person(rng)
            s0 = rng.randint(2, 9) * 5
            down = rng.randint(2, 8) * 5
            up = rng.randint(1, 6) * 5
            need(up != down)
            end = -s0 - down + up
            need(end < 0)
            return Problem(
                stem=(f"{p.name} is scuba diving {m(s0)} feet below the surface, a position of "
                      f"{m(f'{-s0}')} feet. {p.He} swims down {m(down)} more feet and then rises "
                      f"{m(up)} feet. What is {p.his} new position?"),
                answer=Q(end),
                fmt=_ft,
                wrong=[(Q(-s0 - down - up), "treats the rise as going farther down"),
                       (Q(-s0 + down + up), "treats the descent as a rise"),
                       (Q(-end), "drops the negative sign; the diver is still below the surface")],
                steps=[
                    f"Going down is negative and going up is positive: {m(f'{-s0} - {down} + {up}')}.",
                    f"{m(f'{-s0} - {down} = {-s0 - down}')}, then {m(f'{-s0 - down} + {up} = {end}')}.",
                    f"The new position is {m(end)} feet, that is, {m(-end)} feet below the surface.",
                ],
                check=sp.Integer(-s0) - down + up,
                neg_ok=True,
                near=_near_int(end, (5, 10, 15)),
            )
        if kind == "heli":
            h = rng.randint(4, 30) * 50
            d = rng.randint(2, 12) * 50
            return Problem(
                stem=(f"A Navy helicopter hovers at an altitude of {num(h)} feet. Directly below it, a "
                      f"submarine is at {num(-d)} feet (below sea level). What is the vertical "
                      "distance between the helicopter and the submarine?"),
                answer=Q(h + d),
                fmt=_ft,
                wrong=[(Q(h - d), "subtracts the depth instead of adding it"),
                       (Q(-(h + d)), "subtracts in the wrong order; a distance is never negative"),
                       (Q(h), "measures only down to sea level")],
                steps=[
                    f"Distance {m('=')} higher position {m('-')} lower position: {m(f'{int_raw(h)} - ({int_raw(-d)})')}.",
                    f"Subtracting a negative means adding: {m(f'{int_raw(h)} + {int_raw(d)} = {int_raw(h + d)}')} feet.",
                ],
                tip=f"Sea level is {m(0)}: {num(h)} feet above it plus {num(d)} feet below it.",
                check=abs(sp.Integer(h) - (-d)),
                neg_ok=True,
                near=_near_int(h + d, (50, 100, 200)),
            )
        hi_ = rng.randint(10, 60) * 50
        lo_ = rng.randint(2, 30) * 10
        place = rng.choice([("mountain town", "desert valley"), ("ridge on a training range", "dry lake bed"),
                            ("lookout tower base", "nearby salt flat")])
        return Problem(
            stem=(f"The elevation of a {place[0]} is {num(hi_)} feet. The elevation of a {place[1]} is "
                  f"{num(-lo_)} feet (below sea level). How much higher is the {place[0]} than the "
                  f"{place[1]}?"),
            answer=Q(hi_ + lo_),
            fmt=_ft,
            wrong=[(Q(hi_ - lo_), "subtracts the depth instead of adding it"),
                   (Q(-(hi_ + lo_)), "subtracts in the wrong order"),
                   (Q(hi_), "measures only down to sea level")],
            steps=[
                f"Difference {m('=')} higher {m('-')} lower: {m(f'{int_raw(hi_)} - ({int_raw(-lo_)})')}.",
                f"Subtracting a negative means adding: {m(f'{int_raw(hi_)} + {lo_} = {int_raw(hi_ + lo_)}')} feet.",
            ],
            check=sp.Integer(hi_) - (-lo_),
            neg_ok=True,
            near=_near_int(hi_ + lo_, (10, 50, 100)),
        )
    # level 3: rate of rise over time, then a dive
    d0 = rng.randint(8, 30) * 50
    rate = rng.choice([20, 25, 30, 40, 50, 60])
    mins = rng.randint(3, 9)
    dive = rng.randint(2, 9) * 50
    end = -d0 + rate * mins - dive
    need(end < 0 and rate * mins < d0 and rate * mins != dive)
    return Problem(
        stem=(f"A submarine is at {num(-d0)} feet (below sea level). It rises {m(rate)} feet per "
              f"minute for {m(mins)} minutes and then dives {m(dive)} feet. What is its new "
              "position?"),
        answer=Q(end),
        fmt=_ft,
        wrong=[(Q(-d0 - rate * mins - dive), "treats the rise as going down"),
               (Q(-d0 + rate * mins + dive), "treats the dive as a rise"),
               (Q(-d0 + rate - dive), "forgets to multiply the rate by the number of minutes"),
               (Q(-end), "drops the negative sign; the submarine is still below sea level")],
        steps=[
            f"The rise: {m(rf'{rate} \times {mins} = {rate * mins}')} feet up.",
            f"After rising: {m(f'{int_raw(-d0)} + {rate * mins} = {int_raw(-d0 + rate * mins)}')} feet.",
            f"After diving: {m(f'{int_raw(-d0 + rate * mins)} - {dive} = {int_raw(end)}')} feet.",
        ],
        check=sp.Integer(-d0) + sum([rate] * mins) - dive,
        neg_ok=True,
        near=_near_int(end, (50, 100, 150)),
    )


_BILLS = [("a phone bill", 45, 95), ("car insurance", 90, 180), ("groceries", 40, 150),
          ("gas", 30, 70), ("a gym membership", 25, 60), ("a utility bill", 60, 150),
          ("a concert ticket", 40, 120), ("a textbook", 60, 180), ("a car repair", 120, 400)]


@template("AR")
def bank_balance(rng, lvl):
    if rng.random() < 0.6:
        pr = person(rng)
        who, he = pr.name, pr.He
    else:
        who = soldier(rng)
        he = "The " + who.rsplit(" ", 1)[0].lower()
    (w1, l1, h1), (w2, l2, h2) = rng.sample(_BILLS, 2)
    c1 = rng.randint(l1, h1)
    c2 = rng.randint(l2, h2)
    bal = rng.randint(4, 40) * 5
    fee = rng.choice([25, 30, 34, 35])
    after = bal - c1 - c2
    need(after < 0 and bal - c1 > 0 and after > -150)
    final = after - fee
    setup = (f"{who} has {_signed_money(bal)} in a checking account. {he} pays {_signed_money(c1)} for "
             f"{w1} and {_signed_money(c2)} for {w2}. Because the balance went below "
             f"{_signed_money(0)}, the bank also charges a {_signed_money(fee)} overdraft fee.")
    if lvl == 2:
        return Problem(
            stem=setup + " What is the account balance now?",
            answer=Q(final),
            fmt=_signed_money,
            wrong=[(Q(after), "forgets the overdraft fee"),
                   (Q(-final), "drops the negative sign; the account is overdrawn"),
                   (Q(after + fee), "adds the fee instead of subtracting it"),
                   (Q(-bal - c1 - c2 - fee), "treats the starting balance as money owed instead of money in the account")],
            steps=[
                f"Start with {_signed_money(bal)} and subtract both payments: "
                f"{m(f'{bal} - {c1} - {c2} = {_r(after)}')}.",
                f"Subtract the fee: {m(f'{_r(after)} - {fee} = {_r(final)}')}.",
                f"The balance is {_signed_money(final)}: the account is overdrawn by {_signed_money(-final)}.",
            ],
            check=sp.Integer(bal) - (c1 + c2 + fee),
            neg_ok=True,
            near=_near_int(final, (5, 10, 20)),
        )
    target = rng.choice([0, 25, 50, 100])
    dep = target - final
    goal = f"bring the balance back up to {_signed_money(target)}"
    wrong = [(Q(target - after), "forgets the overdraft fee"),
             (Q(dep + fee), "subtracts the fee twice")]
    if target:
        need(target != -final)
        wrong += [(Q(abs(target + final)), f"subtracts {m(min(target, -final))} from {m(max(target, -final))} "
                                           "instead of adding the two amounts"),
                  (Q(-final), f"only brings the balance back up to {_signed_money(0)}")]
    return Problem(
        stem=setup + f" How much must {who} deposit to {goal}?",
        answer=Q(dep),
        fmt=_signed_money,
        wrong=wrong,
        steps=[
            f"Balance after the payments and the fee: {m(f'{bal} - {c1} - {c2} - {fee} = {_r(final)}')}.",
            f"Deposit needed {m('=')} target {m('-')} balance: "
            f"{m(f'{target} - ({_r(final)}) = {target} + {-final} = {dep}')}.",
            f"{who} must deposit {_signed_money(dep)}.",
        ],
        check=sp.Integer(target) - (sp.Integer(bal) - c1 - c2 - fee),
        verify=lambda v: final + Q(v) == target,
        near=_near_int(dep, (5, 10, 20)),
    )


PLAN = [
    # (template, level, count)  -- easy -> hard; 25 problems
    (add_sub, 1, 2),
    (mult_div, 1, 2),
    (abs_value, 1, 1),
    (distance, 1, 1),
    (order_ints, 1, 1),
    (temperature, 1, 1),
    (add_sub, 2, 2),
    (mult_div, 2, 1),
    (abs_value, 2, 1),
    (order_ints, 2, 1),
    (distance, 2, 1),
    (temperature, 2, 1),
    (elevation, 2, 2),
    (bank_balance, 2, 1),
    (neg_powers, 3, 2),
    (mixed_ops, 3, 2),
    (abs_value, 3, 1),
    (elevation, 3, 1),
    (bank_balance, 3, 1),
]
