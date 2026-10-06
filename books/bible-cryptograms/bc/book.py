"""Assemble the interior PDF.

    python3 -m bc.book            -> build/book/interior.pdf

Data flow: data/puzzles.json (+ data/selection.json for theme texts, data/hints.json,
data/reflections.json) -> build/book/data.json -> build/book/main.typ (Typst) -> PDF.
All prose pages are Typst files in content/.
"""
from __future__ import annotations

import collections
import json
import os
import shutil
import sys

import typst

from . import config, kjv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build", "book")
LEVEL_NAMES = {1: "Easy", 2: "Medium", 3: "Hard", 4: "Expert"}


def _load(name, default=None):
    path = os.path.join(ROOT, "data", name)
    if not os.path.exists(path):
        if default is not None:
            return default
        raise FileNotFoundError(path)
    return json.load(open(path))


def display_ref(ref: str) -> str:
    """'Psalms 23:1' -> 'Psalm 23:1' (one psalm); ranges use an en dash."""
    ref = ref.replace("Psalms ", "Psalm ")
    return ref.replace("-", "\u2013")


def cells(cipher: str, given: dict[str, str]):
    """Split the cipher into words; each word is a list of [code char, given letter or '', is_letter]."""
    out = []
    for w in cipher.split(" "):
        if not w:
            continue
        out.append([[ch, given.get(ch, ""), ch.isalpha()] for ch in w])
    return out


def build_data():
    pz = _load("puzzles.json")["puzzles"]
    sel = _load("selection.json")
    refl = {int(k): v for k, v in _load("reflections.json", {}).items()}
    themes = []
    for t in sel["themes"]:
        nums = [p["num"] for p in pz if p["theme"] == t["name"]]
        if not nums:
            continue
        themes.append({"name": t["name"], "intro": t.get("intro", ""), "first": min(nums), "last": max(nums)})
    puzzles = []
    for p in pz:
        counts = collections.Counter(c for c in p["cipher"] if c.isalpha())
        puzzles.append({
            "num": p["num"], "theme": p["theme"], "level": p["level"], "level_name": LEVEL_NAMES[p["level"]],
            "words": cells(p["cipher"], p["given"]),
            "counts": dict(counts), "given": p["given"],
            "given_list": [f"{c} = {v}" for c, v in sorted(p["given"].items())],
            "ref": display_ref(p["ref"]) + (" (part)" if p.get("partial") else ""),
            "text": ("\u2026" if p.get("starts_mid") else "") + p["text"] + ("\u2026" if p.get("ends_mid") else ""),
            "verse_text": p["text"], "book": p["book"],
            "chapter": kjv.parse_ref(p["ref"])[1], "verse": kjv.parse_ref(p["ref"])[2],
            "hints": p["hints"],
            "reflection": refl.get(p["num"], ""),
        })
    from . import cipher, example
    book_words = collections.Counter(w for p in pz for w in cipher.words(p["text"]))
    ranges = {}
    for p in puzzles:
        ranges.setdefault(str(p["level"]), []).append(len(p["given"]))
    given_ranges = {k: [min(v), max(v)] for k, v in ranges.items()}
    return {"example": example.build(), "stats": _load("kjv_stats.json"), "title": config.TITLE, "subtitle": config.SUBTITLE, "author": config.AUTHOR, "year": config.YEAR,
            "book_order": kjv.BOOKS, "themes": themes, "puzzles": puzzles, "given_ranges": given_ranges,
            "book_top_words": [w for w, _ in book_words.most_common(16)], "release": config.release()}


def main():
    os.makedirs(BUILD, exist_ok=True)
    data = build_data()
    with open(os.path.join(BUILD, "data.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False)
    main_typ = os.path.join(ROOT, "layout", "main.typ")
    out = os.path.join(BUILD, "interior.pdf")
    typst.compile(main_typ, output=out, root=ROOT, font_paths=[os.path.join(ROOT, "fonts")],
                  ignore_system_fonts=True)
    import pymupdf
    n = pymupdf.open(out).page_count
    print(f"interior: {n} pages -> {os.path.relpath(out, ROOT)}", file=sys.stderr)
    return out


if __name__ == "__main__":
    main()
