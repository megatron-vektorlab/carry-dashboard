"""Blind inputs for back-translators: only the categories and the final clue sentences.

    .venv/bin/python -m lp.blind            # writes data/blind/NNN.json for every grid puzzle with writing

The back-translators never see the generator's formal clues, its draft
sentences, the trace or the solution, so a sentence that drifted in meaning
cannot be "read back" correctly by accident.
"""
from __future__ import annotations

import json
import os
import sys

from .check_writing import BACK_FORMAT, D, load


def blind_record(P, W):
    cats = []
    for c in P["state"]["cats"]:
        e = {"label": c["label"], "values": c["values"]}
        if c.get("ordered"):
            e["ordered"] = True
            e["numbers"] = c["nums"]
            e["note"] = (f"values in order from smallest to largest number; numbers {c['nums']} "
                         f"(unit: {c.get('dunit', ['', ''])[1] or 'steps'})")
        cats.append(e)
    return {"no": P["no"], "people": P["state"]["theme"].get("entity", ["person", "people"])[1],
            "categories": cats, "clues": W["clues"], "format": BACK_FORMAT.strip()}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    nos = [int(x) for x in argv] or list(range(1, 101))
    os.makedirs(D("blind"), exist_ok=True)
    n = 0
    for no in nos:
        P, W = load("puzzles", no), load("writing", no)
        if not P or not W or P["kind"] != "grid":
            continue
        with open(D("blind", f"{no:03d}.json"), "w") as f:
            json.dump(blind_record(P, W), f, indent=1)
        n += 1
    print(f"wrote {n} blind files")


if __name__ == "__main__":
    main()
