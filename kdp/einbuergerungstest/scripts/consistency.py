#!/usr/bin/env python3
"""Make BKS naming consistent across all translation batches (run before validate_content.py).

Ten translators worked in parallel; this pass unifies the few names they rendered differently.
Only BKS fields (q_bks, options_bks, expl_bks) are touched - never the German catalogue text or
the Merksätze. Every change is logged to content/consistency_log.md.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Croatian standard names (hr. Wikipedia / Hrvatski jezični portal); case forms listed explicitly.
RULES = [
    (r"Zapadna Pomeranija", "Zapadno Pomorje"), (r"Zapadne Pomeranije", "Zapadnog Pomorja"),
    (r"Zapadnoj Pomeraniji", "Zapadnom Pomorju"), (r"Zapadnu Pomeraniju", "Zapadno Pomorje"),
    (r"Zapadnom Pomeranijom", "Zapadnim Pomorjem"),
    (r"Meklenburg", "Mecklenburg"),
    (r"(?<!\()\bElba\b", "Laba"), (r"(?<!\()\bElbe\b(?!\))", "Labe"), (r"(?<!\()\bElbi\b", "Labi"),
    (r"(?<!\()\bElbu\b", "Labu"), (r"(?<!\()\bElbom\b", "Labom"),
    (r"Donja Saksonija", "Donja Saska"), (r"Donje Saksonije", "Donje Saske"), (r"Donjoj Saksoniji", "Donjoj Saskoj"),
    (r"Tiringen", "Tiringija"),
    (r"Sjeverna Rajna – Vestfalija", "Sjeverna Rajna-Vestfalija"),
    (r"Rajna-Falačka", "Porajnje-Falačka"),
]


# Item-level edits after the blind review (content/review_report.md): (id, field, old, new).
# field is "q_bks", "expl_bks" or "options_bks[i]". Idempotent: applied only while `old` is present.
MANUAL = [
    ("G-150", "q_bks", "Sudac porotnik (Gerichtsschöffe) u Njemačkoj je …", "Porotnik (Gerichtsschöffe) u Njemačkoj je …"),
    ("G-150", "expl_bks", "Sudac porotnik (Gerichtsschöffe) je građanin koji zajedno",
     "Porotnik (Gerichtsschöffe) je građanin koji kao sudac porotnik zajedno"),
    ("G-150", "expl_bks", "nego samo naknadu troškova", "nego samo naknadu za troškove i izgubljeno vrijeme"),
    ("G-268", "expl_bks", " ili na više od deset stranih jezika, među njima i na hrvatskom.", " ili na više od deset stranih jezika."),
    ("G-075", "expl_bks", "a Bodo Ramelow ministar predsjednik (Ministerpräsident) Tiringije.",
     "a Bodo Ramelow bio je ministar predsjednik (Ministerpräsident) Tiringije."),
    ("G-006", "expl_bks", "Tada je zamišljen kao privremeno rješenje", "Pri donošenju 1949. zamišljen je kao privremeno rješenje"),
    ("G-006", "options_bks[0]", "narodni zakon (Volksgesetz)", "Narodni zakon (Volksgesetz)"),
    ("G-006", "options_bks[1]", "savezni zakon (Bundesgesetz)", "Savezni zakon (Bundesgesetz)"),
    ("G-006", "options_bks[2]", "njemački zakon (Deutsches Gesetz)", "Njemački zakon (Deutsches Gesetz)"),
    ("G-011", "options_bks[1]", "savezni ustav (Bundesverfassung)", "Savezni ustav (Bundesverfassung)"),
    ("G-011", "options_bks[2]", "zakonik (Gesetzbuch)", "Zakonik (Gesetzbuch)"),
    ("G-011", "options_bks[3]", "ustavni ugovor (Verfassungsvertrag)", "Ustavni ugovor (Verfassungsvertrag)"),
    ("G-015", "expl_bks", "iznimka je samo rad u zatvoru nakon sudske odluke",
     "iznimke su rad pri lišenju slobode po odluci suda, opće javne obveze koje vrijede jednako za sve te vojna ili zamjenska služba (članak 12.a)"),
    ("G-072", "expl_bks", "Gerhard Schröder (1998.–2005.) i Angela Merkel (2005.–2021.) bili su kancelari prije njega",
     "Prije njega kancelari su bili Olaf Scholz (2021.–2025.), Angela Merkel (2005.–2021.) i Gerhard Schröder (1998.–2005.)"),
    ("G-074", "options_bks[3]", "Savezni sud (Bundesgerichtshof)", "Savezni vrhovni sud (Bundesgerichtshof)"),
    ("G-099", "expl_bks", "Dio zaposlenika odbija se automatski", "Zaposlenikov dio doprinosa odbija se automatski"),
    ("G-102", "q_bks", "socijalnom području? …", "socijalnom području?"),
    ("G-233", "q_bks", "Koja je zemlja susjedna zemlja Njemačke?", "Koja je zemlja susjed Njemačke?"),
    ("G-243", "expl_bks", "najkasnije 48 sati prije najave", "najkasnije 48 sati prije nego što se javno najavi"),
    ("G-267", "options_bks[3]", "Potražit će kćeri drugog muškarca.", "Potražit će drugog muškarca za svoju kćer."),
    ("G-271", "options_bks[1]", "okititi božićno drvce (jelu)", "okititi jelu (Tannenbaum)"),
    ("G-293", "options_bks[1]", "kititi jelku", "kititi jelu (Tannenbaum)"),
    ("G-293", "expl_bks", "jelka za Božić", "okićena jela za Božić"),
    ("G-282", "q_bks", "Koji volonterski rad (Ehrenamt) moraju", "Koju počasnu dužnost (Ehrenamt) moraju"),
    ("G-282", "options_bks[0]", "trener u udruzi", "trener u udruzi (Vereinstrainer)"),
    ("G-282", "options_bks[2]", "nadzor u knjižnici", "nadzor u knjižnici (Bibliotheksaufsicht)"),
    ("G-282", "options_bks[3]", "učitelj", "učitelj (Lehrer)"),
    ("HB-07", "q_bks", "Što je njemačka grad-pokrajina (Stadtstaat)?", "Koji je grad njemačka grad-pokrajina (Stadtstaat)?"),
    ("HH-02", "expl_bks", "Pankow okrug u Berlinu", "Pankow gradski kotar u Berlinu"),
    ("NI-08", "expl_bks", "uz Sjeverno more i Nizozemsku (oko Bremena).", "uz Sjeverno more i Nizozemsku."),
    ("SL-05", "expl_bks", "Saarland je jedina savezna pokrajina s tim bojama na zastavi.",
     "Iste boje imaju i zastave Donje Saske i Porajnja-Falačke, ali s drugim grbom."),
    ("TH-01", "expl_bks", "ali Hessenov grb nema zvjezdice", "ali grb Hessena nema zvjezdice"),
    ("G-291", "merksatz_de", "Mitglieder z. B. der katholischen oder evangelischen Kirche zahlen Kirchensteuer, das Finanzamt zieht sie ein.",
     "Katholiken und Protestanten zahlen Kirchensteuer; das Finanzamt zieht sie ein."),
    # External editorial review (2026-09-28): the ballot rule was overbroad.
    ("G-130", "expl_bks", 'Valjan je listić s točno jednim križićem u lijevom stupcu (prvi glas, kandidat) i točno jednim križićem u desnom stupcu (drugi glas, stranka). Listić s dva križića u istom stupcu ili tri križića nije valjan. Prvim glasom birate kandidata u svom izbornom okrugu, a drugim stranku. Na listić se ne smije ništa dopisivati. U katalogu je to listić broj 1.',
     'Među ponuđenim listićima potpuno je valjan samo listić broj 1: ima točno jedan križić za prvi glas (kandidat) i točno jedan za drugi glas (stranka). Na listiću 2 drugi glas ima dva križića, pa taj glas ne vrijedi; na listićima 3 i 4 previše je križića kod prvog glasa. Birač smije dati i samo jedan glas – tada ne vrijedi samo neiskorišteni glas (§ 39 BWahlG). U katalogu je to listić broj 1.'),
]

# Bezirk = "gradski kotar" everywhere ("okrug" is reserved for Landkreis).
BEZIRK = [(r"gradskog okruga", "gradskog kotara"), (r"gradskih okruga", "gradskih kotara"),
          (r"gradski okrug", "gradski kotar"), (r"Svaki okrug", "Svaki kotar")]
COLOUR = re.compile(r"\b(crn|crven|zlatn|plav|bijel|žut|zelen|narančast|smeđ|siv)a\b")


def generic(t, q, log):
    """Rules derived from the review that apply to whole groups of items."""
    qid = t["id"]
    if qid.endswith("-05"):  # flag colours: "crno-crveno-zlatno" (HR standard compound form)
        new = [COLOUR.sub(r"\1o", o) for o in t["options_bks"]]
        if new != t["options_bks"]:
            log.append(f"- `{qid}` options: colour compounds → -o forms"); t["options_bks"] = new
    if t["q_bks"].startswith("Kojeg ministra") or t["q_bks"].startswith("Kojeg senatora"):  # genitive
        new = [re.sub(r"^ministar ", "ministra ", re.sub(r"^senator ", "senatora ", o)) for o in t["options_bks"]]
        if new != t["options_bks"]:
            log.append(f"- `{qid}` options: genitive after 'Kojeg …'"); t["options_bks"] = new
    for pat, rep in BEZIRK:
        for field in ("q_bks", "expl_bks"):
            if re.search(pat, t[field]):
                t[field] = re.sub(pat, rep, t[field]); log.append(f"- `{qid}` {field}: {pat} → {rep}")
    # Picture questions: name the correct picture/number so readers can match the BAMF images.
    if q["images"] and all(re.fullmatch(r"(Bild )?\d", o) for o in q["options"]):
        n = re.sub(r"\D", "", q["options"][q["answer"]])
        if qid.endswith("-08"):
            tail = f" Na karti u katalogu to je broj {n}."
        elif qid == "G-130":
            tail = f" U katalogu je to listić broj {n}."
        else:
            tail = f" U katalogu je to slika {n}."
        if tail.strip() not in t["expl_bks"]:
            t["expl_bks"] = t["expl_bks"].rstrip() + tail; log.append(f"- `{qid}` expl_bks: + '{tail.strip()}'")


def fix(s, log, qid, field):
    for pat, rep in RULES:
        new = re.sub(pat, rep, s)
        if new != s:
            log.append(f"- `{qid}` {field}: `{pat}` → `{rep}`")
            s = new
    return s


def precision_fixes():
    """Fixes proposed by the precision review (content/review2/precision_*_result.json),
    after editorial acceptance; rejected ones are listed in content/review2/rejected.json."""
    rejected = set()
    rej = ROOT / "content" / "review2" / "rejected.json"
    if rej.exists():
        rejected = {(r["id"], r["old"]) for r in json.load(open(rej, encoding="utf-8"))}
    out = []
    for f in sorted((ROOT / "content" / "review2").glob("precision_*_result.json")):
        for r in json.load(open(f, encoding="utf-8")):
            if (r["id"], r["old"]) not in rejected:
                out.append((r["id"], r["field"], r["old"], r["new"]))
    return out


def main():
    log = []
    edits = MANUAL + precision_fixes()
    cat = {q["id"]: q for q in json.load(open(ROOT / "data" / "catalog.json", encoding="utf-8"))["questions"]}
    for f in sorted((ROOT / "content" / "batches").glob("batch_*_output.json")):
        items = json.load(open(f, encoding="utf-8"))
        for t in items:
            for mid, field, old, new in edits:
                if t["id"] != mid:
                    continue
                m = re.fullmatch(r"options_bks\[(\d)\]", field)
                cur = t["options_bks"][int(m.group(1))] if m else t[field]
                if old in cur and new not in cur:
                    cur = cur.replace(old, new)
                    if m:
                        t["options_bks"][int(m.group(1))] = cur
                    else:
                        t[field] = cur
                    log.append(f"- `{mid}` {field}: manual edit → „{new}”")
            t["q_bks"] = fix(t["q_bks"], log, t["id"], "q_bks")
            t["expl_bks"] = fix(t["expl_bks"], log, t["id"], "expl_bks")
            t["options_bks"] = [fix(o, log, t["id"], "option") for o in t["options_bks"]]
            generic(t, cat[t["id"]], log)
        f.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    logf = ROOT / "content" / "consistency_log.md"
    prev = logf.read_text(encoding="utf-8") if logf.exists() else "# Consistency pass (appended per run)\n"
    logf.write_text(prev + f"\n## Run: {len(log)} changes\n" + "\n".join(log) + "\n", encoding="utf-8")
    print(f"{len(log)} changes")


if __name__ == "__main__":
    main()
