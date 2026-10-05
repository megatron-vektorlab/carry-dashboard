"""Chapter 4: Truth or Fib? (August), puzzles 47-58.

Liar puzzles: each suspect makes one statement, and a rule says how many are
true. Three suspects in 47-50, four in 51-55, five in 56-58. The engine picks
the culprit at random, so no story depends on who did it.
Format: THEMES.md (liar themes).  Story and cast: story/bible.md, section 6.
"""

THEMES = [
    # ------------------------------------------------------------------ 47
    {
        "slot": 47,
        "title": "Who Ate the Last Scone?",
        "story": "Every Friday, Rosa saves one cranberry scone from the Salt & Sugar for Ada, and this "
                 "week, while Ada was on the phone, it turned into a plate of crumbs. Inkwell, the usual "
                 "suspect, slept through it all on the proofs. That leaves the three people in the "
                 "Gazette office, and each of them says one thing. Who owes Ada a scone?",
        "names": ["Teddy", "Bea", "Gus"],
        "did": "ate the last scone",
        "didnt": "didn't eat the last scone",
        "cast": ["Teddy", "Gus", "Rosa"],
    },
    # ------------------------------------------------------------------ 48
    {
        "slot": 48,
        "title": "Who Let the Goat Out?",
        "story": "Clementine the goat has never met a pie she didn't like, so when her pen came open at "
                 "the county fair, she trotted straight into the pie tent. Nico swears she ate a dozen; "
                 "the judges count two. Three people were leaning on the fence by her pen just before, "
                 "and each says one thing. Can you work out who let her loose?",
        "names": ["Nico", "Faye", "Linus"],
        "did": "left the goat pen open",
        "didnt": "didn't leave the goat pen open",
        "cast": ["Nico"],
    },
    # ------------------------------------------------------------------ 49
    {
        "slot": 49,
        "title": "Who Tasted the Pie Early?",
        "story": "The pie tent had barely recovered from Clementine's visit when a contest pie on the "
                 "judges' table turned up with a slice missing, a slice far too neat for any goat. The "
                 "judging is an hour away, and the judges are not amused. Three people had been setting "
                 "out entries near the table, and each has one thing to say. Which of them is the early "
                 "taster?",
        "names": ["Hal", "Mabel", "Kit"],
        "did": "cut the contest pie",
        "didnt": "didn't cut the contest pie",
        "cast": ["Mabel"],
    },
    # ------------------------------------------------------------------ 50
    {
        "slot": 50,
        "title": "Who Sounded the Ferry Horn?",
        "story": "At the stroke of midnight, the ferry's horn let out one long, tremendous blast and woke "
                 "half the harbor. Jonah was home asleep with Pilot the beagle at his feet, and only three "
                 "other people have a key to the wheelhouse. Each of them has made one statement. Can you "
                 "give Jonah a name before the 7:30 sailing?",
        "names": ["Otis", "Jade", "Vito"],
        "did": "sounded the ferry horn",
        "didnt": "didn't sound the ferry horn",
        "cast": ["Otis", "Jonah"],
    },
    # ------------------------------------------------------------------ 51
    {
        "slot": 51,
        "title": "Who Swapped the Quilt Ribbons?",
        "story": "Overnight, the blue ribbon and the red ribbon at the fair's quilt show traded places, "
                 "and two quilters are now being extremely polite to each other. Four people were in the "
                 "quilt hall after closing, Hattie and her clipboard among them. Each of them has "
                 "something to say. Can you sort out who did it before the doors open at nine?",
        "names": ["Hattie", "Wren", "Cyrus", "Elsa"],
        "did": "swapped the quilt ribbons",
        "didnt": "didn't swap the quilt ribbons",
        "cast": ["Hattie", "Wren"],
    },
    # ------------------------------------------------------------------ 52
    {
        "slot": 52,
        "title": "Who Hid the Gavel?",
        "story": "Forty folding chairs, a long agenda and strong feelings about the new Main Street "
                 "crosswalk were all in place for the August town meeting. The one thing missing was the "
                 "moderator's gavel, and the moderator refuses to start without it. Four people were in "
                 "the hall early setting out chairs, and each has a statement ready. Who is holding up "
                 "the meeting?",
        "names": ["Priya", "Gideon", "Una", "Ruben"],
        "did": "hid the gavel",
        "didnt": "didn't hide the gavel",
        "cast": ["Priya"],
    },
    # ------------------------------------------------------------------ 53
    {
        "slot": 53,
        "title": "Who Took the Postcards?",
        "story": "Lena Kowalski ordered five hundred postcards for the lighthouse's 150th anniversary, "
                 "each one showing Thimble Point Light at sunset. By closing time on Tuesday, the whole "
                 "stack had vanished from the gift shop counter. Lena counts four visitors that "
                 "afternoon, and each has one sentence to offer. Can you tell her which visitor walked "
                 "off with them?",
        "names": ["Felix", "Teddy", "Marta", "Sam"],
        "did": "took the postcards",
        "didnt": "didn't take the postcards",
        "cast": ["Felix", "Teddy", "Lena"],
    },
    # ------------------------------------------------------------------ 54
    {
        "slot": 54,
        "title": "Who Borrowed the Berry Rake?",
        "story": "Mabel Fitch has won the Blueberry Festival picking contest three summers running, and "
                 "she gives all the credit to her old berry rake. On festival morning, the rake was gone "
                 "from its nail on her porch, and the contest starts at ten. Four neighbors walked past "
                 "early, and each has a word to say about it. Mabel is sure it was only borrowed, but by "
                 "whom?",
        "names": ["Dot", "Rosa", "Enzo", "Quinn"],
        "did": "borrowed the berry rake",
        "didnt": "didn't borrow the berry rake",
        "cast": ["Rosa", "Mabel"],
    },
    # ------------------------------------------------------------------ 55
    {
        "slot": 55,
        "title": "Who Unplugged the Ferris Wheel?",
        "story": "On the last night of the county fair, the Ferris wheel's lights went dark, and the "
                 "operator sensibly stopped the wheel with Gus Mahoney at the very top. Gus spent twenty "
                 "peaceful minutes up there forecasting next week's weather for the whole fairground. "
                 "Four people had been standing by the power box, and each has one thing to report. "
                 "Who pulled the plug?",
        "names": ["Nadia", "Lena", "Ivan", "Oscar"],
        "did": "unplugged the lights",
        "didnt": "didn't unplug the lights",
        "cast": ["Lena", "Gus"],
    },
    # ------------------------------------------------------------------ 56
    {
        "slot": 56,
        "title": "Who Salted the Lemonade?",
        "story": "Hattie's August ice cream social at St. Brendan's ran like clockwork until the first "
                 "sip of lemonade made a whole row of faces pucker the wrong way. Someone had filled the "
                 "big pitcher from the salt tin instead of the sugar tin, which sit side by side on the "
                 "kitchen shelf. Five people worked in the hall kitchen that afternoon, and each makes "
                 "one statement. Whose mix-up was it?",
        "names": ["Arlo", "Hattie", "Della", "Pablo", "Yusuf"],
        "did": "salted the lemonade",
        "didnt": "didn't salt the lemonade",
        "cast": ["Hattie"],
    },
    # ------------------------------------------------------------------ 57
    {
        "slot": 57,
        "title": "Who Fed the Gulls?",
        "story": "Nine pots of chowder were simmering for the cook-off on the town pier when someone "
                 "tossed a bag of popcorn off the end, and two hundred gulls came down on the tasting "
                 "tables. Otis whistled a sea shanty at them, slightly off-key, which only seemed to "
                 "encourage them. Five people were out at the end of the pier, and each says one thing. "
                 "Before the gulls come back for seconds, can you name the popcorn tosser?",
        "names": ["Carmen", "Otis", "Imani", "Basil", "Zeke"],
        "did": "fed the gulls",
        "didnt": "didn't feed the gulls",
        "cast": ["Otis"],
    },
    # ------------------------------------------------------------------ 58
    {
        "slot": 58,
        "title": "Who Gave the Trophy a Mustache?",
        "story": "An hour before the Harbor Days awards, the sandcastle trophy turned up on the prize "
                 "table wearing a curly mustache in grease pencil. It wipes right off, and the committee "
                 "admits the trophy has never looked more distinguished. Still, five people had been "
                 "near the table, and each has one statement to make. Can you find the artist before "
                 "the awards begin?",
        "names": ["Vera", "Gideon", "Felix", "Priya", "Lou"],
        "did": "drew the mustache on the trophy",
        "didnt": "didn't draw the mustache on the trophy",
        "cast": ["Felix", "Priya"],
    },
]
