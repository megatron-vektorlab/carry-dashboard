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
    answer = None
    q = theme.get("question")
    if q:
        ci = [c["label"] for c in B.cats].index(q["cat"])
        vi = B.cats[ci]["values"].index(q["value"])
        owner = sol[ci].index(vi)
        names = B.cats[0]["values"]
        if theme.get("answer"):
            # relabel entities so the intended culprit is the answer (a pure renaming)
            j = names.index(theme["answer"])
            names[owner], names[j] = names[j], names[owner]
        answer = names[owner]
        # optionally give the answer person particular values in unordered categories,
        # again by swapping two labels within a category (the puzzle's logic is unchanged)
        labels = [c["label"] for c in B.cats]
        for lab, want in (theme.get("answer_has") or {}).items():
            c = labels.index(lab)
            if B.cats[c].get("ordered"):
                raise ValueError("answer_has cannot fix an ordered category")
            vals = B.cats[c]["values"]
            have = sol[c][owner]
            i = vals.index(want)
            vals[have], vals[i] = vals[i], vals[have]
    texts = [B.clue_text(c, rng) for c in clues]
    return dict(B=B, sol=sol, clues=clues, d=d, texts=texts, feats=features(d), answer=answer)
