#import "/layout/book.typ": *
#let D = json("/build/book/data.json")

#metadata(none) <sec-welcome>
#chapter-title("Welcome")
This book is for anyone who loves a good puzzle and a good word from Scripture. Each of the #D.puzzles.len() puzzles hides one well-loved verse from the King James Bible. Crack the code, and the verse is yours: a few quiet minutes with a pencil, and a word of comfort, hope or strength at the end.

#section("How the book is arranged")
The verses are gathered into #D.themes.len() parts, from #D.themes.first().name to #D.themes.last().name. Inside each part the puzzles start easy and grow harder:

#let gr(l) = {
  let r = D.given_ranges.at(str(l), default: none)
  if r == none { [] } else if r.at(1) == 0 [no letters are given: just you and the code] else if r.at(0) == r.at(1) [#r.at(0) letters are given] else [#r.at(0) to #r.at(1) letters are given]
}
#table(columns: (auto, auto, 1fr), stroke: none, inset: (x: 0pt, y: 5pt), column-gutter: 12pt, align: (left + horizon, left + horizon, left + horizon),
  ..range(1, 5).filter(l => str(l) in D.given_ranges).map(l => (stars(l), [*#("Easy", "Medium", "Hard", "Expert").at(l - 1)*], gr(l))).flatten()
)

Every puzzle has its own page, with large letters, a line above each letter for your answer, a code key to keep track, and room for notes.

#section("If you get stuck")
Each puzzle tells you where its hints and its answer are. The hints come in three small steps, so you can take just a little help and still finish the puzzle yourself. The solutions give every verse in full, with its reference.

#section("A word about the King James Version")
The verses keep the beloved words of the King James Bible: THEE and THOU, HATH and SHALL, LOVETH and KNOWETH. Far from making the puzzles harder, these words become your best friends, and the next pages show you why.
