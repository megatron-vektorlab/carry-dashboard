#!/usr/bin/env python3
"""Typeset the KDP full-wrap cover. Reads the page count from out/build_info.json
(run build_book.py first). Output: out/cover_de-bks.pdf"""
import json, sys
from pathlib import Path

import typst

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
PAPER_IN_PER_PAGE = 0.002252  # KDP, white paper, black & white interior


def main():
    info = json.load(open(ROOT / "out" / "build_info.json"))
    pages = info["pages"]
    spine = round(pages * PAPER_IN_PER_PAGE, 4)
    rel = json.load(open(ROOT / "kdp" / "release.json", encoding="utf-8"))
    from build_book import release_missing
    missing = release_missing(rel)
    check_note = (f"menschliches Lektorat: {rel['human_proofread_by']}." if rel.get("human_proofread") is True
                  else "automatisch und durch unabhängige KI-Gegenprüfungen kontrolliert.")
    stand = (f"Stand: {rel['catalog_stand']}" if rel.get("catalog_verified") is True
             else f"Datenstand: {rel['public_copy_retrieved']}")
    params = dict(pages=pages, spine_in=spine, stand=stand, author=rel.get("author") or "[AUTOR]",
                  imprint=rel.get("publisher") or "[VERLAG / NAME]", check_note=check_note, draft=bool(missing))
    (ROOT / "build").mkdir(exist_ok=True)
    (ROOT / "build" / "cover_params.json").write_text(json.dumps(params))
    out = ROOT / "out" / "cover_de-bks.pdf"
    typst.compile(str(ROOT / "layout" / "cover.typ"), output=str(out), root=str(ROOT),
                  font_paths=[str(ROOT / "layout" / "fonts")])
    width = 0.125 * 2 + 6.69 * 2 + spine
    # Hand-off record for whoever uploads to KDP: only files from a build with "draft": false
    # may be uploaded, and the cover must match the interior's page count.
    info.update(draft=bool(missing) or info.get("draft", False), spine_in=spine,
                cover_width_in=round(width, 4), cover_height_in=9.86,
                trim="6.69 x 9.61 in", files=["interior_de-bks.pdf", "cover_de-bks.pdf"])
    (ROOT / "out" / "build_info.json").write_text(json.dumps(info, indent=1))
    print(json.dumps(dict(pages=pages, spine_in=spine, cover_in=[round(width, 4), 9.86], draft=info["draft"])))


if __name__ == "__main__":
    main()
