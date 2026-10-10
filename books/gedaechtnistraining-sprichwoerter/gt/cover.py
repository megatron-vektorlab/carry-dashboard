"""Full-wrap paperback cover (KDP: black & white interior, white paper, A4 8.27 x 11.69 in).

    python3 -m gt.cover            # page count taken from build/book/interior.pdf

Width  = 0.125 bleed + 8.27 back + spine + 8.27 front + 0.125 bleed
Height = 0.125 bleed + 11.69 + 0.125 bleed
Spine  = pages x 0.002252 in (KDP, white paper). Spine text only when pages >= 80.
Barcode: KDP prints it in a 2 x 1.2 in box at the lower right of the back cover; that area
stays empty (0.25 in from the trim edges).
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
TRIM_W, TRIM_H = 8.27, 11.69
PAPER_IN_PER_PAGE = 0.002252


def page_count() -> int:
    import pymupdf
    return pymupdf.open(os.path.join(ROOT, "build", "book", "interior.pdf")).page_count


def geometry(pages: int) -> dict:
    spine = round(pages * PAPER_IN_PER_PAGE, 4)
    return {"pages": pages, "spine": spine, "width": round(2 * BLEED + 2 * TRIM_W + spine, 4),
            "height": round(TRIM_H + 2 * BLEED, 4), "bleed": BLEED, "trim_w": TRIM_W, "trim_h": TRIM_H,
            "spine_text": pages >= 80}


def sample_page() -> str:
    """PNG of the first worksheet, shown small on the back cover."""
    import pymupdf
    d = pymupdf.open(os.path.join(ROOT, "build", "book", "interior.pdf"))
    import re
    for i, p in enumerate(d):
        t = p.get_text()
        if re.search(r"Kopiervorlage\s+Blatt 1\b", t):
            path = os.path.join(OUT, "sample.png")
            p.get_pixmap(dpi=200).save(path)
            return "/build/cover/sample.png"
    raise RuntimeError("worksheet 1 not found")


def main(pages: int | None = None):
    pages = pages or page_count()
    g = geometry(pages)
    os.makedirs(OUT, exist_ok=True)
    data = dict(g, title=config.TITLE, author=config.AUTHOR, series=config.SERIES, volume=config.VOLUME,
                front_lines=config.FRONT_LINES, badges=config.FRONT_BADGES, back_headline=config.BACK_HEADLINE,
                blurb=config.BLURB, bullets=config.BULLETS, sample=sample_page(), release=config.release())
    with open(os.path.join(OUT, "cover.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False)
    out = os.path.join(OUT, "cover.pdf")
    kw = dict(root=ROOT, font_paths=[os.path.join(ROOT, "fonts")], ignore_system_fonts=True)
    try:
        typst.compile(os.path.join(ROOT, "layout", "cover.typ"), output=out, **kw)
        typst.compile(os.path.join(ROOT, "layout", "cover.typ"), output=os.path.join(OUT, "cover.png"), ppi=110, **kw)
    except typst.TypstError as e:
        print(e.diagnostic, file=sys.stderr)
        raise
    print(f"cover: {g['width']} x {g['height']} in, spine {g['spine']} in ({pages} pages)", file=sys.stderr)
    return out, g


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
