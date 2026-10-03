"""Build the complete book.

    .venv/bin/python -m asvab.build            # -> output/ASVAB-Math-Workbook-interior.pdf
    .venv/bin/python -m asvab.build --tex-only # just write build/book.tex

Generates all 1,000 problems (chapters, diagnostic, four practice tests),
validates every one of them, writes a QA report (output/qa-report.txt) and
an answer ledger (output/answer-ledger.csv), then compiles the interior PDF.
"""
from __future__ import annotations

import argparse
import collections
import csv
import random
import re
import shutil
import sys

from . import config
from .core import Problem
from .generate import balanced_targets, chapter_problems, load_chapters, make
from .glossary import GLOSSARY
from .render import (BUILD, LETTERS, ROOT, SECTION_NAMES, answer_key_tex, chapter_tex,
                     compile_tex, preamble, problems_block, solutions_block)

OUT = ROOT / "output"
TEX = ROOT / "asvab" / "tex"

PARTS = {
    1: "Number Skills",
    2: "Algebra",
    3: "Geometry",
    4: "Word Problems",
}
PART_BLURB = {
    1: "Whole numbers, signed numbers, factors, fractions, decimals, percents, "
       "ratios, exponents, and roots---the toolkit behind every other question.",
    2: "Expressions, equations, inequalities, systems, polynomials, and "
       "quadratics: the algebra on the Mathematics Knowledge subtest.",
    3: "Angles, triangles, area, circles, volume, and the coordinate plane.",
    4: "The heart of the Arithmetic Reasoning subtest: money, percents, rates, "
       "work, mixtures, statistics, probability, and multi-step problems.",
}

AR_TEST, MK_TEST = 30, 25
N_TESTS = 4
N_DIAG = 30


# ------------------------------------------------------------------ pools
def entries(mod):
    e = getattr(mod, "TEST", None) or [(t, l) for t, l, _ in mod.PLAN]
    return list(dict.fromkeys(e))


def family(mod, tpl) -> tuple:
    """Templates split into variants (commission_a/_b, ratio_total_civ...) are one family."""
    return (mod.NUM, re.sub(r"_(?:[a-z]|civ|mil|\d)$", "", tpl.__name__))


def test_level(rng, weights=(0.25, 0.45, 0.30)) -> int:
    r = rng.random()
    return 1 if r < weights[0] else (2 if r < weights[0] + weights[1] else 3)


def pick_level_entry(rng, ents, prefer):
    """Pick an entry, preferring level `prefer` if available."""
    best = [e for e in ents if e[1] == prefer]
    return rng.choice(best or ents)


def build_section(mods, section, count, rng, seen, used, avoid=None):
    """Draw `count` problems of one subtest from all chapters."""
    by_ch = collections.OrderedDict()
    for mod in mods:
        es = [e for e in entries(mod) if e[0].section == section]
        if es:
            by_ch[mod.NUM] = (mod, es)
    if section == "AR":
        core = [n for n in by_ch if by_ch[n][0].PART == 4]
        alloc = {n: 0 for n in by_ch}
        per = count * 3 // 5 // max(1, len(core))     # 3 per word-problem chapter
        for n in core:
            alloc[n] = per
        others = [n for n in by_ch if n not in core]
        rest = count - sum(alloc.values())
        rng.shuffle(others)
        for i in range(rest):
            alloc[(others or core)[i % len(others or core)]] += 1
    else:
        alloc = {n: 1 for n in by_ch}
        extra = count - len(alloc)
        pool = [n for n in by_ch if by_ch[n][0].PART in (2, 3)] or list(by_ch)
        rng.shuffle(pool)
        while extra < 0:            # more chapters than slots: drop some
            alloc[pool.pop()] = 0
            extra += 1
        for i in range(extra):
            alloc[pool[i % len(pool)]] += 1
    chosen = []
    for n, k in alloc.items():
        mod, es = by_ch[n]
        for j in range(k):
            fresh = [e for e in es if family(mod, e[0]) not in used] or es
            e = pick_level_entry(rng, fresh, test_level(rng))
            used.add(family(mod, e[0]))
            chosen.append((mod, e))
    # rough difficulty ramp with randomness
    chosen.sort(key=lambda c: c[1][1] + rng.random() * 1.6)
    targets = balanced_targets(len(chosen), rng)
    probs = []
    avoid = set() if avoid is None else avoid
    for (mod, (tpl, lvl)), t in zip(chosen, targets):
        probs.append(make(tpl, lvl, rng, t, seen, mod.NUM, avoid))
    return probs


def build_diagnostic(mods, rng, seen, avoid=None):
    chosen = []
    for mod in mods:
        es = entries(mod)
        chosen.append((mod, pick_level_entry(rng, es, test_level(rng, (0.2, 0.6, 0.2)))))
    extra = [m for m in mods if m.PART == 4]
    rng.shuffle(extra)
    for mod in extra[: N_DIAG - len(chosen)]:
        fams = {family(m_, c[0]) for m_, c in chosen}
        es = [e for e in entries(mod) if family(mod, e[0]) not in fams] or entries(mod)
        chosen.append((mod, pick_level_entry(rng, es, 2)))
    chosen.sort(key=lambda c: c[0].NUM)
    targets = balanced_targets(len(chosen), rng)
    avoid = set() if avoid is None else avoid
    return [make(tpl, lvl, rng, t, seen, mod.NUM, avoid) for (mod, (tpl, lvl)), t in zip(chosen, targets)]


# ------------------------------------------------------------------ tex pieces
def toc_chapter(title, label=None):
    s = f"\\chapter*{{{title}}}\n\\phantomsection\\addcontentsline{{toc}}{{chapter}}{{{title}}}\n" \
        f"\\markboth{{{title}}}{{{title}}}\n"
    if label:
        s += f"\\label{{{label}}}\n"
    return s


def chref(mods_by_num):
    def f(i, p):
        return f"\\,{{\\scriptsize\\color{{mid}}ch.\\,{p.chapter}}}"
    return f


def diagnostic_tex(probs, mods_by_num):
    rows = []
    for i, p in enumerate(probs, 1):
        mod = mods_by_num[p.chapter]
        rows.append(f"{i} & {LETTERS[p.key]} & {mod.NUM} & {mod.TITLE} \\\\")
    half = (len(rows) + 1) // 2
    table = (r"\begin{center}\small\renewcommand{\arraystretch}{1.12}"
             r"\begin{tabular}{rclp{2.0in}}\toprule \# & Ans. & Ch. & Topic\\ \midrule" + "\n"
             + "\n".join(rows[:half]) + r"\bottomrule\end{tabular}" + "\n"
             r"\begin{tabular}{rclp{2.0in}}\toprule \# & Ans. & Ch. & Topic\\ \midrule" + "\n"
             + "\n".join(rows[half:]) + r"\bottomrule\end{tabular}\end{center}" + "\n")
    minutes = round(sum(1.2 if p.section == "AR" else 1.0 for p in probs))
    return "\n".join([
        toc_chapter("Diagnostic Test", "diag"),
        ("This test samples every chapter of the book. Take it before you begin "
         "studying, without a calculator, and try to finish in about "
         f"{minutes} minutes. Don't guess wildly---if you have no idea how to "
         "start a problem, leave it blank so that the result shows what you "
         "really need to study."),
        f"\\scoreline{{{len(probs)}}}{{{minutes}}}",
        problems_block(probs),
        "\\clearpage",
        "\\section*{Answers and Your Study Plan}",
        ("Check your answers against the table. Each row shows the chapter the "
         "question comes from. \\textbf{Circle the chapter number of every "
         "question you missed or left blank}---those chapters are your study "
         "plan. Work through them first, then the rest of the book in order."),
        table,
        "\\begin{infobox}{How did you do?}",
        "\\begin{tabular}{@{}ll@{}}",
        "26--30 correct & Strong. Skim the Key Concepts, do the challenge problems, then the practice tests.\\\\",
        "18--25 correct & Solid base. Study your circled chapters fully, then the rest.\\\\",
        "10--17 correct & Work through every chapter in order; take your time with the warm-ups.\\\\",
        "0--9 correct & Start at Chapter 1. Every chapter builds on the ones before it.",
        "\\end{tabular}",
        "\\end{infobox}",
        "\\section*{Explanations}",
        solutions_block(probs),
    ]) + "\n"


def score_table():
    return "\n".join([
        "\\begin{infobox}{Scoring your practice test}",
        "\\begin{tabular}{@{}lll@{}}",
        "\\textbf{Percent correct} & \\textbf{AR (of 30)} & \\textbf{MK (of 25)} \\\\",
        "90\\% or more --- excellent & 27--30 & 23--25 \\\\",
        "75--89\\% --- good & 23--26 & 19--22 \\\\",
        "60--74\\% --- keep practicing & 18--22 & 15--18 \\\\",
        "below 60\\% --- review the chapters & 0--17 & 0--14",
        "\\end{tabular}\\par\\smallskip",
        ("{\\small These bands measure your progress in this book only. Your real "
         "AFQT percentile depends on all four AFQT subtests and is scaled by the "
         "Department of Defense.}"),
        "\\end{infobox}",
    ]) + "\n"


def answer_sheet_tex(k):
    def col(title, n):
        rows = []
        for i in range(1, n + 1):
            bubbles = "".join(
                f"\\tikz[baseline=-0.6ex]\\node[circle,draw,inner sep=0pt,minimum size=1.2em,"
                f"font=\\sans\\scriptsize]{{{L}}};\\hspace{{0.55em}}" for L in LETTERS)
            rows.append(f"\\makebox[2em][r]{{\\sans\\small\\bfseries {i}}}\\hspace{{0.9em}}{bubbles}\\par")
        return (f"\\begin{{minipage}}[t]{{0.46\\linewidth}}{{\\sans\\bfseries {title}}}\\par\\medskip"
                "\\setlength{\\parskip}{0.6pt}" + "\n".join(rows) + "\\end{minipage}")
    return "\n".join([
        f"{{\\sans\\bfseries\\large Answer Sheet}}\\hfill{{\\small\\color{{mid}}Fill in one bubble per question. Photocopy this page to retake the test.}}\\par\\medskip",
        col("Part 1: Arithmetic Reasoning", AR_TEST) + "\\hfill" + col("Part 2: Mathematics Knowledge", MK_TEST),
        "\\clearpage",
    ])


def practice_test_tex(k, ar, mk, mods_by_num):
    f = chref(mods_by_num)
    return "\n".join([
        toc_chapter(f"Practice Test {k}", f"test{k}"),
        "\\begin{infobox}{Instructions}",
        ("This test has two parts, timed like the paper-and-pencil ASVAB. "
         f"\\textbf{{Part 1, Arithmetic Reasoning:}} {AR_TEST} questions, 36 minutes. "
         f"\\textbf{{Part 2, Mathematics Knowledge:}} {MK_TEST} questions, 24 minutes. "
         "No calculator. Use scratch paper. Answer every question---there is no "
         "penalty for guessing. Mark your answers on the answer sheet below."),
        "\\end{infobox}",
        answer_sheet_tex(k),
        f"\\section*{{Part 1: Arithmetic Reasoning}}",
        f"\\scoreline{{{AR_TEST}}}{{36}}",
        problems_block(ar),
        "\\clearpage",
        f"\\section*{{Part 2: Mathematics Knowledge}}",
        f"\\scoreline{{{MK_TEST}}}{{24}}",
        problems_block(mk),
        "\\clearpage",
        f"\\section*{{Answer Key: Practice Test {k}}}",
        "{\\small The small number after each answer is the chapter that teaches the skill.}",
        "\\subsection*{Part 1: Arithmetic Reasoning}",
        answer_key_tex(ar, extra=f),
        "\\subsection*{Part 2: Mathematics Knowledge}",
        answer_key_tex(mk, extra=f),
        score_table(),
        "\\section*{Explanations: Arithmetic Reasoning}",
        solutions_block(ar),
        "\\section*{Explanations: Mathematics Knowledge}",
        solutions_block(mk),
    ]) + "\n"


def squares_table():
    rows = []
    for i in range(1, 14):
        j = i + 13
        left = f"${i}^2 = {i * i}$"
        mid = f"${j}^2 = {j * j}$" if j <= 25 else ""
        right = f"${i}^3 = {i ** 3:,}$".replace(",", "{,}") if i <= 10 else ""
        rows.append(f"{left} & {mid} & {right} \\\\")
    return ("\\begin{tabular}{lll}\\toprule\n" + "\n".join(rows)
            + "\n\\bottomrule\\end{tabular}")


def fdp_table():
    data = [("1/2", "0.5", "50"), ("1/3", "0.333\\ldots", "33\\tfrac13"), ("2/3", "0.666\\ldots", "66\\tfrac23"),
            ("1/4", "0.25", "25"), ("3/4", "0.75", "75"), ("1/5", "0.2", "20"), ("2/5", "0.4", "40"),
            ("3/5", "0.6", "60"), ("4/5", "0.8", "80"), ("1/6", "0.1666\\ldots", "16\\tfrac23"),
            ("1/8", "0.125", "12.5"), ("3/8", "0.375", "37.5"), ("5/8", "0.625", "62.5"),
            ("7/8", "0.875", "87.5"), ("1/10", "0.1", "10"), ("1/20", "0.05", "5"),
            ("1/25", "0.04", "4"), ("1/50", "0.02", "2"), ("1/100", "0.01", "1")]
    rows = []
    for f, d, p in data:
        a, b = f.split("/")
        rows.append(f"$\\frac{{{a}}}{{{b}}}$ & ${d}$ & ${p}\\%$ \\\\")
    return ("\\begin{tabular}{ccc}\\toprule Fraction & Decimal & Percent\\\\\\midrule\n"
            + "\n".join(rows) + "\n\\bottomrule\\end{tabular}")


def glossary_tex():
    return "\n".join(f"\\textbf{{{t}.}} {d}\\par" for t, d in GLOSSARY)


def tracker_tex(mods):
    rows = []
    for mod in mods:
        n = sum(c for _, _, c in mod.PLAN)
        rows.append(f"{mod.NUM} & {mod.TITLE} & \\hspace{{3.2em}}/\\,{n} & & \\hspace{{3.2em}}/\\,{n} \\\\ \\hline")
    rows.append(f"-- & Diagnostic Test & \\hspace{{3.2em}}/\\,{N_DIAG} & & \\\\ \\hline")
    for k in range(1, N_TESTS + 1):
        rows.append(f"-- & Practice Test {k} & \\hspace{{3.2em}}/\\,{AR_TEST + MK_TEST} & & \\\\ \\hline")
    return ("\\begin{tabular}{|c|p{2.9in}|r|p{0.75in}|r|}\\hline\n"
            "\\textbf{Ch.} & \\textbf{Practice set} & \\textbf{Score} & \\textbf{Date} & \\textbf{Redo} \\\\ \\hline\n"
            + "\n".join(rows) + "\n\\end{tabular}")


def fill(text, mapping):
    for k, v in mapping.items():
        text = text.replace(f"<<{k}>>", str(v))
    if "<<" in text:
        raise ValueError("unfilled placeholder: " + text[text.index("<<"):][:40])
    return text


def closing_tex():
    return "\n".join([
        "\\clearpage\\thispagestyle{empty}",
        "\\vspace*{2in}",
        "\\begin{center}",
        "{\\sans\\bfseries\\LARGE Thank you, and good luck!\\par}",
        "\\bigskip",
        "\\begin{minipage}{4.8in}\\centering",
        ("If this workbook helped you prepare, please consider leaving a short "
         "review on Amazon. Reviews help other future service members find the "
         "right study materials---and they help the author keep improving this "
         "book.\\par\\medskip"),
        ("Found an error, or a solution you think could be explained better? "
         "Every report is read and fixed in the next printing."),
        "\\end{minipage}",
        "\\end{center}",
    ]) + "\n"


# ------------------------------------------------------------------ main
def generate_all(mods):
    seen: set[str] = set()
    chapters = {}
    for mod in mods:
        chapters[mod.NUM] = chapter_problems(mod, config.SEED + 101 * mod.NUM, seen)
    rng = random.Random(config.SEED + 7)
    # one shared set: no scenario or (template, answer) repeats across the
    # diagnostic and the four practice tests
    book_avoid: set = set()
    diag = build_diagnostic(mods, rng, seen, book_avoid)
    tests = []
    for k in range(1, N_TESTS + 1):
        rng = random.Random(config.SEED + 1000 * k)
        used: set = set()
        ar = build_section(mods, "AR", AR_TEST, rng, seen, used, book_avoid)
        mk = build_section(mods, "MK", MK_TEST, rng, seen, used, book_avoid)
        tests.append((ar, mk))
    return chapters, diag, tests


def qa_report(mods, chapters, diag, tests) -> str:
    allp: list[tuple[str, int, Problem]] = []
    for mod in mods:
        allp += [(f"ch{mod.NUM:02d}", i + 1, p) for i, p in enumerate(chapters[mod.NUM])]
    allp += [("diag", i + 1, p) for i, p in enumerate(diag)]
    for k, (ar, mk) in enumerate(tests, 1):
        allp += [(f"test{k}-AR", i + 1, p) for i, p in enumerate(ar)]
        allp += [(f"test{k}-MK", i + 1, p) for i, p in enumerate(mk)]
    keys = collections.Counter(LETTERS[p.key] for _, _, p in allp)
    secs = collections.Counter(p.section for _, _, p in allp)
    lv = collections.Counter(p.level for _, _, p in allp)
    traps = sum(1 for _, _, p in allp if any(w for _, w in p.choices))
    tips = sum(1 for _, _, p in allp if p.tip)
    figs = sum(1 for _, _, p in allp if p.figure)
    stems = collections.Counter(p.stem for _, _, p in allp)
    dup = [s for s, c in stems.items() if c > 1]
    tpls = collections.Counter(p.template for _, _, p in allp)
    lines = [
        f"TOTAL PROBLEMS: {len(allp)}",
        f"  chapters: {sum(len(v) for v in chapters.values())}, diagnostic: {len(diag)}, "
        f"tests: {sum(len(a) + len(m) for a, m in tests)}",
        f"answer letters: {dict(sorted(keys.items()))}",
        f"sections: {dict(secs)}   levels: {dict(sorted(lv.items()))}",
        f"with explained traps: {traps}   with tips: {tips}   with figures: {figs}",
        f"distinct templates used: {len(tpls)}",
        f"duplicate stems: {len(dup)}",
        "",
        "per chapter: n, AR/MK, letters",
    ]
    for mod in mods:
        ps = chapters[mod.NUM]
        lines.append(f"  ch{mod.NUM:02d} {mod.TITLE:<45} n={len(ps):<3} "
                     f"AR={sum(p.section == 'AR' for p in ps):<3} "
                     f"letters={dict(sorted(collections.Counter(LETTERS[p.key] for p in ps).items()))}")
    return "\n".join(lines) + "\n", allp


def write_ledger(allp):
    OUT.mkdir(exist_ok=True)
    with open(OUT / "answer-ledger.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["set", "number", "chapter", "template", "level", "section", "answer_letter",
                    "answer", "choices"])
        for setname, i, p in allp:
            w.writerow([setname, i, p.chapter, p.template, p.level, p.section, LETTERS[p.key],
                        p.choices[p.key][0], " | ".join(t for t, _ in p.choices)])


def book_tex(mods, chapters, diag, tests) -> str:
    mods_by_num = {m.NUM: m for m in mods}
    n_drill = sum(len(v) for v in chapters.values())
    front = fill((TEX / "front.tex").read_text(encoding="utf-8"), {
        "TITLE": config.TITLE, "SUBTITLE": config.SUBTITLE, "TAGLINE": config.TAGLINE,
        "AUTHOR": config.AUTHOR, "YEAR": config.YEAR, "EDITION": config.EDITION,
        "NPRACTICE": f"{n_drill:,}", "NCHAPTERS": len(mods),
    })
    back = fill((TEX / "back.tex").read_text(encoding="utf-8"), {
        "SQUARES": squares_table(), "FDP": fdp_table(), "GLOSSARY": glossary_tex(),
        "TRACKER": tracker_tex(mods),
    })
    body = ["\\begin{document}", "\\frontmatter", "\\pagestyle{fancy}",
            "\\setcounter{tocdepth}{0}"]
    # title + copyright + contents are in front.tex; switch to arabic after contents
    i = front.index("%% ---------------------------------------------------------------- how to use")
    body += [front[:i], "\\mainmatter", front[i:]]
    body.append(diagnostic_tex(diag, mods_by_num))
    part = None
    for mod in mods:
        if mod.PART != part:
            part = mod.PART
            listing = "\\\\[2pt]\n".join(
                f"\\makebox[2em][r]{{{m.NUM}}}\\quad {m.TITLE}" for m in mods if m.PART == part)
            body.append(f"\\bookpart{{{PARTS[part]}}}{{{PART_BLURB[part]}}}{{{listing}}}")
        body.append(f"\\setcounter{{chapter}}{{{mod.NUM - 1}}}")
        body.append(chapter_tex(mod, chapters[mod.NUM]))
    listing = "\\\\[2pt]\n".join(f"\\makebox[2em][r]{{}}\\quad Practice Test {k}"
                              for k in range(1, N_TESTS + 1))
    body.append("\\bookpart{Practice Tests}{Four full-length math sections in the "
                "paper-and-pencil format: 30 Arithmetic Reasoning questions in 36 minutes "
                "and 25 Mathematics Knowledge questions in 24 minutes.}{" + listing + "}")
    for k, (ar, mk) in enumerate(tests, 1):
        body.append(practice_test_tex(k, ar, mk, mods_by_num))
    body.append("\\backmatter")
    body.append(back)
    body.append(closing_tex())
    body.append("\\end{document}")
    pre = preamble().replace("\\hypersetup{pdfauthor={},pdftitle={ASVAB Math Workbook}}",
                             f"\\hypersetup{{pdfauthor={{{config.AUTHOR}}},"
                             f"pdftitle={{{config.TITLE}: {config.SUBTITLE}}}}}")
    return pre + "\n" + "\n".join(body) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex-only", action="store_true")
    ap.add_argument("--chapters", help="comma list for a partial test build, e.g. 6,7")
    a = ap.parse_args(argv)
    if a.chapters:
        mods = [m for n in a.chapters.split(",") for m in load_chapters(int(n))]
    else:
        mods = load_chapters()
    chapters, diag, tests = generate_all(mods)
    report, allp = qa_report(mods, chapters, diag, tests)
    OUT.mkdir(exist_ok=True)
    (OUT / "qa-report.txt").write_text(report, encoding="utf-8")
    write_ledger(allp)
    print(report)
    tex = book_tex(mods, chapters, diag, tests)
    if a.tex_only:
        BUILD.mkdir(exist_ok=True)
        (BUILD / "book.tex").write_text(tex, encoding="utf-8")
        print(BUILD / "book.tex")
        return
    pdf = compile_tex(tex, "book", passes=3)
    dest = OUT / "ASVAB-Math-Workbook-interior.pdf"
    shutil.copy(pdf, dest)
    print(dest)
    if len(allp) != 1000:
        print(f"WARNING: {len(allp)} problems, expected 1000", file=sys.stderr)


if __name__ == "__main__":
    main()
