"""KDP paperback cover (full wrap: back + spine + front, with bleed).

    .venv/bin/python -m asvab.cover            # reads the interior page count
    .venv/bin/python -m asvab.cover --pages 312

Spine width follows KDP's formula for black-and-white interiors on white
paper: pages x 0.002252 in.  Bleed 0.125 in on every outer edge.  The
barcode area (2 x 1.2 in, lower right of the back cover) is left empty for
KDP's barcode.  Outputs:
    output/ASVAB-Math-Workbook-cover.pdf   (upload to KDP)
    output/front-cover.png                 (marketing / preview)
"""
from __future__ import annotations

import argparse
import re
import subprocess

from . import config
from .render import BUILD, ROOT

OUT = ROOT / "output"
BLEED = 0.125
PAPER = 0.002252          # in per page, white paper, B&W


def page_count() -> int:
    pdf = OUT / "ASVAB-Math-Workbook-interior.pdf"
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", info).group(1))


def cover_tex(pages: int) -> tuple[str, float, float]:
    tw, th = config.TRIM_W, config.TRIM_H
    spine = pages * PAPER
    W = 2 * BLEED + 2 * tw + spine
    H = 2 * BLEED + th
    bx0 = BLEED                 # back panel trim, left
    sx0 = BLEED + tw            # spine left
    fx0 = sx0 + spine           # front panel trim, left
    fcx = fx0 + tw / 2          # front center
    bcx = bx0 + tw / 2
    top = BLEED + th            # trim top (y)
    T = config
    spine_text = pages >= 80

    tex = rf"""\documentclass{{article}}
\usepackage[paperwidth={W:.4f}in,paperheight={H:.4f}in,margin=0in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[black,medium,lining,defaultfam]{{montserrat}}
\usepackage{{tikz}}
\usetikzlibrary{{calc}}
\definecolor{{navy}}{{HTML}}{{0F1D36}}
\definecolor{{navy2}}{{HTML}}{{1A2C4E}}
\definecolor{{gridc}}{{HTML}}{{22385F}}
\definecolor{{gold}}{{HTML}}{{F2B53A}}
\definecolor{{paper}}{{HTML}}{{F5F1E6}}
\raggedright\hyphenpenalty=10000
\pagestyle{{empty}}
\setlength{{\parindent}}{{0pt}}
\newcommand{{\chk}}{{\tikz[x=1pt,y=1pt,baseline=-1pt]\draw[gold,line width=2.4pt,line cap=round,line join=round] (0,5) -- (4,1) -- (11,10);}}
\begin{{document}}
\begin{{tikzpicture}}[x=1in,y=1in,remember picture,overlay]
\begin{{scope}}[shift={{(current page.south west)}}]
% background
\fill[navy] (0,0) rectangle ({W:.4f},{H:.4f});
% graph-paper texture on the front panel
\begin{{scope}}
\clip ({fx0:.4f},0) rectangle ({W:.4f},{H:.4f});
\draw[gridc,line width=0.4pt,step=0.25] ({fx0:.4f},0) grid ({W:.4f},{H:.4f});
\draw[gridc!70!white,line width=0.9pt,step=1] ({fx0:.4f},0) grid ({W:.4f},{H:.4f});
\end{{scope}}
% gold top band (front)
\fill[gold] ({fx0:.4f},{top - 0.95:.4f}) rectangle ({W:.4f},{H:.4f});
\node[anchor=west,text=navy,font=\bfseries\fontsize{{15}}{{18}}\selectfont]
  at ({fx0 + 0.55:.4f},{top - 0.48:.4f}) {{NO CALCULATOR \textbullet{{}} JUST PRACTICE}};
\node[anchor=east,text=navy,font=\mdseries\fontsize{{13}}{{16}}\selectfont]
  at ({W - BLEED - 0.55:.4f},{top - 0.48:.4f}) {{{T.YEAR} EDITION}};

% title
\node[anchor=north west,text=white,font=\bfseries\fontsize{{132}}{{132}}\selectfont,inner sep=0]
  at ({fx0 + 0.5:.4f},{top - 1.45:.4f}) {{ASVAB}};
\node[anchor=north west,text=gold,font=\bfseries\fontsize{{50}}{{56}}\selectfont,inner sep=0]
  at ({fx0 + 0.56:.4f},{top - 3.45:.4f}) {{MATH WORKBOOK}};
\node[anchor=north west,text=white,font=\mdseries\fontsize{{21}}{{27}}\selectfont,inner sep=0,
  text width=7.3in,align=left] at ({fx0 + 0.58:.4f},{top - 4.55:.4f})
  {{1,000 Practice Problems with\\Step-by-Step Solutions}};

% chevrons
\foreach \i in {{0,1,2}} {{
  \draw[gold,line width=5pt,line cap=butt]
    ({fx0 + 0.6:.4f}+\i*0.42,{top - 6.0:.4f}) -- ++(0.2,0.22) -- ++(0.2,-0.22);
}}
\draw[white!40!navy,line width=1pt] ({fx0 + 2.0:.4f},{top - 5.89:.4f}) -- ({fx0 + tw - 2.6:.4f},{top - 5.89:.4f});

% feature list
\node[anchor=north west,text=white,font=\mdseries\fontsize{{15.5}}{{25}}\selectfont,inner sep=0,
  text width=7.2in,align=left] at ({fx0 + 0.6:.4f},{top - 6.35:.4f}) {{%
  \chk\enspace Key concepts \& worked examples for 27 topics\\
  \chk\enspace Diagnostic test with a personal study plan\\
  \chk\enspace 4 full-length math practice tests\\
  \chk\enspace Every wrong answer explained\\
  \chk\enspace Every answer verified by computer algebra}};

% badge
\fill[gold] ({fx0 + tw - 1.45:.4f},{top - 5.22:.4f}) circle (0.92);
\draw[navy,line width=1.2pt] ({fx0 + tw - 1.45:.4f},{top - 5.22:.4f}) circle (0.81);
\node[text=navy,align=center,font=\bfseries\fontsize{{32}}{{32}}\selectfont]
  at ({fx0 + tw - 1.45:.4f},{top - 5.07:.4f}) {{1,000}};
\node[text=navy,align=center,font=\bfseries\fontsize{{11.5}}{{14}}\selectfont]
  at ({fx0 + tw - 1.45:.4f},{top - 5.55:.4f}) {{PROBLEMS}};

% bottom strip (front)
\fill[navy2] ({fx0:.4f},0) rectangle ({W:.4f},{BLEED + 1.55:.4f});
\draw[gold,line width=2pt] ({fx0:.4f},{BLEED + 1.55:.4f}) -- ({W:.4f},{BLEED + 1.55:.4f});
\node[anchor=west,text=white,font=\mdseries\fontsize{{14}}{{18}}\selectfont,text width=5.4in,align=left]
  at ({fx0 + 0.6:.4f},{BLEED + 0.8:.4f})
  {{Arithmetic Reasoning\\Mathematics Knowledge}};
\node[anchor=east,text=gold,font=\bfseries\fontsize{{17}}{{20}}\selectfont]
  at ({W - BLEED - 0.55:.4f},{BLEED + 0.8:.4f}) {{{T.AUTHOR.upper()}}};

% ---------------------------------------------------------------- spine
\fill[navy2] ({sx0:.4f},0) rectangle ({fx0:.4f},{H:.4f});
"""
    if spine_text:
        fs = min(14, max(8, spine * 72 * 0.42))
        tex += rf"""\node[rotate=-90,text=white,font=\bfseries\fontsize{{{fs:.1f}}}{{{fs:.1f}}}\selectfont]
  at ({sx0 + spine / 2:.4f},{top - 2.9:.4f}) {{ASVAB \textcolor{{gold}}{{MATH WORKBOOK}}}};
\node[rotate=-90,text=white,font=\mdseries\fontsize{{{fs * 0.8:.1f}}}{{{fs:.1f}}}\selectfont]
  at ({sx0 + spine / 2:.4f},{top - 6.9:.4f}) {{1,000 Problems \textbullet{{}} Step-by-Step Solutions}};
\node[rotate=-90,text=gold,font=\bfseries\fontsize{{{fs * 0.8:.1f}}}{{{fs:.1f}}}\selectfont]
  at ({sx0 + spine / 2:.4f},{BLEED + 1.0:.4f}) {{{T.AUTHOR.upper()}}};
"""
    tex += rf"""
% ---------------------------------------------------------------- back
\fill[gold] (0,{top - 0.18:.4f}) rectangle ({sx0:.4f},{H:.4f});
\node[anchor=north west,text=white,font=\bfseries\fontsize{{27}}{{32}}\selectfont,text width=7.2in,align=left]
  at ({bx0 + 0.6:.4f},{top - 0.65:.4f}) {{Master the math.\\\textcolor{{gold}}{{Raise your AFQT.}}}};
\node[anchor=north west,text=white,font=\mdseries\fontsize{{12.5}}{{18}}\selectfont,text width=7.2in,align=left]
  at ({bx0 + 0.6:.4f},{top - 2.0:.4f}) {{%
  Arithmetic Reasoning and Mathematics Knowledge make up about half of your AFQT
  score---the number that decides whether you can enlist and which jobs you
  qualify for. This workbook gives you the one thing that reliably raises math
  scores: a lot of realistic practice, with every solution explained step by
  step, by hand, the way you will solve it on test day.}};
\node[anchor=north west,text=gold,font=\bfseries\fontsize{{13}}{{16}}\selectfont]
  at ({bx0 + 0.6:.4f},{top - 3.75:.4f}) {{INSIDE YOU'LL FIND}};
\node[anchor=north west,text=white,font=\mdseries\fontsize{{11.5}}{{20}}\selectfont,text width=7.4in,align=left]
  at ({bx0 + 0.6:.4f},{top - 4.15:.4f}) {{%
  \chk\enspace \textbf{{1,000 problems}}: 750 drills, a 30-question diagnostic, 4 practice tests\\
  \chk\enspace \textbf{{27 chapters}}: fractions, percents, algebra, geometry, word problems\\
  \chk\enspace \textbf{{Key Concepts}} with worked examples, mental-math tips, and traps\\
  \chk\enspace \textbf{{Step-by-step solutions}} for every single problem\\
  \chk\enspace \textbf{{``Why not'' notes}} that name the mistake behind wrong answers\\
  \chk\enspace \textbf{{Formula sheet}}, glossary, and progress tracker}};
% sample solution card
\fill[paper,rounded corners=4pt] ({bx0 + 0.6:.4f},{BLEED + 1.85:.4f}) rectangle ({bx0 + 5.15:.4f},{BLEED + 4.15:.4f});
\node[anchor=north west,text=navy,font=\mdseries\fontsize{{10.5}}{{14}}\selectfont,text width=4.2in,align=left]
  at ({bx0 + 0.78:.4f},{BLEED + 4.0:.4f}) {{%
  \textbf{{\color{{navy}}EXAMPLE}}\\[2pt]
  A \$48 jacket is on sale for 25\% off. What is the sale price?\\[3pt]
  \textbf{{1}}\enspace Discount: 0.25 \texttimes{{}} 48 = 12 dollars.\\
  \textbf{{2}}\enspace Sale price: 48 \textendash{{}} 12 = 36. \ \textbf{{Answer: \$36}}\\[3pt]
  \textit{{Why not \$12? That is the discount, not the price you pay.}}}};
\node[anchor=south west,text=white!75!navy,font=\mdseries\fontsize{{7}}{{8.5}}\selectfont,text width=4.6in,align=left]
  at ({bx0 + 0.6:.4f},{BLEED + 0.45:.4f}) {{%
  ASVAB is a registered trademark of the U.S.\ Department of Defense, which was not
  involved in the production of, and does not endorse, this book.}};
% barcode area (kept empty; KDP prints the barcode here)
\fill[white] ({sx0 - 0.25 - 2.0:.4f},{BLEED + 0.25:.4f}) rectangle ({sx0 - 0.25:.4f},{BLEED + 0.25 + 1.2:.4f});
\end{{scope}}
\end{{tikzpicture}}
\end{{document}}
"""
    return tex, W, H


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int)
    a = ap.parse_args(argv)
    pages = a.pages or page_count()
    tex, W, H = cover_tex(pages)
    BUILD.mkdir(exist_ok=True)
    (BUILD / "cover.tex").write_text(tex, encoding="utf-8")
    for _ in range(2):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "cover.tex"],
                           cwd=BUILD, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(r.stdout[-3000:])
    OUT.mkdir(exist_ok=True)
    dest = OUT / "ASVAB-Math-Workbook-cover.pdf"
    dest.write_bytes((BUILD / "cover.pdf").read_bytes())
    # front panel PNG (trim only), 1600 px wide
    spine = pages * PAPER
    dpi = 1600 / config.TRIM_W
    x0 = int((BLEED + config.TRIM_W + spine) * dpi)
    y0 = int(BLEED * dpi)
    subprocess.run(["pdftoppm", "-png", "-r", f"{dpi:.2f}", "-x", str(x0), "-y", str(y0),
                    "-W", "1600", "-H", str(int(config.TRIM_H * dpi)), "-singlefile",
                    str(dest), str(OUT / "front-cover")], check=True)
    print(f"{dest}  ({W:.3f} x {H:.3f} in, spine {spine:.3f} in for {pages} pages)")
    print(OUT / "front-cover.png")


if __name__ == "__main__":
    main()
