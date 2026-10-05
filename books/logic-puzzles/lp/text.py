"""Turn engine puzzles into English: themed clues, hints and explained solutions.

A *theme* is a dict:

    {
      "title": "The Pet Show",
      "story": "Four friends entered their pets in the town pet show. ...",
      "entity": ["friend", "friends"],
      "cats": [
        {"label": "Owner", "kind": "name", "values": ["Ava", "Ben", ...]},
        {"label": "Pet", "values": ["beagle", "cat", ...],
         "ref": "the {v} owner",            # noun phrase for "whoever has this value"
         "pred": "owns the {v}",            # predicate: "<subject> owns the beagle"
         "neg": "does not own the {v}",
         "either": "owns either the {a} or the {b}",
         "short": "the {v}"},               # short label used in explanations
        {"label": "Age", "ordered": True, "nums": [8, 9, 10, 11, 12],
         "fmt": "{x}",                      # how a number is written
         "ref": "the {x}-year-old", "pred": "is {x} years old", "neg": "is not {x}",
         "either": "is either {a} or {b} years old", "short": "age {x}",
         "more": "is older than {y}", "less": "is younger than {y}",
         "dmore": "is exactly {d} older than {y}", "dless": "is exactly {d} younger than {y}",
         "dunit": ["year", "years"]}
      ]
    }

Values beyond the puzzle size are allowed; :func:`instantiate` picks ``n``
of them (consecutive, evenly spaced numbers for ordered categories).
"""
from __future__ import annotations

import random
import re

from .engine import Clue


def cap(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s


class Bound:
    """A theme instantiated for one puzzle (n values per category)."""

    def __init__(self, theme: dict, n: int, rng: random.Random, k: int | None = None):
        self.theme = theme
        cats = theme["cats"][: (k or len(theme["cats"]))]
        self.cats = []
        for c in cats:
            c = dict(c)
            vals = list(c["values"]) if "values" in c else None
            if c.get("ordered"):
                nums = list(c["nums"])
                start = rng.randrange(0, len(nums) - n + 1)
                c["nums"] = nums[start:start + n]
                steps = {b - a for a, b in zip(c["nums"], c["nums"][1:])}
                if len(steps) > 1:
                    raise ValueError(f"{c['label']}: ordered values must be evenly spaced")
                c["step"] = steps.pop() if steps else 1
                fmt = c.get("fmt", "{x}")
                c["values"] = [fmt.format(x=v) for v in c["nums"]]
            else:
                if len(vals) < n:
                    raise ValueError(f"{c['label']}: needs {n} values")
                pick = rng.sample(vals, n)
                # keep a stable, readable order in the grid
                c["values"] = sorted(pick, key=vals.index)
            self.cats.append(c)
        self.n = n
        self.k = len(self.cats)
        self.ordered = tuple(i for i, c in enumerate(self.cats) if c.get("ordered"))
        ent = theme.get("entity", ["person", "people"])
        self.entity, self.entities = ent[0], ent[1]

    # ---- phrases
    def val(self, it):
        return self.cats[it[0]]["values"][it[1]]

    def _fill(self, tpl, it):
        c = self.cats[it[0]]
        return tpl.format(v=self.val(it), x=self.val(it))

    def ref(self, it):
        c = self.cats[it[0]]
        if c.get("kind") == "name":
            return self.val(it)
        return self._fill(c.get("ref", "the " + self.entity + " with the {v}"), it)

    def pred(self, it):
        c = self.cats[it[0]]
        if c.get("kind") == "name":
            return "is " + self.val(it)
        return self._fill(c.get("pred", "has the {v}"), it)

    def neg(self, it):
        c = self.cats[it[0]]
        if c.get("kind") == "name":
            return "is not " + self.val(it)
        return self._fill(c.get("neg", "does not have the {v}"), it)

    def short(self, it):
        c = self.cats[it[0]]
        if c.get("kind") == "name":
            return self.val(it)
        return self._fill(c.get("short", "{v}"), it)

    def either(self, b1, b2):
        c = self.cats[b1[0]]
        if c.get("kind") == "name":
            return f"is either {self.val(b1)} or {self.val(b2)}"
        return c.get("either", "has either the {a} or the {b}").format(a=self.val(b1), b=self.val(b2))

    def diff_words(self, o, d):
        c = self.cats[o]
        amount = d * c["step"]
        unit = c.get("dunit", ["", ""])
        u = unit[0] if amount == 1 else unit[1]
        return f"{amount} {u}".strip()

    # ---- clues
    def subject_first(self, a, b):
        """Prefer names (then non-ordered items) as the grammatical subject."""
        def rank(it):
            c = self.cats[it[0]]
            return 0 if c.get("kind") == "name" else (2 if c.get("ordered") else 1)
        return (a, b) if rank(a) <= rank(b) else (b, a)

    def clue_text(self, cl: Clue, rng: random.Random) -> str:
        if cl.kind == "same":
            a, b = self.subject_first(*cl.items)
            return f"{cap(self.ref(a))} {self.pred(b)}."
        if cl.kind == "diff":
            a, b = self.subject_first(*cl.items)
            return f"{cap(self.ref(a))} {self.neg(b)}."
        if cl.kind == "either":
            a, b1, b2 = cl.items
            return f"{cap(self.ref(a))} {self.either(b1, b2)}."
        if cl.kind == "cmp":
            a, b = cl.items
            c = self.cats[cl.cat]
            if cl.op == ">":
                return f"{cap(self.ref(a))} {c['more'].format(y=self.ref(b))}."
            if cl.op == "<":
                return f"{cap(self.ref(a))} {c['less'].format(y=self.ref(b))}."
            words = self.diff_words(cl.cat, cl.d)
            if rng.random() < 0.5:
                return f"{cap(self.ref(a))} {c['dmore'].format(d=words, y=self.ref(b))}."
            return f"{cap(self.ref(b))} {c['dless'].format(d=words, y=self.ref(a))}."
        if cl.kind == "pair":
            a1, a2, b1, b2 = cl.items
            return (f"Of {self.ref(a1)} and {self.ref(a2)}, one {self.pred(b1)} "
                    f"and the other {self.pred(b2)}.")
        if cl.kind == "alldiff":
            refs = [self.ref(it) for it in cl.items]
            words = {3: "three", 4: "four", 5: "five"}[len(refs)]
            return f"{cap(', '.join(refs[:-1]))}, and {refs[-1]} are {words} different {self.entities}."
        raise ValueError(cl.kind)


# ---------------------------------------------------------------- explanations
def _join(words):
    words = list(words)
    if len(words) <= 1:
        return "".join(words)
    if len(words) == 2:
        return f"{words[0]} and {words[1]}"
    return ", ".join(words[:-1]) + f", and {words[-1]}"


def _clue_no(step, numbers):
    c = step.info.get("clue")
    return numbers[c] if c is not None else None


def why_not(B, d, numbers, a, b):
    """Short reason why cell (a, b) is X, as (group key, phrase about b)."""
    t = d.steps[d.cause[(a, b)]] if (a, b) in d.cause else None
    if t is None:
        return ("given", B.short(b))
    n = _clue_no(t, numbers)
    if t.places and t.kind not in ("transfer",) or (t.kind == "transfer" and t.places):
        # side effect of an O placed in the same row or column
        x, y = t.places[0]
        other = None
        if b in (x, y):
            other = y if b == x else x
        if other is not None and other != a and other[0] == a[0]:
            return (f"taken:{B.short(b)}", f"{B.short(b)} already goes with {B.short(other)}")
        if a in (x, y):
            other = y if a == x else x
            return (f"has:{B.short(other)}", f"{B.short(a)} already goes with {B.short(other)}")
    if t.kind == "transfer":
        src, dst = t.info["link"]
        return (f"via:{B.short(src)}", f"{B.short(b)} (ruled out through {B.short(src)})")
    if t.kind == "trial":
        return ("trial", f"{B.short(b)} (by the case check above)")
    if n is not None:
        return (f"clue:{n}", B.short(b))
    return ("other", B.short(b))


def solution_lines(B: Bound, clues, d, numbers):
    """One line per O placed, each with the reasons that matter."""
    lines = []
    for idx, st in enumerate(d.steps):
        i, k = st.info, st.kind
        if k == "trial":
            a, b = i["assume"]
            lines.append((False, f"Try {B.short(a)} with {B.short(b)}: following the clues from there "
                         f"leads to a contradiction, so {B.short(a)} is not with {B.short(b)}."))
            continue
        if not st.places:
            continue
        a, b = st.places[0]
        if k == "fact":
            x, y = B.subject_first(a, b)
            lines.append((False, f"Clue {numbers[i['clue']]} says directly that {B.short(x)} goes with {B.short(y)}."))
        elif k == "only":
            a, p, c = i["item"], i["partner"], i["cat"]
            groups = {}
            for v in range(B.n):
                o = (c, v)
                if o == p:
                    continue
                key, phrase = why_not(B, d, numbers, a, o)
                groups.setdefault(key, []).append((o, phrase))
            parts, taken, vias = [], [], {}
            for key, lst in groups.items():
                if key.startswith("clue:"):
                    parts.append(f"clue {key[5:]} rules out {_join(B.short(o) for o, _ in lst)}")
                elif key.startswith("taken:") or key.startswith("has:"):
                    taken.extend(ph for _, ph in lst)
                elif key.startswith("via:"):
                    vias.setdefault(key[4:], []).extend(o for o, _ in lst)
                else:
                    parts.extend(ph for _, ph in lst)
            for src, objs in vias.items():
                parts.append(f"{_join(B.short(o) for o in objs)} {'is' if len(objs) == 1 else 'are'} "
                             f"already ruled out for {src}")
            if not parts:
                lines.append((True, f"{cap(B.short(a))} must go with {B.short(p)}, the only choice left."))
                continue
            if len(taken) == 1:
                parts.append(taken[0])
            elif taken:
                parts.append("the other choices are already taken")
            lines.append((False, f"{cap(B.short(a))} must go with {B.short(p)}: {_join(parts)}."))
        elif k == "transfer":
            (src, dst), x = i["link"], i["via"]
            lines.append((True, f"{cap(B.short(dst))} goes with {B.short(src)}, so {B.short(dst)} also goes with "
                         f"{B.short(x)}."))
        elif k == "either":
            lines.append((False, f"Clue {numbers[i['clue']]} allows only {B.short(i['out'])} or {B.short(i['chosen'])} "
                         f"for {B.short(clues[i['clue']].items[0])}; {B.short(i['out'])} is out, "
                         f"so it is {B.short(i['chosen'])}."))
        elif k == "pair":
            if i.get("part") == "other":
                (x, y), (p, q) = i["known"], i["chosen"]
                lines.append((False, f"Clue {numbers[i['clue']]} pairs them up: since {B.short(x)} goes with "
                             f"{B.short(y)}, {B.short(p)} goes with {B.short(q)}."))
            else:
                (x, y), (_, z) = i["out"], i["chosen"]
                lines.append((False, f"Clue {numbers[i['clue']]}: {B.short(x)} is not with {B.short(y)}, "
                             f"so {B.short(x)} must be with {B.short(z)}."))
        else:
            lines.append((False, f"Clue {numbers[i['clue']]} gives {B.short(a)} with {B.short(b)}."))
    # collapse the trivial tail: once only bookkeeping is left, say so once
    last = max((j for j, (triv, _) in enumerate(lines) if not triv), default=-1)
    out = [ln for _, ln in lines[:last + 1]]
    if last + 1 < len(lines):
        out.append("Every remaining match is now the only choice left in its row; fill them in "
                   "and the grid is complete.")
    return [re.sub(r"\s+", " ", ln) for ln in out]


KIND_HINT = {
    "same": "it gives you a direct match to mark with an O",
    "diff": "mark the X it gives you, then look for a row with only one choice left",
    "either": "it leaves only two choices for one item, so you can cross out all the others",
    "cmp": "ask which values are impossible: the larger one cannot be the smallest value, "
           "and the smaller one cannot be the largest",
    "pair": "it names two items and two options, so each item is limited to those two",
    "alldiff": "it tells you several items belong to different people, so mark X between them",
}


def hints(B: Bound, clues, d, numbers):
    """Three graded hints: where to start, the first placement, a mid-way fact."""
    first_clue = None
    for st in d.steps:
        if "clue" in st.info:
            first_clue = st.info["clue"]
            break
    placements = [st for st in d.steps if st.places]
    h1 = (f"Start with clue {numbers[first_clue]}: {KIND_HINT[clues[first_clue].kind]}."
          if first_clue is not None else "Start with the clue that names a direct match.")
    a, b = placements[0].places[0]
    x, y = B.subject_first(a, b)
    h2 = f"Your first O: {B.short(x)} goes with {B.short(y)}. Mark it, then cross out the rest of that row and column."
    mid = placements[min(len(placements) - 1, max(1, len(placements) * 2 // 5))]
    a, b = mid.places[0]
    x, y = B.subject_first(a, b)
    h3 = f"Further on, you can show that {B.short(x)} goes with {B.short(y)}. From there, each remaining row has one choice left."
    return [h1, h2, h3]
