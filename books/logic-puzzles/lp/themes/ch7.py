"""Chapter 7: The Lighthouse Affair (December 20-21), puzzles 96-100.

Five linked "suppose" cases, 5 x 4 with one ordered time category each.
Every answer is forced (theme "answer") to match the finale timeline in
story/bible.md, section 7:

    96  Who borrowed the spare lighthouse key?      Teddy   10:00 a.m.-noon
    97  Who rowed out to Thimble Point?             Teddy   1:30-3:30 p.m.
    98  Who received the spare key at the dock?     Jonah   5:00-6:20 p.m.
    99  Who rowed out to Thimble Point after dark?  Jonah   7:00-8:20 p.m.
    100 Who snapped the 9 p.m. photo?               Teddy   7:00-9:00 p.m.

Jonah's secret stays secret: no surname, no family line, no ferry name.
Times are written as minutes after midnight, so a step of 30 is half an hour.
Format: THEMES.md.  Story and cast: story/bible.md.
"""

THEMES = [
    # ------------------------------------------------------------------ 96
    {
        "slot": 96,
        "title": "The Harbor Office Sign-Out",
        "story": "At dawn on Festival day, Lena found the Keeper's Lamp gone from Thimble Point Light "
                 "and a note on the sill: \"It will shine again.\" Ada starts where the spare key is "
                 "kept, at the harbor office. On Festival Eve, Otis left for a harbormasters' meeting "
                 "in Portland at ten, and five visitors in winter gloves signed things out on his "
                 "honor-system slate. This morning, as always, he wiped it clean: \"Fresh tide, fresh "
                 "slate.\" Who took what, and when?",
        "entity": ["visitor", "visitors"],
        "cast": ["Teddy", "Gus", "Otis", "Lena"],
        "question": {"text": "Who borrowed the spare lighthouse key?", "cat": "Item", "value": "spare key"},
        "answer": "Teddy",
        "cats": [
            {"label": "Visitor", "kind": "name", "values": ["Walt", "Teddy", "Amara", "Selma", "Gus"]},
            {"label": "Item", "values": ["spare key", "binoculars", "tide chart", "megaphone", "life ring"],
             "ref": "the borrower of the {v}",
             "pred": "borrowed the {v}",
             "neg": "did not borrow the {v}",
             "either": "borrowed either the {a} or the {b}",
             "nor": "borrowed neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Gloves", "values": ["wool", "leather", "fleece", "fingerless", "ski"],
             "ref": "the person in the {v} gloves",
             "pred": "wore {v} gloves",
             "neg": "did not wear {v} gloves",
             "either": "wore either {a} or {b} gloves",
             "nor": "wore neither {a} nor {b} gloves",
             "short": "the {v} gloves"},
            {"label": "Time", "ordered": True,
             "nums": [600, 630, 660, 690, 720],
             "labels": ["10:00 a.m.", "10:30 a.m.", "11:00 a.m.", "11:30 a.m.", "noon"],
             "ref": "the person who signed the slate at {x}",
             "pred": "signed the slate at {x}",
             "neg": "did not sign the slate at {x}",
             "either": "signed the slate at either {a} or {b}",
             "nor": "signed the slate at neither {a} nor {b}",
             "short": "{x}",
             "more": "signed the slate later than {y}",
             "less": "signed the slate earlier than {y}",
             "dmore": "signed the slate exactly {d} after {y}",
             "dless": "signed the slate exactly {d} before {y}",
             "dunit": ["minute", "minutes"],
             "dmore1": "signed the slate half an hour after {y}",
             "dless1": "signed the slate half an hour before {y}"},
        ],
    },
    # ------------------------------------------------------------------ 97
    {
        "slot": 97,
        "title": "The Afternoon Boats",
        "story": "On a cold, calm Festival Eve afternoon, five rowers in the lantern flotilla took "
                 "the boatyard's rental rowboats out to rehearse, each to a different spot on the "
                 "route. Felix keeps those boats in the water this late only for the flotilla. "
                 "High tide had the causeway under water, so the only way to the Point was by boat. "
                 "Felix rowed too, so he can vouch for his own trip and nobody else's. Who rowed which "
                 "boat where, and when?",
        "entity": ["rower", "rowers"],
        "cast": ["Nico", "Teddy", "Felix"],
        "question": {"text": "Who rowed out to Thimble Point?", "cat": "Went to", "value": "the Point"},
        "answer": "Teddy",
        "cats": [
            {"label": "Rower", "kind": "name", "values": ["Nico", "Teddy", "Felix", "Imani", "Oscar"]},
            {"label": "Boat", "values": ["Minnow", "Pebble", "Skipjack", "Teacup", "Puffin"],
             "ref": "the rower in the {v}",
             "pred": "took out the {v}",
             "neg": "did not take out the {v}",
             "either": "took out either the {a} or the {b}",
             "nor": "took out neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Went to", "values": ["the Point", "Gull Rock", "East Cove", "the Narrows", "Seal Ledge"],
             "ref": "the rower bound for {v}",
             "pred": "rowed to {v}",
             "neg": "did not row to {v}",
             "either": "rowed to either {a} or {b}",
             "nor": "rowed to neither {a} nor {b}",
             "short": "{v}"},
            {"label": "Time", "ordered": True,
             "nums": [810, 840, 870, 900, 930],
             "labels": ["1:30 p.m.", "2:00 p.m.", "2:30 p.m.", "3:00 p.m.", "3:30 p.m."],
             "ref": "the rower who pushed off at {x}",
             "pred": "pushed off at {x}",
             "neg": "did not push off at {x}",
             "either": "pushed off at either {a} or {b}",
             "nor": "pushed off at neither {a} nor {b}",
             "short": "{x}",
             "more": "pushed off later than {y}",
             "less": "pushed off earlier than {y}",
             "dmore": "pushed off exactly {d} after {y}",
             "dless": "pushed off exactly {d} before {y}",
             "dunit": ["minute", "minutes"],
             "dmore1": "pushed off half an hour after {y}",
             "dless1": "pushed off half an hour before {y}"},
        ],
    },
    # ------------------------------------------------------------------ 98
    {
        "slot": 98,
        "title": "The Ferry Dock Hand-Offs",
        "story": "Between five o'clock and twenty past six on Festival Eve, the ferry dock bustled with "
                 "errands, and Pilot the beagle greeted everyone in his orange life vest. Five "
                 "people were each handed something there, from a festival lantern to the spare "
                 "lighthouse key, and each went on somewhere different. Teddy says he passed the key "
                 "along on his way to the green. Ada would like the grid's word for it. Who got what, "
                 "when, and where did each go next?",
        "entity": ["person", "people"],
        "cast": ["Jonah", "Hattie", "Rosa", "Teddy"],
        "question": {"text": "Who received the spare key at the ferry dock?", "cat": "Received",
                     "value": "spare key"},
        "answer": "Jonah",
        "cats": [
            {"label": "Person", "kind": "name", "values": ["Jonah", "Hattie", "Pearl", "Rosa", "Kenji"]},
            {"label": "Received", "values": ["spare key", "lantern", "thermos", "mail sack", "pie tin"],
             "ref": "the person with the {v}",
             "pred": "was handed the {v}",
             "neg": "was not handed the {v}",
             "either": "was handed either the {a} or the {b}",
             "nor": "was handed neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Headed to", "values": ["the inn", "the bakery", "the store", "the church", "the library"],
             "ref": "the person headed to {v}",
             "pred": "went on to {v}",
             "neg": "did not go on to {v}",
             "either": "went on to either {a} or {b}",
             "nor": "went on to neither {a} nor {b}",
             "short": "{v}"},
            {"label": "Time", "ordered": True,
             "nums": [1020, 1040, 1060, 1080, 1100],
             "labels": ["5:00 p.m.", "5:20 p.m.", "5:40 p.m.", "6:00 p.m.", "6:20 p.m."],
             "ref": "the person whose hand-off came at {x}",
             "pred": "was handed something at {x}",
             "neg": "was not handed anything at {x}",
             "either": "was handed something at either {a} or {b}",
             "nor": "was handed something at neither {a} nor {b}",
             "short": "{x}",
             "more": "was handed something later than {y}",
             "less": "was handed something earlier than {y}",
             "dmore": "was handed something exactly {d} after {y}",
             "dless": "was handed something exactly {d} before {y}",
             "dunit": ["minute", "minutes"],
             "dmore1": "was handed something 20 minutes after {y}",
             "dless1": "was handed something 20 minutes before {y}"},
        ],
    },
    # ------------------------------------------------------------------ 99
    {
        "slot": 99,
        "title": "The Moonlight Dinghy",
        "story": "After dark, under a thin December moon, Felix found his own dinghy gone from its slip. "
                 "The tide was high and the causeway under water, so anyone who reached Thimble Point "
                 "that evening got there by boat, and the dinghy was the only boat missing. Five people "
                 "admit they were down by the water, each at a different spot, arriving at a different "
                 "time, by a different light. Who went where, when, and by which light?",
        "entity": ["person", "people"],
        "cast": ["Mabel", "Jonah", "Priya", "Felix"],
        "question": {"text": "Who rowed out to Thimble Point after dark?", "cat": "Spot", "value": "the Point"},
        "answer": "Jonah",
        "cats": [
            {"label": "Person", "kind": "name", "values": ["Mabel", "Jonah", "Zeke", "Priya", "Linus"]},
            {"label": "Spot", "values": ["the Point", "the pier", "the slipway", "the beach", "the seawall"],
             "ref": "the person at {v}",
             "pred": "went out to {v}",
             "neg": "did not go out to {v}",
             "either": "went out to either {a} or {b}",
             "nor": "went out to neither {a} nor {b}",
             "short": "{v}"},
            {"label": "Light", "values": ["flashlight", "headlamp", "lantern", "bike light", "penlight"],
             "ref": "the person with the {v}",
             "pred": "brought a {v}",
             "neg": "did not bring a {v}",
             "either": "brought either a {a} or a {b}",
             "nor": "brought neither a {a} nor a {b}",
             "short": "the {v}"},
            {"label": "Time", "ordered": True,
             "nums": [1140, 1160, 1180, 1200, 1220],
             "labels": ["7:00 p.m.", "7:20 p.m.", "7:40 p.m.", "8:00 p.m.", "8:20 p.m."],
             "ref": "the person who arrived at {x}",
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
             "dmore1": "arrived 20 minutes after {y}",
             "dless1": "arrived 20 minutes before {y}"},
        ],
    },
    # ------------------------------------------------------------------ 100
    {
        "slot": 100,
        "title": "The Rehearsal on the Green",
        "story": "Down on the town green, half of Thimble Harbor spent Festival Eve in winter coats, "
                 "rehearsing the Lantern Festival. Lena's own museum key never left her key ring. Five "
                 "volunteers, each with a different job, took turns at the Gazette's camera: one photo "
                 "each, every half hour from seven. The last one, at nine, shows the light at Thimble "
                 "Point going dark. Who took which photo, and who caught that last one?",
        "entity": ["volunteer", "volunteers"],
        "cast": ["Lena", "Wren", "Teddy", "Hattie"],
        "question": {"text": "Who snapped the 9 p.m. photo?", "cat": "Time", "value": "9:00 p.m."},
        "answer": "Teddy",
        "cats": [
            {"label": "Volunteer", "kind": "name", "values": ["Lena", "Gideon", "Wren", "Teddy", "Hattie"]},
            {"label": "Job", "values": ["lanterns", "choir", "cocoa", "tickets", "banners"],
             "ref": "the person in charge of the {v}",
             "pred": "was in charge of the {v}",
             "neg": "was not in charge of the {v}",
             "either": "was in charge of either the {a} or the {b}",
             "nor": "was in charge of neither the {a} nor the {b}",
             "short": "the {v}"},
            {"label": "Coat", "values": ["red", "navy", "green", "gray", "camel"],
             "ref": "the person in the {v} coat",
             "pred": "wore a {v} coat",
             "neg": "did not wear a {v} coat",
             "either": "wore either a {a} or a {b} coat",
             "nor": "wore neither a {a} nor a {b} coat",
             "short": "the {v} coat"},
            {"label": "Time", "ordered": True,
             "nums": [1140, 1170, 1200, 1230, 1260],
             "labels": ["7:00 p.m.", "7:30 p.m.", "8:00 p.m.", "8:30 p.m.", "9:00 p.m."],
             "ref": "the person who took the {x} photo",
             "pred": "took the {x} photo",
             "neg": "did not take the {x} photo",
             "either": "took either the {a} or the {b} photo",
             "nor": "took neither the {a} nor the {b} photo",
             "short": "the {x} photo",
             "more": "took a photo later than {y}",
             "less": "took a photo earlier than {y}",
             "dmore": "took a photo exactly {d} after {y}",
             "dless": "took a photo exactly {d} before {y}",
             "dunit": ["minute", "minutes"],
             "dmore1": "took a photo half an hour after {y}",
             "dless1": "took a photo half an hour before {y}"},
        ],
    },
]
