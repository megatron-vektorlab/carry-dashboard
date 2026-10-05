"""Logic-grid puzzle engine.

A puzzle has ``n`` entities and ``k`` categories.  Category 0 names the
entities (usually people); every other category assigns each entity exactly
one of its ``n`` values.  An *item* is a (category, value) pair; the *owner*
of an item is the entity it belongs to.

Three independent pieces live here:

* :func:`count_solutions` — exhaustive search (with pruning) that proves a
  clue set has exactly one solution;
* :class:`Deducer` — a human-style solver on the classic O/X grid that only
  uses rules a beginner can follow, logs every step in plain English, and
  rates difficulty;
* :func:`generate` — builds a random solution, picks clues until the puzzle
  is unique, removes redundant clues, and keeps it only if the Deducer can
  solve it within the allowed rule set (no guessing for beginners).
"""
from __future__ import annotations

import itertools
import random

import numpy as np
from dataclasses import dataclass, field

Item = tuple  # (category, value index)


# ---------------------------------------------------------------- clues
@dataclass(frozen=True)
class Clue:
    kind: str                 # same | diff | nor | either | cmp | pair | alldiff
    items: tuple              # items involved (see kinds below)
    cat: int = -1             # ordered category for cmp
    op: str = ""              # '>' '<' or 'd' (exact difference, items[0] - items[1] = d)
    d: int = 0                # step difference for op 'd' (in index units of the ordered category)

    # kinds
    #   same    (a, b)            owner(a) == owner(b)
    #   diff    (a, b)            owner(a) != owner(b)
    #   nor     (a, b1, b2)       owner(a) not in {owner(b1), owner(b2)}; b1, b2 same category
    #   either  (a, b1, b2)       owner(a) in {owner(b1), owner(b2)}; b1, b2 same category
    #   cmp     (a, b)            val(a) op val(b) in ordered category `cat`
    #   pair    (a1, a2, b1, b2)  of a1 and a2, one is b1 and the other is b2
    #   alldiff (a1, ..., am)     pairwise different owners

    def cats(self, k: int) -> frozenset:
        cs = {it[0] for it in self.items}
        if self.kind == "cmp":
            cs.add(self.cat)
        return frozenset(c for c in cs if c != 0) | frozenset()


def owner_of(sol, item):
    c, v = item
    return sol[c].index(v)


def holds(clue: Clue, sol) -> bool:
    """Does the clue hold for a complete solution sol[c][entity] = value?"""
    o = lambda it: owner_of(sol, it)  # noqa: E731
    if clue.kind == "same":
        a, b = clue.items
        return o(a) == o(b)
    if clue.kind == "diff":
        a, b = clue.items
        return o(a) != o(b)
    if clue.kind == "either":
        a, b1, b2 = clue.items
        return o(a) in (o(b1), o(b2))
    if clue.kind == "nor":
        a, b1, b2 = clue.items
        return o(a) not in (o(b1), o(b2))
    if clue.kind == "cmp":
        a, b = clue.items
        va = sol[clue.cat][o(a)]
        vb = sol[clue.cat][o(b)]
        if clue.op == ">":
            return va > vb
        if clue.op == "<":
            return va < vb
        if clue.op == "adj":
            return abs(va - vb) == 1
        if clue.op == "nadj":
            return abs(va - vb) > 1
        return va - vb == clue.d
    if clue.kind == "pair":
        a1, a2, b1, b2 = clue.items
        if o(a1) == o(a2) or o(b1) == o(b2):
            return False
        return {o(a1), o(a2)} == {o(b1), o(b2)}
    if clue.kind == "alldiff":
        owners = [o(it) for it in clue.items]
        return len(set(owners)) == len(owners)
    raise ValueError(clue.kind)


# ---------------------------------------------------------------- exhaustive count
def count_solutions(n: int, k: int, clues, limit: int = 2, ordered_cats=()):
    """Number of solutions (stops at ``limit``). Category 0 is the identity.

    Categories are assigned one at a time (all n! permutations each); a clue
    is checked as soon as every category it mentions has been assigned.
    """
    perms = list(itertools.permutations(range(n)))
    order = list(range(1, k))
    if not order:
        return 1
    pos = {c: i for i, c in enumerate(order)}
    checks = [[] for _ in order]
    for cl in clues:
        cs = cl.cats(k)
        if not cs:
            continue
        checks[max(pos[c] for c in cs)].append(cl)
    sol = [tuple(range(n))] + [None] * (k - 1)
    count = 0

    def rec(idx):
        nonlocal count
        if idx == len(order):
            count += 1
            return count >= limit
        c = order[idx]
        for p in perms:
            sol[c] = p
            if all(holds(cl, sol) for cl in checks[idx]) and rec(idx + 1):
                return True
        sol[c] = None
        return False

    rec(0)
    return count


# ---------------------------------------------------------------- human-style solver
class Contradiction(Exception):
    pass


@dataclass
class Step:
    kind: str            # fact | only | transfer | either | cmp | pair | alldiff | trial
    text: str            # plain-English explanation (filled by the renderer via `info`)
    info: dict = field(default_factory=dict)
    places: list = field(default_factory=list)   # new O cells (item, item)
    rules_out: list = field(default_factory=list)  # new X cells


WEIGHT = {"fact": 1, "only": 2, "transfer": 3, "either": 3, "alldiff": 2,
          "cmp": 4, "pair": 4, "trial": 10, "assume": 0}


class Deducer:
    """Solve on the O/X grid with beginner rules, logging each step."""

    def __init__(self, n, k, clues, ordered_cats=(), allow=("fact", "only", "transfer", "either",
                                                            "alldiff", "cmp", "pair")):
        self.n, self.k = n, k
        self.clues = list(clues)
        self.ordered = set(ordered_cats)
        self.allow = set(allow)
        self.items = [(c, v) for c in range(k) for v in range(n)]
        self.rel = {}
        for a in self.items:
            for b in self.items:
                if a[0] == b[0]:
                    self.rel[(a, b)] = (a == b)
        self.steps: list[Step] = []
        self.applied = set()
        self.cause = {}            # cell -> index of the step that decided it

    # -- cell access
    def get(self, a, b):
        return self.rel.get((a, b))

    def _set(self, a, b, val, newO, newX):
        cur = self.rel.get((a, b))
        if cur is val:
            return False
        if cur is not None and cur != val:
            raise Contradiction((a, b, val))
        self.rel[(a, b)] = val
        self.rel[(b, a)] = val
        (newO if val else newX).append((a, b))
        if val:
            # an O rules out the rest of its row and column in that block
            for v in range(self.n):
                if v != b[1]:
                    self._set(a, (b[0], v), False, newO, newX)
                if v != a[1]:
                    self._set((a[0], v), b, False, newO, newX)
        return True

    def options(self, a, c):
        if a[0] == c:
            return [a]
        return [(c, v) for v in range(self.n) if self.rel.get((a, (c, v))) is not False]

    def check(self):
        for a in self.items:
            for c in range(self.k):
                if not self.options(a, c):
                    raise Contradiction(("empty", a, c))

    def solved(self):
        return all(len(self.options((0, e), c)) == 1 and self.rel.get(((0, e), self.options((0, e), c)[0])) is True
                   for e in range(self.n) for c in range(1, self.k))

    def solution(self):
        sol = [tuple(range(self.n))]
        for c in range(1, self.k):
            row = []
            for e in range(self.n):
                (it,) = self.options((0, e), c)
                row.append(it[1])
            sol.append(tuple(row))
        return sol

    def record(self, kind, newO, newX, **info):
        if newO or newX:
            idx = len(self.steps)
            for a, b in list(newO) + list(newX):
                self.cause[(a, b)] = idx
                self.cause[(b, a)] = idx
            self.steps.append(Step(kind, "", info, list(newO), list(newX)))
            return True
        return False

    # -- value domains for ordered categories
    def vals(self, a, o):
        return [it[1] for it in self.options(a, o)]

    # -- rules (each returns True if it changed something)
    def r_facts(self):
        for i, cl in enumerate(self.clues):
            self._clue = i
            if i in self.applied or cl.kind not in ("same", "diff", "nor"):
                continue
            self.applied.add(i)
            newO, newX = [], []
            if cl.kind == "nor":
                a, b1, b2 = cl.items
                self._set(a, b1, False, newO, newX)
                self._set(a, b2, False, newO, newX)
            else:
                a, b = cl.items
                self._set(a, b, cl.kind == "same", newO, newX)
            if self.record("fact", newO, newX, clue=i):
                return True
        return False

    def r_alldiff(self):
        for i, cl in enumerate(self.clues):
            self._clue = i
            if i in self.applied or cl.kind != "alldiff":
                continue
            self.applied.add(i)
            newO, newX = [], []
            for a, b in itertools.combinations(cl.items, 2):
                if a[0] != b[0]:
                    self._set(a, b, False, newO, newX)
            if self.record("alldiff", newO, newX, clue=i):
                return True
        return False

    def r_only(self):
        for a in self.items:
            for c in range(self.k):
                if c == a[0]:
                    continue
                opts = self.options(a, c)
                if len(opts) == 1 and self.rel.get((a, opts[0])) is not True:
                    newO, newX = [], []
                    self._set(a, opts[0], True, newO, newX)
                    return self.record("only", newO, newX, item=a, cat=c, partner=opts[0])
        return False

    def r_transfer(self):
        for (a, b), val in list(self.rel.items()):
            if val is not True or a[0] == b[0] or a > b:
                continue
            for x in self.items:
                if x[0] in (a[0], b[0]):
                    continue
                va, vb = self.rel.get((a, x)), self.rel.get((b, x))
                for src, dst, v in ((a, b, va), (b, a, vb)):
                    other = vb if src == a else va
                    if v is not None and other is None:
                        newO, newX = [], []
                        self._set(dst, x, v, newO, newX)
                        return self.record("transfer", newO, newX, link=(src, dst), via=x, value=v)
        return False

    def r_either(self):
        for i, cl in enumerate(self.clues):
            self._clue = i
            if cl.kind != "either":
                continue
            a, b1, b2 = cl.items
            newO, newX = [], []
            c = b1[0]
            for v in range(self.n):
                if (c, v) not in (b1, b2):
                    self._set(a, (c, v), False, newO, newX)
            if self.record("either", newO, newX, clue=i, part="limit"):
                return True
            for x, y in ((b1, b2), (b2, b1)):
                if self.rel.get((a, x)) is False and self.rel.get((a, y)) is not True:
                    self._set(a, y, True, newO, newX)
                    if self.record("either", newO, newX, clue=i, part="other", out=x, chosen=y):
                        return True
        return False

    def r_cmp(self):
        for i, cl in enumerate(self.clues):
            self._clue = i
            if cl.kind != "cmp":
                continue
            a, b = cl.items
            o = cl.cat
            newO, newX = [], []
            if a[0] != b[0]:
                self._set(a, b, False, newO, newX)
                if self.record("cmp", newO, newX, clue=i, part="distinct"):
                    return True
            da, db = self.vals(a, o), self.vals(b, o)

            def ok(x, y):
                if cl.op == ">":
                    return x > y
                if cl.op == "<":
                    return x < y
                if cl.op == "adj":
                    return abs(x - y) == 1
                if cl.op == "nadj":
                    return abs(x - y) > 1
                return x - y == cl.d
            keep_a = [x for x in da if any(ok(x, y) for y in db)]
            keep_b = [y for y in db if any(ok(x, y) for x in da)]
            if not keep_a or not keep_b:
                raise Contradiction(("cmp", i))
            for x in da:
                if x not in keep_a and a[0] != o:
                    self._set(a, (o, x), False, newO, newX)
            for y in db:
                if y not in keep_b and b[0] != o:
                    self._set(b, (o, y), False, newO, newX)
            if self.record("cmp", newO, newX, clue=i, part="range", dropped_a=[x for x in da if x not in keep_a],
                           dropped_b=[y for y in db if y not in keep_b], dom_a=list(da), dom_b=list(db)):
                return True
        return False

    def r_pair(self):
        for i, cl in enumerate(self.clues):
            self._clue = i
            if cl.kind != "pair":
                continue
            a1, a2, b1, b2 = cl.items
            newO, newX = [], []
            for p, q in ((a1, a2), (b1, b2)):
                if p[0] != q[0]:
                    self._set(p, q, False, newO, newX)
            # each of a1, a2 is one of b1, b2: rule out the rest of b's category
            if b1[0] == b2[0]:
                for a in (a1, a2):
                    if a[0] != b1[0]:
                        for v in range(self.n):
                            if (b1[0], v) not in (b1, b2):
                                self._set(a, (b1[0], v), False, newO, newX)
            if a1[0] == a2[0]:
                for b in (b1, b2):
                    if b[0] != a1[0]:
                        for v in range(self.n):
                            if (a1[0], v) not in (a1, a2):
                                self._set(b, (a1[0], v), False, newO, newX)
            if self.record("pair", newO, newX, clue=i, part="limit"):
                return True
            # resolve: if a1 is b1 then a2 is b2, etc.
            for (x, y), (p, q) in (((a1, b1), (a2, b2)), ((a1, b2), (a2, b1)),
                                   ((a2, b1), (a1, b2)), ((a2, b2), (a1, b1))):
                if x[0] != y[0] and self.rel.get((x, y)) is True and p[0] != q[0] \
                        and self.rel.get((p, q)) is not True:
                    self._set(p, q, True, newO, newX)
                    if self.record("pair", newO, newX, clue=i, part="other", known=(x, y), chosen=(p, q)):
                        return True
            for (x, y, z) in ((a1, b1, b2), (a1, b2, b1), (a2, b1, b2), (a2, b2, b1)):
                if x[0] != y[0] and x[0] != z[0] and self.rel.get((x, y)) is False and self.rel.get((x, z)) is not True:
                    self._set(x, z, True, newO, newX)
                    if self.record("pair", newO, newX, clue=i, part="forced", out=(x, y), chosen=(x, z)):
                        return True
        return False

    RULES = ("r_facts", "r_alldiff", "r_only", "r_transfer", "r_either", "r_cmp", "r_pair")

    def propagate(self, record=True):
        """Apply rules (simplest first) until nothing changes."""
        while True:
            changed = False
            for name in self.RULES:
                kind = name[2:]
                kind = {"facts": "fact"}.get(kind, kind)
                if kind not in self.allow and kind != "fact":
                    continue
                self._clue = None
                try:
                    hit = getattr(self, name)()
                    if hit:
                        self.check()
                except Contradiction as e:
                    raise Contradiction({"rule": kind, "clue": self._clue, "detail": e.args[0] if e.args else None})
                if hit:
                    changed = True
                    break
            if not changed:
                return

    def r_trial(self, max_options=3):
        """Assume an open O; if the basic rules then hit a contradiction, mark X.

        Only rows with few options are tried (a human picks a row with two or
        three choices left and asks "suppose it is this one?").
        """
        cells = []
        for e in range(self.n):
            a = (0, e)
            for c in range(1, self.k):
                opts = self.options(a, c)
                if 1 < len(opts) <= max_options:
                    cells.extend((len(opts), a, b) for b in opts if self.rel.get((a, b)) is None)
        cells.sort(key=lambda t: t[0])
        best = None
        for _, a, b in cells:
            probe = self.clone()
            start = len(probe.steps)
            try:
                newO, newX = [], []
                probe._set(a, b, True, newO, newX)
                probe.record("assume", newO, newX, assume=(a, b))
                probe.check()
                probe.propagate()
            except Contradiction as e:
                length = len(probe.steps) - start
                if best is None or length < best[0]:
                    best = (length, a, b, probe, start, e.args[0] if e.args else None)
        if best is None:
            return False
        _, a, b, probe, start, why = best
        newO, newX = [], []
        self._set(a, b, False, newO, newX)
        return self.record("trial", newO, newX, assume=(a, b), probe=probe, start=start, why=why)

    def clone(self):
        d = Deducer.__new__(Deducer)
        d.n, d.k, d.clues, d.ordered, d.allow = self.n, self.k, self.clues, self.ordered, self.allow
        d.items = self.items
        d.rel = dict(self.rel)
        d.steps = list(self.steps)
        d.applied = set(self.applied)
        d.cause = dict(self.cause)
        return d

    def run(self, trial=False, max_trials=2):
        try:
            self.propagate()
            used = 0
            while trial and not self.solved() and used < max_trials:
                if not self.r_trial():
                    break
                used += 1
                self.propagate()
        except Contradiction:
            return False
        return self.solved()

    def score(self):
        return sum(WEIGHT[s.kind] for s in self.steps)


# ---------------------------------------------------------------- generation
def stars(d: "Deducer") -> int:
    """Difficulty in stars from the techniques the solve needed.

    1: direct facts + 'only choice left' within a block
    2: also carrying facts across blocks (transfer)
    3: also clue reasoning (either/or, comparisons, pairs) — re-reading clues
    4: clue reasoning with many dependent steps (several passes / combined clues)
    5: needs one 'Suppose' (case check)
    """
    kinds = {s.kind for s in d.steps}
    if "trial" in kinds:
        return 5
    clue_steps = sum(1 for s in d.steps if s.kind in ("either", "cmp", "pair"))
    if kinds & {"either", "cmp", "pair"}:
        # how far into the solve clue reasoning is still needed
        idx = [i for i, s in enumerate(d.steps) if s.kind in ("either", "cmp", "pair")]
        late = idx[-1] / max(1, len(d.steps) - 1)
        return 4 if (clue_steps >= 6 and late > 0.4) else 3
    if "transfer" in kinds:
        return 2
    return 1


def random_solution(n, k, rng):
    sol = [tuple(range(n))]
    for _ in range(1, k):
        p = list(range(n))
        rng.shuffle(p)
        sol.append(tuple(p))
    return sol


def clue_pool(n, k, sol, ordered, rng, kinds):
    """Every candidate clue that is TRUE for sol, of the requested kinds."""
    items = [(c, v) for c in range(k) for v in range(n)]
    own = {it: owner_of(sol, it) for it in items}
    pool = []
    pairs = [(a, b) for a in items for b in items if a[0] < b[0]]
    for a, b in pairs:
        if own[a] == own[b]:
            if "same" in kinds:
                pool.append(Clue("same", (a, b)))
        elif "diff" in kinds:
            pool.append(Clue("diff", (a, b)))
    if "nor" in kinds:
        for a in items:
            for c in range(k):
                if c == a[0]:
                    continue
                true_b = (c, sol[c][own[a]])
                others = [(c, v) for v in range(n) if (c, v) != true_b]
                for b1, b2 in itertools.combinations(others, 2):
                    pool.append(Clue("nor", (a, b1, b2)))
    if "either" in kinds:
        for a in items:
            for c in range(k):
                if c == a[0]:
                    continue
                true_b = (c, sol[c][own[a]])
                for v in range(n):
                    b2 = (c, v)
                    if b2 != true_b:
                        bb = [true_b, b2]
                        rng.shuffle(bb)
                        pool.append(Clue("either", (a, bb[0], bb[1])))
    if "cmp" in kinds or "cmpd" in kinds:
        for o in ordered:
            for a, b in itertools.permutations(items, 2):
                if a[0] == o or b[0] == o:
                    continue    # "later than the 10 a.m. arrival" is a disguised plain fact
                if own[a] == own[b]:
                    continue
                va, vb = sol[o][own[a]], sol[o][own[b]]
                if "cmp" in kinds:
                    pool.append(Clue("cmp", (a, b), cat=o, op=">" if va > vb else "<"))
                if "cmpd" in kinds and va > vb:
                    pool.append(Clue("cmp", (a, b), cat=o, op="d", d=va - vb))
                if "adj" in kinds and a < b and abs(va - vb) == 1:
                    pool.append(Clue("cmp", (a, b), cat=o, op="adj"))
                if "nadj" in kinds and a < b and abs(va - vb) > 1:
                    pool.append(Clue("cmp", (a, b), cat=o, op="nadj"))
    if "pair" in kinds:
        for a1, a2 in itertools.combinations(items, 2):
            if own[a1] == own[a2]:
                continue
            for c in range(k):
                if c in (a1[0], a2[0]):
                    continue
                b1, b2 = (c, sol[c][own[a1]]), (c, sol[c][own[a2]])
                bb = [b1, b2]
                rng.shuffle(bb)
                pool.append(Clue("pair", (a1, a2, bb[0], bb[1])))
    if "alldiff" in kinds and n >= 3:
        for _ in range(40):
            size = rng.randint(3, min(n, 5))
            ents = rng.sample(range(n), size)
            its = []
            for e in ents:
                c = rng.randrange(k)
                its.append((c, sol[c][e]))
            if len({it[0] for it in its}) >= 2:
                pool.append(Clue("alldiff", tuple(its)))
    return pool


@dataclass
class Spec:
    n: int
    k: int
    ordered: tuple = ()
    kinds: dict = field(default_factory=lambda: {"same": 1.0, "diff": 2.0})
    allow: tuple = ("fact", "only", "transfer", "either", "alldiff", "cmp", "pair")
    min_clues: int = 2
    max_clues: int = 99
    stars: tuple = (1, 2, 3, 4, 5)          # acceptable star ratings
    need_trial: bool = False                 # require a 'Suppose' step (5 stars)
    max_trials: int = 1                      # at most this many 'Suppose' steps
    score_range: tuple = (0, 10**9)
    max_positive: int | None = None   # cap on direct "same" clues (they make puzzles too easy)
    max_kind: dict = field(default_factory=dict)   # cap per clue kind, e.g. {"either": 2}


def _wkey(c):
    if c.kind == "cmp":
        return {"d": "cmpd", "adj": "adj", "nadj": "nadj"}.get(c.op, "cmp")
    return c.kind


def features(d: "Deducer") -> dict:
    """Measures of how hard the deducer's solve was."""
    seen, revisits = set(), 0
    for s in d.steps:
        c = s.info.get("clue")
        if c is None:
            continue
        if c in seen and s.kind in ("either", "cmp", "pair"):
            revisits += 1
        seen.add(c)
    kinds = [s.kind for s in d.steps]
    return {"steps": len(d.steps), "score": d.score(), "revisits": revisits,
            "transfer": kinds.count("transfer"), "trial": kinds.count("trial"),
            "clue_steps": sum(k in ("either", "cmp", "pair") for k in kinds)}


def _subject_keys(cl):
    """(item, category) pairs a negative/limiting clue talks about."""
    if cl.kind == "diff":
        a, b = cl.items
        return {(a, b[0]), (b, a[0])}
    if cl.kind in ("nor", "either"):
        a, b1, _ = cl.items
        return {(a, b1[0])}
    return set()


def minimal_clues(spec, sol, pool, weights, rng):
    """Pick clues in weighted random order until unique, then drop redundant ones."""
    from .space import Space, feasible
    keyed = sorted(range(len(pool)), key=lambda i: -(rng.random() ** (1.0 / max(weights[i], 1e-9))))
    caps = dict(spec.max_kind)
    if spec.max_positive is not None:
        caps.setdefault("same", spec.max_positive)
    used = {}
    talked = set()
    if feasible(spec.n, spec.k):
        S = Space(spec.n, spec.k)
        mask = np.ones(S.size, bool)
        chosen, masks = [], []
        total = S.size
        for i in keyed:
            cl = pool[i]
            kk = _wkey(cl)
            if kk in caps and used.get(kk, 0) >= caps[kk]:
                continue
            keys = _subject_keys(cl)
            if keys & talked:
                continue                      # avoid splitting one fact over two clues
            m = S.mask(cl)
            new = mask & m
            cnt = int(new.sum())
            if cnt == total:
                continue                      # adds nothing
            chosen.append(cl)
            masks.append(m)
            talked |= keys
            used[kk] = used.get(kk, 0) + 1
            mask, total = new, cnt
            if total == 1 and len(chosen) >= spec.min_clues:
                break
        if total != 1:
            return None
        keep = list(range(len(chosen)))
        for j in reversed(range(len(chosen))):
            rest = [x for x in keep if x != j]
            if len(rest) < spec.min_clues:
                continue
            m = np.ones(S.size, bool)
            for x in rest:
                m &= masks[x]
            if int(m.sum()) == 1:
                keep = rest
        return [chosen[x] for x in keep]
    chosen = []
    for i in keyed:
        cl = pool[i]
        kk = _wkey(cl)
        if kk in caps and used.get(kk, 0) >= caps[kk]:
            continue
        chosen.append(cl)
        used[kk] = used.get(kk, 0) + 1
        if len(chosen) >= spec.min_clues and count_solutions(spec.n, spec.k, chosen, 2) == 1:
            break
    else:
        return None
    for cl in list(reversed(chosen)):
        trial = [c for c in chosen if c is not cl]
        if len(trial) >= spec.min_clues and count_solutions(spec.n, spec.k, trial, 2) == 1:
            chosen = trial
    return chosen


def generate(spec: Spec, rng: random.Random, tries: int = 200, accept=None):
    """Return (solution, clues, deducer) for a unique, beginner-solvable puzzle.

    ``accept(deducer)`` may add a final filter (e.g. a difficulty band).
    """
    for _ in range(tries):
        sol = random_solution(spec.n, spec.k, rng)
        pool = clue_pool(spec.n, spec.k, sol, spec.ordered, rng, set(spec.kinds))
        weights = [spec.kinds.get(_wkey(c), 0) for c in pool]
        chosen = minimal_clues(spec, sol, pool, weights, rng)
        if chosen is None or not (spec.min_clues <= len(chosen) <= spec.max_clues):
            continue
        rng.shuffle(chosen)
        use_trial = "trial" in spec.allow
        d = Deducer(spec.n, spec.k, chosen, spec.ordered, spec.allow)
        if use_trial:
            # cheap screen first: puzzles the basic rules solve never need a trial
            plain = Deducer(spec.n, spec.k, chosen, spec.ordered, tuple(a for a in spec.allow if a != "trial"))
            if plain.run():
                if spec.need_trial:
                    continue
                d = plain
            elif not d.run(trial=True, max_trials=spec.max_trials):
                continue
        elif not d.run():
            continue
        if spec.need_trial and not any(st.kind == "trial" for st in d.steps):
            continue
        if stars(d) not in spec.stars:
            continue
        if d.solution() != sol:
            raise AssertionError("deducer reached a different solution")
        if not (spec.score_range[0] <= d.score() <= spec.score_range[1]):
            continue
        if accept is not None and not accept(d):
            continue
        return sol, chosen, d
    raise RuntimeError("could not generate a puzzle for spec")
