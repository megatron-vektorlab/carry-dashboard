"""The book plan: 100 puzzle slots in seven chapters.

Each slot fixes the puzzle family (size, clue kinds, techniques) and the star
rating shown in the book.  Themes (story, names, categories, wording) are
written per slot in ``lp/themes/chN.py`` and checked with ``lp.themecheck``.
"""
from __future__ import annotations

BASE = ("fact", "only", "transfer", "either", "alldiff", "cmp", "pair")

FAMILIES = {
    # name: n, k, ordered (0 = no ordered category, 1 = exactly one), clue weights, extras
    "first3":  dict(n=3, k=2, ordered=0, kinds={"same": 0.5, "diff": 2, "either": 1, "nor": 1},
                    max_kind={"same": 1}),
    "first4":  dict(n=4, k=2, ordered=0, kinds={"same": 0.5, "diff": 2, "either": 1, "nor": 1},
                    max_kind={"same": 1}),
    "grid3":   dict(n=3, k=3, ordered=0, kinds={"same": 1, "diff": 2, "nor": 1, "either": 1},
                    max_kind={"same": 2}),
    "grid4":   dict(n=4, k=3, ordered=0, kinds={"same": 0.6, "diff": 2, "nor": 1, "either": 1.5, "pair": 1},
                    max_kind={"same": 2}),
    "lineup":  dict(n=None, k=2, ordered=1, lineup=True,
                    kinds={"same": 0.3, "diff": 0.6, "either": 0.8, "cmp": 2, "cmpd": 1.5, "adj": 1, "nadj": 1},
                    max_kind={"same": 1}),
    "days4":   dict(n=4, k=3, ordered=1, kinds={"same": 0.4, "diff": 1.5, "nor": 0.8, "either": 1, "cmp": 2,
                                                "cmpd": 1, "pair": 0.6},
                    max_kind={"same": 1}),
    "num43":   dict(n=4, k=3, ordered=1, kinds={"same": 0.3, "diff": 1, "nor": 0.8, "either": 1, "cmp": 2.5,
                                                "cmpd": 1.5, "pair": 1},
                    max_kind={"same": 1}),
    "num44":   dict(n=4, k=4, ordered=1, kinds={"same": 0.3, "diff": 1, "nor": 0.8, "either": 1.2, "cmp": 2.5,
                                                "cmpd": 1.5, "pair": 1.2},
                    max_kind={"same": 1, "pair": 2}),
    "case54":  dict(n=5, k=4, ordered=1, kinds={"same": 0.3, "diff": 1, "nor": 0.8, "either": 1.5, "cmp": 2.5,
                                                "cmpd": 1, "pair": 1.5, "alldiff": 0.4},
                    max_kind={"same": 1, "alldiff": 1, "pair": 3}),
    "suppose": dict(n=5, k=4, ordered=1, trial=True,
                    kinds={"same": 0.3, "diff": 1, "nor": 0.7, "either": 1.5, "cmp": 2.5, "cmpd": 1, "pair": 1.5,
                           "nadj": 0.0, "alldiff": 0.4},
                    max_kind={"same": 1, "alldiff": 1, "pair": 3}),
    "liars":   dict(n=None, k=None, ordered=0),
}

CHAPTERS = [
    # (number, title, skill line, [(family, count, stars, extra)])
    (1, "First Clues", "Reading a clue, marking O and X, and the only choice left",
     [("first3", 5, 1, {}), ("first4", 5, 1, {})]),
    (2, "The Full Grid", "The staircase grid and carrying facts from one box to another",
     [("grid3", 8, 1, {}), ("grid4", 12, 2, {})]),
    (3, "First, Next, Last", "Line-ups, before and after, and exact gaps",
     [("lineup", 4, 2, {"n": 4}), ("lineup", 4, 2, {"n": 5}), ("days4", 8, 3, {})]),
    (4, "Truth or Fib?", "Testing one suspect at a time against what everyone says",
     [("liars", 12, 3, {})]),
    (5, "Two Clues at Once", "Number clues, comparisons, and clues that work as a team",
     [("num43", 6, 3, {}), ("num44", 14, 4, {})]),
    (6, "Case Files", "Five-suspect cases and your first careful 'Suppose'",
     [("case54", 8, 4, {}), ("suppose", 9, 5, {})]),
    (7, "The Lighthouse Affair", "Everything at once: the five-part finale",
     [("suppose", 5, 5, {})]),
]


def slots():
    out = []
    no = 1
    for ch, title, skill, groups in CHAPTERS:
        for fam, count, stars, extra in groups:
            f = dict(FAMILIES[fam])
            f.update(extra)
            for _ in range(count):
                out.append(dict(no=no, chapter=ch, family=fam, stars=stars, n=f.get("n"), k=f.get("k"),
                                ordered=f.get("ordered", 0), lineup=f.get("lineup", False)))
                no += 1
    assert no == 101, no
    return out


if __name__ == "__main__":
    import collections
    S = slots()
    print(collections.Counter(s["stars"] for s in S))
    for s in S:
        print(s)
