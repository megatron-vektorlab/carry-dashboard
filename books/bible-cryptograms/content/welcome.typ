#import "/layout/book.typ": *
#let D = json("/build/book/data.json")

#metadata(none) <sec-welcome>
#chapter-title("Welcome")
This book is for anyone who loves a good puzzle and a good word from Scripture. Each of the #D.puzzles.len() puzzles hides a well-loved verse or short passage from the King James Bible. Crack the code, and the verse is yours: a quiet word of comfort, hope or strength.

#section("How the book is arranged")
The verses are gathered into #D.themes.len() parts, from #D.themes.first().name to #D.themes.last().name. Inside each part the puzzles start easy and grow harder:

#let gr(l) = ("usually four or more letters are given", "usually two letters are given", "usually one letter is given", "no letters are given: just you and the code").at(l - 1)
#table(columns: (auto, auto, 1fr), stroke: none, inset: (x: 0pt, y: 5pt), column-gutter: 12pt, align: (left + horizon, left + horizon, left + horizon),
  ..range(1, 5).filter(l => str(l) in D.given_ranges).map(l => (stars(l), [*#("Easy", "Medium", "Hard", "Expert").at(l - 1)*], gr(l))).flatten()
)

Every puzzle has its own page, with large letters, a line above each letter for your answer and a code key to keep track; most pages also leave room for notes.

#section("If you get stuck")
Each puzzle shows the page where its hints begin and the page with its answer. The hints come in three small steps, so you can take just a little help. The solutions give every verse word for word, with its reference and a short line to reflect on.

#section("A word about the King James Version")
The verses keep the beloved King James words: THEE and THOU, HATH and SHALL. In these puzzles they are your best friends, as the next pages show.
