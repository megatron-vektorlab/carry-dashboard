"""Chapter 3, part 1: First, Next, Last (July-early August), puzzles 31-38.

Line-ups: names plus one ordered "place in line" category. Four people in
31-34, five in 35-38. Place 1 is the front of the line (or the far left, or
the castle nearest the pier); a bigger number is farther back, farther right,
or farther from the pier.
Format: THEMES.md.  Story and cast: story/bible.md.
"""

FOUR = ["first", "second", "third", "fourth"]
FIVE = ["first", "second", "third", "fourth", "fifth"]

THEMES = [
    # ------------------------------------------------------------------ 31
    {
        "slot": 31,
        "title": "The Creamery Line",
        "story": "On the first hot afternoon of July, even Rosa left her ovens for a cone, and four "
                 "customers waited in a tidy line at the creamery window by the pier. After they had "
                 "gone, the scooper found a five-dollar bill on the boards right where the second "
                 "customer had stood. Ada believes every lost dollar has an owner. Who stood where in "
                 "line, and whose five dollars is it?",
        "entity": ["customer", "customers"],
        "cast": ["Rosa"],
        "question": {"text": "Who dropped the five-dollar bill?", "cat": "Place", "value": "second"},
        "cats": [
            {"label": "Customer", "kind": "name", "values": ["Rosa", "Ivan", "Faye", "Kit"]},
            {"label": "Place", "ordered": True, "nums": [1, 2, 3, 4], "labels": FOUR,
             "ref": "the {x} customer in line",
             "pred": "stood {x} in line",
             "neg": "did not stand {x} in line",
             "either": "stood either {a} or {b} in line",
             "nor": "stood neither {a} nor {b} in line",
             "short": "the {x} spot",
             "more": "stood somewhere behind {y}",
             "less": "stood somewhere ahead of {y}",
             "dmore": "stood exactly {d} behind {y}",
             "dless": "stood exactly {d} ahead of {y}",
             "dunit": ["place", "places"],
             "dmore1": "stood right behind {y}",
             "dless1": "stood right in front of {y}",
             "adj": "stood right next to {y}",
             "nadj": "did not stand next to {y}",
             "ends": "stood at one end of the line"},
        ],
    },
    # ------------------------------------------------------------------ 32
    {
        "slot": 32,
        "title": "The Fourth of July Parade",
        "story": "Four homemade floats rolled down Main Street for the Fourth of July, each with its "
                 "builder riding proudly on top, and Nico swears the cardboard lobster on his was the "
                 "size of a canoe. Then the Gazette's parade program came out with the floats in the "
                 "wrong order. Hattie is already at the front desk with her clipboard. For the "
                 "correction box, who rode on which float, front to back?",
        "entity": ["rider", "riders"],
        "cast": ["Hattie", "Nico"],
        "cats": [
            {"label": "Rider", "kind": "name", "values": ["Hattie", "Nico", "Selma", "Arlo"]},
            {"label": "Float", "ordered": True, "nums": [1, 2, 3, 4], "labels": FOUR,
             "ref": "the rider on the {x} float",
             "pred": "rode on the {x} float",
             "neg": "did not ride on the {x} float",
             "either": "rode on either the {a} or the {b} float",
             "nor": "rode on neither the {a} nor the {b} float",
             "short": "the {x} float",
             "more": "rode somewhere behind {y}",
             "less": "rode somewhere ahead of {y}",
             "dmore": "rode exactly {d} behind {y}",
             "dless": "rode exactly {d} ahead of {y}",
             "dunit": ["float", "floats"],
             "dmore1": "rode on the float right behind {y}'s",
             "dless1": "rode on the float right in front of {y}'s",
             "adj": "rode right before or right after {y}",
             "nadj": "did not ride right before or right after {y}",
             "ends": "rode at the very front or the very back of the parade"},
        ],
    },
    # ------------------------------------------------------------------ 33
    {
        "slot": 33,
        "title": "The Twice-Punched Ticket",
        "story": "Jonah runs the 8 a.m. ferry to the minute. This morning four passengers came up the "
                 "gangway one at a time, and Pilot the beagle greeted each of them in his little orange "
                 "life vest. Somewhere in there, Jonah's old ticket punch jammed and bit the third "
                 "ticket twice, and he would like to apologize to the right passenger. Who boarded in "
                 "which order?",
        "entity": ["passenger", "passengers"],
        "cast": ["Otis", "Jonah"],
        "question": {"text": "Whose ticket was punched twice?", "cat": "Boarded", "value": "third"},
        "cats": [
            {"label": "Passenger", "kind": "name", "values": ["Otis", "Lou", "Yusuf", "Greta"]},
            {"label": "Boarded", "ordered": True, "nums": [1, 2, 3, 4], "labels": FOUR,
             "ref": "the {x} passenger to board",
             "pred": "boarded {x}",
             "neg": "did not board {x}",
             "either": "boarded either {a} or {b}",
             "nor": "boarded neither {a} nor {b}",
             "short": "the {x} ticket",
             "more": "boarded sometime after {y}",
             "less": "boarded sometime before {y}",
             "dmore": "boarded exactly {d} after {y}",
             "dless": "boarded exactly {d} before {y}",
             "dunit": ["turn", "turns"],
             "dmore1": "boarded right after {y}",
             "dless1": "boarded right before {y}",
             "adj": "boarded right before or right after {y}",
             "nadj": "did not board right before or right after {y}",
             "ends": "boarded either first or last"},
        ],
    },
    # ------------------------------------------------------------------ 34
    {
        "slot": 34,
        "title": "The Sandcastle Row",
        "story": "Sandcastle Saturday brought out every bucket in Thimble Harbor. Four builders worked "
                 "in one row running out from the pier; Teddy photographed his own turrets from six "
                 "angles, and Mabel's moat came with a sign, correctly punctuated. The judges' sheet "
                 "numbers the castles from the pier outward, with no names at all, and the tide is on "
                 "its way in. Who built which castle?",
        "entity": ["builder", "builders"],
        "cast": ["Teddy", "Mabel"],
        "cats": [
            {"label": "Builder", "kind": "name", "values": ["Teddy", "Mabel", "Enzo", "Carmen"]},
            {"label": "Castle", "ordered": True, "nums": [1, 2, 3, 4], "labels": FOUR,
             "ref": "the builder of the {x} castle",
             "pred": "built the {x} castle from the pier",
             "neg": "did not build the {x} castle from the pier",
             "either": "built either the {a} or the {b} castle from the pier",
             "nor": "built neither the {a} nor the {b} castle from the pier",
             "short": "the {x} castle",
             "more": "built a castle farther from the pier than {y}",
             "less": "built a castle closer to the pier than {y}",
             "dmore": "built a castle exactly {d} farther from the pier than {y}",
             "dless": "built a castle exactly {d} closer to the pier than {y}",
             "dunit": ["spot", "spots"],
             "dmore1": "built the castle right beside {y}'s, on the far side from the pier",
             "dless1": "built the castle right beside {y}'s, on the pier side",
             "adj": "built a castle right beside {y}'s",
             "nadj": "did not build a castle right beside {y}'s",
             "ends": "built a castle at one end of the row"},
        ],
    },
    # ------------------------------------------------------------------ 35
    {
        "slot": 35,
        "title": "The Last Ear of Corn",
        "story": "Butter, wood smoke and a whiff of seaweed: the July clambake on Thimble Beach was "
                 "ready, and five hungry people lined up at the buffet before the tarp was even off "
                 "the pit. There was exactly one ear of corn apiece, so the person at the very back of "
                 "the line got the last one. Felix calls that shipshape planning. Who stood where in the "
                 "buffet line, and who got the last ear of corn?",
        "entity": ["diner", "diners"],
        "cast": ["Priya", "Felix"],
        "question": {"text": "Who got the last ear of corn?", "cat": "Place", "value": "fifth"},
        "cats": [
            {"label": "Diner", "kind": "name", "values": ["Priya", "Felix", "Dot", "Hugo", "Vera"]},
            {"label": "Place", "ordered": True, "nums": [1, 2, 3, 4, 5], "labels": FIVE,
             "ref": "the {x} person in line",
             "pred": "was {x} in line",
             "neg": "was not {x} in line",
             "either": "was either {a} or {b} in line",
             "nor": "was neither {a} nor {b} in line",
             "short": "the {x} spot",
             "more": "was farther back in line than {y}",
             "less": "was closer to the front of the line than {y}",
             "dmore": "was exactly {d} farther back than {y}",
             "dless": "was exactly {d} closer to the front than {y}",
             "dunit": ["place", "places"],
             "dmore1": "was right behind {y}",
             "dless1": "was right in front of {y}",
             "adj": "was right next to {y} in line",
             "nadj": "was not next to {y} in line",
             "ends": "was at the very front or the very back of the line"},
        ],
    },
    # ------------------------------------------------------------------ 36
    {
        "slot": 36,
        "title": "The Fireworks Blankets",
        "story": "Gus's knee promised clear skies for the Fourth, and his knee was right. Five friends "
                 "spread their blankets in a single row on the town green and waited for the first "
                 "rocket. From the bandstand, the Gazette's panorama photo caught all five faces lit "
                 "up red and gold, and the caption needs their names, left to right as the camera saw "
                 "them. Who sat on which blanket?",
        "entity": ["friend", "friends"],
        "cast": ["Lena", "Gus"],
        "cats": [
            {"label": "Friend", "kind": "name", "values": ["Lena", "Gus", "Tova", "Amara", "Pablo"]},
            {"label": "Blanket", "ordered": True, "nums": [1, 2, 3, 4, 5], "labels": FIVE,
             "ref": "the person on the {x} blanket",
             "pred": "sat on the {x} blanket from the left",
             "neg": "did not sit on the {x} blanket from the left",
             "either": "sat on either the {a} or the {b} blanket from the left",
             "nor": "sat on neither the {a} nor the {b} blanket from the left",
             "short": "the {x} blanket",
             "more": "sat somewhere to the right of {y}",
             "less": "sat somewhere to the left of {y}",
             "dmore": "sat exactly {d} to the right of {y}",
             "dless": "sat exactly {d} to the left of {y}",
             "dunit": ["blanket", "blankets"],
             "dmore1": "sat on the blanket directly to the right of {y}'s",
             "dless1": "sat on the blanket directly to the left of {y}'s",
             "adj": "spread a blanket right beside {y}'s",
             "nadj": "did not spread a blanket right beside {y}'s",
             "ends": "sat at one end of the row"},
        ],
    },
    # ------------------------------------------------------------------ 37
    {
        "slot": 37,
        "title": "The Book Sale Early Birds",
        "story": "Doors open at nine for the library's summer book sale, but by half past seven, five early "
                 "birds were already waiting on the steps with folding chairs and thermoses. Wren had "
                 "promised, in a whisper, that the first in line would get first pick from the box of "
                 "rare books. By eight, all five remembered being first. Who really held which spot "
                 "in line?",
        "entity": ["early bird", "early birds"],
        "cast": ["Jonah", "Wren"],
        "question": {"text": "Who gets first pick of the rare books?", "cat": "Spot", "value": "first"},
        "cats": [
            {"label": "Early bird", "kind": "name", "values": ["Oscar", "Nadia", "Jonah", "Elsa", "Milo"]},
            {"label": "Spot", "ordered": True, "nums": [1, 2, 3, 4, 5], "labels": FIVE,
             "ref": "the early bird in the {x} spot",
             "pred": "held the {x} spot in line",
             "neg": "did not hold the {x} spot in line",
             "either": "held either the {a} or the {b} spot in line",
             "nor": "held neither the {a} nor the {b} spot in line",
             "short": "the {x} spot",
             "more": "held a spot somewhere behind {y}",
             "less": "held a spot somewhere ahead of {y}",
             "dmore": "held a spot exactly {d} behind {y}",
             "dless": "held a spot exactly {d} ahead of {y}",
             "dunit": ["place", "places"],
             "dmore1": "held the spot right behind {y}",
             "dless1": "held the spot right in front of {y}",
             "adj": "held a spot right next to {y}",
             "nadj": "did not hold a spot next to {y}",
             "ends": "held a spot at one end of the line"},
        ],
    },
    # ------------------------------------------------------------------ 38
    {
        "slot": 38,
        "title": "The Committee Photo",
        "story": "Teddy lined up the Lighthouse Anniversary Committee in one row in front of Thimble "
                 "Point Light and took forty-two pictures to get one where nobody blinked. The Gazette "
                 "needs the caption, left to right as the camera saw them. Studying the print with her "
                 "magnifier, Ada notes that in every frame one member is glancing up at the lantern "
                 "room. Can you name all five, left to right?",
        "entity": ["member", "members"],
        "cast": ["Otis", "Hattie", "Jonah", "Lena", "Gus", "Teddy"],
        "cats": [
            {"label": "Member", "kind": "name", "values": ["Otis", "Hattie", "Jonah", "Lena", "Gus"]},
            {"label": "Spot", "ordered": True, "nums": [1, 2, 3, 4, 5], "labels": FIVE,
             "ref": "the {x} person from the left",
             "pred": "stood {x} from the left",
             "neg": "did not stand {x} from the left",
             "either": "stood either {a} or {b} from the left",
             "nor": "stood neither {a} nor {b} from the left",
             "short": "the {x} spot",
             "more": "stood somewhere to the right of {y}",
             "less": "stood somewhere to the left of {y}",
             "dmore": "stood exactly {d} to the right of {y}",
             "dless": "stood exactly {d} to the left of {y}",
             "dunit": ["place", "places"],
             "dmore1": "stood directly to the right of {y}",
             "dless1": "stood directly to the left of {y}",
             "adj": "stood shoulder to shoulder with {y}",
             "nadj": "did not stand shoulder to shoulder with {y}",
             "ends": "stood at one end of the row"},
        ],
    },
]
