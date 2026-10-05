"""Generate all 100 puzzles from the themes into data/puzzles/NNN.json.

    .venv/bin/python -m lp.build_puzzles            # everything
    .venv/bin/python -m lp.build_puzzles 12 13 40   # only these slots

Several candidates are generated per slot; within each family the chosen
candidates rise in difficulty from the first slot to the last.
"""
from __future__ import annotations

import glob
import json
import multiprocessing as mp
import os
import random
import sys

from .explain import trace
from .liars import case_table, generate_liars, rule_text, statement_text
from .make import make, trial_chain
from .plan import slots
from .themecheck import load

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "puzzles")
CANDIDATES = {"suppose": 3, "case54": 5}
DEFAULT_K = 6


def themes_by_slot():
    out = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "lp", "themes", "ch*.py"))):
        for t in load(path):
            out[t["slot"]] = t
    return out


def grid_record(slot, theme, seed):
    P = make(slot, theme, seed)
    B, sol = P["B"], P["sol"]
    table = [[B.cats[c]["values"][sol[c][e]] for c in range(B.k)] for e in range(B.n)]
    return {
        "no": slot["no"], "chapter": slot["chapter"], "family": slot["family"], "stars": slot["stars"],
        "seed": seed, "kind": "grid", "lineup": slot["lineup"],
        "title": theme["title"], "story": theme["story"], "question": theme.get("question"),
        "answer": P["answer"], "cast": theme.get("cast", []),
        "state": B.state(), "solution": [list(r) for r in sol],
        "clues": [{"kind": c.kind, "items": [list(i) for i in c.items], "cat": c.cat, "op": c.op, "d": c.d}
                  for c in P["clues"]],
        "texts": P["texts"], "trace": trace(B, P["clues"], P["d"]),
        "features": P["feats"], "trial_chain": trial_chain(P["d"]), "table": table,
        "score": P["feats"]["score"],
    }


def liar_record(slot, theme, seed):
    rng = random.Random(seed)
    no = slot["no"]
    names = theme["names"]
    rule_kind = "culprit_lies" if no in (47, 49, 52, 56) else "exactly"
    p = generate_liars(names, rng, rule_kind=rule_kind, allow_ref=no >= 55, tries=20000)
    rows = case_table(p)
    texts = [statement_text(p, i, theme) for i in range(len(names))]
    tr = []
    for c, bits, ok in rows:
        tr.append({"case": names[c], "truth": ["true" if b else "false" for b in bits],
                   "count": sum(bits), "fits": ok})
    refs = sum(st[0] in ("lies", "truth") for st in p.statements)
    return {
        "no": no, "chapter": slot["chapter"], "family": "liars", "stars": slot["stars"], "seed": seed,
        "kind": "liars", "title": theme["title"], "story": theme["story"], "cast": theme.get("cast", []),
        "names": names, "did": theme["did"], "didnt": theme["didnt"],
        "statements": [list(s) for s in p.statements], "texts": texts, "rule": list(p.rule),
        "rule_text": rule_text(p), "culprit": names[p.culprit], "truth": list(p.truth), "cases": tr,
        "question": {"text": f"Who {theme['did']}?"}, "answer": names[p.culprit],
        "score": len(names) * 10 + refs * 5,
    }


def candidates(args):
    slot, theme = args
    if slot["family"] == "liars":
        return [liar_record(slot, theme, slot["no"] * 1000 + i) for i in range(4)]
    k = CANDIDATES.get(slot["family"], DEFAULT_K)
    return [grid_record(slot, theme, slot["no"] * 1000 + i) for i in range(k)]


def choose(fam_slots, cands):
    """Pick one candidate per slot so difficulty rises through the family."""
    scores = sorted(c["score"] for s in fam_slots for c in cands[s["no"]])
    m = len(fam_slots)
    chosen = {}
    for j, s in enumerate(fam_slots):
        target = scores[min(len(scores) - 1, int((j + 0.5) / m * len(scores)))]
        best = min(cands[s["no"]], key=lambda c: (abs(c["score"] - target), c["seed"]))
        chosen[s["no"]] = best
    return chosen


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    only = {int(x) for x in argv}
    os.makedirs(OUT, exist_ok=True)
    th = themes_by_slot()
    S = [s for s in slots() if s["no"] in th]
    missing = sorted(set(range(1, 101)) - {s["no"] for s in S})
    if missing:
        print("no theme yet for slots:", missing)
    work = [(s, th[s["no"]]) for s in S if not only or s["no"] in only]
    # slow families first so the pool stays busy
    work.sort(key=lambda w: w[0]["family"] not in ("suppose", "case54"))
    with mp.Pool(max(1, min(3, os.cpu_count() - 1))) as pool:
        res = pool.map(candidates, work, chunksize=1)
    cands = {w[0]["no"]: r for w, r in zip(work, res)}
    fams = {}
    for s, _ in work:
        key = (s["family"], s["chapter"], s.get("n"))
        fams.setdefault(key, []).append(s)
    for key, fs in fams.items():
        fs.sort(key=lambda s: s["no"])
        for no, rec in choose(fs, cands).items():
            with open(os.path.join(OUT, f"{no:03d}.json"), "w") as f:
                json.dump(rec, f, indent=1)
            print(f"#{no:3d} {rec['family']:8s} score={rec['score']:4d} seed={rec['seed']} {rec['title']}")


if __name__ == "__main__":
    main()
