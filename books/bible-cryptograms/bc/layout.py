"""Page geometry shared by the Python planner and layout/book.typ (keep both in sync).

All sizes in inches.  `lines_needed` wraps a cipher exactly like Typst does (whole words,
never split); `height` is the height of one puzzle block, used to plan which puzzles share
a page.
"""
from __future__ import annotations

PAGE_W, PAGE_H = 8.5, 11.0
INSIDE, OUTSIDE, TOP, BOTTOM = 0.9, 0.45, 0.72, 0.7
TEXT_WIDTH = PAGE_W - INSIDE - OUTSIDE            # 7.15
BODY_HEIGHT = PAGE_H - TOP - BOTTOM               # 9.58

CELL, PUNCT, WORD_GAP = 0.31, 0.15, 0.20
ANSWER_H, CODE_H, STACK_GAP, LINE_GAP = 0.37, 0.28, 0.03, 0.12
LINE_H = ANSWER_H + STACK_GAP + CODE_H + LINE_GAP  # 0.75
MAX_LINES = 9
MIN_LINES = 3


def lines_needed(cipher_text: str) -> int:
    lines, x = 1, 0.0
    for w in cipher_text.split(" "):
        if not w:
            continue
        width = sum(CELL if ch.isalpha() else PUNCT for ch in w)
        if x == 0:
            x = width
        elif x + WORD_GAP + width <= TEXT_WIDTH + 1e-9:
            x += WORD_GAP + width
        else:
            lines += 1
            x = width
    return lines

# Measured from the Typst output (bc.qa re-checks it): one puzzle block is
# BLOCK_BASE + LINE_H * lines tall, and consecutive blocks are BLOCK_GAP apart.
BLOCK_BASE, BLOCK_GAP = 0.974, 0.283
FIRST_TOP = 0.748                       # top of the first puzzle header on a page
PAGE_LIMIT = PAGE_H - BOTTOM - 0.05     # lowest allowed text bottom, with a small safety margin


def fits(lines_list: list[int]) -> bool:
    """Do these puzzles fit on one page, in this order?"""
    if not lines_list:
        return True
    total = sum(BLOCK_BASE + LINE_H * n for n in lines_list) + BLOCK_GAP * (len(lines_list) - 1)
    return FIRST_TOP + total <= PAGE_LIMIT


def pack(items: list[dict]) -> list[list[dict]]:
    """First-fit decreasing: items need a 'lines' key; returns pages (lists of items)."""
    pages: list[list[dict]] = []
    for it in sorted(items, key=lambda x: -x["lines"]):
        for pg in pages:
            if fits([x["lines"] for x in pg] + [it["lines"]]):
                pg.append(it)
                break
        else:
            pages.append([it])
    for pg in pages:
        pg.sort(key=lambda x: -x["lines"])
    return pages
