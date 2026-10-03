"""Chapter 6 - Percents (reference chapter: shows every convention)."""
from ..core import (R, Q, Problem, need, num, pct, money, m, F, tx, dec_raw,
                    int_raw, frac_raw, person, soldier, choose, template)

NUM = 6
TITLE = "Percents"
PART = 1

INTRO = r"""
\emph{Percent} means ``per hundred.'' Percent questions appear on both math
subtests, and most of them reduce to one sentence: \textbf{part = percent
$\times$ whole}.

\begin{concept}{Converting between forms}
\begin{itemize}
\item Percent $\to$ decimal: move the decimal point two places \emph{left}
  ($35\% = 0.35$, $4\% = 0.04$, $150\% = 1.5$).
\item Decimal $\to$ percent: move it two places \emph{right}
  ($0.6 = 60\%$, $0.075 = 7.5\%$).
\item Fraction $\to$ percent: divide, then convert
  ($\frac{3}{8} = 0.375 = 37.5\%$).
\end{itemize}
\end{concept}

\begin{concept}{The three percent questions}
Every basic percent problem gives you two of the three quantities in
\[ \text{part} = \text{percent} \times \text{whole} \]
and asks for the third.
\begin{itemize}
\item \textbf{Find the part:} $25\%$ of $64$ is $0.25 \times 64 = 16$.
\item \textbf{Find the percent:} $18$ is what percent of $72$?
  $\frac{18}{72} = 0.25 = 25\%$.
\item \textbf{Find the whole:} $24$ is $30\%$ of what number?
  $24 \div 0.30 = 80$.
\end{itemize}
\end{concept}

\begin{concept}{Percent change}
\[ \text{percent change} = \frac{\text{new} - \text{original}}{\text{original}} \times 100\% \]
Always divide by the \emph{original} (starting) value.
\end{concept}

\begin{example}{Worked example}
A jacket costs \$60. Its price goes up 15\%. What is the new price?

\textbf{Solution.} The increase is $0.15 \times 60 = 9$ dollars, so the new
price is $60 + 9 = \$69$. \emph{Shortcut:} a 15\% increase means you pay
115\%, and $1.15 \times 60 = 69$.
\end{example}

\begin{tip}
Benchmark percents make mental math fast: $10\%$ = move the decimal one
place left, $5\%$ = half of $10\%$, $1\%$ = move it two places, $25\% =
\frac14$, $50\% = \frac12$, $75\% = \frac34$, $20\% = \frac15$.
So $35\%$ of $80$ is $30\% + 5\% = 24 + 4 = 28$.
\end{tip}

\begin{trap}
\begin{itemize}
\item Answering the wrong question: if 35\% \emph{passed}, the number who
  \emph{did not} pass uses 65\%.
\item Dividing by the new value in a percent-change problem.
\item Adding successive percents: up 25\% then down 20\% is \emph{not} a
  5\% increase.
\end{itemize}
\end{trap}
"""

# percents that give clean mental math, with the number they must divide
_EASY = [5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80]


@template("MK")
def percent_of(rng, lvl):
    p = rng.choice(_EASY if lvl == 1 else _EASY + [12, 35, 45, 65, 120, 150])
    base = rng.choice(range(20, 400, 4) if lvl == 1 else range(20, 900, 4))
    ans = R(p, 100) * base
    need(ans.is_integer and ans > 1)
    return Problem(
        stem=f"What is {pct(p)} of {num(base)}?",
        answer=ans,
        fmt=num,
        wrong=[
            (ans * 10, "moves the decimal point only one place"),
            (base - ans, f"is what is left after removing {pct(p)}, not {pct(p)} of the number"),
            (ans / 10, "moves the decimal point three places"),
            (base + ans, f"adds {pct(p)} to the number"),
        ],
        steps=[
            f"Change the percent to a decimal: {m(f'{p}\\% = {dec_raw(R(p, 100))}')}.",
            f"Multiply by the number: {m(f'{dec_raw(R(p, 100))} \\times {int_raw(base)} = {int_raw(ans)}')}.",
        ],
        check=Q(p) * base / 100,
    )


@template("MK")
def convert(rng, lvl):
    kind = rng.choice(["dec", "frac"])
    if kind == "dec":
        hundredths = rng.choice([R(k) for k in range(2, 99)] + [R(k, 10) for k in range(5, 100, 10)])
        d = hundredths / 100
        need(d.q in (100, 50, 25, 20, 10, 5, 4, 2, 1000, 200, 500, 250, 125, 40, 8))
        ans = d * 100
        return Problem(
            stem=f"Which of the following is equal to {m(dec_raw(d))}?",
            answer=ans,
            fmt=pct,
            wrong=[
                (ans / 10, "moves the decimal point only one place"),
                (ans / 100, "forgets to move the decimal point at all"),
                (ans * 10, "moves the decimal point three places"),
            ],
            steps=[
                "To change a decimal to a percent, multiply by 100 (move the decimal point two places to the right).",
                f"{m(f'{dec_raw(d)} \\times 100 = {dec_raw(ans)}')}, so {m(f'{dec_raw(d)} = {dec_raw(ans)}\\%')}.",
            ],
            check=d * 100,
            sort=True,
        )
    den = rng.choice([4, 5, 8, 20, 25, 40] if lvl > 1 else [4, 5, 10, 20, 25, 50])
    num_ = rng.choice([k for k in range(1, den) if __import__("math").gcd(k, den) == 1])
    f = R(num_, den)
    ans = f * 100
    wrong = [
        (Q(num_), "just writes the numerator as if it were a percent"),
        (R(den, num_) * 100, "divides the denominator by the numerator"),
        (ans / 10, "moves the decimal point only one place"),
        (Q(num_ + den), None),
    ]
    return Problem(
        stem=f"What is {m(frac_raw(f))} written as a percent?",
        answer=ans,
        fmt=pct,
        wrong=wrong,
        steps=[
            f"Divide the numerator by the denominator: {m(f'{num_} \\div {den} = {dec_raw(f)}')}.",
            f"Multiply by 100 to get a percent: {m(f'{dec_raw(f)} = {dec_raw(ans)}\\%')}.",
        ],
        tip=(f"Or scale the fraction to hundredths: {m(F(num_, den) + ' = ' + F(int_raw(f * 100) if (f * 100).is_integer else dec_raw(f * 100), 100))}."
             if (f * 100).is_integer else None),
        check=Q(num_) / den * 100,
    )


def _what_percent_steps(part, whole, p):
    """Show the no-calculator route: reduce the fraction, then scale to /100."""
    from math import gcd
    g = gcd(int(part), int(whole))
    a_, b_ = int(part) // g, int(whole) // g
    steps = [f"Write the part over the whole: {m(F(int_raw(part), int_raw(whole)))}."]
    if g > 1:
        steps.append(f"Simplify by dividing the top and bottom by {num(g)}: "
                     f"{m(F(int_raw(part), int_raw(whole)) + ' = ' + F(a_, b_) if b_ != 1 else F(int_raw(part), int_raw(whole)) + ' = ' + str(a_))}.")
    k = R(100, b_)
    if b_ != 100 and k.is_integer:
        steps.append(f"Rewrite as hundredths: {m(F(a_, b_) + ' = ' + F(int_raw(a_ * k), 100) + ' = ' + int_raw(p) + r'\%')}.")
    else:
        steps.append(f"Convert to a percent: {m(F(a_, b_) + ' = ' + dec_raw(R(p, 100)) + ' = ' + int_raw(p) + r'\%')}.")
    return steps


@template("MK")
def what_percent(rng, lvl):
    p = rng.choice([5, 10, 12, 15, 20, 25, 30, 40, 60, 75, 80, 125, 150] if lvl > 1 else [10, 20, 25, 50, 75])
    whole = rng.choice(range(12, 400, 4))
    part = R(p, 100) * whole
    need(part.is_integer and part > 0)
    return Problem(
        stem=choose(rng,
                    f"The number {num(part)} is what percent of {num(whole)}?",
                    f"What percent of {num(whole)} is {num(part)}?"),
        answer=Q(p),
        fmt=pct,
        wrong=[
            (R(whole, part) * 100, "divides the whole by the part instead of the part by the whole"),
            (R(p, 10), "moves the decimal point only one place"),
            (R(p, 100), "forgets to multiply by 100"),
        ],
        steps=_what_percent_steps(part, whole, p),
        tip=f"Or test the choices: {pct(p)} of {num(whole)} is {m(f'{dec_raw(R(p, 100))} \\times {int_raw(whole)} = {int_raw(part)}')}.",
        check=part * 100 / whole,
    )


@template("MK")
def find_whole(rng, lvl):
    p = rng.choice([10, 20, 25, 30, 40, 50, 60, 75, 80] if lvl > 1 else [10, 20, 25, 50])
    whole = rng.choice(range(20, 500, 10 if lvl == 1 else 5))
    part = R(p, 100) * whole
    need(part.is_integer and part != whole)
    return Problem(
        stem=choose(rng,
                    f"Find the number if {pct(p)} of it is {num(part)}.",
                    f"If {pct(p)} of a number is {num(part)}, what is the number?"),
        answer=Q(whole),
        fmt=num,
        wrong=[
            (R(p, 100) * part, f"finds {pct(p)} of {num(part)} instead"),
            (part * 100 / p / 10, "slips the decimal point"),
            (part + p, "adds the percent to the part"),
            (part * p, "multiplies by the percent without converting it"),
        ],
        steps=[
            f"Use part {m('=')} percent {m(r'\times')} whole: {m(f'{int_raw(part)} = {dec_raw(R(p, 100))} \\times w')}.",
            f"Divide both sides by {m(dec_raw(R(p, 100)))}: {m(f'w = {int_raw(part)} \\div {dec_raw(R(p, 100))} = {int_raw(whole)}')}.",
            f"Check: {pct(p)} of {num(whole)} is {num(part)}. \\checkmark",
        ],
        verify=lambda w: R(p, 100) * w == part,
    )


@template("AR")
def complement_word(rng, lvl):
    p = rng.choice([10, 15, 20, 25, 30, 35, 40, 45, 60, 65, 70, 75, 80, 85, 90])
    total = rng.choice(range(20, 600, 4))
    hit = R(p, 100) * total
    need(hit.is_integer and 0 < hit < total)
    miss = total - hit
    ctx = rng.choice([
        ("A platoon of {T} soldiers took a marksmanship test, and {P} of them qualified as experts.",
         "How many soldiers did \\emph{not} qualify as experts?"),
        ("A recruiting office processed {T} applications last month. Of these, {P} were incomplete.",
         "How many applications were complete?"),
        ("A shipment contains {T} boxes, and {P} of the boxes are damaged.",
         "How many boxes are undamaged?"),
        ("Of the {T} students at a high school who took the ASVAB, {P} scored above 50 on the AFQT.",
         "How many of these students did \\emph{not} score above 50?"),
        ("A motor pool has {T} vehicles, and {P} of them are scheduled for maintenance this week.",
         "How many vehicles are \\emph{not} scheduled for maintenance?"),
    ])
    stem = ctx[0].format(T=num(total), P=pct(p)) + " " + ctx[1]
    return Problem(
        stem=stem,
        answer=miss,
        fmt=num,
        section="AR",
        wrong=[
            (hit, "is the number in the group described, not the number asked for"),
            (total - p, "subtracts the percent as if it were a count"),
            (miss * 10 if miss * 10 < total else miss + 10, None),
            (R(100 - p, 10) * total / 10 + 10, None),
        ],
        steps=[
            f"The question asks about the \\emph{{other}} group: {m(f'100\\% - {p}\\% = {100 - p}\\%')}.",
            f"Find that part: {m(f'{dec_raw(R(100 - p, 100))} \\times {int_raw(total)} = {int_raw(miss)}')}.",
        ],
        tip=f"Or find {pct(p)} first ({num(hit)}) and subtract: {m(f'{int_raw(total)} - {int_raw(hit)} = {int_raw(miss)}')}.",
        check=Q(total) - Q(total) * p / 100,
    )


@template("AR")
def percent_change(rng, lvl):
    # (context, low, high, step, allowed directions, percents) — realistic moves only
    ctx = rng.choice([
        ("the price of a pair of boots", 60, 240, 4, "ud", [10, 20, 25, 30, 40, 50]),
        ("a monthly phone bill", 40, 160, 4, "ud", [5, 10, 20, 25]),
        ("the price of a gallon of paint", 20, 80, 4, "u", [5, 10, 20, 25]),
        ("the cost of a yearly gym membership", 200, 800, 20, "ud", [5, 10, 15, 20, 25]),
        ("the price of a tool kit", 40, 300, 4, "ud", [10, 20, 25, 30, 40]),
        ("the price of a backpack", 30, 160, 2, "d", [10, 20, 25, 30, 40, 50]),
        ("the value of a used car", 4000, 20000, 100, "d", [10, 15, 20, 25, 30]),
        ("monthly rent for an apartment", 800, 2400, 50, "u", [2, 4, 5, 6, 8, 10]),
        ("a soldier's monthly housing allowance", 1200, 2800, 50, "u", [2, 4, 5, 10]),
    ])
    item, lo, hi, step, dirs, pcts = ctx
    up = rng.choice(dirs) == "u"
    p = rng.choice(pcts)
    old = rng.choice(range(lo, hi + 1, step))
    new = Q(old) * (100 + p) / 100 if up else Q(old) * (100 - p) / 100
    need(new.is_integer and new > 0)
    change = abs(new - old)
    word = "increase" if up else "decrease"
    return Problem(
        stem=(f"Last year {item} was {money(old)}. This year it is {money(new)}. "
              f"What is the percent {word}?"),
        answer=Q(p),
        fmt=pct,
        section="AR",
        wrong=[
            (change * 100 / new, "divides by the new amount instead of the original amount"),
            (change, "gives the dollar change instead of the percent change"),
            (new * 100 / old, "gives the new amount as a percent of the old amount"),
        ],
        steps=[
            f"Find the amount of {word}: {m(f'{int_raw(max(old, new))} - {int_raw(min(old, new))} = {int_raw(change)}')} dollars.",
            f"Divide by the \\emph{{original}} amount: {m(F(int_raw(change), int_raw(old)) + ' = ' + dec_raw(R(p, 100)))}.",
            f"Convert to a percent: {m(dec_raw(R(p, 100)) + ' = ' + str(p) + r'\%')} {word}.",
        ],
        tip=f"Hard division? Test the choices instead: {pct(p)} of {money(old)} is {money(change)}, exactly the change.",
        check=abs(new - old) / old * 100,
    )


@template("MK")
def percent_of_percent(rng, lvl):
    p1 = rng.choice([10, 20, 25, 40, 50, 60, 75, 80])
    p2 = rng.choice([10, 20, 25, 40, 50, 60, 75, 80])
    need(p1 != p2)
    base = rng.choice(range(40, 1000, 20))
    mid = R(p2, 100) * base
    ans = R(p1, 100) * mid
    need(mid.is_integer and ans.is_integer)
    return Problem(
        stem=f"What is {pct(p1)} of {pct(p2)} of {num(base)}?",
        answer=ans,
        fmt=num,
        wrong=[
            (R(p1 + p2, 100) * base, "adds the two percents"),
            (mid, f"stops after taking {pct(p2)}"),
            (R(p1, 100) * base, f"takes only {pct(p1)} of {num(base)}"),
            (R(abs(p1 - p2), 100) * base, "subtracts the two percents"),
        ],
        steps=[
            f"Work from the inside out. First, {m(f'{p2}\\%')} of {num(base)}: {m(f'{dec_raw(R(p2, 100))} \\times {int_raw(base)} = {int_raw(mid)}')}.",
            f"Then {m(f'{p1}\\%')} of that result: {m(f'{dec_raw(R(p1, 100))} \\times {int_raw(mid)} = {int_raw(ans)}')}.",
        ],
        tip=(f"Percents of percents multiply: {m(f'{dec_raw(R(p1, 100))} \\times {dec_raw(R(p2, 100))} = {dec_raw(R(p1 * p2, 10000))}')}, and {m(f'{dec_raw(R(p1 * p2, 10000))} \\times {int_raw(base)} = {int_raw(ans)}')}."
             if (p1 * p2) % 100 == 0 else None),
        check=Q(p1) * p2 * base / 10000,
    )


@template("AR")
def up_then_down(rng, lvl):
    pu = rng.choice([10, 20, 25, 40, 50])
    pd = rng.choice([10, 20, 25, 40, 50])
    item, lo, hi = rng.choice([("television", 200, 900), ("bicycle", 120, 800),
                               ("pair of running shoes", 60, 200), ("camping tent", 80, 400),
                               ("power drill", 60, 300), ("winter coat", 80, 360)])
    old = rng.choice(range(lo, hi + 1, 4))
    mid = old * R(100 + pu, 100)
    end = mid * R(100 - pd, 100)
    need(mid.is_integer and end.is_integer)
    net = pu - pd
    wrong = [
        (old * R(100 + net, 100), f"combines the changes into a single {abs(net)}\\% {'increase' if net >= 0 else 'decrease'}" if net else "assumes the two changes cancel out"),
        (mid, "stops after the increase"),
        (old * R(100 - pd, 100), "applies only the decrease"),
        (mid - R(pd, 100) * old, "takes the decrease from the original price instead of the raised price"),
    ]
    return Problem(
        stem=choose(rng,
                    f"A {item} was priced at {money(old)}. The store raised the price by {pct(pu)}, "
                    f"and a month later it marked the new price down by {pct(pd)}. What is the final price?",
                    f"A store priced a {item} at {money(old)}. Later it increased the price by {pct(pu)}, "
                    f"then put the {item} on sale at {pct(pd)} off the new price. What is the sale price?"),
        answer=end,
        fmt=money,
        section="AR",
        wrong=wrong,
        steps=[
            f"Raise the price by {pct(pu)}: {m(f'{int_raw(old)} \\times {dec_raw(R(100 + pu, 100))} = {dec_raw(mid)}')}.",
            f"Take {pct(pd)} off the \\emph{{new}} price: {m(f'{dec_raw(mid)} \\times {dec_raw(R(100 - pd, 100))} = {dec_raw(end)}')}.",
            f"The final price is {money(end)}.",
        ],
        check=Q(old) * (100 + pu) * (100 - pd) / 10000,
    )


@template("AR")
def part_of_part(rng, lvl):
    total = rng.choice(range(100, 1300, 50))
    p = rng.choice([20, 30, 40, 45, 60, 80])
    f_den = rng.choice([3, 4, 5])
    f_num = rng.choice(range(1, f_den))
    group = R(p, 100) * total
    ans = group * R(f_num, f_den)
    need(group.is_integer and ans.is_integer)
    s = soldier(rng)
    fr = frac_raw(R(f_num, f_den))
    ctx = rng.choice([
        (f"A training battalion has {num(total)} recruits. Of these, {pct(p)} are assigned to the morning shift, "
         f"and {m(fr)} of the morning-shift recruits are on kitchen duty. How many recruits are on kitchen duty?"),
        (f"A warehouse holds {num(total)} crates. Of the crates, {pct(p)} contain medical supplies, and "
         f"{m(fr)} of those crates must be kept refrigerated. How many crates must be refrigerated?"),
        (f"{s} surveyed {num(total)} service members. Of those surveyed, {pct(p)} said they exercise every day, "
         f"and {m(fr)} of the daily exercisers said they run. How many said they run?"),
        (f"A high school has {num(total)} seniors. Of the seniors, {pct(p)} plan to go to college, and "
         f"{m(fr)} of those students plan to study engineering. How many seniors plan to study engineering?"),
        (f"A food bank received {num(total)} cans of food. Of the cans, {pct(p)} were vegetables, and "
         f"{m(fr)} of the vegetable cans were corn. How many cans of corn did the food bank receive?"),
    ])
    return Problem(
        stem=ctx,
        answer=ans,
        fmt=num,
        section="AR",
        wrong=[
            (group, "is the size of the first group only"),
            (total * R(f_num, f_den), f"takes {m(fr)} of the whole total"),
            (group - ans, f"is the part of the group that is \\emph{{not}} included"),
        ],
        steps=[
            f"Find the first group: {m(f'{dec_raw(R(p, 100))} \\times {int_raw(total)} = {int_raw(group)}')}.",
            f"Take {m(fr)} of that group: {m(f'{fr} \\times {int_raw(group)} = {int_raw(ans)}')}.",
        ],
        check=Q(total) * p * f_num / (100 * f_den),
    )


PLAN = [
    # (template, level, count)  -- easy -> hard; 25 problems
    (percent_of, 1, 3),
    (convert, 1, 3),
    (complement_word, 1, 2),
    (what_percent, 2, 3),
    (find_whole, 2, 3),
    (convert, 2, 1),
    (percent_change, 2, 2),
    (percent_of, 2, 1),
    (percent_of_percent, 3, 2),
    (up_then_down, 3, 3),
    (part_of_part, 3, 2),
]
