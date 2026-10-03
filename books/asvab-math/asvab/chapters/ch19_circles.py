"""Chapter 19 - Circles."""
import sympy as sp

from ..core import (R, Q, x, Problem, need, num, dec, frac, m, F, dec_raw, int_raw,
                    frac_raw, person, soldier, choose, template)

NUM = 19
TITLE = "Circles"
PART = 3

INTRO = r"""
Circle questions use just two formulas, and the ASVAB does \emph{not} give
them to you, so learn them by heart. Almost every mistake comes from mixing
up the radius and the diameter, or the circumference and the area.

\begin{concept}{Parts of a circle}
\begin{minipage}[c]{0.6\linewidth}
\begin{itemize}
\item The \textbf{radius} $r$ runs from the center to the circle.
\item The \textbf{diameter} $d$ goes all the way across through the
  center: $d = 2r$ and $r = d \div 2$.
\item The \textbf{circumference} $C$ is the distance around the circle
  (its perimeter).
\item The \textbf{area} $A$ is the space inside, in square units.
\end{itemize}
\end{minipage}\hfill
\begin{minipage}[c]{0.36\linewidth}\centering
\begin{tikzpicture}[scale=0.85]
\draw[thick] (0,0) circle (1.2);
\fill (0,0) circle (1.4pt);
\draw (0,0) -- (60:1.2) node[pos=0.55, left] {\small $r$};
\draw (-1.2,0) -- (1.2,0);
\node[below] at (0.6,0) {\small $d$};
\node[below left] at (0,0) {\scriptsize center};
\draw[-{Stealth[length=4pt]}] (-30:1.42) arc (-30:-80:1.42);
\node[right] at (-50:1.45) {\small $C$};
\end{tikzpicture}
\end{minipage}
\end{concept}

\begin{concept}{The two formulas}
\[ C = 2\pi r = \pi d \qquad\qquad A = \pi r^2 \]
$\pi \approx 3.14 \approx \frac{22}{7}$. Most answers are left ``in terms of
$\pi$'': $36\pi$ simply means $36 \times \pi$. Use $3.14$ or $\frac{22}{7}$
only when the question tells you to. In $\pi r^2$ only the radius is squared:
if $r = 6$, then $A = \pi \times 36 = 36\pi$.
\end{concept}

\begin{concept}{Parts of a circle's area and perimeter}
\begin{itemize}
\item A \textbf{semicircle} is half a circle; a \textbf{quarter circle} is
  one fourth. Their perimeters also include the straight edges.
\item A \textbf{sector} (a pie slice) with central angle $a^\circ$ is the
  fraction $\frac{a}{360}$ of the circle:
  \[ \text{arc length} = \frac{a}{360}\times 2\pi r \qquad
     \text{sector area} = \frac{a}{360}\times \pi r^2 \]
\item \textbf{Shaded regions:} area of the whole shape minus the area of
  the part that is cut out. A ring between two circles is $\pi R^2 - \pi r^2$.
\end{itemize}
\end{concept}

\begin{example}{Worked example}
A circular garden has a diameter of 10 feet. Using 3.14 for $\pi$, find its
area and the length of fence needed to go around it.

\textbf{Solution.} The radius is $10 \div 2 = 5$ feet. Area:
$A = \pi r^2 \approx 3.14 \times 5^2 = 3.14 \times 25 = 78.5$ square feet.
Fence: $C = \pi d \approx 3.14 \times 10 = 31.4$ feet.
\end{example}

\begin{tip}
To multiply by $3.14$, multiply by $3$ and by $0.14$ and add:
$3.14 \times 25 = 75 + 3.5 = 78.5$. Scaling: if the radius is multiplied by
$k$, the circumference is multiplied by $k$ but the area by $k^2$, so
doubling the radius makes the area $4$ times as large.
\end{tip}

\begin{trap}
\begin{itemize}
\item Putting the diameter into $\pi r^2$. Halve the diameter \emph{first}.
\item Mixing up the formulas: $2\pi r$ is the distance around, $\pi r^2$ is
  the space inside.
\item Halving after squaring: with $d = 10$, the area is $\pi \times 5^2 =
  25\pi$, not $\pi \times 100 \div 2 = 50\pi$.
\item Leaving out the straight edges in the perimeter of a semicircle or
  quarter circle.
\end{itemize}
\end{trap}
"""

PI = sp.pi

# unit abbreviation -> (singular, plural)
_UNITS = {"in": ("inch", "inches"), "ft": ("foot", "feet"),
          "cm": ("centimeter", "centimeters"), "m": ("meter", "meters"),
          "yd": ("yard", "yards"), "mi": ("mile", "miles"),
          "mm": ("millimeter", "millimeters")}


def _w(ab):
    """Plural unit word: 'in' -> 'inches'."""
    return _UNITS[ab][1]


def _sqw(ab):
    return "square " + _UNITS[ab][1]


# --------------------------------------------------------------------------
# values in terms of pi:  c + k*pi  with rational c, k
# --------------------------------------------------------------------------

def _split(v):
    v = sp.expand(Q(v))
    k = v.coeff(PI)
    c = sp.expand(v - k * PI)
    need(k.is_rational and c.is_rational, "not of the form c + k*pi")
    return sp.Rational(c), sp.Rational(k)


def _kpi(k):
    """Raw LaTeX for k*pi with k > 0 rational."""
    k = sp.Rational(k)
    if k == 1:
        return r"\pi"
    if k.q == 1:
        return int_raw(k) + r"\pi"
    top = "" if k.p == 1 else int_raw(k.p)
    return rf"\frac{{{top}\pi}}{{{k.q}}}"


def _pi_raw(v):
    """'36\\pi', '6\\pi + 12', '64 - 16\\pi' (positive term first)."""
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
    """Formatter: value in terms of pi with a unit, e.g. $36\\pi\\text{ in}^2$."""
    sup = "" if power == 1 else f"^{power}"

    def f(v):
        c, k = _split(v)
        raw = _pi_raw(v)
        if c != 0 and k != 0:
            raw = f"({raw})"
        return m(rf"{raw}\text{{ {ab}}}{sup}")
    return f


def _u(fmt, ab, power=1):
    """Plain number with a unit: _u(dec, 'ft') -> $62.8\\text{ ft}$."""
    sup = "" if power == 1 else f"^{power}"

    def f(v):
        return m(rf"{fmt(v)[1:-1]}\text{{ {ab}}}{sup}")
    return f


def _pi_near(ans, alts=None):
    """Filler choices for an answer c + k*pi: the given alternatives, or nearby
    multiples of pi, two on each side (kept short: every extra candidate costs
    sympy comparisons in finalize)."""
    c, k = _split(ans)

    def f(rng):
        if alts is not None:
            out = list(alts)
        else:
            a = abs(k)
            st = 1 if a <= 12 else 2 if a <= 30 else 5 if a <= 80 else 10 if a <= 200 else 50
            if k.q != 1:
                st = R(1, k.q) if a <= 6 else R(1, 1)
            out = [c + (k + j * st) * PI for j in (1, -1, 2, -2)]
        out = [v for v in out if Q(v) > 0 and _split(v)[1] != 0 and sp.expand(v - ans) != 0]
        rng.shuffle(out)
        return out
    return f


def _int_near(v, steps=(1, -1, 2, -2)):
    """Filler choices close to a whole-number answer."""
    def f(rng):
        out = [Q(v) + s_ for s_ in steps if Q(v) + s_ > 0]
        rng.shuffle(out)
        return out
    return f


def _cents(vals):
    """Keep only distractors that need at most 2 decimal places."""
    return [w for w in vals if (Q(w[0]) * 100).is_integer]


# --------------------------------------------------------------------------
# figures (TikZ, grayscale, about 3 cm across)
# --------------------------------------------------------------------------

def _fig_radius(label, rad=1.25):
    return (rf"\draw[thick] (0,0) circle ({rad});" "\n"
            rf"\fill (0,0) circle (1.3pt);" "\n"
            rf"\draw (0,0) -- ({rad},0) node[midway, above] {{\small {label}}};")


def _fig_diameter(label, rad=1.25):
    return (rf"\draw[thick] (0,0) circle ({rad});" "\n"
            rf"\fill (0,0) circle (1.3pt);" "\n"
            rf"\draw ({-rad},0) -- ({rad},0);" "\n"
            rf"\node[above] at (0,0) {{\small {label}}};")


def _lab(v, ab=None):
    """Figure label: '$12$ in'."""
    s = f"${int_raw(v) if Q(v).is_integer else dec_raw(v)}$"
    return s + (f" {ab}" if ab else "")


# --------------------------------------------------------------------------
# templates
# --------------------------------------------------------------------------

# (object, unit, smallest radius, largest radius) for everyday circles
_OBJ = [
    ("a round tabletop", "in", 15, 30),
    ("a circular mirror", "in", 6, 15),
    ("a circular rug", "ft", 3, 6),
    ("a circular flower bed", "ft", 3, 10),
    ("a round trampoline", "ft", 4, 8),
    ("the top of an above-ground pool", "ft", 6, 12),
    ("a circular helicopter landing pad", "ft", 20, 40),
    ("a round paper target at the rifle range", "in", 5, 12),
    ("a manhole cover", "in", 10, 15),
]
_ABS = ["in", "ft", "cm", "m", "yd"]


@template("MK")
def circle_area(rng, lvl):
    style = rng.choice(["plain", "plain", "fig", "obj"])
    fig = None
    if style == "obj":
        obj, ab, lo, hi = rng.choice(_OBJ)
        r = rng.randint(lo, hi)
    else:
        ab = rng.choice(_ABS)
        r = rng.randint(3, 20)
    d = 2 * r
    ans = r**2 * PI
    Obj = obj[0].upper() + obj[1:] if style == "obj" else ""
    if lvl == 1:
        if style == "fig":
            stem = f"In the figure, the radius of the circle is {m(r)} {_w(ab)}. What is the area of the circle?"
            fig = _fig_radius(_lab(r, ab))
        elif style == "obj":
            stem = f"{Obj} has a radius of {m(r)} {_w(ab)}. What is its area?"
        else:
            stem = choose(rng,
                          f"A circle has a radius of {m(r)} {_w(ab)}. What is the area of the circle?",
                          f"What is the area of a circle with a radius of {m(r)} {_w(ab)}?",
                          f"Find the area of a circle whose radius is {m(r)} {_w(ab)}.")
        return Problem(
            stem=stem, figure=fig,
            answer=ans, fmt=_pi_u(ab, 2),
            near=_pi_near(ans, [(r + 1)**2 * PI, (r - 1)**2 * PI, 2 * r * r * PI]),
            wrong=[
                (2 * r * PI, r"uses the circumference formula $2\pi r$ instead of $\pi r^2$"),
                (r * PI, "forgets to square the radius"),
                (4 * r**2 * PI, "uses the diameter in place of the radius"),
            ],
            steps=[
                f"The area of a circle is {m(r'A = \pi r^2')}. Here the radius is {m(r)} {_w(ab)}.",
                f"Square the radius: {m(f'{r}^2 = {r * r}')}.",
                f"So {m(rf'A = \pi \times {r * r} = {_pi_raw(ans)}')} {_sqw(ab)}.",
            ],
            check=PI * Q(2 * r)**2 / 4,
        )
    # level 2: the diameter is given
    if style == "fig":
        stem = f"In the figure, the diameter of the circle is {m(d)} {_w(ab)}. What is the area of the circle?"
        fig = _fig_diameter(_lab(d, ab))
    elif style == "obj":
        stem = f"{Obj} has a diameter of {m(d)} {_w(ab)}. What is its area?"
    else:
        stem = choose(rng,
                      f"A circle has a diameter of {m(d)} {_w(ab)}. What is its area?",
                      f"What is the area of a circle with a diameter of {m(d)} {_w(ab)}?")
    return Problem(
        stem=stem, figure=fig,
        answer=ans, fmt=_pi_u(ab, 2),
        near=_pi_near(ans, [(r + 1)**2 * PI, (r - 1)**2 * PI, 2 * r * r * PI]),
        wrong=[
            (d**2 * PI, "uses the diameter in place of the radius"),
            (d * PI, "finds the circumference, not the area"),
            (R(d * d, 2) * PI, "squares the diameter and then halves it; halve first, then square"),
            (r * PI, "forgets to square the radius"),
        ],
        steps=[
            f"The formula {m(r'A = \pi r^2')} needs the radius, which is half the diameter: "
            f"{m(f'r = {d} \\div 2 = {r}')} {_w(ab)}.",
            f"Square the radius: {m(f'{r}^2 = {r * r}')}.",
            f"So {m(rf'A = \pi \times {r * r} = {_pi_raw(ans)}')} {_sqw(ab)}.",
        ],
        check=PI * Q(d)**2 / 4,
    )


@template("MK")
def circumference(rng, lvl):
    ab = rng.choice(_ABS)
    given = rng.choice(["r", "d"])
    if given == "r":
        r = rng.randint(3, 20)
        d = 2 * r
        ans = d * PI
        style = rng.choice(["fig", "text", "clock"])
        fig = None
        if style == "fig":
            stem = f"The radius of the circle shown is {m(r)} {_w(ab)}. What is the circumference of the circle?"
            fig = _fig_radius(_lab(r, ab))
        elif style == "clock" and r <= 8:
            ab = "in"
            stem = f"A round wall clock has a radius of {m(r)} inches. What is the distance around the edge of the clock?"
        else:
            stem = choose(rng,
                          f"What is the circumference of a circle with a radius of {m(r)} {_w(ab)}?",
                          f"A circle has a radius of {m(r)} {_w(ab)}. What is its circumference?")
        return Problem(
            stem=stem, figure=fig,
            answer=ans, fmt=_pi_u(ab), near=_pi_near(ans, [2 * (r + 1) * PI, 2 * (r - 1) * PI, 2 * (r - 2) * PI]),
            wrong=[
                (r * PI, r"uses the radius in $C = \pi d$; the diameter is twice the radius"),
                (r**2 * PI, "finds the area, not the circumference"),
                (4 * r * PI, r"doubles the radius and then uses that diameter in $2\pi r$"),
            ],
            steps=[
                f"The circumference is the distance around: {m(r'C = 2\pi r')}.",
                f"Substitute {m(f'r = {r}')}: {m(rf'C = 2 \times \pi \times {r} = {_pi_raw(ans)}')} {_w(ab)}.",
            ],
            check=PI * 2 * Q(r),
        )
    d = rng.choice(range(4, 41, 2))
    r = R(d, 2)
    ans = d * PI
    style = rng.choice(["fig", "text", "wheel"])
    fig = None
    wheel_step = []
    if style == "fig":
        stem = f"The diameter of the circle shown is {m(d)} {_w(ab)}. What is the circumference of the circle?"
        fig = _fig_diameter(_lab(d, ab))
    elif style == "wheel" and 16 <= d <= 29:
        ab = "in"
        stem = (f"A bicycle wheel has a diameter of {m(d)} inches. How far does the wheel roll "
                f"in one complete turn?")
        wheel_step = ["In one complete turn, a wheel rolls forward a distance equal to its circumference."]
    else:
        stem = choose(rng,
                      f"What is the circumference of a circle with a diameter of {m(d)} {_w(ab)}?",
                      f"A circle has a diameter of {m(d)} {_w(ab)}. What is its circumference?")
    return Problem(
        stem=stem, figure=fig,
        answer=ans, fmt=_pi_u(ab), near=_pi_near(ans, [(d + 2) * PI, (d - 2) * PI, (d - 4) * PI]),
        wrong=[
            (2 * d * PI, r"uses the diameter in $2\pi r$, which counts it twice"),
            (r**2 * PI, "finds the area, not the circumference"),
            (r * PI, r"uses the radius in $C = \pi d$"),
            (d**2 * PI, "squares the diameter"),
        ],
        steps=wheel_step + [
            f"When you know the diameter, use {m(r'C = \pi d')}.",
            f"Substitute {m(f'd = {d}')}: {m(rf'C = \pi \times {d} = {_pi_raw(ans)}')} {_w(ab)}.",
        ],
        check=2 * PI * r,
    )


# word problems with 3.14 or 22/7 -------------------------------------------
# (kind, given, pi, ab, values, text);  {g} -> 'diameter'/'radius', {v} -> value
_APPROX = [
    ("C", "d", "3.14", "ft", [6, 8, 10, 12, 15, 16, 20, 25, 30],
     "{P} is putting a fence around a circular garden that has a diameter of {v} feet. "
     "How many feet of fencing does {he} need?"),
    ("C", "r", "3.14", "ft", [5, 6, 8, 10, 12, 15, 20],
     "{P} is putting a fence around a circular garden that has a radius of {v} feet. "
     "How many feet of fencing does {he} need?"),
    ("C", "d", "3.14", "ft", [10, 12, 15, 20, 25],
     "{P} wants to hang a string of lights around the edge of a round patio with a diameter of "
     "{v} feet. How many feet of lights does {he} need?"),
    ("C", "d", "3.14", "ft", [30, 40, 50, 60, 80, 100],
     "A circular helicopter landing pad has a diameter of {v} feet. The ground crew will outline "
     "its edge with reflective tape. How many feet of tape are needed?"),
    ("C", "r", "3.14", "ft", [15, 20, 25, 30, 40, 50],
     "A circular helicopter landing pad has a radius of {v} feet. {S}'s crew will outline "
     "its edge with reflective tape. How many feet of tape are needed?"),
    ("C", "r", "3.14", "m", [20, 25, 30, 40, 50, 100],
     "{S}'s squad is stringing one strand of wire around a circular perimeter with a radius of "
     "{v} meters. How many meters of wire are needed to go around once?"),
    ("C", "d", "22/7", "in", [28, 35, 42, 49, 56, 63],
     "{P} is gluing trim around the edge of a round tabletop with a diameter of {v} inches. "
     "How many inches of trim does {he} need?"),
    ("C", "r", "22/7", "in", [14, 21, 28],
     "{P} is gluing trim around the edge of a round tabletop with a radius of {v} inches. "
     "How many inches of trim does {he} need?"),
    ("C", "d", "22/7", "m", [70, 140, 210],
     "A jogging path is a circle with a diameter of {v} meters. How many meters does {P} run "
     "in one lap?"),
    ("C", "r", "22/7", "m", [35, 70, 105],
     "A jogging path is a circle with a radius of {v} meters. How many meters does {P} run "
     "in one lap?"),
    ("C", "d", "22/7", "yd", [70, 105, 140],
     "{S} marks the edge of a circular landing zone with a diameter of {v} yards using a rope. "
     "How many yards of rope are needed to go all the way around?"),
    ("A", "r", "3.14", "ft", [2, 3, 4, 5, 6],
     "{P} bought a circular rug with a radius of {v} feet. What is the area of the rug?"),
    ("A", "d", "3.14", "ft", [4, 6, 8, 10, 12],
     "{P} bought a circular rug with a diameter of {v} feet. What is the area of the rug?"),
    ("A", "r", "3.14", "ft", [5, 6, 8, 10, 12, 15, 20],
     "{P}'s lawn sprinkler waters a circle with a radius of {v} feet. How many square feet of lawn "
     "does it water?"),
    ("A", "d", "3.14", "ft", [10, 12, 16, 20, 30, 40],
     "{P}'s lawn sprinkler waters a circle with a diameter of {v} feet. How many square feet of lawn "
     "does it water?"),
    ("A", "r", "3.14", "mi", [10, 20, 30, 40, 50, 60],
     "A radar station can detect aircraft up to {v} miles away in every direction. How many "
     "square miles does it cover?"),
    ("A", "d", "3.14", "mi", [20, 40, 60, 80, 100],
     "A radar station covers a circular area with a diameter of {v} miles. How many square "
     "miles does it cover?"),
    ("A", "r", "3.14", "ft", [10, 15, 20, 30],
     "A goat is tied to a stake in an open field with a rope {v} feet long. How many square feet "
     "of grass can the goat reach?"),
    ("A", "r", "22/7", "ft", [7, 14, 21],
     "A goat is tied to a stake in an open field with a rope {v} feet long. How many square feet "
     "of grass can the goat reach?"),
    ("A", "r", "22/7", "ft", [7, 14],
     "A round field tent has a floor with a radius of {v} feet. What is the floor area of the tent?"),
    ("A", "d", "22/7", "ft", [14, 28],
     "A round field tent has a floor with a diameter of {v} feet. What is the floor area of the tent?"),
    ("A", "d", "22/7", "in", [14],
     "{P} ordered a pizza with a diameter of {v} inches. What is the area of the top of the pizza?"),
    ("A", "d", "3.14", "ft", [10, 12, 16, 20, 24],
     "{P} has a circular swimming pool with a diameter of {v} feet. How many square feet of "
     "cover are needed to cover the top of the pool?"),
]


def _times_pi(P, v):
    """Raw LaTeX of 'pi-approx x v = result' with a hand-friendly middle step."""
    res = P * v
    if P == R(22, 7):
        q = Q(v) / 7
        if q.is_integer:
            return rf"\frac{{22}}{{7}} \times {int_raw(v)} = 22 \times {int_raw(q)} = {dec_raw(res)}"
        return rf"\frac{{22}}{{7}} \times {dec_raw(v)} = {dec_raw(res)}"
    return rf"3.14 \times {dec_raw(v)} = {dec_raw(res)}"


@template("AR")
def pi_approx(rng, lvl):
    want = {("C", "d"), ("A", "r")} if lvl == 1 else {("C", "r"), ("A", "d")}
    kind, given, pis, ab, vals, txt = rng.choice([c for c in _APPROX if (c[0], c[1]) in want])
    v = rng.choice(vals)
    P = R(314, 100) if pis == "3.14" else R(22, 7)
    pi_tex = "3.14" if pis == "3.14" else r"$\frac{22}{7}$"
    p = person(rng)
    stem = txt.format(v=m(v), P=p.name, he=p.he, S=soldier(rng)) + f" Use {pi_tex} for {m(r'\pi')}."
    if kind == "C":
        d = v if given == "d" else 2 * v
        ans = P * d
        fmt = _u(dec, ab)
        if given == "d":
            wrong = [(P * R(d, 2), "uses the radius instead of the diameter"),
                     (2 * P * d, r"uses the diameter in $2\pi r$, which doubles the answer"),
                     (P * R(d, 2)**2, "finds the area, not the distance around")]
            steps = [f"The distance around a circle is its circumference: {m(r'C = \pi d')}.",
                     f"{m('C \\approx ' + _times_pi(P, d))} {_w(ab)}."]
        else:
            wrong = [(P * v, r"uses the radius in $C = \pi d$; the diameter is twice the radius"),
                     (P * v * v, "finds the area, not the distance around"),
                     (4 * P * v, r"doubles the radius and then uses that diameter in $2\pi r$")]
            steps = [f"The distance around a circle is its circumference, {m(r'C = \pi d')}. "
                     f"The diameter is twice the radius: {m(f'd = 2 \\times {v} = {d}')} {_w(ab)}.",
                     f"{m('C \\approx ' + _times_pi(P, d))} {_w(ab)}."]
        check = 2 * P * R(d, 2)
    else:
        r = R(v) if given == "r" else R(v, 2)
        ans = P * r**2
        fmt = _u(dec, ab, 2)
        if given == "r":
            wrong = [(2 * P * r, "finds the circumference, not the area"),
                     (P * r, "forgets to square the radius"),
                     (P * (2 * r)**2, "uses the diameter in place of the radius")]
            steps = [f"The area of a circle is {m(r'A = \pi r^2')}. Square the radius: "
                     f"{m(f'{int_raw(r)}^2 = {int_raw(r * r)}')}.",
                     f"{m('A \\approx ' + _times_pi(P, r * r))} {_sqw(ab)}."]
        else:
            wrong = [(P * v * v, "uses the diameter in place of the radius"),
                     (P * v, "finds the circumference, not the area"),
                     (P * R(v * v, 2), "squares the diameter and then halves it; halve first, then square")]
            steps = [f"The area formula {m(r'A = \pi r^2')} needs the radius: "
                     f"{m(f'r = {v} \\div 2 = {int_raw(r)}')} {_w(ab)}.",
                     f"Square the radius: {m(f'{int_raw(r)}^2 = {int_raw(r * r)}')}.",
                     f"{m('A \\approx ' + _times_pi(P, r * r))} {_sqw(ab)}."]
        check = P * Q(2 * r)**2 / 4
    need((ans * 100).is_integer)
    if "goat" in txt:
        steps.insert(0, f"The goat can reach every point within {m(v)} feet of the stake, so the region is a "
                        f"circle with a radius of {m(v)} feet.")
    elif "every direction" in txt:
        steps.insert(0, f"The radar reaches {m(v)} miles in every direction, so it covers a circle with a "
                        f"radius of {m(v)} miles.")
    elif "jogging" in txt:
        steps.insert(0, "One lap is once around the circle, so you need the circumference.")
    n_ = ans / P                     # the number that gets multiplied by pi
    tip = None
    if pis == "3.14":
        wrong.append((3 * n_, r"uses 3 for $\pi$ instead of 3.14"))
        tip = (f"Multiply by 3 and by 0.14, then add: {m(f'3 \\times {dec_raw(n_)} = {dec_raw(3 * n_)}')} and "
               f"{m(f'0.14 \\times {dec_raw(n_)} = {dec_raw(R(14, 100) * n_)}')}, so the total is "
               f"{m(dec_raw(ans))}.")
        alts = [P * (n_ + 2), P * (n_ - 2), P * (n_ + 4)]
    else:
        alts = [P * (n_ + 7), P * (n_ - 7), P * (n_ + 14)]

    def near(rng):
        out = [v_ for v_ in alts if v_ > 0]
        rng.shuffle(out)
        return out
    return Problem(stem=stem, answer=ans, fmt=fmt, wrong=_cents(wrong), steps=steps, check=check,
                   tip=tip, near=near)


@template("MK")
def radius_from(rng, lvl):
    ab = rng.choice(_ABS)
    r = rng.randint(3, 15)
    kind = rng.choice(["A_r", "A_d", "C_r", "A_C", "C_A"])
    A, C = r * r * PI, 2 * r * PI
    if kind == "A_r":
        return Problem(
            stem=choose(rng,
                        f"A circle has an area of {m(_pi_raw(A))} {_sqw(ab)}. What is the radius of the circle?",
                        f"The area of a circle is {m(_pi_raw(A))} {_sqw(ab)}. What is its radius?"),
            answer=Q(r), fmt=_u(dec, ab), near=_int_near(r),
            wrong=[(R(r * r, 2), "divides the area by 2 instead of taking the square root"),
                   (Q(2 * r), "gives the diameter, not the radius"),
                   (Q(r * r), "forgets to take the square root")],
            steps=[f"Set the area formula equal to the area: {m(rf'\pi r^2 = {_pi_raw(A)}')}.",
                   f"Divide both sides by {m(r'\pi')}: {m(f'r^2 = {r * r}')}.",
                   f"Take the square root: {m(f'r = {r}')} {_w(ab)}, because {m(f'{r} \\times {r} = {r * r}')}."],
            verify=lambda v: v**2 * PI == A,
        )
    if kind == "A_d":
        return _radius_from_A_d(rng, r, ab)
    if kind == "C_r":
        d = 2 * r
        return Problem(
            stem=choose(rng,
                        f"The circumference of a circle is {m(_pi_raw(C))} {_w(ab)}. What is the radius of the circle?",
                        f"A circle has a circumference of {m(_pi_raw(C))} {_w(ab)}. What is its radius?"),
            answer=Q(r), fmt=_u(dec, ab), near=_int_near(r),
            wrong=[(Q(d), "gives the diameter; divide by 2 again to get the radius"),
                   (Q(2 * d), "multiplies by 2 instead of dividing by 2"),
                   (R(r, 2), "divides by 4 instead of by 2")],
            steps=[f"Use {m(r'C = 2\pi r')}: {m(rf'2\pi r = {_pi_raw(C)}')}.",
                   f"Divide both sides by {m(r'\pi')}: {m(f'2r = {d}')}. (This is the diameter.)",
                   f"Divide by 2: {m(f'r = {d} \\div 2 = {r}')} {_w(ab)}."],
            verify=lambda v: 2 * v * PI == C,
        )
    if kind == "A_C":
        return Problem(
            stem=f"A circle has an area of {m(_pi_raw(A))} {_sqw(ab)}. What is the circumference of the circle?",
            answer=C, fmt=_pi_u(ab), near=_pi_near(C),
            wrong=[(r * PI, r"finds the radius correctly but then uses $\pi r$ instead of $2\pi r$"),
                   (4 * r * PI, r"uses the diameter in $2\pi r$"),
                   (R(r * r, 2) * PI, None),
                   (2 * r * r * PI, r"mixes up the formulas and uses $2\pi r^2$")],
            steps=[f"First find the radius: {m(rf'\pi r^2 = {_pi_raw(A)}')}, so {m(f'r^2 = {r * r}')} and {m(f'r = {r}')}.",
                   f"Then {m(rf'C = 2\pi r = 2 \times \pi \times {r} = {_pi_raw(C)}')} {_w(ab)}."],
            check=PI * sp.sqrt(A / PI) * 2,
        )
    # C_A
    return Problem(
        stem=f"A circle has a circumference of {m(_pi_raw(C))} {_w(ab)}. What is the area of the circle?",
        answer=A, fmt=_pi_u(ab, 2), near=_pi_near(A),
        wrong=[(4 * r * r * PI, f"uses {m(2 * r)} (the diameter) as the radius"),
               (r * PI, "forgets to square the radius"),
               (2 * r * r * PI, r"mixes up the formulas and uses $2\pi r^2$")],
        steps=[f"First find the radius: {m(rf'2\pi r = {_pi_raw(C)}')}, so {m(f'2r = {2 * r}')} and {m(f'r = {r}')}.",
               f"Then {m(rf'A = \pi r^2 = \pi \times {r}^2 = {_pi_raw(A)}')} {_sqw(ab)}."],
        check=(C / (2 * PI))**2 * PI,
    )


def _radius_from_A_d(rng, r, ab):
    A = r * r * PI
    patio = rng.random() < 0.5
    if patio:
        ab = "ft"
        stem = f"The area of a circular patio is {m(_pi_raw(A))} square feet. What is the diameter of the patio?"
    else:
        stem = f"A circle has an area of {m(_pi_raw(A))} {_sqw(ab)}. What is the diameter of the circle?"
    return Problem(
        stem=stem, answer=Q(2 * r), fmt=_u(dec, ab), near=_int_near(2 * r, (2, -2, 4, -4)),
        wrong=[(Q(r), "gives the radius, not the diameter"),
               (Q(r * r), "forgets to take the square root"),
               (R(r * r, 2), "halves the area instead of taking the square root")],
        steps=[f"Set the area formula equal to the area: {m(rf'\pi r^2 = {_pi_raw(A)}')}, so {m(f'r^2 = {r * r}')}.",
               f"Take the square root: {m(f'r = {r}')} {_w(ab)}.",
               f"The diameter is twice the radius: {m(f'd = 2 \\times {r} = {2 * r}')} {_w(ab)}."],
        verify=lambda v: (v / 2)**2 * PI == A,
    )


def _fig_semi(label):
    return (r"\draw[thick] (-1.5,0) arc (180:0:1.5) -- cycle;" "\n"
            r"\fill (0,0) circle (1.2pt);" "\n"
            rf"\node[below] at (0,0) {{\small {label}}};")


def _fig_quarter(label):
    return (r"\draw[thick] (0,0) -- (2,0) arc (0:90:2) -- cycle;" "\n"
            r"\draw (0.22,0) -- (0.22,0.22) -- (0,0.22);" "\n"
            rf"\node[below] at (1,0) {{\small {label}}};")


@template("MK")
def part_circle(rng, lvl):
    shape = rng.choice(["semi", "quarter"])
    style = rng.choice(["fig", "fig", "ctx"])
    if shape == "semi":
        if style == "ctx":
            ctx, ab, ds = rng.choice([
                ("A window is shaped like a semicircle with a diameter of {d} feet.", "ft", [4, 8] if lvl == 2 else [4, 6, 8]),
                ("A stage is shaped like a semicircle with a diameter of {d} feet.", "ft", list(range(16, 41, 4))),
                ("A doormat is shaped like a semicircle with a diameter of {d} inches.", "in", [20, 24, 28, 32, 36]),
                ("A garden bed is shaped like a semicircle with a diameter of {d} feet.", "ft", [8, 12, 16, 20]),
            ])
            d = rng.choice(ds)
        else:
            ab = rng.choice(_ABS)
            d = rng.choice(range(4, 57, 4) if lvl == 2 else range(4, 41, 2))
            ctx = choose(rng, f"The figure shows a semicircular region with a diameter of {m(d)} {_w(ab)}.",
                         f"In the figure, the straight side of the semicircle is {m(d)} {_w(ab)} long.")
        ctx = ctx.format(d=m(d))
        fig = _fig_semi(_lab(d, ab)) if style == "fig" else None
        r = d // 2
        full = r * r * PI
        if lvl == 2:
            ans = full / 2
            return Problem(
                stem=f"{ctx} What is the area of the {'region' if style == 'fig' else ctx.split(' is shaped')[0].split(' ', 1)[1]}?",
                figure=fig,
                answer=ans, fmt=_pi_u(ab, 2), near=_pi_near(ans),
                wrong=[(full, "finds the area of the whole circle and forgets to take half"),
                       (R(d * d, 2) * PI, "uses the diameter in place of the radius"),
                       (r * PI, "finds the length of the curved edge, not the area"),
                       (full / 4, "takes one fourth of the circle instead of one half")],
                steps=[f"The radius is half the diameter: {m(f'r = {d} \\div 2 = {r}')} {_w(ab)}.",
                       f"A whole circle with this radius has area {m(rf'\pi \times {r}^2 = {_pi_raw(full)}')}.",
                       f"A semicircle is half of a circle: {m(rf'{_pi_raw(full)} \div 2 = {_pi_raw(ans)}')} {_sqw(ab)}."],
                check=PI * Q(d)**2 / 8,
            )
        arc = r * PI
        ans = arc + d
        if style == "fig":
            ask = "What is the perimeter of the region?"
        else:
            ask = (f"How many {_w(ab)} of trim are needed to go all the way around its edge, "
                   f"including the straight side?")
        return Problem(
            stem=f"{ctx} {ask}",
            figure=fig,
            answer=ans, fmt=_pi_u(ab), near=_pi_near(ans),
            wrong=[(arc, "forgets the straight edge (the diameter)"),
                   (d * PI + d, "uses the whole circumference instead of half of it"),
                   (arc + r, "adds the radius instead of the diameter"),
                   (full / 2, "finds the area, not the perimeter")],
            steps=[f"The distance around has two parts: the curved edge and the straight edge (the diameter, {m(d)} {_w(ab)}).",
                   f"The curved edge is half of the circumference: {m(rf'\frac{{1}}{{2}} \times \pi \times {d} = {_pi_raw(arc)}')} {_w(ab)}.",
                   f"Add the straight edge: {m(_pi_raw(ans))} {_w(ab)}."],
            check=PI * Q(d) / 2 + 2 * r,
        )
    # quarter circle
    if style == "ctx":
        ctx, ab, rs, what = rng.choice([
            ("A corner shelf is shaped like a quarter circle with a radius of {r} inches.", "in",
             [8, 10, 12, 14, 16], "shelf"),
            ("A flower bed in the corner of a yard is shaped like a quarter circle with a radius of {r} feet.", "ft",
             [4, 6, 8, 10, 12], "flower bed"),
            ("A tabletop is shaped like a quarter circle with a radius of {r} inches.", "in",
             [20, 24, 28, 30, 32], "tabletop"),
        ])
        r = rng.choice(rs)
    else:
        ab = rng.choice(_ABS)
        r = rng.choice(range(2, 25, 2))
        ctx = choose(rng, f"The figure shows a quarter-circle region with a radius of {m(r)} {_w(ab)}.",
                     f"The figure shows one fourth of a circle. Each straight side is {m(r)} {_w(ab)} long.")
        what = "region"
    ctx = ctx.format(r=m(r))
    fig = _fig_quarter(_lab(r, ab)) if style == "fig" else None
    full = r * r * PI
    if lvl == 2:
        ans = full / 4
        return Problem(
            stem=f"{ctx} What is the area of the {what}?",
            figure=fig,
            answer=ans, fmt=_pi_u(ab, 2), near=_pi_near(ans),
            wrong=[(full, "finds the area of the whole circle"),
                   (full / 2, "takes half of the circle instead of one fourth"),
                   (R(r, 2) * PI, "finds the length of the curved edge, not the area"),
                   (r * PI, "forgets to square the radius")],
            steps=[f"A whole circle with radius {m(r)} has area {m(rf'\pi \times {r}^2 = {_pi_raw(full)}')}.",
                   f"A quarter circle is one fourth of it: {m(rf'{_pi_raw(full)} \div 4 = {_pi_raw(ans)}')} {_sqw(ab)}."],
            check=PI * Q(r)**2 / 4,
        )
    arc = R(r, 2) * PI
    ans = arc + 2 * r
    ask = ("What is the perimeter of the region?" if style == "fig" else
           f"How many {_w(ab)} of edging are needed to go all the way around it, including the two straight sides?")
    return Problem(
        stem=f"{ctx} {ask}",
        figure=fig,
        answer=ans, fmt=_pi_u(ab), near=_pi_near(ans),
        wrong=[(arc, "forgets the two straight edges (the radii)"),
               (arc + r, "adds only one of the two straight edges"),
               (r * PI + 2 * r, "uses half of the circumference instead of one fourth"),
               (2 * r * PI + 2 * r, "uses the whole circumference instead of one fourth")],
        steps=[f"The distance around is the curved edge plus two straight edges, each a radius ({m(r)} {_w(ab)}).",
               f"The curved edge is one fourth of the circumference: "
               f"{m(rf'\frac{{1}}{{4}} \times 2\pi \times {r} = {_pi_raw(arc)}')} {_w(ab)}.",
               f"Add the straight edges: {m(f'{r} + {r} = {2 * r}')}, so the total is {m(_pi_raw(ans))} {_w(ab)}."],
        check=2 * PI * Q(r) / 4 + r + r,
    )


def _fig_ring(Rr, r, lab_R, lab_r):
    Rd = 1.6
    rd = round(Rd * r / Rr, 2)
    return (rf"\fill[black!20, even odd rule] (0,0) circle ({Rd}) (0,0) circle ({rd});" "\n"
            rf"\draw[thick] (0,0) circle ({Rd});" "\n"
            rf"\draw[thick] (0,0) circle ({rd});" "\n"
            r"\fill (0,0) circle (1.2pt);" "\n"
            rf"\draw (0,0) -- (40:{Rd}) node[pos=0.45, above left=-1pt] {{\small {lab_R}}};" "\n"
            rf"\draw (0,0) -- (180:{rd});" "\n"
            rf"\node[above] at (180:{round(rd / 2, 2)}) {{\small {lab_r}}};")


@template("MK")
def annulus(rng, lvl):
    kind = rng.choice(["fig", "fig", "walk", "walk", "washer"])
    if kind == "fig":
        Rr = rng.randint(4, 12)
        r = rng.randint(2, Rr - 1)
        need(r * 4 >= Rr)
        ans = (Rr * Rr - r * r) * PI
        ab = rng.choice(_ABS)
        return Problem(
            stem=(f"The figure shows two circles with the same center. The large circle has a radius of "
                  f"{m(Rr)} {_w(ab)}, and the small circle has a radius of {m(r)} {_w(ab)}. "
                  f"What is the area of the shaded ring?"),
            figure=_fig_ring(Rr, r, _lab(Rr), _lab(r)),
            answer=ans, fmt=_pi_u(ab, 2), near=_pi_near(ans),
            wrong=[((Rr - r)**2 * PI, "subtracts the radii before squaring"),
                   (Rr * Rr * PI, "finds the area of the large circle only"),
                   ((Rr * Rr + r * r) * PI, "adds the two areas instead of subtracting"),
                   (2 * (Rr - r) * PI, None)],
            steps=[f"Shaded ring = large circle {m('-')} small circle.",
                   f"Large circle: {m(rf'\pi \times {Rr}^2 = {_pi_raw(Rr * Rr * PI)}')}. "
                   f"Small circle: {m(rf'\pi \times {r}^2 = {_pi_raw(r * r * PI)}')}.",
                   f"Subtract: {m(rf'{_pi_raw(Rr * Rr * PI)} - {_pi_raw(r * r * PI)} = {_pi_raw(ans)}')} {_sqw(ab)}."],
            check=PI * Rr**2 - PI * r**2,
        )
    if kind == "washer":
        Dd = rng.choice(range(8, 41, 2))
        dd = rng.choice(range(4, Dd - 1, 2))
        need(dd * 4 >= Dd)
        Rr, r = Dd // 2, dd // 2
        ans = (Rr * Rr - r * r) * PI
        thing, ab = rng.choice([("metal washer", "mm"), ("rubber gasket", "mm"),
                                ("wooden ring", "in"), ("round mirror frame", "in")])
        return Problem(
            stem=(f"A flat {thing} has an outer diameter of {m(Dd)} {_w(ab)} and a hole in the center with a "
                  f"diameter of {m(dd)} {_w(ab)}. What is the area of the {thing.split()[-1]} itself "
                  f"(not counting the hole)?"),
            answer=ans, fmt=_pi_u(ab, 2), near=_pi_near(ans),
            wrong=[((Dd * Dd - dd * dd) * PI, "uses the diameters in place of the radii"),
                   ((Rr - r)**2 * PI, "subtracts the radii before squaring"),
                   (Rr * Rr * PI, "forgets to subtract the hole"),
                   ((Rr * Rr + r * r) * PI, "adds the hole instead of subtracting it")],
            steps=[f"Radii: outer {m(f'{Dd} \\div 2 = {Rr}')}, hole {m(f'{dd} \\div 2 = {r}')} {_w(ab)}.",
                   f"Outer circle: {m(rf'\pi \times {Rr}^2 = {_pi_raw(Rr * Rr * PI)}')}. "
                   f"Hole: {m(rf'\pi \times {r}^2 = {_pi_raw(r * r * PI)}')}.",
                   f"Subtract: {m(rf'{_pi_raw(Rr * Rr * PI)} - {_pi_raw(r * r * PI)} = {_pi_raw(ans)}')} {_sqw(ab)}."],
            check=PI * (Q(Dd)**2 - Q(dd)**2) / 4,
        )
    r = rng.randint(3, 12)
    wd = rng.randint(1, 4)
    need(wd < r)
    Rr = r + wd
    ans = (Rr * Rr - r * r) * PI
    thing, path, short = rng.choice([
        ("fountain", "brick walkway", "walkway"), ("pond", "gravel path", "path"),
        ("flower bed", "border of paving stones", "border"),
        ("flagpole base on the parade field", "concrete walkway", "walkway"),
        ("hot tub", "wooden deck", "deck"), ("patio", "strip of grass", "strip of grass"),
    ])
    pl = "foot" if wd == 1 else "feet"
    return Problem(
        stem=(f"A circular {thing} has a radius of {m(r)} feet. A {path} {m(wd)} {pl} wide is built all the "
              f"way around it. What is the area of the {short}?"),
        answer=ans, fmt=_pi_u("ft", 2), near=_pi_near(ans),
        wrong=[(((r + 2 * wd)**2 - r * r) * PI, "adds the width twice when finding the outer radius"),
               (wd * wd * PI, "uses the width of the path as a radius"),
               (Rr * Rr * PI, f"includes the {thing.split(' on ')[0]} itself"),
               ((Rr * Rr + r * r) * PI, "adds the two circle areas instead of subtracting")],
        steps=[f"The {short} and the {thing.split(' on ')[0]} together form a large circle with radius "
               f"{m(f'{r} + {wd} = {Rr}')} feet.",
               f"Large circle: {m(rf'\pi \times {Rr}^2 = {_pi_raw(Rr * Rr * PI)}')}. "
               f"The {thing.split(' on ')[0]}: {m(rf'\pi \times {r}^2 = {_pi_raw(r * r * PI)}')}.",
               f"The {short} is the difference: {m(rf'{_pi_raw(Rr * Rr * PI)} - {_pi_raw(r * r * PI)} = {_pi_raw(ans)}')} square feet."],
        check=PI * ((r + wd)**2 - r**2),
    )


@template("MK")
def scale_circle(rng, lvl):
    kind = rng.choice(["area", "circ", "half", "compare", "compare", "compare", "pizza", "pizza",
                       "new_area", "new_area", "new_area"])
    words = {2: "doubled", 3: "tripled", 4: "multiplied by 4", 5: "multiplied by 5"}
    if kind == "area":
        k = rng.choice([2, 3, 4, 5])
        part = rng.choice(["radius", "diameter"])
        first = f"Area depends on the radius \\emph{{squared}}: {m(r'A = \pi r^2')}."
        if part == "diameter":
            first += f" (Multiplying the diameter by {m(k)} multiplies the radius by {m(k)}, too.)"
        return Problem(
            stem=f"If the {part} of a circle is {words[k]}, the area of the circle is multiplied by what number?",
            answer=Q(k * k), fmt=num, sort=False,
            wrong=[(Q(k), f"assumes the area grows by the same factor as the {part}"),
                   (Q(2 * k), "doubles the factor instead of squaring it"),
                   (Q(k**3), "cubes the factor; that is how volume grows")],
            steps=[first,
                   f"Replace {m('r')} with {m(f'{k}r')}: {m(rf'\pi ({k}r)^2 = \pi \times {k * k}r^2 = {k * k}\pi r^2')}.",
                   f"So the area is multiplied by {m(f'{k}^2 = {k * k}')}."],
            check=sp.expand(PI * (k * x)**2) / (PI * x**2),
        )
    if kind == "circ":
        k = rng.choice([2, 3, 4, 5])
        part = rng.choice(["radius", "diameter"])
        return Problem(
            stem=f"If the {part} of a circle is {words[k]}, the circumference of the circle is multiplied by what number?",
            answer=Q(k), fmt=num, sort=False,
            wrong=[(Q(k * k), "squares the factor; only the area grows by the square"),
                   (Q(2 * k), r"doubles the factor because of the 2 in $2\pi r$"),
                   (Q(k**3), "cubes the factor")],
            steps=[f"Circumference depends on the radius itself (not squared): {m(r'C = 2\pi r')}.",
                   f"Replace {m('r')} with {m(f'{k}r')}: {m(rf'2\pi ({k}r) = {k} \times 2\pi r')}.",
                   f"So the circumference is multiplied by {m(k)}."],
            check=sp.expand(2 * PI * (k * x)) / (2 * PI * x),
        )
    if kind == "half":
        k = rng.choice([2, 3])
        how = "cut in half" if k == 2 else "divided by 3"
        return Problem(
            stem=f"If the radius of a circle is {how}, the area of the new circle is what fraction of the area of the original circle?",
            answer=R(1, k * k), fmt=frac, sort=False,
            wrong=[(R(1, k), "assumes the area shrinks by the same factor as the radius"),
                   (R(1, k**3), "cubes the factor; that is how volume changes"),
                   (R(1, 2 * k), "doubles the factor instead of squaring it")],
            steps=[f"The new radius is {m(rf'\frac{{1}}{{{k}}}r')}.",
                   f"New area: {m(rf'\pi \left(\frac{{1}}{{{k}}}r\right)^2 = \frac{{1}}{{{k * k}}}\pi r^2')}.",
                   f"So the new area is {m(F(1, k * k))} of the original."],
            check=(PI * (x / k)**2) / (PI * x**2),
        )
    if kind == "compare":
        a_ = rng.randint(2, 10)
        k = rng.choice([2, 3, 4, 5])
        b_ = a_ * k
        ab = rng.choice(_ABS)
        part = rng.choice(["radius", "diameter"])
        rA, rB = (R(a_), R(b_)) if part == "radius" else (R(a_, 2), R(b_, 2))
        AA, AB = rA**2 * PI, rB**2 * PI
        return Problem(
            stem=(f"Circle {m('A')} has a {part} of {m(a_)} {_w(ab)}, and circle {m('B')} has a {part} of "
                  f"{m(b_)} {_w(ab)}. The area of circle {m('B')} is how many times the area of circle {m('A')}?"),
            answer=Q(k * k), fmt=num,
            wrong=[(Q(k), f"compares the {part}s instead of the areas"),
                   (Q(2 * k), "doubles the ratio instead of squaring it"),
                   (Q(k**3), "cubes the ratio")],
            steps=([f"Radii: {m(f'{a_} \\div 2 = {dec_raw(rA)}')} and {m(f'{b_} \\div 2 = {dec_raw(rB)}')} {_w(ab)}."]
                   if part == "diameter" else []) +
                  [f"Areas: circle {m('A')} has {m(rf'\pi \times {dec_raw(rA)}^2 = {_pi_raw(AA)}')}, and circle {m('B')} has "
                   f"{m(rf'\pi \times {dec_raw(rB)}^2 = {_pi_raw(AB)}')}.",
                   f"Divide: {m(rf'{_pi_raw(AB)} \div {_pi_raw(AA)} = {k * k}')}."],
            tip=f"Shortcut: the {part} is {m(k)} times as large, so the area is {m(f'{k}^2 = {k * k}')} times as large.",
            check=AB / AA,
        )
    if kind == "pizza":
        small, k = rng.choice([(6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (6, 3)])
        big = small * k
        need(big <= 20)
        p = person(rng)
        rs, rb = R(small, 2), R(big, 2)
        return Problem(
            stem=(f"{p.name} is choosing between a pizza with a diameter of {m(small)} inches and a pizza "
                  f"with a diameter of {m(big)} inches. The area of the larger pizza is how many times the "
                  f"area of the smaller one?"),
            answer=Q(k * k), fmt=num,
            wrong=[(Q(k), "compares the diameters instead of the areas"),
                   (Q(2 * k), "doubles the ratio instead of squaring it"),
                   (Q(k**3), "cubes the ratio")],
            steps=[f"Radii: {m(f'{small} \\div 2 = {dec_raw(rs)}')} and {m(f'{big} \\div 2 = {dec_raw(rb)}')} inches.",
                   f"Areas: {m(rf'\pi \times {dec_raw(rs)}^2 = {_pi_raw(rs * rs * PI)}')} and "
                   f"{m(rf'\pi \times {dec_raw(rb)}^2 = {_pi_raw(rb * rb * PI)}')} square inches.",
                   f"Divide: {m(rf'{_pi_raw(rb * rb * PI)} \div {_pi_raw(rs * rs * PI)} = {k * k}')}."],
            tip=f"The diameter is {m(k)} times as large, so the area is {m(f'{k}^2 = {k * k}')} times as large.",
            check=Q(big)**2 / small**2,
        )
    # new_area
    k = rng.choice([2, 3, 4])
    a0 = rng.randint(2, 25)
    ab = rng.choice(_ABS)
    A0 = a0 * PI
    ans = k * k * A0
    return Problem(
        stem=(f"A circle has an area of {m(_pi_raw(A0))} {_sqw(ab)}. If the radius of the circle is "
              f"{words[k]}, what is the area of the new circle?"),
        answer=ans, fmt=_pi_u(ab, 2), near=_pi_near(ans, [(k * k + 1) * A0, (k * k - 1) * A0, A0 + k * k]),
        wrong=[(k * A0, f"multiplies the area by {m(k)} instead of by {m(k * k)}"),
               (k**3 * A0, f"multiplies the area by {m(f'{k}^3 = {k**3}')} instead of {m(f'{k}^2')}"),
               (2 * k * A0, f"multiplies the area by {m(f'2 \\times {k}')} instead of {m(f'{k}^2')}")],
        steps=[f"Area depends on the radius squared, so multiplying the radius by {m(k)} multiplies the area by "
               f"{m(f'{k}^2 = {k * k}')}.",
               f"New area: {m(rf'{k * k} \times {_pi_raw(A0)} = {_pi_raw(ans)}')} {_sqw(ab)}."],
        check=PI * (k * sp.sqrt(a0))**2,
    )


# shaded regions -------------------------------------------------------------

def _fig_sq_circle(s, ab):
    S = 2.6
    h = S / 2
    return (rf"\fill[black!20] (0,0) rectangle ({S},{S});" "\n"
            rf"\fill[white] ({h},{h}) circle ({h});" "\n"
            rf"\draw[thick] (0,0) rectangle ({S},{S});" "\n"
            rf"\draw[thick] ({h},{h}) circle ({h});" "\n"
            rf"\node[below] at ({h},0) {{\small {_lab(s, ab)}}};")


def _fig_sq_quarter(s, ab):
    S = 2.6
    return (rf"\fill[black!20] (0,0) rectangle ({S},{S});" "\n"
            rf"\fill[white] (0,0) -- ({S},0) arc (0:90:{S}) -- cycle;" "\n"
            rf"\draw[thick] (0,0) rectangle ({S},{S});" "\n"
            rf"\draw[thick] ({S},0) arc (0:90:{S});" "\n"
            r"\fill (0,0) circle (1.2pt);" "\n"
            rf"\node[below] at ({S / 2},0) {{\small {_lab(s, ab)}}};")


def _fig_stadium(L, r, ab):
    Ld = 2.8
    Hd = Ld * 2 * r / L
    to_scale = 0.9 <= Hd <= 2.0
    Hd = round(min(max(Hd, 0.9), 2.0), 2)
    h = round(Hd / 2, 3)
    fig = (rf"\fill[black!20] (0,0) -- ({Ld},0) arc (-90:90:{h}) -- (0,{Hd}) arc (90:270:{h}) -- cycle;" "\n"
           rf"\draw[thick] (0,0) -- ({Ld},0) arc (-90:90:{h}) -- (0,{Hd}) arc (90:270:{h}) -- cycle;" "\n"
           rf"\draw[dashed] (0,0) -- (0,{Hd});" "\n"
           rf"\draw[dashed] ({Ld},0) -- ({Ld},{Hd});" "\n"
           rf"\node[above] at ({Ld / 2},{Hd}) {{\small {_lab(L, ab)}}};" "\n"
           rf"\node[left] at ({Ld},{h}) {{\small {_lab(2 * r, ab)}}};")
    return fig, to_scale


def _fig_arch(w, h, ab):
    Wd = 1.8
    Hd = Wd * h / w
    to_scale = 0.8 <= Hd <= 2.2
    Hd = round(min(max(Hd, 0.8), 2.2), 2)
    rd = Wd / 2
    fig = (rf"\fill[black!20] (0,0) -- ({Wd},0) -- ({Wd},{Hd}) arc (0:180:{rd}) -- cycle;" "\n"
           rf"\draw[thick] (0,0) -- ({Wd},0) -- ({Wd},{Hd}) arc (0:180:{rd}) -- cycle;" "\n"
           rf"\draw[dashed] (0,{Hd}) -- ({Wd},{Hd});" "\n"
           rf"\node[below] at ({rd},0) {{\small {_lab(w, ab)}}};" "\n"
           rf"\node[right] at ({Wd},{Hd / 2}) {{\small {_lab(h, ab)}}};")
    return fig, to_scale


def _whole_pi(wrong):
    """Keep distractors whose pi-coefficient is a whole number (no 11pi/2 clutter)."""
    return [w_ for w_ in wrong if _split(w_[0])[1].q == 1]


@template("MK")
def shaded_region(rng, lvl):
    p_ = _shaded(rng)
    p_.wrong = _whole_pi(p_.wrong)
    return p_


def _shaded(rng):
    kind = rng.choice(["inscribed", "inscribed", "quarter", "stadium", "arch"])
    ab = rng.choice(_ABS)
    if kind == "inscribed":
        s = rng.choice(range(4, 31, 2))
        r = s // 2
        circ = r * r * PI
        ans = s * s - circ
        return Problem(
            stem=(f"In the figure, a circle fits exactly inside a square with sides of {m(s)} {_w(ab)}, "
                  f"touching all four sides. What is the area of the shaded region?"),
            figure=_fig_sq_circle(s, ab),
            answer=ans, fmt=_pi_u(ab, 2), near=_pi_near(ans),
            wrong=[(circ, "finds the area of the circle, not the shaded corners"),
                   (ans / 4 if s % 4 == 0 else s * s - 2 * r * r * PI, "finds only one of the four shaded corners"
                    if s % 4 == 0 else None),
                   (s * s - s * PI, "subtracts the circumference instead of the area of the circle"),
                   (s * s - r * PI, "forgets to square the radius"),
                   (Q(s * s), "finds the area of the square only")],
            steps=[f"The circle touches all four sides, so its diameter equals the side of the square: "
                   f"{m(f'd = {s}')}, so {m(f'r = {r}')}.",
                   f"Square: {m(f'{s}^2 = {s * s}')}. Circle: {m(rf'\pi \times {r}^2 = {_pi_raw(circ)}')}.",
                   f"Shaded region = square {m('-')} circle {m('= ' + _pi_raw(ans))} {_sqw(ab)}."],
            tip=(f"Sense check: {m(_pi_raw(circ))} is a little more than {m(3 * r * r)}, so the shaded corners "
                 f"are only a small part of the square's {m(s * s)}, just as the figure shows."),
            check=Q(s)**2 * (1 - PI / 4),
        )
    if kind == "quarter":
        s = rng.choice(range(4, 25, 2))
        qa = R(s * s, 4) * PI
        ans = s * s - qa
        return Problem(
            stem=(f"The figure shows a square with sides of {m(s)} {_w(ab)}. A quarter circle is drawn inside it "
                  f"with its center at the lower-left corner of the square and a radius of {m(s)} {_w(ab)}. "
                  f"What is the area of the shaded region?"),
            figure=_fig_sq_quarter(s, ab),
            answer=ans, fmt=_pi_u(ab, 2), near=_pi_near(ans),
            wrong=[(qa, "finds the area of the quarter circle, not the shaded region"),
                   (s * s - R(s, 2) * PI, "subtracts the length of the arc instead of the area"),
                   (s * s - R(s, 4) * PI, "forgets to square the radius"),
                   (s * s + qa, "adds the quarter circle instead of subtracting it")],
            steps=[f"Square: {m(f'{s}^2 = {s * s}')}.",
                   f"Quarter circle with radius {m(s)}: {m(rf'\frac{{1}}{{4}} \times \pi \times {s}^2 = {_pi_raw(qa)}')}.",
                   f"Shaded region = square {m('-')} quarter circle {m('= ' + _pi_raw(ans))} {_sqw(ab)}."],
            check=Q(s)**2 - PI * s**2 / 4,
        )
    if kind == "stadium":
        r = rng.randint(2, 7)
        L = rng.choice(range(6, 25, 2))
        need(R(1, 3) <= R(2 * r, L) <= R(3, 4))
        rect = L * 2 * r
        circ = r * r * PI
        ans = rect + circ
        fig, to_scale = _fig_stadium(L, r, ab)
        return Problem(
            stem=(f"The figure is made of a rectangle that is {m(L)} {_w(ab)} long and {m(2 * r)} {_w(ab)} wide, "
                  f"with a semicircle attached to each end. What is the area of the whole figure?"
                  + ("" if to_scale else " (Figure not drawn to scale.)")),
            figure=fig,
            answer=ans, fmt=_pi_u(ab, 2), near=_pi_near(ans),
            wrong=[(rect + 2 * circ, "counts each semicircle as a whole circle"),
                   (rect + circ / 2, "includes only one of the two semicircles"),
                   (rect + 4 * circ, "uses the diameter of the semicircles as the radius"),
                   (Q(rect), "leaves out the semicircles")],
            steps=[f"Rectangle: {m(f'{L} \\times {2 * r} = {rect}')} {_sqw(ab)}.",
                   f"Each semicircle has a diameter of {m(2 * r)}, so a radius of {m(r)}. The two semicircles "
                   f"together make one whole circle: {m(rf'\pi \times {r}^2 = {_pi_raw(circ)}')}.",
                   f"Total area: {m(_pi_raw(ans))} {_sqw(ab)}."],
            check=Q(L) * 2 * r + 2 * (PI * r**2 / 2),
        )
    # arch: rectangle with a semicircle on top
    w = rng.choice([4, 6, 8, 10, 12, 16])
    h = rng.choice(range(3, 21))
    need(R(h, w) >= R(1, 2) and R(h, w) <= 2)
    r = R(w, 2)
    rect = w * h
    semi = r * r * PI / 2
    ans = rect + semi
    fig, to_scale = _fig_arch(w, h, ab)
    return Problem(
        stem=(f"The figure shows a rectangle {m(w)} {_w(ab)} wide and {m(h)} {_w(ab)} tall with a semicircle on top. "
              f"What is the area of the whole figure?" + ("" if to_scale else " (Figure not drawn to scale.)")),
        figure=fig,
        answer=ans, fmt=_pi_u(ab, 2), near=_pi_near(ans),
        wrong=[(rect + r * r * PI, "uses a whole circle instead of a semicircle"),
               (rect + w * w * PI / 2, "uses the width of the rectangle as the radius"),
               (rect + r * PI, "adds the length of the curved edge instead of the area"),
               (Q(rect), "leaves out the semicircle")],
        steps=[f"Rectangle: {m(f'{w} \\times {h} = {rect}')} {_sqw(ab)}.",
               f"The semicircle's diameter is the width, {m(w)}, so its radius is {m(dec_raw(r))}. Its area is half a circle: "
               f"{m(rf'\frac{{1}}{{2}} \times \pi \times {dec_raw(r)}^2 = {_pi_raw(semi)}')}.",
               f"Total area: {m(_pi_raw(ans))} {_sqw(ab)}."],
        check=Q(w) * h + PI * Q(w)**2 / 8,
    )


def _fig_sector(theta, r_lab, mode):
    Rd = 1.35
    lines = []
    if mode == "area":
        lines.append(rf"\fill[black!20] (0,0) -- (0:{Rd}) arc (0:{theta}:{Rd}) -- cycle;")
    lines.append(rf"\draw[thick] (0,0) circle ({Rd});")
    lines.append(rf"\draw (0:{Rd}) -- (0,0) -- ({theta}:{Rd});")
    if mode == "arc":
        lines.append(rf"\draw[line width=2.2pt] (0:{Rd}) arc (0:{theta}:{Rd});")
        lines.append(rf"\node[right] at (0:{Rd}) {{\small $A$}};")
        lines.append(rf"\node[anchor={(theta + 180) % 360}] at ({theta}:{Rd + 0.04}) {{\small $B$}};")
    lines.append(r"\fill (0,0) circle (1.2pt);")
    lines.append(r"\draw (0.28,0) arc (0:" + str(theta) + ":0.28);")
    lines.append(rf"\node at ({theta / 2}:{0.62 if theta >= 60 else 0.78}) {{\scriptsize ${theta}^\circ$}};")
    lines.append(rf"\node[below] at ({Rd / 2},0) {{\small {r_lab}}};")
    return "\n".join(lines)


@template("MK")
def arc_sector(rng, lvl):
    kind = rng.choice(["area", "area", "arc", "arc", "sprinkler", "slice"])
    if kind == "sprinkler":
        theta = rng.choice([60, 90, 120, 150, 180, 270])
        r = rng.choice([6, 8, 10, 12, 15, 18, 20, 24, 25, 30])
        frac_ = R(theta, 360)
        ans = frac_ * r * r * PI
        need(ans.coeff(PI).is_integer)
        return Problem(
            stem=(f"A lawn sprinkler sprays water {m(r)} feet and turns back and forth through an angle of "
                  f"{m(f'{theta}^\\circ')}. What is the area of the lawn it waters?"),
            answer=ans, fmt=_pi_u("ft", 2), near=_pi_near(ans),
            wrong=[(r * r * PI, "finds the area of the whole circle"),
                   (frac_ * 2 * r * PI, "finds the length of the arc, not the area"),
                   (R(theta, 180) * r * r * PI, r"divides the angle by $180^\circ$ instead of $360^\circ$"),
                   (frac_ * r * PI, "forgets to square the radius")],
            steps=[f"The watered region is a sector of a circle with radius {m(r)} feet and angle {m(f'{theta}^\\circ')}.",
                   f"That is {m(F(theta, 360) + ' = ' + frac_raw(frac_))} of a whole circle. Whole circle: "
                   f"{m(rf'\pi \times {r}^2 = {_pi_raw(r * r * PI)}')}.",
                   f"Sector: {m(rf'{frac_raw(frac_)} \times {_pi_raw(r * r * PI)} = {_pi_raw(ans)}')} square feet."],
            check=PI * r**2 * theta / 360,
        )
    if kind == "slice":
        d = rng.choice([10, 12, 14, 16, 18, 20, 24])
        k = rng.choice([4, 6, 8, 12])
        r = d // 2
        ans = R(r * r, k) * PI
        need(ans.coeff(PI).is_integer)
        return Problem(
            stem=(f"A pizza with a diameter of {m(d)} inches is cut into {m(k)} equal slices. "
                  f"What is the area of one slice?"),
            answer=ans, fmt=_pi_u("in", 2), near=_pi_near(ans),
            wrong=[(R(d * d, k) * PI, "uses the diameter in place of the radius"),
                   (r * r * PI, "finds the area of the whole pizza"),
                   (R(d, k) * PI, "finds the length of crust on one slice, not its area"),
                   (R(r * r, 2 * k) * PI, None)],
            steps=[f"The radius is {m(f'{d} \\div 2 = {r}')} inches, so the whole pizza has area "
                   f"{m(rf'\pi \times {r}^2 = {_pi_raw(r * r * PI)}')} square inches.",
                   f"One slice is {m(F(1, k))} of the pizza: {m(rf'{_pi_raw(r * r * PI)} \div {k} = {_pi_raw(ans)}')} square inches."],
            check=PI * Q(d)**2 / (4 * k),
        )
    theta = rng.choice([45, 60, 72, 80, 90, 100, 120, 135, 150, 210, 225, 240, 270, 300])
    r = rng.randint(2, 18)
    ab = rng.choice(_ABS)
    frac_ = R(theta, 360)
    full_A, full_C = r * r * PI, 2 * r * PI
    if kind == "area":
        ans = frac_ * full_A
        need(ans.coeff(PI).is_integer and r * r >= frac_.q)
        return Problem(
            stem=(f"In the circle shown, the radius is {m(r)} {_w(ab)} and the shaded sector has a central angle of "
                  f"{m(f'{theta}^\\circ')}. What is the area of the shaded sector?"),
            figure=_fig_sector(theta, _lab(r, ab), "area"),
            answer=ans, fmt=_pi_u(ab, 2), near=_pi_near(ans),
            wrong=[(full_A, "finds the area of the whole circle"),
                   (frac_ * full_C, "finds the arc length, not the area"),
                   (R(360 - theta, 360) * full_A, "finds the unshaded part of the circle"),
                   (R(theta, 180) * full_A if theta < 180 else R(theta, 90) * r * PI,
                    r"divides the angle by $180^\circ$ instead of $360^\circ$" if theta < 180 else None)],
            steps=[f"The sector is {m(F(theta, 360) + ' = ' + frac_raw(frac_))} of the whole circle.",
                   f"Whole circle: {m(rf'\pi \times {r}^2 = {_pi_raw(full_A)}')}.",
                   f"Sector: {m(rf'{frac_raw(frac_)} \times {_pi_raw(full_A)} = {_pi_raw(ans)}')} {_sqw(ab)}."],
            check=PI * r**2 * theta / 360,
        )
    ans = frac_ * full_C
    need(ans.coeff(PI).is_integer and theta < 360)
    return Problem(
        stem=(f"In the circle shown, the radius is {m(r)} {_w(ab)} and the central angle is {m(f'{theta}^\\circ')}. "
              f"What is the length of the arc from {m('A')} to {m('B')} shown in bold?"),
        figure=_fig_sector(theta, _lab(r, ab), "arc"),
        answer=ans, fmt=_pi_u(ab), near=_pi_near(ans),
        wrong=[(full_C, "finds the circumference of the whole circle"),
               (frac_ * full_A, "finds the area of the sector, not the arc length"),
               (frac_ * r * PI, r"uses $\pi r$ instead of $2\pi r$ for the circumference"),
               (R(360 - theta, 360) * full_C, "finds the length of the other arc")],
        steps=[f"The arc is {m(F(theta, 360) + ' = ' + frac_raw(frac_))} of the whole circle.",
               f"Circumference: {m(rf'2\pi \times {r} = {_pi_raw(full_C)}')}.",
               f"Arc length: {m(rf'{frac_raw(frac_)} \times {_pi_raw(full_C)} = {_pi_raw(ans)}')} {_w(ab)}."],
        check=PI * 2 * r * theta / 360,
    )


_MILES = {R(1, 4): "a quarter of a mile", R(1, 2): "half a mile", Q(1): "1 mile", Q(2): "2 miles",
          Q(3): "3 miles"}


@template("AR")
def wheel(rng, lvl):
    kind = rng.choice(["dist", "dist", "revs", "mile"])
    p = person(rng)
    if kind == "dist":
        thing, d = rng.choice([(f"The front wheel of {p.name}'s bicycle", 28),
                               (f"The wheel of {p.name}'s wheelbarrow", 14),
                               (f"A tire on {soldier(rng)}'s Humvee", 35),
                               (f"The front wheel of {p.name}'s tractor", 42),
                               (f"A wheel on {p.name}'s utility trailer", 21),
                               (f"A wheel on {p.name}'s lawn mower", 7)])
        C = R(22, 7) * d
        n_ = rng.choice([6, 10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 48, 50, 60, 72, 90, 100])
        tot_in = C * n_
        need(tot_in % 12 == 0)
        ans = tot_in / 12
        return Problem(
            stem=(f"{thing} has a diameter of {m(d)} inches. How many feet does it roll in "
                  f"{m(n_)} complete turns? Use {m(F(22, 7))} for {m(r'\pi')}."),
            answer=ans, fmt=_u(dec, "ft"), near=lambda rng: [v_ for v_ in (ans * R(4, 3), ans * R(2, 3), ans * R(3, 2), ans * R(3, 4)) if v_.is_integer],
            wrong=[w_ for w_ in [(ans / 2, "uses the radius instead of the diameter"),
                                 (tot_in, "forgets to convert inches to feet"),
                                 (2 * ans, r"uses the diameter in $2\pi r$"),
                                 (R(22, 7) * R(d, 2)**2 * n_ / 12, "uses the area of the wheel instead of its circumference")]
                   if (Q(w_[0]) * 10).is_integer],
            steps=[f"In one turn the wheel rolls one circumference: {m('C = \\pi d \\approx ' + _times_pi(R(22, 7), d))} inches.",
                   f"In {m(n_)} turns: {m(f'{int_raw(C)} \\times {n_} = {int_raw(tot_in)}')} inches.",
                   f"Convert to feet (12 inches = 1 foot): {m(f'{int_raw(tot_in)} \\div 12 = {dec_raw(ans)}')} feet."],
            check=Q(22) * d * n_ / (7 * 12),
        )
    if kind == "revs":
        d = rng.choice([1, 2, 4, 5])
        n_ = rng.choice([25, 50, 100, 200, 250, 500])
        C = R(314, 100) * d
        dist = C * n_
        need(dist.is_integer and dist <= 3000)
        if d <= 2:
            thing = rng.choice([f"{p.name}'s garden cart", f"{soldier(rng)}'s supply cart",
                                f"{p.name}'s hand truck", f"{p.name}'s hose reel cart"])
        elif d == 4:
            thing = rng.choice(["a horse-drawn wagon at a farm museum", "an old-fashioned farm wagon"])
        else:
            thing = rng.choice([f"the rear axle of {p.name}'s tractor", "the rear axle of a large tractor"])
        return Problem(
            stem=(f"The wheels of {thing} have a diameter of {m(d)} {'foot' if d == 1 else 'feet'}. "
                  f"How many complete turns does each wheel make when the "
                  f"{'cart' if d <= 2 else 'wagon' if d == 4 else 'tractor'} moves {num(dist)} feet? "
                  f"Use 3.14 for {m(r'\pi')}."),
            answer=Q(n_), fmt=num, near=lambda rng: [Q(n_) * R(3, 2), Q(n_) * R(4, 5), Q(n_) * R(3, 5)],
            wrong=[(Q(2 * n_), "uses the radius instead of the diameter"),
                   (dist / d, "divides the distance by the diameter instead of the circumference"),
                   (R(n_, 2), r"uses the diameter in $2\pi r$")],
            steps=[f"Each turn of a wheel moves it forward one circumference: {m('C = \\pi d \\approx ' + _times_pi(R(314, 100), d))} feet.",
                   f"Number of turns {m('=')} distance {m(r'\div')} circumference: {m(f'{int_raw(dist)} \\div {dec_raw(C)} = {n_}')}."],
            tip=f"Move the decimal point to divide by a whole number: {m(f'{int_raw(dist)} \\div {dec_raw(C)} = {int_raw(dist * 100)} \\div {int_raw(C * 100)}')}.",
            verify=lambda v: v * C == dist,
        )
    # revolutions in a mile
    d, Cft = rng.choice([(42, 11), (21, R(11, 2))])
    miles = rng.choice([R(1, 4), R(1, 2), Q(1), Q(2), Q(3)])
    feet = miles * 5280
    ans = feet / Q(Cft)
    if d == 42:
        thing = rng.choice([f"{p.name}'s truck tire", f"a tire on {soldier(rng)}'s cargo truck",
                            f"the front tire of {p.name}'s tractor"])
    else:
        thing = rng.choice([f"a tire on {p.name}'s utility trailer", f"a rear tire of {p.name}'s riding mower",
                            f"a tire on {soldier(rng)}'s supply trailer"])
    dist_step = ([] if miles == 1 else
                 [f"Change the distance to feet: {m(f'{frac_raw(miles)} \\times {int_raw(5280)} = {int_raw(feet)}')} feet."])
    return Problem(
        stem=(f"The diameter of {thing} is {m(d)} inches. About how many complete turns does the tire make "
              f"in {_MILES[miles]}? (1 mile {m('=')} {num(5280)} feet; use {m(F(22, 7))} for {m(r'\pi')}.)"),
        answer=ans, fmt=num, near=lambda rng: [ans * R(3, 4), ans * R(5, 4), ans * R(3, 2)],
        wrong=[(2 * ans, "uses the radius instead of the diameter"),
               (ans / 12, "forgets to convert the circumference from inches to feet"),
               (ans / 2, r"uses the diameter in $2\pi r$"),
               (Q(feet) / d * 12, "divides by the diameter instead of the circumference")],
        steps=[f"One turn covers one circumference: {m('C = \\pi d \\approx ' + _times_pi(R(22, 7), d))} inches.",
               f"Change to feet: {m(f'{int_raw(R(22, 7) * d)} \\div 12 = {dec_raw(Cft)}')} feet.",
               ] + dist_step + [
               f"Turns {m('=')} distance {m(r'\div')} circumference: {m(f'{int_raw(feet)} \\div {dec_raw(Cft)} = {int_raw(ans)}')}."],
        tip=(f"To divide by 5.5, double both numbers and divide by 11: {m(f'{int_raw(2 * feet)} \\div 11 = {int_raw(ans)}')}."
             if Cft != 11 else None),
        verify=lambda v: v * R(22, 7) * d == feet * 12,
    )


PLAN = [
    # (template, level, count) -- easy -> hard; 25 problems
    (circle_area, 1, 3),
    (circumference, 1, 3),
    (pi_approx, 1, 2),
    (circle_area, 2, 1),
    (radius_from, 2, 2),
    (part_circle, 2, 2),
    (annulus, 2, 2),
    (scale_circle, 2, 2),
    (pi_approx, 2, 1),
    (part_circle, 3, 1),
    (shaded_region, 3, 2),
    (arc_sector, 3, 2),
    (wheel, 3, 2),
]
