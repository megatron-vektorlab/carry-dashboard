#!/usr/bin/env python3
"""Blind review of the BKS content.

  review.py prepare [N]   write content/review/review_NN_bks.json (BKS only, no answer key)
                          and review_NN_de.json (German originals) for N reviewers
  review.py merge         compare reviewers' answers with the key -> content/review_report.md

A reviewer first answers every question from the BKS translation alone and states which option
each explanation supports; only then does it open the German file to flag translation problems.
Any disagreement with the locked key points to a translation or explanation defect.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REV = ROOT / "content" / "review"
L = "ABCD"


def prepare(n):
    REV.mkdir(parents=True, exist_ok=True)
    cat = {q["id"]: q for q in json.load(open(ROOT / "data" / "catalog.json", encoding="utf-8"))["questions"]}
    bks = json.load(open(ROOT / "content" / "bks.json", encoding="utf-8"))
    size = -(-len(bks) // n)
    for i in range(n):
        part = bks[i * size:(i + 1) * size]
        blind = [dict(id=t["id"], q_bks=t["q_bks"], options={L[j]: o for j, o in enumerate(t["options_bks"])},
                      expl_bks=t["expl_bks"], merksatz_de=t["merksatz_de"]) for t in part]
        de = [dict(id=t["id"], question_de=cat[t["id"]]["question"],
                   options_de={L[j]: o for j, o in enumerate(cat[t["id"]]["options"])}) for t in part]
        json.dump(blind, open(REV / f"review_{i+1:02d}_bks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump(de, open(REV / f"review_{i+1:02d}_de.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(i + 1, len(part), part[0]["id"], part[-1]["id"])


def merge():
    cat = {q["id"]: q for q in json.load(open(ROOT / "data" / "catalog.json", encoding="utf-8"))["questions"]}
    notes = json.load(open(ROOT / "content" / "image_notes_bks.json", encoding="utf-8"))["notes"]
    rows, seen = [], set()
    for f in sorted(REV.glob("review_*_result.json")):
        for r in json.load(open(f, encoding="utf-8")):
            seen.add(r["id"])
            key = L[cat[r["id"]]["answer"]]
            blind_ok = r.get("answer_from_translation") == key
            expl_ok = r.get("explanation_supports") == key
            issue = (r.get("issues") or "").strip()
            if not blind_ok or not expl_ok or issue:
                rows.append((r["id"], key, r.get("answer_from_translation"), r.get("explanation_supports"),
                             issue, r["id"] in notes))
    missing = [i for i in cat if i not in seen]
    blind_bad = [x for x in rows if x[2] != x[1]]
    expl_bad = [x for x in rows if x[3] != x[1]]
    lines = ["# Blind review (DE–BKS)", "",
             f"- Reviewed: {len(seen)}/{len(cat)}" + (f" (missing: {', '.join(missing[:20])})" if missing else ""),
             f"- Blind answer ≠ key: {len(blind_bad)} (picture questions cannot be answered blind: "
             f"{sum(1 for x in blind_bad if x[5])} of these)",
             f"- Explanation supports another option: {len(expl_bad)}",
             f"- Items with translation/style remarks: {sum(1 for x in rows if x[4])}", "",
             "| id | key | blind | explanation | remark |", "|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4].replace('|', '/')} |")
    (ROOT / "content" / "review_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:7]))


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare(int(sys.argv[2]) if len(sys.argv) > 2 else 5)
    else:
        merge()
