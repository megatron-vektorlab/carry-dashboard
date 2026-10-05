"""Chapter 2, part 1: The Full Grid (May-June), puzzles 11-20.

Slots 11-18 are 3 x 3 grids (names + 2 categories), slots 19-20 are 4 x 3.
Format: see THEMES.md. Story facts: story/bible.md, section 6.
"""

THEMES = [
    # ------------------------------------------------------------------ 11
    {
        "slot": 11,
        "title": "The Regatta Pennants",
        "story": "The Spring Regatta starts at ten sharp, and Otis has the starting horn in one hand "
                 "and a mug of coffee in the other. Some of that coffee is now on the start sheet. "
                 "Three sailors are flying three different pennants on three different boats, and Otis "
                 "needs every line right before he sounds the horn. Can you match each sailor with a "
                 "pennant and a boat?",
        "entity": ["sailor", "sailors"],
        "cast": ["Felix", "Otis"],
        "cats": [
            {"label": "Sailor", "kind": "name", "values": ["Felix", "Selma", "Arlo"]},
            {"label": "Pennant", "values": ["red", "blue", "gold"],
             "ref": "the sailor with the {v} pennant",
             "pred": "flew the {v} pennant",
             "neg": "did not fly the {v} pennant",
             "either": "flew either the {a} or the {b} pennant",
             "nor": "flew neither the {a} nor the {b} pennant",
             "short": "the {v} pennant"},
            {"label": "Boat", "values": ["sloop", "catboat", "dory"],
             "ref": "the {v}'s skipper",
             "pred": "sailed the {v}",
             "neg": "did not sail the {v}",
             "either": "sailed either the {a} or the {b}",
             "nor": "sailed neither the {a} nor the {b}",
             "short": "the {v}"},
        ],
    },
    # ------------------------------------------------------------------ 12
    {
        "slot": 12,
        "title": "The Swapped Jam Labels",
        "story": "For the blind tasting at the St. Brendan's spring supper, Hattie peeled the labels "
                 "off all the jams, her own included. For once in her life, she did not make a list. "
                 "The judges have their ribbons ready, and nobody can say whose jam is whose. Can you "
                 "match each cook with a jam and a jar before the ribbons go out?",
        "entity": ["cook", "cooks"],
        "cast": ["Hattie"],
        "cats": [
            {"label": "Cook", "kind": "name", "values": ["Hattie", "Ruben", "Lou"]},
            {"label": "Jam", "values": ["plum", "fig", "quince"],
             "ref": "the {v} jam's maker",
             "pred": "made the {v} jam",
             "neg": "did not make the {v} jam",
             "either": "made either the {a} or the {b} jam",
             "nor": "made neither the {a} nor the {b} jam",
             "short": "the {v} jam"},
            {"label": "Jar", "values": ["mason jar", "crock", "tin"],
             "ref": "the cook with the {v}",
             "pred": "used the {v}",
             "neg": "did not use the {v}",
             "either": "used either the {a} or the {b}",
             "nor": "used neither the {a} nor the {b}",
             "short": "the {v}"},
        ],
    },
    # ------------------------------------------------------------------ 13
    {
        "slot": 13,
        "title": "The Book Drop Surprise",
        "story": "Sometime overnight, three long-overdue books thumped into the library's book drop, "
                 "each with a stray bookmark still tucked inside. Wren would like to clear the right "
                 "accounts. \"And return the bookmarks,\" she whispers. \"People always want their "
                 "bookmarks back.\" Who returned which book, and which bookmark was tucked in each?",
        "entity": ["reader", "readers"],
        "cast": ["Nico", "Wren"],
        "cats": [
            {"label": "Reader", "kind": "name", "values": ["Nico", "Della", "Kenji"]},
            {"label": "Book", "values": ["atlas", "cookbook", "whodunit"],
             "ref": "the borrower of the {v}",
             "pred": "returned the {v}",
             "neg": "did not return the {v}",
             "either": "returned either the {a} or the {b}",
             "nor": "returned neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Bookmark", "values": ["ribbon", "postcard", "receipt"],
             "ref": "the reader who used the {v}",
             "pred": "used the {v} as a bookmark",
             "neg": "did not use the {v} as a bookmark",
             "either": "used either the {a} or the {b} as a bookmark",
             "nor": "used neither the {a} nor the {b} as a bookmark",
             "short": "the {v}"},
        ],
    },
    # ------------------------------------------------------------------ 14
    {
        "slot": 14,
        "title": "The Mother's Day Corsages",
        "story": "Mother's Day is tomorrow, and the garden club's corsage table has vanished under "
                 "petals, ribbon ends and order slips. Three of the slips got shuffled on the counter. "
                 "Mabel will not hand a single corsage to the wrong person, and she has her "
                 "reading glasses on and her red pencil out. Who ordered which flower, and which "
                 "ribbon goes with it?",
        "entity": ["customer", "customers"],
        "cast": ["Jonah", "Mabel"],
        "cats": [
            {"label": "Customer", "kind": "name", "values": ["Jonah", "Bea", "Cyrus"]},
            {"label": "Flower", "values": ["carnation", "rose", "peony"],
             "ref": "the customer who ordered the {v}",
             "pred": "ordered the {v} corsage",
             "neg": "did not order the {v} corsage",
             "either": "ordered either the {a} or the {b} corsage",
             "nor": "ordered neither the {a} nor the {b} corsage",
             "short": "the {v} corsage"},
            {"label": "Ribbon", "values": ["lavender", "white", "peach"],
             "ref": "the customer who chose the {v} ribbon",
             "pred": "chose the {v} ribbon",
             "neg": "did not choose the {v} ribbon",
             "either": "chose either the {a} or the {b} ribbon",
             "nor": "chose neither the {a} nor the {b} ribbon",
             "short": "the {v} ribbon"},
        ],
    },
    # ------------------------------------------------------------------ 15
    {
        "slot": 15,
        "title": "Kite Day Tangle",
        "story": "A stiff May breeze on Kite Day sent three kites swooping over the town green, then "
                 "into one another, then into a single glorious knot. Teddy took eleven photos of it "
                 "before he remembered that one of the kites was his. Before anyone starts tugging, "
                 "untangle the knot on paper: who flew which kite, with which tail?",
        "entity": ["flier", "fliers"],
        "cast": ["Teddy"],
        "cats": [
            {"label": "Flier", "kind": "name", "values": ["Teddy", "Una", "Hugo"]},
            {"label": "Kite", "values": ["dragon", "box", "diamond"],
             "ref": "the {v} kite's flier",
             "pred": "flew the {v} kite",
             "neg": "did not fly the {v} kite",
             "either": "flew either the {a} or the {b} kite",
             "nor": "flew neither the {a} nor the {b} kite",
             "short": "the {v} kite"},
            {"label": "Tail", "values": ["bows", "streamers", "tassels"],
             "ref": "the flier who chose {v}",
             "pred": "chose {v} for a tail",
             "neg": "did not choose {v} for a tail",
             "either": "chose either {a} or {b} for a tail",
             "nor": "chose neither {a} nor {b} for a tail",
             "short": "the tail of {v}"},
        ],
    },
    # ------------------------------------------------------------------ 16
    {
        "slot": 16,
        "title": "The Boatyard Paint Cans",
        "story": "Three hulls sit on sawhorses at Okafor Boatyard, scraped bare and ready for a fresh "
                 "coat. The paint cans, unfortunately, have lost their tags, and Felix will not open a "
                 "can on a guess. \"Shipshape or nothing,\" he says, reaching for the pencil behind "
                 "his left ear. Which owner brought in which boat, and what color is going on it?",
        "entity": ["owner", "owners"],
        "cast": ["Gus", "Felix"],
        "cats": [
            {"label": "Owner", "kind": "name", "values": ["Gus", "Imani", "Basil"]},
            {"label": "Color", "values": ["sea green", "navy", "cream"],
             "ref": "the owner who chose {v}",
             "pred": "chose {v}",
             "neg": "did not choose {v}",
             "either": "chose either {a} or {b}",
             "nor": "chose neither {a} nor {b}",
             "short": "the {v} paint"},
            {"label": "Boat", "values": ["Sea Pea", "Lucky Gull", "Wavelet"],
             "ref": "the {v}'s owner",
             "pred": "brought in the {v}",
             "neg": "did not bring in the {v}",
             "either": "brought in either the {a} or the {b}",
             "nor": "brought in neither the {a} nor the {b}",
             "short": "the {v}"},
        ],
    },
    # ------------------------------------------------------------------ 17
    {
        "slot": 17,
        "title": "The Rhubarb Social",
        "story": "Hattie lettered the place cards for her May rhubarb social a full week ahead, in her "
                 "very best penmanship. Then three bakers swept in, set their desserts down wherever "
                 "they found room, and drifted off to admire the lilacs. Now every card sits by the "
                 "wrong plate. Can you match each baker to a dessert and a topping before the first "
                 "fork goes in?",
        "entity": ["baker", "bakers"],
        "cast": ["Rosa", "Hattie"],
        "cats": [
            {"label": "Baker", "kind": "name", "values": ["Rosa", "Walt", "Elsa"]},
            {"label": "Dessert", "values": ["shortcake", "pie", "crumble"],
             "ref": "the {v}'s baker",
             "pred": "baked the {v}",
             "neg": "did not bake the {v}",
             "either": "baked either the {a} or the {b}",
             "nor": "baked neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Topping", "values": ["custard", "ice cream", "honey"],
             "ref": "the baker who brought the {v}",
             "pred": "brought the {v}",
             "neg": "did not bring the {v}",
             "either": "brought either the {a} or the {b}",
             "nor": "brought neither the {a} nor the {b}",
             "short": "the {v}"},
        ],
    },
    # ------------------------------------------------------------------ 18
    {
        "slot": 18,
        "title": "The Buoys After the Storm",
        "story": "Last night's gale sent lobster buoys bobbing all over the harbor, from Seal Ledge "
                 "clear to the ferry dock. Otis spent the morning fishing them out with a boat hook, "
                 "whistling a shanty slightly off-key. Three of the strays belong to three different "
                 "lobstermen, and the harbor log has to say who fishes where. Whose buoy is whose, "
                 "and where does each of them fish?",
        "entity": ["lobsterman", "lobstermen"],
        "cast": ["Nico", "Otis"],
        "cats": [
            {"label": "Lobsterman", "kind": "name", "values": ["Oscar", "Nico", "Pablo"]},
            {"label": "Buoy", "values": ["orange", "striped", "checkered"],
             "ref": "the owner of the {v} buoy",
             "pred": "owns the {v} buoy",
             "neg": "does not own the {v} buoy",
             "either": "owns either the {a} or the {b} buoy",
             "nor": "owns neither the {a} nor the {b} buoy",
             "short": "the {v} buoy"},
            {"label": "Spot", "values": ["Gull Rock", "East Cove", "the Narrows"],
             "ref": "the lobsterman who fishes at {v}",
             "pred": "fishes at {v}",
             "neg": "does not fish at {v}",
             "either": "fishes at either {a} or {b}",
             "nor": "fishes at neither {a} nor {b}",
             "short": "{v}"},
        ],
    },
    # ------------------------------------------------------------------ 19
    {
        "slot": 19,
        "title": "The Memorial Day Floats",
        "story": "Every year the Gazette prints one big photo of the Memorial Day floats, and every "
                 "year somebody's name ends up under somebody else's lighthouse. This morning four "
                 "floats rolled down Main Street to the green, each builder riding on top and playing "
                 "a different instrument. Ada would like the caption right the first time. Who built "
                 "which float, and who played what?",
        "entity": ["builder", "builders"],
        "cast": ["Lena", "Gus"],
        "cats": [
            {"label": "Builder", "kind": "name", "values": ["Lena", "Gus", "Zeke", "Marta"]},
            {"label": "Float", "values": ["tall ship", "lobster", "lighthouse", "whale"],
             "ref": "the builder of the {v} float",
             "pred": "built the {v} float",
             "neg": "did not build the {v} float",
             "either": "built either the {a} or the {b} float",
             "nor": "built neither the {a} nor the {b} float",
             "short": "the {v} float"},
            {"label": "Music", "values": ["fiddle", "tuba", "banjo", "accordion"],
             "ref": "the {v} player",
             "pred": "played the {v}",
             "neg": "did not play the {v}",
             "either": "played either the {a} or the {b}",
             "nor": "played neither the {a} nor the {b}",
             "short": "the {v}"},
        ],
    },
    # ------------------------------------------------------------------ 20
    {
        "slot": 20,
        "title": "The Swapped Room Keys",
        "story": "Friday evening brought a rush to the Gull's Rest Inn: four guests checked in within "
                 "ten minutes, all talking at once about the traffic. Somewhere in the hubbub, the room "
                 "keys got swapped on the front desk. Priya has returned forty-one umbrellas to "
                 "forty-one owners, and she is not about to lose track of four guests. Who is staying "
                 "in which room, and where is each guest from?",
        "entity": ["guest", "guests"],
        "cast": ["Priya"],
        "cats": [
            {"label": "Guest", "kind": "name", "values": ["Vito", "Amara", "Kit", "Hal"]},
            {"label": "Room", "values": ["Gull", "Tern", "Puffin", "Heron"],
             "ref": "the guest in the {v} Room",
             "pred": "is staying in the {v} Room",
             "neg": "is not staying in the {v} Room",
             "either": "is staying in either the {a} or the {b} Room",
             "nor": "is staying in neither the {a} nor the {b} Room",
             "short": "the {v} Room"},
            {"label": "Hometown", "values": ["Boston", "Albany", "Hartford", "Portland"],
             "ref": "the guest from {v}",
             "pred": "is from {v}",
             "neg": "is not from {v}",
             "either": "is from either {a} or {b}",
             "nor": "is from neither {a} nor {b}",
             "short": "{v}"},
        ],
    },
]
