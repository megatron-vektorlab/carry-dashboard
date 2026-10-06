"""Build everything, in order, and copy the upload files to output/.

    python3 -m bc.build            # puzzles -> interior -> cover -> QA -> output/ -> KDP-LISTING.md
    python3 -m bc.build --select   # also re-run the verse selection first

The cover is built after the interior because its spine width depends on the page count.
"""
from __future__ import annotations

import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "output")


def main():
    from . import book, cover, listing, puzzles, qa, select, stats
    if "--select" in sys.argv:
        select.main()
    if not os.path.exists(os.path.join(ROOT, "data", "kjv_stats.json")):
        stats.main()
    puzzles.main()
    book.main()
    cover.main()
    qa.main()                      # exits non-zero on any failure
    os.makedirs(os.path.join(OUT, "marketing"), exist_ok=True)
    shutil.copy(os.path.join(ROOT, "build", "book", "interior.pdf"),
                os.path.join(OUT, "Large-Print-Bible-Cryptograms-interior.pdf"))
    shutil.copy(os.path.join(ROOT, "build", "cover", "cover.pdf"),
                os.path.join(OUT, "Large-Print-Bible-Cryptograms-cover.pdf"))
    marketing()
    listing.main()
    print("done: output/ and KDP-LISTING.md are up to date", file=sys.stderr)


def marketing():
    """Front cover PNG and a few sample pages for A+ content / ads."""
    import json

    import pymupdf
    c = pymupdf.open(os.path.join(ROOT, "build", "cover", "cover.pdf"))
    g = json.load(open(os.path.join(ROOT, "build", "cover", "cover.json")))
    x0 = (g["bleed"] + g["trim_w"] + g["spine"]) * 72
    clip = pymupdf.Rect(x0, g["bleed"] * 72, x0 + g["trim_w"] * 72, (g["bleed"] + g["trim_h"]) * 72)
    c[0].get_pixmap(dpi=200, clip=clip).save(os.path.join(OUT, "front-cover.png"))
    d = pymupdf.open(os.path.join(ROOT, "build", "book", "interior.pdf"))
    wanted = {"puzzle-page.png": "Puzzle 1\n", "step-by-step.png": "A Puzzle Solved Step by Step",
              "hints-page.png": "Hint 1 · The book", "solutions-page.png": "Solutions\n"}
    for name, needle in wanted.items():
        for page in d:
            if needle in page.get_text():
                page.get_pixmap(dpi=150).save(os.path.join(OUT, "marketing", name))
                break


if __name__ == "__main__":
    main()
