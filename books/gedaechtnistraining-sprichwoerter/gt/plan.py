"""Plan the 100 worksheets: 10 chapters x 10 units, each unit = one worksheet (right-hand page)
with the group leader's page on its back.

    python3 -m gt.plan          data/corpus.json + data/stories.json -> data/sheets.json

Per chapter (levels follow the practice research: 40 % one diamond, 40 % two, 20 % three):
   1 ◆    Was fehlt?              word bank            (theme-word title where the chapter has one)
   2 ◆    Das richtige Wort       two words to circle
   3 ◆    Was gehört zusammen?    5 halves             (idiom chapters: saying <-> meaning)
   4 ◆    Vorlesegeschichte       story ending in a proverb, three words to choose from
   5 ◆◆   Da stimmt was nicht!    one wrong word per saying
   6 ◆◆   Was fehlt? (letter boxes) or Das richtige Wort (three words), alternating
   7 ◆◆   Was bedeutet das? (idioms) or Wann sagt man das? (proverbs), alternating
   8 ◆◆   Wortsalat / Wie geht es weiter? / Was gehört zusammen? (6), rotating
   9 ◆◆◆  Wie geht es weiter? / Wortsalat, rotating
  10 ◆◆◆  Erste Buchstaben / Wörter suchen / Was fehlt? (free), rotating
Sayings repeat across sheets on purpose (familiarity, success), but never twice on one sheet.
Each sheet starts with its easiest saying and ends with an easy one.
"""
from __future__ import annotations

import collections
import json
import os
import random
import sys

from . import attest, exercises, text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

CHAPTERS = ["Tiere", "Körper", "Essen & Trinken", "Haus, Hof & Garten", "Wetter, Natur & Jahreszeiten",
            "Arbeit & Fleiß", "Geld & Glück", "Reden & Schweigen", "Familie & Freundschaft", "Zeit & Lebensweisheiten"]
# chapter -> (keyword category, the word used in "Welches ... fehlt?")
THEME_WORD = {"Tiere": ("Tier", "Tier"), "Körper": ("Körperteil", "Körperteil"),
              "Essen & Trinken": ("Essen und Trinken", "Wort")}
N_ITEMS = {1: 5, 2: 6, 3: 8}


def ease(it: dict) -> tuple:
    """Smaller = easier: well known first, then short."""
    return (-it["familiarity"], len(text.words(it["wording"])), it["wording"])


def _frame(it: dict) -> tuple[str, str]:
    a, b = exercises.blank(it["wording"], it["keyword"])
    return attest.norm(a), attest.norm(b)


def _known_sayings(pool: list[dict]) -> set[str]:
    out = set()
    for i in pool:
        for w in [i["wording"], *i.get("variants", [])]:
            out.add(attest.norm(w))
            out.add(attest.core(w))
    return out


def conflict(a: dict, b: dict, known: set[str]) -> bool:
    """True if a and b on one sheet would make an answer ambiguous: the same frame
    ('einen ___ haben' twice), or a's key word fits b's gap as another real saying."""
    if _frame(a) == _frame(b):
        return True
    for x, y in ((a, b), (b, a)):
        fa, fb = exercises.blank(x["wording"], x["keyword"])
        filled = f"{fa} {y['keyword']} {fb}"
        if attest.norm(filled) in known or attest.core(filled) in known or attest.attest(filled)["level"] == "strong":
            return True
    return False


class Picker:
    def __init__(self, pool: list[dict], seed: str, known: set[str] | None = None):
        self.pool = pool
        self.known = known if known is not None else _known_sayings(pool)
        self.uses = collections.Counter()
        self.rnd = random.Random("plan:" + seed)

    def pick(self, cands: list[dict], n: int, exclude=(), strict: bool = True, wider: list[dict] | None = None) -> list[dict]:
        """n items, least used first. strict: no shared key word and no ambiguity between items
        (needed wherever a word is filled in). wider: candidates to fall back on."""
        got = self._pick(cands, n, exclude, strict)
        if not got and wider is not None:
            got = self._pick(wider, n, exclude, strict)
        return got

    def _pick(self, cands, n, exclude, strict):
        cands = [c for c in cands if c["id"] not in exclude]
        if len(cands) < n:
            return []
        keyed = [(self.uses[c["id"]], -c["familiarity"], self.rnd.random(), c) for c in cands]
        keyed.sort(key=lambda k: k[:3])
        chosen, seen = [], set()
        for k in keyed:            # no key word twice on one sheet (word banks, word search)
            kw = text.letters_upper(k[3]["keyword"]) if strict else k[3]["id"]
            if kw in seen or (strict and any(conflict(k[3], c, self.known) for c in chosen)):
                continue
            seen.add(kw)
            chosen.append(k[3])
            if len(chosen) == n:
                break
        if len(chosen) < n:
            return []
        for c in chosen:
            self.uses[c["id"]] += 1
        return order_easy(chosen)


def order_easy(items: list[dict]) -> list[dict]:
    """Easiest first, second easiest last, the rest in between (hardest in the middle)."""
    s = sorted(items, key=ease)
    if len(s) < 3:
        return s
    return [s[0]] + s[2:] + [s[1]]


def plan_chapter(ci: int, chapter: str, items: list[dict], stories: dict, known: set[str]) -> list[dict]:
    pk = Picker(items, chapter, known)
    prov = [i for i in items if i["kind"] == "proverb"]
    idio = [i for i in items if i["kind"] == "idiom"]
    easy = sorted(items, key=ease)
    with_split = [p for p in prov if len(p.get("split") or []) == 2]
    sheets = []

    def add(typ, level, chosen, example=None, **extra):
        if not chosen:
            raise RuntimeError(f"{chapter}: not enough items for {typ} level {level}")
        sheets.append(dict(type=typ, level=level, chapter=chapter, items=[c["id"] for c in chosen],
                           example=example["id"] if example else None, **extra))

    def example_for(chosen, need=lambda i: True):
        ids = {c["id"] for c in chosen}
        kws = {text.letters_upper(c["keyword"]) for c in chosen}
        for c in easy:
            if (c["id"] not in ids and need(c) and text.letters_upper(c["keyword"]) not in kws
                    and not any(conflict(c, x, known) for x in chosen)):
                return c
        return None

    # 1 ◆ gaps with word bank (theme word if possible)
    cat = THEME_WORD.get(chapter)
    themed = [i for i in items if cat and i.get("category") == cat[0]]
    if cat and len(themed) >= N_ITEMS[1] + 1:
        ch = pk.pick(sorted(themed, key=ease)[:12], N_ITEMS[1], wider=themed)
        add("gaps", 1, ch, example_for(ch, lambda i: i.get("category") == cat[0]), category=cat[1])
    else:
        ch = pk.pick(easy[:14], N_ITEMS[1], wider=easy)
        add("gaps", 1, ch, example_for(ch))
    with_decoys = [i for i in easy if len(i.get("decoys") or []) >= 2]
    with_swap = [i for i in easy if i.get("swap")]
    # 2 ◆ circle, two words
    ch = pk.pick(with_decoys[:16], N_ITEMS[1], wider=with_decoys)
    add("circle", 1, ch, example_for(ch, lambda i: len(i.get("decoys") or []) >= 2))
    # 3 ◆ match halves (5) or saying <-> meaning
    if len(with_split) >= 7:
        add("match", 1, pk.pick(sorted(with_split, key=ease)[:12], 5, strict=False, wider=with_split))
    else:
        add("match_meaning", 1, pk.pick(sorted(idio, key=ease)[:12], 5, strict=False, wider=idio))
    # 4 ◆ story
    st = stories[chapter]
    add("story", 1, [next(i for i in items if i["id"] == st["item"])], story=st)
    # 5 ◆◆ wrong word
    ch = pk.pick(with_swap[:20], N_ITEMS[2], strict=False, wider=with_swap)
    add("wrong", 2, ch, example_for(ch, lambda i: bool(i.get("swap"))))
    # 6 ◆◆ letter boxes or three words
    if ci % 2 == 0:
        ch = pk.pick(items, N_ITEMS[2])
        add("gaps", 2, ch, example_for(ch))
    else:
        ch = pk.pick(with_decoys, N_ITEMS[2])
        add("circle", 2, ch, example_for(ch, lambda i: len(i.get("decoys") or []) >= 2))
    # 7 ◆◆ meaning (idioms) or situation (proverbs)
    want_meaning = (ci % 2 == 0 and len(idio) >= 4) or len([p for p in prov if p.get("situation")]) < 3
    if want_meaning:
        add("choice", 2, pk.pick(idio, 4, strict=False))
    else:
        add("situation", 2, pk.pick([p for p in prov if p.get("situation")], 3, strict=False))
    # 8 ◆◆ rotating
    short = [p for p in prov if 3 <= len(text.words(p["wording"])) <= 6]
    rot8 = ["scramble", "complete", "match"][ci % 3]
    if rot8 == "scramble" and len(short) >= 8:
        ch = pk.pick(short, N_ITEMS[2], strict=False)
        add("scramble", 2, ch, example_for(ch, lambda i: i in short))
    elif rot8 == "complete" and len(with_split) >= 8 or rot8 == "scramble" and len(with_split) >= 8:
        ch = pk.pick(with_split, N_ITEMS[2], strict=False)
        add("complete", 2, ch, example_for(ch, lambda i: i in with_split))
    elif len(with_split) >= 6:
        add("match", 2, pk.pick(with_split, 6, strict=False))
    else:
        add("match_meaning", 2, pk.pick(idio, 6, strict=False))
    # 9 ◆◆◆ complete or scramble
    longer = [p for p in prov if 5 <= len(text.words(p["wording"])) <= 9]
    if ci % 2 == 0 and len(with_split) >= 7:
        add("complete", 3, pk.pick(with_split, 7, strict=False))
    elif len(longer) >= 6:
        add("scramble", 3, pk.pick(longer, 6, strict=False))
    elif len(with_split) >= 7:
        add("complete", 3, pk.pick(with_split, 7, strict=False))
    else:
        add("gaps", 3, pk.pick(items, N_ITEMS[3]))
    # 10 ◆◆◆ rotating
    rot10 = ["firstletters", "wordsearch", "gaps"][ci % 3]
    fit_ws = [i for i in items if len(text.letters_upper(i["keyword"])) <= 10]
    if rot10 == "wordsearch" and len(fit_ws) >= 8:
        add("wordsearch", 3, pk.pick(fit_ws, 8))
    elif rot10 == "firstletters" and len(prov) >= 6:
        add("firstletters", 3, pk.pick(prov, 6, strict=False))
    else:
        add("gaps", 3, pk.pick(items, N_ITEMS[3]))
    return sheets


def main():
    corpus = [i for i in json.load(open(os.path.join(DATA, "corpus.json")))["items"] if i.get("keep", True)]
    stories = {s["chapter"]: s for s in json.load(open(os.path.join(DATA, "stories.json")))["stories"]}
    out = []
    known = _known_sayings(corpus)
    for ci, chapter in enumerate(CHAPTERS):
        items = [i for i in corpus if i["chapter"] == chapter]
        out.extend(plan_chapter(ci, chapter, items, stories, known))
    for n, s in enumerate(out, 1):
        s["num"] = n
    lv = collections.Counter(s["level"] for s in out)
    ty = collections.Counter(s["type"] for s in out)
    print(f"{len(out)} sheets; levels {dict(sorted(lv.items()))}; types {dict(ty)}", file=sys.stderr)
    with open(os.path.join(DATA, "sheets.json"), "w") as f:
        json.dump({"sheets": out}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
