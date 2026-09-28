#!/usr/bin/env python3
"""Prepare the picture-question images for print and record their provenance.

Usage: prepare_images.py --b <source B dir: .../public/data/bamf>

- Takes the images of source B (downloaded from the BAMF catalogue), verifies each file against
  the SHA-256 recorded in source B's questions.json, flattens transparency on white and converts
  to greyscale (the interior is printed black & white).
- Includes only questions that cannot be answered without the picture (coats of arms, maps,
  ballot papers, occupation-zone map, flags). Photos credited to third parties ("© …") are
  NEVER included; for them the book prints a QR code to the official catalogue instead.
- Writes layout/images/*.png, layout/images/qr_catalogue.svg and content/image_provenance.json.
"""
import argparse, hashlib, json, re
from pathlib import Path

import segno
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "layout" / "images"
CATALOGUE_URL = "https://www.bamf.de/SharedDocs/Anlagen/DE/Integration/Einbuergerung/gesamtfragenkatalog-lebenindeutschland.html"
NEEDED_GENERAL = {"G-021", "G-209", "G-226", "G-130", "G-176"}


def needed(qid):
    return qid in NEEDED_GENERAL or re.fullmatch(r"[A-Z]{2}-0[18]", qid) is not None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--b", required=True)
    src = Path(ap.parse_args().b)
    data = json.load(open(src / "questions.json", encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    prov = {"source": "BAMF Gesamtfragenkatalog, images as published in source B (see data/sources.json)",
            "legal_note": ("Drawings of official emblems, maps and specimen ballots from the BAMF catalogue "
                           "(amtliches Werk, § 5 Abs. 2 UrhG). Coats of arms and flags are not protected by "
                           "copyright, but their use is regulated (§ 124 OWiG, state laws): they are shown only "
                           "as the subject of the exam questions, in a book marked as unofficial. Third-party "
                           "photos (© …) are excluded."),
            "included": {}, "excluded": {}}
    for q in data["questions"]:
        code = q["stateCode"]
        qid = f"{code}-{q['officialNumber']:02d}" if code else f"G-{q['officialNumber']:03d}"
        if not q.get("images"):
            continue
        credit = re.search(r"©.*$", q["question"])
        if credit or not needed(qid):
            prov["excluded"][qid] = credit.group(0).strip() if credit else "not needed to answer the question"
            continue
        files = []
        for i, img in enumerate(q["images"]):
            p = src / img["path"]
            digest = hashlib.sha256(p.read_bytes()).hexdigest()
            if digest != img["sha256"]:
                raise SystemExit(f"{qid}: checksum mismatch for {p}")
            im = Image.open(p).convert("RGBA")
            bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
            bg.alpha_composite(im)
            g = ImageOps.autocontrast(bg.convert("L"), cutoff=0.5)
            name = f"{qid}-{i + 1}.png"
            g.save(OUT / name, optimize=True)
            files.append(dict(file=name, source=img["path"], sha256=digest, px=[im.width, im.height]))
        prov["included"][qid] = files
    qr = segno.make(CATALOGUE_URL, error="m")
    qr.save(OUT / "qr_catalogue.svg", scale=4, border=1)
    prov["qr"] = CATALOGUE_URL
    (ROOT / "content" / "image_provenance.json").write_text(json.dumps(prov, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"included {len(prov['included'])} questions, excluded {len(prov['excluded'])}: {sorted(prov['excluded'])}")


if __name__ == "__main__":
    main()
