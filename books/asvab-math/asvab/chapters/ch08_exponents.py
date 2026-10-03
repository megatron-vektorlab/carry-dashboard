"""Chapter 8 - Exponents & Scientific Notation."""
import re
from fractions import Fraction
from math import gcd

import sympy as sp

from ..core import (R, Q, Problem, need, num, dec, frac, mixed, m, F, tx, dec_raw,
                    int_raw, frac_raw, mixed_raw, choose, template)

NUM = 8
TITLE = r"Exponents \& Scientific Notation"
PART = 1

INTRO = r"""
An \emph{exponent} is shorthand for repeated multiplication:
$2^5 = 2 \times 2 \times 2 \times 2 \times 2 = 32$. \emph{Scientific
notation} uses powers of $10$ to write very large and very small numbers
compactly. Both show up on the test as quick one-step questions.

\begin{concept}{Powers, signs, and special exponents}
\begin{itemize}
\item $b^n$ means $n$ factors of $b$: $3^4 = 3 \times 3 \times 3 \times 3 = 81$.
\item The exponent applies only to what it touches: $(-3)^2 = 9$, but
  $-3^2 = -(3^2) = -9$. An even power of a negative number is positive; an
  odd power is negative.
\item Zero exponent: $b^0 = 1$ (for any $b \ne 0$).
  Negative exponent = reciprocal: $2^{-3} = \frac{1}{2^3} = \frac{1}{8}$,
  and $\left(\frac{2}{3}\right)^{-2} = \left(\frac{3}{2}\right)^{2} = \frac{9}{4}$.
\end{itemize}
\end{concept}

\begin{concept}{Rules for the same base}
\begin{center}
\begin{tabular}{lll}
Multiply: add exponents & $a^m \cdot a^n = a^{m+n}$ & $2^3 \cdot 2^4 = 2^7$\\
Divide: subtract exponents & $\frac{a^m}{a^n} = a^{m-n}$ & $\frac{5^9}{5^3} = 5^6$\\
Power of a power: multiply & $(a^m)^n = a^{mn}$ & $(3^2)^4 = 3^8$\\
Power of a fraction & $\left(\frac{p}{q}\right)^n = \frac{p^n}{q^n}$ & $\left(\frac{2}{3}\right)^3 = \frac{8}{27}$
\end{tabular}
\end{center}
\end{concept}

\begin{concept}{Scientific notation}
A number is in scientific notation when it is written as
$m \times 10^k$ with $1 \le m < 10$. A positive $k$ makes a big number (move
the decimal point $k$ places right); a negative $k$ makes a small number
(move it left): $4.5 \times 10^4 = 45{,}000$ and
$3.6 \times 10^{-3} = 0.0036$.
\end{concept}

\begin{example}{Worked example}
Write $(3 \times 10^4)(4 \times 10^5)$ in scientific notation.

\textbf{Solution.} Multiply the first factors and add the exponents:
$3 \times 4 = 12$ and $10^4 \times 10^5 = 10^9$, giving $12 \times 10^9$.
But $12$ is not between $1$ and $10$: $12 = 1.2 \times 10^1$, so the answer is
$1.2 \times 10^{10}$.
\end{example}

\begin{tip}
Count the jumps. To write $0.0052$ in scientific notation, the decimal
point jumps $3$ places right to make $5.2$, so the exponent is $-3$:
$5.2 \times 10^{-3}$. For $52{,}000$ it jumps $4$ places left to make $5.2$,
so the exponent is $+4$. Small numbers get negative exponents; big numbers
get positive ones.
\end{tip}

\begin{trap}
\begin{itemize}
\item Multiplying the base by the exponent: $3^4$ is $81$, not $12$.
\item Thinking a negative exponent makes a negative number: $2^{-3} = \frac18$, not $-8$.
\item Multiplying exponents when you should add them: $2^3 \cdot 2^4 = 2^7$, not $2^{12}$.
\item Leaving $12 \times 10^9$ unadjusted: the first factor must be less than $10$.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# private helpers
# --------------------------------------------------------------------------

def _pw(b, e) -> str:
    """Raw LaTeX power with parentheses for negative or fractional bases."""
    b = Q(b)
    if b.is_integer and b >= 0:
        base = int_raw(b)
    elif b.is_integer:
        base = f"({int_raw(b)})"
    else:
        base = rf"\left({frac_raw(b)}\right)"
    return f"{base}^{{{e}}}"


def _mant_exp(v):
    """Positive rational -> (mantissa, exponent) with 1 <= mantissa < 10."""
    v = sp.Rational(Q(v))
    need(v > 0)
    k = 0
    while v >= 10:
        v /= 10
        k += 1
    while v < 1:
        v *= 10
        k -= 1
    return v, k


def _sci_raw(mant, k) -> str:
    return rf"{dec_raw(mant, max_places=3)} \times 10^{{{k}}}"


def _sci(v) -> str:
    """Formatter: value -> $m \\times 10^{k}$ (proper scientific notation)."""
    mant, k = _mant_exp(v)
    return m(_sci_raw(mant, k))


def _parse_sci(s: str):
    """'$4.5 \\times 10^{4}$' -> (Rational mantissa, int exponent)."""
    mt = re.fullmatch(r"\$([\d.{},]+) \\times 10\^\{(-?\d+)\}\$", s)
    if not mt:
        raise ValueError(s)
    mant = sp.Rational(mt.group(1).replace("{,}", ""))
    return mant, int(mt.group(2))


def _power_of(base, value):
    """Exponent k with base**k == value, found by counting (independent check)."""
    k, v = 0, Fraction(1)
    target = Fraction(value)
    if target >= 1:
        while v < target:
            v *= base
            k += 1
    else:
        while v > target:
            v /= base
            k -= 1
    if v != target:
        raise ValueError("not a power")
    return k


def _times(b, e) -> str:
    """'3 \\times 3 \\times 3 \\times 3' (raw)."""
    return r" \times ".join([int_raw(b)] * e)


def _build_up(b, e) -> str:
    """'3 \\times 3 = 9, 9 \\times 3 = 27, ...' running products (raw pieces)."""
    out, v = [], b
    for _ in range(e - 1):
        out.append(f"{int_raw(v)} \\times {int_raw(b)} = {int_raw(v * b)}")
        v *= b
    return ", ".join(m(t) for t in out)


# --------------------------------------------------------------------------
# templates
# --------------------------------------------------------------------------

def _neg_term(b, e, form):
    """A power of a negative number: (form, tex, value, explanation)."""
    if form == "paren":
        val = Q(-b) ** e
        rule = ("an even number of negative factors gives a positive result" if e % 2 == 0
                else "an odd number of negative factors gives a negative result")
        return _pw(-b, e), val, f"{m(f'{_pw(-b, e)} = {int_raw(val)}')} ({rule})"
    val = -Q(b) ** e
    return (f"-{_pw(b, e)}", val,
            f"{m(f'-{_pw(b, e)} = -({_pw(b, e)}) = {int_raw(val)}')} (no parentheses, so only the {b} is raised to the power)")


@template("MK")
def evaluate_power(rng, lvl):
    if lvl == 1 and rng.random() < 0.5:
        b = rng.randint(2, 10)
        e = rng.randint(2, 6 if b == 10 else 5)
        need(b ** e <= 1000 or b == 10)
        need(not (b == 2 and e == 2))
        ans = Q(b) ** e
        wrong = [
            (Q(b * e), f"multiplies the base by the exponent ({m(f'{b} \\times {e}')})"),
            (Q(e) ** b, "switches the base and the exponent") if e ** b <= 10 ** 6 else (Q(b) ** (e + 1), None),
            (Q(b) ** (e - 1), f"uses only {e - 1} factors of {b}"),
            (Q(b) ** (e + 1), f"uses {e + 1} factors of {b} instead of {e}"),
        ]
        if b == 10:
            steps = [f"A power of 10 is 1 followed by as many zeros as the exponent: {m(_pw(10, e))} has {e} zeros.",
                     f"{m(f'{_pw(10, e)} = {int_raw(ans)}')}."]
        else:
            steps = [f"The exponent tells how many times to use the base as a factor: "
                     f"{m(f'{_pw(b, e)} = {_times(b, e)}')}.",
                     f"Multiply step by step: {_build_up(b, e)}."]
        return Problem(
            stem=choose(rng, f"What is the value of {m(_pw(b, e))}?", f"Evaluate {m(_pw(b, e))}.",
                        f"Which of the following is equal to {m(_pw(b, e))}?"),
            answer=ans,
            fmt=num,
            wrong=wrong,
            steps=steps,
            check=sp.prod([b] * e),
        )

    if lvl == 1:
        # two powers combined: evaluate the powers first
        b1, b2 = rng.sample(range(2, 7), 2)
        e1, e2 = rng.randint(2, 3), rng.randint(2, 3)
        op = rng.choice(["+", "-", "x"])
        v1, v2 = b1 ** e1, b2 ** e2
        if op == "x":
            need(e1 != e2 and v1 * v2 <= 1000)
        f = {"+": lambda s, t: s + t, "-": lambda s, t: s - t, "x": lambda s, t: s * t}[op]
        ans = Q(f(v1, v2))
        need(ans > 0)
        sym = r"\times" if op == "x" else op
        tex = f"{_pw(b1, e1)} {sym} {_pw(b2, e2)}"
        wrong = [
            (Q(f(b1 * e1, b2 * e2)), "multiplies each base by its exponent"),
            (Q(f(e1 ** b1, e2 ** b2)), "switches the bases and the exponents"),
        ]
        if op != "x" and e1 == e2:
            wrong.append((Q(f(b1, b2)) ** e1, f"combines the bases first; the powers must be found before you {'add' if op == '+' else 'subtract'}"))
        if op == "x":
            wrong.append((Q(b1 * b2) ** (e1 + e2), "multiplies the bases and adds the exponents, but the bases are different"))
        wrong.append((Q(f(v1, b2 * e2)), f"evaluates {m(_pw(b1, e1))} correctly but multiplies {b2} by {e2}"))
        return Problem(
            stem=choose(rng, f"What is the value of {m(tex)}?", f"Evaluate {m(tex)}."),
            answer=ans,
            fmt=num,
            wrong=wrong,
            steps=[
                "Exponents come before multiplying, adding, or subtracting, so find each power first.",
                f"{m(f'{_pw(b1, e1)} = {_times(b1, e1)} = {v1}')} and {m(f'{_pw(b2, e2)} = {_times(b2, e2)} = {v2}')}.",
                f"Then {m(f'{v1} {sym} {v2} = {int_raw(ans)}')}.",
            ],
            check=sp.sympify(f"{b1}**{e1} {'*' if op == 'x' else op} {b2}**{e2}"),
        )

    # level 2: negative bases, with and without parentheses
    if rng.random() < 0.5:
        b = rng.randint(2, 6)
        form = rng.choice(["paren", "paren", "bare"])
        e = rng.choice([2, 4] if form == "bare" else [2, 3, 4, 5])
        need(b ** e <= 1300)
        pos = b ** e
        if form == "paren":
            ans = Q(-b) ** e
            tex = _pw(-b, e)
            sign_rule = ("an even number of negative factors gives a positive product" if e % 2 == 0
                         else "an odd number of negative factors gives a negative product")
            steps = [
                f"The parentheses make {m(int_raw(-b))} the base: {m(f'{tex} = ' + r' \times '.join([f'({-b})'] * e))}.",
                f"Count the negative signs: there are {e}, and {sign_rule}.",
                f"Since {m(f'{_pw(b, e)} = {int_raw(pos)}')}, the answer is {m(int_raw(ans))}.",
            ]
            wrong = [
                (-ans, "gets the sign wrong: " + sign_rule),
                (Q(-b * e), "multiplies the base by the exponent"),
                (Q(b * e) if e % 2 == 0 else Q(-b) ** (e - 1), None),
                (Q(-b) ** (e + 1), f"uses {e + 1} factors instead of {e}"),
            ]
        else:
            ans = Q(-pos)
            tex = f"-{_pw(b, e)}"
            steps = [
                f"There are no parentheses, so the exponent applies only to {m(b)}, not to the negative sign: "
                f"{m(f'{tex} = -({_pw(b, e)})')}.",
                f"{m(f'{_pw(b, e)} = {_times(b, e)} = {int_raw(pos)}')}, so the answer is {m(int_raw(ans))}.",
            ]
            wrong = [
                (Q(pos), f"treats {m(tex)} as {m(_pw(-b, e))}; without parentheses only the {b} is raised to the power"),
                (Q(-b * e), "multiplies the base by the exponent"),
                (Q(b * e), "multiplies the base by the exponent and drops the negative sign"),
                (Q(-b) ** (e - 1) if e > 2 else Q(-b) * 3, None),
            ]
        return Problem(
            stem=choose(rng, f"What is the value of {m(tex)}?", f"Evaluate {m(tex)}.",
                        f"{m(tex)} is equal to which of the following?"),
            answer=ans,
            fmt=num,
            neg_ok=True,
            wrong=wrong,
            steps=steps,
            check=sp.Integer(-1) ** (e if form == "paren" else 1) * sp.prod([b] * e),
        )

    # level 2, second form: a signed power combined with a positive power
    b, c = rng.randint(2, 5), rng.randint(2, 5)
    form = rng.choice(["paren", "paren", "bare"])
    e = rng.choice([2, 4] if form == "bare" else [2, 3])
    f_ = rng.choice([2, 3])
    need(b ** e <= 100 and c ** f_ <= 64)
    t1, v1, expl = _neg_term(b, e, form)
    v2 = Q(c) ** f_
    op = rng.choice(["+", "-"])
    comb = (lambda s, t: s + t) if op == "+" else (lambda s, t: s - t)
    ans = comb(v1, v2)
    tex = f"{t1} {op} {_pw(c, f_)}"
    if form == "paren":
        slip = (comb(-v1, v2), f"gets the sign of {m(t1)} wrong")
    else:
        slip = (comb(-v1, v2), f"treats {m(t1)} as {m(_pw(-b, e))}")
    wrong = [
        slip,
        (comb(Q(-b * e), Q(c * f_)), "multiplies each base by its exponent"),
        (comb(v1, -v2) if op == "+" else comb(v1, -v2), f"{'subtracts' if op == '+' else 'adds'} {m(_pw(c, f_))} instead"),
        (comb(-v1, -v2), None),
    ]
    return Problem(
        stem=choose(rng, f"What is the value of {m(tex)}?", f"Evaluate {m(tex)}."),
        answer=ans,
        fmt=num,
        neg_ok=True,
        wrong=wrong,
        steps=[
            f"Find each power first. {expl[0].upper() + expl[1:]}.",
            f"{m(f'{_pw(c, f_)} = {int_raw(v2)}')}.",
            f"Combine: {m(f'{int_raw(v1)} {op} {int_raw(v2)} = {int_raw(ans)}'.replace('+ -', '- ').replace('- -', '+ '))}.",
        ],
        check=sp.sympify(f"{'(-' + str(b) + ')**' + str(e) if form == 'paren' else '-' + str(b) + '**' + str(e)} {op} {c}**{f_}"),
    )


@template("MK")
def zero_negative(rng, lvl):
    if lvl == 1:
        r = rng.random()
        if r < 0.3:
            b = rng.randint(2, 10)
            e = rng.randint(2, 4)
            need(b ** e <= 1000)
            val = R(1, b ** e)
            cands = [
                (m(_pw(b, e)), Q(b) ** e, "is the number itself; the reciprocal needs a negative exponent"),
                (m(f"-{_pw(b, e)}"), -Q(b) ** e, "confuses a negative exponent with a negative number"),
                (m(_pw(e, -b)), R(1, e ** b), "switches the base and the exponent"),
                (m(_pw(R(1, b), -e)), Q(b) ** e, f"flips twice: this equals {m(_pw(b, e))}"),
                (m(_pw(b, -(e + 1))), R(1, b ** (e + 1)), None),
            ]
            return Problem(
                stem=choose(rng, f"Which of the following is equal to {m(frac_raw(val))}?",
                            f"Which power is equal to {m(frac_raw(val))}?"),
                answer=m(_pw(b, -e)),
                fmt=lambda t: t,
                wrong=[(t, why) for t, v, why in cands if v != val],
                steps=[
                    f"Write the denominator as a power: {m(f'{int_raw(b ** e)} = {_times(b, e)} = {_pw(b, e)}')}.",
                    f"A reciprocal of a power is the same power with a negative exponent: "
                    f"{m(f'{F(1, _pw(b, e))} = {_pw(b, -e)}')}.",
                ],
                check=m(_pw(b, _power_of(b, val))),
            )
        if r < 0.55:
            c = rng.randint(2, 9)
            b = rng.choice([v for v in range(2, 13) if v != c])
            ans = Q(c)
            return Problem(
                stem=choose(rng, f"What is the value of {m(f'{c} \\times {_pw(b, 0)}')}?",
                            f"Evaluate {m(f'{c} \\times {_pw(b, 0)}')}."),
                answer=ans,
                fmt=num,
                wrong=[
                    (Q(0), f"treats {m(_pw(b, 0))} as 0"),
                    (Q(c * b), f"treats {m(_pw(b, 0))} as {b}"),
                    (Q(1), f"raises the whole product {m(f'{c} \\times {b}')} to the zero power"),
                    (Q(c + 1), None),
                ],
                steps=[
                    f"Any nonzero number raised to the zero power equals 1, so {m(f'{_pw(b, 0)} = 1')}.",
                    f"Then {m(f'{c} \\times 1 = {c}')}.",
                ],
                check=sp.Integer(c) * sp.Integer(b) ** 0,
            )
        b = rng.randint(2, 10)
        e = rng.randint(1, 3)
        need(b ** e <= 1000 and (e > 1 or b > 2))
        ans = R(1, b ** e)
        wrong = [
            (Q(-(b ** e)), "makes the answer negative; a negative exponent means a reciprocal, not a negative number"),
            (Q(-b * e), "multiplies the base by the exponent"),
            (Q(b ** e), "forgets to take the reciprocal"),
        ]
        if e > 1:
            wrong.append((R(1, b * e), "multiplies the base by the exponent before taking the reciprocal"))
        wrong.append((-ans, "makes the reciprocal negative"))
        return Problem(
            stem=choose(rng, f"What is the value of {m(_pw(b, -e))}?", f"Evaluate {m(_pw(b, -e))}.",
                        f"Which of the following is equal to {m(_pw(b, -e))}?"),
            answer=ans,
            fmt=frac,
            neg_ok=True,
            wrong=wrong,
            steps=[
                f"A negative exponent means ``take the reciprocal'': {m(f'{_pw(b, -e)} = {F(1, _pw(b, e))}')}.",
                (f"{m(f'{_pw(b, e)} = {int_raw(b ** e)}')}, so the answer is {m(frac_raw(ans))}." if e > 1
                 else f"So the answer is {m(frac_raw(ans))}."),
            ],
            check=sp.Integer(b) ** (-e),
            verify=lambda v: v * b ** e == 1,
        )

    if lvl == 2:
        p, q = rng.randint(1, 5), rng.randint(2, 6)
        need(p != q and gcd(p, q) == 1)
        e = rng.choice([1, 2, 2, 3])
        need(max(p, q) ** e <= 216)
        base = R(p, q)
        ans = base ** (-e)
        flip = 1 / base
        wrong = [
            (base ** e, "forgets to flip the fraction for the negative exponent"),
            (-(flip ** e), "makes the answer negative; a negative exponent does not change the sign"),
            (-(base ** e), "makes the answer negative instead of flipping the fraction"),
        ]
        if e > 1:
            wrong.append((flip * e, "multiplies by the exponent instead of raising to the power"))
            wrong.append((R(q ** e, p), "raises only the numerator after flipping"))
        steps = [
            f"A negative exponent means take the reciprocal: flip {m(frac_raw(base))} to "
            f"{m(frac_raw(flip))} and make the exponent positive.",
        ]
        if e == 1:
            steps.append(f"{m(f'{_pw(base, -1)} = {frac_raw(flip)}')}.")
        else:
            steps.append(f"Raise the top and bottom to the power {e}: "
                         f"{m(f'{_pw(flip, e)} = {F(_pw(flip.p, e), _pw(flip.q, e))} = {frac_raw(ans)}')}.")
        return Problem(
            stem=choose(rng, f"What is the value of {m(_pw(base, -e))}?",
                        f"Which of the following is equal to {m(_pw(base, -e))}?"),
            answer=ans,
            fmt=frac,
            neg_ok=True,
            wrong=wrong,
            steps=steps,
            check=(Fraction(q, p)) ** e,
        )

    # level 3: combine zero / negative exponents
    kind = rng.choice(["sum", "product"])
    if kind == "sum":
        a = rng.randint(2, 9)
        b = rng.randint(2, 6)
        e = rng.choice([1, 2])
        need(b ** e <= 36 and a != b)
        ans = 1 + R(1, b ** e)
        tex = f"{_pw(a, 0)} + {_pw(b, -e)}"
        return Problem(
            stem=choose(rng, f"What is the value of {m(tex)}?", f"Evaluate {m(tex)}."),
            answer=ans,
            fmt=mixed,
            neg_ok=True,
            wrong=[
                (R(1, b ** e), f"treats {m(_pw(a, 0))} as 0"),
                (a + R(1, b ** e), f"treats {m(_pw(a, 0))} as {a}"),
                (Q(1 - b ** e), f"treats {m(_pw(b, -e))} as {m(int_raw(-(b ** e)))}"),
                (Q(1 - b * e), f"treats {m(_pw(b, -e))} as {m(f'{b} \\times ({-e})')}") if e > 1 else
                (Q(1 + b), f"forgets to take the reciprocal of {m(_pw(b, 1))}"),
            ],
            steps=[
                f"Any nonzero number to the zero power is 1: {m(f'{_pw(a, 0)} = 1')}.",
                f"A negative exponent means a reciprocal: {m(f'{_pw(b, -e)} = {F(1, _pw(b, e))} = {frac_raw(R(1, b ** e))}')}.",
                f"Add: {m(f'1 + {frac_raw(R(1, b ** e))} = {mixed_raw(ans)}')}.",
            ],
            check=Fraction(1) + Fraction(1, b ** e),
        )
    b = rng.choice([2, 3, 5, 10])
    e1 = rng.randint(2, 6)
    e2 = rng.randint(2, 8)
    need(e1 != e2)
    k = e2 - e1
    need(abs(k) <= 3 and b ** abs(k) <= 125 and k != 0)
    ans = Q(b) ** k
    tex = f"{_pw(b, -e1)} \\times {_pw(b, e2)}"
    return Problem(
        stem=choose(rng, f"What is the value of {m(tex)}?", f"Evaluate {m(tex)}."),
        answer=ans,
        fmt=frac,
        neg_ok=True,
        wrong=[w for w in [
            (Q(b) ** (e1 + e2) if b ** (e1 + e2) <= 10 ** 6 else None, "ignores the negative sign on the exponent and adds"),
            (Q(b) ** (-k), "subtracts the exponents in the wrong order"),
            (Q(b * b) ** k, "multiplies the bases as well as adding the exponents"),
            (-ans, "makes the answer negative because of the negative exponent"),
        ] if w[0] is not None],
        steps=[
            f"Same base, so add the exponents: {m(f'{-e1} + {e2} = {k}')}, which gives {m(_pw(b, k))}.",
            (f"{m(f'{_pw(b, k)} = {int_raw(ans)}')}." if k > 0 else
             f"A negative exponent means a reciprocal: {m(f'{_pw(b, k)} = {F(1, _pw(b, -k))} = {frac_raw(ans)}')}."),
        ],
        check=Fraction(b) ** e2 / Fraction(b) ** e1,
    )


@template("MK")
def exp_rules(rng, lvl):
    a = rng.randint(2, 9)

    def P(k):                     # choice text for a^k
        return m(_pw(a, k))

    def chk(value):               # independent check: rebuild the power by counting
        return m(_pw(a, _power_of(a, value)))

    if lvl == 1:
        rule = rng.choice(["product", "quotient", "power"])
        mm, nn = rng.randint(2, 9), rng.randint(2, 9)
        if rule == "product":
            k = mm + nn
            tex = f"{_pw(a, mm)} \\times {_pw(a, nn)}"
            wrong = [
                (P(mm * nn), "multiplies the exponents instead of adding them"),
                (m(_pw(a * a, k)), "multiplies the bases as well as adding the exponents"),
                (m(_pw(a * a, mm * nn)), "multiplies both the bases and the exponents"),
                (P(k + 1), None),
            ]
            steps = [f"When you multiply powers with the same base, keep the base and \\emph{{add}} the exponents.",
                     f"{m(f'{tex} = {_pw(a, f"{mm}+{nn}")} = {_pw(a, k)}')}."]
            value = Fraction(a) ** mm * Fraction(a) ** nn
        elif rule == "quotient":
            need(mm > nn + 1)
            k = mm - nn
            tex = F(_pw(a, mm), _pw(a, nn))
            wrong = [
                (P(mm + nn), "adds the exponents instead of subtracting them"),
                (P(nn - mm), "subtracts the exponents in the wrong order"),
                (P(mm // nn) if mm % nn == 0 and mm // nn != k else m(f"1^{{{k}}}"),
                 "divides the exponents instead of subtracting them" if mm % nn == 0 and mm // nn != k
                 else "divides the bases as well as subtracting the exponents"),
                (P(mm * nn), None),
            ]
            steps = [f"When you divide powers with the same base, keep the base and \\emph{{subtract}} the exponents.",
                     f"{m(f'{tex} = {_pw(a, f"{mm}-{nn}")} = {_pw(a, k)}')}."]
            value = Fraction(a) ** mm / Fraction(a) ** nn
        else:
            mm, nn = rng.randint(2, 5), rng.randint(2, 5)
            k = mm * nn
            tex = f"\\left({_pw(a, mm)}\\right)^{{{nn}}}"
            wrong = [
                (P(mm + nn), "adds the exponents instead of multiplying them"),
                (m(f"{nn} \\cdot {_pw(a, mm)}"), "multiplies by the outside exponent instead of raising to it"),
                (P(mm ** nn) if mm ** nn <= 40 and mm ** nn != k else P(k + nn),
                 "raises the exponent to a power instead of multiplying" if mm ** nn <= 40 and mm ** nn != k else None),
                (P(k - 1), None),
            ]
            steps = [f"For a power of a power, keep the base and \\emph{{multiply}} the exponents.",
                     f"{m(f'{tex} = {_pw(a, f"{mm} \\cdot {nn}")} = {_pw(a, k)}')}."]
            value = (Fraction(a) ** mm) ** nn
        return Problem(
            stem=choose(rng, f"Which of the following is equal to {m(tex)}?",
                        f"Simplify {m(tex)}."),
            answer=P(k),
            fmt=lambda s: s,
            wrong=wrong,
            steps=steps,
            check=chk(value),
        )

    # level 2: two rules in one expression
    form = rng.choice(["pp_q", "prod_q"])
    if form == "pp_q":
        mm, nn = rng.randint(2, 4), rng.randint(2, 4)
        p_ = rng.randint(2, 9)
        k = mm * nn + p_
        tex = f"\\left({_pw(a, mm)}\\right)^{{{nn}}} \\times {_pw(a, p_)}"
        wrong = [
            (P(mm + nn + p_), "adds all the exponents; the power of a power should be multiplied"),
            (P(mm * nn * p_), "multiplies all the exponents"),
            (P((mm + nn) * p_) if (mm + nn) * p_ != k else P(k + 2), None),
            (m(_pw(a * a, k)), "multiplies the bases as well"),
        ]
        steps = [f"Power of a power: multiply the exponents. {m(f'\\left({_pw(a, mm)}\\right)^{{{nn}}} = {_pw(a, mm * nn)}')}.",
                 f"Product of powers: add the exponents. {m(f'{_pw(a, mm * nn)} \\times {_pw(a, p_)} = {_pw(a, k)}')}."]
        value = (Fraction(a) ** mm) ** nn * Fraction(a) ** p_
    else:
        mm, nn = rng.randint(2, 9), rng.randint(2, 9)
        p_ = rng.randint(2, 9)
        k = mm + nn - p_
        need(k >= 2)
        tex = F(f"{_pw(a, mm)} \\times {_pw(a, nn)}", _pw(a, p_))
        wrong = [
            (P(mm * nn - p_), "multiplies the exponents in the numerator instead of adding them"),
            (P(mm + nn + p_), "adds the exponent in the denominator instead of subtracting it"),
            (P((mm + nn) // p_) if (mm + nn) % p_ == 0 and (mm + nn) // p_ != k else P(k + 1),
             "divides the exponents instead of subtracting" if (mm + nn) % p_ == 0 and (mm + nn) // p_ != k else None),
            (P(k - 1), None),
        ]
        steps = [f"Numerator: same base, so add the exponents. {m(f'{_pw(a, mm)} \\times {_pw(a, nn)} = {_pw(a, mm + nn)}')}.",
                 f"Divide: subtract the exponents. {m(f'{F(_pw(a, mm + nn), _pw(a, p_))} = {_pw(a, f"{mm + nn}-{p_}")} = {_pw(a, k)}')}."]
        value = Fraction(a) ** mm * Fraction(a) ** nn / Fraction(a) ** p_
    return Problem(
        stem=choose(rng, f"Which of the following is equal to {m(tex)}?", f"Simplify {m(tex)}."),
        answer=P(k),
        fmt=lambda s: s,
        wrong=wrong,
        steps=steps,
        check=chk(value),
    )


_DECS = ([R(v, 10) for v in range(1, 10)] + [R(v, 100) for v in range(2, 10)]
         + [R(v, 10) for v in (11, 12, 13, 14, 15, 25)])


@template("MK")
def power_of_fraction(rng, lvl):
    if rng.random() < 0.6:
        p, q = rng.randint(1, 9), rng.randint(2, 10)
        need(p < q and gcd(p, q) == 1)
        e = rng.choice([2, 2, 3])
        need(q ** e <= 216)
        neg = e == 3 and rng.random() < 0.35
        base = R(-p if neg else p, q)
        ans = base ** e
        sgn = -1 if neg else 1
        wrong = [
            (sgn * R(p, q ** e), "raises only the denominator to the power"),
            (sgn * R(p ** e, q), "raises only the numerator to the power"),
            (base * e, "multiplies by the exponent instead of raising to the power"),
            (base ** (e + 1), f"uses {e + 1} factors instead of {e}"),
        ]
        if neg:
            wrong.insert(0, (-ans, "loses the negative sign; an odd power of a negative number is negative"))
        else:
            wrong.append((R(p * e, q ** e), None))
        return Problem(
            stem=choose(rng, f"What is the value of {m(_pw(base, e))}?", f"Evaluate {m(_pw(base, e))}.",
                        f"Which of the following is equal to {m(_pw(base, e))}?"),
            answer=ans,
            fmt=frac,
            neg_ok=neg,
            wrong=wrong,
            steps=[
                f"Raise the numerator and the denominator to the power {e}: "
                f"{m(f'{_pw(base, e)} = {F(_pw(-p if neg else p, e), _pw(q, e))}')}.",
                f"{m(f'{_pw(-p if neg else p, e)} = {int_raw(sgn * p ** e)}')} and "
                f"{m(f'{_pw(q, e)} = {int_raw(q ** e)}')}, so the answer is {m(frac_raw(ans))}.",
            ],
            check=Fraction(sgn * p, q) ** e,
        )
    d = rng.choice(_DECS)
    e = rng.choice([2, 3])
    ans = d ** e
    need(ans.q <= 10 ** 4)
    places_d = len(dec_raw(d).split(".")[1]) if "." in dec_raw(d) else 0
    places = places_d * e
    digits = int(d * 10 ** places_d)
    wrong = [
        (d * e, "multiplies by the exponent instead of raising to the power"),
        (ans * 10, f"puts too few decimal places in the answer (it needs {places})"),
        (ans / 10, "puts too many decimal places in the answer"),
        (ans * 100, None),
        (d ** (e + 1), f"uses {e + 1} factors instead of {e}"),
    ]
    return Problem(
        stem=choose(rng, f"What is the value of {m(f'({dec_raw(d)})^{{{e}}}')}?",
                    f"Evaluate {m(f'({dec_raw(d)})^{{{e}}}')}.",
                    f"Which of the following is equal to {m(f'({dec_raw(d)})^{{{e}}}')}?"),
        answer=ans,
        fmt=dec,
        wrong=wrong,
        steps=[
            f"Multiply the digits as whole numbers first: {m(f'{_pw(digits, e)} = {int_raw(digits ** e)}')}.",
            f"Count decimal places: {m(dec_raw(d))} has {places_d} decimal place{'s' if places_d > 1 else ''}, "
            f"and it is used as a factor {e} times, so the answer has {m(f'{places_d} \\times {e} = {places}')} "
            f"decimal places: {m(dec_raw(ans))}.",
        ],
        tip=(f"Estimate: {m(dec_raw(d))} is less than 1, so its {'square' if e == 2 else 'cube'} must be "
             f"\\emph{{smaller}} than {m(dec_raw(d))}." if d < 1 else
             f"Estimate: {m(dec_raw(d))} is more than 1, so its {'square' if e == 2 else 'cube'} must be "
             f"\\emph{{larger}} than {m(dec_raw(d))}."),
        check=Fraction(int(d.p), int(d.q)) ** e,
    )


_DECS_BIG = [R(v, 10) for v in range(11, 100) if v % 10 != 0] + [Q(v) for v in range(2, 10)]


def _places(v) -> int:
    t = dec_raw(v)
    return len(t.split(".")[1]) if "." in t else 0


def _mantissa(rng, one_place=True):
    if one_place:
        return rng.choice([R(v, 10) for v in range(11, 100) if v % 10 != 0] + [Q(v) for v in range(2, 10)])
    return rng.choice([R(v, 100) for v in range(101, 1000) if v % 10 != 0])


@template("MK")
def sci_to_standard(rng, lvl):
    mant = _mantissa(rng, one_place=rng.random() < 0.75)
    big = lvl == 1 or rng.random() < 0.4
    if lvl == 2 and big:
        mant = _mantissa(rng, one_place=False)
    if big:
        k = rng.randint(2, 7) if lvl == 1 else rng.randint(4, 8)
        ans = mant * 10 ** k
        need(ans.is_integer)
        right = True
    else:
        k = -rng.choice([1, 2, 2, 3, 3])
        ans = mant * R(1, 10 ** -k)
        need(ans.q <= 10 ** 3)
        right = False
    tex = _sci_raw(mant, k)
    n = abs(k)
    wrong = [
        (ans / 10 if right else ans * 10, "moves the decimal point one place too few"),
        (ans * 10 if right else ans / 10, "moves the decimal point one place too many"),
        (mant * 10 ** n if not right else mant / 10 ** n, "moves the decimal point the wrong way"),
        (mant * k if right else mant * 10 ** (n + 1), "multiplies by the exponent instead of by a power of 10" if right else
         "moves the decimal point the wrong way and one place too far"),
    ]
    direction = "right" if right else "left"
    return Problem(
        stem=choose(rng, f"What is {m(tex)} written in standard form?",
                    f"Which of the following is equal to {m(tex)}?",
                    f"Write {m(tex)} as an ordinary number."),
        answer=ans,
        fmt=dec,
        wrong=wrong,
        steps=[
            (f"Multiplying by {m(f'10^{{{k}}}')} moves the decimal point {n} places to the {direction}."
             if right else
             f"A negative exponent means dividing by a power of 10: {m(f'10^{{{k}}}')} moves the decimal "
             f"point {n} place{'s' if n > 1 else ''} to the {direction}."),
            f"{m(dec_raw(mant))} becomes {m(dec_raw(ans))}"
            + (" (write a 0 in front of the decimal point)." if (not right and n == 1) else
               " (fill the empty places with zeros)." if (not right or n > _places(mant)) else "."),
        ],
        check=sp.Rational(dec_raw(mant).replace("{,}", "")) * sp.Integer(10) ** k,
        near=lambda r: [ans * 100, ans / 100, ans * 1000, ans / 1000],
    )


@template("MK")
def standard_to_sci(rng, lvl):
    mant = _mantissa(rng, one_place=rng.random() < 0.7)
    if lvl == 1 or rng.random() < 0.4:
        k = rng.randint(3, 8)
    else:
        k = -rng.randint(1, 4)
    value = mant * sp.Integer(10) ** k
    need(value.q <= 10 ** 4)
    std = dec_raw(value)
    ans = m(_sci_raw(mant, k))
    if k > 0:
        wrong = [
            (m(_sci_raw(mant * 10, k - 1)), f"is equal to {m(std)} but is not scientific notation: "
                                            f"the first factor must be less than 10"),
            (m(_sci_raw(mant, k - 1)), "counts one place too few"),
            (m(_sci_raw(mant, k + 1)), "counts one place too many"),
            (m(_sci_raw(mant, -k)), "uses a negative exponent, but numbers greater than 1 have positive exponents"),
        ]
        steps = [
            f"Move the decimal point to get a number that is at least 1 but less than 10: {m(dec_raw(mant))}.",
            f"The decimal point moved {k} places to the left, which made the number smaller, so multiply by "
            f"{m(f'10^{{{k}}}')} to keep the same value.",
            f"So {m(f'{std} = {_sci_raw(mant, k)}')}.",
        ]
    else:
        n = -k
        wrong = [
            (m(_sci_raw(mant, n)), "uses a positive exponent, but numbers less than 1 have negative exponents"),
            (m(_sci_raw(mant, k + 1)), "counts one place too few"),
            (m(_sci_raw(mant, k - 1)), "counts one place too many"),
        ]
        if n >= 2:
            wrong.append((m(_sci_raw(mant * 10, k - 1)), f"is equal to {m(std)} but is not scientific notation: "
                                                         f"the first factor must be less than 10"))
        steps = [
            f"Move the decimal point to get a number that is at least 1 but less than 10: {m(dec_raw(mant))}.",
            f"The decimal point moved {n} place{'s' if n > 1 else ''} to the right, which made the number larger, "
            f"so multiply by {m(f'10^{{{k}}}')} to keep the same value. (Numbers less than 1 always get a negative exponent.)",
            f"So {m(f'{std} = {_sci_raw(mant, k)}')}.",
        ]

    def verify(s):
        mt, ex = _parse_sci(s)
        return 1 <= mt < 10 and mt * Fraction(10) ** ex == Fraction(int(value.p), int(value.q))
    return Problem(
        stem=choose(rng, f"What is {m(std)} written in scientific notation?",
                    f"Which of the following shows {m(std)} in scientific notation?"),
        answer=ans,
        fmt=lambda s: s,
        wrong=wrong,
        steps=steps,
        verify=verify,
    )


def _sci_near(ans):
    """Plausible scientific-notation fillers around an answer."""
    mant, k = _mant_exp(ans)

    def f(rng):
        out = [ans * 10, ans / 10, ans * 100, ans / 100]
        for dm in (1, 2, -1):
            if 1 <= mant + dm < 10:
                out.append((mant + dm) * sp.Integer(10) ** k)
        rng.shuffle(out)
        return out
    return f


_SCI_FACTORS = [Q(v) for v in range(2, 10)] + [R(v, 10) for v in (12, 15, 25, 35, 45)]


@template("MK")
def sci_multiply(rng, lvl):
    if lvl == 2:
        a, b = rng.choice(_SCI_FACTORS), rng.choice(_SCI_FACTORS)
        e1, e2 = rng.randint(2, 9), rng.randint(2, 9)
        prod = a * b
        need(_mant_exp(prod)[0].q <= 100)
        ans = prod * sp.Integer(10) ** (e1 + e2)
        big = prod >= 10
        tex = f"({_sci_raw(a, e1)})({_sci_raw(b, e2)})"
        wrong = [
            (prod * sp.Integer(10) ** (e1 * e2), "multiplies the exponents instead of adding them"),
            ((a + b) * sp.Integer(10) ** (e1 + e2), "adds the first factors instead of multiplying them"),
        ]
        if big:
            wrong.insert(0, (ans / 10, f"rewrites {m(dec_raw(prod))} as {m(dec_raw(prod / 10))} but forgets to add 1 to the exponent"))
        else:
            wrong.append((ans * 10, "adds 1 to the exponent when no adjustment is needed"))
        steps = [
            f"Multiply the first factors: {m(f'{dec_raw(a)} \\times {dec_raw(b)} = {dec_raw(prod)}')}.",
            f"Multiply the powers of 10 by adding exponents: {m(f'10^{{{e1}}} \\times 10^{{{e2}}} = 10^{{{e1 + e2}}}')}.",
        ]
        if big:
            steps.append(f"{m(dec_raw(prod))} is not less than 10, so write {m(f'{dec_raw(prod)} = {dec_raw(prod / 10)} \\times 10^{{1}}')}: "
                         f"the answer is {_sci(ans)}.")
        else:
            steps.append(f"{m(dec_raw(prod))} is already between 1 and 10, so the answer is {_sci(ans)}.")
        return Problem(
            stem=choose(rng, f"What is {m(tex)} written in scientific notation?",
                        f"Multiply: {m(tex)}. Give the answer in scientific notation."),
            answer=ans,
            fmt=_sci,
            wrong=wrong,
            steps=steps,
            near=_sci_near(ans),
            check=Fraction(int(a.p), int(a.q)) * Fraction(int(b.p), int(b.q)) * Fraction(10) ** (e1 + e2),
        )

    # level 3: division, or a product with a negative exponent
    if rng.random() < 0.6:
        b = rng.choice([Q(v) for v in (2, 4, 5, 8)] + [R(25, 10)])
        a = rng.choice([Q(v) for v in range(1, 10)] + [R(v, 10) for v in (12, 15, 36, 45, 64, 75)])
        need(a != b)
        e1, e2 = rng.randint(4, 12), rng.randint(2, 8)
        need(e1 - e2 >= 1)
        quo = a / b
        need(quo.q in (1, 2, 4, 5, 10, 20, 25, 50, 100) and quo != 1)
        ans = quo * sp.Integer(10) ** (e1 - e2)
        small = quo < 1
        tex = f"({_sci_raw(a, e1)}) \\div ({_sci_raw(b, e2)})"
        wrong = [
            (quo * sp.Integer(10) ** (e1 + e2), "adds the exponents instead of subtracting them"),
            ((b / a) * sp.Integer(10) ** (e1 - e2), "divides the first factors in the wrong order"),
            (quo * sp.Integer(10) ** (e2 - e1), "subtracts the exponents in the wrong order"),
        ]
        if small:
            wrong.insert(0, (ans * 10, f"rewrites {m(dec_raw(quo))} as {m(dec_raw(quo * 10))} but forgets to subtract 1 from the exponent"))
        if a > b and (a - b) >= 1:
            wrong.append(((a - b) * sp.Integer(10) ** (e1 - e2), "subtracts the first factors instead of dividing them"))
        steps = [
            f"Divide the first factors: {m(f'{dec_raw(a)} \\div {dec_raw(b)} = {dec_raw(quo)}')}.",
            f"Divide the powers of 10 by subtracting exponents: {m(f'10^{{{e1}}} \\div 10^{{{e2}}} = 10^{{{e1 - e2}}}')}.",
        ]
        if small:
            steps.append(f"{m(dec_raw(quo))} is less than 1, so write {m(f'{dec_raw(quo)} = {dec_raw(quo * 10)} \\times 10^{{-1}}')} "
                         f"and subtract 1 from the exponent: the answer is {_sci(ans)}.")
        else:
            steps.append(f"{m(dec_raw(quo))} is between 1 and 10, so the answer is {_sci(ans)}.")
        check = (Fraction(int(a.p), int(a.q)) / Fraction(int(b.p), int(b.q))) * Fraction(10) ** (e1 - e2)
    else:
        a, b = rng.choice(_SCI_FACTORS), rng.choice(_SCI_FACTORS)
        e1, e2 = -rng.randint(2, 8), rng.randint(3, 12)
        prod = a * b
        need(prod >= 10 and _mant_exp(prod)[0].q <= 100)
        need(e1 + e2 + 1 != 0)
        ans = prod * sp.Integer(10) ** (e1 + e2)
        tex = f"({_sci_raw(a, e1)})({_sci_raw(b, e2)})"
        wrong = [
            (ans / 10, f"rewrites {m(dec_raw(prod))} as {m(dec_raw(prod / 10))} but forgets to add 1 to the exponent"),
            (prod / 10 * sp.Integer(10) ** (e2 - e1 + 1), "ignores the negative sign on the first exponent"),
            ((a + b) * sp.Integer(10) ** (e1 + e2), "adds the first factors instead of multiplying them"),
        ]
        steps = [
            f"Multiply the first factors: {m(f'{dec_raw(a)} \\times {dec_raw(b)} = {dec_raw(prod)}')}.",
            f"Add the exponents: {m(f'{e1} + {e2} = {e1 + e2}')}, giving {m(f'{dec_raw(prod)} \\times 10^{{{e1 + e2}}}')}.",
            f"{m(dec_raw(prod))} is not less than 10, so write it as {m(f'{dec_raw(prod / 10)} \\times 10^{{1}}')} "
            f"and add 1 to the exponent: the answer is {_sci(ans)}.",
        ]
        check = Fraction(int(prod.p), int(prod.q)) * Fraction(10) ** (e1 + e2)
    need(_mant_exp(ans)[1] not in (0, 1))
    return Problem(
        stem=choose(rng, f"What is {m(tex)} written in scientific notation?",
                    f"Simplify {m(tex)}. Give the answer in scientific notation."),
        answer=ans,
        fmt=_sci,
        wrong=wrong,
        steps=steps,
        near=_sci_near(ans),
        check=check,
    )


@template("MK")
def compare_sci(rng, lvl):
    if rng.random() < 0.5:
        b = rng.choice([2, 3, 4])
        q = rng.choice([v for v in (2, 3, 4) if b * v < 10])
        a = b * q
        e2 = rng.randint(2, 6)
        e1 = e2 + rng.randint(2, 6)
        ans = Q(q) * sp.Integer(10) ** (e1 - e2)
        A, B = _sci_raw(a, e1), _sci_raw(b, e2)
        wrong = [
            (Q(q) * sp.Integer(10) ** (e1 + e2), "adds the exponents instead of subtracting them"),
            (Q(a - b) * sp.Integer(10) ** (e1 - e2), "subtracts the first factors instead of dividing them"),
            (R(b, a) * sp.Integer(10) ** (e2 - e1), "divides the smaller number by the larger one"),
            (Q(q) * sp.Integer(10) ** (e1 - e2 - 1), None),
        ]
        return Problem(
            stem=choose(rng, f"The number {m(A)} is how many times as large as {m(B)}?",
                        f"How many times as large as {m(B)} is {m(A)}?"),
            answer=ans,
            fmt=_sci,
            wrong=wrong,
            steps=[
                f"``How many times as large'' means divide: {m(f'({A}) \\div ({B})')}.",
                f"Divide the first factors: {m(f'{a} \\div {b} = {q}')}. Subtract the exponents: "
                f"{m(f'{e1} - {e2} = {e1 - e2}')}.",
                f"The answer is {_sci(ans)}, which is {m(int_raw(ans))}.",
            ],
            near=_sci_near(ans),
            check=Fraction(a, b) * Fraction(10) ** (e1 - e2),
        )

    want = rng.choice(["greater", "less"])
    k = rng.randint(-6, 7)
    need(k not in (-1, 0, 1))
    m0 = rng.choice([v for v in _DECS_BIG if 2 <= v <= 9])
    hi = [v for v in _DECS_BIG if v > m0]
    lo = [v for v in _DECS_BIG if v < m0]
    m_hi, m_hi2 = rng.sample(hi, 2) if len(hi) > 1 else (None, None)
    m_lo, m_lo2 = rng.sample(lo, 2) if len(lo) > 1 else (None, None)
    need(m_hi is not None and m_lo is not None)
    T = lambda mt, e: mt * sp.Integer(10) ** e
    ref = T(m0, k)
    ref_t = m(_sci_raw(m0, k))
    if want == "greater":
        if rng.random() < 0.5:
            ans, a_m, a_k = T(m_lo2, k + 1), m_lo2, k + 1
        else:
            ans, a_m, a_k = T(m_hi, k), m_hi, k
        wrong = [
            (T(m_hi2, k - 1), f"has a larger first factor, but its power of 10 is smaller, so it is less than {ref_t}"),
            (T(m_lo, k), "has the same power of 10 but a smaller first factor"),
            (T(m0, -k), "has a negative exponent, so it is less than 1") if k > 0 else
            (T(m_hi2, k - 2), "has a larger first factor, but its power of 10 is smaller"),
        ]
    else:
        if rng.random() < 0.5:
            ans, a_m, a_k = T(m_hi2, k - 1), m_hi2, k - 1
        else:
            ans, a_m, a_k = T(m_lo, k), m_lo, k
        wrong = [
            (T(m_lo2, k + 1), f"has a smaller first factor, but its power of 10 is larger, so it is greater than {ref_t}"),
            (T(m_hi, k), "has the same power of 10 but a larger first factor"),
            (T(m0, -k), "has a positive exponent, so it is greater than 1") if k < 0 else
            (T(m_lo2, k + 2), "has a smaller first factor, but its power of 10 is larger"),
        ]
    if a_k == k:
        why_ans = (f"{_sci(ans)} has the same power of 10 as {ref_t}, so compare the first factors: "
                   f"{m(dec_raw(a_m))} is {'larger' if want == 'greater' else 'smaller'} than {m(dec_raw(m0))}.")
    else:
        why_ans = (f"{_sci(ans)} has {m(f'10^{{{a_k}}}')}, a {'larger' if want == 'greater' else 'smaller'} power of 10 "
                   f"than {m(f'10^{{{k}}}')}, so it is {want} even though its first factor is "
                   f"{'smaller' if want == 'greater' else 'larger'}.")
    pool = [ans] + [w[0] for w in wrong]
    hits = [v for v in pool if (v > ref if want == "greater" else v < ref)]
    need(len(hits) == 1)
    return Problem(
        stem=choose(rng, f"Which of the following numbers is {want} than {ref_t}?",
                    f"Which number below is {want} than {ref_t}?"),
        answer=ans,
        fmt=_sci,
        sort=False,
        wrong=wrong,
        steps=[
            "Compare the powers of 10 first. Because every first factor is between 1 and 10, the number with "
            "the larger power of 10 is always the larger number"
            + (" (and remember that $-5$ is larger than $-6$)." if k < 0 else "."),
            why_ans,
            f"Each of the other choices is {'less' if want == 'greater' else 'greater'} than {ref_t}.",
        ],
        check=hits[0],
    )


@template("MK")
def exp_equation(rng, lvl):
    kind = rng.choice(["product", "power", "rewrite", "quotient"])
    a = rng.choice([2, 3, 5, 7, 10]) if kind != "rewrite" else rng.choice([2, 3, 5])
    n_sym = sp.Symbol("n")

    def brute(lhs):
        """Find the integer n that makes lhs(n) true by trying values."""
        sols = [v for v in range(-30, 61) if lhs(v)]
        need(len(sols) == 1)
        return Q(sols[0])

    if kind == "product":
        mm = rng.randint(2, 9)
        p = rng.randint(mm + 2, 20) if rng.random() < 0.5 else mm * rng.randint(3, 5)
        need(p <= 30)
        ans = Q(p - mm)
        tex = f"{_pw(a, mm)} \\times {_pw(a, 'n')} = {_pw(a, p)}"
        wrong = [
            (Q(p + mm), "adds the exponents instead of subtracting"),
            (R(p, mm), "divides the exponents"),
            (Q(p), None),
            (Q(p - mm - 1), None),
            (Q(p - mm - 2), None),
        ]
        steps = [f"Same base, so the exponents add: {m(f'{mm} + n = {p}')}.",
                 f"Subtract {mm}: {m(f'n = {p} - {mm} = {p - mm}')}."]
        chk = brute(lambda v: Fraction(a) ** mm * Fraction(a) ** v == Fraction(a) ** p)
    elif kind == "quotient":
        mm = rng.randint(2, 9)
        p = rng.randint(2, 12)
        ans = Q(p + mm)
        tex = f"{F(_pw(a, 'n'), _pw(a, mm))} = {_pw(a, p)}"
        wrong = [
            (Q(p - mm), "subtracts instead of adding") if p != mm else (Q(p * mm + 1), None),
            (Q(p * mm), "multiplies the exponents"),
            (Q(p), None),
            (Q(p + mm + 1), None),
        ]
        steps = [f"Dividing powers with the same base subtracts the exponents: {m(f'n - {mm} = {p}')}.",
                 f"Add {mm}: {m(f'n = {p} + {mm} = {p + mm}')}."]
        chk = brute(lambda v: Fraction(a) ** v / Fraction(a) ** mm == Fraction(a) ** p)
    elif kind == "power":
        mm = rng.randint(2, 5)
        nn = rng.randint(2, 6)
        p = mm * nn
        ans = Q(nn)
        tex = f"\\left({_pw(a, mm)}\\right)^{{n}} = {_pw(a, p)}"
        wrong = [
            (Q(p - mm), "subtracts the exponents; a power of a power multiplies them"),
            (Q(p * mm), "multiplies instead of dividing"),
            (Q(p + mm), None),
            (Q(nn - 1), None),
            (Q(nn + 1), None),
        ]
        steps = [f"A power of a power multiplies the exponents: {m(f'{mm} \\cdot n = {p}')}.",
                 f"Divide by {mm}: {m(f'n = {p} \\div {mm} = {nn}')}."]
        chk = brute(lambda v: (Fraction(a) ** mm) ** v == Fraction(a) ** p)
    else:
        r = rng.randint(2, 3) if a != 5 else 2
        c = a ** r                     # c = a^r, e.g. 8 = 2^3
        need(c <= 27)
        mm = rng.randint(2, 9)
        ans = Q(r + mm)
        tex = f"{c} \\times {_pw(a, mm)} = {_pw(a, 'n')}"
        wrong = [
            (Q(c + mm), f"adds {c} to the exponent instead of writing {c} as a power of {a}"),
            (Q(r * mm), "multiplies the exponents instead of adding them"),
            (Q(mm + 1), f"counts {c} as a single factor of {a}"),
            (Q(mm), f"leaves out the {c}"),
            (Q(c * mm), None),
        ]
        steps = [f"Write {c} as a power of {a}: {m(f'{c} = {_pw(a, r)}')}.",
                 f"Now {m(f'{_pw(a, r)} \\times {_pw(a, mm)} = {_pw(a, r + mm)}')}, so {m(f'n = {r} + {mm} = {r + mm}')}."]
        chk = brute(lambda v: c * Fraction(a) ** mm == Fraction(a) ** v)
    return Problem(
        stem=choose(rng, f"If {m(tex)}, what is the value of {m('n')}?",
                    f"What value of {m('n')} makes {m(tex)} true?"),
        answer=ans,
        fmt=num,
        wrong=[w for w in wrong if Q(w[0]) > 0],
        steps=steps,
        check=chk,
    )


PLAN = [
    # (template, level, count)  -- easy -> hard; 25 problems
    (evaluate_power, 1, 2),
    (zero_negative, 1, 2),
    (exp_rules, 1, 2),
    (sci_to_standard, 1, 1),
    (standard_to_sci, 1, 1),
    (evaluate_power, 2, 2),
    (power_of_fraction, 2, 2),
    (standard_to_sci, 2, 2),
    (sci_to_standard, 2, 1),
    (exp_rules, 2, 1),
    (sci_multiply, 2, 2),
    (sci_multiply, 3, 2),
    (compare_sci, 3, 2),
    (exp_equation, 3, 2),
    (zero_negative, 3, 1),
]
