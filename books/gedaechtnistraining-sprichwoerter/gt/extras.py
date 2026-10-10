"""Extras at the back of the book, built from the verified corpus (no new sayings):

  * Sprichwort-Bingo: a call list of 24 well-known sayings from the worksheets, each with its
    key word left out, and 12 different 3 x 3 cards with the key words. No call may accept a
    second word from the cards (the same checks as for one worksheet, gt.plan.conflict), and
    no word may stand in another call.
  * Raterunden: read-aloud rounds "Ich sage den Anfang, Sie das Ende" for in between, with
    well-known proverbs that are not on the sheets or in a warm-up yet.

The sheet checklist, the favourite-saying page and the A-Z list are set in layout/main.typ
from the same data.
"""
from __future__ import annotations

import collections
import random

from . import exercises as ex, plan, text

N_WORDS, N_CARDS, CARD = 24, 12, 9
N_ROUNDS, PER_ROUND = 6, 10


def _stem(w: str) -> str:
    return text.letters_upper(w)[:4]


def _context(it: dict) -> int:
    """Words around the gap: 'Ein ... sein' (2) would accept almost any card word."""
    a, b = ex.blank(it["wording"], it["keyword"])
    return len(text.words(a + " " + b))


def call_text(it: dict) -> str:
    a, b = ex.blank(it["wording"], it["keyword"])
    t = " ".join(x for x in (a, "…", b) if x).replace(" ,", ",")
    return ex.cap(t) if it["kind"] == "proverb" else t


def bingo(corpus: list[dict], sheet_ids: set[str], warm_ids: set[str], seed: str = "bingo") -> dict:
    known = plan._known_sayings(corpus)
    rnd = random.Random("gt1:" + seed)
    cands = [i for i in corpus if i["id"] in sheet_ids and i["familiarity"] >= 3 and i["keyword"][:1].isupper()
             and 3 <= len(text.letters_upper(i["keyword"])) <= 9 and _context(i) >= 3
             and ex.blank(i["wording"], i["keyword"])[0]]          # a noun, not the first word
    # spread over the chapters, best known and shortest first
    by_ch = collections.defaultdict(list)
    for c in sorted(cands, key=plan.ease):
        by_ch[c["chapter"]].append(c)
    for v in by_ch.values():
        rnd.shuffle(v)
    chosen = []
    while len(chosen) < N_WORDS and any(by_ch.values()):
        for ch in plan.CHAPTERS:
            if not by_ch[ch] or len(chosen) >= N_WORDS:
                continue
            c = by_ch[ch].pop(0)
            if any(_stem(c["keyword"]) == _stem(x["keyword"]) or plan.conflict(c, x, known) for x in chosen):
                continue
            chosen.append(c)
    if len(chosen) < N_WORDS:
        raise RuntimeError(f"bingo: only {len(chosen)} usable sayings")
    chosen.sort(key=lambda c: text.letters_upper(c["keyword"]))
    calls = [{"call": call_text(c), "word": c["keyword"], "id": c["id"]} for c in chosen]
    # cards: every word on 4 or 5 cards, no two cards alike
    words = [c["keyword"] for c in chosen]
    count = collections.Counter()
    cards, seen = [], set()
    while len(cards) < N_CARDS:
        order = sorted(words, key=lambda w: (count[w], rnd.random()))
        pick = order[:CARD]
        key = frozenset(pick)
        if key in seen:
            rnd.shuffle(words)
            continue
        seen.add(key)
        count.update(pick)
        rnd.shuffle(pick)
        cards.append(pick)
    return {"calls": calls, "cards": cards, "ids": [c["id"] for c in chosen]}


def rounds(corpus: list[dict], sheet_ids: set[str], warm_ids: set[str], seed: str = "rounds") -> dict:
    """Two-part proverbs for oral rounds: first those not printed anywhere else in the book,
    then well-known ones that are not in a warm-up; mixed chapters in every round."""
    rnd = random.Random("gt1:" + seed)
    prov = [i for i in corpus if i["kind"] == "proverb" and len(i.get("split") or []) == 2
            and i["familiarity"] >= 3 and i["id"] not in warm_ids
            and len(i["split"][0]) <= 40 and len(i["split"][1]) <= 40]
    new = [p for p in prov if p["id"] not in sheet_ids]
    old = [p for p in prov if p["id"] in sheet_ids]
    rnd.shuffle(new)
    rnd.shuffle(old)
    pool = (new + old)[: N_ROUNDS * PER_ROUND]
    if len(pool) < N_ROUNDS * PER_ROUND:
        raise RuntimeError(f"rounds: only {len(pool)} proverbs")
    out = [[] for _ in range(N_ROUNDS)]
    for k, p in enumerate(sorted(pool, key=lambda p: (plan.CHAPTERS.index(p["chapter"]), p["wording"]))):
        out[k % N_ROUNDS].append(p)
    res = []
    for r in out:
        rnd.shuffle(r)
        res.append([{"a": p["split"][0] + " …", "b": p["split"][1], "id": p["id"]} for p in r])
    return {"rounds": res, "n_new": sum(1 for p in pool if p["id"] not in sheet_ids)}
