"""Vectorised solution space: every candidate solution held as numpy arrays.

For n entities and k categories there are (n!)^(k-1) candidate solutions
(1.7 million for 5 x 4).  Each clue becomes a boolean mask over them, so
uniqueness checks and redundancy tests are a few array operations instead of
a fresh backtracking search.  Used for k <= 4 and n <= 5; bigger puzzles fall
back to :func:`engine.count_solutions`.
"""
from __future__ import annotations

import itertools
from functools import lru_cache

import numpy as np


def feasible(n, k):
    return k <= 4 and n <= 5 or (k <= 3 and n <= 6)


@lru_cache(maxsize=8)
def _space(n, k):
    perms = np.array(list(itertools.permutations(range(n))), dtype=np.int8)   # perms[p, e] = value of entity e
    inv = np.argsort(perms, axis=1).astype(np.int8)                           # inv[p, v] = entity holding v
    P, m = len(perms), k - 1
    idx = np.indices((P,) * m, dtype=np.int16).reshape(m, -1) if m else np.zeros((0, 1), np.int16)
    return perms, inv, idx


class Space:
    def __init__(self, n, k):
        self.n, self.k = n, k
        self.perms, self.inv, self.idx = _space(n, k)
        self.size = self.idx.shape[1] if k > 1 else 1
        self._own = {}
        self._val = {}

    def owner(self, it):
        c, v = it
        if c == 0:
            return np.int8(v)
        key = (c, v)
        if key not in self._own:
            self._own[key] = self.inv[self.idx[c - 1], v]
        return self._own[key]

    def value(self, o, it):
        """Value (index) in ordered category o of the owner of item it."""
        if it[0] == o:
            return np.int8(it[1])
        own = self.owner(it)
        p = self.idx[o - 1].astype(np.int32)
        return self.perms.reshape(-1)[p * self.n + own]

    def mask(self, cl):
        O = self.owner
        if cl.kind == "same":
            a, b = cl.items
            return np.broadcast_to(O(a) == O(b), (self.size,))
        if cl.kind == "diff":
            a, b = cl.items
            return np.broadcast_to(O(a) != O(b), (self.size,))
        if cl.kind == "either":
            a, b1, b2 = cl.items
            return np.broadcast_to((O(a) == O(b1)) | (O(a) == O(b2)), (self.size,))
        if cl.kind == "nor":
            a, b1, b2 = cl.items
            return np.broadcast_to((O(a) != O(b1)) & (O(a) != O(b2)), (self.size,))
        if cl.kind == "cmp":
            a, b = cl.items
            va = self.value(cl.cat, a).astype(np.int16)
            vb = self.value(cl.cat, b).astype(np.int16)
            if cl.op == ">":
                r = va > vb
            elif cl.op == "<":
                r = va < vb
            elif cl.op == "adj":
                r = np.abs(va - vb) == 1
            elif cl.op == "nadj":
                r = np.abs(va - vb) > 1
            else:
                r = (va - vb) == cl.d
            return np.broadcast_to(r, (self.size,))
        if cl.kind == "pair":
            a1, a2, b1, b2 = cl.items
            r = (O(a1) != O(a2)) & (O(b1) != O(b2)) & (
                ((O(a1) == O(b1)) & (O(a2) == O(b2))) | ((O(a1) == O(b2)) & (O(a2) == O(b1))))
            return np.broadcast_to(r, (self.size,))
        if cl.kind == "alldiff":
            r = np.ones(self.size, bool)
            for x, y in itertools.combinations(cl.items, 2):
                r = r & (O(x) != O(y))
            return r
        raise ValueError(cl.kind)

    def solution(self, row):
        sol = [tuple(range(self.n))]
        for c in range(1, self.k):
            sol.append(tuple(int(x) for x in self.perms[self.idx[c - 1, row]]))
        return sol
