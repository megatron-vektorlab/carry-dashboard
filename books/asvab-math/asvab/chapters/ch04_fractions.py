"""Chapter 4 - Fractions & Mixed Numbers."""
import math
from fractions import Fraction as Fr

from ..core import (R, Q, Problem, need, num, frac, mixed, money, text, m, F,
                    int_raw, frac_raw, mixed_raw, unit, person, soldier, choose, template)

NUM = 4
TITLE = r"Fractions \& Mixed Numbers"
PART = 1

INTRO = r"""
Fractions are everywhere on the ASVAB: in recipes, distances, shares of a
budget, and parts of a group. Every fraction skill comes down to a few
moves done carefully, one step at a time.

\begin{concept}{Simplifying and comparing}
Divide the top and bottom by their greatest common factor:
$\frac{18}{24} = \frac{18 \div 6}{24 \div 6} = \frac{3}{4}$.
Multiplying the top and bottom by the same number gives an
\emph{equivalent} fraction: $\frac{3}{4} = \frac{15}{20}$.
To compare, rewrite over a common denominator:
$\frac{2}{3} = \frac{8}{12}$ and $\frac{3}{4} = \frac{9}{12}$, so
$\frac{3}{4}$ is larger.
\end{concept}

\begin{concept}{The four operations}
\begin{itemize}
\item \textbf{Add/subtract:} common denominator first, then combine the
  numerators: $\frac{1}{4} + \frac{2}{3} = \frac{3}{12} + \frac{8}{12} = \frac{11}{12}$.
\item \textbf{Multiply:} top times top, bottom times bottom (cancel first):
  $\frac{4}{9} \times \frac{3}{8} = \frac{1}{3} \times \frac{1}{2} = \frac{1}{6}$.
\item \textbf{Divide:} keep the first, flip the \emph{second}, multiply:
  $\frac{2}{3} \div \frac{4}{5} = \frac{2}{3} \times \frac{5}{4} = \frac{5}{6}$.
\end{itemize}
\end{concept}

\begin{concept}{Mixed numbers}
$3\frac{2}{5} = \frac{3 \times 5 + 2}{5} = \frac{17}{5}$. To add or subtract,
work with the whole numbers and the fractions; when the top fraction is too
small, \emph{regroup}: $5\frac{1}{4} = 4\frac{5}{4}$. To multiply or divide,
change to improper fractions first.
\end{concept}

\begin{example}{Worked example}
Maria spent $\frac{1}{3}$ of her \$1{,}200 paycheck on rent and then
$\frac{1}{4}$ of what was left on groceries. How much money does she have now?

\textbf{Solution.} Rent: $\frac{1}{3} \times 1{,}200 = 400$, leaving
$800$. Groceries: $\frac{1}{4}$ of $800$ is $200$, leaving
$800 - 200 = \$600$.
\end{example}

\begin{tip}
To find a fraction of a number, divide by the bottom, then multiply by the
top: $\frac{3}{8}$ of $32$ is $32 \div 8 = 4$, then $4 \times 3 = 12$.
\end{tip}

\begin{trap}
\begin{itemize}
\item Adding tops and bottoms: $\frac{1}{2} + \frac{1}{3}$ is $\frac{5}{6}$, not $\frac{2}{5}$.
\item Flipping the wrong fraction when dividing (flip the second one only).
\item Taking the second fraction of the \emph{original} amount instead of
  what was left.
\item Forgetting to take $1$ from the whole number when you regroup.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _fx(v):
    """sympy Rational -> fractions.Fraction (for independent checks)."""
    v = Q(v)
    return Fr(int(v.p), int(v.q))


def _Fi(p, q):
    """Unsimplified fraction, but n/1 shown as n (after cancelling)."""
    return str(p) if q == 1 else F(p, q)


def _near_int(v):
    def f(r):
        out = [Q(v) + d for d in (1, -1, 2, -2, 3, 4)]
        out = [w for w in out if w > 0]
        r.shuffle(out)
        return out
    return f


def _sy(f):
    return R(f.numerator, f.denominator)


def _mx(v):
    return mixed_raw(v)


def _fr(v):
    return frac_raw(v)


def _improper(v):
    """Raw LaTeX of v as an improper fraction (or integer)."""
    v = Q(v)
    return frac_raw(v)


def _lcd(*qs):
    return math.lcm(*qs)


def _to_mixed_step(v):
    """'= 17/12 = 1 5/12' tail when v is improper, else ''."""
    v = Q(v)
    if v.q != 1 and abs(v) > 1:
        return f" = {_mx(v)}"
    return ""


def _proper(rng, dens, lo=1):
    q = rng.choice(dens)
    p = rng.randint(lo, q - 1)
    need(math.gcd(p, q) == 1)
    return R(p, q)


def _flist(fs, conj="and"):
    parts = [m(_fr(f)) for f in fs]
    return ", ".join(parts[:-1]) + f", {conj} " + parts[-1]


# --------------------------------------------------------------------------
# simplifying, equivalent fractions, comparing
# --------------------------------------------------------------------------

@template("MK")
def simplify(rng, lvl):
    v = _proper(rng, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    p, q = int(v.p), int(v.q)
    k = rng.choice([2, 3, 4, 5, 6, 8, 9, 10, 12])
    a_, b_ = p * k, q * k
    need(b_ <= 120)
    ans = m(F(p, q))
    wrong = [(m(F(q, p)), "flips the fraction")] if p > 1 else []
    wrong.append((m(F(p, b_)), f"divides only the top by {m(k)}"))
    ds = [d for d in range(2, k) if k % d == 0]
    if ds:
        d = rng.choice(ds)
        wrong.append((m(F(a_ // d, b_ // d)),
                      f"is equal to {m(F(a_, b_))}, but not in lowest terms: {m(a_ // d)} and "
                      f"{m(b_ // d)} still share a factor of {m(k // d)}"))
    for alt in (R(p + 1, q), R(p, q + 1), R(p - 1, q) if p > 1 else None, R(p, q - 1) if q - 1 > p else None):
        if alt is not None and alt != v and alt < 1 and alt.q > 1:
            wrong.append((m(_fr(alt)), None))
    return Problem(
        stem=choose(rng, f"Simplify {m(F(a_, b_))} to lowest terms.",
                    f"What is {m(F(a_, b_))} in simplest form?",
                    f"Which fraction is equal to {m(F(a_, b_))} and in lowest terms?"),
        answer=ans,
        fmt=text,
        wrong=wrong,
        steps=[
            f"Find the greatest common factor of {m(a_)} and {m(b_)}: it is {m(k)}.",
            f"Divide the top and bottom by {m(k)}: "
            f"{m(F(a_, b_) + ' = ' + F(rf'{a_} \div {k}', rf'{b_} \div {k}') + ' = ' + F(p, q))}.",
        ],
        tip=(f"You can also divide in smaller steps (for example by {m(ds[0])} first); just keep "
             "going until the top and bottom share no factor." if ds else None),
        check=m(F(Fr(a_, b_).numerator, Fr(a_, b_).denominator)),
    )


@template("MK")
def equivalent(rng, lvl):
    v = _proper(rng, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    p, q = int(v.p), int(v.q)
    k = rng.randint(2, 9)
    if rng.random() < 0.5:
        ans = m(F(p * k, q * k))
        cands = [(F(p + k, q + k), "adds the same number to the top and bottom instead of multiplying",
                  Fr(p + k, q + k)),
                 (F(q * k, p * k), f"is equal to {m(F(q, p))}, the fraction flipped", Fr(q, p)),
                 (F(p * k, q), "multiplies only the numerator", Fr(p * k, q)),
                 (F(p * k, q + k), "multiplies the top but adds to the bottom", Fr(p * k, q + k))]
        wrong = [(m(t), w) for t, w, val in cands if val != Fr(p, q)]
        return Problem(
            stem=choose(rng, f"Which fraction is equivalent to {m(F(p, q))}?",
                        f"Which of the following is equal to {m(F(p, q))}?"),
            answer=ans,
            fmt=text,
            wrong=wrong,
            steps=[
                "Multiplying the top and bottom by the same number does not change a fraction's value.",
                f"{m(F(p, q) + ' = ' + F(rf'{p} \times {k}', rf'{q} \times {k}') + ' = ' + F(p * k, q * k))}.",
            ],
            verify=lambda s: Fr(p * k, q * k) == Fr(p, q) and s == ans,
        )
    N = q * k
    ans = Q(p * k)
    return Problem(
        stem=choose(rng, f"If {m(F(p, q) + ' = ' + F('x', N))}, what is the value of {m('x')}?",
                    f"What number goes in the box? {m(F(p, q) + ' = ' + F(r'\square', N))}"),
        answer=ans,
        fmt=num,
        wrong=[(Q(p + N - q), f"adds {m(N - q)} to the top because {m(N - q)} was added to the bottom; "
                              "you must multiply, not add"),
               (Q(k), f"stops after finding {m(rf'{N} \div {q} = {k}')}"),
               (Q(p * N), f"multiplies {m(p)} by {m(N)} without dividing by {m(q)}"),
               (ans + 1, None), (ans - 1, None)],
        steps=[
            f"The bottom changed from {m(q)} to {m(N)}: {m(rf'{N} \div {q} = {k}')}, so it was multiplied by {m(k)}.",
            f"Multiply the top by the same number: {m(rf'{p} \times {k} = {p * k}')}.",
        ],
        verify=lambda x_: Fr(int(x_), N) == Fr(p, q),
    )


@template("MK")
def compare(rng, lvl):
    want = rng.choice(["largest", "smallest"])
    dens = [2, 3, 4, 5, 6, 8, 10, 12] if lvl == 1 else [3, 4, 5, 6, 7, 8, 9, 10, 12, 15]
    fs = []
    while len(fs) < 4:
        f_ = _proper(rng, dens)
        if f_ not in fs:
            fs.append(f_)
    L = _lcd(*[int(f_.q) for f_ in fs])
    need(L <= (24 if lvl == 1 else 60))
    ans = max(fs) if want == "largest" else min(fs)
    numer = {f_: int(f_ * L) for f_ in fs}
    big_num = max(fs, key=lambda f_: (f_.p, f_.q))
    wrong = []
    for f_ in fs:
        if f_ == ans:
            continue
        cmp = "less" if want == "largest" else "more"
        why = f"equals {m(F(numer[f_], L))}, which is {cmp} than {m(F(numer[ans], L))}"
        if f_ == big_num and want == "largest":
            why = "has the largest numerator, but it " + why
        wrong.append((f_, why))
    rewrite = ", ".join(m(f"{_fr(f_)} = {F(numer[f_], L)}") for f_ in fs)
    return Problem(
        stem=choose(rng, f"Which of the fractions {_flist(fs)} is the {want}?",
                    f"Which is the {want}: {_flist(fs, 'or')}?"),
        answer=ans,
        fmt=frac,
        wrong=wrong,
        steps=[
            f"Rewrite each fraction with the common denominator {m(L)}: {rewrite}.",
            f"The {'largest' if want == 'largest' else 'smallest'} numerator is {m(numer[ans])}, "
            f"so {m(_fr(ans))} is the {want}.",
        ],
        check=_sy(max(_fx(f_) for f_ in fs) if want == "largest" else min(_fx(f_) for f_ in fs)),
        sort=False,
        near=lambda r: [],
    )


# --------------------------------------------------------------------------
# operations
# --------------------------------------------------------------------------

def _add_steps(f1, f2, op):
    L = _lcd(int(f1.q), int(f2.q))
    n1, n2 = int(f1 * L), int(f2 * L)
    res = f1 + f2 if op == "+" else f1 - f2
    raw = F(n1 + n2 if op == "+" else n1 - n2, L)
    steps = [f"The least common denominator of {m(f1.q)} and {m(f2.q)} is {m(L)}."]
    if L in (f1.q, f2.q) and f1.q != f2.q:
        steps[0] = (f"{m(L)} is a multiple of {m(min(f1.q, f2.q))}, so use {m(L)} as the common "
                    "denominator.")
    if f1.q == L:
        steps.append(f"Rewrite {m(_fr(f2))} with denominator {m(L)}: {m(f'{_fr(f2)} = {F(n2, L)}')}.")
    elif f2.q == L:
        steps.append(f"Rewrite {m(_fr(f1))} with denominator {m(L)}: {m(f'{_fr(f1)} = {F(n1, L)}')}.")
    else:
        steps.append(f"Rewrite: {m(f'{_fr(f1)} = {F(n1, L)}')} and {m(f'{_fr(f2)} = {F(n2, L)}')}.")
    tail = ""
    if Q(res).q != L or abs(res) > 1:
        tail = f" = {_fr(res)}" if Q(res).q != L else ""
        tail += _to_mixed_step(res) if abs(res) > 1 else ""
    steps.append(f"{'Add' if op == '+' else 'Subtract'} the numerators: "
                 f"{m(f'{F(n1, L)} {op} {F(n2, L)} = {raw}{tail}')}.")
    return steps, res, L, n1, n2


@template("MK")
def add_sub(rng, lvl):
    op = rng.choice(["+", "-"])
    if lvl == 1:
        d1 = rng.choice([2, 3, 4, 5, 6])
        d2 = d1 * rng.choice([2, 3, 4])
        need(d2 <= 16)
        f1, f2 = _proper(rng, [d1]), _proper(rng, [d2])
        if rng.random() < 0.5:
            f1, f2 = f2, f1
    else:
        f1, f2 = _proper(rng, [3, 4, 5, 6, 7, 8, 9, 10, 12]), _proper(rng, [3, 4, 5, 6, 7, 8, 9, 10, 12])
        need(f1.q != f2.q and math.gcd(int(f1.q), int(f2.q)) < min(f1.q, f2.q) and _lcd(int(f1.q), int(f2.q)) <= 40)
    if op == "-" and f1 < f2:
        f1, f2 = f2, f1
    steps, res, L, n1, n2 = _add_steps(f1, f2, op)
    need(res != 0 and f1.q != f2.q)
    a_, b_, c_, d_ = int(f1.p), int(f1.q), int(f2.p), int(f2.q)
    wrong = []
    if op == "+":
        wrong.append((R(a_ + c_, b_ + d_), "adds the numerators and adds the denominators"))
        wrong.append((R(a_ + c_, L), "uses the common denominator without rewriting the numerators"))
        wrong.append((f1 - f2 if f1 > f2 else f2 - f1, "subtracts instead of adding"))
    else:
        if b_ != d_ and a_ - c_ > 0 and b_ - d_ > 0:
            wrong.append((R(a_ - c_, b_ - d_), "subtracts the numerators and subtracts the denominators"))
        if a_ - c_ > 0:
            wrong.append((R(a_ - c_, L), "uses the common denominator without rewriting the numerators"))
        wrong.append((f1 + f2, "adds instead of subtracting"))
    wrong.append((res + R(1, L), None))
    if res - R(1, L) > 0:
        wrong.append((res - R(1, L), None))
    return Problem(
        stem=choose(rng, f"What is {m(f'{_fr(f1)} {op} {_fr(f2)}')}?",
                    f"{'Add' if op == '+' else 'Subtract'}: {m(f'{_fr(f1)} {op} {_fr(f2)}')}"),
        answer=res,
        fmt=mixed,
        wrong=wrong,
        steps=steps,
        check=_sy(_fx(f1) + _fx(f2) if op == "+" else _fx(f1) - _fx(f2)),
    )


def _cancel_steps(a_, b_, c_, d_):
    """Multiply a/b * c/d with cross-cancelling; returns (steps, result)."""
    g1, g2 = math.gcd(a_, d_), math.gcd(c_, b_)
    steps = []
    if g1 > 1 or g2 > 1:
        parts = []
        if g1 > 1:
            parts.append(f"{m(a_)} and {m(d_)} share {m(g1)}")
        if g2 > 1:
            parts.append(f"{m(c_)} and {m(b_)} share {m(g2)}")
        a2, d2, c2, b2 = a_ // g1, d_ // g1, c_ // g2, b_ // g2
        steps.append(f"Cancel before multiplying: {' and '.join(parts)}, so the problem becomes "
                     f"{m(rf'{_Fi(a2, b2)} \times {_Fi(c2, d2)}')}.")
    else:
        a2, b2, c2, d2 = a_, b_, c_, d_
    res = R(a_ * c_, b_ * d_)
    prod = _Fi(a2 * c2, b2 * d2)
    tail = (f" = {_fr(res)}" if (a2 * c2, b2 * d2) != (int(res.p), int(res.q)) else "") + _to_mixed_step(res)
    steps.append(f"Multiply top times top and bottom times bottom: "
                 f"{m(rf'{_Fi(a2, b2)} \times {_Fi(c2, d2)} = {prod}{tail}')}.")
    return steps, res


@template("MK")
def multiply(rng, lvl):
    if rng.random() < (0.55 if lvl == 1 else 0.3):
        # fraction of a whole number
        f_ = _proper(rng, [3, 4, 5, 6, 8, 10] if lvl == 1 else [3, 4, 5, 6, 7, 8, 9, 12])
        p, q = int(f_.p), int(f_.q)
        n_ = q * rng.randint(2, 12 if lvl == 1 else 15)
        ans = f_ * n_
        return Problem(
            stem=choose(rng, f"What is {m(rf'{F(p, q)} \times {n_}')}?",
                        f"What is {m(F(p, q))} of {m(n_)}?"),
            answer=ans,
            fmt=mixed,
            wrong=[(R(n_, q), f"finds only {m(F(1, q))} of {m(n_)}"),
                   (Q(n_) * q / p, "divides by the fraction instead of multiplying"),
                   (Q(n_ * p), f"multiplies by {m(p)} but forgets to divide by {m(q)}"),
                   (Q(n_) - ans, "is the part that is left, not the part asked for")],
            steps=[f"Divide by the bottom: {m(rf'{n_} \div {q} = {n_ // q}')}.",
                   f"Multiply by the top: {m(rf'{n_ // q} \times {p} = {int_raw(ans)}')}."],
            check=_sy(Fr(p, q) * n_),
            near=_near_int(ans),
        )
    if lvl == 1:
        f1, f2 = _proper(rng, [2, 3, 4, 5, 6, 7, 8, 9]), _proper(rng, [2, 3, 4, 5, 6, 7, 8, 9])
    else:
        f1, f2 = _proper(rng, [5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18]), _proper(rng, [5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18])
        a_, b_, c_, d_ = int(f1.p), int(f1.q), int(f2.p), int(f2.q)
        need(math.gcd(a_, d_) > 1 and math.gcd(c_, b_) > 1)
    a_, b_, c_, d_ = int(f1.p), int(f1.q), int(f2.p), int(f2.q)
    need(f1 != f2)
    steps, res = _cancel_steps(a_, b_, c_, d_)
    wrong = [(R(a_ * d_, b_ * c_), "flips the second fraction; that is division, not multiplication"),
             (f1 + f2, "adds instead of multiplying"),
             (R(a_ * c_, d_), "multiplies the numerators but keeps only one denominator")]
    return Problem(
        stem=choose(rng, f"What is {m(rf'{_fr(f1)} \times {_fr(f2)}')}?",
                    f"Multiply: {m(rf'{_fr(f1)} \times {_fr(f2)}')}"),
        answer=res,
        fmt=mixed,
        wrong=wrong,
        steps=steps,
        check=_sy(_fx(f1) * _fx(f2)),
    )


@template("MK")
def divide(rng, lvl):
    if rng.random() < 0.35:
        f_ = _proper(rng, [3, 4, 5, 6, 8], lo=2)
        p, q = int(f_.p), int(f_.q)
        n_ = p * rng.randint(1, 6)
        need(n_ > 1)
        ans = Q(n_) / f_
        return Problem(
            stem=choose(rng, f"What is {m(rf'{n_} \div {F(p, q)}')}?",
                        f"Divide: {m(rf'{n_} \div {F(p, q)}')}"),
            answer=ans,
            fmt=mixed,
            wrong=[(Q(n_) * f_, "multiplies instead of dividing"),
                   (f_ / n_, "divides in the wrong order"),
                   (Q(n_) * p / q if p != 1 else Q(n_ * q + 1), None if p == 1 else
                    "multiplies by the fraction instead of its reciprocal")],
            steps=[f"Dividing by {m(F(p, q))} means multiplying by its reciprocal, {m(F(q, p))}.",
                   f"{m(rf'{n_} \times {F(q, p)} = {F(n_ * q, p)} = {_mx(ans)}')}."
                   if p != 1 else f"{m(rf'{n_} \times {q} = {int_raw(ans)}')}."],
            check=_sy(Fr(n_) / Fr(p, q)),
        )
    f1, f2 = _proper(rng, [3, 4, 5, 6, 7, 8, 9, 10, 12]), _proper(rng, [2, 3, 4, 5, 6, 7, 8, 9, 10])
    need(f1 != f2)
    a_, b_, c_, d_ = int(f1.p), int(f1.q), int(f2.p), int(f2.q)
    res = f1 / f2
    need(res.q <= 20 and res.p <= 40)
    steps0 = [f"Keep the first fraction, change {m(r'\div')} to {m(r'\times')}, and flip the "
              f"second fraction: {m(rf'{F(a_, b_)} \times {F(d_, c_)}')}."]
    st, res2 = _cancel_steps(a_, b_, d_, c_)
    need(res2 == res)
    wrong = [(R(b_ * c_, a_ * d_), "divides in the wrong order (flips the answer)"),
             (R(b_, a_) * R(c_, d_), "flips the first fraction instead of the second"),
             (f1 * f2, "multiplies without flipping the second fraction"),
             (R(b_, a_) * R(d_, c_), "flips both fractions")]
    return Problem(
        stem=choose(rng, f"What is {m(rf'{_fr(f1)} \div {_fr(f2)}')}?",
                    f"Divide: {m(rf'{_fr(f1)} \div {_fr(f2)}')}"),
        answer=res,
        fmt=mixed,
        wrong=wrong,
        steps=steps0 + st,
        check=_sy(_fx(f1) / _fx(f2)),
    )


# --------------------------------------------------------------------------
# mixed numbers
# --------------------------------------------------------------------------

def _mixed_parts(v):
    v = Q(v)
    w = int(v.p // v.q)
    return w, v - w


def _draw_mixed(rng, wlo, whi, dens):
    w = rng.randint(wlo, whi)
    f_ = _proper(rng, dens)
    return w + f_, w, f_


@template("MK")
def mixed_add_sub(rng, lvl):
    dens = [2, 3, 4, 5, 6, 8, 10, 12]
    if lvl == 2:
        x_, w1, f1 = _draw_mixed(rng, 1, 7, dens)
        y_, w2, f2 = _draw_mixed(rng, 1, 7, dens)
        need(f1 + f2 > 1 and f1.q != f2.q and _lcd(int(f1.q), int(f2.q)) <= 24)
        ans = x_ + y_
        L = _lcd(int(f1.q), int(f2.q))
        n1, n2 = int(f1 * L), int(f2 * L)
        fs = f1 + f2
        wrong = [(w1 + w2 + fs - 1, f"drops the extra whole number from {m(F(n1 + n2, L))}"),
                 (w1 + w2 + R(int(f1.p) + int(f2.p), int(f1.q) + int(f2.q)),
                  "adds the numerators and adds the denominators of the fractions"),
                 (x_ * y_, "multiplies instead of adding"),
                 (ans + 1, None), (ans - R(1, L), None)]
        steps = [
            f"Add the whole numbers: {m(f'{w1} + {w2} = {w1 + w2}')}.",
            f"Add the fractions with the common denominator {m(L)}: "
            f"{m(f'{F(n1, L)} + {F(n2, L)} = {F(n1 + n2, L)} = {_mx(fs)}')}.",
            f"Combine: {m(f'{w1 + w2} + {_mx(fs)} = {_mx(ans)}')}.",
        ]
        op = "+"
    else:
        x_, w1, f1 = _draw_mixed(rng, 3, 9, dens)
        y_, w2, f2 = _draw_mixed(rng, 1, 5, dens)
        need(w1 > w2 + 1 and f1 < f2 and _lcd(int(f1.q), int(f2.q)) <= 24)
        ans = x_ - y_
        L = _lcd(int(f1.q), int(f2.q))
        n1, n2 = int(f1 * L), int(f2 * L)
        wrong = [((w1 - w2) + (f2 - f1), "subtracts the smaller fraction from the larger instead of regrouping"),
                 ((w1 - w2) + (1 + f1 - f2), "regroups but forgets to take 1 from the whole number"),
                 ((w1 - w2 - 1) + (f2 - f1), "takes 1 from the whole number but then subtracts the "
                                             "fractions in the wrong order"),
                 (x_ + y_, "adds instead of subtracting"),
                 (ans - 1, None)]
        steps = [
            f"Rewrite the fractions with the common denominator {m(L)}: "
            f"{m(f'{w1}{F(n1, L)} - {w2}{F(n2, L)}')}.",
            f"Since {m(F(n1, L))} is less than {m(F(n2, L))}, regroup: take $1$ from {m(w1)}, "
            f"so {m(f'{w1}{F(n1, L)} = {w1 - 1}{F(n1 + L, L)}')}.",
            f"Subtract: whole numbers {m(f'{w1 - 1} - {w2} = {w1 - 1 - w2}')}, fractions "
            + m(f"{F(n1 + L, L)} - {F(n2, L)} = {F(n1 + L - n2, L)}"
                + (f" = {_fr(R(n1 + L - n2, L))}" if R(n1 + L - n2, L).q != L else ""))
            + f". The answer is {m(_mx(ans))}.",
        ]
        op = "-"
    return Problem(
        stem=choose(rng, f"What is {m(f'{_mx(x_)} {op} {_mx(y_)}')}?",
                    f"{'Add' if op == '+' else 'Subtract'}: {m(f'{_mx(x_)} {op} {_mx(y_)}')}"),
        answer=ans,
        fmt=mixed,
        wrong=wrong,
        steps=steps,
        check=_sy(_fx(x_) + _fx(y_) if op == "+" else _fx(x_) - _fx(y_)),
    )


@template("MK")
def mixed_mult_div(rng, lvl):
    dens = [2, 3, 4, 5, 6, 8]
    x_, w1, f1 = _draw_mixed(rng, 1, 5, dens)
    y_, w2, f2 = _draw_mixed(rng, 1, 4, dens)
    op = rng.choice(["*", "/"])
    a_, b_ = int(x_.p), int(x_.q)
    c_, d_ = int(y_.p), int(y_.q)
    if op == "*":
        ans = x_ * y_
        need(ans <= 20 and ans.q <= 12)
        wrong = [(w1 * w2 + f1 * f2, "multiplies the whole numbers and the fractions separately"),
                 (R(w1 + int(f1.p), b_) * R(w2 + int(f2.p), d_),
                  "adds the whole number to the numerator instead of multiplying it by the denominator"),
                 (x_ + y_, "adds instead of multiplying"),
                 (x_ / y_, "divides instead of multiplying")]
        st, res = _cancel_steps(a_, b_, c_, d_)
        sym, word = r"\times", "Multiply"
    else:
        ans = x_ / y_
        need(ans.q <= 12 and ans != 1)
        wrong = [((Q(w1) / w2) + (f1 / f2), "divides the whole numbers and the fractions separately"),
                 (x_ * y_, "multiplies instead of dividing"),
                 (y_ / x_, "divides in the wrong order"),
                 (R(b_, a_) * R(c_, d_), "flips the first fraction instead of the second")]
        st, res = _cancel_steps(a_, b_, d_, c_)
        st = [f"Dividing means multiplying by the reciprocal: "
              f"{m(rf'{F(a_, b_)} \div {F(c_, d_)} = {F(a_, b_)} \times {F(d_, c_)}')}."] + st
        sym, word = r"\div", "Divide"
    need(res == ans)
    steps = [f"Change each mixed number to an improper fraction: "
             f"{m(f'{_mx(x_)} = {F(f'{w1} \\times {b_} + {int(f1.p)}', b_)} = {F(a_, b_)}')} and "
             f"{m(f'{_mx(y_)} = {F(c_, d_)}')}."] + st
    return Problem(
        stem=choose(rng, f"What is {m(f'{_mx(x_)} {sym} {_mx(y_)}')}?",
                    f"{word}: {m(f'{_mx(x_)} {sym} {_mx(y_)}')}"),
        answer=ans,
        fmt=mixed,
        wrong=wrong,
        steps=steps,
        check=_sy(_fx(x_) * _fx(y_) if op == "*" else _fx(x_) / _fx(y_)),
    )


# --------------------------------------------------------------------------
# word problems
# --------------------------------------------------------------------------

_GROUPS = [
    ("A platoon has {N} soldiers. {P} of them are on guard duty tonight.", "soldiers are on guard duty",
     "soldiers are \\emph{not} on guard duty", [8, 12, 16, 20, 24, 28, 30, 32, 36, 40, 42, 48]),
    ("A class has {N} students. {P} of them take the bus to school.", "students take the bus",
     "students do \\emph{not} take the bus", [18, 20, 21, 24, 25, 27, 28, 30, 32, 35, 36]),
    ("A recruiting station processed {N} applicants this week. {P} of them chose the Navy.",
     "applicants chose the Navy", "applicants did \\emph{not} choose the Navy", [20, 24, 30, 36, 40, 45, 48, 60]),
    ("A shipment has {N} boxes. {P} of the boxes hold medical supplies.", "boxes hold medical supplies",
     "boxes do \\emph{not} hold medical supplies", [24, 30, 36, 40, 48, 60, 72, 80]),
    ("A parking lot holds {N} vehicles. {P} of them are pickup trucks.", "vehicles are pickup trucks",
     "vehicles are \\emph{not} pickup trucks", [24, 30, 36, 40, 45, 48, 60, 64]),
]


@template("AR")
def fraction_of(rng, lvl):
    setup, q_yes, q_no, sizes = rng.choice(_GROUPS)
    N = rng.choice(sizes)
    dn = [d for d in (3, 4, 5, 6, 8, 10, 12) if N % d == 0]
    need(dn)
    f_ = _proper(rng, dn, lo=1)
    p, q = int(f_.p), int(f_.q)
    part = f_ * N
    if lvl == 3:
        dg = [d for d in (2, 3, 4, 5) if part % d == 0]
        need(part >= 4 and dg)
        g_ = _proper(rng, dg)
        sub = g_ * part
        s = soldier(rng)
        ctx = rng.choice([
            (f"A {'platoon' if N <= 48 else 'company'} of {m(N)} soldiers took a road march. {m(F(p, q))} of them carried the heavy "
             f"rucksack, and {m(_fr(g_))} of those soldiers finished in under three hours. How many "
             "soldiers carried the heavy rucksack and finished in under three hours?"),
            (f"{s} has {m(N)} recruits. {m(F(p, q))} of them passed the swim test on the first try, and "
             f"{m(_fr(g_))} of those also passed the rope climb. How many recruits passed both?"),
            (f"A club has {m(N)} members. {m(F(p, q))} of them signed up for the trip, and {m(_fr(g_))} "
             "of those who signed up want a window seat. How many members want a window seat?"),
        ])
        return Problem(
            stem=ctx,
            answer=Q(sub),
            fmt=num,
            wrong=[(Q(part), "is the size of the first group only"),
                   (g_ * N, f"takes {m(_fr(g_))} of the whole group instead of the smaller group"),
                   (part - sub, f"is the part of the smaller group that is \\emph{{not}} counted"),
                   ((f_ + g_) * N if (f_ + g_) < 1 else Q(sub + 1), "adds the two fractions"
                    if (f_ + g_) < 1 else None)],
            steps=[f"First group: {m(rf'{F(p, q)} \times {N} = {int_raw(part)}')}.",
                   f"Then take {m(_fr(g_))} of that group: "
                   f"{m(rf'{_fr(g_)} \times {int_raw(part)} = {int_raw(sub)}')}."],
            check=_sy(Fr(p, q) * _fx(g_) * N),
        )
    stem = setup.format(N=m(N), P=m(F(p, q)))
    if lvl == 1:
        return Problem(
            stem=f"{stem} How many {q_yes}?",
            answer=part,
            fmt=num,
            wrong=[(R(N, q), f"finds only {m(F(1, q))} of the total"),
                   (Q(N) - part, "is the other part of the group"),
                   (Q(N) * q / p, "divides by the fraction instead of multiplying"),
                   (part + 1, None), (part - 1, None)],
            steps=[f"Find {m(F(p, q))} of {m(N)}: divide by the bottom, {m(rf'{N} \div {q} = {N // q}')}.",
                   f"Multiply by the top: {m(rf'{N // q} \times {p} = {int_raw(part)}')}."],
            check=_sy(Fr(N * p, q)),
        )
    rest = Q(N) - part
    return Problem(
        stem=f"{stem} How many {q_no}?",
        answer=rest,
        fmt=num,
        wrong=[(part, "is the part named in the problem, not the rest"),
               (R(N, q), f"finds only {m(F(1, q))} of the total"),
               (Q(N - p), f"subtracts the numerator {m(p)} from {m(N)}"),
               (rest + 1, None)],
        steps=[f"The part asked about is {m(f'1 - {F(p, q)} = {F(q - p, q)}')} of the group.",
               f"{m(rf'{F(q - p, q)} \times {N} = {int_raw(rest)}')} "
               f"(or find {m(F(p, q))} of {m(N)}, which is {m(int_raw(part))}, and subtract: "
               f"{m(f'{N} - {int_raw(part)} = {int_raw(rest)}')})."],
        check=_sy(Fr(N) - Fr(N * p, q)),
    )


_SPEND = [
    ("{P} earned {M} last month. {He} spent {A} of it on rent and then {B} of what was left on groceries.",
     "rent", "groceries", (900, 3600), money),
    ("{S} received a {M} enlistment bonus, used {A} of it to pay off a car loan, and then put {B} "
     "of the remaining money into savings.", "the car loan", "savings", (3000, 12000), money),
    ("A truck started a trip with {M} gallons of fuel. It used {A} of the fuel on the first day and "
     "{B} of what was left on the second day.", "the first day", "the second day", (24, 120), None),
    ("A supply point had {M} cases of water. On Monday it issued {A} of the cases, and on Tuesday it "
     "issued {B} of the cases that were left.", "Monday", "Tuesday", (60, 600), None),
]


@template("AR")
def remaining_after(rng, lvl):
    tpl, n1, n2, (lo, hi), fmt = rng.choice(_SPEND)
    f1 = _proper(rng, [3, 4, 5, 6])
    f2 = _proper(rng, [2, 3, 4, 5])
    need(f1 != f2)
    if fmt is money:
        need(f2 <= R(1, 2) and (f1 <= R(1, 2) or "bonus" in tpl))
    M = rng.randint(lo, hi)
    if fmt is money:
        M = M // 100 * 100
    first = f1 * M
    left1 = M - first
    second = f2 * left1
    left2 = left1 - second
    need(first.q == 1 and second.q == 1 and left2 > 0 and M > 0)
    need(left2 != second and left2 != first)
    pr = person(rng)
    s = soldier(rng)
    stem = tpl.format(P=pr.name, He=pr.He, S=s, M=money(M) if fmt is money else m(int_raw(M)),
                      A=m(_fr(f1)), B=m(_fr(f2)))
    what = "money" if fmt is money else ("fuel" if "fuel" in tpl else "cases")
    unit_ = "dollars" if fmt is money else ("gallons" if "fuel" in tpl else "cases")
    ffmt = money if fmt is money else (unit(num, "gallon") if "fuel" in tpl else num)
    left_q = {"money": "How much money is left?", "fuel": "How many gallons of fuel are left?",
              "cases": "How many cases are left?"}[what]
    return Problem(
        stem=f"{stem} {left_q}",
        answer=left2,
        fmt=ffmt,
        wrong=[(M - first - f2 * M, f"takes {m(_fr(f2))} of the original amount instead of what was left"),
               (left1, f"stops after {n1}"),
               (second, f"is the amount for {n2}, not what is left"),
               (M * (1 - f1 - f2) if (f1 + f2) < 1 else left2 + 1, None),
               ((1 - f1 * f2) * M, "multiplies the two fractions and subtracts that from the original amount")],
        steps=[
            f"{n1[0].upper() + n1[1:]}: {m(rf'{_fr(f1)} \times {int_raw(M)} = {int_raw(first)}')}, "
            f"which leaves {m(f'{int_raw(M)} - {int_raw(first)} = {int_raw(left1)}')} {unit_}.",
            f"{n2[0].upper() + n2[1:]}: {m(_fr(f2))} of what was left is "
            f"{m(rf'{_fr(f2)} \times {int_raw(left1)} = {int_raw(second)}')}.",
            f"What remains: {m(f'{int_raw(left1)} - {int_raw(second)} = {int_raw(left2)}')} {unit_}.",
        ],
        tip=(f"Shortcut: keep {m(_fr(1 - f1))} and then {m(_fr(1 - f2))} of that: "
             f"{m(rf'{_fr(1 - f1)} \times {_fr(1 - f2)} \times {int_raw(M)} = {int_raw(left2)}')}."),
        check=_sy(_fx(1 - f1) * _fx(1 - f2) * M),
    )


@template("AR")
def mixed_word(rng, lvl):
    kind = rng.choice(["march", "recipe", "runs", "board"])
    dens = [2, 4, 8] if kind in ("board", "march") else [2, 3, 4]
    if kind == "march":
        W = rng.choice([6, 8, 10, 12, 15])
        done, w, f_ = _draw_mixed(rng, 2, W - 2, dens)
        ans = W - done
        s = soldier(rng)
        stem = (f"{s}'s platoon is on a {m(W)}-mile ruck march. So far the platoon has covered "
                f"{m(_mx(done))} miles. How many miles are left?")
        L = int(f_.q)
        wrong = [((W - w) + f_, "subtracts the whole numbers and keeps the fraction"),
                 (Q(W - w) - f_ + 1, "regroups but forgets to take 1 from the whole number"),
                 (ans + R(1, L) * 2 if ans + R(2, L) != (W - w) + f_ else ans + 1, None)]
        steps = [f"Subtract: {m(f'{W} - {_mx(done)}')}.",
                 f"Regroup {m(W)} as {m(f'{W - 1}{F(L, L)}')}.",
                 f"{m(f'{W - 1}{F(L, L)} - {w}{F(int(f_.p), L)} = {_mx(ans)}')} miles."]
        fmt = unit(mixed, "mile")
        chk = _sy(Fr(W) - _fx(done))
    elif kind == "recipe":
        amt, w, f_ = _draw_mixed(rng, 1, 3, dens)
        k = rng.randint(2, 4)
        ans = amt * k
        need(f_ * k > 1)
        p = person(rng)
        item = rng.choice(["cups of flour", "cups of milk", "cups of rice", "teaspoons of salt"])
        stem = (f"A recipe calls for {m(_mx(amt))} {item}. {p.name} is making {m(k)} batches. How many "
                f"{item} does {p.he} need?")
        wrong = [(Q(w * k) + f_, "multiplies only the whole number"),
                 (amt + k, f"adds {m(k)} instead of multiplying by {m(k)}"),
                 (Q(w * k) + f_ * k - 1 if (f_ * k) > 1 else Q(w * k), f"drops the extra whole number from {m(_fr(f_ * k))}"),
                 (ans + 1, None)]
        steps = [f"Multiply the whole number and the fraction by {m(k)}: "
                 f"{m(rf'{w} \times {k} = {w * k}')} and {m(rf'{_fr(f_)} \times {k} = {_fr(f_ * k)} = {_mx(f_ * k)}')}.",
                 f"Add: {m(f'{w * k} + {_mx(f_ * k)} = {_mx(ans)}')}."]
        fmt = text_unit(item)
        chk = _sy(_fx(amt) * k)
    elif kind == "runs":
        x_, w1, f1 = _draw_mixed(rng, 1, 5, [2, 4, 8])
        y_, w2, f2 = _draw_mixed(rng, 1, 5, [2, 3, 4])
        need(f1 + f2 > 1 and f1.q != f2.q)
        ans = x_ + y_
        L = _lcd(int(f1.q), int(f2.q))
        p = person(rng)
        stem = (f"{p.name} ran {m(_mx(x_))} miles on Saturday and {m(_mx(y_))} miles on Sunday. How many "
                "miles did {he} run in all?").replace("{he}", p.he)
        wrong = [(w1 + w2 + f1 + f2 - 1, f"drops the extra whole number from {m(F(int(f1 * L) + int(f2 * L), L))}"),
                 (w1 + w2 + R(int(f1.p) + int(f2.p), int(f1.q) + int(f2.q)),
                  "adds the numerators and adds the denominators of the fractions"),
                 (ans + 1, None)]
        steps = [f"Add the whole numbers: {m(f'{w1} + {w2} = {w1 + w2}')}.",
                 f"Add the fractions: {m(f'{F(int(f1 * L), L)} + {F(int(f2 * L), L)} = {F(int((f1 + f2) * L), L)} = {_mx(f1 + f2)}')}.",
                 f"Total: {m(f'{w1 + w2} + {_mx(f1 + f2)} = {_mx(ans)}')} miles."]
        fmt = unit(mixed, "mile")
        chk = _sy(_fx(x_) + _fx(y_))
    else:
        x_, w1, f1 = _draw_mixed(rng, 6, 12, [2, 4, 8])
        y_, w2, f2 = _draw_mixed(rng, 1, 4, [2, 4, 8])
        need(f1 < f2 and w1 - w2 >= 2)
        ans = x_ - y_
        L = _lcd(int(f1.q), int(f2.q))
        n1, n2 = int(f1 * L), int(f2 * L)
        stem = (f"A board is {m(_mx(x_))} feet long. A carpenter cuts off a piece {m(_mx(y_))} feet long. "
                "How long is the rest of the board? (Ignore the width of the saw cut.)")
        wrong = [((w1 - w2) + (f2 - f1), "subtracts the smaller fraction from the larger instead of regrouping"),
                 ((w1 - w2) + (1 + f1 - f2), "regroups but forgets to take 1 from the whole number"),
                 (x_ + y_, "adds instead of subtracting")]
        steps = [f"Common denominator {m(L)}: {m(f'{w1}{F(n1, L)} - {w2}{F(n2, L)}')}.",
                 f"Regroup: {m(f'{w1}{F(n1, L)} = {w1 - 1}{F(n1 + L, L)}')}.",
                 f"Subtract: {m(f'{w1 - 1}{F(n1 + L, L)} - {w2}{F(n2, L)} = {_mx(ans)}')} feet."]
        fmt = unit(mixed, "foot", "feet")
        chk = _sy(_fx(x_) - _fx(y_))
    return Problem(stem=stem, answer=ans, fmt=fmt, wrong=wrong, steps=steps, check=chk)


def text_unit(item):
    word = item.split(" of ")[0]
    sing = word[:-1] if word.endswith("s") else word
    return unit(mixed, sing, word)


PLAN = [
    # (template, level, count)  -- easy -> hard; 25 problems
    (simplify, 1, 2),
    (equivalent, 1, 1),
    (add_sub, 1, 2),
    (multiply, 1, 1),
    (fraction_of, 1, 2),
    (compare, 2, 2),
    (add_sub, 2, 1),
    (multiply, 2, 1),
    (divide, 2, 2),
    (mixed_add_sub, 2, 2),
    (mixed_word, 2, 2),
    (mixed_add_sub, 3, 2),
    (mixed_mult_div, 3, 2),
    (remaining_after, 3, 2),
    (fraction_of, 3, 1),
]
