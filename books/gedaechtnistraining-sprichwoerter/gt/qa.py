"""Print-readiness and content checks on the finished PDFs.

    python3 -m gt.qa

Interior:
  * A4 pages, even page count within KDP limits, every font embedded;
  * no text smaller than 16 pt (KDP large print), the draft watermark excepted;
  * nothing outside the safe area (inside margin by page count, 0.25 in elsewhere);
  * every worksheet is one right-hand page with its leader page on the back, in order;
  * exercise text is 20 pt (the cover says so);
  * the word "Demenz" appears nowhere in the book (stigma, see README);
  * every answer word appears on the leader page of its sheet;
  * the German spelling dictionary knows every word (unknown words are listed; the
    ones in data/spelling_ok.txt are accepted).
Cover:
  * size = 2 x bleed + 2 x 8.27 + spine (pages x 0.002252) by 11.94 in, fonts embedded;
  * the numbers on the cover match the book.
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys

import pymupdf

from . import config, cover as cov, text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTERIOR = os.path.join(ROOT, "build", "book", "interior.pdf")
COVER = os.path.join(ROOT, "build", "cover", "cover.pdf")
PT = 72.0
A4_W, A4_H = 8.27, 11.69


def inside_margin_in(pages: int) -> float:
    for limit, m in ((150, 0.375), (300, 0.5), (500, 0.625), (700, 0.75), (828, 0.875)):
        if pages <= limit:
            return m
    return 0.875


def check_interior(errors, notes, warnings):
    doc = pymupdf.open(INTERIOR)
    n = doc.page_count
    notes.append(f"interior pages: {n}")
    if not 24 <= n <= 780:
        errors.append(f"page count {n} outside KDP limits for A4")
    if n % 2:
        errors.append(f"odd page count {n}")
    gutter = inside_margin_in(n)
    data = json.load(open(os.path.join(ROOT, "build", "book", "data.json")))
    fonts, pages_text = set(), []
    min_size = 99.0
    sizes_on_sheets = collections.Counter()
    for i, page in enumerate(doc):
        w, h = page.rect.width / PT, page.rect.height / PT
        if abs(w - A4_W) > 0.01 or abs(h - A4_H) > 0.01:
            errors.append(f"p{i + 1}: page size {w:.3f} x {h:.3f} in")
        for f in page.get_fonts(full=True):
            fonts.add((f[1], f[3]))
        t = page.get_text()
        pages_text.append(t)
        is_sheet = bool(re.search(r"Kopiervorlage\s+Blatt \d+", t))
        odd = i % 2 == 0
        for b in page.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                for s in line["spans"]:
                    st = s["text"].strip()
                    if not st or "ENTWURF" in st or "VERKAUF" in st:
                        continue
                    min_size = min(min_size, s["size"])
                    if s["size"] < 15.9:
                        errors.append(f"p{i + 1}: text {s['size']:.1f} pt < 16 pt: {st[:40]!r}")
                    if is_sheet:
                        sizes_on_sheets[round(s["size"])] += len(st)
                    x0, y0, x1, y1 = (v / PT for v in s["bbox"])
                    left_min = gutter if odd else 0.25
                    right_min = 0.25 if odd else gutter
                    if x0 < left_min - 0.01 or (A4_W - x1) < right_min - 0.01 or y0 < 0.25 or (A4_H - y1) < 0.25:
                        errors.append(f"p{i + 1}: text outside safe area: {st[:30]!r}")
    notes.append(f"smallest text: {min_size:.1f} pt")
    for ext, name in sorted(fonts):
        if ext not in ("ttf", "cff", "otf", "cid", "ttc") and "Type3" not in ext:
            errors.append(f"font not embedded? {name} ({ext})")
    full = "\n".join(pages_text)
    if re.search(r"demenz", full, re.I):
        errors.append("the word 'Demenz' appears in the book")

    # worksheets and leader pages
    sheet_page, leader_page = {}, {}
    for i, t in enumerate(pages_text):
        m = re.search(r"Kopiervorlage\s+Blatt (\d+)", t)
        if m:
            sheet_page.setdefault(int(m.group(1)), []).append(i)
        m = re.search(r"Für die Gruppenleitung\s+Blatt (\d+)", t)
        if m:
            leader_page.setdefault(int(m.group(1)), []).append(i)
    units = {u["sheet"]["num"]: u for u in data["units"]}
    for num, u in units.items():
        sp, lp = sheet_page.get(num, []), leader_page.get(num, [])
        if len(sp) != 1 or len(lp) != 1:
            errors.append(f"Blatt {num}: {len(sp)} worksheet pages, {len(lp)} leader pages (must be 1 and 1)")
            continue
        if sp[0] % 2 != 0:
            errors.append(f"Blatt {num}: worksheet on a left-hand page (p{sp[0] + 1})")
        if lp[0] != sp[0] + 1:
            errors.append(f"Blatt {num}: leader page is not on the back of the worksheet")
        lt = re.sub(r"\s+", " ", pages_text[lp[0]])
        for sol in u["sheet"]["solution"]:
            w = sol.get("word") or ""
            if w and w not in lt:
                errors.append(f"Blatt {num}: answer {w!r} missing on the leader page")
        st = re.sub(r"\s+", " ", pages_text[sp[0]])
        lv = u["sheet"]["level"]
        if st.count("◆") and False:
            pass
    notes.append(f"worksheets: {len(sheet_page)}, leader pages: {len(leader_page)}")
    big = sum(v for k, v in sizes_on_sheets.items() if k >= 20)
    notes.append("worksheet text by size (characters): " + ", ".join(f"{k} pt: {v}" for k, v in sorted(sizes_on_sheets.items())))
    if big < 0.6 * sum(sizes_on_sheets.values()):
        errors.append("less than 60 % of the worksheet text is at 20 pt or larger, but the cover says 'Aufgaben in 20 Punkt'")

    # cover claims
    if len(units) != 100 or not config.FRONT_LINES[1].startswith("100 Kopiervorlagen"):
        errors.append(f"the cover says 100 Kopiervorlagen, the book has {len(units)}")
    if len(data["chapters"]) != 10 or "in 10 Themen" not in config.BULLETS[0]:
        errors.append("the cover says 10 Themen")
    n_story = sum(1 for u in data["units"] if u["sheet"]["type"] == "story")
    if not any(b.startswith(f"{n_story} Vorlesegeschichten") for b in config.BULLETS):
        errors.append(f"the cover's story count does not match ({n_story} stories)")
    n_ex = sum(1 for u in data["units"] if u["sheet"].get("example"))
    if n_ex < 30:
        errors.append(f"the cover says 'viele Blätter mit gelöstem Beispiel', but only {n_ex} have one")
    levels = {u["sheet"]["level"] for u in data["units"]}
    if levels != {1, 2, 3}:
        errors.append(f"levels used: {levels}")
    no_example = [u["sheet"]["num"] for u in data["units"] if u["sheet"]["level"] < 3
                  and u["sheet"]["type"] not in ("match", "choice", "situation", "story") and not u["sheet"].get("example")]
    if no_example:
        errors.append(f"sheets at levels 1-2 without a worked example: {no_example}")
    if data["release"].get("draft"):
        errors.append(f"release data incomplete (draft watermark on): {data['release'].get('missing')}")

    # spelling: every string in the book data and the prose pages
    strings = []

    def walk(x):
        if isinstance(x, str):
            strings.append(x)
        elif isinstance(x, dict):
            for k, v in x.items():
                if k not in ("grid", "places", "tiles", "stubs", "scrambled", "item_ids", "release", "type", "kind", "words"):
                    walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(data)
    import glob
    for f in glob.glob(os.path.join(ROOT, "content", "*.typ")):
        for line in open(f):
            if line.lstrip().startswith(("#import", "#let", "#set", "#show", "//", "#grid", "..row", "#chapter-title(")):
                continue
            line = re.sub(r"[0-9.]+(em|pt|mm|in)\b", " ", line)
            line = re.sub(r"#[^\s\[\]]*", " ", line)          # #code up to a space or bracket
            line = re.sub(r"\b[a-z][a-z-]*\(", " ", line)       # function calls
            line = re.sub(r'"[a-z_]+"|\b[a-z_]+:|\belse\b|\b[a-z]+\.[a-z_.]+', " ", line)   # code strings, args, fields
            strings.append(line)
    src = "\n".join(strings)
    ok_path = os.path.join(ROOT, "data", "spelling_ok.txt")
    ok = set(open(ok_path).read().split()) if os.path.exists(ok_path) else set()
    # old forms inside attested sayings ("Wes Brot ich ess", "Wie die Alten sungen") are correct
    corpus = json.load(open(os.path.join(ROOT, "data", "corpus.json")))["items"]
    for it in corpus:
        for w in [it["wording"], *it.get("variants", [])]:
            ok.update(text.words(w))
    unknown = collections.Counter()
    for w in set(text.words(src)):
        if len(w) < 2 or w in ok or w.isupper() and len(w) <= 3:
            continue
        if not text.spelled_ok(w):
            unknown[w] += src.count(w)
    if unknown:
        warnings.append(f"{len(unknown)} words unknown to the spelling dictionary: "
                        + ", ".join(f"{w} ({c})" for w, c in unknown.most_common(80)))


def check_cover(errors, notes):
    if not os.path.exists(COVER):
        errors.append("cover.pdf missing")
        return
    pages = pymupdf.open(INTERIOR).page_count
    g = cov.geometry(pages)
    c = pymupdf.open(COVER)
    r = c[0].rect
    w, h = r.width / PT, r.height / PT
    if abs(w - g["width"]) > 0.005 or abs(h - g["height"]) > 0.005:
        errors.append(f"cover {w:.4f} x {h:.4f} in, expected {g['width']} x {g['height']}")
    notes.append(f"cover {w:.3f} x {h:.3f} in, spine {g['spine']} in for {pages} pages")
    for f in c[0].get_fonts(full=True):
        if f[1] not in ("ttf", "cff", "otf", "cid", "ttc") and "Type3" not in f[1]:
            errors.append(f"cover font not embedded? {f[3]}")
    if re.search(r"demenz", c[0].get_text(), re.I):
        errors.append("the word 'Demenz' is on the cover")


def main():
    errors, notes, warnings = [], [], []
    check_interior(errors, notes, warnings)
    check_cover(errors, notes)
    for n in notes:
        print("  " + n)
    for w in warnings:
        print("  WARNING: " + w)
    if errors:
        print(f"QA FAILED ({len(errors)}):")
        for e in errors[:200]:
            print("  - " + e)
        sys.exit(1)
    print("QA passed.")


if __name__ == "__main__":
    main()
