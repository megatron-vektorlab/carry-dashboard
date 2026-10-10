"""Consensus corpus from three independent lists per kind.

    python3 -m gt.corpus <workflow-result.json>   -> data/corpus_consensus.json

Three agents each listed proverbs (and, separately, idioms) from their own knowledge,
without seeing each other's lists. An item enters the book only if at least two of the three
named it (or one named it and it is in a familiarity-tested list), it is attested in a
recognised source (gt.attest: the model may not author proverb text), and it is not on
data/blacklist.txt. Wordings are matched after normalising case, punctuation, ß/ss and apostrophes,
and through each lister's own variant lists; near-identical wordings (similarity >= 0.92)
are linked too but flagged, so the verification step decides the canonical form.
"""
from __future__ import annotations

import collections
import difflib
import json
import os
import re
import sys

from . import attest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _blacklist() -> list[str]:
    path = os.path.join(ROOT, "data", "blacklist.txt")
    return [norm(line) for line in open(path) if line.strip() and not line.startswith("#")]


def blacklisted(texts) -> bool:
    bl = _blacklist()
    return any(b in f" {norm(t)} " or b in norm(t) for t in texts for b in bl)


def norm(s: str) -> str:
    s = s.lower().replace("ß", "ss").replace("’", "'").replace("'", "")
    s = re.sub(r"[^a-zäöü ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def build(lists: list[dict]) -> dict:
    out = {}
    for kind in ("proverb", "idiom"):
        recs = []
        for L in lists:
            if L["kind"] != kind:
                continue
            for it in L["items"]:
                recs.append(dict(it, lister=L["lister"], n=norm(it["wording"]),
                                 nv={norm(v) for v in it.get("variants") or []}))
        parent = list(range(len(recs)))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        def union(i, j):
            parent[find(i)] = find(j)

        by_norm = collections.defaultdict(list)
        for i, r in enumerate(recs):
            by_norm[r["n"]].append(i)
        for ids in by_norm.values():
            for j in ids[1:]:
                union(ids[0], j)
        for i, r in enumerate(recs):
            for v in r["nv"]:
                for j in by_norm.get(v, []):
                    union(i, j)
        fuzzy = set()
        keys = list(by_norm)
        for a in range(len(keys)):
            for b in range(a + 1, len(keys)):
                ka, kb = keys[a], keys[b]
                if abs(len(ka) - len(kb)) > 6 or ka[:3] != kb[:3]:
                    continue
                if difflib.SequenceMatcher(None, ka, kb).ratio() >= 0.92:
                    union(by_norm[ka][0], by_norm[kb][0])
                    fuzzy.add(find(by_norm[ka][0]))
        groups = collections.defaultdict(list)
        for i in range(len(recs)):
            groups[find(i)].append(recs[i])
        items, dropped = [], []
        for g, members in groups.items():
            listers = sorted({m["lister"] for m in members})
            wordings = collections.Counter(m["wording"].strip().rstrip(".!") for m in members)
            rec = {
                "kind": kind,
                "wording": wordings.most_common(1)[0][0],
                "wordings": dict(wordings),
                "listers": listers,
                "agree": len(listers),
                "wording_differs": len({norm(w) for w in wordings}) > 1 or find(g) in fuzzy,
                "variants": sorted({v for m in members for v in (m.get("variants") or [])} - set(wordings)),
                "meanings": [m["meaning"] for m in members],
                "themes": [t for t, _ in collections.Counter(t for m in members for t in m.get("themes", [])).most_common(3)],
                "familiarity": round(sum(m.get("familiarity", 1) for m in members) / len(members), 2),
                "splits": [m.get("split") for m in members if m.get("split")],
            }
            a = attest.attest(rec["wording"], list(wordings) + rec["variants"])
            rec["attested"] = a["level"]
            rec["sources"] = a["sources"]
            rec["gloss"] = a["gloss"]
            rec["blacklisted"] = blacklisted([rec["wording"], *wordings, *rec["variants"]])
            tested = {"Baur/Chlosta/GfM", "Hallsteinsdóttir 2006"} & set(a["sources"])
            keep = (not rec["blacklisted"] and a["level"] != "none"
                    and (len(listers) >= 2 or tested))
            (items if keep else dropped).append(rec)
        items.sort(key=lambda r: (-r["agree"], -r["familiarity"], r["wording"]))
        out[kind] = {"kept": items, "dropped": sorted(dropped, key=lambda r: r["wording"]),
                     "raw": sum(1 for L in lists if L["kind"] == kind for _ in L["items"])}
    return out


def main():
    lists = json.load(open(sys.argv[1]))
    res = build(lists)
    for kind, r in res.items():
        reasons = collections.Counter("blacklist" if x["blacklisted"] else "not attested" if x["attested"] == "none" else "one lister"
                                      for x in r["dropped"])
        print(f"  dropped: {dict(reasons)}", file=sys.stderr)
        print(f"{kind}: {r['raw']} listed, {len(r['kept'])} kept, {len(r['dropped'])} dropped; "
              f"3 of 3: {sum(1 for x in r['kept'] if x['agree'] == 3)}; "
              f"wording differs: {sum(1 for x in r['kept'] if x['wording_differs'])}", file=sys.stderr)
    with open(os.path.join(ROOT, "data", "corpus_consensus.json"), "w") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
