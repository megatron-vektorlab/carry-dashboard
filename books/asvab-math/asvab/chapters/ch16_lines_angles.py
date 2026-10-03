"""Chapter 16 - Lines & Angles.

Figures are drawn from the same numbers as the stem.  Plain Python floats
appear only in the private drawing helpers (TikZ coordinates); every answer,
check and distractor is exact (ints / sympy).
"""
import math

import sympy as sp

from ..core import (Q, Problem, need, num, m, dec_raw, int_raw, latex, text,
                    choose, soldier, template, x as X)

NUM = 16
TITLE = "Lines & Angles"
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
\node at (1.42,1.82) {$1$}; \node at (2.62,1.82) {$2$};
\node at (1.58,1.18) {$3$}; \node at (2.78,1.18) {$4$};
\node at (0.44,0.32) {$5$}; \node at (1.64,0.32) {$6$};
\node at (0.6,-0.32) {$7$}; \node at (1.8,-0.32) {$8$};
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


def _region_label(cx, cy, a0, a1, tex, base=0.62):
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
    return Problem(
        stem=stem,
        answer=ans,
        fmt=deg,
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


def _draw_kind(rng, kind):
    lo, hi = {"acute": (25, 80), "obtuse": (100, 165), "reflex": (200, 320),
              "right": (90, 90), "straight": (180, 180)}[kind]
    return rng.randint(lo, hi)


@template("MK")
def angle_vocab(rng, lvl):
    mode = rng.choice(["name", "name", "figure", "which", "pair"])
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
    a = _draw_kind(rng, kind)
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
                      f"An angle measures {deg(a)}. What kind of angle is it?")
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
    a = rng.choice([v for v in range(40, 141) if abs(v - 90) >= 10])
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
        body.append(_arc(0, 0, rot + s, rot + e, 0.3))
        body.append(_region_label(0, 0, rot + s, rot + e, tex))
    stem = choose(rng,
                  f"In the figure, two straight lines intersect, forming the {deg(g)} angle shown. What is the value of {m('x')}?",
                  f"Two straight lines cross as shown. One angle measures {deg(g)}. What is the value of {m('x')}?")
    if vert:
        wrong = [(180 - g, r"adds the angles to $180^\circ$, but vertical angles are equal"),
                 (360 - g, r"subtracts from $360^\circ$, but vertical angles are equal")]
        if g < 90:
            wrong.append((90 - g, r"subtracts from $90^\circ$, but vertical angles are equal"))
        steps = [
            f"The {m('x^\\circ')} angle is directly across from the {deg(g)} angle where the lines cross, "
            "so the two are \\emph{vertical angles}.",
            f"Vertical angles are equal, so {m(f'x = {int_raw(ans)}')}.",
        ]
    else:
        wrong = [(g, r"treats the angles as vertical angles, but these two angles together form a straight line"),
                 (360 - g, r"subtracts from $360^\circ$ instead of $180^\circ$")]
        if g < 90:
            wrong.append((90 - g, r"subtracts from $90^\circ$ instead of $180^\circ$"))
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
        check=meas[j],
    )


# --------------------------------------------------------------------------
# level 2
# --------------------------------------------------------------------------

def _on_line_label(xc, yc, ray, side, tex, h=0.4):
    """Label sitting on a horizontal line at (xc, yc), inside the angle between
    the line and a ray at direction ``ray`` (degrees).  side: 'AR','AL','BL','BR'
    (above/below the line, right/left of the vertex)."""
    t = math.radians(float(ray))
    if side == "AR":
        cot = math.cos(t) / math.sin(t)
        dx = h * cot + 0.1 if cot > 0 else 0.12
        return rf"\node[anchor=south west, inner sep=1pt] at {_P(xc + dx, yc + 0.03)} {{{tex}}};"
    if side == "AL":
        cot = math.cos(t) / math.sin(t)
        dx = -h * cot + 0.1 if cot < 0 else 0.12
        return rf"\node[anchor=south east, inner sep=1pt] at {_P(xc - dx, yc + 0.03)} {{{tex}}};"
    if side == "BL":
        cot = math.cos(t) / math.sin(t)
        dx = h * cot + 0.1 if cot > 0 else 0.12
        return rf"\node[anchor=north east, inner sep=1pt] at {_P(xc - dx, yc - 0.03)} {{{tex}}};"
    cot = math.cos(t) / math.sin(t)
    dx = -h * cot + 0.1 if cot < 0 else 0.12
    return rf"\node[anchor=north west, inner sep=1pt] at {_P(xc + dx, yc - 0.03)} {{{tex}}};"


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
    lab1, lab2 = f"$({E1})^\\circ$", f"$({E2})^\\circ$"
    names = {}
    if rel == "vertical":
        x1, y1 = _polar(v1, 2.1)
        body = [r"\draw[thick] (-2.4,0) -- (2.4,0);",
                rf"\draw[thick] {_P(-x1, -y1)} -- {_P(x1, y1)};",
                _arc(0, 0, 0, v1, 0.3), _arc(0, 0, 180, 180 + v1, 0.3),
                _on_line_label(0, 0, v1, "AR", lab1),
                _on_line_label(0, 0, v1, "BL", lab2)]
        fig = _tikz("\n".join(body))
        setup = (f"In the figure, two straight lines intersect. The vertical angles shown measure "
                 f"{m(f'({E1})^\\circ')} and {m(f'({E2})^\\circ')}.")
    elif rel == "linear":
        x1, y1 = _polar(v1, 2.0)
        body = [r"\draw[thick] (-2.4,0) -- (2.4,0);",
                rf"\draw[thick] (0,0) -- {_P(x1, y1)};",
                r"\fill (0,0) circle (1.2pt);",
                _arc(0, 0, 0, v1, 0.3), _arc(0, 0, v1, 180, 0.38),
                _on_line_label(0, 0, v1, "AR", lab1),
                _on_line_label(0, 0, v1, "AL", lab2)]
        fig = _tikz("\n".join(body))
        setup = (f"In the figure, a ray meets a straight line, forming angles of "
                 f"{m(f'({E1})^\\circ')} and {m(f'({E2})^\\circ')}.")
    else:
        A, B = rng.choice([("A", "B"), ("P", "Q"), ("1", "2"), ("J", "K")])
        names = {E1: A, E2: B}
        word = "complementary" if rel == "comp" else "supplementary"
        setup = (f"{m(r'\angle ' + A)} and {m(r'\angle ' + B)} are {word}. "
                 f"{m(r'\angle ' + A)} measures {m(f'({E1})^\\circ')}, and "
                 f"{m(r'\angle ' + B)} measures {m(f'({E2})^\\circ')}.")

    # ---------------- solve for x ----------------
    steps = []
    if rel == "vertical":
        (pb, qb), (ps, qs) = ((p, q), (r, s)) if p > r else ((r, s), (p, q))
        steps.append(f"Vertical angles are equal, so set the expressions equal: "
                     f"{m(f'{_lin(pb, qb)} = {_lin(ps, qs)}')}.")
        steps.append(f"Subtract {m(latex(ps * X))} from both sides: "
                     f"{m(f'{_lin(pb - ps, qb)} = {int_raw(qs)}')}.")
        more, xv = _solve_steps(pb - ps, qb, qs)
        wrong_x = [(Q(180 - q - s) / (p + r), r"adds the angles to $180^\circ$, but vertical angles are equal"),
                   (Q(qs + qb) / (pb - ps), "makes a sign error when moving the constant term")]
    else:
        lead = {"linear": "Angles that form a straight line add up to",
                "supp": "Supplementary angles add up to",
                "comp": "Complementary angles add up to"}[rel]
        steps.append(f"{lead} {m(_d(total))}: {m(f'({E1}) + ({E2}) = {total}')}.")
        steps.append(f"Combine like terms: {m(f'{_lin(p + r, q + s)} = {total}')}.")
        more, xv = _solve_steps(p + r, q + s, total)
        other = 90 if total == 180 else 180
        wrong_x = [(Q(s - q) / (p - r), "sets the two angles equal instead of adding them"),
                   (Q(other - q - s) / (p + r), f"uses {m(_d(other))} instead of {m(_d(total))}"),
                   (Q(total + q + s) / (p + r), "makes a sign error when moving the constant term")]
    steps += more
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
            ask = f"What is the measure of the {m(f'({which})^\\circ')} angle?"
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
