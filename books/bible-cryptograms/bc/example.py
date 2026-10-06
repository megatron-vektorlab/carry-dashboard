"""The worked example in "How to Solve": Psalm 23:1, solved in five steps.

Each step is computed, not typed: the cipher comes from a fixed key (with the same rules
as the puzzles), and the explanations are templates filled with the actual code letters,
so text and picture can never disagree.  bc.book puts the result in data.json.
"""
from __future__ import annotations

import re

from . import cipher, kjv

REF = "Psalms 23:1"
KEY_SEED = "example:3"

# (plain letters revealed in this step, explanation; {X} = code letter for real X, {w:WORD} = coded word)
STEPS = [
    ("I", "A code letter standing alone is almost always *I* or *A* (once in a while *O*). Here {I} stands alone "
          "at the start of a new thought, right after the semicolon, so *I* is the best guess. Try {I} = I everywhere."),
    ("THE", "The most common three-letter word is THE. The first word, {w:THE}, has three different letters, so try "
            "{T} = T, {H} = H and {E} = E. Notice H and E twice inside the long word {w:SHEPHERD}."),
    ("SAL", "Look at {w:I} {w:SHALL}: I, then a five-letter word ending in a double letter. With H in second place, "
            "*SHALL* fits: {S} = S, {A} = A, {L} = L. (L L is the most common double letter in these verses.)"),
    ("ORD", "After THE comes {w:LORD}, and its first letter is already L. Think of the most famous four-letter word "
            "starting with L in the Bible: LORD. So {O} = O, {R} = R, {D} = D."),
    ("MYPNW", "Only a few letters are left. {w:MY} is a two-letter word: MY. The long word is SHEPHERD, and the last "
              "words read NOT WANT. Check every letter once more. Done!"),
]


# Code letters for the example avoid the letters the explanation talks about, so that
# sentences like "a lone letter is I or A" never refer to a code letter of the same name.
TALKED_ABOUT = "IAOTHEL"


def example_key(text: str) -> dict[str, str]:
    import random
    used = sorted(set(kjv.letters(text)))
    allowed = [c for c in cipher.AZ if c not in TALKED_ABOUT + cipher.AVOID]
    rng = random.Random(KEY_SEED)
    while True:
        codes = rng.sample(allowed, len(used))
        key = dict(zip(used, codes))
        rest_plain = [p for p in cipher.AZ if p not in key]
        rest_code = [c for c in cipher.AZ if c not in codes]
        rng.shuffle(rest_code)
        key.update(zip(rest_plain, rest_code))
        if all(p != c for p, c in key.items()):
            return key


def build() -> dict:
    text = kjv.passage(REF)["text"]
    key = example_key(text)
    inv = {c: p for p, c in key.items()}
    ct = cipher.encrypt(text, key)

    def fill(s: str) -> str:
        s = re.sub(r"\{w:([A-Z]+)\}", lambda m: cipher.encrypt(m.group(1), key), s)
        return re.sub(r"\{([A-Z])\}", lambda m: key[m.group(1)], s)

    known: dict[str, str] = {}
    states = []
    for letters, why in STEPS:
        new = {key[p]: p for p in letters if key[p] in ct and key[p] not in known}
        known.update(new)
        states.append({"new": dict(sorted(new.items())), "known": dict(known), "why": fill(why)})
    missing = {c for c in ct if c.isalpha()} - set(known)
    if missing:
        raise AssertionError(f"worked example leaves code letters unsolved: {sorted(missing)}")
    assert "".join(inv.get(c, c) for c in ct) == text.upper()
    assert not set(cipher.AVOID) & set(ct)
    return {"ref": REF, "text": text, "cipher": ct, "states": states}


if __name__ == "__main__":
    import json
    print(json.dumps(build(), indent=1))
