"""Export the generated book as plain review files for blind re-solving.

    .venv/bin/python -m asvab.export_review       # -> build/review/*.txt

For each chapter / test section two files are written:
  <set>.questions.txt   stems + choices only (no answers, no solutions)
  <set>.key.txt         answer letter, solution steps, traps
A reviewer solves the questions file blind, then compares with the key.
"""
from __future__ import annotations

from .build import generate_all
from .generate import load_chapters
from .render import BUILD, LETTERS


def q_text(i, p):
    lines = [f"{i}. {p.stem}"]
    if p.figure:
        lines.append(f"   [FIGURE TikZ: {' '.join(p.figure.split())}]")
    for k, (t, _) in enumerate(p.choices):
        lines.append(f"   ({LETTERS[k]}) {t}")
    return "\n".join(lines)


def k_text(i, p):
    lines = [f"{i}. ANSWER {LETTERS[p.key]} = {p.choices[p.key][0]}   [{p.template} L{p.level}]"]
    for j, s in enumerate(p.steps, 1):
        lines.append(f"   step {j}: {s}")
    if p.tip:
        lines.append(f"   tip: {p.tip}")
    for k, (t, why) in enumerate(p.choices):
        if why:
            lines.append(f"   why not ({LETTERS[k]}): {why}")
    return "\n".join(lines)


def main():
    mods = load_chapters()
    chapters, diag, tests = generate_all(mods)
    out = BUILD / "review"
    out.mkdir(parents=True, exist_ok=True)
    sets = [(f"ch{m.NUM:02d}", chapters[m.NUM]) for m in mods]
    sets.append(("diagnostic", diag))
    for k, (ar, mk) in enumerate(tests, 1):
        sets += [(f"test{k}-AR", ar), (f"test{k}-MK", mk)]
    for name, ps in sets:
        (out / f"{name}.questions.txt").write_text(
            "\n\n".join(q_text(i, p) for i, p in enumerate(ps, 1)) + "\n", encoding="utf-8")
        (out / f"{name}.key.txt").write_text(
            "\n\n".join(k_text(i, p) for i, p in enumerate(ps, 1)) + "\n", encoding="utf-8")
    print(out, len(sets), "sets")


if __name__ == "__main__":
    main()
