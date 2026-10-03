"""Turn chapter templates into finished, validated problems."""
from __future__ import annotations

import importlib
import pkgutil
import random

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


def make(tpl, lvl: int, rng: random.Random, target: int, seen: set[str],
         chapter: int = 0) -> Problem:
    """One finished problem from a template; retries on Reject / duplicates."""
    last = None
    for _ in range(MAX_TRIES):
        try:
            p = tpl(rng, lvl)
            if p.stem in seen:
                raise Reject("duplicate stem")
            if getattr(tpl, "section", None) and p.section == "MK":
                p.section = tpl.section
            finalize(p, rng, target)
        except Reject as e:
            last = e
            continue
        p.level = lvl
        p.template = f"{tpl.__module__.rsplit('.', 1)[-1]}.{tpl.__name__}"
        p.chapter = chapter
        seen.add(p.stem)
        return p
    raise RuntimeError(f"{tpl.__module__}.{tpl.__name__} (level {lvl}) failed {MAX_TRIES} times: {last}")


def balanced_targets(n: int, rng: random.Random) -> list[int]:
    t = [i % 4 for i in range(n)]
    rng.shuffle(t)
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
    for tpl, lvl, count in mod.PLAN:
        for _ in range(count):
            out.append(make(tpl, lvl, rng, targets[len(out)], seen, mod.NUM))
    return interleave(out)
