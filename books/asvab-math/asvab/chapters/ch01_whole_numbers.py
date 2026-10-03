"""Chapter 1 - Whole Numbers & Order of Operations."""
import sympy as sp

from ..core import (R, Q, Problem, need, num, dec, money, text, m, int_raw,
                    dec_raw, person, soldier, choose, template)

NUM = 1
TITLE = "Whole Numbers & Order of Operations"
PART = 1

INTRO = r"""
Every other chapter in this book rests on whole-number arithmetic. With no
calculator on the ASVAB, you need three things: a feel for place value, one
firm rule for the order of operations, and a habit of reading word problems
for what they \emph{really} ask.

\begin{concept}{Place value and rounding}
In $4{,}725{,}316$ the digits name, from the left: millions ($4$),
hundred-thousands ($7$), ten-thousands ($2$), thousands ($5$), hundreds ($3$),
tens ($1$), ones ($6$). The \emph{value} of the $7$ is $700{,}000$.

To round, look at the digit just to the \emph{right} of the rounding place:
$5$ or more $\to$ round up; $4$ or less $\to$ keep the digit. Then change
every digit after the rounding place to $0$.
$38{,}462 \to 38{,}000$ (nearest thousand) and $38{,}500$ (nearest hundred).
\end{concept}

\begin{concept}{Order of operations (PEMDAS)}
\begin{enumerate}
\item \textbf{P}arentheses (innermost first)
\item \textbf{E}xponents ($4^2 = 4 \times 4 = 16$)
\item \textbf{M}ultiplication and \textbf{D}ivision, a tie: work \emph{left to right}
\item \textbf{A}ddition and \textbf{S}ubtraction, a tie: work \emph{left to right}
\end{enumerate}
Example: $20 - 12 \div 4 \times 2 = 20 - 3 \times 2 = 20 - 6 = 14$.
\end{concept}

\begin{concept}{Properties that make mental math easy}
\begin{tabular}{@{}ll@{}}
Commutative (order) & $a + b = b + a$, \quad $a \times b = b \times a$\\
Associative (grouping) & $(a + b) + c = a + (b + c)$\\
Distributive & $a \times (b + c) = a \times b + a \times c$\\
Identity & $a + 0 = a$, \quad $a \times 1 = a$
\end{tabular}

\smallskip
The distributive property turns hard products into easy ones:
$7 \times 98 = 7 \times 100 - 7 \times 2 = 700 - 14 = 686$.
\end{concept}

\begin{example}{Worked example}
A convoy must move $250$ soldiers. Each truck carries $24$ soldiers. How many
trucks are needed?

\textbf{Solution.} $250 \div 24 = 10$ remainder $10$. Ten trucks carry
$240$ soldiers, and the other $10$ still need a ride, so you need
\textbf{11} trucks. When a question asks how many containers, vehicles, or
trips are \emph{needed}, round \emph{up}.
\end{example}

\begin{tip}
Estimate by rounding each number to its first digit, then count zeros:
$398 \times 51 \approx 400 \times 50$; $4 \times 5 = 20$, and the three
zeros give $20{,}000$. Estimating first also catches answers that are off by
a factor of $10$.
\end{tip}

\begin{trap}
\begin{itemize}
\item Adding before multiplying: $6 + 4 \times 3 = 18$, not $30$.
\item Multiplying before an earlier division: $24 \div 4 \times 2 = 12$, not $3$.
\item Rounding \emph{down} the number of buses, boxes, or trips needed.
\item Giving the remainder when the question asks for the quotient (or the reverse).
\end{itemize}
\end{trap}
"""

# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------

_PLACES = ["ones", "tens", "hundreds", "thousands", "ten-thousands",
           "hundred-thousands", "millions", "ten-millions", "hundred-millions"]
_ROUND_NAMES = {10: "ten", 100: "hundred", 1000: "thousand", 10000: "ten thousand"}


def _n(v):
    """Raw integer with thousands separators (for use inside math)."""
    return int_raw(v)


def _round_half_up(v, p):
    return (Q(v) / p + R(1, 2)).floor() * p


# --------------------------------------------------------------------------
# place value and rounding
# --------------------------------------------------------------------------

@template("MK")
def place_value(rng, lvl):
    ndig = rng.choice([5, 6] if lvl == 1 else [6, 7])
    digits = [rng.randint(1, 9)] + [rng.randint(0, 9) for _ in range(ndig - 1)]
    n_ = int("".join(map(str, digits)))
    variant = rng.choice(["value", "which"])
    if variant == "value":
        k = rng.randint(1, ndig - 1)                 # place index from the right
        d = digits[ndig - 1 - k]
        need(d >= 2 and digits.count(d) == 1)        # the digit names one spot
        ans = Q(d) * 10**k
        wrong = [
            (Q(d), "gives the digit itself, not its place value"),
            (ans / 10, f"is the value of a {m(d)} in the {_PLACES[k - 1]} place"),
            (ans * 10, f"is the value of a {m(d)} in the {_PLACES[k + 1]} place"),
            (ans / 100 if k >= 2 else ans * 100,
             f"is the value of a {m(d)} in the {_PLACES[k - 2] if k >= 2 else _PLACES[k + 2]} place"),
        ]
        names = ", ".join(_PLACES[:k + 1])
        return Problem(
            stem=choose(rng,
                        f"What is the value of the digit {m(d)} in the number {num(n_)}?",
                        f"In the number {num(n_)}, what is the value of the digit {m(d)}?"),
            answer=ans,
            fmt=num,
            wrong=wrong,
            steps=[
                f"Name the places from the right: {names}. The {m(d)} is in the "
                f"{_PLACES[k]} place.",
                f"Its value is {m(f'{d} \\times {_n(10**k)} = {_n(ans)}')}.",
            ],
            check=Q(n_ // 10**k % 10) * int("1" + "0" * k),
        )
    # which digit is in a named place
    k = rng.randint(2, ndig - 1)
    d = digits[ndig - 1 - k]
    wrong = []
    for j in (k - 1, k + 1, k - 2, k + 2):
        if 0 <= j < ndig:
            wrong.append((Q(digits[ndig - 1 - j]), f"is the digit in the {_PLACES[j]} place"))
    read = ", ".join(f"{m(digits[ndig - 1 - j])} ({_PLACES[j]})" for j in range(k + 1))
    return Problem(
        stem=f"Which digit is in the {_PLACES[k]} place in {num(n_)}?",
        answer=Q(d),
        fmt=num,
        wrong=wrong,
        steps=[
            f"Read the digits from the right, naming each place: {read}.",
            f"So the {_PLACES[k]} digit is {m(d)}.",
        ],
        check=Q(int(str(n_)[ndig - 1 - k])),
        near=lambda r: [Q(v) for v in r.sample(range(10), 10)],
    )


@template("MK")
def rounding(rng, lvl):
    if lvl == 1:
        p = rng.choice([10, 100])
        n_ = rng.randint(120, 9899)
    else:
        p = rng.choice([100, 1000, 1000])
        n_ = rng.randint(10_000, 989_999) if p == 1000 else rng.randint(1_200, 98_999)
    if lvl == 2 and rng.random() < 0.35:
        # force a carry: rounding digit 9, next digit 5 or more (e.g. 2,961 -> 3,000)
        n_ = n_ // (10 * p) * (10 * p) + 9 * p + rng.randint(5, 9) * (p // 10) + rng.randint(0, p // 10 - 1)
    dig = n_ // p % 10                 # digit in the rounding place
    nxt = n_ // (p // 10) % 10         # digit just to its right
    need(n_ % p != 0 and n_ // p > 0)
    carry = dig == 9 and nxt >= 5
    ans = _round_half_up(n_, p)
    up = nxt >= 5
    down_val, up_val = Q(n_ // p * p), Q(n_ // p * p + p)
    name, small, big = _ROUND_NAMES[p], _ROUND_NAMES.get(p // 10), _ROUND_NAMES.get(p * 10)
    wrong = []
    if up:
        wrong.append((down_val, f"rounds down even though the next digit, {m(nxt)}, is 5 or more"))
        if not carry:
            wrong.append((Q(n_ + p), f"raises the {name}s digit but forgets to change the digits after it to zeros"))
        else:
            wrong.append((Q(n_ // (10 * p) * (10 * p)),
                          f"changes the 9 to 0 but forgets to carry 1 into the {big}s place"))
    else:
        wrong.append((up_val, f"rounds up even though the next digit, {m(nxt)}, is less than 5"))
    if small:
        wrong.append((_round_half_up(n_, p // 10), f"rounds to the nearest {small} instead"))
    if big:
        wrong.append((_round_half_up(n_, p * 10), f"rounds to the nearest {big} instead"))
    place = {10: "tens", 100: "hundreds", 1000: "thousands"}[p]
    right = {10: "ones", 100: "tens", 1000: "hundreds"}[p]
    if up:
        how = (f"Because {m(nxt)} is 5 or more, round up: the {place} digit {m(dig)} becomes "
               + (f"$10$, so write 0 and carry 1 to the next place." if carry else f"{m(dig + 1)}."))
    else:
        how = f"Because {m(nxt)} is less than 5, keep the {place} digit {m(dig)} as it is."
    # independent check: string-based rounding
    s = str(n_)
    cut = len(s) - len(str(p)) + 1                    # index just after the rounding digit
    head = int(s[:cut])
    chk = (head + (1 if int(s[cut]) >= 5 else 0)) * p
    return Problem(
        stem=choose(rng,
                    f"Round {num(n_)} to the nearest {name}.",
                    f"What is {num(n_)} rounded to the nearest {name}?"),
        answer=ans,
        fmt=num,
        wrong=wrong,
        steps=[
            f"The {place} digit is {m(dig)}. Look at the digit just to its right "
            f"(the {right} digit): {m(nxt)}.",
            how,
            f"Change every digit after the {place} place to zero: {num(ans)}.",
        ],
        check=Q(chk),
    )


# --------------------------------------------------------------------------
# order of operations: a tiny evaluator that also produces the traps
# --------------------------------------------------------------------------

_TIERS = {
    "right": [{"^"}, {"*", "/"}, {"+", "-"}],
    "lr": [{"^"}, {"*", "/", "+", "-"}],
    "add_first": [{"^"}, {"+", "-"}, {"*", "/"}],
    "mul_first": [{"^"}, {"*"}, {"/"}, {"+", "-"}],
    "add_before_sub": [{"^"}, {"*", "/"}, {"+"}, {"-"}],
    "double": [{"^"}, {"*", "/"}, {"+", "-"}],
    "mul_before_exp": [{"*", "/"}, {"^"}, {"+", "-"}],
    "noparen": [{"^"}, {"*", "/"}, {"+", "-"}],
}

_TRAP_WHY = {
    "noparen": "ignores the parentheses",
    "add_first": "adds or subtracts before multiplying or dividing",
    "lr": "works straight from left to right instead of multiplying and dividing first",
    "mul_first": "multiplies before dividing; multiplication and division go left to right",
    "add_before_sub": "adds before subtracting; addition and subtraction go left to right",
    "mul_before_exp": "multiplies before applying the exponent",
    "double": "multiplies by the exponent instead of using it as a power",
}

_OPTEX = {"+": "+", "-": "-", "*": r"\times", "/": r"\div"}


def _apply(op, u, v):
    if op == "+":
        return u + v
    if op == "-":
        return u - v
    if op == "*":
        return u * v
    if op == "/":
        if v == 0:
            raise ZeroDivisionError
        return u / v
    return u ** v


def _pick(seg, rule):
    ops = [(i, s) for i, s in enumerate(seg) if isinstance(s, str)]
    if rule == "mul_before_exp":
        # only an operator whose left operand is a plain number (not an exponent)
        ops = [(i, s) for i, s in ops if not (s in "*/" and i >= 2 and seg[i - 2] == "^")]
    for tier in _TIERS[rule]:
        for i, s in ops:
            if s in tier:
                return i
    raise AssertionError("no operator")


def _tex(tokens):
    out = []
    for i, t in enumerate(tokens):
        if isinstance(t, str):
            if t == "^":
                continue
            out.append(_OPTEX.get(t, t))
        elif i > 0 and tokens[i - 1] == "^":
            out[-1] = out[-1] + "^{" + str(t) + "}"
        else:
            out.append(_n(t))
    s = " ".join(out)
    return s.replace("( ", "(").replace(" )", ")")


def _evaluate(tokens, rule="right", log=None):
    t = list(tokens)
    if rule == "noparen":
        t = [k for k in t if k not in ("(", ")")]
    while len(t) > 1:
        if ")" in t:
            j = t.index(")")
            i = max(k for k in range(j) if t[k] == "(")
            if j - i == 2:
                t = t[:i] + [t[i + 1]] + t[j + 1:]
                continue
            lo, hi, inside = i + 1, j, True
        else:
            lo, hi, inside = 0, len(t), False
        seg = t[lo:hi]
        k = _pick(seg, rule)
        u, op, v = seg[k - 1], seg[k], seg[k + 1]
        if rule == "double" and op == "^":
            r = u * v
        else:
            r = _apply(op, u, v)
        new = t[:lo + k - 1] + [r] + t[lo + k + 2:]
        if log is not None:
            log.append(dict(inside=inside, op=op, u=u, v=v, r=r, seg=seg, after=new))
        t = new
    # strip leftover parentheses around the final number
    t = [k for k in t if k not in ("(", ")")]
    return t[0]


def _clean(tokens):
    """Drop parentheses around a single number unless an exponent follows."""
    t = list(tokens)
    i = 0
    while i + 2 < len(t):
        if t[i] == "(" and not isinstance(t[i + 1], str) and t[i + 2] == ")" \
                and not (i + 3 < len(t) and t[i + 3] == "^"):
            t = t[:i] + [t[i + 1]] + t[i + 3:]
        else:
            i += 1
    return t


def _py(tokens):
    out = []
    for t in tokens:
        out.append({"^": "**", "*": "*", "/": "/"}.get(t, str(t)) if isinstance(t, str) else str(t))
    return " ".join(out)


def _steps(tokens):
    log = []
    val = _evaluate(tokens, "right", log)
    steps = []
    seen_paren = False
    for e in log:
        op, u, v, r, seg = e["op"], e["u"], e["v"], e["r"], e["seg"]
        segops = {s for s in seg if isinstance(s, str)}
        if op == "^":
            work = f"{_n(u)}^{{{v}}} = " + r" \times ".join([_n(u)] * int(v)) + f" = {_n(r)}"
        else:
            work = f"{_n(u)} {_OPTEX[op]} {_n(v)} = {_n(r)}"
        if e["inside"]:
            lead = "Still inside the parentheses" if seen_paren else "Parentheses first"
            seen_paren = True
            if op in "*/" and segops & {"+", "-"}:
                lead += (", multiply" if op == "*" else ", divide") + " before adding or subtracting"
        elif op == "^":
            lead = "Exponent next"
        elif op in "*/":
            word = "Multiply" if op == "*" else "Divide"
            if {"*", "/"} <= segops:
                lead = f"{word} (multiplication and division go left to right)"
            elif segops & {"+", "-"}:
                lead = f"{word} before you add or subtract"
            else:
                lead = word
        else:
            word = "Add" if op == "+" else "Subtract"
            lead = (f"{word} (addition and subtraction go left to right)"
                    if {"+", "-"} <= segops else word)
        after = [k for k in e["after"]]
        if len([k for k in after if not isinstance(k, str) or k not in "()"]) > 1:
            steps.append(f"{lead}: {m(work)}, which leaves {m(_tex(_clean(after)))}.")
        else:
            steps.append(f"{lead}: {m(work)}.")
    return val, log, steps


def _parse(form, vals):
    toks = []
    for w in form.split():
        if w in vals:
            toks.append(Q(vals[w]))
        elif w.isdigit():
            toks.append(Q(int(w)))
        else:
            toks.append(w)
    return toks


def _divs(k, lo=2, hi=9):
    return [d for d in range(lo, hi + 1) if k % d == 0]


# form, letter specs (range or function of the values drawn so far)
_FORMS = {
    1: [
        ("a + b * c", dict(a=(2, 30), b=(2, 9), c=(3, 9))),
        ("a - b * c", dict(b=(2, 6), c=(2, 7), a=lambda v, r: v["b"] * v["c"] + r.randint(3, 30))),
        ("a * b + c * d", dict(a=(2, 9), b=(2, 9), c=(2, 9), d=(2, 9))),
        ("a + d / c", dict(a=(3, 25), c=(2, 9), d=lambda v, r: v["c"] * r.randint(2, 9))),
        ("( a + b ) * c", dict(a=(2, 15), b=(2, 15), c=(2, 6))),
        ("a * ( b - c )", dict(a=(2, 9), c=(2, 12), b=lambda v, r: v["c"] + r.randint(2, 9))),
    ],
    2: [
        ("a / b * c", dict(b=(2, 6), c=(2, 6), a=lambda v, r: v["b"] * v["c"] * r.randint(1, 4))),
        ("a - b + c", dict(b=(6, 19), c=(2, 9), a=lambda v, r: v["b"] + v["c"] + r.randint(2, 20))),
        ("a * b ^ 2", dict(a=(2, 5), b=(2, 6))),
        ("a + b ^ 2 * c", dict(a=(2, 12), b=(2, 5), c=(2, 4))),
        ("a - b * ( c - d )", dict(b=(2, 6), d=(2, 9), c=lambda v, r: v["d"] + r.randint(2, 6),
                                 a=lambda v, r: v["b"] * (v["c"] - v["d"]) + r.randint(4, 30))),
        ("( a + b ) * c - d", dict(a=(2, 9), b=(2, 9), c=(2, 6), d=(2, 15))),
        ("a + b * c - d / e", dict(a=(2, 20), b=(2, 9), c=(2, 9), e=(2, 6),
                                   d=lambda v, r: v["e"] * r.randint(2, 6))),
        ("a / ( b + c ) * d", dict(b=(1, 5), c=(1, 5), d=(2, 6),
                                   a=lambda v, r: (v["b"] + v["c"]) * r.randint(2, 9))),
    ],
    3: [
        ("a - b ^ 2 / c * d", dict(b=(2, 8), c=lambda v, r: r.choice(_divs(v["b"] ** 2)), d=(2, 5),
                                   a=lambda v, r: v["b"] ** 2 // v["c"] * v["d"] + r.randint(2, 40))),
        ("( a + b ) ^ 2 / c - d * e", dict(a=(1, 6), b=(1, 6),
                                           c=lambda v, r: r.choice(_divs((v["a"] + v["b"]) ** 2)),
                                           d=(2, 5), e=(2, 5))),
        ("a * ( b + c ) ^ 2 / d", dict(a=(2, 6), b=(1, 4), c=(1, 4),
                                       d=lambda v, r: r.choice(_divs(v["a"] * (v["b"] + v["c"]) ** 2)))),
        ("a - b * ( c + d ) / e + f", dict(b=(2, 6), c=(1, 9), d=(1, 9),
                                           e=lambda v, r: r.choice(_divs(v["b"] * (v["c"] + v["d"]))),
                                           a=lambda v, r: v["b"] * (v["c"] + v["d"]) // v["e"] + r.randint(2, 30),
                                           f=(2, 12))),
        ("a + b * ( c - d ) ^ 2 - e", dict(a=(2, 20), b=(2, 4), d=(1, 6),
                                           c=lambda v, r: v["d"] + r.randint(2, 4), e=(2, 15))),
        ("( a - b ) * c + d ^ 2 / e", dict(b=(2, 9), a=lambda v, r: v["b"] + r.randint(2, 7), c=(2, 6),
                                           d=(2, 9), e=lambda v, r: r.choice(_divs(v["d"] ** 2)))),
        ("a ^ 2 - b * ( c + d ) / e", dict(a=(5, 12), b=(2, 5), c=(1, 6), d=(1, 6),
                                           e=lambda v, r: r.choice(_divs(v["b"] * (v["c"] + v["d"]))))),
    ],
}


@template("MK")
def order_ops(rng, lvl):
    form, spec = rng.choice(_FORMS[lvl])
    vals = {}
    for k, s in spec.items():
        if callable(s):
            try:
                vals[k] = s(vals, rng)
            except IndexError:
                need(False)
        else:
            vals[k] = rng.randint(*s)
    toks = _parse(form, vals)
    ans, log, steps = _steps(toks)
    for e in log:                                      # every step: whole, >= 0, small
        need(e["r"].is_integer and 0 <= e["r"] <= 400)
    need(0 <= ans <= 300)
    wrong = []
    for rule in ("noparen", "add_first", "lr", "mul_first", "add_before_sub", "mul_before_exp", "double"):
        try:
            w = _evaluate(toks, rule)
        except ZeroDivisionError:
            continue
        if rule == "double":
            exps = {toks[i + 1] for i, t in enumerate(toks) if t == "^"}
            why = ("doubles instead of squaring" if exps == {2}
                   else _TRAP_WHY["double"])
        else:
            why = _TRAP_WHY[rule]
        wrong.append((w, why))
    need(sum(1 for w, _ in wrong if w != ans and Q(w).is_integer and w >= 0) >= 1)
    return Problem(
        stem=choose(rng, f"What is the value of {m(_tex(toks))}?",
                    f"Evaluate: {m(_tex(toks))}",
                    f"Simplify: {m(_tex(toks))}"),
        answer=ans,
        fmt=num,
        wrong=wrong,
        steps=steps,
        check=sp.sympify(_py(toks)),
    )


# --------------------------------------------------------------------------
# properties
# --------------------------------------------------------------------------

_PROPS = ["Commutative property", "Associative property", "Distributive property", "Identity property"]
_PROP_WHY = {
    "Commutative property": "is about changing the order of numbers, which does not happen here",
    "Associative property": "is about moving parentheses among numbers that are all added or all "
                            "multiplied, which does not happen here",
    "Distributive property": "is about multiplying a number by each part of a sum or difference, "
                             "which does not happen here",
    "Identity property": "is about adding 0 or multiplying by 1, which does not happen here",
}


def _prop_example(rng, kind):
    a, b, c = rng.sample(range(2, 13), 3)
    if kind == "comm_add":
        return "Commutative property", f"{a} + {b} = {b} + {a}"
    if kind == "comm_mul":
        return "Commutative property", rf"{a} \times {b} = {b} \times {a}"
    if kind == "assoc_add":
        return "Associative property", f"({a} + {b}) + {c} = {a} + ({b} + {c})"
    if kind == "assoc_mul":
        return "Associative property", rf"({a} \times {b}) \times {c} = {a} \times ({b} \times {c})"
    if kind == "dist_add":
        return "Distributive property", rf"{a} \times ({b} + {c}) = {a} \times {b} + {a} \times {c}"
    if kind == "dist_sub":
        b, c = max(b, c), min(b, c)
        return "Distributive property", rf"{a} \times ({b} - {c}) = {a} \times {b} - {a} \times {c}"
    if kind == "id_add":
        return "Identity property", f"{a + 10 * b} + 0 = {a + 10 * b}"
    return "Identity property", rf"{a + 10 * b} \times 1 = {a + 10 * b}"


_PROP_SHOWS = {
    "Commutative property": "shows the commutative property: only the order changes",
    "Associative property": "shows the associative property: only the grouping changes",
    "Distributive property": "shows the distributive property",
    "Identity property": "shows the identity property: adding 0 or multiplying by 1 changes nothing",
}

_PROP_EXPLAIN = {
    "Commutative property": "The same numbers appear on both sides; only their \\emph{order} "
                            "changes. Changing the order is the commutative property.",
    "Associative property": "The numbers stay in the same order; only the parentheses move. "
                            "Changing the \\emph{grouping} is the associative property.",
    "Distributive property": "The number outside the parentheses multiplies \\emph{each} number "
                             "inside. That is the distributive property.",
    "Identity property": "Adding 0 or multiplying by 1 leaves the number unchanged. That is the "
                         "identity property.",
}


def _classify(eq):
    """Independent check: name the property from the shape of the equation."""
    left, right = eq.split("=")
    if right.strip() in left and ("+ 0" in left or r"\times 1 " in left + " "):
        return "Identity property"
    if left.count("(") == 1 and right.count("(") == 1:
        return "Associative property"
    if "(" in left:
        return "Distributive property"
    return "Commutative property"


@template("MK")
def property_name(rng, lvl):
    kinds = ["comm_add", "comm_mul", "assoc_add", "assoc_mul", "dist_add", "dist_sub", "id_add", "id_mul"]
    if rng.random() < 0.6:
        kind = rng.choice(kinds)
        ans, eq = _prop_example(rng, kind)
        return Problem(
            stem=choose(rng, f"Which property is shown by the equation {m(eq)}?",
                        f"The equation {m(eq)} is an example of which property?"),
            answer=ans,
            fmt=text,
            wrong=[(p, _PROP_WHY[p]) for p in _PROPS if p != ans],
            steps=[
                "Compare the two sides of the equation and ask what changed.",
                _PROP_EXPLAIN[ans],
            ],
            check=_classify(eq),
        )
    # pick the equation that shows a named property
    target = rng.choice(["comm", "assoc", "dist"])
    pool = {"comm": ["comm_add", "comm_mul"], "assoc": ["assoc_add", "assoc_mul"],
            "dist": ["dist_add", "dist_sub"], "id": ["id_add", "id_mul"]}
    name, eq = _prop_example(rng, rng.choice(pool[target]))
    others = []
    for g in ("comm", "assoc", "dist", "id"):
        if g != target:
            nm, e2 = _prop_example(rng, rng.choice(pool[g]))
            others.append((m(e2), _PROP_SHOWS[nm]))
    return Problem(
        stem=f"Which equation shows the {name[0].lower() + name[1:]}?",
        answer=m(eq),
        fmt=text,
        wrong=others,
        steps=[
            {"comm": "The commutative property says you may change the \\emph{order}: "
                     "$a + b = b + a$ and $a \\times b = b \\times a$.",
             "assoc": "The associative property says you may change the \\emph{grouping} "
                      "(where the parentheses go) without changing the order.",
             "dist": "The distributive property says a number times a sum (or difference) "
                     "equals the sum (or difference) of the separate products: "
                     "$a \\times (b + c) = a \\times b + a \\times c$."}[target],
            f"Only {m(eq)} fits that pattern.",
        ],
        verify=lambda v: _classify(v.strip("$")) == name,
    )


@template("MK")
def distributive(rng, lvl):
    k = rng.randint(3, 9)
    if lvl == 1:
        tens = rng.choice(range(20, 100, 10))
        ones = rng.randint(2, 9)
        sign = rng.choice(["+", "-"])
        whole = tens + ones if sign == "+" else tens - ones
        ans = rf"${k} \times {tens} {sign} {k} \times {ones}$"
        wrong = [
            (rf"${k} \times {tens} {sign} {ones}$", f"multiplies only the {m(tens)} by {m(k)}, not the {m(ones)}"),
            (rf"${k} \times {tens} \times {k} \times {ones}$", "multiplies everything together"),
        ]
        if sign == "+":
            wrong.append((rf"${k} + {tens} + {k} + {ones}$", "adds the outside number instead of multiplying by it"))
        else:
            wrong.append((rf"${k} \times {tens} + {k} \times {ones}$", "changes the subtraction to addition"))
        # no distractor may equal the original product
        vals = [sp.sympify(w.strip("$").replace(r"\times", "*")) for w, _ in wrong]
        need(all(v != k * whole for v in vals))
        expr_ = f"{k} \\times ({tens} {sign} {ones})"
        return Problem(
            stem=choose(rng,
                        f"Which expression is equal to {m(expr_)}?",
                        f"By the distributive property, {m(expr_)} is equal to which expression?"),
            answer=ans,
            fmt=text,
            wrong=wrong,
            steps=[
                f"The distributive property says the {m(k)} outside the parentheses multiplies "
                f"\\emph{{each}} number inside.",
                f"So {m(expr_ + f' = {k} \\times {tens} {sign} {k} \\times {ones}')}.",
                f"Check: both sides equal {m(_n(k * whole))}.",
            ],
            verify=lambda v: sp.sympify(v.strip("$").replace(r"\times", "*")) == k * whole,
        )
    base = rng.choice([100, 100, 50, 200, 1000])
    d = rng.randint(1, 4) if base != 1000 else rng.randint(1, 3)
    plus = rng.random() < 0.4
    other = base + d if plus else base - d
    ans = Q(k) * other
    s, verb = ("+", "add") if plus else ("-", "subtract")
    return Problem(
        stem=choose(rng, f"What is {m(rf'{k} \times {_n(other)}')}?",
                    f"Find the product: {m(rf'{k} \times {_n(other)}')}"),
        answer=ans,
        fmt=num,
        wrong=[
            (Q(k) * base + (d if plus else -d), f"{verb}s {m(d)} instead of {m(rf'{k} \times {d}')}"),
            (Q(k) * base - (k * d if plus else -k * d), f"{'subtracts' if plus else 'adds'} {m(rf'{k} \times {d}')} instead of {verb}ing it"),
            (Q(k) * base, f"rounds {m(_n(other))} to {m(_n(base))} and stops"),
        ],
        steps=[
            f"Write {m(_n(other))} as {m(f'{_n(base)} {s} {d}')}, an easy number {'plus' if plus else 'minus'} a little.",
            f"Distribute the {m(k)}: {m(rf'{k} \times {_n(base)} {s} {k} \times {d} = {_n(k * base)} {s} {k * d}')}.",
            f"{'Add' if plus else 'Subtract'}: {m(f'{_n(k * base)} {s} {k * d} = {_n(ans)}')}.",
        ],
        check=Q(k) * base + (k * d if plus else -k * d),
    )


# --------------------------------------------------------------------------
# estimation and hand computation
# --------------------------------------------------------------------------

@template("MK")
def estimate(rng, lvl):
    if rng.random() < 0.6:
        X = rng.choice(range(200, 1000, 100))
        Y = rng.choice(range(20, 100, 10))
        a_ = X - rng.randint(1, 4)
        b_ = Y + rng.choice([-2, -1, 1, 2, 3])
        exact = Q(a_) * b_
        est = Q(X) * Y
        wrong = [
            (est / 10, "drops a zero"),
            (est * 10, "adds an extra zero"),
            (Q(X - 100) * Y, f"rounds {m(a_)} down to {m(X - 100)} instead of up to {m(X)}"),
            (Q(X + Y), "adds the rounded numbers instead of multiplying them"),
        ]
        stem = choose(rng,
                      f"Which of the following is the closest estimate of {m(rf'{a_} \times {b_}')}?",
                      f"Without a calculator, which value is closest to {m(rf'{a_} \times {b_}')}?")
        lead = X // 100 * (Y // 10)
        steps = [
            f"Round each number to its first digit: {m(a_)} is about {m(X)}, and {m(b_)} is about {m(Y)}.",
            f"Multiply the leading digits: {m(rf'{X // 100} \times {Y // 10} = {lead}')}.",
            f"Attach the three zeros (two from {m(X)}, one from {m(Y)}): {m(_n(est))}.",
        ]
        tip = None
    else:
        Y = rng.choice(range(20, 100, 10))
        q = rng.choice(range(20, 100, 10))
        D0 = Y * q
        a_ = D0 + rng.choice([-1, 1]) * rng.randint(3, 40)
        b_ = Y + rng.choice([-1, 1])
        exact = R(a_, b_)
        est = Q(q)
        wrong = [
            (est / 10, "drops a zero"),
            (est * 10, "adds an extra zero"),
            (est - 10, None),
            (est + 10, None),
        ]
        stem = choose(rng,
                      f"Which of the following is the closest estimate of {m(rf'{_n(a_)} \div {b_}')}?",
                      f"Without a calculator, which value is closest to {m(rf'{_n(a_)} \div {b_}')}?")
        steps = [
            f"Round to compatible numbers: {m(_n(a_))} is about {m(_n(D0))}, and {m(b_)} is about {m(Y)}.",
            f"Divide: {m(rf'{_n(D0)} \div {Y} = {_n(q)}')} (think {m(rf'{Y} \times {q} = {_n(D0)}')}).",
        ]
        tip = None
    cands = [est] + [w for w, _ in wrong]

    def closest(v):
        dist = abs(Q(v) - exact)
        return all(dist < abs(Q(w) - exact) for w in cands if w != v)
    return Problem(stem=stem, answer=est, fmt=num, wrong=wrong, steps=steps, tip=tip,
                   verify=closest, near=lambda r: [])


def _no_carry(a_, k):
    """Student bug: writes only the ones digit of each partial product (no carrying)."""
    ds = [int(c) for c in str(a_)]
    out = str(ds[0] * k)
    for d in ds[1:]:
        out += str(d * k % 10)
    return int(out)


def _carry_first(a_, k):
    """Student bug: adds the carry to the digit before multiplying."""
    ds = [int(c) for c in str(a_)][::-1]
    carry, out = 0, []
    for i, d in enumerate(ds):
        p = (d + carry) * k
        if i == len(ds) - 1:
            out.append(str(p))
        else:
            out.append(str(p % 10))
            carry = p // 10
    return int("".join(reversed(out)))


@template("MK")
def multiply_by_hand(rng, lvl):
    if lvl == 1:
        k = rng.randint(4, 9)
        a_ = rng.randint(124, 989)
        h, t, o = a_ // 100, a_ // 10 % 10, a_ % 10
        need(t != 0 and o != 0 and o * k >= 10 and t * k >= 10)
        ans = Q(a_) * k
        return Problem(
            stem=choose(rng, f"What is {m(rf'{a_} \times {k}')}?", f"Multiply: {m(rf'{a_} \times {k}')}"),
            answer=ans,
            fmt=num,
            wrong=[
                (Q(_no_carry(a_, k)), "forgets to add the carried digits"),
                (Q(_carry_first(a_, k)), "adds each carried digit before multiplying instead of after"),
                (ans + 100, None), (ans - 10, None),
            ],
            steps=[
                f"Break {m(a_)} into place values: {m(f'{h * 100} + {t * 10} + {o}')}.",
                f"Multiply each part by {m(k)}: {m(rf'{h * 100} \times {k} = {_n(h * 100 * k)}')}, "
                f"{m(rf'{t * 10} \times {k} = {_n(t * 10 * k)}')}, {m(rf'{o} \times {k} = {o * k}')}.",
                f"Add the parts: {m(f'{_n(h * 100 * k)} + {_n(t * 10 * k)} + {o * k} = {_n(ans)}')}.",
            ],
            check=sum(Q(int(c)) * 10**i * k for i, c in enumerate(reversed(str(a_)))),
        )
    a_ = rng.randint(23, 98)
    b_ = rng.randint(23, 98)
    bt, bo = b_ // 10, b_ % 10
    at, ao = a_ // 10, a_ % 10
    need(bo >= 2 and ao >= 2 and a_ != b_)
    ans = Q(a_) * b_
    return Problem(
        stem=choose(rng, f"What is {m(rf'{a_} \times {b_}')}?", f"Multiply: {m(rf'{a_} \times {b_}')}"),
        answer=ans,
        fmt=num,
        wrong=[
            (Q(a_ * bo + a_ * bt), f"forgets the placeholder zero, multiplying by {m(bt)} instead of {m(bt * 10)}"),
            (Q(at * 10 * bt * 10 + ao * bo), "multiplies only tens by tens and ones by ones"),
            (ans + 100, None), (ans - 100, None),
        ],
        steps=[
            f"Split {m(b_)} into {m(f'{bt * 10} + {bo}')} and multiply {m(a_)} by each part.",
            f"{m(rf'{a_} \times {bo} = {_n(a_ * bo)}')} and {m(rf'{a_} \times {bt * 10} = {_n(a_ * bt * 10)}')}.",
            f"Add the partial products: {m(f'{_n(a_ * bo)} + {_n(a_ * bt * 10)} = {_n(ans)}')}.",
        ],
        check=Q((at * 10 + ao) * bt * 10 + (at * 10 + ao) * bo),
    )


@template("MK")
def divide_by_hand(rng, lvl):
    k = rng.randint(3, 9)
    q = rng.randint(101, 909)
    qs = str(q)
    need("0" in qs[1:] and qs[0] != "0" and qs.count("0") == 1)
    D = k * q
    need(D < 10000)
    # long-division narrative, digit by digit
    ds = str(D)
    steps_txt = []
    rem, started, i = 0, False, 0
    parts = []
    for c in ds:
        cur = rem * 10 + int(c)
        if not started and cur < k:
            rem = cur
            continue
        started = True
        qd = cur // k
        parts.append((cur, qd, cur - qd * k))
        rem = cur - qd * k
    need("".join(str(p[1]) for p in parts) == qs)
    lines = []
    for cur, qd, r in parts:
        if qd == 0:
            lines.append(f"{m(k)} does not go into {m(cur)}, so write {m(0)} in the quotient")
        else:
            lines.append(f"{m(rf'{cur} \div {k} = {qd}')}" + (f" with {m(r)} left over" if r else ""))
    zero_drop = int(qs.replace("0", ""))
    i0 = qs.index("0")
    moved = qs[:i0] + qs[i0 + 1:] + "0" if i0 < len(qs) - 1 else None
    wrong = [(Q(zero_drop), "skips the zero in the quotient")]
    if moved and int(moved) != q:
        wrong.append((Q(int(moved)), "puts the zero in the wrong place"))
    wrong += [(Q(q) * 10, "adds an extra zero"), (Q(q + 10), None)]
    return Problem(
        stem=choose(rng, f"What is {m(rf'{_n(D)} \div {k}')}?", f"Divide: {m(rf'{_n(D)} \div {k}')}"),
        answer=Q(q),
        fmt=num,
        wrong=wrong,
        steps=[
            "Divide from left to right, bringing down one digit at a time.",
            "; then ".join(lines[:2]) + ".",
        ] + (["Then " + "; then ".join(lines[2:]) + "."] if lines[2:] else []) + [
            f"The quotient is {m(q)}. Check: {m(rf'{k} \times {q} = {_n(D)}')}.",
        ],
        check=Q(D) / k,
        verify=lambda v: Q(v) * k == D,
    )


# --------------------------------------------------------------------------
# word problems
# --------------------------------------------------------------------------

# (item plural, singular, price range) by context
_SHOP = {
    "school": [("notebooks", "notebook", 2, 6), ("binders", "binder", 4, 9),
               ("packs of pens", "pack of pens", 3, 8), ("backpacks", "backpack", 25, 45)],
    "clothes": [("T-shirts", "T-shirt", 8, 18), ("pairs of jeans", "pair of jeans", 25, 45),
                ("packs of socks", "pack of socks", 6, 12), ("hats", "hat", 12, 25)],
    "hardware": [("gallons of paint", "gallon of paint", 25, 45), ("paint brushes", "paint brush", 6, 14),
                 ("boxes of screws", "box of screws", 4, 9), ("rolls of tape", "roll of tape", 3, 7)],
    "supply": [("cots", "cot", 40, 70), ("sleeping bags", "sleeping bag", 35, 80),
               ("flashlights", "flashlight", 12, 30), ("canteens", "canteen", 8, 15)],
    "pt": [("pairs of running shoes", "pair of running shoes", 60, 110), ("PT shirts", "PT shirt", 10, 18),
           ("reflective belts", "reflective belt", 5, 9), ("water bottles", "water bottle", 6, 14)],
    "party": [("pizzas", "pizza", 9, 16), ("cases of soda", "case of soda", 5, 9),
              ("bags of ice", "bag of ice", 2, 4), ("veggie trays", "veggie tray", 15, 30)],
}


def _buyer(rng, ctx):
    if ctx in ("supply", "pt", "party") and rng.random() < 0.7:
        s = soldier(rng)
        return s, "he or she", "the order"
    p = person(rng)
    return p.name, p.he, None


@template("AR")
def shopping_total(rng, lvl):
    ctx = rng.choice(list(_SHOP))
    items = rng.sample(_SHOP[ctx], 2 if lvl < 3 else 3)
    qs = [rng.randint(2, 6 if lvl == 1 else 12) for _ in items]
    ps = [rng.randint(lo, hi) for _, _, lo, hi in items]
    lines = [q * p for q, p in zip(qs, ps)]
    total = sum(lines)
    s = soldier(rng) if ctx in ("supply", "pt", "party") and rng.random() < 0.6 else None
    who = s if s else person(rng).name
    buy = ", ".join(f"{m(q)} {it[0]} at {money(p)} each" for q, it, p in zip(qs[:-1], items[:-1], ps[:-1]))
    buy += f"{',' if len(items) > 2 else ''} and {m(qs[-1])} {items[-1][0]} at {money(ps[-1])} each"
    parts = r" + ".join(rf"{q} \times {p}" for q, p in zip(qs, ps))
    line_txt = ", ".join(m(rf"{q} \times {p} = {_n(q * p)}") for q, p in zip(qs, ps))
    add_txt = " + ".join(_n(v) for v in lines)
    if lvl == 1:
        return Problem(
            stem=f"{who} buys {buy}. How much does {'the order' if s else 'that'} cost in all?",
            answer=Q(total),
            fmt=money,
            wrong=[
                (Q(sum(ps)), "adds one of each price and ignores the quantities"),
                (Q(sum(qs) * sum(ps)), "multiplies the total number of items by the sum of the prices"),
                (Q(lines[0] + ps[1]), f"forgets to multiply the second price by {m(qs[1])}"),
                (Q(total + 10), None),
            ],
            steps=[
                f"Find the cost of each kind of item: {line_txt}.",
                f"Add: {m(f'{add_txt} = {_n(total)}')} dollars.",
            ],
            check=sum(Q(p) for q, p in zip(qs, ps) for _ in range(q)),
        )
    if lvl == 2:
        bill = next(b for b in (20, 50, 100, 200, 300, 500) if b > total)
        need(bill - total >= 3)
        change = bill - total
        pay = choose(rng, f"pays with {'a' if bill < 200 else 'two' if bill == 200 else 'several'} "
                          f"{money(bill if bill < 200 else 100)} bill{'s' if bill >= 200 else ''}",
                     f"hands the cashier {money(bill)}")
        return Problem(
            stem=(f"{who} buys {buy} and {pay}. How much change should "
                  f"{'come back' if s else 'be given back'}?"),
            answer=Q(change),
            fmt=money,
            wrong=[
                (Q(total), "is the total cost, not the change"),
                (Q(bill - sum(ps)), "subtracts one of each price and ignores the quantities"),
                (Q(bill - lines[0] - ps[1]), f"forgets to multiply the second price by {m(qs[1])}"),
                (Q(change + 10), None),
            ],
            steps=[
                f"Find the cost of each kind of item: {line_txt}.",
                f"Total cost: {m(f'{add_txt} = {_n(total)}')} dollars.",
                f"Change: {m(f'{_n(bill)} - {_n(total)} = {_n(change)}')} dollars.",
            ],
            check=bill - sum(Q(p) for q, p in zip(qs, ps) for _ in range(q)),
        )
    # level 3: down payment, rest split into equal monthly payments
    big = rng.choice([("a sofa", 600, 1400, "matching chairs", 120, 260),
                      ("a laptop", 600, 1500, "software packages", 40, 120),
                      ("a used motorcycle", 2400, 4800, "helmets", 90, 250),
                      ("a refrigerator", 800, 1800, "service plans", 60, 150)])
    name1, lo1, hi1, name2, lo2, hi2 = big
    p1 = rng.choice(range(lo1, hi1 + 1, 10))
    q2 = rng.randint(2, 3)
    p2 = rng.choice(range(lo2, hi2 + 1, 5))
    down = rng.choice(range(100, 700, 50))
    months = rng.choice([4, 5, 6, 8, 10, 12])
    tot = p1 + q2 * p2
    rest = tot - down
    need(rest > 0 and rest % months == 0)
    pay = Q(rest) / months
    p = person(rng)
    return Problem(
        stem=(f"{p.name} buys {name1} for {money(p1)} and {m(q2)} {name2} for {money(p2)} each. "
              f"{p.He} pays {money(down)} up front and splits the rest into {m(months)} equal "
              f"monthly payments. How much is each monthly payment?"),
        answer=pay,
        fmt=money,
        wrong=[
            (Q(tot) / months, "forgets to subtract the up-front payment"),
            (Q(p1 + p2 - down) / months, f"counts only one of the {name2}"),
            (Q(rest), "is the amount left to pay, not each monthly payment"),
            (Q(tot + down) / months, "adds the up-front payment instead of subtracting it"),
        ],
        steps=[
            f"Total cost: {m(rf'{_n(p1)} + {q2} \times {p2} = {_n(p1)} + {_n(q2 * p2)} = {_n(tot)}')} dollars.",
            f"Subtract the up-front payment: {m(f'{_n(tot)} - {down} = {_n(rest)}')} dollars.",
            f"Split into {m(months)} equal payments: {m(rf'{_n(rest)} \div {months} = {_n(pay)}')} dollars.",
        ],
        check=sp.Rational(p1 + sum([p2] * q2) - down, months),
        verify=lambda v: Q(v) * months + down == tot,
    )


@template("AR")
def equal_share(rng, lvl):
    if lvl == 1:
        k = rng.randint(3, 12)
        each = rng.randint(12, 95)
        total = k * each
        ctx = rng.choice([
            (f"A group of {m(k)} friends splits a restaurant bill of {money(total)} equally. "
             "How much does each friend pay?", money),
            (f"{soldier(rng)} divides {num(total)} rounds of ammunition equally among {m(k)} "
             "soldiers. How many rounds does each soldier get?", num),
            (f"A farmer packs {num(total)} eggs equally into {m(k)} crates. How many eggs go "
             "in each crate?", num),
            (f"{person(rng).name} wants to pay off a {money(total)} phone in {m(k)} equal monthly "
             "payments. How much is each payment?", money),
            (f"A supply clerk splits {num(total)} bottles of water equally among {m(k)} "
             "squads. How many bottles does each squad get?", num),
        ])
        return Problem(
            stem=ctx[0],
            answer=Q(each),
            fmt=ctx[1],
            wrong=[
                (Q(total - k), "subtracts instead of dividing"),
                (Q(each) * 10, "puts an extra zero in the quotient"),
                (Q(total + k), "adds instead of dividing"),
                (Q(each + 1), None), (Q(each - 2), None),
            ],
            steps=[
                "Sharing equally means dividing the total by the number of shares.",
                f"{m(rf'{_n(total)} \div {k} = {each}')}. Check: {m(rf'{k} \times {each} = {_n(total)}')}.",
            ],
            check=sp.Rational(total, k),
        )
    if lvl == 2:
        kind = rng.choice(["cabin", "trucks", "rent"])
        if kind == "cabin":
            nightly = rng.choice(range(120, 400, 10))
            nights = rng.randint(2, 5)
            k = rng.randint(3, 8)
            tot = nightly * nights
            need(tot % k == 0)
            each = Q(tot) / k
            stem = (f"{m(k)} friends rent a cabin for {m(nights)} nights at {money(nightly)} per night. "
                    "They split the total cost equally. How much does each friend pay?")
            wrong = [(Q(nightly) / k, "forgets to multiply by the number of nights"),
                     (Q(tot), "is the total cost, not each friend's share"),
                     (Q(tot) / (k - 1), "divides by one person too few")]
            steps = [f"Total cost: {m(rf'{nights} \times {nightly} = {_n(tot)}')} dollars.",
                     f"Split it {m(k)} ways: {m(rf'{_n(tot)} \div {k} = {_n(each)}')} dollars each."]
            fmt = money
        elif kind == "trucks":
            t = rng.randint(2, 6)
            load = rng.choice(range(60, 400, 12))
            k = rng.choice([4, 6, 8, 9, 12])
            tot = t * load
            need(tot % k == 0 and load % k != 0)
            each = Q(tot) / k
            stem = (f"{m(t)} trucks each carry {num(load)} cases of water to a training area. The "
                    f"water is shared equally among {m(k)} companies. How many cases does each "
                    "company get?")
            wrong = [(Q(tot), "is the total number of cases, not each company's share"),
                     (Q(load) * t / (k * 2), None),
                     (Q(tot) / (k + t), "divides by the number of trucks plus companies"),
                     (Q(load) - k, None)]
            steps = [f"Total cases: {m(rf'{t} \times {load} = {_n(tot)}')}.",
                     f"Share among {m(k)} companies: {m(rf'{_n(tot)} \div {k} = {_n(each)}')}."]
            fmt = num
        else:
            rent = rng.choice(range(1200, 2800, 50))
            util = rng.choice(range(120, 400, 10))
            net = rng.choice([40, 50, 60, 70, 80])
            k = rng.randint(3, 5)
            tot = rent + util + net
            need(tot % k == 0)
            each = Q(tot) / k
            stem = (f"{m(k)} roommates share an apartment. Each month the rent is {money(rent)}, "
                    f"utilities are {money(util)}, and internet is {money(net)}. If they split all "
                    "three costs equally, how much does each roommate pay per month?")
            wrong = [(Q(rent) / k, "splits only the rent") if rent % k == 0 else (Q(rent // k), None),
                     (Q(tot), "is the total monthly cost, not each share"),
                     (Q(rent) / k + util + net, "splits the rent but has each roommate pay all of the other bills")]
            steps = [f"Total monthly cost: {m(f'{_n(rent)} + {util} + {net} = {_n(tot)}')} dollars.",
                     f"Split it {m(k)} ways: {m(rf'{_n(tot)} \div {k} = {_n(each)}')} dollars each."]
            fmt = money
        return Problem(stem=stem, answer=each, fmt=fmt, wrong=wrong, steps=steps,
                       verify=lambda v: Q(v) * k == tot)
    # level 3: set some aside, then share the rest
    k = rng.choice([4, 6, 8, 9, 12])
    each = rng.randint(15, 60)
    keep = rng.randint(12, 90)
    total = k * each + keep
    need(total % k != 0)
    s = soldier(rng)
    ctx = rng.choice([
        (f"A unit receives {num(total)} MREs. {s} keeps {m(keep)} in reserve and divides the rest "
         f"equally among {m(k)} squads. How many MREs does each squad get?", num, "MREs"),
        (f"A school raises {money(total)} at a car wash. It spends {money(keep)} on supplies and "
         f"divides the rest equally among {m(k)} teams. How much does each team get?", money, "dollars"),
        (f"A food bank has {num(total)} cans of soup. It saves {m(keep)} cans for an emergency "
         f"shelf and packs the rest equally into {m(k)} boxes. How many cans go in each box?", num, "cans"),
    ])
    rest = total - keep
    return Problem(
        stem=ctx[0],
        answer=Q(each),
        fmt=ctx[1],
        wrong=[
            (Q(rest), "forgets to divide the rest"),
            (Q(each + keep), "adds the reserve back into each share"),
            (Q(total // k), f"divides all {num(total)} without setting any aside (and drops the remainder)"),
            (Q(each - 1), None),
        ],
        steps=[
            f"First set the reserve aside: {m(f'{_n(total)} - {keep} = {_n(rest)}')} {ctx[2]}.",
            f"Divide the rest equally: {m(rf'{_n(rest)} \div {k} = {each}')} {ctx[2]}.",
        ],
        verify=lambda v: Q(v) * k + keep == total,
    )


_GROUPS = [
    # (who, plural noun, container sing., plural, capacity choices, total range, military?)
    ("students", "students", "bus", "buses", [40, 44, 48, 50, 52], (150, 600), False),
    ("people", "people", "van", "vans", [8, 10, 12, 15], (30, 140), False),
    ("soldiers", "soldiers", "truck", "trucks", [16, 18, 20, 24], (60, 400), True),
    ("guests", "guests", "table", "tables", [6, 8, 10, 12], (40, 250), False),
    ("recruits", "recruits", "tent", "tents", [4, 6, 8, 12], (30, 200), True),
    ("books", "books", "box", "boxes", [12, 15, 20, 24, 25], (100, 500), False),
    ("troops", "troops", "helicopter", "helicopters", [10, 12, 15], (40, 160), True),
]


def _group_stem(rng, g, total, cap):
    who, noun, c1, c2 = g[0], g[1], g[2], g[3]
    if c1 == "bus":
        return (f"A school is taking {num(total)} students on a field trip. Each bus holds "
                f"{m(cap)} students. How many buses are needed?")
    if c1 == "van":
        return (f"{num(total)} people are going to a family reunion. Each van can carry {m(cap)} "
                f"people. How many vans are needed to carry everyone?")
    if c1 == "truck":
        return (f"A convoy must move {num(total)} soldiers. Each truck can carry {m(cap)} "
                f"soldiers. How many trucks are needed?")
    if c1 == "table":
        return (f"A wedding has {num(total)} guests. Each table seats {m(cap)} guests. What is "
                f"the least number of tables needed so that every guest has a seat?")
    if c1 == "tent":
        return (f"{num(total)} recruits are camping during field training. Each tent sleeps "
                f"{m(cap)} recruits. How many tents are needed?")
    if c1 == "box":
        return (f"A library is packing {num(total)} books. Each box holds {m(cap)} books. How many "
                f"boxes are needed to pack all the books?")
    return (f"{num(total)} troops must be flown to a landing zone. Each helicopter carries "
            f"{m(cap)} troops. If each helicopter makes one trip, how many helicopters are needed?")


@template("AR")
def round_up_groups(rng, lvl):
    g = rng.choice(_GROUPS)
    cap = rng.choice(g[4])
    total = rng.randint(*g[5])
    qf, r = divmod(total, cap)
    need(r != 0 and qf >= 2)
    need(cap - r >= 2)
    ceil_ = qf + 1
    exact = R(total, cap)
    c1, c2, noun = g[2], g[3], g[1]
    if lvl == 2:
        wrong = [(Q(qf), f"rounds down, which leaves {m(r)} {noun} with no {c1}"),
                 (Q(r), f"is the number of {noun} left over after filling {m(qf)} {c2}")]
        try:
            dec_raw(exact, max_places=2)
            wrong.append((exact, f"is the exact quotient, but you cannot use part of a {c1}"))
        except Exception:
            pass
        wrong.append((Q(ceil_ + 1), None))
        return Problem(
            stem=_group_stem(rng, g, total, cap),
            answer=Q(ceil_),
            fmt=dec,
            wrong=wrong,
            steps=[
                f"Divide: {m(rf'{_n(total)} \div {cap} = {qf}')} remainder {m(r)}.",
                f"{m(qf)} full {c2} hold {m(rf'{qf} \times {cap} = {_n(qf * cap)}')} {noun}, "
                f"so {m(r)} {noun} are still left.",
                f"They need one more {c1}: {m(f'{qf} + 1 = {ceil_}')} {c2}.",
            ],
            check=Q(-((-total) // cap)),
            verify=lambda v: (Q(v) - 1) * cap < total <= Q(v) * cap,
        )
    variant = rng.choice(["cost", "empty"])
    if variant == "empty":
        empty = ceil_ * cap - total
        stem = _group_stem(rng, g, total, cap)
        stem = stem.rsplit(" How", 1)[0].rsplit(" What", 1)[0]
        stem += (f" If they use the least number of {c2} possible, how many empty "
                 f"{'seats' if c1 not in ('box', 'tent') else 'spaces'} are left in the last {c1}?")
        return Problem(
            stem=stem,
            answer=Q(empty),
            fmt=num,
            wrong=[(Q(r), f"is the number of {noun} in the last {c1}, not the empty spaces"),
                   (Q(ceil_), f"is the number of {c2} needed"),
                   (Q(cap - r + cap), None),
                   (Q(qf), f"is the number of full {c2}")],
            steps=[
                f"Divide: {m(rf'{_n(total)} \div {cap} = {qf}')} remainder {m(r)}, "
                f"so {m(ceil_)} {c2} are needed.",
                f"The last {c1} holds only the {m(r)} leftover {noun}.",
                f"Empty spaces in it: {m(f'{cap} - {r} = {empty}')}.",
            ],
            check=Q(ceil_ * cap - total),
        )
    price = rng.choice({"bus": range(250, 500, 25), "van": range(60, 150, 5),
                        "truck": range(80, 200, 10), "table": range(8, 30, 2),
                        "tent": range(40, 120, 5), "box": range(2, 6),
                        "helicopter": range(900, 2000, 100)}[c1])
    what = {"bus": "Each bus costs {P} to rent for the day.",
            "van": "Each van costs {P} to rent for the day.",
            "truck": "Fuel and upkeep cost {P} per truck for the trip.",
            "table": "Each table rents for {P}.",
            "tent": "Each tent costs {P}.",
            "box": "Each box costs {P}.",
            "helicopter": "Each helicopter trip costs {P} in fuel."}[c1].format(P=money(price))
    stem = _group_stem(rng, g, total, cap)
    stem = stem.rsplit(" How", 1)[0].rsplit(" What", 1)[0]
    stem += f" {what} What is the total cost of the {c2} needed?"
    wrong = [(Q(qf) * price, f"rounds the number of {c2} down")]
    try:
        dec_raw(exact * price, max_places=2)
        wrong.append((exact * price, f"pays for a fraction of a {c1}"))
    except Exception:
        pass
    wrong += [(Q(ceil_ + 1) * price, f"rounds up one {c1} too many"),
              (Q(total) * price, f"multiplies the number of {noun} by the price")]
    return Problem(
        stem=stem,
        answer=Q(ceil_) * price,
        fmt=money,
        wrong=wrong,
        steps=[
            f"Divide: {m(rf'{_n(total)} \div {cap} = {qf}')} remainder {m(r)}.",
            f"The {m(r)} leftover {noun} need one more {c1}, so {m(ceil_)} {c2} are needed.",
            f"Cost: {m(rf'{ceil_} \times {_n(price)} = {_n(ceil_ * price)}')} dollars.",
        ],
        check=Q(-((-total) // cap)) * price,
    )


_REM = [
    ("cookies", "box", "boxes", [12, 15, 16, 20, 24], (100, 400), "A bakery packs {N} cookies into boxes of {C}."),
    ("eggs", "carton", "cartons", [12, 18], (100, 500), "A farm packs {N} eggs into cartons that hold {C} eggs each."),
    ("soldiers", "squad", "squads", [9, 10, 12, 13], (60, 250), "{S} divides {N} soldiers into squads of {C}."),
    ("photos", "page", "pages", [4, 6, 8, 9], (50, 200), "{P} puts {N} photos into an album, {C} photos to a page."),
    ("MREs", "case", "cases", [12, 24], (100, 500), "A supply clerk packs {N} MREs into cases of {C}."),
    ("players", "team", "teams", [5, 6, 9, 11], (40, 160), "A recreation league assigns {N} players to teams of {C}."),
]


@template("AR")
def remainder(rng, lvl):
    noun, c1, c2, caps, rngs, txt = rng.choice(_REM)
    cap = rng.choice(caps)
    total = rng.randint(*rngs)
    qf, r = divmod(total, cap)
    need(r >= 2 and cap - r >= 2 and qf >= 3)
    lead = txt.format(N=num(total), C=m(cap), S=soldier(rng), P=person(rng).name)
    full = {"squad": "complete squads", "team": "complete teams"}.get(c1, f"full {c2}")
    if rng.random() < 0.55:
        return Problem(
            stem=f"{lead} After making as many {full} as possible, how many {noun} are left over?",
            answer=Q(r),
            fmt=num,
            wrong=[(Q(qf), f"is the number of {full}, not the leftover {noun}"),
                   (Q(qf + 1), f"is the number of {c2} needed to hold all the {noun}"),
                   (Q(cap - r), f"is how many more {noun} it would take to fill another {c1}")],
            steps=[
                f"Divide: {m(rf'{_n(total)} \div {cap}')}. Since {m(rf'{qf} \times {cap} = {_n(qf * cap)}')}, "
                f"{m(qf)} {full} can be made.",
                f"Left over: {m(f'{_n(total)} - {_n(qf * cap)} = {r}')} {noun}.",
            ],
            check=Q(total % cap),
            verify=lambda v: 0 <= Q(v) < cap and (total - Q(v)) % cap == 0,
        )
    wrong = [(Q(qf + 1), f"rounds up, but the last {c1} would not be full"),
             (Q(r), f"is the number of {noun} left over")]
    exact = R(total, cap)
    try:
        dec_raw(exact, max_places=2)
        wrong.append((exact, f"is the exact quotient; a part of a {c1} is not a full {c1}"))
    except Exception:
        pass
    wrong.append((Q(qf - 1), None))
    return Problem(
        stem=f"{lead} How many {full} can be made?",
        answer=Q(qf),
        fmt=dec,
        wrong=wrong,
        steps=[
            f"Divide: {m(rf'{_n(total)} \div {cap} = {qf}')} remainder {m(r)}.",
            f"Only {m(qf)} {c2} are full; the {m(r)} extra {noun} are not enough for another one.",
        ],
        check=Q(total // cap),
    )


PLAN = [
    # (template, level, count)  -- easy -> hard; 25 problems
    (place_value, 1, 1),
    (rounding, 1, 1),
    (order_ops, 1, 2),
    (property_name, 1, 1),
    (multiply_by_hand, 1, 1),
    (shopping_total, 1, 1),
    (equal_share, 1, 1),
    (rounding, 2, 1),
    (order_ops, 2, 2),
    (distributive, 2, 1),
    (estimate, 2, 1),
    (divide_by_hand, 2, 1),
    (multiply_by_hand, 2, 1),
    (round_up_groups, 2, 1),
    (remainder, 2, 1),
    (shopping_total, 2, 1),
    (order_ops, 3, 3),
    (round_up_groups, 3, 1),
    (shopping_total, 3, 1),
    (equal_share, 3, 1),
    (equal_share, 2, 1),
]
