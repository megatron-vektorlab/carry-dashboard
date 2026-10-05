"""Recurring cast and one-off name pool for "Cozy Mystery Logic Puzzles for Beginners".

See story/bible.md for the full story bible. Ada Quill (the mentor) and the
reader (her apprentice) are never suspects and never grid names. Pets
(Inkwell the Gazette cat, Pilot the ferry dog) never appear as grid names.

Jonah's "secret" field is for writers only: his surname, his family line and
his ferry's name never appear in any puzzle story or Ada intro; they are
revealed only in the bonus solution and the epilogue.

Every name is 3-7 letters. The twelve cast names all start with different
letters. No pool name repeats or closely resembles a cast name or another
pool name.
"""

CAST = [
    {"name": "Hattie", "role": "church hall coordinator (Hattie Pruitt), runs every supper, social and rummage sale",
     "quirk": "carries a clipboard with a list of her other lists"},
    {"name": "Rosa", "role": "baker at the Salt & Sugar Bakery (Rosa Delgado)",
     "quirk": "gives each of her sourdough starters a name and a birthday"},
    {"name": "Otis", "role": "harbormaster (Otis Lund), keeps the spare lighthouse key on a hook in the harbor office",
     "quirk": "whistles sea shanties, always slightly off-key"},
    {"name": "Wren", "role": "town librarian (Wren Takahashi)",
     "quirk": "whispers even outdoors; remembers everyone by their overdue books"},
    {"name": "Felix", "role": "boatbuilder, owner of Okafor Boatyard (Felix Okafor)",
     "quirk": "keeps a pencil behind each ear and calls everything 'shipshape'"},
    {"name": "Gus", "role": "owner of Mahoney's General Store (Gus Mahoney)",
     "quirk": "forecasts the weather by his left knee, and is usually right"},
    {"name": "Priya", "role": "innkeeper of the Gull's Rest Inn (Priya Nair)",
     "quirk": "keeps a lost-and-found of forty-one umbrellas and returns every one"},
    {"name": "Jonah", "role": "ferry captain of the Thimble Harbor ferry",
     "quirk": "on time to the minute; tinkers with old brass in his ferry workshop",
     "secret": "surname Bell; great-grandson of Silas Bell, the last lighthouse keeper; his ferry is the "
               "Silas B. Never in any puzzle story (chapters 1-7); revealed only in the bonus solution and epilogue"},
    {"name": "Mabel", "role": "retired schoolteacher and garden club president (Mabel Fitch)",
     "quirk": "corrects grammar on signs; locked in a friendly dahlia rivalry"},
    {"name": "Teddy", "role": "the Gazette's 19-year-old photographer and bicycle paperboy (Teddy Sousa)",
     "quirk": "never without his camera; working on a '150 Years of Light' photo series"},
    {"name": "Lena", "role": "curator of the Historical Society and the lighthouse museum (Lena Kowalski)",
     "quirk": "wears white cotton gloves to touch anything older than she is"},
    {"name": "Nico", "role": "lobsterman, skipper of the lobster boat Persistence (Nico Papas)",
     "quirk": "tells tall tales; the lobster gets bigger every time"},
]

NAME_POOL = [
    "Amara", "Arlo", "Basil", "Bea", "Boris", "Carmen", "Cass", "Cyrus", "Della",
    "Dev", "Dot", "Elsa", "Emil", "Enzo", "Faye", "Gideon", "Greta", "Hal",
    "Hugo", "Imani", "Ivan", "Jade", "Kenji", "Kit", "Linus", "Lou", "Marta",
    "Milo", "Nadia", "Olive", "Oscar", "Pablo", "Pearl", "Quinn", "Ruben", "Sam",
    "Selma", "Tariq", "Tova", "Una", "Vera", "Vito", "Walt", "Yusuf", "Zeke",
]

PETS = [
    {"name": "Inkwell", "kind": "gray office cat at the Gazette", "note": "sleeps on puzzle proofs; never a grid name"},
    {"name": "Pilot", "kind": "Jonah's old beagle", "note": "rides the ferry in a life vest; never a grid name"},
]

assert len(CAST) == 12 and len({c["name"][0] for c in CAST}) == 12
assert len(NAME_POOL) == 45 and len(set(NAME_POOL)) == 45
assert all(3 <= len(x) <= 7 for x in NAME_POOL + [c["name"] for c in CAST])
assert not set(NAME_POOL) & {c["name"] for c in CAST}
