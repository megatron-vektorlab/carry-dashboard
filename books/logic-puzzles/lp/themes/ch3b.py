"""Chapter 3, part 2: First, Next, Last (July-early August), puzzles 39-46.

All eight slots are 4 x 3 grids: four names, one plain category and one
ordered category (days of the week, weeks of July, or hours of the day).
A bigger number is always the later day, week or hour.
Format: THEMES.md.  Story and cast: story/bible.md.
"""

THEMES = [
    # ------------------------------------------------------------------ 39
    {
        "slot": 39,
        "title": "The Canoe-Sized Lobster",
        "story": "From Monday to Thursday, Nico took one summer visitor a morning out on his lobster "
                 "boat, Persistence, and no two came from the same town. He keeps his bookings in his "
                 "head, right next to his lobster stories, and the two have begun to mix. He is sure "
                 "only that Wednesday's guest hauled up the week's biggest lobster, which has since "
                 "grown to the size of a canoe. Who went out on which day, and from where?",
        "entity": ["visitor", "visitors"],
        "cast": ["Nico"],
        "question": {"text": "Who hauled up the canoe-sized lobster?", "cat": "Day", "value": "Wednesday"},
        "cats": [
            {"label": "Visitor", "kind": "name", "values": ["Cass", "Hal", "Imani", "Boris"]},
            {"label": "Hometown", "values": ["Buffalo", "Tulsa", "Dover", "Reno"],
             "ref": "the visitor from {v}",
             "pred": "came from {v}",
             "neg": "did not come from {v}",
             "either": "came from either {a} or {b}",
             "nor": "came from neither {a} nor {b}",
             "short": "{v}"},
            {"label": "Day", "ordered": True, "nums": [1, 2, 3, 4],
             "labels": ["Monday", "Tuesday", "Wednesday", "Thursday"],
             "ref": "the {x} visitor",
             "pred": "went out on {x}",
             "neg": "did not go out on {x}",
             "either": "went out on either {a} or {b}",
             "nor": "went out on neither {a} nor {b}",
             "short": "{x}",
             "more": "went out later in the week than {y}",
             "less": "went out earlier in the week than {y}",
             "dmore": "went out exactly {d} after {y}",
             "dless": "went out exactly {d} before {y}",
             "dunit": ["day", "days"],
             "dmore1": "went out the day after {y}",
             "dless1": "went out the day before {y}"},
        ],
    },
    # ------------------------------------------------------------------ 40
    {
        "slot": 40,
        "title": "A Piano on the Ferry",
        "story": "Pilot the beagle has greeted plenty of odd cargo from the ferry's deck, but never a "
                 "week like this one: a piano, a beehive, a canoe and an armchair, one a day from "
                 "Tuesday to Friday, each from a different sender and each bound for Gull Island. The "
                 "island postmaster signed every slip on the wrong line. Jonah keeps his log to the "
                 "minute and wants it right. Who sent what, and on which day?",
        "entity": ["sender", "senders"],
        "cast": ["Gus", "Jonah"],
        "cats": [
            {"label": "Sender", "kind": "name", "values": ["Gus", "Faye", "Tariq", "Una"]},
            {"label": "Cargo", "values": ["piano", "beehive", "canoe", "armchair"],
             "ref": "the sender of the {v}",
             "pred": "sent the {v}",
             "neg": "did not send the {v}",
             "either": "sent either the {a} or the {b}",
             "nor": "sent neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Day", "ordered": True, "nums": [1, 2, 3, 4],
             "labels": ["Tuesday", "Wednesday", "Thursday", "Friday"],
             "ref": "the {x} sender",
             "pred": "shipped on {x}",
             "neg": "did not ship on {x}",
             "either": "shipped on either {a} or {b}",
             "nor": "shipped on neither {a} nor {b}",
             "short": "{x}",
             "more": "shipped later in the week than {y}",
             "less": "shipped earlier in the week than {y}",
             "dmore": "shipped exactly {d} after {y}",
             "dless": "shipped exactly {d} before {y}",
             "dunit": ["day", "days"],
             "dmore1": "shipped the day after {y}",
             "dless1": "shipped the day before {y}"},
        ],
    },
    # ------------------------------------------------------------------ 41
    {
        "slot": 41,
        "title": "The Blueberry Picking Map",
        "story": "Wild blueberries ripen all over the hills behind Thimble Harbor in late July, just in "
                 "time for the August festival. Mabel and three neighbors each picked a different patch, "
                 "one picker a day from Wednesday to Saturday. Now Mabel is drawing a picking map for "
                 "next year, every label spelled just so, to show which patch ripens when. Who picked "
                 "which patch, and on which day?",
        "entity": ["picker", "pickers"],
        "cast": ["Mabel"],
        "cats": [
            {"label": "Picker", "kind": "name", "values": ["Mabel", "Ruben", "Jade", "Vito"]},
            {"label": "Patch", "values": ["north field", "hilltop", "stone wall", "creekside"],
             "ref": "the {v} picker",
             "pred": "worked the {v} patch",
             "neg": "did not work the {v} patch",
             "either": "worked either the {a} or the {b} patch",
             "nor": "worked neither the {a} nor the {b} patch",
             "short": "the {v} patch"},
            {"label": "Day", "ordered": True, "nums": [1, 2, 3, 4],
             "labels": ["Wednesday", "Thursday", "Friday", "Saturday"],
             "ref": "the {x} picker",
             "pred": "went picking on {x}",
             "neg": "did not go picking on {x}",
             "either": "went picking on either {a} or {b}",
             "nor": "went picking on neither {a} nor {b}",
             "short": "{x}",
             "more": "went picking later in the week than {y}",
             "less": "went picking earlier in the week than {y}",
             "dmore": "went picking exactly {d} after {y}",
             "dless": "went picking exactly {d} before {y}",
             "dunit": ["day", "days"],
             "dmore1": "went picking the day after {y}",
             "dless1": "went picking the day before {y}"},
        ],
    },
    # ------------------------------------------------------------------ 42
    {
        "slot": 42,
        "title": "Once Upon a Story Hour",
        "story": "Once a week through July, a different volunteer settled onto the library's story-hour "
                 "rug and read aloud to a circle of small children in sun hats. Wren took her turn too, "
                 "in her usual whisper, and the children leaned in so far they nearly tipped over. The "
                 "newsletter thanking all four readers goes to print tomorrow. Who read on which date, "
                 "and what kind of book did each one choose?",
        "entity": ["volunteer", "volunteers"],
        "cast": ["Wren"],
        "cats": [
            {"label": "Volunteer", "kind": "name", "values": ["Wren", "Kenji", "Sam", "Olive"]},
            {"label": "Book", "values": ["pirate tale", "fairy tale", "poems", "fables"],
             "ref": "the volunteer with the {v}",
             "pred": "read the {v}",
             "neg": "did not read the {v}",
             "either": "read either the {a} or the {b}",
             "nor": "read neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Week", "ordered": True, "nums": [1, 2, 3, 4],
             "labels": ["July 8", "July 15", "July 22", "July 29"],
             "ref": "the {x} volunteer",
             "pred": "read on {x}",
             "neg": "did not read on {x}",
             "either": "read on either {a} or {b}",
             "nor": "read on neither {a} nor {b}",
             "short": "{x}",
             "more": "read later in the month than {y}",
             "less": "read earlier in the month than {y}",
             "dmore": "read exactly {d} after {y}",
             "dless": "read exactly {d} before {y}",
             "dunit": ["week", "weeks"],
             "dmore1": "read the week after {y}",
             "dless1": "read the week before {y}"},
        ],
    },
    # ------------------------------------------------------------------ 43
    {
        "slot": 43,
        "title": "A Flicker After Closing",
        "story": "At the lighthouse museum, whoever locks up for the night writes one line in the "
                 "lock-up log. Four volunteers took the nights from Thursday to Sunday, and each wrote "
                 "about something different, but not one of them signed or dated a line. Lena, gloves "
                 "on, is most curious about one note: an odd flicker, high in the dark lantern room, "
                 "after closing time. Who locked up on which night, and who saw the flicker?",
        "entity": ["volunteer", "volunteers"],
        "cast": ["Teddy", "Priya", "Lena"],
        "question": {"text": "Who noticed the odd flicker?", "cat": "Note", "value": "odd flicker"},
        "cats": [
            {"label": "Volunteer", "kind": "name", "values": ["Teddy", "Della", "Priya", "Arlo"]},
            {"label": "Note", "values": ["stuck latch", "gull nest", "wet paint", "odd flicker"],
             "ref": "the volunteer who noted the {v}",
             "pred": "noted the {v}",
             "neg": "did not note the {v}",
             "either": "noted either the {a} or the {b}",
             "nor": "noted neither the {a} nor the {b}",
             "short": "the {v} note"},
            {"label": "Night", "ordered": True, "nums": [1, 2, 3, 4],
             "labels": ["Thursday", "Friday", "Saturday", "Sunday"],
             "ref": "the {x} volunteer",
             "pred": "locked up on {x}",
             "neg": "did not lock up on {x}",
             "either": "locked up on either {a} or {b}",
             "nor": "locked up on neither {a} nor {b}",
             "short": "{x}",
             "more": "locked up on a later night than {y}",
             "less": "locked up on an earlier night than {y}",
             "dmore": "locked up exactly {d} after {y}",
             "dless": "locked up exactly {d} before {y}",
             "dunit": ["night", "nights"],
             "dmore1": "locked up the night after {y}",
             "dless1": "locked up the night before {y}"},
        ],
    },
    # ------------------------------------------------------------------ 44
    {
        "slot": 44,
        "title": "Mostly Shipshape",
        "story": "With a pencil behind each ear, Felix gave four sailing lessons on Saturday morning, "
                 "one an hour, each in a different little sailboat from his yard. He kept the lesson "
                 "sheet in his head, which he calls shipshape. It is mostly shipshape. Every student "
                 "is owed a certificate naming the boat and the hour, so who sailed when, and in which "
                 "boat?",
        "entity": ["student", "students"],
        "cast": ["Felix"],
        "cats": [
            {"label": "Student", "kind": "name", "values": ["Walt", "Carmen", "Emil", "Pearl"]},
            {"label": "Boat", "values": ["Whelk", "Tern", "Bluebell", "Ripple"],
             "ref": "the {v}'s sailor",
             "pred": "sailed the {v}",
             "neg": "did not sail the {v}",
             "either": "sailed either the {a} or the {b}",
             "nor": "sailed neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Time", "ordered": True, "nums": [9, 10, 11, 12],
             "labels": ["9 a.m.", "10 a.m.", "11 a.m.", "noon"],
             "ref": "the {x} student",
             "pred": "had the {x} lesson",
             "neg": "did not have the {x} lesson",
             "either": "had either the {a} or the {b} lesson",
             "nor": "had neither the {a} nor the {b} lesson",
             "short": "{x}",
             "more": "had a later lesson than {y}",
             "less": "had an earlier lesson than {y}",
             "dmore": "had a lesson exactly {d} after {y}",
             "dless": "had a lesson exactly {d} before {y}",
             "dunit": ["hour", "hours"],
             "dmore1": "had the lesson right after {y}",
             "dless1": "had the lesson right before {y}"},
        ],
    },
    # ------------------------------------------------------------------ 45
    {
        "slot": 45,
        "title": "Four Orders on the Back Shelf",
        "story": "Rosa's order book is her pride, second only to Gloria, her oldest sourdough starter. "
                 "On Friday morning four special orders waited on the back shelf at Salt & Sugar, among "
                 "them a cinnamon bun the size of a dinner plate, and four customers came to collect "
                 "them, each at a different hour. In the bustle, Rosa never wrote down who took what. "
                 "Before the next rush, can you work out who collected which order, and when?",
        "entity": ["customer", "customers"],
        "cast": ["Nico", "Rosa"],
        "cats": [
            {"label": "Customer", "kind": "name", "values": ["Nico", "Zeke", "Lou", "Milo"]},
            {"label": "Order", "values": ["layer cake", "baguettes", "rye loaf", "cinnamon bun"],
             "ref": "the customer with the {v}",
             "pred": "ordered the {v}",
             "neg": "did not order the {v}",
             "either": "ordered either the {a} or the {b}",
             "nor": "ordered neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Pickup", "ordered": True, "nums": [7, 8, 9, 10],
             "labels": ["7 a.m.", "8 a.m.", "9 a.m.", "10 a.m."],
             "ref": "the {x} customer",
             "pred": "came in at {x}",
             "neg": "did not come in at {x}",
             "either": "came in at either {a} or {b}",
             "nor": "came in at neither {a} nor {b}",
             "short": "{x}",
             "more": "came in later than {y}",
             "less": "came in earlier than {y}",
             "dmore": "came in exactly {d} after {y}",
             "dless": "came in exactly {d} before {y}",
             "dunit": ["hour", "hours"],
             "dmore1": "came in an hour after {y}",
             "dless1": "came in an hour before {y}"},
        ],
    },
    # ------------------------------------------------------------------ 46
    {
        "slot": 46,
        "title": "Last Call for Pickles",
        "story": "The county fair office stops taking entries at five o'clock on the eve of the fair, "
                 "and this year four last-minute exhibitors came puffing up the steps an hour apart, "
                 "starting at one. The clerk stamped every entry, listened politely to Otis's off-key "
                 "sea shanty, and then knocked a lemonade across the entry sheet. The judges arrive at "
                 "eight tomorrow morning. Who brought which entry, and at what time?",
        "entity": ["exhibitor", "exhibitors"],
        "cast": ["Otis"],
        "cats": [
            {"label": "Exhibitor", "kind": "name", "values": ["Hugo", "Selma", "Dev", "Otis"]},
            {"label": "Entry", "values": ["pickles", "quilt", "honey", "zucchini"],
             "ref": "the exhibitor with the {v}",
             "pred": "entered the {v}",
             "neg": "did not enter the {v}",
             "either": "entered either the {a} or the {b}",
             "nor": "entered neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Time", "ordered": True, "nums": [1, 2, 3, 4],
             "labels": ["1 p.m.", "2 p.m.", "3 p.m.", "4 p.m."],
             "ref": "the {x} exhibitor",
             "pred": "arrived at {x}",
             "neg": "did not arrive at {x}",
             "either": "arrived at either {a} or {b}",
             "nor": "arrived at neither {a} nor {b}",
             "short": "{x}",
             "more": "arrived later than {y}",
             "less": "arrived earlier than {y}",
             "dmore": "arrived exactly {d} after {y}",
             "dless": "arrived exactly {d} before {y}",
             "dunit": ["hour", "hours"],
             "dmore1": "arrived an hour after {y}",
             "dless1": "arrived an hour before {y}"},
        ],
    },
]
