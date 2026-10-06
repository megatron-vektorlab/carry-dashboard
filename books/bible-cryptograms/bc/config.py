"""Book metadata (must match the KDP listing, the cover and the title page)."""
from __future__ import annotations

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLE = "Large Print Bible Cryptograms"
SUBTITLE = "200 King James Verses of Comfort, Hope and Strength"
SERIES = "Large Print Bible Cryptograms"
VOLUME = 1
AUTHOR = "Ivan Sikuten"
YEAR = 2026

# ---- cover texts (every claim here must stay true for the interior; bc.qa checks the numbers) ----
FRONT_LINE = ["200 King James Verses of", "Comfort, Hope and Strength"]
BACK_HEADLINE = "Unlock God's Word, letter by letter"
BLURB = ("Every puzzle in this book hides a well-loved verse or short passage from the King James Bible. Crack the code, "
         "letter by letter, and words of comfort, hope and strength appear in your own handwriting. "
         "Big, clear letters, roomy write-in lines and gentle hints make each puzzle a peaceful few "
         "minutes with Scripture.")
BULLETS = [
    "200 King James cryptograms in 7 themed parts",
    "Large print: 21-point code letters, every word at least 16 point",
    "One puzzle per page, each with its own code key",
    "Easy to Expert, with given letters to start you off",
    "Three gentle hints per puzzle, and full solutions",
    "A reflection with every answer, and a Christmas part",
]
EPIGRAPH_REF = "Psalms 119:105"     # text is looked up in the KJV copies, never typed

# Fields that must be filled in data/release.json before the book is final.
REQUIRED = ["edition_date", "publisher", "address", "email"]


def release() -> dict:
    path = os.path.join(ROOT, "data", "release.json")
    r = json.load(open(path)) if os.path.exists(path) else {}
    missing = [k for k in REQUIRED if not str(r.get(k, "")).strip()]
    r["missing"] = missing
    r["draft"] = bool(missing)
    return r
