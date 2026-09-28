#!/usr/bin/env python3
"""Assemble the book data and typeset the interior PDF with Typst.

Usage: build_book.py [--draft]
  --draft  typeset even if translations are missing (placeholders are printed)

Reads kdp/release.json: while a required release field is empty the book is a DRAFT
(watermark on every page, imprint lists what is missing).

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
    s = re.sub(r"\s*©.*$", "", s)  # photo credits belong to the (omitted) photos
    s = s.replace(" In Anlehnung an Bundeswahlordnung (BWO), Anlage 26", "")
    return s.strip()


def has_word(text, kw):
    return re.search(r"(?<![\wäöüß])" + re.escape(kw) + r"(?![\wäöüß])", text, re.I) is not None


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
    learning = json.load(open(ROOT / "content" / "learning_bks.json", encoding="utf-8"))
    topics = json.load(open(ROOT / "content" / "topics.json", encoding="utf-8"))
    prov = json.load(open(ROOT / "content" / "image_provenance.json", encoding="utf-8"))
    release = json.load(open(ROOT / "kdp" / "release.json", encoding="utf-8"))
    missing = [q["id"] for q in questions if q["id"] not in bks]
    if missing and not args.draft:
        sys.exit(f"{len(missing)} questions have no translation (e.g. {missing[:5]}); run validate_content.py or use --draft")
    missing_release = [k for k in release["required"] if not release.get(k)]
    use_images = bool(release.get("images", True))

    def images_of(q):
        if not use_images or q["id"] not in prov["included"]:
            return None
        files = ["/layout/images/" + f["file"] for f in prov["included"][q["id"]]]
        return dict(files=files, layout="row" if len(files) == 4 else "single")

    def item(q):
        t = bks.get(q["id"], {})

        def tr(i, o):
            if not t:
                return "[prijevod u izradi]"
            b = pretty(t["options_bks"][i])
            same = re.sub(r"[\W_]+", "", b).lower() == re.sub(r"[\W_]+", "", pretty(o)).lower()
            return "" if same else b  # names and numbers are not printed twice

        opts = []
        for i, o in enumerate(q["options"]):
            de, b = pretty(o), tr(i, o)
            opts.append(dict(letter=LETTERS[i], de=de, bks=b, correct=(i == q["answer"]),
                             stack=len(de) + len(b) > 62))  # long pairs: translation on its own line
        label = str(q["num"]) if q["state"] is None else f"{q['state']} {q['num']}"
        return dict(id=q["id"], label=label, num=q["num"], state=q["state"], q_de=pretty(q["question"]),
                    q_bks=pretty(t.get("q_bks", "[prijevod u izradi]")), options=opts,
                    expl=pretty(t.get("expl_bks", "")), merksatz=pretty(t.get("merksatz_de", "")),
                    images=images_of(q), photo_missing=q["id"] in prov["excluded"] and q["id"] in notes,
                    answer=LETTERS[q["answer"]])

    def test_item(c):  # German only, no marked answer - like the exam
        return dict(id=c["id"], num=c["num"], label=c["label"], q_de=c["q_de"], images=c["images"], photo_missing=c["photo_missing"],
                    options=[dict(letter=o["letter"], de=o["de"]) for o in c["options"]], answer=c["answer"])

    general = [item(q) for q in questions if q["state"] is None]
    states = [dict(code=code, name=name, bks_name=learning["state_names_bks"][code],
                   questions=[item(q) for q in questions if q["state"] == code])
              for code, name in meta["states"].items()]

    # Practice tests = full exam simulations: 30 general questions (the 300 are shuffled once with a
    # fixed seed and cut into 10 tests, so together they cover every general question exactly once)
    # + 3 questions of the reader's own state, taken from the answer-free state appendix.
    ids = [g["id"] for g in general]
    random.Random(SEED).shuffle(ids)
    by_id = {g["id"]: g for g in general}
    tests = []
    for n in range(N_TESTS):
        chunk = [by_id[i] for i in ids[n * 30:(n + 1) * 30]]
        state_nums = [((3 * n + k) % 10) + 1 for k in range(3)]  # each state question used 3 times
        tests.append(dict(n=n + 1, questions=[test_item(c) for c in chunk], state_nums=state_nums,
                          photo_missing=[c["num"] for c in chunk if c["photo_missing"]]))
    state_appendix = [dict(code=s["code"], name=s["name"], questions=[test_item(c) for c in s["questions"]])
                      for s in states]
    state_key = [dict(code=s["code"], name=s["name"], answers=[c["answer"] for c in s["questions"]]) for s in states]

    # ---- learning aids -------------------------------------------------------------------
    gen_by_num = {q["num"]: q for q in questions if q["state"] is None}
    for e in learning["timeline"]:
        for num, kw in e["refs"]:
            q = gen_by_num[num]
            if kw.lower() not in (q["question"] + " " + " ".join(q["options"])).lower():
                sys.exit(f"timeline: question {num} does not mention '{kw}'")
        e["nums"] = sorted({num for num, _ in e["refs"]})
    for inst in learning["institutions"]:
        inst["nums"] = [q["num"] for q in questions if q["state"] is None
                        and any(k.lower() in q["question"].lower() for k in inst["kw"])]
    for w in learning["words"]:
        w["nums"] = [q["num"] for q in questions if q["state"] is None and any(has_word(q["question"], k) for k in w["kw"])]
    topic_rows = []
    for key, (hr, de) in learning["topics"].items():
        nums = [int(i[2:]) for i, ts in topics.items() if i.startswith("G-") and key in ts]
        n_state = sum(1 for i, ts in topics.items() if not i.startswith("G-") and key in ts)
        topic_rows.append(dict(key=key, bks=hr, de=de, nums=sorted(nums), state_count=n_state))

    gl = sorted(((k, v) for k, v in glossary.items()), key=lambda kv: kv[0].lower().lstrip('"'))
    data = dict(
        meta=dict(title="Einbürgerungstest & Leben in Deutschland", languages="Deutsch – Bosnisch/Kroatisch/Serbisch",
                  catalog_source=meta["publisher"] + " – " + meta["title"],
                  draft=bool(missing or missing_release), missing_release=missing_release, release=release,
                  catalogue_url=prov["qr"], images=use_images),
        general=general, states=states, tests=tests, state_appendix=state_appendix, state_key=state_key,
        timeline=learning["timeline"], institutions=learning["institutions"], words=learning["words"],
        topics=topic_rows, state_pattern=learning["state_pattern"],
        glossary=[dict(de=k, bks=v) for k, v in gl],
    )
    (ROOT / "build").mkdir(exist_ok=True)
    (ROOT / "build" / "book_data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    (ROOT / "out").mkdir(exist_ok=True)
    pdf = ROOT / "out" / "interior_de-bks.pdf"
    typst.compile(str(ROOT / "layout" / "book.typ"), output=str(pdf), root=str(ROOT),
                  font_paths=[str(ROOT / "layout" / "fonts")])
    pages = count_pages(pdf)
    info = dict(pages=pages, missing_translations=len(missing), questions=len(questions), tests=N_TESTS,
                draft=data["meta"]["draft"], missing_release=missing_release, images=use_images)
    (ROOT / "out" / "build_info.json").write_text(json.dumps(info, indent=1))
    print(json.dumps(info))


def count_pages(pdf):
    try:
        import pymupdf
        return pymupdf.open(pdf).page_count
    except ImportError:
        return len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))


if __name__ == "__main__":
    main()
