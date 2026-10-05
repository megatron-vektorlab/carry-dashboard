"""Validate theme dicts and print every clue form so wording can be proofread.

    .venv/bin/python -m lp.themecheck lp/themes/cozy.py        # all themes in a module
    .venv/bin/python -m lp.themecheck lp/themes/cozy.py -v     # also print sample clues

Checks: required keys, enough values, evenly spaced ordered numbers, every
template formats, sentences start with a capital letter and end without a
doubled period, and a generated sample puzzle of each size renders.
"""
from __future__ import annotations

import argparse
import importlib.util
import random
import re
import sys

from .engine import Clue, Spec, generate
from .text import Bound

REQ_PLAIN = ("ref", "pred", "neg", "either", "short")
REQ_ORD = REQ_PLAIN + ("more", "less", "dmore", "dless", "dunit", "nums")


def load(path):
    spec = importlib.util.spec_from_file_location("themes_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.THEMES


def check_theme(t, verbose=False):
    errs = []
    for key in ("title", "story", "entity", "cats"):
        if key not in t:
            errs.append(f"missing {key}")
    if errs:
        return errs
    if t["cats"][0].get("kind") != "name":
        errs.append("first category must be kind=name")
    for c in t["cats"][1:]:
        need = REQ_ORD if c.get("ordered") else REQ_PLAIN
        for key in need:
            if key not in c:
                errs.append(f"{c.get('label')}: missing {key}")
        if c.get("ordered"):
            nums = c.get("nums", [])
            steps = {b - a for a, b in zip(nums, nums[1:])}
            if len(steps) != 1:
                errs.append(f"{c['label']}: nums must be evenly spaced")
        elif len(c.get("values", [])) < 5:
            errs.append(f"{c.get('label')}: needs at least 5 values")
    if len(t["cats"][0].get("values", [])) < 5:
        errs.append("names: need at least 5")
    if errs:
        return errs
    rng = random.Random(1)
    for n in (3, 4, 5):
        for k in range(2, len(t["cats"]) + 1):
            try:
                B = Bound(t, n, rng, k=k)
            except ValueError as e:
                errs.append(f"n={n}: {e}")
                continue
            kinds = {"same": 1, "diff": 2, "either": 1, "pair": 0.6}
            if B.ordered:
                kinds.update(cmp=2, cmpd=1)
            sol, clues, d = generate(Spec(n, B.k, ordered=B.ordered, kinds=kinds), rng, tries=50)
            for cl in clues:
                s = B.clue_text(cl, rng)
                if not s[0].isupper() or ".." in s or "{" in s:
                    errs.append(f"bad sentence: {s}")
                if verbose:
                    print(f"   [{n}x{B.k}] {s}")
    story = t["story"]
    if "{n}" not in story and "{N}" not in story:
        errs.append("story should mention the number of people via {N} (spelled) or {n}")
    return errs


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("-v", action="store_true")
    a = ap.parse_args(argv)
    themes = load(a.path)
    bad = 0
    for t in themes:
        errs = check_theme(t, a.v)
        print(("OK   " if not errs else "FAIL ") + t.get("title", "?"))
        for e in errs:
            print("     -", e)
        bad += bool(errs)
    print(f"{len(themes) - bad}/{len(themes)} themes OK")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
