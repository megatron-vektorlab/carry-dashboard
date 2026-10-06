"""Fill content/kdp_listing.tmpl.md with the final numbers -> KDP-LISTING.md."""
from __future__ import annotations

import json
import os

import pymupdf

from . import config, cover

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRICES = {"USD": 13.99, "EUR": 13.99, "CAD": 18.99, "AUD": 21.99}


def main():
    pz = json.load(open(os.path.join(ROOT, "data", "puzzles.json")))["puzzles"]
    sel = json.load(open(os.path.join(ROOT, "data", "selection.json")))
    parts = [t["name"] for t in sel["themes"] if any(p["theme"] == t["name"] for p in pz)]
    pages = pymupdf.open(os.path.join(ROOT, "output", "Large-Print-Bible-Cryptograms-interior.pdf")).page_count
    g = cover.geometry(pages)
    print_cost = 1.00 + 0.017 * pages
    royalty = 0.6 * PRICES["USD"] - print_cost
    vals = {
        "SUBTITLE": config.SUBTITLE,
        "TITLE_LEN": str(len(config.TITLE) + len(config.SUBTITLE)),
        "COUNT": str(len(pz)),
        "PARTS": str(len(parts)),
        "PART_NAMES": "; ".join(parts[:-1]) + "; and " + parts[-1] if len(parts) > 1 else parts[0],
        "PAGES": str(pages),
        "SPINE": f"{g['spine']:.4f}",
        "PRICE_USD": f"${PRICES['USD']:.2f}",
        "PRICE_EUR": f"€{PRICES['EUR']:.2f}",
        "PRICE_CAD": f"C${PRICES['CAD']:.2f}",
        "PRICE_AUD": f"A${PRICES['AUD']:.2f}",
        "PRINT_COST": f"${print_cost:.2f}",
        "ROYALTY": f"${royalty:.2f}",
    }
    s = open(os.path.join(ROOT, "content", "kdp_listing.tmpl.md")).read()
    for k, v in vals.items():
        s = s.replace(f"⟨{k}⟩", v)
    assert "⟨" not in s, "unfilled placeholder in the KDP listing"
    with open(os.path.join(ROOT, "KDP-LISTING.md"), "w") as f:
        f.write(s)
    return vals


if __name__ == "__main__":
    main()
