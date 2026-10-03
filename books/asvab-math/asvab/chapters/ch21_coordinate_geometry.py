"""Chapter 21 - Coordinate Geometry."""
import math

import sympy as sp

from ..core import (R, Q, Problem, need, num, frac, text, m, F, int_raw, frac_raw, choose,
                    template)

NUM = 21
TITLE = "Coordinate Geometry"
PART = 3

INTRO = r"""
The coordinate plane is a map: every point has an address $(x, y)$. The
$x$-coordinate tells you how far to go right ($+$) or left ($-$); the
$y$-coordinate tells you how far to go up ($+$) or down ($-$). Always
$x$ first, then $y$.

\begin{concept}{Points and quadrants}
\begin{minipage}[c]{0.56\linewidth}
The axes split the plane into four \textbf{quadrants}, numbered
counterclockwise starting at the upper right:
\begin{itemize}
\item Quadrant I: $(+, +)$ \quad Quadrant II: $(-, +)$
\item Quadrant III: $(-, -)$ \quad Quadrant IV: $(+, -)$
\end{itemize}
A point on an axis is in no quadrant. The point $(3, 2)$ is 3 units right
and 2 units up from the origin $(0, 0)$.
\end{minipage}\hfill
\begin{minipage}[c]{0.4\linewidth}\centering
\begin{tikzpicture}[scale=0.42]
\draw[black!20, very thin] (-4,-3) grid (4,3);
\draw[-{Stealth[length=4pt]}] (-4.3,0) -- (4.5,0) node[right] {\small $x$};
\draw[-{Stealth[length=4pt]}] (0,-3.3) -- (0,3.5) node[above] {\small $y$};
\node at (2.3,2.5) {\small I};
\node at (-2.3,2.5) {\small II};
\node at (-2.3,-2.3) {\small III};
\node at (2.3,-2.3) {\small IV};
\draw[dashed] (3,0) -- (3,2) -- (0,2);
\fill (3,2) circle (4pt) node[right] {\scriptsize $(3,2)$};
\end{tikzpicture}
\end{minipage}
\end{concept}

\begin{concept}{Slope}
Slope measures steepness: \textbf{rise over run}.
\[ m = \frac{\text{rise}}{\text{run}} = \frac{y_2 - y_1}{x_2 - x_1} \]
A positive slope goes up to the right, a negative slope goes down to the
right, a horizontal line has slope $0$, and a vertical line has no slope
(undefined). \textbf{Parallel} lines have equal slopes.
\textbf{Perpendicular} lines have slopes that are negative reciprocals:
flip the fraction \emph{and} change the sign ($\frac{2}{3}$ and
$-\frac{3}{2}$).
\end{concept}

\begin{concept}{Equations of lines}
In \textbf{slope-intercept form} $y = mx + b$, $m$ is the slope and $b$ is
the $y$-intercept (where the line crosses the $y$-axis). To read the slope
of an equation like $2x + 3y = 12$, solve for $y$ first:
$3y = -2x + 12$, so $y = -\frac{2}{3}x + 4$. To find the $x$-intercept, set
$y = 0$; for the $y$-intercept, set $x = 0$. A point is on a line exactly
when its coordinates make the equation true.
\end{concept}

\begin{concept}{Distance and midpoint}
For points $(x_1, y_1)$ and $(x_2, y_2)$:
\[ d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2} \qquad
   M = \left(\frac{x_1 + x_2}{2},\ \frac{y_1 + y_2}{2}\right) \]
The distance formula is the Pythagorean theorem: the horizontal and vertical
changes are the legs of a right triangle.
\end{concept}

\begin{example}{Worked example}
Find the equation of the line through $(1, 2)$ and $(3, 8)$.

\textbf{Solution.} Slope: $m = \frac{8 - 2}{3 - 1} = \frac{6}{2} = 3$.
Put $(1, 2)$ into $y = 3x + b$: $2 = 3 + b$, so $b = -1$. The line is
$y = 3x - 1$. Check with $(3, 8)$: $3 \times 3 - 1 = 8$. \checkmark
\end{example}

\begin{tip}
Check a line by plugging in a point. For distances, look for Pythagorean
triples: $3$-$4$-$5$, $6$-$8$-$10$, $5$-$12$-$13$, $8$-$15$-$17$. If the
legs are 6 and 8, the distance is 10, with no square roots needed.
\end{tip}

\begin{trap}
\begin{itemize}
\item Putting the run on top: slope is $\frac{\text{change in } y}{\text{change in } x}$.
\item Subtracting in different orders on top and bottom (sign error).
\item Perpendicular slope: changing the sign \emph{or} flipping, instead of both.
\item Reading $y = 4 - 2x$ as slope $4$; the slope is the number with $x$, so it is $-2$.
\end{itemize}
\end{trap}
"""

ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV"}


# --------------------------------------------------------------------------
# text helpers
# --------------------------------------------------------------------------

def _pr(a_, b_):
    """Raw '(3, -2)'."""
    return f"({frac_raw(a_)}, {frac_raw(b_)})"


def _pt(a_, b_):
    return m(_pr(a_, b_))


def _coef(k, var="x"):
    """Raw coefficient times var: 3x, -x, \\frac{2}{3}x, -\\frac{1}{2}x."""
    k = Q(k)
    if k == 1:
        return var
    if k == -1:
        return "-" + var
    return frac_raw(k) + var


def _line_raw(m_, b_):
    """Raw 'y = 3x - 1' (slope-intercept form)."""
    m_, b_ = Q(m_), Q(b_)
    if m_ == 0:
        return f"y = {frac_raw(b_)}"
    s = f"y = {_coef(m_)}"
    if b_ > 0:
        s += f" + {frac_raw(b_)}"
    elif b_ < 0:
        s += f" - {frac_raw(-b_)}"
    return s


def _std_raw(A, B, C):
    """Raw 'Ax + By = C' with tidy signs: 2x - 3y = 12."""
    s = _coef(A)
    if B > 0:
        s += " + " + _coef(B, "y")
    else:
        s += " - " + _coef(-B, "y")
    return f"{s} = {int_raw(C)}"


def _sub(a_, b_):
    """Raw 'a - b' with parentheses around a negative b: 3 - (-2)."""
    b_ = Q(b_)
    return f"{frac_raw(a_)} - {'(' + frac_raw(b_) + ')' if b_ < 0 else frac_raw(b_)}"


def _add(a_, b_):
    b_ = Q(b_)
    return f"{frac_raw(a_)} + {'(' + frac_raw(b_) + ')' if b_ < 0 else frac_raw(b_)}"


def _par(v):
    """Parenthesize a negative number for products: 3(-2)."""
    v = Q(v)
    return f"({frac_raw(v)})" if v < 0 else frac_raw(v)


def _times_val(k, v):
    """Raw 'k(v)' for substituting: 3(2), -(4), \\frac{1}{2}(6), (5) for k = 1."""
    k = Q(k)
    pre = "" if k == 1 else "-" if k == -1 else frac_raw(k)
    return f"{pre}({frac_raw(v)})"


def _ratio(top, bot):
    """Raw '\\frac{top}{bot}' followed by '= simplified' when it reduces."""
    out = F(int_raw(top), int_raw(bot))
    v = R(top, bot)
    if (v.p, v.q) != (top, bot) or v.q == 1:
        out += " = " + frac_raw(v)
    return out


def _pm(b_):
    """Raw ' + 3' or ' - 3'."""
    return f" + {frac_raw(b_)}" if Q(b_) > 0 else f" - {frac_raw(-Q(b_))}"


def _quad(a_, b_):
    """Quadrant from the angle of the point (independent of the sign table)."""
    ang = sp.atan2(b_, a_)
    if ang < 0:
        ang += 2 * sp.pi
    return int(sp.floor(ang / (sp.pi / 2))) + 1


def _quad_fmt(v):
    v = Q(v)
    need(v.is_integer and 1 <= v <= 4, "not a quadrant")
    return f"Quadrant {ROMAN[int(v)]}"


# --------------------------------------------------------------------------
# coordinate-grid figure
# --------------------------------------------------------------------------

def _grid(points=(), lim=5, scale=0.3, segs=(), line=None, ticks=(-4, -2, 2, 4), dashed=()):
    """TikZ grid from -lim..lim. points: (x, y, label, anchor)."""
    out = [rf"\begin{{tikzpicture}}[scale={scale}]",
           rf"\draw[black!22, very thin] (-{lim},-{lim}) grid ({lim},{lim});",
           rf"\draw[-{{Stealth[length=3pt]}}] (-{lim + 0.5},0) -- ({lim + 0.7},0) node[right] {{\scriptsize $x$}};",
           rf"\draw[-{{Stealth[length=3pt]}}] (0,-{lim + 0.5}) -- (0,{lim + 0.7}) node[above] {{\scriptsize $y$}};"]
    for t in ticks:
        out.append(rf"\node[below, inner sep=1pt, fill=white] at ({t},-0.1) {{\tiny ${t}$}};")
        out.append(rf"\node[left, inner sep=1pt, fill=white] at (-0.1,{t}) {{\tiny ${t}$}};")
    if line is not None:
        (x1, y1), (x2, y2) = line
        out.append(r"\begin{scope}")
        out.append(rf"\clip (-{lim},-{lim}) rectangle ({lim},{lim});")
        dx, dy = x2 - x1, y2 - y1
        t = 20 / max(abs(dx), abs(dy))
        out.append(rf"\draw[thick] ({x1 - t * dx},{y1 - t * dy}) -- ({x1 + t * dx},{y1 + t * dy});")
        out.append(r"\end{scope}")
    for (p1, p2) in segs:
        out.append(rf"\draw[thick] ({p1[0]},{p1[1]}) -- ({p2[0]},{p2[1]});")
    for (p1, p2) in dashed:
        out.append(rf"\draw[dashed] ({p1[0]},{p1[1]}) -- ({p2[0]},{p2[1]});")
    for (px, py, lab, anchor) in points:
        out.append(rf"\fill ({px},{py}) circle (5pt);")
        if lab:
            out.append(rf"\node[{anchor}, inner sep=1.5pt, fill=white] at ({px},{py}) {{\scriptsize {lab}}};")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def _anchor(px, py):
    """Label position that points away from the origin."""
    return ("above " if py >= 0 else "below ") + ("right" if px >= 0 else "left")


# --------------------------------------------------------------------------
# templates
# --------------------------------------------------------------------------

@template("MK")
def quadrant(rng, lvl):
    a_ = rng.choice([v for v in range(-12, 13) if v])
    b_ = rng.choice([v for v in range(-12, 13) if v])
    need(abs(a_) != abs(b_))
    q = _quad(a_, b_)
    sx, sy = (a_ > 0), (b_ > 0)
    style = rng.choice(["point", "point", "signs"])
    if style == "point":
        stem = choose(rng, f"In which quadrant does the point {_pt(a_, b_)} lie?",
                      f"The point {_pt(a_, b_)} is plotted on a coordinate plane. In which quadrant is it?")
    else:
        lr = "positive" if sx else "negative"
        ud = "positive" if sy else "negative"
        stem = (f"Point {m('P')} has a {lr} {m('x')}-coordinate and a {ud} {m('y')}-coordinate. "
                f"In which quadrant is point {m('P')}?")
    why = {}
    swap = _quad(b_, a_)
    if swap != q:
        why.setdefault(swap, "swaps the $x$- and $y$-coordinates")
    clockwise = {1: 1, 2: 4, 3: 3, 4: 2}[q]
    if clockwise != q:
        why.setdefault(clockwise, "numbers the quadrants clockwise instead of counterclockwise")
    why.setdefault(_quad(-a_, -b_), "reverses both signs")
    why.setdefault(_quad(-a_, b_), "reads the sign of the $x$-coordinate backwards")
    why.setdefault(_quad(a_, -b_), "reads the sign of the $y$-coordinate backwards")
    wrong = [(Q(k), why.get(k)) for k in (1, 2, 3, 4) if k != q]
    side = "right of" if sx else "left of"
    vert = "above" if sy else "below"
    if style == "point":
        first = (f"The {m('x')}-coordinate {m(a_)} is {'positive' if sx else 'negative'}, so the point is {side} the "
                 f"{m('y')}-axis. The {m('y')}-coordinate {m(b_)} is {'positive' if sy else 'negative'}, so it is "
                 f"{vert} the {m('x')}-axis.")
    else:
        first = (f"A {'positive' if sx else 'negative'} {m('x')}-coordinate means {side} the {m('y')}-axis; a "
                 f"{'positive' if sy else 'negative'} {m('y')}-coordinate means {vert} the {m('x')}-axis.")
    names = {1: "upper right", 2: "upper left", 3: "lower left", 4: "lower right"}
    return Problem(
        stem=stem, answer=Q(q), fmt=_quad_fmt, near=lambda rng: [], wrong=wrong,
        steps=[first,
               f"That is the {names[q]} region. The quadrants are numbered counterclockwise from the upper right "
               f"(I, II, III, IV), so this is Quadrant {ROMAN[q]}."],
        verify=lambda v: v == {(True, True): 1, (False, True): 2, (False, False): 3, (True, False): 4}[(sx, sy)],
    )


@template("MK")
def read_grid(rng, lvl):
    a_ = rng.choice([v for v in range(-5, 6) if v])
    b_ = rng.choice([v for v in range(-5, 6) if v])
    need(abs(a_) != abs(b_))
    kind = rng.choice(["coords", "coords", "which"])
    if kind == "coords":
        lab = rng.choice(["P", "Q", "A", "K", "T", "W", "F", "M"])
        fig = _grid([(a_, b_, f"${lab}$", _anchor(a_, b_))])
        thing = rng.choice(["the water pump at a campsite", "the flagpole on a base", "a supply tent",
                            "a radio tower", "the first-aid station at a fair", "a lookout post",
                            "the entrance of a park", "a helicopter landing zone", "a fuel point",
                            "the main gate of a training area", "a picnic shelter", "a parking lot",
                            "a rally point", "the motor pool", "a hiking trailhead", "a water tower"])
        ans = _pt(a_, b_)
        wrong = [(_pt(b_, a_), "swaps the $x$- and $y$-coordinates"),
                 (_pt(-a_, b_), "reads the sign of the $x$-coordinate backwards"),
                 (_pt(a_, -b_), "reads the sign of the $y$-coordinate backwards"),
                 (_pt(-b_, -a_), None)]
        return Problem(
            stem=choose(rng,
                        f"On the map grid shown, point {m(lab)} marks {thing}. What are the coordinates of point "
                        f"{m(lab)}? (Each grid square is 1 unit.)",
                        f"A map is drawn on a coordinate grid, and point {m(lab)} shows the location of {thing}. "
                        f"What are the coordinates of point {m(lab)}? (Each grid square is 1 unit.)"),
            figure=fig, answer=ans, fmt=text, wrong=wrong,
            steps=[f"Start at the origin. Point {m(lab)} is {abs(a_)} {'unit' if abs(a_) == 1 else 'units'} "
                   f"{'right' if a_ > 0 else 'left'}, so {m(f'x = {a_}')}.",
                   f"It is {abs(b_)} {'unit' if abs(b_) == 1 else 'units'} {'up' if b_ > 0 else 'down'}, so "
                   f"{m(f'y = {b_}')}. Write {m('x')} first: {ans}."],
            verify=lambda v: v == _pt(a_, b_),
        )
    # which labeled point has the given coordinates?
    cands = [(a_, b_), (b_, a_), (-a_, b_), (a_, -b_)]
    labels = ["P", "Q", "R", "S"]
    rng.shuffle(labels)
    pts = [(cx, cy, f"${lab}$", _anchor(cx, cy)) for (cx, cy), lab in zip(cands, labels)]
    why = ["swaps the $x$- and $y$-coordinates", "reads the sign of the $x$-coordinate backwards",
           "reads the sign of the $y$-coordinate backwards"]
    return Problem(
        stem=f"Which point in the figure has coordinates {_pt(a_, b_)}? (Each grid square is 1 unit.)",
        figure=_grid(pts), answer=f"point {m(labels[0])}", fmt=text,
        wrong=[(f"point {m(lab)}", w_) for lab, w_ in zip(labels[1:], why)],
        steps=[f"The {m('x')}-coordinate comes first: go {abs(a_)} {'unit' if abs(a_) == 1 else 'units'} "
               f"{'right' if a_ > 0 else 'left'} from the origin.",
               f"Then go {abs(b_)} {'unit' if abs(b_) == 1 else 'units'} {'up' if b_ > 0 else 'down'}. "
               f"That is point {m(labels[0])}."],
        verify=lambda v: v == f"point {m(labels[0])}",
    )


def _slope_steps(x1, y1, x2, y2):
    dy, dx = y2 - y1, x2 - x1
    return [f"Use {m(r'm = \frac{y_2 - y_1}{x_2 - x_1}')} with {_pt(x1, y1)} and {_pt(x2, y2)}.",
            f"Rise: {m(f'{_sub(y2, y1)} = {dy}')}. Run: {m(f'{_sub(x2, x1)} = {dx}')}.",
            f"Slope: {m(_ratio(dy, dx))}."]


@template("MK")
def slope_two_points(rng, lvl):
    if lvl == 1:
        x1, y1 = rng.randint(0, 6), rng.randint(0, 6)
        x2, y2 = x1 + rng.randint(1, 6), y1 + rng.randint(1, 9)
    else:
        x1, y1 = rng.randint(-6, 6), rng.randint(-8, 8)
        x2, y2 = rng.randint(-6, 6), rng.randint(-8, 8)
    dx, dy = x2 - x1, y2 - y1
    need(dx != 0 and dy != 0 and abs(dx) != abs(dy))
    sl = R(dy, dx)
    need(abs(sl.p) <= 9 and sl.q <= 6)
    graph = lvl == 2 and rng.random() < 0.4 and max(abs(x1), abs(x2), abs(y1), abs(y2)) <= 5
    fig = None
    if graph:
        fig = _grid([(x1, y1, "", ""), (x2, y2, "", "")], line=((x1, y1), (x2, y2)))
        stem = (f"The line in the figure passes through the points {_pt(x1, y1)} and {_pt(x2, y2)}. "
                f"What is the slope of the line?")
    else:
        stem = choose(rng, f"What is the slope of the line that passes through {_pt(x1, y1)} and {_pt(x2, y2)}?",
                      f"A line passes through the points {_pt(x1, y1)} and {_pt(x2, y2)}. What is its slope?")
    wrong = [(1 / sl, "divides the change in $x$ by the change in $y$ (run over rise)"),
             (-sl, "subtracts the coordinates in opposite orders on the top and bottom"),
             (Q(dy), "finds the rise but forgets to divide by the run")]
    if x1 + x2 != 0 and y1 + y2 != 0:
        wrong.append((R(y1 + y2, x1 + x2), "adds the coordinates instead of subtracting them"))
    wrong.append((-1 / sl, None))
    return Problem(
        stem=stem, figure=fig, answer=sl, fmt=frac, neg_ok=True, must=1 if lvl == 1 else 2, wrong=wrong,
        steps=_slope_steps(x1, y1, x2, y2),
        tip=("Quick check: as $x$ increases, $y$ increases, so the slope must be positive." if sl > 0 else
             "Quick check: as $x$ increases, $y$ decreases, so the slope must be negative."),
        check=sp.Line(sp.Point(x1, y1), sp.Point(x2, y2)).slope,
    )


@template("MK")
def slope_from_eq(rng, lvl):
    if lvl == 1:
        m_ = rng.choice([v for v in range(-9, 10) if v not in (0, 1, -1)] + [R(1, 2), R(-1, 2), R(2, 3), R(-3, 4)])
        b_ = rng.choice([v for v in range(-12, 13) if v])
        need(abs(m_) != abs(b_))
        ask = rng.choice(["slope", "slope", "intercept"])
        form = rng.choice(["mxb", "mxb", "bmx"]) if ask == "slope" else "mxb"
        if form == "mxb":
            eq = _line_raw(m_, b_)
        else:
            eq = f"y = {frac_raw(b_)} {'+' if m_ > 0 else '-'} {_coef(abs(m_))}"
        if ask == "slope":
            return Problem(
                stem=f"What is the slope of the line {m(eq)}?",
                answer=Q(m_), fmt=frac, neg_ok=True, must=2,
                wrong=[(Q(b_), "gives the $y$-intercept (the number without $x$)" if form == "mxb"
                        else "takes the first number in the equation; the slope is the number multiplied by $x$"),
                       (-Q(m_), "drops the sign of the slope" if m_ < 0 else "changes the sign of the slope"),
                       (1 / Q(m_), "flips the slope upside down")],
                steps=([f"Rewrite the equation in the order {m('y = mx + b')}: {m(_line_raw(m_, b_))}."]
                       if form == "bmx" else []) +
                      [f"In {m('y = mx + b')}, the slope is {m('m')}, the number multiplied by {m('x')}.",
                       f"Here that number is {m(frac_raw(m_))}, so the slope is {m(frac_raw(m_))}."],
                check=sp.Poly(sp.sympify(f"{m_}*x + {b_}"), sp.Symbol("x")).coeffs()[0],
            )
        return Problem(
            stem=f"What is the {m('y')}-intercept of the line {m(eq)}?",
            answer=Q(b_), fmt=frac, neg_ok=True, must=2,
            wrong=[(Q(m_), "gives the slope instead of the $y$-intercept"),
                   (-Q(b_), "changes the sign of the $y$-intercept"),
                   (-Q(b_) / m_, "finds the $x$-intercept instead")],
            steps=[f"In {m('y = mx + b')}, the {m('y')}-intercept is {m('b')}, the number added on its own.",
                   f"Check by setting {m('x = 0')}: {m(f'y = {_times_val(m_, 0)}{_pm(b_)} = {b_}')}. "
                   f"So the {m('y')}-intercept is {m(b_)}."],
            check=Q(m_) * 0 + b_,
        )
    # level 3: standard form Ax + By = C
    A = rng.choice([v for v in range(-6, 7) if v])
    B = rng.choice([v for v in range(-6, 7) if v not in (0, 1)])
    C = rng.choice([v for v in range(-24, 25) if v])
    need(math.gcd(math.gcd(abs(A), abs(B)), abs(C)) == 1 or rng.random() < 0.3)
    need(abs(A) != abs(B) and A > 0)
    need(C % B == 0)
    sl, yi = R(-A, B), R(C, B)
    need(abs(sl.q) <= 6)
    ask = rng.choice(["slope", "slope", "intercept"])
    eq = _std_raw(A, B, C)
    steps = [f"Solve for {m('y')}. Move the {m('x')}-term to the other side: "
             f"{m(f'{_coef(B, chr(121))} = {_coef(-A)} {chr(43) if C > 0 else chr(45)} {abs(C)}')}.",
             f"Divide every term by {m(B)}: {m(_line_raw(sl, yi))}."]
    if ask == "slope":
        steps.append(f"The slope is the coefficient of {m('x')}: {m(frac_raw(sl))}.")
        return Problem(
            stem=f"What is the slope of the line {m(eq)}?",
            answer=sl, fmt=frac, neg_ok=True, must=2,
            wrong=[(R(A, B), "forgets to change the sign when moving the $x$-term"),
                   (R(-B, A), "flips the fraction (puts the $x$-coefficient on the bottom)"),
                   (Q(A), "uses the coefficient of $x$ without solving for $y$"),
                   (yi, "gives the $y$-intercept instead of the slope")],
            steps=steps,
            check=sp.solve(sp.Eq(A * sp.Symbol("x") + B * sp.Symbol("y"), C), sp.Symbol("y"))[0].coeff(sp.Symbol("x")),
        )
    steps.append(f"The {m('y')}-intercept is the constant term: {m(frac_raw(yi))}.")
    return Problem(
        stem=f"What is the {m('y')}-intercept of the line {m(eq)}?",
        answer=yi, fmt=frac, neg_ok=True, must=2,
        wrong=[(Q(C), "forgets to divide by the coefficient of $y$"),
               (-yi, "gets the sign wrong when dividing"),
               (R(C, A), "finds the $x$-intercept instead"),
               (sl, "gives the slope instead of the $y$-intercept")],
        steps=steps,
        verify=lambda v: A * 0 + B * v == C,
    )


@template("MK")
def midpoint(rng, lvl):
    kind = rng.choice(["mid", "mid", "end"])
    if kind == "mid":
        x1, y1 = rng.randint(-9, 9), rng.randint(-9, 9)
        x2, y2 = rng.randint(-9, 9), rng.randint(-9, 9)
        need((x1 + x2) % 2 == 0 and (y1 + y2) % 2 == 0 and x1 != x2 and y1 != y2)
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        need(mx != my and (mx, my) != (0, 0))
        hx, hy = R(x2 - x1, 2), R(y2 - y1, 2)
        wrong = [(_pt(hx, hy), "subtracts the coordinates instead of adding them"),
                 (_pt(x1 + x2, y1 + y2), "adds the coordinates but forgets to divide by 2"),
                 (_pt(my, mx), "swaps the $x$- and $y$-coordinates"),
                 (_pt(-mx, my) if mx else _pt(mx, -my), None)]
        return Problem(
            stem=choose(rng, f"What is the midpoint of the segment joining {_pt(x1, y1)} and {_pt(x2, y2)}?",
                        f"Find the midpoint between the points {_pt(x1, y1)} and {_pt(x2, y2)}."),
            answer=_pt(mx, my), fmt=text, wrong=wrong,
            steps=[f"Average the {m('x')}-coordinates: {m(rf'\frac{{{_add(x1, x2)}}}{{2}} = \frac{{{x1 + x2}}}{{2}} = {mx}')}.",
                   f"Average the {m('y')}-coordinates: {m(rf'\frac{{{_add(y1, y2)}}}{{2}} = \frac{{{y1 + y2}}}{{2}} = {my}')}.",
                   f"The midpoint is {_pt(mx, my)}."],
            verify=lambda v: v == _pt(sp.Point(x1, y1).midpoint(sp.Point(x2, y2)).x,
                                      sp.Point(x1, y1).midpoint(sp.Point(x2, y2)).y),
        )
    # find the other endpoint
    ax, ay = rng.randint(-8, 8), rng.randint(-8, 8)
    mx, my = rng.randint(-6, 6), rng.randint(-6, 6)
    need(ax != mx and ay != my)
    bx, by = 2 * mx - ax, 2 * my - ay
    need(abs(bx) <= 14 and abs(by) <= 14)
    wrong = [(_pt(mx - ax, my - ay), "finds only the change from $A$ to $M$, not the endpoint"),
             (_pt(ax + mx, ay + my), "adds $A$ and $M$ without doubling $M$"),
             (_pt(2 * ax - mx, 2 * ay - my), "goes from $M$ through $A$ instead of from $A$ through $M$")]
    if (ax + mx) % 2 == 0 and (ay + my) % 2 == 0:
        wrong.append((_pt((ax + mx) // 2, (ay + my) // 2), "finds the midpoint of $A$ and $M$"))
    return Problem(
        stem=(f"The midpoint of segment {m('AB')} is {m('M' + _pr(mx, my))}. If point {m('A')} is "
              f"{_pt(ax, ay)}, what are the coordinates of point {m('B')}?"),
        answer=_pt(bx, by), fmt=text, wrong=wrong,
        steps=[f"From {m('A')} to {m('M')}, {m('x')} changes by {m(f'{_sub(mx, ax)} = {mx - ax}')} and {m('y')} "
               f"changes by {m(f'{_sub(my, ay)} = {my - ay}')}.",
               f"{m('B')} is the same distance past {m('M')}: {m(f'x = {_add(mx, mx - ax)} = {bx}')} and "
               f"{m(f'y = {_add(my, my - ay)} = {by}')}.",
               f"Check: the midpoint of {_pt(ax, ay)} and {_pt(bx, by)} is "
               f"{m(rf'\left(\frac{{{ax + bx}}}{{2}}, \frac{{{ay + by}}}{{2}}\right)')} {m('=')} {_pt(mx, my)}. \\checkmark"],
        verify=lambda v: v == _pt(2 * mx - ax, 2 * my - ay) and (ax + bx) == 2 * mx and (ay + by) == 2 * my,
    )


_TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20), (4, 3, 5), (8, 6, 10),
            (12, 5, 13), (15, 8, 17), (12, 9, 15)]


@template("MK")
def distance(rng, lvl):
    a_, b_, c_ = rng.choice(_TRIPLES)
    sx, sy = rng.choice([1, -1]), rng.choice([1, -1])
    small = a_ <= 8 and b_ <= 8 and rng.random() < 0.5
    lim = 5 if small else 12
    x1 = rng.randint(-lim, lim - a_) if sx > 0 else rng.randint(-lim + a_, lim)
    y1 = rng.randint(-lim, lim - b_) if sy > 0 else rng.randint(-lim + b_, lim)
    x2, y2 = x1 + sx * a_, y1 + sy * b_
    fig = None
    if small:
        fig = _grid([(x1, y1, "", ""), (x2, y2, "", "")], segs=[((x1, y1), (x2, y2))],
                    dashed=[((x1, y1), (x2, y1)), ((x2, y1), (x2, y2))])
        stem = (f"In the figure, a segment joins the points {_pt(x1, y1)} and {_pt(x2, y2)}. "
                f"How long is the segment?")
    else:
        stem = choose(rng, f"What is the distance between the points {_pt(x1, y1)} and {_pt(x2, y2)}?",
                      f"How far apart are the points {_pt(x1, y1)} and {_pt(x2, y2)}?")
    return Problem(
        stem=stem, figure=fig, answer=Q(c_), fmt=num, must=3,
        wrong=[(Q(a_ + b_), "adds the horizontal and vertical distances instead of using the Pythagorean theorem"),
               (Q(a_ * a_ + b_ * b_), "forgets to take the square root"),
               rng.choice([(Q(abs(a_ - b_)), "subtracts the horizontal and vertical distances"),
                           (Q(a_ * b_), "multiplies the horizontal and vertical distances")]),
               (Q(c_ + 1), None), (Q(c_ - 1), None)],
        steps=[f"Horizontal change: {m(rf'\lvert {_sub(x2, x1)} \rvert = {a_}')}. "
               f"Vertical change: {m(rf'\lvert {_sub(y2, y1)} \rvert = {b_}')}.",
               f"These are the legs of a right triangle, and the distance is the hypotenuse: "
               f"{m(rf'd = \sqrt{{{a_}^2 + {b_}^2}} = \sqrt{{{a_ * a_} + {b_ * b_}}} = \sqrt{{{c_ * c_}}} = {c_}')}."],
        tip=f"The legs {m(f'{min(a_, b_)}')} and {m(f'{max(a_, b_)}')} belong to the Pythagorean triple "
            f"{m(f'{min(a_, b_)}')}-{m(f'{max(a_, b_)}')}-{m(c_)}.",
        check=sp.Point(x1, y1).distance(sp.Point(x2, y2)),
    )


@template("MK")
def intercepts(rng, lvl):
    kind = rng.choice(["x_si", "x_std", "y_std", "x_std"])
    if kind == "x_si":
        m_ = rng.choice([v for v in range(-6, 7) if v not in (0, 1, -1)])
        xi = rng.choice([v for v in range(-8, 9) if v])
        b_ = -m_ * xi
        need(abs(b_) <= 30 and abs(xi) != abs(b_))
        return Problem(
            stem=f"What is the {m('x')}-intercept of the line {m(_line_raw(m_, b_))}?",
            answer=Q(xi), fmt=frac, neg_ok=True, must=2,
            wrong=[(Q(b_), "gives the $y$-intercept instead of the $x$-intercept"),
                   (-Q(xi), "makes a sign error when solving for $x$"),
                   (R(m_, b_) if b_ else Q(m_), "divides the slope by the $y$-intercept instead of dividing $-b$ by the slope"),
                   (Q(m_), None)],
            steps=[f"The {m('x')}-intercept is where the line crosses the {m('x')}-axis, so set {m('y = 0')}: "
                   f"{m(f'0 = {_coef(m_)} {chr(43) if b_ > 0 else chr(45)} {abs(b_)}')}.",
                   f"{m(f'{_coef(m_)} = {-b_}')}, so {m(f'x = {-b_} \\div {_par(m_)} = {xi}')}."],
            verify=lambda v: m_ * v + b_ == 0,
        )
    A = rng.choice([v for v in range(-6, 7) if v not in (0,)])
    B = rng.choice([v for v in range(-6, 7) if v not in (0,)])
    C = rng.choice([v for v in range(-48, 49) if v])
    need(A > 0 and abs(A) != abs(B) and C % A == 0 and C % B == 0)
    xi, yi = R(C, A), R(C, B)
    need(xi != yi and abs(xi) != abs(yi))
    eq = _std_raw(A, B, C)
    if kind == "x_std":
        return Problem(
            stem=f"What is the {m('x')}-intercept of the line {m(eq)}?",
            answer=xi, fmt=frac, neg_ok=True, must=2,
            wrong=[(yi, "finds the $y$-intercept instead (sets $x = 0$)"),
                   (-xi, "makes a sign error"),
                   (Q(C), "forgets to divide by the coefficient of $x$"),
                   (R(A, C), "divides upside down")],
            steps=[f"On the {m('x')}-axis, {m('y = 0')}. Substitute: {m(f'{_coef(A)} {chr(43) if B > 0 else chr(45)} {abs(B)}(0) = {C}')}, so "
                   f"{m(f'{_coef(A)} = {C}')}.",
                   f"Divide by {m(A)}: {m(f'x = {C} \\div {A} = {frac_raw(xi)}')}."],
            verify=lambda v: A * v + B * 0 == C,
        )
    return Problem(
        stem=f"At what value of {m('y')} does the line {m(eq)} cross the {m('y')}-axis?",
        answer=yi, fmt=frac, neg_ok=True, must=2,
        wrong=[(xi, "finds the $x$-intercept instead (sets $y = 0$)"),
               (-yi, "makes a sign error"),
               (Q(C), "forgets to divide by the coefficient of $y$"),
               (R(B, C), "divides upside down")],
        steps=[f"On the {m('y')}-axis, {m('x = 0')}. Substitute: {m(f'{A}(0) {chr(43) if B > 0 else chr(45)} {_coef(abs(B), chr(121))} = {C}')}, "
               f"so {m(f'{_coef(B, chr(121))} = {C}')}.",
               f"Divide by {m(B)}: {m(f'y = {C} \\div {_par(B)} = {frac_raw(yi)}')}."],
        verify=lambda v: A * 0 + B * v == C,
    )


_SLOPES = [2, 3, 4, 5, -2, -3, -4, -5, R(1, 2), R(-1, 2), R(1, 3), R(-1, 3), R(2, 3), R(-2, 3), R(3, 4),
           R(-3, 4), R(3, 2), R(-3, 2), R(4, 3), R(-4, 3), R(2, 5), R(-5, 2)]


@template("MK")
def parallel_perp(rng, lvl):
    m_ = rng.choice(_SLOPES)
    b_ = rng.choice([v for v in range(-9, 10) if v])
    rel = rng.choice(["perpendicular", "perpendicular", "parallel"])
    if lvl == 3 and rng.random() < 0.6:
        # give the line in standard form
        Ms = sp.Rational(m_)
        A, B = -Ms.p, Ms.q
        if A < 0:
            A, B = -A, -B
        C = B * b_
        eq = _std_raw(A, B, C)
        first = [f"Solve for {m('y')} to find the slope: {m(f'{_coef(B, chr(121))} = {_coef(-A)} {chr(43) if C > 0 else chr(45)} {abs(C)}')}, "
                 f"so {m(_line_raw(m_, b_))} and the slope is {m(frac_raw(m_))}."]
        std = True
    else:
        eq = _line_raw(m_, b_)
        first = [f"The line {m(eq)} has slope {m(frac_raw(m_))} (the coefficient of {m('x')})."]
        std = False
    ans = -1 / Q(m_) if rel == "perpendicular" else Q(m_)
    if rel == "perpendicular":
        wrong = [(Q(m_), "gives the slope of a parallel line"),
                 (-Q(m_), "changes the sign but forgets to flip the fraction"),
                 (1 / Q(m_), "flips the fraction but forgets to change the sign")]
        steps = first + [f"A perpendicular slope is the negative reciprocal: flip {m(frac_raw(m_))} and change its "
                         f"sign to get {m(frac_raw(ans))}.",
                         f"Check: {m(rf'{_par(m_)} \times {_par(ans)} = -1')}. \\checkmark"]
    else:
        wrong = [(-1 / Q(m_), "gives the perpendicular slope"),
                 (-Q(m_), "changes the sign of the slope"),
                 (1 / Q(m_), "flips the slope upside down"),
                 (Q(b_), "gives the $y$-intercept")]
        steps = first + [f"Parallel lines have the same slope, so the answer is {m(frac_raw(ans))}."]
    if std and Q(A) != ans:
        wrong.append((Q(A), "uses the coefficient of $x$ without solving for $y$ first"))
    return Problem(
        stem=f"What is the slope of a line that is {rel} to the line {m(eq)}?",
        answer=ans, fmt=frac, neg_ok=True, must=3, wrong=wrong, steps=steps,
        verify=(lambda v: v * m_ == -1) if rel == "perpendicular" else (lambda v: v == m_),
    )


@template("MK")
def point_on_line(rng, lvl):
    m_ = rng.choice([v for v in range(-5, 6) if v not in (0,)])
    b_ = rng.choice([v for v in range(-9, 10) if v])
    x0 = rng.choice([v for v in range(-4, 5) if v not in (0,)])
    y0 = m_ * x0 + b_
    need(y0 != x0)
    eq = _line_raw(m_, b_)
    sw = (y0, x0)
    need(sw[1] != m_ * sw[0] + b_)
    wrong = [(_pt(*sw), "swaps the $x$- and $y$-coordinates of a point on the line"),
             (_pt(x0, m_ * x0 - b_), "uses the wrong sign for the $y$-intercept"),
             (_pt(x0, x0 + m_ + b_), "adds the slope to $x$ instead of multiplying")]
    x1 = x0 + rng.choice([1, 2, -1])
    wrong.append((_pt(x1, m_ * x1 + b_ + rng.choice([1, -1, 2])), None))
    wrong = [w_ for w_ in wrong if w_[0] != _pt(x0, y0)]
    return Problem(
        stem=choose(rng, f"Which of the following points lies on the line {m(eq)}?",
                    f"The graph of {m(eq)} passes through which of these points?",
                    f"Which ordered pair is a solution of the equation {m(eq)}?"),
        answer=_pt(x0, y0), fmt=text, wrong=wrong,
        steps=[f"A point is on the line if its coordinates make the equation true. Substitute each {m('x')} and "
               f"see whether you get the matching {m('y')}.",
               f"For {_pt(x0, y0)}: {m(f'y = {_times_val(m_, x0)}{_pm(b_)} = {m_ * x0}{_pm(b_)} = {y0}')}. "
               f"It matches, so {_pt(x0, y0)} is on the line.",
               f"Each of the other points gives a different {m('y')} when you substitute its {m('x')}."],
        verify=lambda v: v == _pt(x0, m_ * x0 + b_),
    )


@template("MK")
def line_equation(rng, lvl):
    kind = rng.choice(["two", "two", "slope_pt"])
    m_ = rng.choice([2, 3, 4, -2, -3, -4, R(1, 2), R(-1, 2), R(2, 3), R(-2, 3), R(3, 2), R(-3, 2), 5, -5])
    b_ = rng.choice([v for v in range(-8, 9) if v])
    Ms = sp.Rational(m_)
    x1 = Ms.q * rng.choice([-2, -1, 1, 2, 3])
    y1 = Ms * x1 + b_
    x2 = x1 + Ms.q * rng.choice([1, 2])
    y2 = Ms * x2 + b_
    need(y1.is_integer and y2.is_integer and abs(y1) <= 15 and abs(y2) <= 15 and y1 != b_)
    ans = m(_line_raw(Ms, b_))
    wrong = [(m(_line_raw(Ms, -b_)), "gets the sign of the $y$-intercept wrong"),
             (m(_line_raw(Ms, y1)), f"uses {m(int_raw(y1))}, the $y$-coordinate of a point, as the $y$-intercept")]
    if kind == "two":
        inv = 1 / Ms
        wrong.append((m(_line_raw(inv, y1 - inv * x1)), "uses run over rise for the slope"))
        wrong.append((m(_line_raw(-Ms, y1 + Ms * x1)), "makes a sign error in the slope"))
        stem = choose(rng,
                      f"Which equation describes the line that passes through {_pt(x1, y1)} and {_pt(x2, y2)}?",
                      f"A line passes through the points {_pt(x1, y1)} and {_pt(x2, y2)}. What is its equation?")
        steps = [f"Slope: {m(rf'm = \frac{{{_sub(y2, y1)}}}{{{_sub(x2, x1)}}} = ' + _ratio(int(y2 - y1), int(x2 - x1)))}."]
    else:
        wrong.append((m(_line_raw(-Ms, y1 + Ms * x1)), "makes a sign error in the slope"))
        wrong.append((m(_line_raw(b_, Ms)), "swaps the slope and the $y$-intercept"))
        stem = f"A line has a slope of {m(frac_raw(Ms))} and passes through the point {_pt(x1, y1)}. What is its equation?"
        steps = [f"Start with {m(_line_raw(Ms, 0) + ' + b')}, since the slope is {m(frac_raw(Ms))}."]
    steps += [f"Substitute the point {_pt(x1, y1)} to find {m('b')}: "
              f"{m(f'{int_raw(y1)} = {_times_val(Ms, x1)} + b = {int_raw(Ms * x1)} + b')}, so "
              f"{m(f'b = {_sub(y1, Ms * x1)} = {b_}')}.",
              f"The equation is {ans}."]
    if kind == "two":
        steps.append(f"Check with {_pt(x2, y2)}: {m(f'{_times_val(Ms, x2)}{_pm(b_)} = {int_raw(y2)}')}. \\checkmark")
    xs, ys = sp.symbols("x y")
    line = sp.Line(sp.Point(x1, y1), sp.Point(x2, y2))
    return Problem(
        stem=stem, answer=ans, fmt=text, wrong=wrong, steps=steps,
        verify=lambda v: v == m(_line_raw(line.slope, sp.solve(line.equation(xs, ys).subs(xs, 0), ys)[0])),
    )


PLAN = [
    # (template, level, count) -- easy -> hard; 25 problems
    (quadrant, 1, 2),
    (read_grid, 1, 2),
    (slope_two_points, 1, 2),
    (slope_from_eq, 1, 2),
    (slope_two_points, 2, 2),
    (midpoint, 2, 2),
    (distance, 2, 2),
    (intercepts, 2, 2),
    (point_on_line, 2, 2),
    (line_equation, 3, 3),
    (parallel_perp, 3, 2),
    (slope_from_eq, 3, 2),
]
