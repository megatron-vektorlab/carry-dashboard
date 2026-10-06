"""The worked example in "How to Solve": Psalm 23:1, solved in five steps.

Each step is computed, not typed: the cipher comes from a fixed key, and every step
lists which code letters become known and why.  bc.book puts the result in data.json.
"""
from __future__ import annotations

from . import cipher, kjv

REF = "Psalms 23:1"
KEY_SEED = "example:3"   # VBN WLAQ RI FS IBNCBNAQ; R IBKWW GLV TKGV.

# (plain letters revealed in this step, explanation in the book's words)
STEPS = [
    ("I", "A code letter standing alone is almost always *I* or *A* (once in a while *O*). Here R stands alone at the "
          "start of a new thought, right after the semicolon, so *I* is the best guess. Try R = I everywhere."),
    ("THE", "The most common three-letter word is THE. The first word, VBN, has three different letters, so try "
            "V = T, B = H and N = E. Notice H and E twice inside the long word IBNCBNAQ."),
    ("SAL", "Look at R IBKWW: I, then a five-letter word ending in a double letter. With H and the double letter, "
           "*SHALL* fits: I = S, K = A, W = L. (L L is the most common double letter in these verses.)"),
    ("ORD", "After THE comes WLAQ, and its first letter is already L. Think of the most famous four-letter word starting with L "
            "in the Bible: LORD. So L = O, A = R, Q = D."),
    ("MYPNW", "Only a few letters are left. F S is a two-letter word: MY. The long word is SHEPHERD, and the last "
              "words read NOT WANT. Check every letter once more. Done!"),
]


def build() -> dict:
    text = kjv.passage(REF)["text"]
    key = cipher.make_key(KEY_SEED)
    inv = {c: p for p, c in key.items()}
    ct = cipher.encrypt(text, key)
    known: dict[str, str] = {}
    states = []
    for letters, why in STEPS:
        new = {}
        for p in letters:
            c = key[p]
            if c in ct and c not in known:
                new[c] = p
        known.update(new)
        states.append({"new": dict(sorted(new.items())), "known": dict(known), "why": why})
    missing = {c for c in ct if c.isalpha()} - set(known)
    if missing:
        raise AssertionError(f"worked example leaves code letters unsolved: {sorted(missing)}")
    assert "".join(inv.get(c, c) for c in ct) == text.upper()
    return {"ref": REF, "text": text, "cipher": ct, "states": states}


if __name__ == "__main__":
    import json
    print(json.dumps(build(), indent=1))
