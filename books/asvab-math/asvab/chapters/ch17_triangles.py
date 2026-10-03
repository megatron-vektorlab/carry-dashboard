"""Chapter 17 - Triangles & the Pythagorean Theorem.

Figures are drawn from the same numbers as the stem.  Plain Python floats
appear only in the private drawing helpers (TikZ coordinates); every answer,
check and distractor is exact (ints / sympy).
"""
import math

import sympy as sp

from ..core import (R, Q, Problem, need, num, m, dec_raw, int_raw, latex, text,
                    expr, choose, person, soldier, template, x as X)

NUM = 17
TITLE = r"Triangles \& the Pythagorean Theorem"
PART = 3

INTRO = r"""
A triangle has three sides and three angles. Two facts solve most triangle
questions on the ASVAB: the angles always add up to $180^\circ$, and in a
right triangle $a^2 + b^2 = c^2$.

\begin{concept}{Angles in a triangle}
\begin{itemize}
\item The three angles add up to $180^\circ$. Missing angle $= 180^\circ - (\text{the other two})$.
\item \textbf{Isosceles} triangle: two equal sides, and the two angles opposite them (the \emph{base angles}) are equal.
  \textbf{Equilateral}: three equal sides and three $60^\circ$ angles. \textbf{Scalene}: no equal sides.
\item By angles: \textbf{acute} (all angles less than $90^\circ$), \textbf{right} (one $90^\circ$ angle), \textbf{obtuse} (one angle more than $90^\circ$).
\item An \textbf{exterior angle} (made by extending one side) equals the sum of the two \emph{remote} interior angles.
\item \textbf{Triangle inequality:} any two sides must add up to \emph{more} than the third side.
\end{itemize}
\end{concept}

\begin{concept}{The Pythagorean theorem (right triangles only)}
\begin{minipage}[c]{0.3\linewidth}\centering
\begin{tikzpicture}[font=\small, line join=round]
\draw[thick] (0,0) -- (2.4,0) -- (0,1.6) -- cycle;
\draw (0.22,0) -- (0.22,0.22) -- (0,0.22);
\node[below] at (1.2,0) {$b$};
\node[left] at (0,0.8) {$a$};
\node[anchor=214] at (1.25,0.85) {$c$};
\end{tikzpicture}
\end{minipage}\hfill
\begin{minipage}[c]{0.68\linewidth}
\[ a^2 + b^2 = c^2 \]
$c$ is the \textbf{hypotenuse}: the longest side, across from the right angle.
To find a leg, subtract: $a^2 = c^2 - b^2$.
Memorize the common \textbf{Pythagorean triples} and their multiples:
$3$-$4$-$5$ ($6$-$8$-$10$, $9$-$12$-$15$, \dots), $5$-$12$-$13$, $8$-$15$-$17$, $7$-$24$-$25$.
\end{minipage}
\end{concept}

\begin{concept}{Special right triangles and similar triangles}
\begin{itemize}
\item $45^\circ$-$45^\circ$-$90^\circ$: sides in the ratio $1 : 1 : \sqrt{2}$ \quad (legs $s$, hypotenuse $s\sqrt{2}$).
\item $30^\circ$-$60^\circ$-$90^\circ$: sides in the ratio $1 : \sqrt{3} : 2$ \quad (short leg $s$, long leg $s\sqrt{3}$, hypotenuse $2s$).
\item \textbf{Similar} triangles have the same shape: equal angles and proportional sides. Shadows cast at the same time of day make similar triangles.
\end{itemize}
\end{concept}

\begin{example}{Worked example}
A $13$-foot ladder leans against a wall. Its foot is $5$ feet from the wall. How high up the wall does the ladder reach?

\textbf{Solution.} The ladder is the hypotenuse: $5^2 + h^2 = 13^2$, so
$h^2 = 169 - 25 = 144$ and $h = \sqrt{144} = 12$ feet.
\end{example}

\begin{tip}
Spot the triple before you square anything. For legs $15$ and $20$, divide by
$5$ to get $3$ and $4$; the hypotenuse is $5 \times 5 = 25$.
\end{tip}

\begin{trap}
\begin{itemize}
\item Forgetting the square root: $a^2 + b^2$ is $c^2$, not $c$.
\item Adding the squares when you need a leg; subtract from the hypotenuse instead.
\item Mixing up $\sqrt{2}$ ($45^\circ$-$45^\circ$-$90^\circ$) and $\sqrt{3}$ ($30^\circ$-$60^\circ$-$90^\circ$).
\item In similar triangles, \emph{multiplying} by the scale factor, not \emph{adding} the difference.
\end{itemize}
\end{trap}
"""


# --------------------------------------------------------------------------
# formatting helpers
# --------------------------------------------------------------------------

def _d(v):
    return dec_raw(v) + r"^\circ"


def deg(v):
    """Answer formatter for angle measures."""
    return m(_d(v))


_UNITS = {"ft": ("foot", "feet"), "in": ("inch", "inches"), "cm": ("centimeter", "centimeters"),
          "m": ("meter", "meters"), "yd": ("yard", "yards"), "mi": ("mile", "miles"),
          "km": ("kilometer", "kilometers")}


def _lenfmt(u):
    """Formatter: 10 -> $10\\text{ ft}$."""
    def f(v):
        return m(dec_raw(v) + rf"\text{{ {u}}}")
    return f


def _w(v, u):
    """'6 feet' for stems."""
    one, many = _UNITS[u]
    return f"{m(dec_raw(v))} {one if Q(v) == 1 else many}"


def _lab(v, u=None):
    """Figure label: $6$ ft."""
    return m(dec_raw(v)) + (f" {u}" if u else "")


def _near_int(ans, deltas=(1, 2, 3, 4), hi=10**6):
    def f(rng):
        out = [Q(ans) + d for d in deltas] + [Q(ans) - d for d in deltas]
        out = [v for v in out if 0 < v < hi]
        rng.shuffle(out)
        return out
    return f


def _triple_tip(x1, x2, known_hyp):
    """'Spot the triple' shortcut when the numbers are a multiple of a basic triple."""
    for base in ((3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)):
        for k in range(2, 60):
            t = tuple(v * k for v in base)
            if known_hyp and x2 == t[2] and x1 in t[:2]:
                other = t[1] if x1 == t[0] else t[0]
                kb = base[1] if x1 == t[0] else base[0]
                return (f"Shortcut: divide by {m(k)} and you get the {m(base[0])}-{m(base[1])}-{m(base[2])} triple, "
                        f"so the missing side is {m(f'{kb} \\times {k} = {other}')}.")
            if not known_hyp and {x1, x2} == {t[0], t[1]}:
                return (f"Shortcut: divide by {m(k)} and you get the {m(base[0])}-{m(base[1])}-{m(base[2])} triple, "
                        f"so the hypotenuse is {m(f'{base[2]} \\times {k} = {t[2]}')}.")
    return None


def _isqrt_check(n2):
    """Independent route for a square root: brute-force search."""
    k = 0
    while k * k < n2:
        k += 1
    return Q(k) if k * k == n2 else sp.sqrt(n2)


# --------------------------------------------------------------------------
# drawing helpers (floats only for TikZ coordinates)
# --------------------------------------------------------------------------

def _f(v):
    s = f"{float(v):.2f}"
    return "0.00" if s == "-0.00" else s


def _P(px, py):
    return f"({_f(px)},{_f(py)})"


def _tikz(body):
    return ("\\begin{tikzpicture}[font=\\small, line cap=round, line join=round]\n"
            + "\n".join(body) + "\n\\end{tikzpicture}")


def _fit(pts, wmax=4.4, hmax=2.8):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    sc = min(wmax / w if w else 99, hmax / h if h else 99)
    return [((px - min(xs)) * sc, (py - min(ys)) * sc) for px, py in pts], sc


def _unit(vx, vy):
    L = math.hypot(vx, vy)
    return vx / L, vy / L


def _arc_at(V, a0, a1, r):
    sx, sy = V[0] + r * math.cos(math.radians(a0)), V[1] + r * math.sin(math.radians(a0))
    return (rf"\draw {_P(sx, sy)} arc[start angle={_f(a0)}, end angle={_f(a1)}, "
            rf"radius={_f(r)}];")


def _label_width(tex):
    """Rough printed width (cm) of a short label such as $12$ ft or $5\\sqrt{3}$."""
    import re
    core = re.sub(r"\\sqrt\{(\w+)\}", r"v\1", tex)
    core = re.sub(r"\\circ", "o", core)
    spaces = core.count(" ")
    core = re.sub(r"[$\\{}^ ]", "", core)
    return 0.2 * len(core) + 0.12 * spaces + 0.15


def _tri_points_from_angles(a, b):
    """ccw triangle with angle a at A=(0,0) and angle b at B=(1,0)."""
    ra, rb = math.radians(float(a)), math.radians(float(b))
    t = math.sin(rb) / math.sin(ra + rb)
    return [(0.0, 0.0), (1.0, 0.0), (t * math.cos(ra), t * math.sin(ra))]


def _tri_body(P, sides=None, angles=None, right=None, ticks=None, verts=None, arcs=True):
    """TikZ lines for a ccw triangle P (already scaled, in cm).
    sides[i]: label for side P[i]-P[i+1] (placed outside); angles[i]: label
    inside vertex i; right: vertex with a right-angle mark; ticks[i]: number
    of tick marks on side i; verts[i]: vertex letter."""
    body = [r"\draw[thick] " + " -- ".join(_P(*p) for p in P) + " -- cycle;"]
    for i, tex in (sides or {}).items():
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % 3]
        nx, ny = _unit(y2 - y1, -(x2 - x1))                 # outward normal (ccw)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        w, h = _label_width(tex), 0.34
        d = 0.5 * w * abs(nx) + 0.5 * h * abs(ny) + 0.09   # push the whole label box clear of the side
        body.append(rf"\node[inner sep=0pt] at {_P(mx + d * nx, my + d * ny)} {{{tex}}};")
    for i in range(3):
        V, U, W = P[i], P[i - 1], P[(i + 1) % 3]
        ux, uy = _unit(U[0] - V[0], U[1] - V[1])
        wx, wy = _unit(W[0] - V[0], W[1] - V[1])
        bx, by = _unit(ux + wx, uy + wy)
        theta = math.acos(max(-1.0, min(1.0, ux * wx + uy * wy)))
        if right == i:
            s = 0.2
            body.append(rf"\draw {_P(V[0] + s * ux, V[1] + s * uy)} -- "
                        rf"{_P(V[0] + s * (ux + wx), V[1] + s * (uy + wy))} -- {_P(V[0] + s * wx, V[1] + s * wy)};")
        if angles and i in angles:
            r = min(1.35, max(0.5, 0.36 / math.sin(theta / 2)))
            body.append(rf"\node at {_P(V[0] + r * bx, V[1] + r * by)} {{{angles[i]}}};")
            if arcs and right != i:
                a0 = math.degrees(math.atan2(wy, wx))
                a1 = math.degrees(math.atan2(uy, ux))
                while a1 < a0:
                    a1 += 360
                body.append(_arc_at(V, a0, a1, 0.25))
        if verts and i in verts:
            body.append(rf"\node at {_P(V[0] - 0.24 * bx, V[1] - 0.24 * by)} {{{verts[i]}}};")
    for i, k in (ticks or {}).items():
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % 3]
        dx, dy = _unit(x2 - x1, y2 - y1)
        nx, ny = -dy, dx
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        for j in range(k):
            o = (j - (k - 1) / 2) * 0.08
            cx, cy = mx + o * dx, my + o * dy
            body.append(rf"\draw {_P(cx - 0.09 * nx, cy - 0.09 * ny)} -- {_P(cx + 0.09 * nx, cy + 0.09 * ny)};")
    return body


_NAMES = [("A", "B", "C"), ("P", "Q", "R"), ("D", "E", "F"), ("J", "K", "L"), ("R", "S", "T")]


# --------------------------------------------------------------------------
# level 1
# --------------------------------------------------------------------------

@template("MK")
def third_angle(rng, lvl):
    a, b = rng.randint(35, 105), rng.randint(35, 105)
    c = 180 - a - b
    need(35 <= c <= 110 and a != b and c not in (a, b))
    names = rng.choice(_NAMES)
    if rng.random() < 0.6:
        meas = [(a, m(_d(a))), (b, m(_d(b))), (c, r"$x^\circ$")]
        rng.shuffle(meas)
        meas.sort(key=lambda t: t[0] == max(a, b, c))     # largest angle at the apex: a wide triangle
        P, _ = _fit(_tri_points_from_angles(meas[0][0], meas[1][0]), 4.2, 2.6)
        fig = _tikz(_tri_body(P, angles={i: meas[i][1] for i in range(3)}))
        stem = choose(rng,
                      f"In the triangle shown, two angles measure {deg(a)} and {deg(b)}. What is the value of {m('x')}?",
                      f"Two angles of the triangle shown measure {deg(a)} and {deg(b)}. Find {m('x')}.")
        fmt, label = num, m("x")
    else:
        fig = None
        A, B, C = names
        stem = choose(rng,
                      f"In triangle {m(A + B + C)}, {m(r'\angle ' + A)} measures {deg(a)} and "
                      f"{m(r'\angle ' + B)} measures {deg(b)}. What is the measure of {m(r'\angle ' + C)}?",
                      f"Two angles of a triangle measure {deg(a)} and {deg(b)}. What is the measure of the third angle?")
        fmt, label = deg, "the third angle"
    wrong = [(Q(360 - a - b), r"uses $360^\circ$ instead of $180^\circ$ for the angle sum"),
             (Q(a + b), "adds the two given angles and stops"),
             (Q(180 - max(a, b)), "subtracts only one of the given angles")]
    if a + b < 90:
        wrong.append((Q(90 - a - b), r"uses $90^\circ$ instead of $180^\circ$ for the angle sum"))
    return Problem(
        stem=stem,
        answer=Q(c),
        fmt=fmt,
        wrong=wrong,
        steps=[r"The three angles of any triangle add up to $180^\circ$.",
               f"Add the two known angles: {m(f'{a} + {b} = {int_raw(a + b)}')}.",
               f"Subtract from 180: {m(f'180 - {int_raw(a + b)} = {c}')}, so {label} is {deg(c)}."
               if fmt is deg else f"Subtract from 180: {m(f'x = 180 - {int_raw(a + b)} = {c}')}."],
        figure=fig,
        near=_near_int(c, (5, 10, 15, 20), 180),
        check=sp.solve(sp.Eq(a + b + X, 180), X)[0],
    )


def _classify(angles):
    big = max(angles)
    if big == 90:
        return "a right triangle"
    if big > 90:
        return "an obtuse triangle"
    return "an acute triangle"


@template("MK")
def classify_triangle(rng, lvl):
    kind = rng.choice(["right", "obtuse", "acute"])
    for _ in range(200):
        if kind == "right":
            a = rng.randint(15, 75)
            b = 90 - a if rng.random() < 0.85 else 90
        elif kind == "obtuse":
            a = rng.randint(15, 70)
            b = rng.choice([rng.randint(95, 150), rng.randint(10, 80)])
        else:
            a, b = rng.randint(35, 85), rng.randint(35, 85)
        c = 180 - a - b
        ang = [a, b, c]
        if c >= 10 and a != b and sorted(ang) != [60, 60, 60] and _classify(ang).split()[1] == kind:
            break
    else:
        need(False)
    ans = _classify(ang)
    big = max(ang)
    wrong_all = {
        "an acute triangle": f"would need all three angles to be less than {m('90^\\circ')}, but one angle is {deg(big)}",
        "a right triangle": f"would need a {m('90^\\circ')} angle, but the angles are {deg(a)}, {deg(b)}, and {deg(c)}",
        "an obtuse triangle": f"would need an angle greater than {m('90^\\circ')}, but the largest angle is {deg(big)}",
        "an equilateral triangle": f"would need all three angles to be {m('60^\\circ')}",
    }
    wrong = [(k, v) for k, v in wrong_all.items() if k != ans]
    rule = {"right": "exactly", "obtuse": "more than", "acute": "less than"}[kind]
    return Problem(
        stem=choose(rng,
                    f"A triangle has angles of {deg(a)} and {deg(b)}. Which of the following describes the triangle?",
                    f"Two angles of a triangle measure {deg(a)} and {deg(b)}. What kind of triangle is it?"),
        answer=ans,
        fmt=text,
        wrong=wrong,
        steps=[f"Find the third angle: {m(f'180^\\circ - {a}^\\circ - {b}^\\circ = {c}^\\circ')}.",
               f"The largest angle is {deg(big)}, which is {rule} {m('90^\\circ')}"
               + ("" if kind != "acute" else ", so all three angles are acute")
               + f". It is {ans}."],
        check=_classify([a, b, 180 - a - b]),
    )


# Pythagorean triples (legs a < b, hypotenuse c)
_EASY_TRIPLES = [(3 * k, 4 * k, 5 * k) for k in range(1, 6)] + [(5, 12, 13)]
# leg problems use a different mix than the hypotenuse warm-ups
_LEG_TRIPLES = [(5, 12, 13), (10, 24, 26), (15, 36, 39), (8, 15, 17), (16, 30, 34), (7, 24, 25), (9, 12, 15),
                (12, 16, 20), (21, 28, 35), (24, 32, 40), (27, 36, 45), (30, 40, 50)]
_TRIPLES = ([(3 * k, 4 * k, 5 * k) for k in range(7, 11)] + [(5 * k, 12 * k, 13 * k) for k in (1, 2, 3)]
            + [(8 * k, 15 * k, 17 * k) for k in (1, 2)] + [(7, 24, 25)])


def _right_fig(a, b, labels, corner=None):
    """Right triangle with horizontal leg b and vertical leg a (a < b).
    labels: {'h': tex, 'v': tex, 'c': tex}; corner: 'left' or 'right'."""
    if corner == "right":
        pts = [(0.0, 0.0), (float(b), 0.0), (float(b), float(a))]       # right angle at vertex 1
        side = {0: labels.get("h"), 1: labels.get("v"), 2: labels.get("c")}
        ra = 1
    else:
        pts = [(0.0, 0.0), (float(b), 0.0), (0.0, float(a))]             # right angle at vertex 0
        side = {0: labels.get("h"), 1: labels.get("c"), 2: labels.get("v")}
        ra = 0
    P, _ = _fit(pts, 4.0, 2.4)
    return _tikz(_tri_body(P, sides={k: v for k, v in side.items() if v}, right=ra))


@template("MK")
def pyth_hyp(rng, lvl):
    a, b, c = rng.choice(_EASY_TRIPLES if lvl <= 1 else _TRIPLES)
    u = rng.choice(["ft", "in", "cm", "m", "yd"])
    l1, l2 = (a, b) if rng.random() < 0.5 else (b, a)
    fig = _right_fig(a, b, {"h": _lab(b, u), "v": _lab(a, u), "c": "$x$"}, rng.choice(["left", "right"]))
    T = "".join(rng.choice(_NAMES))
    stem = choose(rng,
                  f"A right triangle has legs of {_w(l1, u)} and {_w(l2, u)}. What is the length of the hypotenuse?",
                  f"The legs of a right triangle measure {_w(l1, u)} and {_w(l2, u)}. How long is the hypotenuse?",
                  f"In right triangle {m(T)}, the legs are {_w(l1, u)} and {_w(l2, u)} long. What is the length {m('x')} of the hypotenuse?",
                  f"What is the value of {m('x')} in the right triangle shown, whose legs measure {_w(l1, u)} and {_w(l2, u)}?")
    k = math.gcd(a, b)
    base = (a // k, b // k, c // k)
    tip = None
    if k > 1 and base in ((3, 4, 5), (5, 12, 13), (8, 15, 17)):
        tip = (f"Spot the triple: {m(a)}-{m(b)}-? is {m(base[0])}-{m(base[1])}-{m(base[2])} "
               f"times {m(k)}, so the hypotenuse is {m(f'{base[2]} \\times {k} = {c}')}.")
    return Problem(
        stem=stem,
        answer=Q(c),
        fmt=_lenfmt(u),
        wrong=[(Q(a + b), r"adds the legs instead of using $a^2 + b^2 = c^2$"),
               (Q(a * a + b * b), "forgets to take the square root")],
        steps=[r"Use the Pythagorean theorem: $a^2 + b^2 = c^2$, where $c$ is the hypotenuse.",
               f"Square the legs and add: {m(f'{a}^2 + {b}^2 = {int_raw(a * a)} + {int_raw(b * b)} = {int_raw(a * a + b * b)}')}.",
               f"Take the square root: {m(f'c = \\sqrt{{{int_raw(a * a + b * b)}}} = {c}')} {u}."],
        tip=tip,
        figure=fig,
        near=_near_int(c, (1, 2, 3, 5)),
        check=_isqrt_check(a * a + b * b),
    )


# --------------------------------------------------------------------------
# level 2
# --------------------------------------------------------------------------

@template("MK")
def isosceles_angles(rng, lvl):
    mode = rng.choice(["vertex", "base"])
    A, B, C = rng.choice(_NAMES)
    if mode == "vertex":
        v = rng.randrange(36, 121, 2)
        base_ang = Q(180 - v) / 2
        ans = base_ang
        given_lab, target = {2: m(_d(v)), rng.choice([0, 1]): r"$x^\circ$"}, "base"
        stem = choose(rng,
                      f"In triangle {m(A + B + C)}, {m(f'{A}{B} = {A}{C}')} and {m(r'\angle ' + A)} measures {deg(v)}. "
                      f"What is the value of {m('x')}?",
                      f"The triangle shown is isosceles, with the two marked sides equal. The angle between the equal sides "
                      f"measures {deg(v)}. What is the value of {m('x')}?",
                      f"In isosceles triangle {m(A + B + C)}, the vertex angle {m(r'\angle ' + A)} is {deg(v)}. "
                      f"What is the value of {m('x')}, the measure of a base angle?")
        wrong = [(Q(180 - v), "forgets to split what is left between the two equal base angles"),
                 (Q(v), "assumes the base angle equals the vertex angle"),
                 (Q(360 - v) / 2, r"uses $360^\circ$ instead of $180^\circ$")]
        steps = [r"In an isosceles triangle the two base angles (opposite the equal sides) are equal. Call each one $x$.",
                 f"The angles add up to 180: {m(f'x + x + {v} = 180')}, so {m(f'2x = 180 - {v} = {180 - v}')}.",
                 f"Divide by 2: {m(f'x = {180 - v} \\div 2 = {int_raw(ans)}')}."]
        check = sp.solve(sp.Eq(2 * X + v, 180), X)[0]
        bang = base_ang
    else:
        bb = rng.randint(30, 72)
        need(bb != 60)
        ans = Q(180 - 2 * bb)
        bang = Q(bb)
        given_lab = {0: m(_d(bb)), 2: r"$x^\circ$"}
        stem = choose(rng,
                      f"In triangle {m(A + B + C)}, {m(f'{A}{B} = {A}{C}')} and {m(r'\angle ' + B)} measures {deg(bb)}. "
                      f"What is the value of {m('x')}?",
                      f"The triangle shown is isosceles, with the two marked sides equal. One base angle measures "
                      f"{deg(bb)}. What is the value of {m('x')}?",
                      f"Each base angle of isosceles triangle {m(A + B + C)} measures {deg(bb)}. "
                      f"What is the value of {m('x')}, the measure of the vertex angle?")
        wrong = [(Q(180 - bb), "subtracts only one base angle from $180^\\circ$"),
                 (Q(bb), "assumes the vertex angle equals the base angle"),
                 (Q(180 - bb) / 2, "splits the rest in half, as if the given angle were the vertex angle")]
        steps = [f"The two base angles of an isosceles triangle are equal, so both measure {deg(bb)}.",
                 f"The angles add up to 180: {m(f'x = 180 - {bb} - {bb} = 180 - {2 * bb} = {int_raw(ans)}')}."]
        check = sp.solve(sp.Eq(X + 2 * bb, 180), X)[0]
    w = 1.0
    h = w * math.tan(math.radians(float(bang)))
    P, _ = _fit([(-w, 0.0), (w, 0.0), (0.0, h)], 3.6, 2.9)
    # vertices: 0 = B (base left), 1 = C (base right), 2 = A (apex)
    fig = _tikz(_tri_body(P, angles=given_lab, ticks={1: 1, 2: 1}, verts={0: m(B), 1: m(C), 2: m(A)}))
    return Problem(stem=stem, answer=ans, fmt=num, wrong=wrong, steps=steps, figure=fig,
                   near=_near_int(ans, (5, 10, 15, 20), 180), check=check)


@template("MK")
def exterior_angle(rng, lvl):
    a, c = rng.randint(30, 85), rng.randint(30, 85)
    bint = 180 - a - c
    need(25 <= bint <= 110 and a != c)
    ext = a + c
    pts = _tri_points_from_angles(a, bint)
    # extend the base beyond B by 0.6 of the base length
    pts_ext = pts + [(1.6, 0.0)]
    S, sc = _fit(pts_ext, 4.6, 2.5)
    P, D = S[:3], S[3]
    mode = rng.choice(["ext", "ext", "remote"])
    if mode == "ext":
        labels = {0: m(_d(a)), 2: m(_d(c))}
        ext_lab = r"$x^\circ$"
        ans = Q(ext)
        stem = choose(rng,
                      f"In the figure, one side of the triangle is extended. The two interior angles shown measure "
                      f"{deg(a)} and {deg(c)}. What is the value of {m('x')}?",
                      f"A side of the triangle shown is extended to form an exterior angle of {m('x^\\circ')}. "
                      f"The two remote interior angles measure {deg(a)} and {deg(c)}. What is {m('x')}?")
        wrong = [(Q(bint), "finds the interior angle next to the exterior angle, not the exterior angle"),
                 (Q(360 - ext), r"subtracts from $360^\circ$"),
                 (Q(abs(a - c)), "subtracts the two remote angles instead of adding them")]
        steps = [r"An exterior angle of a triangle equals the sum of the two \emph{remote} (non-adjacent) interior angles.",
                 f"{m(f'x = {a} + {c} = {ext}')}.",
                 f"Check: the interior angle next to it is {m(f'180 - {ext} = {bint}')}, and "
                 f"{m(f'{a} + {c} + {bint} = 180')}. \\checkmark"]
        check = 180 - Q(180 - a - c)
    else:
        labels = {0: m(_d(a)), 2: r"$x^\circ$"}
        ext_lab = m(_d(ext))
        ans = Q(c)
        stem = choose(rng,
                      f"In the figure, one side of the triangle is extended to form a {deg(ext)} exterior angle. "
                      f"One remote interior angle measures {deg(a)}. What is the value of {m('x')}?",
                      f"The exterior angle shown measures {deg(ext)}, and one of the remote interior angles measures "
                      f"{deg(a)}. What is the value of {m('x')}?")
        wrong = [(Q(ext + a), "adds the angles instead of subtracting"),
                 (Q(180 - ext), "gives the interior angle next to the exterior angle"),
                 (Q(180 - a), "subtracts the known angle from 180 and ignores the exterior angle")]
        steps = [r"An exterior angle of a triangle equals the sum of the two remote interior angles.",
                 f"So {m(f'{a} + x = {ext}')}, and {m(f'x = {ext} - {a} = {c}')}."]
        check = sp.solve(sp.Eq(a + X, ext), X)[0]
    body = _tri_body(P, angles=labels)
    B, C = P[1], P[2]
    body.append(rf"\draw[thick] {_P(*B)} -- {_P(*D)};")
    up = math.degrees(math.atan2(C[1] - B[1], C[0] - B[0]))
    body.append(_arc_at(B, 0, up, 0.28))
    r = max(0.68, 0.45 / math.sin(math.radians(up / 2)))
    body.append(rf"\node at {_P(B[0] + r * math.cos(math.radians(up / 2)), B[1] + r * math.sin(math.radians(up / 2)))} {{{ext_lab}}};")
    return Problem(stem=stem, answer=ans, fmt=num, wrong=wrong, steps=steps, figure=_tikz(body),
                   near=_near_int(ans, (5, 10, 15, 20), 180), check=check)


@template("MK")
def pyth_leg(rng, lvl):
    a, b, c = rng.choice(_LEG_TRIPLES)
    u = rng.choice(["ft", "in", "cm", "m", "yd"])
    known, unknown = (a, b) if rng.random() < 0.5 else (b, a)
    labels = {"c": _lab(c, u)}
    if known == a:
        labels.update({"v": _lab(a, u), "h": "$x$"})
    else:
        labels.update({"h": _lab(b, u), "v": "$x$"})
    fig = _right_fig(a, b, labels, rng.choice(["left", "right"]))
    stem = choose(rng,
                  f"The hypotenuse of a right triangle is {_w(c, u)} long, and one leg is {_w(known, u)}. "
                  f"What is the length of the other leg?",
                  f"In the right triangle shown, the hypotenuse is {_w(c, u)} and one leg is {_w(known, u)}. "
                  f"What is the value of {m('x')}?",
                  f"A right triangle has a hypotenuse of {_w(c, u)} and a leg of {_w(known, u)}. How long is its other leg?")
    wrong = [(Q(c - known), "subtracts the lengths instead of their squares"),
             (Q(c * c - known * known), "forgets to take the square root"),
             (_isqrt_check(c * c + known * known), "adds the squares instead of subtracting them")]
    return Problem(
        stem=stem,
        answer=Q(unknown),
        fmt=_lenfmt(u),
        wrong=wrong,
        steps=[r"The hypotenuse is the longest side, so use $a^2 + b^2 = c^2$ and solve for the missing leg: "
               r"$\text{leg}^2 = c^2 - (\text{other leg})^2$.",
               f"{m(f'{c}^2 - {known}^2 = {int_raw(c * c)} - {int_raw(known * known)} = {int_raw(c * c - known * known)}')}.",
               f"Take the square root: {m(f'\\sqrt{{{int_raw(c * c - known * known)}}} = {unknown}')} {u}."],
        figure=fig,
        tip=_triple_tip(known, c, True),
        near=_near_int(unknown, (1, 2, 3, 5)),
        check=_isqrt_check(c * c - known * known),
        verify=lambda v: v * v + known * known == c * c,
    )


def _scaled(rng, lo, hi, pool=None):
    """A Pythagorean triple scaled into the range [lo, hi] for the hypotenuse."""
    pool = pool or [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]
    a, b, c = rng.choice(pool)                    # pick the family first, so 3-4-5 does not dominate
    opts = [(a * k, b * k, c * k) for k in range(1, 60) if lo <= c * k <= hi]
    need(bool(opts))
    return rng.choice(opts)


@template("AR")
def pyth_word(rng, lvl):
    who = person(rng)
    s = soldier(rng)
    if lvl >= 3:
        return _pyth_word_hard(rng, who, s)
    ctx = rng.choice(["ladder", "trip", "trip_mil", "wire", "tv", "kite"])
    if ctx == "ladder":
        a, b, c = _scaled(rng, 10, 30, [(3, 4, 5), (5, 12, 13), (7, 24, 25), (8, 15, 17)])
        need(a <= 10)
        stem = choose(rng,
                      f"A {m(c)}-foot ladder leans against a wall. The foot of the ladder is {m(a)} feet from the base of "
                      f"the wall. How high up the wall does the top of the ladder reach?",
                      f"{who.name} sets the foot of a {m(c)}-foot ladder {m(a)} feet away from the side of a house. "
                      f"How high up the wall does the ladder reach?")
        ans, k1, k2, u, hyp = Q(b), a, c, "ft", False
        setup = (f"The wall, the ground, and the ladder form a right triangle. The ladder ({m(c)} ft) is the hypotenuse.")
    elif ctx in ("trip", "trip_mil"):
        a, b, c = _scaled(rng, 10, 60) if ctx == "trip" else _scaled(rng, 5, 30)
        d1, d2 = rng.choice([("north", "east"), ("south", "west"), ("east", "north"), ("west", "south")])
        if rng.random() < 0.5:
            a, b = b, a
        if ctx == "trip":
            u = "mi"
            stem = (f"{who.name} drives {m(a)} miles {d1}, then {m(b)} miles {d2}. "
                    f"How far is {who.he} from the starting point, in a straight line?")
        else:
            u = "km"
            stem = (f"{s}'s patrol moves {m(a)} kilometers {d1}, then {m(b)} kilometers {d2}. "
                    f"What is the straight-line distance from the patrol back to its starting point?")
        ans, k1, k2, hyp = Q(c), a, b, True
        setup = f"Traveling {d1} and then {d2} makes a right angle, so the two legs of the trip and the straight-line distance form a right triangle."
    elif ctx == "wire":
        a, b, c = _scaled(rng, 15, 60)
        need(b >= 12)
        stem = choose(rng,
                      f"A guy wire runs from the top of a {m(b)}-foot pole to a stake in the ground {m(a)} feet from the "
                      f"base of the pole. How long is the wire?",
                      f"Engineers on base anchor a radio antenna that is {m(b)} feet tall with a cable from its top to a "
                      f"stake {m(a)} feet from its base. How long is the cable?")
        ans, k1, k2, u, hyp = Q(c), a, b, "ft", True
        setup = "The pole, the ground, and the wire form a right triangle with the wire as the hypotenuse."
    elif ctx == "tv":
        a, b, c = rng.choice([(15, 20, 25), (24, 32, 40), (30, 40, 50), (36, 48, 60), (45, 60, 75), (27, 36, 45)])
        stem = (f"A rectangular TV screen measures {m(c)} inches on the diagonal and is {m(b)} inches wide. "
                f"How tall is the screen?")
        ans, k1, k2, u, hyp = Q(a), b, c, "in", False
        setup = "The width, the height, and the diagonal of the screen form a right triangle with the diagonal as the hypotenuse."
    else:
        a, b, c = _scaled(rng, 50, 150, [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)])
        stem = (f"{who.name} flies a kite on a {m(c)}-foot string. The kite is directly above a point {m(a)} feet "
                f"from where {who.he} stands. How high is the kite? (Ignore {who.his} height.)")
        ans, k1, k2, u, hyp = Q(b), a, c, "ft", False
        setup = "The string is the hypotenuse of a right triangle; the ground distance and the height are the legs."
    if hyp:
        wrong = [(Q(k1 + k2), "adds the two distances instead of using the Pythagorean theorem"),
                 (Q(k1 * k1 + k2 * k2), "forgets to take the square root")]
        steps = [setup,
                 f"{m(f'{k1}^2 + {k2}^2 = {int_raw(k1 * k1)} + {int_raw(k2 * k2)} = {int_raw(k1 * k1 + k2 * k2)}')}.",
                 f"{m(f'\\sqrt{{{int_raw(k1 * k1 + k2 * k2)}}} = {int_raw(ans)}')}, so the answer is {_w(ans, u)}."]
        chk = _isqrt_check(k1 * k1 + k2 * k2)
    else:
        wrong = [(Q(k2 - k1), "subtracts the lengths instead of their squares"),
                 (Q(k2 * k2 - k1 * k1), "forgets to take the square root"),
                 (_isqrt_check(k1 * k1 + k2 * k2), "adds the squares instead of subtracting them")]
        steps = [setup,
                 f"Missing leg: {m(f'{k2}^2 - {k1}^2 = {int_raw(k2 * k2)} - {int_raw(k1 * k1)} = {int_raw(k2 * k2 - k1 * k1)}')}.",
                 f"{m(f'\\sqrt{{{int_raw(k2 * k2 - k1 * k1)}}} = {int_raw(ans)}')}, so the answer is {_w(ans, u)}."]
        chk = _isqrt_check(k2 * k2 - k1 * k1)
    tip = _triple_tip(k1, k2, not hyp)
    return Problem(stem=stem, answer=ans, fmt=_lenfmt(u), wrong=wrong, steps=steps, tip=tip,
                   near=_near_int(ans, (1, 2, 3, 5)), check=chk, section="AR")


def _pyth_word_hard(rng, who, s):
    if rng.random() < 0.5:
        # shortcut across a rectangular field
        a, b, c = rng.choice([(30, 40, 50), (45, 60, 75), (60, 80, 100), (75, 100, 125), (90, 120, 150),
                              (120, 160, 200), (150, 200, 250), (50, 120, 130)])
        place = rng.choice([("a rectangular park", who.name, "walks"), ("a rectangular parade field", s, "marches"),
                            ("a rectangular parking lot", who.name, "walks"), ("a rectangular field", s, "runs")])
        u = "yd" if "field" in place[0] else "ft"
        unit_w = "yards" if u == "yd" else "feet"
        stem = (f"{place[0][0].upper() + place[0][1:]} is {m(b)} {unit_w} long and {m(a)} {unit_w} wide. "
                f"{place[1]} {place[2]} diagonally across it instead of along two sides. How many {unit_w} shorter is the "
                f"diagonal route?")
        ans = Q(a + b - c)
        steps = [f"Going along two sides: {m(f'{a} + {b} = {int_raw(a + b)}')} {unit_w}.",
                 f"The diagonal is the hypotenuse: {m(f'\\sqrt{{{a}^2 + {b}^2}} = \\sqrt{{{int_raw(a * a + b * b)}}} = {c}')} {unit_w}.",
                 f"The savings: {m(f'{int_raw(a + b)} - {c} = {int_raw(ans)}')} {unit_w}."]
        wrong = [(Q(c), "gives the length of the diagonal, not the savings"),
                 (Q(a + b), "gives the length of the route along two sides"),
                 (Q(b - a), "subtracts the width from the length")]
        return Problem(stem=stem, answer=ans, fmt=_lenfmt(u), wrong=wrong, steps=steps, section="AR",
                       tip=_triple_tip(a, b, False),
                       near=_near_int(ans, (5, 10, 15, 20)), check=Q(a + b) - _isqrt_check(a * a + b * b))
    if rng.random() < 0.5:
        return _two_travelers(rng, who, s)
    # ladder moved: two DIFFERENT triples with the same 25-ft hypotenuse, so the
    # change in height is not equal to the change at the foot
    L = 25
    p1, p2 = rng.choice([(7, 15), (7, 20), (15, 7)])
    h1, h2 = {7: 24, 15: 20, 20: 15}[p1], {7: 24, 15: 20, 20: 15}[p2]
    out = p2 > p1
    if out:
        stem = choose(rng,
                      f"A {m(L)}-foot ladder leans against a wall with its foot {m(p1)} feet from the base of the wall. "
                      f"The foot of the ladder slides out until it is {m(p2)} feet from the wall. "
                      f"How many feet does the top of the ladder slide down the wall?",
                      f"{who.name} leans a {m(L)}-foot ladder against a building, with its foot {m(p1)} feet from the "
                      f"base of the wall. The foot slips until it is {m(p2)} feet from the wall. How far down the wall "
                      f"does the top of the ladder slide?",
                      f"{s} sets a {m(L)}-foot ladder against a barracks wall, with its foot {m(p1)} feet from the base "
                      f"of the wall. If the foot of the ladder is moved out to {m(p2)} feet from the wall, how many feet "
                      f"lower will the top of the ladder be?")
    else:
        stem = choose(rng,
                      f"A {m(L)}-foot ladder leans against a wall with its foot {m(p1)} feet from the base of the wall. "
                      f"The foot is pushed in until it is {m(p2)} feet from the wall. How many feet higher up the wall "
                      f"does the top of the ladder reach now?",
                      f"{s} sets a {m(L)}-foot ladder against a barracks wall, with its foot {m(p1)} feet from the base "
                      f"of the wall, then moves the foot in to {m(p2)} feet from the wall. How many feet does the top of "
                      f"the ladder rise?")
    ans = Q(abs(h1 - h2))
    steps = [f"The ladder, the wall, and the ground form a right triangle with the {m(L)}-foot ladder as the hypotenuse.",
             f"Before: height {m(f'= \\sqrt{{{L}^2 - {p1}^2}} = \\sqrt{{{int_raw(L * L - p1 * p1)}}} = {h1}')} feet.",
             f"After: height {m(f'= \\sqrt{{{L}^2 - {p2}^2}} = \\sqrt{{{int_raw(L * L - p2 * p2)}}} = {h2}')} feet.",
             f"The top {'slides down' if out else 'rises'} {m(f'{max(h1, h2)} - {min(h1, h2)} = {int_raw(ans)}')} feet."]
    wrong = [(Q(abs(p2 - p1)), f"assumes the top moves as far as the foot moves ({m(f'{max(p1, p2)} - {min(p1, p2)}')})"),
             (Q(h1), "gives the starting height of the ladder"),
             (Q(h2), "gives the final height of the ladder")]
    return Problem(stem=stem, answer=ans, fmt=_lenfmt("ft"), wrong=wrong, steps=steps, section="AR", must=1,
                   tip=r"Both positions are Pythagorean triples with hypotenuse $25$: $7$-$24$-$25$ and $15$-$20$-$25$.",
                   near=_near_int(ans, (1, 2, 3, 5)),
                   check=abs(_isqrt_check(L * L - p1 * p1) - _isqrt_check(L * L - p2 * p2)))


def _two_travelers(rng, who, s):
    """Two people leave the same point at right angles; distance apart after t hours."""
    ctx = rng.choice(["cars", "cyclists", "boats", "patrols", "hikers"])
    t = rng.choice([2, 3])
    if ctx == "cars":
        r1, r2 = rng.choice([(30, 40), (45, 60), (36, 48), (24, 45)])
        unit, uw = "mi", "miles"
        stem = (f"Two cars leave the same intersection at the same time. One drives north at {m(r1)} miles per hour "
                f"and the other drives east at {m(r2)} miles per hour. How far apart are the cars after {m(t)} hours?")
    elif ctx == "cyclists":
        r1, r2 = rng.choice([(9, 12), (12, 16), (5, 12), (8, 15)])
        unit, uw = "mi", "miles"
        stem = (f"{who.name} and a friend start biking from the same corner at the same time. {who.name} rides south at "
                f"{m(r1)} miles per hour and the friend rides west at {m(r2)} miles per hour. How far apart are they "
                f"after {m(t)} hours?")
    elif ctx == "boats":
        r1, r2 = rng.choice([(6, 8), (9, 12), (5, 12), (12, 16)])
        unit, uw = "mi", "miles"
        stem = (f"Two boats leave the same dock at the same time. One travels due east at {m(r1)} miles per hour and "
                f"the other travels due north at {m(r2)} miles per hour. How far apart are the boats after {m(t)} hours?")
    elif ctx == "patrols":
        r1, r2 = rng.choice([(3, 4), (6, 8), (5, 12)])
        unit, uw = "km", "kilometers"
        stem = (f"Two patrols leave a checkpoint at the same time. {s}'s patrol marches north at {m(r1)} kilometers per "
                f"hour, and the other marches east at {m(r2)} kilometers per hour. How far apart are the patrols after "
                f"{m(t)} hours?")
    else:
        r1, r2 = 3, 4
        unit, uw = "mi", "miles"
        stem = (f"Two hikers leave camp at the same time. One walks north at {m(r1)} miles per hour and the other walks "
                f"west at {m(r2)} miles per hour. How far apart are they after {m(t)} hours?")
    d1, d2 = r1 * t, r2 * t
    ans = _isqrt_check(d1 * d1 + d2 * d2)
    need(ans.is_integer)
    steps = [f"Distances after {m(t)} hours: {m(f'{r1} \\times {t} = {d1}')} and {m(f'{r2} \\times {t} = {d2}')} {uw}.",
             "The two paths meet at a right angle, so the distance between them is the hypotenuse of a right triangle.",
             f"{m(f'\\sqrt{{{d1}^2 + {d2}^2}} = \\sqrt{{{int_raw(d1 * d1)} + {int_raw(d2 * d2)}}} = '
                   f'\\sqrt{{{int_raw(d1 * d1 + d2 * d2)}}} = {int_raw(ans)}')} {uw}."]
    wrong = [(Q(d1 + d2), "adds the two distances instead of using the Pythagorean theorem"),
             (ans / t, "finds how far apart they are after 1 hour only"),
             (Q(d1 * d1 + d2 * d2), "forgets to take the square root"),
             (Q(d2 - d1), "subtracts the two distances")]
    return Problem(stem=stem, answer=ans, fmt=_lenfmt(unit), wrong=wrong, steps=steps, section="AR",
                   tip=_triple_tip(d1, d2, False),
                   near=_near_int(ans, (2, 4, 5, 10)),
                   check=Q(t) * sp.sqrt(r1 * r1 + r2 * r2))


def _range_check(p, q):
    """Independent route: try every whole-number third side (and the
    half-way values) and report the open interval that works."""
    ok = [Q(t) / 2 for t in range(1, 4 * (p + q)) if (Q(t) / 2 + p > q and Q(t) / 2 + q > p and p + q > Q(t) / 2)]
    return f"{m(f'{int_raw(min(ok) - R(1, 2))} < x < {int_raw(max(ok) + R(1, 2))}')}"


@template("MK")
def triangle_inequality(rng, lvl):
    mode = rng.choice(["third", "third", "range", "sets"])
    if mode == "range":
        p, q = sorted(rng.sample(range(3, 26), 2))
        lo, hi = q - p, p + q
        who = person(rng)
        ans = f"{m(f'{lo} < x < {hi}')}"
        wrong = [(f"{m(f'{lo} \\le x \\le {hi}')}", f"includes {m(lo)} and {m(hi)}, but then the sides would lie flat"),
                 (f"{m(f'{p} < x < {q}')}", "uses the two given sides as the limits"),
                 (f"{m(f'0 < x < {hi}')}", "forgets the lower limit (the difference of the sides)"),
                 (f"{m(f'{lo} < x < {q}')}", "uses the longer given side as the upper limit")]
        return Problem(
            stem=choose(rng,
                        f"Two sides of a triangle measure {m(p)} and {m(q)}. Which describes all possible lengths "
                        f"{m('x')} of the third side?",
                        f"{who.name} is making a triangle from two sticks {m(p)} inches and {m(q)} inches long and a third "
                        f"stick {m('x')} inches long. Which describes all possible values of {m('x')}?"),
            answer=ans,
            fmt=text,
            wrong=wrong,
            steps=[r"Triangle inequality: any two sides must add up to \emph{more} than the third side.",
                   f"The third side must be shorter than the sum: {m(f'x < {p} + {q} = {hi}')}.",
                   f"It must be longer than the difference (otherwise {m(f'x + {p}')} would not reach past {m(q)}): "
                   f"{m(f'x > {q} - {p} = {lo}')}.",
                   f"Together: {ans}."],
            check=_range_check(p, q),
        )
    if mode == "third":
        p, q = sorted(rng.sample(range(3, 26), 2))
        lo, hi = q - p, p + q
        ans = rng.randint(lo + 1, hi - 1)
        bad_lo = [v for v in range(1, lo) if v != ans]
        bad_hi = list(range(hi + 1, hi + 8))
        wrong = [(Q(lo), f"equals {m(f'{q} - {p}')}; the two shorter sides would lie flat along the longest side"),
                 (Q(hi), f"equals {m(f'{p} + {q}')}; the two given sides would lie flat along the third side")]
        if bad_lo:
            v = rng.choice(bad_lo)
            wrong.append((Q(v), f"is too short: {m(f'{v} + {p} < {q}')}"))
        v = rng.choice(bad_hi)
        wrong.append((Q(v), f"is too long: {m(f'{p} + {q} < {v}')}"))

        def near(r):
            out = [Q(v) for v in bad_lo + bad_hi]
            r.shuffle(out)
            return out
        who = person(rng)
        return Problem(
            stem=choose(rng,
                        f"Two sides of a triangle measure {m(p)} and {m(q)}. Which of the following could be the length "
                        f"of the third side?",
                        f"A triangle has sides of length {m(p)} and {m(q)}. Which of these could be the length of its third side?",
                        f"{who.name} has two boards, {m(p)} feet and {m(q)} feet long, and wants to make a triangular "
                        f"frame with a third board. Which of these board lengths, in feet, would work?",
                        f"Two sides of a triangular garden measure {m(p)} yards and {m(q)} yards. Which of the following "
                        f"could be the length, in yards, of the third side?"),
            answer=Q(ans),
            fmt=num,
            wrong=wrong,
            near=near,
            steps=[r"Triangle inequality: any two sides must add up to \emph{more} than the third side.",
                   f"So the third side must be longer than {m(f'{q} - {p} = {lo}')} and shorter than "
                   f"{m(f'{p} + {q} = {hi}')}: between {m(lo)} and {m(hi)}, not equal to either.",
                   f"Only {m(ans)} is in that range."],
            verify=lambda t: lo < t < hi,
            check=Q(ans),
        )
    # which set of three lengths can form a triangle?
    for _ in range(100):
        a, b = sorted(rng.sample(range(2, 15), 2))
        good = (a, b, rng.randint(b + 1, a + b - 1)) if a > 1 and b + 1 <= a + b - 1 else None
        if good is None:
            continue
        a2, b2 = sorted(rng.sample(range(2, 15), 2))
        flat = (a2, b2, a2 + b2)
        a3, b3 = sorted(rng.sample(range(2, 12), 2))
        short = (a3, b3, a3 + b3 + rng.randint(1, 5))
        a4, b4 = sorted(rng.sample(range(2, 12), 2))
        short2 = (a4, b4, a4 + b4 + rng.randint(2, 7))
        sets = [good, flat, short, short2]
        if len({tuple(s) for s in sets}) == 4:
            break
    else:
        need(False)

    def tx(t):
        return f"{m(t[0])}, {m(t[1])}, {m(t[2])}"

    def ok(t):
        x1, x2, x3 = sorted(t)
        return x1 + x2 > x3

    def why_bad(t):
        x1, x2, x3 = sorted(t)
        sign = "=" if x1 + x2 == x3 else "<"
        return f"fails because {m(f'{x1} + {x2} = {x1 + x2}')}, which is not more than {m(x3)}" if sign == "=" \
            else f"fails because {m(f'{x1} + {x2} = {x1 + x2}')} is less than {m(x3)}"
    # the choices are shown in this same (sorted) order -- see order= below --
    # so the checks can be listed choice by choice, A to D
    checks = []
    for letter, t in zip("ABCD", sorted(sets)):
        x1, x2, x3 = t
        verdict = "\\checkmark" if ok(t) else r"$\times$"
        rel = ">" if x1 + x2 > x3 else ("=" if x1 + x2 == x3 else "<")
        checks.append(f"({letter}) {tx(t)}: {m(f'{x1} + {x2} = {x1 + x2} {rel} {x3}')} {verdict}")
    lookup = {tx(t): t for t in sets}
    survivors = [t for t in sets if ok(t)]
    return Problem(
        stem=choose(rng,
                    "Which of the following could be the lengths of the three sides of a triangle?",
                    "Which set of side lengths could form a triangle?",
                    "A student has four sets of sticks. Which set can be put together, end to end, to form a triangle?"),
        answer=tx(good),
        fmt=text,
        wrong=[(tx(t), why_bad(t)) for t in sets[1:]],
        order=lambda v: lookup[v],
        steps=[r"For three lengths to form a triangle, the two shorter ones must add up to \emph{more} than the longest one.",
               "Test each choice: " + "; ".join(checks) + ".",
               f"Only {tx(good)} works."],
        check=tx(survivors[0]) if len(survivors) == 1 else "ambiguous",
    )


# --------------------------------------------------------------------------
# level 3
# --------------------------------------------------------------------------

def _special_fig(kind, labels):
    """kind '45' or '30'.  labels: {'h': tex (bottom leg), 'v': tex (left leg), 'c': tex (hypotenuse)}."""
    if kind == "45":
        pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
        angs = {1: r"$45^\circ$", 2: r"$45^\circ$"}
    else:
        pts = [(0.0, 0.0), (math.sqrt(3), 0.0), (0.0, 1.0)]
        angs = {1: r"$30^\circ$", 2: r"$60^\circ$"}
    P, _ = _fit(pts, 3.6, 2.5)
    sides = {0: labels.get("h"), 1: labels.get("c"), 2: labels.get("v")}
    return _tikz(_tri_body(P, sides={k: v for k, v in sides.items() if v}, angles=angs, right=0))


@template("MK")
def special_right(rng, lvl):
    s2, s3 = sp.sqrt(2), sp.sqrt(3)
    case = rng.choice(["45_leg_hyp", "45_hyp_leg", "45_hypint_leg",
                       "30_short_hyp", "30_short_long", "30_hyp_short", "30_hyp_long", "30_long_short", "30_long_hyp"])
    k = rng.randint(2, 15)
    deg45, deg30 = sp.pi / 4, sp.pi / 6
    if case.startswith("45"):
        kind = "45"
        name = r"$45^\circ$-$45^\circ$-$90^\circ$"
        ratio = r"In a $45^\circ$-$45^\circ$-$90^\circ$ triangle the sides are in the ratio $1 : 1 : \sqrt{2}$ (leg : leg : hypotenuse)."
        if case == "45_leg_hyp":
            given, ans = Q(k), k * s2
            lab = {"h": m(latex(given)), "c": "$x$"}
            what = "the hypotenuse"
            steps = [ratio, f"Hypotenuse = leg {m(r'\times \sqrt{2}')} = {m(f'{k}\\sqrt{{2}}')}."]
            wrong = [(Q(2 * k), r"doubles the leg, which is the $30^\circ$-$60^\circ$-$90^\circ$ rule for the hypotenuse"),
                     (k * s3, r"multiplies the leg by $\sqrt{3}$ (the $30^\circ$-$60^\circ$-$90^\circ$ long-leg rule) instead of by $\sqrt{2}$"),
                     (Q(k), "gives the other leg, not the hypotenuse"),
                     (Q(k) / 2 * s2, r"divides the leg by $\sqrt{2}$ instead of multiplying")]
            check = given / sp.cos(deg45)
        elif case == "45_hyp_leg":
            given, ans = k * s2, Q(k)
            lab = {"c": m(latex(given)), "h": "$x$"}
            what = "each leg"
            steps = [ratio, f"Leg = hypotenuse {m(r'\div \sqrt{2}')} = {m(f'{k}\\sqrt{{2}} \\div \\sqrt{{2}} = {k}')}."]
            wrong = [(Q(2 * k), r"multiplies the hypotenuse by $\sqrt{2}$ instead of dividing"),
                     (k * s2 / 2, r"halves the hypotenuse, which is the $30^\circ$-$60^\circ$-$90^\circ$ rule for the short leg"),
                     (k * s2, r"solves $x^2 = c^2$ instead of $x^2 + x^2 = c^2$, forgetting the second leg")]
            check = given * sp.cos(deg45)
        else:
            h = 2 * k
            given, ans = Q(h), k * s2
            lab = {"c": m(latex(given)), "v": "$x$"}
            what = "each leg"
            steps = [ratio, f"Leg = hypotenuse {m(r'\div \sqrt{2}')} = {m(f'\\frac{{{h}}}{{\\sqrt{{2}}}}')}.",
                     f"Multiply top and bottom by {m(r'\sqrt{2}')}: "
                     f"{m(f'\\frac{{{h}\\sqrt{{2}}}}{{2}} = {k}\\sqrt{{2}}')}."]
            wrong = [(h * s2, r"multiplies the hypotenuse by $\sqrt{2}$ instead of dividing"),
                     (Q(k), r"halves the hypotenuse, which is the $30^\circ$-$60^\circ$-$90^\circ$ rule for the short leg"),
                     (k * s3, r"halves the hypotenuse and multiplies by $\sqrt{3}$, the $30^\circ$-$60^\circ$-$90^\circ$ rule for the long leg")]
            check = given * sp.sin(deg45)
    else:
        kind = "30"
        name = r"$30^\circ$-$60^\circ$-$90^\circ$"
        ratio = (r"In a $30^\circ$-$60^\circ$-$90^\circ$ triangle the sides are in the ratio $1 : \sqrt{3} : 2$ "
                 r"(short leg : long leg : hypotenuse). The short leg is across from the $30^\circ$ angle.")
        short, long_, hyp = Q(k), k * s3, Q(2 * k)
        if case == "30_short_hyp":
            given, ans, lab, what = short, hyp, {"v": m(latex(short)), "c": "$x$"}, "the hypotenuse"
            steps = [ratio, f"Hypotenuse = 2 {m(r'\times')} short leg = {m(f'2 \\times {k} = {2 * k}')}."]
            wrong = [(k * s3, "gives the long leg, not the hypotenuse"),
                     (k * s2, r"multiplies the short leg by $\sqrt{2}$, the $45^\circ$-$45^\circ$-$90^\circ$ rule for the hypotenuse"),
                     (Q(k) / 2, "halves the short leg instead of doubling it")]
            check = short / sp.sin(deg30)
        elif case == "30_short_long":
            given, ans, lab, what = short, long_, {"v": m(latex(short)), "h": "$x$"}, "the longer leg"
            steps = [ratio, f"Long leg = short leg {m(r'\times \sqrt{3}')} = {m(f'{k}\\sqrt{{3}}')}."]
            wrong = [(Q(2 * k), "gives the hypotenuse, not the long leg"),
                     (k * s2, r"multiplies the short leg by $\sqrt{2}$ (the $45^\circ$-$45^\circ$-$90^\circ$ rule) instead of by $\sqrt{3}$"),
                     (Q(k) / 3 * s3, r"divides the short leg by $\sqrt{3}$ instead of multiplying")]
            check = short / sp.tan(deg30)
        elif case == "30_hyp_short":
            given, ans, lab, what = hyp, short, {"c": m(latex(hyp)), "v": "$x$"}, "the shorter leg"
            steps = [ratio, f"Short leg = hypotenuse {m(r'\div 2')} = {m(f'{2 * k} \\div 2 = {k}')}."]
            wrong = [(Q(4 * k), "doubles the hypotenuse instead of halving it"),
                     (k * s3, "gives the long leg, not the short leg"),
                     (k * s2, r"divides the hypotenuse by $\sqrt{2}$, the $45^\circ$-$45^\circ$-$90^\circ$ rule for a leg")]
            check = hyp * sp.sin(deg30)
        elif case == "30_hyp_long":
            given, ans, lab, what = hyp, long_, {"c": m(latex(hyp)), "h": "$x$"}, "the longer leg"
            steps = [ratio, f"Short leg = hypotenuse {m(r'\div 2')} = {m(f'{2 * k} \\div 2 = {k}')}.",
                     f"Long leg = short leg {m(r'\times \sqrt{3}')} = {m(f'{k}\\sqrt{{3}}')}."]
            wrong = [(Q(k), "gives the short leg, not the long leg"),
                     (2 * k * s3, r"multiplies the hypotenuse by $\sqrt{3}$ instead of the short leg"),
                     (k * s2, r"divides the hypotenuse by $\sqrt{2}$, the $45^\circ$-$45^\circ$-$90^\circ$ rule for a leg")]
            check = hyp * sp.cos(deg30)
        elif case == "30_long_short":
            given, ans, lab, what = long_, short, {"h": m(latex(long_)), "v": "$x$"}, "the shorter leg"
            steps = [ratio, f"Short leg = long leg {m(r'\div \sqrt{3}')} = {m(f'{k}\\sqrt{{3}} \\div \\sqrt{{3}} = {k}')}."]
            wrong = [(Q(3 * k), r"multiplies by $\sqrt{3}$ instead of dividing"),
                     (Q(2 * k), "gives the hypotenuse, not the short leg"),
                     (k * s3 / 2, "halves the long leg instead of dividing it by $\\sqrt{3}$")]
            check = long_ * sp.tan(deg30)
        else:
            given, ans, lab, what = long_, hyp, {"h": m(latex(long_)), "c": "$x$"}, "the hypotenuse"
            steps = [ratio, f"Short leg = long leg {m(r'\div \sqrt{3}')} = {m(f'{k}\\sqrt{{3}} \\div \\sqrt{{3}} = {k}')}.",
                     f"Hypotenuse = 2 {m(r'\times')} short leg = {m(f'2 \\times {k} = {2 * k}')}."]
            wrong = [(Q(k), "gives the short leg, not the hypotenuse"),
                     (2 * k * s3, "doubles the long leg instead of the short leg"),
                     (k * sp.sqrt(6), r"multiplies the long leg by $\sqrt{2}$, as if the triangle were $45^\circ$-$45^\circ$-$90^\circ$")]
            check = long_ / sp.cos(deg30)
    fig = _special_fig(kind, lab)
    gname = {"leg": "each leg", "hyp": "the hypotenuse", "hypint": "the hypotenuse",
             "short": "the shorter leg", "long": "the longer leg"}[case.split("_")[1]]
    gv = f"{m(latex(given))} units"
    stem = choose(rng,
                  f"In the {name} triangle shown, {gname} measures {gv}. What is the length {m('x')} of {what}?",
                  f"The figure shows a {name} triangle in which {gname} is {gv} long. What is the value of {m('x')}?",
                  f"In a {name} triangle, {gname} is {gv} long. How many units long is {what}?")

    def near(r):
        out = [ans * 2, ans / 2, ans * 3 / 2, ans * 3]
        r.shuffle(out)
        return out
    return Problem(stem=stem, answer=ans, fmt=expr, wrong=wrong, steps=steps, figure=fig,
                   check=sp.nsimplify(sp.simplify(check)), near=near)


@template("MK")
def similar_triangles(rng, lvl):
    k = rng.choice([R(3, 2), Q(2), R(5, 2), R(4, 3), R(5, 3), Q(2)])
    a = rng.randint(3, 15)
    b = rng.randint(3, 15)
    need(a != b and (k * a).is_integer and (k * b).is_integer and k * max(a, b) <= 36)
    need(R(2, 3) <= Q(b) / a <= R(3, 2))
    small_unknown = rng.random() < 0.35
    A, B, C, D, E, F = rng.choice([("A", "B", "C", "D", "E", "F"), ("P", "Q", "R", "S", "T", "U"),
                                   ("J", "K", "L", "M", "N", "P"), ("A", "B", "C", "P", "Q", "R"),
                                   ("D", "E", "F", "R", "S", "T")])
    gamma = rng.randint(55, 80)
    g = math.radians(gamma)
    shape = [(0.0, 0.0), (float(a), 0.0), (float(b) * math.cos(g), float(b) * math.sin(g))]
    ws = max(px for px, _ in shape)
    hs = max(py for _, py in shape)
    sc = min(4.6 / (ws * (1 + float(k))), 2.9 / (hs * float(k)))   # cm per unit; leaves 0.9 cm gap
    Ps = [(px * sc, py * sc) for px, py in shape]
    off = ws * sc + 0.9
    Pb = [(px * sc * float(k) + off, py * sc * float(k)) for px, py in shape]
    ka, kb = k * a, k * b
    if small_unknown:
        sl = {0: _lab(a), 2: "$x$"}
        bl = {0: _lab(ka), 2: _lab(kb)}
        ans = Q(b)
        stem = choose(rng,
                      f"In the figure, {m(r'\triangle ' + A + B + C)} is similar to {m(r'\triangle ' + D + E + F)}, with "
                      f"{m(f'{D}{E} = {int_raw(ka)}')}, {m(f'{D}{F} = {int_raw(kb)}')}, and {m(f'{A}{B} = {a}')}. "
                      f"What is the value of {m('x')}?",
                      f"{m(r'\triangle ' + A + B + C + r' \sim \triangle ' + D + E + F)}. If {m(f'{D}{E} = {int_raw(ka)}')}, "
                      f"{m(f'{D}{F} = {int_raw(kb)}')}, and {m(f'{A}{B} = {a}')}, what is the length {m('x')} of "
                      f"{m(A + C)}?")
        steps = [f"The order of the letters gives the matching vertices: {m(f'{A} \\leftrightarrow {D}')}, "
                 f"{m(f'{B} \\leftrightarrow {E}')}, {m(f'{C} \\leftrightarrow {F}')}. So {m('x')} is side {m(A + C)}, "
                 f"which matches {m(D + F)} ({m(int_raw(kb))}), and {m(A + B)} matches {m(D + E)}.",
                 f"Corresponding sides are proportional. The scale factor from {m(r'\triangle ' + A + B + C)} to "
                 f"{m(r'\triangle ' + D + E + F)} is {m(f'{int_raw(ka)} \\div {a} = {latex(k)}')}.",
                 f"Divide the big triangle's side by the scale factor: {m(f'x = {int_raw(kb)} \\div {latex(k)} = {b}')}."]
        wrong = [(Q(kb) - (ka - a), "subtracts the difference between corresponding sides instead of dividing by the scale factor"),
                 (Q(kb) * k, "multiplies by the scale factor instead of dividing"),
                 (Q(a) * ka / kb, "matches the wrong sides in the proportion")]
        check = sp.solve(sp.Eq(Q(a) / ka, X / kb), X)[0]
    else:
        sl = {0: _lab(a), 2: _lab(b)}
        bl = {0: _lab(ka), 2: "$x$"}
        ans = kb
        stem = choose(rng,
                      f"In the figure, {m(r'\triangle ' + A + B + C)} is similar to {m(r'\triangle ' + D + E + F)}, with "
                      f"{m(f'{A}{B} = {a}')}, {m(f'{A}{C} = {b}')}, and {m(f'{D}{E} = {int_raw(ka)}')}. "
                      f"What is the value of {m('x')}?",
                      f"{m(r'\triangle ' + A + B + C + r' \sim \triangle ' + D + E + F)}. If {m(f'{A}{B} = {a}')}, "
                      f"{m(f'{A}{C} = {b}')}, and {m(f'{D}{E} = {int_raw(ka)}')}, what is the length {m('x')} of "
                      f"{m(D + F)}?")
        steps = [f"The order of the letters gives the matching vertices: {m(f'{A} \\leftrightarrow {D}')}, "
                 f"{m(f'{B} \\leftrightarrow {E}')}, {m(f'{C} \\leftrightarrow {F}')}. So {m('x')} is side {m(D + F)}, "
                 f"which matches {m(A + C)} ({m(b)}), and {m(D + E)} matches {m(A + B)}.",
                 f"Corresponding sides are proportional: {m(f'\\frac{{{D}{F}}}{{{A}{C}}} = \\frac{{{D}{E}}}{{{A}{B}}}')}, "
                 f"so {m(f'\\frac{{x}}{{{b}}} = \\frac{{{int_raw(ka)}}}{{{a}}}')}.",
                 f"The scale factor is {m(f'{int_raw(ka)} \\div {a} = {latex(k)}')}.",
                 f"Multiply: {m(f'x = {b} \\times {latex(k)} = {int_raw(kb)}')}."]
        wrong = [(Q(b) + (ka - a), "adds the difference between corresponding sides instead of multiplying by the scale factor"),
                 (Q(b) / k, "divides by the scale factor instead of multiplying"),
                 (Q(a) * ka / b, "matches the wrong sides in the proportion")]
        check = sp.solve(sp.Eq(X / b, Q(ka) / a), X)[0]
    body = _tri_body(Ps, sides=sl, verts={0: m(A), 1: m(B), 2: m(C)}, arcs=False)
    body += _tri_body(Pb, sides=bl, verts={0: m(D), 1: m(E), 2: m(F)}, arcs=False)
    return Problem(stem=stem, answer=ans, fmt=num, wrong=wrong, steps=steps, figure=_tikz(body),
                   near=_near_int(ans, (1, 2, 3, 4)), check=check)


@template("AR")
def shadow(rng, lvl):
    who = person(rng)
    s = soldier(rng)
    ref = rng.choice([("person", 6), ("person", 5), ("post", 4), ("post", 3), ("soldier", 6)])
    rh = ref[1]
    obj, lo, hi = rng.choice([("flagpole", 20, 45), ("tree", 15, 60), ("building", 30, 120),
                              ("radio tower", 60, 200), ("light pole", 12, 30), ("water tower", 50, 150)])
    for _ in range(200):
        rs = rng.randint(2, 12)
        H = rng.randint(lo, hi)
        os_ = Q(H) * rs / rh
        if os_.is_integer and rs != rh and os_ != H:
            break
    else:
        need(False)
    if ref[0] == "person":
        first = f"{who.name}, who is {m(rh)} feet tall, casts a shadow {m(rs)} feet long."
    elif ref[0] == "soldier":
        first = f"{s}, who is {m(rh)} feet tall, casts a {m(rs)}-foot shadow."
    else:
        first = f"A {m(rh)}-foot fence post casts a shadow {m(rs)} feet long."
    where = "on base " if ref[0] == "soldier" else ""
    stem = (f"{first} At the same time, a {obj} {where}casts a shadow {m(int_raw(os_))} feet long. "
            f"How tall is the {obj}?")
    ans = Q(H)
    tip = None
    times = {2: "twice", 3: "three times", 4: "four times", 5: "five times"}
    if rs % rh == 0 and rs // rh in times:
        tip = (f"Shortcut: at this time of day every shadow is {times[rs // rh]} as long as the object is tall, "
               f"so the {obj} is {m(f'{int_raw(os_)} \\div {rs // rh} = {int_raw(ans)}')} feet tall.")
    elif rh % rs == 0 and rh // rs in times:
        tip = (f"Shortcut: at this time of day every object is {times[rh // rs]} as tall as its shadow is long, so the {obj} is "
               f"{m(f'{int_raw(os_)} \\times {rh // rs} = {int_raw(ans)}')} feet tall.")
    refname = {"person": who.name, "soldier": s, "post": "the post"}[ref[0]]
    d = rh - rs
    diff_why = (f"assumes the {obj} is {m(abs(d))} feet {'shorter' if d < 0 else 'taller'} than its shadow, "
                f"just as {refname} is, instead of using a ratio")
    wrong = [(os_ + d, diff_why),
             (os_ * rs / rh, "sets up the proportion upside down"),
             (os_ * rh, "multiplies by the height but forgets to divide by the shadow")]
    return Problem(
        stem=stem,
        answer=ans,
        fmt=_lenfmt("ft"),
        wrong=wrong,
        section="AR",
        steps=[f"Objects and their shadows at the same time of day form similar triangles, so "
               f"{m(r'\frac{\text{height}}{\text{shadow}}')} is the same for both: "
               f"{m(f'\\frac{{h}}{{{int_raw(os_)}}} = \\frac{{{rh}}}{{{rs}}}')}.",
               f"Cross-multiply: {m(f'{rs}h = {rh} \\times {int_raw(os_)} = {int_raw(rh * os_)}')}.",
               f"Divide by {m(rs)}: {m(f'h = {int_raw(rh * os_)} \\div {rs} = {int_raw(ans)}')} feet."],
        tip=tip,
        near=_near_int(ans, (2, 4, 5, 10)),
        check=sp.solve(sp.Eq(X * rs, rh * os_), X)[0],
    )


PLAN = [
    # (template, level, count) -- easy -> hard; 25 problems
    (third_angle, 1, 3),
    (classify_triangle, 1, 2),
    (pyth_hyp, 1, 3),
    (isosceles_angles, 2, 2),
    (exterior_angle, 2, 2),
    (pyth_leg, 2, 2),
    (pyth_word, 2, 2),
    (triangle_inequality, 2, 2),
    (special_right, 3, 3),
    (similar_triangles, 3, 1),
    (shadow, 3, 2),
    (pyth_word, 3, 1),
]
