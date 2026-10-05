"""Chapter 5, part 1: Two Clues at Once (September-October), puzzles 59-68.

Slots 59-64 are 4 x 3 grids (four names, one plain category, one ordered
category); slots 65-68 are 4 x 4 grids (four names, two plain categories, one
ordered category). A bigger number is "more": heavier, a higher price, older,
longer, a later ferry, a bigger fine, a later arrival, a slower maze time, a
newer clock.
Format: THEMES.md.  Story and cast: story/bible.md.
"""

THEMES = [
    # ------------------------------------------------------------------ 59
    {
        "slot": 59,
        "title": "Apples by the Pound",
        "story": "Crisp September air brought four friends to Hilltop Orchard, and each came down from "
                 "the ladders with one basket of one kind of apple. The farm stand charges by the pound, "
                 "but the scale's paper tape has jammed, and Mabel is busy removing a stray apostrophe "
                 "from the sign that reads \"Fresh Apple's.\" Who picked which apple, and how much did "
                 "each friend pick?",
        "entity": ["picker", "pickers"],
        "cast": ["Mabel"],
        "cats": [
            {"label": "Picker", "kind": "name", "values": ["Pablo", "Mabel", "Kit", "Sam"]},
            {"label": "Apple", "values": ["Cortland", "Macoun", "Baldwin", "Empire"],
             "ref": "the {v} picker",
             "pred": "picked {v} apples",
             "neg": "did not pick {v} apples",
             "either": "picked either {a} or {b} apples",
             "nor": "picked neither {a} nor {b} apples",
             "short": "the {v} apples"},
            {"label": "Weight", "ordered": True, "nums": [10, 15, 20, 25],
             "labels": ["10 pounds", "15 pounds", "20 pounds", "25 pounds"],
             "ref": "the friend who picked {x}",
             "pred": "picked {x} of apples",
             "neg": "did not pick {x} of apples",
             "either": "picked either {a} or {b} of apples",
             "nor": "picked neither {a} nor {b} of apples",
             "short": "{x}",
             "more": "had a heavier basket than {y}",
             "less": "had a lighter basket than {y}",
             "dmore": "picked exactly {d} more than {y}",
             "dless": "picked exactly {d} less than {y}",
             "dunit": ["pound", "pounds"],
             "dmore1": "had a basket just 5 pounds heavier than {y}'s",
             "dless1": "had a basket just 5 pounds lighter than {y}'s"},
        ],
    },
    # ------------------------------------------------------------------ 60
    {
        "slot": 60,
        "title": "The Elm Street Yard Sale",
        "story": "Over Labor Day weekend, four neighbors on Elm Street hauled a hundred odds and ends "
                 "onto one long table and shared a single cash box. By the time Gus's knee called the "
                 "rain, each of them had sold exactly one treasure, and the notes in the cash box had "
                 "turned into soggy scribbles. Before anyone splits the money, who sold what, and for "
                 "how much?",
        "entity": ["seller", "sellers"],
        "cast": ["Gus"],
        "cats": [
            {"label": "Seller", "kind": "name", "values": ["Linus", "Vera", "Gus", "Dot"]},
            {"label": "Item", "values": ["lamp", "teapot", "birdcage", "records"],
             "ref": "the seller of the {v}",
             "pred": "sold the {v}",
             "neg": "did not sell the {v}",
             "either": "sold either the {a} or the {b}",
             "nor": "sold neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Price", "ordered": True, "nums": [2, 4, 6, 8],
             "labels": ["$2", "$4", "$6", "$8"],
             "ref": "the seller who made {x}",
             "pred": "made {x}",
             "neg": "did not make {x}",
             "either": "made either {a} or {b}",
             "nor": "made neither {a} nor {b}",
             "short": "{x}",
             "more": "made more money than {y}",
             "less": "made less money than {y}",
             "dmore": "made exactly {d} more than {y}",
             "dless": "made exactly {d} less than {y}",
             "dunit": ["dollar", "dollars"],
             "dmore1": "made just $2 more than {y}",
             "dless1": "made just $2 less than {y}"},
        ],
    },
    # ------------------------------------------------------------------ 61
    {
        "slot": 61,
        "title": "The Smudged Class Roll",
        "story": "Tuesday is school night again in Thimble Harbor, this time for grown-ups, with evening "
                 "classes until nine. Mabel, who now teaches the grammar class, keeps the roll for the "
                 "whole building. Four new students each signed up for one class and wrote an age on "
                 "the form, in a pencil that has since smudged, and Mabel does not accept a smudged roll. "
                 "Who is taking which class, and how old is each?",
        "entity": ["student", "students"],
        "cast": ["Felix", "Mabel"],
        "cats": [
            {"label": "Student", "kind": "name", "values": ["Felix", "Jade", "Hugo", "Una"]},
            {"label": "Class", "values": ["watercolor", "Spanish", "pottery", "guitar"],
             "ref": "the student taking {v}",
             "pred": "is taking {v}",
             "neg": "is not taking {v}",
             "either": "is taking either {a} or {b}",
             "nor": "is taking neither {a} nor {b}",
             "short": "the {v} class"},
            {"label": "Age", "ordered": True, "nums": [40, 45, 50, 55],
             "ref": "the {x}-year-old",
             "pred": "is {x} years old",
             "neg": "is not {x} years old",
             "either": "is either {a} or {b} years old",
             "nor": "is neither {a} nor {b} years old",
             "short": "age {x}",
             "more": "is older than {y}",
             "less": "is younger than {y}",
             "dmore": "is exactly {d} older than {y}",
             "dless": "is exactly {d} younger than {y}",
             "dunit": ["year", "years"],
             "dmore1": "is 5 years older than {y}",
             "dless1": "is 5 years younger than {y}"},
        ],
    },
    # ------------------------------------------------------------------ 62
    {
        "slot": 62,
        "title": "The Fishing Derby Trophy",
        "story": "At dawn on derby day, four anglers cast their lines from the town pier, and each landed "
                 "one fish of a different kind and a different length before the noon horn. Otis "
                 "measured every catch, whistling a shanty off-key, then wrote the lengths on a tide "
                 "chart that the wind carried straight into the harbor. The trophy goes to the longest "
                 "fish. Who caught what, and who takes the trophy home?",
        "entity": ["angler", "anglers"],
        "cast": ["Nico", "Otis"],
        "question": {"text": "Who wins the derby trophy?", "cat": "Length", "value": "18 inches"},
        "cats": [
            {"label": "Angler", "kind": "name", "values": ["Elsa", "Nico", "Oscar", "Cyrus"]},
            {"label": "Fish", "values": ["scup", "bluefish", "mackerel", "flounder"],
             "ref": "the angler with the {v}",
             "pred": "landed the {v}",
             "neg": "did not land the {v}",
             "either": "landed either the {a} or the {b}",
             "nor": "landed neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Length", "ordered": True, "nums": [12, 14, 16, 18],
             "labels": ["12 inches", "14 inches", "16 inches", "18 inches"],
             "ref": "the angler whose fish was {x} long",
             "pred": "landed a fish {x} long",
             "neg": "did not land a fish {x} long",
             "either": "landed a fish either {a} or {b} long",
             "nor": "landed a fish neither {a} nor {b} long",
             "short": "{x}",
             "more": "landed a longer fish than {y}",
             "less": "landed a shorter fish than {y}",
             "dmore": "topped {y} by exactly {d}",
             "dless": "fell short of {y} by exactly {d}",
             "dunit": ["inch", "inches"],
             "dmore1": "topped {y} by just 2 inches",
             "dless1": "fell short of {y} by just 2 inches"},
        ],
    },
    # ------------------------------------------------------------------ 63
    {
        "slot": 63,
        "title": "The Ferry Schedule Shuffle",
        "story": "Jonah's ferry leaves every half hour on September mornings, never a minute late. Last "
                 "Tuesday, four regulars each rode a different morning run to a different stop, and "
                 "Pilot greeted each of them in his little orange life vest. Now two of the four say "
                 "they saw a light blink out at Thimble Point on the way, though the old lamp is "
                 "supposed to be dark. Jonah wants his passenger log straight. Who rode when, and where?",
        "entity": ["passenger", "passengers"],
        "cast": ["Priya", "Jonah"],
        "cats": [
            {"label": "Passenger", "kind": "name", "values": ["Ruben", "Priya", "Amara", "Tova"]},
            {"label": "Stop", "values": ["Gull Island", "Cobb Point", "Pine Key", "the mainland"],
             "ref": "the passenger bound for {v}",
             "pred": "rode to {v}",
             "neg": "did not ride to {v}",
             "either": "rode to either {a} or {b}",
             "nor": "rode to neither {a} nor {b}",
             "short": "{v}"},
            {"label": "Ferry", "ordered": True, "nums": [420, 450, 480, 510],
             "labels": ["7:00 a.m.", "7:30 a.m.", "8:00 a.m.", "8:30 a.m."],
             "ref": "the passenger on the {x} ferry",
             "pred": "took the {x} ferry",
             "neg": "did not take the {x} ferry",
             "either": "took either the {a} or the {b} ferry",
             "nor": "took neither the {a} nor the {b} ferry",
             "short": "the {x} ferry",
             "more": "took a later ferry than {y}",
             "less": "took an earlier ferry than {y}",
             "dmore": "sailed exactly {d} after {y}",
             "dless": "sailed exactly {d} before {y}",
             "dunit": ["minute", "minutes"],
             "dmore1": "sailed half an hour after {y}",
             "dless1": "sailed half an hour before {y}"},
        ],
    },
    # ------------------------------------------------------------------ 64
    {
        "slot": 64,
        "title": "The Whispered Fines",
        "story": "Rain drummed on the library roof, and four patrons came in to pay overdue fines, each "
                 "for a different book. Wren whispered every amount as she took it, so softly that not "
                 "even Wren heard herself. She whispers one more puzzle, too: "
                 "the 1876 keeper's logbook is checked out to an \"S. Bell,\" and Silas Bell, "
                 "the last keeper, has been gone for eighty years. First things first: who paid how "
                 "much, and for which book?",
        "entity": ["patron", "patrons"],
        "cast": ["Teddy", "Wren"],
        "cats": [
            {"label": "Patron", "kind": "name", "values": ["Teddy", "Basil", "Marta", "Ivan"]},
            {"label": "Book", "values": ["biography", "atlas", "poetry", "thriller"],
             "ref": "the patron with the {v} fine",
             "pred": "paid the {v} fine",
             "neg": "did not pay the {v} fine",
             "either": "paid either the {a} or the {b} fine",
             "nor": "paid neither the {a} nor the {b} fine",
             "short": "the {v} fine"},
            {"label": "Fine", "ordered": True, "nums": [25, 50, 75, 100],
             "labels": ["25 cents", "50 cents", "75 cents", "$1.00"],
             "ref": "the patron who paid {x}",
             "pred": "paid {x}",
             "neg": "did not pay {x}",
             "either": "paid either {a} or {b}",
             "nor": "paid neither {a} nor {b}",
             "short": "{x}",
             "more": "paid a bigger fine than {y}",
             "less": "paid a smaller fine than {y}",
             "dmore": "paid exactly {d} more than {y}",
             "dless": "paid exactly {d} less than {y}",
             "dunit": ["cent", "cents"],
             "dmore1": "paid just a quarter more than {y}",
             "dless1": "paid just a quarter less than {y}"},
        ],
    },
    # ------------------------------------------------------------------ 65
    {
        "slot": 65,
        "title": "The Pumpkin Weigh-Off",
        "story": "Wagons groaned onto the town green for the October weigh-off with four giant pumpkins, "
                 "each with a pet name painted on its side and a secret fertilizer its grower will not "
                 "discuss. "
                 "The big scale worked perfectly; its printout came out blank. Mabel, whose dahlia "
                 "rivalry has spread to squash, wants every ribbon pinned on the right pumpkin. Whose "
                 "pumpkin is whose, what was each one fed, and how much does each weigh?",
        "entity": ["grower", "growers"],
        "cast": ["Gus", "Mabel"],
        "cats": [
            {"label": "Grower", "kind": "name", "values": ["Zeke", "Gus", "Kenji", "Mabel"]},
            {"label": "Pumpkin", "values": ["Big Mo", "Sunny", "Tubby", "Duchess"],
             "ref": "the grower of {v}",
             "pred": "grew {v}",
             "neg": "did not grow {v}",
             "either": "grew either {a} or {b}",
             "nor": "grew neither {a} nor {b}",
             "short": "{v}"},
            {"label": "Fertilizer", "values": ["seaweed", "compost", "fish meal", "coffee"],
             "ref": "the grower who used {v}",
             "pred": "fertilized with {v}",
             "neg": "did not fertilize with {v}",
             "either": "fertilized with either {a} or {b}",
             "nor": "fertilized with neither {a} nor {b}",
             "short": "{v}"},
            {"label": "Weight", "ordered": True, "nums": [300, 400, 500, 600],
             "labels": ["300 pounds", "400 pounds", "500 pounds", "600 pounds"],
             "ref": "the grower whose pumpkin weighed {x}",
             "pred": "brought in {x} of pumpkin",
             "neg": "did not bring in {x} of pumpkin",
             "either": "brought in either {a} or {b} of pumpkin",
             "nor": "brought in neither {a} nor {b} of pumpkin",
             "short": "{x}",
             "more": "grew a heavier pumpkin than {y}",
             "less": "grew a lighter pumpkin than {y}",
             "dmore": "beat {y} by exactly {d}",
             "dless": "trailed {y} by exactly {d}",
             "dunit": ["pound", "pounds"],
             "dmore1": "beat {y} by just 100 pounds",
             "dless1": "trailed {y} by just 100 pounds"},
        ],
    },
    # ------------------------------------------------------------------ 66
    {
        "slot": 66,
        "title": "The Harvest Supper Arrivals",
        "story": "Of all the nights on Hattie's clipboard, the harvest supper is the biggest. Her four cooks arrived "
                 "fifteen minutes apart, each with a different dish carried in a different way, and "
                 "Hattie wrote down every detail on the one sheet she now cannot find. The doors of "
                 "St. Brendan's Church Hall open at six, and the table plan is still blank. Who brought "
                 "what, how, and when?",
        "entity": ["cook", "cooks"],
        "cast": ["Rosa", "Hattie"],
        "cats": [
            {"label": "Cook", "kind": "name", "values": ["Rosa", "Lou", "Selma", "Dev"]},
            {"label": "Dish", "values": ["squash soup", "cornbread", "baked beans", "apple crisp"],
             "ref": "the cook who brought the {v}",
             "pred": "brought the {v}",
             "neg": "did not bring the {v}",
             "either": "brought either the {a} or the {b}",
             "nor": "brought neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Carrier", "values": ["basket", "wagon", "tote bag", "box"],
             "ref": "the cook with the {v}",
             "pred": "came with a {v}",
             "neg": "did not come with a {v}",
             "either": "came with either a {a} or a {b}",
             "nor": "came with neither a {a} nor a {b}",
             "short": "the {v}"},
            {"label": "Arrival", "ordered": True, "nums": [0, 15, 30, 45],
             "labels": ["5:00 p.m.", "5:15 p.m.", "5:30 p.m.", "5:45 p.m."],
             "ref": "the cook who arrived at {x}",
             "pred": "arrived at {x}",
             "neg": "did not arrive at {x}",
             "either": "arrived at either {a} or {b}",
             "nor": "arrived at neither {a} nor {b}",
             "short": "{x}",
             "more": "arrived later than {y}",
             "less": "arrived earlier than {y}",
             "dmore": "arrived exactly {d} after {y}",
             "dless": "arrived exactly {d} before {y}",
             "dunit": ["minute", "minutes"],
             "dmore1": "arrived just 15 minutes after {y}",
             "dless1": "arrived just 15 minutes before {y}"},
        ],
    },
    # ------------------------------------------------------------------ 67
    {
        "slot": 67,
        "title": "The Corn Maze Chalkboard",
        "story": "Hilltop Orchard's corn maze has four ways in: two gates, the old barn door, and a gap "
                 "beside the scarecrow. Four friends each took a different one and chose a different "
                 "snack at the exit. The farmer chalked their times on the board, and then a squall "
                 "washed it clean. Jonah, who keeps his ferry on time to the minute, had left his watch "
                 "at home. Who went in where, with which snack, and how fast?",
        "entity": ["friend", "friends"],
        "cast": ["Jonah"],
        "cats": [
            {"label": "Friend", "kind": "name", "values": ["Jonah", "Faye", "Quinn", "Hal"]},
            {"label": "Entrance", "values": ["north gate", "south gate", "barn door", "scarecrow"],
             "ref": "the friend who went in by the {v}",
             "pred": "went in by the {v}",
             "neg": "did not go in by the {v}",
             "either": "went in by either the {a} or the {b}",
             "nor": "went in by neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Snack", "values": ["cider", "kettle corn", "candy apple", "donut"],
             "ref": "the friend who chose the {v}",
             "pred": "chose the {v}",
             "neg": "did not choose the {v}",
             "either": "chose either the {a} or the {b}",
             "nor": "chose neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Time", "ordered": True, "nums": [20, 25, 30, 35],
             "labels": ["20 minutes", "25 minutes", "30 minutes", "35 minutes"],
             "ref": "the friend who took {x}",
             "pred": "finished the maze in {x}",
             "neg": "did not finish the maze in {x}",
             "either": "finished the maze in either {a} or {b}",
             "nor": "finished the maze in neither {a} nor {b}",
             "short": "{x}",
             "more": "took longer than {y}",
             "less": "finished faster than {y}",
             "dmore": "took exactly {d} longer than {y}",
             "dless": "finished exactly {d} faster than {y}",
             "dunit": ["minute", "minutes"],
             "dmore1": "took just 5 minutes longer than {y}",
             "dless1": "finished just 5 minutes faster than {y}"},
        ],
    },
    # ------------------------------------------------------------------ 68
    {
        "slot": 68,
        "title": "The Sticky Auction Receipts",
        "story": "Going once, going twice: four antique clocks sold at the St. Brendan's autumn auction, "
                 "each made in a different year from a different wood, and each to a different buyer. "
                 "Hattie wrote a receipt for every sale, then set her mug of hot cider down on the "
                 "stack. The receipts are now one sticky brick. Can you match each buyer to a clock, "
                 "a wood, and a year?",
        "entity": ["buyer", "buyers"],
        "cast": ["Otis", "Hattie"],
        "cats": [
            {"label": "Buyer", "kind": "name", "values": ["Otis", "Della", "Carmen", "Pablo"]},
            {"label": "Clock", "values": ["mantel clock", "cuckoo clock", "banjo clock", "ship's clock"],
             "ref": "the buyer of the {v}",
             "pred": "bought the {v}",
             "neg": "did not buy the {v}",
             "either": "bought either the {a} or the {b}",
             "nor": "bought neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Wood", "values": ["oak", "walnut", "cherry", "maple"],
             "ref": "the buyer whose clock is {v}",
             "pred": "bought a clock made of {v}",
             "neg": "did not buy a clock made of {v}",
             "either": "bought a clock made of either {a} or {b}",
             "nor": "bought a clock made of neither {a} nor {b}",
             "short": "{v}"},
            {"label": "Year", "ordered": True, "nums": [1880, 1890, 1900, 1910],
             "ref": "the buyer whose clock dates from {x}",
             "pred": "bought a clock made in {x}",
             "neg": "did not buy a clock made in {x}",
             "either": "bought a clock made in either {a} or {b}",
             "nor": "bought a clock made in neither {a} nor {b}",
             "short": "{x}",
             "more": "bought a newer clock than {y} did",
             "less": "bought an older clock than {y} did",
             "dmore": "bought a clock exactly {d} newer than {y} did",
             "dless": "bought a clock exactly {d} older than {y} did",
             "dunit": ["year", "years"],
             "dmore1": "bought a clock a decade newer than {y} did",
             "dless1": "bought a clock a decade older than {y} did"},
        ],
    },
]
