"""Substitution ciphers and an exhaustive solver over the King James vocabulary.

A puzzle is the verse in capitals with every letter replaced by another letter.
Rules (the same as printed in the book):
  * one key per puzzle, no letter ever stands for itself;
  * spaces, punctuation and apostrophes are kept as they are.

`count_solutions` proves how many readings fit a puzzle: it tries every assignment of
King James words to the cipher words that is consistent with one substitution key and
with the given (hint) letters, and stops at `limit`.  A puzzle goes into the book only
when exactly one reading fits.
"""
from __future__ import annotations

import collections
import functools
import random
import re
import string

from . import kjv

AZ = string.ascii_uppercase
WORD_RE = re.compile(r"[A-Z]+(?:['\-][A-Z]+)*")


def make_key(seed) -> dict[str, str]:
    """plain -> cipher; a derangement (no letter maps to itself), reproducible from `seed`."""
    rng = random.Random(f"key:{seed}")
    while True:
        perm = list(AZ)
        rng.shuffle(perm)
        if all(p != c for p, c in zip(AZ, perm)):
            # also avoid keys that keep alphabet neighbours (A->B, B->C ...) in more than 2 places
            shifts = sum(1 for p, c in zip(AZ, perm) if (ord(c) - ord(p)) % 26 in (1, 25))
            if shifts <= 2:
                return dict(zip(AZ, perm))


def encrypt(plain: str, key: dict[str, str]) -> str:
    return "".join(key.get(ch, ch) for ch in plain.upper())


def words(text: str) -> list[str]:
    return WORD_RE.findall(text.upper())


def pattern(word: str) -> tuple:
    seen: dict[str, int] = {}
    return tuple(seen.setdefault(ch, len(seen)) if ch.isalpha() else ch for ch in word)


@functools.lru_cache(maxsize=1)
def vocabulary() -> dict[tuple, list[str]]:
    """Every distinct word of the KJV (all copies), grouped by letter pattern."""
    vocab = set()
    for src in kjv.load().values():
        for t in src.values():
            vocab.update(words(t))
    by_pat: dict[tuple, list[str]] = collections.defaultdict(list)
    for w in sorted(vocab):
        by_pat[pattern(w)].append(w)
    return dict(by_pat)


def count_solutions(cipher_text: str, given: dict[str, str], limit: int = 2, node_limit: int = 2_000_000):
    """Number of KJV-word readings of `cipher_text` consistent with one key.

    given: cipher letter -> plain letter (the hint letters printed in the puzzle).
    Returns (count, solutions[:limit], exhausted) where exhausted=False means the node
    limit was hit before the search finished (treat as "not proven unique").
    """
    vocab = vocabulary()
    cwords = sorted(set(words(cipher_text)), key=len, reverse=True)
    cands: dict[str, list[str]] = {}
    for cw in cwords:
        lst = []
        for w in vocab.get(pattern(cw), []):
            ok = True
            for c, p in zip(cw, w):
                if not c.isalpha():
                    continue
                if c == p:                              # no letter stands for itself
                    ok = False
                    break
                g = given.get(c)
                if g is not None and g != p:
                    ok = False
                    break
                if g is None and p in given.values():   # plain letter already used by a hint
                    ok = False
                    break
            if ok:
                lst.append(w)
        cands[cw] = lst
        if not lst:
            return 0, [], True

    c2p = dict(given)
    p2c = {p: c for c, p in given.items()}
    sols: list[dict[str, str]] = []
    nodes = 0
    remaining = set(cwords)

    def fits(cw, w):
        for c, p in zip(cw, w):
            if not c.isalpha():
                continue
            a = c2p.get(c)
            if a is not None:
                if a != p:
                    return False
            else:
                b = p2c.get(p)
                if b is not None and b != c:
                    return False
        # inside one word the pattern already guarantees consistency
        return True

    def search():
        nonlocal nodes
        if len(sols) >= limit or nodes > node_limit:
            return
        nodes += 1
        if not remaining:
            sols.append(dict(c2p))
            return
        best, best_opts = None, None
        for cw in remaining:
            opts = [w for w in cands[cw] if fits(cw, w)]
            if best_opts is None or len(opts) < len(best_opts):
                best, best_opts = cw, opts
                if len(opts) <= 1:
                    break
        if not best_opts:
            return
        remaining.discard(best)
        for w in best_opts:
            added = []
            for c, p in zip(best, w):
                if c.isalpha() and c not in c2p:
                    c2p[c] = p
                    p2c[p] = c
                    added.append(c)
            search()
            for c in added:
                del p2c[c2p[c]]
                del c2p[c]
            if len(sols) >= limit or nodes > node_limit:
                break
        remaining.add(best)

    search()
    return len(sols), sols, nodes <= node_limit


def forced_solve(cipher_text: str, given: dict[str, str]):
    """Human-style solving: repeatedly fill any cipher word that has exactly one KJV word
    left that fits.  Returns (fraction of letters solved, number of rounds)."""
    vocab = vocabulary()
    c2p = dict(given)
    cws = set(words(cipher_text))
    rounds = 0
    while True:
        progress = False
        p2c = {p: c for c, p in c2p.items()}
        for cw in sorted(cws):
            if all((not c.isalpha()) or c in c2p for c in cw):
                continue
            opts = []
            for w in vocab.get(pattern(cw), []):
                ok = True
                for c, p in zip(cw, w):
                    if not c.isalpha():
                        continue
                    if c == p or (c in c2p and c2p[c] != p) or (c not in c2p and p in p2c):
                        ok = False
                        break
                if ok:
                    opts.append(w)
                    if len(opts) > 1:
                        break
            if len(opts) == 1:
                for c, p in zip(cw, opts[0]):
                    if c.isalpha() and c not in c2p:
                        c2p[c] = p
                        p2c[p] = c
                progress = True
        rounds += 1
        if not progress:
            break
    letters_all = [c for c in cipher_text if c.isalpha()]
    solved = sum(1 for c in letters_all if c in c2p)
    return solved / max(1, len(letters_all)), rounds
