"""Text widths in inches, measured with the real fonts (for grid label space)."""
from __future__ import annotations

from functools import lru_cache

from PIL import ImageFont

FONTS = {
    "sf": "/usr/share/texlive/texmf-dist/fonts/opentype/public/atkinson/Atkinson-Hyperlegible-Regular-102.otf",
    "sfb": "/usr/share/texlive/texmf-dist/fonts/opentype/public/atkinson/Atkinson-Hyperlegible-Bold-102.otf",
    "rm": "/usr/share/texlive/texmf-dist/fonts/opentype/impallari/librecaslon/LibreCaslonText-Regular.otf",
}


@lru_cache(maxsize=None)
def _font(face, size10):
    return ImageFont.truetype(FONTS[face], size=size10)


def width(text: str, pt: float = 16, face: str = "sf") -> float:
    """Width of text set at pt points, in inches."""
    f = _font(face, int(pt * 10))
    return f.getlength(text) / 10 / 72.27
