"""Book metadata (must match the KDP listing, the cover and the title page)."""
from __future__ import annotations

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLE = "Sprichwörter und Redewendungen für Senioren"
# The subtitle must appear on the cover exactly like this (KDP metadata rules).
SUBTITLE = "Gedächtnistraining in Großdruck: 100 Kopiervorlagen in A4 mit Lösungen und Gesprächsimpulsen"
SERIES = "Gedächtnistraining für Senioren in Großdruck"
VOLUME = 1
AUTHOR = "Ivan Sikuten"
YEAR = 2026

# ---- cover texts (every claim must stay true for the interior; gt.qa checks the numbers) ----
FRONT_LINES = ["Gedächtnistraining in Großdruck", "100 Kopiervorlagen in A4"]
FRONT_BADGES = ["3 Stufen", "mit Lösungen", "Gesprächsimpulse"]
BACK_HEADLINE = "Morgenstund hat Gold im Mund …"
BLURB = ("… und wie geht es weiter? Sprichwörter und Redewendungen kennt fast jeder seit Kindertagen. "
         "Sie wecken Erinnerungen, bringen Menschen zum Lachen und ins Gespräch. Dieses Buch macht daraus "
         "100 abwechslungsreiche Arbeitsblätter für die Gruppe, zu zweit oder allein.")
BULLETS = [
    "100 Kopiervorlagen in A4, in 10 Themen",
    "3 Stufen, viele Blätter mit gelöstem Beispiel",
    "Großdruck: Aufgaben in 20 Punkt",
    "Auf jeder Rückseite: Lösungen und Fragen zum Gespräch",
    "10 Vorlesegeschichten mit Sprichwort",
    "Kopiererlaubnis für die eigene Gruppe",
]

# Fields that must be filled in data/release.json before the book is final.
REQUIRED = ["edition_date", "publisher", "address", "email"]


def release() -> dict:
    path = os.path.join(ROOT, "data", "release.json")
    r = json.load(open(path)) if os.path.exists(path) else {}
    missing = [k for k in REQUIRED if not str(r.get(k, "")).strip()]
    r["missing"] = missing
    r["draft"] = bool(missing)
    return r
