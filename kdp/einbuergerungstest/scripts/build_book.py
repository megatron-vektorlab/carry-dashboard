#!/usr/bin/env python3
"""Assemble the book data and typeset the interior PDF with Typst.

Usage: build_book.py [--draft]
  --draft  typeset even if translations are missing (placeholders are printed)

Outputs: build/book_data.json, out/interior_de-bks.pdf, out/build_info.json
"""
import argparse, json, random, re, sys
from pathlib import Path

import typst

ROOT = Path(__file__).resolve().parents[1]
N_TESTS = 10
SEED = 20260926  # fixed: the practice tests must not change between builds
LETTERS = "ABCD"


def pretty(s):
    """Typography for print only; the catalogue text itself is never altered."""
    s = s.replace("...", "…")
    s = re.sub(r'"([^"]+)"', "„\\1“", s)
    s = re.sub(r"\s*©.*$", "", s)  # photo credits belong to the (omitted) pictures
    s = s.replace(" In Anlehnung an Bundeswahlordnung (BWO), Anlage 26", "")
    return s.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", action="store_true")
    args = ap.parse_args()

    cat = json.load(open(ROOT / "data" / "catalog.json", encoding="utf-8"))
    meta, questions = cat["meta"], cat["questions"]
    bks_path = ROOT / "content" / "bks.json"
    bks = {t["id"]: t for t in json.load(open(bks_path, encoding="utf-8"))} if bks_path.exists() else {}
    notes = json.load(open(ROOT / "content" / "image_notes_bks.json", encoding="utf-8"))["notes"]
    glossary = json.load(open(ROOT / "content" / "glossary_bks.json", encoding="utf-8"))["terms"]
    missing = [q["id"] for q in questions if q["id"] not in bks]
    if missing and not args.draft:
        sys.exit(f"{len(missing)} questions have no translation (e.g. {missing[:5]}); run validate_content.py or use --draft")

    def item(q):
        t = bks.get(q["id"], {})
        opts = [dict(letter=LETTERS[i], de=pretty(o), bks=pretty(t["options_bks"][i]) if t else "[prijevod u izradi]",
                     correct=(i == q["answer"])) for i, o in enumerate(q["options"])]
        label = str(q["num"]) if q["state"] is None else f"{q['state']} {q['num']}"
        return dict(id=q["id"], label=label, num=q["num"], q_de=pretty(q["question"]),
                    q_bks=pretty(t.get("q_bks", "[prijevod u izradi]")), options=opts,
                    expl=pretty(t.get("expl_bks", "")), merksatz=pretty(t.get("merksatz_de", "")),
                    picture=q["id"] in notes, answer=LETTERS[q["answer"]])

    general = [item(q) for q in questions if q["state"] is None]
    states = []
    for code, name in meta["states"].items():
        states.append(dict(code=code, name=name, questions=[item(q) for q in questions if q["state"] == code]))

    # Practice tests: the 300 general questions, shuffled once with a fixed seed and cut into
    # 10 tests of 30, so the tests together cover every general question exactly once.
    ids = [g["id"] for g in general]
    random.Random(SEED).shuffle(ids)
    by_id = {g["id"]: g for g in general}
    tests = []
    for n in range(N_TESTS):
        chunk = [by_id[i] for i in ids[n * 30:(n + 1) * 30]]
        tests.append(dict(n=n + 1, questions=[dict(num=c["num"], q_de=c["q_de"], picture=c["picture"],
                                                   options=[dict(letter=o["letter"], de=o["de"]) for o in c["options"]],
                                                   answer=c["answer"]) for c in chunk]))

    gl = sorted(((k, v) for k, v in glossary.items()), key=lambda kv: kv[0].lower().lstrip('"'))
    data = dict(
        meta=dict(title="Einbürgerungstest & Leben in Deutschland", languages="Deutsch – Bosnisch/Kroatisch/Serbisch",
                  catalog_source=meta["publisher"] + " – " + meta["title"], catalog_retrieved="17.09.2026",
                  imprint="[IMPRESSUM: Verlag / Name]", draft=bool(missing)),
        general=general, states=states, tests=tests,
        glossary=[dict(de=k, bks=v) for k, v in gl],
    )
    (ROOT / "build").mkdir(exist_ok=True)
    (ROOT / "build" / "book_data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    (ROOT / "out").mkdir(exist_ok=True)
    pdf = ROOT / "out" / "interior_de-bks.pdf"
    typst.compile(str(ROOT / "layout" / "book.typ"), output=str(pdf), root=str(ROOT),
                  font_paths=[str(ROOT / "layout" / "fonts")])
    pages = count_pages(pdf)
    info = dict(pages=pages, missing_translations=len(missing), questions=len(questions), tests=N_TESTS)
    (ROOT / "out" / "build_info.json").write_text(json.dumps(info, indent=1))
    print(json.dumps(info))


def count_pages(pdf):
    try:
        import fitz
        return fitz.open(pdf).page_count
    except ImportError:
        return len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))


if __name__ == "__main__":
    main()
