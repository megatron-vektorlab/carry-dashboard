"""Chapter 18 - Perimeter & Area.

Figures are drawn from the same numbers as the stem.  Plain Python floats
appear only in the private drawing helpers (TikZ coordinates); every answer,
check and distractor is exact (ints / sympy).
"""
import sympy as sp

from ..core import (R, Q, Problem, need, num, money, m, dec_raw, int_raw,
                    sq_unit, choose, person, soldier, template, x as X)

NUM = 18
TITLE = r"Perimeter \& Area"
PART = 3

INTRO = r"""
\textbf{Perimeter} is the distance around a figure: add up the sides, and the
answer is in plain units (feet, meters). \textbf{Area} is the amount of
surface inside: it is measured in \emph{square} units (ft$^2$, or square feet).

\begin{concept}{Formulas}
\begin{minipage}[c]{0.5\linewidth}
\renewcommand{\arraystretch}{1.25}
\begin{tabular}{@{}lll@{}}
\textbf{Shape} & \textbf{Perimeter} & \textbf{Area}\\
Rectangle & $2l + 2w$ & $l \times w$\\
Square & $4s$ & $s^2$\\
Triangle & add the sides & $\frac12 \times b \times h$\\
Parallelogram & add the sides & $b \times h$\\
Trapezoid & add the sides & $\frac12 (b_1 + b_2) \times h$\\
\end{tabular}
\end{minipage}\hfill
\begin{minipage}[c]{0.46\linewidth}\centering
\begin{tikzpicture}[font=\small, line join=round]
\draw[thick] (0,0) -- (1.6,0) -- (0.5,1.2) -- cycle;
\draw[dashed] (0.5,1.2) -- (0.5,0);
\draw (0.5,0.15) -- (0.65,0.15) -- (0.65,0);
\node[right] at (0.5,0.55) {$h$}; \node[below] at (0.8,0) {$b$};
\begin{scope}[xshift=2cm]
\draw[thick] (0,0) -- (1.5,0) -- (2.0,1.2) -- (0.5,1.2) -- cycle;
\draw[dashed] (0.5,1.2) -- (0.5,0);
\draw (0.5,0.15) -- (0.65,0.15) -- (0.65,0);
\node[right] at (0.5,0.55) {$h$}; \node[below] at (0.75,0) {$b$};
\end{scope}
\end{tikzpicture}
\end{minipage}
\smallskip

The height $h$ is always measured at a \emph{right angle} to the base (the dashed lines). It is not a slanted side.
\end{concept}

\begin{concept}{Composite shapes, units, and scaling}
\begin{itemize}
\item Split an odd shape into rectangles and add the areas, or take a big rectangle and subtract the missing piece.
\item $1$ yard $= 3$ feet, so $1$ square yard $= 3 \times 3 = 9$ square feet. Likewise $1$ square foot $= 12 \times 12 = 144$ square inches.
\item If every side is multiplied by $k$, the perimeter is multiplied by $k$ and the area by $k^2$: doubling the sides makes the area $4$ times as large.
\end{itemize}
\end{concept}

\begin{example}{Worked example}
Carpet costs \$25 per square yard. How much does it cost to carpet a room that is 15 feet by 12 feet?

\textbf{Solution.} Area $= 15 \times 12 = 180$ square feet. Change to square yards: $180 \div 9 = 20$ square yards.
Cost $= 20 \times \$25 = \$500$.
\end{example}

\begin{tip}
Convert lengths \emph{before} you multiply when the numbers divide evenly:
15 ft $\times$ 12 ft is 5 yd $\times$ 4 yd $= 20$ square yards, with no large division at all.
\end{tip}

\begin{trap}
\begin{itemize}
\item Mixing up perimeter (add the sides) and area (multiply).
\item Forgetting the $\frac12$ in the triangle and trapezoid formulas.
\item Using a slanted side instead of the height.
\item Dividing by $3$ instead of $9$ to change square feet to square yards.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# helpers (floats only for TikZ coordinates)
# --------------------------------------------------------------------------

_UNITS = {"ft": ("foot", "feet"), "in": ("inch", "inches"), "cm": ("centimeter", "centimeters"),
          "m": ("meter", "meters"), "yd": ("yard", "yards")}


def _lenfmt(u):
    def f(v):
        return m(dec_raw(v) + rf"\text{{ {u}}}")
    return f


def _areafmt(u):
    return sq_unit(lambda v: m(dec_raw(v)), u)


def _w(v, u):
    one, many = _UNITS[u]
    return f"{m(dec_raw(v))} {one if Q(v) == 1 else many}"


def _sq(v, u):
    """'84 square feet' for steps and stems."""
    return f"{m(dec_raw(v))} square {_UNITS[u][1] if Q(v) != 1 else _UNITS[u][0]}"


def _lab(v, u):
    return f"{m(dec_raw(v))} {u}"


def _near_int(ans, deltas, lo=0):
    def f(rng):
        out = [Q(ans) + d for d in deltas] + [Q(ans) - d for d in deltas]
        out = [v for v in out if v > lo]
        rng.shuffle(out)
        return out
    return f


def _f(v):
    s = f"{float(v):.2f}"
    return "0.00" if s == "-0.00" else s


def _P(px, py):
    return f"({_f(px)},{_f(py)})"


def _tikz(body):
    return ("\\begin{tikzpicture}[font=\\small, line cap=round, line join=round]\n"
            + "\n".join(body) + "\n\\end{tikzpicture}")


def _scale(wu, hu, wmax=4.2, hmax=2.6):
    """cm per unit so a wu x hu drawing fits wmax x hmax."""
    return min(wmax / float(wu), hmax / float(hu))


def _ticks_h(x0, x1, y, k=1):
    mx = (x0 + x1) / 2
    return [rf"\draw {_P(mx + (j - (k - 1) / 2) * 0.08, y - 0.09)} -- {_P(mx + (j - (k - 1) / 2) * 0.08, y + 0.09)};"
            for j in range(k)]


def _ticks_v(x, y0, y1, k=1):
    my = (y0 + y1) / 2
    return [rf"\draw {_P(x - 0.09, my + (j - (k - 1) / 2) * 0.08)} -- {_P(x + 0.09, my + (j - (k - 1) / 2) * 0.08)};"
            for j in range(k)]


def _rect_fig(L, W, u, square=False):
    sc = _scale(L, W, 3.8, 2.4)
    a, b = float(L) * sc, float(W) * sc
    body = [rf"\draw[thick] (0,0) rectangle {_P(a, b)};",
            rf"\node[below] at {_P(a / 2, 0)} {{{_lab(L, u)}}};"]
    if square:
        body += _ticks_h(0, a, 0) + _ticks_h(0, a, b) + _ticks_v(0, 0, b) + _ticks_v(a, 0, b)
    else:
        body.append(rf"\node[right] at {_P(a, b / 2)} {{{_lab(W, u)}}};")
    return _tikz(body)


def _right_mark(x, y, dx=1, dy=1, s=0.16):
    return rf"\draw {_P(x + dx * s, y)} -- {_P(x + dx * s, y + dy * s)} -- {_P(x, y + dy * s)};"


_SHAPE_CTX = ["a garden bed", "a patio", "a rug", "a deck", "a parking lot", "a storage room floor"]

# realistic rectangles: (context, unit, length range, width range)
_RECT_CTX = [("a garden bed", "ft", (6, 20), (3, 8)), ("a patio", "ft", (10, 24), (8, 16)),
             ("a rug", "ft", (5, 12), (3, 9)), ("a bulletin board", "ft", (3, 8), (2, 4)),
             ("a parking space", "ft", (16, 20), (8, 10)), ("a tabletop", "in", (30, 72), (24, 40)),
             ("a window", "in", (24, 60), (18, 40)), ("a barracks room floor", "ft", (12, 24), (10, 16)),
             ("a tarp", "ft", (8, 20), (6, 12)), ("a basketball court", "ft", (74, 94), (42, 50))]


# --------------------------------------------------------------------------
# level 1
# --------------------------------------------------------------------------

@template("MK")
def rect_basic(rng, lvl):
    u = rng.choice(["ft", "in", "m", "cm", "yd"])
    shape = rng.choice(["rect", "rect", "square"])
    ask = rng.choice(["area", "perimeter"])
    if shape == "rect":
        ctx = rng.choice(_RECT_CTX) if rng.random() < 0.4 else None
        if ctx:
            u = ctx[1]
            L, W = rng.randint(*ctx[2]), rng.randint(*ctx[3])
        else:
            L = rng.randint(5, 25)
            W = rng.randint(3, L - 1)
        need(L > W)
        area, per = L * W, 2 * (L + W)
        fig = _rect_fig(L, W, u) if rng.random() < 0.6 and not ctx else None
        dims = f"{_w(L, u)} long and {_w(W, u)} wide"
        thing = ctx[0].capitalize() if ctx else "A rectangle"
        if ask == "area":
            stem = (f"{thing} is a rectangle {dims}. What is its area?" if ctx else
                    choose(rng, f"What is the area of a rectangle that is {dims}?",
                           f"A rectangle is {dims}. What is its area?"))
            ans, fmt = Q(area), _areafmt(u)
            wrong = [(Q(per), "gives the perimeter, not the area"),
                     (Q(L + W), "adds the length and width instead of multiplying"),
                     (Q(area) / 2, r"takes half, as if the shape were a triangle")]
            steps = [r"Area of a rectangle $= \text{length} \times \text{width}$.",
                     f"{m(f'{L} \\times {W} = {int_raw(area)}')}, so the area is {_sq(area, u)}."]
            check = sum([W] * L)
        else:
            stem = (f"{thing} is a rectangle {dims}. What is the distance around it?" if ctx else
                    choose(rng, f"What is the perimeter of a rectangle that is {dims}?",
                           f"A rectangle is {dims}. What is its perimeter?"))
            ans, fmt = Q(per), _lenfmt(u)
            wrong = [(Q(area), "gives the area, not the perimeter"),
                     (Q(L + W), "adds only one length and one width"),
                     (Q(2 * L + W), "leaves out one of the widths")]
            steps = [r"Perimeter is the distance around: add all four sides, $l + w + l + w$.",
                     f"{m(f'{L} + {W} + {L} + {W} = {int_raw(per)}')}, so the perimeter is {_w(per, u)}."]
            check = L + W + L + W
    else:
        s = rng.randint(3, 20)
        fig = _rect_fig(s, s, u, square=True) if rng.random() < 0.6 else None
        if ask == "area":
            stem = choose(rng,
                          f"A square has sides of {_w(s, u)}. What is its area?",
                          f"What is the area of a square with a side length of {_w(s, u)}?")
            ans, fmt = Q(s * s), _areafmt(u)
            wrong = [(Q(4 * s), "gives the perimeter, not the area"),
                     (Q(2 * s), "doubles the side instead of squaring it"),
                     (Q(s * s) / 2, None)]
            steps = [r"Area of a square $= \text{side} \times \text{side} = s^2$.",
                     f"{m(f'{s} \\times {s} = {s * s}')}, so the area is {_sq(s * s, u)}."]
            check = sum([s] * s)
        else:
            stem = choose(rng,
                          f"A square has sides of {_w(s, u)}. What is its perimeter?",
                          f"What is the perimeter of a square with a side length of {_w(s, u)}?")
            ans, fmt = Q(4 * s), _lenfmt(u)
            wrong = [(Q(s * s), "gives the area, not the perimeter"),
                     (Q(2 * s), "counts only two sides"),
                     (Q(3 * s), "counts only three sides")]
            steps = [r"A square has four equal sides, so perimeter $= 4 \times \text{side}$.",
                     f"{m(f'4 \\times {s} = {4 * s}')}, so the perimeter is {_w(4 * s, u)}."]
            check = s + s + s + s
        if fig:
            stem = stem.replace("A square has", "The square shown has")
    return Problem(stem=stem, answer=ans, fmt=fmt, wrong=wrong, steps=steps, figure=fig,
                   near=_near_int(ans, (2, 4, 6, 10)), check=Q(check))


def _label_width(tex):
    """Rough printed width (cm) of a short label such as $12$ ft."""
    import re
    core = re.sub(r"\\circ", "o", tex)
    spaces = core.count(" ")
    core = re.sub(r"[$\\{}^ ]", "", core)
    return 0.2 * len(core) + 0.12 * spaces + 0.15


def _side_label(x1, y1, x2, y2, tex, cx, cy, gap=0.1):
    """Label just outside the segment (x1,y1)-(x2,y2), on the side away from
    the interior point (cx, cy); the whole label box clears the segment."""
    import math
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if (cx - mx) * nx + (cy - my) * ny > 0:
        nx, ny = -nx, -ny
    d = 0.5 * _label_width(tex) * abs(nx) + 0.5 * 0.34 * abs(ny) + gap
    return rf"\node[inner sep=0pt] at {_P(mx + d * nx, my + d * ny)} {{{tex}}};"


def _height_label(xd, H, left_x, right_x, tex):
    """Put the height label beside a dashed height at x = xd, inside the shape.
    left_x(y) / right_x(y) give the shape's left / right edge at height y.
    Returns TikZ or None when there is no room."""
    w = _label_width(tex) + 0.08
    for frac in (0.45, 0.35, 0.55):
        y0, y1 = H * frac - 0.17, H * frac + 0.17
        if min(right_x(y0), right_x(y1)) - xd >= w + 0.06:
            return rf"\node[anchor=west, inner sep=1pt] at {_P(xd + 0.04, H * frac)} {{{tex}}};"
        if xd - max(left_x(y0), left_x(y1)) >= w + 0.06:
            return rf"\node[anchor=east, inner sep=1pt] at {_P(xd - 0.04, H * frac)} {{{tex}}};"
    return None


def _half_product(a, b):
    """'13 \\times 5 = 65' style working for (1/2) * a * b, halving whichever factor is even."""
    if a % 2 == 0:
        return f"{a // 2} \\times {b} = {int_raw(Q(a * b) / 2)}"
    if b % 2 == 0:
        return f"{a} \\times {b // 2} = {int_raw(Q(a * b) / 2)}"
    return f"\\frac12 \\times {int_raw(a * b)} = {int_raw(Q(a * b) / 2)}"


def _triangle_fig(b, h, p, u, slant=None, right=False):
    """Triangle with base b on the x-axis and apex at (p, h): a dashed height
    from the apex, or (right=True, p == 0) a right angle at the origin."""
    sc = _scale(max(b, p), h, 3.8, 2.4)
    B, H, Pp = float(b) * sc, float(h) * sc, float(p) * sc
    cx, cy = (B + Pp) / 3, H / 3
    body = [rf"\draw[thick] (0,0) -- {_P(B, 0)} -- {_P(Pp, H)} -- cycle;",
            rf"\node[below] at {_P(B / 2, 0)} {{{_lab(b, u)}}};"]
    if right:
        body.append(_right_mark(0, 0))
        body.append(_side_label(0, 0, 0, H, _lab(h, u), cx, cy))
    else:
        body.append(rf"\draw[dashed] {_P(Pp, H)} -- {_P(Pp, 0)};")
        body.append(_right_mark(Pp, 0, 1 if Pp < B - 0.3 else -1))
        lab = _height_label(Pp, H, lambda y: Pp * y / H, lambda y: B + (Pp - B) * y / H, _lab(h, u))
        need(lab is not None, "no room for the height label")
        body.append(lab)
    if slant is not None:
        body.append(_side_label(0, 0, Pp, H, _lab(slant, u), cx, cy))
    return _tikz(body)


@template("MK")
def triangle_area(rng, lvl):
    u = rng.choice(["ft", "in", "m", "cm", "yd"])
    if lvl <= 1:
        mode = rng.choice(["general", "general", "right"])
        b, h = rng.randint(4, 20), rng.randint(3, 16)
        need((b * h) % 2 == 0 and b != h)
        if mode == "right":
            fig = _triangle_fig(b, h, 0, u, right=True)
            stem = choose(rng,
                          f"A right triangle has legs of {_w(b, u)} and {_w(h, u)}. What is its area?",
                          f"What is the area of the right triangle shown, whose legs measure {_w(b, u)} and {_w(h, u)}?")
            lead = "In a right triangle the two legs are a base and a height."
            check = sp.integrate(sp.Rational(h, b) * X, (X, 0, b))     # area under the hypotenuse
        else:
            p = rng.choice([R(1, 5), R(1, 4), R(1, 3), R(2, 3), R(3, 4), R(4, 5)]) * b
            fig = _triangle_fig(b, h, p, u)
            stem = choose(rng,
                          f"A triangle has a base of {_w(b, u)} and a height of {_w(h, u)}. What is its area?",
                          f"What is the area of the triangle shown, with base {_w(b, u)} and height {_w(h, u)}?")
            lead = "The base and the height (the dashed line, at a right angle to the base) are given."
            check = Q(p) * h / 2 + (b - Q(p)) * h / 2                  # two right triangles
        wrong = [(Q(b * h), r"forgets to multiply by $\frac12$"),
                 (Q(b + h), "adds the base and height"),
                 (Q(b * h) / 4, r"takes half of the base and half of the height")]
        slant = None
    else:
        mode = rng.choice(["slant", "slant", "right_hyp"])
        if mode == "slant":
            p_, h, s = rng.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (4, 3, 5), (8, 6, 10),
                                   (12, 5, 13), (8, 15, 17), (12, 9, 15)])
            b = rng.randint(p_ + 3, p_ + 16)
            need((b * h) % 2 == 0 and b != s and b != h and 10 * h >= 3 * b)
            slant = s
            fig = _triangle_fig(b, h, p_, u, slant=s)
            stem = choose(rng,
                          f"In the triangle shown, the base is {_w(b, u)}, the height is {_w(h, u)}, and the slanted side "
                          f"is {_w(s, u)}. What is the area of the triangle?",
                          f"A triangle has a base of {_w(b, u)}, a height of {_w(h, u)}, and a slanted side of "
                          f"{_w(s, u)}, as shown. What is its area?")
            lead = (f"Use the base and the height. The height is the dashed line ({_w(h, u)}), which meets the base at "
                    f"a right angle; the slanted side ({_w(s, u)}) is not the height.")
            check = Q(p_ * h) / 2 + Q((b - p_) * h) / 2
            wrong = [(Q(b * s) / 2, "uses the slanted side instead of the height"),
                     (Q(b * h), r"forgets to multiply by $\frac12$"),
                     (Q(b * s), r"uses the slanted side and forgets the $\frac12$"),
                     (Q(b + h + s), "adds the three lengths")]
        else:
            h, b, c = rng.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20),
                                  (7, 24, 25), (15, 20, 25)])
            if rng.random() < 0.5:
                h, b = b, h
            slant = c
            sc = _scale(b, h, 3.8, 2.4)
            B, H = b * sc, h * sc
            fig = _tikz([rf"\draw[thick] (0,0) -- {_P(B, 0)} -- {_P(0, H)} -- cycle;", _right_mark(0, 0),
                         rf"\node[below] at {_P(B / 2, 0)} {{{_lab(b, u)}}};",
                         rf"\node[left] at {_P(0, H / 2)} {{{_lab(h, u)}}};",
                         rf"\node[above right] at {_P(B / 2, H / 2)} {{{_lab(c, u)}}};"])
            stem = choose(rng,
                          f"A right triangle has sides of {_w(h, u)}, {_w(b, u)}, and {_w(c, u)}. What is its area?",
                          f"The right triangle shown has sides of {_w(h, u)}, {_w(b, u)}, and {_w(c, u)}. "
                          f"What is its area?")
            lead = (f"In a right triangle the two legs (the sides that form the right angle) are the base and the "
                    f"height. The longest side, {_w(c, u)}, is the hypotenuse and is not used.")
            sh = Q(h + b + c) / 2
            check = sp.sqrt(sh * (sh - h) * (sh - b) * (sh - c))          # Heron's formula
            wrong = [(Q(max(b, h) * c) / 2, "uses the hypotenuse as the height"),
                     (Q(b * h), r"forgets to multiply by $\frac12$"),
                     (Q(b + h + c), "gives the perimeter, not the area"),
                     (Q(b * h * c) / 2, "multiplies all three sides, then halves")]
            need((b * h) % 2 == 0)
    area = Q(b * h) / 2
    return Problem(
        stem=stem,
        answer=area,
        fmt=_areafmt(u),
        wrong=wrong,
        steps=[lead,
               r"Area of a triangle $= \frac12 \times \text{base} \times \text{height}$.",
               f"{m(f'\\frac12 \\times {b} \\times {h} = \\frac12 \\times {int_raw(b * h)} = {int_raw(area)}')}, so the area is "
               f"{_sq(area, u)}."],
        figure=fig,
        near=_near_int(area, (2, 4, 6, 10)),
        check=check,
    )


@template("MK")
def missing_side(rng, lvl):
    u = rng.choice(["ft", "in", "m", "cm", "yd"])
    if lvl <= 1:
        mode = rng.choice(["rect_area", "rect_area", "sq_area", "sq_per"])
    else:
        mode = rng.choice(["rect_per", "rect_per", "sq_per_area", "area_to_per"])
    if mode == "rect_area":
        L = rng.randint(4, 20)
        W = rng.randint(2, 15)
        need(L != W)
        A = L * W
        ctx = choose(rng, "A rectangle", choose(rng, *_SHAPE_CTX).capitalize() + " (a rectangle)")
        stem = choose(rng,
                      f"{ctx} has an area of {_sq(A, u)} and a length of {_w(L, u)}. What is its width?",
                      f"The area of a rectangle is {_sq(A, u)}. If the rectangle is {_w(L, u)} long, how wide is it?")
        ans, fmt = Q(W), _lenfmt(u)
        wrong = [(Q(A - L), "subtracts the length from the area instead of dividing"),
                 (Q(A - 2 * L) / 2, "uses the perimeter formula instead of the area formula"),
                 (Q(A) * L, "multiplies instead of dividing")]
        steps = [r"Area $= \text{length} \times \text{width}$, so width $= \text{area} \div \text{length}$.",
                 f"{m(f'{int_raw(A)} \\div {L} = {W}')}, so the width is {_w(W, u)}.",
                 f"Check: {m(f'{L} \\times {W} = {int_raw(A)}')}. \\checkmark"]
        check = sp.solve(sp.Eq(L * X, A), X)[0]
    elif mode == "sq_area":
        s = rng.randint(3, 15)
        A = s * s
        stem = choose(rng,
                      f"A square has an area of {_sq(A, u)}. What is the length of one side?",
                      f"The area of a square is {_sq(A, u)}. How long is each side?")
        ans, fmt = Q(s), _lenfmt(u)
        wrong = [(Q(A) / 4, "divides the area by 4, as if it were the perimeter"),
                 (Q(A) / 2, "divides the area by 2 instead of taking the square root"),
                 (Q(2 * s), None)]
        steps = [r"Area of a square $= s \times s$, so the side is the number that times itself gives the area.",
                 f"{m(f'{s} \\times {s} = {int_raw(A)}')}, so each side is {_w(s, u)}."]
        check = sp.sqrt(A)
    elif mode == "sq_per":
        s = rng.randint(3, 25)
        Pm = 4 * s
        stem = choose(rng,
                      f"A square has a perimeter of {_w(Pm, u)}. How long is each side?",
                      f"The perimeter of a square is {_w(Pm, u)}. What is the length of one side?")
        ans, fmt = Q(s), _lenfmt(u)
        wrong = [(Q(Pm) / 2, "divides by 2 instead of 4"),
                 (Q(Pm - 4), "subtracts 4 instead of dividing by 4"),
                 (Q(Pm) * 4, "multiplies by 4 instead of dividing")]
        if sp.sqrt(Pm).is_integer:
            wrong.append((sp.sqrt(Pm), "takes the square root, as if the perimeter were the area"))
        steps = [r"A square has 4 equal sides, so each side is the perimeter divided by 4.",
                 f"{m(f'{int_raw(Pm)} \\div 4 = {s}')}, so each side is {_w(s, u)}."]
        check = sp.solve(sp.Eq(4 * X, Pm), X)[0]
    elif mode == "rect_per":
        L = rng.randint(6, 30)
        W = rng.randint(3, 25)
        need(L > W)
        Pm = 2 * (L + W)
        if rng.random() < 0.5:
            stem = f"A rectangle has a perimeter of {_w(Pm, u)} and a length of {_w(L, u)}. What is its width?"
        else:
            u = rng.choice(["ft", "yd", "m"])
            stem = (f"The perimeter of a rectangular {choose(rng, 'garden', 'yard', 'patio', 'parking area')} is "
                    f"{_w(Pm, u)}. If it is {_w(L, u)} long, how wide is it?")
        ans, fmt = Q(W), _lenfmt(u)
        wrong = [(Q(Pm - 2 * L), "subtracts both lengths but forgets to divide by 2"),
                 (Q(Pm - L), "subtracts the length only once"),
                 (Q(Pm) / 2, "finds half the perimeter and stops"),
                 (Q(Pm) / 4, "divides by 4, as if the rectangle were a square")]
        steps = [r"Perimeter $= 2 \times \text{length} + 2 \times \text{width}$.",
                 f"Subtract the two lengths: {m(f'{int_raw(Pm)} - 2 \\times {L} = {int_raw(Pm)} - {2 * L} = {Pm - 2 * L}')}. "
                 "That is the two widths together.",
                 f"Divide by 2: {m(f'{Pm - 2 * L} \\div 2 = {W}')}, so the width is {_w(W, u)}."]
        check = sp.solve(sp.Eq(2 * L + 2 * X, Pm), X)[0]
    elif mode == "sq_per_area":
        s = rng.randint(3, 15)
        Pm = 4 * s
        stem = choose(rng,
                      f"A square has a perimeter of {_w(Pm, u)}. What is its area?",
                      f"The perimeter of a square is {_w(Pm, u)}. Find the area of the square.")
        ans, fmt = Q(s * s), _areafmt(u)
        wrong = [(Q(s), "finds the side length and stops"),
                 (Q(Pm // 2) ** 2, "divides the perimeter by 2 instead of 4"),
                 (Q(Pm), "gives the perimeter again")]
        steps = [f"Find the side: {m(f'{int_raw(Pm)} \\div 4 = {s}')} {u}.",
                 f"Area {m('= s^2')} {m(f'= {s} \\times {s} = {s * s}')}, so the area is {_sq(s * s, u)}."]
        check = Q(Pm) ** 2 / 16
    else:
        L = rng.randint(5, 20)
        W = rng.randint(2, 15)
        need(L > W)
        A = L * W
        stem = choose(rng,
                      f"A rectangle has an area of {_sq(A, u)} and a length of {_w(L, u)}. What is its perimeter?",
                      f"The area of a rectangle is {_sq(A, u)}, and the rectangle is {_w(L, u)} long. "
                      f"What is its perimeter?")
        ans, fmt = Q(2 * (L + W)), _lenfmt(u)
        wrong = [(Q(W), "finds the width and stops"),
                 (Q(L + W), "adds only one length and one width"),
                 (Q(A), "gives the area, not the perimeter")]
        steps = [f"Find the width: {m(f'{int_raw(A)} \\div {L} = {W}')} {u}.",
                 f"Perimeter {m(f'= 2 \\times {L} + 2 \\times {W} = {2 * L} + {2 * W} = {2 * (L + W)}')}, so the "
                 f"perimeter is {_w(2 * (L + W), u)}."]
        check = 2 * (L + sp.solve(sp.Eq(L * X, A), X)[0])
    return Problem(stem=stem, answer=ans, fmt=fmt, wrong=wrong, steps=steps,
                   near=_near_int(ans, (1, 2, 3, 4) if ans < 40 else (2, 4, 6, 10)), check=check)


# --------------------------------------------------------------------------
# level 2
# --------------------------------------------------------------------------

_SLANT_TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (4, 3, 5), (8, 6, 10), (12, 5, 13), (12, 9, 15)]


@template("MK")
def parallelogram(rng, lvl):
    u = rng.choice(["ft", "in", "m", "cm", "yd"])
    p_, h, s = rng.choice(_SLANT_TRIPLES)
    b = rng.randint(max(p_ + 2, 6), 24)
    need(Q(h) / (b + p_) >= R(1, 4) and b != s and b != h)
    sc = _scale(b + p_, h, 4.2, 2.4)
    B, H, Pp = b * sc, h * sc, p_ * sc
    lab = _height_label(Pp, H, lambda y: Pp * y / H, lambda y: B + Pp * y / H, _lab(h, u))
    need(lab is not None)
    fig = _tikz([rf"\draw[thick] (0,0) -- {_P(B, 0)} -- {_P(B + Pp, H)} -- {_P(Pp, H)} -- cycle;",
                 rf"\draw[dashed] {_P(Pp, H)} -- {_P(Pp, 0)};",
                 _right_mark(Pp, 0),
                 rf"\node[below] at {_P(B / 2, 0)} {{{_lab(b, u)}}};",
                 lab,
                 _side_label(0, 0, Pp, H, _lab(s, u), (B + Pp) / 2, H / 2)])
    dims = f"a base of {_w(b, u)}, a height of {_w(h, u)}, and slanted sides of {_w(s, u)}"
    if rng.random() < 0.7:
        stem = choose(rng,
                      f"The parallelogram shown has {dims}. What is its area?",
                      f"What is the area of a parallelogram with {dims}, as shown?")
        ans, fmt = Q(b * h), _areafmt(u)
        wrong = [(Q(b * s), "multiplies by the slanted side instead of the height"),
                 (Q(b * h) / 2, r"takes $\frac12$, as for a triangle"),
                 (Q(2 * (b + s)), "gives the perimeter, not the area")]
        steps = [r"Area of a parallelogram $= \text{base} \times \text{height}$, where the height is the dashed line at a right "
                 r"angle to the base (not the slanted side).",
                 f"{m(f'{b} \\times {h} = {int_raw(b * h)}')}, so the area is {_sq(b * h, u)}."]
        tip = ("Why it works: cut the triangle off one end and slide it to the other end. "
               f"You get a {m(f'{b} \\times {h}')} rectangle.")
        check = Q(b * h - p_ * h) + Q(p_ * h)          # rectangle + the two end triangles
    else:
        stem = choose(rng,
                      f"The parallelogram shown has {dims}. What is its perimeter?",
                      f"What is the perimeter of a parallelogram with {dims}, as shown?")
        ans, fmt = Q(2 * (b + s)), _lenfmt(u)
        wrong = [(Q(2 * (b + h)), "uses the height instead of the slanted side"),
                 (Q(b + s), "adds only two of the four sides"),
                 (Q(b * h), "gives the area, not the perimeter")]
        steps = ["The perimeter is the distance around: two bases and two slanted sides. The height is inside the "
                 "figure, so it is not part of the perimeter.",
                 f"{m(f'{b} + {s} + {b} + {s} = {2 * (b + s)}')}, so the perimeter is {_w(2 * (b + s), u)}."]
        tip = None
        check = Q(b + s + b + s)
    return Problem(stem=stem, answer=ans, fmt=fmt, wrong=wrong, steps=steps, tip=tip, figure=fig,
                   near=_near_int(ans, (2, 4, 6, 10)), check=check)


@template("MK")
def trapezoid(rng, lvl):
    u = rng.choice(["ft", "in", "m", "cm", "yd"])
    b1 = rng.randint(8, 24)
    b2 = rng.randint(3, b1 - 3)
    h = rng.randint(3, 14)
    need(((b1 + b2) * h) % 2 == 0)
    right = rng.random() < 0.3
    o = 0 if right else rng.choice([R(1, 4), R(1, 2), R(3, 4)]) * (b1 - b2)
    sc = _scale(b1, h, 4.0, 2.4)
    B1, B2, H, O = b1 * sc, b2 * sc, h * sc, float(o) * sc
    body = [rf"\draw[thick] (0,0) -- {_P(B1, 0)} -- {_P(O + B2, H)} -- {_P(O, H)} -- cycle;",
            rf"\node[below] at {_P(B1 / 2, 0)} {{{_lab(b1, u)}}};",
            rf"\node[above] at {_P(O + B2 / 2, H)} {{{_lab(b2, u)}}};"]
    if right:
        body += [_right_mark(0, 0), rf"\node[left] at {_P(0, H / 2)} {{{_lab(h, u)}}};"]
    else:
        xd = O + 0.3 * B2
        lab = _height_label(xd, H, lambda y: O * y / H, lambda y: B1 + (O + B2 - B1) * y / H, _lab(h, u))
        need(lab is not None)
        body += [rf"\draw[dashed] {_P(xd, H)} -- {_P(xd, 0)};", _right_mark(xd, 0), lab]
    area = Q(b1 + b2) * h / 2
    need(area.is_integer)
    stem = choose(rng,
                  f"The trapezoid shown has parallel bases of {_w(b1, u)} and {_w(b2, u)} and a height of {_w(h, u)}. "
                  f"What is its area?",
                  f"What is the area of a trapezoid with bases of {_w(b2, u)} and {_w(b1, u)} and a height of {_w(h, u)}?")
    return Problem(
        stem=stem,
        answer=area,
        fmt=_areafmt(u),
        wrong=[(Q((b1 + b2) * h), r"forgets to multiply by $\frac12$"),
               (Q(b1 * h), "uses only the longer base"),
               (Q(b2 * h), "uses only the shorter base"),
               (Q(b1 * b2 * h) / 2, "multiplies the two bases instead of adding them")],
        steps=[r"Area of a trapezoid $= \frac12 \times (b_1 + b_2) \times h$: average the two parallel bases, then "
               r"multiply by the height.",
               f"Add the bases: {m(f'{b1} + {b2} = {b1 + b2}')}.",
               f"{m(f'\\frac12 \\times {b1 + b2} \\times {h} = ' + _half_product(b1 + b2, h))}, so the area is "
               f"{_sq(area, u)}."],
        figure=_tikz(body),
        near=_near_int(area, (2, 4, 6, 10)),
        check=Q(b2 * h) + Q(b1 - b2) * h / 2,          # rectangle + triangle(s) with total base b1 - b2
    )


def _l_shape_fig(W, H, cw, ch, u, mirror, label_cut):
    """L-shaped region: W x H rectangle with a cw x ch notch cut from a top corner."""
    sc = _scale(W, H, 3.6, 2.5)
    w, hh, c1, c2 = W * sc, H * sc, cw * sc, ch * sc

    def X_(v):
        return w - v if mirror else v
    pts = [(0, 0), (w, 0), (w, hh - c2), (w - c1, hh - c2), (w - c1, hh), (0, hh)]
    pts = [(X_(px), py) for px, py in pts]
    body = [r"\draw[thick] " + " -- ".join(_P(*p) for p in pts) + " -- cycle;",
            rf"\node[below] at {_P(w / 2, 0)} {{{_lab(W, u)}}};",
            rf"\node[{'right' if mirror else 'left'}] at {_P(X_(0), hh / 2)} {{{_lab(H, u)}}};"]
    if label_cut:
        # the two edges of the notch, labeled from inside the notch
        need(c2 >= 0.8 and c1 >= _label_width(_lab(cw, u)) + 0.15
             and c1 >= _label_width(_lab(ch, u)) + 0.15, "notch too small for its labels")
        anchor = "east" if mirror else "west"
        body += [rf"\node[anchor={anchor}, inner sep=1pt] at {_P(X_(w - c1 + 0.04), hh - 0.2)} {{{_lab(ch, u)}}};",
                 rf"\node[anchor=south, inner sep=1pt] at {_P(X_(w - c1 / 2), hh - c2 + 0.03)} {{{_lab(cw, u)}}};"]
    else:
        body += [rf"\node[above] at {_P(X_((w - c1) / 2), hh)} {{{_lab(W - cw, u)}}};",
                 rf"\node[{'left' if mirror else 'right'}] at {_P(X_(w), (hh - c2) / 2)} {{{_lab(H - ch, u)}}};"]
    return _tikz(body)


@template("MK")
def composite(rng, lvl):
    ctx, u = rng.choice([("the floor plan of a room", "ft"), ("a garden", rng.choice(["ft", "yd", "m"])),
                         ("the floor of a storage building", "ft"), ("a parking lot", rng.choice(["yd", "m"])),
                         ("the floor of a barracks day room", "ft"), ("a deck", "ft"), ("a lawn", "yd")])
    W = rng.randint(10, 30)
    H = rng.randint(8, 24)
    cw = rng.randint(3, W - 4)
    ch = rng.randint(3, H - 3)
    need(cw * 4 >= W and ch * 4 >= H and W != H and cw * 10 <= W * 7 and ch * 10 <= H * 7)
    label_cut = lvl <= 2 and rng.random() < 0.4
    fig = _l_shape_fig(W, H, cw, ch, u, rng.random() < 0.5, label_cut)
    if label_cut:
        known = (f"The outside measures {_w(W, u)} by {_w(H, u)}, and the corner cut out of it measures "
                 f"{_w(cw, u)} by {_w(ch, u)}.")
        find_cut = []
    else:
        known = (f"The sides shown measure {_w(W, u)}, {_w(H, u)}, {_w(W - cw, u)}, and {_w(H - ch, u)}.")
        find_cut = [f"Find the missing corner: it is {m(f'{W} - {W - cw} = {cw}')} {u} wide and "
                    f"{m(f'{H} - {H - ch} = {ch}')} {u} tall."]
    area = W * H - cw * ch
    per = 2 * (W + H)
    if lvl <= 2:
        stem = (f"The figure shows {ctx}. All corners are right angles. {known} What is the area?")
        ans, fmt = Q(area), _areafmt(u)
        wrong = [(Q(W * H), "forgets to subtract the missing corner"),
                 (Q((W - cw) * (H - ch)), "multiplies the two shorter sides only"),
                 (Q(W * H - (W - cw) * (H - ch)), "subtracts the wrong rectangle"),
                 (Q(per), "gives the perimeter, not the area")]
        steps = find_cut + [
            f"Area of the whole {m(f'{W} \\times {H}')} rectangle: {m(f'{W} \\times {H} = {int_raw(W * H)}')}.",
            f"Subtract the missing corner: {m(f'{int_raw(W * H)} - {cw} \\times {ch} = {int_raw(W * H)} - {int_raw(cw * ch)} = {int_raw(area)}')} "
            f"square {_UNITS[u][1]}."]
        tip = (f"Or split the shape into two rectangles: {m(f'{W - cw} \\times {H} = {int_raw((W - cw) * H)}')} and "
               f"{m(f'{cw} \\times {H - ch} = {int_raw(cw * (H - ch))}')}; {m(f'{int_raw((W - cw) * H)} + {int_raw(cw * (H - ch))} = {int_raw(area)}')}.")
        check = Q((W - cw) * H + cw * (H - ch))
    else:
        stem = (f"The figure shows {ctx}. All corners are right angles. {known} What is the perimeter?")
        ans, fmt = Q(per), _lenfmt(u)
        wrong = [(Q(W + H + (W - cw) + (H - ch)) if not label_cut else Q(W + H + cw + ch),
                  "adds only the four labeled sides and leaves out the other edges" if label_cut else
                  "adds only the four labeled sides and leaves out the two edges of the cut-out corner"),
                 (Q(area), "gives the area, not the perimeter"),
                 (Q(per + cw + ch), "counts the two inside edges twice")]
        steps = find_cut + [
            f"Go around the shape and add all six sides: "
            f"{m(f'{W} + {H - ch} + {cw} + {ch} + {W - cw} + {H} = {int_raw(per)}')} {_UNITS[u][1]}."]
        tip = (f"Shortcut: the two inside edges together make up for the missing pieces of the top and side, so the "
               f"perimeter equals that of a {m(f'{W} \\times {H}')} rectangle: {m(f'2 \\times ({W} + {H}) = {int_raw(per)}')}.")
        check = Q(W + (H - ch) + cw + ch + (W - cw) + H)
    return Problem(stem=stem, answer=ans, fmt=fmt, wrong=wrong, steps=steps, tip=tip, figure=fig,
                   near=_near_int(ans, (4, 8, 10, 20)), check=check)


@template("AR")
def cost_word(rng, lvl):
    who = person(rng)
    s = soldier(rng)
    ctx = rng.choice(["carpet", "fence", "fence_mil", "tile", "seal", "trim", "paint"])
    if ctx == "carpet":
        L, W = rng.randint(10, 20), rng.randint(9, 16)
        price = rng.choice([R(2), R(5, 2), R(3), R(7, 2), R(4), R(9, 2), R(5)])
        need(L > W)
        area, per = L * W, 2 * (L + W)
        ans = area * price
        stem = (f"{who.name} wants to carpet a bedroom that is {m(L)} feet long and {m(W)} feet wide. Carpet costs "
                f"{money(price)} per square foot, installed. How much will the carpet cost?")
        wrong = [(per * price, "uses the perimeter instead of the area"),
                 ((L + W) * price, "adds the length and width instead of multiplying"),
                 (Q(area), "finds the area but forgets to multiply by the price")]
        steps = [f"Carpet covers the floor, so find the area: {m(f'{L} \\times {W} = {int_raw(area)}')} square feet.",
                 f"Multiply by the price per square foot: {m(f'{int_raw(area)} \\times {dec_raw(price)} = {dec_raw(ans)}')}, "
                 f"so the carpet costs {money(ans)}."]
        fmt = money
        check = Q(L) * W * price
    elif ctx in ("fence", "fence_mil"):
        L, W = rng.randrange(30, 85, 5), rng.randrange(20, 65, 5)
        price = rng.randint(8, 20)
        need(L > W)
        per = 2 * (L + W)
        ans = Q(per * price)
        if ctx == "fence":
            stem = (f"{who.name} is putting a fence around a rectangular yard that measures {m(L)} feet by {m(W)} feet. "
                    f"Fencing costs {money(price)} per foot. How much will it cost to fence the whole yard?")
        else:
            stem = (f"{s} must fence a rectangular equipment yard on base that measures {m(L)} feet by {m(W)} feet. "
                    f"The fencing costs {money(price)} per foot. What is the total cost of the fence?")
        wrong = [(Q((L + W) * price), "fences only one length and one width (half the perimeter)"),
                 (Q((2 * L + W) * price), "leaves out one side"),
                 (Q(L * W * price), "uses the area instead of the perimeter")]
        steps = [f"A fence goes around the edge, so find the perimeter: "
                 f"{m(f'2 \\times {L} + 2 \\times {W} = {2 * L} + {2 * W} = {int_raw(per)}')} feet.",
                 f"Multiply by the price per foot: {m(f'{int_raw(per)} \\times {price} = {int_raw(ans)}')}, so the fence costs "
                 f"{money(ans)}."]
        fmt = money
        check = Q(L + W + L + W) * price
    elif ctx == "tile":
        t = rng.choice([2, 3])
        L, W = t * rng.randint(4, 10), t * rng.randint(3, 8)
        need(L != W)
        area = L * W
        ans = Q(area) / (t * t)
        place = rng.choice(["kitchen floor", "patio", "barracks hallway floor", "bathroom floor"])
        stem = (f"A {place} is a rectangle {m(L)} feet by {m(W)} feet. It will be covered with square tiles that "
                f"measure {m(t)} feet on each side. How many tiles are needed?")
        wrong = [(Q(area) / t, f"divides by the side of a tile ({m(t)}) instead of its area ({m(t * t)})"),
                 (Q(area), f"forgets that each tile covers {m(t * t)} square feet"),
                 (Q(2 * (L + W)) / t, "works with the perimeter instead of the area")]
        steps = [f"Area of the floor: {m(f'{L} \\times {W} = {int_raw(area)}')} square feet.",
                 f"Each tile covers {m(f'{t} \\times {t} = {t * t}')} square feet.",
                 f"Number of tiles: {m(f'{int_raw(area)} \\div {t * t} = {int_raw(ans)}')}."]
        tip = (f"Or count tiles along each side: {m(f'{L} \\div {t} = {L // t}')} by {m(f'{W} \\div {t} = {W // t}')}, "
               f"and {m(f'{L // t} \\times {W // t} = {int_raw(ans)}')}.")
        return Problem(stem=stem, answer=ans, fmt=num, wrong=wrong, steps=steps, tip=tip, section="AR",
                       near=_near_int(ans, (2, 4, 5, 10)), check=Q(L // t) * (W // t))
    elif ctx == "seal":
        L, W = rng.randrange(20, 65, 5), rng.randrange(10, 45, 5)
        price = rng.choice([R(1, 2), R(1, 4), R(3, 4), R(6, 5), R(3, 2)])
        need(L > W)
        area = L * W
        ans = area * price
        stem = rng.choice([
            f"A rectangular concrete pad in the motor pool measures {m(L)} feet by {m(W)} feet. Sealing it costs "
            f"{money(price)} per square foot. What is the total cost to seal the pad?",
            f"{who.name} is covering a rectangular lawn {m(L)} feet by {m(W)} feet with sod that costs "
            f"{money(price)} per square foot. How much will the sod cost?"])
        wrong = [(2 * (L + W) * price, "uses the perimeter instead of the area"),
                 ((L + W) * price, "adds the length and width instead of multiplying"),
                 (Q(area), "finds the area but forgets to multiply by the price")]
        steps = [f"Find the area: {m(f'{L} \\times {W} = {int_raw(area)}')} square feet.",
                 f"Multiply by the price: {m(f'{int_raw(area)} \\times {dec_raw(price)} = {dec_raw(ans)}')}, so the cost is "
                 f"{money(ans)}."]
        fmt = money
        check = Q(L) * W * price
    elif ctx == "trim":
        L, W = rng.randint(10, 20), rng.randint(9, 16)
        price = rng.choice([R(3, 2), R(2), R(5, 2), R(3)])
        need(L > W)
        per = 2 * (L + W)
        ans = per * price
        stem = (f"{who.name} is putting new baseboard trim along all four walls of a room that is {m(L)} feet by "
                f"{m(W)} feet. Trim costs {money(price)} per foot. Ignoring the doorway, how much will the trim cost?")
        wrong = [(Q(L * W) * price, "uses the area instead of the perimeter"),
                 ((L + W) * price, "covers only two of the four walls"),
                 (Q(per), "finds the perimeter but forgets to multiply by the price")]
        steps = [f"Trim runs along the walls, so find the perimeter: "
                 f"{m(f'2 \\times {L} + 2 \\times {W} = {int_raw(per)}')} feet.",
                 f"Multiply by the price: {m(f'{int_raw(per)} \\times {dec_raw(price)} = {dec_raw(ans)}')}, so the trim costs "
                 f"{money(ans)}."]
        fmt = money
        check = Q(L + W + L + W) * price
    else:
        L, Hh = rng.randint(10, 24), rng.choice([8, 9, 10])
        dw, dh = rng.choice([(3, 7), (4, 7), (6, 7)])
        area = L * Hh - dw * dh
        ans = Q(area)
        stem = (f"{who.name} is painting one wall of a room. The wall is {m(L)} feet wide and {m(Hh)} feet high, and "
                f"it has a door that is {m(dw)} feet wide and {m(dh)} feet high. How many square feet of wall will "
                f"{who.he} paint?")
        wrong = [(Q(L * Hh), "forgets to subtract the door"),
                 (Q(L * Hh + dw * dh), "adds the door instead of subtracting it"),
                 (Q(2 * (L + Hh)), "finds the perimeter of the wall")]
        steps = [f"Area of the whole wall: {m(f'{L} \\times {Hh} = {int_raw(L * Hh)}')} square feet.",
                 f"Area of the door: {m(f'{dw} \\times {dh} = {int_raw(dw * dh)}')} square feet.",
                 f"Paint covers the wall but not the door: {m(f'{int_raw(L * Hh)} - {int_raw(dw * dh)} = {int_raw(area)}')} square feet."]
        return Problem(stem=stem, answer=ans, fmt=_areafmt("ft"), wrong=wrong, steps=steps, section="AR",
                       near=_near_int(ans, (4, 6, 10, 12)), check=Q(sum([Hh] * L) - sum([dh] * dw)))
    return Problem(stem=stem, answer=ans, fmt=fmt, wrong=wrong, steps=steps, section="AR",
                   near=_near_int(ans, (10, 20, 25, 50)), check=check)


# --------------------------------------------------------------------------
# level 3
# --------------------------------------------------------------------------

@template("AR")
def square_yards(rng, lvl):
    who = person(rng)
    L, W = 3 * rng.randint(3, 8), 3 * rng.randint(3, 6)
    need(L != W)
    sqft = L * W
    sqyd = Q(sqft) / 9
    if rng.random() < 0.6:
        price = rng.choice([15, 18, 20, 24, 25, 30, 32, 35, 40])
        ans = sqyd * price
        room = rng.choice(["living room", "bedroom", "office", "dayroom in the barracks", "recreation room"])
        stem = (f"{who.name} is buying carpet for {"an" if room[0] in "aeiou" else "a"} {room} that measures {m(L)} feet by {m(W)} feet. The carpet costs "
                f"{money(price)} per square yard. What is the cost of the carpet?")
        wrong = [(Q(sqft * price), "forgets to change square feet to square yards"),
                 (Q(sqft) / 3 * price, "divides by 3 instead of 9 (a square yard is 3 ft by 3 ft)"),
                 (sqyd, "finds the number of square yards but forgets to multiply by the price")]
        steps = [f"Change each length to yards: {m(f'{L} \\div 3 = {L // 3}')} yd and {m(f'{W} \\div 3 = {W // 3}')} yd.",
                 f"Area in square yards: {m(f'{L // 3} \\times {W // 3} = {int_raw(sqyd)}')} square yards.",
                 f"Cost: {m(f'{int_raw(sqyd)} \\times {price} = {int_raw(ans)}')}, so the carpet costs {money(ans)}."]
        tip = (f"Or find square feet first ({m(f'{L} \\times {W} = {int_raw(sqft)}')}) and divide by 9: "
               f"{m(f'{int_raw(sqft)} \\div 9 = {int_raw(sqyd)}')} square yards.")
        return Problem(stem=stem, answer=ans, fmt=money, wrong=wrong, steps=steps, tip=tip, section="AR",
                       near=_near_int(ans, (20, 40, 50, 100)), check=Q(sqft) * price / 9)
    stem = choose(rng,
                  f"A room measures {m(L)} feet by {m(W)} feet. What is the area of the floor in square yards?",
                  f"How many square yards of carpet are needed to cover a floor that is {m(L)} feet by {m(W)} feet?",
                  f"{who.name}'s patio is {m(L)} feet long and {m(W)} feet wide. What is its area in square yards?")
    return Problem(
        stem=stem,
        answer=sqyd,
        fmt=_areafmt("yd"),
        wrong=[(Q(sqft) / 3, "divides by 3 instead of 9 (a square yard is 3 ft by 3 ft)"),
               (Q(sqft), "gives the area in square feet"),
               (Q(sqft * 9), "multiplies by 9 instead of dividing")],
        steps=[f"Change each length to yards (3 feet = 1 yard): {m(f'{L} \\div 3 = {L // 3}')} yd and "
               f"{m(f'{W} \\div 3 = {W // 3}')} yd.",
               f"Area: {m(f'{L // 3} \\times {W // 3} = {int_raw(sqyd)}')} square yards."],
        tip=(f"Check: {m(f'{L} \\times {W} = {int_raw(sqft)}')} square feet, and {m(f'{int_raw(sqft)} \\div 9 = {int_raw(sqyd)}')}, "
             "because 1 square yard is 9 square feet."),
        section="AR",
        near=_near_int(sqyd, (2, 4, 5, 10)),
        check=Q(L // 3) * (W // 3),
    )


@template("AR")
def walkway(rng, lvl):
    who = person(rng)
    kind = rng.choice(["pool", "garden", "pad", "lawn", "rug", "frame"])
    if kind == "frame":                                   # a framed photo, in inches
        u, uw = "in", "inches"
        L, W, k = rng.choice([(10, 8), (14, 11), (12, 8), (20, 16), (24, 18), (16, 12)]) + (rng.choice([1, 2, 3]),)
    elif kind == "rug":                                   # bare floor around a centered rug
        u, uw = "ft", "feet"
        L, W = rng.choice([(8, 5), (9, 6), (10, 8), (12, 9), (14, 10), (12, 8)])
        k = rng.choice([1, 2, 3])
    else:
        u, uw = "ft", "feet"
        L = rng.randrange(12, 41, 2)
        W = rng.randrange(8, 25, 2)
        k = rng.choice([2, 3, 4, 5])
    need(L > W)
    outer = (L + 2 * k) * (W + 2 * k)
    ans = Q(outer - L * W)
    inner_name, outer_name, ctx = {
        "pool": ("pool", "walkway", f"A rectangular swimming pool is {m(L)} feet long and {m(W)} feet wide. A concrete "
                                    f"walkway {m(k)} feet wide surrounds the pool."),
        "garden": ("garden", "border", f"{who.name}'s rectangular garden is {m(L)} feet by {m(W)} feet. {who.He} puts a "
                                       f"gravel border {m(k)} feet wide around the outside of the garden."),
        "pad": ("landing pad", "border", f"A rectangular helicopter landing pad on base measures {m(L)} feet by {m(W)} "
                                         f"feet. It is surrounded by a gravel border {m(k)} feet wide."),
        "lawn": ("lawn", "path", f"A rectangular lawn {m(L)} feet by {m(W)} feet has a brick path {m(k)} feet wide "
                                 f"all the way around it."),
        "rug": ("rug", "bare floor", f"A {m(L)}-foot by {m(W)}-foot rug is centered in a rectangular room, leaving a "
                                     f"strip of bare floor {m(k)} {'foot' if k == 1 else 'feet'} wide along every wall."),
        "frame": ("photo", "frame", f"A photo {m(L)} inches by {m(W)} inches is surrounded by a frame "
                                    f"{m(k)} {'inch' if k == 1 else 'inches'} wide on every side."),
    }[kind]
    stem = f"{ctx} What is the area of the {outer_name} alone?"
    sc = min(3.9 / (L + 2 * k), 2.8 / (W + 2 * k))
    OL, OW, KK = (L + 2 * k) * sc, (W + 2 * k) * sc, k * sc
    IW, IH = L * sc, W * sc
    need(IH >= 1.3 and IW >= 1.8, "inner rectangle too small for its labels")
    yk = OW - KK - 0.3
    fig = _tikz([rf"\fill[black!15] (0,0) rectangle {_P(OL, OW)};",
                 rf"\draw[thick] (0,0) rectangle {_P(OL, OW)};",
                 rf"\fill[white] {_P(KK, KK)} rectangle {_P(OL - KK, OW - KK)};",
                 rf"\draw[thick] {_P(KK, KK)} rectangle {_P(OL - KK, OW - KK)};",
                 rf"\node[anchor=north, inner sep=2pt] at {_P(KK + IW / 2, OW - KK)} {{{_lab(L, u)}}};",
                 rf"\node[anchor=west, inner sep=2pt] at {_P(KK, KK + IH / 2)} {{{_lab(W, u)}}};",
                 rf"\node[anchor=south, inner sep=2pt] at {_P(KK + IW / 2 + 0.2, KK)} {{\footnotesize {inner_name}}};",
                 rf"\draw[<->, >=stealth] {_P(OL - KK, yk)} -- {_P(OL, yk)};",
                 rf"\node[right] at {_P(OL, yk)} {{{_lab(k, u)}}};"])
    sq = f"square {uw}"
    return Problem(
        stem=stem,
        answer=ans,
        fmt=_areafmt(u),
        wrong=[(Q((L + k) * (W + k) - L * W), f"adds the {outer_name} width to only one end of each side"),
               (Q(outer), f"gives the total area, including the {inner_name}"),
               (Q(2 * (L + W) * k), "multiplies the perimeter by the width and misses the four corner squares"),
               (Q(L * W), f"gives the area of the {inner_name}")],
        steps=[f"The {outer_name} adds {m(k)} {uw if k != 1 else ('inch' if u == 'in' else 'foot')} on \\emph{{both}} "
               f"ends of each side, so the outer rectangle is "
               f"{m(f'{L} + 2 \\times {k} = {L + 2 * k}')} by {m(f'{W} + 2 \\times {k} = {W + 2 * k}')} {uw}.",
               f"Outer area: {m(f'{L + 2 * k} \\times {W + 2 * k} = {int_raw(outer)}')} {sq}.",
               f"{inner_name.capitalize()} area: {m(f'{L} \\times {W} = {int_raw(L * W)}')} {sq}.",
               f"{outer_name.capitalize()} alone: {m(f'{int_raw(outer)} - {int_raw(L * W)} = {int_raw(ans)}')} {sq}."],
        figure=fig,
        section="AR",
        near=_near_int(ans, (4, 8, 12, 16) if ans < 100 else (8, 12, 16, 20)),
        check=Q(2 * k * (L + 2 * k) + 2 * k * W),       # two long strips (with corners) + two short strips
    )


@template("MK")
def scale_change(rng, lvl):
    mode = rng.choice(["factor", "rect_new", "square_new", "perimeter"])
    # (factor mode skips k = 2, where "2k" and the answer k^2 would both be 4)
    k = rng.choice([2, 3, 4, 5]) if mode != "factor" else rng.choice([3, 4, 5, 10])
    word = {2: "doubled", 3: "tripled", 4: "multiplied by 4", 5: "multiplied by 5", 10: "multiplied by 10"}[k]
    if mode == "factor":
        shape = rng.choice(["square", "rectangle", "triangle"])
        part = {"square": "each side of a square is", "rectangle": "the length and the width of a rectangle are both",
                "triangle": "the base and the height of a triangle are both"}[shape]
        if rng.random() < 0.6:
            stem = (f"If {part} {word}, the area of the {shape} is multiplied by what number?")
            ans = Q(k * k)
            wrong = [(Q(k), "assumes the area grows by the same factor as the sides"),
                     (Q(2 * k), "doubles the scale factor instead of squaring it"),
                     (Q(k ** 3), "cubes the factor, which is how volume changes, not area")]
            steps = [f"Area multiplies two lengths together, and each length is multiplied by {m(k)}.",
                     f"So the area is multiplied by {m(f'{k} \\times {k} = {k * k}')}."]
            tip = f"Try numbers: a 1-by-1 square has area 1; a {k}-by-{k} square has area {k * k}."
            return Problem(stem=stem, answer=ans, fmt=num, wrong=wrong, steps=steps, tip=tip, check=Q(k) ** 2,
                           near=lambda r: [])
        # reverse: the area factor is given; find the side factor
        k = rng.choice([4, 6, 8, 10])
        stem = choose(rng,
                      f"Each side of a square is multiplied by the same number, and the area of the square becomes "
                      f"{m(k * k)} times as large. By what number was each side multiplied?",
                      f"A square photo is enlarged so that its area is {m(k * k)} times as large. By what number "
                      f"was the length of each side multiplied?")
        wrong = [(Q(k * k), "gives the area factor itself"),
                 (Q(k * k) / 2, "halves the area factor instead of taking its square root"),
                 (Q(k ** 4), "squares the area factor instead of taking its square root")]
        steps = [f"If each side is multiplied by {m('k')}, the area is multiplied by {m('k^2')}.",
                 f"So {m(f'k^2 = {k * k}')}, and {m(f'k = \\sqrt{{{k * k}}} = {k}')}."]
        return Problem(stem=stem, answer=Q(k), fmt=num, wrong=wrong, steps=steps,
                       tip=f"Check: {m(f'{k} \\times {k} = {k * k}')}.",
                       check=sp.sqrt(k * k), near=lambda r: [])
    u = rng.choice(["ft", "in", "m", "cm"])
    if mode == "rect_new":
        L, W = rng.randint(3, 12), rng.randint(2, 9)
        need(L != W and k * L <= 40)
        A = L * W
        ans = Q(A * k * k)
        stem = (f"A rectangle is {_w(L, u)} long and {_w(W, u)} wide. If both its length and its width are {word}, "
                f"what is the area of the new rectangle?")
        wrong = [(Q(A * k), f"multiplies the area by {m(k)} instead of {m(k * k)}"),
                 (Q(A), "gives the original area"),
                 (Q((L + k) * (W + k)), f"adds {m(k)} to the length and the width instead of multiplying"),
                 (Q(2 * (k * L + k * W)), "finds the new perimeter instead of the new area"),
                 (Q(A * k ** 3), f"multiplies the area by {m(k ** 3)}, which is how volume changes, not area")]
        steps = [f"New sides: {m(f'{L} \\times {k} = {L * k}')} and {m(f'{W} \\times {k} = {W * k}')} {u}.",
                 f"New area: {m(f'{L * k} \\times {W * k} = {int_raw(ans)}')} square {_UNITS[u][1]}."]
        tip = f"Check: the old area is {m(f'{L} \\times {W} = {int_raw(A)}')}, and {m(f'{int_raw(A)} \\times {k * k} = {int_raw(ans)}')}."
        check = Q(A) * k ** 2
        fmt = _areafmt(u)
    elif mode == "square_new":
        sd = rng.randint(2, 10)
        A = sd * sd
        ans = Q(A * k * k)
        stem = (f"A square has an area of {_sq(A, u)}. If each side of the square is {word}, what is the area of "
                f"the new square?")
        wrong = [(Q(A * k), f"multiplies the area by {m(k)} instead of {m(k * k)}"),
                 (Q(4 * sd * k), "gives the new perimeter instead of the new area"),
                 (Q((sd + k) ** 2), f"adds {m(k)} to the side instead of multiplying"),
                 (Q(A), "gives the original area"),
                 (Q(A * k ** 3), f"multiplies the area by {m(k ** 3)}, which is how volume changes, not area")]
        steps = [f"The original side is {m(sd)} {u}, because {m(f'{sd} \\times {sd} = {int_raw(A)}')}.",
                 f"The new side is {m(f'{sd} \\times {k} = {sd * k}')} {u}.",
                 f"New area: {m(f'{sd * k} \\times {sd * k} = {int_raw(ans)}')} square {_UNITS[u][1]}."]
        tip = None
        check = sp.sqrt(A) ** 2 * k ** 2
        fmt = _areafmt(u)
    else:
        L, W = rng.randint(3, 15), rng.randint(2, 12)
        need(L != W)
        Pm = 2 * (L + W)
        ans = Q(Pm * k)
        stem = (f"A rectangle has a perimeter of {_w(Pm, u)}. If its length and width are both {word}, what is "
                f"the perimeter of the new rectangle?")
        wrong = [(Q(Pm * k * k), f"multiplies by {m(k * k)}, which is how the area changes"),
                 (Q(2 * ((L + k) + (W + k))), f"adds {m(k)} to the length and to the width instead of multiplying"),
                 (Q(Pm), "gives the original perimeter"),
                 (Q(2 * (k * L + W)), f"multiplies only the length by {m(k)}")]
        steps = [f"Perimeter is a length (a sum of sides), so when every side is multiplied by {m(k)}, the "
                 f"perimeter is multiplied by {m(k)} too.",
                 f"{m(f'{int_raw(Pm)} \\times {k} = {int_raw(ans)}')}, so the new perimeter is {_w(ans, u)}."]
        tip = None
        fmt = _lenfmt(u)
        stem = stem.replace(f"A rectangle has a perimeter of {_w(Pm, u)}.",
                            f"A rectangle that is {_w(L, u)} by {_w(W, u)} has a perimeter of {_w(Pm, u)}.")
        check = Q(2 * (k * L + k * W))
    return Problem(stem=stem, answer=ans, fmt=fmt, wrong=wrong, steps=steps, tip=tip, check=check,
                   near=lambda r: [])


PLAN = [
    # (template, level, count) -- easy -> hard; 25 problems
    (rect_basic, 1, 3),
    (triangle_area, 1, 3),
    (missing_side, 1, 2),
    (parallelogram, 2, 2),
    (trapezoid, 2, 2),
    (composite, 2, 2),
    (cost_word, 2, 2),
    (triangle_area, 2, 1),
    (missing_side, 2, 1),
    (square_yards, 3, 2),
    (walkway, 3, 2),
    (scale_change, 3, 2),
    (composite, 3, 1),
]
