"""Compile one chapter to build/preview_chNN.pdf (and optional PNG pages).

    .venv/bin/python -m asvab.preview 6
    .venv/bin/python -m asvab.preview 6 --png     # also build/preview_ch06-*.png
"""
from __future__ import annotations

import argparse
import subprocess
import sys

from .generate import chapter_problems, load_chapters
from .render import BUILD, chapter_tex, compile_tex, standalone


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", type=int)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--png", action="store_true")
    a = ap.parse_args(argv)
    mods = [m for m in load_chapters(a.chapter) if m.NUM == a.chapter]
    if not mods:
        sys.exit("no such chapter")
    mod = mods[0]
    probs = chapter_problems(mod, a.seed, set())
    body = f"\\setcounter{{chapter}}{{{mod.NUM - 1}}}\n" + chapter_tex(mod, probs)
    name = f"preview_ch{mod.NUM:02d}"
    pdf = compile_tex(standalone(body), name)
    print(pdf)
    if a.png:
        subprocess.run(["pdftoppm", "-r", "70", "-png", str(pdf), str(BUILD / name)], check=True)
        print(sorted(str(p) for p in BUILD.glob(f"{name}-*.png")))


if __name__ == "__main__":
    main()
