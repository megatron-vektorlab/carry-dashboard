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
   7 ◆◆   Was bedeutet das? (idioms, 3) or Wann sagt man das? (proverbs, 3), alternating
   8 ◆◆   Wortsalat / Wie geht es weiter? / Was gehört zusammen? (6), rotating
   9 ◆◆◆  Wie geht es weiter? / Wortsalat: never the same type as sheet 8 (at most 6 items)
  10 ◆◆◆  Erste Buchstaben / Wörter suchen / Was fehlt? (free), rotating; no free gaps in a
          chapter that already has letter boxes
Sayings repeat across sheets on purpose (familiarity, success), but never twice on one sheet,
and never on the sheet right after the one that used them: a worksheet faces the leader page
of the sheet before it, and that page prints its solutions. The first sheet of a chapter faces
the chapter page, so a saying quoted there is kept off it. The saying that ends the chapter's
story is kept off the three sheets before the story, and a solved example is used only once
per chapter. Level-1 sheets use the best-known sayings only (familiarity 3) where there are
enough. Each sheet starts with its easiest saying and ends with an easy one.
"""
from __future__ import annotations

import collections
import copy
import json
import re
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
N_ITEMS = {1: 5, 2: 6, 3: 6}


def ease(it: dict) -> tuple:
    """Smaller = easier: well known first, then short."""
    return (-it["familiarity"], len(text.words(it["wording"])), it["wording"])


def _frame(it: dict) -> tuple[str, str]:
    a, b = exercises.blank(it["wording"], it["keyword"])
    return attest.norm(a), attest.norm(b)


def framed(it: dict) -> bool:
    """At least two words around the gap ("_____ haben" gives no clue)."""
    a, b = exercises.blank(it["wording"], it["keyword"])
    return len(text.words(a + " " + b)) >= 2


def swap_ok(it: dict) -> bool:
    if not it.get("swap"):
        return False
    a, b = exercises.blank(it["wording"], it["swap"]["right"])
    return bool(text.words(a + " " + b))


def complete_ok(it: dict, level: int) -> bool:
    """'Wie geht es weiter?': the start must point to one saying only, and at level 2 the
    printed first word must not already be the whole ending ("Versprochen ist ... versprochen")."""
    sp = it.get("split") or []
    if len(sp) != 2 or it.get("no_complete"):
        return False
    if level == 2 and len(text.words(sp[1])) < 2:
        return False
    first = text.words(sp[0])
    if first and first[0] == "Man" and len(first) <= 3:          # "Man kann nicht ..." is far too open
        return False
    return not attest.starts_other(sp[0], it["wording"])


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
    ka, kb = (x["keyword"].lower().translate(str.maketrans("äöü", "aou")) for x in (a, b))
    if ka[:4] == kb[:4] or ka.startswith(kb) or kb.startswith(ka):     # Hund / Hunde on one sheet
        return True
    # a hint must not name another answer on the sheet, and two hints must not sound alike
    for x, y in ((a, b), (b, a)):
        h = (x.get("hint") or "").lower()
        if h and y["keyword"].lower()[:max(4, len(y["keyword"]) - 3)] in h:
            return True
    from .book import similar
    if a.get("hint") and b.get("hint") and similar(a["hint"], b["hint"]):
        return True
    # one saying must not show another's answer ("die Katze im Sack" next to "Die K... lässt das Mausen")
    if exercises.blank and (re.search(rf"(?<![{exercises.W}]){re.escape(a['keyword'])}", b["wording"], re.I)
                            or re.search(rf"(?<![{exercises.W}]){re.escape(b['keyword'])}", a["wording"], re.I)):
        return True
    for x, y in ((a, b), (b, a)):
        if y["keyword"] in x.get("also_fits", []):        # "Feuer und Wasser" next to "Feuer und Flamme"
            return True
        fa, fb = exercises.blank(x["wording"], x["keyword"])
        filled = f"{fa} {y['keyword']} {fb}"
        if (attest.norm(filled) in known or attest.core(filled) in known
                or attest.attest(filled, exact=True)["level"] == "strong" or attest.phrase_with(filled, y["keyword"])):
            return True
    return False


def _first(s: str, n: int = 1) -> str:
    return " ".join(attest.norm(w) for w in text.words(s)[:n])


def match_clash(a: dict, b: dict) -> bool:
    """Two halves that look alike invite a wrong match: 'Wo Licht ist,' / 'Wo Rauch ist,'
    or 'ist auch Schatten' / 'ist auch Feuer'."""
    sa, sb = a.get("split") or ["", ""], b.get("split") or ["", ""]
    return _first(sa[0]) == _first(sb[0]) or _first(sa[1], 2) == _first(sb[1], 2)


def circle_clash(n: int):
    """Words to circle: no wrong word twice on a sheet, and no answer offered as a wrong word."""
    def clash(a: dict, b: dict) -> bool:
        da = {d.lower() for d in (a.get("decoys") or [])[: n - 1]}
        db = {d.lower() for d in (b.get("decoys") or [])[: n - 1]}
        return bool(da & db) or a["keyword"].lower() in db or b["keyword"].lower() in da
    return clash


def wrong_clash(a: dict, b: dict) -> bool:
    """'Da stimmt was nicht!': no answer twice on a sheet (Mund, Mund), and no word that is
    wrong in one sentence but right in the next (Bauch)."""
    ra, rb = a["swap"]["right"].lower(), b["swap"]["right"].lower()
    wa, wb = a["swap"]["wrong"].lower(), b["swap"]["wrong"].lower()
    words_a = {w.lower() for w in text.words(a["wording"])}
    words_b = {w.lower() for w in text.words(b["wording"])}
    return ra == rb or wa == wb or wa in words_b or wb in words_a


class Picker:
    def __init__(self, pool: list[dict], seed: str, known: set[str] | None = None):
        self.pool = pool
        self.known = known if known is not None else _known_sayings(pool)
        self.uses = collections.Counter()
        self.rnd = random.Random("plan:" + seed)

    def pick(self, cands: list[dict], n: int, exclude=(), strict: bool = True, wider: list[dict] | None = None,
             clash=None) -> list[dict]:
        """n items, least used first. strict: no shared key word and no ambiguity between items
        (needed wherever a word is filled in). wider: candidates to fall back on.
        clash(a, b): a further reason why two items must not share a sheet."""
        got = self._pick(cands, n, exclude, strict, clash)
        if not got and wider is not None:
            got = self._pick(wider, n, exclude, strict, clash)
        return got

    def _pick(self, cands, n, exclude, strict, clash=None):
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
            if clash and any(clash(k[3], c) for c in chosen):
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


def plan_chapter(ci: int, chapter: str, items: list[dict], stories: dict, known: set[str],
                 chapter_page: str = "") -> list[dict]:
    # a gap needs a real word: no one-letter key words ("Wer A sagt, muss auch B sagen"),
    # and words around it: no one-word idioms ("blaumachen") on gap, circle or wrong-word sheets
    story_id = stories[chapter]["item"]
    items = [i for i in items if (len(i["keyword"]) >= 3 and framed(i)) or i["id"] == story_id]
    pk = Picker(items, chapter, known)
    prov = [i for i in items if i["kind"] == "proverb"]
    idio = [i for i in items if i["kind"] == "idiom"]
    easy = sorted(items, key=ease)
    with_split = [p for p in prov if len(p.get("split") or []) == 2]
    complete2 = [p for p in prov if complete_ok(p, 2)]
    complete3 = [p for p in prov if complete_ok(p, 3)]
    page = attest.norm(chapter_page)
    on_chapter_page = {i["id"] for i in items if attest.norm(i["wording"]) in page}
    sheets, examples = [], set()

    def facing() -> set:
        """Sayings printed on the page the next worksheet faces: the leader page of the
        sheet before it, or the chapter page for the first sheet."""
        return set(sheets[-1]["items"]) if sheets else set(on_chapter_page)

    def fam3(cands: list[dict], n: int) -> list[dict]:
        """Level 1: only sayings everybody knows, where there are enough of them."""
        best = [c for c in cands if c["familiarity"] >= 3]
        return best if len(best) >= n + 2 else cands

    def add(typ, level, chosen, example=None, **extra):
        if not chosen:
            raise RuntimeError(f"{chapter}: not enough items for {typ} level {level}")
        if example:
            examples.add(example["id"])
        sheets.append(dict(type=typ, level=level, chapter=chapter, items=[c["id"] for c in chosen],
                           example=example["id"] if example else None, **extra))
        return True

    def example_for(chosen, need=lambda i: True, clash=None):
        """A solved example: preferably a saying not used anywhere else in the chapter;
        it is then kept off later sheets, so no item comes pre-solved. Never the story's
        saying, never an example twice in a chapter."""
        ids = {c["id"] for c in chosen}
        kws = {text.letters_upper(c["keyword"]) for c in chosen}
        cands = [c for c in easy if c["id"] not in ids | examples | {story_id} and need(c)
                 and text.letters_upper(c["keyword"]) not in kws
                 and not any(conflict(c, x, known) for x in chosen)
                 and not (clash and any(clash(c, x) for x in chosen))]
        cands.sort(key=lambda c: (pk.uses[c["id"]] > 0, ease(c)))
        if not cands:
            return None
        pk.uses[cands[0]["id"]] += 5
        return cands[0]

    def pick(cands, n, exclude=(), **kw):
        """Never a saying from the facing page; drop the extra exclusions if they leave too few."""
        got = pk.pick(cands, n, exclude=facing() | set(exclude), **kw)
        if not got and exclude:
            got = pk.pick(cands, n, exclude=facing(), **kw)
        return got

    def ids_of(*positions):
        return {i for p in positions if p < len(sheets) for i in sheets[p]["items"]}

    before_story = {story_id}
    # 1 ◆ gaps with word bank (theme word if possible)
    cat = THEME_WORD.get(chapter)
    themed = [i for i in items if cat and i.get("category") == cat[0]]
    if cat and len(themed) >= N_ITEMS[1] + 1:
        ch = pick(fam3(sorted(themed, key=ease), N_ITEMS[1])[:12], N_ITEMS[1], before_story, wider=themed)
        add("gaps", 1, ch, example_for(ch, lambda i: i.get("category") == cat[0]), category=cat[1])
    else:
        ch = pick(fam3(easy, N_ITEMS[1])[:14], N_ITEMS[1], before_story, wider=easy)
        add("gaps", 1, ch, example_for(ch))
    with_decoys = [i for i in easy if len(i.get("decoys") or []) >= 2]
    with_swap = [i for i in easy if swap_ok(i)]
    # 2 ◆ circle, two words
    ch = pick(fam3(with_decoys, N_ITEMS[1])[:16], N_ITEMS[1], before_story, wider=with_decoys, clash=circle_clash(2))
    add("circle", 1, ch, example_for(ch, lambda i: len(i.get("decoys") or []) >= 2, clash=circle_clash(2)))
    # 3 ◆ match halves (5) or saying <-> meaning
    if len(with_split) >= 7:
        add("match", 1, pick(fam3(sorted(with_split, key=ease), 5)[:12], 5, before_story, strict=False,
                             wider=with_split, clash=match_clash))
    else:
        add("match_meaning", 1, pick(fam3(sorted(idio, key=ease), 5)[:12], 5, before_story, strict=False, wider=idio))
    # 4 ◆ story (its saying is kept off sheets 1-3, see above)
    st = stories[chapter]
    if story_id in ids_of(2):
        raise RuntimeError(f"{chapter}: the story's saying is on the sheet it faces")
    add("story", 1, [next(i for i in items if i["id"] == story_id)], story=st)
    # 5 ◆◆ wrong word (every sentence with a different wrong word)
    seen_wrong, swap_pool = set(), []
    for i in with_swap:
        w = i["swap"]["wrong"].lower()
        if w not in seen_wrong:
            seen_wrong.add(w)
            swap_pool.append(i)
    ch = pick(swap_pool[:20], N_ITEMS[2], strict=False, wider=swap_pool, clash=wrong_clash)
    add("wrong", 2, ch, example_for(ch, swap_ok, clash=wrong_clash))
    # 6 ◆◆ letter boxes or three words (not the sayings of sheet 2 or of the story again)
    if ci % 2 == 0:
        ch = pick(items, N_ITEMS[2], ids_of(0) | {story_id})
        add("gaps", 2, ch, example_for(ch))
    else:
        ch = pick(with_decoys, N_ITEMS[2], ids_of(1) | {story_id}, clash=circle_clash(3))
        add("circle", 2, ch, example_for(ch, lambda i: len(i.get("decoys") or []) >= 2, clash=circle_clash(3)))
    # 7 ◆◆ meaning (idioms) or situation (proverbs)
    want_meaning = (ci % 2 == 0 and len(idio) >= 4) or len([p for p in prov if p.get("situation")]) < 3
    if want_meaning:
        add("choice", 2, pick(idio, 3, strict=False))
    else:
        add("situation", 2, pick([p for p in prov if p.get("situation")], 3, strict=False))
    # 8 ◆◆ rotating (chapters 3 and 9 get a Wortsalat instead of a second matching sheet) and
    # 9 ◆◆◆ complete or scramble, never the same type as sheet 8: the first combination that
    # works (small chapters run short of sayings once the facing-page rule applies)
    short = [p for p in prov if 3 <= len(text.words(p["wording"])) <= 6]
    longer = [p for p in prov if 5 <= len(text.words(p["wording"])) <= 9]
    rot8 = ["scramble", "complete", "match"][ci % 3]
    if ci in (2, 8):
        rot8 = "scramble"

    def sheet8(t8):
        if t8 == "scramble" and len(short) >= 8:
            ch = pick(short, N_ITEMS[2], strict=False)
            return ch and add("scramble", 2, ch, example_for(ch, lambda i: i in short))
        if t8 == "complete" and len(complete2) >= 8:
            ch = pick(complete2, N_ITEMS[2], strict=False)
            return ch and add("complete", 2, ch, example_for(ch, lambda i: i in complete2))
        if t8 == "match":
            if len(with_split) >= 6:
                ch = pick(with_split, 6, ids_of(2), strict=False, clash=match_clash)
                return ch and add("match", 2, ch)
            ch = pick(idio, 6, ids_of(2), strict=False)
            return ch and add("match_meaning", 2, ch)
        return False

    def sheet9(t8):
        for n in (6, 5):
            for t9 in ("complete", "scramble"):
                if t9 != t8:
                    ch = pick(complete3 if t9 == "complete" else longer, n, strict=False)
                    if ch:
                        return add(t9, 3, ch)
        return False

    for t8 in [rot8] + [t for t in ("scramble", "complete", "match") if t != rot8]:
        saved = (copy.deepcopy(pk.uses), pk.rnd.getstate(), len(sheets), set(examples))
        if sheet8(t8) and sheet9(t8):
            break
        pk.uses, examples = saved[0], saved[3]
        pk.rnd.setstate(saved[1])
        del sheets[saved[2]:]
    else:       # a small chapter: sheet 9 asks for single words instead
        if not any(sheet8(t) for t in [rot8] + [t for t in ("scramble", "complete", "match") if t != rot8]):
            raise RuntimeError(f"{chapter}: no sheet 8")
        add("gaps", 3, pick(items, N_ITEMS[3], ids_of(0, 1, 5)))
    # 10 ◆◆◆ rotating; free gaps only where sheet 6 had no letter boxes, and with sayings
    # that were not gaps on the level-1 sheets already
    rot10 = {0: "firstletters", 1: "wordsearch", 2: "firstletters", 3: "gaps", 4: "wordsearch",
             5: "gaps", 6: "firstletters", 7: "wordsearch", 8: "firstletters", 9: "gaps"}[ci % 10]
    fit_ws = [i for i in items if len(text.letters_upper(i["keyword"])) <= 10]
    if rot10 == "gaps" and sheets[-1]["type"] == "gaps":
        rot10 = "firstletters"
    if rot10 == "wordsearch" and len(fit_ws) >= 8:
        add("wordsearch", 3, pick(fit_ws, 8, wider=None))
    elif rot10 == "firstletters" and len(prov) >= 6:
        add("firstletters", 3, pick(prov, 6, ids_of(2), strict=False))
    else:
        add("gaps", 3, pick(items, N_ITEMS[3], ids_of(0, 1, 5)))
    return sheets


def main():
    corpus = [i for i in json.load(open(os.path.join(DATA, "corpus.json")))["items"] if i.get("keep", True)]
    stories = {s["chapter"]: s for s in json.load(open(os.path.join(DATA, "stories.json")))["stories"]}
    chap = {c["name"]: c for c in json.load(open(os.path.join(DATA, "chapters.json")))["chapters"]}
    out = []
    known = _known_sayings(corpus)
    for ci, chapter in enumerate(CHAPTERS):
        items = [i for i in corpus if i["chapter"] == chapter]
        c = chap[chapter]
        page = " ".join(c["talk"] + c["move"] + c["props"])
        out.extend(plan_chapter(ci, chapter, items, stories, known, page))
    for n, s in enumerate(out, 1):
        s["num"] = n
    lv = collections.Counter(s["level"] for s in out)
    ty = collections.Counter(s["type"] for s in out)
    print(f"{len(out)} sheets; levels {dict(sorted(lv.items()))}; types {dict(ty)}", file=sys.stderr)
    with open(os.path.join(DATA, "sheets.json"), "w") as f:
        json.dump({"sheets": out}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
