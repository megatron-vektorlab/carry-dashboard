"""King James Version text from five independent public-domain copies.

    python3 -m bc.kjv download     # fetch the five copies into sources_cache/ (not committed)
    python3 -m bc.kjv stats        # how often the copies agree, over the whole Bible

The model never types a verse.  Every verse in the book is looked up by reference in
these files; the text used is the one most copies agree on (see `verse`).  Checksums of
the downloaded files are written to data/sources.json so the build is reproducible.
"""
from __future__ import annotations

import collections
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "sources_cache")
RAW = "https://raw.githubusercontent.com"

BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth",
    "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon",
    "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah",
    "Malachi", "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians",
    "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians",
    "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation",
]

SOURCES = {
    # key: (description, list of (url, local file))
    "farskipper": ("farskipper/kjv, verses-1769.json (1769 text, italics in [ ])",
                   [(f"{RAW}/farskipper/kjv/master/json/verses-1769.json", "farskipper_verses-1769.json")]),
    "thiagobodruk": ("thiagobodruk/bible, json/en_kjv.json",
                     [(f"{RAW}/thiagobodruk/bible/master/json/en_kjv.json", "thiagobodruk_en_kjv.json")]),
    "aruljohn": ("aruljohn/Bible-kjv, one JSON file per book",
                 [(f"{RAW}/aruljohn/Bible-kjv/master/{b.replace(' ', '')}.json", f"aruljohn/{b.replace(' ', '')}.json")
                  for b in BOOKS]),
    "bibleapi": ("bibleapi/bibleapi-bibles-json, kjv.json",
                 [(f"{RAW}/bibleapi/bibleapi-bibles-json/master/kjv.json", "bibleapi_kjv.json")]),
    "scrollmapper": ("scrollmapper/bible_databases, sources/en/KJV/KJV.json (Psalm titles inside verse 1)",
                     [(f"{RAW}/scrollmapper/bible_databases/master/sources/en/KJV/KJV.json", "scrollmapper_KJV.json")]),
}
# When copies disagree and there is no majority, prefer the earlier source in this list.
PREFERENCE = ["farskipper", "thiagobodruk", "aruljohn", "bibleapi", "scrollmapper"]


def download():
    os.makedirs(os.path.join(CACHE, "aruljohn"), exist_ok=True)
    for key, (_, files) in SOURCES.items():
        for url, local in files:
            path = os.path.join(CACHE, local)
            if not os.path.exists(path):
                subprocess.run(["curl", "-sSfL", "--retry", "4", "-o", path, url], check=True)
    meta = {}
    for key, (desc, files) in SOURCES.items():
        h = hashlib.sha256()
        for _, local in files:
            with open(os.path.join(CACHE, local), "rb") as f:
                h.update(f.read())
        meta[key] = {"description": desc, "urls": [u for u, _ in files][:1] + ([f"... ({len(files)} files)"] if len(files) > 1 else []),
                     "sha256": h.hexdigest()}
    with open(os.path.join(ROOT, "data", "sources.json"), "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")


def _clean(text: str) -> str:
    """Remove edition markup but keep every letter and punctuation mark."""
    t = text.replace("’", "'").replace("‘", "'").replace("¶", "")
    t = t.replace("#", "").replace("[", "").replace("]", "")
    t = re.sub(r"\s+", " ", t).strip()
    return t


_cache: dict | None = None


def load() -> dict[str, dict[tuple, str]]:
    """{source: {(book, chapter, verse): cleaned text}}"""
    global _cache
    if _cache is not None:
        return _cache
    out: dict[str, dict[tuple, str]] = {}

    d = json.load(open(os.path.join(CACHE, "farskipper_verses-1769.json")))
    order: list[str] = []
    m = {}
    for k, v in d.items():
        b, cv = k.rsplit(" ", 1)
        if b not in order:
            order.append(b)
        c, vs = cv.split(":")
        m[(BOOKS[order.index(b)], int(c), int(vs))] = _clean(v)
    out["farskipper"] = m

    d = json.load(open(os.path.join(CACHE, "thiagobodruk_en_kjv.json"), encoding="utf-8-sig"))
    m = {}
    for bi, b in enumerate(d):
        for ci, ch in enumerate(b["chapters"]):
            for vi, v in enumerate(ch):
                m[(BOOKS[bi], ci + 1, vi + 1)] = _clean(v)
    out["thiagobodruk"] = m

    m = {}
    for b in BOOKS:
        d = json.load(open(os.path.join(CACHE, "aruljohn", b.replace(" ", "") + ".json")))
        for ch in d["chapters"]:
            for v in ch["verses"]:
                m[(b, int(ch["chapter"]), int(v["verse"]))] = _clean(v["text"])
    out["aruljohn"] = m

    d = json.load(open(os.path.join(CACHE, "bibleapi_kjv.json")))
    m = {}
    for r in d["resultset"]["row"]:
        _, b, c, vs, text = r["field"]
        m[(BOOKS[b - 1], c, vs)] = _clean(text)
    out["bibleapi"] = m

    d = json.load(open(os.path.join(CACHE, "scrollmapper_KJV.json")))
    m = {}
    for bi, b in enumerate(d["books"]):
        for ch in b["chapters"]:
            for v in ch["verses"]:
                m[(BOOKS[bi], ch["chapter"], v["verse"])] = _clean(v["text"])
    out["scrollmapper"] = m

    _cache = out
    return out


def letters(text: str) -> str:
    return re.sub(r"[^A-Z]", "", text.upper())


def verse(book: str, chapter: int, v: int) -> dict:
    """Majority text of one verse plus a record of how the copies agree."""
    src = load()
    texts = {k: s.get((book, chapter, v)) for k, s in src.items()}
    present = {k: t for k, t in texts.items() if t}
    if not present:
        raise KeyError(f"{book} {chapter}:{v} not found in any copy")
    exact = collections.Counter(present.values())
    best_n = max(exact.values())
    best = [t for t, n in exact.items() if n == best_n]
    text = best[0] if len(best) == 1 else next(present[k] for k in PREFERENCE if present.get(k) in best)
    same_exact = sorted(k for k, t in present.items() if t == text)
    # Letters only (case-blind): what the puzzle is built from.
    lt = letters(text)
    same_letters = sorted(k for k, t in present.items() if letters(t) == lt)
    # scrollmapper puts Psalm titles in front of verse 1: accept if it only *adds* a prefix.
    prefixed = sorted(k for k, t in present.items() if k not in same_letters and letters(t).endswith(lt))
    differ = {k: t for k, t in present.items() if k not in same_letters and k not in prefixed}
    return {"ref": (book, chapter, v), "text": text, "exact": same_exact, "letters_agree": same_letters,
            "title_prefixed": prefixed, "differ": differ}


REF_RE = re.compile(r"^(?P<book>(?:[123] )?[A-Za-z ]+?) (?P<c>\d+):(?P<v1>\d+)(?:-(?P<v2>\d+))?$")


def parse_ref(ref: str) -> tuple[str, int, int, int]:
    m = REF_RE.match(ref.strip())
    if not m:
        raise ValueError(f"bad reference: {ref!r}")
    book = m["book"].strip()
    if book == "Psalm":
        book = "Psalms"
    if book not in BOOKS:
        raise ValueError(f"unknown book in {ref!r}")
    v1 = int(m["v1"])
    v2 = int(m["v2"] or v1)
    return book, int(m["c"]), v1, v2


def passage(ref: str, frm: str | None = None, to: str | None = None) -> dict:
    """A reference like 'Proverbs 3:5-6' -> joined majority text and per-verse agreement.

    frm / to: optional exact phrases that cut out part of a long verse (the part starts
    with `frm` and ends with `to`, both included).  The part is always a literal slice of
    the majority text, so nothing is ever retyped."""
    book, c, v1, v2 = parse_ref(ref)
    parts = [verse(book, c, v) for v in range(v1, v2 + 1)]
    full = " ".join(p["text"] for p in parts)
    text, partial = full, False
    if frm or to:
        a = full.index(frm) if frm else 0
        b = full.index(to, a) + len(to) if to else len(full)
        text = full[a:b].strip()
        partial = (a, b) != (0, len(full))
    return {"ref": ref, "book": book, "chapter": c, "verses": [v1, v2],
            "text": text, "full_text": full, "partial": partial,
            "starts_mid": partial and not full.startswith(text), "ends_mid": partial and not full.endswith(text),
            "parts": parts}


def stats():
    src = load()
    n = collections.Counter()
    for key in src["farskipper"]:
        r = verse(*key)
        n[len(r["letters_agree"]) + len(r["title_prefixed"])] += 1
    total = sum(n.values())
    print(f"{total} verses; copies agreeing on the letters of the chosen text:")
    for k in sorted(n, reverse=True):
        print(f"  {k}/5: {n[k]} ({100 * n[k] / total:.2f}%)")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    {"download": download, "stats": stats}[cmd]()
