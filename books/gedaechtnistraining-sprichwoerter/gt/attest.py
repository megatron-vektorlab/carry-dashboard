"""Attestation: every saying printed in the book must exist in a recognised source.

The model may not author proverb text. A wording (or one of its variants) counts as
attested if, after normalising case, punctuation, ß/ss and the placeholders
jemandem/jemanden/etwas/sich, it equals an entry in one of:
  * German Wiktionary (Sprichwort, Redewendung, Wortverbindung, Geflügeltes Wort; CC BY-SA),
  * English Wiktionary, German proverbs (CC BY-SA),
  * German Wikiquote, "Deutsche Sprichwörter" (about 900 proverbs, many with a Wander reference; CC BY-SA),
  * Baur/Chlosta 57 and GfM 15 best-known proverbs (via Schatte 2008),
  * Hallsteinsdóttir et al. 2006, 143 core idioms (CC BY 4.0),
or appears word for word in Borchardt (1888/1895) or Wander (vol. 1) (weaker: "historical").
The source files live in sources_cache/proverb_sources/ (not in git; see README).
Wiktionary glosses are never printed and never given to the model (CC BY-SA share-alike).
"""
from __future__ import annotations

import csv
import functools
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "sources_cache", "proverb_sources")
PLACEHOLDERS = {"jemandem", "jemanden", "jemandes", "jemand", "etwas", "sich", "jm", "jn", "js", "etw", "einem", "einen"}


def norm(s: str) -> str:
    s = s.lower().replace("ß", "ss").replace("’", "'").replace("'", "")
    s = re.sub(r"\([^)]*\)", " ", s)          # optional parts in brackets
    s = re.sub(r"[^a-zäöü ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def core(s: str) -> str:
    """Normalised, without placeholders: 'jemandem einen Bären aufbinden' -> 'baren aufbinden'-ish key."""
    return " ".join(w for w in norm(s).split() if w not in PLACEHOLDERS)


def _variants_of(phrase: str) -> list[str]:
    """'keine (blasse) Ahnung haben' -> with and without the bracket; 'jm' -> 'jemandem'."""
    p = phrase.replace("jm ", "jemandem ").replace("jn ", "jemanden ").replace("etw. ", "etwas ")
    with_br = re.sub(r"[()]", "", p)
    without = re.sub(r"\([^)]*\)", "", p)
    return [with_br, without]


@functools.lru_cache(maxsize=1)
def sources() -> dict:
    strong: dict[str, set] = {}
    gloss: dict[str, list] = {}

    def add(s, src):
        for v in _variants_of(s):
            for k in (norm(v), core(v)):
                if k:
                    strong.setdefault(k, set()).add(src)

    # The IDS OWID headword list is NOT used: its terms require written consent and the
    # database right (§87a/b UrhG) may cover the list; owid.de may be consulted by hand.
    p = os.path.join(SRC, "kaikki_dewiktionary_Deutsch_pos-phrase.jsonl")
    if os.path.exists(p):
        for line in open(p):
            d = json.loads(line)
            if d.get("pos_title") in ("Sprichwort", "Redewendung", "Wortverbindung", "Geflügeltes Wort"):
                add(d["word"], "de.wiktionary")
                gl = [g for s in d.get("senses", []) for g in s.get("glosses", [])][:2]
                gloss.setdefault(core(d["word"]), gl)
                for f in d.get("forms", []):
                    if f.get("form") and len(f["form"].split()) > 1:
                        add(f["form"], "de.wiktionary")
    p = os.path.join(SRC, "kaikki_enwiktionary_German_pos-proverb.jsonl")
    if os.path.exists(p):
        for line in open(p):
            add(json.loads(line)["word"], "en.wiktionary")
    p = os.path.join(SRC, "proverb_minima_baurchlosta57_gfm15.tsv")
    if os.path.exists(p):
        for row in csv.DictReader(open(p), delimiter="\t"):
            add(row["proverb"], "Baur/Chlosta/GfM")
    p = os.path.join(SRC, "hallsteinsdottir2006_143_idioms.tsv")
    if os.path.exists(p):
        for row in csv.DictReader(open(p), delimiter="\t"):
            add(row["phraseologismus"], "Hallsteinsdóttir 2006")
    for name, src in (("ynsrc_wiktionary_expression-idiom.txt", "de.wiktionary"),
                      ("ynsrc_wiktionary_expression-proverb.txt", "de.wiktionary")):
        p = os.path.join(SRC, name)
        if os.path.exists(p):
            for line in open(p):
                if line.strip():
                    add(line.strip(), src)
    p = os.path.join(SRC, "dewikiquote_deutsche_sprichwoerter.wiki")
    if os.path.exists(p):
        for line in open(p):
            m = re.match(r'\*\s*"(.+?)"', line)
            if m:
                q = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", m.group(1))
                add(q, "de.wikiquote")
    p = os.path.join(ROOT, "data", "attested_web.json")       # single web lookups (DWDS, Duden, Wiktionary ...), URL kept
    if os.path.exists(p):
        for w, url in json.load(open(p)).items():
            add(w, "web lookup")
    hist = ""
    for name in os.listdir(SRC) if os.path.isdir(SRC) else []:
        if name.startswith(("borchardt", "wander")):
            hist += " " + norm(open(os.path.join(SRC, name), errors="ignore").read())
    return {"strong": strong, "gloss": gloss, "hist": hist}


def attest(wording: str, variants=(), exact: bool = False) -> dict:
    """{'level': 'strong'|'historical'|'none', 'sources': [...], 'matched': str, 'gloss': [...]}
    exact: only whole-saying matches (used to test whether a decoy sentence is a real saying)."""
    S = sources()
    for w in [wording, *variants]:
        for k in (norm(w), core(w)):
            if k in S["strong"]:
                return {"level": "strong", "sources": sorted(S["strong"][k]), "matched": w,
                        "gloss": S["gloss"].get(core(w), [])}
    if exact:
        return {"level": "none", "sources": [], "matched": "", "gloss": []}
    # the source lists the idiom without its verb: "wie ein begossener Pudel" (+ dastehen)
    for w in [wording, *variants]:
        words = core(w).split()
        for n in range(len(words) - 1, max(1, len(words) - 2) - 1, -1):
            for i in range(0, len(words) - n + 1):
                k = " ".join(words[i:i + n])
                if n >= 2 and k in S["strong"]:
                    return {"level": "strong", "sources": sorted(S["strong"][k]), "matched": k,
                            "gloss": S["gloss"].get(k, [])}
    for w in [wording, *variants]:
        k = core(w)
        if len(k.split()) >= 3 and f" {k} " in S["hist"]:
            return {"level": "historical", "sources": ["Borchardt/Wander"], "matched": w, "gloss": []}
    return {"level": "none", "sources": [], "matched": "", "gloss": S["gloss"].get(core(wording), [])}


if __name__ == "__main__":
    import sys
    for w in sys.argv[1:]:
        print(w, attest(w))
