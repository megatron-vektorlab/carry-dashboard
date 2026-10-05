"""Front matter, lessons, the finale bonus page and back matter as TeX parts.

Prose comes from content/*.md (see book.md for the tiny markup).  Lesson
figures are written in the text as directives:

    [[grid L2 | O: Rosa=fig, fig=tin | X: Felix=crock | new: Rosa=tin | caption: After clues 1 and 2]]
    [[grid L1 | ... || ... ]]        two grids side by side
    [[clues L2]]                     the example's clue list
    [[answer L2]]                    the solved answer table
    [[liar L4]] / [[liar L4 filled]] the example's statements and (filled) truth table
"""
from __future__ import annotations

import json
import os
import re

from . import config
from .book import BUILD, CONTENT, inline, md, read_content, sections
from .engine import Contradiction, Deducer
from .grid import esc
from .layout import answer_table, grid_tikz, liar_table, lineup_strip, stars_tikz
from .plan import CHAPTERS, slots
from .text import Bound

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSON_TITLES = {1: "Your First Grid", 2: "The Staircase Grid", 3: "Lining Up", 4: "Truth or Fib?",
                 5: "Clues That Team Up", 6: "One Careful Suppose"}


def load_lesson(name):
    p = os.path.join(ROOT, "data", "lessons", f"{name}.json")
    return json.load(open(p)) if os.path.exists(p) else None


def find_item(B, text):
    text = text.strip().lower()
    hits = [(c, v) for c in range(B.k) for v, val in enumerate(B.cats[c]["values"]) if str(val).lower() == text]
    if len(hits) != 1:
        raise ValueError(f"lesson figure: '{text}' matches {hits}")
    return hits[0]


def figure_marks(B, spec):
    """Parse 'O: a=b, c=d | X: e=f | new: g=h' into marks and highlight sets."""
    d = Deducer(B.n, B.k, [], B.ordered)
    newO, newX = [], []
    hl, caption = set(), ""
    for part in spec.split("|"):
        part = part.strip()
        if not part or ":" not in part:
            continue
        key, val = part.split(":", 1)
        key = key.strip().lower()
        if key == "caption":
            caption = val.strip()
            continue
        for pair in filter(None, (x.strip() for x in val.split(","))):
            a, b = (find_item(B, x) for x in pair.split("="))
            if key == "o":
                d._set(a, b, True, newO, newX)
            elif key == "x":
                d._set(a, b, False, newO, newX)
            elif key == "new":
                hl.add((a, b))
    marks = {}
    for (a, b), v in d.rel.items():
        if a[0] < b[0] and v is not None:
            marks[(a, b)] = "O" if v else "X"
    return marks, hl, caption


def lesson_figures(text):
    figs = {}
    for m in re.finditer(r"\[\[(.+?)\]\]", text):
        key = m.group(1).strip()
        words = key.split()
        kind, name = words[0], words[1]
        L = load_lesson(name)
        if L is None:
            figs[key] = f"% no data for {name}"
            continue
        if kind == "liar":
            figs[key] = liar_figure(L, filled="filled" in words)
            continue
        B = Bound.restore(L["state"])
        if kind == "clues":
            figs[key] = (r"\begin{clues}" + "\n".join(r"\item " + inline(t) for t in L["clues"]) + r"\end{clues}")
        elif kind == "answer":
            figs[key] = r"\begin{center}" + answer_table(B, filled=L["solution"]) + r"\end{center}"
        elif kind == "grid":
            rest = key.split(None, 2)[2] if len(key.split(None, 2)) > 2 else ""
            panels = [p for p in rest.split("||")]
            cells = []
            w = 7.0 / len(panels) - 0.15
            for p in panels:
                marks, hl, cap = figure_marks(B, p)
                g, _ = grid_tikz(B, max_w=w, max_h=4.2, marks=marks, highlight=hl, max_cell=0.48)
                cells.append(r"\begin{minipage}[t]{%.2fin}\centering " % w + g +
                             (r"\par\vspace{3pt}\textit{" + inline(cap) + "}" if cap else "") + r"\end{minipage}")
            figs[key] = r"\par\begin{center}" + r"\hfill".join(cells) + r"\end{center}\par"
    return figs


def liar_figure(L, filled=False):
    out = [r"\par"]
    for nm, t in zip(L["names"], L["texts"]):
        out.append(rf"\saying{{{esc(nm)}}}{{{inline(t)}}}")
    out.append(r"\rulebox{" + inline(L["rule_text"]) + "}")
    if filled:
        names = L["names"]
        cols = "|l|" + "c|" * len(names) + "c|c|"
        rows = [r"\begin{center}\begingroup\renewcommand{\arraystretch}{1.35}\begin{tabular}{" + cols + r"}\hline",
                r"\bfseries Suspect tested & " + " & ".join(r"\bfseries " + esc(n) for n in names) +
                r" & \bfseries True & \bfseries Fits? \\ \hline"]
        for c in L["cases"]:
            rows.append(f"If {esc(c['case'])} did it & " + " & ".join("T" if t else "F" for t in c["truth"]) +
                        f" & {sum(c['truth'])} & " + (r"\textbf{yes}" if c["fits"] else "no") + r" \\ \hline")
        rows.append(r"\end{tabular}\endgroup\end{center}")
        out.append("\n".join(rows))
    return "\n".join(out)


# ---------------------------------------------------------------- front matter
def lighthouse(scale=1.0):
    return (r"\begin{tikzpicture}[x=%.2fin,y=%.2fin,line width=1.4pt,line join=round]" % (scale, scale) +
            r"\draw (-0.32,0) -- (-0.22,1.55) -- (0.22,1.55) -- (0.32,0) -- cycle;"
            r"\fill[black!100] (-0.29,0.42) -- (0.29,0.42) -- (0.28,0.62) -- (-0.28,0.62) -- cycle;"
            r"\fill (-0.255,0.95) -- (0.255,0.95) -- (0.245,1.12) -- (-0.245,1.12) -- cycle;"
            r"\draw (-0.3,1.55) -- (0.3,1.55);"
            r"\draw (-0.17,1.55) rectangle (0.17,1.85);"
            r"\draw (-0.22,1.85) -- (0,2.05) -- (0.22,1.85);"
            r"\draw[line width=1pt] (0.25,1.72) -- (0.9,1.9) (0.25,1.68) -- (0.9,1.5) (-0.25,1.72) -- (-0.9,1.9) "
            r"(-0.25,1.68) -- (-0.9,1.5);"
            r"\draw (-0.9,0) .. controls (-0.5,0.08) and (0.5,-0.08) .. (0.9,0);"
            r"\end{tikzpicture}")


def title_page():
    return (r"\thispagestyle{empty}\setpuzzlefoot{}\vspace*{0.3in}\begin{center}"
            r"{\display\fontsize{18}{22}\selectfont " + esc(config.SERIES.upper()) + r"\enspace\textperiodcentered\enspace BOOK "
            + str(config.SERIES_NO) + r"\par}\vspace{0.35in}"
            r"{\display\fontsize{46}{52}\selectfont Cozy Mystery\\[2pt] Logic Puzzles\\[2pt] for Beginners\par}"
            r"\vspace{0.3in}" + lighthouse(1.15) + r"\par\vspace{0.3in}"
            r"\begin{minipage}{5.6in}\centering\fontsize{17}{22}\selectfont 100 Large Print Whodunit Grid Puzzles from Easy "
            r"to Expert, with Step-by-Step Lessons, 3~Hints per Puzzle, and Every Solution Explained\end{minipage}\par"
            r"\vfill{\display\fontsize{24}{28}\selectfont " + esc(config.AUTHOR) + r"\par}\vspace{0.2in}\end{center}"
            r"\clearpage")


def copyright_page():
    return (r"\thispagestyle{empty}\vspace*{\fill}\begingroup\setlength{\parskip}{8pt}"
            + f"\\textit{{{esc(config.TITLE)}}}\\par\n"
            + f"{esc(config.SERIES)}, Book {config.SERIES_NO}\\par\n"
            + f"Copyright \\textcopyright\\ {config.YEAR} {esc(config.AUTHOR)}. All rights reserved.\\par\n"
            + r"No part of this book may be reproduced without written permission, except that the blank grids "
              r"and the Scratch Pad pages may be copied for your own personal use.\par "
              r"This is a work of fiction. Thimble Harbor and everyone in it are invented; any resemblance to real "
              r"people or places is coincidence.\par "
              r"Every puzzle in this book was checked by computer to have exactly one solution, and every solution "
              r"was checked step by step against the clues.\par "
              r"First edition.\par\endgroup\clearpage")


def contents():
    rows = []
    rows.append(("A Letter from Ada", r"\pageref{front:letter}"))
    rows.append(("How This Book Works", r"\pageref{front:howto}"))
    rows.append(("Welcome to Thimble Harbor", r"\pageref{front:town}"))
    for ch, title, skill, groups in CHAPTERS:
        rows.append((rf"\textbf{{Chapter {ch}: {esc(title)}}}", rf"\pageref{{ch:{ch}}}"))
        if ch in LESSON_TITLES:
            rows.append((rf"\hspace{{0.3in}}Lesson {ch}: {esc(LESSON_TITLES[ch])}", rf"\pageref{{lesson:{ch}}}"))
    rows.append((r"\hspace{0.3in}Putting It All Together", r"\pageref{bonus}"))
    rows.append((r"\textbf{Hints}", r"\pageref{hints}"))
    rows.append((r"\textbf{Solutions}", r"\pageref{solutions}"))
    rows.append(("Puzzle Index and Tracker", r"\pageref{back:tracker}"))
    rows.append(("Clue Language at a Glance", r"\pageref{back:glossary}"))
    rows.append(("Common Mistakes and Quick Repairs", r"\pageref{back:mistakes}"))
    rows.append(("Make Your Own Puzzle", r"\pageref{back:make}"))
    rows.append(("Blank Grids", r"\pageref{back:grids}"))
    rows.append(("Your Certificate", r"\pageref{back:cert}"))
    out = [r"\setpuzzlefoot{}{\display\fontsize{40}{44}\selectfont Contents\par}\vspace{10pt}",
           r"\begingroup\setlength{\parskip}{3pt}"]
    for a, b in rows:
        out.append(rf"\noindent {a}\dotfill {b}\par")
    out.append(r"\endgroup\clearpage")
    return "\n".join(out)


def prose_page(title, label, body, figs=None):
    return (r"\clearpage\setpuzzlefoot{}{\display\fontsize{34}{38}\selectfont " + esc(title) + r"\par}"
            + rf"\label{{{label}}}\vspace{{2pt}}\noindent\rule{{\linewidth}}{{1.2pt}}\par" + "\n" + md(body, figs) + "\n")


def front(P, W):
    F = sections(read_content("front.md"))
    out = [title_page(), copyright_page(), contents()]
    out.append(prose_page("A Letter from Ada", "front:letter", F.get("Letter", "")))
    out.append(prose_page("How This Book Works", "front:howto", F.get("How This Book Works", "")))
    out.append(prose_page("Welcome to Thimble Harbor", "front:town", F.get("Welcome to Thimble Harbor", "")))
    out.append(town_map())
    return "\n".join(out)


def lessons():
    text = sections(read_content("lessons.md"))
    out = {}
    for no, title in LESSON_TITLES.items():
        body = text.get(f"Lesson {no}", "")
        figs = lesson_figures(body)
        out[no] = (rf"\lessonhead{{{no}}}{{{esc(title)}}}\label{{lesson:{no}}}" + "\n" + md(body, figs) + "\n")
    return out


def bonus():
    text = read_content("bonus.md")
    return (r"\clearpage\setpuzzlefoot{}{\display\fontsize{34}{38}\selectfont Putting It All Together\par}"
            r"\label{bonus}\vspace{2pt}\noindent\rule{\linewidth}{1.2pt}\par" + "\n" + md(text) + r"\clearpage")


# ---------------------------------------------------------------- back matter
def tracker(P):
    out = [r"\clearpage\setpuzzlefoot{}{\display\fontsize{34}{38}\selectfont Puzzle Index and Tracker\par}"
           r"\label{back:tracker}\vspace{2pt}Tick each puzzle as you solve it, and fill in a ring for every hint you used."
           r"\par\vspace{4pt}"]
    rows = []
    for no in sorted(P):
        p = P[no]
        rows.append(rf"{no} & {esc(p['title'])} & \pageref{{puz:{no}}} & {stars_tikz(p['stars'], size=0.13)} & "
                    r"\cluebox & \ringbox\,\ringbox\,\ringbox \\")
    head = (r"\textbf{No.} & \textbf{Puzzle} & \textbf{Page} & \textbf{Stars} & \textbf{Done} & \textbf{Hints} \\"
            r"\hline\endhead")
    out.append(r"\begingroup\renewcommand{\arraystretch}{1.18}\setlength{\tabcolsep}{4pt}"
               r"\begin{longtable}{r p{3.05in} r c c c}" + head + "\n" + "\n".join(rows) +
               r"\end{longtable}\endgroup")
    return "\n".join(out)


def blank_grids():
    from .text import Bound as _B
    out = [r"\clearpage\setpuzzlefoot{}{\display\fontsize{34}{38}\selectfont Blank Grids\par}\label{back:grids}"
           r"\vspace{2pt}For making your own puzzles or re-solving a favorite. You may copy these pages for your own use."
           r"\par\vspace{6pt}"]
    for n, k in ((3, 3), (4, 3), (4, 4), (5, 4)):
        cats = [{"label": "Names", "kind": "name", "values": [" "] * n}]
        for j in range(1, k):
            cats.append({"label": f"Category {j}", "values": [" "] * n})
        B = _B.restore({"theme": {"entity": ["person", "people"]}, "cats": cats})
        g, _ = grid_tikz(B, max_w=6.6, max_h=7.6 if n >= 4 else 4.5, max_cell=0.5)
        out.append(r"\begin{center}" + g.replace(r"\strut  ", r"\rule{1.1in}{0.6pt}") + r"\end{center}")
        out.append(r"\clearpage" if (n, k) != (3, 3) else r"\vspace{0.2in}")
    return "\n".join(out)


def certificate():
    return (r"\clearpage\thispagestyle{empty}\setpuzzlefoot{}\label{back:cert}\vspace*{0.4in}\begin{center}"
            r"\begin{tikzpicture}\draw[line width=3pt, rounded corners=10pt] (0,0) rectangle (6.8in,8.4in);"
            r"\draw[line width=1pt, rounded corners=7pt] (0.15in,0.15in) rectangle (6.65in,8.25in);"
            r"\node[text width=5.8in, align=center] at (3.4in,4.2in) {"
            + lighthouse(0.8) + r"\\[14pt]{\display\fontsize{20}{24}\selectfont THE THIMBLE HARBOR GAZETTE}\\[18pt]"
            r"{\display\fontsize{40}{46}\selectfont Honorary Detective}\\[18pt]"
            r"This certifies that\\[26pt]\rule{4.5in}{0.8pt}\\[18pt]"
            r"has solved all one hundred cases of\\ \textit{" + esc(config.TITLE) + r"}\\[10pt]"
            r"and is hereby welcome at the puzzle desk any time.\\[36pt]"
            r"\rule{2.2in}{0.8pt}\hspace{0.5in}\rule{2.2in}{0.8pt}\\[2pt]"
            r"Ada Quill, Puzzle Editor (retired)\hspace{0.6in}Date};"
            r"\end{tikzpicture}\end{center}\clearpage")


def back(P, W):
    B = sections(read_content("back.md"))
    out = [tracker(P)]
    out.append(prose_page("Clue Language at a Glance", "back:glossary", B.get("Clue Language at a Glance", "")))
    out.append(prose_page("Common Mistakes and Quick Repairs", "back:mistakes",
                          B.get("Common Mistakes and Quick Repairs", "")))
    out.append(prose_page("Make Your Own Puzzle", "back:make", B.get("Make Your Own Puzzle", "")))
    out.append(blank_grids())
    out.append(certificate())
    out.append(prose_page("Until Next Time", "back:next", B.get("Until Next Time", "")))
    return "\n".join(out)


def write_parts(P, W):
    d = os.path.join(BUILD, "parts")
    os.makedirs(d, exist_ok=True)
    for name in os.listdir(d):
        os.remove(os.path.join(d, name))
    open(os.path.join(d, "front.tex"), "w").write(front(P, W))
    for no, t in lessons().items():
        open(os.path.join(d, f"lesson{no}.tex"), "w").write(t)
    open(os.path.join(d, "bonus.tex"), "w").write(bonus())
    open(os.path.join(d, "back.tex"), "w").write(back(P, W))


def town_map():
    """A simple schematic map of Thimble Harbor (16 pt labels)."""
    coast = ("(3.55,8.0) .. controls (3.35,7.4) and (3.7,6.9) .. (3.5,6.3) .. controls (3.35,5.7) and (3.7,5.2) .. "
             "(3.55,4.7) .. controls (3.45,4.3) and (3.3,3.8) .. (3.5,3.2) .. controls (3.7,2.5) and (3.2,1.8) .. "
             "(3.45,1.1) .. controls (3.6,0.6) and (3.4,0.3) .. (3.5,0)")
    point = ("(3.53,4.55) .. controls (4.4,4.5) and (5.4,3.9) .. (6.05,3.45) -- (6.35,3.25) -- (6.5,3.4) -- "
             "(6.25,3.65) .. controls (5.5,4.3) and (4.5,4.85) .. (3.56,4.95)")
    return r"""
\clearpage\setpuzzlefoot{}{\display\fontsize{34}{38}\selectfont Map of Thimble Harbor\par}\vspace{2pt}
\noindent\rule{\linewidth}{1.2pt}\par\vspace{8pt}
\begin{center}\begin{tikzpicture}[x=1in,y=0.98in, lbl/.style={font=\normalsize, align=center, inner sep=2pt},
  place/.style={draw, line width=1.2pt, fill=white, minimum size=0.17in, inner sep=0pt}]
  \fill[black!12] """ + coast + r""" -- (7.1,0) -- (7.1,8.0) -- cycle;
  \draw[line width=1.6pt] """ + coast + r""";
  \fill[white] """ + point + r""" -- cycle;
  \draw[line width=1.6pt] """ + point + r""";
  % lighthouse on the point
  \begin{scope}[shift={(6.38,3.38)}, scale=0.34]
    \fill (-0.3,0) -- (-0.2,1.3) -- (0.2,1.3) -- (0.3,0) -- cycle; \fill (-0.15,1.3) rectangle (0.15,1.6);
    \fill (-0.2,1.6) -- (0,1.8) -- (0.2,1.6) -- cycle;
  \end{scope}
  \node[lbl, anchor=north] at (6.15,3.15) {Thimble Point Light};
  \node[place] at (5.55,3.95) {}; \node[lbl, anchor=south] at (5.2,4.6) {Lighthouse Museum}; \draw[line width=0.8pt] (5.45,4.62) -- (5.55,4.06);
  \draw[line width=1pt, dashed] (5.9,3.75) -- (6.25,3.5);
  % Main Street and the town
  \draw[line width=5pt, black!40] (0.15,6.3) -- (3.45,6.3);
  \node[lbl, font=\bfseries] at (1.8,6.3) {\colorbox{white}{Main Street}};
  \node[place] at (0.55,6.75) {}; \node[lbl, anchor=south] at (0.55,6.88) {Library};
  \node[place] at (2.3,6.75) {}; \node[lbl, anchor=south] at (2.3,6.88) {Church Hall};
  \node[place] at (0.55,5.85) {}; \node[lbl, anchor=north] at (0.55,5.72) {Gazette};
  \node[place] at (1.55,5.85) {}; \node[lbl, anchor=north] at (1.55,5.72) {Bakery};
  \node[place] at (2.75,5.85) {}; \node[lbl, anchor=north] at (2.75,5.72) {General Store};
  \node[place] at (0.55,7.65) {}; \node[lbl, anchor=west] at (0.72,7.65) {Gull's Rest Inn};
  \draw[line width=1.4pt] (0.2,4.25) rectangle (1.75,4.95); \node[lbl] at (0.97,4.6) {Town Green};
  % piers
  \draw[line width=3.5pt] (3.5,7.2) -- (4.25,7.2); \node[lbl, anchor=west] at (4.3,7.2) {Ferry Dock};
  \draw[line width=3.5pt] (3.5,5.3) -- (4.35,5.3); \node[lbl, anchor=west] at (4.4,5.3) {Town Pier};
  \node[place] at (3.1,5.05) {}; \node[lbl, anchor=east] at (2.95,5.05) {Harbor Office};
  % shore
  \draw[line width=1.2pt, dotted] (3.3,3.95) .. controls (3.15,3.5) and (3.2,3.1) .. (3.35,2.75);
  \node[lbl, anchor=east] at (3.1,3.35) {Thimble Beach};
  \node[place] at (3.1,1.6) {}; \node[lbl, anchor=east] at (2.95,1.6) {Okafor Boatyard};
  % water
  \node[lbl] at (4.45,1.35) {East Cove};
  \draw[line width=1.4pt, fill=white] (5.75,6.65) ellipse (0.72 and 0.36); \node[lbl] at (5.75,6.65) {Gull Island};
  \node[lbl] at (4.75,6.2) {the Narrows};
  \fill (4.75,2.55) circle (0.07); \node[lbl, anchor=west] at (4.85,2.55) {Gull Rock};
  \node[lbl, anchor=west, font=\itshape] at (4.85,2.22) {(the beacon)};
  \draw[->, line width=1.2pt] (5.6,1.65) -- (6.4,1.0); \node[lbl, anchor=west] at (5.35,0.62) {to Cobb Point};
  \node[lbl, anchor=west] at (5.35,0.3) {and Pine Key};
  % inland
  \draw[<-, line width=1.2pt] (0.15,2.6) -- (0.75,2.6); \node[lbl, anchor=west] at (0.8,2.6) {Hilltop Orchard};
  \draw[<-, line width=1.2pt] (0.15,2.05) -- (0.75,2.05); \node[lbl, anchor=west] at (0.8,2.05) {County Fairgrounds};
  % compass
  \begin{scope}[shift={(6.7,7.4)}]
    \draw[line width=1pt] (0,-0.3) -- (0,0.3) (-0.3,0) -- (0.3,0);
    \fill (0,0.3) -- (-0.08,0.08) -- (0.08,0.08) -- cycle;
    \node[lbl, anchor=south, font=\bfseries] at (0,0.32) {N};
  \end{scope}
\end{tikzpicture}\end{center}
\clearpage"""
