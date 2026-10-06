"""Build every puzzle from data/selection.json -> data/puzzles.json.

    python3 -m bc.puzzles

For each verse:
  1. text = majority King James text from five copies (bc.kjv); stop if fewer than
     four copies agree on the letters;
  2. key = a fresh derangement (no letter stands for itself), fixed by the reference;
  3. U = the fewest given letters that make the reading unique over the whole KJV
     vocabulary (proved by bc.cipher.count_solutions);
  4. level (per theme: ~30% Easy, 35% Medium, 25% Hard, 10% Expert):
       Expert = no given letters at all (only verses that are unique without help),
       Easy   = the shortest verses, at least 4 given letters and >= 90% solvable by
                pure deduction (bc.cipher.forced_solve),
       Medium / Hard = the rest, split by how far deduction gets with one letter given;
                Medium gets at least 2 given letters, Hard at least 1;
  5. checks: decrypting with the key gives the verse letter for letter, no letter maps
     to itself, the solver's one reading equals the verse;
  6. hints: (1) book of the Bible + one letter, (2) two more letters, (3) the longest
     word + the full reference.
"""
from __future__ import annotations

import collections
import json
import os
import sys

from . import cipher, kjv
from .layout import MAX_LINES, MIN_LINES, lines_needed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

LEVEL_NAMES = {1: "Easy", 2: "Medium", 3: "Hard", 4: "Expert"}
SHARE = {4: 0.10, 1: 0.30, 2: 0.35, 3: 0.25}


def _pick_unique_hints(ct: str, inv: dict[str, str], given: dict[str, str]) -> dict[str, str]:
    """Add given letters greedily until exactly one KJV reading remains."""
    given = dict(given)
    freq = collections.Counter(c for c in ct if c.isalpha())
    while True:
        n, sols, done = cipher.count_solutions(ct, given, limit=2)
        if n == 1 and done:
            return given
        if n == 0:
            raise RuntimeError("solver found no reading at all - vocabulary problem")
        if n >= 2:
            diff = sorted({c for c in sols[0] if sols[0][c] != sols[1].get(c)} - set(given))
        else:  # search not finished: add the most frequent unknown letter
            diff = [c for c, _ in freq.most_common() if c not in given][:1]
        best, best_n = None, None
        for c in diff:
            trial = dict(given, **{c: inv[c]})
            m, _, ok = cipher.count_solutions(ct, trial, limit=50)
            score = (m if ok else 10_000, -freq[c], c)
            if best_n is None or score < best_n:
                best, best_n = c, score
        given[best] = inv[best]


def _top_up(ct: str, inv: dict[str, str], given: dict[str, str], target: int) -> dict[str, str]:
    """Add mid-frequency letters until `target` letters are given (the two most common
    code letters are left for the solver: finding E and T is the fun part)."""
    given = dict(given)
    freq = collections.Counter(c for c in ct if c.isalpha())
    order = [c for c, _ in freq.most_common() if c not in given]
    for c in order[2:] + order[:2]:
        if len(given) >= target:
            break
        given[c] = inv[c]
    return given


def analyze(item: dict) -> dict:
    p = kjv.passage(item["ref"], item.get("from"), item.get("to"))
    for part in p["parts"]:
        agree = len(part["letters_agree"]) + len(part["title_prefixed"])
        if agree < 4:
            raise RuntimeError(f"{item['ref']}: only {agree}/5 copies agree on the letters")
    text = p["text"]
    key = cipher.make_key(f"v1:{item['ref']}:{item.get('from', '')}")
    inv = {c: pl for pl, c in key.items()}
    ct = cipher.encrypt(text, key)
    lines = lines_needed(ct)
    if not MIN_LINES <= lines <= MAX_LINES:
        raise RuntimeError(f"{item['ref']}: needs {lines} lines (allowed {MIN_LINES}-{MAX_LINES})")
    unique = _pick_unique_hints(ct, inv, {})
    f0 = cipher.forced_solve(ct, unique)[0]
    f1 = cipher.forced_solve(ct, _top_up(ct, inv, unique, max(1, len(unique))))[0]
    return {"item": item, "passage": p, "text": text, "key": key, "inv": inv, "cipher": ct,
            "lines": lines, "unique": unique, "f0": f0, "f1": f1, "letters": len(kjv.letters(text))}


def assign_levels(recs: list[dict]) -> None:
    """Per theme: Expert, then Easy, then Medium/Hard (see module docstring)."""
    n = len(recs)
    quota = {lv: round(SHARE[lv] * n) for lv in SHARE}
    quota[2] = n - quota[1] - quota[3] - quota[4]
    left = list(recs)
    experts = sorted([r for r in left if not r["unique"] and r["letters"] >= 80], key=lambda r: (r["f0"], -r["letters"]))
    for r in experts[: quota[4]]:
        r["level"] = 4
    left = [r for r in left if "level" not in r]
    for r in sorted(left, key=lambda r: r["letters"])[: quota[1]]:
        r["level"] = 1
    left = [r for r in left if "level" not in r]
    left.sort(key=lambda r: (-r["f1"], -r["letters"]))
    n_medium = quota[2] + (quota[4] - sum(1 for r in recs if r.get("level") == 4))  # unused Expert slots -> Medium
    for i, r in enumerate(left):
        r["level"] = 2 if i < n_medium else 3


def finalize(r: dict) -> dict:
    ct, inv, key, level = r["cipher"], r["inv"], r["key"], r["level"]
    u = r["unique"]
    if level == 4:
        given = {}
    elif level == 1:
        given = _top_up(ct, inv, u, max(len(u), 4))
        while cipher.forced_solve(ct, given)[0] < 0.90 and len(given) < 7:
            given = _top_up(ct, inv, given, len(given) + 1)
    elif level == 2:
        given = _top_up(ct, inv, u, max(len(u), 2))
        if cipher.forced_solve(ct, given)[0] < 0.60:
            given = _top_up(ct, inv, given, max(len(given), 3))
    else:
        given = _top_up(ct, inv, u, max(len(u), 1))

    # independent checks
    text = r["text"]
    assert "".join(inv.get(c, c) for c in ct) == text.upper(), "decryption mismatch"
    assert all(k != v for k, v in key.items()), "a letter maps to itself"
    n, sols, done = cipher.count_solutions(ct, given, limit=2)
    assert n == 1 and done, f"{r['item']['ref']}: not unique with the printed letters"
    assert all(sols[0][c] == inv[c] for c in sols[0]), "solver reading differs from the verse"
    forced = cipher.forced_solve(ct, given)[0]

    freq = collections.Counter(c for c in ct if c.isalpha())
    rest = [c for c, _ in freq.most_common() if c not in given]
    words_plain = cipher.words(text)
    longest = max(words_plain, key=lambda w: (len(set(w)), len(w)))
    p = r["passage"]
    return {
        "ref": r["item"]["ref"],
        "partial": p["partial"], "starts_mid": p["starts_mid"], "ends_mid": p["ends_mid"],
        "book": p["book"],
        "theme": r["item"]["theme"],
        "level": level,
        "text": text,
        "cipher": ct,
        "key": key,
        "given": dict(sorted(given.items())),
        "needed_for_uniqueness": sorted(u),
        "hints": {
            "1": {"book": p["book"], "letters": [[c, inv[c]] for c in rest[:1]]},
            "2": {"letters": [[c, inv[c]] for c in rest[1:3]]},
            "3": {"word": longest, "ref": r["item"]["ref"]},
        },
        "letters": r["letters"],
        "lines": r["lines"],
        "distinct": len(set(kjv.letters(text))),
        "forced_fraction": round(forced, 3),
        "agreement": [{"ref": f"{pt['ref'][0]} {pt['ref'][1]}:{pt['ref'][2]}",
                       "exact": pt["exact"], "letters_agree": pt["letters_agree"],
                       "title_prefixed": pt["title_prefixed"], "differ": pt["differ"]} for pt in p["parts"]],
    }


def main():
    sel = json.load(open(os.path.join(DATA, "selection.json")))
    themes = [t["name"] for t in sel["themes"]]
    recs = []
    for i, item in enumerate(sel["puzzles"], 1):
        recs.append(analyze(item))
        if i % 50 == 0:
            print(f"  analysed {i}/{len(sel['puzzles'])}", file=sys.stderr)
    print(file=sys.stderr)
    out = []
    for theme in themes:
        mine = [r for r in recs if r["item"]["theme"] == theme]
        if not mine:
            continue
        assign_levels(mine)
        done = [finalize(r) for r in mine]
        # inside a theme: Easy -> Expert; inside a level, the most deducible first
        done.sort(key=lambda d: (d["level"], -d["forced_fraction"], d["ref"]))
        out.extend(done)
    for i, d in enumerate(out, 1):
        d["num"] = i
    levels = collections.Counter(d["level"] for d in out)
    print(f"{len(out)} puzzles; levels: " + ", ".join(f"{LEVEL_NAMES[k]} {levels[k]}" for k in sorted(levels)),
          file=sys.stderr)
    with open(os.path.join(DATA, "puzzles.json"), "w") as f:
        json.dump({"puzzles": out}, f, indent=1, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main()
