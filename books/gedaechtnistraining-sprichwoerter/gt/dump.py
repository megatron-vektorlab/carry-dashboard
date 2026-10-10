"""Plain-text dump of the book for reviewers.

    python3 -m gt.dump        -> build/review/sheets.md (participant pages), leader.md, solutions.json

The participant dump never contains answers, so it can be given to a blind tester.
"""
from __future__ import annotations

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "review")
GAP = "_____"


def joined(a, mid, b):
    tight = not b or b[0] in ",.!?"
    return (a + " " if a else "") + mid + ("" if tight else " ") + b


def gap_of(it):
    if it.get("boxes"):
        return it["first"] + " " + "□ " * (it["boxes"] - 1)
    return GAP


def sheet_text(s) -> str:
    L = [f"## Blatt {s['num']}: {s['title']}  (Kapitel: {s['chapter']}, Stufe {s['level']})", f"Aufgabe: {s['task']}"]
    ex = s.get("example")
    t = s["type"]
    if "bank" in s:
        L.append("Kasten: " + " · ".join(s["bank"]))
    if t == "gaps":
        if ex:
            L.append(f"Beispiel: {joined(ex['parts'][0], '[' + ex['answer'] + ']', ex['parts'][1])}")
        L += [f"{i}. {joined(it['parts'][0], gap_of(it), it['parts'][1])}" for i, it in enumerate(s["items"], 1)]
    elif t == "circle":
        if ex:
            L.append(f"Beispiel: {joined(ex['parts'][0], GAP, ex['parts'][1])}   Wörter: {' / '.join(ex['options'])}  → eingekreist: {ex['answer']}")
        L += [f"{i}. {joined(it['parts'][0], GAP, it['parts'][1])}   Wörter: {' / '.join(it['options'])}" for i, it in enumerate(s["items"], 1)]
    elif t == "match":
        L += [f"{i}. {l}" for i, l in enumerate(s["left"], 1)]
        L += [f"{'ABCDEFGHIJ'[i]}) {r}" for i, r in enumerate(s["right"])]
    elif t == "complete":
        if ex:
            L.append(f"Beispiel: {ex['start']} → {(ex.get('given', '') + ' ' + ex['answer']).strip()}")
        L += [f"{i}. {it['start']}   Linie: {it.get('hint', '')}______" for i, it in enumerate(s["items"], 1)]
    elif t == "scramble":
        if ex:
            L.append(f"Beispiel: [{'] ['.join(ex['tiles'])}] → {ex['answer']}")
        L += [f"{i}. [{'] ['.join(it['tiles'])}]   Linie: {it.get('first', '')} ______" for i, it in enumerate(s["items"], 1)]
    elif t == "wrong":
        if ex:
            L.append(f"Beispiel: {''.join(ex['parts'])}  (falsch: {ex['parts'][1]}, richtig: {ex['answer']})")
        L += [f"{i}. {it['shown']}   Richtig heißt es: ______" for i, it in enumerate(s["items"], 1)]
    elif t == "firstletters":
        L += [f"{i}. " + " ".join(st["first"] + "_" * (st["len"] - 1) + st.get("punct", "") for st in it["stubs"])
              for i, it in enumerate(s["items"], 1)]
    elif t in ("choice", "situation"):
        for i, it in enumerate(s["items"], 1):
            L.append(f"{i}. {it['phrase']}")
            L += [f"   {'abc'[k]}) {o}" for k, o in enumerate(it["options"])]
    elif t == "wordsearch":
        L.append("Wörter: " + ", ".join(s["words"]))
        L += ["   " + " ".join(r) for r in s["grid"]]
    elif t == "story":
        L += s["paragraphs"]
        L.append("Ende: " + joined(s["parts"][0], GAP, s["parts"][1]) + "   Wörter: " + " / ".join(s["options"]))
    return "\n".join(L)


def solution_text(s) -> list[str]:
    out = []
    for x in s["solution"]:
        line = x["before"] + (f"**{x['word']}**" if x["word"] else "") + x["after"]
        if x.get("variants"):
            line += " (auch: " + " / ".join(x["variants"]) + ")"
        out.append(line)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    data = json.load(open(os.path.join(ROOT, "build", "book", "data.json")))
    sheets, leaders, sols = [], [], {}
    for u in data["units"]:
        s, L = u["sheet"], u["leader"]
        sheets.append(sheet_text(s))
        sols[s["num"]] = solution_text(s)
        leaders.append("\n".join([f"## Blatt {L['num']} – Für die Gruppenleitung ({L['title']}, {L['chapter']})",
                                  f"Übt: {L['trains']} · etwa {L['minutes']} Minuten",
                                  "So geht's: " + " | ".join(L["steps"]),
                                  "Lösungen: " + " | ".join(solution_text(s)),
                                  "Hilfen: " + " | ".join(L["hints"]),
                                  "Zum Gespräch: " + " | ".join(L["prompts"]),
                                  f"Leichter: {L['easier']} | Anspruchsvoller: {L['harder']}",
                                  f"Achtsam: {L['note']}" if L.get("note") else ""]))
    open(os.path.join(OUT, "sheets.md"), "w").write("\n\n".join(sheets) + "\n")
    open(os.path.join(OUT, "leader.md"), "w").write("\n\n".join(leaders) + "\n")
    json.dump(sols, open(os.path.join(OUT, "solutions.json"), "w"), ensure_ascii=False, indent=1)
    ch = []
    for c in data["chapters"]:
        ch.append(f"## Kapitel {c['num']}: {c['name']}\n{c['intro']}\nAufwärmen: " +
                  " | ".join(w["a"] + " " + w["b"] for w in c["warmup"]) + "\nZum Erzählen: " + " | ".join(c["talk"]) +
                  "\nIn Bewegung: " + " | ".join(c["move"]) + "\nZum Mitbringen: " + " | ".join(c["props"]))
    open(os.path.join(OUT, "chapters.md"), "w").write("\n\n".join(ch) + "\n")
    print(f"review dumps in {os.path.relpath(OUT, ROOT)}/")


if __name__ == "__main__":
    main()
