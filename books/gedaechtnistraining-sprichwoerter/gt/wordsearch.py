"""Word search grids (Suchsel) for older readers.

Words run only left-to-right and top-to-bottom (level 3 adds diagonals down to the right);
nothing is written backwards. Every word must occur exactly once in the finished grid, in
any of the directions a reader might check, and no offensive word may appear by accident.
"""
from __future__ import annotations

import random

DIRS = {1: [(0, 1)], 2: [(0, 1), (1, 0)], 3: [(0, 1), (1, 0), (1, 1)]}
ALL_DIRS = [(0, 1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1), (-1, 1)]
# filler letters weighted like German text (umlauts rare, no Q/X/Y)
FILL = ("E" * 17 + "N" * 10 + "I" * 8 + "S" * 7 + "R" * 7 + "A" * 7 + "T" * 6 + "D" * 5 + "H" * 5
        + "U" * 4 + "L" * 3 + "C" * 3 + "G" * 3 + "M" * 3 + "O" * 3 + "B" * 2 + "W" * 2 + "F" * 2
        + "K" * 2 + "Z" + "P" + "V" + "Ä" + "Ö" + "Ü" + "J")
BAD = ["NAZI", "HITLER", "ARSCH", "FICK", "HURE", "NEGER", "SCHEISS", "PISS", "KACK", "FOTZE",
       "TOD", "MORD", "SAU", "DOOF", "BLOED", "BLÖD", "SEX", "TITTE", "PENIS", "NUTTE"]
BAD_SHORT_OK = {"SAU", "TOD", "SEX"}   # short words: checked only in the reading directions


def _count(grid: list[list[str]], word: str, dirs) -> int:
    n = len(grid)
    m = len(grid[0])
    c = 0
    for r in range(n):
        for k in range(m):
            for dr, dk in dirs:
                ok = True
                for i, ch in enumerate(word):
                    rr, kk = r + dr * i, k + dk * i
                    if not (0 <= rr < n and 0 <= kk < m) or grid[rr][kk] != ch:
                        ok = False
                        break
                if ok:
                    c += 1
    return c


def make(words: list[str], size: int, level: int, seed: str, tries: int = 400) -> dict:
    """Place `words` (already upper case, ß -> SS) in a size x size grid.
    Returns {grid: [[str]], places: [{word, row, col, dr, dc}]}."""
    rnd = random.Random(seed)
    order = sorted(words, key=len, reverse=True)
    for attempt in range(tries):
        grid = [[""] * size for _ in range(size)]
        places = []
        ok = True
        for w in order:
            if len(w) > size:
                raise ValueError(f"{w} is longer than the grid")
            spots = []
            for dr, dc in DIRS[level]:
                for r in range(size - (len(w) - 1) * dr):
                    for c in range(size - (len(w) - 1) * dc):
                        overlap, fits = 0, True
                        for i, ch in enumerate(w):
                            g = grid[r + dr * i][c + dc * i]
                            if g and g != ch:
                                fits = False
                                break
                            overlap += g == ch
                        if fits:
                            spots.append((overlap, rnd.random(), r, c, dr, dc))
            if not spots:
                ok = False
                break
            # a little overlap is nice, but mostly spread the words out
            spots.sort(reverse=True)
            pick = spots[0] if (spots[0][0] > 0 and rnd.random() < 0.35) else rnd.choice(spots)
            _, _, r, c, dr, dc = pick
            for i, ch in enumerate(w):
                grid[r + dr * i][c + dc * i] = ch
            places.append({"word": w, "row": r, "col": c, "dr": dr, "dc": dc})
        if not ok:
            continue
        for r in range(size):
            for c in range(size):
                if not grid[r][c]:
                    grid[r][c] = rnd.choice(FILL)
        # checks: each word exactly once in any direction; no offensive word
        if any(_count(grid, w, ALL_DIRS) != 1 for w in words):
            continue
        if any(_count(grid, b, ALL_DIRS if b not in BAD_SHORT_OK else DIRS[level]) for b in BAD
               if not any(b in w for w in words)):
            continue
        places.sort(key=lambda p: words.index(p["word"]))
        return {"grid": grid, "places": places, "size": size, "level": level}
    raise RuntimeError(f"could not build a word search for {words}")
