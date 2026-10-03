"""Chapter 5 - Decimals."""
from decimal import Decimal as D

from ..core import (R, Q, Problem, need, dec, frac, money, money_cents, m, F,
                    int_raw, dec_raw, frac_raw, unit, person, soldier, choose, template)

NUM = 5
TITLE = "Decimals"
PART = 1

INTRO = r"""
Decimals are fractions with denominators of $10$, $100$, $1{,}000$, and so
on. Money is the everyday example, and most decimal word problems on the
ASVAB are about prices, pay, and fuel. The whole chapter rests on keeping
track of the decimal point.

\begin{concept}{Place value}
In $3.472$: $4$ tenths, $7$ hundredths, $2$ thousandths. Compare decimals
place by place from the left: $0.5 > 0.45 > 0.405 > 0.054$ (look at the
tenths first). Extra zeros on the right change nothing: $0.5 = 0.50$.
To \textbf{round}, look at the next digit to the right: $5$ or more rounds up.
$7.486 \approx 7.49$ (nearest hundredth) $\approx 7.5$ (nearest tenth).
\end{concept}

\begin{concept}{The four operations}
\begin{itemize}
\item \textbf{Add/subtract:} line up the decimal points; fill empty places
  with zeros: $15.00 - 3.84 = 11.16$.
\item \textbf{Multiply:} multiply as whole numbers, then count the decimal
  places in both factors: $0.6 \times 0.04$: $6 \times 4 = 24$, three places,
  $0.024$.
\item \textbf{Divide by a decimal:} move the point in \emph{both} numbers
  until the divisor is whole: $7.2 \div 0.08 = 720 \div 8 = 90$.
\end{itemize}
\end{concept}

\begin{concept}{Fractions and decimals}
Fraction $\to$ decimal: divide the top by the bottom ($\frac{3}{8} = 3 \div 8 = 0.375$).
Decimal $\to$ fraction: read the place value and simplify
($0.45 = \frac{45}{100} = \frac{9}{20}$). Worth memorizing:
$\frac{1}{2} = 0.5$, $\frac{1}{4} = 0.25$, $\frac{3}{4} = 0.75$,
$\frac{1}{5} = 0.2$, $\frac{1}{8} = 0.125$.
\end{concept}

\begin{example}{Worked example}
Gas costs \$3.49 per gallon. How much do $12$ gallons cost?

\textbf{Solution.} $3.49 \times 12 = 3.49 \times 10 + 3.49 \times 2 = 34.90 + 6.98 = \$41.88$.
\end{example}

\begin{tip}
Estimate first to place the decimal point: $3.49 \times 12$ is about
$3.5 \times 12 = 42$, so the answer must be about \$42, not \$4.19 or \$418.80.
\end{tip}

\begin{trap}
\begin{itemize}
\item Lining up the last digits instead of the decimal points.
\item Thinking a longer decimal is larger: $0.405 < 0.5$.
\item Moving the decimal point in only one number when dividing.
\item Forgetting to borrow across zeros: $20.00 - 7.36 = 12.64$.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _places(v):
    v = Q(v)
    p = 0
    while not (v * 10 ** p).is_integer:
        p += 1
    return p


def _draw(rng, lo, hi, places, nonzero_last=True):
    """A decimal in [lo, hi] with exactly `places` decimal places."""
    k = 10 ** places
    n_ = rng.randint(int(lo * k), int(hi * k))
    need(n_ > 0)
    if nonzero_last and places:
        need(n_ % 10 != 0)
    return R(n_, k)


def _n(v):
    return int_raw(v)


def _d(v):
    return dec_raw(v)


def _dp(v, p):
    return dec_raw(v, places=p)


def _misalign(a_, b_, op):
    """Student bug: lines up the right-hand digits instead of the decimal points."""
    pa, pb = _places(a_), _places(b_)
    ai, bi = int(a_ * 10 ** pa), int(b_ * 10 ** pb)
    P = max(pa, pb)
    r = ai + bi if op == "+" else ai - bi
    return R(r, 10 ** P)


def _no_borrow(a_, b_):
    """Student bug: in each column subtracts the smaller digit from the larger."""
    P = max(_places(a_), _places(b_))
    x_, y_ = str(int(a_ * 10 ** P)), str(int(b_ * 10 ** P))
    n_ = max(len(x_), len(y_))
    x_, y_ = x_.zfill(n_), y_.zfill(n_)
    out = "".join(str(abs(int(c1) - int(c2))) for c1, c2 in zip(x_, y_))
    return R(int(out), 10 ** P)


def _fixed(p):
    """Formatter showing exactly p decimal places."""
    return lambda v: m(dec_raw(v, places=p))


_PLACE = {0: "whole number", 1: "tenth", 2: "hundredth", 3: "thousandth"}
_DIGIT = {1: "tenths", 2: "hundredths", 3: "thousandths", 4: "ten-thousandths"}


def _round(v, p):
    k = 10 ** p
    return (Q(v) * k + R(1, 2)).floor() / k


def _near_cents(v, steps=(R(1, 100), R(10, 100), R(1), R(5, 10))):
    def f(r):
        out = [Q(v) + s * d for s in steps for d in (1, -1)]
        out = [w for w in out if w > 0]
        r.shuffle(out)
        return out
    return f


# --------------------------------------------------------------------------
# computation
# --------------------------------------------------------------------------

@template("MK")
def add_sub_dec(rng, lvl):
    if lvl == 1:
        op = rng.choice(["+", "-"])
        pa, pb = rng.sample([1, 2, 2, 3], 2)
        need(pa != pb)
        a_ = _draw(rng, 1, 40, pa)
        b_ = _draw(rng, 1, 40, pb)
        if op == "-" and a_ < b_:
            a_, b_ = b_, a_
        ans = a_ + b_ if op == "+" else a_ - b_
        wrong = [(_misalign(a_, b_, op), "lines up the last digits instead of the decimal points")]
        if op == "-":
            wrong.append((a_ + b_, "adds instead of subtracting"))
            wrong.append((_no_borrow(a_, b_), "subtracts the smaller digit from the larger in each column instead of borrowing"))
        else:
            wrong.append((ans * 10, "misplaces the decimal point"))
    else:
        op = "-"
        a_ = Q(rng.choice([10, 12, 15, 20, 25, 30, 40, 50]))
        b_ = _draw(rng, 1, int(a_) - 1, 2)
        ans = a_ - b_
        wrong = [(_no_borrow(a_, b_), "subtracts the smaller digit from the larger in each column instead of borrowing"),
                 (a_ + b_, "adds instead of subtracting"),
                 (ans + 1, "borrows but forgets to reduce the ones digit it borrowed from"),
                 (a_ - (b_ // 1 + 1), f"rounds {m(_d(b_))} up to {m(int(b_ // 1 + 1))} and subtracts; that is only an estimate")]
    P = max(_places(a_), _places(b_))
    A_, B_ = _dp(a_, P), _dp(b_, P)
    sym = "+" if op == "+" else "-"
    steps = [f"Line up the decimal points and fill in zeros so both numbers have {m(P)} decimal places: "
             f"{m(f'{A_} {sym} {B_}')}.",
             f"{'Add' if op == '+' else 'Subtract'} column by column, keeping the point in place: "
             f"{m(f'{A_} {sym} {B_} = {_dp(ans, P)}')}" + (f", which is {m(_d(ans))}." if _places(ans) < P else ".")]
    return Problem(
        stem=choose(rng, f"What is {m(f'{_d(a_)} {sym} {_d(b_)}')}?",
                    f"{'Add' if op == '+' else 'Subtract'}: {m(f'{_d(a_)} {sym} {_d(b_)}')}"),
        answer=ans,
        fmt=dec,
        wrong=wrong,
        steps=steps,
        check=Q(str(D(_d(a_).replace("{,}", "")) + D(_d(b_).replace("{,}", "")) if op == "+"
                    else D(_d(a_).replace("{,}", "")) - D(_d(b_).replace("{,}", "")))),
    )


def _dq(v):
    """sympy Rational -> Decimal (independent check route)."""
    return D(dec_raw(v).replace("{,}", ""))


def _qd(x_):
    return Q(R(str(x_)))


@template("MK")
def multiply_dec(rng, lvl):
    if lvl == 1:
        a_ = R(rng.randint(2, 9), 10)
        b_ = R(rng.randint(2, 9), 10 if rng.random() < 0.6 else 100) if rng.random() < 0.7 else Q(rng.randint(3, 12))
    else:
        a_ = _draw(rng, 1, 9, 1) if rng.random() < 0.5 else R(rng.randint(11, 99), 100)
        b_ = _draw(rng, 1, 5, 1) if rng.random() < 0.6 else R(rng.choice([12, 15, 25, 35, 45, 75]), 10)
    need(a_ != b_)
    ans = a_ * b_
    pa, pb = _places(a_), _places(b_)
    ai, bi = int(a_ * 10 ** pa), int(b_ * 10 ** pb)
    need(_places(ans) <= 4 and ai * bi < 1000)
    tot = pa + pb
    wrong = [(Q(ai * bi), "ignores the decimal points completely")]
    if pa and pb:
        big, bp, other = (a_, pa, b_) if pa >= pb else (b_, pb, a_)
        wrong.append((R(ai * bi, 10 ** bp), f"counts only the decimal place{'s' if bp > 1 else ''} in "
                                            f"{m(_d(big))} and ignores the one{'s' if _places(other) > 1 else ''} "
                                            f"in {m(_d(other))}"))
    wrong += [(ans * 10, "puts one decimal place too few in the answer"),
              (ans / 10, "puts one decimal place too many in the answer"),
              (a_ + b_, "adds instead of multiplying")]
    raw = R(ai * bi, 10 ** tot)
    steps = [f"Ignore the decimal points and multiply: {m(rf'{ai} \times {bi} = {int_raw(ai * bi)}')}.",
             f"Count the decimal places: {m(pa)} in {m(_d(a_))} and {m(pb)} in {m(_d(b_))}, "
             f"{m(tot)} in all."
             if pb else f"{m(_d(a_))} has {m(pa)} decimal place{'s' if pa > 1 else ''}, and {m(_d(b_))} has none.",
             f"Put {m(tot)} decimal place{'s' if tot > 1 else ''} in the product: "
             f"{m(_dp(raw, tot))}" + (f", which is {m(_d(ans))}." if _places(ans) < tot else ".")]
    return Problem(
        stem=choose(rng, f"What is {m(rf'{_d(a_)} \times {_d(b_)}')}?",
                    f"Multiply: {m(rf'{_d(a_)} \times {_d(b_)}')}"),
        answer=ans,
        fmt=dec,
        wrong=wrong,
        steps=steps,
        check=_qd(_dq(a_) * _dq(b_)),
    )


@template("MK")
def divide_dec(rng, lvl):
    if lvl == 1:
        k = rng.randint(2, 9)
        q = _draw(rng, 0.2, 9, 1)
        a_ = q * k
        need(_places(a_) <= 2)
        b_ = Q(k)
        steps = [f"Divide as with whole numbers and put the point in the answer directly above the point "
                 f"in {m(_d(a_))}.",
                 f"{m(rf'{_d(a_)} \div {k} = {_d(q)}')}. Check: {m(rf'{k} \times {_d(q)} = {_d(a_)}')}."]
        wrong = [(q * 10, "drops the decimal point"),
                 (q / 10, "puts the decimal point one place too far left"),
                 (a_ * k, "multiplies instead of dividing")]
    else:
        pb = rng.choice([1, 2])
        b_ = R(rng.randint(2, 9), 10 ** pb)
        q = Q(rng.choice([rng.randint(2, 99), rng.randint(2, 9) * 10]))
        if rng.random() < 0.3:
            q = R(rng.randint(12, 99), 10)
        a_ = q * b_
        need(_places(a_) <= 3 and a_ >= R(1, 10))
        shift = 10 ** pb
        A2, B2 = a_ * shift, b_ * shift
        steps = [f"Make the divisor a whole number: move the decimal point {m(pb)} place{'s' if pb > 1 else ''} "
                 f"to the right in \\emph{{both}} numbers.",
                 f"{m(rf'{_d(a_)} \div {_d(b_)}')} becomes {m(rf'{_d(A2)} \div {_d(B2)}')}.",
                 f"Divide: {m(rf'{_d(A2)} \div {_d(B2)} = {_d(q)}')}. "
                 f"Check: {m(rf'{_d(b_)} \times {_d(q)} = {_d(a_)}')}."]
        wrong = [(q / shift, "moves the decimal point in the divisor but not in the number being divided"),
                 (q * 10, "moves the decimal point in the number being divided one place too many"),
                 (q / 10, "moves the decimal point in the number being divided one place too few"),
                 (a_ * b_, "multiplies instead of dividing")]
    ans = a_ / b_
    need(ans == q)
    return Problem(
        stem=choose(rng, f"What is {m(rf'{_d(a_)} \div {_d(b_)}')}?",
                    f"Divide: {m(rf'{_d(a_)} \div {_d(b_)}')}"),
        answer=ans,
        fmt=dec,
        wrong=wrong,
        steps=steps,
        check=_qd(_dq(a_) / _dq(b_)),
        verify=lambda v: Q(v) * b_ == a_,
    )


@template("MK")
def round_dec(rng, lvl):
    p = rng.choice([1, 2, 2, 0]) if lvl == 1 else rng.choice([1, 2])
    extra = rng.choice([1, 2])
    x_ = _draw(rng, 1, 60, p + extra)
    nxt = int(x_ * 10 ** (p + 1)) % 10
    if lvl == 2 or rng.random() < 0.3:
        # a 9 in the rounding place that carries
        d_here = int(x_ * 10 ** p) % 10
        need(d_here == 9 and nxt >= 5)
    ans = _round(x_, p)
    fmt = _fixed(p)
    trunc = (Q(x_) * 10 ** p).floor() / 10 ** p
    wrong = []
    if trunc != ans:
        wrong.append((trunc, f"drops the extra digits without rounding up (the next digit, {m(nxt)}, is 5 or more)",
                      m(_dp(trunc, p))))
    else:
        up = trunc + R(1, 10 ** p)
        wrong.append((up, f"rounds up even though the next digit, {m(nxt)}, is less than 5", m(_dp(up, p))))
    for q_ in (p - 1, p + 1):
        if 0 <= q_ <= p + extra - 1 and q_ != p:
            v = _round(x_, q_)
            wrong.append((v, f"rounds to the nearest {_PLACE[q_]} instead", m(_dp(v, q_))))
    if p >= 1:
        bad = ans + R(1, 10 ** p)
        wrong.append((bad, None, m(_dp(bad, p))))
    place_word = {0: "ones", 1: "tenths", 2: "hundredths"}[p]
    right_word = {0: "tenths", 1: "hundredths", 2: "thousandths"}[p]
    steps = [f"The {place_word} digit is {m(int(x_ * 10 ** p) % 10)}. The digit to its right "
             f"(the {right_word} digit) is {m(nxt)}.",
             (f"Since {m(nxt)} is 5 or more, round up" if nxt >= 5 else f"Since {m(nxt)} is less than 5, keep the "
              f"{place_word} digit") + f" and drop the digits after it: {m(_dp(ans, p))}."]
    if nxt >= 5 and int(x_ * 10 ** p) % 10 == 9:
        steps[1] = (f"Since {m(nxt)} is 5 or more, round up. The {place_word} digit is 9, so it becomes 0 "
                    f"and you carry 1 to the left: {m(_dp(ans, p))}.")
    return Problem(
        stem=choose(rng, f"Round {m(_d(x_))} to the nearest {_PLACE[p]}.",
                    f"What is {m(_d(x_))} rounded to the nearest {_PLACE[p]}?"),
        answer=ans,
        fmt=fmt,
        wrong=wrong,
        steps=steps,
        check=_qd(_dq(x_).quantize(D(1).scaleb(-p), rounding="ROUND_HALF_UP")),
        near=lambda r: [ans + R(k, 10 ** p) for k in (2, -1, -2, 3)],
    )


@template("MK")
def frac_dec(rng, lvl):
    if rng.random() < 0.55:
        q = rng.choice([4, 5, 8, 20, 25, 40, 50] if lvl == 2 else [2, 4, 5, 10, 20])
        p = rng.choice([k for k in range(1, q) if __import__("math").gcd(k, q) == 1])
        f_ = R(p, q)
        ans = f_
        concat = R(int(f"{p}{q}"), 10 ** len(f"{p}{q}"))
        wrong = [(concat, "just writes the numerator and denominator after the decimal point"),
                 (f_ * 10, "puts the decimal point one place too far right"),
                 (f_ / 10, "puts an extra zero after the decimal point")]
        if (R(q, p) * 1000).is_integer:
            wrong.append((R(q, p), "divides the bottom by the top"))
        steps = [f"A fraction bar means divide: {m(rf'{p} \div {q}')}."]
        if 100 % q == 0:
            k = 100 // q
            steps.append(f"Or scale to hundredths: {m(F(p, q) + ' = ' + F(rf'{p} \times {k}', rf'{q} \times {k}') + ' = ' + F(p * k, 100) + ' = ' + _d(f_))}.")
        elif 1000 % q == 0:
            k = 1000 // q
            steps.append(f"Scale to thousandths: {m(F(p, q) + ' = ' + F(p * k, 1000) + ' = ' + _d(f_))}.")
        steps.append(f"So {m(F(p, q) + ' = ' + _d(f_))}.")
        return Problem(
            stem=choose(rng, f"What is {m(F(p, q))} written as a decimal?",
                        f"Which decimal is equal to {m(F(p, q))}?",
                        f"Convert {m(F(p, q))} to a decimal."),
            answer=ans,
            fmt=dec,
            wrong=wrong,
            steps=steps,
            check=_qd(D(p) / D(q)),
        )
    # decimal -> fraction
    if lvl == 1 or rng.random() < 0.6:
        k = rng.randint(11, 99)
        d_ = R(k, 100)
        need(d_.q < 100 or rng.random() < 0.4)
    else:
        k = rng.choice([125, 375, 625, 875, 25, 75, 175, 225, 275, 325, 425, 475, 525, 575, 675, 725,
                        775, 825, 925, 975, 8, 12, 16, 24, 36, 44, 48, 56])
        d_ = R(k, 1000)
    ans = d_
    pl = _places(d_)
    need(pl >= 2)
    base = 10 ** pl
    wrong = [(d_ * 10, f"reads the last digit as {_DIGIT[pl - 1]} instead of {_DIGIT[pl]}"),
             (d_ / 10, f"reads the last digit as {_DIGIT[pl + 1]} instead of {_DIGIT[pl]}"),
             (1 / d_, "flips the fraction")]
    g = __import__("math").gcd(int(d_ * base), base)
    return Problem(
        stem=choose(rng, f"Which fraction is equal to {m(_d(d_))}?",
                    f"What is {m(_d(d_))} written as a fraction in lowest terms?",
                    f"Convert {m(_d(d_))} to a fraction in simplest form."),
        answer=ans,
        fmt=frac,
        wrong=wrong,
        steps=[f"The last digit is in the {_DIGIT[pl]} place, so {m(_d(d_) + ' = ' + F(int(d_ * base), base))}.",
               (f"Simplify by dividing the top and bottom by {m(g)}: "
                f"{m(F(int(d_ * base), base) + ' = ' + frac_raw(d_))}." if g > 1 else
                f"{m(F(int(d_ * base), base))} is already in lowest terms.")],
        check=Q(R(str(D(_d(d_))))),
    )


@template("MK")
def compare_dec(rng, lvl):
    d1, d2 = rng.sample(range(1, 10), 2)
    pool = {R(d1, 10), R(10 * d1 + d2, 100), R(10 * d2 + d1, 100), R(100 * d1 + d2, 1000),
            R(10 * d1 + d2, 1000), R(d2, 10), R(100 * d2 + d1, 1000)}
    if lvl == 2:
        pool |= {R(d1, 100), R(10 * d1, 1000) + R(d2, 10000)}
    vals = rng.sample(sorted(pool), 4)
    want = rng.choice(["greatest", "least"])
    ans = max(vals) if want == "greatest" else min(vals)
    longest = max(vals, key=lambda v: (_places(v), v))

    def why(v):
        a_s, v_s = _dp(ans, 4)[2:], _dp(v, 4)[2:]
        i = next(j for j in range(4) if a_s[j] != v_s[j])
        place = _DIGIT[i + 1][:-1]
        rel = "less" if want == "greatest" else "greater"
        w = (f"is {rel} than {m(_d(ans))}: in the {place}s place it has {m(v_s[i])}, while "
             f"{m(_d(ans))} has {m(a_s[i])}")
        if v == longest and want == "greatest" and _places(v) > _places(ans):
            w = "has more digits, but it " + w
        return w
    wrong = [(v, why(v)) for v in vals if v != ans]
    padded = ", ".join(m(_dp(v, 3 if lvl == 1 else max(_places(x) for x in vals))) for v in vals)
    return Problem(
        stem=choose(rng, f"Which of the numbers {', '.join(m(_d(v)) for v in vals[:-1])}, and {m(_d(vals[-1]))} is the {want}?",
                    f"Which is the {want}: {', '.join(m(_d(v)) for v in vals[:-1])}, or {m(_d(vals[-1]))}?"),
        answer=ans,
        fmt=dec,
        wrong=wrong,
        steps=[f"Give every number the same number of decimal places by adding zeros: {padded}.",
               f"Now compare them like whole numbers. In order from "
               f"{'greatest to least' if want == 'greatest' else 'least to greatest'}: "
               f"{m(' > '.join(_d(v) for v in sorted(vals, reverse=True)) if want == 'greatest' else ' < '.join(_d(v) for v in sorted(vals)))}.",
               f"The {want} is {m(_d(ans))}."],
        check=_qd(max(_dq(v) for v in vals) if want == "greatest" else min(_dq(v) for v in vals)),
        sort=False,
        near=lambda r: [],
    )


# --------------------------------------------------------------------------
# word problems (money)
# --------------------------------------------------------------------------

_UNIT_ITEMS = [
    ("Gas costs {P} per gallon. How much do {N} gallons cost?", (299, 489), (8, 18)),
    ("Apples cost {P} per pound. How much do {N} pounds of apples cost?", (119, 299), (3, 9)),
    ("At the base exchange, energy drinks cost {P} each. How much do {N} energy drinks cost?", (189, 349), (4, 12)),
    ("A movie ticket costs {P}. How much do {N} tickets cost?", (899, 1499), (3, 8)),
    ("Notebooks cost {P} each. How much do {N} notebooks cost?", (129, 389), (4, 12)),
    ("A sports drink costs {P}. How much do {N} sports drinks cost?", (119, 249), (6, 15)),
]


@template("AR")
def money_mult(rng, lvl):
    if lvl == 1:
        tpl, (plo, phi), (nlo, nhi) = rng.choice(_UNIT_ITEMS)
        pc = rng.randint(plo, phi)
        need(pc % 10 != 0)
        price = R(pc, 100)
        n_ = rng.randint(nlo, nhi)
        ans = price * n_
        dollars = int(price)
        cents = price - dollars
        return Problem(
            stem=tpl.format(P=money_cents(price), N=m(n_)),
            answer=ans,
            fmt=money,
            wrong=[(Q(dollars * n_) + cents, "multiplies only the dollars and then tacks on the cents"),
                   (ans * 10, "misplaces the decimal point"),
                   (price + n_, "adds instead of multiplying"),
                   (ans + 1, None), (ans - 1, None)],
            steps=[f"Multiply the price by the number: {m(rf'{_d(price)} \times {n_}')}.",
                   f"Split it up: {m(rf'{dollars} \times {n_} = {dollars * n_}')} and "
                   f"{m(rf'{_dp(cents, 2)} \times {n_} = {_dp(cents * n_, 2)}')}.",
                   f"Add: {m(f'{dollars * n_} + {_dp(cents * n_, 2)} = {_dp(ans, 2)}')}, so the cost is {money(ans)}."],
            tip=(f"Estimate: {money(price)} is about {money(_round(price * 2, 0) / 2)}, and "
                 f"{m(rf'{_d(_round(price * 2, 0) / 2)} \times {n_} = {_d(_round(price * 2, 0) / 2 * n_)}')}, "
                 f"so the answer is near {money(_round(price * 2, 0) / 2 * n_)}."),
            check=_qd(_dq(price) * n_),
            near=_near_cents(ans),
        )
    if lvl == 2:
        (i1, l1, h1), (i2, l2, h2) = rng.sample([("notebooks", 125, 395), ("pens", 85, 175), ("folders", 45, 125),
                                                 ("bottles of water", 99, 189), ("granola bars", 75, 149),
                                                 ("candy bars", 89, 179), ("rolls of tape", 199, 449)], 2)
        q1, q2 = rng.randint(2, 6), rng.randint(2, 6)
        p1, p2 = R(rng.randint(l1, h1), 100), R(rng.randint(l2, h2), 100)
        need(q1 != q2 and (p1 * 100) % 5 == 0 and (p2 * 100) % 5 == 0 and p1.q != 1 and p2.q != 1)
        ans = q1 * p1 + q2 * p2
        who = rng.choice([person(rng).name, soldier(rng)])
        return Problem(
            stem=(f"{who} buys {m(q1)} {i1} at {money_cents(p1)} each and {m(q2)} {i2} at "
                  f"{money_cents(p2)} each. What is the total cost?"),
            answer=ans,
            fmt=money,
            wrong=[(p1 + p2, "adds one of each price and ignores the quantities"),
                   (q1 * p1 + p2, f"forgets to multiply the second price by {m(q2)}"),
                   ((q1 + q2) * max(p1, p2), "charges every item at the higher price"),
                   (ans + 1, None)],
            steps=[f"First item: {m(rf'{q1} \times {_dp(p1, 2)} = {_dp(q1 * p1, 2)}')}.",
                   f"Second item: {m(rf'{q2} \times {_dp(p2, 2)} = {_dp(q2 * p2, 2)}')}.",
                   f"Total: {m(f'{_dp(q1 * p1, 2)} + {_dp(q2 * p2, 2)} = {_dp(ans, 2)}')}, so {money_cents(ans)}."],
            check=_qd(q1 * _dq(p1) + q2 * _dq(p2)),
            near=_near_cents(ans),
        )
    (i1, l1, h1), (i2, l2, h2) = rng.sample([("chicken", 249, 449), ("ground beef", 399, 599), ("cheese", 349, 699),
                                             ("grapes", 199, 349), ("shrimp", 799, 1199), ("turkey", 499, 899)], 2)
    w1 = R(rng.choice([15, 25, 35, 5, 45]), 10)
    w2 = R(rng.choice([15, 25, 5]), 10) if rng.random() < 0.5 else Q(rng.randint(2, 4))
    p1 = R(rng.randint(l1 // 10, h1 // 10) * 10, 100)
    p2 = R(rng.randint(l2 // 10, h2 // 10) * 10, 100)
    c1, c2 = w1 * p1, w2 * p2
    need((c1 * 100).is_integer and (c2 * 100).is_integer and w1 != w2)
    ans = c1 + c2
    p = person(rng)
    return Problem(
        stem=(f"{p.name} buys {m(_d(w1))} pounds of {i1} at {money_cents(p1)} per pound and {m(_d(w2))} "
              f"pound{'' if w2 == R(1, 2) else 's'} of {i2} at {money_cents(p2)} per pound. How much does {p.he} spend?"),
        answer=ans,
        fmt=money,
        wrong=[(c1 * 10 + c2, f"misplaces the decimal point in {m(rf'{_d(w1)} \times {_dp(p1, 2)}')}"),
               ((w1 + w2) * p1, "uses the first price for both items"),
               (w1 + p1 + w2 + p2, "adds the weights and prices instead of multiplying"),
               (c1 + c2 * 10 if c2 * 10 != c1 * 10 + c2 else ans + 2, None)],
        steps=[f"First item: {m(rf'{_d(w1)} \times {_dp(p1, 2)} = {_dp(c1, 2)}')}.",
               f"Second item: {m(rf'{_d(w2)} \times {_dp(p2, 2)} = {_dp(c2, 2)}')}.",
               f"Total: {m(f'{_dp(c1, 2)} + {_dp(c2, 2)} = {_dp(ans, 2)}')}, so {money_cents(ans)}."],
        tip=(f"For {m(rf'{_d(w1)} \times {_dp(p1, 2)}')}, think {m(rf'{int(w1)} \times {_dp(p1, 2)}')} plus "
             f"half of {money_cents(p1)}." if w1 > 1 and w1 - int(w1) == R(1, 2) else None),
        check=_qd(_dq(w1) * _dq(p1) + _dq(w2) * _dq(p2)),
        near=_near_cents(ans),
    )


_STORE = [("a sandwich", "sandwiches", 499, 899), ("a bag of chips", "bags of chips", 129, 249),
          ("a drink", "drinks", 149, 299), ("a magazine", "magazines", 399, 699),
          ("a pack of gum", "packs of gum", 99, 199), ("a phone charger", "phone chargers", 899, 1499),
          ("a bottle of sunscreen", "bottles of sunscreen", 599, 999), ("a pair of socks", "pairs of socks", 349, 799),
          ("a notebook", "notebooks", 199, 399), ("a pen", "pens", 89, 189)]


@template("AR")
def change_from_bill(rng, lvl):
    if lvl == 1:
        items = rng.sample(_STORE[:8], 2)
        prices = [R(rng.randint(lo, hi), 100) for _, _, lo, hi in items]
        need(all(x_.q != 1 for x_ in prices))
        total = sum(prices)
        bill = rng.choice([b for b in (10, 20) if b > total + 1] or [0])
        need(bill > 0)
        desc = f"{items[0][0]} for {money_cents(prices[0])} and {items[1][0]} for {money_cents(prices[1])}"
        qtxt = None
    else:
        (_, n1, l1, h1), (_, n2, l2, h2) = rng.sample([_STORE[i] for i in (0, 1, 2, 3, 4, 8, 9)], 2)
        q1, q2 = rng.randint(2, 4), rng.randint(2, 3)
        p1, p2 = R(rng.randint(l1, h1), 100), R(rng.randint(l2, h2), 100)
        need(p1.q != 1 and p2.q != 1)
        prices = [q1 * p1, q2 * p2]
        total = sum(prices)
        bill = next(b for b in (20, 50, 100) if b > total + 1)
        desc = f"{m(q1)} {n1} at {money_cents(p1)} each and {m(q2)} {n2} at {money_cents(p2)} each"
        qtxt = (q1, p1, q2, p2)
    who = person(rng)
    change = bill - total
    nb = _no_borrow(Q(bill), total)
    wrong = [(total, "is the total cost, not the change"),
             (bill - prices[0], "subtracts only the first item")]
    if nb != change:
        wrong.append((nb, "subtracts the smaller digit from the larger in each column instead of borrowing"))
    if qtxt:
        wrong.append((bill - qtxt[1] - qtxt[3], "subtracts one of each price and ignores the quantities"))
    wrong.append((change + 1, None))
    steps = []
    if qtxt:
        q1, p1, q2, p2 = qtxt
        steps.append(f"Cost of each kind: {m(rf'{q1} \times {_dp(p1, 2)} = {_dp(q1 * p1, 2)}')} and "
                     f"{m(rf'{q2} \times {_dp(p2, 2)} = {_dp(q2 * p2, 2)}')}.")
    steps.append(f"Total: {m(f'{_dp(prices[0], 2)} + {_dp(prices[1], 2)} = {_dp(total, 2)}')}.")
    steps.append(f"Change: {m(f'{bill}.00 - {_dp(total, 2)} = {_dp(change, 2)}')}, so {money_cents(change)}.")
    return Problem(
        stem=(f"{who.name} buys {desc}. {who.He} pays with a {money(bill)} bill. How much change "
              f"should {who.he} get back?"),
        answer=change,
        fmt=money_cents,
        wrong=wrong,
        steps=steps,
        tip=(f"Count up from {money_cents(total)}: to the next dollar, then to {money(bill)}."),
        check=_qd(D(bill) - sum(_dq(x_) for x_ in prices)),
        near=_near_cents(change),
    )


_PACKS = [("A {N}-pack of soda costs {P}.", "can", (6, 8, 12, 24)),
          ("A box of {N} granola bars costs {P}.", "bar", (6, 8, 10, 12)),
          ("A package of {N} AA batteries costs {P}.", "battery", (4, 8, 12, 16)),
          ("A case of {N} bottles of water costs {P}.", "bottle", (12, 24, 32)),
          ("A pack of {N} pairs of boot socks costs {P}.", "pair", (3, 4, 5, 6))]


@template("AR")
def unit_price(rng, lvl):
    if lvl == 2:
        tpl, item, ns = rng.choice(_PACKS)
        n_ = rng.choice(ns)
        each = R(rng.randint(15, 299 if item == "pair" else 149), 100)
        if rng.random() < 0.5:
            each = R(rng.randint(2, 29 if item == "pair" else 14), 10)
        tot = each * n_
        need(tot < 40 and each.q != 1)
        return Problem(
            stem=tpl.format(N=n_ if "-pack" in tpl else m(n_), P=money_cents(tot))
            + f" What is the price per {item}?",
            answer=each,
            fmt=money_cents,
            wrong=[(each * 10, "puts the decimal point one place too far right"),
                   (tot - n_, f"subtracts {m(n_)} instead of dividing by it"),
                   (each / 10, "puts the decimal point one place too far left"),
                   (Q(n_) / tot, "divides the number of items by the price")],
            steps=[f"Price per {item} {m('=')} total price {m(r'\div')} number of {item}s."
                   .replace("batterys", "batteries"),
                   f"{m(rf'{_dp(tot, 2)} \div {n_} = {_dp(each, 2)}')}. Check: "
                   f"{m(rf'{n_} \times {_dp(each, 2)} = {_dp(tot, 2)}')}."],
            check=_qd(_dq(tot) / n_),
            near=_near_cents(each, (R(1, 100), R(5, 100), R(10, 100))),
        )
    item, n1, n2, lo, hi = rng.choice([("can of soda", 6, 8, 40, 90), ("bottle of water", 12, 24, 20, 60),
                                       ("granola bar", 5, 8, 40, 99), ("battery", 4, 10, 50, 150),
                                       ("pound of rice", 2, 5, 90, 199)])
    e1 = R(rng.randint(lo, hi), 100)
    e2 = R(rng.randint(lo, hi), 100)
    need(e1 != e2 and abs(e1 - e2) <= R(30, 100))
    t1, t2 = e1 * n1, e2 * n2
    need(t1 != t2 and (t1 * 100).is_integer and (t2 * 100).is_integer)
    diff = abs(e1 - e2)
    cheaper = "A" if e1 < e2 else "B"
    plural = {"can of soda": "cans of soda", "bottle of water": "bottles of water", "granola bar": "granola bars",
              "battery": "batteries", "pound of rice": "pounds of rice"}[item]
    pk = "bag" if "rice" in item else "pack"
    unit_w = item.split(' of ')[0] if 'rice' not in item else 'pound'
    setup = (f"Store A sells a {pk} of {m(n1)} {plural} for {money_cents(t1)}. Store B sells a {pk} of "
             f"{m(n2)} {plural} for {money_cents(t2)}.")
    if rng.random() < 0.4:
        lo_e = min(e1, e2)
        return Problem(
            stem=f"{setup} What is the lower price per {unit_w}?",
            answer=lo_e,
            fmt=money_cents,
            wrong=[(max(e1, e2), f"is the higher of the two prices per {unit_w}"),
                   (diff, f"is the difference between the prices per {unit_w}"),
                   (min(t1, t2), f"is the cheaper {pk} price, not the price per {unit_w}"),
                   (lo_e * 10, "misplaces the decimal point")],
            steps=[f"Store A: {m(rf'{_dp(t1, 2)} \div {n1} = {_dp(e1, 2)}')} per {unit_w}.",
                   f"Store B: {m(rf'{_dp(t2, 2)} \div {n2} = {_dp(e2, 2)}')} per {unit_w}.",
                   f"The lower price is at Store {cheaper}: {money_cents(lo_e)} per {unit_w}."],
            check=_qd(min(_dq(t1) / n1, _dq(t2) / n2)),
            near=_near_cents(lo_e, (R(1, 100), R(2, 100), R(5, 100))),
        )
    return Problem(
        stem=f"{setup} How much less is the price per {unit_w} at the cheaper store?",
        answer=diff,
        fmt=money_cents,
        wrong=[(abs(t1 - t2), f"compares the {pk} prices instead of the prices per {unit_w}"),
               (min(e1, e2), f"is the price per {unit_w} at the cheaper store, not the difference"),
               (max(e1, e2), f"is the price per {unit_w} at the more expensive store"),
               (diff * 10, "misplaces the decimal point")],
        steps=[f"Store A: {m(rf'{_dp(t1, 2)} \div {n1} = {_dp(e1, 2)}')} per {unit_w}.",
               f"Store B: {m(rf'{_dp(t2, 2)} \div {n2} = {_dp(e2, 2)}')} per {unit_w}.",
               f"Store {cheaper} is cheaper by {m(f'{_dp(max(e1, e2), 2)} - {_dp(min(e1, e2), 2)} = {_dp(diff, 2)}')}, "
               f"or {money_cents(diff)} per {unit_w}."],
        check=_qd(abs(_dq(t1) / n1 - _dq(t2) / n2)),
        near=_near_cents(diff, (R(1, 100), R(2, 100), R(5, 100))),
    )


@template("AR")
def paycheck(rng, lvl):
    rate = R(rng.randint(22, 44) * 50, 100)       # $11.00 - $22.00 in 50-cent steps
    reg = 40
    ot = rng.randint(2, 8)
    ot_rate = rate * R(3, 2)
    need((ot_rate * 100).is_integer)
    base = rate * reg
    extra = ot_rate * ot
    ans = base + extra
    p = person(rng)
    job = rng.choice(["at a warehouse", "at a hardware store", "as a security guard", "at a restaurant",
                      "on a construction crew"])
    return Problem(
        stem=(f"{p.name} works {job} and earns {money_cents(rate)} per hour for the first {m(reg)} hours each "
              f"week. Every hour over {m(reg)} is overtime and pays {m(_d(R(3, 2)))} times the regular rate. "
              f"Last week {p.he} worked {m(reg + ot)} hours. How much did {p.he} earn?"),
        answer=ans,
        fmt=money,
        wrong=[(rate * (reg + ot), "pays the overtime hours at the regular rate"),
               (base, "leaves out the overtime pay"),
               (base + (rate + R(3, 2)) * ot, f"adds {m(_d(R(3, 2)))} dollars to the rate instead of multiplying by {m(_d(R(3, 2)))}"),
               (ot_rate * (reg + ot), "pays every hour at the overtime rate")],
        steps=[f"Regular pay: {m(rf'{reg} \times {_dp(rate, 2)} = {_dp(base, 2)}')}.",
               f"Overtime rate: {m(rf'1.5 \times {_dp(rate, 2)} = {_dp(ot_rate, 2)}')} per hour.",
               f"Overtime pay: {m(rf'{ot} \times {_dp(ot_rate, 2)} = {_dp(extra, 2)}')}.",
               f"Total: {m(f'{_dp(base, 2)} + {_dp(extra, 2)} = {_dp(ans, 2)}')}, so {money(ans)}."],
        check=_qd(D(reg) * _dq(rate) + D(ot) * _dq(rate) * D("1.5")),
        near=_near_cents(ans, (R(1), R(5), R(10))),
    )


@template("AR")
def mpg(rng, lvl):
    veh, rlo, rhi, glo, ghi = rng.choice([("A car", 24, 38, 80, 160), ("A pickup truck", 15, 24, 120, 260),
                                          ("A Humvee", 9, 14, 150, 250), ("A delivery van", 12, 20, 120, 260),
                                          ("A motorcycle", 36, 52, 30, 55)])
    g = R(rng.randint(glo, ghi), 10)
    need(g.q != 1 and (g - int(g)) <= R(3, 10))
    rate = rng.randint(rlo, rhi)
    miles = g * rate
    need(_places(miles) <= 1)
    Dm, Gm = int(miles * 10), int(g * 10)
    tens, ones = rate // 10 * 10, rate % 10
    return Problem(
        stem=(f"{veh} traveled {m(_d(miles))} miles on {m(_d(g))} gallons of fuel. How many miles per gallon "
              "did it get?"),
        answer=Q(rate),
        fmt=unit(dec, "mile per gallon", "miles per gallon"),
        wrong=[(Q(rate) / 10, "moves the decimal point in the gallons but not in the miles"),
               (Q(rate) * 10, "moves the decimal point in the miles but not in the gallons"),
               (miles - g, "subtracts instead of dividing"),
               (Q(rate + 2), None), (Q(rate - 2), None)],
        steps=[f"Miles per gallon {m('=')} miles {m(r'\div')} gallons: {m(rf'{_d(miles)} \div {_d(g)}')}.",
               f"Move the decimal point one place to the right in both numbers: {m(rf'{_n(Dm)} \div {Gm}')}.",
               (f"Divide: {m(rf'{Gm} \times {tens} = {_n(Gm * tens)}')}, and "
                f"{m(f'{_n(Dm)} - {_n(Gm * tens)} = {_n(Dm - Gm * tens)}')}, which is "
                f"{m(rf'{Gm} \times {ones}')}. So {m(rf'{_n(Dm)} \div {Gm} = {tens} + {ones} = {rate}')} "
                "miles per gallon."
                if tens and ones else
                f"Divide: {m(rf'{Gm} \times {rate} = {_n(Dm)}')}, so {m(rf'{_n(Dm)} \div {Gm} = {rate}')} "
                "miles per gallon.")],
        check=_qd(_dq(miles) / _dq(g)),
        near=lambda r: [Q(rate + d) for d in (1, -1, 2, -2, 3)],
    )


PLAN = [
    # (template, level, count)  -- easy -> hard; 25 problems
    (add_sub_dec, 1, 2),
    (multiply_dec, 1, 1),
    (divide_dec, 1, 1),
    (round_dec, 1, 2),
    (money_mult, 1, 1),
    (change_from_bill, 1, 1),
    (add_sub_dec, 2, 1),
    (multiply_dec, 2, 1),
    (divide_dec, 2, 2),
    (frac_dec, 2, 2),
    (compare_dec, 2, 2),
    (money_mult, 2, 1),
    (unit_price, 2, 1),
    (unit_price, 3, 2),
    (paycheck, 3, 2),
    (mpg, 3, 1),
    (money_mult, 3, 1),
    (change_from_bill, 3, 1),
]
