"""Chapter 2, part 2: The Full Grid (May-June), puzzles 21-30.

All ten slots are 4 x 3 grids (four names + 2 categories), no ordered category.
Format: see THEMES.md. Story facts: story/bible.md, section 6.
"""

THEMES = [
    # ------------------------------------------------------------------ 21
    {
        "slot": 21,
        "title": "The Spring Bird Count",
        "story": "At first light on bird count morning, Mabel and three fellow garden club members "
                 "fanned out across Thimble Harbor with binoculars, thermoses and very sharp pencils. "
                 "Each came back with one special sighting from one favorite spot, and everyone told "
                 "it at once. Mabel's report goes to the state by Friday, and she has never mailed an "
                 "untidy report in her life. Who spotted which bird, and where?",
        "entity": ["birder", "birders"],
        "cast": ["Mabel"],
        "cats": [
            {"label": "Birder", "kind": "name", "values": ["Mabel", "Dev", "Tova", "Ivan"]},
            {"label": "Bird", "values": ["osprey", "heron", "oriole", "loon"],
             "ref": "the {v}'s spotter",
             "pred": "spotted the {v}",
             "neg": "did not spot the {v}",
             "either": "spotted either the {a} or the {b}",
             "nor": "spotted neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Spot", "values": ["salt marsh", "old pier", "beach", "orchard"],
             "ref": "the birder at the {v}",
             "pred": "kept watch at the {v}",
             "neg": "did not keep watch at the {v}",
             "either": "kept watch at either the {a} or the {b}",
             "nor": "kept watch at neither the {a} nor the {b}",
             "short": "the {v}"},
        ],
    },
    # ------------------------------------------------------------------ 22
    {
        "slot": 22,
        "title": "The Lighthouse Paint Crew",
        "story": "Thimble Point Light turns 150 this year, so on a bright May Saturday four volunteers "
                 "walked out to the Point at low tide with drop cloths to make it look the part. Each painted one "
                 "part of the lighthouse with one kind of tool, while the old Keeper's Lamp waited "
                 "safely under a sheet. Lena, white gloves on, wants the work log exactly right before "
                 "the big birthday night. Who painted what, and with which tool?",
        "entity": ["volunteer", "volunteers"],
        "cast": ["Teddy", "Jonah", "Lena"],
        "cats": [
            {"label": "Volunteer", "kind": "name", "values": ["Teddy", "Jonah", "Faye", "Ruben"]},
            {"label": "Part", "values": ["door", "railing", "spiral stair", "window trim"],
             "ref": "the painter of the {v}",
             "pred": "painted the {v}",
             "neg": "did not paint the {v}",
             "either": "painted either the {a} or the {b}",
             "nor": "painted neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Tool", "values": ["roller", "wide brush", "sponge", "small brush"],
             "ref": "the volunteer with the {v}",
             "pred": "worked with the {v}",
             "neg": "did not work with the {v}",
             "either": "worked with either the {a} or the {b}",
             "nor": "worked with neither the {a} nor the {b}",
             "short": "the {v}"},
        ],
    },
    # ------------------------------------------------------------------ 23
    {
        "slot": 23,
        "title": "The Ferry Lost-and-Found",
        "story": "Jonah's ferry leaves at 7:30, not 7:31, and his lost-and-found is kept just as "
                 "strictly. After Tuesday's morning run, Pilot the beagle trotted from deck to deck in "
                 "his little orange life vest and sniffed out four forgotten belongings, each left by a "
                 "different regular passenger. No item goes on the shelf without a proper tag. Who left "
                 "what behind, and where did each passenger ride?",
        "entity": ["passenger", "passengers"],
        "cast": ["Otis", "Jonah"],
        "cats": [
            {"label": "Passenger", "kind": "name", "values": ["Otis", "Carmen", "Yusuf", "Linus"]},
            {"label": "Item", "values": ["scarf", "thermos", "novel", "sun hat"],
             "ref": "the owner of the {v}",
             "pred": "left the {v} behind",
             "neg": "did not leave the {v} behind",
             "either": "left either the {a} or the {b} behind",
             "nor": "left neither the {a} nor the {b} behind",
             "short": "the {v}"},
            {"label": "Deck", "values": ["upper deck", "lower deck", "foredeck", "aft deck"],
             "ref": "the passenger on the {v}",
             "pred": "rode on the {v}",
             "neg": "did not ride on the {v}",
             "either": "rode on either the {a} or the {b}",
             "nor": "rode on neither the {a} nor the {b}",
             "short": "the {v}"},
        ],
    },
    # ------------------------------------------------------------------ 24
    {
        "slot": 24,
        "title": "The Garden Tour Signs",
        "story": "Ten minutes before the tour bus was due, a gust off the harbor flattened every sign "
                 "on the garden club's June tour and piled them on the sidewalk, Mabel's red-pencil "
                 "corrections and all. Four gardens, four flowers, four ornaments, and one garden club "
                 "president who would rather not admit she has lost track. Can you help Mabel work out "
                 "whose garden has which flower and which ornament?",
        "entity": ["gardener", "gardeners"],
        "cast": ["Hattie", "Mabel"],
        "cats": [
            {"label": "Gardener", "kind": "name", "values": ["Hattie", "Gideon", "Pearl", "Enzo"]},
            {"label": "Flower", "values": ["roses", "irises", "lupines", "peonies"],
             "ref": "the gardener who grows {v}",
             "pred": "grows {v}",
             "neg": "does not grow {v}",
             "either": "grows either {a} or {b}",
             "nor": "grows neither {a} nor {b}",
             "short": "the bed of {v}"},
            {"label": "Ornament", "values": ["birdbath", "sundial", "gnome", "trellis"],
             "ref": "the owner of the {v}",
             "pred": "has a {v}",
             "neg": "does not have a {v}",
             "either": "has either a {a} or a {b}",
             "nor": "has neither a {a} nor a {b}",
             "short": "the {v}"},
        ],
    },
    # ------------------------------------------------------------------ 25
    {
        "slot": 25,
        "title": "Supper at the Clam Shack",
        "story": "Nico was halfway through the one about the lobster the size of a canoe (a smaller "
                 "canoe than last time) when four friends gave their orders at the harbor clam shack. "
                 "Nobody was listening, the cook included. Now the fryer is hot, the cook is waiting, "
                 "and the order pad says only \"four suppers, four drinks.\" Who ordered which dish, "
                 "and who drank what?",
        "entity": ["diner", "diners"],
        "cast": ["Nico", "Felix"],
        "cats": [
            {"label": "Diner", "kind": "name", "values": ["Nico", "Felix", "Bea", "Sam"]},
            {"label": "Dish", "values": ["lobster roll", "clam basket", "haddock", "crab cake"],
             "ref": "the diner with the {v}",
             "pred": "ordered the {v}",
             "neg": "did not order the {v}",
             "either": "ordered either the {a} or the {b}",
             "nor": "ordered neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Drink", "values": ["lemonade", "iced tea", "root beer", "cider"],
             "ref": "the {v} drinker",
             "pred": "drank {v}",
             "neg": "did not drink {v}",
             "either": "drank either {a} or {b}",
             "nor": "drank neither {a} nor {b}",
             "short": "the {v}"},
        ],
    },
    # ------------------------------------------------------------------ 26
    {
        "slot": 26,
        "title": "The Grown-Up Spelling Bee",
        "story": "Four grown-ups made it to the final round of the library's spelling bee, each given "
                 "one fiendish word and each clutching a lucky charm. Wren spelled in a whisper, as "
                 "usual, and Mabel judged with her red pencil poised. Then Mabel's score sheet "
                 "slipped under the cookie table and came out with a coffee ring on it. Who spelled "
                 "which word, and which charm did each finalist hold?",
        "entity": ["finalist", "finalists"],
        "cast": ["Wren", "Mabel"],
        "cats": [
            {"label": "Finalist", "kind": "name", "values": ["Wren", "Oscar", "Imani", "Cyrus"]},
            {"label": "Word", "values": ["rhythm", "kayak", "pharaoh", "zucchini"],
             "ref": "the finalist who spelled {v}",
             "pred": "spelled {v}",
             "neg": "did not spell {v}",
             "either": "spelled either {a} or {b}",
             "nor": "spelled neither {a} nor {b}",
             "short": "the word {v}"},
            {"label": "Charm", "values": ["lucky penny", "acorn", "sea glass", "wishbone"],
             "ref": "the finalist with the {v}",
             "pred": "clutched the {v}",
             "neg": "did not clutch the {v}",
             "either": "clutched either the {a} or the {b}",
             "nor": "clutched neither the {a} nor the {b}",
             "short": "the {v}"},
        ],
    },
    # ------------------------------------------------------------------ 27
    {
        "slot": 27,
        "title": "The Graduation Cakes",
        "story": "June means graduations, and in Thimble Harbor graduations mean cake from the Salt & "
                 "Sugar Bakery. Rosa took four cake orders while feeding Gloria, her sourdough starter, "
                 "and wrote down every flavor and every topper but not a single customer's name. "
                 "Pickup starts at noon. Which customer ordered which flavor, and which topper goes "
                 "on each cake?",
        "entity": ["customer", "customers"],
        "cast": ["Gus", "Rosa"],
        "cats": [
            {"label": "Customer", "kind": "name", "values": ["Tariq", "Gus", "Jade", "Elsa"]},
            {"label": "Flavor", "values": ["lemon", "carrot", "chocolate", "coconut"],
             "ref": "the {v} cake's buyer",
             "pred": "ordered the {v} cake",
             "neg": "did not order the {v} cake",
             "either": "ordered either the {a} or the {b} cake",
             "nor": "ordered neither the {a} nor the {b} cake",
             "short": "the {v} cake"},
            {"label": "Topper", "values": ["mortarboard", "diploma", "owl", "star"],
             "ref": "the customer who chose the {v}",
             "pred": "chose the {v} topper",
             "neg": "did not choose the {v} topper",
             "either": "chose either the {a} or the {b} topper",
             "nor": "chose neither the {a} nor the {b} topper",
             "short": "the {v} topper"},
        ],
    },
    # ------------------------------------------------------------------ 28
    {
        "slot": 28,
        "title": "The Tide Pool Walk",
        "story": "Lena left her white cotton gloves at the museum this morning, since nothing in a "
                 "tide pool is likely to be older than she is. On her walk along Thimble Beach, she "
                 "and three others each found one creature in a different pool. Everything must go "
                 "back exactly where it came from before the tide turns. Who found what, and in "
                 "which pool?",
        "entity": ["walker", "walkers"],
        "cast": ["Lena"],
        "cats": [
            {"label": "Walker", "kind": "name", "values": ["Lena", "Marta", "Hugo", "Zeke"]},
            {"label": "Creature", "values": ["sea star", "crab", "snail", "urchin"],
             "ref": "the {v}'s finder",
             "pred": "found the {v}",
             "neg": "did not find the {v}",
             "either": "found either the {a} or the {b}",
             "nor": "found neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Pool", "values": ["Bathtub Pool", "Kettle Pool", "Mermaid Pool", "Moon Pool"],
             "ref": "the walker at {v}",
             "pred": "explored {v}",
             "neg": "did not explore {v}",
             "either": "explored either {a} or {b}",
             "nor": "explored neither {a} nor {b}",
             "short": "{v}"},
        ],
    },
    # ------------------------------------------------------------------ 29
    {
        "slot": 29,
        "title": "The Water Day Photos",
        "story": "Teddy shot four terrific photos at Water Day on Thimble Beach: four winners, four "
                 "races, and four prizes, one of them a whole strawberry-rhubarb pie. As usual, he did "
                 "not write down a single name. The Gazette goes to press at five, and Ada will not run "
                 "a photo without a proper caption. Who won which race, and what did each winner take "
                 "home?",
        "entity": ["winner", "winners"],
        "cast": ["Priya", "Teddy"],
        "cats": [
            {"label": "Winner", "kind": "name", "values": ["Priya", "Vera", "Kenji", "Della"]},
            {"label": "Race", "values": ["kayak", "swim", "rowing", "sailboard"],
             "ref": "the {v} race winner",
             "pred": "won the {v} race",
             "neg": "did not win the {v} race",
             "either": "won either the {a} or the {b} race",
             "nor": "won neither the {a} nor the {b} race",
             "short": "the {v} race"},
            {"label": "Prize", "values": ["trophy", "ribbon", "medal", "pie"],
             "ref": "the {v}'s new owner",
             "pred": "took home the {v}",
             "neg": "did not take home the {v}",
             "either": "took home either the {a} or the {b}",
             "nor": "took home neither the {a} nor the {b}",
             "short": "the {v}"},
        ],
    },
    # ------------------------------------------------------------------ 30
    {
        "slot": 30,
        "title": "The Borrowed Oars",
        "story": "Before Saturday's dinghy race, four rowers, Felix among them, took oars from the "
                 "rack at Okafor Boatyard, and afterward every pair went back on the wrong hook. Felix "
                 "wants each pair matched to its dinghy, shipshape. He has also noticed that his own "
                 "little dinghy sits a few yards farther up the beach than he left it, which is not "
                 "shipshape at all. Who rowed which dinghy, and with which oars?",
        "entity": ["rower", "rowers"],
        "cast": ["Felix", "Otis"],
        "cats": [
            {"label": "Rower", "kind": "name", "values": ["Felix", "Otis", "Walt", "Amara"]},
            {"label": "Oars", "values": ["varnished", "blue-tipped", "spruce", "ash"],
             "ref": "the rower with the {v} oars",
             "pred": "used the {v} oars",
             "neg": "did not use the {v} oars",
             "either": "used either the {a} or the {b} oars",
             "nor": "used neither the {a} nor the {b} oars",
             "short": "the {v} pair"},
            {"label": "Dinghy", "values": ["Minnow", "Pebble", "Skipjack", "Teacup"],
             "ref": "the {v}'s rower",
             "pred": "rowed the {v}",
             "neg": "did not row the {v}",
             "either": "rowed either the {a} or the {b}",
             "nor": "rowed neither the {a} nor the {b}",
             "short": "the {v}"},
        ],
    },
]
