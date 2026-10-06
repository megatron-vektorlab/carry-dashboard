#import "/layout/book.typ": *
#let D = json("/build/book/data.json")
#let R = D.release
#v(1fr)
#set text(size: 16pt)
#set par(spacing: 0.75em)
*#D.title* \
#D.subtitle \
Volume 1

#R.at("edition", default: "First edition"), #R.at("edition_date", default: "")

Copyright © #D.year #D.author. All rights reserved. The selection and arrangement of the verses, the puzzles, hints, introductions and all other original text in this book may not be reproduced without permission, except for brief quotations in reviews. You are welcome to copy single puzzle pages for your own use or for a Bible study group.

Scripture quotations are from the King James Version (Authorized Version), standard 1769 text, which is in the public domain in the United States.
#if R.at("uk_permission", default: false) [Rights in the Authorized Version in the United Kingdom are vested in the Crown. Reproduced by permission of the Crown's patentee, Cambridge University Press.] else [Rights in the Authorized Version in the United Kingdom are vested in the Crown.]

*How the puzzles were checked.* Every verse was compared letter by letter with five independent public-domain copies of the King James text. Every puzzle was checked by computer: it decodes to the verse exactly, no letter stands for itself, and with the given letters only one reading fits, tested against every word in the King James Bible.

Publisher: #R.publisher, #R.address · #R.email \
#if R.at("isbn", default: "KDP") == "KDP" [ISBN: see the back cover. Independently published.] else [ISBN #R.isbn]
