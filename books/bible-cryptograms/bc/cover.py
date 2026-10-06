"""Full-wrap paperback cover (KDP: black & white interior, white paper, 8.5 x 11 in).

    python3 -m bc.cover            # page count taken from build/book/interior.pdf

Width  = 0.125 bleed + 8.5 back + spine + 8.5 front + 0.125 bleed
Height = 0.125 bleed + 11 + 0.125 bleed
Spine  = pages x 0.002252 in (KDP, white paper).  Spine text only when pages >= 80.
Barcode: KDP prints it in a 2 x 1.2 in box, lower right of the back cover; we keep that
area empty (0.25 in from the trim edges).
"""
from __future__ import annotations

import json
import os
import sys

import typst

from . import config

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "cover")
BLEED = 0.125
TRIM_W, TRIM_H = 8.5, 11.0
PAPER_IN_PER_PAGE = 0.002252


def page_count() -> int:
    import pymupdf
    return pymupdf.open(os.path.join(ROOT, "build", "book", "interior.pdf")).page_count


def geometry(pages: int) -> dict:
    spine = round(pages * PAPER_IN_PER_PAGE, 4)
    return {
        "pages": pages,
        "spine": spine,
        "width": round(2 * BLEED + 2 * TRIM_W + spine, 4),
        "height": TRIM_H + 2 * BLEED,
        "bleed": BLEED,
        "trim_w": TRIM_W,
        "trim_h": TRIM_H,
        "spine_text": pages >= 80,
    }


def pick_sample(pz: list[dict]) -> dict:
    """A short Easy puzzle for the back cover (fits the card in three lines)."""
    from . import layout
    easy = [p for p in pz if p["level"] == 1 and layout.lines_needed(p["cipher"]) <= 3
            and sum(1 for c in p["cipher"] if c.isalpha() or c in " ") * layout.CELL < 3 * 6.3]
    return min(easy or pz, key=lambda p: (layout.lines_needed(p["cipher"]), -p["letters"]))


def main(pages: int | None = None):
    pages = pages or page_count()
    g = geometry(pages)
    os.makedirs(OUT, exist_ok=True)
    pz = json.load(open(os.path.join(ROOT, "data", "puzzles.json")))["puzzles"]
    sample = pick_sample(pz)
    from . import book, cipher, kjv
    key = cipher.make_key("cover:CRYPTOGRAMS", used="CRYPTOGRAMS")
    data = dict(g, title=config.TITLE, subtitle=config.SUBTITLE, author=config.AUTHOR,
                count=len(pz), front_line=config.FRONT_LINE, back_headline=book.typo(config.BACK_HEADLINE),
                blurb=book.typo(config.BLURB), bullets=[book.typo(b) for b in config.BULLETS],
                epigraph="\u201c" + kjv.passage(config.EPIGRAPH_REF)["text"] + "\u201d (" + config.EPIGRAPH_REF.replace("Psalms", "Psalm") + ")",
                tile_code=cipher.encrypt("CRYPTOGRAMS", key),
                sample_words=book.cells(sample["cipher"], sample["given"]), sample_num=sample["num"],
                sample_level_name=book.LEVEL_NAMES[sample["level"]], release=config.release())
    with open(os.path.join(OUT, "cover.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False)
    out = os.path.join(OUT, "cover.pdf")
    typst.compile(os.path.join(ROOT, "layout", "cover.typ"), output=out, root=ROOT,
                  font_paths=[os.path.join(ROOT, "fonts")], ignore_system_fonts=True)
    typst.compile(os.path.join(ROOT, "layout", "cover.typ"), output=os.path.join(OUT, "cover.png"), root=ROOT,
                  font_paths=[os.path.join(ROOT, "fonts")], ignore_system_fonts=True, ppi=150)
    print(f"cover: {g['width']} x {g['height']} in, spine {g['spine']} in ({pages} pages)", file=sys.stderr)
    return out, g


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
