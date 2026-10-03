"""Chapter 9 - Square Roots & Radicals."""
from fractions import Fraction
from math import gcd, isqrt

import sympy as sp

from ..core import (R, Q, Problem, need, num, dec, frac, mixed, expr, m, F, tx, latex,
                    dec_raw, int_raw, frac_raw, mixed_raw, choose, template)

NUM = 9
TITLE = r"Square Roots \& Radicals"
PART = 1

INTRO = r"""
The \emph{square root} of a number is the value that, multiplied by itself,
gives the number: $\sqrt{49} = 7$ because $7 \times 7 = 49$. The symbol
$\sqrt{\phantom{x}}$ always means the positive root. Knowing the perfect
squares by heart makes every problem in this chapter faster.

\begin{concept}{Perfect squares and cubes to memorize}
\begin{center}\small
\begin{tabular}{l*{8}{c}}
$n$ & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 \\
$n^2$ & 1 & 4 & 9 & 16 & 25 & 36 & 49 & 64 \\
$n^3$ & 1 & 8 & 27 & 64 & 125 & 216 & 343 & 512 \\[2pt]
$n$ & 9 & 10 & 11 & 12 & 13 & 14 & 15 & 20 \\
$n^2$ & 81 & 100 & 121 & 144 & 169 & 196 & 225 & 400
\end{tabular}
\end{center}
The \emph{cube root} undoes a cube: $\sqrt[3]{125} = 5$ because $5^3 = 125$.
\end{concept}

\begin{concept}{Working with radicals}
\begin{itemize}
\item Simplify: pull out the \emph{largest} perfect-square factor.
  $\sqrt{72} = \sqrt{36 \cdot 2} = 6\sqrt{2}$.
\item Add or subtract only \emph{like} radicals (same number under the root):
  $3\sqrt{5} + 4\sqrt{5} = 7\sqrt{5}$.
\item Multiply the numbers under the roots: $\sqrt{6} \cdot \sqrt{15} =
  \sqrt{90} = 3\sqrt{10}$.
\item Rationalize a denominator: multiply top and bottom by the root.
  $\frac{6}{\sqrt{3}} = \frac{6\sqrt{3}}{3} = 2\sqrt{3}$.
\end{itemize}
\end{concept}

\begin{concept}{Fractions, decimals, and equations}
$\sqrt{\frac{49}{64}} = \frac{7}{8}$ (root of top over root of bottom), and
$\sqrt{0.09} = \sqrt{\frac{9}{100}} = \frac{3}{10} = 0.3$. The equation
$x^2 = 81$ has \emph{two} solutions, $x = 9$ and $x = -9$; read the question
to see whether it wants both or only the positive one.
\end{concept}

\begin{example}{Worked example}
Simplify $\sqrt{12} + \sqrt{27}$.

\textbf{Solution.} The radicals are not alike yet, so simplify each:
$\sqrt{12} = \sqrt{4 \cdot 3} = 2\sqrt{3}$ and $\sqrt{27} = \sqrt{9 \cdot 3} =
3\sqrt{3}$. Now they are like radicals: $2\sqrt{3} + 3\sqrt{3} = 5\sqrt{3}$.
\end{example}

\begin{tip}
Estimate a root by trapping it between perfect squares: $49 < 53 < 64$, so
$\sqrt{53}$ is between $7$ and $8$, a little above $7$.
\end{tip}

\begin{trap}
\begin{itemize}
\item Splitting a root over addition: $\sqrt{9 + 16} = \sqrt{25} = 5$, not $3 + 4 = 7$.
\item Adding unlike radicals: $\sqrt{2} + \sqrt{3}$ is \emph{not} $\sqrt{5}$.
\item Decimal places: $\sqrt{0.09} = 0.3$, not $0.03$ (check: $0.3^2 = 0.09$).
\item Forgetting the negative solution of $x^2 = 81$ when the question asks for all solutions.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# private helpers
# --------------------------------------------------------------------------

_SQUAREFREE = [2, 3, 5, 6, 7, 10, 11, 13, 14, 15]


def _split(n):
    """n = k^2 * r with r square-free: the hand method (largest square factor)."""
    k = 1
    for f in range(isqrt(n), 1, -1):
        if n % (f * f) == 0:
            k = f
            break
    return k, n // (k * k)


def _rad(k, r):
    """Exact value k*sqrt(r)."""
    return Q(k) * sp.sqrt(r)


def _rt(k, r) -> str:
    """Raw LaTeX for k*sqrt(r) (k may be 1)."""
    if r == 1:
        return int_raw(k)
    return (f"{int_raw(k)}" if k != 1 else "") + rf"\sqrt{{{r}}}"


def _rfmt(v) -> str:
    """Choice formatter: whole numbers with thousands separators, radicals via LaTeX."""
    v = Q(v)
    return num(v) if v.is_integer else expr(v)


def _clean(n) -> bool:
    """sqrt(n) displays as the student would write it: n square-free or a perfect square."""
    if isqrt(n) ** 2 == n:
        return True
    return _split(n)[0] == 1


def _rad_near(ans_k, r):
    """Fillers with the same radical: (k±1)sqrt(r), (k±2)sqrt(r)."""
    def f(rng):
        out = [_rad(ans_k + d, r) for d in (1, -1, 2, -2, 3) if ans_k + d > 0]
        rng.shuffle(out)
        return out
    return f


def _cx(a) -> str:
    return "x" if a == 1 else f"{a}x"


def _simplify_both(n1, p, n2, q, r) -> str:
    def piece(v, k):
        return m(f"\\sqrt{{{v}}} = \\sqrt{{{k * k} \\cdot {r}}} = {_rt(k, r)}")
    if p > 1 and q > 1:
        return f"{piece(n1, p)} and {piece(n2, q)}."
    big, simple = ((n1, p), n2) if p > 1 else ((n2, q), n1)
    return f"{piece(*big)}, and {m(f'\\sqrt{{{simple}}}')} is already simplified."


# --------------------------------------------------------------------------
# templates
# --------------------------------------------------------------------------

_SQ_CTX = [
    "A square rug has an area of {A} square feet. How long is each side, in feet?",
    "A square garden plot has an area of {A} square yards. How long is each side, in yards?",
    "A square floor tile has an area of {A} square inches. How long is each side, in inches?",
    "A square parade field has an area of {A} square yards. How long is each side, in yards?",
    "A square tent floor has an area of {A} square feet. How long is each side, in feet?",
    "What number multiplied by itself equals {A}?",
]
_CUBE_CTX = [
    "A cube-shaped storage box has a volume of {V} cubic feet. How long is each edge, in feet?",
    "A cube-shaped block of ice has a volume of {V} cubic inches. How long is each edge, in inches?",
    "What number used as a factor three times equals {V}?",
]


@template("MK")
def perfect_root(rng, lvl):
    if lvl == 1:
        kind = rng.choice(["square", "square", "tens", "cube", "two"])
        if kind == "two":
            a, b = rng.sample(range(2, 13), 2)
            A, B = a * a, b * b
            op = rng.choice(["+", "-", "x"])
            if op == "-" and a < b:
                a, b, A, B = b, a, B, A
            f = {"+": lambda u, v: u + v, "-": lambda u, v: u - v, "x": lambda u, v: u * v}[op]
            sym = r"\times" if op == "x" else op
            ans = Q(f(a, b))
            wrong = [
                (Q(f(A, B)), "forgets to take the square roots"),
                (R(f(A, B), 2) if op != "x" else R(A * B, 2), "divides by 2 instead of taking the square roots"),
            ]
            if op in "+-" and isqrt(f(A, B)) ** 2 == f(A, B) and f(A, B) > 0:
                wrong.append((Q(isqrt(f(A, B))), f"{'adds' if op == '+' else 'subtracts'} first and then takes one square root"))
            wrong += [(ans + 1, None), (ans - 1, None), (ans + 2, None)]
            tex = f"\\sqrt{{{A}}} {sym} \\sqrt{{{B}}}"
            return Problem(
                stem=choose(rng, f"What is the value of {m(tex)}?", f"Evaluate {m(tex)}.",
                            f"Which of the following is equal to {m(tex)}?"),
                answer=ans,
                fmt=num,
                wrong=[w for w in wrong if Q(w[0]) > 0],
                steps=[
                    f"Find each square root: {m(f'\\sqrt{{{A}}} = {a}')} and {m(f'\\sqrt{{{B}}} = {b}')}.",
                    f"Then {m(f'{a} {sym} {b} = {int_raw(ans)}')}.",
                ],
                check=sp.sympify(f"sqrt({A}) {'*' if op == 'x' else op} sqrt({B})"),
            )
        if kind in ("square", "tens"):
            k = rng.choice(list(range(4, 21)) + [25]) if kind == "square" else 10 * rng.randint(2, 9)
            n2 = k * k
            wrong = [
                (R(n2, 2), "divides by 2 instead of taking the square root"),
                (Q(k + 1), None), (Q(k - 1), None), (Q(k + 2), None), (Q(k - 2), None),
            ]
            if kind == "tens":
                wrong = [
                    (R(n2, 2), "divides by 2 instead of taking the square root"),
                    (Q(k // 10), f"takes the square root of {num(k * k // 100)} but drops the zero"),
                    (Q(k * 10), "keeps too many zeros: the square root has half as many zeros"),
                    (Q(k + 10), None), (Q(k - 10), None),
                ]
            n2t = m(f"\\sqrt{{{int_raw(n2)}}}")
            stem = choose(rng, f"What is the value of {n2t}?", f"Evaluate {n2t}.",
                          f"What is the square root of {num(n2)}?",
                          rng.choice(_SQ_CTX).format(A=num(n2)))
            steps = [f"Look for the number that, multiplied by itself, gives {num(n2)}."]
            if kind == "tens":
                steps.append(f"{m(f'{k // 10} \\times {k // 10} = {k * k // 100}')}, so "
                             f"{m(f'{k} \\times {k} = {int_raw(n2)}')} (two zeros in the answer, one in the root).")
            steps.append(f"{m(f'{k} \\times {k} = {int_raw(n2)}')}, so the square root is {num(k)}.")
            return Problem(
                stem=stem,
                answer=Q(k),
                fmt=num,
                wrong=wrong,
                steps=steps if kind == "square" else steps[:2],
                check=sp.sqrt(n2),
                verify=lambda v: v * v == n2,
            )
        k = rng.randint(2, 10)
        neg = k <= 6 and rng.random() < 0.25
        c = k ** 3
        ans = Q(-k if neg else k)
        sgn = -1 if neg else 1
        wrong = [
            (R(sgn * c, 3), "divides by 3 instead of taking the cube root"),
            (Q(sgn * k * k), f"gives {m(f'{k}^2')} instead"),
            (Q(sgn * (k + 1)), None), (Q(sgn * (k - 1)), None), (Q(sgn * (k + 2)), None),
        ]
        if neg:
            wrong.insert(0, (Q(k), "drops the negative sign; the cube root of a negative number is negative"))
        elif isqrt(c) ** 2 == c:
            wrong.insert(0, (Q(isqrt(c)), "takes the square root instead of the cube root"))
        ct = m(f"\\sqrt[3]{{{int_raw(sgn * c)}}}")
        fac = f"({int_raw(ans)})" if neg else int_raw(ans)
        stem = (choose(rng, f"What is the value of {ct}?", f"Evaluate {ct}.") if neg else
                choose(rng, f"What is the value of {ct}?", f"Evaluate {ct}.", f"What is the cube root of {num(c)}?",
                       rng.choice(_CUBE_CTX).format(V=num(c))))
        return Problem(
            stem=stem,
            answer=ans,
            fmt=num,
            neg_ok=neg,
            wrong=[w for w in wrong if neg or Q(w[0]) > 0],
            steps=[
                f"The cube root is the number that, used as a factor three times, gives {num(sgn * c)}.",
                f"{m(f'{fac} \\times {fac} \\times {fac} = {int_raw(sgn * c)}')}, so the cube root is {num(ans)}.",
            ],
            check=sgn * sp.cbrt(c),
            verify=lambda v: v ** 3 == sgn * c,
        )

    # level 3: roots of sums, differences, and products
    kind = rng.choice(["sum", "sum", "diff", "prod"])
    if kind == "prod":
        a, b = rng.sample(range(2, 13), 2)
        A, B = a * a, b * b
        ans = Q(a * b)
        inside = f"{A} \\times {B}"
        wrong = [
            (Q(a + b), f"adds the square roots instead of multiplying them"),
            (R(A * B, 2), "divides by 2 instead of taking the square root"),
            (Q(A * B), "forgets to take the square root"),
            (Q(a * b + a), None),
        ]
        steps = [
            f"The square root of a product is the product of the square roots: "
            f"{m(f'\\sqrt{{{inside}}} = \\sqrt{{{A}}} \\times \\sqrt{{{B}}}')}.",
            f"{m(f'\\sqrt{{{A}}} = {a}')} and {m(f'\\sqrt{{{B}}} = {b}')}, so the answer is {m(f'{a} \\times {b} = {a * b}')}.",
        ]
        ver = lambda v: v * v == A * B
    else:
        a0, b0, c0 = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)])
        t = rng.choice([1, 1, 2, 3, 4, 5])
        a, b, c = a0 * t, b0 * t, c0 * t
        if rng.random() < 0.5:
            a, b = b, a
        need(c <= 30)
        if kind == "sum":
            inside, ans = f"{a * a} + {b * b}", Q(c)
            wrong = [
                (Q(a + b), f"takes the square root of each number and adds ({m(f'{a} + {b}')}); a root does not split over addition"),
                (Q(c * c), "forgets to take the square root"),
                (R(c * c, 2), "divides by 2 instead of taking the square root"),
                (Q(c - 1), None), (Q(c + 1), None),
            ]
            steps = [
                f"Work inside the root first: {m(f'{a * a} + {b * b} = {c * c}')}.",
                f"Then {m(f'\\sqrt{{{c * c}}} = {c}')}, because {m(f'{c} \\times {c} = {c * c}')}.",
            ]
            ver = lambda v: v * v == a * a + b * b
        else:
            inside, ans = f"{c * c} - {a * a}", Q(b)
            wrong = [
                (Q(c - a), f"takes the square root of each number and subtracts ({m(f'{c} - {a}')}); a root does not split over subtraction"),
                (Q(b * b), "forgets to take the square root"),
                (R(b * b, 2), "divides by 2 instead of taking the square root"),
                (Q(b - 1), None), (Q(b + 1), None),
            ]
            steps = [
                f"Work inside the root first: {m(f'{c * c} - {a * a} = {b * b}')}.",
                f"Then {m(f'\\sqrt{{{b * b}}} = {b}')}, because {m(f'{b} \\times {b} = {b * b}')}.",
            ]
            ver = lambda v: v * v == c * c - a * a
    return Problem(
        stem=choose(rng, f"What is the value of {m(f'\\sqrt{{{inside}}}')}?",
                    f"Evaluate {m(f'\\sqrt{{{inside}}}')}.",
                    f"Which of the following is equal to {m(f'\\sqrt{{{inside}}}')}?"),
        answer=ans,
        fmt=num,
        wrong=[w for w in wrong if w[0] != ans],
        steps=steps,
        check=sp.sqrt(sp.sympify(inside.replace("\\times", "*"))),
        verify=ver,
    )


@template("MK")
def estimate_root(rng, lvl):
    k = rng.randint(2, 14)
    N = rng.randint(k * k + 1, (k + 1) ** 2 - 1)
    lo, hi = k * k, (k + 1) ** 2
    between = lambda v: m(f"{int_raw(v)}") + " and " + m(f"{int_raw(v + 1)}")
    if lvl == 1:
        wrong = [
            (Q(N // 2), f"divides {num(N)} by 2 instead of taking the square root")
            if (N // 2 > k + 2 and rng.random() < 0.5) else (Q(k + 3), None),
            (Q(k - 1), None), (Q(k + 1), None), (Q(k - 2) if k > 2 else Q(k + 2), None),
            (Q(k - 3) if k > 3 else Q(k + 3), None), (Q(k + 2), None),
        ]
        return Problem(
            stem=choose(rng, f"{m(f'\\sqrt{{{N}}}')} is between which two consecutive whole numbers?",
                        f"Between which two consecutive whole numbers does {m(f'\\sqrt{{{N}}}')} lie?",
                        f"A square {rng.choice(['patio', 'rug', 'room', 'tarp'])} has an area of "
                        f"{num(N)} square feet. Its side length, in feet, is between which two consecutive whole numbers?"),
            answer=Q(k),
            fmt=lambda v: between(Q(v)),
            wrong=wrong,
            steps=[
                f"Find the perfect squares on either side of {num(N)}: {m(f'{k}^2 = {lo}')} and {m(f'{k + 1}^2 = {hi}')}.",
                f"Since {m(f'{lo} < {N} < {hi}')}, the square root is between {m(k)} and {m(k + 1)}.",
            ],
            check=sp.floor(sp.sqrt(N)),
        )
    near_hi = N - lo > hi - N
    ans = Q(k + 1 if near_hi else k)
    other = Q(k if near_hi else k + 1)
    return Problem(
        stem=choose(rng, f"Which whole number is closest to {m(f'\\sqrt{{{N}}}')}?",
                    f"To the nearest whole number, what is {m(f'\\sqrt{{{N}}}')}?",
                    f"A square {rng.choice(['garden', 'helipad', 'deck', 'storage pad'])} has an area of "
                    f"{num(N)} square feet. To the nearest foot, how long is each side?"),
        answer=ans,
        fmt=num,
        wrong=[
            (other, f"is the other neighbor, but {num(N)} is closer to {num(hi if near_hi else lo)}"),
            (R(N, 2) if N % 2 == 0 else Q(N // 2), f"divides {num(N)} by 2 instead of taking the square root"),
            (ans + 1 if near_hi else ans - 1, None),
            (ans + 2 if not near_hi else ans - 2, None),
            (ans - 2, None), (ans - 3, None), (ans + 2, None),
        ],
        steps=[
            f"Trap the root between perfect squares: {m(f'{k}^2 = {lo}')} and {m(f'{k + 1}^2 = {hi}')}, "
            f"so {m(f'\\sqrt{{{N}}}')} is between {k} and {k + 1}.",
            f"Compare distances: {m(f'{N} - {lo} = {N - lo}')} and {m(f'{hi} - {N} = {hi - N}')}. "
            f"{num(N)} is closer to {num(hi if near_hi else lo)}.",
            f"So {m(f'\\sqrt{{{N}}}')} is closest to {num(ans)}.",
        ],
        check=sp.floor(sp.sqrt(N) + R(1, 2)),
    )


@template("MK")
def root_fraction_decimal(rng, lvl):
    if lvl == 1:
        a, b = rng.randint(1, 12), rng.randint(2, 12)
        need(a != b and gcd(a, b) == 1)
        ans = R(a, b)
        stem_tex = f"\\sqrt{{{F(a * a, b * b)}}}"
        return Problem(
            stem=choose(rng, f"What is the value of {m(stem_tex)}?", f"Evaluate {m(stem_tex)}.",
                        f"Which of the following is equal to {m(stem_tex)}?"),
            answer=ans,
            fmt=frac,
            wrong=[
                (R(a * a, b), "takes the square root of the denominator only"),
                (R(a, b * b), "takes the square root of the numerator only"),
                (R(b, a), "flips the fraction"),
                (R(a * a, 2 * b * b), "divides by 2 instead of taking the square root"),
            ],
            steps=[
                f"Take the square root of the top and of the bottom: "
                f"{m(f'{stem_tex} = {F(f"\\sqrt{{{a * a}}}", f"\\sqrt{{{b * b}}}")}')}.",
                f"{m(f'\\sqrt{{{a * a}}} = {a}')} and {m(f'\\sqrt{{{b * b}}} = {b}')}, so the answer is {m(frac_raw(ans))}.",
            ],
            check=sp.sqrt(R(a * a, b * b)),
            verify=lambda v: v * v == R(a * a, b * b),
        )
    if rng.random() < 0.4:
        a, b = rng.randint(3, 12), rng.randint(2, 9)
        need(a > b and gcd(a, b) == 1 and a % b != 0)
        ans = R(a, b)
        sqv = ans * ans
        need(sqv.q <= 100)
        whole = sqv.p // sqv.q
        part = sqv - whole
        stem_tex = f"\\sqrt{{{mixed_raw(sqv)}}}"
        wrong = [
            (whole + sp.sqrt(part) if sp.sqrt(part).is_rational else None, "takes the square root of the fraction part only"),
            (R(a * a, b), "changes to an improper fraction, then takes the root of the denominator only"),
            (R(a, b * b), "changes to an improper fraction, then takes the root of the numerator only"),
            (sqv / 2, "divides by 2 instead of taking the square root"),
            (R(b, a), "flips the fraction"),
        ]
        return Problem(
            stem=choose(rng, f"What is the value of {m(stem_tex)}?", f"Evaluate {m(stem_tex)}.",
                        f"Which of the following is equal to {m(stem_tex)}?"),
            answer=ans,
            fmt=mixed,
            wrong=[w for w in wrong if w[0] is not None],
            steps=[
                f"Change the mixed number to an improper fraction: {m(f'{mixed_raw(sqv)} = {frac_raw(sqv)}')}.",
                f"Take the root of the top and the bottom: {m(f'\\sqrt{{{frac_raw(sqv)}}} = {F(a, b)}')}.",
                f"As a mixed number, {m(f'{F(a, b)} = {mixed_raw(ans)}')}. Check: "
                f"{m(f'{F(a, b)} \\times {F(a, b)} = {frac_raw(sqv)}')}. \\checkmark",
            ],
            check=sp.sqrt(sqv),
            verify=lambda v: v * v == sqv,
        )
    places = rng.choice([1, 1, 2])
    digits = (rng.choice([v for v in range(2, 21) if v != 10] + [25, 35, 45, 55, 65, 75, 85, 95]) if places == 1
              else rng.choice([v for v in range(1, 16) if v != 10]))
    d = R(digits, 10 ** places)
    sq = d * d
    need(sq.q <= 10 ** 4 and d != 1)
    sq_places = 2 * places
    return Problem(
        stem=choose(rng, f"What is the value of {m(f'\\sqrt{{{dec_raw(sq)}}}')}?",
                    f"Evaluate {m(f'\\sqrt{{{dec_raw(sq)}}}')}.",
                    f"What is the square root of {m(dec_raw(sq))}?",
                    f"Which of the following is equal to {m(f'\\sqrt{{{dec_raw(sq)}}}')}?"),
        answer=d,
        fmt=dec,
        wrong=[
            (d / 10, f"keeps {sq_places} decimal places; a square root has half as many"),
            (sq / 2, "divides by 2 instead of taking the square root"),
            (d * 10, "puts the decimal point too far to the right"),
            (d + R(1, 10 ** places), None),
        ],
        steps=[
            f"Write the decimal as a fraction: {m(f'{dec_raw(sq)} = {F(int_raw(sq * 10 ** sq_places), int_raw(10 ** sq_places))}')}.",
            f"Take the root of the top and the bottom: "
            f"{m(f'\\sqrt{{{F(int_raw(sq * 10 ** sq_places), int_raw(10 ** sq_places))}}} = {F(int_raw(digits), int_raw(10 ** places))} = {dec_raw(d)}')}.",
            f"Check: {m(f'{dec_raw(d)} \\times {dec_raw(d)} = {dec_raw(sq)}')}. \\checkmark",
        ],
        check=sp.sqrt(sq),
        verify=lambda v: v * v == sq,
    )


@template("MK")
def simplify_radical(rng, lvl):
    r = rng.choice([2, 2, 3, 3, 5, 5, 6, 7, 10, 11, 13, 14, 15])
    k = rng.randint(2, 12)
    n = k * k * r
    need(n <= 450)
    kk, rr = _split(n)
    ans = _rad(kk, rr)
    wrong = [
        (_rad(kk * kk, rr), f"pulls out {kk * kk} instead of its square root, {kk}"),
    ]
    if isqrt(kk) ** 2 != kk:
        wrong.append((_rad(rr, kk), "swaps the number outside the radical with the number inside"))
    wrong.append((Q(kk), f"drops the leftover {m(f'\\sqrt{{{rr}}}')}"))
    return Problem(
        stem=choose(rng, f"Simplify {m(f'\\sqrt{{{n}}}')}.",
                    f"Which of the following is equal to {m(f'\\sqrt{{{n}}}')}?",
                    f"What is {m(f'\\sqrt{{{n}}}')} in simplest radical form?",
                    f"Write {m(f'\\sqrt{{{n}}}')} in simplest form."),
        answer=ans,
        fmt=_rfmt,
        wrong=wrong,
        steps=[
            f"Find the largest perfect square that divides {num(n)}: it is {num(kk * kk)}, because "
            f"{m(f'{n} = {kk * kk} \\times {rr}')}.",
            f"Split the root: {m(f'\\sqrt{{{n}}} = \\sqrt{{{kk * kk}}} \\times \\sqrt{{{rr}}} = {_rt(kk, rr)}')}.",
        ],
        tip=f"Check: {m(f'({_rt(kk, rr)})^2 = {kk * kk} \\times {rr} = {n}')}. \\checkmark",
        check=sp.sqrt(n),
        near=_rad_near(kk, rr),
    )


@template("MK")
def like_radicals(rng, lvl):
    r = rng.choice([2, 3, 5, 6, 7])
    if lvl == 2:
        a, b = rng.randint(1, 9), rng.randint(1, 9)
        op = rng.choice(["+", "-"])
        if op == "-":
            need(a > b)
        need(a != b or op == "+")
        c = a + b if op == "+" else a - b
        need(c > 0)
        ans = _rad(c, r)
        t = f"{_rt(a, r)} {op} {_rt(b, r)}"
        wrong = [(_rad(a * b, r), "multiplies the numbers in front instead of combining them")]
        if op == "+" and _clean(2 * r):
            wrong.append((_rad(c, 2 * r), "adds the numbers under the radicals too"))
            wrong.append((Q(c), f"drops the {m(f'\\sqrt{{{r}}}')} after adding"))
        else:
            wrong.append((_rad(a + b, r), "adds instead of subtracting"))
            wrong.append((Q(c), f"drops the {m(f'\\sqrt{{{r}}}')} after subtracting"))
        return Problem(
            stem=choose(rng, f"Simplify {m(t)}.", f"What is {m(t)}?", f"Which of the following is equal to {m(t)}?"),
            answer=ans,
            fmt=_rfmt,
            wrong=wrong,
            steps=[
                f"Both terms have {m(f'\\sqrt{{{r}}}')}, so they are like radicals: combine the numbers in front, "
                f"just like {m(f'{_cx(a)} {op} {_cx(b)}')}.",
                f"{m(f'{a} {op} {b} = {c}')}, so the answer is {m(_rt(c, r))}. The {m(f'\\sqrt{{{r}}}')} stays the same.",
            ],
            check=sp.sqrt(r) * a + (1 if op == "+" else -1) * sp.sqrt(r) * b,
            near=_rad_near(c, r),
        )

    # level 3: simplify first, then combine
    r = rng.choice([2, 3, 5])
    r = rng.choice([2, 3, 5, 6, 7])
    p, q = rng.sample(range(1, 7), 2)
    need(max(p, q) >= 2)
    n1, n2 = p * p * r, q * q * r
    need(n1 <= 200 and n2 <= 200)
    op = rng.choice(["+", "+", "-"])
    if op == "-":
        if p < q:
            p, q, n1, n2 = q, p, n2, n1
    c = p + q if op == "+" else p - q
    ans = _rad(c, r)
    t = f"\\sqrt{{{n1}}} {op} \\sqrt{{{n2}}}"
    wrong = [
        (sp.sqrt(n1 + n2) if op == "+" else sp.sqrt(n1 - n2),
         f"{'adds' if op == '+' else 'subtracts'} the numbers under the radicals; roots of different numbers cannot be combined that way")
        if _clean(n1 + n2 if op == "+" else n1 - n2) else (None, None),
        (_rad(c, 2 * r) if op == "+" else _rad(p * q, r), "adds the numbers under the radicals after simplifying" if op == "+"
         else "multiplies the numbers in front instead of subtracting") if (op == "-" or _clean(2 * r)) else (None, None),
        (_rad(p * q, r) if op == "+" else _rad(p + q, r), "multiplies the numbers in front instead of adding" if op == "+"
         else "adds instead of subtracting"),
        (Q(c), f"drops the {m(f'\\sqrt{{{r}}}')} after combining"),
    ]

    return Problem(
        stem=choose(rng, f"Simplify {m(t)}.", f"What is {m(t)} in simplest form?"),
        answer=ans,
        fmt=_rfmt,
        wrong=[w for w in wrong if w[0] is not None and not Q(w[0]).is_zero],
        steps=[
            "The numbers under the radicals are different, so simplify each radical first.",
            _simplify_both(n1, p, n2, q, r),
            f"Now they are like radicals: {m(f'{_rt(p, r)} {op} {_rt(q, r)} = {_rt(c, r)}')}.",
        ],
        check=sp.sqrt(n1) + (1 if op == "+" else -1) * sp.sqrt(n2),
        near=_rad_near(c, r),
    )


@template("MK")
def multiply_radicals(rng, lvl):
    if lvl == 2 and rng.random() < 0.3:
        # square of a radical term
        a = rng.randint(2, 6)
        r = rng.choice([2, 3, 5, 6, 7])
        ans = Q(a * a * r)
        t = f"({_rt(a, r)})^2"
        return Problem(
            stem=choose(rng, f"What is the value of {m(t)}?", f"Simplify {m(t)}."),
            answer=ans,
            fmt=_rfmt,
            wrong=[
                (Q(a * r), f"squares the {m(f'\\sqrt{{{r}}}')} but forgets to square the {a}"),
                (_rad(a * a, r), f"squares the {a} but not the {m(f'\\sqrt{{{r}}}')}"),
                (_rad(2 * a, r), "doubles instead of squaring"),
                (Q(a * a * r * r), f"squares {r} instead of {m(f'\\sqrt{{{r}}}')}"),
            ],
            steps=[
                f"Square each factor: {m(f'({_rt(a, r)})^2 = {a}^2 \\times (\\sqrt{{{r}}})^2')}.",
                f"{m(f'{a}^2 = {a * a}')} and {m(f'(\\sqrt{{{r}}})^2 = {r}')}, so the answer is "
                f"{m(f'{a * a} \\times {r} = {int_raw(ans)}')}.",
            ],
            check=(a * sp.sqrt(r)) ** 2,
        )
    if lvl == 2:
        a, b = rng.sample([2, 3, 5, 6, 7, 8, 10, 12, 14, 15, 18, 20, 21], 2)
        prod = a * b
        k, r = _split(prod)
        need(k >= 2 and prod <= 300)
        ans = _rad(k, r)
        t = f"\\sqrt{{{a}}} \\cdot \\sqrt{{{b}}}"
        wrong = [(Q(prod), "drops the radical sign")]
        if _clean(a + b):
            wrong.append((sp.sqrt(a + b), "adds the numbers under the radicals instead of multiplying"))
        if r > 1:
            wrong.append((_rad(k * k, r), f"pulls out {k * k} instead of its square root, {k}"))
        else:
            wrong.append((Q(prod // 2), "divides by 2 instead of taking the square root"))
        steps = [
            f"Multiply the numbers under the radicals: {m(f'{t} = \\sqrt{{{a} \\times {b}}} = \\sqrt{{{prod}}}')}.",
            (f"Simplify: {m(f'\\sqrt{{{prod}}} = \\sqrt{{{k * k} \\cdot {r}}} = {_rt(k, r)}')}." if r > 1 else
             f"{num(prod)} is a perfect square: {m(f'\\sqrt{{{prod}}} = {k}')}."),
        ]
        return Problem(
            stem=choose(rng, f"Simplify {m(t)}.", f"What is {m(t)} in simplest form?",
                        f"Which of the following is equal to {m(t)}?"),
            answer=ans,
            fmt=_rfmt,
            wrong=wrong,
            steps=steps,
            check=sp.sqrt(a) * sp.sqrt(b),
            near=_rad_near(k, r),
        )

    # level 3: coefficients and radicals
    c, d = rng.randint(2, 5), rng.randint(2, 5)
    a, b = rng.sample([2, 3, 5, 6, 7, 10, 12, 14, 15], 2)
    prod = a * b
    k, r = _split(prod)
    need(k >= 2 and r > 1 and prod <= 200)
    cd = c * d
    ans = _rad(cd * k, r)
    t = f"({_rt(c, a)})({_rt(d, b)})"
    return Problem(
        stem=choose(rng, f"Simplify {m(t)}.", f"What is {m(t)} in simplest form?"),
        answer=ans,
        fmt=_rfmt,
        wrong=[w for w in [
            (_rad((c + d) * k, r), "adds the numbers in front instead of multiplying them"),
            (_rad(cd * k * k, r), f"pulls {k * k} out of the radical instead of its square root, {k}"),
            (_rad(cd, a + b) if _clean(a + b) else None, "adds the numbers under the radicals"),
            (_rad(k * max(c, d), r), "multiplies by only one of the numbers in front"),
            (_rad(cd, r), f"forgets to multiply by the {k} that came out of the radical"),
            (_rad(cd + k, r), f"adds the {k} that came out of the radical instead of multiplying"),
        ] if w[0] is not None],
        steps=[
            f"Multiply the numbers in front and the numbers under the radicals separately: "
            f"{m(f'{c} \\times {d} = {cd}')} and {m(f'\\sqrt{{{a}}} \\cdot \\sqrt{{{b}}} = \\sqrt{{{prod}}}')}.",
            f"Simplify the radical: {m(f'\\sqrt{{{prod}}} = \\sqrt{{{k * k} \\cdot {r}}} = {_rt(k, r)}')}.",
            f"Multiply: {m(f'{cd} \\times {_rt(k, r)} = {_rt(cd * k, r)}')}.",
        ],
        check=c * sp.sqrt(a) * d * sp.sqrt(b),
        near=lambda _r: [_rad(cd * k * 2, r), _rad(cd * k + cd, r), _rad(cd * k - cd, r), _rad(cd * k + 2 * k, r)],
    )


@template("MK")
def solve_square(rng, lvl):
    if lvl == 1:
        k = rng.choice(list(range(3, 21)) + [25])
        n2 = k * k
        v = rng.choice(["x", "x", "y", "n"])
        form = rng.choice(["plain", "plain", "zero", "plus"])
        c = rng.randint(1, 20)
        if form == "plain":
            eq, first = f"{v}^2 = {n2}", None
        elif form == "zero":
            eq, first = f"{v}^2 - {n2} = 0", f"Add {n2} to both sides: {m(f'{v}^2 = {n2}')}."
        else:
            eq, first = f"{v}^2 + {c} = {n2 + c}", f"Subtract {c} from both sides: {m(f'{v}^2 = {n2}')}."
        wrong = [
            (Q(-k), "is the negative solution, but the question asks for the positive one"),
            (R(n2, 2), "divides by 2 instead of taking the square root"),
            (Q(n2), "forgets to take the square root"),
            (Q(k + 1), None),
        ]
        if form == "plus":
            wrong.append((sp.sqrt(n2 + 2 * c) if isqrt(n2 + 2 * c) ** 2 == n2 + 2 * c else Q(k - 1),
                          f"adds {c} instead of subtracting it" if isqrt(n2 + 2 * c) ** 2 == n2 + 2 * c else None))
        steps = ([first] if first else []) + [
            f"Undo the square by taking the square root: {m(f'{v} = \\sqrt{{{n2}}}')} or {m(f'{v} = -\\sqrt{{{n2}}}')}.",
            f"{m(f'\\sqrt{{{n2}}} = {k}')}, and the positive solution is {m(f'{v} = {k}')}.",
        ]
        Xs = sp.Symbol(v)
        lhs, rhs = eq.split(" = ")
        return Problem(
            stem=choose(rng, f"If {m(eq)} and {m(v)} is positive, what is the value of {m(v)}?",
                        f"What is the positive solution of {m(eq)}?",
                        f"If {m(eq)} and {m(f'{v} > 0')}, what is {m(v)}?"),
            answer=Q(k),
            fmt=num,
            neg_ok=True,
            wrong=wrong,
            steps=steps,
            check=max(sp.solve(sp.Eq(sp.sympify(lhs.replace("^", "**")), sp.sympify(rhs)), Xs)),
            verify=lambda val: val * val == n2 and val > 0,
        )
    X = sp.Symbol("x")
    k = rng.randint(2, 12)
    a = rng.choice([1, 2, 3, 4, 5, 9])
    c = rng.choice([0, 0, rng.randint(1, 20)])
    need(a > 1 or c > 0)
    sgn = rng.choice(["+", "-"])
    cval = c if sgn == "+" else -c
    d = a * k * k + cval
    need(d > 0)
    lhs = (f"{a if a > 1 else ''}x^2" + (f" {sgn} {c}" if c else ""))
    solve_steps = []
    if c:
        solve_steps.append(f"{'Subtract' if sgn == '+' else 'Add'} {c} on both sides: "
                           f"{m(f'{a if a > 1 else ''}x^2 = {a * k * k}')}.")
    if a > 1:
        solve_steps.append(f"Divide both sides by {a}: {m(f'x^2 = {k * k}')}.")
    if lvl == 2:
        want_neg = rng.random() < 0.5
        ans = Q(-k if want_neg else k)
        wrong = [
            (-ans, f"is the {'positive' if want_neg else 'negative'} solution, but the question says "
                   f"{m('x < 0' if want_neg else 'x > 0')}"),
            (Q(k * k) * (-1 if want_neg else 1), "forgets to take the square root"),
        ]
        wrong.append((Q((-1 if want_neg else 1) * (k + 1)), None))
        if a in (4, 9):
            wrong.append((ans * isqrt(a), f"forgets to divide by {a}"))
        elif a > 1:
            wrong.append((ans * a, f"multiplies by {a} instead of dividing"))
        return Problem(
            stem=f"If {m(f'{lhs} = {d}')} and {m('x < 0' if want_neg else 'x > 0')}, what is the value of {m('x')}?",
            answer=ans,
            fmt=num,
            neg_ok=True,
            wrong=wrong,
            steps=solve_steps + [
                f"Take the square root: {m(f'x = {k}')} or {m(f'x = -{k}')}. "
                f"Since {m('x < 0' if want_neg else 'x > 0')}, {m(f'x = {int_raw(ans)}')}.",
            ],
            check=[s for s in sp.solve(sp.Eq(a * X ** 2 + cval, d), X) if (s < 0) == want_neg][0],
            verify=lambda v: a * v * v + cval == d,
        )
    # level 3: all solutions
    pair = lambda v: m(f"{v}") + " and " + m(f"-{v}")
    wrong = [
        (m(f"{k}") + " only", "forgets the negative solution"),
        (pair(k * k), "forgets to take the square root"),
    ]
    if a in (4, 9):
        wrong.append((pair(k * isqrt(a)), f"forgets to divide by {a}"))
    wrong.append((pair(k + 1), None))
    wrong.append((m(f"-{k}") + " only", "keeps only the negative solution"))
    sols = sorted(sp.solve(sp.Eq(a * X ** 2 + cval, d), X))
    return Problem(
        stem=choose(rng, f"What are all the solutions of {m(f'{lhs} = {d}')}?",
                    f"Which of the following gives every solution of {m(f'{lhs} = {d}')}?"),
        answer=pair(k),
        fmt=lambda s: s,
        wrong=wrong,
        steps=solve_steps + [
            f"Take the square root of both sides. A positive number has two square roots: "
            f"{m(f'x = {k}')} or {m(f'x = -{k}')}.",
            f"Check: {m(f'{a if a > 1 else ''}({k})^2' + (f' {sgn} {c}' if c else '') + f' = {d}')}, and "
            f"{m(f'(-{k})^2')} is also {m(k * k)}. \\checkmark",
        ],
        check=pair(int(sols[1])) if len(sols) == 2 and sols[0] == -sols[1] else "no",
    )


@template("MK")
def rationalize(rng, lvl):
    r = rng.choice([2, 3, 5, 6, 7, 10])
    c = rng.randint(1, 30)
    val = Q(c) / sp.sqrt(r)
    g = gcd(c, r)
    ans_num, ans_den = c // g, r // g        # value = (ans_num/ans_den) sqrt(r)
    ans = R(ans_num, ans_den) * sp.sqrt(r)
    need(c != r and (g > 1 or rng.random() < 0.4))
    wrong = [
        (_rad(c, r), f"multiplies the top by {m(f'\\sqrt{{{r}}}')} but forgets that the bottom becomes {r}"),
        (R(c, r), f"multiplies only the bottom by {m(f'\\sqrt{{{r}}}')}"),
        (R(c, r * r) * sp.sqrt(r), f"thinks {m(f'\\sqrt{{{r}}} \\cdot \\sqrt{{{r}}} = {r * r}')}"),
        (sp.sqrt(r) / c, "turns the fraction upside down"),
    ]
    if ans_num != c or ans_den != 1:
        wrong.append((Q(c), f"cancels the {r} on the bottom against the {m(f'\\sqrt{{{r}}}')} on top"))
    frac_t = F(c, f"\\sqrt{{{r}}}")
    top = f"{c}\\sqrt{{{r}}}" if c != 1 else f"\\sqrt{{{r}}}"
    simp = latex(ans)
    steps = [
        f"Multiply the top and bottom by {m(f'\\sqrt{{{r}}}')}: "
        f"{m(f'{frac_t} \\times {F(f"\\sqrt{{{r}}}", f"\\sqrt{{{r}}}")} = {F(top, r)}')}, because "
        f"{m(f'\\sqrt{{{r}}} \\cdot \\sqrt{{{r}}} = {r}')}.",
    ]
    if g > 1:
        steps.append(f"Simplify {m(F(c, r))}: divide top and bottom by {g}, giving {m(simp)}.")
    else:
        steps.append(f"Nothing cancels, so the answer is {m(simp)}.")
    return Problem(
        stem=choose(rng, f"Which of the following is equal to {m(frac_t)}?",
                    f"Rationalize the denominator: {m(frac_t)}.",
                    f"Simplify {m(frac_t)} so that there is no radical in the denominator."),
        answer=ans,
        fmt=_rfmt,
        wrong=wrong,
        steps=steps,
        check=sp.radsimp(val),
        verify=lambda v: sp.simplify(v * sp.sqrt(r) - c) == 0,
        near=lambda rr: [ans * 2, ans * 3],
    )


PLAN = [
    # (template, level, count)  -- easy -> hard; 25 problems
    (perfect_root, 1, 3),
    (estimate_root, 1, 2),
    (root_fraction_decimal, 1, 2),
    (solve_square, 1, 1),
    (simplify_radical, 2, 3),
    (like_radicals, 2, 2),
    (multiply_radicals, 2, 2),
    (root_fraction_decimal, 2, 1),
    (estimate_root, 2, 1),
    (solve_square, 2, 1),
    (like_radicals, 3, 2),
    (multiply_radicals, 3, 1),
    (rationalize, 3, 2),
    (solve_square, 3, 1),
    (perfect_root, 3, 1),
]
