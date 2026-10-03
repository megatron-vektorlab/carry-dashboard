"""Chapter 23 - Interest, Commission & Percent Change (word problems)."""
import functools
from fractions import Fraction

from ..core import (R, Q, Problem, Person, need, num, money, pct, m, F, unit, dec,
                    dec_raw, int_raw, frac_raw, mixed_raw, person, choose, template)

NUM = 23
TITLE = r"Interest, Commission \& Percent Change"
PART = 4

INTRO = r"""
Chapter 6 covered the basic percent questions. This chapter puts percents to
work with money: interest on savings and loans, commission and markup, raises,
and the two kinds of problems that trip up the most test takers, \emph{chains}
of percents and \emph{working backward} from a percent.

\begin{concept}{Simple interest}
\[ I = P \times r \times t \]
$P$ = principal (the amount saved or borrowed), $r$ = yearly rate as a decimal,
$t$ = time \emph{in years}. The balance (or the amount owed) is $P + I$.
Change months to years by dividing by 12: 6 months $= \frac{6}{12} = \frac12$
year, 8 months $= \frac{8}{12} = \frac23$ year, 18 months $= 1\frac12$ years.
\end{concept}

\begin{concept}{Commission, markup, and raises}
\begin{itemize}
\item \textbf{Commission} $=$ rate $\times$ sales. Total pay $=$ base pay $+$ commission.
\item \textbf{Markup} $=$ rate $\times$ cost; selling price $=$ cost $+$ markup;
  profit $=$ selling price $-$ cost.
\item \textbf{Raise:} new pay $=$ old pay $+$ rate $\times$ old pay $= (1 + \text{rate}) \times$ old pay.
\end{itemize}
\end{concept}

\begin{concept}{Chains of percents and working backward}
\begin{itemize}
\item Percent changes in a row \textbf{multiply}: $20\%$ off and then $10\%$ off
  leaves $0.80 \times 0.90 = 0.72$ of the price, a $28\%$ discount, not $30\%$.
\item \textbf{Compound interest} works the same way: each year's interest is added
  before the next year's interest is figured.
\item \textbf{Working backward:} if the price \emph{after} $20\%$ off is \$64, then
  \$64 is $80\%$ of the original. Divide: $64 \div 0.80 = \$80$.
\end{itemize}
\end{concept}

\begin{example}{Worked example}
After a $25\%$ raise, a store manager earns \$20 per hour. What did she earn
before the raise?

\textbf{Solution.} The new wage is $125\%$ of the old wage:
$1.25 \times \text{old} = 20$, so old $= 20 \div 1.25 = \$16$.
Check: $25\%$ of \$16 is \$4, and $\$16 + \$4 = \$20$. (Taking $25\%$ off
\$20 gives \$15, which is wrong: the raise was $25\%$ of the \emph{old} wage.)
\end{example}

\begin{tip}
Turn friendly decimals into fractions: dividing by $0.80$ is multiplying by
$\frac54$, and dividing by $1.25$ is multiplying by $\frac45$. For interest, find
one year's interest first, then multiply by the number of years.
\end{tip}

\begin{trap}
\begin{itemize}
\item Using months as if they were years in $I = Prt$.
\item Working backward by adding the percent to the \emph{new} amount
  (\$64 after $20\%$ off is not $64 + 12.80$).
\item Adding two discounts in a row, or adding a raise and a cut that follow each other.
\item Paying commission on \emph{all} sales when it is earned only above a set amount.
\end{itemize}
\end{trap}
"""

# --------------------------------------------------------------------------
# private helpers
# --------------------------------------------------------------------------

_LAST = ["Ruiz", "Chen", "Walker", "Okafor", "Patel", "Novak", "Brooks", "Kim",
         "Santos", "Reyes", "Jensen", "Haddad", "Lopez", "Nguyen", "Carter", "Murphy"]
_RANKS = ["Private", "Specialist", "Corporal", "Sergeant", "Airman",
          "Lance Corporal", "Petty Officer", "Seaman"]


def _trooper(rng, ranks=None):
    he, him, his = rng.choice([("he", "him", "his"), ("she", "her", "her")])
    return Person(f"{rng.choice(ranks or _RANKS)} {rng.choice(_LAST)}", he, him, his)


def _art(word):
    return "an" if word[0] in "aeiouAEIO" else "a"


def _cap(s):
    return s[0].upper() + s[1:]


def _art_n(v):
    """'a' or 'an' before a number as it is read aloud (an 8, an 18, an 11,000)."""
    v = Q(v)
    s = str(int(v.floor())) if v >= 1 else "0"
    if s[0] == "8" or (s[:2] in ("11", "18") and len(s) % 3 == 2):
        return "an"
    return "a"


def _pdec(p):
    """Percent p as a decimal string: 6 -> 0.06, 4.5 -> 0.045."""
    return dec_raw(Q(p) / 100)


def _ok_cents(v):
    return (Q(v) * 100).is_integer


def _near_money(ans):
    A = Q(ans)
    step = next((Q(x) for x in (R(1, 100), R(1, 20), R(1, 4), 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000,
                                2000, 5000, 10000) if abs(A) <= 12 * Q(x)), Q(20000))

    def f(rng):
        out = [A + k * step for k in (1, 2, 3, -1, -2, -3)]
        out = [v for v in out if v > 0]
        rng.shuffle(out)
        return out
    return f


def _near_pct(ans):
    A = Q(ans)
    step = 1 if A < 12 else 5

    def f(rng):
        out = [A + k * step for k in (1, 2, 3, -1, -2, -3) if A + k * step > 0]
        rng.shuffle(out)
        return out
    return f


def _pick(rng, seq, part):
    """rng.choice(seq), or - for a template variant - only from slice k of n."""
    if part is None:
        return rng.choice(seq)
    k, n = part
    return rng.choice(seq[k::n])


def _variants(fn, n):
    """Split a template into n variants that draw from disjoint slices of its
    contexts, so the copies used in one practice set never share a context."""
    out = []
    for k in range(n):
        def g(rng, lvl, _k=k):
            return fn(rng, lvl, part=(_k, n))
        g.__name__ = g.__qualname__ = f"{fn.__name__}_{'abcd'[k]}"
        g.__module__ = fn.__module__
        g.section = fn.section
        out.append(g)
    return out


def _fill(fn):
    """Same-shape filler distractors for money and percent answers."""
    @functools.wraps(fn)
    def wrapper(rng, lvl, **kw):
        p = fn(rng, lvl, **kw)
        if p.near is None and not isinstance(p.answer, str):
            if p.fmt is money:
                p.near = _near_money(p.answer)
            elif p.fmt is pct:
                p.near = _near_pct(p.answer)
        return p
    return wrapper


def _years_txt(mo):
    """'8 months = 8/12 = 2/3 year' style conversion text (math, raw)."""
    t = R(mo, 12)
    shown = mixed_raw(t) if t > 1 else frac_raw(t)
    extra = f" = {dec_raw(t)}" if t.q in (2, 4) else ""
    return f"{mo} \\text{{ months}} = {F(mo, 12)} = {shown}{extra}"


# --------------------------------------------------------------------------
# simple interest: contexts
# --------------------------------------------------------------------------

_INT_CTX = [
    # (kind, stem, P lo, hi, step, rates, years, military)
    ("save", "{B} deposits {P} in a savings account that pays {r} simple interest per year.",
     500, 5000, 100, [2, 3, 4, 5], [2, 3, 4, 5], False),
    ("save", "{B} puts {aP} {P} enlistment bonus into a savings account at the base credit union. The "
     "account pays {r} simple interest per year.", 2000, 10000, 500, [2, 3, 4, 5], [2, 3, 4, 5], True),
    ("save", "{B} buys a certificate of deposit (CD) for {P}. The CD pays {r} simple interest per year.",
     1000, 10000, 500, [3, 4, 5], [2, 3, 4, 5], False),
    ("loan", "{B} borrows {P} from a credit union to buy a used car. The loan charges {r} simple interest "
     "per year.", 4000, 12000, 500, [4, 5, 6, 7, 8], [2, 3, 4, 5], False),
    ("loan", "{B} takes out {aP} {P} personal loan that charges {r} simple interest per year.",
     1000, 5000, 250, [8, 9, 10, 12], [1, 2, 3], False),
    ("loan", "{B} borrows {P} from the base credit union to furnish {his} first apartment off base. The "
     "loan charges {r} simple interest per year.", 1500, 6000, 250, [6, 7, 8, 9], [1, 2, 3], True),
]


def _int_setup(rng, kinds=("save", "loan"), half=False, part=None):
    """Context sentence for an interest problem. The rate is drawn here (from the
    context's realistic rates, plus half-percents if ``half``) so that the
    sentence and the numbers can never disagree."""
    kind, st, lo, hi, step, rates, years, mil = _pick(rng, [c for c in _INT_CTX if c[0] in kinds], part)
    B = _trooper(rng) if mil else person(rng)
    P = Q(rng.choice(range(lo, hi + 1, step)))
    if half:
        rates = sorted(set(rates) | {Q(x) + R(1, 2) for x in rates[:-1]})
    r = Q(rng.choice(rates))
    text = st.format(B=B, P=money(P), aP=_art_n(P), r=pct(r), his=B.his)
    return kind, B, P, r, years, text


# --------------------------------------------------------------------------
# 1. simple interest (L1 years, L2 months)
# --------------------------------------------------------------------------

@template("AR")
@_fill
def simple_interest(rng, lvl, part=None):
    kind, B, P, r, years, intro = _int_setup(rng, part=part)
    Y = P * r / 100                       # one year's interest
    if lvl == 1:
        t = rng.choice(years)
        I = Y * t
        need(t > 1)
        q = f" How much interest will {B.he} {'earn' if kind == 'save' else 'pay'} in {t} years?"
        return Problem(
            stem=intro + q, answer=I, fmt=money, section="AR",
            wrong=[(Y, "finds the interest for only one year"),
                   (P + I, "is the total with interest, not the interest alone"),
                   (I * 10, f"writes {pct(r)} as {m(dec_raw(Q(r) / 10))} instead of {m(_pdec(r))}"),
                   (P * r * t, "forgets to change the percent to a decimal")],
            steps=[f"Use {m('I = P \\times r \\times t')} with {m(f'r = {r}\\% = {_pdec(r)}')} and "
                   f"{m(f't = {t}')} years.",
                   f"One year's interest: {m(f'{money(P)} \\times {_pdec(r)} = {money(Y)}')}.",
                   f"For {t} years: {m(f'{money(Y)} \\times {t} = {money(I)}')}."],
            check=Fraction(int(P)) * Fraction(r, 100) * t,
        )
    mo = rng.choice([3, 4, 6, 8, 9, 10, 15, 18, 20, 30])
    t = R(mo, 12)
    I = Y * t
    need(_ok_cents(I) and _ok_cents(Y))
    q = f" How much interest will {B.he} {'earn' if kind == 'save' else 'pay'} in {mo} months?"
    wrong = [(Y * mo, f"uses {mo} years instead of {mo} months"),
             (Y, "finds the interest for a full year"),
             (Y / 12, "finds the interest for just one month"),
             (P + I, "is the total with interest, not the interest alone")]
    if mo != 10:
        wrong.append((Y * R(mo, 10), f"writes {mo} months as {m(dec_raw(R(mo, 10)))} years"))
    return Problem(
        stem=intro + q, answer=I, fmt=money, section="AR", wrong=wrong,
        steps=[f"Time must be in years: {m(_years_txt(mo))} year{'s' if t > 1 else ''}.",
               f"One year's interest: {m(f'{money(P)} \\times {_pdec(r)} = {money(Y)}')}.",
               (f"For {m(frac_raw(t))} of a year: " if t < 1 else f"For {m(mixed_raw(t))} years: ")
               + f"{m(f'{money(Y)} \\times {mixed_raw(t) if t > 1 else frac_raw(t)} = {money(I)}')}."],
        check=Fraction(int(P)) * Fraction(r, 100) * Fraction(mo, 12),
    )


# --------------------------------------------------------------------------
# 2. balance / total owed (L2)
# --------------------------------------------------------------------------

@template("AR")
@_fill
def interest_balance(rng, lvl, part=None):
    kind, B, P, r, years, intro = _int_setup(rng, kinds=("save", "loan") if part is None
                                             else (("save",), ("loan",))[part[0]])
    Y = P * r / 100
    if rng.random() < 0.7:
        t, tt = Q(rng.choice(years)), None
        need(t > 1)
        when = f"at the end of {int(t)} years"
    else:
        mo = rng.choice([6, 18, 30])
        t, tt = R(mo, 12), mo
        when = f"after {mo} months"
    I = Y * t
    need(_ok_cents(I))
    total = P + I
    if kind == "save":
        q = f" How much money will be in the account {when}?"
    else:
        q = f" What is the total amount {B.he} must pay back {when}?"
    wrong = [(I, "is only the interest, not the total"),
             (P + Y, "adds only one year of interest"),
             (P + 10 * I, f"writes {pct(r)} as {m(dec_raw(Q(r) / 10))} instead of {m(_pdec(r))}")]
    if tt:
        wrong.append((P + Y * tt, f"uses {tt} years instead of {tt} months"))
    comp = P * (1 + Q(r) / 100) ** int(t) if t.is_integer else None
    if comp is not None and _ok_cents(comp) and comp != total:
        wrong.append((comp, "adds interest on the interest, but simple interest is figured on the "
                            "principal only"))
    steps = []
    if tt:
        steps.append(f"Change the time to years: {m(_years_txt(tt))} year{'s' if t > 1 else ''}.")
    steps += [f"One year's interest: {m(f'{money(P)} \\times {_pdec(r)} = {money(Y)}')}.",
              f"Interest for the whole time: {m(f'{money(Y)} \\times {mixed_raw(t) if tt else int_raw(t)} = {money(I)}')}.",
              f"Add it to the principal: {m(f'{money(P)} + {money(I)} = {money(total)}')}."]
    return Problem(stem=intro + q, answer=total, fmt=money, section="AR", wrong=wrong, steps=steps,
                   check=Fraction(int(P)) * (1 + Fraction(r, 100) * Fraction(t.p, t.q)))


# --------------------------------------------------------------------------
# 3. monthly payment on a simple-interest loan (L3)
# --------------------------------------------------------------------------

_LOANS = [
    ("{B} borrows {P} from the base credit union to buy a used truck.", True),
    ("{B} takes out a loan of {P} to buy a used car.", False),
    ("{B} borrows {P} to buy a motorcycle.", False),
    ("{B} takes out a loan of {P} to buy furniture for {his} apartment off base.", True),
    ("{B} borrows {P} to pay for a welding certification course.", False),
]


@template("AR")
@_fill
def loan_payment(rng, lvl, part=None):
    st, mil = rng.choice(_LOANS)
    B = _trooper(rng) if mil else person(rng)
    t = rng.choice([2, 3, 4])
    r = rng.choice([4, 5, 6, 8, 10])
    P = Q(rng.choice(range(2400, 14401, 600)))
    I = P * r * t / 100
    total = P + I
    pay = total / (12 * t)
    need(pay.is_integer)
    stem = (st.format(B=B, P=money(P), his=B.his)
            + f" The loan charges {pct(r)} simple interest per year, and {B.he} will repay the principal "
              f"plus interest in equal monthly payments over {t} years. How much is each monthly payment?")
    return Problem(
        stem=stem, answer=pay, fmt=money, section="AR",
        wrong=[(P / (12 * t), "forgets to add the interest"),
               (total / 12, "divides by 12 instead of by the total number of months"),
               (total / t, "gives the yearly payment, not the monthly payment"),
               ((P + P * r / 100) / (12 * t), "adds only one year of interest")],
        steps=[f"Interest: {m(f'{money(P)} \\times {_pdec(r)} \\times {t} = {money(I)}')}.",
               f"Total to repay: {m(f'{money(P)} + {money(I)} = {money(total)}')}.",
               f"Number of payments: {m(f'{t} \\times 12 = {12 * t}')} months.",
               f"Each payment: {m(f'{money(total)} \\div {12 * t} = {money(pay)}')}."],
        verify=lambda v: v * 12 * t == P * (100 + r * t) / 100,
    )


# --------------------------------------------------------------------------
# 4. find the rate or the time (L3)
# --------------------------------------------------------------------------

@template("AR")
@_fill
def find_rate_time(rng, lvl, part=None):
    kind, B, P, r, years, intro = _int_setup(rng, half=True)
    t = rng.choice([2, 3, 4, 5])
    Y = P * r / 100
    I = Y * t
    need(I.is_integer and _ok_cents(Y))
    if (rng.random() < 0.6) if part is None else part[0] == 0:
        # find the rate
        if kind == "save":
            stem = (f"{B} deposited {money(P)} in an account that pays simple interest. After {t} years "
                    f"the account had earned {money(I)} in interest. What is the yearly interest rate?")
        else:
            stem = (f"{B} borrowed {money(P)} at simple interest and paid {money(I)} in interest over {t} "
                    f"years. What was the yearly interest rate?")
        wrong = [(Q(r) * t, f"forgets to divide by the {t} years"),
                 (Q(r) / 100, "forgets to change the decimal to a percent"),
                 (Q(r) / t if _ok_cents(Q(r) / t) else Q(r) + 1, f"divides by {t} twice" if _ok_cents(Q(r) / t) else None)]
        dec_r = Q(r) / 100
        return Problem(
            stem=stem, answer=Q(r), fmt=pct, section="AR", wrong=wrong,
            steps=[f"Interest for one year: {m(f'{money(I)} \\div {t} = {money(Y)}')}.",
                   f"Divide by the principal: {m(f'{money(Y)} \\div {money(P)} = {dec_raw(dec_r)}')}.",
                   f"Change to a percent: {m(f'{dec_raw(dec_r)} = {dec_raw(r)}\\%')}."],
            tip=f"Check: {m(f'{money(P)} \\times {dec_raw(dec_r)} \\times {t} = {money(I)}')}.",
            verify=lambda v: P * v / 100 * t == I,
        )
    # find the time
    stem = intro + (f" How many years will it take for the account to earn {money(I)} in interest?"
                    if kind == "save" else
                    f" After how many years will the interest on the loan add up to {money(I)}?")
    yr = unit(dec, "year")
    return Problem(
        stem=stem, answer=Q(t), fmt=yr, section="AR",
        wrong=[(Q(t) * 12, "gives the number of months, not years"),
               (Q(t) / 100, "forgets to change the percent to a decimal"),
               (Q(t) + 1, None), (Q(t) - 1 if t > 2 else Q(t) + 2, None)],
        steps=[f"One year's interest: {m(f'{money(P)} \\times {_pdec(r)} = {money(Y)}')}.",
               f"Number of years: {m(f'{money(I)} \\div {money(Y)} = {t}')}."],
        tip=f"Check: {m(f'{money(Y)} \\times {t} = {money(I)}')}.",
        verify=lambda v: Y * v == I,
    )


# --------------------------------------------------------------------------
# 5. commission
# --------------------------------------------------------------------------

_COMM1 = [
    # (stem, S lo, hi, step, rates, military)
    ("A real estate agent earns {ar} {r} commission on each home {he} sells. How much commission does {he} "
     "earn on a home that sells for {S}?", 150000, 450000, 5000, [2, R(5, 2), 3], False),
    ("{B} sells cars and earns {ar} {r} commission on the price of each car {he} sells. What is {his} "
     "commission on a car that sells for {S}?", 16000, 48000, 500, [2, 3, 4, 5], False),
    ("{B} works at an electronics store and earns {ar} {r} commission on everything {he} sells. Last week "
     "{he} sold {S} worth of merchandise. How much commission did {he} earn?", 3000, 12000, 100,
     [3, 4, 5, 6, 8], False),
    ("After leaving the Navy, {B} took a job selling boats. {He} earns {ar} {r} commission on each sale. "
     "How much does {he} earn for selling a boat priced at {S}?", 20000, 90000, 1000, [3, 4, 5, 6], True),
    ("{B}, an Army veteran, sells insurance and earns {ar} {r} commission on the yearly premiums {he} sells. "
     "This month {he} sold {S} in premiums. What is {his} commission?", 8000, 30000, 500, [5, 8, 10, 12], True),
]


@template("AR")
@_fill
def commission(rng, lvl, part=None):
    B = person(rng)
    if lvl == 1:
        st, lo, hi, step, rates, mil = _pick(rng, _COMM1, part)
        S = Q(rng.choice(range(lo, hi + 1, step)))
        r = rng.choice(rates)
        c = S * r / 100
        need(_ok_cents(c))
        he = B.he if "{B}" in st else rng.choice(["he", "she"])
        his = {"he": "his", "she": "her"}[he]
        stem = st.format(B=B, He=he.capitalize(), he=he, his=his, S=money(S), r=pct(r), ar=_art_n(r))
        return Problem(
            stem=stem, answer=c, fmt=money, section="AR",
            wrong=[(c * 10, f"writes {pct(r)} as {m(dec_raw(Q(r) / 10))} instead of {m(_pdec(r))}"),
                   (c / 10, "moves the decimal point three places instead of two"),
                   (S - c, "subtracts the commission from the sale price"),
                   (S * r, "forgets to change the percent to a decimal")],
            steps=[f"Commission {m('=')} rate {m('\\times')} sales. Change the rate to a decimal: "
                   f"{m(f'{dec_raw(r)}\\% = {_pdec(r)}')}.",
                   f"Multiply: {m(f'{_pdec(r)} \\times {money(S)} = {money(c)}')}."],
            check=Fraction(int(S)) * Fraction(Q(r).p, Q(r).q * 100),
        )
    weekly = (rng.random() < 0.6) if (part is None or lvl == 3) else part[0] == 0
    if weekly:
        base = Q(rng.choice([300, 350, 400, 450, 500, 550]))
        r = rng.choice([4, 5, 6, 8, 10])
        S = Q(rng.choice(range(3000, 15001, 100)))
        per, when = "week", "this week"
    else:
        base = Q(rng.choice(range(1500, 2601, 100)))
        r = rng.choice([2, 3, 4, 5])
        S = Q(rng.choice(range(20000, 80001, 500)))
        per, when = "month", "this month"
    job = rng.choice(["furniture store", "car dealership", "cell phone store", "appliance store",
                      "home-security company"])
    if lvl == 2:
        c = S * r / 100
        need(_ok_cents(c))
        pay = base + c
        stem = (f"{B} works at {_art(job)} {job} and earns a base salary of {money(base)} per {per} plus {_art_n(r)} {pct(r)} "
                f"commission on {B.his} sales. {B.His} sales {when} total {money(S)}. What is {B.his} total "
                f"pay for the {per}?")
        return Problem(
            stem=stem, answer=pay, fmt=money, section="AR",
            wrong=[(c, "is the commission only; it leaves out the base salary"),
                   ((base + S) * r / 100, "takes the commission on the base salary plus sales"),
                   (base + c * 10, f"writes {pct(r)} as {m(dec_raw(Q(r) / 10))}"),
                   (base + S, "adds the sales instead of the commission")],
            steps=[f"Commission: {m(f'{_pdec(r)} \\times {money(S)} = {money(c)}')}.",
                   f"Add the base salary: {m(f'{money(base)} + {money(c)} = {money(pay)}')}."],
            check=base + Fraction(int(S)) * Fraction(r, 100),
        )
    # level 3: commission only on sales above a threshold, or sales needed for a target
    if (rng.random() < 0.6) if part is None else part[0] == 0:
        T = Q(rng.choice([2000, 3000, 5000] if weekly else [10000, 15000, 20000]))
        r = rng.choice([5, 8, 10, 12])
        need(S > T + 1000)
        over = S - T
        c = over * r / 100
        need(_ok_cents(c))
        pay = base + c
        stem = (f"{B} works at {_art(job)} {job}. {B.He} earns {money(base)} per {per} plus {_art_n(r)} {pct(r)} commission on "
                f"all sales \\emph{{over}} {money(T)} for the {per}. {B.His} sales {when} total {money(S)}. "
                f"What is {B.his} total pay for the {per}?")
        return Problem(
            stem=stem, answer=pay, fmt=money, section="AR",
            wrong=[(base + S * r / 100, f"pays commission on all the sales, not just the sales over {money(T)}"),
                   (c, "is the commission only; it leaves out the base pay"),
                   (base + T * r / 100, f"takes the commission on the first {money(T)} instead of the amount over it"),
                   (S * r / 100, "pays commission on all the sales and leaves out the base pay")],
            steps=[f"Sales that earn commission: {m(f'{money(S)} - {money(T)} = {money(over)}')}.",
                   f"Commission: {m(f'{_pdec(r)} \\times {money(over)} = {money(c)}')}.",
                   f"Total pay: {m(f'{money(base)} + {money(c)} = {money(pay)}')}."],
            check=base + Fraction(int(S - T)) * Fraction(r, 100),
        )
    c = S * r / 100
    need(c.is_integer)
    pay = base + c
    stem = (f"{B} earns {money(base)} per {per} plus {_art_n(r)} {pct(r)} commission on {B.his} sales at {_art(job)} {job}. "
            f"How much must {B.he} sell in a {per} to earn a total of {money(pay)}?")
    return Problem(
        stem=stem, answer=S, fmt=money, section="AR",
        wrong=[(pay * 100 / r, "forgets to subtract the base pay first"),
               (c, "is the commission needed, not the sales needed"),
               (c * r / 100, "multiplies by the rate instead of dividing"),
               (S / 10, "slips the decimal point when dividing by the rate")],
        steps=[f"Commission needed: {m(f'{money(pay)} - {money(base)} = {money(c)}')}.",
               f"That commission is {pct(r)} of sales: {m(f'{_pdec(r)} \\times \\text{{sales}} = {money(c)}')}.",
               f"Divide: {m(f'{money(c)} \\div {_pdec(r)} = {money(S)}')}."],
        tip=f"Check: {m(f'{_pdec(r)} \\times {money(S)} = {money(c)}')}, and {m(f'{money(base)} + {money(c)} = {money(pay)}')}.",
        verify=lambda v: base + v * r / 100 == pay,
    )


# --------------------------------------------------------------------------
# 6. raise or pay cut (L1)
# --------------------------------------------------------------------------

@template("AR")
@_fill
def pay_raise(rng, lvl, part=None):
    v = _pick(rng, [0, 1, 2, 3, 4], part)
    up = True
    if v == 0:
        B = person(rng)
        w = Q(rng.choice(range(28, 49))) / 2
        p = rng.choice([2, 3, 4, 5, 6, 8, 10])
        stem_a = (f"{B} earns {money(w)} per hour at a grocery store. After {_art_n(p)} {pct(p)} raise, what is "
                  f"{B.his} new hourly wage?")
        what = "hourly wage"
    elif v == 1:
        B = person(rng)
        w = Q(rng.choice(range(30000, 70001, 500)))
        p = rng.choice([2, 3, 4, 5, 6])
        stem_a = (f"{B} earns a salary of {money(w)} a year. {B.He} gets {_art_n(p)} {pct(p)} raise. What is "
                  f"{B.his} new yearly salary?")
        what = "salary"
    elif v == 2:
        B = _trooper(rng)
        w = Q(rng.choice(range(2100, 4501, 50)))
        p = rng.choice([3, 4, R(9, 2), 5])
        stem_a = (f"{B}'s monthly base pay is {money(w)}. This year's military pay raise is {pct(p)}. What "
                  f"will {B.his} new monthly base pay be?")
        what = "monthly base pay"
    elif v == 3:
        B = _trooper(rng, ["Specialist", "Corporal", "Sergeant", "Airman First Class", "Petty Officer"])
        w = Q(rng.choice(range(2400, 4001, 50)))
        p = rng.choice([6, 8, 10, 12, 15])
        stem_a = (f"When {B} is promoted, {B.his} monthly base pay goes up {pct(p)}. Before the promotion it "
                  f"was {money(w)}. What is it after the promotion?")
        what = "monthly base pay"
    else:
        B = person(rng)
        w = Q(rng.choice(range(28, 49))) / 2
        p = rng.choice([5, 10, 15, 20])
        up = False
        stem_a = (f"Business is slow, so a restaurant cuts every server's hourly wage by {pct(p)}. {B} was "
                  f"earning {money(w)} per hour. What is {B.his} new hourly wage?")
        what = "hourly wage"
    ch = w * Q(p) / 100
    need(_ok_cents(ch))
    new = w + ch if up else w - ch
    word = "raise" if up else "cut"
    return Problem(
        stem=stem_a, answer=new, fmt=money, section="AR",
        wrong=[(ch, f"is the amount of the {word}, not the new {what}"),
               ((w + p) if up else (w - p), f"{'adds' if up else 'subtracts'} the percent as if it were dollars"),
               ((w + 10 * ch) if up else (w - 10 * ch), "moves the decimal point only one place"),
               ((w - ch) if up else (w + ch), f"{'subtracts' if up else 'adds'} the change instead of "
                                              f"{'adding' if up else 'subtracting'} it")],
        steps=[f"Find the {word}: {m(f'{_pdec(p)} \\times {money(w)} = {money(ch)}')}.",
               f"{'Add it to' if up else 'Subtract it from'} the old pay: "
               f"{m(f'{money(w)} {chr(43) if up else chr(45)} {money(ch)} = {money(new)}')}."],
        tip=(f"In one step: {m(f'{dec_raw(1 + Q(p) / 100) if up else dec_raw(1 - Q(p) / 100)} \\times {money(w)} = {money(new)}')}."),
        check=w * (100 + p if up else 100 - p) / 100,
    )


# --------------------------------------------------------------------------
# 7. working backward from a percent (L2, L3)
# --------------------------------------------------------------------------

_ITEMS = [("pair of boots", 60, 200), ("jacket", 40, 160), ("tent", 80, 300), ("microwave", 60, 160),
          ("pair of headphones", 40, 200), ("backpack", 40, 120), ("bicycle", 160, 480),
          ("coffee table", 80, 300), ("video game console", 200, 500)]


@template("AR")
@_fill
def reverse_percent(rng, lvl, part=None):
    B = person(rng)
    if lvl == 2:
        v = _pick(rng, [0, 1, 2, 3], part)
        if v == 0:
            item, lo, hi = rng.choice(_ITEMS)
            d = rng.choice([10, 20, 25, 30, 40, 50])
            O = Q(rng.choice(range(lo, hi + 1, 4)))
            S = O * (100 - d) / 100
            need(S.is_integer)
            stem = (f"{B} paid {money(S)} for {'an' if item[0] in 'aeiou' else 'a'} {item} that was on sale "
                    f"for {pct(d)} off. What was the original price?")
            keep = 100 - d
            wrong = [(S * (100 + d) / 100, f"adds {pct(d)} of the sale price, but the discount was {pct(d)} of "
                                           f"the original price"),
                     (S * 100 / d, f"divides by {m(_pdec(d))}, the discount, instead of {m(_pdec(keep))}, "
                                   f"the part paid"),
                     (S + d, "adds the percent as if it were dollars")]
            what, part = "the sale price", f"{pct(keep)} of the original"
            ans, base_word = O, "original price"
            mult = R(keep, 100)
        elif v == 1:
            item, lo, hi = rng.choice(_ITEMS)
            t = rng.choice([4, 5, 6, 8, 10])
            O = Q(rng.choice(range(lo, hi + 1, 5)))
            S = O * (100 + t) / 100
            need(_ok_cents(S))
            stem = (f"The total cost of {'an' if item[0] in 'aeiou' else 'a'} {item}, including {_art_n(t)} "
                    f"{pct(t)} sales tax, was {money(S)}. What was the price before tax?")
            wrong = [(S * (100 - t) / 100, f"subtracts {pct(t)} of the total, but the tax was {pct(t)} of the "
                                           f"price before tax"),
                     (S - t, "subtracts the percent as if it were dollars"),
                     (S * t / 100, "finds the tax on the total instead of removing it")]
            what, part = "the total", f"{pct(100 + t)} of the price"
            ans, base_word = O, "price before tax"
            mult = R(100 + t, 100)
        elif v == 2:
            T = _trooper(rng, ["Specialist", "Corporal", "Sergeant", "Petty Officer", "Airman First Class"])
            p = rng.choice([4, 5, 10, 12, 15, 20])
            O = Q(rng.choice(range(2400, 3801, 20)))
            S = O * (100 + p) / 100
            need(S.is_integer)
            stem = (f"After a promotion, {T}'s monthly base pay went up {pct(p)} to {money(S)}. What was "
                    f"{T.his} monthly base pay before the promotion?")
            wrong = [(S * (100 - p) / 100, f"takes {pct(p)} off the new pay, but the raise was {pct(p)} of the "
                                           f"old pay"),
                     (S - p, "subtracts the percent as if it were dollars"),
                     (S * p / 100, "finds {0} of the new pay instead of removing the raise".format(pct(p)))]
            what, part = "the new pay", f"{pct(100 + p)} of the old pay"
            ans, base_word = O, "old pay"
            mult = R(100 + p, 100)
        else:
            p = rng.choice([20, 25, 50])
            O = Q(rng.choice(range(16, 81, 4)))
            S = O * (100 + p) / 100
            need(S.is_integer)
            ctx = rng.choice([("A recruiting station enlisted {S} recruits this month, which is {p} more than "
                               "last month. How many recruits did it enlist last month?", "recruits"),
                              ("A unit's blood drive collected {S} pints this year, {p} more than last year. "
                               "How many pints did it collect last year?", "pints"),
                              ("A gym had {S} new members in March, {p} more than in February. How many new "
                               "members did it have in February?", "members")])
            stem = ctx[0].format(S=num(S), p=pct(p))
            wrong = [(S * (100 - p) / 100, f"takes {pct(p)} off this year's number, but the increase was "
                                           f"{pct(p)} of the earlier number"),
                     (S - p, "subtracts the percent as if it were a count"),
                     (S * p / 100, f"is {pct(p)} of the new number")]
            what, part = "the new number", f"{pct(100 + p)} of the old number"
            ans, base_word = O, "old number"
            mult = R(100 + p, 100)
            f = num
            return Problem(
                stem=stem, answer=ans, fmt=f, section="AR",
                wrong=[(w, y) for w, y in wrong if Q(w).is_integer],
                steps=[f"The new number is {part}: {m(f'{dec_raw(mult)} \\times \\text{{old}} = {int_raw(S)}')}.",
                       f"Divide: {m(f'{int_raw(S)} \\div {dec_raw(mult)} = {int_raw(O)}')}."],
                tip=f"Check: {pct(p)} of {num(O)} is {num(O * p / 100)}, and {m(f'{int_raw(O)} + {int_raw(O * p / 100)} = {int_raw(S)}')}.",
                verify=lambda v: v * mult == S,
                near=lambda g: [O + k for k in g.sample([-4, -3, -2, -1, 1, 2, 3, 4, 5, 6], 8)],
            )
        frac = mult
        return Problem(
            stem=stem, answer=ans, fmt=money, section="AR", wrong=wrong,
            steps=[f"{_cap(what)} is {part}: {m(f'{dec_raw(mult)} \\times \\text{{{base_word}}} = {money(S)}')}.",
                   f"Divide: {m(f'{money(S)} \\div {dec_raw(mult)} = {money(ans)}')}."],
            tip=(f"Dividing by {m(dec_raw(mult))} is the same as multiplying by {m(F(frac.q, frac.p))}: "
                 f"{m(f'{money(S)} \\times {F(frac.q, frac.p)} = {money(ans)}')}." if frac.p < 10 else
                 f"Check: {m(f'{dec_raw(mult)} \\times {money(ans)} = {money(S)}')}."),
            verify=lambda v: v * mult == S,
        )
    # level 3: discount and tax removed in turn
    item, lo, hi = _pick(rng, _ITEMS, part)
    d = rng.choice([10, 20, 25, 40, 50])
    t = rng.choice([4, 5, 6, 8])
    O = Q(rng.choice(range(lo, hi + 1, 10)))
    sale = O * (100 - d) / 100
    T = sale * (100 + t) / 100
    need(sale.is_integer and _ok_cents(T))
    stem = (f"{B} bought {'an' if item[0] in 'aeiou' else 'a'} {item} on sale for {pct(d)} off. With "
            f"{_art_n(t)} {pct(t)} sales tax added to the sale price, {B.he} paid {money(T)}. What was the "
            f"original price of the {item}?")
    wrong = [(sale, "is the sale price, not the original price"),
             (T * 100 / (100 - d), "forgets to remove the sales tax"),
             (T * (100 + d) * (100 - t) / 10000, "adds the discount and subtracts the tax as percents of the amount paid"),
             (T * 100 / (100 - d + t), f"combines the two percents into one {pct(d - t)} discount")]
    return Problem(
        stem=stem, answer=O, fmt=money, section="AR", wrong=wrong,
        steps=[f"Remove the tax first. The amount paid is {pct(100 + t)} of the sale price: "
               f"{m(f'{money(T)} \\div {dec_raw(R(100 + t, 100))} = {money(sale)}')}.",
               f"The sale price is {pct(100 - d)} of the original: "
               f"{m(f'{money(sale)} \\div {_pdec(100 - d)} = {money(O)}')}."],
        tip=f"Check: {m(f'{money(O)} \\times {_pdec(100 - d)} = {money(sale)}')}, and {m(f'{money(sale)} \\times {dec_raw(R(100 + t, 100))} = {money(T)}')}.",
        verify=lambda v: v * (100 - d) * (100 + t) / 10000 == T,
    )


# --------------------------------------------------------------------------
# 8. markup and profit
# --------------------------------------------------------------------------

_MARKUP = [
    # (stem start, item, plural, cost lo, hi, cost step (cents), markups, military)
    ("A bike shop buys bicycles for {C} each", "bicycle", "bicycles", 12000, 40000, 1000, [20, 25, 30, 40, 50], False),
    ("A clothing store pays {C} for each pair of jeans", "pair of jeans", "pairs of jeans", 1200, 3000, 100,
     [40, 50, 60, 75, 80, 100], False),
    ("A food truck spends {C} to make each burrito", "burrito", "burritos", 160, 320, 20, [50, 75, 100, 150], False),
    ("A vendor at the base's Fourth of July fair buys T-shirts for {C} each", "T-shirt", "T-shirts", 400, 900,
     50, [50, 60, 80, 100], True),
    ("A furniture store buys a sofa from the maker for {C}", "sofa", "sofas", 30000, 80000, 2000,
     [30, 40, 50, 60], False),
    ("The snack bar at the base bowling alley pays {C} for each slice of pizza it sells", "slice of pizza",
     "slices of pizza", 80, 160, 10, [50, 75, 100, 150], True),
    ("A hardware store buys hammers from a supplier for {C} each", "hammer", "hammers", 800, 1500, 50,
     [40, 50, 60, 75], False),
    ("A used-car dealer pays {C} for a pickup truck", "truck", "trucks", 800000, 2000000, 50000,
     [10, 15, 20, 25], False),
    ("An online seller buys phone cases for {C} each", "phone case", "phone cases", 200, 600, 25,
     [100, 150, 200], False),
    ("A military surplus store buys used rucksacks for {C} each", "rucksack", "rucksacks", 1500, 4000, 100,
     [50, 60, 75, 100], True),
]


@template("AR")
@_fill
def markup(rng, lvl, part=None):
    st, item, items, lo, hi, step, mks, mil = _pick(rng, _MARKUP, part)
    C = R(rng.choice(range(lo, hi + 1, step)), 100)
    mk = rng.choice(mks)
    up = C * mk / 100
    price = C + up
    need(_ok_cents(up))
    if lvl == 2:
        one = "the" if item in ("sofa", "truck") else "each"
        stem = (st.format(C=money(C)) + f" and marks up the cost by {pct(mk)}. "
                + choose(rng, f"What is the selling price of {one} {item}?",
                         f"What price is put on {one} {item}?",
                         f"How much does a customer pay for {one} {item}?"))
        return Problem(
            stem=stem, answer=price, fmt=money, section="AR",
            wrong=[(up, "is the markup, not the selling price"),
                   (C - up if C > up else C + 2 * up, "subtracts the markup instead of adding it" if C > up else None),
                   (C + mk, "adds the percent as if it were dollars"),
                   (C + up / 10, "moves the decimal point one place too far when finding the markup")],
            steps=[f"Markup: {m(f'{_pdec(mk)} \\times {money(C)} = {money(up)}')}.",
                   f"Selling price: {m(f'{money(C)} + {money(up)} = {money(price)}')}."],
            tip=f"In one step: {m(f'{dec_raw(1 + Q(mk) / 100)} \\times {money(C)} = {money(price)}')}.",
            check=C * (100 + mk) / 100,
        )
    d = rng.choice([10, 20, 25, 30])
    need(d < mk)
    sale = price * (100 - d) / 100
    need(_ok_cents(sale))
    profit = sale - C
    need(profit > 0)
    seller = ("the dealer" if "dealer" in st else "the seller" if "seller" in st
              else "the owner" if "food truck" in st or "vendor" in st.lower()
              else "the snack bar" if "snack bar" in st else "the store")
    if rng.random() < 0.4:
        stem = (st.format(C=money(C)) + f" and marks up the cost by {pct(mk)}. Later, the {item} goes on sale "
                f"for {pct(d)} off the marked price. What is the sale price?")
        return Problem(
            stem=stem, answer=sale, fmt=money, section="AR",
            wrong=[(price, "is the marked price; it forgets the sale"),
                   (C * (100 + mk - d) / 100, f"combines {pct(mk)} up and {pct(d)} off into one {pct(mk - d)} markup"),
                   (C * (100 - d) / 100, "takes the discount off the cost instead of the marked price"),
                   (profit, "is the profit, not the sale price")],
            steps=[f"Marked price: {m(f'{money(C)} + {_pdec(mk)} \\times {money(C)} = {money(C)} + {money(up)} = {money(price)}')}.",
                   f"Take {pct(d)} off the \\emph{{marked}} price: {m(f'{money(price)} - {_pdec(d)} \\times {money(price)} = {money(price)} - {money(price * d / 100)} = {money(sale)}')}."],
            tip=f"In one line: {m(f'{money(C)} \\times {dec_raw(1 + Q(mk) / 100)} \\times {_pdec(100 - d)} = {money(sale)}')}.",
            check=C * (100 + mk) * (100 - d) / 10000,
        )
    stem = (st.format(C=money(C)) + f" and marks up the cost by {pct(mk)}. Later, the {item} goes on sale "
            f"for {pct(d)} off the marked price. How much profit does {seller} make on each {item} sold at the "
            f"sale price?")
    stem = stem.replace("each sofa sold", "the sofa if it is sold").replace("each truck sold", "the truck if it is sold")
    return Problem(
        stem=stem, answer=profit, fmt=money, section="AR",
        wrong=[(C * (mk - d) / 100, f"combines {pct(mk)} up and {pct(d)} off into one {pct(mk - d)} markup"),
               (up, "is the original markup; it forgets the sale"),
               (sale, "is the sale price, not the profit"),
               (price * d / 100, "is the discount, not the profit")],
        steps=[f"Marked price: {m(f'{money(C)} + {_pdec(mk)} \\times {money(C)} = {money(C)} + {money(up)} = {money(price)}')}.",
               f"Sale price: {m(f'{money(price)} - {_pdec(d)} \\times {money(price)} = {money(price)} - {money(price * d / 100)} = {money(sale)}')}.",
               f"Profit: {m(f'{money(sale)} - {money(C)} = {money(profit)}')}."],
        check=C * ((100 + mk) * (100 - d) - 10000) / 10000,
    )


# --------------------------------------------------------------------------
# 9. successive discounts
# --------------------------------------------------------------------------

_SUCC = [
    # stem with {X} = item phrase (with its price at level 2), item, price lo, hi, step
    ("During a clearance sale, a sporting-goods store marks {X} down {d1}. At the register, customers "
     "get an additional {d2} off the sale price.", "tent", 100, 400, 10),
    ("An outlet store marks {X} down {d1}. On Saturday it takes another {d2} off the reduced "
     "price.", "pair of boots", 80, 200, 10),
    ("A furniture store discounts {X} by {d1}. A coupon gives {d2} off the discounted price.",
     "recliner", 300, 900, 20),
    ("The base exchange marks {X} down {d1} for a holiday sale and then takes an extra {d2} off the sale "
     "price on the last day.", "TV", 300, 900, 20),
    ("An online store lists {X} at {d1} off. Members get another {d2} off the sale price at "
     "checkout.", "laptop", 400, 1200, 20),
    ("A tire shop takes {d1} off {X} and then gives veterans an additional {d2} off the "
     "sale price.", "set of four tires", 400, 900, 20),
    ("A shoe store marks {X} down {d1}. A week later it cuts the new price by another "
     "{d2}.", "pair of running shoes", 60, 160, 10),
    ("A hardware store takes {d1} off {X}, and a rewards card takes {d2} off the sale price.",
     "power drill", 80, 240, 10),
    ("A car dealer lowers the price of {X} by {d1}. When the car does not sell, the dealer cuts the "
     "new price by another {d2}.", "used car", 8000, 20000, 500),
    ("A store takes {d1} off {X}. Service members get an extra {d2} military discount on the sale "
     "price.", "winter coat", 80, 240, 10),
]

_SUCC_Q = [" The two discounts together are the same as a single discount of what percent?",
           " What single percent discount gives the same final price?",
           " By what percent, in all, has the original price been reduced?"]


@template("AR")
@_fill
def successive(rng, lvl, part=None):
    st, item, lo, hi, step = _pick(rng, _SUCC, part)
    d1 = rng.choice([10, 20, 25, 30, 40, 50])
    d2 = rng.choice([10, 15, 20, 25, 5, 30] if lvl == 3 else [10, 15, 20, 25])
    keep = R((100 - d1) * (100 - d2), 10000)
    eq = 100 - keep * 100
    if lvl == 2:
        P = Q(rng.choice(range(lo, hi + 1, step)))
        s1 = P * (100 - d1) / 100
        s2 = s1 * (100 - d2) / 100
        need(_ok_cents(s1) and _ok_cents(s2))
        X = f"{_art_n(P)} {money(P)} {item}"
        stem = (st.format(X=X, d1=pct(d1), d2=pct(d2))
                + choose(rng, f" What is the final price of the {item}?",
                         f" What is the price after both discounts?"))
        return Problem(
            stem=stem, answer=s2, fmt=money, section="AR",
            wrong=[(P * (100 - d1 - d2) / 100, f"adds the discounts to get {pct(d1 + d2)} off"),
                   (s1, "stops after the first discount"),
                   (P * (100 - d2) / 100, "applies only the second discount"),
                   (P * d1 * d2 / 10000, "multiplies the two discounts together")],
            steps=[f"First discount: {m(f'{money(P)} - {_pdec(d1)} \\times {money(P)} = {money(P)} - {money(P * d1 / 100)} = {money(s1)}')}.",
                   f"The second discount is taken from the \\emph{{new}} price: "
                   f"{m(f'{money(s1)} - {_pdec(d2)} \\times {money(s1)} = {money(s1)} - {money(s1 * d2 / 100)} = {money(s2)}')}."],
            tip=f"In one line: {m(f'{money(P)} \\times {_pdec(100 - d1)} \\times {_pdec(100 - d2)} = {money(s2)}')}.",
            check=P * keep,
        )
    need(eq.is_integer or (eq * 2).is_integer)
    X = f"{'an' if item[0] in 'aeiou' else 'a'} {item}"
    stem = st.format(X=X, d1=pct(d1), d2=pct(d2)) + rng.choice(_SUCC_Q)
    return Problem(
        stem=stem, answer=eq, fmt=pct, section="AR",
        wrong=[(Q(d1 + d2), "adds the two discounts, but the second is taken from a smaller price"),
               (keep * 100, "is the percent of the price you still pay, not the discount"),
               (R(d1 * d2, 100), "multiplies the two percents")],
        steps=[f"After {pct(d1)} off you pay {pct(100 - d1)} of the price, and after another {pct(d2)} off you "
               f"pay {pct(100 - d2)} of \\emph{{that}}.",
               f"Multiply: {m(f'{_pdec(100 - d1)} \\times {_pdec(100 - d2)} = {dec_raw(keep)}')}, so you pay "
               f"{pct(keep * 100)} of the original price.",
               f"The single discount is {m(f'100\\% - {dec_raw(keep * 100)}\\% = {dec_raw(eq)}\\%')}."],
        tip=f"Test it on \\$100: {pct(d1)} off gives {money(100 - d1)}, and {pct(d2)} off that gives {money(keep * 100)}, which is {money(eq)} off.",
        check=Fraction(100) - Fraction(100 - d1) * Fraction(100 - d2) / 100,
    )


# --------------------------------------------------------------------------
# 10. tip and tax on a meal (L2)
# --------------------------------------------------------------------------

@template("AR")
@_fill
def tip_tax(rng, lvl, part=None):
    t = rng.choice([5, 6, 7, 8])
    p = rng.choice([15, 18, 20])
    v = rng.randrange(4)
    if v == 0:
        B = person(rng)
        M = Q(rng.choice(range(30, 121, 2)))
        stem = (f"{B}'s dinner bill is {money(M)} before tax. The sales tax is {pct(t)}, and {B.he} leaves "
                f"{_art_n(p)} {pct(p)} tip on the {money(M)} (before tax). What is the total cost?")
    elif v == 1:
        T = _trooper(rng, ["Sergeant", "Staff Sergeant", "Petty Officer"])
        M = Q(rng.choice(range(80, 201, 4)))
        stem = (f"After a promotion ceremony, {T} takes {T.his} team out to lunch. The food costs "
                f"{money(M)}. There is {_art_n(t)} {pct(t)} sales tax, and {T.he} adds {_art_n(p)} {pct(p)} tip "
                f"figured on the food cost before tax. How much does {T.he} pay in all?")
    elif v == 2:
        B = person(rng)
        M = Q(rng.choice(range(20, 61, 2)))
        stem = (f"{B} orders food for delivery. The food costs {money(M)}, the sales tax is {pct(t)} of the "
                f"food cost, and {B.he} tips the driver {pct(p)} of the food cost. What is the total?")
    else:
        M = Q(rng.choice(range(40, 141, 4)))
        stem = (f"On a weekend pass, a group of airmen order a meal that costs {money(M)}. They pay "
                f"{_art_n(t)} {pct(t)} sales tax and leave {_art_n(p)} {pct(p)} tip, both figured on the "
                f"{money(M)}. What is the total cost?")
    tax = M * t / 100
    tip = M * p / 100
    total = M + tax + tip
    need(_ok_cents(tax) and _ok_cents(tip))
    w = [(M + tax, "forgets the tip"), (M + tip, "forgets the tax"), (tax + tip, "is just the tax and the tip")]
    both = M * (100 + t) * (100 + p) / 10000
    if _ok_cents(both) and both != total:
        w.append((both, "figures the tip on the total with tax, but the tip is on the food cost only"))
    return Problem(
        stem=stem, answer=total, fmt=money, section="AR", wrong=w,
        steps=[f"Tax: {m(f'{_pdec(t)} \\times {money(M)} = {money(tax)}')}.",
               f"Tip: {m(f'{_pdec(p)} \\times {money(M)} = {money(tip)}')}.",
               f"Total: {m(f'{money(M)} + {money(tax)} + {money(tip)} = {money(total)}')}."],
        tip=(f"Both percents are of the same amount, so add them first: {m(f'{t}\\% + {p}\\% = {t + p}\\%')}, "
             f"and {m(f'{dec_raw(1 + Q(t + p) / 100)} \\times {money(M)} = {money(total)}')}."),
        check=M * (100 + t + p) / 100,
    )


# --------------------------------------------------------------------------
# 11. percent of a goal
# --------------------------------------------------------------------------

_GOAL = [
    # (stem L1, stem L2 (how much more), stem L2b (find goal), unit fmt, G lo, hi, step, military)
    ("A battalion's goal for its charity drive is {G}. So far it has raised {X}. What percent of the goal "
     "has it reached?",
     "A battalion's goal for its charity drive is {G}. It has reached {p} of the goal. How much more money "
     "does it need to raise?",
     "After raising {X}, a battalion has reached {p} of the goal for its charity drive. What is the goal?",
     "money", 2000, 12000, 500, True),
    ("A recruiting station's goal is {G} enlistments this quarter. So far it has signed {X} recruits. What "
     "percent of its goal has it met?",
     "A recruiting station's goal is {G} enlistments this quarter. It has met {p} of the goal. How many "
     "more enlistments does it need?",
     "A recruiting station has signed {X} recruits, which is {p} of its goal for the quarter. What is its "
     "goal?", "count", 40, 200, 20, True),
    ("{B} wants to run {G} miles this month to get ready for a PT test. So far {he} has run {X} miles. "
     "What percent of {his} goal has {he} completed?",
     "{B} wants to run {G} miles this month to get ready for a PT test. {He} has completed {p} of that "
     "distance. How many more miles must {he} run?",
     "{B} has run {X} miles, which is {p} of {his} goal for the month. What is {his} goal?",
     "miles", 40, 120, 10, True),
    ("A school band is raising {G} for a trip. So far it has raised {X}. What percent of its goal has it "
     "raised?",
     "A school band is raising {G} for a trip. It has raised {p} of the money. How much more does it need?",
     "A school band has raised {X} for a trip, which is {p} of its goal. What is the goal?",
     "money", 1000, 8000, 250, False),
    ("{B} is saving {G} for a used car. {He} has saved {X} so far. What percent of {his} goal has {he} "
     "saved?",
     "{B} is saving {G} for a used car and has saved {p} of it. How much more does {he} need?",
     "{B} has saved {X} for a used car, which is {p} of {his} goal. How much does the car cost?",
     "money", 2000, 9000, 250, False),
]


@template("AR")
@_fill
def percent_goal(rng, lvl, part=None):
    s1, s2, s3, kind, lo, hi, step, mil = _pick(rng, _GOAL, part)
    B = _trooper(rng) if mil else person(rng)
    G = Q(rng.choice(range(lo, hi + 1, step)))
    p = rng.choice([20, 25, 30, 40, 45, 55, 60, 65, 70, 75, 80, 85, 90])
    X = G * p / 100
    need(X.is_integer)
    fm = money if kind == "money" else (num if kind == "count" else unit(num, "mile"))
    show = money if kind == "money" else num
    raw = money if kind == "money" else int_raw          # inside math mode
    kw = dict(B=B, he=B.he, He=B.He, his=B.his, G=show(G), X=show(X), p=pct(p))
    if lvl == 1:
        return Problem(
            stem=s1.format(**kw), answer=Q(p), fmt=pct, section="AR",
            wrong=[(G * 100 / X, "divides the goal by the amount done instead of the amount done by the goal"),
                   (Q(100 - p), "is the percent still to go, not the percent done"),
                   (R(p, 100), "forgets to multiply by 100")],
            steps=[f"Write the part done over the goal: {m(F(int_raw(X), int_raw(G)))}.",
                   f"Divide and change to a percent: {m(f'{int_raw(X)} \\div {int_raw(G)} = {dec_raw(R(p, 100))} = {p}\\%')}."],
            check=X * 100 / G,
        )
    if rng.random() < 0.5:
        left = G - X
        return Problem(
            stem=s2.format(**kw), answer=left, fmt=fm, section="AR",
            wrong=[(X, "is the amount already done, not the amount still needed"),
                   (G - p, "subtracts the percent as if it were an amount"),
                   (G * p / 1000 if (G * p / 1000).is_integer else G - X / 2, None)],
            steps=[f"Amount done: {m(f'{_pdec(p)} \\times {raw(G)} = {raw(X)}')}.",
                   f"Amount still needed: {m(f'{raw(G)} - {raw(X)} = {raw(left)}')}."],
            tip=f"Or: {m(f'100\\% - {p}\\% = {100 - p}\\%')} is left, and {m(f'{_pdec(100 - p)} \\times {raw(G)} = {raw(left)}')}.",
            check=G * (100 - p) / 100,
            near=(None if kind == "money" else (lambda g: [left + k for k in g.sample([-6, -4, -2, 2, 4, 6, 8], 6)
                                                            if left + k > 0])),
        )
    return Problem(
        stem=s3.format(**kw), answer=G, fmt=fm, section="AR",
        wrong=[(X * (100 + (100 - p)) / 100, f"adds {pct(100 - p)} of {show(X)} instead of dividing"),
               (X * p / 100, f"finds {pct(p)} of {show(X)} instead of dividing"),
               (X + (100 - p), "adds the missing percent as if it were an amount")],
        steps=[f"{show(X)} is {pct(p)} of the goal: {m(f'{_pdec(p)} \\times \\text{{goal}} = {raw(X)}')}.",
               f"Divide: {m(f'{raw(X)} \\div {_pdec(p)} = {raw(G)}')}."],
        tip=f"Check: {pct(p)} of {show(G)} is {show(X)}.",
        verify=lambda v: v * p / 100 == X,
        near=(None if kind == "money" else (lambda g: [G + k for k in g.sample([-8, -4, -2, 2, 4, 8, 10], 6)])),
    )


# --------------------------------------------------------------------------
# 12. compound interest, two periods (L3)
# --------------------------------------------------------------------------

@template("AR")
@_fill
def compound(rng, lvl, part=None):
    mil = rng.random() < 0.4
    B = _trooper(rng) if mil else person(rng)
    semi = (rng.random() < 0.35) if part is None else part[0] == 1
    if semi:
        r = rng.choice([4, 6, 8, 10])
        P = Q(rng.choice(range(1000, 10001, 500)))
        i = Q(r) / 2
        what = (f"pays {pct(r)} yearly interest, compounded every six months (so {pct(i)} is added every "
                f"six months)")
        span = "1 year"
    else:
        r = rng.choice([2, 3, 4, 5, 6, 8, 10])
        P = Q(rng.choice(range(1000, 10001, 500)))
        i = Q(r)
        what = f"pays {pct(r)} interest per year, compounded once a year"
        span = "2 years"
    a1 = P * (100 + i) / 100
    a2 = a1 * (100 + i) / 100
    need(_ok_cents(a2))
    ask_int = rng.random() < 0.4
    src = (f"{_art_n(P)} {money(P)} reenlistment bonus" if mil else money(P))
    stem = (f"{B} deposits {src} in an account that {what}. "
            + (f"How much interest will the account earn in {span}?" if ask_int
               else f"How much will be in the account after {span}?"))
    I = a2 - P
    ans = I if ask_int else a2
    simple = P * (100 + 2 * i) / 100
    wrong = [((simple - P) if ask_int else simple,
              "uses simple interest; it leaves out the interest earned on the first interest"),
             ((a1 - P) if ask_int else a1, "stops after the first period"),
             (a2 if ask_int else I, "is the balance, not the interest" if ask_int else "is the interest only, not the balance")]
    if semi:
        full = P * (100 + r) ** 2 / 10000
        wrong.append(((full - P) if ask_int else full, f"adds the full {pct(r)} every six months instead of {pct(i)}"))
    steps = [f"Rate for each period: {pct(i)} {'(half of the yearly rate)' if semi else ''}".rstrip() + ".",
             f"After the first {'six months' if semi else 'year'}: {m(f'{money(P)} + {_pdec(i)} \\times {money(P)} = {money(P)} + {money(a1 - P)} = {money(a1)}')}.",
             f"After the second: {m(f'{money(a1)} + {_pdec(i)} \\times {money(a1)} = {money(a1)} + {money(a2 - a1)} = {money(a2)}')}."]
    if ask_int:
        steps.append(f"Interest earned: {m(f'{money(a2)} - {money(P)} = {money(I)}')}.")
    return Problem(
        stem=stem, answer=ans, fmt=money, section="AR", wrong=wrong, steps=steps,
        tip=f"The second {'period' if semi else 'year'} earns more ({money(a2 - a1)} vs. {money(a1 - P)}) because it earns interest on the interest.",
        check=(Fraction(int(P)) * (1 + Fraction(i.p, i.q * 100)) ** 2) - (Fraction(int(P)) if ask_int else 0),
    )


# --------------------------------------------------------------------------

PLAN = [
    # level 1 (10)
    *[(v, 1, 1) for v in _variants(simple_interest, 3)],
    *[(v, 1, 1) for v in _variants(commission, 2)],
    *[(v, 1, 1) for v in _variants(pay_raise, 3)],
    *[(v, 1, 1) for v in _variants(percent_goal, 2)],
    # level 2 (14)
    *[(v, 2, 1) for v in _variants(simple_interest, 2)],
    *[(v, 2, 1) for v in _variants(interest_balance, 2)],
    *[(v, 2, 1) for v in _variants(commission, 2)],
    *[(v, 2, 1) for v in _variants(reverse_percent, 2)],
    *[(v, 2, 1) for v in _variants(markup, 2)],
    *[(v, 2, 1) for v in _variants(successive, 2)],
    (tip_tax, 2, 1),
    (percent_goal, 2, 1),
    # level 3 (11)
    *[(v, 3, 1) for v in _variants(find_rate_time, 2)],
    *[(v, 3, 1) for v in _variants(commission, 2)],
    *[(v, 3, 1) for v in _variants(reverse_percent, 2)],
    (successive, 3, 1),
    (markup, 3, 1),
    *[(v, 3, 1) for v in _variants(compound, 2)],
    (loan_payment, 3, 1),
]
