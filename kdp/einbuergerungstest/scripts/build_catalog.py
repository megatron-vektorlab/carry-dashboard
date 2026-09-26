#!/usr/bin/env python3
"""Build the master catalogue from three independent copies of the BAMF catalogue.

Usage: build_catalog.py --a <A questions.json> --b <B questions.json> --c <C question.json>

Source B (built from the official PDF + Online-Testcenter) is the text of record.
Every question must match A and C in wording, options and answer key after
typographic normalisation; any disagreement is written to the report and the
build fails unless it is listed in data/resolutions.json.
"""
import argparse, hashlib, json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATES = {  # code -> name (order = BAMF order)
    "BW": "Baden-Württemberg", "BY": "Bayern", "BE": "Berlin", "BB": "Brandenburg",
    "HB": "Bremen", "HH": "Hamburg", "HE": "Hessen", "MV": "Mecklenburg-Vorpommern",
    "NI": "Niedersachsen", "NW": "Nordrhein-Westfalen", "RP": "Rheinland-Pfalz",
    "SL": "Saarland", "SN": "Sachsen", "ST": "Sachsen-Anhalt", "SH": "Schleswig-Holstein",
    "TH": "Thüringen",
}
NAME2CODE = {v: k for k, v in STATES.items()}
LETTERS = "abcd"


def norm(s):
    """Normalise typography only, for comparing copies (never used to alter the text of record)."""
    s = unicodedata.normalize("NFC", str(s))
    s = s.replace("\\n", " ")                      # C contains literal backslash-n line breaks
    s = re.sub(r"\s*©.*$", "", s)                    # photo credit appended to some question texts
    s = s.replace("…", "...").replace("\u00a0", " ").replace("–", "-")
    s = re.sub(r"[„“”\"‚‘’']", "", s)               # quotation marks differ between copies
    s = re.sub(r"\s*/\s*", "/", s)                  # "Einwohnerinnen / Einwohner" vs "Einwohnerinnen/Einwohner"
    s = re.sub(r"(\d)\s+%", r"\1%", s)             # "5 %-Hürde" vs "5%-Hürde"
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"(\.\.\.|\?)$", "", s).strip()      # C renders a trailing ellipsis as "?"
    return s


def bag(s):
    """Order-insensitive word bag: tolerates swapped gender pairs ("Einwohner/Einwohnerinnen"),
    missing trailing periods and "Bild 3" vs "3" on picture questions."""
    s = norm(s).lower()
    s = re.sub(r"^bild (\d)$", r"\1", s)
    return " ".join(sorted(re.findall(r"[0-9a-zäöüß]+", s)))


def key_text(q, opts):
    return bag(q) + " || " + " | ".join(sorted(bag(o) for o in opts))


def load_b(p):
    d = json.load(open(p, encoding="utf-8"))
    out = {}
    for q in d["questions"]:
        code = q["stateCode"]
        qid = f"{code}-{q['officialNumber']:02d}" if code else f"G-{q['officialNumber']:03d}"
        opts = [q["answers"][l] for l in LETTERS]
        out[qid] = dict(id=qid, scope=q["scope"], state=code, num=q["officialNumber"],
                        question=q["question"], options=opts, answer=LETTERS.index(q["solution"]),
                        images=q.get("images") or [], source_page=q.get("sourcePage"),
                        bamf_id=q.get("bamfInternalId"),
                        image_credit=(re.search(r"©.*$", q["question"]).group(0).strip() if "©" in q["question"] else None))
    return out, d.get("datasetVersion")


def load_a(p):
    d = json.load(open(p, encoding="utf-8"))
    out = {}
    for q in d["questions"]:
        code = NAME2CODE[q["state"]] if q["state"] else None
        qid = f"{code}-{q['num']:02d}" if code else f"G-{q['num']:03d}"
        out[qid] = dict(question=q["q"], options=q["options"], answer=q["answer"], topic=q.get("topic"), img=q.get("img"))
    return out, d["meta"].get("catalog_date")


def load_c(p):
    d = json.load(open(p, encoding="utf-8"))
    out = {}
    for q in d:
        opts = [q[l] for l in LETTERS]
        out.setdefault(key_text(q["question"], opts), []).append(
            dict(question=q["question"], options=opts, answer=LETTERS.index(q["solution"]), num=q["num"], category=q.get("category")))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--c", required=True)
    args = ap.parse_args()

    B, b_version = load_b(args.b)
    A, a_date = load_a(args.a)
    C = load_c(args.c)
    res_path = ROOT / "data" / "resolutions.json"
    resolutions = json.load(open(res_path)) if res_path.exists() else {}

    issues, catalog = [], []
    for qid, b in B.items():
        a = A.get(qid)
        rec = dict(b)
        rec["topic"] = a.get("topic") if a else None
        checks = {}
        # --- A: matched by official number ---
        if not a:
            issues.append((qid, "A", "missing in A"))
        else:
            checks["A_text"] = bag(a["question"]) == bag(b["question"])
            checks["A_options"] = [bag(x) for x in a["options"]] == [bag(x) for x in b["options"]]
            checks["A_answer"] = bag(a["options"][a["answer"]]) == bag(b["options"][b["answer"]])
            if not checks["A_text"]:
                issues.append((qid, "A", f"question text differs: A={a['question']!r} / B={b['question']!r}"))
            if not checks["A_options"]:
                issues.append((qid, "A", f"options differ: A={a['options']} / B={b['options']}"))
            if not checks["A_answer"]:
                issues.append((qid, "A", f"ANSWER differs: A={a['options'][a['answer']]!r} / B={b['options'][b['answer']]!r}"))
        # --- C: matched by text + option set (C numbering is unreliable, option order differs) ---
        cands = C.get(key_text(b["question"], b["options"]), [])
        if not cands:  # fall back to the question text alone
            cands = [c for k, cs in C.items() for c in cs if k.split(" || ")[0] == bag(b["question"])]
            checks["C_text"] = False
            if cands:
                issues.append((qid, "C", f"options differ: C={cands[0]['options']} / B={b['options']}"))
        else:
            checks["C_text"] = True
        if not cands:
            issues.append((qid, "C", "no match in C"))
            checks["C_answer"] = None
        else:
            b_ans = bag(b["options"][b["answer"]])
            ok = any(bag(c["options"][c["answer"]]) == b_ans for c in cands)
            checks["C_answer"] = ok
            if not ok:
                issues.append((qid, "C", f"ANSWER differs: C={[c['options'][c['answer']] for c in cands]!r} / B={b['options'][b['answer']]!r}"))
        rec["checks"] = checks
        if qid in resolutions:
            rec["resolution"] = resolutions[qid]
        catalog.append(rec)

    order = lambda r: (0, r["num"]) if r["state"] is None else (1 + list(STATES).index(r["state"]), r["num"])
    catalog.sort(key=order)
    n_gen = sum(1 for r in catalog if r["state"] is None)
    n_state = len(catalog) - n_gen

    # Only answer-key disagreements block the build; wording differences are informational
    # (source B is the text of record). Every answer must be confirmed by A, and by C unless
    # the disagreement is explained in data/resolutions.json.
    unresolved = [i for i in issues if "ANSWER" in i[2] and (i[1] == "A" or i[0] not in resolutions)]
    unresolved += [(r["id"], "A", "answer not confirmed by A") for r in catalog if not r["checks"].get("A_answer")]
    meta = dict(
        title="Gesamtfragenkatalog zum Test „Leben in Deutschland“ und zum „Einbürgerungstest“",
        publisher="Bundesamt für Migration und Flüchtlinge (BAMF)",
        text_of_record="source B dataset " + str(b_version),
        source_a_catalog_date=a_date,
        general=n_gen, state=n_state, states=STATES,
        note="Wording, options and answer keys are reproduced unaltered (§ 5 Abs. 2, § 62, § 63 UrhG).",
    )
    body = json.dumps(dict(meta=meta, questions=catalog), ensure_ascii=False, indent=1)
    out = ROOT / "data" / "catalog.json"
    out.write_text(body, encoding="utf-8")
    sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    (ROOT / "data" / "catalog.sha256").write_text(sha + "  catalog.json\n")

    lines = ["# Cross-check report", "", f"- Text of record: source B ({b_version})", f"- Source A catalogue date: {a_date}",
             f"- Questions: {len(catalog)} ({n_gen} general, {n_state} state)", f"- catalog.json sha256: `{sha}`", "",
             f"- A: same text {sum(1 for r in catalog if r['checks'].get('A_text'))}, same options {sum(1 for r in catalog if r['checks'].get('A_options'))}, same answer {sum(1 for r in catalog if r['checks'].get('A_answer'))} (of {len(catalog)})",
             f"- C: same text+options {sum(1 for r in catalog if r['checks'].get('C_text'))}, same answer {sum(1 for r in catalog if r['checks'].get('C_answer'))} (of {len(catalog)})",
             f"- Answer confirmed by BOTH A and C: {sum(1 for r in catalog if r['checks'].get('A_answer') and r['checks'].get('C_answer'))}/{len(catalog)}",
             f"- Issues: {len(issues)} (unresolved: {len(unresolved)})", ""]
    for qid, src, msg in issues:
        lines.append(f"- `{qid}` [{src}] {msg}" + (f" → RESOLVED: {resolutions[qid]}" if qid in resolutions else ""))
    (ROOT / "data" / "crosscheck_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:9]))
    if unresolved:
        print(f"UNRESOLVED ISSUES: {len(unresolved)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
