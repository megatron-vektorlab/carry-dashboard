"""Merge the enrichment and the second editor's fixes into data/corpus.json, then check
every entry by machine.

    python3 -m gt.finalize <enrich-workflow-result.json>

Checks (an entry that fails a hard check is dropped, with the reason in data/corpus_report.md):
  * keep=true, not on data/blacklist.txt, wording attested (gt.attest);
  * split halves join to exactly the wording (proverbs);
  * the key word occurs exactly once (where a variant has another word in that place, the
    leader page lists the variant as also correct);
  * two decoys: single words, different from the key word, known to the spelling dictionary,
    and the sentence with a decoy is not itself a real saying;
  * the "wrong word" swap: 'right' occurs in the wording, the swapped sentence is not a real saying;
  * the hint does not contain the key word or its stem; the situation does not contain it either;
  * two prompts ending in a question mark; chapter and category from the fixed lists.
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys

from . import attest, corpus, exercises, plan, text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATEGORIES = ["Tier", "Körperteil", "Essen und Trinken", "Farbe", "Zahl", "Wetter und Natur", "Ding im Haus",
              "Kleidung", "Mensch oder Beruf", "Geld", "Zeit", "anderes"]
W = r"A-Za-zÄÖÜäöüß"


def occurrences(wording: str, word: str) -> int:
    return len(re.findall(rf"(?<![{W}]){re.escape(word)}(?![{W}])", wording))


def stem(w: str) -> str:
    return w.lower()[: max(4, len(w) - 3)]


def check(e: dict, known: set[str]) -> tuple[list[str], list[str]]:
    """Returns (hard problems -> drop, soft notes)."""
    hard, soft = [], []
    w = e["wording"]
    if not e.get("keep", True):
        hard.append("editor: " + (e.get("reason") or "keep=false"))
    if corpus.blacklisted([w, *e.get("variants", [])]):
        hard.append("blacklist")
    a = attest.attest(w, e.get("variants", []) + e.get("consensus_wordings", []))
    if a["level"] == "none":
        hard.append("wording not attested")
    e["attested"], e["sources"] = a["level"], a["sources"]
    if e["kind"] == "proverb":
        sp = e.get("split") or []
        if len(sp) != 2 or re.sub(r"\s+", " ", sp[0] + " " + sp[1]).strip() != w:
            hard.append(f"split does not join to the wording: {sp}")
    k = e.get("keyword", "")
    if occurrences(w, k) != 1:
        hard.append(f"keyword {k!r} occurs {occurrences(w, k)} times")
    else:
        for v in e.get("variants", []):
            if occurrences(v, k) == 0:
                # the leader page lists the variant as also correct ("auch: ...")
                soft.append(f"variant {v!r} has another word in the gap (listed as also correct)")
        frame = exercises.blank(w, k)
        decoys = []
        for d in e.get("decoys", []):
            filled = f"{frame[0]} {d} {frame[1]}"
            if (" " in d.strip() or d.lower() == k.lower() or not text.spelled_ok(d)
                    or attest.norm(filled) in known or attest.attest(filled, exact=True)["level"] == "strong"):
                soft.append(f"decoy {d!r} dropped")
                continue
            decoys.append(d)
        e["decoys"] = decoys
        if len(decoys) < 2:
            soft.append("fewer than 2 decoys: not used on 'Das richtige Wort' sheets")
        h = e.get("hint", "")
        if stem(k) in h.lower():
            soft.append(f"hint gives the word away: {h!r}; hint removed")
            e["hint"] = ""
        sit = e.get("situation", "")
        if sit and stem(k) in sit.lower():
            soft.append("situation contains the key word; situation removed")
            e["situation"] = ""
    sw = e.get("swap") or {}
    if not sw.get("right") or occurrences(w, sw["right"]) != 1 or not sw.get("wrong") or sw["wrong"] == sw["right"]:
        soft.append(f"swap unusable: {sw}")
        e["swap"] = None
    else:
        a2, b2 = exercises.blank(w, sw["right"])
        filled = f"{a2} {sw['wrong']} {b2}"
        if attest.norm(filled) in known or attest.attest(filled, exact=True)["level"] == "strong":
            soft.append(f"swap makes a real saying: {filled!r}")
            e["swap"] = None
    if e.get("chapter") not in plan.CHAPTERS:
        hard.append(f"chapter {e.get('chapter')!r}")
    if e.get("category") not in CATEGORIES:
        e["category"] = "anderes"
    e["prompts"] = [p.strip() for p in e.get("prompts", []) if p.strip().endswith("?")]
    if len(e["prompts"]) < 2:
        soft.append("fewer than 2 prompts")
    m = e.get("meaning", "").strip()
    if not m.endswith("."):
        m += "."
    e["meaning"] = m[:1].upper() + m[1:]
    if len(m.split()) > 22:
        soft.append("meaning longer than 22 words")
    e["familiarity"] = max(1, min(3, int(e.get("familiarity", 1))))
    for f in ("hint", "situation", "note"):
        e[f] = (e.get(f) or "").strip()
    return hard, soft


def main():
    res = json.load(open(sys.argv[1]))
    cons = json.load(open(os.path.join(ROOT, "data", "corpus_consensus.json")))
    by_cid = {}
    for kind in ("proverb", "idiom"):
        for n, r in enumerate(cons[kind]["kept"], 1):
            by_cid[f"{kind[0]}{n:03d}"] = r
    entries = {}
    for batch in res:
        for it in batch["items"]:
            entries[it["id"]] = dict(it)
        for fx in batch["fixes"]:
            if fx["id"] in entries:
                entries[fx["id"]][fx["field"]] = fx["value"]
                entries[fx["id"]].setdefault("fixed", []).append(f"{fx['field']}: {fx['problem']}")
    # the proverb of each chapter's story belongs to that chapter
    sp = os.path.join(ROOT, "data", "stories.json")
    if os.path.exists(sp):
        for st in json.load(open(sp))["stories"]:
            if st["item"] in entries:
                entries[st["item"]]["chapter"] = st["chapter"]
    known = set()
    for e in entries.values():
        for w in [e["wording"], *e.get("variants", [])]:
            known.add(attest.norm(w))
    out, report = [], []
    for cid, e in sorted(entries.items()):
        src = by_cid.get(cid, {})
        e["kind"] = "proverb" if cid.startswith("p") else "idiom"
        e["consensus_wordings"] = list(src.get("wordings", {}))
        e["agree"] = src.get("agree", 0)
        hard, soft = check(e, known - {attest.norm(e["wording"])})
        if hard:
            report.append(f"- DROP {cid} {e['wording']!r}: {'; '.join(hard)}")
            continue
        if soft:
            report.append(f"- note {cid} {e['wording']!r}: {'; '.join(soft)}")
        e["id"] = cid
        out.append(e)
    by_ch = collections.Counter((e["chapter"], e["kind"]) for e in out)
    lines = [f"# Corpus report\n\n{len(out)} entries kept of {len(entries)}.\n"]
    for ch in plan.CHAPTERS:
        lines.append(f"- {ch}: {by_ch[(ch, 'proverb')]} proverbs, {by_ch[(ch, 'idiom')]} idioms")
    lines += ["", *report]
    open(os.path.join(ROOT, "data", "corpus_report.md"), "w").write("\n".join(lines) + "\n")
    json.dump({"items": out}, open(os.path.join(ROOT, "data", "corpus.json"), "w"), ensure_ascii=False, indent=1)
    print("\n".join(lines[:14]), file=sys.stderr)


if __name__ == "__main__":
    main()
