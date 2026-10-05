"""Chapter 1: First Clues (April), puzzles 1-10.

Names plus one category; three people in 1-5, four in 6-10.
Format: THEMES.md.  Story and cast: story/bible.md.
"""

THEMES = [
    {
        "slot": 1,
        "title": "Ada's Welcome Tea",
        "story": "Ada Quill edited the Gazette's puzzle page for forty-one years, and this morning she put "
                 "the kettle on at the puzzle desk to welcome her new apprentice: you. Three neighbors "
                 "dropped by to say hello, and each chose a different tea. \"Your first assignment, partner, "
                 "is to remember who drinks what,\" Ada says, handing you a sharp pencil. Who drank which tea?",
        "entity": ["guest", "guests"],
        "cast": ["Teddy", "Lena"],
        "cats": [
            {"label": "Guest", "kind": "name", "values": ["Teddy", "Una", "Lena"]},
            {"label": "Tea", "values": ["Earl Grey", "mint", "chamomile"],
             "ref": "the guest who drank {v} tea",
             "pred": "drank {v} tea",
             "neg": "did not drink {v} tea",
             "either": "drank either {a} or {b} tea",
             "nor": "drank neither {a} nor {b} tea",
             "short": "{v} tea"},
        ],
    },
    {
        "slot": 2,
        "title": "The Seed Swap Envelopes",
        "story": "April showers moved the library's spring seed swap indoors, and three gardeners left "
                 "envelopes of saved seeds on the returns cart. Then someone opened the front door, and a "
                 "draft sent every label skating under the shelves. Wren, who can recite every overdue book "
                 "in town, whispers that each thank-you note must reach the right gardener. "
                 "Who brought which seeds?",
        "entity": ["gardener", "gardeners"],
        "cast": ["Rosa", "Wren"],
        "cats": [
            {"label": "Gardener", "kind": "name", "values": ["Rosa", "Della", "Hugo"]},
            {"label": "Seeds", "values": ["zinnia", "sweet pea", "marigold"],
             "ref": "the gardener with the {v} seeds",
             "pred": "brought the {v} seeds",
             "neg": "did not bring the {v} seeds",
             "either": "brought either the {a} or the {b} seeds",
             "nor": "brought neither the {a} nor the {b} seeds",
             "short": "the {v} seeds"},
        ],
    },
    {
        "slot": 3,
        "title": "The Lunch Pail Mix-Up",
        "story": "When the noon whistle blew at Okafor Boatyard, three workers reached for their lunch pails, "
                 "which had spent the morning side by side on one sawhorse. The pails are identical, and "
                 "nobody thought to label them. Felix pulls a pencil from behind one ear, calls the whole "
                 "business \"not shipshape,\" and says he would like to eat his own lunch, thank you. "
                 "Who packed which lunch?",
        "entity": ["worker", "workers"],
        "cast": ["Felix"],
        "cats": [
            {"label": "Worker", "kind": "name", "values": ["Felix", "Tova", "Ivan"]},
            {"label": "Lunch", "values": ["chowder", "egg salad", "meatloaf"],
             "ref": "whoever packed the {v}",
             "pred": "packed the {v}",
             "neg": "did not pack the {v}",
             "either": "packed either the {a} or the {b}",
             "nor": "packed neither the {a} nor the {b}",
             "short": "the {v}"},
        ],
    },
    {
        "slot": 4,
        "title": "The Rummage Sale Hats",
        "story": "Hattie Pruitt's spring rummage sale runs on lists: a list of tables, a list of volunteers, "
                 "and a list of her other lists. So when three hats turned up in the donation box without a "
                 "single donor slip, the clipboard came out at once. Every donor gets a handwritten thank-you "
                 "card, and Hattie does not guess. Who gave which hat?",
        "entity": ["donor", "donors"],
        "cast": ["Otis", "Hattie"],
        "cats": [
            {"label": "Donor", "kind": "name", "values": ["Otis", "Linus", "Pearl"]},
            {"label": "Hat", "values": ["sou'wester", "straw hat", "beret"],
             "ref": "the {v}'s donor",
             "pred": "donated the {v}",
             "neg": "did not donate the {v}",
             "either": "donated either the {a} or the {b}",
             "nor": "donated neither the {a} nor the {b}",
             "short": "the {v}"},
        ],
    },
    {
        "slot": 5,
        "title": "The New Paper Route",
        "story": "On his first morning delivering the Gazette, Teddy Sousa pedaled down Main Street with his "
                 "camera bouncing on his back, and three customers each asked for a little extra with "
                 "tomorrow's paper. He was sure he would remember, so he wrote nothing down. He did not "
                 "remember. Can you help him get the right extra to the right porch?",
        "entity": ["customer", "customers"],
        "cast": ["Nico", "Teddy"],
        "cats": [
            {"label": "Customer", "kind": "name", "values": ["Nico", "Amara", "Sam"]},
            {"label": "Extra", "values": ["tide table", "puzzle book", "coupons"],
             "ref": "the customer who wanted the {v}",
             "pred": "asked for the {v}",
             "neg": "did not ask for the {v}",
             "either": "asked for either the {a} or the {b}",
             "nor": "asked for neither the {a} nor the {b}",
             "short": "the {v}"},
        ],
    },
    {
        "slot": 6,
        "title": "The Muddled Umbrellas",
        "story": "Gus's left knee called for rain, and the knee was right: four people ducked into the Gull's "
                 "Rest Inn for breakfast, and when the sun came out, all four left without their umbrellas. "
                 "Priya Nair already keeps forty-one lost umbrellas, and she has no intention of making it "
                 "forty-five. She means to return every one before the noon ferry. Whose umbrella is whose?",
        "entity": ["guest", "guests"],
        "cast": ["Mabel", "Gus", "Priya"],
        "cats": [
            {"label": "Guest", "kind": "name", "values": ["Mabel", "Gus", "Kit", "Oscar"]},
            {"label": "Umbrella", "values": ["plaid", "yellow", "polka-dot", "navy"],
             "ref": "the {v} umbrella's owner",
             "pred": "left the {v} umbrella",
             "neg": "did not leave the {v} umbrella",
             "either": "left either the {a} or the {b} umbrella",
             "nor": "left neither the {a} nor the {b} umbrella",
             "short": "the {v} umbrella"},
        ],
    },
    {
        "slot": 7,
        "title": "Opening Day at the Light",
        "story": "Thimble Point Light opened for the season on a blustery April Saturday, and Lena Kowalski, "
                 "white gloves and all, made an announcement from the top step. The 1876 Keeper's Lamp, a "
                 "ceremonial light since the lighthouse retired from guiding ships, turns 150 this year: it "
                 "will shine every evening of Lantern Festival week and get a birthday lighting on Festival "
                 "night. Four volunteers each took one opening-day job. Who did which job?",
        "entity": ["volunteer", "volunteers"],
        "cast": ["Jonah", "Lena"],
        "cats": [
            {"label": "Volunteer", "kind": "name", "values": ["Jonah", "Imani", "Boris", "Faye"]},
            {"label": "Job", "values": ["ticket desk", "gift shop", "tours", "cocoa stand"],
             "ref": "the volunteer in charge of the {v}",
             "pred": "took charge of the {v}",
             "neg": "did not take charge of the {v}",
             "either": "took charge of either the {a} or the {b}",
             "nor": "took charge of neither the {a} nor the {b}",
             "short": "the {v}"},
        ],
    },
    {
        "slot": 8,
        "title": "The Sourdough Adoption",
        "story": "Rosa Delgado's Saturday bread class ended the way all her classes end: with jars. Each of "
                 "four students carried home a jar of her sourdough starter, and every starter, naturally, "
                 "came with its own name and a birthday. Now Rosa cannot remember which starter went home "
                 "with whom, and she worries about them the way other people worry about puppies. "
                 "Can you work out who adopted which starter and set her mind at rest?",
        "entity": ["student", "students"],
        "cast": ["Wren", "Rosa"],
        "cats": [
            {"label": "Student", "kind": "name", "values": ["Wren", "Dev", "Quinn", "Enzo"]},
            {"label": "Starter", "values": ["Bubbles", "Admiral", "Pip", "Barnacle"],
             "ref": "whoever took home {v}",
             "pred": "took home {v}",
             "neg": "did not take home {v}",
             "either": "took home either {a} or {b}",
             "nor": "took home neither {a} nor {b}",
             "short": "{v}"},
        ],
    },
    {
        "slot": 9,
        "title": "The Tulip Planting Gloves",
        "story": "The garden club planted four hundred tulip bulbs on the town green, and when the last bulb "
                 "went in, four pairs of muddy gloves stayed behind on the bandstand bench. Mabel Fitch, club "
                 "president and retired schoolteacher, has already written four polite notes about putting "
                 "things away. Now she needs to know whose name goes on each envelope. "
                 "Who wore which gloves?",
        "entity": ["gardener", "gardeners"],
        "cast": ["Priya", "Mabel"],
        "cats": [
            {"label": "Gardener", "kind": "name", "values": ["Priya", "Zeke", "Olive", "Cass"]},
            {"label": "Gloves", "values": ["green", "floral", "leather", "striped"],
             "ref": "the gardener in the {v} gloves",
             "pred": "wore the {v} gloves",
             "neg": "did not wear the {v} gloves",
             "either": "wore either the {a} or the {b} gloves",
             "nor": "wore neither the {a} nor the {b} gloves",
             "short": "the {v} gloves"},
        ],
    },
    {
        "slot": 10,
        "title": "The Unsigned Letters",
        "story": "Four letters to the editor landed on the Gazette's front counter this week, each on a "
                 "different burning issue of the day, and not one of them was signed. The Gazette never "
                 "prints an unsigned letter, so Ada lifted Inkwell off the stack, spread the letters across "
                 "the puzzle desk, and sent you out to ask around. Who wrote which letter?",
        "entity": ["writer", "writers"],
        "cast": ["Gus"],
        "cats": [
            {"label": "Writer", "kind": "name", "values": ["Gus", "Tariq", "Hal", "Vera"]},
            {"label": "Letter", "values": ["pothole", "parking", "seagull", "bake sale"],
             "ref": "the author of the {v} letter",
             "pred": "wrote the {v} letter",
             "neg": "did not write the {v} letter",
             "either": "wrote either the {a} or the {b} letter",
             "nor": "wrote neither the {a} nor the {b} letter",
             "short": "the {v} letter"},
        ],
    },
]
