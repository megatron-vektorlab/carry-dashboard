"""Worksheet generators. Each takes corpus items (data/corpus.json) and returns a sheet:

    {"type", "title", "task", "level", "items": [...], "example": {...} | None,
     extra fields per type, "solution": [lines for the solutions pages]}

Rules from the practice research (README, "Fachliche Grundlagen"):
  * level 1 (one diamond): 5 items, a worked example, a word bank with exactly the missing
    words, or two options to circle;
  * level 2: 6 items, a worked example, first letter / three options / one extra word;
  * level 3: 8 items (fewer where the items are long), free recall;
  * no anagrams; word searches only left-to-right and top-to-bottom;
  * meaning questions use unrelated wrong answers, never a literal reading.
Everything is deterministic (seeded by the sheet id), so a rebuild gives the same book.
"""
from __future__ import annotations

import random
import re

from . import text, wordsearch

LETTERS = "ABCDEFGHIJ"
W = r"A-Za-zÄÖÜäöüß"


def _rnd(seed: str) -> random.Random:
    return random.Random("gt1:" + seed)


def _derange(n: int, rnd: random.Random) -> list[int]:
    """A shuffle where no position keeps its place."""
    while True:
        p = list(range(n))
        rnd.shuffle(p)
        if all(p[i] != i for i in range(n)):
            return p


def end_dot(s: str) -> str:
    return s if s.endswith(("!", "?", ".")) else s + "."


def cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def blank(wording: str, word: str) -> list[str]:
    """Split the wording around the last whole-word occurrence of `word` -> [before, after]."""
    ms = list(re.finditer(rf"(?<![{W}]){re.escape(word)}(?![{W}])", wording))
    if not ms:
        raise ValueError(f"{word!r} not in {wording!r}")
    m = ms[-1]
    return [wording[:m.start()].rstrip(), wording[m.end():].lstrip()]


def spaced(a: str, b: str) -> tuple[str, str]:
    """Spaces around a bold word: 'Morgenstund hat ' + Gold + ' im Mund'."""
    a = a + " " if a and not a.endswith((" ", "„", "(")) else a
    b = " " + b if b and b[0] not in ",.!?;:" else b
    return a, b


def _n(s: str) -> str:
    return re.sub(r"[^a-zäöüß ]+", "", re.sub(r"\s+", " ", s.lower())).strip()


def fitting_variants(it: dict, kind: str, word: str | None = None) -> list[str]:
    """Only variants that fit what the sheet already prints: same text around the gap
    (gaps, circle, story, wrong), same beginning (complete), same first letters."""
    out = []
    for v in it.get("variants", []):
        if kind in ("gap", "wrong"):
            w = word or it["keyword"]
            a, b = blank(it["wording"], w)
            if _n(v).startswith(_n(a)) and _n(v).endswith(_n(b)) and _n(v) != _n(it["wording"]):
                out.append(v)
        elif kind == "complete":
            if _n(v).startswith(_n(it["split"][0])):
                out.append(v)
        elif kind == "firstletters":
            if [x[0].lower() for x in text.words(v)] == [x[0].lower() for x in text.words(it["wording"])]:
                out.append(v)
    return out


def sol_word(it: dict, word: str | None = None) -> dict:
    """Solution line with the answer word in bold: {before, word, after} (spaces included)."""
    w = word or it["keyword"]
    a, b = spaced(*blank(it["wording"], w))
    if it.get("kind") == "proverb":
        b = end_dot(b) if b else "."
    return {"before": a, "word": w, "after": b, "variants": fitting_variants(it, "gap", w)}


def sol_full(it: dict, prefix: str = "", kind: str = "") -> dict:
    return {"before": prefix, "word": "", "after": end_dot(it["wording"]) if it.get("kind") == "proverb" else it["wording"],
            "variants": fitting_variants(it, kind) if kind else []}


def _gap(it: dict, level: int, word: str | None = None) -> dict:
    k = word or it["keyword"]
    g = {"parts": blank(it["wording"], k), "gap": max(6, min(12, len(k) + 2))}
    if level == 2:
        g.update(boxes=len(k), first=k[0])     # one box per letter, the first one filled in
    return g


def _example(kind: str, it: dict | None, **kw) -> dict | None:
    return None if it is None else dict(kind=kind, **kw)


# ---------------------------------------------------------------- one word missing

def gaps(items, level, seed, example=None, title="Was fehlt?", category=None):
    """One key word is missing. Level 1: word bank with exactly these words;
    level 2: a box per letter, the first one filled in; level 3: a free line."""
    rnd = _rnd(seed)
    bank = [it["keyword"] for it in items]
    rnd.shuffle(bank)
    tasks = {1: "Welches Wort fehlt? Die Wörter im Kasten helfen Ihnen.",
             2: "Welches Wort fehlt? Für jeden Buchstaben gibt es ein Kästchen, der erste steht schon da.",
             3: "Welches Wort fehlt? Schreiben Sie es auf die Linie."}
    if category:
        tasks = {1: f"Welches {category} fehlt? Die Wörter im Kasten helfen Ihnen.",
                 2: f"Welches {category} fehlt? Für jeden Buchstaben gibt es ein Kästchen, der erste steht schon da.",
                 3: f"Welches {category} fehlt? Schreiben Sie es auf die Linie."}
    ex = None
    if example is not None and level < 3:
        ex = {"parts": blank(example["wording"], example["keyword"]), "answer": example["keyword"]}
    sheet = {"type": "gaps", "title": title, "level": level, "task": tasks[level], "example": ex,
             "items": [_gap(it, level) for it in items], "solution": [sol_word(it) for it in items]}
    if level == 1:
        sheet["bank"] = bank
    return sheet


def circle(items, level, seed, example=None):
    """Kreisen Sie das richtige Wort ein: two (level 1) or three (level 2) words to choose from."""
    rnd = _rnd(seed)
    n = 2 if level == 1 else 3
    out = []
    for it in items:
        opts = [it["keyword"]] + it["decoys"][: n - 1]
        rnd.shuffle(opts)
        out.append({"parts": blank(it["wording"], it["keyword"]), "options": opts})
    ex = None
    if example is not None:
        opts = [example["keyword"]] + example["decoys"][: n - 1]
        rnd.shuffle(opts)
        ex = {"parts": blank(example["wording"], example["keyword"]), "options": opts, "answer": example["keyword"]}
    return {"type": "circle", "title": "Das richtige Wort", "level": level, "items": out, "example": ex,
            "task": "Welches Wort ist richtig? Kreisen Sie es ein.",
            "solution": [sol_word(it) for it in items]}


# ---------------------------------------------------------------- whole proverbs

def match(items, level, seed, example=None):
    """Was gehört zusammen? Beginnings numbered on the left, endings lettered on the right."""
    rnd = _rnd(seed)
    perm = _derange(len(items), rnd)
    left = [it["split"][0] for it in items]
    right = [items[perm[i]]["split"][1] for i in range(len(items))]   # right[i] belongs to items[perm[i]]
    answer = {perm[i]: LETTERS[i] for i in range(len(items))}         # item index -> letter
    return {"type": "match", "title": "Was gehört zusammen?", "level": level, "left": left, "right": right,
            "items": [], "example": None,
            "task": "Verbinden Sie Anfang und Ende mit einem Strich.",
            "solution": [sol_full(it, f"{answer[i]} – ") for i, it in enumerate(items)]}


def complete(items, level, seed, example=None):
    """Wie geht es weiter? The beginning is printed, the reader writes the end
    (level 2: the first word of the end is given)."""
    out = []
    for it in items:
        a, b = it["split"]
        out.append({"start": a + " …", "hint": text.words(b)[0] + " …" if level == 2 else "",
                    "long": len(b) > 30})
    ex = None
    if example is not None and level < 3:
        b = example["split"][1]
        first = text.words(b)[0] if level == 2 else ""
        ex = {"start": example["split"][0] + " …", "given": first, "answer": b[len(first):].strip() if first else b}
    return {"type": "complete", "title": "Wie geht es weiter?", "level": level, "items": out, "example": ex,
            "task": {2: "Wie geht das Sprichwort weiter? Das erste Wort steht schon da.",
                     3: "Wie geht das Sprichwort weiter? Schreiben Sie das Ende auf."}.get(level, "Wie geht es weiter?"),
            "solution": [sol_full(it, kind="complete") for it in items]}


def scramble(items, level, seed, example=None):
    """Wortsalat. Level 2: short sayings, the first word is already on the line."""
    rnd = _rnd(seed)
    out = []
    for it in items:
        w = text.words(it["wording"])
        rest = list(range(1, len(w))) if level == 2 else list(range(len(w)))
        order = list(rest)
        for _ in range(50):
            rnd.shuffle(order)
            if order != rest:
                break
        out.append({"tiles": [w[i] for i in order], "first": w[0] if level == 2 else "",
                    "long": len(it["wording"]) > 40})
    ex = None
    if example is not None and level < 3:
        w = text.words(example["wording"])
        order = list(range(1, len(w)))
        rnd.shuffle(order)
        ex = {"tiles": [w[i] for i in order], "first": w[0], "answer": end_dot(example["wording"])}
    return {"type": "scramble", "title": "Wortsalat", "level": level, "items": out, "example": ex,
            "task": {2: "Die Wörter sind durcheinander. Das erste Wort steht schon auf der Linie.",
                     3: "Die Wörter sind durcheinander. Schreiben Sie das Sprichwort richtig auf."}[level],
            "solution": [sol_full(it) for it in items]}


def wrongword(items, level, seed, example=None):
    """Da stimmt was nicht! One word was swapped for a wrong one."""
    def parts(it):
        sw = it["swap"]
        a, b = spaced(*blank(it["wording"], sw["right"]))
        if a:
            a = cap(a)
            wrong = sw["wrong"]
        else:
            wrong = cap(sw["wrong"])
        return [a, wrong, b]
    out = [{"shown": "".join(parts(it)), "parts": parts(it)} for it in items]
    ex = None
    if example is not None and level < 3:
        ex = {"parts": parts(example), "answer": example["swap"]["right"]}
    sol = []
    for it in items:
        sw = it["swap"]
        alts = []
        for v in fitting_variants(it, "wrong", sw["right"]):
            a, b = blank(it["wording"], sw["right"])
            mid = re.sub(r"\s+", " ", v)[len(a):len(v) - len(b) if b else None].strip(" ,.")
            if mid and mid != sw["right"]:
                alts.append(mid)
        sol.append({"before": sw["wrong"] + " → ", "word": sw["right"],
                    "after": (f" (auch: {' / '.join(alts)})" if alts else "") + ": " + end_dot(cap(it["wording"])),
                    "variants": []})
    return {"type": "wrong", "title": "Da stimmt was nicht!", "level": level, "items": out, "example": ex,
            "task": "In jedem Satz ist ein Wort falsch. Streichen Sie es durch und schreiben Sie das richtige Wort auf.",
            "solution": sol}


def firstletters(items, level, seed, example=None):
    """Only the first letter of every word is printed; the line is as long as the word."""
    out = []
    for it in items:
        stubs = []
        for tok in re.findall(rf"[{W}]+|[,.!?;:]", it["wording"]):
            if tok[0].isalpha():
                stubs.append({"first": tok[0], "len": len(tok)})
            elif stubs:
                stubs[-1]["punct"] = stubs[-1].get("punct", "") + tok
        out.append({"stubs": stubs, "long": len(it["wording"]) > 40})
    return {"type": "firstletters", "title": "Erste Buchstaben", "level": level, "items": out, "example": None,
            "task": "Von jedem Wort steht nur der erste Buchstabe da. Welches Sprichwort ist es?",
            "solution": [sol_full(it, kind="firstletters") for it in items]}


# ---------------------------------------------------------------- meaning

_STOP = set("""der die das den dem des ein eine einen einem einer eines und oder aber nicht kein keine keinen
man sich sie er es wir ihr ich du jemand jemanden jemandem etwas sehr viel viele mehr ist sind hat haben wird werden
mit von zu zum zur bei für auf aus an in im am um als wie was wer wenn dass so auch nur noch schon ganz immer oft
alles alle allem andere anderen anderer anderes selbst sein seine seinen seinem seiner gut gute guten dann kann muss""".split())


def _content(s: str) -> set[str]:
    return {w.lower()[:5] for w in text.words(s) if w.lower() not in _STOP and len(w) > 2}


def _distractors(it, pool, used, field, n, rnd, avoid=None):
    mine = _content(it[field]) | _content(it["wording"])
    bad = set((avoid or {}).get(it["id"], []))
    cands = [p for p in pool if p["id"] not in used and p["id"] != it["id"] and p["kind"] == it["kind"] and p["id"] not in bad
             and p["chapter"] != it["chapter"] and not (_content(p[field]) & mine)]
    rnd.shuffle(cands)
    picks = []
    for c in cands:
        if all(not (_content(c[field]) & _content(x[field])) for x in picks):
            picks.append(c)
        if len(picks) == n:
            break
    if len(picks) < n:
        raise RuntimeError(f"not enough distractors for {it['wording']}")
    return picks


def meaning(items, level, seed, pool, example=None, avoid=None):
    """Was bedeutet das? Three explanations, one is right; the wrong ones are meanings of
    unrelated sayings from other chapters (never a literal reading). The right answer moves
    between a), b) and c) so that it cannot be guessed from a pattern."""
    rnd = _rnd(seed)
    out, sol, out_right = [], [], []
    used = {it["id"] for it in items}
    for it in items:
        picks = _distractors(it, pool, used, "meaning", 2, rnd, avoid)
        used.update(p["id"] for p in picks)
        wrong = [p["meaning"] for p in picks]
        rnd.shuffle(wrong)
        right = rnd.randrange(3) if not out_right else (out_right[-1] + 1 + rnd.randrange(2)) % 3
        opts = wrong[:right] + [it["meaning"]] + wrong[right:]
        out_right.append(right)
        out.append({"phrase": cap(it["wording"]), "options": [cap(o) for o in opts]})
        sol.append({"before": cap(it["wording"]) + ": ", "word": "abc"[right] + ")", "after": " " + cap(it["meaning"]), "variants": []})
    return {"type": "choice", "title": "Was bedeutet das?", "level": level, "items": out, "example": None,
            "task": "Was ist damit gemeint? Kreuzen Sie an.", "solution": sol}


def situation(items, level, seed, pool, example=None, avoid=None):
    """Wann sagt man das? An everyday scene and three sayings; one fits."""
    rnd = _rnd(seed)
    out, sol, out_right = [], [], []
    used = {it["id"] for it in items}
    for it in items:
        picks = _distractors(it, pool, used, "meaning", 2, rnd, avoid)
        used.update(p["id"] for p in picks)
        wrong = [p["wording"] for p in picks]
        rnd.shuffle(wrong)
        right = rnd.randrange(3) if not out_right else (out_right[-1] + 1 + rnd.randrange(2)) % 3
        opts = wrong[:right] + [it["wording"]] + wrong[right:]
        out_right.append(right)
        out.append({"phrase": it["situation"], "options": [end_dot(cap(o)) for o in opts]})
        sol.append({"before": "", "word": "abc"[right] + ")", "after": " " + end_dot(cap(it["wording"])), "variants": []})
    return {"type": "situation", "title": "Wann sagt man das?", "level": level, "items": out, "example": None,
            "shown_ids": sorted(used),
            "task": "Welches Sprichwort passt? Kreuzen Sie an.", "solution": sol}


# ---------------------------------------------------------------- word search

def wsearch(items, level, seed, size=10):
    """Suchsel: the key words of the chapter, left-to-right and top-to-bottom only."""
    words = [text.letters_upper(it["keyword"]) for it in items]
    g = wordsearch.make(words, size, 2, seed)
    return {"type": "wordsearch", "title": "Wörter suchen", "level": level, "grid": g["grid"], "places": g["places"],
            "words": words, "items": [], "example": None,
            "task": "Finden Sie die Wörter im Gitter. Sie stehen von links nach rechts oder von oben nach unten.",
            "solution": [sol_word(it) for it in items]}


def match_meaning(items, level, seed, example=None):
    """Was gehört zusammen? Sayings on the left, their meanings on the right."""
    rnd = _rnd(seed)
    perm = _derange(len(items), rnd)
    left = [cap(it["wording"]) for it in items]
    right = [cap(items[perm[i]]["meaning"]) for i in range(len(items))]
    answer = {perm[i]: LETTERS[i] for i in range(len(items))}
    return {"type": "match", "title": "Was gehört zusammen?", "level": level, "left": left, "right": right,
            "items": [], "example": None, "wide_right": True,
            "task": "Was ist gemeint? Verbinden Sie jede Redewendung mit ihrer Bedeutung.",
            "solution": [{"before": f"{answer[i]} – ", "word": "", "after": f"{cap(it['wording'])}: {cap(it['meaning'])}",
                          "variants": []} for i, it in enumerate(items)]}


def story(it, st, level, seed):
    """Vorlesegeschichte: a short story whose last sentence is the proverb; its key word is
    missing and three words are offered."""
    rnd = _rnd(seed)
    ending = st["ending"]
    if it["wording"].rstrip(".!") not in ending:
        raise ValueError(f"story {st['title']!r} does not end with {it['wording']!r}")
    opts = [it["keyword"]] + it["decoys"][:2]
    rnd.shuffle(opts)
    return {"type": "story", "title": st["title"], "level": level, "items": [], "example": None,
            "paragraphs": st["paragraphs"], "parts": blank(ending, it["keyword"]), "options": opts,
            "task": "Hören Sie zu oder lesen Sie mit. Welches Wort fehlt am Ende? Kreisen Sie es ein.",
            "solution": [dict(zip(("before", "after"), spaced(*blank(ending, it["keyword"]))), word=it["keyword"],
                              variants=[])]}
