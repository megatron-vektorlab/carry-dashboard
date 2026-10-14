"""Chapter 20 - Volume & Surface Area."""
import sympy as sp

from ..core import (R, Q, x, y, z, Problem, need, num, dec, m, F, dec_raw, int_raw,
                    frac_raw, person, soldier, choose, template)

NUM = 20
TITLE = r"Volume \& Surface Area"   # LaTeX-ready: render.py puts TITLE straight into \chapter{}
PART = 3

INTRO = r"""
\emph{Volume} is the amount of space inside a solid, measured in cubic units
(in$^3$, ft$^3$). \emph{Surface area} is the total area of all the faces you
could paint or wrap, measured in square units (in$^2$, ft$^2$).

\begin{concept}{Boxes and cubes}
\begin{minipage}[c]{0.62\linewidth}
A rectangular box (prism) with length $l$, width $w$, and height $h$:
\[ V = l \times w \times h \qquad SA = 2lw + 2lh + 2wh \]
The surface area adds three \emph{pairs} of matching faces: top and bottom,
front and back, left and right.

A cube with edge $s$ has six identical square faces:
\[ V = s^3 \qquad SA = 6s^2 \]
\end{minipage}\hfill
\begin{minipage}[c]{0.34\linewidth}\centering
\begin{tikzpicture}[scale=0.8]
\fill[black!8] (0,1.4) -- (0.7,1.9) -- (3.2,1.9) -- (2.5,1.4) -- cycle;
\fill[black!18] (2.5,0) -- (3.2,0.5) -- (3.2,1.9) -- (2.5,1.4) -- cycle;
\draw[thick] (0,0) rectangle (2.5,1.4);
\draw[thick] (0,1.4) -- (0.7,1.9) -- (3.2,1.9) -- (2.5,1.4);
\draw[thick] (2.5,0) -- (3.2,0.5) -- (3.2,1.9);
\draw[dashed] (0,0) -- (0.7,0.5) -- (3.2,0.5);
\draw[dashed] (0.7,0.5) -- (0.7,1.9);
\node[below] at (1.25,0) {$l$};
\node[left] at (0,0.7) {$h$};
\node[below right] at (2.8,0.22) {$w$};
\end{tikzpicture}
\end{minipage}
\end{concept}

\begin{concept}{Cylinders, cones, and spheres}
Any solid with the same shape all the way up has
$V = (\text{area of the base}) \times \text{height}$. For a cylinder the base
is a circle, so
\[ V = \pi r^2 h \]
A cone holds exactly $\frac{1}{3}$ as much as a cylinder with the same base
and height: $V = \frac{1}{3}\pi r^2 h$. A sphere of radius $r$ has
$V = \frac{4}{3}\pi r^3$. (In this book, the cone and sphere formulas are
given in the problem when you need them.)
\end{concept}

\begin{concept}{Units}
Use one unit for every length \emph{before} you multiply: $6$ inches $=
\frac{1}{2}$ foot, $4$ inches $= \frac{1}{3}$ foot.
\begin{itemize}
\item $1 \text{ ft}^3 = 12 \times 12 \times 12 = 1{,}728 \text{ in}^3$
\item $1 \text{ yd}^3 = 3 \times 3 \times 3 = 27 \text{ ft}^3$ (concrete, gravel,
  and soil are sold by the cubic yard)
\item $1 \text{ ft}^3$ of water is about $7.5$ gallons
\end{itemize}
\end{concept}

\begin{example}{Worked example}
A fish tank is 3 feet long, 2 feet wide, and 2 feet tall. If 1 cubic foot
holds 7.5 gallons, how many gallons does the tank hold?

\textbf{Solution.} $V = 3 \times 2 \times 2 = 12$ cubic feet, and
$12 \times 7.5 = 90$ gallons.
\end{example}

\begin{tip}
Multiply in the easiest order: $25 \times 7 \times 4 = (25 \times 4)
\times 7 = 700$. Scaling: if every edge is doubled, the surface area is
multiplied by $2^2 = 4$ and the volume by $2^3 = 8$.
\end{tip}

\begin{trap}
\begin{itemize}
\item Adding the dimensions instead of multiplying them.
\item Mixing inches and feet in one calculation.
\item Counting only three faces for surface area (each face has a twin).
\item Using the diameter instead of the radius in $\pi r^2 h$.
\item Dividing cubic feet by 9 (or 3) instead of 27 to get cubic yards.
\end{itemize}
\end{trap}
"""

PI = sp.pi

_UNITS = {"in": ("inch", "inches"), "ft": ("foot", "feet"), "cm": ("centimeter", "centimeters"),
          "m": ("meter", "meters"), "yd": ("yard", "yards"), "mm": ("millimeter", "millimeters")}
_ABS = ["in", "ft", "cm", "m"]


def _w(ab, n=2):
    return _UNITS[ab][0] if n == 1 else _UNITS[ab][1]


def _cuw(ab):
    return "cubic " + _UNITS[ab][1]


def _sqw(ab):
    return "square " + _UNITS[ab][1]


def _u(fmt, ab, power=1):
    """Number with a unit: _u(num, 'ft', 3) -> $120\\text{ ft}^3$."""
    sup = "" if power == 1 else f"^{power}"

    def f(v):
        return m(rf"{fmt(v)[1:-1]}\text{{ {ab}}}{sup}")
    return f


def _int_near(v, steps=(1, -1, 2, -2)):
    def f(rng):
        out = [Q(v) + s_ for s_ in steps if Q(v) + s_ > 0]
        rng.shuffle(out)
        return out
    return f


def _whole(vals):
    """Keep only whole-number distractors."""
    return [w for w in vals if Q(w[0]).is_integer]


# values in terms of pi ---------------------------------------------------------

def _split(v):
    v = sp.expand(Q(v))
    k = v.coeff(PI)
    c = sp.expand(v - k * PI)
    need(k.is_rational and c.is_rational, "not of the form c + k*pi")
    return sp.Rational(c), sp.Rational(k)


def _kpi(k):
    k = sp.Rational(k)
    if k == 1:
        return r"\pi"
    if k.q == 1:
        return int_raw(k) + r"\pi"
    top = "" if k.p == 1 else int_raw(k.p)
    return rf"\frac{{{top}\pi}}{{{k.q}}}"


def _pi_raw(v):
    c, k = _split(v)
    if k == 0:
        return frac_raw(c)
    if c == 0:
        return ("-" if k < 0 else "") + _kpi(abs(k))
    if k > 0:
        return f"{_kpi(k)} {'+' if c > 0 else '-'} {frac_raw(abs(c))}"
    if c > 0:
        return f"{frac_raw(c)} - {_kpi(-k)}"
    return f"-{_kpi(-k)} - {frac_raw(-c)}"


def _pi_u(ab, power=1):
    sup = "" if power == 1 else f"^{power}"

    def f(v):
        c, k = _split(v)
        raw = _pi_raw(v)
        if c != 0 and k != 0:
            raw = f"({raw})"
        return m(rf"{raw}\text{{ {ab}}}{sup}")
    return f


def _pi_near(ans, alts=None):
    c, k = _split(ans)

    def f(rng):
        if alts is not None:
            out = list(alts)
        else:
            a = abs(k)
            st = 1 if a <= 12 else 2 if a <= 30 else 5 if a <= 80 else 10 if a <= 200 else 50
            out = [c + (k + j * st) * PI for j in (1, -1, 2, -2)]
        out = [v for v in out if Q(v) > 0 and _split(v)[1] != 0 and sp.expand(v - ans) != 0]
        rng.shuffle(out)
        return out
    return f


def _lab(v, ab=None):
    s = f"${int_raw(v) if Q(v).is_integer else dec_raw(v)}$"
    return s + (f" {ab}" if ab else "")


# figures ------------------------------------------------------------------------

def _r2(v):
    return round(float(v), 2)


def _fig_box(l, w, h, ab=None, labels=("l", "w", "h")):
    """Oblique box; returns (tikz, drawn_to_scale)."""
    L, W, H = float(l), float(w), float(h)
    sc = min(4.0 / (L + 0.41 * W), 2.7 / (H + 0.29 * W))
    Ld, Wd, Hd = L * sc, W * sc, H * sc
    to_scale = Ld >= 0.6 and Hd >= 0.6 and Wd >= 0.8
    Ld, Hd, Wd = max(Ld, 0.6), max(Hd, 0.6), max(Wd, 0.8)
    if not to_scale:   # re-fit after clamping
        f_ = min(1.0, 4.0 / (Ld + 0.41 * Wd), 2.7 / (Hd + 0.29 * Wd))
        Ld, Wd, Hd = Ld * f_, Wd * f_, Hd * f_
    dx, dy = _r2(0.41 * Wd), _r2(0.29 * Wd)
    Ld, Hd = _r2(Ld), _r2(Hd)
    X, Y = _r2(Ld + dx), _r2(Hd + dy)
    out = [rf"\fill[black!8] (0,{Hd}) -- ({dx},{Y}) -- ({X},{Y}) -- ({Ld},{Hd}) -- cycle;",
           rf"\fill[black!18] ({Ld},0) -- ({X},{dy}) -- ({X},{Y}) -- ({Ld},{Hd}) -- cycle;",
           rf"\draw[thick] (0,0) rectangle ({Ld},{Hd});",
           rf"\draw[thick] (0,{Hd}) -- ({dx},{Y}) -- ({X},{Y}) -- ({Ld},{Hd});",
           rf"\draw[thick] ({Ld},0) -- ({X},{dy}) -- ({X},{Y});",
           rf"\draw[dashed] (0,0) -- ({dx},{dy}) -- ({X},{dy});",
           rf"\draw[dashed] ({dx},{dy}) -- ({dx},{Y});"]
    if "l" in labels:
        out.append(rf"\node[below] at ({_r2(Ld / 2)},0) {{\small {_lab(l, ab)}}};")
    if "h" in labels:
        out.append(rf"\node[left] at (0,{_r2(Hd / 2)}) {{\small {_lab(h, ab)}}};")
    if "w" in labels:
        out.append(rf"\node[below right] at ({_r2(Ld + dx / 2 - 0.05)},{_r2(dy / 2 - 0.02)}) {{\small {_lab(w, ab)}}};")
    return "\n".join(out), to_scale


def _fit_round(r, h, hmin):
    """Drawn radius and height for a cylinder or cone: (rx, ry, Hd, to_scale)."""
    rx = 0.9
    Hd = rx * float(h) / float(r)
    if Hd > 2.6:                       # tall: shrink the drawn radius instead
        rx = max(0.45, 2.6 * float(r) / float(h))
        Hd = rx * float(h) / float(r)
    to_scale = hmin <= Hd <= 2.6
    Hd = _r2(min(max(Hd, hmin), 2.6))
    rx = _r2(rx)
    return rx, _r2(0.27 * rx), Hd, to_scale


def _fig_cyl(r, h, ab, use_d=False):
    rx, ry, Hd, to_scale = _fit_round(r, h, 0.6)
    out = [rf"\fill[black!8] (0,{Hd}) ellipse ({rx} and {ry});",
           rf"\draw[thick] (-{rx},0) arc (180:360:{rx} and {ry});",
           rf"\draw[dashed] ({rx},0) arc (0:180:{rx} and {ry});",
           rf"\draw[thick] (0,{Hd}) ellipse ({rx} and {ry});",
           rf"\draw[thick] (-{rx},0) -- (-{rx},{Hd});",
           rf"\draw[thick] ({rx},0) -- ({rx},{Hd});",
           rf"\fill (0,{Hd}) circle (1.1pt);"]
    if use_d:
        out.append(rf"\draw (-{rx},{Hd}) -- ({rx},{Hd});")
        out.append(rf"\node[above] at (0,{_r2(Hd + ry)}) {{\small {_lab(2 * r, ab)}}};")
    else:
        out.append(rf"\draw (0,{Hd}) -- ({rx},{Hd});")
        out.append(rf"\node[above] at ({rx / 2},{_r2(Hd + ry - 0.02)}) {{\small {_lab(r, ab)}}};")
    out.append(rf"\node[right] at ({rx},{_r2(Hd / 2)}) {{\small {_lab(h, ab)}}};")
    return "\n".join(out), to_scale


def _fig_cone(r, h, ab, use_d=False):
    rx, ry, Hd, to_scale = _fit_round(r, h, 0.5)
    xd = rx + 0.3                                  # height dimension line, outside the cone
    out = [rf"\draw[thick] (-{rx},0) arc (180:360:{rx} and {ry});",
           rf"\draw[dashed] ({rx},0) arc (0:180:{rx} and {ry});",
           rf"\draw[thick] (-{rx},0) -- (0,{Hd}) -- ({rx},0);",
           rf"\draw[dashed] (0,0) -- (0,{Hd});",
           r"\draw (0.15,0) -- (0.15,0.15) -- (0,0.15);",
           r"\fill (0,0) circle (1.1pt);",
           rf"\draw[thin, black!60] (0.08,{Hd}) -- ({_r2(xd + 0.1)},{Hd});",
           rf"\draw[{{Stealth[length=3pt]}}-{{Stealth[length=3pt]}}] ({_r2(xd)},0) -- ({_r2(xd)},{Hd})"
           rf" node[midway, right] {{\small {_lab(h, ab)}}};"]
    if use_d:
        out.append(rf"\draw (-{rx},0) -- ({rx},0);")
        out.append(rf"\node[below] at (0,-{ry}) {{\small {_lab(2 * r, ab)}}};")
    else:
        out.append(rf"\draw (0,0) -- ({rx},0);")
        out.append(rf"\node[below] at ({rx / 2},-0.2) {{\small {_lab(r, ab)}}};")
    return "\n".join(out), to_scale


def _fig_sphere(r, ab, use_d=False):
    Rd = 1.05
    out = [rf"\draw[thick] (0,0) circle ({Rd});",
           rf"\draw (-{Rd},0) arc (180:360:{Rd} and 0.3);",
           rf"\draw[dashed] ({Rd},0) arc (0:180:{Rd} and 0.3);",
           r"\fill (0,0) circle (1.1pt);"]
    if use_d:
        out.append(rf"\draw (145:{Rd}) -- (-35:{Rd});")
        out.append(rf"\node[below left, inner sep=1pt] at (-35:{_r2(Rd * 0.55)}) {{\small {_lab(2 * r, ab)}}};")
    else:
        out.append(rf"\draw (0,0) -- (-35:{Rd});")
        out.append(rf"\node[below left, inner sep=1pt] at (-35:{_r2(Rd * 0.62)}) {{\small {_lab(r, ab)}}};")
    return "\n".join(out)


# --------------------------------------------------------------------------------
# templates
# --------------------------------------------------------------------------------

# (description, unit, length range, width range, height range)
_BOXES = [
    ("A shipping box", "in", (8, 24), (6, 16), (4, 12)),
    ("A footlocker", "in", (28, 32), (14, 16), (10, 12)),
    ("A toolbox", "in", (14, 20), (6, 9), (6, 9)),
    ("A storage bin", "in", (16, 24), (10, 16), (8, 12)),
    ("A fish tank", "in", (20, 30), (10, 12), (12, 16)),
    ("A storage shed", "ft", (8, 12), (6, 8), (7, 8)),
    ("A cargo trailer", "ft", (8, 14), (5, 7), (5, 6)),
    ("A raised garden bed", "ft", (6, 10), (3, 4), (1, 2)),
]


@template("MK")
def box_volume(rng, lvl):
    style = rng.choice(["fig", "fig", "text", "ctx"])
    fig = None
    if style == "ctx":
        what, ab, L_, W_, H_ = rng.choice(_BOXES)
        l, w, h = rng.randint(*L_), rng.randint(*W_), rng.randint(*H_)
        stem = (f"{what} is {m(l)} {_w(ab)} long, {m(w)} {_w(ab)} wide, and {m(h)} {_w(ab, h)} "
                f"{'deep' if 'garden' in what else 'high'}. What is its volume?")
    else:
        ab = rng.choice(_ABS)
        l, w, h = rng.randint(3, 15), rng.randint(2, 10), rng.randint(2, 12)
        need(l >= w)
        if style == "fig":
            fig, ok = _fig_box(l, w, h, ab)
            stem = (f"The rectangular box shown is {m(l)} {_w(ab)} long, {m(w)} {_w(ab)} wide, and {m(h)} {_w(ab)} "
                    f"high. What is its volume?" + ("" if ok else " (Figure not drawn to scale.)"))
        else:
            stem = choose(rng,
                          f"A rectangular box is {m(l)} {_w(ab)} long, {m(w)} {_w(ab)} wide, and {m(h)} {_w(ab)} high. "
                          f"What is its volume?",
                          f"What is the volume of a rectangular prism with length {m(l)} {_w(ab)}, width {m(w)} "
                          f"{_w(ab)}, and height {m(h)} {_w(ab)}?")
    need(len({l, w, h}) >= 2)
    V = l * w * h
    need(V <= 5000)
    sa = 2 * (l * w + l * h + w * h)
    # friendly order: multiply the pair whose product is "roundest" first
    pairs = sorted([(l, w, h), (l, h, w), (w, h, l)], key=lambda t: ((t[0] * t[1]) % 10 != 0, t[0] * t[1]))
    a_, b_, c_ = pairs[0]
    return Problem(
        stem=stem, figure=fig,
        answer=Q(V), fmt=_u(num, ab, 3), near=_int_near(V, (l * w, -l * w, w * h, -w * h)),
        wrong=[(Q(l + w + h), "adds the three dimensions instead of multiplying them"),
               (Q(l * w), "finds the area of the base only and forgets the height"),
               (Q(sa), "finds the surface area, not the volume"),
               (Q(V) / 2, None)],
        steps=[f"The volume of a rectangular box is {m(r'V = l \times w \times h')}.",
               f"Multiply in a convenient order: {m(f'{a_} \\times {b_} = {a_ * b_}')}, then "
               f"{m(f'{a_ * b_} \\times {c_} = {int_raw(V)}')}.",
               f"The volume is {num(V)} {_cuw(ab)}."],
        check=sum(Q(l * w) for _ in range(h)),      # h layers of l*w unit cubes
        verify=lambda v: v / l / w == h,
    )


@template("MK")
def cube(rng, lvl):
    thing, units = rng.choice([("A cube", _ABS), ("A cube", _ABS), ("A cube-shaped box", ["in", "cm"]),
                               ("A cube-shaped water tank", ["ft", "m"]), ("A cube-shaped storage crate", ["ft", "in"])])
    ab = rng.choice(units)
    if lvl == 1:
        s = rng.randint(2, 12)
        V, SA = s**3, 6 * s * s
        if rng.random() < 0.5:
            fig, _ = _fig_box(s, s, s, ab, labels=("l",))
            return Problem(
                stem=choose(rng, f"{thing} has edges that are each {m(s)} {_w(ab)} long. What is its volume?",
                            f"What is the volume of a cube with an edge length of {m(s)} {_w(ab)}?"),
                figure=fig if thing == "A cube" else None,
                answer=Q(V), fmt=_u(num, ab, 3), near=_int_near(V, (s * s, -s * s, 2 * s * s)),
                wrong=[(Q(3 * s), "multiplies the edge by 3 instead of cubing it"),
                       (Q(s * s), "squares the edge instead of cubing it"),
                       (Q(SA), "finds the surface area, not the volume")],
                steps=[f"All three dimensions of a cube equal the edge: {m(r'V = s^3 = s \times s \times s')}.",
                       f"{m(f'{s} \\times {s} = {s * s}')}, and {m(f'{s * s} \\times {s} = {int_raw(V)}')}.",
                       f"The volume is {num(V)} {_cuw(ab)}."],
                check=Q(s)**2 * s,
            )
        return Problem(
            stem=choose(rng, f"{thing} has edges that are each {m(s)} {_w(ab)} long. What is its total surface area?",
                        f"What is the surface area of a cube with an edge length of {m(s)} {_w(ab)}?"),
            answer=Q(SA), fmt=_u(num, ab, 2), near=_int_near(SA, (s * s, -s * s, 2 * s * s)),
            wrong=[(Q(V), "finds the volume, not the surface area"),
                   (Q(4 * s * s), "counts only four of the six faces"),
                   (Q(6 * s), "forgets to square the edge"),
                   (Q(s * s), "finds the area of only one face")],
            steps=[f"A cube has 6 identical square faces. One face has area {m(f'{s}^2 = {s * s}')} {_sqw(ab)}.",
                   f"All six faces: {m(f'6 \\times {s * s} = {int_raw(SA)}')} {_sqw(ab)}."],
            check=sum(Q(s) * s for _ in range(6)),
        )
    # level 2: work backward from one measurement
    s = rng.randint(2, 12)
    V, SA = s**3, 6 * s * s
    kind = rng.choice(["V_SA", "V_s", "SA_V"])
    if kind == "V_SA":
        return Problem(
            stem=choose(rng, f"{thing} has a volume of {num(V)} {_cuw(ab)}. What is its total surface area?",
                        f"The volume of {thing[0].lower() + thing[1:]} is {num(V)} {_cuw(ab)}. "
                        f"What is the total area of its six faces?"),
            answer=Q(SA), fmt=_u(num, ab, 2), near=_int_near(SA, (s * s, -s * s, 2 * s * s)),
            wrong=[(Q(4 * s * s), "counts only four of the six faces"),
                   (Q(s * s), "finds the area of only one face"),
                   (Q(6 * s), "forgets to square the edge"),
                   (Q(V), "gives the volume, not the surface area")],
            steps=[f"Find the edge: which number cubed is {num(V)}? {m(f'{s} \\times {s} \\times {s} = {int_raw(V)}')}, "
                   f"so {m(f's = {s}')} {_w(ab)}.",
                   f"One face: {m(f'{s}^2 = {s * s}')}. Six faces: {m(f'6 \\times {s * s} = {int_raw(SA)}')} {_sqw(ab)}."],
            verify=lambda v: v == 6 * (sp.integer_nthroot(V, 3)[0])**2,
        )
    if kind == "V_s":
        need(s in (3, 4, 6, 9))
        return Problem(
            stem=choose(rng, f"{thing} has a volume of {num(V)} {_cuw(ab)}. How long is each edge?",
                        f"The volume of {thing[0].lower() + thing[1:]} is {num(V)} {_cuw(ab)}. What is the length "
                        f"of one edge?"),
            answer=Q(s), fmt=_u(num, ab), near=_int_near(s, (1, -1, 2, 3)),
            wrong=_whole([(Q(V) / 3, "divides the volume by 3 instead of finding the cube root"),
                          (Q(V) / 6, "divides the volume by 6"),
                          (sp.sqrt(V), "takes the square root instead of the cube root"),
                          (Q(s * s), None)]),
            steps=[f"The volume of a cube is {m('s^3')}, so look for the number that, cubed, gives {num(V)}.",
                   f"{m(f'{s} \\times {s} \\times {s} = {s * s} \\times {s} = {int_raw(V)}')}, so each edge is {m(s)} {_w(ab)}."],
            verify=lambda v: v**3 == V,
        )
    return Problem(
        stem=choose(rng, f"{thing} has a total surface area of {num(SA)} {_sqw(ab)}. What is its volume?",
                    f"The six faces of {thing[0].lower() + thing[1:]} have a total area of {num(SA)} {_sqw(ab)}. "
                    f"What is its volume?"),
        answer=Q(V), fmt=_u(num, ab, 3), near=_int_near(V, (s * s, -s * s, 2 * s * s)),
        wrong=[(Q(s * s), "stops at the area of one face"),
               (Q(SA), "gives the surface area, not the volume"),
               (Q(3 * s), "multiplies the edge by 3 instead of cubing it"),
               (Q((s + 1)**3), None)],
        steps=[f"Each of the 6 faces has area {m(f'{num(SA)[1:-1]} \\div 6 = {s * s}')} {_sqw(ab)}.",
               f"A square with area {m(s * s)} has side {m(s)}, so the edge is {m(s)} {_w(ab)}.",
               f"Volume: {m(f'{s}^3 = {int_raw(V)}')} {_cuw(ab)}."],
        verify=lambda v: v == (sp.sqrt(Q(SA) / 6))**3,
    )


def _faces_area(l, w, h):
    """Surface area by adding the areas of the six face polygons (independent check)."""
    P = sp.Polygon
    faces = [P((0, 0), (l, 0), (l, w), (0, w)), P((0, 0), (l, 0), (l, h), (0, h)),
             P((0, 0), (w, 0), (w, h), (0, h))]
    return sum(abs(f_.area) for f_ in faces + faces)


@template("MK")
def box_surface(rng, lvl):
    style = rng.choice(["fig", "fig", "paint", "wrap"])
    fig = None
    if style == "fig":
        ab = rng.choice(_ABS)
        l, w, h = rng.randint(3, 12), rng.randint(2, 8), rng.randint(2, 10)
        fig, ok = _fig_box(l, w, h, ab)
        stem = (f"The closed rectangular box shown is {m(l)} {_w(ab)} long, {m(w)} {_w(ab)} wide, and {m(h)} "
                f"{_w(ab)} high. What is its total surface area?" + ("" if ok else " (Figure not drawn to scale.)"))
    elif style == "paint":
        ab = "ft"
        l, w, h = rng.randint(3, 8), rng.randint(2, 4), rng.randint(2, 4)
        who = choose(rng, person(rng).name, soldier(rng))
        stem = (f"{who} is painting all six outside faces of a wooden crate that is {m(l)} feet long, "
                f"{m(w)} feet wide, and {m(h)} feet tall. How many square feet will be painted?")
    else:
        ab = "in"
        l, w, h = rng.randint(8, 20), rng.randint(4, 12), rng.randint(2, 8)
        p = person(rng)
        stem = (f"{p.name} wants to cover a gift box with wrapping paper with no overlap. The box is "
                f"{m(l)} inches long, {m(w)} inches wide, and {m(h)} inches tall. How many square inches "
                f"of paper will cover the whole box?")
    need(len({l, w, h}) == 3)
    a1, a2, a3 = l * w, l * h, w * h
    SA = 2 * (a1 + a2 + a3)
    return Problem(
        stem=stem, figure=fig,
        answer=Q(SA), fmt=_u(num, ab, 2),
        near=_int_near(SA, (2 * a3, -2 * a3, 2 * a1, -2 * a2)),
        wrong=[(Q(a1 + a2 + a3), "adds three faces but forgets that each face has a matching opposite face"),
               (Q(l * w * h), "finds the volume, not the surface area"),
               (Q(2 * (a2 + a3)), "leaves out the top and bottom"),
               (Q(6 * a1), "assumes all six faces are the same size as the bottom")],
        steps=[f"The box has three pairs of matching faces: top and bottom ({m(f'{l} \\times {w} = {a1}')}), "
               f"front and back ({m(f'{l} \\times {h} = {a2}')}), and the two ends ({m(f'{w} \\times {h} = {a3}')}).",
               f"Add one face of each pair: {m(f'{a1} + {a2} + {a3} = {a1 + a2 + a3}')}.",
               f"Double it for the matching faces: {m(f'2 \\times {a1 + a2 + a3} = {int_raw(SA)}')} {_sqw(ab)}."],
        check=_faces_area(l, w, h),
    )


@template("MK")
def cylinder(rng, lvl):
    if lvl == 1:
        ab = rng.choice(_ABS)
        r, h = rng.randint(2, 10), rng.randint(2, 15)
        need(r != h)
        V = r * r * h * PI
        fig, ok = _fig_cyl(r, h, ab)
        return Problem(
            stem=(f"What is the volume of the cylinder shown? The radius is {m(r)} {_w(ab)} and the height is "
                  f"{m(h)} {_w(ab, h)}." + ("" if ok else " (Figure not drawn to scale.)")),
            figure=fig,
            answer=V, fmt=_pi_u(ab, 3),
            near=_pi_near(V, [r * r * (h + 1) * PI, r * r * (h - 1) * PI, (r + 1)**2 * h * PI, 2 * r * r * h * PI]),
            wrong=[(2 * r * h * PI, r"uses $2\pi r$ instead of $\pi r^2$ for the base"),
                   (r * h * PI, "forgets to square the radius"),
                   (4 * r * r * h * PI, "uses the diameter in place of the radius"),
                   (r * r * PI, "finds the area of the base only")],
            steps=[f"The volume of a cylinder is (area of the base) {m(r'\times')} height: {m(r'V = \pi r^2 h')}.",
                   f"Base: {m(rf'\pi \times {r}^2 = {r * r}\pi')}.",
                   f"Volume: {m(rf'{r * r}\pi \times {h} = {_pi_raw(V)}')} {_cuw(ab)}."],
            check=PI * Q(2 * r)**2 * h / 4,
        )
    kind = rng.choice(["diam", "diam", "approx"])
    if kind == "diam":
        ab = rng.choice(_ABS)
        d, h = rng.choice(range(4, 21, 2)), rng.randint(2, 15)
        r = d // 2
        V = r * r * h * PI
        fig, ok = _fig_cyl(r, h, ab, use_d=True)
        return Problem(
            stem=(f"The cylinder shown has a diameter of {m(d)} {_w(ab)} and a height of {m(h)} {_w(ab, h)}. "
                  f"What is its volume?" + ("" if ok else " (Figure not drawn to scale.)")),
            figure=fig,
            answer=V, fmt=_pi_u(ab, 3),
            near=_pi_near(V, [r * r * (h + 1) * PI, r * r * (h - 1) * PI, (r + 1)**2 * h * PI, 2 * r * r * h * PI]),
            wrong=[(d * d * h * PI, "uses the diameter in place of the radius"),
                   (d * h * PI, r"uses $\pi d$ (the circumference) instead of the area of the base"),
                   (R(d * d, 2) * h * PI, "squares the diameter and then halves it; halve first"),
                   (r * h * PI, "forgets to square the radius")],
            steps=[f"The radius is half the diameter: {m(f'r = {d} \\div 2 = {r}')} {_w(ab)}.",
                   f"Base: {m(rf'\pi r^2 = \pi \times {r}^2 = {r * r}\pi')} {_sqw(ab)}.",
                   f"Volume: {m(rf'V = \pi r^2 h = {r * r}\pi \times {h} = {_pi_raw(V)}')} {_cuw(ab)}."],
            check=PI * Q(d)**2 * h / 4,
        )
    # 3.14 with friendly numbers
    r, h = rng.choice([(1, 3), (1, 4), (1, 5), (2, 3), (2, 5), (2, 10), (5, 2), (5, 4), (10, 2), (10, 3),
                       (2, 4), (1, 10), (3, 10), (5, 10), (4, 5)])
    what, ab = rng.choice([("a cylindrical water tank", "ft"), ("a cylindrical rain barrel", "ft"),
                           ("a round silo", "m"), ("a cylindrical fuel tank", "ft"),
                           ("a cylindrical storage tank", "m")])
    need(not (what == "a cylindrical rain barrel" and r > 2) and not (what == "a round silo" and r < 2))
    P = R(314, 100)
    base = r * r
    V = P * base * h
    p = person(rng)
    return Problem(
        stem=(f"{what[0].upper() + what[1:]} has a radius of {m(r)} {_w(ab, r)} and a height of {m(h)} {_w(ab, h)}. "
              f"What is its volume? Use 3.14 for {m(r'\pi')}."),
        answer=V, fmt=_u(dec, ab, 3),
        wrong=[w_ for w_ in [(P * 2 * r * h, r"uses $2\pi r$ instead of $\pi r^2$"),
                             (P * 4 * base * h, "uses the diameter in place of the radius"),
                             (P * base, "finds the area of the base only"),
                             (3 * base * h, r"uses 3 for $\pi$ instead of 3.14")]
               if not _same_val(w_[0], V)],
        steps=[f"Use {m(r'V = \pi r^2 h')}. The base: {m(rf'\pi r^2 \approx 3.14 \times {r}^2 = 3.14 \times {base} = {dec_raw(P * base)}')}.",
               f"Multiply by the height: {m(f'{dec_raw(P * base)} \\times {h} = {dec_raw(V)}')} {_cuw(ab)}."],
        check=Q(314) * r * r * h / 100,
    )


def _same_val(a_, b_):
    return sp.simplify(Q(a_) - Q(b_)) == 0


# (description, length choices, width choices, depth choices) -- all in feet
_TANKS = [
    ("{P}'s rectangular fish tank", [3, 4, 5, 6], [2], [2]),
    ("A water trough on {P}'s farm", [4, 6, 8, 10], [2, 3], [2]),
    ("{P}'s backyard pond", [6, 8, 10, 12], [4, 5, 6], [2, 3]),
    ("The water tank on {S}'s field trailer", [5, 6, 7, 8], [3, 4, 5], [2, 3]),
    ("A water storage tank at a forward operating base", [8, 9, 10, 12, 14], [6, 8], [4, 5]),
    ("A small swimming pool at {P}'s apartment complex", [12, 15, 16, 18, 20], [8, 10, 12], [3, 4]),
]


@template("AR")
def fill_tank(rng, lvl):
    what, Ls, Ws, Hs = rng.choice(_TANKS)
    what = what.format(P=person(rng).name, S=soldier(rng))
    l, w, h = rng.choice(Ls), rng.choice(Ws), rng.choice(Hs)
    V = l * w * h
    G = R(15, 2)
    note = "(1 cubic foot holds 7.5 gallons.)"
    if lvl == 2:
        gal = V * G
        need(gal.is_integer)
        return Problem(
            stem=(f"{what} is {m(l)} feet long, {m(w)} feet wide, and {m(h)} feet deep. How many gallons of water "
                  f"does it hold when it is full? {note}"),
            answer=gal, fmt=_u(num, "gal"),
            near=_int_near(gal, (G * l * w, -G * l * w, 2 * G * l * w)),
            wrong=_whole([(Q(V), "finds the volume in cubic feet but forgets to change it to gallons"),
                          (Q(V) / G, "divides by 7.5 instead of multiplying"),
                          (2 * (l * w + l * h + w * h) * G, "uses the surface area instead of the volume"),
                          (Q(V) * 7, "uses 7 gallons per cubic foot instead of 7.5")]),
            steps=[f"Volume: {m(f'{l} \\times {w} \\times {h} = {int_raw(V)}')} cubic feet.",
                   f"Each cubic foot holds 7.5 gallons: {m(f'{V} \\times 7.5 = {int_raw(gal)}')} gallons."],
            tip=(f"Multiplying by 7.5 is the same as multiplying by 15 and halving: "
                 f"{m(f'{V} \\times 15 = {int_raw(15 * V)}')}, and {m(f'{int_raw(15 * V)} \\div 2 = {int_raw(gal)}')}."),
            verify=lambda v: v * 2 / 15 == l * w * h,
        )
    # level 3: fill to a depth with a pump
    dep = rng.choice([Q(k) for k in range(1, h)] + [R(k, 2) for k in range(1, 2 * h) if k % 2])
    need(0 < dep < h)
    gal = l * w * dep * G
    pump = rng.choice(["a garden hose that delivers", "a pump that delivers"])
    rate = rng.choice([5, 6, 8, 10] if "hose" in pump else [15, 20, 25, 30, 40, 50])
    mins = gal / rate
    full = V * G / rate
    need(gal.is_integer and mins.is_integer and 5 <= mins <= 180 and (full * 10).is_integer)
    dep_t = dec_raw(dep)
    return Problem(
        stem=(f"{what} is {m(l)} feet long, {m(w)} feet wide, and {m(h)} feet deep. It is being filled with "
              f"{pump} {m(rate)} gallons per minute. How many minutes will it take to fill it to a depth of "
              f"{m(dep_t)} {'foot' if dep == 1 else 'feet'}? {note}"),
        answer=mins, fmt=_u(dec, "min"), must=1,
        near=_int_near(mins, (mins / 2, -mins / 2, mins, -mins * R(2, 3))),
        wrong=[w_ for w_ in [(full, f"uses the tank's full depth of {h} ft instead of the water depth of {dep_t} ft"),
                             (l * w * dep / rate, "forgets to change cubic feet to gallons"),
                             (gal, "finds the number of gallons, not the number of minutes"),
                             (l * w * dep / G / rate, "divides by 7.5 instead of multiplying")]
               if (Q(w_[0]) * 10).is_integer],
        steps=[f"Volume of water: {m(f'{l} \\times {w} \\times {dep_t} = {dec_raw(l * w * dep)}')} cubic feet "
               f"(use the water depth, not the tank's full depth).",
               f"Gallons: {m(f'{dec_raw(l * w * dep)} \\times 7.5 = {int_raw(gal)}')}.",
               f"Time: {m(f'{int_raw(gal)} \\div {rate} = {int_raw(mins)}')} minutes."],
        check=Q(l) * w * dep * 15 / (2 * rate),
    )


@template("AR")
def how_many_fit(rng, lvl):
    # kind, unit, edge choices, (length range), (width range), (height range)
    kind, ab, edges, Lr, Wr, Hr = rng.choice([
        ("cubes", "in", [2, 3], (6, 24), (4, 18), (4, 18)),
        ("blocks", "in", [2, 3, 4], (18, 36), (12, 24), (12, 24)),
        ("crates", "ft", [2, 3, 4], (12, 40), (6, 8), (6, 8)),
        ("boxes", "in", [4, 6], (12, 36), (12, 30), (12, 24)),
    ])
    e = rng.choice(edges)

    def pick(lo, hi):
        opts = [t for t in range(lo, hi + 1) if t % e == 0]
        need(opts)
        return rng.choice(opts)
    L, W, H = pick(*Lr), pick(*Wr), pick(*Hr)
    need(L >= W and len({L, W, H}) >= 2)
    nL, nW, nH = L // e, W // e, H // e
    ans = nL * nW * nH
    need(ans <= 500)
    Vb = L * W * H
    s_ = soldier(rng)
    p = person(rng)
    if kind == "crates":
        stem = (f"{s_} is loading cube-shaped crates that measure {m(e)} feet on each side into a cargo container "
                f"that is {m(L)} feet long, {m(W)} feet wide, and {m(H)} feet high. What is the greatest number of "
                f"crates that will fit inside?")
    elif kind == "boxes":
        stem = (f"A warehouse packs cube-shaped boxes that measure {m(e)} inches on each side into a carton that is "
                f"{m(L)} inches long, {m(W)} inches wide, and {m(H)} inches high. How many boxes fit in one carton?")
    elif kind == "blocks":
        stem = (f"{p.name} is packing wooden blocks shaped like cubes, {m(e)} inches on each side, into a toy chest "
                f"that is {m(L)} inches long, {m(W)} inches wide, and {m(H)} inches deep. How many blocks will fill "
                f"the chest?")
    else:
        stem = (f"How many cubes that measure {m(e)} inches on each side are needed to fill a box that is "
                f"{m(L)} inches long, {m(W)} inches wide, and {m(H)} inches high?")
    return Problem(
        stem=stem,
        answer=Q(ans), fmt=num, near=_int_near(ans, (nL * nW, -nL * nW, nW * nH, -nW * nH)),
        wrong=_whole([(Q(Vb) / e, "divides the volume by the edge length instead of by the volume of one cube"),
                      (Q(nL * nW), "counts only the bottom layer"),
                      (Q(nL + nW + nH), "adds the counts along each edge instead of multiplying"),
                      (Q(Vb), "finds the volume of the container but forgets to divide")]),
        steps=[f"Count how many fit along each edge: {m(f'{L} \\div {e} = {nL}')}, {m(f'{W} \\div {e} = {nW}')}, "
               f"and {m(f'{H} \\div {e} = {nH}')}.",
               f"Multiply: {m(f'{nL} \\times {nW} \\times {nH} = {ans}')}."],
        tip=(f"Check with volumes: the container holds {m(f'{L} \\times {W} \\times {H} = {int_raw(Vb)}')} cubic "
             f"{'feet' if ab == 'ft' else 'inches'}, and one cube is {m(f'{e}^3 = {e**3}')}, so "
             f"{m(f'{int_raw(Vb)} \\div {e**3} = {ans}')}."),
        check=Q(Vb) / e**3,
    )


@template("AR")
def concrete(rng, lvl):
    kind = rng.choice(["slab", "slab", "trench", "sandbox", "mulch"])
    if kind in ("slab", "mulch"):
        t = rng.choice([3, 4, 6] if kind == "slab" else [3, 4, 6])
        L, W = rng.randint(6, 30), rng.randint(4, 24)
        if kind == "mulch":
            L, W = rng.randint(6, 30), rng.randint(3, 12)
        ft3 = R(L * W * t, 12)
        need(ft3.is_integer and (ft3 / 27).is_integer and 1 <= ft3 / 27 <= 12)
        yd3 = ft3 / 27
        tf = R(t, 12)
        p = person(rng)
        if kind == "slab":
            stem = (f"{p.name} is pouring a concrete patio {m(L)} feet long and {m(W)} feet wide. The concrete "
                    f"will be {m(t)} inches thick. How many cubic yards of concrete are needed? "
                    f"(1 cubic yard {m('=')} 27 cubic feet.)")
        else:
            stem = (f"{p.name} wants to spread mulch {m(t)} inches deep over a garden bed that is {m(L)} feet long "
                    f"and {m(W)} feet wide. How many cubic yards of mulch does {p.he} need? "
                    f"(1 cubic yard {m('=')} 27 cubic feet.)")
        return Problem(
            stem=stem, answer=yd3, fmt=_u(num, "yd", 3),
            near=_int_near(yd3, (1, -1, 2, 3)),
            wrong=_whole([(L * W * t / Q(27), "uses the thickness in inches as if it were feet"),
                          (ft3 / 9, "divides by 9 instead of 27 (9 is for square yards)"),
                          (ft3 / 36, "divides by 36 (the inches in a yard) instead of 27"),
                          (ft3 / 3, "divides by 3 instead of 27"),
                          (ft3, "forgets to change cubic feet to cubic yards")]),
            steps=[f"Change the thickness to feet: {m(f'{t} \\text{{ in}} = {F(t, 12)} \\text{{ ft}} = {frac_raw(tf)} \\text{{ ft}}')}.",
                   f"Volume in cubic feet: {m(f'{L} \\times {W} \\times {frac_raw(tf)} = {int_raw(ft3)}')}.",
                   f"Change to cubic yards: {m(f'{int_raw(ft3)} \\div 27 = {int_raw(yd3)}')}."],
            check=Q(L) / 3 * W / 3 * R(t, 36),
        )
    if kind == "trench":
        L, W, D = rng.randint(6, 40), rng.choice([2, 3]), rng.choice([2, 3, 4])
        ft3 = L * W * D
        need(ft3 % 27 == 0 and 1 <= ft3 // 27 <= 20)
        yd3 = Q(ft3) / 27
        s_ = soldier(rng)
        return Problem(
            stem=(f"{s_}'s team digs a trench {m(L)} feet long, {m(W)} feet wide, and {m(D)} feet deep. "
                  f"How many cubic yards of dirt do they remove? (1 cubic yard {m('=')} 27 cubic feet.)"),
            answer=yd3, fmt=_u(num, "yd", 3), near=_int_near(yd3, (1, -1, 2, 3)),
            wrong=_whole([(Q(ft3) / 9, "divides by 9 instead of 27 (9 is for square yards)"),
                          (Q(ft3) / 36, "divides by 36 (the inches in a yard) instead of 27"),
                          (Q(ft3) / 3, "divides by 3 instead of 27"),
                          (Q(ft3), "forgets to change cubic feet to cubic yards")]),
            steps=[f"Volume in cubic feet: {m(f'{L} \\times {W} \\times {D} = {ft3}')}.",
                   f"A cubic yard is {m(r'3 \times 3 \times 3 = 27')} cubic feet, so divide: "
                   f"{m(f'{ft3} \\div 27 = {int_raw(yd3)}')} cubic yards."],
            tip=(f"Or change every length to yards first: "
                 f"{m(f'{F(L, 3)} \\times {F(W, 3)} \\times {F(D, 3)} = {frac_raw(R(L, 3))} \\times {frac_raw(R(W, 3))} \\times {frac_raw(R(D, 3))} = {int_raw(yd3)}')} cubic yards."),
            check=Q(L) / 3 * Q(W) / 3 * Q(D) / 3,
        )
    # sandbox: whole bags of sand (1/2, 1 or 2 cubic feet each); sometimes you must round up
    L, W = rng.randint(3, 10), rng.randint(3, 8)
    need(L >= W)
    t = rng.choice([4, 6, 8, 9, 12])
    bag = rng.choice([R(1, 2), R(1, 2), Q(1), Q(2), Q(2)])
    tf = R(t, 12)
    need(tf != bag)                      # depth and bag size must not cancel (answer = floor area)
    ft3 = L * W * tf
    exact = ft3 / bag
    bags = sp.ceiling(exact)
    rounded = not exact.is_integer
    need(8 <= bags <= 200)
    p = person(rng)
    bag_t = {R(1, 2): "half a cubic foot", Q(1): "1 cubic foot", Q(2): "2 cubic feet"}[bag]
    v_t = int_raw(ft3) if ft3.is_integer else dec_raw(ft3)
    wrong = []
    if rounded:
        wrong.append((sp.floor(exact), "rounds down; that many bags would leave the sandbox short of sand"))
    wrong += _whole([(Q(L * W * t) / bag, "uses the depth in inches as if it were feet"),
                     (Q(L * W) / bag, "leaves out the depth"),
                     (ft3 * bag, "multiplies by the bag size instead of dividing by it")])
    if bag != 1 and ft3.is_integer:
        wrong.append((ft3, "finds the number of cubic feet but forgets to divide by the bag size"))
    if bag == R(1, 2):
        last = [f"Each bag holds {m(F(1, 2))} cubic foot, so it takes 2 bags for every cubic foot: "
                f"{m(f'{v_t} \\times 2 = {dec_raw(exact)}')} bags."]
    elif bag == 1:
        last = [f"Each bag holds 1 cubic foot, so you need one bag for each cubic foot: {m(v_t)} bags."]
    else:
        last = [f"Each bag holds 2 cubic feet: {m(f'{v_t} \\div 2 = {dec_raw(exact)}')} bags."]
    if rounded:
        last.append(f"You can't buy part of a bag, and {m(int_raw(sp.floor(exact)))} bags would not be enough, "
                    f"so round up to {m(int_raw(bags))} bags.")
    return Problem(
        stem=(f"{p.name} is filling a sandbox that is {m(L)} feet long and {m(W)} feet wide with sand "
              f"{m(t)} inches deep. Sand is sold in bags that each hold {bag_t}. "
              f"How many bags does {p.he} need to buy?"),
        answer=bags, fmt=num, near=_int_near(bags, (2, -2, 3, -3)), must=1 if rounded else 0,
        wrong=wrong,
        steps=[f"Change the depth to feet: {m(f'{t} \\text{{ in}} = {F(t, 12)} \\text{{ ft}} = {frac_raw(tf)} \\text{{ ft}}')}.",
               f"Volume: {m(f'{L} \\times {W} \\times {frac_raw(tf)} = {v_t}')} cubic feet."] + last,
        check=next(k_ for k_ in range(1, 1000) if k_ * bag >= ft3),     # smallest number of bags that is enough
    )


@template("MK")
def missing_dim(rng, lvl):
    kind = rng.choice(["box", "tank", "cyl", "cyl"])
    if kind in ("box", "tank"):
        if kind == "box":
            ab = rng.choice(_ABS)
            l, w, h = rng.randint(3, 15), rng.randint(2, 12), rng.randint(2, 15)
            V = l * w * h
            stem = choose(rng,
                          f"A rectangular box has a volume of {num(V)} {_cuw(ab)}. Its base is {m(l)} {_w(ab)} long "
                          f"and {m(w)} {_w(ab)} wide. How tall is the box?",
                          f"The volume of a rectangular prism is {num(V)} {_cuw(ab)}. Its length is {m(l)} {_w(ab)} "
                          f"and its width is {m(w)} {_w(ab)}. What is its height?")
        else:
            ab = "in"
            l, w, h = rng.choice([20, 24, 30, 36]), rng.choice([10, 12, 15]), rng.randint(8, 18)
            V = l * w * h
            stem = (f"An aquarium is {m(l)} inches long and {m(w)} inches wide. It holds {num(V)} cubic inches "
                    f"of water. How deep is the water?")
        need(len({l, w, h}) == 3 and V <= 6000)
        return Problem(
            stem=stem, answer=Q(h), fmt=_u(num, ab), near=_int_near(h),
            wrong=_whole([(Q(V) / l, "divides by only one of the two given dimensions"),
                          (Q(V) / (l + w), "divides by the sum of the length and width instead of their product"),
                          (Q(l * w), "gives the area of the base")]),
            steps=[f"Use {m(r'V = l \times w \times h')}: {m(f'{int_raw(V)} = {l} \\times {w} \\times h')}.",
                   f"Area of the base: {m(f'{l} \\times {w} = {l * w}')}.",
                   f"Divide: {m(f'h = {int_raw(V)} \\div {l * w} = {h}')} {_w(ab, h)}."],
            verify=lambda v: v * l * w == V,
        )
    ab = rng.choice(_ABS)
    use_d = rng.random() < 0.6
    r, h = rng.randint(2, 8), rng.randint(2, 15)
    need(r != h)
    k = r * r * h
    V = k * PI
    given = (f"a diameter of {m(2 * r)} {_w(ab)}" if use_d else f"a radius of {m(r)} {_w(ab)}")
    wrong = [(R(k, r), "forgets to square the radius"),
             (R(k, 2 * r), r"divides by $2r$ instead of $r^2$")]
    if use_d:
        wrong.append((R(k, 4 * r * r), "uses the diameter in place of the radius"))
    wrong.append((R(k, r * r) * 2, None))
    first = [f"The radius is {m(f'{2 * r} \\div 2 = {r}')} {_w(ab)}."] if use_d else []
    return Problem(
        stem=f"A cylinder has {given} and a volume of {m(_pi_raw(V))} {_cuw(ab)}. What is its height?",
        answer=Q(h), fmt=_u(dec, ab), near=_int_near(h),
        wrong=[w_ for w_ in wrong if (Q(w_[0]) * 100).is_integer],
        steps=first + [f"Use {m(r'V = \pi r^2 h')}: {m(rf'{_pi_raw(V)} = \pi \times {r}^2 \times h = {r * r}\pi h')}.",
                       f"Divide both sides by {m(rf'{r * r}\pi')}: {m(f'h = {k} \\div {r * r} = {h}')} {_w(ab, h)}."],
        verify=lambda v: PI * r**2 * v == V,
    )


@template("MK")
def scale_solid(rng, lvl):
    kind = rng.choice(["cube_V", "cube_SA", "box_num", "box_num", "box_num", "cyl_r", "cyl_h",
                       "cyl_num", "cyl_num", "half", "half"])
    words = {2: "doubled", 3: "tripled"}
    if kind in ("cube_V", "cube_SA"):
        k = rng.choice([2, 3])
        solid = rng.choice(["a cube", "a rectangular box"])
        what = "volume" if kind == "cube_V" else "surface area"
        ans = k**3 if kind == "cube_V" else k**2
        wrong = [(Q(k), f"assumes the {what} grows by the same factor as the edges"),
                 (Q(k**2 if kind == "cube_V" else k**3),
                  "squares the factor; that is how surface area grows" if kind == "cube_V"
                  else "cubes the factor; that is how volume grows"),
                 (Q(3 * k), "multiplies the factor by 3 instead of cubing it" if kind == "cube_V" else None),
                 (Q(2 * k), None)]
        if kind == "cube_V":
            steps = [f"Volume multiplies three lengths, and each one is multiplied by {m(k)}.",
                     f"So the volume is multiplied by {m(f'{k} \\times {k} \\times {k} = {k**3}')}."]
        else:
            steps = [f"Each face's area multiplies two lengths, and each one is multiplied by {m(k)}.",
                     f"So every face, and the total surface area, is multiplied by {m(f'{k} \\times {k} = {k * k}')}."]
        return Problem(
            stem=f"If every edge of {solid} is {words[k]}, its {what} is multiplied by what number?",
            answer=Q(ans), fmt=num, must=2, wrong=wrong, steps=steps,
            check=sp.expand((k * x)**3 / x**3) if kind == "cube_V" else sp.expand(6 * (k * x)**2 / (6 * x**2)),
        )
    if kind == "box_num":
        k = rng.choice([2, 2, 3])
        ab = rng.choice(["in", "ft", "cm"])
        V0 = rng.choice([24, 30, 36, 40, 45, 48, 50, 60, 72, 80, 96, 100, 120, 150, 200] if ab != "ft"
                        else [2, 3, 4, 5, 6, 8, 10, 12, 15])
        p = person(rng)
        ans = V0 * k**3
        return Problem(
            stem=(f"{p.name} has a box with a volume of {num(V0)} {_cuw(ab)}. {p.He} builds a second box whose length, "
                  f"width, and height are each {m(k)} times as long as those of the first box. What is the volume of "
                  f"the second box?"),
            answer=Q(ans), fmt=_u(num, ab, 3), must=1,
            near=lambda rng: [Q(ans + V0), Q(ans - V0), Q(V0 * (k**3 + 2)), Q(V0 * 4 * k)],
            wrong=[(Q(V0 * k), f"multiplies the volume by {m(k)} instead of {m(f'{k}^3')}"),
                   (Q(V0 * k * k), f"multiplies the volume by {m(f'{k}^2')} instead of {m(f'{k}^3')}"),
                   (Q(V0 * 3 * k), f"multiplies the volume by {m(f'3 \\times {k}')} instead of {m(f'{k}^3')}")],
            steps=[f"Each of the three dimensions is multiplied by {m(k)}, so the volume is multiplied by "
                   f"{m(f'{k} \\times {k} \\times {k} = {k**3}')}.",
                   f"New volume: {m(f'{int_raw(V0)} \\times {k**3} = {int_raw(ans)}')} {_cuw(ab)}."],
            check=sp.expand((k * x) * (k * y) * (k * z)).subs({x: 1, y: 1, z: V0}),
        )
    if kind == "cyl_r":
        k = rng.choice([2, 3])
        return Problem(
            stem=(f"The radius of a cylinder is {words[k]}, and its height stays the same. The volume of the new "
                  f"cylinder is how many times the volume of the original?"),
            answer=Q(k * k), fmt=num, must=1,
            wrong=[(Q(k), "assumes the volume grows by the same factor as the radius"),
                   (Q(k**3), "cubes the factor, but only the radius changed, not the height"),
                   (Q(2 * k), "doubles the factor instead of squaring it")],
            steps=[f"In {m(r'V = \pi r^2 h')}, the radius is squared.",
                   f"Replace {m('r')} with {m(f'{k}r')}: {m(rf'\pi ({k}r)^2 h = {k * k}\pi r^2 h')}, so the volume is "
                   f"multiplied by {m(k * k)}."],
            check=sp.expand(PI * (k * x)**2 * y) / (PI * x**2 * y),
        )
    if kind == "cyl_h":
        k = rng.choice([2, 3])
        return Problem(
            stem=(f"The height of a cylinder is {words[k]}, and its radius stays the same. The volume of the new "
                  f"cylinder is how many times the volume of the original?"),
            answer=Q(k), fmt=num, must=1,
            wrong=[(Q(k * k), "squares the factor; only the radius is squared in the formula"),
                   (Q(k**3), "cubes the factor"),
                   (Q(2 * k), None)],
            steps=[f"In {m(r'V = \pi r^2 h')}, the height is not squared.",
                   f"Replace {m('h')} with {m(f'{k}h')}: {m(rf'\pi r^2 ({k}h) = {k}\pi r^2 h')}, so the volume is "
                   f"multiplied by {m(k)}."],
            check=sp.expand(PI * x**2 * (k * y)) / (PI * x**2 * y),
        )
    if kind == "cyl_num":
        k = rng.choice([2, 3])
        c0 = rng.choice([4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 30, 36, 40])
        ab = rng.choice(["in", "cm", "ft"])
        what = rng.choice(["can", "jar", "tank", "cylinder"])
        V0 = c0 * PI
        which = rng.choice(["r", "h"])
        f_ = k * k if which == "r" else k
        ans = f_ * V0
        part, other = ("radius", "height") if which == "r" else ("height", "radius")
        wrong = [(k * V0 if which == "r" else k * k * V0,
                  "multiplies the volume by the same factor as the radius" if which == "r"
                  else "squares the factor, but the height is not squared in the formula"),
                 (k**3 * V0, f"multiplies by {m(f'{k}^3')}, but only one measurement changed"),
                 (2 * k * V0 if 2 * k != f_ else (f_ + 1) * V0, None)]
        return Problem(
            stem=(f"{'A cylinder' if what == 'cylinder' else f'A {what} shaped like a cylinder'} holds "
                  f"{m(_pi_raw(V0))} {_cuw(ab)}. A second {what} has the same "
                  f"{other}, but its {part} is {m(k)} times as large. How much does the second {what} hold?"),
            answer=ans, fmt=_pi_u(ab, 3), near=_pi_near(ans), wrong=wrong, must=1,
            steps=[f"In {m(r'V = \pi r^2 h')} the radius is squared but the height is not.",
                   (f"Multiplying the radius by {m(k)} multiplies the volume by {m(f'{k}^2 = {k * k}')}." if which == "r"
                    else f"Multiplying the height by {m(k)} multiplies the volume by {m(k)}."),
                   f"New volume: {m(rf'{f_} \times {_pi_raw(V0)} = {_pi_raw(ans)}')} {_cuw(ab)}."],
            check=(PI * (k * x)**2 * y / (PI * x**2 * y) if which == "r" else PI * x**2 * (k * y) / (PI * x**2 * y)) * V0,
        )
    # half: every edge cut in half
    V0 = rng.choice([64, 80, 96, 120, 160, 200, 240, 320, 400, 480, 560, 640, 720, 800])
    ab = rng.choice(["in", "cm"])
    ans = R(V0, 8)
    need(ans.is_integer)
    who = person(rng).name
    return Problem(
        stem=(f"{who} has a box with a volume of {num(V0)} {_cuw(ab)}. A smaller box has every dimension half as "
              f"long as the first box. What is the volume of the smaller box?"),
        answer=ans, fmt=_u(num, ab, 3),
        wrong=_whole([(R(V0, 2), "halves the volume instead of dividing by 8"),
                      (R(V0, 4), "divides by 4 instead of 8"),
                      (R(V0, 6), "divides by 6 instead of 8")]),
        steps=[f"Each of the three dimensions is multiplied by {m(F(1, 2))}, so the volume is multiplied by "
               f"{m(rf'\frac{{1}}{{2}} \times \frac{{1}}{{2}} \times \frac{{1}}{{2}} = \frac{{1}}{{8}}')}.",
               f"New volume: {m(f'{int_raw(V0)} \\div 8 = {int_raw(ans)}')} {_cuw(ab)}."],
        check=Q(V0) * R(1, 2)**3,
    )


@template("MK")
def cone_sphere(rng, lvl):
    kind = rng.choice(["cone", "cone", "sphere", "hemi", "relation"])
    ab = rng.choice(["in", "cm", "ft", "m"])
    if kind == "cone":
        use_d = rng.random() < 0.4
        r, h = rng.randint(2, 9), rng.randint(3, 15)
        need((r * r * h) % 3 == 0 and r != h)
        V = R(r * r * h, 3) * PI
        fig, ok = _fig_cone(r, h, ab, use_d)
        given = f"diameter {m(2 * r)} {_w(ab)}" if use_d else f"radius {m(r)} {_w(ab)}"
        wrong = [(r * r * h * PI, r"forgets the $\frac{1}{3}$ (that is the volume of a cylinder)"),
                 (R(r * h, 3) * PI, "forgets to square the radius"),
                 (R(2 * r * h, 3) * PI, r"uses $2r$ instead of $r^2$")]
        if use_d:
            wrong.insert(0, (R(4 * r * r * h, 3) * PI, "uses the diameter in place of the radius"))
        return Problem(
            stem=(f"The volume of a cone is {m(r'V = \frac{1}{3}\pi r^2 h')}. What is the volume of a cone with "
                  f"{given} and height {m(h)} {_w(ab, h)}?" + ("" if ok else " (Figure not drawn to scale.)")),
            figure=fig,
            answer=V, fmt=_pi_u(ab, 3), near=_pi_near(V), wrong=wrong,
            steps=([f"The radius is half the diameter: {m(f'{2 * r} \\div 2 = {r}')}."] if use_d else []) +
                  [f"Square the radius: {m(f'{r}^2 = {r * r}')}.",
                   f"Substitute: {m(rf'V = \frac{{1}}{{3}} \times \pi \times {r * r} \times {h} = \frac{{1}}{{3}} \times {int_raw(r * r * h)}\pi = {_pi_raw(V)}')} {_cuw(ab)}."],
            check=PI * Q(2 * r)**2 * h / 12,
        )
    if kind in ("sphere", "hemi"):
        use_d = rng.random() < 0.4
        r = rng.choice([3, 6, 9])
        full = R(4, 3) * r**3 * PI
        V = full if kind == "sphere" else full / 2
        given = f"diameter {m(2 * r)} {_w(ab)}" if use_d else f"radius {m(r)} {_w(ab)}"
        if kind == "sphere":
            what = rng.choice(["a sphere", "a ball", "a round water tank shaped like a sphere"])
            if what == "a ball":
                ab = rng.choice(["in", "cm"])
            elif what != "a sphere":
                ab = rng.choice(["ft", "m"])
            given = f"diameter {m(2 * r)} {_w(ab)}" if use_d else f"radius {m(r)} {_w(ab)}"
            stem = (f"The volume of a sphere is {m(r'V = \frac{4}{3}\pi r^3')}. What is the volume of {what} "
                    f"with {given}?")
            fig = _fig_sphere(r, ab, use_d) if what == "a sphere" else None
        else:
            ab = rng.choice(["in", "cm"])
            need(r in ((3, 6) if ab == "in" else (6, 9)))     # a real bowl: 6-12 in or 12-18 cm across
            given = f"diameter {m(2 * r)} {_w(ab)}" if use_d else f"radius {m(r)} {_w(ab)}"
            stem = (f"The volume of a sphere is {m(r'V = \frac{4}{3}\pi r^3')}. A bowl is shaped like half of a "
                    f"sphere (a hemisphere) with {given}. How much does the bowl hold when full?")
            fig = None
        half = 1 if kind == "sphere" else R(1, 2)
        wrong = [(4 * r * r * PI * half, r"uses $4\pi r^2$, which is the surface area"),
                 (R(4, 3) * r * r * PI * half, "squares the radius instead of cubing it"),
                 (4 * r**3 * PI * half, r"forgets the $\frac{1}{3}$")]
        if use_d:
            wrong.insert(0, (R(4, 3) * (2 * r)**3 * PI * half, "uses the diameter in place of the radius"))
        if kind == "hemi":
            wrong.insert(0, (full, "finds the volume of the whole sphere, not half"))
        return Problem(
            stem=stem, figure=fig,
            answer=V, fmt=_pi_u(ab, 3), near=_pi_near(V), wrong=wrong,
            steps=([f"The radius is half the diameter: {m(f'{2 * r} \\div 2 = {r}')}."] if use_d else []) +
                  [f"Cube the radius: {m(f'{r}^3 = {r} \\times {r} \\times {r} = {r**3}')}.",
                   f"Substitute: {m(rf'V = \frac{{4}}{{3}} \times \pi \times {r**3} = {_pi_raw(full)}')}"
                   + (f". Half of the sphere: {m(rf'{_pi_raw(full)} \div 2 = {_pi_raw(V)}')}" if kind == "hemi" else "")
                   + f" {_cuw(ab)}."],
            tip=f"Divide before you multiply: {m(f'{r**3} \\div 3 = {r**3 // 3}')}, then {m(f'4 \\times {r**3 // 3} = {4 * r**3 // 3}')}.",
            check=4 * PI * Q(2 * r)**3 / 24 * half,
        )
    # relation between a cone and a cylinder
    k = rng.choice(range(3, 61, 3))
    Vc = k * PI
    up = rng.random() < 0.5
    if up:
        ans = R(k, 3) * PI
        stem = (f"A cylinder and a cone have the same radius and the same height. The cylinder holds "
                f"{m(_pi_raw(Vc))} {_cuw(ab)}. How much does the cone hold? (Cone: {m(r'V = \frac{1}{3}\pi r^2 h')}.)")
        wrong = [(3 * Vc, "multiplies by 3 instead of dividing by 3"),
                 (Vc / 2, "takes half instead of one third"),
                 (Vc, "assumes the cone holds the same amount")]
        steps = [f"A cone holds {m(F(1, 3))} as much as a cylinder with the same base and height "
                 f"({m(r'\frac{1}{3}\pi r^2 h')} compared with {m(r'\pi r^2 h')}).",
                 f"{m(rf'\frac{{1}}{{3}} \times {_pi_raw(Vc)} = {_pi_raw(ans)}')} {_cuw(ab)}."]
    else:
        ans = 3 * Vc
        stem = (f"A cone and a cylinder have the same radius and the same height. The cone holds "
                f"{m(_pi_raw(Vc))} {_cuw(ab)}. How much does the cylinder hold? (Cone: {m(r'V = \frac{1}{3}\pi r^2 h')}.)")
        wrong = [(Vc / 3, "divides by 3 instead of multiplying by 3"),
                 (2 * Vc, "doubles instead of tripling"),
                 (Vc, "assumes the cylinder holds the same amount")]
        steps = [f"A cone holds {m(F(1, 3))} as much as a cylinder with the same base and height, so the "
                 f"cylinder holds 3 times as much as the cone.",
                 f"{m(rf'3 \times {_pi_raw(Vc)} = {_pi_raw(ans)}')} {_cuw(ab)}."]
    return Problem(
        stem=stem, answer=ans, fmt=_pi_u(ab, 3), near=_pi_near(ans), wrong=[w_ for w_ in wrong if (_split(w_[0])[1]).is_integer],
        steps=steps,
        verify=(lambda v: sp.expand(3 * v - Vc) == 0) if up else (lambda v: sp.expand(v - 3 * Vc) == 0),
    )


PLAN = [
    # (template, level, count) -- easy -> hard; 25 problems
    (box_volume, 1, 3),
    (cube, 1, 3),
    (cylinder, 1, 2),
    (box_surface, 2, 2),
    (cube, 2, 1),
    (missing_dim, 2, 2),
    (fill_tank, 2, 2),
    (how_many_fit, 2, 2),
    (cylinder, 2, 1),
    (concrete, 3, 2),
    (scale_solid, 3, 2),
    (cone_sphere, 3, 2),
    (fill_tank, 3, 1),
]
