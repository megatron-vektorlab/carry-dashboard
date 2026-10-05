"""Machine trace of a solve, in plain English, for the writers and checkers.

Every line is a true statement backed by the deducer's step log.  Writers turn
the important lines into hints and a short solution; checkers compare what
the writers say against these lines.
"""
from __future__ import annotations

import re

from .text import _join, cap, why_not


def _or(words):
    words = list(words)
    if len(words) <= 1:
        return "".join(words)
    if len(words) == 2:
        return f"{words[0]} or {words[1]}"
    return ", ".join(words[:-1]) + f", or {words[-1]}"


def _only_reason(B, d, numbers, a, p, c):
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
        elif key == "trial":
            parts.append(f"the Suppose test ruled out {_join(B.short(o) for o, _ in lst)}")
        else:
            parts.append(_join(ph for _, ph in lst))
    for src, objs in vias.items():
        parts.append(f"{_join(B.short(o) for o in objs)} {'is' if len(objs) == 1 else 'are'} "
                     f"already ruled out for {src}")
    if len(taken) == 1:
        parts.append(taken[0])
    elif taken:
        parts.append("the other choices are already taken")
    return parts


def step_line(B, clues, d, numbers, idx):
    """(trivial, text, clue numbers) for one deducer step, or None if it only marks X's."""
    st = d.steps[idx]
    i, k = st.info, st.kind
    cn = [numbers[i["clue"]]] if i.get("clue") is not None else []
    if k == "assume":
        a, b = i["assume"]
        x, y = B.subject_first(a, b)
        return (False, f"Suppose {B.short(x)} goes with {B.short(y)}.", cn)
    if k == "trial":
        return None
    if k == "cmp" and not st.places:
        if i.get("part") == "distinct":
            return None
        cl = clues[i["clue"]]
        a, b = cl.items
        o = cl.cat
        da, db = i.get("dropped_a", []), i.get("dropped_b", [])
        segs = []
        if da:
            segs.append(f"{B.short(a)} cannot be {_or(B.short((o, v)) for v in da)}")
        if db:
            segs.append(f"{B.short(b)} cannot be {_or(B.short((o, v)) for v in db)}")
        if not segs:
            return None
        ctx = []
        for it, dom in ((a, i.get("dom_a")), (b, i.get("dom_b"))):
            if it[0] != o and dom is not None and len(dom) < B.n:
                ctx.append(f"{B.short(it)} can still be only {_or(B.short((o, v)) for v in dom)}")
        pre = f"Since {_join(ctx)}, clue {cn[0]} means" if ctx else f"Clue {cn[0]} means"
        return (False, f"{pre} {_join(segs)}.", cn)
    if k in ("either", "pair") and not st.places:
        if i.get("part") == "limit":
            return (True, f"Clue {cn[0]} limits the choices (mark the X's it gives).", cn)
        return None
    if k == "alldiff":
        return (True, f"Clue {cn[0]}: mark X between the people it lists.", cn)
    if not st.places:
        if k == "fact":
            return (True, f"Clue {cn[0]} gives an X.", cn)
        return None
    a, b = st.places[0]
    if k == "fact":
        x, y = B.subject_first(a, b)
        return (False, f"Clue {cn[0]} says directly that {B.short(x)} goes with {B.short(y)}.", cn)
    if k == "only":
        a, p, c = i["item"], i["partner"], i["cat"]
        parts = _only_reason(B, d, numbers, a, p, c)
        refs = sorted({int(x) for x in re.findall(r"clue (\d+)", " ".join(parts))})
        if not parts:
            return (True, f"{cap(B.short(a))} must go with {B.short(p)}, the only choice left.", refs)
        return (False, f"{cap(B.short(a))} must go with {B.short(p)}: {'; '.join(parts)}.", refs)
    if k == "transfer":
        (src, dst), x = i["link"], i["via"]
        if i.get("value"):
            return (True, f"{cap(B.short(dst))} goes with {B.short(src)}, so {B.short(dst)} also goes with "
                    f"{B.short(x)}.", [])
        return (True, f"{cap(B.short(dst))} goes with {B.short(src)}, so {B.short(dst)} is not with {B.short(x)}.", [])
    if k == "either":
        return (False, f"Clue {cn[0]} allows only {B.short(i['out'])} or {B.short(i['chosen'])} for "
                f"{B.short(clues[i['clue']].items[0])}; {B.short(i['out'])} is out, so it is {B.short(i['chosen'])}.", cn)
    if k == "pair":
        if i.get("part") == "other":
            (x, y), (p, q) = i["known"], i["chosen"]
            return (False, f"Clue {cn[0]} pairs them up: since {B.short(x)} goes with {B.short(y)}, "
                    f"{B.short(p)} goes with {B.short(q)}.", cn)
        (x, y), (_, z) = i["out"], i["chosen"]
        return (False, f"Clue {cn[0]}: {B.short(x)} is not with {B.short(y)}, so {B.short(x)} must be with "
                f"{B.short(z)}.", cn)
    return (False, f"Clue {cn[0]} gives {B.short(a)} with {B.short(b)}.", cn)


def contradiction_text(B, numbers, why):
    if not isinstance(why, dict):
        why = {"rule": None, "clue": None, "detail": why}
    det = why.get("detail")
    if why.get("clue") is not None:
        return f"But then clue {numbers[why['clue']]} cannot be true."
    if isinstance(det, tuple) and det and det[0] == "empty":
        _, a, c = det
        return f"But then {B.short(a)} has no {B.cats[c]['label'].lower()} left."
    return "But then two marks clash in the grid."


def trace(B, clues, d, numbers=None, start=0, collapse=True):
    """List of dicts {text, trivial, clues, kind} describing the solve."""
    numbers = numbers or {i: i + 1 for i in range(len(clues))}
    out = []
    for idx in range(start, len(d.steps)):
        st = d.steps[idx]
        if st.kind == "trial":
            a, b = st.info["assume"]
            probe, s0 = st.info["probe"], st.info["start"]
            sub = trace(B, clues, probe, numbers, start=s0, collapse=False)
            x, y = B.subject_first(a, b)
            out.append({"kind": "suppose", "trivial": False, "clues": sorted({c for s in sub for c in s["clues"]}),
                        "text": f"SUPPOSE TEST: try {B.short(x)} with {B.short(y)}.",
                        "chain": [s["text"] for s in sub] + [contradiction_text(B, numbers, st.info["why"])],
                        "result": f"So {B.short(x)} does NOT go with {B.short(y)}: mark that X."})
            continue
        r = step_line(B, clues, d, numbers, idx)
        if r is None:
            continue
        triv, text, cn = r
        text = re.sub(r"\.\.(?=\s|$)", ".", re.sub(r"\s+", " ", text))
        out.append({"kind": st.kind, "trivial": triv, "clues": cn, "text": text})
    if collapse:
        last = max((j for j, s in enumerate(out) if not s["trivial"]), default=-1)
        tail = out[last + 1:]
        out = out[:last + 1]
        if tail:
            out.append({"kind": "tail", "trivial": True, "clues": [],
                        "text": "Every remaining match is now the only choice left in its row; fill them in."})
    return out
