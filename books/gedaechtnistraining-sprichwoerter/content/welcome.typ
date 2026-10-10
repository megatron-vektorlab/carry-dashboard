#import "/layout/book.typ": *
#let D = json("/build/book/data.json")
#chapter-title("Willkommen!")
„Morgenstund hat Gold im Mund“, „Wer anderen eine Grube gräbt …“: Sprichwörter und Redewendungen begleiten uns ein Leben lang. Viele haben wir als Kind von den Eltern und Großeltern gehört, in der Schule gelernt oder bei der Arbeit oft gesagt. Sie sitzen tief im Gedächtnis und kommen meist ganz von selbst wieder, sobald jemand den Anfang sagt.

Dieses Buch lädt dazu ein, die alten Bekannten wiederzuentdecken: beim Raten, Ergänzen und Verbinden, beim Vorlesen und vor allem im Gespräch.

#section[So ist das Buch aufgebaut]
- *#D.chapters.len() Kapitel mit je 10 Arbeitsblättern:* #D.chapters.map(c => c.name).join("; ").
- *Jedes Arbeitsblatt steht auf einer rechten Seite* und ist eine Kopiervorlage.
- *Auf der Rückseite jedes Blattes* stehen die Lösungen, Fragen zum Gespräch und Ideen, wie die Aufgabe leichter oder anspruchsvoller wird, bei vielen Blättern auch Hilfen, wenn ein Wort nicht einfällt.
- *Jedes Kapitel beginnt* mit einer Aufwärmrunde und mit Ideen zum Erzählen, Bewegen und Mitbringen. In jedem Kapitel gibt es eine kleine Geschichte zum Vorlesen.
- *Hinten im Buch* finden Sie ein Blatt zum Erzählen („Mein Sprichwort“), ein Sprichwort-Bingo mit 12 Karten, Raterunden für zwischendurch, eine Liste zum Abhaken aller Blätter und alle Sprichwörter und Redewendungen von A bis Z, jeweils mit einer kurzen Erklärung.

#section[Drei Stufen]
#grid(columns: (22mm, 1fr), row-gutter: 0.7em,
  level-mark(1), [*Mit Hilfen:* Wörter zur Auswahl, oft auch ein gelöstes Beispiel.],
  level-mark(2), [*Mit kleinen Hilfen:* zum Beispiel der erste Buchstabe, das erste Wort oder drei Antworten zur Auswahl.],
  level-mark(3), [*Mit wenigen Hilfen:* frei ergänzen, ordnen oder Wörter suchen und aufschreiben.])
#v(0.4em)
Das Zeichen für die Stufe steht unten auf jedem Blatt. Jedes Blatt steht für sich: Sie können überall anfangen, gern auch mit der ersten Stufe. Die Blätter der dritten Stufe greifen viele Sprichwörter des Kapitels noch einmal auf: Was vorher mit Hilfen gelöst wurde, wird jetzt frei erinnert. Sie eignen sich gut als Wiederholung am Ende eines Kapitels.

#section[Allein, zu zweit oder in der Gruppe]
*Allein:* Lösen Sie ein Blatt in Ruhe mit dem Bleistift. Die Lösung steht auf der Rückseite; wer nachschlagen möchte, was ein Sprichwort bedeutet, findet es hinten im Buch. \
*Zu zweit:* Eine Person liest vor, die andere ergänzt. Die Fragen auf der Rückseite laden zum Erzählen ein. \
*In der Gruppe:* Kopieren Sie die Blätter, gern auch auf A3 vergrößert. Auf den nächsten Seiten finden Sie Hinweise für die Gruppenleitung.

Viel Freude beim Erinnern, Raten und Erzählen!
