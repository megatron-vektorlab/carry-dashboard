"""LaTeX/TikZ building blocks for the book pages (large print).

All lengths are in inches.  Reading text is 16 pt Atkinson Hyperlegible
(\\normalsize); grid labels are 16 pt too.
"""
from __future__ import annotations

from .grid import esc, layout
from .measure import width

LABEL_PT = 16
BAND = 0.40            # gray band holding a category name
GAP = 0.08             # gap between labels and grid


def _col_values(cat):
    return [str(v) for v in cat["values"]]


def grid_geometry(B, max_w, max_h, max_cell=0.52):
    rows, cols, _ = layout(B.k)
    n = B.n
    row_lab = max(width(v, LABEL_PT) for c in rows for v in _col_values(B.cats[c])) + GAP + 0.06
    col_lab = max(width(v, LABEL_PT) for c in cols for v in _col_values(B.cats[c])) + GAP + 0.06
    cell = min(max_cell, (max_w - BAND - row_lab) / (len(cols) * n), (max_h - BAND - col_lab) / (len(rows) * n))
    return dict(rows=rows, cols=cols, cell=cell, row_lab=row_lab, col_lab=col_lab,
                w=BAND + row_lab + len(cols) * n * cell, h=BAND + col_lab + len(rows) * n * cell)


def mark_o(cx, cy, cell):
    return rf"\fill ({cx:.3f},{cy:.3f}) circle ({cell * 0.24:.3f});"


def mark_x(cx, cy, cell):
    d = cell * 0.24
    return (rf"\draw[line width=1.1pt] ({cx - d:.3f},{cy - d:.3f}) -- ({cx + d:.3f},{cy + d:.3f}) "
            rf"({cx - d:.3f},{cy + d:.3f}) -- ({cx + d:.3f},{cy - d:.3f});")


def grid_tikz(B, max_w=7.0, max_h=6.0, marks=None, highlight=None, max_cell=0.52):
    """The staircase grid, sized to fit max_w x max_h inches.

    marks: {((c1, v1), (c2, v2)): 'O' | 'X'}; highlight: set of such cells.
    """
    g = grid_geometry(B, max_w, max_h, max_cell)
    rows, cols, cell, n = g["rows"], g["cols"], g["cell"], B.n
    out = [r"\begin{tikzpicture}[x=1in,y=1in,line cap=rect,line join=miter]"]
    blocks = layout(B.k)[2]
    W, H = len(cols) * n * cell, len(rows) * n * cell
    # category bands
    for ci, cc in enumerate(cols):
        x0 = ci * n * cell
        y0 = g["col_lab"]
        out.append(rf"\fill[black!13] ({x0:.3f},{y0:.3f}) rectangle ({x0 + n * cell:.3f},{y0 + BAND:.3f});")
        out.append(rf"\draw[line width=0.8pt] ({x0:.3f},{y0:.3f}) rectangle ({x0 + n * cell:.3f},{y0 + BAND:.3f});")
        out.append(rf"\node[font=\bfseries] at ({x0 + n * cell / 2:.3f},{y0 + BAND / 2:.3f}) "
                   rf"{{{esc(B.cats[cc]['label'])}}};")
        for j, v in enumerate(_col_values(B.cats[cc])):
            out.append(rf"\node[rotate=90, anchor=west, inner sep=0pt] at ({x0 + (j + 0.5) * cell:.3f},{GAP:.3f}) "
                       rf"{{\strut {esc(v)}}};")
    for ri, rc in enumerate(rows):
        y0 = -ri * n * cell
        x0 = -g["row_lab"] - BAND
        out.append(rf"\fill[black!13] ({x0:.3f},{y0:.3f}) rectangle ({x0 + BAND:.3f},{y0 - n * cell:.3f});")
        out.append(rf"\draw[line width=0.8pt] ({x0:.3f},{y0:.3f}) rectangle ({x0 + BAND:.3f},{y0 - n * cell:.3f});")
        out.append(rf"\node[font=\bfseries, rotate=90] at ({x0 + BAND / 2:.3f},{y0 - n * cell / 2:.3f}) "
                   rf"{{{esc(B.cats[rc]['label'])}}};")
        for i, v in enumerate(_col_values(B.cats[rc])):
            out.append(rf"\node[anchor=east, inner sep=0pt] at ({-GAP:.3f},{y0 - (i + 0.5) * cell:.3f}) "
                       rf"{{\strut {esc(v)}}};")
    for (ri, ci), (rc, cc) in blocks.items():
        x0, y0 = ci * n * cell, -ri * n * cell
        for i in range(n):
            for j in range(n):
                key = ((rc, i), (cc, j))
                if highlight and (key in highlight or (key[1], key[0]) in highlight):
                    out.append(rf"\fill[black!22] ({x0 + j * cell:.3f},{y0 - i * cell:.3f}) rectangle "
                               rf"({x0 + (j + 1) * cell:.3f},{y0 - (i + 1) * cell:.3f});")
        for t in range(1, n):
            out.append(rf"\draw[black!60, line width=0.8pt] ({x0 + t * cell:.3f},{y0:.3f}) -- ({x0 + t * cell:.3f},{y0 - n * cell:.3f});")
            out.append(rf"\draw[black!60, line width=0.8pt] ({x0:.3f},{y0 - t * cell:.3f}) -- ({x0 + n * cell:.3f},{y0 - t * cell:.3f});")
        out.append(rf"\draw[line width=2pt] ({x0:.3f},{y0:.3f}) rectangle ({x0 + n * cell:.3f},{y0 - n * cell:.3f});")
        if marks:
            for i in range(n):
                for j in range(n):
                    m = marks.get(((rc, i), (cc, j))) or marks.get(((cc, j), (rc, i)))
                    if m:
                        cx, cy = x0 + (j + 0.5) * cell, y0 - (i + 0.5) * cell
                        out.append(mark_o(cx, cy, cell) if m == "O" else mark_x(cx, cy, cell))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out), g


def answer_table(B, filled=None, name_w=None, stretch=1.45):
    """Blank (or filled) answer table: one row per person."""
    k = B.k
    cols = "|" + "|".join(["l"] + ["p{%.2fin}" % max(1.15, 0.12 + max(width(v) for v in _col_values(B.cats[c])))
                                   for c in range(1, k)]) + "|"
    out = [r"\begingroup\renewcommand{\arraystretch}{%.2f}\begin{tabular}{" % stretch + cols + r"}\hline"]
    out.append(" & ".join(r"\bfseries " + esc(B.cats[c]["label"]) for c in range(k)) + r" \\ \hline")
    for e in range(B.n):
        cells = [esc(B.cats[0]["values"][e])]
        for c in range(1, k):
            cells.append(esc(B.cats[c]["values"][filled[c][e]]) if filled else "")
        out.append(" & ".join(cells) + r" \\ \hline")
    out.append(r"\end{tabular}\endgroup")
    return "\n".join(out)


def lineup_strip(B, cat):
    """Boxes for writing the final order of a line-up."""
    labs = _col_values(B.cats[cat])
    w = min(1.3, 6.6 / len(labs))
    out = [r"\begin{tikzpicture}[x=1in,y=1in]"]
    for i, lab in enumerate(labs):
        x = i * w
        out.append(rf"\draw[line width=1.5pt] ({x + 0.05:.3f},0) rectangle ({x + w - 0.05:.3f},0.62);")
        out.append(rf"\node[anchor=north] at ({x + w / 2:.3f},-0.04) {{\strut {esc(lab)}}};")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def liar_table(names, n_statements=None, rh=0.44):
    """Truth table: one row per suspect tested, one column per statement."""
    n = len(names)
    cw = max(0.62, max(width(x, LABEL_PT, "sfb") for x in names) + 0.14)
    name_w0 = max(width(f"If {x} did it") for x in names) + 0.25
    short = name_w0 + (n + 2) * cw > 7.0
    if short:
        cw = max(0.62, (7.0 - name_w0) / (n + 2))
    name_w = max(width(f"If {x} did it") for x in names) + 0.25
    out = [r"\begin{tikzpicture}[x=1in,y=1in]"]
    cols = [f"{x[:1]}." for x in names] + ["True", "Fits?"]
    top = 0
    for j, c in enumerate(cols):
        x = name_w + j * cw
        out.append(rf"\fill[black!13] ({x:.3f},{top:.3f}) rectangle ({x + cw:.3f},{top + rh:.3f});")
        out.append(rf"\node[font=\bfseries] at ({x + cw / 2:.3f},{top + rh / 2:.3f}) {{{esc(c) if j >= n else (esc(names[j][:1]) + "." if short else esc(names[j]))}}};")
    for i, x in enumerate(names):
        y = top - (i + 1) * rh
        out.append(rf"\node[anchor=east] at ({name_w - 0.1:.3f},{y + rh / 2:.3f}) {{If {esc(x)} did it}};")
        for j in range(len(cols)):
            xx = name_w + j * cw
            out.append(rf"\draw[line width=0.8pt] ({xx:.3f},{y:.3f}) rectangle ({xx + cw:.3f},{y + rh:.3f});")
    out.append(rf"\draw[line width=2pt] ({name_w:.3f},{top + rh:.3f}) rectangle ({name_w + len(cols) * cw:.3f},{top - n * rh:.3f});")
    out.append(rf"\draw[line width=2pt] ({name_w + n * cw:.3f},{top + rh:.3f}) -- ({name_w + n * cw:.3f},{top - n * rh:.3f});")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def stars_tikz(k, total=5, size=0.17):
    out = [r"\begin{tikzpicture}[x=1in,y=1in,baseline=-0.07in]"]
    for i in range(total):
        style = "fill=black, draw=black" if i < k else "draw=black, line width=0.9pt"
        out.append(rf"\node[star, star points=5, star point ratio=2.3, minimum size={size}in, inner sep=0pt, {style}] "
                   rf"at ({i * (size + 0.06):.3f},0) {{}};")
    out.append(r"\end{tikzpicture}")
    return "".join(out)
