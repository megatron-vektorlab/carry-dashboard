"""Stress-test chapter templates.

    .venv/bin/python -m asvab.selftest 6          # chapter 6
    .venv/bin/python -m asvab.selftest 6 -n 500   # more samples per template
    .venv/bin/python -m asvab.selftest all

For every (template, level) in a chapter's PLAN it generates many problems
with different seeds and checks: the sympy answer equals the independent
check / passes verify, four distinct choices, the answer is among them,
no float leaks, enough variety (distinct stems), the answer position is not
stuck, and the text survives a LaTeX sanity scan.  Prints two samples per
template so the wording can be read.
"""
from __future__ import annotations

import argparse
import collections
import random
import re
import sys

from .core import Problem
from .generate import load_chapters, make


# problems per chapter (Parts I-III: 25 each; Part IV word-problem chapters vary)
EXPECTED = {22: 40, 23: 35, 24: 40, 25: 35, 26: 40, 27: 35}


def latex_sanity(s: str) -> list[str]:
    errs = []
    if s.count("{") != s.count("}"):
        errs.append("unbalanced braces")
    # unescaped $ pairs: \$ is money, $ toggles math
    toggles = len(re.findall(r"(?<!\\)\$", s))
    if toggles % 2:
        errs.append("odd number of $ (math mode not closed)")
    if re.search(r"(?<![\\\w])%", s):
        errs.append("unescaped % (LaTeX comment)")
    if "**" in s or "sqrt(" in s:
        errs.append("python syntax leaked into text")
    if re.search(r"\d\.\d{5,}", s):
        errs.append("long decimal (float leak?)")
    return errs


def show(p: Problem) -> str:
    lines = [f"  STEM: {p.stem}"]
    for i, (t, why) in enumerate(p.choices):
        mark = "*" if i == p.key else " "
        lines.append(f"   {mark}({'ABCD'[i]}) {t}" + (f"   <- trap: {why}" if why else ""))
    for s in p.steps:
        lines.append(f"    - {s}")
    if p.tip:
        lines.append(f"    TIP: {p.tip}")
    if p.figure:
        lines.append(f"    FIGURE: {p.figure[:200]}...")
    return "\n".join(lines)


def test_chapter(mod, n: int, quiet: bool) -> int:
    fails = 0
    print(f"\n=== Chapter {mod.NUM}: {mod.TITLE} ===")
    total = sum(c for _, _, c in mod.PLAN)
    want = EXPECTED.get(mod.NUM, 25)
    if total != want:
        print(f"  !! PLAN totals {total}, expected {want}"); fails += 1
    print(f"  PLAN total: {total}")
    for k in ("INTRO", "TITLE", "PART", "PLAN"):
        if not hasattr(mod, k):
            print(f"  !! missing {k}"); fails += 1
    errs = latex_sanity(mod.INTRO)
    if errs:
        print(f"  !! INTRO: {errs}"); fails += 1
    combos = list(dict.fromkeys((t, l) for t, l, _ in mod.PLAN))
    for tpl, lvl in combos:
        rng = random.Random(1000 + lvl)
        seen: set[str] = set()
        stems, keys, traps = set(), collections.Counter(), 0
        samples = []
        try:
            for i in range(n):
                p = make(tpl, lvl, rng, i % 4, seen=set(), chapter=mod.NUM)
                stems.add(p.stem)
                keys[p.key] += 1
                traps += any(w for _, w in p.choices)
                blob = p.stem + " ".join(p.steps) + " ".join(t for t, _ in p.choices) + (p.tip or "") \
                    + " ".join(w or "" for _, w in p.choices)
                e = latex_sanity(blob)
                if e:
                    raise AssertionError(f"LaTeX sanity {e}:\n{show(p)}")
                if len(samples) < 2 and (not samples or samples[0].stem != p.stem):
                    samples.append(p)
        except Exception as e:  # noqa: BLE001
            print(f"  !! {tpl.__name__} L{lvl}: {type(e).__name__}: {e}")
            fails += 1
            continue
        variety = len(stems) / n
        flag = "" if variety >= 0.5 else "  !! LOW VARIETY"
        if variety < 0.5:
            fails += 1
        print(f"  {tpl.__name__:<28} L{lvl} [{getattr(tpl, 'section', '?')}] "
              f"distinct={len(stems)}/{n} keys={dict(sorted(keys.items()))} "
              f"with-trap={traps}/{n}{flag}")
        if not quiet:
            for s in samples:
                print(show(s))
    return fails


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", help="chapter number or 'all'")
    ap.add_argument("-n", type=int, default=200)
    ap.add_argument("-q", "--quiet", action="store_true")
    a = ap.parse_args(argv)
    mods = load_chapters(None if a.chapter == "all" else int(a.chapter))
    if a.chapter != "all":
        mods = [m for m in mods if m.NUM == int(a.chapter)]
        if not mods:
            sys.exit(f"chapter {a.chapter} not found")
    fails = sum(test_chapter(m, a.n, a.quiet) for m in mods)
    print(f"\n{'FAILED' if fails else 'OK'}: {fails} problem(s)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
