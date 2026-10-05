"""Full-wrap paperback cover (KDP, no bleed interior, white paper).

    .venv/bin/python -m lp.cover [PAGES]      # default: page count of build/book/interior.pdf

Size: 2 x 8.5 in + spine + 2 x 0.125 in bleed wide, 11.25 in tall.
Spine width = pages x 0.002252 in (white paper).  Everything important stays
0.375 in inside the trim; spine text keeps 0.0625 in from the spine folds.
"""
from __future__ import annotations

import os
import subprocess
import sys

from . import config

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "cover")
BLEED = 0.125
TRIM_W, TRIM_H = 8.5, 11.0


def page_count():
    import fitz
    return fitz.open(os.path.join(ROOT, "build", "book", "interior.pdf")).page_count


def grid_card():
    """A small half-solved logic grid with X's and dots, drawn at the origin (4 x 4 cells)."""
    marks = {(0, 0): "O", (0, 1): "X", (0, 2): "X", (0, 3): "X", (1, 0): "X", (2, 0): "X", (3, 0): "X",
             (1, 2): "O", (1, 1): "X", (1, 3): "X", (2, 2): "X", (3, 2): "X", (2, 1): "X"}
    c = 0.42
    out = [r"\fill[cream, rounded corners=6pt] (-0.25,-0.25) rectangle (%.2f,%.2f);" % (4 * c + 0.25, 4 * c + 0.25)]
    for i in range(5):
        lw = "1.6pt" if i in (0, 4) else "0.9pt"
        out.append(r"\draw[navy, line width=%s] (0,%.3f) -- (%.3f,%.3f);" % (lw, i * c, 4 * c, i * c))
        out.append(r"\draw[navy, line width=%s] (%.3f,0) -- (%.3f,%.3f);" % (lw, i * c, i * c, 4 * c))
    for (r, k), m in marks.items():
        x, y = (k + 0.5) * c, (3 - r + 0.5) * c
        if m == "O":
            out.append(r"\fill[navy] (%.3f,%.3f) circle (0.11);" % (x, y))
        else:
            d = 0.11
            out.append(r"\draw[coral, line width=2.2pt] (%.3f,%.3f) -- (%.3f,%.3f) (%.3f,%.3f) -- (%.3f,%.3f);"
                       % (x - d, y - d, x + d, y + d, x - d, y + d, x + d, y - d))
    return "\n".join(out)


def lighthouse(x, y, s):
    """Lighthouse with beams, base at (x, y), height about 3.2*s in."""
    return rf"""
\begin{{scope}}[shift={{({x},{y})}}, scale={s}]
  \fill[beam, opacity=0.30] (0,2.92) -- (-4.2,3.75) -- (-4.2,2.35) -- cycle;
  \fill[beam, opacity=0.22] (0,2.92) -- (3.4,3.55) -- (3.4,2.45) -- cycle;
  \fill[cream] (-0.42,0) -- (-0.28,2.4) -- (0.28,2.4) -- (0.42,0) -- cycle;
  \fill[coral] (-0.385,0.55) -- (0.385,0.55) -- (0.37,0.85) -- (-0.37,0.85) -- cycle;
  \fill[coral] (-0.34,1.35) -- (0.34,1.35) -- (0.325,1.62) -- (-0.325,1.62) -- cycle;
  \fill[cream] (-0.4,2.4) rectangle (0.4,2.5);
  \fill[mustard] (-0.22,2.5) rectangle (0.22,2.95);
  \draw[navy, line width=1pt] (0,2.5) -- (0,2.95) (-0.22,2.72) -- (0.22,2.72);
  \fill[cream] (-0.3,2.95) -- (0,3.2) -- (0.3,2.95) -- cycle;
  \fill[navy!70!black] (-0.1,0) rectangle (0.1,0.35);
\end{{scope}}"""


def front_panel(x0):
    """TikZ for the front cover; x0 = left edge of the front trim."""
    cx = x0 + TRIM_W / 2
    return rf"""
% sky and sea
\shade[top color=navy, bottom color=dusk] ({x0 - 0.01},{BLEED + 3.2}) rectangle ({x0 + TRIM_W + BLEED},{TRIM_H + 2 * BLEED});
\fill[sea] ({x0 - 0.01},0) rectangle ({x0 + TRIM_W + BLEED},{BLEED + 3.25});
% stars
\foreach \sx/\sy in {{0.6/9.0, 1.4/8.4, 2.3/8.9, 6.9/9.2, 7.6/8.5, 5.9/8.7, 3.4/8.2, 7.9/7.6, 0.9/7.7}}
  \fill[cream, opacity=0.8] ({x0}+\sx,{BLEED}+\sy) circle (0.022);
\fill[cream] ({x0 + 7.1},{BLEED + 7.95}) circle (0.30);
\fill[navy] ({x0 + 7.22},{BLEED + 8.03}) circle (0.27);
% headland, lighthouse and town
\fill[land] ({x0 + 4.6},{BLEED + 3.2}) .. controls ({x0 + 5.6},{BLEED + 3.9}) and ({x0 + 7.4},{BLEED + 3.95}) .. ({x0 + TRIM_W + BLEED},{BLEED + 3.9}) -- ({x0 + TRIM_W + BLEED},{BLEED + 3.2}) -- cycle;
{lighthouse(x0 + 6.75, BLEED + 3.85, 0.95)}
\foreach \hx/\hw/\hh in {{5.1/0.42/0.38, 5.6/0.36/0.30}}
  {{\fill[cream!85!navy] ({x0}+\hx,{BLEED + 3.55}) rectangle ++(\hw,\hh);
   \fill[cream!85!navy] ({x0}+\hx-0.04,{BLEED + 3.55}+\hh) -- ++(\hw/2+0.04,0.2) -- ++(\hw/2+0.04,-0.2) -- cycle;
   \fill[mustard] ({x0}+\hx+0.12,{BLEED + 3.62}) rectangle ++(0.09,0.1);}}
% waves
\foreach \wy in {{2.75, 2.25, 1.75}}
  \draw[cream, opacity=0.35, line width=1.2pt] ({x0 + 0.4},{BLEED}+\wy) .. controls ({x0 + 0.9},{BLEED}+\wy+0.12) and ({x0 + 1.3},{BLEED}+\wy-0.12) .. ({x0 + 1.8},{BLEED}+\wy)
     .. controls ({x0 + 2.3},{BLEED}+\wy+0.12) and ({x0 + 2.7},{BLEED}+\wy-0.12) .. ({x0 + 3.2},{BLEED}+\wy);
% large print band
\fill[mustard] ({x0 - 0.01},{BLEED + TRIM_H - 0.95}) rectangle ({x0 + TRIM_W + BLEED},{BLEED + TRIM_H - 0.38});
\node[navy, font=\sffamily\bfseries\fontsize{24}{24}\selectfont] at ({cx},{BLEED + TRIM_H - 0.665}) {L\,A\,R\,G\,E\quad P\,R\,I\,N\,T};
\node[cream, font=\sffamily\bfseries\fontsize{13.5}{16}\selectfont] at ({cx},{BLEED + TRIM_H - 1.32}) {{{config.SERIES.upper()}\enspace\textperiodcentered\enspace BOOK {config.SERIES_NO}}};
% title
\node[cream, align=center, font=\rmfamily\fontsize{58}{62}\selectfont] at ({cx},{BLEED + TRIM_H - 2.75})
  {{Cozy Mystery\\[2pt]Logic Puzzles}};
\node[mustard, font=\rmfamily\itshape\fontsize{40}{44}\selectfont] at ({cx},{BLEED + TRIM_H - 4.3}) {{for Beginners}};
% badge
\fill[coral] ({x0 + 7.15},{BLEED + 6.25}) circle (0.78);
\draw[cream, line width=1.5pt] ({x0 + 7.15},{BLEED + 6.25}) circle (0.70);
\node[cream, align=center, font=\sffamily\bfseries] at ({x0 + 7.15},{BLEED + 6.25}) {{\fontsize{34}{34}\selectfont 100\\[2pt]\fontsize{13}{13}\selectfont PUZZLES}};
% grid card and magnifier
\begin{{scope}}[shift={{({x0 + 1.05},{BLEED + 4.15})}}, rotate=-6]
{grid_card()}
\draw[mustard, line width=5pt] (1.55,1.15) circle (0.62);
\fill[cream, opacity=0.18] (1.55,1.15) circle (0.6);
\draw[mustard, line width=9pt, line cap=round] (2.0,0.7) -- (2.55,0.15);
\end{{scope}}
% subtitle strip
\fill[navy, opacity=0.85] ({x0 - 0.01},{BLEED + 1.55}) rectangle ({x0 + TRIM_W + BLEED},{BLEED + 2.62});
\node[cream, align=center, font=\sffamily\bfseries\fontsize{15.5}{20}\selectfont] at ({cx},{BLEED + 2.09})
  {{Step-by-Step Lessons\enspace\textperiodcentered\enspace 3-Step Hints for Every Puzzle\\Every Solution Explained\enspace\textperiodcentered\enspace Whodunits from Easy to Expert}};
% difficulty bar
\node[cream, font=\sffamily\bfseries\fontsize{13}{13}\selectfont, anchor=east] at ({cx - 1.55},{BLEED + 1.12}) {{EASY}};
\node[cream, font=\sffamily\bfseries\fontsize{13}{13}\selectfont, anchor=west] at ({cx + 1.55},{BLEED + 1.12}) {{EXPERT}};
\foreach \k in {{0,...,4}}
  \node[star, star points=5, star point ratio=2.3, minimum size={{0.2+0.06*\k}}in, inner sep=0pt, fill=mustard]
     at ({cx - 1.2}+0.6*\k,{BLEED + 1.12}) {{}};
% author
\node[cream, font=\rmfamily\fontsize{22}{24}\selectfont] at ({cx},{BLEED + 0.55}) {{{config.AUTHOR}}};
"""


def back_panel(x0, thumb):
    cx = x0 + TRIM_W / 2
    img = (rf"\node[draw=cream, line width=3pt, inner sep=0pt, rotate=3] at ({x0 + 6.0},{BLEED + 3.6}) "
           rf"{{\includegraphics[width=2.55in]{{{thumb}}}}};") if thumb else ""
    return rf"""
\fill[navy] ({-0.01},0) rectangle ({x0 + TRIM_W + 0.01},{TRIM_H + 2 * BLEED});
\node[mustard, anchor=north west, align=left, font=\rmfamily\fontsize{30}{34}\selectfont] at ({x0 + 0.6},{BLEED + TRIM_H - 0.6})
  {{Learn it. Solve it.\\Never get stuck.}};
\node[cream, anchor=north west, text width=7.1in, align=left, font=\sffamily\fontsize{14.5}{19.5}\selectfont] at ({x0 + 0.6},{BLEED + TRIM_H - 2.05})
  {{Welcome to Thimble Harbor, a small New England town with one ferry, one lighthouse, and far too many opinions about pie.
  Retired puzzle editor Ada Quill needs an apprentice, and she will teach you everything, one clue at a time.\par\vspace{{8pt}}
  Start with swapped jam labels and a goat in the pie tent. Finish with the Lighthouse Affair: five linked cases and
  one final question. Who took the town's beloved Keeper's Lamp?}};
\node[cream, anchor=north west, text width=3.85in, align=left, font=\sffamily\fontsize{14}{18.5}\selectfont] at ({x0 + 0.6},{BLEED + 5.75})
  {{\textbf{{\color{{mustard}}Six friendly lessons}} with pictures of the grid, step by step.\par\vspace{{6pt}}
  \textbf{{\color{{mustard}}A three-step hint ladder}} for every puzzle, so you take only the help you need.\par\vspace{{6pt}}
  \textbf{{\color{{mustard}}Every solution explained}} in plain words, not just the answer.\par\vspace{{6pt}}
  \textbf{{\color{{mustard}}Large 16-point print}}, big grids, and room to write.}};
{img}
\node[cream, anchor=south west, text width=4.3in, align=left, font=\sffamily\itshape\fontsize{12.5}{16}\selectfont] at ({x0 + 0.6},{BLEED + 0.6})
  {{Every puzzle was checked by computer to have exactly one solution.}};
"""


def spine(x0, w):
    if w < 0.4:
        return ""
    cx = x0 + w / 2
    fs = min(15, w * 72 * 0.42)
    return rf"""
\fill[navy!85!black] ({x0},0) rectangle ({x0 + w},{TRIM_H + 2 * BLEED});
\node[cream, rotate=-90, font=\rmfamily\fontsize{{{fs:.1f}}}{{{fs:.1f}}}\selectfont] at ({cx},{BLEED + TRIM_H / 2 + 0.6})
  {{Cozy Mystery Logic Puzzles for Beginners}};
\node[mustard, rotate=-90, font=\sffamily\bfseries\fontsize{{{fs * 0.8:.1f}}}{{{fs * 0.8:.1f}}}\selectfont] at ({cx},{BLEED + 1.75})
  {{{config.AUTHOR}}};
\node[mustard, rotate=-90, font=\sffamily\bfseries\fontsize{{{fs * 0.8:.1f}}}{{{fs * 0.8:.1f}}}\selectfont] at ({cx},{BLEED + TRIM_H - 0.85})
  {{BOOK {config.SERIES_NO}}};
"""


def build(pages, thumb=None):
    sw = round(pages * 0.002252, 4)
    W = 2 * TRIM_W + sw + 2 * BLEED
    H = TRIM_H + 2 * BLEED
    back_x0 = BLEED
    spine_x0 = BLEED + TRIM_W
    front_x0 = spine_x0 + sw
    src = rf"""\documentclass{{article}}
\usepackage[paperwidth={W:.4f}in, paperheight={H:.4f}in, margin=0in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[lining]{{librecaslon}}
\usepackage{{atkinson}}
\usepackage{{tikz, graphicx, xcolor}}
\usetikzlibrary{{shapes.geometric}}
\definecolor{{navy}}{{HTML}}{{1B2F4E}}
\definecolor{{dusk}}{{HTML}}{{2F5D73}}
\definecolor{{sea}}{{HTML}}{{1C4A57}}
\definecolor{{land}}{{HTML}}{{243B4A}}
\definecolor{{cream}}{{HTML}}{{F6EEDC}}
\definecolor{{mustard}}{{HTML}}{{E6AE3E}}
\definecolor{{coral}}{{HTML}}{{E07A5F}}
\definecolor{{beam}}{{HTML}}{{F9E7B0}}
\pagestyle{{empty}}
\pdfinfo{{/Title (Cover: {config.TITLE}) /Author ({config.AUTHOR})}}
\begin{{document}}
\noindent\begin{{tikzpicture}}[x=1in, y=1in]
\useasboundingbox (0,0) rectangle ({W:.4f},{H:.4f});
\clip (0,0) rectangle ({W:.4f},{H:.4f});
{back_panel(back_x0, thumb)}
{spine(spine_x0, sw)}
{front_panel(front_x0)}
\end{{tikzpicture}}
\end{{document}}
"""
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "cover.tex"), "w") as f:
        f.write(src)
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "cover.tex"], cwd=OUT,
                       capture_output=True, text=True)
    if r.returncode:
        sys.stdout.write(r.stdout[-3000:])
        raise SystemExit("cover failed")
    # front-only image for the listing / ads
    subprocess.run(["pdftoppm", "-r", "150", "-png", "-x", str(int(front_x0 * 150)), "-y", str(int(BLEED * 150)),
                    "-W", str(int(TRIM_W * 150)), "-H", str(int(TRIM_H * 150)), "-singlefile", "cover.pdf",
                    "front"], cwd=OUT, check=True)
    print(f"cover: {pages} pages, spine {sw:.3f} in, {W:.3f} x {H:.3f} in")
    return os.path.join(OUT, "cover.pdf")


def main():
    pages = int(sys.argv[1]) if len(sys.argv) > 1 else page_count()
    thumb = os.path.join(ROOT, "build", "cover", "thumb.png")
    build(pages, thumb if os.path.exists(thumb) else None)


if __name__ == "__main__":
    main()
