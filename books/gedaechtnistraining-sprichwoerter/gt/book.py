"""Assemble the interior PDF.

    python3 -m gt.book            -> build/book/interior.pdf

data/corpus.json + data/sheets.json (gt.plan) + data/stories.json + data/chapters.json
-> build/book/data.json -> layout/main.typ (Typst) -> PDF.
Every unit is one leaf: the worksheet (Kopiervorlage) on the right-hand page, the group
leader's page with solutions, hints and prompts on its back.
"""
from __future__ import annotations

import collections
import json
import os
import sys

import typst

from . import config, exercises as ex, extras, leader, text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build", "book")
HINT_TYPES = {"gaps", "circle", "wordsearch"}
TYPE_NAMES = {"gaps": "Was fehlt?", "circle": "Das richtige Wort", "match": "Was gehört zusammen?",
              "complete": "Wie geht es weiter?", "scramble": "Wortsalat", "wrong": "Da stimmt was nicht!",
              "firstletters": "Erste Buchstaben", "choice": "Was bedeutet das?", "situation": "Wann sagt man das?",
              "wordsearch": "Wörter suchen", "story": "Vorlesegeschichten"}


def _load(name):
    return json.load(open(os.path.join(ROOT, "data", name)))


def typo(s: str) -> str:
    """Straight quotes and apostrophes -> German typographic ones."""
    out, open_q = [], True
    for ch in s:
        if ch == '"':
            out.append("„" if open_q else "“")
            open_q = not open_q
        elif ch == "'":
            out.append("’")
        else:
            out.append(ch)
    return "".join(out)


def make_sheet(spec: dict, by_id: dict, pool: list[dict], drop: int = 0) -> dict:
    avoid = {i["id"]: i.get("avoid_with", []) for i in pool if i.get("avoid_with")}
    ids = spec["items"][: len(spec["items"]) - drop] if drop else spec["items"]
    if len(ids) < 3 and spec["type"] != "story":
        raise RuntimeError(f"Blatt {spec['num']}: does not fit on the page even with {len(ids)} items")
    spec = dict(spec, items=ids)
    items = [by_id[i] for i in ids]
    exm = by_id.get(spec.get("example"))
    seed = f"{spec['num']}:{spec['type']}"
    t, lv = spec["type"], spec["level"]
    if t == "gaps":
        cat = spec.get("category")
        title = f"Welches {cat} fehlt?" if cat and cat != "Wort" else "Was fehlt?"
        if cat == "Körperteil":
            title = "Welcher Körperteil fehlt?"
        s = ex.gaps(items, lv, seed, example=exm, title=title,
                    category=("Tier" if cat == "Tier" else None))
        if cat == "Körperteil":
            s["task"] = s["task"].replace("Welches Wort fehlt?", "Welcher Körperteil fehlt?")
    elif t == "circle":
        s = ex.circle(items, lv, seed, example=exm)
    elif t == "match":
        s = ex.match(items, lv, seed)
    elif t == "match_meaning":
        s = ex.match_meaning(items, lv, seed)
    elif t == "complete":
        s = ex.complete(items, lv, seed, example=exm)
    elif t == "scramble":
        s = ex.scramble(items, lv, seed, example=exm)
    elif t == "wrong":
        s = ex.wrongword(items, lv, seed, example=exm)
    elif t == "firstletters":
        s = ex.firstletters(items, lv, seed)
    elif t == "choice":
        s = ex.meaning(items, lv, seed, pool, avoid=avoid)
    elif t == "situation":
        s = ex.situation(items, lv, seed, pool, avoid=avoid)
    elif t == "wordsearch":
        s = ex.wsearch(items, lv, seed)
    elif t == "story":
        s = ex.story(items[0], spec["story"], lv, seed)
    else:
        raise ValueError(t)
    s.update(num=spec["num"], chapter=spec["chapter"], item_ids=spec["items"], example_id=spec.get("example"))
    return s


def _content_words(p: str) -> set[str]:
    stop = {"sie", "ihnen", "ihr", "ihre", "was", "wie", "welche", "welcher", "welches", "welchen", "haben", "sind",
            "meinen", "eher", "lieber", "oder", "und", "der", "die", "das", "den", "dem", "ein", "eine", "einen",
            "mit", "von", "zu", "für", "früher", "einmal", "gern", "besonders", "man", "es", "ist", "am", "im", "in"}
    return {w.lower()[:6] for w in text.words(p) if w.lower() not in stop and len(w) > 2}


def similar(p: str, q: str) -> bool:
    a, b = _content_words(p), _content_words(q)
    return bool(a and b) and len(a & b) / min(len(a), len(b)) >= 0.6


def leader_page(s: dict, items: list[dict], used_prompts: list, chapter_pool: list[dict], story: dict | None) -> dict:
    """The back of a worksheet. Prompts come from the sheet's own sayings (for a story: the
    story's own prompts first); a prompt that repeats or closely resembles one already used
    anywhere in the book is skipped. Only if fewer than two remain do other sayings of the
    chapter fill the gap, so the questions stay with what the group has just done."""
    typ = s["type"]
    own = list(story.get("prompts", [])) if story else []
    for it in items:
        own += it.get("prompts", [])[:1]
    for it in items:
        own += it.get("prompts", [])[1:]
    prompts = []
    for pool, limit in ((own, 3), ([p for it in chapter_pool for p in it.get("prompts", [])], 2)):
        for p in pool:
            if len(prompts) >= limit:
                break
            if any(similar(p, q) for q in used_prompts + prompts):
                continue
            prompts.append(p)
    used_prompts.extend(prompts)
    hints = [it["hint"] for it in items if it.get("hint")] if typ in HINT_TYPES else []
    if typ in HINT_TYPES and len(hints) != len(items):
        hints = [it.get("hint") or "–" for it in items]
    if typ == "story":
        hints = [items[0]["hint"]] if items[0].get("hint") else []
    hints_title, hints_intro = "Hilfen, wenn ein Wort nicht einfällt", ""
    if typ == "wordsearch":
        hints_title, hints_intro = "Wo die Wörter stehen", "Zeile 1 ist oben, Spalte 1 ist links."
        nb = "\u00a0"
        hints = [f"{p['word']}: Zeile{nb}{p['row'] + 1}, Spalte{nb}{p['col'] + 1}, nach{nb}"
                 + ("rechts" if p["dc"] else "unten") for p in s["places"]]
    # care notes: one per kind of concern; sayings with the same concern share one note
    notes = []                                           # [[sayings], note]
    if story and story.get("note"):
        notes.append([[], story["note"]])
    for it in items:
        n = it.get("note")
        if not n:
            continue
        for entry in notes:
            if entry[0] and similar(n, entry[1]):
                entry[0].append(it["wording"])
                break
        else:
            notes.append([[it["wording"]], n])
    notes = [(" und ".join(f"„{ex.cap(w)}“" for w in ws) + ": " if ws else "") + n for ws, n in notes[:3]]
    return {
        "num": s["num"], "level": s["level"], "title": s["title"], "chapter": s["chapter"],
        "minutes": leader.MINUTES[s["level"]] if typ != "story" else "10 bis 15",
        "trains": leader.TRAINS[typ],
        "steps": leader.pick(leader.STEPS, typ, s["level"]),
        "solution": s["solution"], "hints": hints, "hints_title": hints_title, "hints_intro": hints_intro,
        "prompts": [typo(p) for p in prompts],
        "easier": leader.pick(leader.EASIER, typ, s["level"]), "harder": leader.pick(leader.HARDER, typ, s["level"]),
        "notes": notes, "note": " ".join(notes),
    }


def warmup(items: list[dict], n: int = 8) -> list[dict]:
    prov = sorted([i for i in items if i["kind"] == "proverb" and len(i.get("split") or []) == 2],
                  key=lambda i: (-i["familiarity"], len(i["wording"])))
    return [{"a": p["split"][0] + " …", "b": p["split"][1], "id": p["id"]} for p in prov[:n]]


def index_key(w: str) -> str:
    skip = {"jemandem", "jemanden", "jemandes", "etwas", "sich", "der", "die", "das", "den", "dem", "ein", "eine", "einen"}
    ws = text.words(w)
    while len(ws) > 1 and ws[0].lower() in skip:
        ws = ws[1:]
    k = " ".join(ws).lower()
    return k.translate(str.maketrans({"ä": "a", "ö": "o", "ü": "u", "ß": "ss"}))


def build_data(flags: dict | None = None) -> dict:
    flags = flags or {}
    corpus = [i for i in _load("corpus.json")["items"] if i.get("keep", True)]
    by_id = {i["id"]: i for i in corpus}
    specs = _load("sheets.json")["sheets"]
    chapters = _load("chapters.json")["chapters"]
    chap_by = {c["name"]: c for c in chapters}
    units = []
    used = [typo(t) for c in chapters for t in c["talk"]]      # never repeat a chapter-page question
    for spec in specs:
        s = make_sheet(spec, by_id, corpus, drop=flags.get(str(spec["num"]), {}).get("drop", 0))
        items = [by_id[i] for i in s["item_ids"]]
        pool = [i for i in corpus if i["chapter"] == spec["chapter"] and i["id"] not in s["item_ids"]]
        L = leader_page(s, items, used, pool, spec.get("story"))
        short = flags.get(str(s["num"]), {}).get("short", 0)
        # step by step until the leader page fits. What decides whether an answer counts
        # (accepted variants) and the care notes stay longest.
        if short >= 1:
            L["prompts"] = L["prompts"][:2]
        if short >= 2:
            L["easier"] = L["harder"] = ""
        if short >= 3:
            L["solution"] = [dict(x, variants=x.get("variants", [])[:1]) for x in L["solution"]]
        if short >= 4:
            L["prompts"] = L["prompts"][:1]
        if short >= 5 and s["type"] != "wordsearch":
            L["hints"] = []
        if short >= 6:
            L["note"] = " ".join(L["notes"][:1])
        if short >= 7:
            L["solution"] = [dict(x, variants=[]) for x in L["solution"]]
        units.append({"sheet": s, "leader": L})
    chs = []
    for k, c in enumerate(chapters, 1):
        mine = [u["sheet"] for u in units if u["sheet"]["chapter"] == c["name"]]
        items = [i for i in corpus if i["chapter"] == c["name"]]
        chs.append(dict(c, num=k, intro=typo(c["intro"]), talk=[typo(t) for t in c["talk"]],
                        move=[typo(m) for m in c["move"]], props=c["props"], warmup=warmup(items),
                        sheets=[{"num": s["num"], "title": s["title"], "level": s["level"]} for s in mine]))
    # the index: every saying printed in the book. Bold numbers: sheets where it is an answer
    # or the solved example; in brackets: sheets where it is only offered as a wrong choice.
    uses, also = collections.defaultdict(list), collections.defaultdict(list)
    for u in units:
        sh = u["sheet"]
        for i in sh["item_ids"] + ([sh["example_id"]] if sh.get("example_id") else []):
            if sh["num"] not in uses[i]:
                uses[i].append(sh["num"])
        for i in sh.get("shown_ids", []):
            if i not in sh["item_ids"]:
                also[i].append(sh["num"])
    warm = collections.defaultdict(list)
    for c in chs:
        for w in c["warmup"]:
            warm[w["id"]].append(c["num"])
    # extras at the back: bingo (sayings from the sheets) and read-aloud rounds
    shown = set(uses) | set(also)
    bingo = extras.bingo(corpus, set(uses), set(warm))
    rounds = extras.rounds(corpus, shown, set(warm))
    extra = collections.defaultdict(list)
    for k, r in enumerate(rounds["rounds"], 1):
        for w in r:
            extra[w["id"]].append(f"Raterunde {k}")
    ids = set(uses) | set(also) | set(warm) | set(extra)
    index = sorted(({"w": ex.cap(by_id[i]["wording"]) if by_id[i]["kind"] == "proverb" else by_id[i]["wording"],
                     "sheets": sorted(uses.get(i, [])), "also": sorted(set(also.get(i, [])) - set(uses.get(i, []))),
                     "chapters": warm.get(i, []) if not uses.get(i) else [], "extra": extra.get(i, []),
                     "m": typo(by_id[i]["meaning"]), "kind": by_id[i]["kind"], "id": i}
                    for i in ids),
                   key=lambda e: index_key(e["w"]))
    by_level = collections.defaultdict(list)
    by_type = collections.defaultdict(lambda: collections.defaultdict(list))
    for u in units:
        s = u["sheet"]
        by_level[str(s["level"])].append(s["num"])
        by_type[TYPE_NAMES.get(s["type"], s["title"])][s["level"]].append(s["num"])
    return {"title": config.TITLE, "subtitle": config.SUBTITLE, "series": config.SERIES, "volume": config.VOLUME,
            "author": config.AUTHOR, "year": config.YEAR, "release": config.release(),
            "chapters": chs, "units": units, "index": index, "bingo": bingo, "rounds": rounds["rounds"],
            "by_level": by_level,
            "by_type": [{"name": k, "nums": [n for lv in sorted(v) for n in v[lv]],
                         "levels": [{"level": lv, "nums": v[lv]} for lv in sorted(v)]} for k, v in by_type.items()],
            "n_sayings": len(index), "n_sheet_sayings": sum(1 for e in index if e["sheets"]),
            "pad_page": flags.get("pad_page", False)}


def compile_pdf(data: dict) -> str:
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, "data.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False)
    out = os.path.join(BUILD, "interior.pdf")
    try:
        typst.compile(os.path.join(ROOT, "layout", "main.typ"), output=out, root=ROOT,
                      font_paths=[os.path.join(ROOT, "fonts")], ignore_system_fonts=True)
    except typst.TypstError as e:
        print(e.diagnostic, file=sys.stderr)
        raise
    return out


def overflowing(pdf: str) -> list[int]:
    """Sheets whose leader page ran onto a second page (its next sheet is not 2 pages later)."""
    import pymupdf
    d = pymupdf.open(pdf)
    sheet_page, leader_page_ = {}, {}
    import re
    for i, p in enumerate(d):
        t = p.get_text()
        m = re.search(r"Kopiervorlage\s+Blatt (\d+)", t)
        if m:
            sheet_page.setdefault(int(m.group(1)), i)
        m = re.search(r"Für die Gruppenleitung\s+Blatt (\d+)", t)
        if m:
            leader_page_.setdefault(int(m.group(1)), i)
    bad = []
    for n, sp in sheet_page.items():
        lp = leader_page_.get(n)
        nxt = sheet_page.get(n + 1)
        if lp != sp + 1 or (nxt is not None and nxt != lp + 1 and not _chapter_between(d, lp, nxt)):
            bad.append(n)
    return bad


def _chapter_between(d, a, b) -> bool:
    import re
    return b == a + 3 and re.search(r"Zum\s+Aufwärmen", d[a + 1].get_text()) is not None


def sheet_overflow() -> list[int]:
    """Worksheets whose items do not fit on their page (Typst leaves an <overflow> mark)."""
    r = typst.query(os.path.join(ROOT, "layout", "main.typ"), "<overflow>", field="value", root=ROOT,
                    font_paths=[os.path.join(ROOT, "fonts")], ignore_system_fonts=True)
    return sorted(set(json.loads(r)))


def main():
    flags = {}
    for attempt in range(14):
        data = build_data(flags)
        out = compile_pdf(data)
        full = sheet_overflow()
        bad = overflowing(out)
        if not bad and not full:
            break
        if full:
            print(f"  worksheets too full, one item fewer: {full}", file=sys.stderr)
        if bad:
            print(f"  leader pages too long, shortening: {bad}", file=sys.stderr)
        for n in full:
            f = flags.setdefault(str(n), {})
            f["drop"] = f.get("drop", 0) + 1
        for n in bad:
            f = flags.setdefault(str(n), {})
            f["short"] = f.get("short", 0) + 1
    else:
        raise RuntimeError("layout did not settle")
    import pymupdf
    n = pymupdf.open(out).page_count
    if n % 2 and not flags.get("pad_page"):
        flags["pad_page"] = True
        out = compile_pdf(build_data(flags))
        n = pymupdf.open(out).page_count
    print(f"interior: {n} pages -> {os.path.relpath(out, ROOT)}", file=sys.stderr)
    return out


if __name__ == "__main__":
    main()
