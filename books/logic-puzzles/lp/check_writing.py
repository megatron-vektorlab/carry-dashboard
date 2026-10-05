"""Mechanical checks on the writers' work.

    .venv/bin/python -m lp.check_writing                # all puzzles that have writing
    .venv/bin/python -m lp.check_writing 12 40          # some puzzles
    .venv/bin/python -m lp.check_writing --back 12      # also compare back-translations

data/writing/NNN.json (by the writers):
    {"no": 12, "clues": [...same count and order as the puzzle...],
     "hints": ["...", "...", "..."(, "halfway hint" for 4-5 stars)],
     "solution": {"key_idea": "...", "steps": ["...", ...], "epilogue": "..."},
     "tip": "optional one-line tip from Ada (chapters 1-3)"}

data/back/NNN.json (by blind back-translators, who never see the formal clues):
    {"no": 12, "clues": [ formal clue, ... ]}   -- format in BACK_FORMAT below

A back-translation is compared with the generator's clue by evaluating both
on every possible grid: they must allow exactly the same solutions.
"""
from __future__ import annotations

import json
import os
import re
import sys

import numpy as np

from .engine import Clue
from .space import Space

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, "data", *p)  # noqa: E731

BACK_FORMAT = """
Items are written "Category=value" using the category labels and values exactly as listed
(for number categories use the value as shown, e.g. "Time=9 a.m.").
  {"kind": "same", "a": ITEM, "b": ITEM}                 a and b belong to the same person
  {"kind": "diff", "a": ITEM, "b": ITEM}                 a and b belong to different people
  {"kind": "nor", "a": ITEM, "not": [ITEM, ITEM]}         a's person has neither of the two
  {"kind": "either", "a": ITEM, "one_of": [ITEM, ITEM]}  a's person has one of the two
  {"kind": "compare", "a": ITEM, "b": ITEM, "cat": CATEGORY,
     "rel": "a_greater" | "a_less" | "a_greater_by" | "a_less_by" | "next_to" | "not_next_to",
     "by": NUMBER}   compare the CATEGORY numbers of a's person and b's person; "by" (only for
                     *_by) is the exact difference in the category's own numbers (e.g. 2 for
                     "two hours later" when times are whole hours; 1 for "right behind" in a line)
  {"kind": "pair", "people": [ITEM, ITEM], "options": [ITEM, ITEM]}
                     of the two people named by "people", one has the first option and the
                     other has the second (in some order); they are two different people
  {"kind": "all_different", "items": [ITEM, ITEM, ...]}  all belong to different people
  {"kind": "other", "text": "..."}                       anything that fits none of these
"""


def load(kind, no):
    p = D(kind, f"{no:03d}.json")
    if not os.path.exists(p):
        return None
    with open(p) as f:
        return json.load(f)


def clue_from_record(c):
    return Clue(c["kind"], tuple(tuple(i) for i in c["items"]), c.get("cat", -1), c.get("op", ""), c.get("d", 0))


class Items:
    def __init__(self, P):
        self.cats = P["state"]["cats"]
        self.labels = [c["label"].lower() for c in self.cats]

    def item(self, s):
        if not isinstance(s, str) or "=" not in s:
            raise ValueError(f"bad item {s!r}")
        cat, val = s.split("=", 1)
        ci = self.labels.index(cat.strip().lower())
        vals = [str(v).lower() for v in self.cats[ci]["values"]]
        return (ci, vals.index(val.strip().lower()))

    def cat(self, s):
        return self.labels.index(s.strip().lower())


def clue_from_back(P, b):
    I = Items(P)
    k = b.get("kind")
    if k in ("same", "diff"):
        return Clue(k, (I.item(b["a"]), I.item(b["b"])))
    if k == "nor":
        x, y = b["not"]
        return Clue("nor", (I.item(b["a"]), I.item(x), I.item(y)))
    if k == "either":
        x, y = b["one_of"]
        return Clue("either", (I.item(b["a"]), I.item(x), I.item(y)))
    if k == "compare":
        o = I.cat(b["cat"])
        c = I.cats[o]
        a, bb = I.item(b["a"]), I.item(b["b"])
        rel = b["rel"]
        if rel == "a_greater":
            return Clue("cmp", (a, bb), cat=o, op=">")
        if rel == "a_less":
            return Clue("cmp", (a, bb), cat=o, op="<")
        if rel in ("next_to", "not_next_to"):
            return Clue("cmp", (a, bb), cat=o, op="adj" if rel == "next_to" else "nadj")
        nums = c["nums"]
        step = nums[1] - nums[0]
        by = float(b["by"]) / step
        if abs(by - round(by)) > 1e-9:
            raise ValueError(f"'by' {b['by']} is not a multiple of the step {step}")
        d = int(round(by))
        if rel == "a_greater_by":
            return Clue("cmp", (a, bb), cat=o, op="d", d=d)
        if rel == "a_less_by":
            return Clue("cmp", (bb, a), cat=o, op="d", d=d)
    if k == "pair":
        p1, p2 = b["people"]
        o1, o2 = b["options"]
        return Clue("pair", (I.item(p1), I.item(p2), I.item(o1), I.item(o2)))
    if k == "all_different":
        return Clue("alldiff", tuple(I.item(x) for x in b["items"]))
    raise ValueError(f"cannot use back-translation kind {k!r}")


def compare_back(P, back):
    """List of (clue number, problem) where the back-translation differs."""
    n, k = len(P["state"]["cats"][0]["values"]), len(P["state"]["cats"])
    S = Space(n, k)
    probs = []
    clues = [clue_from_record(c) for c in P["clues"]]
    bl = back.get("clues", [])
    if len(bl) != len(clues):
        return [(0, f"back-translation has {len(bl)} clues, puzzle has {len(clues)}")]
    for i, (c, b) in enumerate(zip(clues, bl)):
        try:
            bc = clue_from_back(P, b)
        except (ValueError, KeyError, TypeError) as e:
            probs.append((i + 1, f"could not read back-translation {b}: {e}"))
            continue
        m1, m2 = np.asarray(S.mask(c)), np.asarray(S.mask(bc))
        if not np.array_equal(m1, m2):
            extra = int((m2 & ~m1).sum())
            lost = int((m1 & ~m2).sum())
            probs.append((i + 1, f"meaning differs (back-translation {b}; allows {extra} extra grids, "
                                 f"forbids {lost} grids the original allows)"))
    return probs


BAD = re.compile(r"[{}]|\.\.|\s[,.;:]|\bthe the\b", re.I)


def check_writing(P, W):
    probs = []
    no = P["no"]
    if P["kind"] == "grid":
        if len(W.get("clues", [])) != len(P["texts"]):
            probs.append(f"clue count {len(W.get('clues', []))} != {len(P['texts'])}")
    hints = W.get("hints", [])
    want = 4 if P["stars"] >= 4 else 3
    if len(hints) != want:
        probs.append(f"needs {want} hints, has {len(hints)}")
    sol = W.get("solution", {})
    steps = sol.get("steps", [])
    if not sol.get("key_idea"):
        probs.append("missing key_idea")
    lo, hi = {1: (3, 5), 2: (3, 5), 3: (4, 6), 4: (5, 8), 5: (5, 8)}[P["stars"]]
    if not lo <= len(steps) <= hi:
        probs.append(f"solution has {len(steps)} steps (want {lo}-{hi} for {P['stars']} stars)")
    words = lambda t: len((t or "").split())  # noqa: E731
    for i, h in enumerate(hints):
        if words(h) > 35:
            probs.append(f"hint {i + 1} has {words(h)} words (max 35)")
    for i, st in enumerate(steps):
        if words(st) > 30:
            probs.append(f"step {i + 1} has {words(st)} words (max 25-30)")
    if words(sol.get("key_idea")) > 30:
        probs.append(f"key_idea has {words(sol.get('key_idea'))} words (max 25)")
    if words(sol.get("epilogue")) > 40:
        probs.append(f"epilogue has {words(sol.get('epilogue'))} words (max 35)")
    if P.get("question") and P["kind"] == "grid" and not W.get("answer_line"):
        probs.append("missing answer_line (puzzle has a question)")
    if not sol.get("epilogue"):
        probs.append("missing epilogue")
    texts = list(W.get("clues", [])) + hints + steps + [sol.get("key_idea", ""), sol.get("epilogue", ""),
                                                         W.get("tip", "") or ""]
    nclues = len(P["texts"])
    for t in texts:
        if BAD.search(t or ""):
            probs.append(f"typo pattern in: {t}")
        for m in re.findall(r"[Cc]lues? (\d+)(?:\s*(?:and|,|&)\s*(\d+))?", t or ""):
            for x in m:
                if x and not 1 <= int(x) <= nclues:
                    probs.append(f"refers to clue {x} (only {nclues}): {t}")
    for i, c in enumerate(W.get("clues", [])):
        if not c or not c[0].isupper() or not c.rstrip().endswith((".", "!", "?", "”", '"')):
            probs.append(f"clue {i + 1} is not a full sentence: {c}")
    return probs


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    back = "--back" in argv
    nos = [int(x) for x in argv if x.isdigit()] or list(range(1, 101))
    total = 0
    for no in nos:
        P = load("puzzles", no)
        W = load("writing", no)
        if P is None or W is None:
            continue
        probs = [f"writing: {p}" for p in check_writing(P, W)]
        if back and P["kind"] == "grid":
            B = load("back", no)
            if B is None:
                probs.append("no back-translation")
            else:
                probs += [f"clue {i}: {p}" for i, p in compare_back(P, B)]
        for p in probs:
            print(f"#{no}: {p}")
        total += len(probs)
    print(f"{total} problems")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
