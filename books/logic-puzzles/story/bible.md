# Story Bible: The Thimble Harbor Puzzle School, Book 1

*Cozy Mystery Logic Puzzles for Beginners* — 100 puzzles, 7 chapters, one season in Thimble Harbor.

This is the shared reference for every theme writer. Read sections 1-5 once, then work from your slots in
section 6. The machine-readable cast and name pool live in `story/cast.py`. Format rules for theme files are in
`THEMES.md`; this bible never overrides them.

**Ground rules for every writer**

- Ada Quill and the reader (her apprentice) are never suspects, never grid names, and never "the answer".
- Pets (Inkwell, Pilot) are never grid names. They may appear in a story setup.
- Grid names come only from the 12 cast names and the 45-name pool below. Use the names listed for your slot;
  if you must swap one, keep first letters different, keep the list out of alphabetical order, and keep each
  cast member's total inside 8-20 appearances (the counts are in section 3).
- Every grid value is 12 characters or fewer. The example values in section 6 already obey this.
- No murder, no violence, no injuries, nothing scary. The worst thing that happens in this book is a sunk
  rowboat and a borrowed lamp. Culprits are pranksters, borrowers, or well-meaning people who got muddled.
- Never write anything in a story that is also a clue, and never hint at the finale's answer (Jonah) in
  chapters 1-6 beyond the planted threads listed in section 5.
- **Jonah's secret stays secret.** His surname (Bell), his family line (great-grandson of Silas Bell, the last
  keeper) and his ferry's name (the *Silas B.*) never appear in any puzzle story or Ada intro, in chapters 1-6
  or in 96-100. In stories he is "Jonah" or "the ferry captain", and the boat is "the ferry". They are revealed only in the bonus solution and the epilogue. Silas Bell may still be named as the
  last keeper (#64), but never linked to Jonah.
- **The engine forces only the culprit value** (plus, if the theme lists them in `answer_has`, the answer
  person's values in unordered categories). Ordered values (times, ages) and every value of everyone else are
  drawn at random. So a story fact about a person must hold for *any* value they might get: never give a cast
  member an Age range that does not fit them (Teddy is 19, Mabel is retired), put each cast member in at most one
  Age grid in the book, never pair two categories that go together in real life (ad size and price, jug and
  gallons), and in the finale keep every time window and category consistent with section 7 whatever the engine
  draws.
- US spelling, dollars, a.m./p.m., Main Street.

---

## 1. Voice: Ada Quill

Ada Quill edited the puzzle page of the *Thimble Harbor Gazette* for forty-one years. She is retired in name
only: she still keeps the puzzle desk by the front window, a sharp pencil, and a tin of lemon drops. She has
taken on an apprentice (the reader) to keep the page going.

- **Warm, wry, precise.** Short sentences. One idea at a time. She never gushes and never scolds.
- **Her one habit: she calls the reader "partner."** Use it at most once per text, never twice in a row of
  puzzles' intros. No other pet names ("dear", "kiddo", "friend") ever.
- She explains a step by naming it and then doing it: "That's a pair clue. Two people, two facts, no overlap."
- She is fond of the townsfolk and teases them gently, never meanly.
- She does not use exclamation marks, except once, in the finale.
- She believes in pencils, erasers and second looks. Her favorite word is "so": "So it isn't Gus. So it's Rosa."

Sample lines:

> "Every clue is a small promise, partner. Our job is to hold the town to it."

> "Mark the X first. The O can wait. The O always waits for the X."

> "Gus says it'll snow by Thursday. His knee is usually right. His knee is not a clue."

---

## 2. The Town: Thimble Harbor

A small harbor town on a crooked thumb of the New England coast, with one main street, one ferry, one
lighthouse, and far too many opinions about pie. Use these places by name; invent small extra spots (a bench,
a cove, a shed) freely.

| Place | One line |
|---|---|
| **Thimble Point Light** | White brick lighthouse at the tip of the point, built 1876; its brass Keeper's Lamp turns 150 this year. Retired from guiding ships in 1976, when the automatic beacon on Gull Rock took over, so its light is **ceremonial only**: no boat depends on it. The lamp is lit on special nights, and every evening of Lantern Festival week (on a simple timer, dusk to 10 p.m.); on Festival night it gets its 150th-birthday lighting ceremony. Reached by a causeway at low tide, or by boat. |
| **The Lighthouse Museum** | The old keeper's cottage beside the light, run by Lena; gift shop, logbooks, a creaky spiral stair to the lantern room. |
| **The Thimble Harbor Gazette** | Two-story clapboard newspaper office on Main Street; Ada's puzzle desk sits in the front window, Inkwell the cat sleeps on the proofs. |
| **The Harbor Office** | Otis's shingled shack at the head of the town pier; tide charts, the radio, and the hook where the spare lighthouse key hangs. |
| **The Ferry Dock** | Where Jonah's ferry leaves for Gull Island, Cobb Point and Pine Key; a big clock hangs over the ticket window. (The ferry is named the *Silas B.*, but that name is secret until the epilogue: in stories it is just "the ferry".) |
| **Salt & Sugar Bakery** | Rosa's bakery on Main Street; the town's unofficial meeting room from 6 a.m. |
| **Mahoney's General Store** | Gus sells bait, birthday cards, paint, rubber boots, and gossip; the Keeper's Lamp fund jar sits by the register. |
| **Gull's Rest Inn** | Priya's eight-room inn on the hill, every room named for a seabird; famous parlor, famous umbrella stand. |
| **Okafor Boatyard** | Felix's yard on the east shore: slips, a paint shed, a cider press, and a copper whale weathervane on the roof. Most boats come out of the water in November; Felix keeps his five rental rowboats (Minnow, Pebble, Skipjack, Teacup, Puffin) and his own small dinghy in until the Lantern Festival, for the lantern flotilla. |
| **Thimble Harbor Library** | Brick library with a book drop, a story-hour rug, and the town's oldest records, including the 1876 keeper's logbook. |
| **St. Brendan's Church Hall** | Hattie's kingdom: suppers, rummage sales, auctions, raffles, and a bell tower with a temperamental bell. |
| **The Town Green** | Grass, a bandstand and a war memorial in the middle of town; kites in spring, fireworks in July, the Lantern Festival in December (lanterns on the green, and a lantern flotilla of rowboats on the harbor). |
| **Thimble Beach** | The sandy curve south of the pier; tide pools, sandcastles, and the clambake pit. |
| **Hilltop Orchard** | Apples, a corn maze, a hayride and a cider stand just outside town. |
| **The County Fairgrounds** | Ten minutes inland; the August fair with its goat pens, pie tent and Ferris wheel. |

Harbor features for boat puzzles: Gull Rock (with the automatic beacon), East Cove, the Narrows, Seal Ledge, Gull
Island, Cobb Point, Pine Key.

---

## 3. Recurring Cast

Twelve townsfolk. In grids, use the first name only. Surnames may appear in stories, **except Jonah's** (see
the ground rules: his surname and family line are the finale's secret). Counts are this bible's planned
appearances (grid name or story role) across the 100 slots.

| Name | Role | Quirk | Sample line | Slots (count) |
|---|---|---|---|---|
| **Hattie** | church hall coordinator (Hattie Pruitt), runs every supper, social and rummage sale | carries a clipboard with a list of her other lists | "If it isn't on the list, it isn't happening. Who has the list?" | 4, 12, 17, 24, 32, 38, 51, 56, 66, 68, 74, 76, 79, 85, 89, 98, 100 (17) |
| **Rosa** | baker at the Salt & Sugar Bakery (Rosa Delgado) | gives each of her sourdough starters a name and a birthday | "Gloria needs feeding at six. Gloria is a starter. Please keep up." | 2, 8, 17, 27, 31, 45, 47, 54, 66, 70, 79, 81, 88, 95, 98 (15) |
| **Otis** | harbormaster (Otis Lund), keeps the spare lighthouse key on a hook in the harbor office | whistles sea shanties, always slightly off-key | "Tide's turning at four. So am I, if anyone touches my charts." | 4, 11, 18, 23, 30, 33, 38, 46, 50, 57, 62, 68, 78, 83, 84, 88, 93, 96 (18) |
| **Wren** | town librarian (Wren Takahashi) | whispers even outdoors; remembers everyone by their overdue books | "(whispering) You returned this in 1998. I remember the coffee ring." | 2, 8, 13, 26, 37, 42, 51, 64, 71, 76, 83, 86, 91, 93, 100 (15) |
| **Felix** | boatbuilder, owner of Okafor Boatyard (Felix Okafor) | keeps a pencil behind each ear and calls everything 'shipshape' | "Shipshape. Mostly shipshape. Hand me the other pencil." | 3, 11, 16, 25, 30, 35, 44, 53, 58, 61, 71, 77, 80, 82, 90, 94, 97, 99 (18) |
| **Gus** | owner of Mahoney's General Store (Gus Mahoney) | forecasts the weather by his left knee, and is usually right | "Knee says rain by Thursday. Buy the umbrella now, save yourself the trip." | 6, 10, 16, 19, 27, 36, 38, 40, 47, 55, 60, 65, 72, 73, 79, 84, 90, 95, 96 (19) |
| **Priya** | innkeeper of the Gull's Rest Inn (Priya Nair) | keeps a lost-and-found of forty-one umbrellas and returns every one | "Forty-one umbrellas, forty-one owners. I am patient." | 6, 9, 20, 29, 35, 43, 52, 58, 63, 70, 77, 81, 87, 94, 99 (15) |
| **Jonah** | ferry captain of the Thimble Harbor ferry. **Secret, for writers only:** surname Bell, great-grandson of the last lighthouse keeper; never in any puzzle story (see ground rules) | on time to the minute; tinkers with old brass in his ferry workshop | "Ferry leaves at 7:30. Not 7:31. Pilot, life vest." | 7, 14, 22, 23, 33, 37, 38, 40, 50, 63, 67, 73, 88, 91, 98, 99 (16) |
| **Mabel** | retired schoolteacher and garden club president (Mabel Fitch) | corrects grammar on signs; locked in a friendly dahlia rivalry | "It's 'fewer cars,' not 'less cars.' Also, those are my dahlias." | 6, 9, 14, 21, 24, 26, 34, 41, 49, 54, 59, 61, 65, 78, 81, 87, 95, 99 (18) |
| **Teddy** | the Gazette's 19-year-old photographer and bicycle paperboy (Teddy Sousa) | never without his camera; working on a '150 Years of Light' photo series | "Hold still, just one more, the light's perfect." | 1, 5, 15, 22, 29, 34, 38, 43, 47, 53, 64, 75, 84, 91, 96, 97, 98, 100 (18) |
| **Lena** | curator of the Historical Society and the lighthouse museum (Lena Kowalski) | wears white cotton gloves to touch anything older than she is | "Gloves on, please. That lamp is older than all of us put together." | 1, 7, 19, 22, 28, 36, 38, 43, 53, 55, 72, 73, 84, 91, 96, 100 (16) |
| **Nico** | lobsterman, skipper of the lobster boat Persistence (Nico Papas) | tells tall tales; the lobster gets bigger every time | "Biggest lobster I ever saw. Size of a canoe. Smaller canoe than last time." | 5, 13, 18, 25, 32, 39, 45, 48, 62, 69, 80, 86, 90, 94, 97 (15) |

**Pets (never grid names):**

- **Inkwell** — the Gazette's gray office cat. Sleeps on the puzzle proofs, steps on wet ink, is suspected of
  everything and guilty of nothing.
- **Pilot** — Jonah's elderly beagle, who rides the ferry in a small orange life vest and greets every passenger.

**Not suspects, not grid names:** Ada Quill; the reader; **Silas Bell**, the last keeper of Thimble Point Light
(Jonah's great-grandfather, long gone; he appears only in the threads, as a name in the old logbook). A story may
call him "Silas Bell, the last keeper", but nothing before the bonus solution may connect him to Jonah.

---

## 4. Name Pool (45 one-off names)

Use these for everyone who is not in the cast. Each starts with a letter that makes a five-name grid easy, none
looks like another name in the pool or cast, and all are 3-7 letters.

Amara, Arlo, Basil, Bea, Boris, Carmen, Cass, Cyrus, Della, Dev, Dot, Elsa, Emil, Enzo, Faye, Gideon, Greta, Hal, Hugo, Imani, Ivan, Jade, Kenji, Kit, Linus, Lou, Marta, Milo, Nadia, Olive, Oscar, Pablo, Pearl, Quinn, Ruben, Sam, Selma, Tariq, Tova, Una, Vera, Vito, Walt, Yusuf, Zeke

Do not add new names without checking them against this list and the cast for look-alikes (no Ann/Anna, no Rosa/Rose, no Teddy/Eddie).

---

## 5. Season Arc

The book runs from April to the winter solstice. Each chapter is one stretch of the season. Stories should
mention the season's weather and events lightly; the town events below are free for any writer to use.

### The secret behind the threads (for writers only)

Thimble Point Light turns 150 this year. It has not guided ships since 1976 (the automatic beacon on Gull Rock
does that), so its 1876 brass **Keeper's Lamp** is a ceremonial light: dark most of the year, lit on special
nights, and lit every evening of Lantern Festival week on a timer, dusk to 10 p.m. On Festival night (the winter
solstice) it gets its 150th-birthday lighting ceremony. Because no boat depends on it, the lamp going dark is a
town mystery, never a safety scare. **Jonah Bell**, ferry captain, is the great-grandson of Silas Bell,
the last keeper. Jonah has noticed that the lamp's old reflector is too tarnished to shine properly, and he has
quietly decided to fix it himself as a gift to the town: testing it at night (the odd flickers), reading up on it
(the logbook, borrowed on Silas's old library card as a private joke: "S. Bell"), and finally, on Festival Eve,
taking the lamp to his ferry workshop to re-silver it. He leaves a note, "It will shine again", signed with a
tiny drawn bell. On Festival night the lamp returns for its birthday lighting, brighter than it has been in fifty
years.

**Teddy Sousa** is the red herring. His "150 Years of Light" photo series keeps putting him near the lighthouse,
near the key, and near a camera.

Do not reveal any of this in chapters 1-6. Plant only what the episode list says. Jonah's surname, family line
and ferry name never appear in a puzzle story at all (ground rules).

### Running threads

1. **The Keeper's Lamp** — announced in April (#7), painted around in May (#22), photographed in July (#38),
   funded in October (#72, #73), its brass found mysteriously polished in November (#91, mentioned as a separate
   puzzle that predates and has nothing to do with that episode's question), gone on Festival Eve (#96-100).
2. **The blinking light** — an odd flicker in the dark lantern room after closing (#43, July); ferry passengers
   see a light blink out at the Point (#63, September); in the finale, on a Festival-week evening when the lamp is
   lit, it blinks three times and goes dark at 9 p.m., an hour before its timer would switch it off.
   (Three blinks was Silas Bell's old "all's well" signal; reveal only in the epilogue.)
3. **"S. Bell"** — the keeper's logbook is checked out to an "S. Bell" (#64, September). Nobody solves this
   until the epilogue.
4. **The spare key and the boats** — Felix's dinghy turns up farther up the beach than he left it (#30, June);
   the spare key wanders off for a day and comes back (#84, November: Teddy borrowed it for photos, which makes
   him look guilty in the finale).

### Chapter by chapter

| Ch. | Puzzles | Months | Town events | Thread beats |
|---|---|---|---|---|
| 1 First Clues | 1-10 | April | spring rain, seed swap, rummage sale, the lighthouse opens for the season, tulip planting | Ada takes on her apprentice (#1); Lena announces the lamp's 150th-birthday lighting (#7); Teddy starts his paper route (#5) |
| 2 The Full Grid | 11-30 | May-June | Spring Regatta, Kite Day, Mother's Day, Rhubarb Social, bird count, Memorial Day parade, garden tour, graduations, Water Day on the beach, dinghy race | Volunteers paint the lighthouse (#22); Felix's dinghy has moved (#30) |
| 3 First, Next, Last | 31-46 | July-early August | Fourth of July parade, fireworks on the green, clambake, library book sale, sailing lessons, story hour, blueberry picking, fair entries | Committee photo, one member glancing up at the lantern room (#38); the "odd flicker" note (#43) |
| 4 Truth or Fib? | 47-58 | August | County Fair (goats, pies, quilts, Ferris wheel), Blueberry Festival, town meeting, ice cream social, chowder cook-off, Harbor Days | The anniversary postcards vanish (#53); stakes still small and silly |
| 5 Two Clues at Once | 59-78 | September-October | Labor Day yard sales, apple picking, evening classes, fishing derby, pumpkin weigh-off, harvest supper, corn maze, harvest shuttle, firewood, Halloween parade (#78, the chapter's last puzzle) | The light blinks at the Point (#63); "S. Bell" (#64); the lamp ad and fund jar (#72, #73) |
| 6 Case Files | 79-95 | November | pie auction for Thanksgiving orders (early November), first frost, boats hauled out, Thanksgiving, holiday craft fair (the Saturday after Thanksgiving), gingerbread | Bigger mysteries: heirlooms, a sunk rowboat; the wandering key (#84); footprints in the lighthouse, and the lamp's brass found polished (#91) |
| 7 The Lighthouse Affair | 96-100 | December 20-21 | Lantern Festival week (the lamp lit each evening); on Festival Eve a lantern-flotilla rehearsal on the harbor and a rehearsal on the green; the Festival itself in the epilogue | The Keeper's Lamp disappears; five linked puzzles; "Putting It All Together" |

**Dated stories must stay in order.** Chapter 6 runs: #79 early November (pie auction), #80 a frosty morning
before haul-out, #85 the Sunday before Thanksgiving, #87 Thanksgiving afternoon, #89 the Saturday after
Thanksgiving (holiday craft fair); the others carry no date. In chapter 5, Halloween is #78, the last puzzle of
October. In chapter 2, #17 is a May social, before the Memorial Day parade (#19).

Tone ladder: chapter 1 stakes are a lost glove; chapter 4 a goat in the pie tent; chapter 6 a missing heirloom
or a sunk rowboat; chapter 7 the town's beloved lamp, the night before its birthday. Nobody is ever hurt, and
every culprit in chapters 6-7 turns out to have a forgivable reason (a prank, a borrowing, a surprise, a
muddle). Writers may hint at the reason in the story but must not give clue information.

---

## 6. Episode List

Format: number and working title, chapter/family/size/stars, premise, then the grid: names first, then each
category with exactly n example values. Categories marked **(ordered)** are the slot's one ordered category;
the step is the unit for "exactly N more" clues and the values are evenly spaced. "Cast" lists recurring
characters in the grid and, after "story", those who appear only in the setup.

Chapter 6-7 entries give the whodunit question and the category value that identifies the culprit. Where an
answer is marked **forced**, set `"answer"` in the theme; otherwise let the engine decide. Every chapter 6-7
premise also carries one line of story evidence (marked *Evidence* below) that explains why the culprit value
points to the culprit ("a witness saw a yellow slicker"). It names the value, never a person, so it is not a
grid clue. Put it in the story.

Liar entries (47-58) give the suspects and the deed. The engine picks the culprit at random, so the deed must
be something any of the suspects could plausibly have done, and the story must not depend on who did it.


### Chapter 1: First Clues (April)

**1. Ada's Welcome Tea** — first3, n=3, k=2, *

Ada threw a welcome tea at the Gazette for her new apprentice, and three neighbors dropped by. She wants to remember who drinks what for next time, and she says that is your first assignment.

- Names: Teddy, Una, Lena
- Tea: Earl Grey, mint, chamomile
- Cast: Teddy, Lena

**2. The Seed Swap Envelopes** — first3, n=3, k=2, *

At the library's spring seed swap, three gardeners' envelopes lost their labels in a draft. Wren needs to know who brought which seeds so the thank-you notes go to the right people.

- Names: Rosa, Della, Hugo
- Seeds: zinnia, sweet pea, marigold
- Cast: Rosa; story: Wren

**3. The Lunch Pail Mix-Up** — first3, n=3, k=2, *

Three workers at Okafor Boatyard set their lunch pails on the same sawhorse, and now nobody is sure whose lunch is whose. Felix would like to eat his own sandwich, thank you.

- Names: Felix, Tova, Ivan
- Lunch: chowder, egg salad, meatloaf
- Cast: Felix

**4. The Rummage Sale Hats** — first3, n=3, k=2, *

Three hats arrived at Hattie's spring rummage sale with no donor slips. She keeps a careful list for her thank-you cards, so who gave which hat?

- Names: Otis, Linus, Pearl
- Hat: sou'wester, straw hat, beret
- Cast: Otis; story: Hattie

**5. The New Paper Route** — first3, n=3, k=2, *

On Teddy's first morning delivering the Gazette, three customers asked for a little extra with their paper. Teddy did not write anything down. He was sure he would remember. He did not. Help him get each extra to the right porch tomorrow.

- Names: Nico, Amara, Sam
- Extra: tide table, puzzle book, coupons
- Cast: Nico; story: Teddy

**6. The Muddled Umbrellas** — first4, n=4, k=2, *

A rainy April morning at the Gull's Rest Inn: four people who stopped in for breakfast left umbrellas in the stand by the door, and Priya wants each one back with its owner before the noon ferry.

- Names: Mabel, Gus, Kit, Oscar
- Umbrella: plaid, yellow, polka-dot, navy
- Cast: Mabel, Gus; story: Priya

**7. Opening Day at the Light** — first4, n=4, k=2, *

Thimble Point Light opens for the season, and Lena announces that the 1876 Keeper's Lamp, a ceremonial light since the lighthouse retired from guiding ships, will shine every evening of Lantern Festival week and get a 150th-birthday lighting on Festival night. Four volunteers each took one opening-day job. Who did what?

- Names: Jonah, Imani, Boris, Faye
- Job: ticket desk, gift shop, tours, cocoa stand
- Cast: Jonah; story: Lena

**8. The Sourdough Adoption** — first4, n=4, k=2, *

Rosa held a bread class and sent four students home with a jar of her sourdough starter, each with its own name. She has forgotten which starter went home with whom, and she worries about them.

- Names: Wren, Dev, Quinn, Enzo
- Starter: Bubbles, Gloria, Admiral, Pip
- Cast: Wren; story: Rosa

**9. The Tulip Planting Gloves** — first4, n=4, k=2, *

After the garden club planted tulips on the town green, four pairs of gloves were left on the bench. Mabel wants to return them with a polite note about putting things away.

- Names: Priya, Zeke, Olive, Cass
- Gloves: green, floral, leather, striped
- Cast: Priya; story: Mabel

**10. The Unsigned Letters** — first4, n=4, k=2, *

Four letters to the editor arrived at the Gazette without signatures, each on a different topic. The Gazette never prints an unsigned letter, so Ada needs to know who wrote which.

- Names: Gus, Tariq, Hal, Vera
- Topic: potholes, parking, seagulls, bake sale
- Cast: Gus


### Chapter 2: The Full Grid (May-June)

**11. The Regatta Pennants** — grid3, n=3, k=3, *

Three sailors at the Spring Regatta flew different pennants on different boats, and Otis's start sheet got smudged. He needs the sheet right before the starting horn.

- Names: Felix, Selma, Arlo
- Pennant: red, blue, gold
- Boat: sloop, catboat, dory
- Cast: Felix; story: Otis

**12. The Swapped Jam Labels** — grid3, n=3, k=3, *

Three neighbors brought jam to the church supper. For blind judging, Hattie peeled off every label and, for once in her life, made no list. The judges need to know whose is whose before the ribbons go out.

- Names: Hattie, Ruben, Lou
- Jam: plum, fig, quince
- Jar: mason jar, crock, tin
- Cast: Hattie

**13. The Book Drop Surprise** — grid3, n=3, k=3, *

Three overdue books came back through the library's book drop overnight, each with a stray bookmark tucked inside. Wren wants to clear the right accounts, and return the bookmarks.

- Names: Nico, Della, Kenji
- Book: atlas, cookbook, mystery
- Bookmark: ribbon, postcard, receipt
- Cast: Nico; story: Wren

**14. The Mother's Day Corsages** — grid3, n=3, k=3, *

The garden club made corsages for Mother's Day, and three customers' orders got shuffled on the counter. Mabel insists every corsage go to the person who ordered it.

- Names: Jonah, Bea, Cyrus
- Flower: carnation, rose, peony
- Ribbon: lavender, white, peach
- Cast: Jonah; story: Mabel

**15. Kite Day Tangle** — grid3, n=3, k=3, *

On a breezy May Saturday, three kites tangled into one knot over the town green. Untangle the knot on paper first: who flew which kite, with which tail?

- Names: Teddy, Una, Hugo
- Kite: dragon, box kite, diamond
- Tail: bows, streamers, tassels
- Cast: Teddy

**16. The Boatyard Paint Cans** — grid3, n=3, k=3, *

Three boat owners came to Felix's yard to repaint their hulls, and the paint cans lost their tags. Before anyone opens a can, Felix wants to know which color goes on which boat.

- Names: Gus, Imani, Basil
- Color: sea green, navy, cream
- Boat: Sea Pea, Lucky Gull, Wavelet
- Cast: Gus; story: Felix

**17. The Rhubarb Social** — grid3, n=3, k=3, *

At Hattie's May rhubarb social, three bakers brought desserts with different toppings. Hattie lettered the place cards a week ahead, and the bakers set their desserts down wherever they found room. Match each baker to a dessert and a topping.

- Names: Rosa, Walt, Elsa
- Dessert: shortcake, rhubarb pie, tart
- Topping: cream, ice cream, honey
- Cast: Rosa; story: Hattie

**18. The Buoys After the Storm** — grid3, n=3, k=3, *

A spring storm scattered lobster buoys across the harbor. Three lobstermen each lost a buoy in a different spot, and Otis needs to log who fishes where.

- Names: Oscar, Nico, Pablo
- Buoy: orange, striped, checkered
- Spot: Gull Rock, East Cove, the Narrows
- Cast: Nico; story: Otis

**19. The Memorial Day Floats** — grid4, n=4, k=3, **

Four floats rolled down Main Street in the Memorial Day parade, each with its own music. The Gazette caption needs to say who built which float.

- Names: Lena, Gus, Zeke, Marta
- Float: tall ship, lobster, lighthouse, whale
- Music: fiddle, kazoo, drum, banjo
- Cast: Lena, Gus

**20. The Swapped Room Keys** — grid4, n=4, k=3, **

Four guests checked in at the Gull's Rest Inn on the same Friday evening, and the room keys got swapped at the front desk. Priya needs to know who is in which room, and where each guest came from.

- Names: Vito, Amara, Kit, Hal
- Room: Gull, Tern, Puffin, Heron
- Hometown: Boston, Albany, Hartford, Portland
- Cast: none in grid; story: Priya

**21. The Spring Bird Count** — grid4, n=4, k=3, **

For the spring bird count, four birders each spotted one special bird at a different spot. The garden club must send a tidy report to the state by Friday.

- Names: Mabel, Dev, Tova, Ivan
- Bird: osprey, heron, puffin, loon
- Spot: salt marsh, old pier, dunes, orchard
- Cast: Mabel

**22. The Lighthouse Paint Crew** — grid4, n=4, k=3, **

Four volunteers spent Saturday painting Thimble Point Light for its 150th year, each on one part with one kind of tool. Lena wants the work log done right, since the light is getting ready for its big night.

- Names: Teddy, Jonah, Faye, Ruben
- Part: door, railing, stairs, shutters
- Tool: roller, wide brush, sponge, small brush
- Cast: Teddy, Jonah; story: Lena

**23. The Ferry Lost-and-Found** — grid4, n=4, k=3, **

Four commuters left something behind on the morning ferry, each on a different deck. Jonah keeps a proper lost-and-found and wants every item tagged.

- Names: Otis, Carmen, Yusuf, Linus
- Item: scarf, thermos, novel, sun hat
- Deck: bow, stern, upper deck, cabin
- Cast: Otis; story: Jonah

**24. The Garden Tour Signs** — grid4, n=4, k=3, **

A gust blew down the signs on the garden club's June tour. Four gardens, four flowers, four ornaments, and a tour bus arriving at ten. Help Mabel put the signs back.

- Names: Hattie, Gideon, Pearl, Enzo
- Flower: roses, irises, lupines, peonies
- Ornament: birdbath, sundial, gnome, trellis
- Cast: Hattie; story: Mabel

**25. Supper at the Clam Shack** — grid4, n=4, k=3, **

Four friends ordered supper at the harbor clam shack while Nico told the one about the lobster the size of a canoe, so nobody, the cook included, was listening when the orders went in. The cook is waiting: who ordered which dish and which drink?

- Names: Nico, Felix, Bea, Sam
- Dish: lobster roll, fried clams, fish tacos, crab cake
- Drink: lemonade, iced tea, root beer, cider
- Cast: Nico, Felix

**26. The Grown-Up Spelling Bee** — grid4, n=4, k=3, **

Four adults reached the final round of the library's spelling bee. Each spelled one tricky word and clutched a different lucky charm. Mabel, the judge, has lost her score sheet.

- Names: Wren, Oscar, Imani, Cyrus
- Word: rhythm, kayak, pharaoh, zucchini
- Charm: lucky penny, acorn, sea glass, wishbone
- Cast: Wren; story: Mabel

**27. The Graduation Cakes** — grid4, n=4, k=3, **

Rosa baked four graduation cakes, each a different flavor with a different topper. She took the orders while feeding Gloria, her sourdough starter, and wrote down the cakes but not the families. Which cake goes to which family?

- Names: Tariq, Gus, Jade, Elsa
- Flavor: lemon, carrot, chocolate, coconut
- Topper: mortarboard, diploma, owl, star
- Cast: Gus; story: Rosa

**28. The Tide Pool Walk** — grid4, n=4, k=3, **

On Lena's tide pool walk, four walkers each found one creature in a different named pool. Everything goes back where it came from before the tide turns, so who found what, and where?

- Names: Lena, Marta, Hugo, Zeke
- Creature: sea star, crab, snail, urchin
- Pool: Bathtub Pool, Kettle Pool, Mermaid Pool, Moon Pool
- Cast: Lena

**29. The Water Day Photos** — grid4, n=4, k=3, **

Teddy took four great photos at the June Water Day on Thimble Beach and, as usual, wrote down not a single name. Each shows one person in one race with one prize, and the Gazette goes to press at five.

- Names: Priya, Vera, Kenji, Della
- Race: kayak, swim, rowing, sailboard
- Prize: trophy, ribbon, medal, pie
- Cast: Priya; story: Teddy

**30. The Borrowed Oars** — grid4, n=4, k=3, **

Before the June dinghy race, four pairs of oars were borrowed from Felix's rack and hung back on the wrong hooks. Felix wants each pair matched to its dinghy. (He also notices his own small dinghy is back a little farther up the beach than he left it.)

- Names: Felix, Otis, Walt, Amara
- Oars: varnished, blue-tipped, spruce, ash
- Dinghy: Minnow, Pebble, Skipjack, Teacup
- Cast: Felix, Otis


### Chapter 3: First, Next, Last (July-early August)

**31. The Creamery Line** — lineup, n=4, k=2, line-up, 1 ordered, **

On the first hot afternoon of July, four people lined up at the harbor creamery and one of them dropped a five-dollar bill. To return it, Ada wants the order of the line.

- Names: Rosa, Ivan, Faye, Kit
- Place **(ordered, step 1 place; 1st = front of the line)**: 1st, 2nd, 3rd, 4th
- Cast: Rosa

**32. The Fourth of July Parade** — lineup, n=4, k=2, line-up, 1 ordered, **

Four floats rolled down Main Street on the Fourth, and the Gazette's parade program printed them in the wrong order. Fix the program for the paper's correction box.

- Names: Hattie, Nico, Selma, Arlo
- Place **(ordered, step 1 place; 1st = front of the line)**: 1st, 2nd, 3rd, 4th
- Cast: Hattie, Nico

**33. The Ferry Boarding Line** — lineup, n=4, k=2, line-up, 1 ordered, **

Four passengers boarded the 8 a.m. ferry one at a time, and one boarding pass was punched twice. Jonah wants to know who boarded in which order.

- Names: Otis, Lou, Yusuf, Greta
- Place **(ordered, step 1 place; 1st = front of the line)**: 1st, 2nd, 3rd, 4th
- Cast: Otis; story: Jonah

**34. The Sandcastle Row** — lineup, n=4, k=2, line-up, 1 ordered, **

Four sandcastles stood in a row along Thimble Beach, counting out from the pier. The judges' sheet lists castles by position only, so who built which one?

- Names: Teddy, Mabel, Enzo, Carmen
- Place **(ordered, step 1 place; 1st = front of the line)**: 1st, 2nd, 3rd, 4th
- Cast: Teddy, Mabel

**35. The Clambake Buffet** — lineup, n=5, k=2, line-up, 1 ordered, **

Five hungry people lined up at the July clambake, and the last ear of corn went to the person at the back. Who stood where in the buffet line?

- Names: Priya, Felix, Dot, Hugo, Vera
- Place **(ordered, step 1 place; 1st = front of the line)**: 1st, 2nd, 3rd, 4th, 5th
- Cast: Priya, Felix

**36. The Fireworks Blankets** — lineup, n=5, k=2, line-up, 1 ordered, **

Five friends spread blankets in a single row on the town green to watch the fireworks. The Gazette's panorama photo needs names, left to right.

- Names: Lena, Gus, Tova, Amara, Pablo
- Spot **(ordered, step 1 blanket; 1st = far left)**: 1st, 2nd, 3rd, 4th, 5th
- Cast: Lena, Gus

**37. The Book Sale Early Birds** — lineup, n=5, k=2, line-up, 1 ordered, **

Five early birds lined up outside the library before the summer book sale opened. Wren promised the first in line the pick of the rare books, but who was first?

- Names: Oscar, Nadia, Jonah, Elsa, Milo
- Place **(ordered, step 1 place; 1st = front of the line)**: 1st, 2nd, 3rd, 4th, 5th
- Cast: Jonah; story: Wren

**38. The Committee Photo** — lineup, n=5, k=2, line-up, 1 ordered, **

Teddy photographed the Lighthouse Anniversary Committee standing in one row in front of the light, and the Gazette needs the caption left to right. Ada notes that one member kept glancing up at the lantern room.

- Names: Otis, Hattie, Jonah, Lena, Gus
- Spot **(ordered, step 1 place; 1st = far left)**: 1st, 2nd, 3rd, 4th, 5th
- Cast: Otis, Hattie, Jonah, Lena, Gus; story: Teddy

**39. The Lobster Boat Tours** — days4, n=4, k=3, 1 ordered, ***

Nico takes one visitor out on Persistence each weekday morning. He keeps the bookings in his head, right next to the lobster stories, and the two have begun to mix. Each visitor came from a different town. Who went out on which day?

- Names: Cass, Hal, Imani, Boris
- Hometown: Buffalo, Tulsa, Dover, Reno
- Day **(ordered, step 1 day)**: Monday, Tuesday, Wednesday, Thursday
- Cast: none in grid; story: Nico

**40. The Ferry Freight Week** — days4, n=4, k=3, 1 ordered, ***

Jonah's ferry carried one odd shipment to Gull Island each day this week. Four senders, four parcels, four days, and one very confused island postmaster.

- Names: Gus, Faye, Tariq, Una
- Cargo: piano, beehive, canoe, armchair
- Day **(ordered, step 1 day)**: Tuesday, Wednesday, Thursday, Friday
- Cast: Gus; story: Jonah

**41. The Blueberry Patches** — days4, n=4, k=3, 1 ordered, ***

Four pickers each worked a different blueberry patch on a different day before the August festival. Mabel is making a picking map for next year.

- Names: Mabel, Ruben, Jade, Vito
- Patch: north field, hilltop, stone wall, creekside
- Day **(ordered, step 1 day)**: Wednesday, Thursday, Friday, Saturday
- Cast: Mabel

**42. The Story Hour Volunteers** — days4, n=4, k=3, 1 ordered, ***

Four volunteers each read at the library's summer story hour, held once a week through July, each on a different week with a different kind of book. The library newsletter goes to print tomorrow.

- Names: Wren, Kenji, Sam, Olive
- Book: pirate tale, fairy tale, poems, fables
- Week **(ordered, step 1 week)**: July 8, July 15, July 22, July 29
- Cast: Wren

**43. The Museum Lock-Up Log** — days4, n=4, k=3, 1 ordered, ***

Four volunteers each locked up the lighthouse museum on a different night and wrote one note in the log. Lena wants to know who wrote which note, especially the one about an odd flicker high in the lantern room.

- Names: Teddy, Della, Priya, Arlo
- Note: stuck latch, gull nest, wet paint, odd flicker
- Day **(ordered, step 1 day)**: Thursday, Friday, Saturday, Sunday
- Cast: Teddy, Priya; story: Lena

**44. The Saturday Sailing Lessons** — days4, n=4, k=3, 1 ordered, ***

Felix gave four sailing lessons on Saturday morning, one an hour, each in a different boat. He kept the lesson sheet in his head, which he calls shipshape. It is mostly shipshape. Who sailed when, and in what?

- Names: Walt, Carmen, Emil, Pearl
- Boat: Whelk, Tern, Bluebell, Ripple
- Time **(ordered, step 1 hour)**: 9 a.m., 10 a.m., 11 a.m., noon
- Cast: none in grid; story: Felix

**45. The Bakery Pickup Times** — days4, n=4, k=3, 1 ordered, ***

Four special orders sat waiting at the Salt & Sugar Bakery, each picked up at a different hour. Rosa wants her order book straight before the next rush.

- Names: Nico, Zeke, Lou, Milo
- Order: layer cake, baguettes, rye loaf, cinnamon bun
- Pickup **(ordered, step 1 hour)**: 7 a.m., 8 a.m., 9 a.m., 10 a.m.
- Cast: Nico; story: Rosa

**46. The Fair Entry Deadline** — days4, n=4, k=3, 1 ordered, ***

On the last afternoon before the county fair, four exhibitors dropped off entries at the fair office, an hour apart. The clerk needs the entry sheet in order.

- Names: Hugo, Selma, Dev, Otis
- Entry: pickles, quilt, honey, zucchini
- Time **(ordered, step 1 hour)**: 1 p.m., 2 p.m., 3 p.m., 4 p.m.
- Cast: Otis


### Chapter 4: Truth or Fib? (August)

**47. Who Ate the Last Scone?** — liars, 3 suspects, ***

Ada left one cranberry scone on her desk at the Gazette and came back to crumbs. Three people were in the office, and each says one thing.

- Suspects: Teddy, Bea, Gus
- Deed: "ate the last scone" / "didn't eat the last scone"
- Cast: Teddy, Gus; story: Rosa

**48. Who Let the Goat Out?** — liars, 3 suspects, ***

At the county fair, a goat named Clementine went wandering through the pie tent. Three people were near the pen, and each says one thing.

- Suspects: Nico, Faye, Linus
- Deed: "left the goat pen open" / "didn't leave the goat pen open"
- Cast: Nico

**49. Who Tasted the Pie Early?** — liars, 3 suspects, ***

Someone cut a slice from a contest pie before the judging at the fair. Three people were near the judges' table, and the judges are not amused.

- Suspects: Hal, Mabel, Kit
- Deed: "cut the contest pie" / "didn't cut the contest pie"
- Cast: Mabel

**50. Who Sounded the Ferry Horn?** — liars, 3 suspects, ***

At midnight, the ferry horn woke half the harbor. Jonah was home asleep, and three people had a key to the wheelhouse. Pilot the beagle is not a suspect.

- Suspects: Otis, Jade, Vito
- Deed: "sounded the ferry horn" / "didn't sound the ferry horn"
- Cast: Otis; story: Jonah

**51. Who Swapped the Quilt Ribbons?** — liars, 4 suspects, ***

At the fair's quilt show, the blue ribbon and the red ribbon traded places overnight. Four people had been in the hall after closing.

- Suspects: Hattie, Wren, Cyrus, Elsa
- Deed: "swapped the quilt ribbons" / "didn't swap the quilt ribbons"
- Cast: Hattie, Wren

**52. Who Hid the Gavel?** — liars, 4 suspects, ***

The town meeting couldn't start because the moderator's gavel was missing. Four people were in the hall early, and each says one thing.

- Suspects: Priya, Gideon, Una, Ruben
- Deed: "hid the gavel" / "didn't hide the gavel"
- Cast: Priya

**53. Who Took the Postcards?** — liars, 4 suspects, ***

The whole stack of 150th-anniversary postcards vanished from the lighthouse gift shop. Lena counts four visitors that afternoon, and each says one thing.

- Suspects: Felix, Teddy, Marta, Sam
- Deed: "took the postcards" / "didn't take the postcards"
- Cast: Felix, Teddy; story: Lena

**54. Who Borrowed the Berry Rake?** — liars, 4 suspects, ***

Mabel's blueberry rake disappeared from her porch the morning of the Blueberry Festival. Four neighbors walked by, and each says one thing.

- Suspects: Dot, Rosa, Enzo, Quinn
- Deed: "borrowed the berry rake" / "didn't borrow the berry rake"
- Cast: Rosa; story: Mabel

**55. Who Unplugged the Ferris Wheel?** — liars, 4 suspects, ***

The Ferris wheel lights went dark on the last night of the fair, with Gus stuck at the top. Four people were near the power box.

- Suspects: Nadia, Lena, Ivan, Oscar
- Deed: "unplugged the lights" / "didn't unplug the lights"
- Cast: Lena; story: Gus

**56. Who Salted the Lemonade?** — liars, 5 suspects, ***

At the church hall's August ice cream social, the big pitcher of lemonade came out salty: someone had filled it from the salt tin instead of the sugar tin, which sit side by side. Five people had worked in the hall kitchen that afternoon, and each says one thing.

- Suspects: Arlo, Hattie, Della, Pablo, Yusuf
- Deed: "salted the lemonade" / "didn't salt the lemonade"
- Cast: Hattie

**57. Who Fed the Gulls?** — liars, 5 suspects, ***

At the chowder cook-off on the town pier, someone tossed a bag of popcorn off the end, and two hundred gulls came down on the tasting tables. Five people were out at the end of the pier, and each says one thing.

- Suspects: Carmen, Otis, Imani, Basil, Zeke
- Deed: "fed the gulls" / "didn't feed the gulls"
- Cast: Otis

**58. Who Gave the Trophy a Mustache?** — liars, 5 suspects, ***

An hour before the Harbor Days awards, the sandcastle trophy was found on the prize table wearing a curly mustache in grease pencil. Five people had been near the table, and each says one thing.

- Suspects: Vera, Gideon, Felix, Priya, Lou
- Deed: "drew the mustache on the trophy" / "didn't draw the mustache on the trophy"
- Cast: Felix, Priya


### Chapter 5: Two Clues at Once (September-October)

**59. The Orchard Baskets** — num43, n=4, k=3, 1 ordered, ***

Four friends went apple picking at Hilltop Orchard, each picking a different apple and a different amount. The farm stand charges by the pound, and the scale's tape has jammed.

- Names: Pablo, Mabel, Kit, Sam
- Apple: Cortland, Macoun, Baldwin, Empire
- Weight **(ordered, step 5 pounds)**: 10 lb, 15 lb, 20 lb, 25 lb
- Cast: Mabel

**60. The Elm Street Yard Sale** — num43, n=4, k=3, 1 ordered, ***

Four sellers at the Labor Day yard sale each sold one treasure at a different price, and the cash box notes are a mess. Who sold what, and for how much?

- Names: Linus, Vera, Gus, Dot
- Item: lamp, teapot, birdcage, records
- Price **(ordered, step 2 dollars)**: $2, $4, $6, $8
- Cast: Gus

**61. The Evening Class Roll** — num43, n=4, k=3, 1 ordered, ***

Four students signed up for adult evening classes at the school, each in a different subject, and each a different age. Mabel, who now teaches the grammar class, needs the roll right.

- Names: Felix, Jade, Hugo, Una
- Class: watercolor, Spanish, pottery, guitar
- Age **(ordered, step 5 years)**: 40, 45, 50, 55
- Cast: Felix; story: Mabel

**62. The Fishing Derby** — num43, n=4, k=3, 1 ordered, ***

Four anglers entered the harbor fishing derby, each landing a different fish of a different length. Otis has the trophy ready but not the results.

- Names: Elsa, Nico, Oscar, Cyrus
- Fish: scup, bluefish, mackerel, flounder
- Length **(ordered, step 2 inches)**: 12 in., 14 in., 16 in., 18 in.
- Cast: Nico; story: Otis

**63. The Ferry Schedule Shuffle** — num43, n=4, k=3, 1 ordered, ***

Four passengers each took a different morning ferry to a different stop. Two of them say they saw a light blink out at Thimble Point on the way, and Jonah needs to know who rode when.

- Names: Ruben, Priya, Amara, Tova
- Stop: Gull Island, Cobb Point, Pine Key, the mainland
- Ferry **(ordered, step 30 minutes)**: 7:00 a.m., 7:30 a.m., 8:00 a.m., 8:30 a.m.
- Cast: Priya; story: Jonah

**64. The Library Fines** — num43, n=4, k=3, 1 ordered, ***

Four patrons paid overdue fines on the same afternoon, each for a different kind of book. Wren whispered each amount as she took it, and not even Wren heard herself. She also mentions, in a whisper, that the 1876 keeper's logbook is checked out to an 'S. Bell', and Silas Bell, the last keeper, has been gone for eighty years. (Never connect the name to Jonah.)

- Names: Teddy, Basil, Marta, Ivan
- Book: biography, atlas, poetry, thriller
- Fine **(ordered, step 25 cents)**: 25 cents, 50 cents, 75 cents, $1.00
- Cast: Teddy; story: Wren

**65. The Pumpkin Weigh-Off** — num44, n=4, k=4, 1 ordered, ****

Four growers brought giant pumpkins to the October weigh-off, each fed a secret fertilizer and given a pet name. The scale printout came out blank.

- Names: Zeke, Gus, Kenji, Mabel
- Pumpkin: Big Mo, Sunny, Tubby, Duchess
- Fertilizer: seaweed, compost, fish meal, coffee
- Weight **(ordered, step 100 pounds)**: 300 lb, 400 lb, 500 lb, 600 lb
- Cast: Gus, Mabel

**66. The Harvest Supper Arrivals** — num44, n=4, k=4, 1 ordered, ****

Four cooks arrived at the harvest supper fifteen minutes apart, each with a different dish carried a different way. Hattie needs the table plan before the doors open.

- Names: Rosa, Lou, Selma, Dev
- Dish: squash soup, cornbread, baked beans, apple crisp
- Carrier: basket, wagon, tote bag, box
- Arrival **(ordered, step 15 minutes)**: 5:00 p.m., 5:15 p.m., 5:30 p.m., 5:45 p.m.
- Cast: Rosa; story: Hattie

**67. The Corn Maze Times** — num44, n=4, k=4, 1 ordered, ****

Four friends raced through the corn maze, each going in a different entrance and stopping for a different snack. The farmer posts the times on a chalkboard, but the rain washed it off.

- Names: Jonah, Faye, Quinn, Hal
- Entrance: north gate, south gate, barn door, scarecrow
- Snack: cider, kettle corn, apple, donut
- Time **(ordered, step 5 minutes)**: 20 min., 25 min., 30 min., 35 min.
- Cast: Jonah

**68. The Clock Auction** — num44, n=4, k=4, 1 ordered, ****

Four antique clocks sold at the church hall auction, each made in a different year of a different wood. Hattie's receipts got stuck together.

- Names: Otis, Della, Carmen, Pablo
- Clock: mantel, cuckoo, banjo, ship's clock
- Wood: oak, walnut, cherry, maple
- Year **(ordered, step 10 years)**: 1880, 1890, 1900, 1910
- Cast: Otis; story: Hattie

**69. The Lobster Trap Tally** — num44, n=4, k=4, 1 ordered, ****

Four lobstermen hauled a different number of traps on Tuesday, each with a different bait and buoy color. Nico tells it differently each time, so you will need the clues.

- Names: Arlo, Yusuf, Greta, Nico
- Bait: herring, pogies, redfish, squid
- Buoy: orange, white, purple, lime
- Traps **(ordered, step 10 traps)**: 20, 30, 40, 50
- Cast: Nico

**70. The Apple Pie Bake-Off** — num44, n=4, k=4, 1 ordered, ****

Four bakers each baked an apple pie with a different crust and a different spice, for a different number of minutes. Rosa, the judge, wants to know the secrets.

- Names: Priya, Vito, Imani, Boris
- Crust: lattice, crumble, plain, braided
- Spice: cinnamon, nutmeg, ginger, cardamom
- Bake **(ordered, step 5 minutes)**: 40 min., 45 min., 50 min., 55 min.
- Cast: Priya; story: Rosa

**71. The Hiking Club Summits** — num44, n=4, k=4, 1 ordered, ****

Four members of the hiking club each climbed a different hill on the long October weekend, each with a different trail snack. The club's logbook only has the heights.

- Names: Felix, Wren, Enzo, Cass
- Hill: Bramble Hill, Crow's Nest, Fiddler Hill, Thimble Knob (made-up local hills)
- Snack: trail mix, jerky, cheese, figs
- Height **(ordered, step 200 feet)**: 800 ft, 1,000 ft, 1,200 ft, 1,400 ft
- Cast: Felix, Wren

**72. The Gazette Ad Rates** — num44, n=4, k=4, 1 ordered, ****

Four advertisers bought autumn ads in the Gazette, each with a different border in a different section. Lena's ad announces the Keeper's Lamp's 150th-birthday lighting at the Lantern Festival, and the invoices are all wrong.

- Names: Gus, Lena, Tariq, Olive
- Border: plain, dotted, wavy, rope
- Section: sports, recipes, tides, puzzles
- Price **(ordered, step 10 dollars)**: $10, $20, $30, $40
- Cast: Gus, Lena

**73. The Lamp Fund Jar** — num44, n=4, k=4, 1 ordered, ****

Four donors put money in the Keeper's Lamp fund jar at Mahoney's, each with a different note and a different way of paying. The Gazette wants to thank each one properly.

- Names: Lena, Jonah, Tova, Gus
- Paid: check, cash, coins, money order
- Note: poem, drawing, thank-you, riddle
- Gift **(ordered, step 25 dollars)**: $25, $50, $75, $100
- Cast: Lena, Jonah, Gus

**74. The Firewood Orders** — num44, n=4, k=4, 1 ordered, ****

Four households ordered firewood for winter, each a different wood and amount, stacked in a different place. Hattie collected the orders for the whole lane on one of her lists, and that list is now somewhere on another list.

- Names: Kit, Hattie, Ruben, Amara
- Wood: oak, birch, maple, ash
- Stacked: porch, shed, barn, garage
- Cords **(ordered, step 1 cord)**: 1 cord, 2 cords, 3 cords, 4 cords
- Cast: Hattie

**75. The Harvest Shuttle Fares** — num44, n=4, k=4, 1 ordered, ****

On harvest weekend, Hilltop Orchard runs a hay-wagon shuttle from Main Street out to its fields. Four riders paid different fares to different stops, and each carried something different home. The orchard's fare can is a dollar off, and the farmer would like it to balance before the next run.

- Names: Teddy, Basil, Nadia, Zeke
- Stop: corn maze, cider stand, orchard gate, farm stand
- Carried: pumpkin, apple crate, cider jug, mums
- Fare **(ordered, step 2 dollars)**: $3, $5, $7, $9
- Cast: Teddy

**76. The Quilt Raffle** — num44, n=4, k=4, 1 ordered, ****

Four people bought raffle tickets for the church hall's quilt raffle, each a different number of tickets for a different quilt, and each with a different room in mind for it. The winner must be checked.

- Names: Emil, Wren, Jade, Pablo
- Quilt: log cabin, star, nine patch, wedding ring
- Wants it for: bedroom, den, porch, guest room
- Tickets **(ordered, step 2 tickets)**: 2, 4, 6, 8
- Cast: Wren; story: Hattie

**77. The Cider Press Batches** — num44, n=4, k=4, 1 ordered, ****

Four neighbors pressed cider at the boatyard's old press, each with a different apple mix and a different hand-drawn label, and a different number of gallons. Felix lent the press and wants a fair share of cider.

- Names: Marta, Priya, Cyrus, Felix
- Mix: tart, sweet, spicy, wild
- Label: owl, anchor, moon, star
- Gallons **(ordered, step 5 gallons)**: 5 gal., 10 gal., 15 gal., 20 gal.
- Cast: Priya, Felix

**78. The Costume Parade** — num44, n=4, k=4, 1 ordered, ****

Four grown-ups marched in the Halloween costume parade that closes out October, each in a different costume, handing out a different candy. Each started with a different-sized bag and gave every last piece away. The Gazette prints numbers, not guesses, says Ada.

- Names: Mabel, Otis, Hugo, Dot
- Costume: pirate, mermaid, scarecrow, robot
- Candy: taffy, caramels, licorice, gumdrops
- Handed out **(ordered, step 25 pieces)**: 50 pieces, 75 pieces, 100 pieces, 125 pieces
- Cast: Mabel, Otis
- (Not an Age grid: Mabel's only Age grid is #95, Otis's is #93.)


### Chapter 6: Case Files (November)

**79. The Case of the Pie Server** — case54, n=5, k=4, 1 ordered, ****

At the church hall's early-November pie auction, where the town orders its Thanksgiving pies, Hattie's grandmother's silver pie server went missing between bids. Five helpers were each in a different spot with a different pie. *Evidence:* the server turned up that night in a coat hanging in the cloakroom, and only the helper posted in the cloakroom handled the coats. Who slipped it into a coat pocket?

- Names: Rosa, Gus, Della, Vito, Imani
- Pie: pecan, pumpkin, apple, mince, cherry
- Spot: kitchen, stage, cloakroom, porch, bake table
- Time **(ordered, step 15 minutes)**: 6:00 p.m., 6:15 p.m., 6:30 p.m., 6:45 p.m., 7:00 p.m.
- Question: "Who slipped the pie server into a coat pocket?" Culprit: whoever has Spot = cloakroom; answer: engine decides
- Cast: Rosa, Gus; story: Hattie

**80. The Case of the Loose Mooring** — case54, n=5, k=4, 1 ordered, ****

On a frosty November morning, the week before haul-out, someone untied Felix's sailboat Ripple from its mooring, and it drifted onto Gull Rock. Five people were on the dock that morning, each in a different coat on a different errand. *Evidence:* a dog walker on the seawall saw someone in a yellow slicker bent over the Ripple's mooring line.

- Names: Walt, Quinn, Bea, Nico, Hal
- Coat: slicker, peacoat, parka, barn coat, fleece
- Errand: bait, mail, coffee, ice, diesel
- Time **(ordered, step 30 minutes)**: 6:00 a.m., 6:30 a.m., 7:00 a.m., 7:30 a.m., 8:00 a.m.
- Question: "Who untied the Ripple?" Culprit: whoever has Coat = slicker; answer: engine decides
- Cast: Nico; story: Felix

**81. The Case of the Recipe Card** — case54, n=5, k=4, 1 ordered, ****

Rosa's great-grandmother's cranberry bread recipe card vanished from the bakery corkboard. Five customers came in that morning, each ordering something different and sitting somewhere different. *Evidence:* the corkboard hangs right beside the window table, out of reach of every other seat.

- Names: Selma, Priya, Kenji, Lou, Mabel
- Order: muffin, scone, bagel, croissant, danish
- Seat: window, counter, corner, patio, booth
- Time **(ordered, step 30 minutes)**: 7:00 a.m., 7:30 a.m., 8:00 a.m., 8:30 a.m., 9:00 a.m.
- Question: "Who pocketed the recipe card?" Culprit: whoever has Seat = window; answer: engine decides
- Cast: Priya, Mabel; story: Rosa

**82. The Case of the Copper Whale** — case54, n=5, k=4, 1 ordered, ****

The copper whale weathervane disappeared from the boatyard roof overnight. Five people were in the yard the evening before, each with a different tool and a different excuse. *Evidence:* the roof is too high to reach without a ladder, and there are fresh ladder marks in the frost under the eaves.

- Names: Jade, Arlo, Boris, Cass, Milo
- Tool: ladder, rope, wrench, lantern, crowbar
- Excuse: fishing, jogging, sketching, lost dog, stargazing
- Age **(ordered, step 10 years)**: 20, 30, 40, 50, 60
- Question: "Who took down the copper whale?" Culprit: whoever has Tool = ladder; answer: engine decides
- Cast: none in grid; story: Felix
- (Teddy is kept out of this grid: he is 19, and the engine assigns ages at random.)

**83. The Case of the Crossword** — case54, n=5, k=4, 1 ordered, ****

Someone changed three answers in Ada's crossword the night before press day, and the Gazette nearly printed 'GULL' as a kind of cheese. Five visitors used the puzzle desk that evening. *Evidence:* all three changes are in green ink.

- Names: Otis, Faye, Emil, Tariq, Wren
- Pen: green, red, blue, black, purple
- Snack: pretzels, fudge, grapes, popcorn, almonds
- Time **(ordered, step 30 minutes)**: 5:00 p.m., 5:30 p.m., 6:00 p.m., 6:30 p.m., 7:00 p.m.
- Question: "Who scrambled the crossword?" Culprit: whoever has Pen = green; answer: engine decides
- Cast: Otis, Wren

**84. The Case of the Wandering Key** — case54, n=5, k=4, 1 ordered, ****

The spare lighthouse key was missing from its hook in the harbor office for one whole day, then quietly came back. Otis wants to know who borrowed it. Five people visited the office that day. *Evidence:* the hook is on the key wall, and only someone standing at that wall could have lifted the key unseen.

- Names: Lena, Gus, Nadia, Teddy, Sam
- Visit: tide chart, mooring fee, lost cap, radio, permit
- Spot: key wall, desk, window, map table, stove
- Time **(ordered, step 1 hour)**: 9:00 a.m., 10:00 a.m., 11:00 a.m., noon, 1:00 p.m.
- Question: "Who borrowed the spare key?" Culprit: whoever has Spot = key wall; answer: **forced: Teddy**
- Cast: Lena, Gus, Teddy; story: Otis

**85. The Case of the Silent Bell** — case54, n=5, k=4, 1 ordered, ****

On the Sunday before Thanksgiving, the church bell would not ring: someone had wrapped the clapper in a wool scarf. Five people were in the bell tower that week. *Evidence:* the scarf on the clapper is cable-knit.

- Names: Tova, Linus, Hattie, Gideon, Pablo
- Scarf: striped, plaid, argyle, red, cable
- Reason: dusting, repairs, bats, the view, pigeons
- Day **(ordered, step 1 day)**: Monday, Tuesday, Wednesday, Thursday, Friday
- Question: "Who muffled the bell?" Culprit: whoever has Scarf = cable; answer: engine decides
- Cast: Hattie

**86. The Case of the Muddy Bootprints** — case54, n=5, k=4, 1 ordered, ****

Someone tracked mud across the library's freshly waxed floor and left a soggy book about whales on the returns cart. Wren was at lunch. Five patrons came by that afternoon. *Evidence:* the prints have the deep ridged tread of rubber boots.

- Names: Pearl, Nico, Milo, Greta, Oscar
- Boots: rubber, hiking, cowboy, snow, work
- Section: maps, history, cooking, travel, poetry
- Time **(ordered, step 30 minutes)**: 1:00 p.m., 1:30 p.m., 2:00 p.m., 2:30 p.m., 3:00 p.m.
- Question: "Who tracked in the mud?" Culprit: whoever has Boots = rubber; answer: engine decides
- Cast: Nico; story: Wren

**87. The Case of the Vanishing Cameo** — suppose, n=5, k=4, 1 ordered, *****

Priya's heirloom cameo brooch went missing from the inn's front parlor on Thanksgiving afternoon. Five guests sat in the parlor, each with a different drink and a different book from the parlor shelf. *Evidence:* the cameo's empty velvet pouch turned up tucked inside the parlor's almanac.

- Names: Mabel, Zeke, Carmen, Ivan, Basil
- Drink: cocoa, cider, tea, coffee, eggnog
- Book: almanac, sea stories, poems, cookbook, mystery
- Time **(ordered, step 20 minutes)**: 2:00 p.m., 2:20 p.m., 2:40 p.m., 3:00 p.m., 3:20 p.m.
- Question: "Who tucked the cameo away?" Culprit: whoever has Book = almanac; answer: engine decides
- Cast: Mabel; story: Priya

**88. The Case of the Fast Clock** — suppose, n=5, k=4, 1 ordered, *****

The clock above the ferry dock was set ten minutes fast, and Jonah's ferry left early, stranding the town moderator. Five people had been on the dock the evening before. *Evidence:* the clock hangs too high to reach without something to stand on.

- Names: Amara, Rosa, Kit, Vito, Otis
- Carried: toolbox, umbrella, basket, lantern, step stool
- Hat: beret, cap, beanie, fedora, bonnet
- Time **(ordered, step 30 minutes)**: 6:00 p.m., 6:30 p.m., 7:00 p.m., 7:30 p.m., 8:00 p.m.
- Question: "Who set the dock clock fast?" Culprit: whoever has Carried = step stool; answer: engine decides
- Cast: Rosa, Otis; story: Jonah

**89. The Case of the Short Cash Box** — suppose, n=5, k=4, 1 ordered, *****

At the holiday craft fair on the Saturday after Thanksgiving, the cash box came up exactly twenty dollars short. The fair committee suspects a mistake, not a thief. Five volunteers each worked a different table for a different length of time. *Evidence:* the cash box sat on the cocoa table all day, and only the cocoa volunteer made change from it.

- Names: Una, Ruben, Hattie, Dev, Elsa
- Table: cocoa, candles, wreaths, mittens, fudge
- Name tag: holly, star, snowman, reindeer, pinecone
- Shift **(ordered, step 1 hour)**: 1 hour, 2 hours, 3 hours, 4 hours, 5 hours
- Question: "Who made the wrong change?" Culprit: whoever has Table = cocoa; answer: engine decides
- Cast: Hattie

**90. The Case of the Painted Buoys** — suppose, n=5, k=4, 1 ordered, *****

Overnight, someone painted Nico's orange lobster buoys bright purple, and now nobody can tell whose traps are whose. Five people bought paint at Mahoney's that week. *Evidence:* the buoys are now purple, and the store sold just one can of purple that week.

- Names: Enzo, Della, Yusuf, Marta, Felix
- Paint: purple, teal, white, black, yellow
- Brush: roller, sponge, wide brush, spray can, rag
- Cost **(ordered, step 2 dollars)**: $8, $10, $12, $14, $16
- Question: "Who painted the buoys?" Culprit: whoever has Paint = purple; answer: engine decides
- Cast: Felix; story: Nico, Gus

**91. The Case of the Lantern Room** — suppose, n=5, k=4, 1 ordered, *****

The lighthouse museum closes at a quarter to six, and Lena stays on to count the gift-shop till. On Wednesday morning she found muddy footprints on the spiral stair, though it was spotless when the doors closed on Tuesday. Five people climbed the tower on Tuesday afternoon, each stopping at a different landing with a different thing in hand. *Evidence:* the mud went down after the doors closed, so it belongs to whoever climbed after a quarter to six. Who went back up after closing time?

- Names: Hugo, Jonah, Wren, Teddy, Cass
- Item: sketchbook, thermos, field guide, flashlight, notebook
- (No "camera" value: Teddy's own Item is random, so a camera could land on someone else, which would look odd next to Teddy.)
- Landing: 1st landing, 2nd landing, 3rd landing, 4th landing, top
- Time **(ordered, step 30 minutes)**: 4:00 p.m., 4:30 p.m., 5:00 p.m., 5:30 p.m., 6:00 p.m.
- Question: "Who climbed the tower after closing?" Culprit: whoever has Time = 6:00 p.m.; answer: **forced: Hugo**
- Cast: Jonah, Wren, Teddy; story: Lena
- **Hugo's innocent reason** (Ada gives it after the answer): Hugo, the museum's newest volunteer, left his reading glasses up the tower and slipped back in at six while Lena was counting the till, in his muddy boots, and was too embarrassed to say so. He never touched the lamp.
- **The polished brass stays apart from this question.** If the story mentions it at all, it is a separate, older puzzle: Lena says the Keeper's Lamp's brass has been shining "as if someone polished it" since early November, weeks before Tuesday, and none of her volunteers did it. Never tie it to the footprints, the landings or the 6:00 p.m. climber. (It was Jonah; reveal only in the epilogue.)

**92. The Case of the Jammed Press** — suppose, n=5, k=4, 1 ordered, *****

The Gazette's printing press jammed on press night, and Ada pulled a red mitten out of the rollers. Five people were in the press room, each doing a different job. *Evidence:* the red mitten itself; each of the five wore a different color.

- Names: Selma, Quinn, Milo, Imani, Greta
- Mittens: red, gray, green, white, brown
- Job: folding, inking, bundling, sweeping, proofing
- Time **(ordered, step 20 minutes)**: 8:00 p.m., 8:20 p.m., 8:40 p.m., 9:00 p.m., 9:20 p.m.
- Question: "Whose mitten jammed the press?" Culprit: whoever has Mittens = red; answer: engine decides
- Cast: none in grid

**93. The Case of the Bottled Ship** — suppose, n=5, k=4, 1 ordered, *****

The library's prized ship in a bottle, the *Constance*, was missing from its glass case on Monday morning. Five volunteers had dusted displays over the weekend. *Evidence:* in the ship's place sat a short length of rope tied in a neat bowline, borrowed from the knots display.

- Names: Faye, Otis, Cyrus, Bea, Jade
- Display: maps, anchors, shells, lanterns, knots
- Duster: feather, cloth, brush, mitt, wand
- Age **(ordered, step 10 years)**: 35, 45, 55, 65, 75
- Question: "Who moved the ship in a bottle?" Culprit: whoever has Display = knots; answer: engine decides
- Cast: Otis; story: Wren

**94. The Case of the Leaky Rowboat** — suppose, n=5, k=4, 1 ordered, *****

Someone pulled the drain plug on the boatyard's work rowboat, one of the last boats still in the water, and it sank in two feet of water at the slip. Felix is fuming, politely. Five people were at the slips that afternoon. *Evidence:* the drain plug turned up at the bottom of a bailing bucket left on the dock.

- Names: Kenji, Nico, Priya, Hal, Una
- Boat: skiff, kayak, canoe, dory, punt
- Gear: oars, net, cooler, anchor, bucket
- Time **(ordered, step 15 minutes)**: 1:00 p.m., 1:15 p.m., 1:30 p.m., 1:45 p.m., 2:00 p.m.
- Question: "Who pulled the plug?" Culprit: whoever has Gear = bucket; answer: engine decides
- Cast: Nico, Priya; story: Felix

**95. The Case of the Midnight Ovens** — suppose, n=5, k=4, 1 ordered, *****

Rosa came in at 4 a.m. to find her ovens warm and a tray of gingerbread lighthouses cooling on the rack. Five people know where she hides the spare key. *Evidence:* the gingerbread on the rack; each of the five has a different specialty. Who baked at midnight?

- Names: Emil, Ruben, Mabel, Lou, Gus
- Apron: blue, flowered, plaid, white, striped
- Treat: gingerbread, biscotti, brownies, rolls, fudge
- Age **(ordered, step 5 years)**: 60, 65, 70, 75, 80
- (Range raised so that Mabel, a retired schoolteacher, is never in her forties. This is her only Age grid, and Gus's.)
- Question: "Who baked at midnight?" Culprit: whoever has Treat = gingerbread; answer: engine decides
- Cast: Mabel, Gus; story: Rosa


### Chapter 7: The Lighthouse Affair (December 20-21)

All five finale grids are pinned to the timeline in section 7. The engine forces only each answer's culprit
value, so every time window below is chosen so that *any* time the engine gives Teddy or Jonah fits that
timeline. Do not widen or move a window without re-checking section 7.

**96. The Harbor Office Sign-Out** — suppose, n=5, k=4, 1 ordered, *****

Lantern Festival Eve, December 20. At dawn on the 21st the Keeper's Lamp is gone from Thimble Point Light, and a note on the sill reads 'It will shine again.' Start at the harbor office. Otis left for a harbormasters' meeting in Portland at ten that morning, and five people signed things out on his honor-system slate while he was gone. Back late, he wiped the slate at dawn, as he does every morning: "Fresh tide, fresh slate." Who borrowed the spare lighthouse key?

- Names: Walt, Teddy, Amara, Selma, Gus
- Item: spare key, binoculars, tide chart, megaphone, life ring
- Gloves: wool, leather, fleece, fingerless, ski
- Time **(ordered, step 30 minutes)**: 10:00 a.m., 10:30 a.m., 11:00 a.m., 11:30 a.m., noon
- Time = when each person signed out. Gloves replaces the old Reason category, which left Teddy's motive to chance (it could come out "fishing") and paired freely with Item; gloves say nothing about motive.
- Question: "Who borrowed the spare lighthouse key?" Culprit: whoever has Item = spare key; answer: **forced: Teddy**
- Cast: Teddy, Gus; story: Otis, Lena

**97. The Afternoon Boats** — suppose, n=5, k=4, 1 ordered, *****

That same cold, calm afternoon, five rowers of the Festival's lantern flotilla took the boatyard's rental rowboats out for a rehearsal, each to a different spot on the flotilla route. (Felix keeps those boats in the water this late only for the flotilla.) The high tide had the causeway under water, so the only way to the Point was by boat. Felix rowed too, so he can vouch for his own trip and nobody else's. Who rowed out to Thimble Point?

- Names: Nico, Teddy, Felix, Imani, Oscar
- Boat: Minnow, Pebble, Skipjack, Teacup, Puffin
- Went to: the Point, Gull Rock, East Cove, the Narrows, Seal Ledge
- Time **(ordered, step 30 minutes)**: 1:30 p.m., 2:00 p.m., 2:30 p.m., 3:00 p.m., 3:30 p.m.
- Time = when each person rowed out. The window starts after the 96 window ends, so Teddy always has the key before he rows.
- Question: "Who rowed out to Thimble Point?" Culprit: whoever has Went to = the Point; answer: **forced: Teddy**
- Cast: Nico, Teddy, Felix

**98. The Ferry Dock Hand-Offs** — suppose, n=5, k=4, 1 ordered, *****

Between five o'clock and twenty past six that evening, the ferry dock was busy with Festival errands, and five people each received something there: a festival lantern, a thermos, the spare key... Each was headed somewhere different afterward. Who received the spare key?

- Names: Jonah, Hattie, Pearl, Rosa, Kenji
- Received: spare key, lantern, thermos, mail sack, pie tin
- Headed to: the inn, the bakery, the store, the church, the library
- Time **(ordered, step 20 minutes)**: 5:00 p.m., 5:20 p.m., 5:40 p.m., 6:00 p.m., 6:20 p.m.
- Time = when each person received their item. The window starts after Teddy is back from rowing and ends before the 99 window starts. "Headed to" replaces the old From category, whose values (the ferry, the inn...) clashed with Teddy, a person, handing Jonah the key.
- Pilot (Jonah's beagle) and "the ferry" stay story-only: never grid values here.
- Question: "Who received the spare key at the ferry dock?" Culprit: whoever has Received = spare key; answer: **forced: Jonah**
- Cast: Jonah, Hattie, Rosa; story: Teddy

**99. The Moonlight Dinghy** — suppose, n=5, k=4, 1 ordered, *****

After dark, Felix's own dinghy was gone from its slip. The tide was high and the causeway under water, so anyone who reached Thimble Point that evening got there by boat, and the dinghy was the only boat missing. Five people admit they were down by the water, each reaching a different spot at a different time, with a different light. Who rowed out to Thimble Point?

- Names: Mabel, Jonah, Zeke, Priya, Linus
- Spot: the Point, the pier, the slipway, the beach, the seawall
- Light: flashlight, headlamp, lantern, bike light, penlight
- Time **(ordered, step 20 minutes)**: 7:00 p.m., 7:20 p.m., 7:40 p.m., 8:00 p.m., 8:20 p.m.
- Time = when each person reached their spot (write the templates that way: "reached their spot at {x}"). The window starts after the 98 window ends and ends well before 9 p.m., when Jonah must be in the lantern room.
- Every spot except the Point is on the shore and reachable on foot; only the answer rowed.
- Question: "Who rowed out to Thimble Point after dark?" Culprit: whoever has Spot = the Point; answer: **forced: Jonah**
- Cast: Mabel, Jonah, Priya; story: Felix

**100. The Rehearsal on the Green** — suppose, n=5, k=4, 1 ordered, *****

While the lamp went dark, the town was on the green rehearsing the Lantern Festival. Five volunteers took turns at the Gazette's camera, one photo each, every half hour. The 9 p.m. photo shows the light at Thimble Point going out. Who snapped it?

- Names: Lena, Gideon, Wren, Teddy, Hattie
- Job: lanterns, choir, cocoa, tickets, banners
- Coat: red, navy, green, gray, camel
- Time **(ordered, step 30 minutes)**: 7:00 p.m., 7:30 p.m., 8:00 p.m., 8:30 p.m., 9:00 p.m.
- Question: "Who snapped the 9 p.m. photo?" Culprit: whoever has Time = 9:00 p.m.; answer: **forced: Teddy**
- Cast: Lena, Wren, Teddy, Hattie


---

## 7. Finale Design: The Lighthouse Affair (96-100)

**The night.** December 20, Lantern Festival Eve. All Festival week the Keeper's Lamp has been lit each evening
as a ceremonial light (no ship depends on it; the Gull Rock beacon guides the harbor), on a timer from dusk to
10 p.m. The town is on the green rehearsing. At exactly 9 p.m. the light at Thimble Point blinks three times and
goes dark, an hour early. At dawn on the 21st, Lena finds the lantern room empty: the 1876 Keeper's Lamp is gone,
and a note on the sill says "It will shine again", signed with a tiny drawing of a bell. The Festival, with the
lamp's 150th-birthday lighting, is that night. Ada pulls her chair up to the puzzle desk: "Five puzzles, partner.
Then we put them together."

**Tide.** Low tide about 11 a.m., high tide about 5:30 p.m. The causeway to the Point is under water from about
1 p.m. until about 10 p.m., so all afternoon and evening the only way to the Point is by boat. Stories 97 and 99
both say the tide is high and the causeway is under water.

**What really happened (keep every puzzle consistent with this):**

- From 10 a.m. Otis is away at a harbormasters' meeting in Portland, back late. Between 10:00 a.m. and noon,
  Teddy borrows the spare lighthouse key from the harbor office on the honor-system slate, to photograph the
  lamp in the low winter afternoon light for his "150 Years of Light" series (#96).
- Between 1:30 and 3:30 p.m., the flotilla crew rows out for its rehearsal. Teddy rows one of the boatyard's
  rental rowboats to Thimble Point, lets himself in, photographs the lamp, locks up, and rows back by about
  4:30 (#97).
- Between 5:00 and 6:20 p.m., at the ferry dock, Teddy, on his way to help set up the rehearsal, hands the key
  to Jonah, who offers to drop it back at the harbor office on his way home. Jonah does not (#98).
- Between 7:00 and 8:20 p.m., Jonah rows Felix's dinghy to the Point (#99) and lets himself in with the key. At
  9 p.m. he blinks the lamp three times in Silas Bell's old "all's well" signal, switches it off, and carries
  the lamp down to the dinghy.
- 9:00 p.m. Teddy, on the green, takes his turn at the Gazette camera and snaps the 9 p.m. rehearsal photo, which
  shows the light going out (#100).
- Lena's own museum key never leaves her key ring; she is on the green all evening (#100).

**Only two people held the spare key that day** (Teddy, Jonah). **Only two people rowed out to the Point that day**
(Teddy in the afternoon, Jonah after dark). Puzzle writers for 96-100 must not contradict these facts: do not
put a second key or a third rower to the Point in any story. In #97 every person rowed a rental rowboat
somewhere, but only the answer went to the Point. In #99 the five were at different spots along the waterfront,
all on foot except the answer, who rowed Felix's dinghy to the Point; with the causeway under the high tide, the
Point cannot be reached any other way.

| # | Title | Question (theme `question`) | Culprit value | Intended answer (`answer`) |
|---|---|---|---|---|
| 96 | The Harbor Office Sign-Out | Who borrowed the spare lighthouse key? | Item = spare key | **Teddy** |
| 97 | The Afternoon Boats | Who rowed out to Thimble Point? | Went to = the Point | **Teddy** |
| 98 | The Ferry Dock Hand-Offs | Who received the spare key at the ferry dock? | Received = spare key | **Jonah** |
| 99 | The Moonlight Dinghy | Who rowed out to Thimble Point after dark? | Spot = the Point | **Jonah** |
| 100 | The Rehearsal on the Green | Who snapped the 9 p.m. photo? | Time = 9:00 p.m. | **Teddy** |

The key-and-boat windows run in order and never overlap: 96 sign-out 10:00 a.m.-noon; 97 row-out 1:30-3:30
p.m.; 98 hand-offs 5:00-6:20 p.m.; 99 arrivals 7:00-8:20 p.m. Puzzle 100's photos (7:00-9:00 p.m., Teddy forced
to 9:00) run on the green alongside 99, with a different cast.

Each finale puzzle ends with its own answer line ("So the spare key went home with Teddy."); Ada's comment after
each should be noncommittal: Teddy looks worse and worse through 96-97, and Jonah enters the picture at 98-99.
In those comments and stories Jonah is only "Jonah": no surname, no family line, no ferry name.

### Bonus page: "Putting It All Together" (placed after puzzle 100)

> **Putting It All Together**
>
> The Keeper's Lamp is gone, the Festival is tonight, and your five answers sit in a row on the puzzle desk.
> Ada taps them with her pencil. "No guessing now, partner. Three facts, and your answers do the rest."
>
> **Fact 1.** The person behind the Affair let themselves into the locked lighthouse with the spare key. Only
> two people had that key in hand on December 20: the answer to Puzzle 96 and the answer to Puzzle 98.
>
> **Fact 2.** The person behind the Affair carried the lamp away by rowboat. Only two people rowed out to
> Thimble Point that day: the answer to Puzzle 97 and the answer to Puzzle 99.
>
> **Fact 3.** At 9 p.m., when the light blinked three times and went dark, the person behind the Affair was up
> in the lantern room, not down on the town green, where the answer to Puzzle 100 was snapping a photo.
>
> Who was behind the Lighthouse Affair?

(About 150 words. Exactly three extra facts; nothing else on the page is evidence.)

**Solution.** Fact 1 says the person behind the Affair is Teddy (Puzzle 96) or Jonah (Puzzle 98). Fact 2 says
the same person rowed out to the Point, which again means Teddy (97) or Jonah (99), so both are still possible.
Fact 3 settles it: Teddy snapped the 9 p.m. photo on the green (Puzzle 100), so he could not have been in the
lantern room at nine. The only person who held the key, rowed to the Point, and could be at the lamp at 9 p.m.
is **Jonah Bell**.

Then a short line in Ada's voice, right after the solution:

> "The rowing didn't narrow it, partner. It told us both of them could reach the lamp. So the photo had to do the
> deciding."

(Epilogue for the solutions section: Jonah meets Ada and the apprentice at the ferry workshop
with the lamp, its reflector freshly re-silvered. The three blinks were his great-grandfather's "all's well";
"S. Bell" on the logbook was Silas's old library card; the dinghy and the flicker were his practice runs; the
polished brass in November (#91) was his first try at cleaning it; and his ferry, it turns out, is named the
*Silas B.* That night the Keeper's Lamp gets its 150th-birthday lighting on time and shines brighter than anyone
remembers. Ada allows herself one exclamation mark: "Case closed, partner!")
