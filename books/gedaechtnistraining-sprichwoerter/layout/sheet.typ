// Renders one participant page (Kopiervorlage) from its data (see gt/exercises.py).
#import "book.typ": *

// Five words: 3 + 2, so the fifth word does not stand alone in a second row.
#let bank-cols(words, wide: 4) = {
  let m = calc.max(..words.map(w => w.clusters().len()))
  if m > 16 { 2 } else if m > 10 or words.len() == 5 { 3 } else { wide }
}

#let render-sheet(s) = {
  current-sheet.update(s.num)
  sheet-head(num: s.num, title: s.title, level: s.level, chapter: s.chapter)
  task(s.task)
  if s.type == "gaps" {
    if "bank" in s { bank-grid(s.bank, cols: bank-cols(s.bank), title: "Diese Wörter fehlen:") }
    ex-gaps(s)
  } else if s.type == "circle" { ex-circle(s)
  } else if s.type == "match" { ex-match(s)
  } else if s.type == "complete" { ex-complete(s)
  } else if s.type == "scramble" { ex-scramble(s)
  } else if s.type == "wrong" { ex-wrong(s)
  } else if s.type == "firstletters" { ex-firstletters(s)
  } else if s.type == "choice" { ex-choice(s)
  } else if s.type == "situation" { ex-situation(s)
  } else if s.type == "wordsearch" { ex-wordsearch(s)
  } else if s.type == "story" { ex-story(s)
  } else { panic("unknown sheet type " + s.type) }
}
