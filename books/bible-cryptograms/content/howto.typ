#import "/layout/book.typ": *
#let D = json("/build/book/data.json")
#let E = D.example

#metadata(none) <sec-howto>
#chapter-title("How to Solve a Cryptogram")
A cryptogram is a sentence written in a secret code. Every letter has been swapped for a different letter. Your task is to swap them back.

#section("The rules of the code")
- One code letter always stands for the same real letter, all through the puzzle. If *Q* means *E* once, it means *E* everywhere.
- No letter ever stands for itself. A code *A* is never a real *A*.
- Spaces, commas, colons and apostrophes are real. They show you where words begin and end.
- Each puzzle has its own code. What you learn in one puzzle does not carry over to the next.

#section("What is on each page")
#table(columns: (auto, 1fr), stroke: none, inset: (x: 0pt, y: 5pt), column-gutter: 14pt,
  [*Given letters*], [These are filled in for you, in bold, everywhere they appear.],
  [*The lines*], [Write each real letter on the line above its code letter.],
  [*Code key*], [The row *Code* lists every code letter. *Used* tells you how often it appears in this puzzle, so you do not have to count. In the row *Real*, write the real letter as soon as you know it.],
  [*Notes*], [Room to try out words before you write them in.],
)
Use a pencil with a good eraser. Guessing is allowed; that is half the fun.

#pagebreak()
#chapter-title("A Puzzle Solved Step by Step", sub: [#E.ref.replace("Psalms", "Psalm")])
Here is a puzzle with no letters given. Watch how it opens up, one step at a time. The shaded spaces show the letters found in each step.

#for (i, st) in E.states.enumerate() {
  block(breakable: false, above: 0.22in, below: 0.1in, {
    text(font: serif, size: 18pt, weight: "bold")[Step #(i + 1).]
    h(6pt)
    eval(st.why, mode: "markup")
    v(0.02in)
    example-state(E, st)
  })
}
#v(0.1in)
The verse: *#E.text* (#E.ref.replace("Psalms", "Psalm"))

#section("The method in short")
+ Write in the given letters everywhere they appear.
+ A code letter standing alone is *I*, *A* or *O*.
+ Look at the *Used* row: the most used code letter is often *E*, then *T* or *H*.
+ A three-letter code word that appears more than once is often THE or AND.
+ After an apostrophe comes *S*: LORD'S, FATHER'S.
+ Look for the old friends: UNTO, LORD, THEE, THOU, SHALL, HATH, and words ending in *-ETH*.
+ Fill in every new letter everywhere, then look for words that are almost finished.
+ Stuck? Take Hint 1, then Hint 2, then Hint 3. Every step leaves the rest to you.
