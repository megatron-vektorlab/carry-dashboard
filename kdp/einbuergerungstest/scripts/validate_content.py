#!/usr/bin/env python3
"""Merge the translation batches into content/bks.json and run automatic checks.

Errors (build fails): missing/extra ids, wrong option count, empty fields, forbidden words,
missing picture note, duplicate option translations, out-of-range lengths.
Warnings (listed for human review): glossary term not rendered as locked, numbers in the
German question missing from the translation.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Promises are errors; "official" wording is only flagged, because the catalogue itself needs
# terms like "Amtssprache" / "službeni jezik".
FORBIDDEN = re.compile(r"\b(garantira\w*|zajamčen\w* prolaz|sigurno ćete)\b", re.I)
OFFICIAL = re.compile(r"\b(offiziell\w*|amtlich\w*|službeno|službeni)\b", re.I)
# German term in the question -> stem that must appear in the BKS question/options
GLOSSARY_CHECKS = {
    "Bundestag": "Bundestag", "Bundesrat": "Bundesrat", "Grundgesetz": "Temeljn",
    "Landtag": "Landtag", "Bundesverfassungsgericht": "Savezn", "Meinungsfreiheit": "sloboda mišljenja",
    "Pressefreiheit": "sloboda tiska", "Religionsfreiheit": "vjeroispovijesti", "Rechtsstaat": "pravn",
    "Gewaltenteilung": "podjel", "Ministerpräsident": "Ministerpräsident", "Bundeskanzler": "kancelar",
    "Bundespräsident": "predsjedni", "DDR": "DDR", "Europäische Union": "Europsk",
}


def words(s):
    return len(re.findall(r"\w+", s))


def main():
    catalog = json.load(open(ROOT / "data" / "catalog.json", encoding="utf-8"))["questions"]
    notes = json.load(open(ROOT / "content" / "image_notes_bks.json", encoding="utf-8"))["notes"]
    by_id = {q["id"]: q for q in catalog}
    merged, errors, warnings = {}, [], []
    for f in sorted((ROOT / "content" / "batches").glob("batch_*_output.json")):
        for item in json.load(open(f, encoding="utf-8")):
            if item["id"] in merged:
                errors.append(f"{item['id']}: duplicate (in {f.name})")
            merged[item["id"]] = item
    missing = [i for i in by_id if i not in merged]
    extra = [i for i in merged if i not in by_id]
    errors += [f"{i}: missing translation" for i in missing] + [f"{i}: unknown id" for i in extra]

    for qid, t in merged.items():
        q = by_id.get(qid)
        if not q:
            continue
        for k in ("q_bks", "expl_bks", "merksatz_de"):
            if not str(t.get(k, "")).strip():
                errors.append(f"{qid}: empty {k}")
        opts = t.get("options_bks", [])
        if len(opts) != 4 or not all(str(o).strip() for o in opts):
            errors.append(f"{qid}: options_bks must be 4 non-empty strings")
        elif len({o.strip().lower() for o in opts}) < 4:
            errors.append(f"{qid}: duplicate option translations {opts}")
        n = words(t.get("expl_bks", ""))
        if not 20 <= n <= 80:
            errors.append(f"{qid}: explanation has {n} words")
        m = words(t.get("merksatz_de", ""))
        if m > 14:
            errors.append(f"{qid}: Merksatz has {m} words")
        blob = " ".join([t.get("q_bks", ""), t.get("expl_bks", ""), t.get("merksatz_de", "")] + list(opts))
        if FORBIDDEN.search(blob):
            errors.append(f"{qid}: forbidden word '{FORBIDDEN.search(blob).group(0)}'")
        if OFFICIAL.search(blob):
            warnings.append(f"{qid}: check wording '{OFFICIAL.search(blob).group(0)}' (must not describe this book)")
        if qid in notes and notes[qid][:25] not in t.get("expl_bks", ""):
            warnings.append(f"{qid}: picture note not quoted verbatim at the start of the explanation")
        bks_q = t.get("q_bks", "") + " " + " ".join(opts)
        for de, stem in GLOSSARY_CHECKS.items():
            if de in q["question"] and stem.lower() not in bks_q.lower():
                warnings.append(f"{qid}: '{de}' not rendered with locked term (expected '{stem}')")
        for num in re.findall(r"\d+", q["question"]):
            if num not in t.get("q_bks", ""):
                warnings.append(f"{qid}: number {num} missing in q_bks")

    out = [dict(merged[q["id"]]) for q in catalog if q["id"] in merged]
    (ROOT / "content" / "bks.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    report = ["# Content validation (DE–BKS)", "", f"- Items: {len(out)}/{len(catalog)}",
              f"- Errors: {len(errors)}", f"- Warnings: {len(warnings)}", ""]
    report += ["## Errors"] + [f"- {e}" for e in errors] + ["", "## Warnings"] + [f"- {w}" for w in warnings]
    (ROOT / "content" / "validation_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report[:5]))
    if errors:
        print("\n".join(errors[:40]), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
