"""Turn chapter templates into finished, validated problems."""
from __future__ import annotations

import importlib
import pkgutil
import random
import re

from . import chapters as _chapters_pkg
from .core import Problem, Reject, finalize

MAX_TRIES = 400


def load_chapters(only: int | None = None):
    """All chapter modules (files chNN_*.py), sorted by NUM.

    With ``only``, import just that chapter so a broken sibling module
    cannot stop work on another chapter.
    """
    mods = []
    for info in pkgutil.iter_modules(_chapters_pkg.__path__):
        if not info.name.startswith("ch"):
            continue
        if only is not None and info.name[2:4] != f"{only:02d}":
            continue
        mods.append(importlib.import_module(f"{_chapters_pkg.__name__}.{info.name}"))
    mods.sort(key=lambda m: m.NUM)
    return mods


def _skeleton(stem: str) -> str:
    """Scenario fingerprint: the opening words with every number masked."""
    s = re.sub(r"\$[^$]*\$|\\\$[\d{},.]+|\d[\d{},.]*", "#", stem)
    words = re.findall(r"[A-Za-z#']+", s)
    return " ".join(words[:7]).lower()


def make(tpl, lvl: int, rng: random.Random, target: int, seen: set[str],
         chapter: int = 0, avoid: set | None = None) -> Problem:
    """One finished problem from a template; retries on Reject / duplicates.

    ``avoid`` (shared across one chapter or test section) holds scenario
    fingerprints and (template, answer) pairs already used, so a set does
    not tell the same story twice or reuse the same numbers; after half the
    tries the rule is relaxed rather than failing.
    """
    last = None
    name = f"{tpl.__module__.rsplit('.', 1)[-1]}.{tpl.__name__}"
    for i in range(MAX_TRIES):
        try:
            p = tpl(rng, lvl)
            if p.stem in seen:
                raise Reject("duplicate stem")
            keys = {("ans", name, str(p.answer))}
            if len(p.stem) > 70:          # word problems: vary the scenario too
                keys.add(("sk", _skeleton(p.stem)))
            if avoid is not None and i < MAX_TRIES // 2 and keys & avoid:
                raise Reject("scenario or numbers already used in this set")
            if getattr(tpl, "section", None) and p.section == "MK":
                p.section = tpl.section
            finalize(p, rng, target, strict=i < MAX_TRIES // 2)
        except Reject as e:
            last = e
            continue
        p.level = lvl
        p.template = name
        p.chapter = chapter
        seen.add(p.stem)
        if avoid is not None:
            avoid |= keys
        return p
    raise RuntimeError(f"{tpl.__module__}.{tpl.__name__} (level {lvl}) failed {MAX_TRIES} times: {last}")


def balanced_targets(n: int, rng: random.Random) -> list[int]:
    """Evenly spread answer slots with no slot repeated 3 times in a row."""
    t = [i % 4 for i in range(n)]
    for _ in range(200):
        rng.shuffle(t)
        if all(not (t[i] == t[i + 1] == t[i + 2]) for i in range(n - 2)):
            break
    return t


def interleave(problems: list[Problem]) -> list[Problem]:
    """Within each level, alternate templates so look-alikes are not adjacent."""
    out = []
    for lvl in sorted({p.level for p in problems}):
        groups: dict[str, list[Problem]] = {}
        for p in problems:
            if p.level == lvl:
                groups.setdefault(p.template, []).append(p)
        queues = sorted(groups.values(), key=len, reverse=True)
        last = None
        while any(queues):
            queues.sort(key=len, reverse=True)
            pick = next((q for q in queues if q and q[0].template != last), None)
            if pick is None:
                pick = next(q for q in queues if q)
            p = pick.pop(0)
            out.append(p)
            last = p.template
    return out


def chapter_problems(mod, seed: int, seen: set[str]) -> list[Problem]:
    rng = random.Random(seed)
    total = sum(c for _, _, c in mod.PLAN)
    targets = balanced_targets(total, rng)
    out = []
    avoid: set = set()
    for tpl, lvl, count in mod.PLAN:
        for _ in range(count):
            out.append(make(tpl, lvl, rng, targets[len(out)], seen, mod.NUM, avoid))
    return interleave(out)
