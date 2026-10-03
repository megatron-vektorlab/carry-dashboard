"""Chapter 3 - Factors, Multiples, Primes, GCF & LCM."""
import math

import sympy as sp

from ..core import (R, Q, Problem, need, num, frac, text, m, int_raw, frac_raw,
                    unit, person, soldier, choose, template)

NUM = 3
TITLE = r"Factors, Multiples, Primes, GCF \& LCM"
PART = 1

INTRO = r"""
Factors and multiples are the building blocks of fractions (Chapter 4) and of
many ``when will it happen again?'' word problems. Keep the vocabulary
straight and the rest is careful listing.

\begin{concept}{Vocabulary}
\begin{itemize}
\item A \textbf{factor} of $n$ divides $n$ evenly: the factors of $12$ are
  $1, 2, 3, 4, 6, 12$.
\item A \textbf{multiple} of $n$ is $n$ times a whole number: $12, 24, 36, \dots$
\item A \textbf{prime} number has exactly two factors, $1$ and itself:
  $2, 3, 5, 7, 11, 13, 17, 19, 23, 29, \dots$ The number $1$ is \emph{not}
  prime, and $2$ is the only even prime.
\item The \textbf{reciprocal} of $\frac{a}{b}$ is $\frac{b}{a}$; a number
  times its reciprocal is $1$.
\end{itemize}
\end{concept}

\begin{concept}{Prime factorization, GCF and LCM}
Split a number into primes with a factor tree:
$360 = 2^3 \times 3^2 \times 5$. For $36 = 2^2 \times 3^2$ and
$48 = 2^4 \times 3$:
\begin{itemize}
\item \textbf{GCF} (greatest common factor): shared primes, \emph{lowest}
  powers: $2^2 \times 3 = 12$.
\item \textbf{LCM} (least common multiple): every prime, \emph{highest}
  powers: $2^4 \times 3^2 = 144$.
\end{itemize}
\end{concept}

\begin{concept}{Divisibility rules}
\begin{tabular}{@{}ll@{}}
by $2$: last digit even & by $5$: last digit $0$ or $5$\\
by $3$: digit sum divisible by $3$ & by $6$: divisible by $2$ \emph{and} $3$\\
by $4$: last two digits divisible by $4$ & by $9$: digit sum divisible by $9$
\end{tabular}
\end{concept}

\begin{example}{Worked example}
One bus leaves the depot every $12$ minutes and another every $18$ minutes.
Both leave at 8:00 a.m. When do they next leave together?

\textbf{Solution.} You need the LCM of $12$ and $18$. Multiples of $18$:
$18, 36, \dots$; $36$ is also a multiple of $12$. They leave together again
after $36$ minutes, at 8:36 a.m.
\end{example}

\begin{tip}
Word-problem signal: ``greatest number of identical kits,'' ``largest equal
groups,'' or ``longest equal pieces'' means \textbf{GCF}. ``Next time
together,'' ``least number of packs so the counts match'' means \textbf{LCM}.
\end{tip}

\begin{trap}
\begin{itemize}
\item Mixing up GCF and LCM; the GCF is never larger than the smaller number,
  and the LCM is never smaller than the larger number.
\item Multiplying two numbers and calling it the LCM ($12 \times 18 = 216$, but
  the LCM is $36$).
\item Calling $1$ prime, or calling numbers like $51 = 3 \times 17$ and
  $91 = 7 \times 13$ prime.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _is_prime_td(n):
    """Independent primality test by trial division."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def _spf(n):
    d = 2
    while n % d:
        d += 1
    return d


def _factor_td(n):
    """Prime factorization by trial division -> list of (p, e)."""
    out, d = [], 2
    while n > 1:
        e = 0
        while n % d == 0:
            n //= d
            e += 1
        if e:
            out.append((d, e))
        d += 1
    return out


def _pf_tex(fs):
    return r" \times ".join(f"{p}^{{{e}}}" if e > 1 else f"{p}" for p, e in fs)


def _divs(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def _gcf_steps(nums):
    """Steps that find the GCF from prime factorizations."""
    fs = {n_: dict(_factor_td(n_)) for n_ in nums}
    lines = ", ".join(_pf_line(n_) for n_ in nums)
    shared = sorted(set.intersection(*[set(f) for f in fs.values()]))
    g = math.prod(p ** min(fs[n_][p] for n_ in nums) for p in shared)
    if shared:
        pw = _pf_tex([(p, min(fs[n_][p] for n_ in nums)) for p in shared])
        last = (f"Take each prime they \\emph{{all}} share, with its lowest power: "
                f"{m(pw + (f' = {g}' if pw != str(g) else ''))}.")
    else:
        last = "They share no prime factor, so the GCF is $1$."
    return [f"Write each number as a product of primes: {lines}.", last], g


def _lcm_steps(nums):
    fs = {n_: dict(_factor_td(n_)) for n_ in nums}
    lines = ", ".join(_pf_line(n_) for n_ in nums)
    primes = sorted(set().union(*[set(f) for f in fs.values()]))
    hi = [(p, max(fs[n_].get(p, 0) for n_ in nums)) for p in primes]
    L = math.prod(p ** e for p, e in hi)
    return [f"Write each number as a product of primes: {lines}.",
            f"Take every prime that appears, with its highest power: "
            f"{m(_pf_tex(hi) + f' = {int_raw(L)}')}."], L


def _mlist(vals, conj="and"):
    """$51$, $53$, $57$, and $91$ (separate math pieces so lines can break)."""
    vals = [m(int_raw(v)) for v in vals]
    return ", ".join(vals[:-1]) + f", {conj} " + vals[-1]


def _brk(vals):
    """A list of numbers as separate math pieces so the line can break."""
    return ", ".join(m(int_raw(v)) for v in vals)


def _pf_line(n_):
    fs = _factor_td(n_)
    return m(str(n_)) + " (prime)" if fs == [(n_, 1)] else m(f"{n_} = {_pf_tex(fs)}")


def _lst(vals):
    return ", ".join(int_raw(v) for v in vals)


# --------------------------------------------------------------------------
# primes
# --------------------------------------------------------------------------

_LOOKS_PRIME_1 = [1, 9, 21, 27, 33, 39, 49, 51, 57]
_LOOKS_PRIME_2 = [51, 57, 63, 69, 77, 81, 87, 91, 93, 111, 117, 119, 121, 123, 129, 133, 141, 143]


def _why_composite(n):
    if n == 1:
        return "is not prime; a prime has exactly two factors, and $1$ has only one"
    p = _spf(n)
    return f"is not prime: {m(rf'{n} = {p} \times {n // p}')}"


@template("MK")
def which_prime(rng, lvl):
    if lvl == 1 or rng.random() < 0.5:
        if lvl == 1:
            ans = rng.choice([v for v in range(2, 60) if _is_prime_td(v)])
            comps = rng.sample(_LOOKS_PRIME_1, 3)
        else:
            ans = rng.choice([v for v in range(53, 150) if _is_prime_td(v)])
            comps = rng.sample(_LOOKS_PRIME_2, 3)
        need(ans not in comps)
        tests = "; ".join(m(rf"{c} = {_spf(c)} \times {c // _spf(c)}") for c in sorted(comps) if c != 1)
        root = math.isqrt(ans)
        small = [p for p in (2, 3, 5, 7, 11) if p <= root]
        if ans == 2:
            why_ans = "$2$ is prime: its only factors are $1$ and $2$ (it is the only even prime)."
        elif not small:
            why_ans = f"{m(ans)} is prime: its only factors are $1$ and {m(ans)}."
        else:
            nxt = next(p for p in (2, 3, 5, 7, 11, 13) if p > root)
            why_ans = (f"{m(ans)} is not divisible by {', '.join(m(p) for p in small)}, and "
                       f"{m(rf'{nxt} \times {nxt} = {nxt * nxt}')} is already more than {m(ans)}, "
                       f"so {m(ans)} is prime.")
        steps = ["A prime number has exactly two factors: $1$ and itself."]
        if tests:
            steps.append(f"Each of the other choices has another factor: {tests}."
                         + (" And $1$ is not prime." if 1 in comps else ""))
        else:
            steps.append("$1$ is not prime.")
        steps.append(why_ans)
        return Problem(
            stem=choose(rng, f"Which of the numbers {_mlist(sorted(comps + [ans]))} is prime?",
                        f"Which one of {_mlist(sorted(comps + [ans]), 'or')} is a prime number?"),
            answer=Q(ans),
            fmt=num,
            wrong=[(Q(c), _why_composite(c)) for c in comps],
            steps=steps,
            verify=lambda v: _is_prime_td(int(v)) and not any(_is_prime_td(c) for c in comps),
            check=Q([v for v in comps + [ans] if sp.isprime(v)][0]),
            near=lambda r: [],
        )
    # level 2 variant: which is NOT prime
    ans = rng.choice(_LOOKS_PRIME_2)
    primes = rng.sample([v for v in range(31, 150) if _is_prime_td(v)], 3)
    p = _spf(ans)
    return Problem(
        stem=choose(rng, f"Which of the numbers {_mlist(sorted(primes + [ans]))} is \\emph{{not}} prime?",
                    f"Which one of {_mlist(sorted(primes + [ans]), 'or')} is \\emph{{not}} a prime number?"),
        answer=Q(ans),
        fmt=num,
        wrong=[(Q(v), "is prime; its only factors are $1$ and itself") for v in primes],
        steps=[
            "Test each choice for small prime factors: $2, 3, 5, 7, 11$.",
            f"{m(ans)} {'has digit sum ' + m(sum(map(int, str(ans)))) + ', so it is divisible by $3$: ' if p == 3 else 'is divisible by ' + m(p) + ': '}"
            f"{m(rf'{ans} = {p} \times {ans // p}')}.",
            f"So {m(ans)} has factors other than $1$ and itself; it is not prime. The other "
            "three choices have no such factors.",
        ],
        verify=lambda v: not _is_prime_td(int(v)) and all(_is_prime_td(c) for c in primes),
        check=Q([v for v in primes + [ans] if not sp.isprime(v)][0]),
        near=lambda r: [],
    )


@template("MK")
def prime_factorization(rng, lvl):
    n_ = rng.randint(60, 1200)
    fs = _factor_td(n_)
    need(all(p <= 11 for p, _ in fs) and sum(e for _, e in fs) >= 4 and len(fs) >= 2
         and any(e >= 2 for _, e in fs) and fs[0][0] == 2)
    ans = m(_pf_tex(fs))
    # wrong choices
    big = max(fs, key=lambda t: t[1])
    wrong = []
    # one exponent too small
    p0, e0 = big
    alt = [(p, e - 1 if p == p0 else e) for p, e in fs]
    alt = [(p, e) for p, e in alt if e > 0]
    wrong.append((m(_pf_tex(alt)), f"multiplies out to {num(n_ // p0)}, not {num(n_)}"))
    # a composite factor sneaks in
    if any(p == 2 for p, _ in fs) and any(p == 5 for p, _ in fs):
        e2_ = dict(fs)[2]
        e5_ = dict(fs)[5]
        rest = [(p, e) for p, e in fs if p not in (2, 5)]
        comp = ([(2, e2_ - 1)] if e2_ > 1 else []) + rest + ([(5, e5_ - 1)] if e5_ > 1 else [])
        comp_tex = (_pf_tex(comp) + r" \times 10") if comp else "10"
        wrong.append((m(comp_tex), "uses $10$, which is not prime"))
    else:
        d2 = dict(fs)
        if d2.get(2, 0) >= 2:
            rest = [(p, e) for p, e in fs if p != 2]
            comp = ([(2, d2[2] - 2)] if d2[2] > 2 else []) + rest
            wrong.append((m("4 \\times " + _pf_tex(comp)), "uses $4$, which is not prime"))
    # drop the exponents
    wrong.append((m(r" \times ".join(str(p) for p, _ in fs)),
                  f"lists each prime only once; that product is only {num(math.prod(p for p, _ in fs))}"))
    # one exponent too big
    p1 = min(fs)[0]
    alt2 = [(p, e + 1 if p == p1 else e) for p, e in fs]
    wrong.append((m(_pf_tex(alt2)), f"multiplies out to {num(n_ * p1)}, not {num(n_)}"))
    # division steps
    steps, cur = [], n_
    for p, e in fs:
        chain = [cur]
        for _ in range(e):
            cur //= p
            chain.append(cur)
        steps.append(f"Divide by {m(p)} {'as many times as you can' if e > 1 else 'once'}: "
                     f"{m(r' \to '.join(int_raw(c) for c in chain))} "
                     f"({m(e)} factor{'s' if e > 1 else ''} of {m(p)}).")
    steps = steps[:3] if len(steps) > 3 else steps
    if len(fs) > 3:
        steps[-1] = steps[-1].rstrip(".") + f", and the last factor is {m(fs[-1][0])}."
    steps.append(f"So {m(f'{int_raw(n_)} = {_pf_tex(fs)}')}.")
    return Problem(
        stem=choose(rng, f"What is the prime factorization of {num(n_)}?",
                    f"Which of the following is the prime factorization of {num(n_)}?",
                    f"Which shows {num(n_)} written as a product of prime numbers?"),
        answer=ans,
        fmt=text,
        wrong=wrong,
        steps=steps,
        check=m(_pf_tex(sorted(sp.factorint(n_).items()))),
        verify=lambda v: v == ans and math.prod(p ** e for p, e in fs) == n_,
    )


# --------------------------------------------------------------------------
# GCF and LCM
# --------------------------------------------------------------------------

@template("MK")
def gcf(rng, lvl):
    if lvl == 1:
        g = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 12])
        a_, b_ = rng.sample(range(2, 9), 2)
        need(math.gcd(a_, b_) == 1)
        x_, y_ = sorted([g * a_, g * b_])
        need(y_ <= 72)
        steps = [f"List the factors of {m(x_)}: {_brk(_divs(x_))}.",
                 f"List the factors of {m(y_)}: {_brk(_divs(y_))}.",
                 f"The greatest number in both lists is {m(g)}."]
        nums = [x_, y_]
    else:
        if rng.random() < 0.5:
            g = rng.choice([4, 6, 8, 9, 12, 14, 15, 16, 18])
            a_, b_ = rng.sample(range(2, 10), 2)
            need(math.gcd(a_, b_) == 1)
            nums = sorted([g * a_, g * b_])
            need(nums[1] <= 150)
        else:
            g = rng.choice([2, 3, 4, 5, 6, 8])
            ks = rng.sample(range(2, 12), 3)
            need(math.gcd(math.gcd(ks[0], ks[1]), ks[2]) == 1)
            nums = sorted(g * k for k in ks)
            need(nums[2] <= 100)
        steps, g2 = _gcf_steps(nums)
        need(g2 == g)
    L = math.lcm(*nums)
    smaller_cf = [d for d in _divs(g) if 1 < d < g]
    wrong = [(Q(L), "is the least common multiple, not the greatest common factor")]
    if smaller_cf:
        d = rng.choice(smaller_cf)
        wrong.append((Q(d), "is a common factor, but not the greatest one"))
    if nums[0] != g:
        wrong.append((Q(nums[0]), f"is the smallest number, but it is not a factor of {m(nums[1])}"))
    wrong.append((Q(g * 2) if all(n_ % (2 * g) for n_ in nums) else Q(g + 1), None))
    shown = rng.sample(nums, len(nums))
    names = ", ".join(m(v) for v in shown[:-1]) + (", and " if len(shown) > 2 else " and ") + m(shown[-1])
    return Problem(
        stem=choose(rng, f"What is the greatest common factor of {names}?",
                    f"What is the GCF of {names}?"),
        answer=Q(g),
        fmt=num,
        wrong=wrong,
        steps=steps,
        check=Q(max(d for d in range(1, nums[0] + 1) if all(n_ % d == 0 for n_ in nums))),
    )


def _names(nums):
    return ", ".join(m(v) for v in nums[:-1]) + (", and " if len(nums) > 2 else " and ") + m(nums[-1])


@template("MK")
def lcm(rng, lvl):
    if lvl == 3:
        if rng.random() < 0.5:
            nums = sorted(rng.sample(range(2, 21), 3))
            need(math.prod(nums) != math.lcm(*nums))
        else:
            nums = sorted(rng.sample(range(2, 13), 4))
        L = math.lcm(*nums)
        need(L <= 360)
        need(not any(b_ % a_ == 0 for a_ in nums for b_ in nums if a_ < b_) or len(nums) == 4)
        wrong = [(Q(2 * L), "is divisible by all of them, but it is not the smallest such number")]
        if math.prod(nums) not in (L, 2 * L):
            wrong.append((Q(math.prod(nums)), "multiplies all the numbers; that works, but it is not the smallest"))
        for k in nums:
            sub = math.lcm(*[v for v in nums if v != k])
            if sub != L:
                wrong.append((Q(sub), f"is not divisible by {m(k)}"))
        wrong.append((Q(L + max(nums)), None))
        steps, _ = _lcm_steps(nums)
        shown = rng.sample(nums, len(nums))
        return Problem(
            stem=choose(rng, f"What is the smallest positive number that is divisible by each of {_names(shown)}?",
                        f"What is the least common multiple of {_names(shown)}?"),
            answer=Q(L),
            fmt=num,
            wrong=wrong,
            steps=steps + [f"Check: {m(int_raw(L))} divided by each of the numbers gives a whole number."],
            check=Q(next(v for v in range(1, 10 ** 4) if all(v % k == 0 for k in nums))),
        )
    if lvl == 1:
        a_, b_ = sorted(rng.sample(range(3, 31), 2))
        g = math.gcd(a_, b_)
        L = math.lcm(a_, b_)
        need(g > 1 and L // b_ <= 6 and L <= 120)
        k = L // b_
        mults = [b_ * i for i in range(1, k + 1)]
        if k == 1:
            steps = [f"{m(b_)} is itself a multiple of {m(a_)}: {m(rf'{a_} \times {b_ // a_} = {b_}')}.",
                     f"So the least common multiple is the larger number, {m(b_)}."]
        else:
            steps = [f"List multiples of the larger number, {m(b_)}: {_brk(mults)}.",
                     f"The first one that is also a multiple of {m(a_)} is {m(L)} "
                     f"({m(rf'{a_} \times {L // a_} = {L}')})."]
        nums = [a_, b_]
    else:
        if rng.random() < 0.6:
            a_, b_ = sorted(rng.sample(range(6, 41), 2))
            g = math.gcd(a_, b_)
            need(g > 1 and b_ % a_ != 0 and math.lcm(a_, b_) <= 360)
            nums = [a_, b_]
        else:
            nums = sorted(rng.sample(range(3, 21), 3))
            need(math.lcm(*nums) <= 180 and math.prod(nums) != math.lcm(*nums))
            need(all(nums[2] % v for v in nums[:2]))
        L = math.lcm(*nums)
        steps, _ = _lcm_steps(nums)
    g = math.gcd(*nums)
    wrong = [(Q(math.prod(nums)), "multiplies the numbers; that is a common multiple, but not the least one"),
             (Q(g), "is the greatest common factor, not the least common multiple"),
             (Q(2 * L), "is a common multiple, but not the least one"),
             (Q(L // 2) if any((L // 2) % v for v in nums) else Q(L - nums[0]), None)]
    shown = rng.sample(nums, len(nums))
    return Problem(
        stem=choose(rng, f"What is the least common multiple of {_names(shown)}?",
                    f"What is the LCM of {_names(shown)}?",
                    f"What is the smallest number that is a multiple of both {_names(shown)}?"
                    if len(nums) == 2 else f"Find the least common multiple of {_names(shown)}."),
        answer=Q(L),
        fmt=num,
        wrong=wrong,
        steps=steps,
        check=Q(next(v for v in range(nums[-1], 10 ** 5, nums[-1]) if all(v % k == 0 for k in nums))),
    )


_ROWS = [("A drill sergeant wants to line up {N} recruits in equal rows with no one left over.",
          "row lengths", "recruits"),
         ("A teacher wants to set up {N} chairs in equal rows with none left over.", "row lengths", "chairs"),
         ("A gardener wants to plant {N} tomato plants in equal rows with none left over.", "row lengths",
          "plants"),
         ("A supply clerk wants to stack {N} boxes in equal piles with none left over.", "pile sizes", "boxes")]


@template("MK")
def num_factors(rng, lvl):
    n_ = rng.choice([v for v in range(12, 201) if 6 <= len(_divs(v)) <= 12])
    ds = _divs(n_)
    cnt = len(ds)
    pairs = [(d, n_ // d) for d in ds if d * d <= n_]
    square = math.isqrt(n_) ** 2 == n_
    pf = _factor_td(n_)
    wrong = [(Q(cnt - 2), f"leaves out $1$ and {m(n_)}"),
             (Q(sum(e for _, e in pf)), "counts only the prime factors")]
    if square:
        wrong.insert(0, (Q(cnt + 1), f"counts the factor {m(math.isqrt(n_))} twice"))
    else:
        wrong.append((Q(cnt // 2), "counts the factor pairs instead of the factors"))
    wrong.append((Q(cnt - 1), None))
    pair_txt = ", ".join(m(rf"{a} \times {b}") for a, b in pairs)
    if rng.random() < 0.3:
        setup, what, noun = rng.choice(_ROWS)
        unit_ = "row" if "row" in what else "pile"
        inner = [d for d in ds if 1 < d < n_]
        return Problem(
            stem=(setup.format(N=m(n_)) + f" Each {unit_} must have at least {m(2)} {noun}, and there must be at "
                  f"least {m(2)} {unit_}s. How many different {what} are possible?"),
            answer=Q(cnt - 2),
            fmt=num,
            wrong=[(Q(cnt), f"also counts {m(1)} per {unit_} and a single {unit_} of {m(n_)}, which the problem rules out"),
                   (Q(cnt - 1), "rules out only one of the two forbidden cases"),
                   (Q(sum(e for _, e in pf)), "counts only the prime factors"),
                   (Q(cnt - 3), None)],
            steps=[f"Each possible {what[:-1]} is a factor of {m(n_)}.",
                   f"Factor pairs of {m(n_)}: {pair_txt}.",
                   f"Leave out {m(1)} and {m(n_)} (a {unit_} of {m(1)}, or only one {unit_}). That leaves "
                   f"{_brk(inner)}: {m(cnt - 2)} possibilities."],
            check=Q(sum(1 for d in range(2, n_) if n_ % d == 0)),
        )
    if rng.random() < 0.35:
        setup, what, noun = rng.choice(_ROWS)
        unit_ = "row" if "row" in what else "pile"
        stem = (setup.format(N=m(n_)) + f" How many different {what} are possible, counting "
                f"{m(1)} per {unit_} and all {m(n_)} in one {unit_}?")
        lead = f"Each possible {what[:-1]} is a factor of {m(n_)}, so count the factors of {m(n_)}."
    else:
        stem = choose(rng, f"How many positive factors does {m(n_)} have?",
                      f"How many different whole numbers divide {m(n_)} evenly?")
        lead = None
    steps = ([lead] if lead else []) + [
        f"List the factor pairs, starting from $1$: {pair_txt}.",
        f"The factors are {_brk(ds)}"
        + (f"; {m(math.isqrt(n_))} pairs with itself, so count it once." if square else "."),
        f"Count them: {m(cnt)} factors.",
    ]
    return Problem(
        stem=stem,
        answer=Q(cnt),
        fmt=num,
        wrong=wrong,
        steps=steps,
        tip=(f"Shortcut: {m(f'{n_} = {_pf_tex(pf)}')}; add $1$ to each exponent and multiply: "
             f"{m(r' \times '.join(f'({e} + 1)' for _, e in pf) + f' = {cnt}')}."),
        check=Q(sp.divisor_count(n_)),
    )


# --------------------------------------------------------------------------
# divisibility and vocabulary
# --------------------------------------------------------------------------

_RULE = {
    2: "its last digit is even",
    3: "its digit sum is divisible by $3$",
    4: "the number formed by its last two digits is divisible by $4$",
    5: "its last digit is $0$ or $5$",
    6: "it is divisible by both $2$ and $3$",
    9: "its digit sum is divisible by $9$",
}


def _fails(n_, k):
    """Explain why n is not divisible by k (by the rule)."""
    s = sum(map(int, str(n_)))
    if k in (3, 9):
        return f"its digit sum, {m(s)}, is not divisible by {m(k)}"
    if k == 4:
        return f"its last two digits, {m(str(n_)[-2:])}, are not divisible by $4$"
    if k == 2:
        return "it is odd"
    if k == 5:
        return f"it does not end in $0$ or $5$"
    if k == 6:
        return "it is odd" if n_ % 2 else f"its digit sum, {m(s)}, is not divisible by $3$"
    return f"it is not divisible by {m(k)}"


def _passes(n_, k):
    s = sum(map(int, str(n_)))
    if k in (3, 9):
        return f"digit sum {m(s)}"
    if k == 4:
        return f"last two digits {m(str(n_)[-2:])}"
    if k == 2:
        return "even"
    if k == 5:
        return f"ends in {m(str(n_)[-1])}"
    return f"even, digit sum {m(s)}"


@template("MK")
def divisibility(rng, lvl):
    if lvl == 1:
        k = rng.choice([3, 4, 6, 9])
        ans = rng.randint(12, 99) * k
        need(100 <= ans <= 999)
        wrong = []
        tries = 0
        while len(wrong) < 3 and tries < 200:
            tries += 1
            v = rng.randint(101, 999)
            if v % k == 0 or v in [w for w, _ in wrong]:
                continue
            if k == 9 and v % 3 == 0:
                wrong.append((v, f"is divisible by $3$, but {_fails(v, 9)}"))
            elif k == 6 and v % 2 == 0:
                wrong.append((v, f"is even, but {_fails(v, 3)}"))
            elif k == 6 and v % 3 == 0:
                wrong.append((v, f"has a digit sum divisible by $3$, but it is odd"))
            elif k == 4 and v % 2 == 0:
                wrong.append((v, f"is even, but {_fails(v, 4)}"))
            elif k == 3 and rng.random() < 0.5:
                wrong.append((v, f"is not divisible by $3$: {_fails(v, 3)}"))
        need(len(wrong) == 3)
        ks = [k]
        allv = sorted([ans] + [w for w, _ in wrong])
        stem = choose(rng, f"Which of the numbers {_mlist(allv)} is divisible by {m(k)}?",
                      f"Which one of {_mlist(allv, 'or')} can be divided evenly by {m(k)}?")
        steps = [f"Rule: a number is divisible by {m(k)} when {_RULE[k]}.",
                 f"{m(ans)} passes ({_passes(ans, k)}): {m(rf'{ans} \div {k} = {ans // k}')}.",
                 "Each of the other choices fails the rule."]
    else:
        k1, k2 = rng.choice([(3, 4), (2, 9), (3, 5), (4, 9), (5, 6), (4, 5)])
        L = k1 * k2
        ans = rng.randint(4, 999 // L) * L
        need(ans >= 100)
        cands = []
        while len(cands) < 2:
            v = rng.randint(101, 999)
            if v % k1 == 0 and v % k2 and v not in cands:
                cands.append(v)
        c2 = None
        while c2 is None:
            v = rng.randint(101, 999)
            if v % k2 == 0 and v % k1:
                c2 = v
        wrong = [(cands[0], f"is divisible by {m(k1)}, but not by {m(k2)}: {_fails(cands[0], k2)}"),
                 (c2, f"is divisible by {m(k2)}, but not by {m(k1)}: {_fails(c2, k1)}"),
                 (cands[1], f"is divisible by {m(k1)}, but not by {m(k2)}: {_fails(cands[1], k2)}")]
        ks = [k1, k2]
        allv = sorted([ans] + [w for w, _ in wrong])
        stem = choose(rng, f"Which of the numbers {_mlist(allv)} is divisible by both {m(k1)} and {m(k2)}?",
                      f"Which one of {_mlist(allv, 'or')} is divisible by {m(k1)} \\emph{{and}} by {m(k2)}?")
        steps = [f"Divisible by {m(k1)}: {_RULE[k1]}. Divisible by {m(k2)}: {_RULE[k2]}.",
                 f"{m(ans)} passes both tests ({_passes(ans, k1)}; {_passes(ans, k2)}): "
                 f"{m(rf'{ans} \div {k1 * k2} = {ans // (k1 * k2)}')}.",
                 "Each of the other choices fails one of the tests."]
    return Problem(
        stem=stem,
        answer=Q(ans),
        fmt=num,
        wrong=[(Q(v), w) for v, w in wrong],
        steps=steps,
        verify=lambda v: all(int(v) % k == 0 for k in ks) and all(any(w % k for k in ks) for w, _ in wrong),
        check=Q(next(v for v in [ans] + [w for w, _ in wrong] if all(v % k == 0 for k in ks))),
        near=lambda r: [],
    )


@template("MK")
def vocab(rng, lvl):
    kind = rng.choice(["factor", "multiple", "reciprocal"])
    if kind == "factor":
        n_ = rng.choice([v for v in range(24, 181) if any(6 <= d <= v // 2 for d in _divs(v))])
        ds = [d for d in _divs(n_) if 6 <= d <= n_ // 2]
        ans = rng.choice(ds)
        nonf = [v for v in range(5, 30) if n_ % v and v != ans]
        bad = rng.sample(nonf, 2)
        return Problem(
            stem=choose(rng, f"Which of the following is a factor of {m(n_)}?",
                        f"Which number is a factor of {m(n_)}?"),
            answer=Q(ans),
            fmt=num,
            wrong=[(Q(2 * n_), f"is a multiple of {m(n_)}, not a factor"),
                   (Q(bad[0]), f"does not divide {m(n_)} evenly"),
                   (Q(bad[1]), f"does not divide {m(n_)} evenly")],
            steps=[f"A factor of {m(n_)} divides it with no remainder.",
                   f"{m(rf'{n_} \div {ans} = {n_ // ans}')}, so {m(ans)} is a factor. "
                   f"{m(2 * n_)} is bigger than {m(n_)}, so it can only be a multiple."],
            verify=lambda v: n_ % int(v) == 0,
            check=Q(next(v for v in sorted([ans, 2 * n_] + bad) if n_ % v == 0)),
            near=lambda r: [],
        )
    if kind == "multiple":
        k = rng.randint(4, 20)
        ans = k * rng.randint(3, 15)
        facs = [d for d in _divs(k) if 1 < d < k]
        nonm = [v for v in range(ans - 15, ans + 16) if v % k and v > k]
        bad = rng.sample(nonm, 3)
        wrong = [(Q(bad[0]), f"is not {m(k)} times a whole number"),
                 (Q(bad[1]), f"is not {m(k)} times a whole number")]
        wrong.insert(0, (Q(rng.choice(facs)), f"is a factor of {m(k)}, not a multiple") if facs
                     else (Q(bad[2]), f"is not {m(k)} times a whole number"))
        return Problem(
            stem=choose(rng, f"Which of the following is a multiple of {m(k)}?",
                        f"Which number is a multiple of {m(k)}?"),
            answer=Q(ans),
            fmt=num,
            wrong=wrong,
            steps=[f"A multiple of {m(k)} is {m(k)} times a whole number.",
                   f"{m(rf'{k} \times {ans // k} = {ans}')}, so {m(ans)} is a multiple of {m(k)}."],
            verify=lambda v: int(v) % k == 0 and int(v) >= k,
            check=Q(next(v for v in sorted([ans] + [int(w) for w, _ in wrong]) if v % k == 0 and v >= k)),
            near=lambda r: [],
        )
    if rng.random() < 0.35:
        b_ = rng.randint(3, 25)
        v, ans, shown = Q(b_), R(1, b_), str(b_)
    else:
        a_, b_ = rng.choice([(p_, q_) for p_ in range(2, 10) for q_ in range(2, 12)
                             if p_ != q_ and math.gcd(p_, q_) == 1])
        v = R(a_, b_)
        ans, shown = 1 / v, frac_raw(v)
    return Problem(
        stem=choose(rng, f"What is the reciprocal of {m(shown)}?",
                    f"Which number is the reciprocal of {m(shown)}?"),
        answer=ans,
        fmt=frac,
        wrong=[(-v, "is the opposite, not the reciprocal"),
               (-ans, "is the opposite of the reciprocal; a reciprocal keeps the sign"),
               (v, "is the number itself, not its reciprocal")],
        steps=[f"The reciprocal flips the fraction: the numerator and denominator trade places.",
               (f"Write {m(shown)} as {m(F_(shown, 1))}; flipped, it becomes {m(frac_raw(ans))}."
                if v.q == 1 else f"Flipped, {m(shown)} becomes {m(frac_raw(ans))}.")
               + f" Check: {m(rf'{shown} \times {frac_raw(ans)} = 1')}."],
        verify=lambda w: Q(w) * v == 1,
        neg_ok=True,
        sort=False,
        near=lambda r: [],
    )


def F_(p, q):
    return rf"\frac{{{p}}}{{{q}}}"


# --------------------------------------------------------------------------
# word problems
# --------------------------------------------------------------------------

def _clock(start_h, start_m, add_min):
    t = start_h * 60 + start_m + add_min
    h, mi = divmod(t, 60)
    suffix = "a.m." if h % 24 < 12 else "p.m."
    h12 = h % 12 or 12
    return f"{h12}:{mi:02d} {suffix}"


@template("AR")
def lcm_word(rng, lvl):
    a_, b_ = sorted(rng.sample(range(4, 21), 2))
    need(math.gcd(a_, b_) > 1 and b_ % a_ != 0)
    L = math.lcm(a_, b_)
    need(L <= 120)
    g = math.gcd(a_, b_)
    if lvl == 2:
        ctx = rng.choice([
            (f"Two buses leave a station at the same time. One bus leaves every {m(a_)} minutes and "
             f"the other every {m(b_)} minutes. After how many minutes will they next leave at the "
             "same time?", unit(num, "minute")),
            (f"{soldier(rng)} checks the generator every {m(a_)} hours and refuels the vehicles every "
             f"{m(b_)} hours. Both tasks were done at 0600. After how many hours will both tasks next "
             "fall at the same time?", unit(num, "hour")),
            (f"{person(rng).name} runs every {m(a_)} days and swims every {m(b_)} days. "
             "Today is a run day and a swim day. In how many days will both happen on the same day again?",
             unit(num, "day")),
            (f"Two warning lights blink together. One blinks every {m(a_)} seconds and the other every "
             f"{m(b_)} seconds. After how many seconds will they next blink at the same time?",
             unit(num, "second")),
        ])
        steps = ([f"The events line up again after a common multiple of {m(a_)} and {m(b_)}; the "
                  "first time is the least common multiple."]
                 + [f"Multiples of {m(b_)}: {_brk([b_ * i for i in range(1, L // b_ + 1)])}. "
                    f"The first one that is also a multiple of {m(a_)} is {m(L)}."])
        return Problem(
            stem=ctx[0], answer=Q(L), fmt=ctx[1],
            wrong=[(Q(a_ * b_), "multiplies the two numbers; that is a common multiple, but not the first one"),
                   (Q(g), "is the greatest common factor, not the least common multiple"),
                   (Q(a_ + b_), "adds the two numbers"),
                   (Q(2 * L), "is the second time they line up, not the first")],
            steps=steps,
            check=Q(next(t for t in range(1, 10 ** 4) if t % a_ == 0 and t % b_ == 0)),
        )
    if rng.random() < 0.5:
        h0 = rng.choice([6, 7, 8, 9, 10])
        mm = rng.choice([0, 0, 15, 30])
        start = _clock(h0, mm, 0)
        ans = _clock(h0, mm, L)
        prod_t = _clock(h0, mm, a_ * b_)
        wrong = [(_clock(h0, mm, a_ * b_), f"uses {m(rf'{a_} \times {b_} = {a_ * b_}')} minutes, "
                                          "a common multiple but not the least one"),
                 (_clock(h0, mm, g), f"uses the greatest common factor, {m(g)} minutes"),
                 (_clock(h0, mm, 2 * L), "is the second time they leave together, not the first"),
                 (_clock(h0, mm, a_ + b_), "adds the two waiting times")]
        need(len({ans} | {w for w, _ in wrong}) == 5 and prod_t != ans)
        who = rng.choice([("Two shuttle buses", "shuttle"), ("Two trains", "train"), ("Two convoys", "convoy")])
        return Problem(
            stem=(f"At {start}, {who[0].lower()} leave a station together. One {who[1]} leaves every "
                  f"{m(a_)} minutes and the other every {m(b_)} minutes. At what time will they next "
                  "leave together?"),
            answer=ans,
            fmt=text,
            wrong=wrong,
            steps=_lcm_steps([a_, b_])[0] + [f"They leave together again after {m(L)} minutes: "
                                             f"{m(L)} minutes after {start} is {ans}"],
            check=_clock(h0, mm, next(t for t in range(1, 10 ** 4) if t % a_ == 0 and t % b_ == 0)),
        )
    sa, sb = rng.choice([("hot dogs", "buns"), ("hamburger patties", "buns"), ("cups", "lids"),
                         ("bolts", "nuts"), ("envelopes", "greeting cards"), ("juice boxes", "granola bars"),
                         ("paper plates", "napkins"), ("pens", "notepads")])
    pa, pb = (a_, b_) if rng.random() < 0.5 else (b_, a_)
    need(max(pa, pb) <= 20)
    na, nb = L // pa, L // pb
    ask_b = rng.random() < 0.5
    tgt, other = (sb, sa) if ask_b else (sa, sb)
    pt, po = (pb, pa) if ask_b else (pa, pb)
    nt, no = (nb, na) if ask_b else (na, nb)
    p = person(rng)
    hi_p = max(pa, pb)
    mults = [hi_p * i for i in range(1, L // hi_p + 1)]
    return Problem(
        stem=(f"{p.name} is buying {sa} and {sb}. {sa.capitalize()} come in packs of {m(pa)}, and "
              f"{sb} come in packs of {m(pb)}. {p.He} wants exactly the same number of {sa} and {sb}. "
              f"What is the least number of packs of {tgt} {p.he} can buy?"),
        answer=Q(nt),
        fmt=num,
        wrong=[(Q(no), f"is the number of packs of {other}"),
               (Q(L), f"is the number of {tgt}, not the number of packs"),
               (Q(po), f"buys one pack of {tgt} for each item in a pack of {other}; that works, but it is "
                       "not the least") if po != nt and (po * pt) % po == 0 and po != no else (Q(nt + 1), None),
               (Q(na + nb), "adds the packs of both items")],
        steps=[f"The number of each item must be a common multiple of {m(pa)} and {m(pb)}; the least "
               "one is the LCM.",
               f"Multiples of {m(hi_p)}: {_brk(mults)}. The first that is also a multiple of "
               f"{m(min(pa, pb))} is {m(L)}, so {p.he} needs {m(L)} of each.",
               f"Packs of {tgt}: {m(rf'{L} \div {pt} = {nt}')}."],
        check=Q(next(k for k in range(1, 100) if (k * pt) % po == 0)),
    )


@template("AR")
def gcf_word(rng, lvl):
    g = rng.choice([4, 6, 8, 9, 12, 14, 15, 16, 18])
    ka, kb = rng.sample(range(2, 9), 2)
    need(math.gcd(ka, kb) == 1)
    A, B = g * ka, g * kb
    cf = [d for d in _divs(g) if 1 < d < g]
    need(max(A, B) <= 120)
    L = math.lcm(A, B)
    kind = rng.choice(["kits", "kits", "teams", "boards"])
    if kind == "kits":
        ia, ib, kit = rng.choice([("bottles of water", "granola bars", "care package"),
                                  ("bandages", "antiseptic wipes", "first-aid kit"),
                                  ("pencils", "erasers", "school-supply bag"),
                                  ("protein bars", "energy drinks", "snack pack"),
                                  ("pairs of socks", "bars of soap", "comfort kit"),
                                  ("chemical light sticks", "batteries", "field kit"),
                                  ("stickers", "small toys", "party bag")])
        who = rng.choice(["A volunteer group", soldier(rng), "A youth club", person(rng).name,
                          "A church group", "The unit's family readiness group"])
        setup = (f"{who} has {m(A)} {ia} and {m(B)} {ib}. Every {kit} must be identical, "
                 f"with nothing left over.")
        q2 = f"What is the greatest number of {kit}s that can be made?"
        q3 = f"If the greatest possible number of {kit}s is made, how many {ia} go in each one?"
        unit_ = f"{kit}s"
    elif kind == "teams":
        setup = (f"A training class has {m(A)} soldiers from Alpha Company and {m(B)} from Bravo "
                 f"Company. The instructor wants to form teams so that every team has the same "
                 f"number of Alpha soldiers and the same number of Bravo soldiers, with no one left out.")
        q2 = "What is the greatest number of teams that can be formed?"
        q3 = "If the greatest possible number of teams is formed, how many Alpha soldiers are on each team?"
        ia, ib, unit_ = "Alpha soldiers", "Bravo soldiers", "teams"
    else:
        setup = (f"A carpenter has two boards, {m(A)} inches and {m(B)} inches long. She wants to "
                 f"cut both boards into pieces that are all the same length, with no wood left over.")
        q2 = "What is the longest each piece can be?"
        q3 = "If she cuts the longest possible pieces, how many pieces will she have in all?"
        ia, ib, unit_ = None, None, "inches"
    steps0, _ = _gcf_steps([A, B])
    if lvl == 2:
        fmt = unit(num, "inch", "inches") if kind == "boards" else num
        return Problem(
            stem=f"{setup} {q2}",
            answer=Q(g),
            fmt=fmt,
            wrong=[(Q(L), "is the least common multiple, not the greatest common factor"),
                   (Q(rng.choice(cf)), "is a common factor, but not the greatest one"),
                   (Q(A + B), "adds the two numbers"),
                   (Q(min(A, B)), f"does not divide {m(max(A, B))} evenly")],
            steps=[("The pieces must divide both lengths evenly, so look for the greatest common factor."
                    if kind == "boards" else
                    "Each item count must split evenly into the groups, so the number of groups must "
                    "divide both numbers. The greatest such number is the GCF.")] + steps0,
            check=Q(max(d for d in range(1, min(A, B) + 1) if A % d == 0 and B % d == 0)),
        )
    if kind == "boards":
        ans = Q(ka + kb)
        wrong = [(Q(g), "is the length of each piece, not the number of pieces"),
                 (Q(ka), "counts only the pieces from the first board"),
                 (Q(A + B), "adds the lengths of the boards"),
                 (Q((A + B) // cf[-1]), f"cuts pieces {m(cf[-1])} inches long, a common factor that "
                                        "is not the greatest")]
        last = [f"Pieces: {m(rf'{A} \div {g} = {ka}')} and {m(rf'{B} \div {g} = {kb}')}, so "
                f"{m(f'{ka} + {kb} = {ka + kb}')} pieces in all."]
    else:
        ans = Q(ka)
        wrong = [(Q(g), f"is the number of {unit_}, not the number of {ia} in each"),
                 (Q(kb), f"is the number of {ib} in each"),
                 (Q(A // cf[0]), f"splits into only {m(cf[0])} groups, a common factor that is not the greatest"),
                 (Q(ka + kb), "adds the counts of both items in each group")]
        last = [f"There are {m(g)} {unit_}, so each gets {m(rf'{A} \div {g} = {ka}')} {ia}."]
    return Problem(
        stem=f"{setup} {q3}",
        answer=ans,
        fmt=num,
        wrong=wrong,
        steps=[("First find the longest piece: the GCF of the two lengths."
                if kind == "boards" else f"First find the greatest number of {unit_}: the GCF.")]
        + steps0 + last,
        check=(Q(A // math.gcd(A, B) + B // math.gcd(A, B)) if kind == "boards"
               else Q(A // max(d for d in range(1, min(A, B) + 1) if A % d == 0 and B % d == 0))),
    )


PLAN = [
    # (template, level, count)  -- easy -> hard; 25 problems
    (which_prime, 1, 2),
    (vocab, 1, 2),
    (gcf, 1, 2),
    (lcm, 1, 2),
    (prime_factorization, 2, 2),
    (divisibility, 2, 2),
    (gcf, 2, 1),
    (lcm, 2, 1),
    (lcm_word, 2, 2),
    (gcf_word, 2, 2),
    (num_factors, 3, 2),
    (lcm_word, 3, 2),
    (gcf_word, 3, 2),
    (lcm, 3, 1),
]
