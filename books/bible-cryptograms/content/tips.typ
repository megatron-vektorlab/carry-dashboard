#import "/layout/book.typ": *
#let D = json("/build/book/data.json")
#let S = D.stats

#let wordrow(n) = S.top_by_length.at(str(n)).slice(0, 10).map(w => w.at(0)).join(" · ")

#metadata(none) <sec-tips>
#chapter-title("Tips for King James Verses", sub: "What the counting tells us")
We counted every letter and every word of the King James Bible (all #str(S.verses).slice(0, -3),#str(S.verses).slice(-3) verses). Here is what helps most when you solve.

#section("The most common letters")
#v(4pt)
#block(breakable: false, grid(columns: (1fr,) * 10, row-gutter: 6pt,
  ..S.letter_freq.slice(0, 10).map(r => align(center, text(font: serif, size: 26pt, weight: "bold", r.at(0)))),
  ..S.letter_freq.slice(0, 10).map(r => align(center, text(size: 16pt, fill: soft, str(calc.round(r.at(2), digits: 0)) + "%"))),
))
#v(4pt)
*E* is by far the most common letter: about one letter in eight. Then come *T* and *H*, because THE, THAT, THEY, THOU and UNTO are everywhere. The code letter that appears most often in a puzzle (see the *Used* row of the code key) is very often E, T or H.

#section("Short words")
#table(columns: (auto, 1fr), stroke: none, inset: (x: 0pt, y: 5pt), column-gutter: 14pt,
  [*1 letter*], [#S.one_letter_words.map(w => w.at(0)).join(" · ") #h(6pt) #text(fill: soft)[(O as in "O LORD")]],
  [*2 letters*], [#wordrow(2)],
  [*3 letters*], [#wordrow(3)],
  [*4 letters*], [#wordrow(4)],
)

#section("The most common words in this book")
In these #D.puzzles.len() verses the words you will meet most often are #D.book_top_words.slice(0, -1).join(", ") and #D.book_top_words.last(). Keep this list handy.

#block(breakable: false)[
#section("Letter patterns to look for")
#table(columns: (auto, 1fr), stroke: none, inset: (x: 0pt, y: 4pt), column-gutter: 14pt,
  [*THAT, HATH*], [four letters, the first and last the same],
  [*THEE, WILL*], [four letters ending in a double letter],
  [*SHALL*], [five letters ending in a double letter],
  [*UNTO, LORD*], [four different letters; UNTO often comes right before THEE, ME or HIM],
)]

#section("Old words you will meet often")
THEE · THOU · THY · THINE · YE · UNTO · HATH · SHALL · SAITH. If a three-letter code word sits where "your" would go, try *THY*; if a four-letter word starts like THE, try *THEE*, *THEM*, *THEY* or *THEN*.

#section("Word endings")
Many King James verbs end in *-ETH* (LOVETH, MAKETH, GIVETH) or *-EST* (KNOWEST). A long code word that ends in the same three code letters as another one may share that ending. Endings in *-ED* and *-ING* are common too.

#section("Double letters and apostrophes")
The most common double letters are #S.doubles.slice(0, 6).map(d => d.at(0)).join(", "). A double letter at the end of a short word is usually *LL* (ALL, SHALL, WILL) or *EE* (THEE). A code word ending with an apostrophe and one letter, like XYZW’K, usually ends in *’S*: LORD’S, FATHER’S.

#block(breakable: false)[
#section("Old words with new meanings")
A few King James words meant something different four hundred years ago:
#table(columns: (auto, 1fr), stroke: none, inset: (x: 0pt, y: 4pt), column-gutter: 14pt,
  [*careful*], [anxious, worried ("Be careful for nothing")],
  [*conversation*], [way of life],
  [*expected end*], [a hoped-for future],
  [*stayed*], [kept steady, fixed],
  [*suffer*], [allow, let],
  [*offend*], [cause to stumble],
  [*charity*], [love],
  [*quickened*], [made alive],
  [*shew*], [show],
  [*nigh*], [near],
)]

#section("A verse may end with a comma")
Each verse keeps its own King James punctuation. When a sentence carries on into the next verse, the puzzle ends with a comma, colon or semicolon. Nothing is missing.
