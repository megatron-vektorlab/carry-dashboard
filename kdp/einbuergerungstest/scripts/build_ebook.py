#!/usr/bin/env python3
"""Kindle eBook (reflowable EPUB 3) from the same data as the paperback.

Usage: build_ebook.py
Outputs: out/ebook_de-bks.epub, out/ebook_cover_de-bks.jpg (1600 x 2560), out/ebook_info.json

What changes against print (an eBook is read on a phone or a Kindle, not written in):
  * every question number in the indexes, the timeline, the test solutions and the word list is
    a link to the question; "back" on the reader returns;
  * the correct answer is set in bold and marked "richtig / točno";
  * the practice tests keep the exam form (German only, no marked answers), each with a link to
    its solutions; answers are noted on paper or with the reader's note function, so the answer
    sheets and the mistakes table of the print book are left out;
  * page references become links; the QR code becomes a link to the BAMF catalogue;
  * the "Who is who" chart is a picture, everything else is text.
"""
import json
import re
import sys
from pathlib import Path

import typst
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_book import assemble, N_TESTS  # noqa: E402
from epubkit import Book, Doc, esc, check  # noqa: E402

CHUNK = 50          # general questions per file (Kindle prefers files well below 300 KB)
OK_TAG = "richtig · točno"

CSS = """
body { margin: 0 0.2em; }
h1 { font-size: 1.45em; line-height: 1.2; margin: 0.8em 0 0.5em; page-break-before: always; }
h2 { font-size: 1.2em; line-height: 1.25; margin: 1.3em 0 0.45em; page-break-after: avoid; }
h3 { font-size: 1.05em; margin: 1em 0 0.35em; page-break-after: avoid; }
p { margin: 0.3em 0; text-indent: 0; }
.sub { font-style: italic; margin-top: -0.2em; }
.center { text-align: center; }
.title-page h1 { page-break-before: avoid; font-size: 1.7em; margin-top: 2em; text-align: center; }
.title-page p { text-align: center; margin: 0.6em 0; }
.small { font-size: 0.85em; }
.imprint p { font-size: 0.85em; margin: 0.5em 0; }
.toc p { margin: 0.35em 0; }
.toc .l2 { margin-left: 1.2em; }
.q { margin: 1.5em 0 0.4em; page-break-inside: avoid; }
.qh { margin-bottom: 0.15em; }
.qn { font-weight: bold; border: 1px solid #000; padding: 0 0.3em; }
.tr { font-style: italic; color: #333333; }
.opt { margin: 0.4em 0 0.4em 1.7em; text-indent: -1.7em; }
.ok { font-weight: bold; }
.ok-tag { font-size: 0.75em; font-weight: bold; border: 1px solid #000; padding: 0 0.25em; white-space: nowrap; }
.ex { margin: 0.55em 0 0.2em 1.7em; padding: 0.35em 0.6em; border-left: 3px solid #666666; background-color: #eeeeee; }
.ex p { font-size: 0.95em; }
.pic { text-align: center; margin: 0.5em 0; }
.pic img { width: 60%; }
.pic img.wide { width: 95%; }
.pic img.narrow { width: 40%; }
.pics4 { text-align: center; margin: 0.5em 0; }
.pic4 { display: inline-block; width: 44%; margin: 0.3em 2%; text-align: center; font-size: 0.85em; }
.pic4 img { width: 85%; }
.photo { font-size: 0.9em; border: 1px solid #888888; padding: 0.3em 0.5em; margin: 0.4em 0 0.4em 1.7em; }
.note { border: 1px solid #000; padding: 0.4em 0.6em; margin: 0.8em 0; }
.nums { font-size: 0.9em; }
.entry { margin: 0.7em 0; }
.sol { margin: 0.25em 0; }
table { border-collapse: collapse; margin: 0.5em 0; }
td, th { border: 1px solid #888888; padding: 0.15em 0.4em; vertical-align: top; text-align: left; }
.cover { text-align: center; margin: 0; padding: 0; }
.cover img { height: 100%; max-width: 100%; }
img { max-width: 100%; }
"""


def link_nums(nums, href_of, sep=", "):
    return sep.join(f'<a href="{href_of(n)}">{n}</a>' for n in nums)


def main():
    data, missing, missing_release, use_images, questions = assemble()
    if missing:
        sys.exit(f"{len(missing)} questions without translation")
    M, R = data["meta"], data["meta"]["release"]
    build = ROOT / "build" / "ebook"
    build.mkdir(parents=True, exist_ok=True)
    out = ROOT / "out"
    out.mkdir(exist_ok=True)

    verified = R.get("catalog_verified") is True
    stand = f"Stand {R['catalog_stand']}" if verified else f"Datenstand {R['public_copy_retrieved']}"
    proof = R.get("human_proofread")
    proof_de = f"{R['human_proofread_by']}, {R['human_proofread_date']}" if proof is True else "nicht erfolgt"
    proof_hr = f"{R['human_proofread_by']}, {R['human_proofread_date']}" if proof is True else "nije provedena"

    # ---- cover and chart ------------------------------------------------------------------
    (ROOT / "build" / "ebook_cover_params.json").write_text(json.dumps(
        dict(author=R["author"], stand=stand, draft=M["draft"])))
    png = build / "cover.png"
    typst.compile(str(ROOT / "layout" / "ebook_cover.typ"), output=str(png), root=str(ROOT), format="png", ppi=320,
                  font_paths=[str(ROOT / "layout" / "fonts")])
    cover = out / "ebook_cover_de-bks.jpg"
    Image.open(png).convert("RGB").save(cover, quality=92)
    chart = build / "staat.png"
    typst.compile(str(ROOT / "layout" / "ebook_diagram.typ"), output=str(chart), root=str(ROOT), format="png", ppi=220,
                  font_paths=[str(ROOT / "layout" / "fonts")])
    imgdir = build / "img"
    imgdir.mkdir(exist_ok=True)

    def small_png(src, longest=1400):
        """16-grey PNG at most `longest` px: a smaller file lowers Amazon's per-MB delivery cost
        (the pictures are greyscale line art, so 16 levels look the same on a Kindle screen)."""
        dst = imgdir / src.name
        im = Image.open(src)
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGBA", im.size, "white")
            im = Image.alpha_composite(bg, im)
        im = im.convert("L")
        if max(im.size) > longest:
            k = longest / max(im.size)
            im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        im.quantize(16, dither=Image.Dither.NONE).save(dst, optimize=True, bits=4)
        return dst

    images = {"images/staat.png": small_png(chart)}

    # ---- where every question lives -------------------------------------------------------
    where = {}
    for k in range(0, 300, CHUNK):
        for q in data["general"][k:k + CHUNK]:
            where[q["id"]] = f"teil1-{k // CHUNK + 1}.xhtml"
    for s in data["states"]:
        for q in s["questions"]:
            where[q["id"]] = f"land-{s['code']}.xhtml"

    def qhref(qid):
        return f"{where[qid]}#q-{qid}"

    def gen(num):
        return qhref(f"G-{num:03d}")

    def pictures(q, small=False):
        if not q.get("images"):
            return ""
        files = [f.split("/")[-1] for f in q["images"]["files"]]
        for f in files:
            images[f"images/{f}"] = small_png(ROOT / "layout" / "images" / f)
        if q["images"]["layout"] == "row":
            cells = "".join(f'<span class="pic4"><img src="images/{f}" alt="Bild {i + 1}"/><br/>Bild {i + 1}</span>'
                            for i, f in enumerate(files))
            return f'<p class="pics4">{cells}</p>'
        cls = "wide" if q["id"] == "G-130" else "narrow" if q["id"] == "G-176" or small else ""
        cls = f' class="{cls}"' if cls else ""
        return f'<p class="pic"><img{cls} src="images/{files[0]}" alt="Bild zur Frage {esc(q["label"])}"/></p>'

    def photo_note(q):
        if not q.get("photo_missing"):
            return ""
        return (f'<p class="photo" lang="hr"><b>Fotografija nije uvrštena</b> (autorska prava treće strane). '
                f'Pogledajte je u <a href="{M["catalogue_url"]}">BAMF-ovu katalogu</a>, pitanje {q["num"]}.</p>')

    def question(q):
        h = [f'<div class="q" id="q-{q["id"]}">',
             f'<p class="qh"><span class="qn">{esc(q["label"])}</span> <b>{esc(q["q_de"])}</b></p>',
             f'<p class="tr" lang="hr">{esc(q["q_bks"])}</p>', pictures(q), photo_note(q)]
        for o in q["options"]:
            de = f'<b>{esc(o["de"])}</b> <span class="ok-tag">{OK_TAG}</span>' if o["correct"] else esc(o["de"])
            tr = f'<br/><span class="tr" lang="hr">{esc(o["bks"])}</span>' if o["bks"] else ""
            h.append(f'<p class="opt{" ok" if o["correct"] else ""}"><b>{o["letter"]}</b>&#160;&#160;{de}{tr}</p>')
        h.append(f'<div class="ex"><p lang="hr"><b>Objašnjenje:</b> {esc(q["expl"])}</p>'
                 f'<p><b>Merksatz:</b> <i>{esc(q["merksatz"])}</i></p></div></div>')
        return "\n".join(x for x in h if x)

    def exam_question(no, q, anchor=None):
        aid = f' id="{anchor}"' if anchor else ""
        h = [f'<div class="q"{aid}>',
             f'<p class="qh"><b>{no}.</b> <b>{esc(q["q_de"])}</b> <span class="small">(Nr. {esc(q["label"])})</span></p>',
             pictures(q, small=True)]
        if q.get("photo_missing"):
            h.append(f'<p class="photo" lang="hr">Fotografija nije uvrštena: pogledajte je u '
                     f'<a href="{M["catalogue_url"]}">BAMF-ovu katalogu</a>, pitanje {q["num"]}.</p>')
        for o in q["options"]:
            h.append(f'<p class="opt"><b>{o["letter"]}</b>&#160;&#160;{esc(o["de"])}</p>')
        h.append("</div>")
        return "\n".join(x for x in h if x)

    docs = []

    # ---- title, imprint, contents -----------------------------------------------------------
    docs.append(Doc("titel", "Titel", lang="de", toc=False, landmark="titlepage", body_class="title-page", body=f"""
<h1>Einbürgerungstest<br/>&amp; Leben in Deutschland</h1>
<p><b>Deutsch – Bosnisch/Kroatisch/Serbisch</b></p>
<p>Alle 460 Fragen des BAMF-Fragenkatalogs (300 allgemeine Fragen + 10 Fragen je Bundesland) mit Übersetzung,
Erklärungen, Merksätzen und 10 vollständigen Probetests</p>
<p lang="hr"><i>Razumijte svako pitanje na svom jeziku: sva pitanja s prijevodom, objašnjenjima i 10 potpunih probnih testova</i></p>
<p><b>{esc(R['author'])}</b></p>
<p class="small">{esc(R['edition'])} · E-Book · {esc(R['edition_date'])}<br/>Fragenkatalog: {esc(stand)}</p>"""))

    katalog = (f"Stand des Katalogs: {esc(R['catalog_stand'])}; mit dem offiziellen BAMF-PDF abgeglichen am {esc(R['catalog_compared_on'])}."
               if verified else
               f"Datenstand: öffentliche Kopie des Katalogs vom {esc(R['public_copy_retrieved'])} (aus dem offiziellen BAMF-PDF erstellt), "
               "abgeglichen mit zwei weiteren unabhängigen Kopien. Ein eigener Abgleich mit dem offiziellen BAMF-PDF ist nicht erfolgt.")
    docs.append(Doc("impressum", "Impressum", lang="de", toc=False, landmark="copyright-page", body_class="imprint", body=f"""
<h2>Impressum</h2>
<p><b>Hinweis:</b> Dieses Buch ist keine Veröffentlichung des Bundesamts für Migration und Flüchtlinge (BAMF) und steht in keiner Verbindung zum BAMF.</p>
<p><b>Ausgabe:</b> {esc(R['edition'])}, E-Book, {esc(R['edition_date'])}.</p>
<p><b>Fragen und Antworten:</b> {esc(M['catalog_source'])}. Die Fragen, Antwortmöglichkeiten und richtigen Antworten sind unverändert wiedergegeben (§ 5 Abs. 2 UrhG); Schreibweise nur typografisch angepasst. {katalog} Maßgeblich ist allein der aktuelle Katalog des BAMF.</p>
<p><b>Abbildungen:</b> Wappen, Karten, Stimmzettel und Flaggen stammen aus dem Fragenkatalog des BAMF (Graustufen). Sie werden nur als Gegenstand der Prüfungsfragen gezeigt. Ein Foto Dritter (Frage 55) ist nicht enthalten.</p>
<p><b>Übersetzungen, Erklärungen und Merksätze:</b> mit Unterstützung durch künstliche Intelligenz erstellt; automatisch und durch unabhängige KI-Gegenprüfungen kontrolliert. Menschliches Lektorat: {proof_de}.</p>
<p>Alle Angaben ohne Gewähr. Das Buch ersetzt keine Beratung durch die Einbürgerungsbehörde.</p>
<p>© 2026 {esc(R['author'])} (Übersetzungen, Erklärungen, Merksätze, Gestaltung). Alle Rechte vorbehalten.<br/>
Herausgeber (Selbstverlag) und Verantwortlicher: {esc(R['publisher'])}, {esc(R['address'])}, {esc(R['email'])}</p>"""))

    # ---- introduction (BKS) ----------------------------------------------------------------
    cat_row = (f"{esc(R['catalog_stand'])} (datum otisnut na BAMF-ovu PDF-u)" if verified
               else f"podaci javne kopije BAMF-ova kataloga od {esc(R['public_copy_retrieved'])} (izrađene iz službenog PDF-a)")
    cmp_row = esc(R['catalog_compared_on']) if verified else "izdavač je nije proveo – prije ispita usporedite pitanja na www.bamf.de"
    docs.append(Doc("uvod", "Uvod", lang="hr", landmark="bodymatter", body=f"""
<h1>Uvod</h1>
<h2>O testu</h2>
<p>Test <b>„Leben in Deutschland”</b> (Život u Njemačkoj, LiD) polaže se na kraju integracijskog tečaja, a <b>Einbürgerungstest</b> (test naturalizacije) prije stjecanja njemačkog državljanstva. Oba testa koriste <b>isti katalog od 310 pitanja</b>: 300 općih pitanja i 10 pitanja o saveznoj pokrajini u kojoj živite. Ova knjiga sadrži cijeli katalog: 300 općih pitanja i pitanja za <b>svih 16 pokrajina</b>.</p>
<ul>
<li>Test ima <b>33 pitanja</b>: 30 općih i 3 o Vašoj pokrajini. Imate <b>60 minuta</b>.</li>
<li>Za svako pitanje ponuđena su 4 odgovora; točan je uvijek samo jedan.</li>
<li><b>Koliko točnih odgovora trebate:</b> <b>17 od 33</b> – dokaz znanja za <b>naturalizaciju</b> (Einbürgerungstest ili LiD sa 17 točnih); <b>15 od 33</b> – položen test <b>LiD na kraju orijentacijskog tečaja</b>.</li>
<li>Test se polaže <b>na njemačkom jeziku</b>. Zato u ovoj knjizi njemački tekst uvijek stoji prvi.</li>
<li>Pristojba za Einbürgerungstest iznosi 25 €. Prijavljujete se u ispitnom centru, npr. u pučkom učilištu (Volkshochschule). Neke osobe su oslobođene testa (npr. nakon završene njemačke škole) – to provjerite u svom uredu za naturalizaciju.</li>
</ul>
<h2>Kako koristiti ovu e-knjigu</h2>
<ul>
<li><b>Masno:</b> pitanje na njemačkom, točno kako je u katalogu. Ispod njega, u <i>kurzivu</i>: prijevod.</li>
<li>Četiri odgovora označena su s A–D. Točan odgovor je <b>masno otisnut</b> i označen s „{OK_TAG}”. Ispod svakog odgovora je prijevod.</li>
<li><b>Objašnjenje</b> kaže zašto je odgovor točan – razumijevanje se pamti bolje od napamet naučenih slova.</li>
<li><b>Merksatz</b> je kratka njemačka rečenica za pamćenje. Pročitajte je naglas.</li>
<li><b>Brojevi pitanja su poveznice:</b> u kazalima, na vremenskoj crti i u rješenjima testova dodirnite broj i otvorit će se pitanje. Funkcijom „natrag” svog čitača vraćate se na mjesto s kojeg ste došli.</li>
<li><b>Pogreške:</b> pitanje na kojem pogriješite označite (na Kindleu: dugi dodir na tekst → označi ili dodaj bilješku) i ponovite ga nakon 1, 3 i 7 dana. Sva označena mjesta nalaze se u izborniku bilješki.</li>
</ul>
<p>Prije učenja pogledajte poglavlja <a href="prije.xhtml#pokrajina">Moja pokrajina</a>, <a href="prije.xhtml#plan">Plan učenja</a>, <a href="prije.xhtml#rijec">Pazi na riječ</a>, <a href="prije.xhtml#tko">Tko je tko u državi</a> i <a href="prije.xhtml#crta">Vremenska crta</a>. Na kraju su <a href="teil3.xhtml">10 potpunih probnih testova</a> s rješenjima, <a href="register.xhtml">tematsko kazalo</a> i <a href="glossar.xhtml">pojmovnik</a>.</p>
<h2>Aktualnost i provjera sadržaja</h2>
<table>
<tr><th>Izdanje knjige</th><td>{esc(R['edition'])}, e-knjiga, {esc(R['edition_date'])}</td></tr>
<tr><th>Stanje kataloga</th><td>{cat_row}</td></tr>
<tr><th>Usporedba sa službenim PDF-om</th><td>{cmp_row}</td></tr>
<tr><th>Podloga</th><td>javna kopija BAMF-ova kataloga preuzeta {esc(R['public_copy_retrieved'])}, uspoređena s još dvije neovisne kopije; ključ odgovora potvrđen za svih 460 pitanja</td></tr>
<tr><th>Provjere prijevoda i objašnjenja</th><td>automatska provjera; neovisne provjere drugim AI modelima (slijepo rješavanje bez ključa, provjera preciznosti); ljudska lektura: {proof_hr}</td></tr>
</table>
<p>Katalog se povremeno mijenja (npr. pitanja o aktualnim dužnosnicima). Prije ispita usporedite pitanja na www.bamf.de.</p>
<h2>Slikovna pitanja</h2>
<p>Grbovi, karte, glasački listići i zastave preuzeti su iz službenog kataloga, u sivim tonovima. U ispitu su u boji – boje su opisane u objašnjenjima. <b>Jedna fotografija (pitanje 55)</b> zaštićena je autorskim pravom treće strane i nije uvrštena: pogledajte je u <a href="{M['catalogue_url']}">BAMF-ovu katalogu</a> pod brojem 55.</p>
<h2>Napomene</h2>
<ul>
<li><b>Prijevod:</b> radi čitljivosti za osobe koristimo muški rod, koji se odnosi na oba spola. Nazivi njemačkih institucija ostaju na njemačkom, s objašnjenjem u zagradi. Tekst je pisan ijekavicom i latinicom.</li>
<li><b>Brojevi pitanja</b> odgovaraju brojevima u BAMF-ovu katalogu, pa pitanja lako pronađete i u aplikacijama.</li>
</ul>
<h2 lang="de">Vorwort (Deutsch)</h2>
<p lang="de">Dieses Buch enthält alle 460 Fragen des Gesamtfragenkatalogs zum Test „Leben in Deutschland“ und zum Einbürgerungstest. Zu jeder Frage finden Sie die Übersetzung ins Bosnische/Kroatische/Serbische, die richtige Antwort, eine kurze Erklärung und einen Merksatz auf Deutsch. Am Ende stehen 10 vollständige Probetests (30 allgemeine + 3 Landesfragen) mit Lösungen. Viel Erfolg!</p>"""))

    # ---- before you start ------------------------------------------------------------------
    states_list = "".join(f'<li><a href="land-{s["code"]}.xhtml">{esc(s["name"])}</a> · {esc(s["bks_name"])}</li>'
                          for s in data["states"])
    pattern = "".join(f"<li>{esc(p)}</li>" for p in data["state_pattern"])
    plan14 = [(f"{i + 1}.", f'{30 * i + 1}–{30 * i + 30}', "pogreške od jučer") for i in range(10)] + [
        ("11.", "pitanja moje pokrajine", "Probetest 1, 2"), ("12.", "–", "Probetest 3, 4, 5"),
        ("13.", "–", "Probetest 6, 7, 8"), ("14.", "–", "Probetest 9, 10 + označena pitanja")]
    plan30 = [(f"{i + 1}.", f'{15 * i + 1}–{15 * i + 15}', "pogreške") for i in range(20)] + [
        ("21.", "moja pokrajina", "pogreške")] + [(f"{22 + i}.", "–", f"Probetest {i + 1}") for i in range(8)] + [
        ("30.", "–", "Probetest 9, 10")]

    def table(rows):
        head = "<tr><th>Dan</th><th>Nova pitanja</th><th>Ponavljanje · test</th></tr>"
        return "<table>" + head + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows) + "</table>"

    words = "".join(f'<div class="entry"><p><b lang="de">{esc(w["de"])}</b> – {esc(w["bks"])}</p>'
                    f'<p class="nums">Pitanja: {link_nums(w["nums"], gen)}</p></div>' for w in data["words"])
    insts = "".join(f'<div class="entry"><p><b lang="de">{esc(i["name"])}</b> – {esc(i["bks"])}</p>'
                    f'<p>{esc(i["does"])}. <i>Bira:</i> {esc(i["who"])}.</p>'
                    f'<p class="nums">Pitanja: {link_nums(i["nums"], gen)}</p></div>' for i in data["institutions"])
    timeline = "".join(f'<div class="entry"><p><b>{esc(e["year"])}</b> {esc(e["text"])}</p>'
                       f'<p class="nums">Pitanja: {link_nums(e["nums"], gen)}</p></div>' for e in data["timeline"])
    docs.append(Doc("prije", "Prije početka", lang="hr", children=[
        ("Moja pokrajina", "prije.xhtml#pokrajina"), ("Plan učenja", "prije.xhtml#plan"),
        ("Pazi na riječ", "prije.xhtml#rijec"), ("Tko je tko u njemačkoj državi", "prije.xhtml#tko"),
        ("Vremenska crta", "prije.xhtml#crta")], body=f"""
<h1>Prije početka</h1>
<h2 id="pokrajina">Moja pokrajina</h2>
<p>Na ispitu dobivate 3 pitanja o pokrajini u kojoj živite. Otvorite svoju pokrajinu i učite samo njezinih 10 pitanja.</p>
<ul>{states_list}</ul>
<p>U svim pokrajinama pitanja slijede isti raspored:</p>
<ol>{pattern}</ol>
<h2 id="plan">Plan učenja</h2>
<p>Učite po planu i svaki dan ponovite pitanja na kojima ste pogriješili. Brojevi su brojevi općih pitanja.</p>
<h3>Plan za 14 dana</h3>
{table(plan14)}
<h3>Plan za 30 dana</h3>
{table(plan30)}
<p>Svako pogrešno pitanje označite u čitaču i ponovite ga nakon 1, 3 i 7 dana.</p>
<h2 id="rijec">Pazi na riječ</h2>
<p>Neke male riječi potpuno mijenjaju smisao pitanja. Brojevi su pitanja u kojima se riječ pojavljuje.</p>
{words}
<h2 id="tko">Tko je tko u njemačkoj državi</h2>
<p class="pic"><img class="wide" src="images/staat.png" alt="Shema: birači biraju Bundestag i Landtag; Bundestag bira kancelara; Bundesrat, Bundesversammlung, Bundespräsident i Bundesverfassungsgericht"/></p>
{insts}
<h2 id="crta">Vremenska crta</h2>
{timeline}"""))

    # ---- part 1 and 2: all questions with answers ----------------------------------------------
    chunks = []
    for k in range(0, 300, CHUNK):
        qs = data["general"][k:k + CHUNK]
        n = k // CHUNK + 1
        head = (f'<h1 lang="de">Teil 1: 300 allgemeine Fragen</h1><p class="sub" lang="hr">Dio 1: 300 općih pitanja</p>' if n == 1 else "")
        title = f"Fragen {qs[0]['num']}–{qs[-1]['num']}"
        chunks.append((title, f"teil1-{n}.xhtml"))
        docs.append(Doc(f"teil1-{n}", title, lang="de", toc=False,
                        body=head + f"<h2>{title}</h2>\n" + "\n".join(question(q) for q in qs)))
    # the part-1 entry in the contents points at its first file
    docs.insert(len(docs) - len(chunks), Doc("teil1", "Teil 1: 300 allgemeine Fragen", lang="de", children=chunks, body=(
        '<h1>Teil 1: 300 allgemeine Fragen</h1><p class="sub" lang="hr">Dio 1: 300 općih pitanja</p>'
        + "".join(f'<p><a href="{h}">{t}</a></p>' for t, h in chunks))))
    states_children = [(s["name"], f"land-{s['code']}.xhtml") for s in data["states"]]
    docs.append(Doc("teil2", "Teil 2: Fragen zu den Bundesländern", lang="de", children=states_children, body=(
        '<h1>Teil 2: Fragen zu den Bundesländern</h1><p class="sub" lang="hr">Dio 2: Pitanja o saveznim pokrajinama</p>'
        '<p lang="hr">Na ispitu dobivate 3 pitanja o pokrajini u kojoj živite. Naučite 10 pitanja svoje pokrajine – ostale možete preskočiti.</p>'
        + "".join(f'<p><a href="{h}">{esc(t)}</a></p>' for t, h in states_children))))
    for s in data["states"]:
        docs.append(Doc(f"land-{s['code']}", s["name"], lang="de", toc=False, body=(
            f'<h1>{esc(s["name"])}</h1><p class="sub" lang="hr">{esc(s["bks_name"])}</p>'
            + "\n".join(question(q) for q in s["questions"]))))

    # ---- part 3: practice tests -------------------------------------------------------------------
    test_children = [(f"Probetest {t['n']}", f"test-{t['n']}.xhtml") for t in data["tests"]]
    test_children += [("Anhang A: Landesfragen ohne Lösungen", "anhang-a.xhtml"), ("Lösungen", "loesungen.xhtml")]
    docs.append(Doc("teil3", "Teil 3: 10 Probetests", lang="hr", children=test_children, body=f"""
<h1 lang="de">Teil 3: 10 Probetests</h1>
<p class="sub">Dio 3: 10 potpunih probnih testova</p>
<p>Svaki probni test izgleda kao pravi ispit: <b>33 pitanja, 60 minuta</b>, samo na njemačkom.</p>
<ol>
<li>Pitanja <b>1–30</b> su opća pitanja (zajedno 10 testova pokrivaju svih 300 općih pitanja).</li>
<li>Pitanja <b>31–33</b> uzmite iz <a href="anhang-a.xhtml">Dodatka A</a> (pitanja o pokrajinama bez označenih odgovora): za svaki test naveden je koja tri pitanja Vaše pokrajine rješavate.</li>
<li>Odgovore zapišite na papir (brojevi 1–33 i slova) – tako test možete ponoviti.</li>
<li>Izmjerite vrijeme. Zatim provjerite <a href="loesungen.xhtml">rješenja</a>: svako rješenje vodi na pitanje s objašnjenjem.</li>
</ol>
<p class="note"><b>Rezultat:</b> <b>17 ili više točnih</b> – ispunjen je uvjet znanja za naturalizaciju. <b>15 ili više</b> – položen je test LiD na kraju orijentacijskog tečaja. <b>Pitanje 55</b> prikazuje fotografiju koja nije uvrštena – prije testa je pogledajte u <a href="{M['catalogue_url']}">BAMF-ovu katalogu</a>.</p>
""" + "".join(f'<p><a href="{h}">{esc(t)}</a></p>' for t, h in test_children)))
    for t in data["tests"]:
        nums = ", ".join(str(n) for n in t["state_nums"])
        body = [f'<h1>Probetest {t["n"]}</h1>']
        body += [exam_question(i + 1, q) for i, q in enumerate(t["questions"])]
        body.append(f'<p class="note"><b>Fragen 31–33:</b> Aus <a href="anhang-a.xhtml">Anhang A</a> die Fragen <b>{nums}</b> Ihres Bundeslandes lösen.<br/>'
                    f'<i lang="hr">Pitanja 31–33: iz Dodatka A riješite pitanja <b>{nums}</b> svoje pokrajine.</i></p>')
        body.append(f'<p><a href="loesungen.xhtml#t{t["n"]}"><b>→ Lösungen zu Probetest {t["n"]}</b></a> <span lang="hr">· rješenja</span></p>')
        docs.append(Doc(f"test-{t['n']}", f"Probetest {t['n']}", lang="de", toc=False, body="\n".join(body)))
    app = ['<h1>Anhang A: Landesfragen ohne Lösungen</h1>',
           '<p class="sub" lang="hr">Dodatak A: pitanja o pokrajinama za probne testove (bez rješenja)</p>',
           "<p>" + " · ".join(f'<a href="#a-{s["code"]}">{esc(s["name"])}</a>' for s in data["state_appendix"]) + "</p>"]
    for s in data["state_appendix"]:
        app.append(f'<h2 id="a-{s["code"]}">{esc(s["name"])}</h2>')
        app += [exam_question(q["num"], q) for q in s["questions"]]
    docs.append(Doc("anhang-a", "Anhang A", lang="de", toc=False, body="\n".join(app)))
    sol = ['<h1>Lösungen · Rješenja</h1>',
           '<p lang="hr">Dodirnite odgovor da biste otvorili pitanje s objašnjenjem. U zagradi je broj u katalogu.</p>']
    for t in data["tests"]:
        sol.append(f'<h2 id="t{t["n"]}">Probetest {t["n"]}</h2>')
        sol.append('<p class="sol">' + " · ".join(
            f'<a href="{qhref(q["id"])}">{i + 1}:&#160;{q["answer"]}</a>&#160;<span class="small">({esc(q["label"])})</span>'
            for i, q in enumerate(t["questions"])) + "</p>")
        sol.append(f'<p class="small">Fragen 31–33: Landesfragen {", ".join(str(n) for n in t["state_nums"])} – '
                   f'<a href="#laender">Lösungen der Landesfragen</a></p>')
    sol.append('<h2 id="laender">Landesfragen · Pitanja o pokrajinama</h2>')
    for s in data["state_key"]:
        code = s["code"]
        sol.append(f'<p class="sol"><b>{esc(s["name"])}:</b> ' + " · ".join(
            f'<a href="{qhref(f"{code}-{i + 1:02d}") if f"{code}-{i + 1:02d}" in where else "#"}">{i + 1}:&#160;{a}</a>'
            for i, a in enumerate(s["answers"])) + "</p>")
    docs.append(Doc("loesungen", "Lösungen", lang="de", toc=False, body="\n".join(sol)))

    # ---- indexes -------------------------------------------------------------------------------------
    topics = "".join(
        f'<div class="entry"><p><b>{esc(tp["bks"])}</b> · <span lang="de">{esc(tp["de"])}</span> '
        f'({len(tp["nums"])} pitanja{f" + {tp["state_count"]} pitanja o pokrajinama" if tp["state_count"] else ""})</p>'
        f'<p class="nums">{link_nums(tp["nums"], gen)}</p></div>' for tp in data["topics"])
    docs.append(Doc("register", "Tematsko kazalo", lang="hr", body=(
        '<h1>Tematsko kazalo</h1><p class="sub" lang="de">Themenregister – ciljano ponavljanje po temama</p>'
        '<p>Griješite li često u nekoj temi, ponovite sva njezina pitanja. Brojevi su brojevi općih pitanja; pitanja o pokrajinama su u <a href="teil2.xhtml">Dijelu 2</a>.</p>'
        + topics)))
    gloss = "".join(f'<p class="entry"><b lang="de">{esc(g["de"])}</b><br/>{esc(g["bks"])}</p>' for g in data["glossary"])
    docs.append(Doc("glossar", "Glossar Deutsch – BKS", lang="hr", body=(
        '<h1 lang="de">Glossar Deutsch – BKS</h1><p class="sub">Pojmovnik njemački – BKS</p>' + gloss)))

    # ---- inline table of contents (after the imprint) ---------------------------------------------
    toc_lines = []
    for d in docs:
        if not d.toc:
            continue
        toc_lines.append(f'<p><a href="{d.href}">{esc(d.title)}</a></p>')
        toc_lines += [f'<p class="l2"><a href="{h}">{esc(t)}</a></p>' for t, h in d.children]
    docs.insert(2, Doc("inhalt", "Sadržaj / Inhalt", lang="de", landmark="toc", toc=False, body_class="toc",
                       body="<h1>Sadržaj / Inhalt</h1>\n" + "\n".join(toc_lines)))

    # check that every internal link has a target
    ids = {}
    for d in docs:
        ids[d.href] = set(re.findall(r'id="([^"]+)"', d.body))
    bad = []
    for d in docs:
        for href in re.findall(r'href="([^"#:]+\.xhtml)(?:#([^"]+))?"', d.body):
            f, a = href
            if f not in ids or (a and a not in ids[f]):
                bad.append((d.href, f, a))
    if bad:
        sys.exit(f"broken links: {bad[:10]}")

    book = Book(title="Einbürgerungstest & Leben in Deutschland – Deutsch–Bosnisch/Kroatisch/Serbisch", language="de",
                creator=R["author"], publisher=R["publisher"], css=CSS, cover=cover, images=images, docs=docs,
                identifier="urn:uuid:5f6c1d3e-9a63-4c1f-8f3b-ebk-de-bks".replace("ebk-de-bks", "0e1b2c3d4e5f"),
                description="Alle 460 Fragen zum Test „Leben in Deutschland“ und zum Einbürgerungstest mit Übersetzung ins Bosnische/Kroatische/Serbische, Erklärungen und 10 Probetests.")
    book.toc_title = "Sadržaj / Inhalt"
    epub = book.write(out / "ebook_de-bks.epub")
    errors = check(epub)
    info = dict(epub=epub.name, cover=cover.name, size_kb=round(epub.stat().st_size / 1024), files=len(docs),
                images=len(images), draft=M["draft"], epubcheck_errors=len(errors))
    (out / "ebook_info.json").write_text(json.dumps(info, indent=1))
    print(json.dumps(info))
    if errors:
        print("\n".join(errors[:30]))
        sys.exit(1)


if __name__ == "__main__":
    main()
