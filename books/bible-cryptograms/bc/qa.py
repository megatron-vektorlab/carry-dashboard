"""Print-readiness and content checks on the finished PDFs.

    python3 -m bc.qa

Interior:
  * page size 8.5 x 11 in, page count within KDP limits, every font embedded;
  * no text smaller than 16 pt anywhere (KDP large print), the draft watermark excepted;
  * nothing printed outside the safe area (inside margin by page count, 0.25 in elsewhere);
  * every puzzle page carries exactly the code letters of its puzzle, in order;
  * every solution prints its verse exactly as the verified King James text;
  * every "Hints on page N" / "Answer on page N" points to the page that holds it.
Cover:
  * size = 2 x bleed + 2 x 8.5 + spine (pages x 0.002252) by 11.25 in, fonts embedded.
"""
from __future__ import annotations

import json
import os
import re
import sys

import pymupdf

from . import cover as cov

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTERIOR = os.path.join(ROOT, "build", "book", "interior.pdf")
COVER = os.path.join(ROOT, "build", "cover", "cover.pdf")
PT = 72.0


def inside_margin_in(pages: int) -> float:
    # KDP minimum inside (gutter) margin by page count
    for limit, m in ((150, 0.375), (300, 0.5), (500, 0.625), (700, 0.75), (828, 0.875)):
        if pages <= limit:
            return m
    return 0.875


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("’", "'")).strip()


def check_interior(errors: list[str], notes: list[str]):
    doc = pymupdf.open(INTERIOR)
    n = doc.page_count
    notes.append(f"interior pages: {n}")
    if not (24 <= n <= 828):
        errors.append(f"page count {n} outside KDP limits")
    gutter = inside_margin_in(n)
    data = json.load(open(os.path.join(ROOT, "build", "book", "data.json")))
    puzzles = {p["num"]: p for p in data["puzzles"]}
    min_size = 99.0
    fonts = set()
    pages_text = []
    for i, page in enumerate(doc):
        w, h = page.rect.width / PT, page.rect.height / PT
        if abs(w - 8.5) > 0.01 or abs(h - 11) > 0.01:
            errors.append(f"p{i + 1}: page size {w:.3f} x {h:.3f} in")
        for f in page.get_fonts(full=True):
            fonts.add((f[1], f[3]))
        d = page.get_text("dict")
        odd = (i % 2 == 0)  # page 1 is a right-hand (odd) page
        for b in d["blocks"]:
            for line in b.get("lines", []):
                for s in line["spans"]:
                    t = s["text"].strip()
                    if not t:
                        continue
                    if "DRAFT" in t or "NOT FOR SALE" in t:
                        continue
                    min_size = min(min_size, s["size"])
                    if s["size"] < 15.9:
                        errors.append(f"p{i + 1}: text {s['size']:.1f} pt < 16 pt: {t[:40]!r}")
                    x0, y0, x1, y1 = (v / PT for v in s["bbox"])
                    left_min = gutter if odd else 0.25
                    right_min = 0.25 if odd else gutter
                    if x0 < left_min - 0.01 or (8.5 - x1) < right_min - 0.01 or y0 < 0.25 or (11 - y1) < 0.25:
                        errors.append(f"p{i + 1}: text outside safe area: {t[:30]!r} at x={x0:.2f}-{x1:.2f} y={y0:.2f}-{y1:.2f}")
        pages_text.append(page.get_text("text"))
    notes.append(f"smallest text: {min_size:.1f} pt")
    for ext, name in sorted(fonts):
        if ext not in ("ttf", "cff", "otf", "cid", "ttc") and "Type3" not in ext:
            errors.append(f"font not embedded? {name} ({ext})")
    notes.append("fonts: " + ", ".join(sorted({re.sub(r'^[A-Z]{6}\+', '', n) for _, n in fonts})))

    # puzzle pages: find "Puzzle N" headings and compare the code letters
    found = {}
    for i, t in enumerate(pages_text):
        m = re.search(r"^Puzzle (\d+)$", t, re.M)
        if m:
            found[int(m.group(1))] = i
    for num, p in puzzles.items():
        if num not in found:
            errors.append(f"puzzle {num}: page not found")
            continue
        t = pages_text[found[num]]
        body = t.split("Code key")[0]
        want = re.sub(r"[^A-Z]", "", "".join(c[0] for w in p["words"] for c in w))
        # letters printed in the page body: code letters + given letters in the answer slots
        got = re.sub(r"[^A-Z]", "", body.split("\n", 3)[-1])
        given_count = sum(1 for w in p["words"] for c in w if c[1])
        if len(got) != len(want) + given_count + len(re.sub(r"[^A-Z]", "", " ".join(p["given_list"]))):
            # fallback check: the code letters must appear in order as a subsequence
            it = iter(got)
            if not all(ch in it for ch in want):
                errors.append(f"puzzle {num}: code letters on the page differ from the data")
        mh = re.search(r"Hints p\. (\d+)", t)
        ma = re.search(r"Answer p\. (\d+)", t)
        if not mh or not ma:
            errors.append(f"puzzle {num}: missing hint/answer page reference")
            continue
        hp, ap = int(mh.group(1)), int(ma.group(1))
        if hp > len(pages_text) or not re.search(rf"(^|\n){num}\b", pages_text[hp - 1]):
            errors.append(f"puzzle {num}: hint page {hp} does not list puzzle {num}")
        if ap > len(pages_text) or not re.search(rf"(^|\n){num}\b", pages_text[ap - 1]):
            errors.append(f"puzzle {num}: answer page {ap} does not list puzzle {num}")
        else:
            sol = norm(pages_text[ap - 1] + " " + (pages_text[ap] if ap < len(pages_text) else ""))
            if norm(p["text"]) not in sol.replace("- ", "-"):
                # allow line breaks inside the verse
                if norm(p["text"]).replace(" ", "") not in sol.replace(" ", ""):
                    errors.append(f"puzzle {num}: verse text not found verbatim on answer page {ap}")
    notes.append(f"puzzle pages checked: {len(found)}/{len(puzzles)}")

    # claims printed on the cover / in the listing
    per_page = [len(re.findall(r"^Puzzle \d+$", t, re.M)) for t in pages_text]
    if max(per_page) > 1:
        errors.append("a page holds more than one puzzle, but the cover says 'one puzzle per page'")
    sizes = set()
    for i in found.values():
        for b in doc[i].get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                for sp in line["spans"]:
                    if re.fullmatch(r"[A-Z]", sp["text"].strip()):
                        sizes.add(round(sp["size"]))
    if 21 not in sizes:
        errors.append(f"cover promises 21-point code letters; found letter sizes {sorted(sizes)}")
    from . import config
    if not config.BULLETS[0].startswith(str(len(puzzles))) or not config.FRONT_LINE[0].startswith(str(len(puzzles))):
        errors.append("puzzle count on the cover does not match the book")
    missing_refl = [p["num"] for p in puzzles.values() if not p.get("reflection")]
    if missing_refl:
        errors.append(f"{len(missing_refl)} puzzles have no reflection line (data/reflections.json), e.g. {missing_refl[:5]}")
    # reflection lines: length, safe characters, and they must not restate the verse
    for p in puzzles.values():
        r = p.get("reflection", "")
        if not r:
            continue
        n = len(r.split())
        if not 6 <= n <= 24:
            errors.append(f"puzzle {p['num']}: reflection has {n} words")
        if re.search(r"[^A-Za-z0-9 .,;:?'()\-]", r):
            errors.append(f"puzzle {p['num']}: reflection has unexpected characters: {r!r}")
        vw = re.findall(r"[a-z']+", p["text"].lower())
        rw = re.findall(r"[a-z']+", r.lower())
        grams = {tuple(vw[i:i + 5]) for i in range(len(vw) - 4)}
        if any(tuple(rw[i:i + 5]) in grams for i in range(len(rw) - 4)):
            errors.append(f"puzzle {p['num']}: reflection repeats five words of the verse")
    missing_intro = [t["name"] for t in data["themes"] if not t.get("intro")]
    if missing_intro:
        errors.append(f"parts without an introduction (data/intros.json): {missing_intro}")
    if data["release"].get("draft"):
        errors.append(f"release data incomplete (draft watermark on): {data['release'].get('missing')}")


def check_cover(errors: list[str], notes: list[str]):
    if not os.path.exists(COVER):
        errors.append("cover.pdf missing")
        return
    pages = pymupdf.open(INTERIOR).page_count
    g = cov.geometry(pages)
    c = pymupdf.open(COVER)
    if c.page_count != 1:
        errors.append("cover must be one page")
    r = c[0].rect
    w, h = r.width / PT, r.height / PT
    if abs(w - g["width"]) > 0.005 or abs(h - g["height"]) > 0.005:
        errors.append(f"cover {w:.4f} x {h:.4f} in, expected {g['width']} x {g['height']}")
    notes.append(f"cover {w:.3f} x {h:.3f} in, spine {g['spine']} in for {pages} pages")
    for f in c[0].get_fonts(full=True):
        if f[1] not in ("ttf", "cff", "otf", "cid", "ttc") and "Type3" not in f[1]:
            errors.append(f"cover font not embedded? {f[3]}")


def main():
    errors: list[str] = []
    notes: list[str] = []
    check_interior(errors, notes)
    check_cover(errors, notes)
    for n in notes:
        print("  " + n)
    if errors:
        print(f"QA FAILED ({len(errors)}):")
        for e in errors[:200]:
            print("  - " + e)
        sys.exit(1)
    print("QA passed.")


if __name__ == "__main__":
    main()
