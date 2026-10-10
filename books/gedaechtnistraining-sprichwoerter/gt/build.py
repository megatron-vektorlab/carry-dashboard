"""Build everything, in order, and copy the upload files to output/.

    python3 -m gt.build            # plan -> interior -> cover -> QA -> output/ -> KDP-LISTING.md

The cover is built after the interior because its spine width depends on the page count.
"""
from __future__ import annotations

import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "output")


def main():
    from . import book, cover, listing, plan, qa
    plan.main()
    book.main()
    cover.main()
    qa.main()                      # exits non-zero on any failure
    os.makedirs(os.path.join(OUT, "marketing"), exist_ok=True)
    shutil.copy(os.path.join(ROOT, "build", "book", "interior.pdf"),
                os.path.join(OUT, f"{listing.OUT_NAME}-interior.pdf"))
    shutil.copy(os.path.join(ROOT, "build", "cover", "cover.pdf"),
                os.path.join(OUT, f"{listing.OUT_NAME}-cover.pdf"))
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
    wanted = {"worksheet.png": r"Kopiervorlage\s+Blatt 2\b", "leader-page.png": r"Für die Gruppenleitung\s+Blatt 2\b",
              "chapter-opener.png": r"Zum Aufwärmen", "story.png": r"Kopiervorlage\s+Blatt 4\b"}
    for name, pat in wanted.items():
        for page in d:
            if re.search(pat, page.get_text()):
                page.get_pixmap(dpi=150).save(os.path.join(OUT, "marketing", name))
                break


if __name__ == "__main__":
    main()
