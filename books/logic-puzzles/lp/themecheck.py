"""Validate theme files against the book plan and print every clue form.

    .venv/bin/python -m lp.themecheck lp/themes/ch2.py        # check one chapter file
    .venv/bin/python -m lp.themecheck lp/themes/ch2.py -v     # also print sample clues
    .venv/bin/python -m lp.themecheck all                     # every file, plus book-wide checks

See THEMES.md for the format.  Grid themes are checked by generating several
real puzzles for the theme's slot and rendering every clue; liar themes are
checked by generating sample puzzles from them.
"""
from __future__ import annotations

import argparse
import glob
import importlib.util
import os
import random
import re
import sys

from .engine import Clue
from .liars import generate_liars, rule_text, statement_text
from .make import spec_for
from .engine import generate
from .plan import slots
from .text import Bound

REQ_PLAIN = ("ref", "pred", "neg", "either", "nor", "short")
REQ_ORD = REQ_PLAIN + ("more", "less", "dmore", "dless", "dunit", "nums")
REQ_LINEUP = ("adj", "nadj", "ends")
SLOTS = {s["no"]: s for s in slots()}
MAX_LABEL = 12


def load(path):
    spec = importlib.util.spec_from_file_location("themes_" + os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.THEMES


def _sentence_ok(s):
    return s[:1].isupper() and not re.search(r"\.\.|\{|\}|  |\s[,.]", s) and s.endswith((".", "?", "!"))


def check_grid(t, slot, verbose=False):
    errs = []
    n, k = slot["n"], slot["k"]
    cats = t.get("cats", [])
    if len(cats) != k:
        return [f"needs exactly {k} categories (names + {k - 1}), has {len(cats)}"]
    if cats[0].get("kind") != "name":
        errs.append("first category must be kind='name'")
    names = cats[0].get("values", [])
    if len(names) != n:
        errs.append(f"needs exactly {n} names, has {len(names)}")
    if len({x[0] for x in names}) != len(names):
        errs.append(f"names must start with different letters: {names}")
    if len(names) >= 3 and names == sorted(names):
        errs.append("names are in alphabetical order; mix them up")
    ordered = [c for c in cats[1:] if c.get("ordered")]
    if len(ordered) != slot["ordered"]:
        errs.append(f"needs exactly {slot['ordered']} ordered (number/time/position) categories, has {len(ordered)}")
    for c in cats[1:]:
        lab = c.get("label", "?")
        need = REQ_ORD if c.get("ordered") else REQ_PLAIN
        if c.get("ordered") and slot.get("lineup"):
            need = need + REQ_LINEUP
        for key in need:
            if key not in c:
                errs.append(f"{lab}: missing '{key}'")
        if c.get("ordered"):
            nums = c.get("nums", [])
            if len(nums) != n:
                errs.append(f"{lab}: needs exactly {n} nums")
            if len({b - a for a, b in zip(nums, nums[1:])}) > 1 or any(b <= a for a, b in zip(nums, nums[1:])):
                errs.append(f"{lab}: nums must be increasing and evenly spaced")
            if c.get("labels") is not None and len(c["labels"]) != len(nums):
                errs.append(f"{lab}: labels must match nums")
            for key in ("dmore1", "dless1"):
                if (key in c) != ("dmore1" in c and "dless1" in c):
                    errs.append(f"{lab}: give both dmore1 and dless1 or neither")
        else:
            if len(c.get("values", [])) != n:
                errs.append(f"{lab}: needs exactly {n} values")
            if len(set(c.get("values", []))) != len(c.get("values", [])):
                errs.append(f"{lab}: duplicate values")
    for key in ("title", "story", "entity"):
        if not t.get(key):
            errs.append(f"missing {key}")
    if slot["chapter"] >= 6 and not t.get("question"):
        errs.append("chapters 6-7 need a 'question' (whodunit payoff)")
    if errs:
        return errs
    labels = list(names)
    for c in cats[1:]:
        labels += (c.get("labels") or [c.get("fmt", "{x}").format(x=x) for x in c["nums"]]) if c.get("ordered") else c["values"]
    for lab in labels:
        if len(str(lab)) > MAX_LABEL:
            errs.append(f"grid label too long (max {MAX_LABEL} chars): '{lab}'")
    q = t.get("question")
    if q:
        labs = [c["label"] for c in cats]
        if not isinstance(q, dict) or q.get("cat") not in labs:
            errs.append("question needs {'text', 'cat' (a category label), 'value'}")
        else:
            c = cats[labs.index(q["cat"])]
            vals = c.get("labels") or c.get("values") or [c.get("fmt", "{x}").format(x=x) for x in c.get("nums", [])]
            if q.get("value") not in vals:
                errs.append(f"question value '{q.get('value')}' is not one of {vals}")
            if not str(q.get("text", "")).endswith("?"):
                errs.append("question text should be a question ending with '?'")
    if not _sentence_ok(t["story"].strip()):
        errs.append("story should be complete sentences")
    rng = random.Random(slot["no"])
    seen = set()
    for trial in range(3):
        B = Bound(t, n, rng, k=k)
        try:
            sol, clues, d = generate(spec_for(slot, B), rng, tries=400)
        except RuntimeError:
            errs.append("could not generate a sample puzzle")
            break
        for cl in clues:
            s = B.clue_text(cl, rng)
            if not _sentence_ok(s):
                errs.append(f"bad sentence: {s}")
            if verbose and s not in seen:
                print(f"   [{slot['no']}] {s}")
            seen.add(s)
    return errs


def check_liars(t, slot, verbose=False):
    errs = []
    for key in ("title", "story", "names", "did", "didnt"):
        if not t.get(key):
            errs.append(f"missing {key}")
    if errs:
        return errs
    names = t["names"]
    if not 3 <= len(names) <= 5:
        errs.append("liar puzzles need 3-5 names")
    if len({x[0] for x in names}) != len(names):
        errs.append("names must start with different letters")
    rng = random.Random(slot["no"])
    for i in range(2):
        p = generate_liars(names, rng, rule_kind=rng.choice(["exactly", "culprit_lies"]), allow_ref=True)
        for j in range(len(names)):
            s = statement_text(p, j, t)
            if not _sentence_ok(s):
                errs.append(f"bad statement: {s}")
            if verbose:
                print(f"   [{slot['no']}] {names[j]}: \"{s}\"")
        if verbose:
            print("   ", rule_text(p))
    return errs


def check_file(path, verbose=False):
    themes = load(path)
    bad = 0
    for t in themes:
        slot = SLOTS.get(t.get("slot"))
        if slot is None:
            print(f"FAIL {t.get('title', '?')}: unknown slot {t.get('slot')}")
            bad += 1
            continue
        errs = check_liars(t, slot, verbose) if slot["family"] == "liars" else check_grid(t, slot, verbose)
        print(("OK   " if not errs else "FAIL ") + f"#{slot['no']} {t.get('title', '?')}")
        for e in errs:
            print("     -", e)
        bad += bool(errs)
    return themes, bad


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("-v", action="store_true")
    a = ap.parse_args(argv)
    paths = sorted(glob.glob(os.path.join(os.path.dirname(__file__), "themes", "ch*.py"))) if a.path == "all" else [a.path]
    allt, bad = [], 0
    for p in paths:
        th, b = check_file(p, a.v)
        allt += th
        bad += b
    if a.path == "all":
        nos = sorted(t.get("slot") for t in allt)
        missing = sorted(set(range(1, 101)) - set(nos))
        dup = sorted({x for x in nos if nos.count(x) > 1})
        titles = [t.get("title", "").lower() for t in allt]
        dupt = sorted({x for x in titles if titles.count(x) > 1})
        for label, v in (("missing slots", missing), ("duplicate slots", dup), ("duplicate titles", dupt)):
            if v:
                print(f"BOOK {label}: {v}")
                bad += 1
    print(f"{len(allt) - bad if bad <= len(allt) else 0}/{len(allt)} themes OK")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
