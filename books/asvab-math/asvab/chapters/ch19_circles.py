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
          "yd": ("yard", "yards"), "mi": ("mile", "miles")}


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
    c = sp.simplify(v - k * PI)
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


def pifmt(v):
    return m(_pi_raw(v))


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


def _pi_near(ans):
    """Plausible filler choices for an answer c + k*pi (other multiples of pi)."""
    c, k = _split(ans)

    def f(rng):
        a = abs(k)
        st = 1 if a <= 12 else 2 if a <= 30 else 5 if a <= 80 else 10 if a <= 200 else 50
        out = [c + (k + j * st) * PI for j in (1, -1, 2, -2, 3, -3)]
        out += [c + 2 * k * PI, c + k * PI / 2]
        out = [v for v in out if Q(v) > 0 and sp.simplify(v - ans) != 0]
        rng.shuffle(out)
        return out
    return f


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

@template("MK")
def circle_area(rng, lvl):
    if lvl == 1:
        ab = rng.choice(["in", "ft", "cm", "m"])
        r = rng.randint(3, 12)
        ans = r**2 * PI
        style = rng.choice(["fig", "text", "text"])
        fig = None
        if style == "fig":
            stem = f"What is the area of the circle shown? The radius is {m(r)} {_w(ab)}."
            fig = _fig_radius(_lab(r, ab))
        else:
            stem = choose(rng,
                          f"A circle has a radius of {m(r)} {_w(ab)}. What is the area of the circle?",
                          f"What is the area of a circle with a radius of {m(r)} {_w(ab)}?",
                          f"Find the area of a circle whose radius is {m(r)} {_w(ab)}.")
        return Problem(
            stem=stem, figure=fig,
            answer=ans, fmt=_pi_u(ab, 2), near=_pi_near(ans),
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
    # level 2: diameter given
    ctx = rng.choice([
        ("plain", "cm", list(range(6, 25, 2))),
        ("fig", "in", list(range(6, 25, 2))),
        ("a circular mirror", "in", [12, 14, 16, 18, 20, 24]),
        ("a round trampoline", "ft", [8, 10, 12, 14, 16]),
        ("a circular helicopter landing pad", "ft", [40, 50, 60, 80]),
        ("a round paper target at the rifle range", "in", [12, 14, 16, 18, 20]),
        ("a circular rug", "ft", [6, 8, 10, 12]),
    ])
    what, ab, ds = ctx
    d = rng.choice(ds)
    r = d // 2
    ans = r**2 * PI
    fig = None
    if what == "plain":
        stem = f"A circle has a diameter of {m(d)} {_w(ab)}. What is its area?"
    elif what == "fig":
        stem = f"The diameter of the circle shown is {m(d)} {_w(ab)}. What is the area of the circle?"
        fig = _fig_diameter(_lab(d, ab))
    else:
        stem = (f"{what[0].upper() + what[1:]} has a diameter of {m(d)} {_w(ab)}. "
                f"What is its area?")
    return Problem(
        stem=stem, figure=fig,
        answer=ans, fmt=_pi_u(ab, 2), near=_pi_near(ans),
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
    ab = rng.choice(["in", "ft", "cm", "m"])
    given = rng.choice(["r", "d"])
    if given == "r":
        r = rng.randint(3, 15)
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
            answer=ans, fmt=_pi_u(ab), near=_pi_near(ans),
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
    d = rng.randint(4, 30)
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
        answer=ans, fmt=_pi_u(ab), near=_pi_near(ans),
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
    ("C", "d", "3.14", "ft", [10, 20, 30, 15, 25],
     "{P} is putting a fence around a circular garden that has a diameter of {v} feet. "
     "How many feet of fencing does {he} need?"),
    ("C", "r", "3.14", "ft", [5, 10, 15, 20],
     "{P} is putting a fence around a circular garden that has a radius of {v} feet. "
     "How many feet of fencing does {he} need?"),
    ("C", "d", "3.14", "ft", [40, 50, 60, 100],
     "A circular helicopter landing pad has a diameter of {v} feet. The ground crew will outline "
     "its edge with reflective tape. How many feet of tape are needed?"),
    ("C", "r", "3.14", "ft", [20, 25, 30, 50],
     "A circular helicopter landing pad has a radius of {v} feet. The ground crew will outline "
     "its edge with reflective tape. How many feet of tape are needed?"),
    ("C", "r", "3.14", "m", [25, 50, 100],
     "{S}'s squad is stringing one strand of wire around a circular perimeter with a radius of "
     "{v} meters. How many meters of wire are needed to go around once?"),
    ("C", "d", "22/7", "in", [28, 35, 42, 49, 56],
     "A round tabletop has a diameter of {v} inches. How many inches of trim are needed to go "
     "around its edge?"),
    ("C", "r", "22/7", "in", [14, 21, 28],
     "A round tabletop has a radius of {v} inches. How many inches of trim are needed to go "
     "around its edge?"),
    ("C", "d", "22/7", "m", [70, 140],
     "A jogging path is a circle with a diameter of {v} meters. How many meters does {P} run "
     "in one lap?"),
    ("A", "r", "3.14", "ft", [2, 3, 4, 5],
     "A circular rug has a radius of {v} feet. What is the area of the rug?"),
    ("A", "d", "3.14", "ft", [4, 6, 8, 10],
     "A circular rug has a diameter of {v} feet. What is the area of the rug?"),
    ("A", "r", "3.14", "ft", [5, 10, 20],
     "A lawn sprinkler waters a circle with a radius of {v} feet. How many square feet of lawn "
     "does it water?"),
    ("A", "d", "3.14", "ft", [10, 20, 40],
     "A lawn sprinkler waters a circle with a diameter of {v} feet. How many square feet of lawn "
     "does it water?"),
    ("A", "r", "3.14", "mi", [10, 20, 30, 50],
     "A radar station can detect aircraft up to {v} miles away in every direction. How many "
     "square miles does it cover?"),
    ("A", "d", "3.14", "mi", [20, 40, 60],
     "A radar station covers a circular area with a diameter of {v} miles. How many square "
     "miles does it cover?"),
    ("A", "r", "22/7", "ft", [7, 14],
     "A round field tent has a floor with a radius of {v} feet. What is the floor area of the tent?"),
    ("A", "d", "22/7", "ft", [14, 28],
     "A round field tent has a floor with a diameter of {v} feet. What is the floor area of the tent?"),
    ("A", "d", "22/7", "in", [14],
     "A pizza has a diameter of {v} inches. What is the area of the top of the pizza?"),
    ("A", "d", "3.14", "ft", [10, 20],
     "A circular swimming pool has a diameter of {v} feet. How many square feet of cover are "
     "needed to cover the top of the pool?"),
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
    need(ans.q in (1, 2, 4, 5, 10, 20, 25, 50, 100))
    tip = None
    if pis == "3.14":
        n_ = (ans / P)
        tip = (f"Multiply by 3 and by 0.14, then add: {m(f'3 \\times {dec_raw(n_)} = {dec_raw(3 * n_)}')} and "
               f"{m(f'0.14 \\times {dec_raw(n_)} = {dec_raw(R(14, 100) * n_)}')}, so the total is "
               f"{m(dec_raw(ans))}.")
    return Problem(stem=stem, answer=ans, fmt=fmt, wrong=wrong, steps=steps, check=check, tip=tip)


@template("MK")
def radius_from(rng, lvl):
    ab = rng.choice(["in", "ft", "cm", "m"])
    r = rng.randint(3, 12)
    kind = rng.choice(["A_r", "A_d", "C_r", "A_C", "C_A"])
    A, C = r * r * PI, 2 * r * PI
    if kind == "A_r":
        return Problem(
            stem=choose(rng,
                        f"A circle has an area of {m(_pi_raw(A))} {_sqw(ab)}. What is the radius of the circle?",
                        f"The area of a circle is {m(_pi_raw(A))} {_sqw(ab)}. What is its radius?"),
            answer=Q(r), fmt=_u(dec, ab),
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
            answer=Q(r), fmt=_u(dec, ab),
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
                   (R(r * r, 2) * PI, "just halves the area"),
                   (2 * r * r * PI, "doubles the area instead of finding the circumference")],
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
               (2 * r * r * PI, r"doubles $r^2$ instead of using $\pi r^2$")],
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
        stem=stem, answer=Q(2 * r), fmt=_u(dec, ab),
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
    ab = rng.choice(["in", "ft", "cm", "m"])
    shape = rng.choice(["semi", "quarter"])
    if lvl == 2:   # areas
        if shape == "semi":
            r = rng.choice([2, 4, 6, 8, 10])
            d = 2 * r
            ans = R(r * r, 2) * PI
            return Problem(
                stem=f"The figure shows a semicircle with a diameter of {m(d)} {_w(ab)}. What is the area of the semicircle?",
                figure=_fig_semi(_lab(d, ab)),
                answer=ans, fmt=_pi_u(ab, 2), near=_pi_near(ans),
                wrong=[(r * r * PI, "finds the area of the whole circle and forgets to take half"),
                       (R(d * d, 2) * PI, "uses the diameter in place of the radius"),
                       (r * PI, "finds the length of the curved edge, not the area"),
                       (R(r * r, 4) * PI, "takes one fourth of the circle instead of one half")],
                steps=[f"The radius is half the diameter: {m(f'r = {d} \\div 2 = {r}')} {_w(ab)}.",
                       f"A whole circle with this radius has area {m(rf'\pi \times {r}^2 = {_pi_raw(r * r * PI)}')}.",
                       f"A semicircle is half of a circle: {m(rf'{_pi_raw(r * r * PI)} \div 2 = {_pi_raw(ans)}')} {_sqw(ab)}."],
                check=PI * Q(d)**2 / 8,
            )
        r = rng.choice([2, 4, 6, 8, 10, 12])
        ans = R(r * r, 4) * PI
        return Problem(
            stem=f"The figure shows a quarter circle with a radius of {m(r)} {_w(ab)}. What is the area of the figure?",
            figure=_fig_quarter(_lab(r, ab)),
            answer=ans, fmt=_pi_u(ab, 2), near=_pi_near(ans),
            wrong=[(r * r * PI, "finds the area of the whole circle"),
                   (R(r * r, 2) * PI, "takes half of the circle instead of one fourth"),
                   (R(r, 2) * PI, "finds the length of the curved edge, not the area"),
                   (r * PI, "forgets to square the radius")],
            steps=[f"A whole circle with radius {m(r)} has area {m(rf'\pi \times {r}^2 = {_pi_raw(r * r * PI)}')}.",
                   f"A quarter circle is one fourth of it: {m(rf'{_pi_raw(r * r * PI)} \div 4 = {_pi_raw(ans)}')} {_sqw(ab)}."],
            check=PI * Q(r)**2 / 4,
        )
    # level 3: perimeters
    if shape == "semi":
        r = rng.randint(3, 12)
        d = 2 * r
        arc = r * PI
        ans = arc + d
        return Problem(
            stem=f"The figure shows a semicircular region with a diameter of {m(d)} {_w(ab)}. "
                 f"What is the perimeter of the region?",
            figure=_fig_semi(_lab(d, ab)),
            answer=ans, fmt=_pi_u(ab), near=_pi_near(ans),
            wrong=[(arc, "forgets the straight edge (the diameter)"),
                   (d * PI + d, "uses the whole circumference instead of half of it"),
                   (arc + r, "adds the radius instead of the diameter"),
                   (R(r * r, 2) * PI, "finds the area, not the perimeter")],
            steps=[f"The perimeter has two parts: the curved edge and the straight edge (the diameter, {m(d)} {_w(ab)}).",
                   f"The curved edge is half of the circumference: {m(rf'\frac{{1}}{{2}} \times \pi \times {d} = {_pi_raw(arc)}')} {_w(ab)}.",
                   f"Add the straight edge: the perimeter is {m(_pi_raw(ans))} {_w(ab)}."],
            check=PI * Q(d) / 2 + 2 * r,
        )
    r = rng.choice([2, 4, 6, 8, 10, 12])
    arc = R(r, 2) * PI
    ans = arc + 2 * r
    return Problem(
        stem=f"The figure shows a quarter-circle region with a radius of {m(r)} {_w(ab)}. "
             f"What is the perimeter of the region?",
        figure=_fig_quarter(_lab(r, ab)),
        answer=ans, fmt=_pi_u(ab), near=_pi_near(ans),
        wrong=[(arc, "forgets the two straight edges (the radii)"),
               (arc + r, "adds only one of the two straight edges"),
               (r * PI + 2 * r, "uses half of the circumference instead of one fourth"),
               (2 * r * PI + 2 * r, "uses the whole circumference instead of one fourth")],
        steps=[f"The perimeter is the curved edge plus two straight edges, each a radius ({m(r)} {_w(ab)}).",
               f"The curved edge is one fourth of the circumference: "
               f"{m(rf'\frac{{1}}{{4}} \times 2\pi \times {r} = {_pi_raw(arc)}')} {_w(ab)}.",
               f"Add the straight edges: {m(f'{r} + {r} = {2 * r}')}, so the perimeter is {m(_pi_raw(ans))} {_w(ab)}."],
        check=2 * PI * Q(r) / 4 + r + r,
    )


def _fig_ring(Rr, r, lab_R, lab_r):
    Rd = 1.6
    rd = round(Rd * r / Rr, 2)
    return (rf"\fill[black!20, even odd rule] (0,0) circle ({Rd}) (0,0) circle ({rd});" "\n"
            rf"\draw[thick] (0,0) circle ({Rd});" "\n"
            rf"\draw[thick] (0,0) circle ({rd});" "\n"
            r"\fill (0,0) circle (1.2pt);" "\n"
            rf"\draw (0,0) -- (35:{Rd});" "\n"
            rf"\node[fill=black!20, inner sep=1pt] at (35:{round((Rd + rd) / 2 + 0.05, 2)}) {{\small {lab_R}}};" "\n"
            rf"\draw (0,0) -- (180:{rd});" "\n"
            rf"\node[above] at (180:{round(rd / 2, 2)}) {{\small {lab_r}}};")


@template("MK")
def annulus(rng, lvl):
    kind = rng.choice(["fig", "fig", "walk"])
    if kind == "fig":
        Rr = rng.randint(4, 10)
        r = rng.randint(2, Rr - 1)
        need(r * 4 >= Rr)
        ans = (Rr * Rr - r * r) * PI
        ab = rng.choice(["in", "cm", "ft"])
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
    r = rng.randint(3, 10)
    wd = rng.randint(1, 4)
    need(wd < r)
    Rr = r + wd
    ans = (Rr * Rr - r * r) * PI
    thing, path = rng.choice([("fountain", "brick walkway"), ("pond", "gravel path"),
                              ("flower bed", "border of paving stones"),
                              ("flagpole base on the parade field", "concrete walkway")])
    return Problem(
        stem=(f"A circular {thing} has a radius of {m(r)} feet. A {path} {m(wd)} "
              f"{'foot' if wd == 1 else 'feet'} wide is built all the way around it. "
              f"What is the area of the {path.split(' of ')[0] if ' of ' in path else path}?"),
        answer=ans, fmt=_pi_u("ft", 2), near=_pi_near(ans),
        wrong=[(((r + 2 * wd)**2 - r * r) * PI, "adds the width twice when finding the outer radius"),
               (wd * wd * PI, "uses the width of the path as a radius"),
               (Rr * Rr * PI, f"includes the {thing} itself"),
               ((Rr * Rr + r * r) * PI, "adds the two circle areas instead of subtracting")],
        steps=[f"The path and the {thing} together form a large circle with radius "
               f"{m(f'{r} + {wd} = {Rr}')} feet.",
               f"Large circle: {m(rf'\pi \times {Rr}^2 = {_pi_raw(Rr * Rr * PI)}')}. "
               f"The {thing}: {m(rf'\pi \times {r}^2 = {_pi_raw(r * r * PI)}')}.",
               f"The path is the difference: {m(rf'{_pi_raw(Rr * Rr * PI)} - {_pi_raw(r * r * PI)} = {_pi_raw(ans)}')} square feet."],
        check=PI * ((r + wd)**2 - r**2),
    )


@template("MK")
def scale_circle(rng, lvl):
    kind = rng.choice(["area", "area", "circ", "half", "pizza", "new_area"])
    words = {2: "doubled", 3: "tripled", 4: "multiplied by 4", 5: "multiplied by 5"}
    if kind == "area":
        k = rng.choice([2, 3, 4, 5])
        part = rng.choice(["radius", "diameter"])
        return Problem(
            stem=f"If the {part} of a circle is {words[k]}, the area of the circle is multiplied by what number?",
            answer=Q(k * k), fmt=num,
            wrong=[(Q(k), f"assumes the area grows by the same factor as the {part}"),
                   (Q(2 * k), "doubles the factor instead of squaring it"),
                   (Q(k**3), "cubes the factor; that is how volume grows")],
            steps=[f"Area depends on the radius \\emph{{squared}}: {m(r'A = \pi r^2')}. "
                   f"(Multiplying the diameter by {m(k)} multiplies the radius by {m(k)} too.)" if part == "diameter" else
                   f"Area depends on the radius \\emph{{squared}}: {m(r'A = \pi r^2')}.",
                   f"Replace {m('r')} with {m(f'{k}r')}: {m(rf'\pi ({k}r)^2 = {k * k}\pi r^2')}.",
                   f"So the area is multiplied by {m(f'{k}^2 = {k * k}')}."],
            check=sp.expand(PI * (k * x)**2) / (PI * x**2),
        )
    if kind == "circ":
        k = rng.choice([2, 3, 4, 5])
        part = rng.choice(["radius", "diameter"])
        return Problem(
            stem=f"If the {part} of a circle is {words[k]}, the circumference of the circle is multiplied by what number?",
            answer=Q(k), fmt=num,
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
            answer=R(1, k * k), fmt=frac,
            wrong=[(R(1, k), "assumes the area shrinks by the same factor as the radius"),
                   (R(1, k**3), "cubes the factor; that is how volume changes"),
                   (R(1, 2 * k), "doubles the factor instead of squaring it")],
            steps=[f"The new radius is {m(rf'\frac{{1}}{{{k}}}r')}.",
                   f"New area: {m(rf'\pi \left(\frac{{1}}{{{k}}}r\right)^2 = \frac{{1}}{{{k * k}}}\pi r^2')}.",
                   f"So the new area is {m(F(1, k * k))} of the original."],
            check=(PI * (x / k)**2) / (PI * x**2),
        )
    if kind == "pizza":
        small, k = rng.choice([(6, 2), (7, 2), (8, 2), (6, 3), (5, 3), (4, 3), (4, 4)])
        big = small * k
        need(big <= 20)
        return Problem(
            stem=(f"A pizza shop sells a small pizza with a diameter of {m(small)} inches and a large pizza "
                  f"with a diameter of {m(big)} inches. The area of the large pizza is how many times the "
                  f"area of the small pizza?"),
            answer=Q(k * k), fmt=num,
            wrong=[(Q(k), "compares the diameters instead of the areas"),
                   (Q(2 * k), "doubles the ratio instead of squaring it"),
                   (Q(k**3), "cubes the ratio")],
            steps=[f"Radii: small {m(f'{small} \\div 2 = {dec_raw(R(small, 2))}')}, large {m(f'{big} \\div 2 = {dec_raw(R(big, 2))}')} inches.",
                   f"Areas: small {m(rf'\pi \times {dec_raw(R(small, 2))}^2 = {_pi_raw(R(small * small, 4) * PI)}')}, "
                   f"large {m(rf'\pi \times {dec_raw(R(big, 2))}^2 = {_pi_raw(R(big * big, 4) * PI)}')}.",
                   f"Divide: {m(rf'{_pi_raw(R(big * big, 4) * PI)} \div {_pi_raw(R(small * small, 4) * PI)} = {k * k}')}."],
            tip=f"The diameter is {m(k)} times as large, so the area is {m(f'{k}^2 = {k * k}')} times as large.",
            check=Q(big)**2 / small**2,
        )
    # new_area
    k = rng.choice([2, 3])
    a0 = rng.choice([2, 3, 4, 5, 6, 7, 8, 10])
    A0 = a0 * PI
    ans = k * k * A0
    return Problem(
        stem=(f"A circle has an area of {m(_pi_raw(A0))} square inches. If the radius of the circle is "
              f"{words[k]}, what is the area of the new circle?"),
        answer=ans, fmt=_pi_u("in", 2), near=_pi_near(ans),
        wrong=[(k * A0, f"multiplies the area by {m(k)} instead of by {m(k * k)}"),
               (k**3 * A0, f"multiplies the area by {m(k**3)}"),
               (a0 * a0 * PI if a0 * a0 != k * k * a0 else (a0 + k) * PI, "squares the old area instead of the factor")],
        steps=[f"When the radius is multiplied by {m(k)}, the area is multiplied by {m(f'{k}^2 = {k * k}')}.",
               f"New area: {m(rf'{k * k} \times {_pi_raw(A0)} = {_pi_raw(ans)}')} square inches."],
        check=PI * (k * sp.sqrt(a0))**2,
    )


# shaded regions -------------------------------------------------------------

def _fig_sq_circle(s):
    S = 2.6
    h = S / 2
    return (rf"\fill[black!20] (0,0) rectangle ({S},{S});" "\n"
            rf"\fill[white] ({h},{h}) circle ({h});" "\n"
            rf"\draw[thick] (0,0) rectangle ({S},{S});" "\n"
            rf"\draw[thick] ({h},{h}) circle ({h});" "\n"
            rf"\node[below] at ({h},0) {{\small {_lab(s)}}};")


def _fig_sq_quarter(s):
    S = 2.6
    return (rf"\fill[black!20] (0,0) rectangle ({S},{S});" "\n"
            rf"\fill[white] (0,0) -- ({S},0) arc (0:90:{S}) -- cycle;" "\n"
            rf"\draw[thick] (0,0) rectangle ({S},{S});" "\n"
            rf"\draw[thick] ({S},0) arc (0:90:{S});" "\n"
            rf"\node[below] at ({S / 2},0) {{\small {_lab(s)}}};")


def _fig_stadium(L, r):
    Ld = 2.8
    Hd = Ld * 2 * r / L
    scaled = True
    if Hd < 0.9 or Hd > 2.0:
        Hd = min(max(Hd, 0.9), 2.0)
        scaled = False
    Hd = round(Hd, 2)
    h = round(Hd / 2, 3)
    fig = (rf"\fill[black!20] (0,0) -- ({Ld},0) arc (-90:90:{h}) -- (0,{Hd}) arc (90:270:{h}) -- cycle;" "\n"
           rf"\draw[thick] (0,0) -- ({Ld},0) arc (-90:90:{h}) -- (0,{Hd}) arc (90:270:{h}) -- cycle;" "\n"
           rf"\draw[dashed] (0,0) -- (0,{Hd});" "\n"
           rf"\draw[dashed] ({Ld},0) -- ({Ld},{Hd});" "\n"
           rf"\node[above] at ({Ld / 2},{Hd}) {{\small {_lab(L)}}};" "\n"
           rf"\node[left] at ({Ld},{h}) {{\small {_lab(2 * r)}}};")
    return fig, scaled


@template("MK")
def shaded_region(rng, lvl):
    kind = rng.choice(["inscribed", "quarter", "stadium"])
    if kind == "inscribed":
        s = rng.choice([4, 6, 8, 10, 12, 14, 16, 20])
        r = s // 2
        circ = r * r * PI
        ans = s * s - circ
        return Problem(
            stem=(f"In the figure, a circle fits exactly inside a square with sides of length {m(s)}, "
                  f"touching all four sides. What is the area of the shaded region?"),
            figure=_fig_sq_circle(s),
            answer=ans, fmt=pifmt, near=_pi_near(ans),
            wrong=[(circ, "finds the area of the circle, not the shaded corners"),
                   (s * s - s * PI, "subtracts the circumference instead of the area of the circle"),
                   (s * s - r * PI, "forgets to square the radius"),
                   (Q(s * s), "finds the area of the square only")],
            steps=[f"The circle touches all four sides, so its diameter equals the side of the square: "
                   f"{m(f'd = {s}')}, so {m(f'r = {r}')}.",
                   f"Square: {m(f'{s}^2 = {s * s}')}. Circle: {m(rf'\pi \times {r}^2 = {_pi_raw(circ)}')}.",
                   f"Shaded region = square {m('-')} circle {m('= ' + _pi_raw(ans))}."],
            tip=f"Sense check: {m(_pi_raw(circ))} is a bit more than {m(3 * r * r)}, so the shaded corners are a small part of {m(s * s)}, just as the figure shows.",
            check=Q(s)**2 * (1 - PI / 4),
        )
    if kind == "quarter":
        s = rng.choice([4, 6, 8, 10, 12])
        qa = R(s * s, 4) * PI
        ans = s * s - qa
        return Problem(
            stem=(f"The figure shows a square with sides of length {m(s)}. A quarter circle is drawn inside it "
                  f"with its center at the lower-left corner of the square and a radius of {m(s)}. "
                  f"What is the area of the shaded region?"),
            figure=_fig_sq_quarter(s),
            answer=ans, fmt=pifmt, near=_pi_near(ans),
            wrong=[(qa, "finds the area of the quarter circle, not the shaded region"),
                   (s * s - R(s, 2) * PI, "subtracts the length of the arc instead of the area"),
                   (s * s - R(s, 4) * PI, "forgets to square the radius"),
                   (s * s + qa, "adds the quarter circle instead of subtracting it")],
            steps=[f"Square: {m(f'{s}^2 = {s * s}')}.",
                   f"Quarter circle with radius {m(s)}: {m(rf'\frac{{1}}{{4}} \times \pi \times {s}^2 = {_pi_raw(qa)}')}.",
                   f"Shaded region = square {m('-')} quarter circle {m('= ' + _pi_raw(ans))}."],
            check=Q(s)**2 - PI * s**2 / 4,
        )
    r = rng.randint(2, 6)
    L = rng.choice(range(6, 21, 2))
    need(L > 2 * r)
    rect = L * 2 * r
    circ = r * r * PI
    ans = rect + circ
    fig, scaled = _fig_stadium(L, r)
    return Problem(
        stem=(f"The figure is made of a rectangle that is {m(L)} meters long and {m(2 * r)} meters wide, "
              f"with a semicircle attached to each end. What is the area of the whole figure, in square meters?"
              + ("" if scaled else " (Figure not drawn to scale.)")),
        figure=fig,
        answer=ans, fmt=pifmt, near=_pi_near(ans),
        wrong=[(rect + 2 * circ, "counts each semicircle as a whole circle"),
               (rect + circ / 2, "includes only one of the two semicircles"),
               (rect + 4 * circ, "uses the diameter of the semicircles as the radius"),
               (Q(rect), "leaves out the semicircles")],
        steps=[f"Rectangle: {m(f'{L} \\times {2 * r} = {rect}')} square meters.",
               f"Each semicircle has diameter {m(2 * r)}, so radius {m(r)}. The two semicircles together make one whole "
               f"circle: {m(rf'\pi \times {r}^2 = {_pi_raw(circ)}')}.",
               f"Total area: {m(_pi_raw(ans))} square meters."],
        check=Q(L) * 2 * r + 2 * (PI * r**2 / 2),
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
        lines.append(rf"\node[anchor={'south' if theta <= 120 else 'east'}] at ({theta}:{Rd + 0.05}) {{\small $B$}};")
    lines.append(r"\fill (0,0) circle (1.2pt);")
    lines.append(r"\draw (0.28,0) arc (0:" + str(theta) + ":0.28);")
    lines.append(rf"\node at ({theta / 2}:{0.62 if theta >= 60 else 0.78}) {{\scriptsize ${theta}^\circ$}};")
    lines.append(rf"\node[below] at ({Rd / 2},0) {{\small {r_lab}}};")
    return "\n".join(lines)


@template("MK")
def arc_sector(rng, lvl):
    kind = rng.choice(["area", "area", "arc", "arc", "sprinkler", "slice"])
    if kind == "sprinkler":
        theta = rng.choice([90, 120, 180, 60])
        r = rng.choice([6, 8, 10, 12, 15, 18, 20, 24, 30])
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
        d = rng.choice([12, 14, 16, 18, 20])
        k = rng.choice([4, 6, 8])
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
    theta = rng.choice([45, 60, 72, 90, 120, 135, 150, 240, 270, 300])
    r = rng.randint(2, 15)
    frac_ = R(theta, 360)
    full_A, full_C = r * r * PI, 2 * r * PI
    if kind == "area":
        ans = frac_ * full_A
        need(ans.coeff(PI).is_integer and r * r >= frac_.q)
        return Problem(
            stem=(f"In the circle shown, the radius is {m(r)} and the shaded sector has a central angle of "
                  f"{m(f'{theta}^\\circ')}. What is the area of the shaded sector?"),
            figure=_fig_sector(theta, _lab(r), "area"),
            answer=ans, fmt=pifmt, near=_pi_near(ans),
            wrong=[(full_A, "finds the area of the whole circle"),
                   (frac_ * full_C, "finds the arc length, not the area"),
                   (R(360 - theta, 360) * full_A, "finds the unshaded part of the circle"),
                   (R(theta, 180) * full_A if theta < 180 else R(theta, 90) * r * PI,
                    r"divides the angle by $180^\circ$ instead of $360^\circ$" if theta < 180 else None)],
            steps=[f"The sector is {m(F(theta, 360) + ' = ' + frac_raw(frac_))} of the whole circle.",
                   f"Whole circle: {m(rf'\pi \times {r}^2 = {_pi_raw(full_A)}')}.",
                   f"Sector: {m(rf'{frac_raw(frac_)} \times {_pi_raw(full_A)} = {_pi_raw(ans)}')}."],
            check=PI * r**2 * theta / 360,
        )
    ans = frac_ * full_C
    need(ans.coeff(PI).is_integer and theta < 360)
    return Problem(
        stem=(f"In the circle shown, the radius is {m(r)} and the central angle is {m(f'{theta}^\\circ')}. "
              f"What is the length of the arc from {m('A')} to {m('B')} shown in bold?"),
        figure=_fig_sector(theta, _lab(r), "arc"),
        answer=ans, fmt=pifmt, near=_pi_near(ans),
        wrong=[(full_C, "finds the circumference of the whole circle"),
               (frac_ * full_A, "finds the area of the sector, not the arc length"),
               (frac_ * r * PI, r"uses $\pi r$ instead of $2\pi r$ for the circumference"),
               (R(360 - theta, 360) * full_C, "finds the length of the other arc")],
        steps=[f"The arc is {m(F(theta, 360) + ' = ' + frac_raw(frac_))} of the whole circle.",
               f"Circumference: {m(rf'2\pi \times {r} = {_pi_raw(full_C)}')}.",
               f"Arc length: {m(rf'{frac_raw(frac_)} \times {_pi_raw(full_C)} = {_pi_raw(ans)}')}."],
        check=PI * 2 * r * theta / 360,
    )


@template("AR")
def wheel(rng, lvl):
    kind = rng.choice(["dist", "dist", "revs", "mile"])
    p = person(rng)
    if kind == "dist":
        thing, d = rng.choice([(f"The front wheel of {p.name}'s bicycle", 28),
                               ("A wheelbarrow wheel", 14), ("A Humvee tire", 35),
                               ("A tractor's front wheel", 42), ("A trailer wheel", 21)])
        C = R(22, 7) * d
        n_ = rng.choice([10, 12, 15, 20, 24, 30, 36, 40, 45, 50, 60, 100])
        tot_in = C * n_
        need(tot_in % 12 == 0)
        ans = tot_in / 12
        return Problem(
            stem=(f"{thing} has a diameter of {m(d)} inches. How many feet does it roll in "
                  f"{m(n_)} complete turns? Use {m(F(22, 7))} for {m(r'\pi')}."),
            answer=ans, fmt=_u(dec, "ft"),
            wrong=[(ans / 2, "uses the radius instead of the diameter"),
                   (tot_in, "forgets to convert inches to feet"),
                   (2 * ans, r"uses the diameter in $2\pi r$"),
                   (R(22, 7) * R(d, 2)**2 * n_ / 12, "uses the area of the wheel instead of its circumference")],
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
        thing = rng.choice(["a garden cart", "a supply cart", "a hand truck", "a hose reel cart"])
        return Problem(
            stem=(f"The wheels of {thing} have a diameter of {m(d)} {'foot' if d == 1 else 'feet'}. "
                  f"How many complete turns does each wheel make when the cart is pushed {num(dist)} feet? "
                  f"Use 3.14 for {m(r'\pi')}."),
            answer=Q(n_), fmt=num,
            wrong=[(Q(2 * n_), "uses the radius instead of the diameter"),
                   (dist / d, "divides the distance by the diameter instead of the circumference"),
                   (R(n_, 2), r"uses the diameter in $2\pi r$")],
            steps=[f"One turn moves the cart one circumference: {m('C = \\pi d \\approx ' + _times_pi(R(314, 100), d))} feet.",
                   f"Number of turns {m('=')} distance {m(r'\div')} circumference: {m(f'{int_raw(dist)} \\div {dec_raw(C)} = {n_}')}."],
            tip=f"Move the decimal point to divide by a whole number: {m(f'{int_raw(dist)} \\div {dec_raw(C)} = {int_raw(dist * 100)} \\div {int_raw(C * 100)}')}.",
            verify=lambda v: v * C == dist,
        )
    # revolutions in a mile
    d, Cft = rng.choice([(42, 11), (21, R(11, 2))])
    half = rng.random() < 0.4
    feet = 2640 if half else 5280
    ans = feet / Q(Cft)
    thing = rng.choice([f"{p.name}'s truck tire", "a military truck's tire", "a tractor wheel"])
    return Problem(
        stem=(f"The diameter of {thing} is {m(d)} inches. About how many complete turns does the tire make "
              f"in {'half a mile' if half else '1 mile'}? (1 mile {m('=')} {num(5280)} feet; use {m(F(22, 7))} for {m(r'\pi')}.)"),
        answer=ans, fmt=num,
        wrong=[(2 * ans, "uses the radius instead of the diameter"),
               (ans / 12, "forgets to convert the circumference from inches to feet"),
               (ans / 2, r"uses the diameter in $2\pi r$"),
               (Q(feet) / d * 12, "divides by the diameter instead of the circumference")],
        steps=[f"One turn covers one circumference: {m('C = \\pi d \\approx ' + _times_pi(R(22, 7), d))} inches.",
               f"Change to feet: {m(f'{int_raw(R(22, 7) * d)} \\div 12 = {dec_raw(Cft)}')} feet.",
               f"Turns {m('=')} distance {m(r'\div')} circumference: {m(f'{int_raw(feet)} \\div {dec_raw(Cft)} = {int_raw(ans)}')}."],
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
