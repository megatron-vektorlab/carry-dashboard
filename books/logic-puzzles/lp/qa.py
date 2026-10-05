"""Print-readiness checks on the finished PDFs.

    .venv/bin/python -m lp.qa

- every font embedded (pdffonts)
- large print: no reading text under 15.5 pt (footers and page numbers excepted)
- page size 8.5 x 11 in, page count, spine width
- every puzzle fits its planned pages; every hint and solution label resolves
- every puzzle has its writing, and the writing passes lp.check_writing
"""
from __future__ import annotations

import collections
import json
import os
import re
import subprocess
import sys

import fitz

from .book import BUILD, SPREAD_FAMILIES, page_labels

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fonts(pdf):
    out = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout.splitlines()[2:]
    bad = [ln for ln in out if ln.split()[-5] != "yes"] if out else []
    return len(out), bad


def small_text(pdf, min_pt=15.5, foot_in=0.75):
    doc = fitz.open(pdf)
    hits = collections.Counter()
    samples = {}
    for pno, page in enumerate(doc):
        H = page.rect.height
        for b in page.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                for sp in ln["spans"]:
                    t = sp["text"].strip()
                    if not t or sp["size"] >= min_pt:
                        continue
                    if sp["bbox"][1] > H - foot_in * 72:
                        continue        # footer / page number
                    hits[pno + 1] += 1
                    samples.setdefault(pno + 1, f"{sp['size']:.1f}pt '{t[:40]}'")
    return hits, samples


def main():
    pdf = os.path.join(BUILD, "interior.pdf")
    doc = fitz.open(pdf)
    n = doc.page_count
    w, h = doc[0].rect.width / 72, doc[0].rect.height / 72
    print(f"interior: {n} pages, {w:.2f} x {h:.2f} in, spine {n * 0.002252:.3f} in")
    total, bad = fonts(pdf)
    print(f"fonts: {total} listed, {len(bad)} not embedded")
    for b in bad:
        print("   ", b)
    hits, samples = small_text(pdf)
    print(f"text under 15.5 pt outside footers: {sum(hits.values())} spans on {len(hits)} pages")
    for p in sorted(hits)[:15]:
        print(f"    page {p}: {hits[p]} spans, e.g. {samples[p]}")
    labs = page_labels()
    probs = 0
    for f in sorted(os.listdir(os.path.join(ROOT, "data", "puzzles"))):
        P = json.load(open(os.path.join(ROOT, "data", "puzzles", f)))
        no = P["no"]
        a, b = labs.get(f"puz:{no}"), labs.get(f"puzend:{no}")
        want = 2 if P.get("family") in SPREAD_FAMILIES else 1
        if not (a and b and a.isdigit() and b.isdigit()) or int(b) - int(a) + 1 != want:
            print(f"    puzzle {no}: pages {a}-{b}, planned {want}")
            probs += 1
        for key in [f"sol:{no}", f"h1:{no}", f"h2:{no}", f"h3:{no}"] + ([f"h4:{no}"] if P["stars"] >= 4 else []):
            if key not in labs:
                print(f"    missing label {key}")
                probs += 1
    log = open(os.path.join(BUILD, "interior.log"), errors="replace").read()
    over = re.findall(r"Overfull \\hbox \((\d+\.\d+)pt too wide\)", log)
    big = [float(x) for x in over if float(x) > 2]
    print(f"overfull hboxes > 2pt: {len(big)}; undefined refs: {log.count('undefined')}")
    print("layout problems:", probs)
    r = subprocess.run([sys.executable, "-m", "lp.check_writing", "--back"], cwd=ROOT, capture_output=True, text=True)
    print("check_writing:", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:])
    cov = os.path.join(ROOT, "build", "cover", "cover.pdf")
    if os.path.exists(cov):
        c = fitz.open(cov)[0].rect
        print(f"cover: {c.width / 72:.3f} x {c.height / 72:.3f} in (expected {2 * 8.5 + n * 0.002252 + 0.25:.3f} x 11.250)")
        total, bad = fonts(cov)
        print(f"cover fonts: {total} listed, {len(bad)} not embedded")


if __name__ == "__main__":
    main()
