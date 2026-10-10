"""German text helpers: words, syllables, spelling.

Syllables come from the LibreOffice/TeX hyphenation patterns (pyphen) with one fix:
hyphenation never splits off a single first letter, syllables do (A-bend, O-fen, I-gel).
"""
from __future__ import annotations

import functools
import os
import re

import pyphen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOWELS = "aeiouäöüyAEIOUÄÖÜY"
_HY = pyphen.Pyphen(lang="de_DE")
WORD_RE = re.compile(r"[A-Za-zÄÖÜäöüß]+(?:[-'’][A-Za-zÄÖÜäöüß]+)*")   # keeps "Wer's", "so's" whole


def words(s: str) -> list[str]:
    """Words of a phrase without punctuation ('Wer A sagt, muss auch B sagen' -> 7 words)."""
    return WORD_RE.findall(s)


def tokens(s: str) -> list[str]:
    """Words and punctuation marks, in order; spaces dropped."""
    return re.findall(r"[A-Za-zÄÖÜäöüß]+(?:[-'’][A-Za-zÄÖÜäöüß]+)*|[^\sA-Za-zÄÖÜäöüß]", s)


def syllables(word: str) -> list[str]:
    """'Morgenstund' -> ['Mor', 'gen', 'stund'];  'Abend' -> ['A', 'bend']."""
    pos = list(_HY.positions(word))
    if (len(word) >= 3 and word[0] in VOWELS and word[1] not in VOWELS and word[2] in VOWELS
            and word[1] not in "hH" and (not pos or pos[0] != 1)):
        pos = [1] + pos
    out, last = [], 0
    for p in pos:
        out.append(word[last:p])
        last = p
    out.append(word[last:])
    # a piece without a vowel is not a syllable ('Un-g-lück'): join it to its neighbour
    i = 0
    while len(out) > 1 and i < len(out):
        if not any(ch in VOWELS for ch in out[i]):
            if i + 1 < len(out):
                out[i:i + 2] = [out[i] + out[i + 1]]
            else:
                out[i - 1:i + 1] = [out[i - 1] + out[i]]
            continue
        i += 1
    return out


def letters_upper(word: str) -> str:
    """Grid letters for word puzzles: capitals, ß -> SS (as in German puzzle magazines)."""
    return word.replace("ß", "ss").upper()


@functools.lru_cache(maxsize=1)
def _dictionary():
    from spylls.hunspell import Dictionary
    return Dictionary.from_files(os.path.join(ROOT, "sources_cache", "de_DE_frami"))


def spelled_ok(word: str) -> bool:
    """True if the LibreOffice German dictionary (de_DE_frami) knows the word."""
    return bool(_dictionary().lookup(word))


def strip_end(s: str) -> str:
    return s.rstrip(" .!")
