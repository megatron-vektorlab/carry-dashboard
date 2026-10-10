"""Texts for the group leader's page on the back of every worksheet.

The steps and the easier/harder suggestions depend only on the exercise type and level;
solutions, hints and conversation prompts come from the sheet and the corpus.
"""
from __future__ import annotations

TRAINS = {
    "gaps": "Wortfindung, Langzeitgedächtnis",
    "circle": "Erkennen, Langzeitgedächtnis, Konzentration",
    "match": "Langzeitgedächtnis, Zuordnen",
    "complete": "Wortfindung, Langzeitgedächtnis, Formulieren",
    "scramble": "Strukturieren, logisches Denken, Sprachgefühl",
    "wrong": "Konzentration, genaues Lesen und Hören",
    "firstletters": "Wortfindung, Merkfähigkeit",
    "choice": "Sprachverständnis, Urteilsfähigkeit",
    "situation": "Zusammenhänge erkennen, Sprachverständnis",
    "wordsearch": "Wahrnehmung, Konzentration",
    "story": "Zuhören, Langzeitgedächtnis, Wortfindung",
    "talk": "Erinnern, Erzählen, Austausch in der Gruppe",
}

MINUTES = {1: "10 bis 15", 2: "15", 3: "15 bis 20"}

FIRST = "Lesen Sie die Aufgabe und das Beispiel gemeinsam laut vor."
LAST = "Lesen Sie zum Schluss jedes Sprichwort noch einmal ganz vor und sprechen Sie es gemeinsam."

STEPS = {
    ("gaps", 1): [FIRST, "Lesen Sie jeden Satz bis zur Lücke vor. Die Gruppe sucht das passende Wort im Kasten. Wer möchte, schreibt es auf.", LAST],
    ("gaps", 2): [FIRST, "Lesen Sie jeden Satz bis zur Lücke vor. Die Kästchen zeigen, wie viele Buchstaben das Wort hat; der erste steht schon da.", LAST],
    ("gaps", 3): ["Lesen Sie die Aufgabe vor.", "Lesen Sie jeden Satz bis zur Lücke vor und lassen Sie Zeit. Fällt das Wort nicht ein, lesen Sie die passende Hilfe weiter unten auf dieser Seite vor.", LAST],
    ("circle", 1): [FIRST, "Lesen Sie jeden Satz vor und an der Lücke beide Wörter. Welches klingt richtig? Es wird eingekreist.", LAST],
    ("circle", 2): [FIRST, "Lesen Sie jeden Satz vor und an der Lücke alle drei Wörter. Welches klingt richtig? Es wird eingekreist.", LAST],
    ("match", 0): ["Lesen Sie zuerst alle Anfänge vor, dann alle Enden.", "Die Gruppe sucht zu jedem Anfang das passende Ende. Verbunden wird mit einem Strich; man kann auch nur den Buchstaben sagen.", "Lesen Sie die fertigen Sprichwörter gemeinsam vor."],
    ("complete", 2): [FIRST, "Lesen Sie den Anfang vor und machen Sie eine kleine Pause. Oft fällt das Ende von selbst ein. Das erste Wort steht schon auf der Linie.", LAST],
    ("complete", 3): ["Lesen Sie die Aufgabe vor.", "Lesen Sie den Anfang vor und machen Sie eine kleine Pause. Oft fällt das Ende von selbst ein. Erst sagen, dann schreiben.", LAST],
    ("scramble", 2): [FIRST, "Lesen Sie die Wörter langsam vor. Welches Sprichwort könnte es sein? Das erste Wort steht schon auf der Linie.", LAST],
    ("scramble", 3): ["Lesen Sie die Aufgabe vor.", "Lesen Sie die Wörter langsam vor. Welches Sprichwort könnte es sein? Erst sagen, dann schreiben.", LAST],
    ("wrong", 0): [FIRST, "Lesen Sie jeden Satz vor. Was klingt komisch? Oft lacht die Gruppe schon beim Vorlesen.", "Lesen Sie danach das richtige Sprichwort vor und sprechen Sie es gemeinsam."],
    ("firstletters", 0): ["Lesen Sie die Aufgabe vor.", "Lesen Sie die Anfangsbuchstaben langsam vor und fragen Sie: Welches Sprichwort beginnt so?", "Ist es gefunden, wird es gemeinsam gesprochen und aufgeschrieben."],
    ("choice", 0): ["Lesen Sie die Aufgabe vor.", "Lesen Sie die Redewendung vor und danach die drei Erklärungen. Die Gruppe entscheidet gemeinsam.", "Fragen Sie: In welcher Lage sagt man das?"],
    ("situation", 0): ["Lesen Sie die Aufgabe vor.", "Lesen Sie die kleine Szene vor und danach die drei Sprichwörter. Welches passt am besten?", "Fragen Sie: Wem ist so etwas auch schon passiert?"],
    ("wordsearch", 0): ["Lesen Sie die Wörter im Kasten vor. Fragen Sie: In welchem Sprichwort kommt das Wort vor?", "Dann wird gesucht: nur von links nach rechts und von oben nach unten. Gefundene Wörter werden eingekreist.", "Am Ende sagt die Gruppe zu jedem Wort das passende Sprichwort."],
    ("story", 0): ["Lesen Sie die Geschichte langsam und deutlich vor. Die Teilnehmenden können mitlesen.", "Halten Sie vor dem letzten Satz inne: Welches Sprichwort passt? Die Wörter unter der Geschichte helfen.", "Sprechen Sie das Sprichwort zum Schluss gemeinsam."],
    ("talk", 0): ["Lesen Sie das Sprichwort langsam vor und sprechen Sie es gemeinsam.", "Stellen Sie eine Frage nach der anderen. Es gibt keine richtigen oder falschen Antworten; wer nichts sagen möchte, hört einfach zu.", "Fassen Sie zum Schluss freundlich zusammen, was erzählt wurde."],
}

EASIER = {
    ("gaps", 1): "Nur drei Sätze bearbeiten oder zwei Wörter zur Auswahl vorlesen.",
    ("gaps", 2): "Zwei Wörter zur Auswahl nennen.",
    ("gaps", 3): "Den ersten Buchstaben verraten.",
    ("circle", 0): "Nur ein Wort zur Auswahl vorlesen und fragen: Stimmt das?",
    ("match", 0): "Nur die ersten drei Paare bearbeiten.",
    ("complete", 0): "Zwei mögliche Enden zur Auswahl vorlesen.",
    ("scramble", 2): "Das zweite Wort verraten; das erste steht schon auf der Linie.",
    ("scramble", 3): "Die ersten beiden Wörter verraten.",
    ("wrong", 0): "Auf das falsche Wort zeigen; die Gruppe sucht nur noch das richtige.",
    ("firstletters", 0): "Ein Wort aus dem Sprichwort verraten.",
    ("choice", 0): "Nur zwei der drei Erklärungen vorlesen, darunter die richtige.",
    ("situation", 0): "Nur zwei der drei Sprichwörter vorlesen, darunter das passende.",
    ("wordsearch", 0): "Im Gitter auf die Zeile oder Spalte zeigen, in der das Wort steht.",
    ("story", 0): "Die drei Wörter zur Auswahl gleich mit vorlesen.",
    ("talk", 0): "Nur eine Frage stellen und viel Zeit lassen.",
}

HARDER = {
    ("gaps", 1): "Den Kasten abdecken.",
    ("gaps", 2): "Die Kästchen abdecken und das Wort frei finden.",
    ("gaps", 3): "Nach weiteren Sprichwörtern mit demselben Wort fragen.",
    ("circle", 0): "Die Wörter abdecken und frei ergänzen.",
    ("match", 0): "Die Enden abdecken: Wer weiß das Ende auswendig?",
    ("complete", 0): "Nach der Bedeutung fragen: Wann sagt man das?",
    ("scramble", 0): "Das Sprichwort danach auswendig sagen.",
    ("wrong", 0): "Selbst ein Sprichwort mit einem falschen Wort sagen und die anderen raten lassen.",
    ("firstletters", 0): "Mündlich besprechen, was das Sprichwort bedeutet.",
    ("choice", 0): "Die Erklärungen abdecken und mündlich erklären lassen.",
    ("situation", 0): "Zu einem Sprichwort eine eigene kleine Szene erzählen lassen.",
    ("wordsearch", 0): "Zu jedem Wort ein weiteres Sprichwort suchen.",
    ("story", 0): "Eine eigene kleine Geschichte zum Sprichwort erzählen lassen.",
    ("talk", 0): "Fragen: Welches Sprichwort würden Sie einem jungen Menschen mitgeben?",
}


def pick(table: dict, typ: str, level: int):
    return table.get((typ, level), table.get((typ, 0)))
