#!/usr/bin/env python3
"""Typeset the KDP full-wrap cover. Reads the page count from out/build_info.json
(run build_book.py first). Output: out/cover_de-bks.pdf"""
import json
from pathlib import Path

import typst

ROOT = Path(__file__).resolve().parents[1]
PAPER_IN_PER_PAGE = 0.002252  # KDP, white paper, black & white interior


def main():
    info = json.load(open(ROOT / "out" / "build_info.json"))
    pages = info["pages"]
    spine = round(pages * PAPER_IN_PER_PAGE, 4)
    params = dict(pages=pages, spine_in=spine, stand="September 2026", imprint="[VERLAG / NAME]")
    (ROOT / "build").mkdir(exist_ok=True)
    (ROOT / "build" / "cover_params.json").write_text(json.dumps(params))
    out = ROOT / "out" / "cover_de-bks.pdf"
    typst.compile(str(ROOT / "layout" / "cover.typ"), output=str(out), root=str(ROOT),
                  font_paths=[str(ROOT / "layout" / "fonts")])
    width = 0.125 * 2 + 6.69 * 2 + spine
    print(json.dumps(dict(pages=pages, spine_in=spine, cover_in=[round(width, 4), 9.86])))


if __name__ == "__main__":
    main()
