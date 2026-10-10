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

from . import config, exercises as ex, leader, text

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
        s = ex.meaning(items, lv, seed, pool)
    elif t == "situation":
        s = ex.situation(items, lv, seed, pool)
    elif t == "wordsearch":
        s = ex.wsearch(items, lv, seed)
    elif t == "story":
        s = ex.story(items[0], spec["story"], lv, seed)
    else:
        raise ValueError(t)
    s.update(num=spec["num"], chapter=spec["chapter"], item_ids=spec["items"])
    return s


def leader_page(s: dict, items: list[dict], used_prompts: set, chapter: dict) -> dict:
    typ = "match" if s["type"] == "match" else s["type"]
    prompts = []
    for it in items:
        for p in it.get("prompts", []):
            if p not in used_prompts and len(prompts) < 3:
                prompts.append(p)
                used_prompts.add(p)
                break
    for p in chapter["talk"]:
        if len(prompts) >= 3:
            break
        if p not in used_prompts and p not in prompts:
            prompts.append(p)
    hints = [it["hint"] for it in items] if s["type"] in HINT_TYPES else []
    if s["type"] == "story":
        hints = [items[0]["hint"]]
    notes = sorted({it["note"] for it in items if it.get("note")})
    return {
        "num": s["num"], "level": s["level"], "title": s["title"], "chapter": s["chapter"],
        "minutes": leader.MINUTES[s["level"]] if s["type"] != "story" else "10 bis 15",
        "trains": leader.TRAINS[typ],
        "steps": leader.pick(leader.STEPS, typ, s["level"]),
        "solution": s["solution"], "hints": hints, "prompts": [typo(p) for p in prompts],
        "easier": leader.pick(leader.EASIER, typ, s["level"]), "harder": leader.pick(leader.HARDER, typ, s["level"]),
        "note": " ".join(notes),
    }


def warmup(items: list[dict], n: int = 8) -> list[dict]:
    prov = sorted([i for i in items if i["kind"] == "proverb" and len(i.get("split") or []) == 2],
                  key=lambda i: (-i["familiarity"], len(i["wording"])))
    return [{"a": p["split"][0] + " …", "b": p["split"][1]} for p in prov[:n]]


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
    units, used = [], collections.defaultdict(set)
    for spec in specs:
        s = make_sheet(spec, by_id, corpus, drop=flags.get(str(spec["num"]), {}).get("drop", 0))
        items = [by_id[i] for i in s["item_ids"]]
        L = leader_page(s, items, used[spec["chapter"]], chap_by[spec["chapter"]])
        short = flags.get(str(s["num"]), {}).get("short", 0)
        if short >= 1:                       # step by step until the leader page fits
            L["prompts"] = L["prompts"][:2]
            L["easier"] = L["harder"] = ""
        if short >= 2:
            L["solution"] = [dict(x, variants=x.get("variants", [])[:1]) for x in L["solution"]]
        if short >= 3:
            L["hints"] = []
        units.append({"sheet": s, "leader": L})
    chs = []
    for k, c in enumerate(chapters, 1):
        mine = [u["sheet"] for u in units if u["sheet"]["chapter"] == c["name"]]
        items = [i for i in corpus if i["chapter"] == c["name"]]
        chs.append(dict(c, num=k, intro=typo(c["intro"]), talk=[typo(t) for t in c["talk"]],
                        move=[typo(m) for m in c["move"]], props=c["props"], warmup=warmup(items),
                        sheets=[{"num": s["num"], "title": s["title"], "level": s["level"]} for s in mine]))
    uses = collections.defaultdict(list)
    for u in units:
        for i in u["sheet"]["item_ids"]:
            if u["sheet"]["num"] not in uses[i]:
                uses[i].append(u["sheet"]["num"])
    index = sorted(({"w": ex.cap(by_id[i]["wording"]) if by_id[i]["kind"] == "proverb" else by_id[i]["wording"],
                     "sheets": v, "kind": by_id[i]["kind"]} for i, v in uses.items()),
                   key=lambda e: index_key(e["w"]))
    by_level = collections.defaultdict(list)
    by_type = collections.defaultdict(list)
    for u in units:
        s = u["sheet"]
        by_level[str(s["level"])].append(s["num"])
        by_type[TYPE_NAMES.get(s["type"], s["title"])].append(s["num"])
    return {"title": config.TITLE, "subtitle": config.SUBTITLE, "series": config.SERIES, "volume": config.VOLUME,
            "author": config.AUTHOR, "year": config.YEAR, "release": config.release(),
            "chapters": chs, "units": units, "index": index,
            "by_level": by_level, "by_type": [{"name": k, "nums": v} for k, v in by_type.items()],
            "n_sayings": len(uses), "pad_page": flags.get("pad_page", False)}


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
    for attempt in range(6):
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
