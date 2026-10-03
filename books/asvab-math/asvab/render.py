"""LaTeX rendering of problems, solutions and chapters."""
from __future__ import annotations

import pathlib
import subprocess

from .core import Problem

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
BUILD = ROOT / "build"
LETTERS = "ABCD"


def figure_tex(fig: str | None) -> str:
    if not fig:
        return ""
    body = fig.strip()
    if not body.startswith(r"\begin{tikzpicture}"):
        body = r"\begin{tikzpicture}" + "\n" + body + "\n" + r"\end{tikzpicture}"
    return r"\probfig{" + body + "}\n"


def problem_tex(p: Problem, number: int | str) -> str:
    ch = "".join("{" + t + "}" for t, _ in p.choices)
    return (f"\\begin{{problem}}{{{number}}}\n{p.stem}\n"
            f"{figure_tex(p.figure)}\\choices{ch}\n\\end{{problem}}\n")


def solution_tex(p: Problem, number: int | str) -> str:
    letter = LETTERS[p.key]
    ans = p.choices[p.key][0]
    out = [f"\\begin{{solution}}{{{number}}}{{{letter}}}{{{ans}}}"]
    for i, s in enumerate(p.steps, 1):
        out.append(f"\\step{{{i}}}{{{s}}}")
    if p.tip:
        out.append(f"\\tipline{{{p.tip}}}")
    traps = [f"({LETTERS[i]}) {why.rstrip('.')}." for i, (_, why) in enumerate(p.choices)
             if why and i != p.key]
    if traps:
        out.append(f"\\trapline{{{' '.join(traps)}}}")
    out.append("\\end{solution}")
    return "\n".join(out) + "\n"


def answer_key_tex(problems: list[Problem], start: int = 1, cols: int = 5,
                   extra=None) -> str:
    """Grid of '12 C' entries; extra(i, p) may append text (e.g. chapter ref)."""
    n = len(problems)
    rows = (n + cols - 1) // cols
    lines = [r"\begin{center}\small\renewcommand{\arraystretch}{1.15}",
             r"\begin{tabular}{" + "l" * cols + "}", r"\toprule"]
    for r in range(rows):
        cells = []
        for c in range(cols):
            i = c * rows + r
            if i < n:
                p = problems[i]
                cell = f"\\keyentry{{{start + i}}}{{{LETTERS[p.key]}}}"
                if extra:
                    cell += extra(i, p)
                cells.append(cell)
            else:
                cells.append("")
        lines.append(" & ".join(cells) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{center}"]
    return "\n".join(lines) + "\n"


def problems_block(problems: list[Problem], start: int = 1) -> str:
    body = "".join(problem_tex(p, start + i) for i, p in enumerate(problems))
    return "\\begin{multicols}{2}\n" + body + "\\end{multicols}\n"


def solutions_block(problems: list[Problem], start: int = 1) -> str:
    body = "".join(solution_tex(p, start + i) for i, p in enumerate(problems))
    return "\\begin{multicols}{2}\n" + body + "\\end{multicols}\n"


SECTION_NAMES = {"AR": "Arithmetic Reasoning", "MK": "Mathematics Knowledge"}


def chapter_tex(mod, problems: list[Problem]) -> str:
    n = len(problems)
    secs = sorted({p.section for p in problems}, key=lambda s: s != "MK")
    meta = " \\textbullet{} ".join(SECTION_NAMES[s] for s in secs)
    minutes = round(sum(1.2 if p.section == "AR" else 1.0 for p in problems))
    lv = [sum(1 for p in problems if p.level == k) for k in (1, 2, 3)]
    out = [
        f"\\chapter{{{mod.TITLE}}}\\label{{ch:{mod.NUM}}}",
        f"\\chaptermeta{{Tested on: {meta}}}",
        "\\section*{Key Concepts}",
        mod.INTRO.strip(),
        "\\needspace{0.45\\textheight}",
        f"\\section*{{Practice Set {mod.NUM}}}",
        f"\\scoreline{{{n}}}{{{minutes}}}",
        (f"{{\\small\\color{{mid}}Problems 1--{lv[0]} are warm-ups, "
         f"{lv[0] + 1}--{lv[0] + lv[1]} are test level, and "
         f"{lv[0] + lv[1] + 1}--{n} are challenge problems.}}\\par\\medskip"),
        problems_block(problems),
        "\\clearpage",
        f"\\section*{{Answers \\& Explanations {mod.NUM}}}",
        answer_key_tex(problems),
        solutions_block(problems),
    ]
    return "\n".join(out) + "\n"


def compile_tex(tex: str, name: str, passes: int = 2) -> pathlib.Path:
    BUILD.mkdir(exist_ok=True)
    src = BUILD / f"{name}.tex"
    src.write_text(tex, encoding="utf-8")
    for _ in range(passes):
        r = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", src.name],
            cwd=BUILD, capture_output=True, text=True)
        if r.returncode != 0:
            log = (BUILD / f"{name}.log").read_text(errors="replace")
            i = log.find("\n!")
            snippet = log[i:i + 1500] if i >= 0 else r.stdout[-2500:]
            raise RuntimeError(f"pdflatex failed for {name}:\n{snippet}")
    return BUILD / f"{name}.pdf"


def preamble() -> str:
    return (HERE / "tex" / "preamble.tex").read_text(encoding="utf-8")


def standalone(body: str) -> str:
    return preamble() + "\n\\begin{document}\n" + body + "\n\\end{document}\n"
