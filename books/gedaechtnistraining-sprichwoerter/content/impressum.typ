#import "/layout/book.typ": *
#let D = json("/build/book/data.json")
#let R = D.release
#set text(size: 16pt)
#set par(spacing: 0.7em, leading: 0.5em)
*#D.title* \
#D.subtitle \
Reihe „#D.series“, Band #D.volume

#R.at("edition", default: "1. Auflage"), #R.at("edition_date", default: "") \
© #D.year #D.author. Alle Rechte vorbehalten.

#text(weight: "bold")[Kopiererlaubnis.] Die Seiten mit dem Vermerk „Kopiervorlage“ dürfen für die Arbeit mit älteren Menschen in der benötigten Anzahl vervielfältigt werden, auch vergrößert (zum Beispiel auf DIN A3). Das gilt für Privatpersonen, die das Buch gekauft haben, für alle Mitarbeitenden der Einrichtung, die das Buch gekauft hat, an einem Standort (zum Beispiel Pflegeheim, Tagespflege, Praxis oder Begegnungsstätte), und für Gedächtnistrainerinnen und Gedächtnistrainer in ihren eigenen Gruppen und Kursen. Die Kopien dürfen an die Teilnehmenden ausgegeben werden und bei ihnen bleiben.

Nicht erlaubt ist es, Vorlagen oder Kopien an andere Einrichtungen oder Standorte zu deren eigener Verwendung weiterzugeben, Kopien zu verkaufen, Seiten einzuscannen oder digital zu verbreiten (zum Beispiel per E-Mail, im Internet oder in einer Cloud) oder Inhalte in andere Werke zu übernehmen. Der Vermerk „© #D.year #D.author“ auf den Seiten darf nicht entfernt werden. Anfragen zu weiteren Nutzungen, etwa für mehrere Standorte: #R.email

#text(weight: "bold")[Hinweis.] Die Übungen dienen der geistigen Anregung, der Unterhaltung und dem Gespräch. Sie sind kein Test und kein Diagnoseinstrument und ersetzen keine ärztliche oder therapeutische Behandlung. Die Bewegungsideen sind für das Sitzen gedacht; jede Person macht nur so viel mit, wie es angenehm ist.

Die Sprichwörter und Redewendungen sind überliefertes Volksgut. Auswahl, Anordnung und Gestaltung der Kopiervorlagen sind urheberrechtlich geschützt.

Herausgeber und Hersteller: #R.publisher, #R.address · #R.email \
Druck: siehe letzte Seite. #if R.at("isbn", default: "KDP") == "KDP" [ISBN: siehe Rückseite des Buches.] else [ISBN #R.isbn]
