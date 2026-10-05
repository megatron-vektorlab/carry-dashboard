"""'Who did it?' statement puzzles (truth-tellers and liars).

Suspects each make one statement. Exactly one suspect is the culprit. A rule
says how many statements are true (e.g. "exactly one statement is true", or
"only the culprit lies"). The reader tests each suspect as the culprit and
counts true statements; exactly one case fits.

Statements (about the culprit c, or about another statement):
    ("is", X)        "X did it."
    ("not", X)       "X didn't do it."            (self: "I didn't do it.")
    ("or", X, Y)     "It was X or Y."
    ("nor", X, Y)    "Neither X nor Y did it."
    ("lies", j)      "<suspect j> is lying."
    ("truth", j)     "<suspect j> is telling the truth."
"""
from __future__ import annotations

import itertools
import random
from dataclasses import dataclass


@dataclass
class LiarPuzzle:
    names: list
    statements: list           # one per suspect
    rule: tuple                # ("exactly", m) or ("culprit_lies",)
    culprit: int
    truth: tuple               # truth value of each statement in the solution


def _direct(st, c):
    k = st[0]
    if k == "is":
        return c == st[1]
    if k == "not":
        return c != st[1]
    if k == "or":
        return c in (st[1], st[2])
    if k == "nor":
        return c not in (st[1], st[2])
    return None


def evaluations(statements, c):
    """All consistent truth assignments for culprit c (referential statements may branch)."""
    n = len(statements)
    out = []
    for bits in itertools.product((False, True), repeat=n):
        ok = True
        for i, st in enumerate(statements):
            d = _direct(st, c)
            if d is None:
                j = st[1]
                d = (not bits[j]) if st[0] == "lies" else bits[j]
            if d != bits[i]:
                ok = False
                break
        if ok:
            out.append(bits)
    return out


def rule_ok(rule, bits, c):
    if rule[0] == "exactly":
        return sum(bits) == rule[1]
    if rule[0] == "culprit_lies":
        return all((not b) if i == c else b for i, b in enumerate(bits))
    raise ValueError(rule)


def solutions(statements, rule):
    sols = []
    for c in range(len(statements)):
        for bits in evaluations(statements, c):
            if rule_ok(rule, bits, c):
                sols.append((c, bits))
    return sols


def random_statement(rng, i, n, allow_ref):
    others = [x for x in range(n) if x != i]
    kinds = ["is", "not", "not_self", "or", "nor"] + (["lies", "truth"] if allow_ref else [])
    k = rng.choice(kinds)
    if k == "is":
        return ("is", rng.choice(range(n)))
    if k == "not":
        return ("not", rng.choice(others))
    if k == "not_self":
        return ("not", i)
    if k in ("or", "nor"):
        x, y = rng.sample(range(n), 2)
        return (k, min(x, y), max(x, y))
    return (k, rng.choice(others))


def generate_liars(names, rng: random.Random, rule_kind="exactly", allow_ref=False, tries=5000):
    n = len(names)
    for _ in range(tries):
        sts = [random_statement(rng, i, n, allow_ref) for i in range(n)]
        if len(set(sts)) < n:
            continue
        if rule_kind == "exactly":
            m = rng.choice(range(1, n))
            rule = ("exactly", m)
        else:
            rule = ("culprit_lies",)
        sols = solutions(sts, rule)
        if len(sols) != 1:
            continue
        c, bits = sols[0]
        # every case must be settled by simple counting: exactly one consistent
        # assignment per culprit keeps the explanation table clean
        if any(len(evaluations(sts, x)) != 1 for x in range(n)):
            continue
        return LiarPuzzle(list(names), sts, rule, c, bits)
    raise RuntimeError("no liar puzzle found")


def statement_text(p: LiarPuzzle, i):
    st = p.statements[i]
    N = p.names
    k = st[0]
    if k == "is":
        return "I did it." if st[1] == i else f"{N[st[1]]} did it."
    if k == "not":
        return "I didn't do it." if st[1] == i else f"{N[st[1]]} didn't do it."
    if k == "or":
        x, y = st[1], st[2]
        nx = "me" if x == i else N[x]
        ny = "me" if y == i else N[y]
        return f"It was {nx} or {ny}."
    if k == "nor":
        x, y = st[1], st[2]
        if i in (x, y):
            o = y if x == i else x
            return f"Neither {N[o]} nor I did it."
        return f"Neither {N[x]} nor {N[y]} did it."
    if k == "lies":
        return f"{N[st[1]]} is lying."
    if k == "truth":
        return f"{N[st[1]]} is telling the truth."
    raise ValueError(k)


def rule_text(p: LiarPuzzle):
    if p.rule[0] == "exactly":
        m = p.rule[1]
        words = {1: "one", 2: "two", 3: "three", 4: "four"}[m]
        return f"Exactly {words} of these statements {'is' if m == 1 else 'are'} true."
    return "The culprit is lying. Everyone else is telling the truth."


def case_table(p: LiarPuzzle):
    """Rows: (suspect tested, truth values of statements, fits rule?)."""
    rows = []
    for c in range(len(p.names)):
        (bits,) = evaluations(p.statements, c)
        rows.append((c, bits, rule_ok(p.rule, bits, c)))
    return rows
