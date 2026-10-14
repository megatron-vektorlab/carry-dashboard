"""Minimal EPUB 3 writer for Kindle (KDP) eBooks.

Writes a reflowable EPUB 3 with an EPUB 2 NCX for older readers, a navigation document, a
cover image and landmarks. KDP converts it for every Kindle device and app; EPUBCheck must
report no errors (see check()).
"""
from __future__ import annotations

import datetime
import html
import mimetypes
import uuid
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

XHTML = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{lang}" xml:lang="{lang}">
<head>
<meta charset="utf-8"/>
<title>{title}</title>
<link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body{body_attr}>
{body}
</body>
</html>
"""


def esc(s: str) -> str:
    return html.escape(s, quote=False)


@dataclass
class Doc:
    id: str                      # manifest id, also the file name stem
    title: str
    body: str                    # XHTML body content
    lang: str = "en"
    toc: bool = True             # list in the table of contents
    children: list = field(default_factory=list)   # (title, "file.xhtml#anchor") sub-entries
    landmark: str | None = None  # e.g. "bodymatter", "toc"
    body_class: str = ""

    @property
    def href(self) -> str:
        return f"{self.id}.xhtml"


@dataclass
class Book:
    title: str
    language: str
    creator: str
    publisher: str = ""
    description: str = ""
    identifier: str = ""
    css: str = ""
    cover: Path | None = None
    images: dict = field(default_factory=dict)    # href in EPUB -> source Path
    docs: list = field(default_factory=list)
    modified: str = ""

    def write(self, out: Path) -> Path:
        ident = self.identifier or f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, self.title)}"
        modified = self.modified or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        out.parent.mkdir(parents=True, exist_ok=True)
        files = {}
        files["mimetype"] = b"application/epub+zip"
        files["META-INF/container.xml"] = (
            '<?xml version="1.0" encoding="utf-8"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
            '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>').encode()
        files["OEBPS/style.css"] = self.css.encode()
        manifest = ['<item id="css" href="style.css" media-type="text/css"/>',
                    '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
                    '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>']
        spine = []
        if self.cover:
            ext = self.cover.suffix.lower()
            mt = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
            files[f"OEBPS/images/cover{ext}"] = self.cover.read_bytes()
            manifest.append(f'<item id="cover-image" href="images/cover{ext}" media-type="{mt}" properties="cover-image"/>')
        # no HTML cover page: Kindle shows the cover image from the metadata, and an extra cover
        # page would make the cover appear twice (Kindle Publishing Guidelines 4.2 and 9.1)
        docs = list(self.docs)
        for href, src in self.images.items():
            mt = mimetypes.guess_type(href)[0] or "image/png"
            iid = "img-" + href.replace("/", "-").replace(".", "-")
            files[f"OEBPS/{href}"] = Path(src).read_bytes()
            manifest.append(f'<item id="{iid}" href="{href}" media-type="{mt}"/>')
        for d in docs:
            body_attr = f' class="{d.body_class}"' if d.body_class else ""
            files[f"OEBPS/{d.href}"] = XHTML.format(lang=d.lang, title=esc(d.title), body=d.body, body_attr=body_attr).encode()
            props = ' properties="mathml"' if "<math" in d.body else ""
            manifest.append(f'<item id="{d.id}" href="{d.href}" media-type="application/xhtml+xml"{props}/>')
            spine.append(f'<itemref idref="{d.id}"/>')
        toc_docs = [d for d in docs if d.toc]
        # navigation document
        def label(text, lang):
            # entries in another language than the book are marked, so text-to-speech reads them right
            if lang and lang != self.language:
                return f'<span lang="{lang}" xml:lang="{lang}">{esc(text)}</span>'
            return esc(text)

        nav_items = []
        for d in toc_docs:
            sub = ""
            if d.children:
                sub = "<ol>" + "".join(f'<li><a href="{h}">{label(t, d.lang)}</a></li>' for t, h in d.children) + "</ol>"
            nav_items.append(f'<li><a href="{d.href}">{label(d.title, d.lang)}</a>{sub}</li>')
        landmarks = []
        for d in docs:
            if d.landmark:
                landmarks.append(f'<li><a epub:type="{d.landmark}" href="{d.href}">{esc(d.title)}</a></li>')
        nav = (f'<nav epub:type="toc" id="toc"><h1>{esc(self.toc_title)}</h1><ol>' + "".join(nav_items) + '</ol></nav>'
               + ('<nav epub:type="landmarks" hidden=""><ol>' + "".join(landmarks) + '</ol></nav>' if landmarks else ""))
        files["OEBPS/nav.xhtml"] = XHTML.format(lang=self.language, title=esc(self.toc_title), body=nav, body_attr="").encode()
        # NCX (EPUB 2 compatibility; Kindle uses it for the "Go to" menu on older devices)
        points, order = [], 0
        for d in toc_docs:
            order += 1
            kids = ""
            for t, h in d.children:
                order += 1
                kids += (f'<navPoint id="np{order}" playOrder="{order}"><navLabel><text>{esc(t)}</text></navLabel>'
                         f'<content src="{h}"/></navPoint>')
            points.append(f'<navPoint id="np{order}x" playOrder="{order - len(d.children)}"><navLabel><text>{esc(d.title)}</text></navLabel>'
                          f'<content src="{d.href}"/>{kids}</navPoint>')
        ncx = ('<?xml version="1.0" encoding="utf-8"?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">'
               f'<head><meta name="dtb:uid" content="{ident}"/><meta name="dtb:depth" content="2"/>'
               '<meta name="dtb:totalPageCount" content="0"/><meta name="dtb:maxPageNumber" content="0"/></head>'
               f'<docTitle><text>{esc(self.title)}</text></docTitle><navMap>' + "".join(points) + '</navMap></ncx>')
        files["OEBPS/toc.ncx"] = ncx.encode()
        meta = [f'<dc:identifier id="bookid">{esc(ident)}</dc:identifier>',
                f'<dc:title>{esc(self.title)}</dc:title>',
                f'<dc:language>{self.language}</dc:language>',
                f'<dc:creator>{esc(self.creator)}</dc:creator>',
                f'<meta property="dcterms:modified">{modified}</meta>']
        if self.publisher:
            meta.append(f'<dc:publisher>{esc(self.publisher)}</dc:publisher>')
        if self.description:
            meta.append(f'<dc:description>{esc(self.description)}</dc:description>')
        if self.cover:
            meta.append('<meta name="cover" content="cover-image"/>')
        opf = ('<?xml version="1.0" encoding="utf-8"?>\n'
               '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">'
               '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">' + "".join(meta) + '</metadata>'
               '<manifest>' + "".join(manifest) + '</manifest>'
               '<spine toc="ncx">' + "".join(spine) + '</spine></package>')
        files["OEBPS/content.opf"] = opf.encode()
        with zipfile.ZipFile(out, "w") as z:
            z.writestr(zipfile.ZipInfo("mimetype"), files.pop("mimetype"), compress_type=zipfile.ZIP_STORED)
            for name, data in files.items():
                z.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)
        return out

    toc_title: str = "Contents"


def check(epub: Path) -> list[str]:
    """Run EPUBCheck; returns the error/fatal messages (warnings are printed).

    A missing jar, a Java failure or a non-zero exit without a parsable message is
    reported as an error too, so a broken check can never pass silently."""
    import subprocess
    import epubcheck  # noqa: F401  (pip install epubcheck; needs Java)
    base = Path(epubcheck.__file__).parent
    jar = next((p for p in (base / "epubcheck.jar", base / "lib" / "epubcheck.jar") if p.exists()), None)
    if jar is None:
        return [f"FATAL: epubcheck.jar not found in {base}"]
    r = subprocess.run(["java", "-jar", str(jar), str(epub)], capture_output=True, text=True)
    lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip() and "JAVA_TOOL_OPTIONS" not in l]
    errors = [l for l in lines if l.startswith(("ERROR", "FATAL"))]
    for l in lines:
        if l.startswith(("WARNING", "USAGE")):
            print("  epubcheck:", l)
    if r.returncode != 0 and not errors:
        errors = [f"FATAL: epubcheck exited with {r.returncode}: " + " | ".join(lines[-5:])]
    if r.returncode == 0 and not any("No errors or warnings detected" in l or "Messages:" in l for l in lines):
        errors.append("FATAL: epubcheck produced no result line: " + " | ".join(lines[-5:]))
    return errors
