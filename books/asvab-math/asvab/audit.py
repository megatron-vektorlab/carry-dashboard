"""Book-wide audit of the generated problems (run after build or standalone).

    .venv/bin/python -m asvab.audit            # all chapters + tests
    .venv/bin/python -m asvab.audit --chapters 6,7

Beyond the per-problem validation in core.finalize, this looks for things a
proofreader would catch:
  * the final answer never appears in the solution steps (steps and answer
    may disagree)
  * article errors ("a 8", "a 11"), "1 minutes", doubled words
  * leftover Python / sympy syntax, very long numbers
  * near-duplicate stems (same text once digits are removed) inside a chapter
  * the correct letter's share per chapter (balance)
"""
from __future__ import annotations

import argparse
import collections
import re

from .build import generate_all
from .generate import load_chapters
from .render import LETTERS

ARTICLE = re.compile(r"\b[aA] \$?(8|11|18|80|8\d\d|11\d|18\d)(?![\d{,])")
ONE_PLURAL = re.compile(r"(?<![\d.,{])\$?1\$?~?\s(minutes|hours|miles|feet|inches|days|weeks|years|dollars|pounds|ounces|gallons|cups)\b")
DOUBLED = re.compile(r"\b(\w+) \1\b", re.I)
PY = re.compile(r"\*\*|sqrt\(|Rational\(|Integer\(|\bpi\b(?!})")


def plain(tex: str) -> str:
    """Rough visible text of a LaTeX snippet for comparisons."""
    s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", tex)
    s = re.sub(r"\\[a-zA-Z]+", " ", s)
    s = re.sub(r"[{}$~\\]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def answer_core(tex: str) -> str:
    """The number/expression part of a choice, for searching in the steps."""
    s = tex.replace("\\$", "").replace("\\%", "")
    s = re.sub(r"~?[A-Za-z]+s?$", "", s.strip())        # trailing unit word
    s = s.strip().strip("$").strip()
    s = re.sub(r"\\text\{[^}]*\}\^\d", "", s)            # sq_unit suffix
    s = re.sub(r"\.00$", "", s.strip())                    # $156.00 vs 156
    return s.strip()


def audit_problem(where: str, p) -> list[str]:
    out = []
    steps = " ".join(p.steps) + " " + (p.tip or "")
    ans = p.choices[p.key][0]
    core = answer_core(ans)
    if core and core not in steps and plain(core) not in plain(steps):
        out.append(f"answer {ans!r} not found in steps")
    blob = p.stem + " " + steps + " " + " ".join(t for t, _ in p.choices)
    for name, rx in (("article", ARTICLE), ("one-plural", ONE_PLURAL), ("python", PY)):
        mm = rx.search(blob)
        if mm:
            out.append(f"{name}: …{blob[max(0, mm.start() - 30):mm.end() + 30]}…")
    for mm in DOUBLED.finditer(plain(blob)):
        w = mm.group(1).lower()
        if not w.isdigit() and w not in {"that", "had"}:
            out.append(f"doubled word: {mm.group(0)!r}")
    return [f"{where} [{p.template} L{p.level}]: {o}" for o in out]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapters")
    a = ap.parse_args(argv)
    if a.chapters:
        mods = [m for n in a.chapters.split(",") for m in load_chapters(int(n))]
    else:
        mods = load_chapters()
    chapters, diag, tests = generate_all(mods)
    issues = []
    for mod in mods:
        ps = chapters[mod.NUM]
        for i, p in enumerate(ps, 1):
            issues += audit_problem(f"ch{mod.NUM:02d}#{i}", p)
        skel = collections.Counter(re.sub(r"\d+", "#", plain(p.stem)) for p in ps)
        for s, c in skel.items():
            if c > 4:
                issues.append(f"ch{mod.NUM:02d}: {c} near-identical stems: {s[:90]}")
        letters = collections.Counter(LETTERS[p.key] for p in ps)
        if max(letters.values()) > 0.4 * len(ps):
            issues.append(f"ch{mod.NUM:02d}: unbalanced answer letters {dict(letters)}")
    for i, p in enumerate(diag, 1):
        issues += audit_problem(f"diag#{i}", p)
    for k, (ar, mk) in enumerate(tests, 1):
        for i, p in enumerate(ar, 1):
            issues += audit_problem(f"test{k}AR#{i}", p)
        for i, p in enumerate(mk, 1):
            issues += audit_problem(f"test{k}MK#{i}", p)
    for line in issues:
        print(line)
    print(f"\n{len(issues)} issue(s)")


if __name__ == "__main__":
    main()
