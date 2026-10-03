"""Chapter 16 - Lines & Angles.

Figures are drawn from the same numbers as the stem.  Plain Python floats
appear only in the private drawing helpers (TikZ coordinates); every answer,
check and distractor is exact (ints / sympy).
"""
import math
import re

import sympy as sp

from ..core import (Q, Problem, need, num, m, dec_raw, int_raw, latex, text,
                    choose, person, soldier, template, x as X)

NUM = 16
TITLE = r"Lines \& Angles"
PART = 3

INTRO = r"""
Angles are measured in degrees ($^\circ$). Almost every angle question on the
ASVAB comes down to a few facts: a straight line is $180^\circ$, a full turn
is $360^\circ$, and parallel lines create pairs of equal angles.

\begin{concept}{Angle vocabulary and angle pairs}
\begin{tabular}{@{}ll@{\qquad}ll@{}}
\textbf{acute} & less than $90^\circ$ & \textbf{straight} & exactly $180^\circ$\\
\textbf{right} & exactly $90^\circ$ (marked with a small square) & \textbf{reflex} & between $180^\circ$ and $360^\circ$\\
\textbf{obtuse} & between $90^\circ$ and $180^\circ$ & & \\
\end{tabular}
\begin{itemize}
\item \textbf{Complementary} angles add up to $90^\circ$; \textbf{supplementary} angles add up to $180^\circ$.
\item Angles side by side on a straight line add up to $180^\circ$; angles all the way around a point add up to $360^\circ$.
\item When two lines cross, the angles directly across from each other are \textbf{vertical angles}, and they are \emph{equal}.
\end{itemize}
\end{concept}

\begin{concept}{Parallel lines cut by a transversal}
\begin{minipage}[c]{0.36\linewidth}\centering
\begin{tikzpicture}[font=\small, line cap=round]
\draw[thick] (0,1.5) -- (4,1.5) node[right] {$\ell$};
\draw[thick] (0,0) -- (4,0) node[right] {$m$};
\draw (0.45,1.58) -- (0.55,1.5) -- (0.45,1.42);
\draw (0.45,0.08) -- (0.55,0) -- (0.45,-0.08);
\draw[thick] (0.95,-0.85) -- (3.05,2.35) node[right] {$t$};
\node at (2.08,1.76) {$1$}; \node at (2.98,1.74) {$2$};
\node at (2.02,1.26) {$3$}; \node at (2.86,1.24) {$4$};
\node at (1.10,0.26) {$5$}; \node at (2.00,0.24) {$6$};
\node at (1.04,-0.24) {$7$}; \node at (1.88,-0.26) {$8$};
\end{tikzpicture}
\end{minipage}\hfill
\begin{minipage}[c]{0.6\linewidth}
When $\ell \parallel m$:
\begin{itemize}
\item \textbf{Corresponding} angles (same position at each crossing) are equal: $\angle 1 = \angle 5$, $\angle 4 = \angle 8$.
\item \textbf{Alternate interior} angles are equal: $\angle 3 = \angle 6$, $\angle 4 = \angle 5$.
\item \textbf{Alternate exterior} angles are equal: $\angle 1 = \angle 8$, $\angle 2 = \angle 7$.
\item \textbf{Same-side interior} angles add up to $180^\circ$: $\angle 3 + \angle 5 = 180^\circ$.
\end{itemize}
\end{minipage}
\end{concept}

\begin{concept}{Angles of a polygon ($n$ = number of sides)}
\begin{itemize}
\item Sum of the interior angles: $(n-2) \times 180^\circ$ \quad (triangle $180^\circ$, quadrilateral $360^\circ$,
  pentagon $540^\circ$, hexagon $720^\circ$, octagon $1{,}080^\circ$).
\item In a \emph{regular} polygon all angles are equal: each interior angle is $\dfrac{(n-2)\times 180^\circ}{n}$.
\item The exterior angles of any polygon add up to $360^\circ$, so each exterior angle of a regular polygon is $360^\circ \div n$.
\end{itemize}
\end{concept}

\begin{example}{Worked example}
Two angles form a straight line. One measures $(2x+10)^\circ$ and the other $(3x-5)^\circ$. What is $x$?

\textbf{Solution.} Angles on a straight line add up to $180^\circ$:
$(2x+10)+(3x-5)=180$, so $5x+5=180$, $5x=175$, and $x=35$.
Check: the angles are $80^\circ$ and $100^\circ$, and $80+100=180$.
\end{example}

\begin{tip}
In a parallel-lines figure there are only \emph{two} angle sizes: every small
(acute) angle is equal to every other small angle, every large (obtuse) angle
is equal to every other large angle, and small $+$ large $=180^\circ$.
\end{tip}

\begin{trap}
\begin{itemize}
\item Mixing up the totals: \textbf{c}omplementary comes before \textbf{s}upplementary, just as $90$ comes before $180$.
\item Treating same-side interior angles as equal. They add up to $180^\circ$.
\item Finding $x$ and stopping when the question asks for the \emph{angle}: plug $x$ back in.
\item Using $n \times 180^\circ$ instead of $(n-2)\times 180^\circ$ for a polygon.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# formatting and drawing helpers (floats only for TikZ coordinates)
# --------------------------------------------------------------------------

def _d(v):
    """Raw LaTeX for an angle: 65 -> 65^\\circ, 52.5 -> 52.5^\\circ."""
    return dec_raw(v) + r"^\circ"


def deg(v):
    """Answer formatter for angle measures."""
    return m(_d(v))


def _lin(p, q):
    """Raw LaTeX for the expression p*x + q (e.g. 2x + 10, 3x - 5, x)."""
    return latex(p * X + q)


def _f(v):
    s = f"{float(v):.2f}"
    return "0.00" if s == "-0.00" else s


def _P(px, py):
    return f"({_f(px)},{_f(py)})"


def _polar(ang, r):
    t = math.radians(float(ang))
    return r * math.cos(t), r * math.sin(t)


def _arc(cx, cy, a0, a1, r=0.3):
    """Arc of radius r around (cx, cy) from direction a0 to a1 (ccw)."""
    sx, sy = _polar(a0, r)
    return (rf"\draw {_P(cx + sx, cy + sy)} arc[start angle={_f(a0)}, "
            rf"end angle={_f(a1)}, radius={_f(r)}];")


def _region_label(cx, cy, a0, a1, tex, base=0.78):
    """Label placed inside the angle a0..a1 (ccw), far enough out to fit."""
    w = math.radians(float(a1 - a0))
    r = 1.3 if w < 0.2 else min(1.3, max(base, 0.36 / math.tan(w / 2)))
    lx, ly = _polar((float(a0) + float(a1)) / 2, r)
    return rf"\node at {_P(cx + lx, cy + ly)} {{{tex}}};"


def _tikz(body):
    return ("\\begin{tikzpicture}[font=\\small, line cap=round, line join=round]\n"
            + body + "\n\\end{tikzpicture}")


def _solve_sum(terms, total):
    """Independent route: sympy solves sum(terms) = total for x."""
    return sp.solve(sp.Eq(sum(terms), total), X)[0]


def _solve_steps(p, c, total):
    """Steps that solve p*x + c = total (p > 0); returns (steps, x)."""
    steps = []
    rhs = total - c
    if c > 0:
        steps.append(f"Subtract {m(int_raw(c))} from both sides: "
                     f"{m(f'{latex(p * X)} = {int_raw(total)} - {int_raw(c)} = {int_raw(rhs)}')}.")
    elif c < 0:
        steps.append(f"Add {m(int_raw(-c))} to both sides: "
                     f"{m(f'{latex(p * X)} = {int_raw(total)} + {int_raw(-c)} = {int_raw(rhs)}')}.")
    xv = Q(rhs) / p
    if p != 1:
        steps.append(f"Divide both sides by {m(int_raw(p))}: "
                     f"{m(f'x = {int_raw(rhs)} \\div {int_raw(p)} = {dec_raw(xv)}')}.")
    return steps, xv


def _near_int(ans, deltas=(5, 10, 15, 20), hi=360, lo=0):
    """Filler distractors: whole numbers a few steps either side of the answer
    (strictly between lo and hi; use lo=2 for numbers of sides)."""
    def f(rng):
        out = [Q(ans) + d for d in deltas] + [Q(ans) - d for d in deltas]
        out = [v for v in out if lo < v < hi]
        rng.shuffle(out)
        return out
    return f


# --------------------------------------------------------------------------
# level 1
# --------------------------------------------------------------------------

@template("MK")
def comp_supp(rng, lvl):
    comp = rng.random() < 0.5
    if comp:
        a = rng.randint(12, 78)
        total, word, adj = 90, "complement", "complementary"
    else:
        a = rng.choice([rng.randint(12, 78), rng.randint(102, 168)])
        total, word, adj = 180, "supplement", "supplementary"
    ans = Q(total - a)
    A, B = rng.choice([("A", "B"), ("P", "Q"), ("1", "2"), ("R", "S")])
    stem = choose(
        rng,
        f"What is the measure of the {word} of a {deg(a)} angle?",
        f"Two angles are {adj}. One of them measures {deg(a)}. What is the measure of the other angle?",
        f"{m(r'\angle ' + A)} and {m(r'\angle ' + B)} are {adj}. If {m(r'\angle ' + A)} measures "
        f"{deg(a)}, what is the measure of {m(r'\angle ' + B)}?",
    )
    if comp:
        wrong = [
            (Q(180 - a), r"finds the supplement (total $180^\circ$) instead of the complement (total $90^\circ$)"),
            (Q(360 - a), r"subtracts from $360^\circ$, the total all the way around a point"),
            (Q(90 + a), r"adds the angle to $90^\circ$ instead of subtracting it"),
        ]
    else:
        wrong = [(Q(360 - a), r"subtracts from $360^\circ$, the total all the way around a point")]
        if a < 90:
            wrong.append((Q(90 - a), r"finds the complement (total $90^\circ$) instead of the supplement (total $180^\circ$)"))
        else:
            wrong.append((Q(a - 90), r"subtracts $90^\circ$ instead of subtracting from $180^\circ$"))
        wrong.append((Q(180 + a), r"adds the angle to $180^\circ$ instead of subtracting it"))
    wrong.append((Q(a), f"repeats the given angle, but {adj} angles are not equal; they add up to {m(_d(total))}"))
    return Problem(
        stem=stem,
        answer=ans,
        fmt=deg,
        near=_near_int(ans, (3, 7, 10, 13, 20)),
        wrong=wrong,
        steps=[
            f"{adj.capitalize()} angles add up to {m(_d(total))}.",
            f"Subtract the angle you know: {m(f'{total}^\\circ - {a}^\\circ = {_d(ans)}')}.",
            f"Check: {m(f'{a}^\\circ + {_d(ans)} = {total}^\\circ')}. \\checkmark",
        ],
        tip=(r"\textbf{C}omplementary comes before \textbf{s}upplementary in the alphabet, "
             r"just as $90$ comes before $180$."),
        check=_solve_sum([X, a], total),
        verify=lambda v: v + a == total,
    )


_KIND_WHY = {
    "acute": r"describes an angle smaller than $90^\circ$",
    "right": r"describes an angle of exactly $90^\circ$",
    "obtuse": r"describes an angle between $90^\circ$ and $180^\circ$",
    "straight": r"describes an angle of exactly $180^\circ$",
    "reflex": r"describes an angle between $180^\circ$ and $360^\circ$",
}
_KIND_RULE = {
    "acute": r"less than $90^\circ$",
    "right": r"exactly $90^\circ$",
    "obtuse": r"between $90^\circ$ and $180^\circ$",
    "straight": r"exactly $180^\circ$",
    "reflex": r"between $180^\circ$ and $360^\circ$",
}


def _classify(a):
    """Angle type from its measure (used as the independent check)."""
    if a < 90:
        return "acute"
    if a == 90:
        return "right"
    if a < 180:
        return "obtuse"
    if a == 180:
        return "straight"
    return "reflex"


def _draw_kind(rng, kind, wide=False):
    lo, hi = {"acute": (25, 80), "obtuse": (100, 165), "reflex": (200, 320),
              "right": (90, 90), "straight": (180, 180)}[kind]
    if wide:                              # text-only questions can use the full range
        lo, hi = {"acute": (5, 88), "obtuse": (92, 178), "reflex": (182, 355)}.get(kind, (lo, hi))
    return rng.randint(lo, hi)


@template("MK")
def angle_vocab(rng, lvl):
    mode = rng.choice(["name"] * 4 + ["figure"] * 2 + ["which", "pair"])
    if mode == "pair":
        pairs = {
            "complementary": (r"Two angles whose measures add up to $90^\circ$ are called", r"describes two angles that add up to $90^\circ$"),
            "supplementary": (r"Two angles whose measures add up to $180^\circ$ are called", r"describes two angles that add up to $180^\circ$"),
            "vertical": (r"When two straight lines cross, the angles directly across from each other are called", r"describes the angles directly across from each other where two lines cross"),
            "adjacent": (r"Two angles that share a vertex and a common side, without overlapping, are called", r"describes angles that share a vertex and a side"),
        }
        key = rng.choice(["complementary", "supplementary", "vertical", "adjacent"])
        lead = pairs[key][0]
        stem = f"{lead} which kind of angles?"
        wrong = [(f"{k} angles", pairs[k][1]) for k in pairs if k != key]
        rng.shuffle(wrong)
        rule = {"complementary": r"Complementary angles add up to $90^\circ$.",
                "supplementary": r"Supplementary angles add up to $180^\circ$.",
                "vertical": r"Vertical angles are the pairs of opposite angles formed where two lines cross; they are always equal.",
                "adjacent": r"Adjacent angles are next to each other: they share a vertex and one side."}[key]
        return Problem(
            stem=stem,
            answer=f"{key} angles",
            fmt=text,
            wrong=wrong,
            steps=[rule, f"So the answer is \\emph{{{key} angles}}."],
            tip=r"\textbf{C}omplementary ($90^\circ$) comes before \textbf{s}upplementary ($180^\circ$), like the letters C and S.",
            check=f"{key} angles",
        )
    if mode == "which":
        kind = rng.choice(["acute", "obtuse", "reflex"])
        a = _draw_kind(rng, kind)
        others = [k for k in _KIND_WHY if k != kind]
        wrong = []
        for k in others:
            v = _draw_kind(rng, k)
            wrong.append((Q(v), f"is {('an ' if k[0] in 'aeiou' else 'a ')}{k} angle ({_KIND_RULE[k]})"))
        art = "an" if kind[0] in "aeiou" else "a"
        return Problem(
            stem=choose(rng,
                        f"Which of the following is the measure of {art} {kind} angle?",
                        f"Which angle measure below describes {art} {kind} angle?"),
            answer=Q(a),
            fmt=deg,
            wrong=wrong,
            steps=[
                f"{art.capitalize()} {kind} angle measures {_KIND_RULE[kind]}.",
                f"Only {deg(a)} is {_KIND_RULE[kind]}.",
            ],
            check=Q(a),
            verify=lambda v: _classify(v) == kind,
            near=lambda r: [],
        )
    kind = rng.choice(["acute", "acute", "obtuse", "obtuse", "reflex", "reflex", "right", "straight"])
    a = _draw_kind(rng, kind, wide=(mode == "name"))
    wrong = [(k, _KIND_WHY[k]) for k in _KIND_WHY if k != kind]
    rng.shuffle(wrong)
    fig = None
    if mode == "figure":
        rot = rng.choice([0, 0, 10, 20, -10])
        L = 1.7
        x1, y1 = _polar(rot, L)
        x2, y2 = _polar(rot + a, L)
        body = [rf"\draw[thick] {_P(x1, y1)} -- (0,0) -- {_P(x2, y2)};",
                r"\fill (0,0) circle (1.2pt);"]
        if a == 90:
            ux, uy = _polar(rot, 0.25)
            vx, vy = _polar(rot + 90, 0.25)
            body.append(rf"\draw {_P(ux, uy)} -- {_P(ux + vx, uy + vy)} -- {_P(vx, vy)};")
        else:
            body.append(_arc(0, 0, rot, rot + a, 0.35))
        body.append(_region_label(0, 0, rot, rot + a, m(_d(a)), base=0.75))
        fig = _tikz("\n".join(body))
        stem = choose(rng,
                      f"The angle shown measures {deg(a)}. Which term describes it?",
                      f"What kind of angle is shown in the figure, which measures {deg(a)}?")
    else:
        stem = choose(rng,
                      f"Which term describes an angle that measures {deg(a)}?",
                      f"An angle measures {deg(a)}. What kind of angle is it?",
                      f"What type of angle has a measure of {deg(a)}?")
    return Problem(
        stem=stem,
        answer=kind,
        fmt=text,
        wrong=wrong,
        steps=[
            r"Compare with the benchmarks: acute is less than $90^\circ$, right is exactly $90^\circ$, "
            r"obtuse is between $90^\circ$ and $180^\circ$, straight is exactly $180^\circ$, "
            r"and reflex is between $180^\circ$ and $360^\circ$.",
            f"{deg(a)} is {_KIND_RULE[kind]}, so the angle is \\emph{{{kind}}}.",
        ],
        figure=fig,
        check=_classify(a),
    )


@template("MK")
def vertical_adjacent(rng, lvl):
    a = rng.choice([v for v in range(35, 146) if abs(v - 90) >= 10])
    regions = [(0, a), (a, 180), (180, 180 + a), (180 + a, 360)]
    meas = [Q(a), Q(180 - a), Q(a), Q(180 - a)]       # read off the drawing
    i = rng.randrange(4)
    j = rng.choice([k for k in range(4) if k != i])
    g = meas[i]
    vert = (j - i) % 2 == 0
    ans = g if vert else 180 - g
    rot = rng.choice([0, 0, 10, -10, 20])
    L = 1.9
    body = []
    for d in (rot, rot + a):
        x1, y1 = _polar(d, L)
        body.append(rf"\draw[thick] {_P(-x1, -y1)} -- {_P(x1, y1)};")
    for k, tex in ((i, m(_d(g))), (j, r"$x^\circ$")):
        s, e = regions[k]
        body.append(_arc(0, 0, rot + s, rot + e, 0.25))
        body.append(_region_label(0, 0, rot + s, rot + e, tex))
    stem = choose(rng,
                  f"In the figure, two straight lines intersect, forming the {deg(g)} angle shown. What is the value of {m('x')}?",
                  f"Two straight lines cross as shown. One angle measures {deg(g)}. What is the value of {m('x')}?",
                  f"Two lines cross, and one of the four angles they form measures {deg(g)}, as shown. Find {m('x')}.",
                  f"The figure shows two intersecting straight lines and a {deg(g)} angle. What is the value of {m('x')}?")
    if vert:
        wrong = [(180 - g, r"assumes the two angles add up to $180^\circ$, but vertical angles are equal"),
                 (360 - g, r"assumes the two angles add up to $360^\circ$, but vertical angles are equal")]
        if g < 90:
            wrong.append((90 - g, r"assumes the two angles add up to $90^\circ$, but vertical angles are equal"))
        steps = [
            f"The {m('x^\\circ')} angle is directly across from the {deg(g)} angle where the lines cross, "
            "so the two are \\emph{vertical angles}.",
            f"Vertical angles are equal, so {m(f'x = {int_raw(ans)}')}.",
        ]
    else:
        wrong = [(g, r"treats the angles as vertical angles, but these two angles together form a straight line"),
                 (360 - g, r"assumes the two angles add up to $360^\circ$ instead of $180^\circ$")]
        if g < 90:
            wrong.append((90 - g, r"assumes the two angles add up to $90^\circ$ instead of $180^\circ$"))
        steps = [
            f"The {m('x^\\circ')} angle and the {deg(g)} angle sit side by side along one straight line, "
            f"so together they make {m('180^\\circ')}.",
            f"{m(f'x + {int_raw(g)} = 180')}, so {m(f'x = 180 - {int_raw(g)} = {int_raw(ans)}')}.",
        ]
    return Problem(
        stem=stem,
        answer=ans,
        fmt=num,
        wrong=wrong,
        steps=steps,
        figure=_tikz("\n".join(body)),
        near=_near_int(ans),
        check=meas[j],
    )


# --------------------------------------------------------------------------
# level 2
# --------------------------------------------------------------------------

def _label_width(tex):
    """Rough printed width (cm) of a small label such as $(2x + 10)^\\circ$."""
    core = re.sub(r"\\circ", "o", tex)
    core = re.sub(r"[$\\{}^ ]", "", core)
    return 0.19 * len(core) + 0.15


def _line_label(xc, yc, ray, side, tex, h=0.42):
    """Label sitting on a horizontal line at (xc, yc), inside the angle
    between the line and a line/ray through (xc, yc) at direction ``ray``.
    side: 'AR', 'AL', 'BL', 'BR' (above/below the line, right/left of the
    crossing).  Returns (tikz, xmin, xmax) so callers can size the figure."""
    t = math.radians(float(ray))
    cot = math.cos(t) / math.sin(t)
    lean = cot if side in ("AR", "BL") else -cot     # > 0: the ray leans over this label
    dx = max(0.36, h * lean + 0.12) if lean > 0 else 0.36
    w = _label_width(tex)
    if side == "AR":
        anchor, px, py, lo, hi = "south west", xc + dx, yc + 0.03, xc + dx, xc + dx + w
    elif side == "AL":
        anchor, px, py, lo, hi = "south east", xc - dx, yc + 0.03, xc - dx - w, xc - dx
    elif side == "BL":
        anchor, px, py, lo, hi = "north east", xc - dx, yc - 0.03, xc - dx - w, xc - dx
    else:
        anchor, px, py, lo, hi = "north west", xc + dx, yc - 0.03, xc + dx, xc + dx + w
    return rf"\node[anchor={anchor}, inner sep=1pt] at {_P(px, py)} {{{tex}}};", lo, hi


def _ae(p, q):
    """Raw LaTeX for an angle written as an expression: (2x + 10)^\\circ, 3x^\\circ."""
    return f"({_lin(p, q)})^\\circ" if q != 0 else f"{_lin(p, q)}^\\circ"


def _aem(p, q):
    """Inline math for an angle expression; the braces stop line breaks inside it."""
    return m("{" + _ae(p, q) + "}")


def _cross_fig(v, labels, ray_only=False):
    """A horizontal line crossed at the origin by a line (or, with
    ray_only, a single ray) at direction v.  labels: {side: tex}."""
    parts, lo, hi = [], -1.2, 1.2
    regions = {"AR": (0, v), "AL": (v, 180), "BL": (180, 180 + v), "BR": (180 + v, 360)}
    for i, (side, tex) in enumerate(labels.items()):
        code, a, b = _line_label(0, 0, v, side, tex)
        parts.append(_arc(0, 0, *regions[side], 0.25 if i == 0 else 0.32))
        parts.append(code)
        lo, hi = min(lo, a), max(hi, b)
    L = max(-lo, hi) + 0.25
    x1, y1 = _polar(v, 1.9)
    body = [rf"\draw[thick] ({_f(-L)},0) -- ({_f(L)},0);"]
    if ray_only:
        body += [rf"\draw[thick] (0,0) -- {_P(x1, y1)};", r"\fill (0,0) circle (1.2pt);"]
    else:
        body.append(rf"\draw[thick] {_P(-x1, -y1)} -- {_P(x1, y1)};")
    return _tikz("\n".join(body + parts))


@template("MK")
def angle_algebra(rng, lvl):
    rel = rng.choice(["vertical", "linear", "linear", "comp", "supp"])
    x0 = rng.randint(6, 35)
    p, r = rng.sample(range(1, 7), 2)
    if rel == "vertical":
        v1 = rng.choice([v for v in range(40, 141) if abs(v - 90) >= 12])
        v2, total = v1, None
    elif rel in ("linear", "supp"):
        v1 = rng.choice([v for v in range(40, 141) if abs(v - 90) >= 12])
        v2, total = 180 - v1, 180
    else:
        v1 = rng.randint(20, 70)
        v2, total = 90 - v1, 90
    q, s = v1 - p * x0, v2 - r * x0
    need(-40 <= q <= 60 and -40 <= s <= 60 and (q != 0 or s != 0))
    need(q % 5 == 0 or s % 5 == 0 or rng.random() < 0.4)
    e1, e2 = p * X + q, r * X + s
    E1, E2 = _lin(p, q), _lin(r, s)
    eq = sp.Eq(e1, e2) if total is None else sp.Eq(e1 + e2, total)
    x_solved = sp.solve(eq, X)[0]          # independent route (sympy)

    # ---------------- figure and setup sentence ----------------
    fig = None
    lab1, lab2 = f"${_ae(p, q)}$", f"${_ae(r, s)}$"
    A1, A2 = _aem(p, q), _aem(r, s)
    names = {}
    if rel == "vertical":
        fig = _cross_fig(v1, {"AR": lab1, "BL": lab2})
        setup = (f"In the figure, two straight lines intersect. The vertical angles shown measure "
                 f"{A1} and {A2}.")
    elif rel == "linear":
        fig = _cross_fig(v1, {"AR": lab1, "AL": lab2}, ray_only=True)
        setup = f"In the figure, a ray meets a straight line, forming angles of {A1} and {A2}."
    else:
        A, B = rng.choice([("A", "B"), ("P", "Q"), ("1", "2"), ("J", "K")])
        names = {E1: A, E2: B}
        word = "complementary" if rel == "comp" else "supplementary"
        setup = (f"{m(r'\angle ' + A)} and {m(r'\angle ' + B)} are {word}. "
                 f"{m(r'\angle ' + A)} measures {A1}, and {m(r'\angle ' + B)} measures {A2}.")

    # ---------------- solve for x ----------------
    lead = {"vertical": "Vertical angles are equal",
            "linear": "Angles that form a straight line add up to",
            "supp": "Supplementary angles add up to",
            "comp": "Complementary angles add up to"}[rel]
    steps, xv, wrong_x = _pair_steps(p, q, r, s, total, lead)
    need(xv == x0)

    if lvl <= 2:
        stem = setup + f" What is the value of {m('x')}?"
        ans = Q(x0)
        wrong = wrong_x + [(Q(v1), r"is the measure of an angle, not the value of $x$")]
        fmt = num
        check = x_solved
        verify = ((lambda v: e1.subs(X, v) == e2.subs(X, v)) if total is None
                  else (lambda v: (e1 + e2).subs(X, v) == total))
        tip = f"Check: with {m(f'x = {x0}')} the angles are {deg(v1)} and {deg(v2)}" + (
            "; they are equal." if total is None else f", and {m(f'{v1} + {v2} = {total}')}.")
    else:
        which, target = rng.choice([(E1, e1), (E2, e2)])
        if rel == "vertical":
            ask = "What is the measure of each of these angles?"
        elif rel == "linear":
            ask = f"What is the measure of the {A1 if which == E1 else A2} angle?"
        else:
            ask = f"What is the measure of {m(r'\angle ' + names[which])}?"
        stem = setup + " " + ask
        ans = target.subs(X, x0)
        other_ang = (e2 if target is e1 else e1).subs(X, x0)
        wrong = [(Q(x0), r"stops at the value of $x$ instead of finding the angle")]
        if other_ang != ans:
            wrong.append((other_ang, "is the measure of the other angle"))
        else:
            wrong.append((180 - ans, "is the supplement of the angle, not the angle itself"))
        wv, why = wrong_x[0]
        if wv.is_integer and wv > 0 and target.subs(X, wv) > 0:
            wrong.append((target.subs(X, wv), why))
        steps.append(f"Plug {m(f'x = {x0}')} into {m(latex(target))}: {m(_plug(target, x0))}, "
                     f"so the angle measures {deg(ans)}.")
        fmt = deg
        check = target.subs(X, x_solved)
        verify = None
        tip = None
    return Problem(
        stem=stem,
        answer=ans,
        fmt=fmt,
        wrong=wrong,
        steps=steps,
        figure=fig,
        tip=tip,
        near=_near_int(ans, (1, 2, 3, 5) if fmt is num else (5, 10, 15, 20), hi=100 if fmt is num else 180),
        check=check,
        verify=verify,
    )


def _plug(e, xv):
    """'2(35) + 10 = 80' for e = 2x + 10 at x = 35."""
    p = e.coeff(X)
    c = e - p * X
    head = f"{int_raw(p)}({xv})" if p != 1 else f"{xv}"
    if c > 0:
        head += f" + {int_raw(c)}"
    elif c < 0:
        head += f" - {int_raw(-c)}"
    return f"{head} = {int_raw(e.subs(X, xv))}"


def _pair_steps(p, q, r, s, total, lead):
    """Solve (p x + q) = (r x + s) when ``total`` is None, else
    (p x + q) + (r x + s) = total.  ``lead`` names the fact used.
    Returns (steps, x, wrong_x) where wrong_x are x-values from real mistakes."""
    steps = []
    if total is None:
        (pb, qb), (ps, qs) = ((p, q), (r, s)) if p > r else ((r, s), (p, q))
        steps.append(f"{lead}, so set the expressions equal: "
                     f"{m(f'{_lin(pb, qb)} = {_lin(ps, qs)}')}.")
        steps.append(f"Subtract {m(latex(ps * X))} from both sides: "
                     f"{m(f'{_lin(pb - ps, qb)} = {int_raw(qs)}')}.")
        more, xv = _solve_steps(pb - ps, qb, qs)
        wrong_x = [(Q(180 - q - s) / (p + r), r"assumes the two angles add up to $180^\circ$, but these angles are equal"),
                   (Q(qs + qb) / (pb - ps), "makes a sign error when moving the constant term")]
    else:
        steps.append(f"{lead} {m(_d(total))}: {m(f'({_lin(p, q)}) + ({_lin(r, s)}) = {total}')}.")
        steps.append(f"Combine like terms: {m(f'{_lin(p + r, q + s)} = {total}')}.")
        more, xv = _solve_steps(p + r, q + s, total)
        other = 90 if total == 180 else 180
        wrong_x = [(Q(s - q) / (p - r), "sets the two angles equal instead of adding them"),
                   (Q(other - q - s) / (p + r), f"uses {m(_d(other))} instead of {m(_d(total))}"),
                   (Q(total + q + s) / (p + r), "makes a sign error when moving the constant term")]
    return steps + more, xv, wrong_x


# ---- parallel lines cut by a transversal --------------------------------
# Positions at each crossing: A/B = above/below the parallel line, R/L =
# right/left of the transversal.  "U" = upper line l, "L" = lower line m.
# Canonical drawing: the transversal rises to the right, so AR and BL are
# the acute angles.
_PACUTE = {"AR", "BL"}
_PRELS = {
    "corresponding": [(("U", p), ("L", p)) for p in ("AR", "AL", "BL", "BR")],
    "alternate interior": [(("U", "BL"), ("L", "AR")), (("U", "BR"), ("L", "AL"))],
    "alternate exterior": [(("U", "AL"), ("L", "BR")), (("U", "AR"), ("L", "BL"))],
    "same-side interior": [(("U", "BL"), ("L", "AL")), (("U", "BR"), ("L", "AR"))],
}
_PEQUAL = {"corresponding": True, "alternate interior": True,
           "alternate exterior": True, "same-side interior": False}
_PWHERE = {
    "corresponding": "they sit in the same position at the two crossings",
    "alternate interior": "they are between the parallel lines, on opposite sides of the transversal",
    "alternate exterior": "they are outside the parallel lines, on opposite sides of the transversal",
    "same-side interior": "they are between the parallel lines, on the same side of the transversal",
}
_MIRROR = {"AR": "AL", "AL": "AR", "BL": "BR", "BR": "BL"}


_LINE_NAMES = [(r"\ell", "m", "t"), ("p", "q", "t"), ("j", "k", "n"), ("m", "n", "s"), ("a", "b", "c")]


def _parallel_fig(phi, labels, mirror, names=_LINE_NAMES[0]):
    """Two horizontal parallel lines cut by a transversal making the acute
    angle ``phi`` with them.  labels: {(line, canonical position): tex}.
    The lines are made just long enough to carry the labels."""
    H = 1.6
    psi = 180 - phi if mirror else phi          # direction of the transversal as drawn
    t = math.radians(psi)
    cot = math.cos(t) / math.sin(t)
    xl, xu = 0.0, H * cot
    ex, ey = 0.9 * math.cos(t), 0.9 * math.sin(t)
    regions = {"AR": (0, psi), "AL": (psi, 180), "BL": (180, 180 + psi), "BR": (180 + psi, 360)}
    parts, lo, hi = [], min(xl, xu) - 1.0, max(xl, xu) + 1.0
    for (line, pos), tex in labels.items():
        vis = _MIRROR[pos] if mirror else pos
        xc, yc = (xu, H) if line == "U" else (xl, 0.0)
        code, a, b = _line_label(xc, yc, psi, vis, tex)
        parts.append(_arc(xc, yc, *regions[vis], 0.25))
        parts.append(code)
        lo, hi = min(lo, a), max(hi, b)
    lo, hi = lo - 0.5, hi + 0.25
    body = [rf"\draw[thick] ({_f(lo)},{H}) -- ({_f(hi)},{H}) node[right] {{${names[0]}$}};",
            rf"\draw[thick] ({_f(lo)},0) -- ({_f(hi)},0) node[right] {{${names[1]}$}};",
            rf"\draw {_P(lo + 0.15, H + 0.08)} -- {_P(lo + 0.25, H)} -- {_P(lo + 0.15, H - 0.08)};",
            rf"\draw {_P(lo + 0.15, 0.08)} -- {_P(lo + 0.25, 0)} -- {_P(lo + 0.15, -0.08)};",
            rf"\draw[thick] {_P(xl - ex, -ey)} -- {_P(xu + ex, H + ey)} "
            rf"node[{'right' if psi < 90 else 'left'}] {{${names[2]}$}};"]
    return _tikz("\n".join(body + parts))


@template("MK")
def parallel_lines(rng, lvl):
    phi = rng.randint(40, 75)
    rel = rng.choice(list(_PRELS))
    pair = rng.choice(_PRELS[rel])
    if rng.random() < 0.5:
        pair = (pair[1], pair[0])
    (gl, gp), (tl, tp) = pair
    mirror = rng.random() < 0.5

    def drawn(pos):                      # angle as drawn (geometry, not the rule)
        return Q(phi) if pos in _PACUTE else Q(180 - phi)

    g, tgt = drawn(gp), drawn(tp)
    equal = _PEQUAL[rel]
    name = rel
    names = rng.choice(_LINE_NAMES)
    L1, L2, T = (m(v) for v in names)
    if lvl <= 2:
        ans = g if equal else 180 - g
        fig = _parallel_fig(phi, {(gl, gp): m(_d(g)), (tl, tp): r"$x^\circ$"}, mirror, names)
        stem = choose(
            rng,
            f"In the figure, lines {L1} and {L2} are parallel, and one angle formed by "
            f"transversal {T} measures {deg(g)}. What is the value of {m('x')}?",
            f"Parallel lines {L1} and {L2} are cut by transversal {T}, forming the "
            f"{deg(g)} angle shown. What is the value of {m('x')}?",
            f"In the figure, {m(names[0] + r' \parallel ' + names[1])}, and one of the angles measures {deg(g)}. "
            f"What is the value of {m('x')}?",
            f"Line {T} crosses parallel lines {L1} and {L2}, making the {deg(g)} angle shown. Find {m('x')}.")
        if equal:
            wrong = [(180 - g, f"assumes the two angles add up to {m('180^\\circ')}, but {name} angles are equal")]
            if g < 90:
                wrong.append((90 - g, r"assumes the two angles add up to $90^\circ$; they are equal"))
            else:
                wrong.append((g - 90, r"subtracts $90^\circ$ from the given angle; the two angles are equal"))
            wrong.append((360 - g, r"assumes the two angles add up to $360^\circ$; they are equal"))
            steps = [f"The {deg(g)} angle and the {m('x^\\circ')} angle are \\emph{{{name}}} angles: {_PWHERE[rel]}.",
                     f"When the lines are parallel, {name} angles are equal, so {m(f'x = {int_raw(ans)}')}."]
        else:
            wrong = [(g, "treats the angles as equal, but same-side interior angles add up to $180^\\circ$"),
                     (360 - g, r"assumes the two angles add up to $360^\circ$ instead of $180^\circ$")]
            if g < 90:
                wrong.append((90 - g, r"assumes the two angles add up to $90^\circ$ instead of $180^\circ$"))
            steps = [f"The {deg(g)} angle and the {m('x^\\circ')} angle are \\emph{{same-side interior}} angles: {_PWHERE[rel]}.",
                     f"Same-side interior angles add up to {m('180^\\circ')}: "
                     f"{m(f'x = 180 - {int_raw(g)} = {int_raw(ans)}')}."]
        small, large = min(g, 180 - g), max(g, 180 - g)
        tip = (f"Every acute angle in this figure is {deg(small)} and every obtuse angle is {deg(large)}. "
               f"The {m('x^\\circ')} angle is {'acute' if tgt < 90 else 'obtuse'}, so {m(f'x = {int_raw(ans)}')}.")
        return Problem(stem=stem, answer=ans, fmt=num, wrong=wrong, steps=steps,
                       tip=tip, figure=fig, near=_near_int(ans), check=tgt)

    # level 3: algebraic labels (long labels need a steeper transversal)
    need(phi >= 50)
    x0 = rng.randint(6, 30)
    p, r = rng.sample(range(1, 7), 2)
    q, s = g - p * x0, tgt - r * x0
    need(-40 <= q <= 60 and -40 <= s <= 60 and (q != 0 or s != 0))
    need(q % 5 == 0 or s % 5 == 0 or rng.random() < 0.4)
    e1, e2 = p * X + q, r * X + s
    E1, E2 = _lin(p, q), _lin(r, s)
    fig = _parallel_fig(phi, {(gl, gp): f"${_ae(p, q)}$", (tl, tp): f"${_ae(r, s)}$"}, mirror, names)
    total = None if equal else 180
    lead = (f"These are {name} angles ({_PWHERE[rel]}). {name.capitalize()} angles are equal"
            if equal else
            f"These are same-side interior angles ({_PWHERE[rel]}). Same-side interior angles add up to")
    steps, xv, wrong_x = _pair_steps(p, q, r, s, total, lead)
    need(xv == x0)
    eq = sp.Eq(e1, e2) if equal else sp.Eq(e1 + e2, 180)
    x_solved = sp.solve(eq, X)[0]
    setup = (f"In the figure, lines {L1} and {L2} are parallel. The marked angles measure "
             f"{_aem(p, q)} and {_aem(r, s)}.")
    if rng.random() < 0.5:
        stem = setup + f" What is the value of {m('x')}?"
        return Problem(stem=stem, answer=Q(x0), fmt=num,
                       wrong=wrong_x + [(g, r"is the measure of an angle, not the value of $x$")],
                       steps=steps, figure=fig, check=x_solved, near=_near_int(x0, (1, 2, 3, 5), hi=100),
                       verify=lambda v: (e1.subs(X, v) == e2.subs(X, v)) if equal
                       else (e1 + e2).subs(X, v) == 180)
    which, target = rng.choice([(E1, e1), (E2, e2)])
    ans = target.subs(X, x0)
    other_ang = (e2 if target is e1 else e1).subs(X, x0)
    wrong = [(Q(x0), r"stops at the value of $x$ instead of finding the angle")]
    if other_ang != ans:
        wrong.append((other_ang, "is the measure of the other marked angle"))
    else:
        wrong.append((180 - ans, "is the supplement of the angle, not the angle itself"))
    wv, why = wrong_x[0]
    if wv.is_integer and wv > 0 and target.subs(X, wv) > 0:
        wrong.append((target.subs(X, wv), why))
    steps.append(f"Plug {m(f'x = {x0}')} into {m(latex(target))}: {m(_plug(target, x0))}, "
                 f"so the angle measures {deg(ans)}.")
    return Problem(stem=setup + f" What is the measure of the {_aem(p, q) if which == E1 else _aem(r, s)} angle?",
                   answer=ans, fmt=deg, wrong=wrong, steps=steps, figure=fig,
                   near=_near_int(ans), check=target.subs(X, x_solved))


@template("MK")
def around_point(rng, lvl):
    mode = rng.choice(["line", "line", "point", "ratio_line", "ratio_point"])
    if mode in ("line", "point"):
        k = 3 if mode == "line" else 4
        total = 180 if mode == "line" else 360
        lo, hi = (35, 100) if mode == "line" else (55, 130)
        given = [rng.randint(lo, hi) for _ in range(k - 1)]
        xv = total - sum(given)
        need(lo <= xv <= hi + 20 and len(set(given + [xv])) == k)
        meas = given + [xv]
        idx = rng.randrange(k)
        meas[idx], meas[-1] = meas[-1], meas[idx]          # put x somewhere random
        labels = [m(_d(v)) if i != idx else r"$x^\circ$" for i, v in enumerate(meas)]
        gtxt = ", ".join(deg(v) for v in given[:-1]) + f"{',' if k > 3 else ''} and {deg(given[-1])}"
        if mode == "line":
            stem = (f"In the figure, three angles share a vertex on a straight line. Two of them measure "
                    f"{gtxt}. What is the value of {m('x')}?")
            wrong = [(Q(360 - sum(given)), r"uses $360^\circ$ instead of $180^\circ$"),
                     (Q(sum(given)), "adds the two given angles and stops"),
                     (Q(180 - given[0]), "subtracts only one of the given angles")]
            fact = r"Angles that together form a straight line add up to $180^\circ$"
        else:
            stem = (f"Four angles meet at a point, as shown. Three of them measure {gtxt}. "
                    f"What is the value of {m('x')}?")
            wrong = [(Q(sum(given)), "adds the three given angles and stops"),
                     (Q(360 - sum(given[:2])), "leaves out one of the given angles"),
                     (Q(180 - sum(given[:2])), r"uses $180^\circ$ and leaves out one angle")]
            fact = r"Angles all the way around a point add up to $360^\circ$"
        plus = " + ".join(str(v) for v in given)
        steps = [f"{fact}: {m(plus + ' + x = ' + str(total))}.",
                 f"Add the known angles: {m(f'{plus} = {sum(given)}')}.",
                 f"Subtract: {m(f'x = {total} - {sum(given)} = {xv}')}."]
        ans, check = Q(xv), _solve_sum(given + [X], total)
    else:
        if mode == "ratio_line":
            ks = list(rng.choice([(1, 2, 3), (1, 1, 2), (2, 3, 4), (2, 3, 5), (3, 4, 5), (2, 2, 5), (1, 2, 2)]))
            total = 180
        else:
            ks = list(rng.choice([(1, 2, 3, 4), (1, 1, 2, 2), (2, 3, 3, 4), (1, 2, 2, 3), (2, 3, 4, 6),
                                  (3, 4, 5, 6), (1, 2, 4, 5)]))
            total = 360
        rng.shuffle(ks)
        K = sum(ks)
        xv = Q(total) / K
        need(xv.is_integer)
        meas = [kk * xv for kk in ks]
        labels = [f"${latex(kk * X)}^\\circ$" for kk in ks]
        terms = " + ".join(latex(kk * X) for kk in ks)
        n_ang = len(ks)
        if mode == "ratio_line":
            stem = (f"In the figure, angles measuring {', '.join(m(latex(kk * X) + '^\\circ') for kk in ks[:-1])}, "
                    f"and {m(latex(ks[-1] * X) + '^\\circ')} together form a straight line. What is the value of {m('x')}?")
            fact = r"The angles form a straight line, so they add up to $180^\circ$"
            wrong = [(Q(360) / K, r"uses $360^\circ$ instead of $180^\circ$"),
                     (Q(180) / n_ang, r"divides $180^\circ$ by the number of angles, as if they were all equal")]
        else:
            stem = (f"In the figure, four angles meet at a point and measure "
                    f"{', '.join(m(latex(kk * X) + '^\\circ') for kk in ks[:-1])}, and "
                    f"{m(latex(ks[-1] * X) + '^\\circ')}. What is the value of {m('x')}?")
            fact = r"The angles go all the way around a point, so they add up to $360^\circ$"
            wrong = [(Q(180) / K, r"uses $180^\circ$ instead of $360^\circ$"),
                     (Q(90), r"divides $360^\circ$ by the number of angles, as if they were all equal")]
        wrong.append((max(ks) * xv, r"gives the largest angle instead of the value of $x$"))
        steps = [f"{fact}: {m(f'{terms} = {total}')}.",
                 f"Combine like terms: {m(f'{latex(K * X)} = {total}')}.",
                 f"Divide both sides by {m(K)}: {m(f'x = {total} \\div {K} = {int_raw(xv)}')}."]
        ans, check = xv, sp.solve(sp.Eq(sum(kk * X for kk in ks), total), X)[0]
        idx = None
    # ---- figure: rays from O, regions drawn to the true angle sizes ----
    body = []
    if mode in ("line", "ratio_line"):
        body.append(r"\draw[thick] (-2.1,0) -- (2.1,0);")
        start = 0
    else:
        start = rng.choice([0, 15, 30, 45])
    cur = start
    edges = []
    for v in meas:
        edges.append((cur, cur + v))
        cur += v
    rays = [e[1] for e in edges[:-1]] if mode in ("line", "ratio_line") else [e[0] for e in edges]
    for d in rays:
        ex_, ey_ = _polar(d, 1.75)
        body.append(rf"\draw[thick] (0,0) -- {_P(ex_, ey_)};")
    body.append(r"\fill (0,0) circle (1.2pt);")
    for i, ((a0, a1), tex) in enumerate(zip(edges, labels)):
        body.append(_arc(0, 0, a0, a1, 0.25 if i % 2 == 0 else 0.32))
        body.append(_region_label(0, 0, a0, a1, tex, base=0.88))
    return Problem(stem=stem, answer=ans, fmt=num, wrong=wrong, steps=steps,
                   figure=_tikz("\n".join(body)), near=_near_int(ans), check=check)


_POLY = {5: "pentagon", 6: "hexagon", 7: "heptagon (7 sides)", 8: "octagon",
         9: "nonagon (9 sides)", 10: "decagon (10 sides)"}


def _pname(n):
    return _POLY.get(n, f"{n}-sided polygon")


def _a(word):
    return ("an " if word[0] in "aeiou" else "a ") + word


_SUM_OBJECTS = {
    5: ["Home plate on a baseball field", "The outline of the Pentagon building", "A school crossing sign"],
    6: ["A hex nut", "A honeycomb cell", "A floor tile"],
    8: ["A stop sign", "A boxing ring", "A gazebo floor"],
}


@template("MK")
def polygon_sum(rng, lvl):
    mode = rng.choice(["sum", "sum", "sides", "algebra", "algebra"])
    if mode == "sum":
        n = rng.randint(5, 20)
        name = _pname(n)
        total = (n - 2) * 180
        stems = [f"What is the sum of the measures of the interior angles of {_a(name)}?",
                 f"The interior angles of {_a(name)} add up to how many degrees?",
                 f"Find the sum of the interior angles of a polygon with {n} sides."]
        if n in _SUM_OBJECTS:
            obj = rng.choice(_SUM_OBJECTS[n])
            stems += [f"{obj} has the shape of {_a(name)}. What is the sum of its interior angles?"] * 2
        wrong = [(Q(n * 180), r"multiplies by the number of sides instead of $n-2$"),
                 (Q((n - 1) * 180), r"uses $n-1$ instead of $n-2$"),
                 (Q(360), r"gives the sum of the exterior angles, which is always $360^\circ$"),
                 (Q(total) / n, "gives one angle of a regular polygon, not the sum of all the angles")]
        return Problem(
            stem=rng.choice(stems),
            answer=Q(total),
            fmt=deg,
            wrong=wrong,
            steps=[f"The polygon has {m(f'n = {n}')} sides. "
                   r"Use: sum of interior angles $= (n-2) \times 180^\circ$.",
                   f"{m(f'({n} - 2) \\times 180^\\circ = {n - 2} \\times 180^\\circ = {_d(total)}')}."],
            tip=(f"Why it works: diagonals from one corner cut the polygon into {m(f'{n} - 2 = {n - 2}')} "
                 r"triangles, and each triangle holds $180^\circ$."),
            check=Q(n * 180 - 360),          # n straight angles at the vertices minus the 360 of exterior angles
        )
    if mode == "sides":
        n = rng.randint(5, 20)
        total = (n - 2) * 180
        stem = choose(rng,
                      f"The interior angles of a polygon add up to {deg(total)}. How many sides does the polygon have?",
                      f"A polygon's interior angles have a sum of {deg(total)}. How many sides does it have?",
                      f"How many sides does a polygon have if the sum of its interior angles is {deg(total)}?")
        brute = next(k for k in range(3, 100) if (k - 2) * 180 == total)
        return Problem(
            stem=stem,
            answer=Q(n),
            fmt=num,
            wrong=[(Q(n - 2), r"finds $n-2$ and forgets to add the $2$ back"),
                   (Q(n - 1), r"adds $1$ instead of $2$")]
                  + ([(Q(total) / 360, r"divides by $360^\circ$ instead of $180^\circ$, then stops")]
                     if Q(total) / 360 >= 3 else []),
            steps=[f"Set up the angle-sum formula: {m(f'(n-2) \\times 180 = {int_raw(total)}')}.",
                   f"Divide both sides by 180: {m(f'n - 2 = {int_raw(total)} \\div 180 = {n - 2}')}.",
                   f"Add 2: {m(f'n = {n - 2} + 2 = {n}')}."],
            near=_near_int(n, (1, 2, 3, 4), hi=100, lo=2),
            check=Q(brute),
        )
    # algebra: the four angles of a quadrilateral are given as expressions in x
    for _ in range(200):                     # search locally: the angle sum must come out exactly
        x0 = rng.randint(10, 40)
        coefs = [rng.choice([1, 1, 2, 2, 3]) for _ in range(4)]
        consts = [rng.choice([0, 0, 10, 20, 30, -10, -20, 15, 25, -15]) for _ in range(3)]
        vals = [p * x0 + c for p, c in zip(coefs, consts)]
        last = 360 - sum(vals)
        c4 = last - coefs[3] * x0
        if (all(45 <= v <= 160 for v in vals + [last]) and abs(c4) <= 40 and c4 % 5 == 0
                and len(set(zip(coefs, consts + [c4]))) == 4):
            break
    else:
        need(False)
    consts.append(c4)
    vals.append(last)
    exprs = [p * X + c for p, c in zip(coefs, consts)]
    K, C = sum(coefs), sum(consts)
    terms = ", ".join(_aem(pp, cc) for pp, cc in zip(coefs[:-1], consts[:-1]))
    terms += f", and {_aem(coefs[-1], c4)}"
    stem = choose(rng,
                  f"The four angles of a quadrilateral measure {terms}. What is the value of {m('x')}?",
                  f"A quadrilateral has angles of {terms}. What is the value of {m('x')}?")
    steps = [r"The angles of a quadrilateral add up to $(4-2) \times 180^\circ = 360^\circ$.",
             f"Add the expressions and combine like terms: {m(f'{latex(K * X + C)} = 360')}."]
    more, xv = _solve_steps(K, C, 360)
    steps += more
    need(xv == x0)
    return Problem(
        stem=stem,
        answer=Q(x0),
        fmt=num,
        wrong=[(Q(180 - C) / K, r"uses $180^\circ$, the angle sum of a triangle"),
               (Q(540 - C) / K, r"uses $540^\circ$, the angle sum of a pentagon"),
               (Q(360 + C) / K, "makes a sign error when moving the constant term"),
               (Q(360) / K, "ignores the constant terms")],
        steps=steps,
        tip=f"Check: with {m(f'x = {x0}')} the angles are " + ", ".join(m(_d(v)) for v in vals)
            + f", and they add up to {m('360^\\circ')}.",
        near=_near_int(x0, (1, 2, 3, 5), hi=100),
        check=_solve_sum(exprs, 360),
    )


_REG_OBJECTS = {
    5: ["flower bed", "patio", "garden bed"],
    6: ["patio", "sandbox", "garden bed", "tabletop", "gazebo floor"],
    8: ["gazebo floor", "picnic table top", "deck", "window frame"],
    10: ["tabletop", "patio"],
    12: ["gazebo floor", "fountain base"],
}


@template("MK")
def regular_polygon(rng, lvl):
    who = person(rng)
    if lvl <= 2:
        mode = rng.choice(["interior", "interior", "exterior"])
        n = rng.choice([5, 6, 8, 10, 12] if rng.random() < 0.6 else [9, 15, 18, 20])
        name = _pname(n)
        total = (n - 2) * 180
        obj = rng.choice(_REG_OBJECTS.get(n, ["patio"]))
        if mode == "interior":
            ans = Q(total) / n
            stems = [f"What is the measure of each interior angle of a regular {name}?",
                     f"Each angle of a regular {name} has the same measure. What is that measure?",
                     f"{who.name} draws a regular {name} for a logo design. What is the measure of "
                     f"each interior angle of {who.his} drawing?",
                     f"{soldier(rng)} lays out a concrete pad shaped like a regular {name}. "
                     f"What must each interior angle of the pad measure?"]
            if n in _REG_OBJECTS:
                stems += [f"{who.name} is building a {obj} in the shape of a regular {name}. "
                          f"What is the measure of each interior angle of the {obj}?"] * 2
            wrong = [(Q(total), "is the sum of all the interior angles, not one angle"),
                     (Q(360) / n, "is the exterior angle, not the interior angle"),
                     (Q((n - 1) * 180) / n, r"uses $n-1$ instead of $n-2$")]
            intro = "" if "side" in name else f"{_a(name).capitalize()} has {m(n)} sides. "
            steps = [f"{intro}Sum of the interior angles: "
                     f"{m(f'({n} - 2) \\times 180^\\circ = {_d(total)}')}.",
                     f"A regular polygon has {m(n)} equal angles: "
                     f"{m(f'{int_raw(total)}^\\circ \\div {n} = {_d(ans)}')}."]
            tip = (f"Faster: each exterior angle is {m(f'360^\\circ \\div {n} = {_d(Q(360) / n)}')}, "
                   f"so each interior angle is {m(f'180^\\circ - {_d(Q(360) / n)} = {_d(ans)}')}.")
            check = 180 - Q(360) / n
        else:
            ans = Q(360) / n
            stems = [f"What is the measure of each exterior angle of a regular {name}?",
                     f"A regular {name} has equal exterior angles. What does each one measure?",
                     f"{who.name} walks along the edge of a {obj} shaped like a regular {name}. At each corner "
                     f"{who.he} turns through the exterior angle. How many degrees does {who.he} turn at each corner?",
                     f"{soldier(rng)} marches a squad around a course shaped like a regular {name}, turning "
                     f"through the same exterior angle at every corner. How many degrees is each turn?"]
            wrong = [(Q(180) / n, r"divides $180^\circ$ instead of $360^\circ$"),
                     (Q(total) / n, "is the interior angle, not the exterior angle"),
                     (Q(total), "is the sum of the interior angles")]
            steps = [r"The exterior angles of any polygon add up to $360^\circ$ (one full turn).",
                     f"A regular {name.split(' (')[0]} has {m(n)} equal exterior angles: "
                     f"{m(f'360^\\circ \\div {n} = {_d(ans)}')}."]
            tip = None
            check = 180 - Q(total) / n
        return Problem(stem=rng.choice(stems), answer=ans, fmt=deg, wrong=wrong, steps=steps,
                       tip=tip, check=check)
    # level 3: find the number of sides
    n = rng.choice([5, 6, 8, 9, 10, 12, 15, 18, 20])
    ext = Q(360) / n
    interior = 180 - ext
    brute = next(k for k in range(3, 200) if Q((k - 2) * 180) == interior * k)
    s = soldier(rng)
    if rng.random() < 0.55:
        stem = choose(
            rng,
            f"Each interior angle of a regular polygon measures {deg(interior)}. How many sides does the polygon have?",
            f"{who.name} is cutting boards to build a frame in the shape of a regular polygon, one board per side. "
            f"Each interior angle of the frame must measure {deg(interior)}. How many boards does {who.he} need?",
            f"A tabletop is shaped like a regular polygon with interior angles of {deg(interior)} each. "
            f"How many sides does the tabletop have?",
            f"{who.name} designs a regular polygon for a garden path. Each interior angle is {deg(interior)}. "
            f"How many sides does {who.his} polygon have?",
            f"{s} sketches a regular polygon whose interior angles each measure {deg(interior)}. "
            f"How many sides does the polygon have?")
        steps = [f"Each exterior angle is {m(f'180^\\circ - {_d(interior)} = {_d(ext)}')}.",
                 f"The exterior angles add up to {m('360^\\circ')}, so the number of sides is "
                 f"{m(f'360 \\div {int_raw(ext)} = {n}')}.",
                 f"Check: {m(f'({n} - 2) \\times 180^\\circ \\div {n} = {_d(interior)}')}. \\checkmark"]
        wrong = [(Q(360) / interior, r"divides $360^\circ$ by the interior angle instead of the exterior angle"),
                 (Q(180) / ext, r"divides $180^\circ$ instead of $360^\circ$ by the exterior angle"),
                 (ext, "gives the exterior angle instead of the number of sides")]
    else:
        stem = choose(
            rng,
            f"Each exterior angle of a regular polygon measures {deg(ext)}. How many sides does the polygon have?",
            f"{s} pilots a patrol boat around a course shaped like a regular polygon, turning {deg(ext)} "
            f"at each corner. How many sides does the course have?",
            f"A drone flies the outline of a regular polygon and turns {deg(ext)} at every corner. "
            f"How many sides does its path have?",
            f"{who.name} runs laps around a path shaped like a regular polygon, turning {deg(ext)} at "
            f"each corner. How many sides does the path have?")
        steps = [r"The exterior angles of any polygon add up to $360^\circ$; the turn at each corner is an exterior angle.",
                 f"All {m('n')} exterior angles are equal, so {m(f'n = 360 \\div {int_raw(ext)} = {n}')}."]
        wrong = [(Q(180) / ext, r"divides $180^\circ$ instead of $360^\circ$"),
                 (interior, "gives the interior angle instead of the number of sides")]
    wrong += [(Q(n + 2), None)] + ([(Q(n - 2), None)] if n - 2 >= 3 else [])
    return Problem(stem=stem, answer=Q(n), fmt=num, wrong=wrong, steps=steps, check=Q(brute),
                   near=_near_int(n, (1, 2, 3, 4), hi=100, lo=2))


# ---- polygon drawn from its angles --------------------------------------

def _polygon_points(angles, rng):
    """Vertices of a convex polygon with the given interior angles (floats)."""
    n = len(angles)
    dirs = [0.0]
    for i in range(1, n):
        dirs.append(dirs[-1] + 180 - float(angles[i]))
    us = [(math.cos(math.radians(d)), math.sin(math.radians(d))) for d in dirs]
    for _ in range(200):
        L = [rng.uniform(1.0, 1.7) for _ in range(n - 2)]
        sx = sum(l * u[0] for l, u in zip(L, us))
        sy = sum(l * u[1] for l, u in zip(L, us))
        (a1, b1), (a2, b2) = us[n - 2], us[n - 1]
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-9:
            continue
        la = (-sx * b2 + sy * a2) / det
        lb = (-a1 * sy + b1 * sx) / det
        Ls = L + [la, lb]
        if min(Ls) > 0.8 and max(Ls) / min(Ls) < 2.2:
            pts = [(0.0, 0.0)]
            for l, u in zip(Ls[:-1], us[:-1]):
                pts.append((pts[-1][0] + l * u[0], pts[-1][1] + l * u[1]))
            return pts
    need(False, "polygon could not be drawn")


def _polygon_fig(angles, labels, rng, wmax=4.8, hmax=3.4):
    pts = _polygon_points(angles, rng)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    sc = min(wmax / (max(xs) - min(xs)), hmax / (max(ys) - min(ys)))
    pts = [((px - min(xs)) * sc, (py - min(ys)) * sc) for px, py in pts]
    n = len(pts)
    body = [r"\draw[thick] " + " -- ".join(_P(*p) for p in pts) + " -- cycle;"]
    for i, tex in enumerate(labels):
        vx, vy = pts[i]
        ux, uy = pts[i - 1][0] - vx, pts[i - 1][1] - vy
        wx, wy = pts[(i + 1) % n][0] - vx, pts[(i + 1) % n][1] - vy
        lu, lw = math.hypot(ux, uy), math.hypot(wx, wy)
        bx, by = ux / lu + wx / lw, uy / lu + wy / lw
        lb = math.hypot(bx, by)
        half = math.radians(float(angles[i]) / 2)
        r = min(1.0, max(0.55, 0.5 / math.sin(half)))
        body.append(rf"\node at {_P(vx + r * bx / lb, vy + r * by / lb)} {{{tex}}};")
    return _tikz("\n".join(body))


@template("MK")
def polygon_missing(rng, lvl):
    n = rng.choice([5, 5, 6] if lvl >= 3 else [4])
    name = {4: "quadrilateral", 5: "pentagon", 6: "hexagon"}[n]
    total = (n - 2) * 180
    lo, hi = {4: (60, 130), 5: (85, 150), 6: (100, 160)}[n]
    given = [rng.randint(lo, hi) for _ in range(n - 1)]
    xv = total - sum(given)
    need(lo - 10 <= xv <= 170 and len(set(given)) >= n - 2)
    pos = rng.randrange(n)
    angles = given[:pos] + [xv] + given[pos:]
    labels = [m(_d(v)) if i != pos else r"$x^\circ$" for i, v in enumerate(angles)]
    fig = _polygon_fig(angles, labels, rng)
    gtxt = ", ".join(deg(v) for v in given[:-1]) + f", and {deg(given[-1])}"
    stem = (f"In the {name} shown, {['three', 'four', 'five'][n - 4]} of the interior angles measure {gtxt}. "
            f"What is the value of {m('x')}?")
    plus = " + ".join(str(v) for v in given)
    wrong = [(Q((n - 1) * 180 - sum(given)), r"uses $(n-1) \times 180^\circ$ for the angle sum instead of $(n-2) \times 180^\circ$"),
             (Q((n - 3) * 180 - sum(given)), "uses the angle sum of a polygon with one fewer side"),
             (Q(360 - sum(given)), r"uses $360^\circ$ for the angle sum"),
             (Q(total) / n, "divides the angle sum by the number of angles, as if all the angles were equal")]
    return Problem(
        stem=stem,
        answer=Q(xv),
        fmt=num,
        wrong=wrong,
        steps=[f"{_a(name).capitalize()} has {m(n)} sides, so its interior angles add up to "
               f"{m(f'({n} - 2) \\times 180^\\circ = {_d(total)}')}.",
               f"Add the known angles: {m(f'{plus} = {sum(given)}')}.",
               f"Subtract: {m(f'x = {int_raw(total)} - {sum(given)} = {xv}')}."],
        figure=fig,
        near=_near_int(xv),
        check=_solve_sum(given + [X], total),
    )


@template("MK")
def clock_angle(rng, lvl):
    h = rng.randint(1, 11)
    mm = rng.choice([10, 20, 40, 50, 15, 45, 25, 35, 5, 55])
    hour = Q(30 * h) + Q(mm) / 2
    minute = Q(6 * mm)
    diff = abs(hour - minute)
    ans = min(diff, 360 - diff)
    need(0 < ans < 180 and ans != 90)
    # independent route: count in minute marks (6 degrees each); hour hand at 5h + mm/12
    marks = abs(Q(5 * h) + Q(mm) / 12 - mm)
    chk = min(marks, 60 - marks) * 6
    tm = f"{h}{{:}}{mm:02d}"
    s = soldier(rng)
    stem = choose(
        rng,
        f"What is the measure of the smaller angle between the hour hand and the minute hand of a clock at {tm}?",
        f"A clock shows {tm}. What is the smaller angle formed by its hour hand and minute hand?",
        f"{s} checks the wall clock at {tm}. What is the measure of the smaller angle between the clock's two hands?",
    )
    naive = abs(Q(30 * h) - minute)
    naive = min(naive, 360 - naive)
    back = abs(Q(30 * h) - Q(mm) / 2 - minute)
    back = min(back, 360 - back)
    wrong = [(naive, r"forgets that the hour hand moves past the hour mark ($0.5^\circ$ per minute)"),
             (360 - ans, "gives the larger angle, not the smaller one"),
             (back, None)]
    steps = [
        f"The minute hand moves {m('360^\\circ \\div 60 = 6^\\circ')} per minute. "
        f"At {mm} minutes past the hour it is {m(f'{mm} \\times 6^\\circ = {_d(minute)}')} past the 12.",
        f"The hour hand moves {m('30^\\circ')} per hour plus {m('0.5^\\circ')} per minute. At {tm} it is "
        f"{m(f'{h} \\times 30^\\circ + {mm} \\times 0.5^\\circ = {30 * h}^\\circ + {_d(Q(mm) / 2)} = {_d(hour)}')} past the 12.",
        f"The hands are {m(f'{_d(max(hour, minute))} - {_d(min(hour, minute))} = {_d(diff)}')} apart.",
    ]
    if diff > 180:
        steps.append(f"That is more than {m('180^\\circ')}, so the smaller angle is "
                     f"{m(f'360^\\circ - {_d(diff)} = {_d(ans)}')}.")
    return Problem(stem=stem, answer=ans, fmt=deg, wrong=wrong, steps=steps,
                   tip=r"Each hour mark on a clock face is $360^\circ \div 12 = 30^\circ$ from the next.",
                   near=_near_int(ans, (5, 10, 15, 30)), check=chk)


PLAN = [
    # (template, level, count) -- easy -> hard; 25 problems
    (comp_supp, 1, 3),
    (angle_vocab, 1, 2),
    (vertical_adjacent, 1, 3),
    (parallel_lines, 2, 3),
    (angle_algebra, 2, 2),
    (around_point, 2, 1),
    (polygon_sum, 2, 2),
    (regular_polygon, 2, 1),
    (polygon_missing, 2, 1),
    (parallel_lines, 3, 2),
    (angle_algebra, 3, 1),
    (polygon_missing, 3, 1),
    (regular_polygon, 3, 1),
    (clock_angle, 3, 2),
]
