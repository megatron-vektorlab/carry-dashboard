"""Kindle eBook: reflowable EPUB 3 with MathML equations.

    python3 -m asvab.ebook     # -> output/ASVAB-Math-Workbook-ebook.epub
                               #    output/ASVAB-Math-Workbook-ebook-cover.jpg

The same 1,000 problems as the paperback (same SEED, same generator), laid out
for a reading device instead of paper:

* equations are MathML (Amazon's Kindle Publishing Guidelines recommend MathML
  for mathematical content; Enhanced Typesetting renders it), converted from the
  book's LaTeX by pandoc;
* TikZ figures are rendered by pdflatex to 300 ppi greyscale PNGs;
* every problem number links to its solution (one way only: a link back would make Kindle
  show the pair as a footnote pop-up, KPG 7.1; readers return with Back); answer keys link to
  solutions, test keys to the teaching chapter;
* no answer sheets or progress tracker (nothing can be written on a Kindle).

Needs pandoc (3.x), pdflatex with the paperback's packages, pdftoppm, and
`pip install epubcheck` (Java) for the final check.
"""
from __future__ import annotations

import datetime
import hashlib
import html
import re
import subprocess
import sys
import uuid

from PIL import Image

from . import config
from .build import (AR_TEST, MK_TEST, N_TESTS, PART_BLURB, PARTS, TEX, diag_minutes, fdp_table, generate_all,
                    squares_table)
from .epubkit import Book, Doc, check
from .generate import load_chapters
from .glossary import GLOSSARY
from .render import BUILD, LETTERS, ROOT, SECTION_NAMES, preamble

OUT = ROOT / "output"
EB = BUILD / "ebook"
EPUB = OUT / "ASVAB-Math-Workbook-ebook.epub"
COVER = OUT / "ASVAB-Math-Workbook-ebook-cover.jpg"
FIG_PPI = 600           # >= 300 ppi even for the smallest figure at its displayed size
TEXT_W_IN = 4.2         # figure width (in) that fills the text column on a Kindle

CSS = """
body { margin: 0; }
h1 { font-size: 1.45em; line-height: 1.2em; margin: 0.6em 0 0.5em; page-break-before: always; text-align: left; }
h2 { font-size: 1.2em; line-height: 1.25em; margin: 1.3em 0 0.4em; page-break-after: avoid; text-align: left; }
h3 { font-size: 1.05em; margin: 1em 0 0.3em; page-break-after: avoid; text-align: left; }
p { margin: 0.35em 0; text-indent: 0; }
.center { text-align: center; }
.title-page h1 { page-break-before: avoid; font-size: 2.2em; margin: 1.6em 0 0.2em; text-align: center; }
.title-page p { text-align: center; margin: 0.5em 0; }
.title-page .sub { font-size: 1.2em; }
.small { font-size: 0.85em; }
.meta { font-size: 0.9em; }
.copyright p { font-size: 0.85em; margin: 0.6em 0; }
.toc p { margin: 0.3em 0; }
.toc .l2 { margin-left: 4%; }
.concept, .trap { border: 1px solid; padding: 0.3em 2%; margin: 0.9em 0; }
.example, .tip, .infobox { border-left: 3px solid #888888; padding: 0.2em 0 0.2em 3%; margin: 0.9em 0; }
.boxtitle { font-weight: bold; margin: 0.1em 0 0.3em; }
.boxtitle p { margin: 0; }
table { border-collapse: collapse; margin: 0.6em 0; }
td, th { border: 1px solid #888888; padding: 0.15em 0.4em; vertical-align: top; }
td.l, th.l { text-align: left; }
td.c, th.c { text-align: center; }
td.r, th.r { text-align: right; }
.prob { margin: 1.2em 0 0.6em; }
.prob .stem { margin-bottom: 0.35em; }
.pn { font-weight: bold; }
.opt { margin: 0.25em 0 0.25em 5%; padding-left: 1.4em; text-indent: -1.4em; }
.ol { font-weight: bold; }
.fig { text-align: center; margin: 0.5em 0; }
.sol { margin: 1.1em 0 0.5em; }
.sh { margin-bottom: 0.25em; }
.key { font-weight: bold; border: 1px solid; padding: 0 0.3em; }
.step { margin: 0.2em 0 0.2em 4%; padding-left: 1.2em; text-indent: -1.2em; }
.sn { font-weight: bold; }
.tipl, .why { margin: 0.3em 0 0.3em 3%; font-size: 0.95em; }
.lbl { font-weight: bold; font-size: 0.85em; letter-spacing: 0.04em; }
.keys { line-height: 1.7em; }
.next { margin-top: 1.4em; font-weight: bold; }
.nw { white-space: nowrap; }
.dm { margin: 0.3em 0; }
.al mtd { padding-left: 0; padding-right: 0; }
"""


# ------------------------------------------------------------------ LaTeX -> XHTML
def env_arg(s: str, i: int) -> tuple[str, int]:
    """The brace group starting at s[i] ('{'); returns (content, index after it)."""
    assert s[i] == "{", s[i:i + 30]
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "\\":
            continue
        if s[j] == "{" and s[j - 1] != "\\":
            depth += 1
        elif s[j] == "}" and s[j - 1] != "\\":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
    raise ValueError("unbalanced braces: " + s[i:i + 60])


MATH_RE = re.compile(r"(\\\[.*?\\\]|(?<!\\)\$.+?(?<!\\)\$)", re.S)
PHONE_WIDTH = 30        # inline math wider than this (in rough character widths) becomes a display


def top_level(tex: str, pattern: str) -> list[int]:
    """Start positions of `pattern` outside braces and LaTeX environments."""
    out, depth, env, i = [], 0, 0, 0
    rx = re.compile(pattern)
    while i < len(tex):
        if tex.startswith("\\begin{", i):
            env += 1
        elif tex.startswith("\\end{", i):
            env -= 1
        c = tex[i]
        if c == "\\" and i + 1 < len(tex) and not tex[i + 1].isalpha():
            i += 2          # \{ \} \, \$ ...
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif depth == 0 and env == 0:
            m = rx.match(tex, i)
            if m:
                out.append(i)
        i += 1
    return out


def brace_group(t: str, i: int) -> tuple[str, int]:
    depth = 0
    for j in range(i, len(t)):
        if t[j] == "{" and t[j - 1] != "\\":
            depth += 1
        elif t[j] == "}" and t[j - 1] != "\\":
            depth -= 1
            if depth == 0:
                return t[i + 1:j], j + 1
    return t[i + 1:], len(t)


def vis_len(t: str) -> float:
    """Rough rendered width of a TeX formula in character widths (fractions stack)."""
    w, i = 0.0, 0
    while i < len(t):
        m = re.match(r"\\[dt]?frac\s*", t[i:])
        if m and i + m.end() < len(t) and t[i + m.end()] == "{":
            a, i = brace_group(t, i + m.end())
            b, i = brace_group(t, i) if i < len(t) and t[i] == "{" else ("", i)
            w += max(vis_len(a), vis_len(b)) + 0.5
            continue
        m = re.match(r"\\(text|mathrm)\s*", t[i:])
        if m and i + m.end() < len(t) and t[i + m.end()] == "{":
            a, i = brace_group(t, i + m.end())
            w += 0.9 * len(a)
            continue
        m = re.match(r"\\[a-zA-Z]+|\\.", t[i:])
        if m:
            name = m.group(0)
            i += len(name)
            if name not in ("\\left", "\\right", "\\,", "\\;", "\\!", "\\ "):
                w += 1.6 if name in ("\\times", "\\div", "\\cdot", "\\le", "\\ge", "\\approx", "\\Rightarrow", "\\to") else 1
            continue
        c = t[i]
        i += 1
        if c not in "{}^_ ":
            w += 1.8 if c in "=+-<>" else 1
    return w


ROW_MAX = 30            # widest row of a broken equation (same units as vis_len)
CELL_MAX = 18           # widest formula piece inside a table cell


def eq_parts(tex: str) -> list[str]:
    """tex split at its top-level '=' signs (none inside braces or environments)."""
    cuts = top_level(tex, r"=")
    parts, last = [], 0
    for c in cuts:
        parts.append(tex[last:c].strip())
        last = c + 1
    parts.append(tex[last:].strip())
    return parts


def eq_rows(tex: str) -> list[str]:
    """Rows for an aligned display: 'lhs &= a', '&= b', ... ; the left side gets a row of its own
    when 'lhs = a' would not fit a phone screen."""
    parts = eq_parts(tex)
    if len(parts) == 1:
        return [tex]
    if vis_len(parts[0]) + vis_len(parts[1]) + 2 <= ROW_MAX:
        rows = [f"{parts[0]} &= {parts[1]}"]
    else:
        rows = [f"& {parts[0]}", f"&= {parts[1]}"]
    return rows + [f"&= {x}" for x in parts[2:]]


def aligned(rows: list[str], tail: str = "") -> str:
    rows = list(rows)
    rows[-1] += tail
    if len(rows) == 1 and "&" not in rows[0]:
        return f"\\[ {rows[0]} \\]"
    return "\\[ \\begin{aligned} " + " \\\\ ".join(rows) + " \\end{aligned} \\]"


def split_display(tex: str) -> str:
    """Make a display fit a phone: formulas joined by \\quad become rows of one aligned display
    (or separate displays when they are not all equations), and a long chain a = b = c gets one
    '=' per row. An arrow standing alone between two formulas starts the next one."""
    inner = tex[2:-2].strip()
    if "\\begin{" in inner and not top_level(inner, r"\\q?quad\b"):
        return tex
    cuts = top_level(inner, r"\\q?quad\b")
    pieces, last = [], 0
    for c in cuts:
        pieces.append(inner[last:c])
        last = c + (6 if inner.startswith("\\qquad", c) else 5)
    pieces.append(inner[last:])
    pieces = [x.strip() for x in pieces if x.strip()]
    merged = []
    for x in pieces:
        if merged and re.fullmatch(r"\\(Rightarrow|to|implies|Longrightarrow)", merged[-1]):
            merged[-1] = merged[-1] + " " + x
        else:
            merged.append(x)
    if len(merged) > 1 and all("\\begin{" not in x and len(eq_parts(x)) > 1 for x in merged):
        rows = []
        for x in merged:
            parts = eq_parts(x)
            first = f"{parts[0]} &= {parts[1]}"
            rows.append(first if vis_len(x) <= ROW_MAX else first)
            rows += [f"&= {y}" for y in parts[2:]]
        return aligned(rows)
    out = []
    for x in merged:
        out.append(aligned(eq_rows(x)) if "\\begin{" not in x and vis_len(x) > ROW_MAX else f"\\[ {x} \\]")
    return "\n".join(out)


def split_inline(body: str, limit: float) -> str:
    """A long inline chain becomes several inline formulas, each continuing with '=', so the
    line can wrap between them."""
    parts = eq_parts(body)
    if len(parts) == 1:
        return f"${body}$"
    chunks, cur = [], parts[0]
    for x in parts[1:]:
        if vis_len(cur) + vis_len(x) + 2 > limit:
            chunks.append(cur)
            cur = "= " + x
        else:
            cur += " = " + x
    chunks.append(cur)
    return " ".join(f"${c}$" for c in chunks)


TAIL_RE = re.compile(r"[ ]?([^$\\%&_#^{}~\n]{0,40}?[.;:!?])(\s*✓)?(?=\s|$)")


def text_quads(text: str) -> str:
    """Text-mode \\quad separates two items; HTML would collapse it to one space, so write "; "
    (after a comma, semicolon or period, or before a parenthesis, only a space). Column specs like
    @{\\qquad} stay. A control space "\\ " used as a separator becomes a normal space."""
    text = re.sub(r"([,;:.])\s*\\q?quad(?![a-zA-Z])\s*", r"\1 ", text)
    text = re.sub(r"\s*\\q?quad(?![a-zA-Z])\s*(?=\()", " ", text)
    text = re.sub(r"(?<!@\{)\s*\\q?quad(?![a-zA-Z])\s*", "; ", text)
    return re.sub(r"\s+\\ (?=\S)", " ", text)


def prep_math(s: str) -> str:
    """Math-aware rewrites so that formulas fit a phone screen: wide displays are split into
    rows, long inline chains become a display (at the end of a sentence) or several inline pieces;
    text-mode \\quad separators are made visible."""
    # a word directly before a formula that starts with a relation stays with it: "1 yard~$= 3$ feet"
    s = re.sub(r"(\w) \$(\s*(?:=|<|>|\\le\b|\\ge\b|\\approx\b|\\ne\b))", r"\1~$\2", s)
    # 30°-60°-90°, 5-12-13: one formula, so the line cannot break at a hyphen ("-90°")
    s = re.sub(r"\$([^$]+)\$-\$([^$]+)\$(?:-\$([^$]+)\$)?",
               lambda m: "$" + "\\text{-}".join(x for x in m.groups() if x) + "$", s)
    tables = [(t.start(), t.end()) for t in
              re.finditer(r"\\begin\{(tabular|tabularx|array)\}.*?\\end\{\1\}", s, flags=re.S)]
    out, last = [], 0
    for m in MATH_RE.finditer(s):
        if m.start() < last:
            continue
        in_table = any(a <= m.start() < b for a, b in tables)
        out.append(text_quads(s[last:m.start()]))
        tok = m.group(0)
        end = m.end()
        if tok.startswith("\\["):
            tok = split_display(tok)
        else:
            body = tok[1:-1]
            if in_table:
                if vis_len(body) > CELL_MAX:
                    tok = split_inline(body, CELL_MAX)
            elif vis_len(body) > PHONE_WIDTH:
                tail = TAIL_RE.match(s, end)
                rest = s[tail.end():].strip() if tail else ""
                if tail and len(tail.group(1).split()) <= 5:
                    words = (" " if tail.group(1)[0].isalnum() else "") + tail.group(1) + (" ✓" if tail.group(2) else "")
                    tok = "\n" + aligned(eq_rows(body), f"\\text{{{words}}}") + "\n"
                    end = tail.end()
                else:
                    tok = split_inline(body, ROW_MAX)
        tok = tok.replace("\\underline{\\ \\ }", "\\square")
        out.append(tok)
        last = end
    out.append(text_quads(s[last:]))
    return "".join(out)


def two_column_tables(s: str) -> str:
    """4-column 'rule | meaning | rule | meaning' tables become 2 columns (one pair per row): a
    phone screen has no room for four columns."""
    def fix(m):
        rows = [r.strip() for r in re.split(r"\\\\", m.group(2)) if r.strip()]
        out = []
        for r in rows:
            cells = [r[a:b].strip() for a, b in zip([0] + [c + 1 for c in top_level(r, "&")],
                                                     top_level(r, "&") + [len(r)])]
            if len(cells) == 4:
                out += [f"{cells[0]} & {cells[1]}", f"{cells[2]} & {cells[3]}"]
            else:
                out.append(r)
        return "\\begin{tabular}{ll}\n" + " \\\\\n".join(out) + " \\\\\n\\end{tabular}"
    return re.sub(r"\\begin\{tabular\}\{(@\{\}ll@\{\\qquad\}ll@\{\})\}(.*?)\\end\{tabular\}", fix, s, flags=re.S)


class Converter:
    """Collects LaTeX fragments and figures, converts them all in one pandoc run."""

    BOX_TITLES = {"tip": "No-Calculator Tip", "trap": "Common Traps"}

    def __init__(self):
        self.frags: dict[str, str] = {}
        self.figs: list[str] = []          # TikZ sources, index = figure number
        self.fig_index: dict[str, int] = {}
        self.html: dict[str, str] = {}

    # -- figures
    def fig_id(self, tikz: str) -> int:
        """Number of a TikZ figure (full tikzpicture environment); identical figures share one image."""
        body = tikz.strip()
        if not body.startswith(r"\begin{tikzpicture}"):
            body = r"\begin{tikzpicture}" + "\n" + body + "\n" + r"\end{tikzpicture}"
        h = hashlib.sha1(body.encode()).hexdigest()
        if h not in self.fig_index:
            self.fig_index[h] = len(self.figs)
            self.figs.append(body)
        return self.fig_index[h]

    def figure(self, tikz: str) -> str:
        return f"\n\nFIGPH{self.fig_id(tikz)}X\n\n"

    # -- preprocessing of the book's LaTeX for pandoc
    def prep(self, s: str) -> str:
        s = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", lambda m: self.figure(m.group(0)), s, flags=re.S)
        for env in ("concept", "example", "infobox"):
            while True:
                m = re.search(r"\\begin\{%s\}\s*\{" % env, s)
                if not m:
                    break
                title, end = env_arg(s, m.end() - 1)
                s = s[:m.start()] + f"\\begin{{{env}x}}\\begin{{boxtitle}}{title}\\end{{boxtitle}}\n" + s[end:]
            s = s.replace(f"\\end{{{env}}}", f"\\end{{{env}x}}")
        for env, title in self.BOX_TITLES.items():
            s = s.replace(f"\\begin{{{env}}}", f"\\begin{{{env}x}}\\begin{{boxtitle}}{title}\\end{{boxtitle}}\n")
            s = s.replace(f"\\end{{{env}}}", f"\\end{{{env}x}}")
        s = re.sub(r"\\begin\{tabularx\}\{[^}]*\}\{@\{\}>\{\\bfseries\}p\{[^}]*\}X@\{\}\}",
                   r"\\begin{boldfirst}\\begin{tabular}{ll}", s)
        s = s.replace("\\end{tabularx}", "\\end{tabular}\\end{boldfirst}")
        s = re.sub(r"\\begin\{(itemize|enumerate)\}\[[^\]]*\]", r"\\begin{\1}", s)
        s = re.sub(r"\\(begin|end)\{multicols\}(\{\d\})?", "", s)
        s = re.sub(r"\\begin\{minipage\}(\[[^\]]*\])?\{[^}]*\}", "", s)
        s = s.replace("\\end{minipage}", "")
        s = re.sub(r"\\footnote\{([^{}]*)\}", r" (\1)", s)
        for cmd in ("tcbset", "setlist", "color"):
            s = re.sub(r"\\%s\{[^{}]*(\{[^{}]*\}[^{}]*)*\}" % cmd, "", s)
        s = re.sub(r"\\renewcommand\{\\arraystretch\}\{[^}]*\}", "", s)
        s = re.sub(r"\\setlength\{\\[a-z]+\}\{[^}]*\}", "", s)
        s = re.sub(r"\\vspace\*?\{[^}]*\}", "", s)
        s = re.sub(r"\\\\\[[^\]]*\]", r"\\\\", s)
        s = re.sub(r"\\(columnbreak|hfill|smallskip|medskip|bigskip|small|sans|clearpage|noindent)\b", "", s)
        s = s.replace("\\checkmark", "✓")
        s = two_column_tables(s)
        s = prep_math(s)
        s = re.sub(r"\\begin\{array\}\{([rcl@{}\\;]+)\}",
                   lambda m: "\\begin{array}{" + re.sub(r"@\{[^}]*\}", "", m.group(1)) + "}", s)
        return s

    def add(self, key: str, latex: str) -> str:
        if key not in self.frags:
            self.frags[key] = self.prep(latex)
        return key

    # -- one pandoc run for everything
    def run(self):
        keys = list(self.frags)
        src = "".join(f"\n\nFRAGSEP{i}X\n\n{self.frags[k]}\n" for i, k in enumerate(keys)) + "\n\nFRAGSEPENDX\n"
        r = subprocess.run(["pandoc", "-f", "latex", "-t", "html5", "--mathml", "--wrap=none"],
                           input=src, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("pandoc failed: " + r.stderr[-2000:])
        parts = re.split(r"<p>FRAGSEP(\d+|END)X</p>", r.stdout)
        found = {}
        for i in range(1, len(parts) - 1, 2):
            if parts[i] != "END":
                found[int(parts[i])] = parts[i + 1]
        missing = [keys[i] for i in range(len(keys)) if i not in found]
        if missing:
            raise SystemExit(f"pandoc lost {len(missing)} fragments, e.g. {missing[:3]}")
        for i, k in enumerate(keys):
            self.html[k] = clean_html(found[i])

    def block(self, key: str) -> str:
        return self.html[key]

    def inline(self, key: str) -> str:
        h = self.html[key].strip()
        m = re.fullmatch(r"<p>(.*)</p>", h, flags=re.S)
        if m and "<p>" not in m.group(1):
            return m.group(1)
        return h


def math_clean(m: re.Match) -> str:
    """Drop pandoc's <semantics>/<annotation> wrapper; keep the TeX as alttext."""
    whole = m.group(0)
    tex = re.search(r'<annotation encoding="application/x-tex">(.*?)</annotation>', whole, flags=re.S)
    inner = re.sub(r"</?semantics>", "", whole)
    inner = re.sub(r'<annotation encoding="application/x-tex">.*?</annotation>', "", inner, flags=re.S)
    if tex:
        alt = html.unescape(tex.group(1)).strip()
        inner = inner.replace("<math ", f'<math alttext="{html.escape(alt, quote=True)}" ', 1)
    return inner


FENCE = re.compile(r'<mo stretchy="true" form="(prefix|postfix)">([^<]*)</mo>')


def fences(m: re.Match) -> str:
    """texmath makes every ( ) a stretchy fence; keep that only around fractions and roots.
    Plain parentheses get stretchy="false" and zero side spacing, like ( ) in LaTeX."""
    s = m.group(0)
    toks = list(FENCE.finditer(s))
    keep = set()
    stack = []
    for t in toks:
        if t.group(1) == "prefix":
            stack.append(t)
        elif stack:
            o = stack.pop()
            inner = s[o.end():t.start()]
            if "<mfrac" in inner or "<msqrt" in inner or "<mroot" in inner:
                keep |= {o.start(), t.start()}
    out, last = [], 0
    for t in toks:
        out.append(s[last:t.start()])
        if t.start() in keep:
            out.append(t.group(0))
        else:
            out.append(f'<mo stretchy="false" form="{t.group(1)}" lspace="0em" rspace="0em">{t.group(2)}</mo>')
        last = t.end()
    out.append(s[last:])
    return "".join(out)


UNARY_AFTER = set("([{,=+−×÷·<>≤≥≠≈→⇒:;±")
UNARY = re.compile(r'(<mo( [^>]*)?>([^<]*)</mo>|<mrow>|<mtd[^>]*>|<math [^>]*>)<mo>([−+])</mo>')


def unary(h: str) -> str:
    """A minus right after an opening bracket, a comma or another operator is a sign, not
    a subtraction (LaTeX knows this; MathML renderers need form="prefix")."""
    def rep(m):
        op, attrs = m.group(3), m.group(2) or ""
        if op is not None:
            op = html.unescape(op)          # pandoc writes < and > as &lt; &gt;
        if op is not None and op not in UNARY_AFTER and 'form="prefix"' not in attrs:
            return m.group(0)
        return f'{m.group(1)}<mo form="prefix">{m.group(4)}</mo>'
    while True:
        new = UNARY.sub(rep, h)
        if new == h:
            return h
        h = new


def digit_groups(m: re.Match) -> str:
    """1{,}080 and 11{:}50 are one number in TeX; texmath splits them into <mn>1</mn><mo>,</mo>...,
    and the comma (colon) then gets operator spacing: "1, 080", "11 : 50". Merge them back."""
    s = m.group(0)
    alt = html.unescape(re.search(r'alttext="([^"]*)"', s).group(1)) if "alttext=" in s else ""
    if "{,}" in alt:
        while True:
            new = re.sub(r"<mn>([0-9][0-9,]*)</mn><mo>,</mo>(<msup>|<msub>|<msubsup>)?<mn>([0-9]{3}(?:,[0-9]{3})*(?:\.[0-9]+)?)</mn>",
                         r"\2<mn>\1,\3</mn>", s)
            if new == s:
                break
            s = new
    if "{:}" in alt:
        s = re.sub(r"<mn>([0-9]{1,2})</mn><mo>:</mo><mn>([0-9]{2})</mn>", r"<mn>\1:\2</mn>", s)
    return s


def mfrac_style(s: str) -> str:
    """MathML 3 (the EPUB schema) has no displaystyle on <mfrac>: wrap the fraction in <mstyle>."""
    while True:
        m = re.search(r'<mfrac displaystyle="(true|false)">', s)
        if not m:
            return s
        depth, i = 0, m.start()
        for t in re.finditer(r"<mfrac\b[^>]*>|</mfrac>", s[m.start():]):
            depth += 1 if t.group(0).startswith("<mfrac") else -1
            if depth == 0:
                end = m.start() + t.end()
                break
        inner = "<mfrac>" + s[m.end():end]
        s = s[:i] + f'<mstyle displaystyle="{m.group(1)}">' + inner + "</mstyle>" + s[end:]


LEAD_OPS = "=<>≤≥≈≠×÷·→⇒"


def lead_op(m: re.Match) -> str:
    """A formula that starts with an operator ("1 yard $= 3$ feet") already has a word space in
    front of it: no extra space on the left. A formula that is only an operator gets none at all."""
    s = m.group(0)
    lone = re.fullmatch(r'(<math [^>]*>)(?:<mrow>)?<mo>([^<]*)</mo>(?:</mrow>)?</math>', s)
    if lone and html.unescape(lone.group(2)) in LEAD_OPS:
        return f'{lone.group(1)}<mo lspace="0em" rspace="0em">{lone.group(2)}</mo></math>'
    first = re.match(r'(<math [^>]*>(?:<mrow>)?)<mo>([^<]*)</mo>', s)
    if first and html.unescape(first.group(2)) in LEAD_OPS:
        return f'{first.group(1)}<mo form="infix" lspace="0em">{first.group(2)}</mo>' + s[first.end():]
    return s


def hline_rule(m: re.Match) -> str:
    """\\hline in an array (written-out elimination): rule above the last row. rowlines for
    MathML engines that know it, a border on the cells for those that follow CSS."""
    s = m.group(0)
    s = s.replace("<mtable>", '<mtable rowlines="none solid">', 1)
    k = s.rfind("<mtr>")
    def cell(t):
        attrs = t.group(1) or ""
        if 'style="' in attrs:
            attrs = attrs.replace('style="', 'style="border-top: 1px solid; ', 1)
        else:
            attrs += ' style="border-top: 1px solid"'
        return f"<mtd{attrs}>"
    tail = re.sub(r"<mtd( [^>]*)?>", cell, s[k:])
    return s[:k] + tail


def clean_html(h: str) -> str:
    h = re.sub(r"<math .*?</math>", math_clean, h, flags=re.S)
    h = re.sub(r"<math .*?</math>", fences, h, flags=re.S)
    h = unary(h)
    h = re.sub(r"<math .*?</math>", digit_groups, h, flags=re.S)
    h = mfrac_style(h)
    h = re.sub(r"<math .*?</math>", lead_op, h, flags=re.S)
    h = re.sub(r'<math alttext="[^"]*\\hline.*?</math>', hline_rule, h, flags=re.S)
    # keep a formula together with an opening bracket/quote before it and punctuation after it
    h = re.sub(r'([(\[“‘]?)(<math (?:(?!display="block")[^>])*>(?:(?!</math>).)*</math>)([.,;:?!)\]”’]*)',
               lambda m: f'<span class="nw">{m.group(0)}</span>' if m.group(1) or m.group(3) else m.group(0), h, flags=re.S)
    # aligned rows (broken equations): no gap between the left side and '='
    h = re.sub(r'(<math alttext="[^"]*\\begin\{aligned\}[^"]*"[^>]*>(?:<mrow>)?)<mtable>',
               r'\1<mtable columnspacing="0em" class="al">', h)
    h = h.replace('<math display="block"', '<math class="dm" display="block"')
    h = re.sub(r'(<math alttext="[^"]*") display="block"', r'\1 class="dm" display="block"', h)
    # unknown environments arrive as <div class="conceptx"> etc.
    h = re.sub(r'<div class="(concept|example|infobox|tip|trap)x">', r'<div class="\1">', h)
    h = h.replace('<div class="center">', '<div class="center">')
    # pandoc's empty table header row for header-less tabulars
    h = re.sub(r'<tr class="(odd|even|header)">', "<tr>", h)
    h = re.sub(r'\s*style="text-align: (left|center|right);"', lambda m: f' class="{m.group(1)[0]}"', h)
    h = h.replace("<br />", "<br/>").replace("<hr />", "<hr/>")
    h = re.sub(r"<col (style=\"width: [0-9.]+%\") />", r"<col \1/>", h)
    # Mental Math Toolkit: the trick names (first column) are bold, as in print
    h = re.sub(r'<div class="boldfirst">.*?</div>', lambda m: re.sub(
        r"(<tr>\s*<td[^>]*>)(.*?)(</td>)", r"\1<strong>\2</strong>\3", m.group(0), flags=re.S), h, flags=re.S)
    # a first row of bold cells is a header row (KPG 11.5.2)
    def header(m):
        cells = re.findall(r"<td([^>]*)>\s*<strong>(.*?)</strong>\s*</td>", m.group(2), flags=re.S)
        n = len(re.findall(r"<td", m.group(2)))
        if n and len(cells) == n:
            return m.group(1) + "".join(f'<th{a} scope="col">{c}</th>' for a, c in cells) + m.group(3)
        return m.group(0)
    h = re.sub(r"(<table>\s*(?:<colgroup>.*?</colgroup>\s*)?(?:<tbody>\s*)?<tr>)(.*?)(</tr>)", header, h, flags=re.S)
    return h


# ------------------------------------------------------------------ figures
def render_figures(figs: list[str]) -> list[tuple[str, float]]:
    """pdflatex all TikZ figures (one page each) -> PNG files; returns (file name, width in)."""
    EB.mkdir(parents=True, exist_ok=True)
    body = "\n".join(f"\\begin{{preview}}{f}\\end{{preview}}" for f in figs)
    pre = preamble() + "\n\\usepackage[active,tightpage]{preview}\n\\setlength\\PreviewBorder{3pt}\n"
    (EB / "figs.tex").write_text(pre + "\\begin{document}\n" + body + "\n\\end{document}\n", encoding="utf-8")
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "figs.tex"],
                       cwd=EB, capture_output=True, text=True)
    if r.returncode:
        log = (EB / "figs.log").read_text(errors="replace")
        i = log.find("\n!")
        raise SystemExit("figure rendering failed:\n" + log[i:i + 1500])
    info = subprocess.run(["pdfinfo", "-f", "1", "-l", str(len(figs)), "figs.pdf"], cwd=EB,
                          capture_output=True, text=True, check=True).stdout
    sizes = [float(w) / 72 for w in re.findall(r"Page\s+\d+ size:\s+([0-9.]+) x", info)]
    if len(sizes) != len(figs):
        raise SystemExit(f"expected {len(figs)} figure pages, got {len(sizes)}")
    for old in EB.glob("fig-*.png"):
        old.unlink()
    subprocess.run(["pdftoppm", "-r", str(FIG_PPI), "-gray", "-png", "figs.pdf", "fig"], cwd=EB, check=True)
    files = sorted(EB.glob("fig-*.png"), key=lambda p: int(p.stem.split("-")[1]))
    out = []
    for k, (src, w) in enumerate(zip(files, sizes)):
        name = f"fig{k + 1:03d}.png"
        im = Image.open(src).convert("L")
        im.quantize(16, dither=Image.Dither.NONE).save(EB / name, optimize=True, bits=4)
        out.append((name, w))
    return out


# alt text (KPG 11.4.1: describe the image and its meaning, < 140 characters). The shape is read from
# the TikZ source, because one template draws several variants (radius or diameter, rug or pool, ...).
FIG_KIND = {
    "vertical_adjacent": "Two intersecting lines", "parallel_lines": "Parallel lines cut by a transversal",
    "angle_algebra": "A ray meeting a straight line", "around_point": "Four angles around a point",
    "third_angle": "Triangle", "exterior_angle": "Triangle with one side extended",
    "pyth_hyp": "Right triangle", "pyth_leg": "Right triangle", "special_right": "Special right triangle",
    "isosceles_angles": "Isosceles triangle, the two equal sides marked", "similar_triangles": "Two similar triangles",
    "parallelogram": "Parallelogram with base, dashed height and slanted side", "trapezoid": "Trapezoid with two bases and dashed height",
    "composite": "L-shaped figure, all corners right angles",
    "walkway": "Rectangle centered inside a larger rectangle, the border between them shaded",
    "annulus": "Two circles with the same center", "arc_sector": "Circle with a sector between two radii",
    "part_circle": "Quarter of a circle", "box_volume": "Rectangular box", "box_surface": "Closed rectangular box",
    "cube": "Cube", "cylinder": "Cylinder", "cone_sphere": "Cone",
}
POLYGONS = {3: "Triangle", 4: "Quadrilateral", 5: "Pentagon", 6: "Hexagon", 7: "Heptagon", 8: "Octagon"}
INTRO_ALT = {
    12: "Number line from −5 to 5: open circle at −2, shaded to the right (x > −2)",
    16: "Parallel lines ℓ and m cut by transversal t, forming angles numbered 1 to 8",
    17: "Right triangle with legs a and b and hypotenuse c",
    18: "A triangle and a parallelogram, each with base b and dashed height h",
    19: "Circle with center, radius r, diameter d and circumference C",
    20: "Rectangular box with length l, width w and height h",
    21: "Coordinate plane with x- and y-axes, quadrants I to IV and the point (3, 2)",
}


def tikz_label(t: str) -> str:
    t = re.sub(r"\\(tiny|scriptsize|footnotesize|small|normalsize)\b", "", t)
    t = re.sub(r"\^\{?\\circ\}?", "°", t)
    t = re.sub(r"\\sqrt\s*\{?(\w+)\}?", r"√\1", t)
    t = t.replace("\\ell", "ℓ").replace("$", "").replace("\\,", " ").replace("{", "").replace("}", "")
    t = re.sub(r"(?<![\w)])-", "−", t)
    return re.sub(r"\s+", " ", t).strip()


def fig_alt(src: str, template: str = "") -> str:
    base = re.sub(r"_(?:[a-z]|civ|mil|\d)$", "", template.split(".")[-1])
    labels = []
    for m in re.finditer(r"node\s*(?:\[[^\]]*\])?\s*(?:at\s*\([^)]*\))?\s*\{", src):
        lab = tikz_label(brace_group(src, m.end() - 1)[0])
        if lab:
            labels.append(lab)          # duplicates kept: a hexagon can have two 127° angles
    if "grid" in src:
        names = re.findall(r"\\node\[[^\]]*\] at \(-?[\d.]+,-?[\d.]+\) \{\\scriptsize \$?([A-Z])\$?\}", src)
        if base == "read_grid":         # the question is to read the coordinates: do not give them away
            alt = "Coordinate grid with " + (f"points {', '.join(names[:-1])} and {names[-1]}" if len(names) > 1
                                             else f"point {names[0]}" if names else "a marked point")
        else:
            pts = [f"({x}, {y})".replace("-", "−") for x, y in re.findall(r"\\fill \((-?[\d.]+),(-?[\d.]+)\) circle", src)]
            alt = "Coordinate grid with a line through " + " and ".join(pts) if pts else "Coordinate grid with a line"
        return alt
    full_circle = re.search(r"\\draw\[thick\] \([-\d.]+,[-\d.]+\) circle \(", src)
    if base in ("circle_area", "circumference"):
        diameter = re.search(r"\\draw \((-[\d.]+),0\) -- \(([\d.]+),0\)", src)
        kind = "Circle with a diameter drawn" if diameter else "Circle with a radius drawn from the center"
    elif base == "shaded_region":
        if full_circle and "rectangle" in src:
            kind = "Circle inscribed in a square; the corners outside the circle are shaded"
        elif "arc (0:180" in src:
            kind = "Shaded rectangle with a semicircle on top, dashed line where they meet"
        elif "arc (0:90" in src:
            kind = "Square with a quarter circle drawn from one corner; the part outside the quarter circle is shaded"
        else:
            kind = "Shaded figure"
    elif base == "triangle_area":
        kind = "Triangle with base and dashed height" if "dashed" in src else "Right triangle"
    elif base == "polygon_missing":
        m = re.search(r"\\draw\[thick\] ((?:\([^)]*\)\s*--\s*)+)cycle", src)
        n = len(re.findall(r"\(", m.group(1))) if m else 4
        kind = f"{POLYGONS.get(n, 'Polygon')} with its interior angles"
    else:
        kind = FIG_KIND.get(base, "Figure")
    alt = kind + (". Labels: " + ", ".join(labels) if labels else "")
    return alt if len(alt) < 140 else alt[:136].rsplit(" ", 1)[0] + " …"


def fig_html(name: str, width_in: float, alt: str) -> str:
    pct = max(40, min(100, round(width_in / TEXT_W_IN * 100)))     # KPG 11.4.2: not below 40 %
    return f'<div class="fig"><img src="images/{name}" alt="{html.escape(alt)}" style="width: {pct}%"/></div>'


# ------------------------------------------------------------------ cover
def cover_tex() -> str:
    """Front cover of the paperback, re-laid out for Kindle's 1:1.6 portrait."""
    W, H = 5.0, 8.0
    T = config
    return rf"""\documentclass{{article}}
\usepackage[paperwidth={W}in,paperheight={H}in,margin=0in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[black,medium,lining,defaultfam]{{montserrat}}
\usepackage{{tikz}}
\definecolor{{navy}}{{HTML}}{{0F1D36}}
\definecolor{{navy2}}{{HTML}}{{1A2C4E}}
\definecolor{{gridc}}{{HTML}}{{22385F}}
\definecolor{{gold}}{{HTML}}{{F2B53A}}
\pagestyle{{empty}}
\setlength{{\parindent}}{{0pt}}
\newcommand{{\chk}}{{\tikz[x=1pt,y=1pt,baseline=-1pt]\draw[gold,line width=1.7pt,line cap=round,line join=round] (0,4) -- (3,1) -- (8,7.5);}}
\begin{{document}}
\begin{{tikzpicture}}[x=1in,y=1in,remember picture,overlay]
\begin{{scope}}[shift={{(current page.south west)}}]
\fill[navy] (0,0) rectangle ({W},{H});
\draw[gridc,line width=0.3pt,step=0.25] (0,0) grid ({W},{H});
\draw[gridc!70!white,line width=0.7pt,step=1] (0,0) grid ({W},{H});
\fill[gold] (0,{H - 0.6}) rectangle ({W},{H});
\node[anchor=west,text=navy,font=\bfseries\fontsize{{9.5}}{{11}}\selectfont] at (0.32,{H - 0.3}) {{NO CALCULATOR \textbullet{{}} JUST PRACTICE}};
\node[anchor=east,text=navy,font=\mdseries\fontsize{{8.5}}{{10}}\selectfont] at ({W - 0.32},{H - 0.3}) {{{T.YEAR} EDITION}};
\node[anchor=north west,text=white,font=\bfseries\fontsize{{80}}{{80}}\selectfont,inner sep=0] at (0.3,{H - 0.95}) {{ASVAB}};
\node[anchor=north west,text=gold,font=\bfseries\fontsize{{30.5}}{{34}}\selectfont,inner sep=0] at (0.34,{H - 2.2}) {{MATH WORKBOOK}};
\node[anchor=north west,text=white,font=\mdseries\fontsize{{13.5}}{{17.5}}\selectfont,inner sep=0,text width=3.2in,align=left]
  at (0.36,{H - 2.85}) {{1,000 Practice Problems with\\Step-by-Step Solutions}};
\foreach \i in {{0,1,2}} {{
  \draw[gold,line width=3.4pt,line cap=butt] (0.38+\i*0.29,{H - 3.95}) -- ++(0.14,0.15) -- ++(0.14,-0.15);
}}
\draw[white!40!navy,line width=0.8pt] (1.35,{H - 3.87}) -- (3.15,{H - 3.87});
\fill[gold] (4.17,{H - 3.4}) circle (0.55);
\draw[navy,line width=1pt] (4.17,{H - 3.4}) circle (0.485);
\node[text=navy,font=\bfseries\fontsize{{19}}{{19}}\selectfont] at (4.17,{H - 3.31}) {{1,000}};
\node[text=navy,font=\bfseries\fontsize{{7}}{{9}}\selectfont] at (4.17,{H - 3.59}) {{PROBLEMS}};
\node[anchor=north west,text=white,font=\mdseries\fontsize{{10.5}}{{17.5}}\selectfont,inner sep=0,text width=4.4in,align=left]
  at (0.38,{H - 4.3}) {{%
  \chk\enspace Key concepts \& worked examples for 27 topics\\
  \chk\enspace Diagnostic test with a personal study plan\\
  \chk\enspace 4 full-length math practice tests\\
  \chk\enspace Every wrong answer explained\\
  \chk\enspace Every answer verified by computer algebra}};
\fill[navy2] (0,0) rectangle ({W},1.05);
\draw[gold,line width=1.4pt] (0,1.05) -- ({W},1.05);
\node[anchor=west,text=white,font=\mdseries\fontsize{{10}}{{13}}\selectfont,text width=2.6in,align=left]
  at (0.36,0.53) {{Arithmetic Reasoning\\Mathematics Knowledge}};
\node[anchor=east,text=gold,font=\bfseries\fontsize{{11.5}}{{14}}\selectfont] at ({W - 0.32},0.53) {{{T.AUTHOR.upper()}}};
\end{{scope}}
\end{{tikzpicture}}
\end{{document}}
"""


def make_cover():
    EB.mkdir(parents=True, exist_ok=True)
    (EB / "cover.tex").write_text(cover_tex(), encoding="utf-8")
    for _ in range(2):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "cover.tex"],
                           cwd=EB, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(r.stdout[-3000:])
    subprocess.run(["pdftoppm", "-png", "-r", "320", "-singlefile", "cover.pdf", "cover"], cwd=EB, check=True)
    im = Image.open(EB / "cover.png").convert("RGB")
    assert im.size == (1600, 2560), im.size
    OUT.mkdir(exist_ok=True)
    im.save(COVER, quality=92)


# ------------------------------------------------------------------ book
def nb(s) -> str:
    return str(s).replace(" ", "&#160;")


def main():
    mods = load_chapters()
    chapters, diag, tests = generate_all(mods)
    total = sum(len(v) for v in chapters.values()) + len(diag) + sum(len(a) + len(m) for a, m in tests)
    if total != 1000:
        raise SystemExit(f"{total} problems, expected 1000")
    by_num = {m.NUM: m for m in mods}
    for m in mods:
        m.ETITLE = m.TITLE.replace("\\&", "&")
    C = Converter()

    # ---- problem sets: ids, files and fragments
    sets = []    # (set id, problems, problem file, solution file)
    for m in mods:
        sets.append((f"c{m.NUM:02d}", chapters[m.NUM], f"ch{m.NUM:02d}.xhtml", f"ch{m.NUM:02d}-answers.xhtml"))
    sets.append(("d", diag, "diagnostic.xhtml", "diagnostic-answers.xhtml"))
    for k, (ar, mk) in enumerate(tests, 1):
        sets.append((f"t{k}a", ar, f"test{k}.xhtml", f"test{k}-answers.xhtml"))
        sets.append((f"t{k}m", mk, f"test{k}.xhtml", f"test{k}-answers.xhtml"))
    fig_of = {}
    for sid, probs, _, _ in sets:
        for i, p in enumerate(probs, 1):
            pid = f"{sid}-{i}"
            C.add(pid + ":stem", p.stem)
            for j, (t, why) in enumerate(p.choices):
                C.add(f"{pid}:c{j}", t)
                if why and j != p.key:
                    C.add(f"{pid}:w{j}", why.rstrip(".") + ".")
            for j, s in enumerate(p.steps):
                C.add(f"{pid}:s{j}", s)
            if p.tip:
                C.add(pid + ":tip", p.tip)
            if p.figure:
                fig_of[pid] = C.fig_id(p.figure)
    for m in mods:
        C.add(f"intro{m.NUM}", m.INTRO)

    # ---- front and back matter from the paperback's text
    front = (TEX / "front.tex").read_text(encoding="utf-8")
    sections = re.split(r"%% -+ ([a-z ]+)\n", front)
    fr = dict(zip(sections[1::2], sections[2::2]))
    howto = fr["how to use"].replace("<<DIAGMIN>>", str(diag_minutes(diag)))
    howto = howto.replace("\\textbf{Take the Diagnostic Test} (page~\\pageref{diag})",
                          "\\textbf{Take the \\href{diagnostic.xhtml}{Diagnostic Test}}")
    howto = howto.replace("\\textbf{Redo your misses a week later} and log them in the Progress\n  Tracker at the back of the book.",
                          "\\textbf{Redo your misses a week later.} Keep a list of them on paper, or highlight\n  them in your Kindle.")
    howto += r"""
\section*{Using this eBook}
\begin{itemize}
\item \textbf{Tap a problem number} to jump to its full solution. To return to the problem,
  use your Kindle's \emph{Back} command (the back arrow at the top of the screen, or
  ``Go back'' in the menu).
\item \textbf{Answer keys are links, too.} In every key, tap an answer to open its explanation;
  in the practice-test keys, the chapter number takes you to the chapter that teaches the skill.
\item \textbf{Work on paper.} Write the problem number and your answer letter (A--D) in a
  notebook, then check them against the key at the end of the set.
\item \textbf{Mark what you miss.} Highlight or bookmark the problems you get wrong; your
  Kindle collects them under Notes, so you can redo them later.
\item \textbf{Figures} can be enlarged: double-tap (or press and hold) a picture to zoom in.
\end{itemize}
"""
    for name, txt in (("howto", howto), ("subtests", fr["the test"]), ("strategy", fr["strategy"])):
        txt = re.sub(r"\\chapter\*\{[^}]*\}\n\\addcontentsline\{[^\n]*\n\\markboth\{[^\n]*\n", "", txt)
        txt = txt.replace("\\section*{", "\\subsection*{")     # h2 under the chapter's h1
        txt = txt.replace("memorize the ones on the Formula Sheet at the back of this book",
                          "memorize the ones on the \\href{formulas.xhtml}{Formula Sheet} at the end of this book")
        C.add(name, txt)
    back = (TEX / "back.tex").read_text(encoding="utf-8")
    bsec = re.split(r"%% -+ ([a-z ]+)\n", back)
    bk = dict(zip(bsec[1::2], bsec[2::2]))
    for name, key in (("formulas", "formula sheet"), ("tables", "reference tables")):
        txt = re.sub(r"\\chapter\*\{[^}]*\}\n\\addcontentsline\{[^\n]*\n\\markboth\{[^\n]*\n", "", bk[key])
        txt = txt.replace("<<SQUARES>>", squares_table()).replace("<<FDP>>", fdp_table())
        txt = txt.replace("Everything on this page is fair", "Everything here is fair")
        C.add(name, txt)
    for i, (t, d) in enumerate(GLOSSARY):
        C.add(f"gl{i}", d)
    for k, blurb in PART_BLURB.items():
        C.add(f"part{k}", blurb)

    print(f"converting {len(C.frags)} fragments and {len(C.figs)} figures ...", flush=True)
    C.run()
    figs = render_figures(C.figs)
    images = {f"images/{n}": EB / n for n, _ in figs}

    def figure(n, alt):
        name, w = figs[n]
        return fig_html(name, w, alt)

    def expand_figs(h, alt="Figure"):
        h = re.sub(r"<p>FIGPH(\d+)X</p>", lambda m: figure(int(m.group(1)), alt), h)
        return re.sub(r"FIGPH(\d+)X", lambda m: figure(int(m.group(1)), alt), h)

    # ---- problem and solution HTML
    def problem_html(sid, i, p, sol_file):
        pid = f"{sid}-{i}"
        stem = C.html[pid + ":stem"].strip()
        num = f'<a class="pn" href="{sol_file}#{pid}s">{i}.</a>'
        m = re.fullmatch(r"<p>(.*)</p>", stem, flags=re.S)
        if m and "<p>" not in m.group(1):
            head = f'<p class="stem">{num} {m.group(1)}</p>'
        else:
            head = f'<p class="stem">{num}</p>\n{stem}'
        fig = figure(fig_of[pid], fig_alt(C.figs[fig_of[pid]], p.template)) if pid in fig_of else ""
        opts = "\n".join(f'<p class="opt"><span class="ol">{LETTERS[j]}</span>&#160;&#160;{C.inline(f"{pid}:c{j}")}</p>'
                         for j in range(len(p.choices)))
        return f'<div class="prob" id="{pid}">\n{head}\n{fig}{opts}\n</div>'

    def solution_html(sid, i, p, prob_file):
        pid = f"{sid}-{i}"
        out = [f'<div class="sol" id="{pid}s">',
               f'<p class="sh"><span class="pn">{i}.</span> <span class="key">{LETTERS[p.key]}</span> '
               f'{C.inline(f"{pid}:c{p.key}")}</p>']
        for j in range(len(p.steps)):
            out.append(f'<p class="step"><span class="sn">{j + 1}</span>&#160; {C.inline(f"{pid}:s{j}")}</p>')
        if p.tip:
            out.append(f'<p class="tipl"><span class="lbl">TIP</span>&#160; {C.inline(pid + ":tip")}</p>')
        traps = [f"({LETTERS[j]}) {C.inline(f'{pid}:w{j}')}" for j, (_, why) in enumerate(p.choices)
                 if why and j != p.key]
        if traps:
            out.append(f'<p class="why"><span class="lbl">WHY NOT</span>&#160; {" ".join(traps)}</p>')
        out.append("</div>")
        return "\n".join(out)

    def key_html(sid, probs, chapter_links=False):
        items = []
        for i, p in enumerate(probs, 1):
            s = f'<a href="#{sid}-{i}s">{i}&#160;{LETTERS[p.key]}</a>'
            if chapter_links:
                s += f'&#160;<a class="small" href="ch{p.chapter:02d}.xhtml">ch.&#160;{p.chapter}</a>'
            items.append(s)
        return '<p class="keys">' + " · ".join(items) + "</p>"

    docs = []
    T = config
    # ---- title, copyright, contents
    docs.append(Doc("title", "Title Page", lang="en-US", toc=False, body_class="title-page", body=f"""
<h1>{T.TITLE}</h1>
<p class="sub">{T.SUBTITLE}</p>
<p>{T.TAGLINE.replace(chr(92) + '&', '&amp;')}</p>
<p>&#160;</p>
<p>Key concepts and worked examples for every topic<br/>A diagnostic test with a personal study plan<br/>
{sum(len(v) for v in chapters.values()):,} drill problems in {len(mods)} chapters<br/>4 full-length math practice tests<br/>
Every answer checked by computer algebra</p>
<p>&#160;</p>
<p><b>{T.AUTHOR}</b></p>"""))
    docs.append(Doc("copyright", "Copyright", lang="en-US", toc=False, body_class="copyright", body=f"""
<p><b>{T.TITLE}: {T.SUBTITLE}</b><br/>{T.EDITION}, Kindle edition, {T.YEAR}</p>
<p>Copyright © {T.YEAR} {T.AUTHOR}. All rights reserved.</p>
<p>No part of this book may be reproduced, stored in a retrieval system, or transmitted in any form or by any
means without the prior written permission of the author, except for brief quotations in reviews.</p>
<p>ASVAB is a registered trademark of the United States Department of Defense, which was not involved in the
production of, and does not endorse, this book. This book is an independent study aid. It is not affiliated with
the Department of Defense, any branch of the U.S. Armed Forces, or any recruiting organization.</p>
<p>Test formats, question counts, time limits, and qualifying scores are set by the Department of Defense and the
individual services and can change. Always confirm current details with your recruiter or at officialasvab.com.
The author makes no guarantee of any particular test score.</p>
<p>The practice problems in this book were generated and their answers verified with the SymPy computer algebra
system; every answer was computed exactly and then confirmed by a second, independent calculation.</p>"""))

    toc_lines = []

    def toc(title, href, level=1):
        toc_lines.append(f'<p class="l{level}"><a href="{href}">{html.escape(title)}</a></p>')

    def section_doc(id_, title, key, intro=""):
        body = f"<h1>{html.escape(title)}</h1>\n{intro}{expand_figs(C.block(key))}"
        return Doc(id_, title, lang="en-US", body=body)

    howto_doc = section_doc("howto", "How to Use This Book", "howto")
    howto_doc.landmark = "bodymatter"
    front_docs = [howto_doc, section_doc("subtests", "The ASVAB Math Subtests", "subtests"),
                  section_doc("strategy", "Test-Day Strategies", "strategy")]

    # ---- diagnostic
    minutes = diag_minutes(diag)
    diag_doc = Doc("diagnostic", "Diagnostic Test", lang="en-US",
                   children=[("Answers and Your Study Plan", "diagnostic-answers.xhtml")], body="\n".join([
        '<h1 id="diag">Diagnostic Test</h1>',
        f"<p>This test samples every chapter of the book. Take it before you begin studying, without a calculator, "
        f"and try to finish in about {minutes} minutes. Don’t guess wildly—if you have no idea how to start a "
        f"problem, leave it blank so that the result shows what you really need to study.</p>",
        f'<p class="meta">{len(diag)} questions · target time: {minutes} minutes. Write your answers on paper, then '
        f'check them in the <a href="diagnostic-answers.xhtml">answer table</a>.</p>',
        *[problem_html("d", i, p, "diagnostic-answers.xhtml") for i, p in enumerate(diag, 1)],
        '<p class="next"><a href="diagnostic-answers.xhtml">→ Answers and Your Study Plan</a></p>']))
    rows = "\n".join(
        f'<tr><td><a href="#d-{i}s">{i}</a></td><td class="c"><b>{LETTERS[p.key]}</b></td>'
        f'<td class="c"><a href="ch{p.chapter:02d}.xhtml">{p.chapter}</a></td><td>{html.escape(by_num[p.chapter].ETITLE)}</td></tr>'
        for i, p in enumerate(diag, 1))
    diag_sol = Doc("diagnostic-answers", "Diagnostic Test: Answers", lang="en-US", toc=False, body="\n".join([
        "<h1>Diagnostic Test: Answers and Your Study Plan</h1>",
        "<p>Check your answers against the table. Each row shows the chapter the question comes from. "
        "<b>Note the chapter number of every question you missed or left blank</b>—those chapters are your study "
        "plan. Work through them first, then the rest of the book in order. Tap a question number for its "
        "explanation, or a chapter number to go to the chapter.</p>",
        f'<table><tr><th>#</th><th>Ans.</th><th>Ch.</th><th>Topic</th></tr>\n{rows}\n</table>',
        '<div class="infobox"><p class="boxtitle">How did you do?</p><table>'
        "<tr><td><b>26–30</b> correct</td><td>Strong. Skim the Key Concepts, do the challenge problems, then the practice tests.</td></tr>"
        "<tr><td><b>18–25</b> correct</td><td>Solid base. Study your weak chapters fully, then the rest.</td></tr>"
        "<tr><td><b>10–17</b> correct</td><td>Work through every chapter in order; take your time with the warm-ups.</td></tr>"
        "<tr><td><b>0–9</b> correct</td><td>Start at Chapter 1. Every chapter builds on the ones before it.</td></tr></table></div>",
        "<h2>Explanations</h2>",
        *[solution_html("d", i, p, "diagnostic.xhtml") for i, p in enumerate(diag, 1)],
        '<p class="next"><a href="diagnostic.xhtml">← Back to the Diagnostic Test</a></p>']))

    # ---- chapters
    body_docs = []
    part = None
    for m in mods:
        probs = chapters[m.NUM]
        if m.PART != part:
            part = m.PART
            pmods = [x for x in mods if x.PART == part]
            body_docs.append(Doc(f"part{part}", f"Part {part}: {PARTS[part]}", lang="en-US",
                                 children=[(f"{x.NUM}. {x.ETITLE}", f"ch{x.NUM:02d}.xhtml") for x in pmods], body="\n".join([
                f"<h1>Part {part}<br/>{html.escape(PARTS[part])}</h1>",
                C.block(f"part{part}"),
                *[f'<p class="toc"><a href="ch{x.NUM:02d}.xhtml">Chapter {x.NUM}: {html.escape(x.ETITLE)}</a></p>' for x in pmods]])))
        sid = f"c{m.NUM:02d}"
        pf, sf = f"ch{m.NUM:02d}.xhtml", f"ch{m.NUM:02d}-answers.xhtml"
        n = len(probs)
        secs = sorted({p.section for p in probs}, key=lambda s: s != "MK")
        minutes = round(sum(1.2 if p.section == "AR" else 1.0 for p in probs))
        lv = [sum(1 for p in probs if p.level == k) for k in (1, 2, 3)]
        body_docs.append(Doc(f"ch{m.NUM:02d}", f"Chapter {m.NUM}: {m.ETITLE}", lang="en-US", toc=False, body="\n".join([
            f"<h1>Chapter {m.NUM}<br/>{html.escape(m.ETITLE)}</h1>",
            f'<p class="meta">Tested on: {" · ".join(SECTION_NAMES[s] for s in secs)}</p>',
            "<h2>Key Concepts</h2>",
            expand_figs(C.block(f"intro{m.NUM}"), INTRO_ALT.get(m.NUM, "Figure")),
            f'<h2 id="{sid}-set">Practice Set {m.NUM}</h2>',
            f'<p class="meta">{n} problems · target time: {minutes} minutes. Problems 1–{lv[0]} are warm-ups, '
            f'{lv[0] + 1}–{lv[0] + lv[1]} are test level, and {lv[0] + lv[1] + 1}–{n} are challenge problems. '
            f'Tap a problem number for its solution.</p>',
            *[problem_html(sid, i, p, sf) for i, p in enumerate(probs, 1)],
            f'<p class="next"><a href="{sf}">→ Answers &amp; Explanations {m.NUM}</a></p>'])))
        nxt = f"ch{m.NUM + 1:02d}.xhtml" if m.NUM < len(mods) else "practice-tests.xhtml"
        body_docs.append(Doc(f"ch{m.NUM:02d}-answers", f"Answers & Explanations {m.NUM}", lang="en-US", toc=False,
                             body="\n".join([
            f"<h1>Answers &amp; Explanations {m.NUM}</h1>",
            f'<p class="meta">{html.escape(m.ETITLE)} · <a href="{pf}#{sid}-set">back to Practice Set {m.NUM}</a></p>',
            "<h2>Answer key</h2>", key_html(sid, probs),
            "<h2>Explanations</h2>",
            *[solution_html(sid, i, p, pf) for i, p in enumerate(probs, 1)],
            f'<p class="next"><a href="{nxt}">→ Next: {"Chapter " + str(m.NUM + 1) if m.NUM < len(mods) else "Practice Tests"}</a></p>'])))

    # ---- practice tests
    test_docs = [Doc("practice-tests", "Practice Tests", lang="en-US",
                     children=[x for k in range(1, N_TESTS + 1)
                               for x in ((f"Practice Test {k}", f"test{k}.xhtml"),
                                         (f"Answer Key: Practice Test {k}", f"test{k}-answers.xhtml"))], body="\n".join([
        "<h1>Practice Tests</h1>",
        f"<p>Four full-length math sections in the paper-and-pencil format: {AR_TEST} Arithmetic Reasoning questions "
        f"in 36 minutes and {MK_TEST} Mathematics Knowledge questions in 24 minutes.</p>",
        *[f'<p class="toc"><a href="test{k}.xhtml">Practice Test {k}</a></p>' for k in range(1, N_TESTS + 1)]]))]
    for k, (ar, mk) in enumerate(tests, 1):
        pf, sf = f"test{k}.xhtml", f"test{k}-answers.xhtml"
        test_docs.append(Doc(f"test{k}", f"Practice Test {k}", lang="en-US", toc=False, body="\n".join([
            f"<h1>Practice Test {k}</h1>",
            '<div class="infobox"><p class="boxtitle">Instructions</p>'
            f"<p>This test has two parts, timed like the paper-and-pencil ASVAB. <b>Part 1, Arithmetic Reasoning:</b> "
            f"{AR_TEST} questions, 36 minutes. <b>Part 2, Mathematics Knowledge:</b> {MK_TEST} questions, 24 minutes. "
            "No calculator. Use scratch paper. Answer every question—there is no penalty for guessing. Write the "
            "question number and your answer letter on paper; check them in the answer key at the end.</p></div>",
            f'<h2 id="t{k}a">Part 1: Arithmetic Reasoning</h2>',
            f'<p class="meta">{AR_TEST} questions · 36 minutes</p>',
            *[problem_html(f"t{k}a", i, p, sf) for i, p in enumerate(ar, 1)],
            f'<h2 id="t{k}m">Part 2: Mathematics Knowledge</h2>',
            f'<p class="meta">{MK_TEST} questions · 24 minutes</p>',
            *[problem_html(f"t{k}m", i, p, sf) for i, p in enumerate(mk, 1)],
            f'<p class="next"><a href="{sf}">→ Answer Key: Practice Test {k}</a></p>'])))
        nxt = f"test{k + 1}.xhtml" if k < N_TESTS else "formulas.xhtml"
        test_docs.append(Doc(f"test{k}-answers", f"Answer Key: Practice Test {k}", lang="en-US", toc=False, body="\n".join([
            f"<h1>Answer Key: Practice Test {k}</h1>",
            '<p class="meta">Tap an answer for its explanation; “ch.” is the chapter that teaches the skill.</p>',
            "<h2>Part 1: Arithmetic Reasoning</h2>", key_html(f"t{k}a", ar, True),
            "<h2>Part 2: Mathematics Knowledge</h2>", key_html(f"t{k}m", mk, True),
            '<div class="infobox"><p class="boxtitle">Scoring your practice test</p><table>'
            "<tr><th>Percent correct</th><th>AR (of 30)</th><th>MK (of 25)</th></tr>"
            "<tr><td>90% or more: excellent</td><td>27–30</td><td>23–25</td></tr>"
            "<tr><td>75–89%: good</td><td>23–26</td><td>19–22</td></tr>"
            "<tr><td>60–74%: keep practicing</td><td>18–22</td><td>15–18</td></tr>"
            "<tr><td>below 60%: review the chapters</td><td>0–17</td><td>0–14</td></tr></table>"
            '<p class="small">These bands measure your progress in this book only. Your real AFQT percentile depends on '
            "all four AFQT subtests and is scaled by the Department of Defense.</p></div>",
            "<h2>Explanations: Arithmetic Reasoning</h2>",
            *[solution_html(f"t{k}a", i, p, pf) for i, p in enumerate(ar, 1)],
            "<h2>Explanations: Mathematics Knowledge</h2>",
            *[solution_html(f"t{k}m", i, p, pf) for i, p in enumerate(mk, 1)],
            f'<p class="next"><a href="{nxt}">→ Next: {"Practice Test " + str(k + 1) if k < N_TESTS else "Formula Sheet"}</a></p>'])))

    # ---- back matter
    back_docs = [section_doc("formulas", "Formula Sheet", "formulas"),
                 section_doc("tables", "Quick Reference Tables", "tables")]
    gl = "\n".join(f"<p><b>{html.escape(t)}.</b> {C.inline(f'gl{i}')}</p>" for i, (t, _) in enumerate(GLOSSARY))
    back_docs.append(Doc("glossary", "Glossary of Math Terms", lang="en-US", body=
        "<h1>Glossary of Math Terms</h1>\n<p>Mathematics Knowledge questions often test vocabulary directly "
        "(“Which of the following is a prime number?”). Make sure every term below is familiar.</p>\n" + gl))
    back_docs.append(Doc("thanks", "Thank You", lang="en-US", body="""
<h1>Thank you, and good luck!</h1>
<p>If this workbook helped you prepare, please consider leaving a short review on Amazon. Reviews help other future
service members find the right study materials—and they help the author keep improving this book.</p>
<p>Found an error, or a solution you think could be explained better? Every report is read and fixed in the next
edition.</p>"""))

    # ---- inline table of contents
    main_docs = front_docs + [diag_doc, diag_sol] + body_docs + test_docs + back_docs
    for d in main_docs:
        if d.toc:
            toc(d.title, d.href)
            for t, h in d.children:
                toc(t, h, 2)
    contents = Doc("contents", "Contents", lang="en-US", landmark="toc", body_class="toc",
                   body="<h1>Contents</h1>\n" + "\n".join(toc_lines))
    docs += [contents] + main_docs

    # ---- checks: every internal link must resolve
    ids = {}
    for d in docs:
        ids[d.href] = set(re.findall(r'\bid="([^"]+)"', d.body))
    bad = []
    for d in docs:
        for href in re.findall(r'href="([^"#:]*)(?:#([^"]*))?"', d.body):
            f, a = href
            f = f or d.href
            if f not in ids or (a and a not in ids[f]):
                bad.append((d.href, f, a))
    if bad:
        raise SystemExit(f"{len(bad)} broken links, e.g. {bad[:5]}")
    leftovers = []
    for d in docs:
        plain = re.sub(r"<math.*?</math>", "", d.body, flags=re.S)
        for m_ in re.finditer(r"\\[a-zA-Z]+|FIGPH|FRAGSEP|<<|\$", plain):
            leftovers.append((d.href, plain[max(0, m_.start() - 40):m_.end() + 40]))
    # a literal $ in prose is a currency sign; report only LaTeX-looking leftovers
    leftovers = [x for x in leftovers if "\\" in x[1] or "FIGPH" in x[1] or "FRAGSEP" in x[1]]
    if leftovers:
        print(f"WARNING: {len(leftovers)} LaTeX leftovers, e.g.:")
        for x in leftovers[:12]:
            print("  ", x)

    make_cover()
    book = Book(title=f"{T.TITLE}: {T.SUBTITLE}", language="en-US", creator=T.AUTHOR, publisher=T.AUTHOR,
                description="1,000 ASVAB Arithmetic Reasoning and Mathematics Knowledge practice problems with "
                            "step-by-step solutions, a diagnostic test and four practice tests.",
                identifier=f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, f'asvab-math-workbook-{T.YEAR}-ebook')}",
                css=CSS, cover=COVER, images=images, docs=docs,
                modified=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    book.toc_title = "Contents"
    book.write(EPUB)
    errors = check(EPUB)
    size = EPUB.stat().st_size // 1024
    print(f"{EPUB.name}: {size} KB, {len(docs)} documents, {len(images)} figures, EPUBCheck errors: {len(errors)}")
    for e in errors[:20]:
        print("  ", e)
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
