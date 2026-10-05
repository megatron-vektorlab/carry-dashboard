"""Assemble the interior PDF.

    .venv/bin/python -m lp.book            # build build/book/interior.pdf

Reads data/puzzles/*.json, data/writing/*.json, data/lessons/*.json and the
prose in content/*.md.  Grid sizes are fitted automatically: after each
compile the page labels are checked, and any puzzle that spilled onto an
extra page gets a smaller grid and the book is compiled again.
"""
from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import sys

from . import config
from .grid import esc
from .layout import answer_table, grid_tikz, liar_table, lineup_strip, stars_tikz
from .measure import width
from .plan import CHAPTERS, slots
from .text import Bound

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build", "book")
CONTENT = os.path.join(ROOT, "content")
TEXT_W = 7.15                       # text block width (in)
TEXT_H = 9.45                       # usable height above the footer (in)
LINE = 0.285                        # one 16 pt line (in)
SPREAD_FAMILIES = {"grid4", "days4", "num43", "num44", "case54", "suppose"}


# ---------------------------------------------------------------- tiny markup
def inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\\textit{\1}", s)
    s = s.replace("\u2014", "---").replace("\u2013", "--")
    s = re.sub(r'(^|[\s(\[])"', r"\1``", s)
    s = s.replace('"', "''")
    s = s.replace("[O]", r"\omark{}").replace("[X]", r"\xmark{}").replace("[ ]", r"\cluebox{}")
    s = s.replace("[LINE]", r"\rule{3in}{0.6pt}")
    return s


def md(text: str, figures=None) -> str:
    """Paragraphs, ## headings, - bullets, 1. lists, > Ada boxes, [[figure]] lines."""
    out, para, lst = [], [], None

    def flush():
        nonlocal para, lst
        if para:
            out.append(inline(" ".join(para)) + "\n")
            para = []
        if lst:
            env = "itemize" if lst[0] == "-" else "enumerate"
            out.append(rf"\begin{{{env}}}[itemsep=2pt, topsep=2pt, leftmargin=0.35in]" + "\n" +
                       "\n".join(r"\item " + inline(x) for x in lst[1]) + rf"\end{{{env}}}" + "\n")
            lst = None

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush()
            continue
        if line.startswith("## "):
            flush()
            out.append(r"\needspace{5\baselineskip}\subsection*{" + inline(line[3:]) + "}\n")
        elif line.startswith("[[") and line.endswith("]]"):
            flush()
            key = line[2:-2].strip()
            out.append((figures or {}).get(key, f"% missing figure {key}") + "\n")
        elif line.startswith("> "):
            flush()
            out.append(r"\adabox{" + inline(line[2:]) + "}\n")
        elif re.match(r"^- ", line):
            if para:
                out.append(inline(" ".join(para)) + "\n")
                para = []
            if not lst or lst[0] != "-":
                flush()
                lst = ("-", [])
            lst[1].append(line[2:])
        elif re.match(r"^\d+\. ", line):
            if para:
                out.append(inline(" ".join(para)) + "\n")
                para = []
            if not lst or lst[0] != "1":
                flush()
                lst = ("1", [])
            lst[1].append(re.sub(r"^\d+\. ", "", line))
        else:
            if lst:
                flush()
            para.append(line.strip())
    flush()
    return "\n".join(out)


def read_content(name):
    p = os.path.join(CONTENT, name)
    return open(p).read() if os.path.exists(p) else ""


def sections(text):
    """Split '# Heading' sections of a content file."""
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith("# "):
            if cur:
                out[cur] = "\n".join(buf).strip()
            cur, buf = line[2:].strip(), []
        else:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf).strip()
    return out


# ---------------------------------------------------------------- data
def load_all():
    P, W = {}, {}
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "puzzles", "*.json"))):
        d = json.load(open(p))
        P[d["no"]] = d
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "writing", "*.json"))):
        d = json.load(open(p))
        W[d["no"]] = d
    return P, W


def est_lines(text, w=TEXT_W, indent=0.0):
    """Rough number of 16 pt lines a paragraph takes."""
    words = text.split()
    lines, cur = 1, 0.0
    avail = w - indent
    sp = width(" ")
    for wd in words:
        ww = width(wd)
        if cur and cur + sp + ww > avail:
            lines += 1
            cur = ww
        else:
            cur = cur + (sp if cur else 0) + ww
    return lines


TRACKER = (r"Solved \cluebox\hspace{0.22in}Hints used \ringbox\,\ringbox\,\ringbox"
           r"\hspace{0.22in}Time \rule{0.75in}{0.6pt}")


def foot(no, stars):
    hints = [rf"\pageref{{h1:{no}}}", rf"\pageref{{h2:{no}}}", rf"\pageref{{h3:{no}}}"]
    if stars >= 4:
        hints.append(rf"\pageref{{h4:{no}}}")
    return (rf"\setpuzzlefoot{{Hints: pages {', '.join(hints)}\quad$\cdot$\quad "
            rf"Solution: page \pageref{{sol:{no}}}}}")


def head(no, title, stars):
    return rf"\puzzlehead{{{no}}}{{{esc(title)}}}{{{stars_tikz(stars)}}}{{{TRACKER}}}"


def clue_list(texts):
    return r"\begin{clues}" + "\n".join(r"\item " + inline(t) for t in texts) + r"\end{clues}"


def question_line(P):
    q = P.get("question")
    if not q or not q.get("text"):
        return ""
    return r"\par\vspace{4pt}\noindent\textbf{Your question:} " + inline(q["text"]) + r"\par"


def top_block(P, W):
    texts = (W or {}).get("clues") or P["texts"]
    story = (W or {}).get("story") or P["story"]
    return "\n".join([head(P["no"], P["title"], P["stars"]), inline(story) + r"\par", clue_list(texts), question_line(P)])


def tip_block(P, W):
    tip = (W or {}).get("tip") if P["chapter"] <= 3 else None
    return (r"\tipbox{" + inline(tip) + "}") if tip else ""


def table_block(B):
    return r"\begin{center}\textbf{Your answers}\par\vspace{4pt}" + answer_table(B) + r"\end{center}"


STRIP_H = 1.15          # "The line, front to back" + boxes
MEASURED = {}           # no -> {"top": in, "tip": in, "table": in}; filled by measure()
PT = 1 / 72.27


def measure(P, W):
    """Typeset every puzzle's text block once and record its real height."""
    out = [preamble(), r"\begin{document}", r"\typeout{TH:\the\textheight}"]
    for no in sorted(P):
        p = P[no]
        if p["kind"] != "grid":
            continue
        B = Bound.restore(p["state"])
        for key, tex in (("top", top_block(p, W.get(no))), ("tip", tip_block(p, W.get(no))),
                         ("table", table_block(B))):
            if not tex:
                continue
            out.append(r"\setbox0=\vbox{\hsize=\textwidth\linewidth=\textwidth " + tex + "}")
            out.append(rf"\typeout{{M:{no}:{key}:\the\ht0:\the\dp0}}")
    out.append(r"\end{document}")
    d = os.path.join(BUILD, "measure")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "measure.tex"), "w") as f:
        f.write("\n".join(out))
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "measure.tex"], cwd=d, capture_output=True, text=True)
    log = open(os.path.join(d, "measure.log"), errors="replace").read()
    global TEXT_H
    m = re.search(r"TH:([\d.]+)pt", log)
    if m:
        TEXT_H = float(m.group(1)) * PT
    MEASURED.clear()
    for no, key, ht, dp in re.findall(r"M:(\d+):(\w+):([\d.]+)pt:([\d.]+)pt", log):
        MEASURED.setdefault(int(no), {})[key] = (float(ht) + float(dp)) * PT


def grid_puzzle(P, W, shrink=0.0):
    no, stars = P["no"], P["stars"]
    B = Bound.restore(P["state"])
    spread = P["family"] in SPREAD_FAMILIES
    M = MEASURED.get(no, {})
    top = M.get("top", 4.0)
    parts = [rf"\puzzlestart{{{no}}}", foot(no, stars), top_block(P, W)]
    if not spread:
        tip = tip_block(P, W)
        tip_h = M.get("tip", 0.0) + 0.25 if tip else 0.0
        strip_h = STRIP_H if P.get("lineup") else 0.0
        max_cell = 0.8 if B.k == 2 else 0.62
        good = 0.5 if B.k == 2 else 0.42

        def fit(tip_h, strip_h):
            return grid_tikz(B, max_w=TEXT_W, max_h=TEXT_H - top - tip_h - strip_h - 0.6 - shrink,
                             max_cell=max_cell)
        g, geo = fit(tip_h, strip_h)
        if geo["cell"] < good and tip:
            tip, tip_h = "", 0.0
            g, geo = fit(tip_h, strip_h)
        if geo["cell"] < good and strip_h:
            strip_h = 0.0
            g, geo = fit(tip_h, strip_h)
        parts += [r"\vfill\begin{center}", g, r"\end{center}"]
        if strip_h:
            parts += [r"\begin{center}\textbf{The line, front to back}\par\vspace{3pt}",
                      lineup_strip(B, B.ordered[0]), r"\end{center}"]
        if tip:
            parts += [r"\vfill" + tip]
        parts += [r"\vfill", rf"\label{{puzend:{no}}}", r"\clearpage"]
        return "\n".join(parts), 1
    table = table_block(B)
    table_h = M.get("table", (B.n + 1) * 0.37 + 0.6) + 0.2
    if top > TEXT_H - 0.25:
        # the clues run over onto the right-hand page; the grid follows them there
        over = top - TEXT_H + 0.75
        g, geo = grid_tikz(B, max_w=TEXT_W, max_h=TEXT_H - over - 0.6 - shrink, max_cell=0.58)
        parts += [r"\par\vfill\begin{center}", g, r"\end{center}\vfill", rf"\label{{puzend:{no}}}", r"\clearpage"]
        return "\n".join(parts), 2
    tip = tip_block(P, W)
    tip_h = M.get("tip", 0.0) + 0.25 if tip else 0.0
    where = "left" if top + table_h <= TEXT_H - 0.3 else "right"
    if tip and top + tip_h + (table_h if where == "left" else 0) > TEXT_H - 0.3:
        tip = ""
    if tip:
        parts += [r"\vfill" + tip]
    if where == "left":
        parts += [r"\vfill", table]
    parts += [r"\vfill\clearpage"]
    big = 0.7 if (B.n, B.k) == (4, 3) else 0.58
    if where == "right":
        table = (r"\begin{center}\textbf{Your answers}\par\vspace{4pt}" + answer_table(B, stretch=1.2)
                 + r"\end{center}")
        table_h = table_h * 0.85
    max_h = TEXT_H - 0.45 - shrink - (table_h if where == "right" else 0)
    g, geo = grid_tikz(B, max_w=TEXT_W, max_h=max_h, max_cell=big)
    if where == "right" and geo["cell"] < 0.33:
        where, table = "none", ""
        g, geo = grid_tikz(B, max_w=TEXT_W, max_h=TEXT_H - 0.45 - shrink, max_cell=big)
    parts += [r"\vspace*{\fill}\begin{center}", g, r"\end{center}\vspace*{\fill}"]
    if where == "right":
        parts += [table, r"\vspace*{\fill}"]
    parts += [rf"\label{{puzend:{no}}}", r"\clearpage"]
    return "\n".join(parts), 2


def liar_puzzle(P, W, shrink=0.0):
    no, stars = P["no"], P["stars"]
    story = (W or {}).get("story") or P["story"]
    lines = [r"\begingroup\setlength{\parskip}{3pt}"] + [rf"\saying{{{esc(nm)}}}{{{inline(t)}}}"
                                                          for nm, t in zip(P["names"], P["texts"])] + [r"\endgroup"]
    parts = [rf"\puzzlestart{{{no}}}", foot(no, stars), head(no, P["title"], stars), inline(story) + r"\par",
             r"\vspace{2pt}", "\n".join(lines),
             r"\rulebox{" + inline(P["rule_text"]) + "}",
             r"\vfill\begin{center}\textbf{Test each suspect. Write T (true) or F (false) for each statement.}\par\vspace{6pt}",
             liar_table(P["names"]), r"\end{center}\vfill", rf"\label{{puzend:{no}}}", r"\clearpage"]
    return "\n".join(parts), 1


# ---------------------------------------------------------------- hints and solutions
HINT_TITLES = [
    ("Hints, Step 1: Where to Look", "A gentle nudge toward the right clue or row. Try this first."),
    ("Hints, Step 2: What to Notice", "What that clue or row is really telling you."),
    ("Hints, Step 3: The Key Step", "The turning point of the puzzle, spelled out. After this, the rest should flow."),
    ("Stuck Halfway?", "For the four- and five-star puzzles: a push through the middle of the solve."),
]


def hints_tex(P, W):
    out = []
    for h, (title, blurb) in enumerate(HINT_TITLES):
        out.append(r"\hintsection{" + esc(title) + "}{" + esc(blurb) + "}" + (r"\label{hints}" if h == 0 else ""))
        for no in sorted(P):
            hs = (W.get(no) or {}).get("hints", [])
            if h < len(hs):
                out.append(rf"\hintentry{{{no}}}{{{inline(hs[h])}}}{{h{h + 1}:{no}}}")
    return "\n".join(out)


def compact_answer(p):
    """Answer rows 'Name: v1, v2, v3', two per line when they fit."""
    if p["kind"] != "grid":
        return r"\begin{center}" + liar_solution_table(p) + r"\end{center}"
    B = Bound.restore(p["state"])
    rows = []
    for e in range(B.n):
        vals = [B.cats[c]["values"][p["solution"][c][e]] for c in range(1, B.k)]
        rows.append((B.cats[0]["values"][e], ", ".join(vals)))
    wmax = max(width(f"{a}: {b}", 16, "sf") + 0.25 for a, b in rows)
    cols = 2 if wmax <= (TEXT_W - 0.6) / 2 else 1
    cells = [rf"\textbf{{{esc(a)}:}} {esc(b)}" for a, b in rows]
    if cols == 1:
        body = r"\\".join(cells)
        return r"\answerbox{" + body + "}"
    lines = []
    for i in range(0, len(cells), 2):
        pair = cells[i:i + 2]
        lines.append(r"\makebox[%.2fin][l]{%s}" % ((TEXT_W - 0.6) / 2, pair[0]) + (pair[1] if len(pair) > 1 else ""))
    return r"\answerbox{" + r"\\".join(lines) + "}"


def solution_tex(P, W):
    out = [r"\solutionsstart"]
    for no in sorted(P):
        p, w = P[no], W.get(no) or {}
        sol = w.get("solution", {})
        out.append(rf"\solhead{{{no}}}{{{esc(p['title'])}}}{{sol:{no}}}")
        out.append(compact_answer(p))
        lead = ""
        if p.get("question") and p.get("answer"):
            line = w.get("answer_line") or f"{p['answer']}."
            lead = r"\textbf{Answer: " + inline(line) + r"}\enspace "
        para = lead
        if sol.get("key_idea"):
            para += r"\textbf{Key idea:} " + inline(sol["key_idea"])
        out.append(r"\noindent " + para + r"\par")
        if sol.get("steps"):
            out.append(r"\noindent " + " ".join(inline(x) for x in sol["steps"]) + r"\par")
        if sol.get("epilogue"):
            out.append(r"\noindent\textit{" + inline(sol["epilogue"]) + r"}\par")
        out.append(r"\solsep")
    bonus = read_content("bonus_solution.md")
    if bonus:
        out.append(r"\solhead{}{Putting It All Together}{sol:bonus}")
        out.append(md(bonus))
    return "\n".join(out)


def liar_solution_table(p):
    names = p["names"]
    cols = "|l|" + "c|" * len(names) + "c|c|"
    rows = [r"\begingroup\renewcommand{\arraystretch}{1.35}\begin{tabular}{" + cols + r"}\hline",
            r"\bfseries Suspect tested & " + " & ".join(r"\bfseries " + esc(n[:1]) + "." for n in names) +
            r" & \bfseries True & \bfseries Fits? \\ \hline"]
    for c in p["cases"]:
        rows.append(f"If {esc(c['case'])} did it & " + " & ".join("T" if t == "true" else "F" for t in c["truth"]) +
                    f" & {c['count']} & " + (r"\textbf{yes}" if c["fits"] else "no") + r" \\ \hline")
    rows.append(r"\end{tabular}\endgroup")
    return "\n".join(rows)


# ---------------------------------------------------------------- assembly
def preamble():
    pre = open(os.path.join(ROOT, "tex", "preamble.tex")).read()
    return pre.replace("AUTHOR", config.AUTHOR)


def build_tex(P, W, shrink=None, extra=None):
    shrink = shrink or {}
    body = [r"\begin{document}", r"\frontmatter", r"\pagestyle{plain.scrheadings}"]
    body.append(read_tex("front.tex"))
    body.append(r"\mainmatter")
    ch_slots = {}
    for s in slots():
        ch_slots.setdefault(s["chapter"], []).append(s["no"])
    chapter_text = sections(read_content("chapters.md"))
    lessons = load_lessons()
    for ch, title, skill, groups in CHAPTERS:
        nos = ch_slots[ch]
        stars = sorted({g[2] for g in groups})
        intro = chapter_text.get(f"Chapter {ch}", "")
        from .frontback import lighthouse
        body.append(rf"\chapteropener{{{ch}}}{{{esc(title)}}}{{{esc(skill)}}}{{{stars_tikz(max(stars))}}}"
                    rf"{{Puzzles {nos[0]}--{nos[-1]}}}{{{md(intro)}" + r"\vfill\begin{center}" + lighthouse(0.9)
                    + r"\end{center}\vfill}")
        if ch in lessons:
            body.append(lessons[ch])
        for no in nos:
            if no not in P:
                continue
            p = P[no]
            if p["kind"] == "liars":
                t, pages = liar_puzzle(p, W.get(no), shrink.get(no, 0))
            else:
                t, pages = grid_puzzle(p, W.get(no), shrink.get(no, 0))
            if pages == 2:
                body.append(r"\startspread")
            body.append(t)
        if ch == 7:
            body.append(read_tex("bonus.tex"))
    body.append(r"\backmatter")
    body.append(r"\startodd" + "\n" + r"\begingroup\setlength{\parskip}{3pt plus 1pt}" + hints_tex(P, W))
    body.append(r"\startodd" + "\n" + solution_tex(P, W) + r"\endgroup")
    body.append(read_tex("back.tex"))
    body.append(r"\end{document}")
    return preamble() + "\n".join(body)


def read_tex(name):
    p = os.path.join(BUILD, "parts", name)
    return open(p).read() if os.path.exists(p) else f"% {name} not generated yet\n"


def load_lessons():
    out = {}
    for p in sorted(glob.glob(os.path.join(BUILD, "parts", "lesson*.tex"))):
        ch = int(re.findall(r"lesson(\d+)", p)[0])
        out[ch] = open(p).read()
    return out


def compile_tex(src, runs=2):
    os.makedirs(BUILD, exist_ok=True)
    path = os.path.join(BUILD, "interior.tex")
    with open(path, "w") as f:
        f.write(src)
    for _ in range(runs):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "interior.tex"], cwd=BUILD,
                           capture_output=True, text=True)
        if r.returncode:
            sys.stdout.write(r.stdout[-3000:])
            raise SystemExit("pdflatex failed")
    return path


def page_labels():
    labs = {}
    aux = os.path.join(BUILD, "interior.aux")
    for line in open(aux, errors="replace"):
        m = re.match(r"\\newlabel\{([^}]*)\}\{\{[^}]*\}\{([^}]*)\}", line)
        if m:
            labs[m.group(1)] = m.group(2)
    return labs


def main():
    from .frontback import write_parts
    P, W = load_all()
    write_parts(P, W)
    measure(P, W)
    shrink = {}
    for rnd in range(6):
        compile_tex(build_tex(P, W, shrink), runs=2 if rnd else 3)
        labs = page_labels()
        bad = []
        for no, p in P.items():
            a, b = labs.get(f"puz:{no}"), labs.get(f"puzend:{no}")
            if a is None or b is None or not a.isdigit() or not b.isdigit():
                continue
            pages = 2 if p.get("family") in SPREAD_FAMILIES else 1
            if int(b) - int(a) + 1 != pages:
                bad.append(no)
        if not bad:
            break
        for no in bad:
            shrink[no] = shrink.get(no, 0) + 0.2
        print(f"round {rnd}: shrinking grids of {bad}")
    compile_tex(build_tex(P, W, shrink), runs=2)
    print("built", os.path.join(BUILD, "interior.pdf"))


if __name__ == "__main__":
    main()
