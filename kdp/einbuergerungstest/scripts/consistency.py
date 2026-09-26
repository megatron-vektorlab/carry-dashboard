#!/usr/bin/env python3
"""Make BKS naming consistent across all translation batches (run before validate_content.py).

Ten translators worked in parallel; this pass unifies the few names they rendered differently.
Only BKS fields (q_bks, options_bks, expl_bks) are touched - never the German catalogue text or
the Merksätze. Every change is logged to content/consistency_log.md.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Croatian standard names (hr. Wikipedia / Hrvatski jezični portal); case forms listed explicitly.
RULES = [
    (r"Zapadna Pomeranija", "Zapadno Pomorje"), (r"Zapadne Pomeranije", "Zapadnog Pomorja"),
    (r"Zapadnoj Pomeraniji", "Zapadnom Pomorju"), (r"Zapadnu Pomeraniju", "Zapadno Pomorje"),
    (r"Zapadnom Pomeranijom", "Zapadnim Pomorjem"),
    (r"Meklenburg", "Mecklenburg"),
    (r"(?<!\()\bElba\b", "Laba"), (r"(?<!\()\bElbe\b(?!\))", "Labe"), (r"(?<!\()\bElbi\b", "Labi"),
    (r"(?<!\()\bElbu\b", "Labu"), (r"(?<!\()\bElbom\b", "Labom"),
    (r"Donja Saksonija", "Donja Saska"), (r"Donje Saksonije", "Donje Saske"), (r"Donjoj Saksoniji", "Donjoj Saskoj"),
    (r"Tiringen", "Tiringija"),
    (r"Sjeverna Rajna – Vestfalija", "Sjeverna Rajna-Vestfalija"),
    (r"Rajna-Falačka", "Porajnje-Falačka"),
]


# Item-level edits after human/orchestrator review: (id, field, old text, new text).
MANUAL = [
    ("G-150", "q_bks", "Sudac porotnik (Gerichtsschöffe) u Njemačkoj je …", "Porotnik (Gerichtsschöffe) u Njemačkoj je …"),
    ("G-150", "expl_bks", "Sudac porotnik (Gerichtsschöffe) je građanin koji zajedno",
     "Porotnik (Gerichtsschöffe) je građanin koji kao sudac porotnik zajedno"),
    ("G-268", "expl_bks", " ili na više od deset stranih jezika, među njima i na hrvatskom.", " ili na više od deset stranih jezika."),
    ("G-075", "expl_bks", "a Bodo Ramelow ministar predsjednik (Ministerpräsident) Tiringije.",
     "a Bodo Ramelow bio je ministar predsjednik (Ministerpräsident) Tiringije."),
]


def fix(s, log, qid, field):
    for pat, rep in RULES:
        new = re.sub(pat, rep, s)
        if new != s:
            log.append(f"- `{qid}` {field}: `{pat}` → `{rep}`")
            s = new
    return s


def main():
    log = []
    for f in sorted((ROOT / "content" / "batches").glob("batch_*_output.json")):
        items = json.load(open(f, encoding="utf-8"))
        for t in items:
            for mid, field, old, new in MANUAL:
                if t["id"] == mid and old in t[field]:
                    t[field] = t[field].replace(old, new)
                    log.append(f"- `{mid}` {field}: manual edit → „{new}”")
            t["q_bks"] = fix(t["q_bks"], log, t["id"], "q_bks")
            t["expl_bks"] = fix(t["expl_bks"], log, t["id"], "expl_bks")
            t["options_bks"] = [fix(o, log, t["id"], "option") for o in t["options_bks"]]
        f.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    logf = ROOT / "content" / "consistency_log.md"
    prev = logf.read_text(encoding="utf-8") if logf.exists() else "# Consistency pass (appended per run)\n"
    logf.write_text(prev + f"\n## Run: {len(log)} changes\n" + "\n".join(log) + "\n", encoding="utf-8")
    print(f"{len(log)} changes")


if __name__ == "__main__":
    main()
