"""TikZ drawing of the classic staircase logic grid.

Columns: categories 1..k-1, left to right.
Rows:    category 0 first, then k-1, k-2, ..., 2 (the standard layout), so
every pair of categories appears exactly once.
"""
from __future__ import annotations


def esc(s: str) -> str:
    return (s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%")
            .replace("$", r"\$").replace("#", r"\#").replace("_", r"\_"))


def layout(k: int):
    cols = list(range(1, k))
    rows = [0] + list(range(k - 1, 1, -1))
    blocks = {}
    for ri, rc in enumerate(rows):
        for ci, cc in enumerate(cols):
            if rc == 0 or cc < rc:
                blocks[(ri, ci)] = (rc, cc)
    return rows, cols, blocks


def grid_tikz(B, cell: float = 0.5, marks: dict | None = None, label_w: float = 2.3,
              head_h: float = 2.3, font: str = r"\small") -> str:
    """Return a tikzpicture of the empty (or marked) staircase grid.

    ``marks`` maps ((c1, v1), (c2, v2)) -> 'O' or 'X' to pre-fill cells.
    """
    n, k = B.n, B.k
    rows, cols, blocks = layout(k)
    W = len(cols) * n * cell
    H = len(rows) * n * cell
    out = [r"\begin{tikzpicture}[x=1cm,y=1cm,line cap=rect]"]
    # coordinates: grid top-left at (0, 0), growing right (x) and down (-y)
    for (ri, ci), (rc, cc) in blocks.items():
        x0, y0 = ci * n * cell, -ri * n * cell
        out.append(rf"\draw[black!55, line width=0.35pt] ({x0},{y0}) grid[step={cell}] ({x0 + n * cell},{y0 - n * cell});")
        out.append(rf"\draw[line width=1.1pt] ({x0},{y0}) rectangle ({x0 + n * cell},{y0 - n * cell});")
        if marks:
            for i in range(n):          # row value index (category rc)
                for j in range(n):      # column value index (category cc)
                    m = marks.get(((rc, i), (cc, j))) or marks.get(((cc, j), (rc, i)))
                    if m:
                        cx, cy = x0 + (j + 0.5) * cell, y0 - (i + 0.5) * cell
                        if m == "O":
                            out.append(rf"\draw[line width=0.9pt] ({cx},{cy}) circle ({cell * 0.32});")
                        else:
                            d = cell * 0.25
                            out.append(rf"\draw[line width=0.6pt] ({cx - d},{cy - d}) -- ({cx + d},{cy + d}) "
                                       rf"({cx - d},{cy + d}) -- ({cx + d},{cy - d});")
    # column headers (rotated value labels + category name)
    for ci, cc in enumerate(cols):
        x0 = ci * n * cell
        cat = B.cats[cc]
        for j, v in enumerate(cat["values"]):
            out.append(rf"\node[rotate=90, anchor=west, inner sep=1.5pt, font={font}] at "
                       rf"({x0 + (j + 0.5) * cell},0.06) {{{esc(v)}}};")
        out.append(rf"\node[anchor=south, font=\sffamily\bfseries\footnotesize] at ({x0 + n * cell / 2},{head_h}) "
                   rf"{{{esc(cat['label'].upper())}}};")
        out.append(rf"\draw[black!40] ({x0 + 0.05},{head_h - 0.02}) -- ({x0 + n * cell - 0.05},{head_h - 0.02});")
    # row headers
    for ri, rc in enumerate(rows):
        y0 = -ri * n * cell
        cat = B.cats[rc]
        for i, v in enumerate(cat["values"]):
            out.append(rf"\node[anchor=east, inner sep=1.5pt, font={font}] at (-0.06,{y0 - (i + 0.5) * cell}) "
                       rf"{{{esc(v)}}};")
        out.append(rf"\node[rotate=90, anchor=south, font=\sffamily\bfseries\footnotesize] at "
                   rf"(-{label_w},{y0 - n * cell / 2}) {{{esc(cat['label'].upper())}}};")
        out.append(rf"\draw[black!40] (-{label_w - 0.02},{y0 - 0.05}) -- (-{label_w - 0.02},{y0 - n * cell + 0.05});")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def solution_marks(B, sol):
    """O/X marks for every block of the solved grid."""
    marks = {}
    n, k = B.n, B.k
    owner = {}
    for c in range(k):
        for e in range(n):
            owner[(c, sol[c][e])] = e
    for c1 in range(k):
        for c2 in range(k):
            if c1 >= c2:
                continue
            for v1 in range(n):
                for v2 in range(n):
                    marks[((c1, v1), (c2, v2))] = "O" if owner[(c1, v1)] == owner[(c2, v2)] else "X"
    return marks
