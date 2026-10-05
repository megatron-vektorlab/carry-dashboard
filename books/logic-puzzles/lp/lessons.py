"""Worked examples for the six lessons, with grid snapshots.

    .venv/bin/python -m lp.lessons          # writes data/lessons/L1..L6.json and prints the traces

Each example is a small puzzle with hand-written clues (checked for a unique
solution) or, for Lesson 6, a generated puzzle that needs one Suppose.
Lesson text (content/lessons.md) refers to snapshots by step number.
"""
from __future__ import annotations

import json
import os
import random

from .engine import Clue, Deducer, Spec, count_solutions, generate
from .explain import trace
from .liars import case_table, generate_liars, rule_text, statement_text
from .make import trial_chain
from .text import Bound

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "lessons")

PIE = {"label": "Pie", "values": ["apple", "cherry", "peach"],
       "ref": "the {v} pie's baker", "pred": "brought the {v} pie", "neg": "did not bring the {v} pie",
       "either": "brought either the {a} or the {b} pie", "nor": "brought neither the {a} nor the {b} pie",
       "short": "the {v} pie"}
JAM = {"label": "Jam", "values": ["plum", "fig", "quince"],
       "ref": "the {v} jam's maker", "pred": "made the {v} jam", "neg": "did not make the {v} jam",
       "either": "made either the {a} or the {b} jam", "nor": "made neither the {a} nor the {b} jam",
       "short": "the {v} jam"}
JAR = {"label": "Jar", "values": ["crock", "mason jar", "tin"],
       "ref": "whoever used the {v}", "pred": "used the {v}", "neg": "did not use the {v}",
       "either": "used either the {a} or the {b}", "nor": "used neither the {a} nor the {b}",
       "short": "the {v}"}
PLACE = {"label": "Place", "ordered": True, "nums": [1, 2, 3, 4], "labels": ["first", "second", "third", "fourth"],
         "ref": "the {x} person in line", "pred": "was {x} in line", "neg": "was not {x} in line",
         "either": "was either {a} or {b} in line", "nor": "was neither {a} nor {b} in line", "short": "{x}",
         "more": "stood somewhere behind {y}", "less": "stood somewhere ahead of {y}",
         "dmore": "stood exactly {d} behind {y}", "dless": "stood exactly {d} ahead of {y}",
         "dmore1": "stood right behind {y}", "dless1": "stood right in front of {y}", "dunit": ["place", "places"],
         "adj": "stood right next to {y}", "nadj": "did not stand next to {y}", "ends": "stood at one end of the line"}
AGE = {"label": "Age", "ordered": True, "nums": [60, 65, 70],
       "ref": "the {x}-year-old", "pred": "is {x}", "neg": "is not {x}", "short": "{x}",
       "either": "is either {a} or {b}", "nor": "is neither {a} nor {b}",
       "more": "is older than {y}", "less": "is younger than {y}",
       "dmore": "is exactly {d} older than {y}", "dless": "is exactly {d} younger than {y}", "dunit": ["year", "years"]}
BOAT = {"label": "Boat", "values": ["dory", "skiff", "sloop"],
        "ref": "the {v}'s owner", "pred": "owns the {v}", "neg": "does not own the {v}",
        "either": "owns either the {a} or the {b}", "nor": "owns neither the {a} nor the {b}", "short": "the {v}"}
TIME4 = {"label": "Time", "ordered": True, "nums": [9, 10, 11, 12], "labels": ["9 a.m.", "10 a.m.", "11 a.m.", "noon"],
         "ref": "the {x} visitor", "pred": "came at {x}", "neg": "did not come at {x}", "short": "{x}",
         "either": "came at either {a} or {b}", "nor": "came at neither {a} nor {b}",
         "more": "came later than {y}", "less": "came earlier than {y}",
         "dmore": "came exactly {d} after {y}", "dless": "came exactly {d} before {y}",
         "dmore1": "came one hour after {y}", "dless1": "came one hour before {y}", "dunit": ["hour", "hours"]}
BOOK = {"label": "Book", "values": ["atlas", "cookbook", "diary", "almanac"],
        "ref": "the {v} borrower", "pred": "borrowed the {v}", "neg": "did not borrow the {v}",
        "either": "borrowed either the {a} or the {b}", "nor": "borrowed neither the {a} nor the {b}",
        "short": "the {v}"}


def theme(title, names, cats, entity=("neighbor", "neighbors")):
    return {"title": title, "story": "", "entity": list(entity),
            "cats": [{"label": "Name", "kind": "name", "values": names}] + cats}


def S(kind, *items, **kw):
    return Clue(kind, tuple(items), **kw)


# (category, value index) shorthands are used below: (0, i) is the i-th name.
EXAMPLES = {
    1: dict(theme=theme("Pie Day", ["Hattie", "Gus", "Wren"], [PIE]),
            clues=[S("same", (0, 1), (1, 1)), S("diff", (0, 2), (1, 0))]),
    2: dict(theme=theme("The Jam Jars", ["Rosa", "Felix", "Mabel"], [JAM, JAR]),
            clues=[S("same", (0, 0), (1, 1)), S("same", (1, 1), (2, 2)), S("diff", (0, 1), (2, 0)),
                   S("diff", (1, 2), (2, 1))]),
    3: dict(theme=theme("The Ferry Line", ["Jonah", "Priya", "Teddy", "Lena"], [PLACE]),
            clues=[S("cmp", (0, 1), (0, 0), cat=1, op="<"), S("cmp", (0, 2), (0, 1), cat=1, op="d", d=1),
                   S("diff", (0, 3), (1, 0)), S("diff", (0, 0), (1, 3))]),
    5: dict(theme=theme("Three Old Salts", ["Gus", "Nico", "Mabel"], [AGE, BOAT]),
            clues=[S("cmp", (0, 0), (0, 2), cat=1, op=">"), S("pair", (0, 2), (2, 1), (1, 1), (1, 2)),
                   S("diff", (0, 1), (2, 0))]),
}


def snapshots(d):
    """marks after each step: list of dicts (index i = after steps[0..i])."""
    marks, out = {}, []
    for st in d.steps:
        if st.kind == "assume":
            continue
        for a, b in st.places:
            marks[(a, b)] = "O"
        for a, b in st.rules_out:
            marks[(a, b)] = "X"
        out.append(dict(marks))
    return out


def ser_marks(m):
    return [[list(a), list(b), v] for (a, b), v in m.items()]


def grid_example(no, ex, rng):
    th = ex["theme"]
    n = len(th["cats"][0]["values"])
    B = Bound(th, n, rng)
    clues = ex["clues"]
    assert count_solutions(B.n, B.k, clues, 3) == 1, f"lesson {no}: not unique"
    d = Deducer(B.n, B.k, clues, B.ordered)
    assert d.run(), f"lesson {no}: deducer stuck"
    return B, clues, d


def lesson6(rng):
    th = theme("The Library Hour", ["Wren", "Otis", "Dot", "Basil"], [BOOK, TIME4])
    B = Bound(th, 4, rng)
    kinds = {"same": 0.3, "diff": 1, "nor": 0.8, "either": 1.5, "pair": 1.5, "cmp": 2.5, "cmpd": 1}
    spec = Spec(4, 3, ordered=B.ordered, kinds=kinds,
                allow=("fact", "only", "transfer", "either", "alldiff", "cmp", "pair", "trial"),
                need_trial=True, max_trials=1)
    sol, clues, d = generate(spec, rng, tries=5000, accept=lambda d: 3 <= trial_chain(d) <= 6)
    return B, clues, d


def record(no, B, clues, d):
    snaps = snapshots(d)
    probe = None
    for st in d.steps:
        if st.kind == "trial":
            pr, s0 = st.info["probe"], st.info["start"]
            probe = {"snaps": [ser_marks(m) for m in snapshots_from(pr, s0, snaps_before(d, st))]}
    return {"lesson": no, "state": B.state(), "clues": [B.clue_text(c, random.Random(0)) for c in clues],
            "formal": [{"kind": c.kind, "items": [list(i) for i in c.items], "cat": c.cat, "op": c.op, "d": c.d}
                       for c in clues],
            "solution": [list(r) for r in d.solution()],
            "trace": trace(B, clues, d, collapse=False), "snaps": [ser_marks(m) for m in snaps],
            "steps": [s.kind for s in d.steps if s.kind != "assume"], "probe": probe}


def snaps_before(d, st):
    marks = {}
    for s in d.steps:
        if s is st:
            break
        for a, b in s.places:
            marks[(a, b)] = "O"
        for a, b in s.rules_out:
            marks[(a, b)] = "X"
    return marks


def snapshots_from(pr, s0, base):
    marks, out = dict(base), []
    for st in pr.steps[s0:]:
        for a, b in st.places:
            marks[(a, b)] = "O"
        for a, b in st.rules_out:
            marks[(a, b)] = "X"
        out.append(dict(marks))
    return out


def liar_example(rng):
    names = ["Bea", "Otto", "Juno"]
    th = {"did": "ate the last scone", "didnt": "didn't eat the last scone"}
    for _ in range(200):
        p = generate_liars(names, rng, rule_kind="exactly")
        if p.rule == ("exactly", 1) and all(st[0] != "lies" and st[0] != "truth" for st in p.statements):
            break
    return {"lesson": 4, "names": names, "texts": [statement_text(p, i, th) for i in range(3)],
            "rule_text": rule_text(p), "culprit": names[p.culprit],
            "cases": [{"case": names[c], "truth": list(b), "fits": ok} for c, b, ok in case_table(p)],
            "statements": [list(s) for s in p.statements]}


def main():
    os.makedirs(OUT, exist_ok=True)
    rng = random.Random(2026)
    for no, ex in EXAMPLES.items():
        B, clues, d = grid_example(no, ex, rng)
        rec = record(no, B, clues, d)
        json.dump(rec, open(os.path.join(OUT, f"L{no}.json"), "w"), indent=1)
        print(f"== Lesson {no}")
        for i, c in enumerate(rec["clues"]):
            print(f"  {i + 1}. {c}")
        for i, s in enumerate(rec["trace"]):
            print(f"   step {i}: {s['text']}")
    B, clues, d = lesson6(random.Random(66))
    rec = record(6, B, clues, d)
    json.dump(rec, open(os.path.join(OUT, "L6.json"), "w"), indent=1)
    print("== Lesson 6")
    for i, c in enumerate(rec["clues"]):
        print(f"  {i + 1}. {c}")
    for i, s in enumerate(rec["trace"]):
        print(f"   step {i}: {s['text']}")
        for c in s.get("chain", []):
            print("        > " + c)
    L4 = liar_example(random.Random(4))
    json.dump(L4, open(os.path.join(OUT, "L4.json"), "w"), indent=1)
    print("== Lesson 4", L4["texts"], L4["rule_text"], L4["culprit"])


if __name__ == "__main__":
    main()
