"""Letter and word statistics of the King James text, for the solving-tips pages.

    python3 -m bc.stats      -> data/kjv_stats.json

Every number printed in "Tips for King James Verses" comes from this file.
"""
from __future__ import annotations

import collections
import json
import os

from . import cipher, kjv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    src = kjv.load()["farskipper"]
    keys = sorted(src)
    text = " ".join(kjv.verse(*k)["text"] for k in keys)
    letters = collections.Counter(c for c in text.upper() if c.isalpha())
    total = sum(letters.values())
    ws = collections.Counter(cipher.words(text))
    by_len = collections.defaultdict(list)
    for w, n in ws.most_common():
        if "'" in w or "-" in w:
            continue
        if len(by_len[len(w)]) < 12:
            by_len[len(w)].append([w, n])
    apos = collections.Counter(w for w in cipher.words(text) if "'" in w)
    endings = collections.Counter()
    for w, n in ws.items():
        for e in ("ETH", "EST", "ING", "ED", "LY", "NESS"):
            if len(w) > len(e) + 2 and w.endswith(e):
                endings[e] += n
    doubles = collections.Counter()
    for w, n in ws.items():
        for a, b in zip(w, w[1:]):
            if a == b and a.isalpha():
                doubles[a + b] += n
    out = {
        "verses": len(keys),
        "letters_total": total,
        "letter_freq": [[c, n, round(100 * n / total, 2)] for c, n in letters.most_common()],
        "top_words": ws.most_common(40),
        "top_by_length": {str(k): v for k, v in sorted(by_len.items()) if k <= 7},
        "apostrophe_words": apos.most_common(10),
        "endings": endings.most_common(),
        "doubles": doubles.most_common(10),
        "one_letter_words": [[w, n] for w, n in ws.most_common() if len(w) == 1],
    }
    with open(os.path.join(ROOT, "data", "kjv_stats.json"), "w") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    print("letters:", " ".join(f"{c}{p:.1f}" for c, _, p in out["letter_freq"][:12]))
    print("top words:", " ".join(w for w, _ in out["top_words"][:30]))
    print("2:", out["top_by_length"]["2"][:10]); print("3:", out["top_by_length"]["3"][:10]); print("4:", out["top_by_length"]["4"][:10])
    print("apos:", out["apostrophe_words"][:6]); print("endings:", out["endings"]); print("doubles:", out["doubles"][:8])
    print("one-letter:", out["one_letter_words"])


if __name__ == "__main__":
    main()
