"""Fill content/kdp_listing.tmpl.md with the final numbers -> KDP-LISTING.md."""
from __future__ import annotations

import json
import os

import pymupdf

from . import config, cover

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRICE_SHELF_EUR = 18.99
VAT = 0.07
OUT_NAME = "Sprichwoerter-Redewendungen-Senioren"


def _q(t: str) -> str:
    """Exercise names in German quotes ("„Was fehlt?“, „Wortsalat“"), the stories plain."""
    return t if t == "Vorlesegeschichten" else f"„{t}“"


def eur(x: float) -> str:
    return f"{x:.2f} €".replace(".", ",")


def main():
    data = json.load(open(os.path.join(ROOT, "build", "book", "data.json")))
    pages = pymupdf.open(os.path.join(ROOT, "output", f"{OUT_NAME}-interior.pdf")).page_count
    g = cover.geometry(pages)
    net = round(PRICE_SHELF_EUR / (1 + VAT), 2)
    print_eur = 0.75 + 0.016 * pages
    names = [c["name"] for c in data["chapters"]]
    types = [t["name"] for t in data["by_type"]]
    vals = {
        "SUBTITLE": config.SUBTITLE,
        "SERIES": config.SERIES,
        "TITLE_LEN": str(len(config.TITLE) + len(config.SUBTITLE)),
        "CHAPTERS": "; ".join(names),
        "N_TYPES": str(len(types)),
        "TYPES": ", ".join(map(_q, types[:-1])) + " und " + _q(types[-1]),
        "N_SAYINGS": str(data["n_sayings"]),
        "N_EXAMPLES": str(sum(1 for u in data["units"] if u["sheet"].get("example"))),
        "PAGES": str(pages),
        "SPINE": f"{g['spine']:.4f}",
        "PRICE_SHELF": eur(PRICE_SHELF_EUR),
        "PRICE_NET": eur(net),
        "PRINT_EUR": eur(print_eur),
        "ROYALTY_EUR": eur(0.6 * net - print_eur),
        "PRICE_NET19": eur(round(PRICE_SHELF_EUR / 1.19, 2)),
        "ROYALTY_EUR19": eur(0.6 * round(PRICE_SHELF_EUR / 1.19, 2) - print_eur),
        "PRINT_USD": f"${1.00 + 0.017 * pages:.2f}",
    }
    s = open(os.path.join(ROOT, "content", "kdp_listing.tmpl.md")).read()
    for k, v in vals.items():
        s = s.replace(f"⟨{k}⟩", v)
    assert "⟨" not in s, "unfilled placeholder in the KDP listing"
    import re
    for kw in re.findall(r"^\d\. `([^`]+)`", s.split("### Keywords")[1].split("###")[0], re.M):
        assert len(kw.encode()) <= 50, f"keyword field over 50 bytes: {kw!r}"
    with open(os.path.join(ROOT, "KDP-LISTING.md"), "w") as f:
        f.write(s)
    return vals


if __name__ == "__main__":
    main()
