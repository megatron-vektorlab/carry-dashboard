"""Generate the puzzle for one slot from its theme."""
from __future__ import annotations

import random

from .engine import Spec, features, generate
from .plan import BASE, FAMILIES
from .text import Bound


def trial_chain(d):
    for s in d.steps:
        if s.kind == "trial":
            return len(s.info["probe"].steps) - s.info["start"]
    return 0


def spec_for(slot, B):
    fam = FAMILIES[slot["family"]]
    kinds = dict(fam["kinds"])
    if not B.ordered:
        for key in ("cmp", "cmpd", "adj", "nadj"):
            kinds.pop(key, None)
    else:
        cat = B.cats[B.ordered[0]]
        if "adj" not in cat or "nadj" not in cat:
            kinds.pop("adj", None)
            kinds.pop("nadj", None)
    trial = fam.get("trial", False)
    return Spec(B.n, B.k, ordered=B.ordered, kinds=kinds,
                allow=BASE + (("trial",) if trial else ()), need_trial=trial,
                max_kind=dict(fam.get("max_kind", {})), max_trials=1,
                min_clues=2, max_clues=12)


def make(slot, theme, seed, tries=3000):
    rng = random.Random(seed)
    B = Bound(theme, slot["n"], rng, k=slot["k"])
    spec = spec_for(slot, B)
    accept = None
    if spec.need_trial:
        accept = lambda d: 3 <= trial_chain(d) <= 10  # noqa: E731
    sol, clues, d = generate(spec, rng, tries=tries, accept=accept)
    texts = [B.clue_text(c, rng) for c in clues]
    return dict(B=B, sol=sol, clues=clues, d=d, texts=texts, feats=features(d))
