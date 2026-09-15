
import os
import re
import sys
import json
import urllib.parse

sys.path.append("/opt/userdata/busicode/clientscript")

import client_util as CSUTIL
import docx as docxlib  # python-docx
import fitz  # PyMuPDF
import requests

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
WORK_DIR = PROJECT_ROOT / "working"

FORMAT_DOC_DIR = WORK_DIR / "formatted"
TEXT_DIR = WORK_DIR / "text"


# ---------------------------------------------------------------------------
# Path access control
#
# The single-file PDF analysis tools below take the input PDF as a caller-
# supplied path argument (pdf=...), but it is checked - before any work
# happens - against two rules: it must start with "working/" and it must
# already exist as a file. This keeps callers confined to the gitignored
# scratch area without pinning them to one hardcoded filename.
#
# Output still goes to a single canonical file/dir inside WORK_DIR, so there
# is no output path to inject.
# ---------------------------------------------------------------------------

OUTPUT_PATH = WORK_DIR / "OUTPUT.txt"

# The page-render tool can't fit its output into a single text file (it
# writes one PNG per page), so it gets its own fixed, hardcoded directory.
OUTPUT_PAGES_DIR = WORK_DIR / "OUTPUT_PAGES"


def _resolve_under_workdir(argval, argname):
    """Shared core check for any caller-supplied path argument: it must be
    given, must start with "working/", and must not escape WORK_DIR (e.g. via
    ".."). Existence/type is the caller's job to check next. Returns the
    resolved Path."""

    assert argval, f"{argname}=<path> is required (must start with 'working/')"
    assert argval.startswith("working/"), f"{argname} path must start with 'working/', got {argval!r}"

    candidate = (PROJECT_ROOT / argval).resolve()
    workdir_resolved = WORK_DIR.resolve()

    assert candidate == workdir_resolved or workdir_resolved in candidate.parents, \
        f"{argname} path {argval!r} escapes the working/ directory"

    return candidate


def resolve_input_pdf(pdf_arg):
    """Validate and resolve a caller-supplied pdf= path argument. Enforces,
    before any work is done: the argument must be given, must start with
    "working/", must not escape WORK_DIR (e.g. via ".."), and must already
    exist as a file. Despite the name/arg convention (kept for compatibility
    with existing callers), this accepts .docx as well as .pdf - see
    _is_docx/_get_docx_full_text for how each is handled downstream."""

    candidate = _resolve_under_workdir(pdf_arg, "pdf")

    assert candidate.exists(), f"No such file: {candidate}"
    assert candidate.is_file(), f"{candidate} is not a file"

    return candidate


def resolve_dest_dir(dest_arg):
    """Validate and resolve a caller-supplied dest= directory argument (used
    by FetchUrl). Enforces, before any work is done: the argument must be
    given, must start with "working/", must not escape WORK_DIR, and must
    already exist as a directory."""

    candidate = _resolve_under_workdir(dest_arg, "dest")

    assert candidate.exists(), f"No such directory: {candidate}"
    assert candidate.is_dir(), f"{candidate} is not a directory"

    return candidate


def get_output_path():
    """Return the canonical output file path, creating WORK_DIR if needed."""

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    return OUTPUT_PATH


def get_output_pages_dir():
    """Return the canonical output directory for rendered page images."""

    OUTPUT_PAGES_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_PAGES_DIR


def load_doc_info():

    def probe():
        for basedir, _, fnames in os.walk(WORK_DIR):
            for f in fnames:
                if f == "document_info.json":
                    yield Path(basedir) / f

    probelist = list(probe())
    assert len(probelist) == 1, f"Expected exactly 1 document_info file"

    with open(probelist[0]) as fh:
        return json.load(fh)


def insert_doc_info():

    docinfo = load_doc_info()

    CSUTIL.direct_init_db("dburfoot", "planscan")

    idgen = CSUTIL.gen_valid_assign_id("doc_info")

    def gen_records():
        for entry in docinfo:
            filename = entry["filename"]
            textpath = TEXT_DIR / (Path(filename).stem + ".txt")

            extracted_text = ""
            if textpath.exists():
                with open(textpath, encoding="utf-8") as fh:
                    extracted_text = fh.read()

            yield {
                "id": next(idgen),
                "doc_link": entry["url"],
                "location": str(FORMAT_DOC_DIR / filename),
                "extracted_text": extracted_text,
                "file_name": filename,
                "day_code": entry["date"],
            }

    CSUTIL.bulk_insert("doc_info", list(gen_records()))



def _is_docx(path):
    return Path(path).suffix.lower() == ".docx"


def _get_docx_full_text(docxpath):
    """Join every paragraph and table-cell string in the .docx into one text
    blob. .docx has no reliable notion of "pages" without actually rendering
    it (page breaks are a print-time layout detail, not stored positions), so
    callers treat the whole document as a single page."""

    doc = docxlib.Document(docxpath)

    parts = [p.text for p in doc.paragraphs if p.text.strip()]

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    parts.append(cell.text)

    return "\n".join(parts).strip()


def _gen_page_text(pdfpath, *, ocr_fallback=True):
    """Yield the text of each "page" of pdfpath in order. For a PDF, falls
    back to OCR for scanned/image-only pages (no selectable text layer) when
    ocr_fallback is set. For a .docx, yields exactly one page - see
    _get_docx_full_text."""

    if _is_docx(pdfpath):
        yield _get_docx_full_text(pdfpath)
        return

    with fitz.open(pdfpath) as doc:
        for page in doc:
            pagetext = page.get_text().strip()

            if not pagetext and ocr_fallback:
                # Scanned/image-only page, fall back to OCR
                pagetext = page.get_textpage_ocr(full=True).extractTEXT().strip()

            yield pagetext


def extract_text_info(mainpath):

    mainpath = Path(mainpath)
    textpath = TEXT_DIR / (mainpath.stem + ".txt")

    if textpath.exists():
        print(f"Text file {textpath} already exists, skipping")
        return

    TEXT_DIR.mkdir(parents=True, exist_ok=True)

    fulltext = "\n\n".join(_gen_page_text(mainpath))

    with open(textpath, "w", encoding="utf-8") as fh:
        fh.write(fulltext)

    print(f"Extracted text for {mainpath} -> {textpath}")


# ---------------------------------------------------------------------------
# Single-file PDF analysis tools. Each one reads a caller-supplied, validated
# pdf= path (see resolve_input_pdf) and writes to the hardcoded OUTPUT_PATH
# (or OUTPUT_PAGES_DIR) - see plan_entry.py.
# ---------------------------------------------------------------------------

# Terms relevant to spotting residential/commercial development projects in
# planning board documents. Overridable at the command line (comma-separated).
DEFAULT_SCAN_KEYWORDS = ",".join([
    "site plan", "subdivision", "rezoning", "zoning amendment", "variance",
    "special exception", "conditional use", "lot line adjustment",
    "residential", "commercial", "industrial", "multi-family", "condominium",
    "senior housing", "affordable housing", "warehouse", "retail",
    "new construction", "demolition", "renovation", "expansion",
])


FETCH_USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")


def _filename_from_response(target, resp):
    """Pick a filename for a fetched URL: prefer the Content-Disposition
    header's filename (what CivicPlus's Agenda Center sends, e.g.
    'inline;filename=09092026.pdf'), falling back to the last segment of the
    URL's path."""

    cdisp = resp.headers.get("content-disposition", "")
    match = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)"?', cdisp, re.IGNORECASE)
    if match:
        return Path(match.group(1)).name

    filename = Path(urllib.parse.urlparse(target).path).name
    assert filename, f"Could not determine a filename from URL: {target}"
    return filename


def fetch_url(target, dest_arg=""):
    """Download `target` (a URL) via requests, using a normal desktop-browser
    User-Agent - a curl replacement that doesn't need a permission prompt.

    With no dest_arg, writes straight to WORK_DIR/TARGET.pdf (overwriting
    whatever was there). With dest_arg given, it must resolve (per
    resolve_dest_dir) to an existing directory under working/, and the file
    is written there under its original filename - taken from the response's
    Content-Disposition header if the server sends one (as CivicPlus's
    Agenda Center does), otherwise from the last segment of the URL path."""

    assert target, "target=<url> is required"

    # Validate dest_arg before making any network request, so a bad dest=
    # fails fast instead of after burning a download.
    destdir = resolve_dest_dir(dest_arg) if dest_arg else None

    resp = requests.get(target, headers={"User-Agent": FETCH_USER_AGENT}, timeout=30)
    resp.raise_for_status()

    if destdir is not None:
        outpath = destdir / _filename_from_response(target, resp)
    else:
        WORK_DIR.mkdir(parents=True, exist_ok=True)
        outpath = WORK_DIR / "TARGET.pdf"

    with open(outpath, "wb") as fh:
        fh.write(resp.content)

    print(f"Fetched {target} -> {outpath} ({len(resp.content)} bytes, "
          f"content-type: {resp.headers.get('content-type', '?')})")


def extract_pdf_text(pdf_arg):
    """Extract the full text of the given PDF (with OCR fallback per page) to OUTPUT_PATH."""

    inpath = resolve_input_pdf(pdf_arg)
    outpath = get_output_path()

    fulltext = "\n\n".join(_gen_page_text(inpath))

    with open(outpath, "w", encoding="utf-8") as fh:
        fh.write(fulltext)

    print(f"Extracted text for {inpath} -> {outpath} ({len(fulltext)} chars)")


def get_pdf_page_texts(pdf_arg):
    """Return a list of the given PDF's page texts (OCR fallback per scanned
    page), 1-indexed by position - the per-page counterpart to
    extract_pdf_text's single joined blob. Used to populate the doc_pages
    table (see plan_db.record_document_text) rather than write to
    OUTPUT_PATH."""

    inpath = resolve_input_pdf(pdf_arg)
    return list(_gen_page_text(inpath))


def _extract_docx_info(inpath):
    """docx counterpart to the fitz-based branch of extract_pdf_info: no
    per-page dimensions (docx has no fixed page geometry), so the whole
    document is reported as a single "page" - consistent with
    _get_docx_full_text treating it as one page of text."""

    doc = docxlib.Document(inpath)
    fulltext = _get_docx_full_text(inpath)

    props = doc.core_properties
    metadata = {
        "title": props.title,
        "author": props.author,
        "created": props.created.isoformat() if props.created else None,
        "modified": props.modified.isoformat() if props.modified else None,
    }

    return {
        "source_path": str(inpath),
        "file_size_bytes": inpath.stat().st_size,
        "page_count": 1,
        "metadata": {k: v for k, v in metadata.items() if v is not None},
        "pages": [{
            "page": 1,
            "width": None,
            "height": None,
            "text_chars": len(fulltext),
            "has_selectable_text": bool(fulltext),
        }],
    }


def extract_pdf_info(pdf_arg):
    """Write a JSON summary of the given PDF/docx to OUTPUT_PATH: metadata,
    page count/size, and per-page stats (dimensions, text length, whether OCR
    would be needed). A .docx has no page geometry, so it's always reported
    as a single page - see _extract_docx_info."""

    inpath = resolve_input_pdf(pdf_arg)
    outpath = get_output_path()

    if _is_docx(inpath):
        info = _extract_docx_info(inpath)
    else:
        with fitz.open(inpath) as doc:

            def gen_pages():
                for pagenum, page in enumerate(doc):
                    pagetext = page.get_text().strip()
                    yield {
                        "page": pagenum + 1,
                        "width": page.rect.width,
                        "height": page.rect.height,
                        "text_chars": len(pagetext),
                        "has_selectable_text": bool(pagetext),
                    }

            info = {
                "source_path": str(inpath),
                "file_size_bytes": inpath.stat().st_size,
                "page_count": doc.page_count,
                "metadata": dict(doc.metadata or {}),
                "pages": list(gen_pages()),
            }

    with open(outpath, "w", encoding="utf-8") as fh:
        json.dump(info, fh, indent=2)

    print(f"Wrote PDF info for {inpath} -> {outpath} ({info['page_count']} pages)")


def scan_pdf_keywords(keywords_str, pdf_arg, *, context_chars=80):
    """Scan the given PDF's text (page by page, no OCR - keyword scans are
    meant to be fast) for the given comma-separated keywords, and write a
    JSON list of hits (page, keyword, count, and a short surrounding
    snippet) to OUTPUT_PATH."""

    inpath = resolve_input_pdf(pdf_arg)
    outpath = get_output_path()

    keywords = [kw.strip() for kw in keywords_str.split(",") if kw.strip()]
    assert keywords, "No keywords supplied"

    def gen_hits():
        for pagenum, pagetext in enumerate(_gen_page_text(inpath, ocr_fallback=False)):
            lowertext = pagetext.lower()
            for kw in keywords:
                kwlower = kw.lower()
                count = lowertext.count(kwlower)
                if count == 0:
                    continue

                firstidx = lowertext.index(kwlower)
                lo = max(0, firstidx - context_chars)
                hi = min(len(pagetext), firstidx + len(kw) + context_chars)
                snippet = pagetext[lo:hi].replace("\n", " ").strip()

                yield {
                    "page": pagenum + 1,
                    "keyword": kw,
                    "count": count,
                    "snippet": snippet,
                }

    hits = list(gen_hits())

    result = {
        "source_path": str(inpath),
        "keywords": keywords,
        "hit_count": len(hits),
        "hits": hits,
    }

    with open(outpath, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)

    print(f"Scanned {inpath} for {len(keywords)} keywords -> {outpath} ({len(hits)} hits)")


MAX_RENDER_PAGES_DEFAULT = 30


def _parse_page_spec(pages_str, page_count):
    """Parse a spec like '1-6,10,12-14' (1-indexed, inclusive) into a sorted
    list of 0-indexed page numbers. An empty spec means "all pages"."""

    if not pages_str:
        return list(range(page_count))

    result = set()
    for chunk in pages_str.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            lo, hi = chunk.split("-", 1)
            lo, hi = int(lo), int(hi)
        else:
            lo = hi = int(chunk)

        assert 1 <= lo <= hi <= page_count, f"Page range {chunk} out of bounds for a {page_count}-page document"
        result.update(range(lo - 1, hi))

    return sorted(result)


def render_pdf_pages(dpi, pages_str, pdf_arg):
    """Render pages of the given PDF to PNG files inside OUTPUT_PAGES_DIR (one
    file per page, page_NNN.png). With no explicit pages_str, renders the
    whole document up to MAX_RENDER_PAGES_DEFAULT pages, to avoid an
    accidental huge/unbounded write - pass an explicit pages_str to go
    further."""

    inpath = resolve_input_pdf(pdf_arg)
    assert not _is_docx(inpath), \
        f"{inpath} is a .docx - PdfRenderPages only supports PDF (no page-image equivalent for docx)"
    outdir = get_output_pages_dir()

    with fitz.open(inpath) as doc:
        pageidxs = _parse_page_spec(pages_str, doc.page_count)

        if not pages_str and len(pageidxs) > MAX_RENDER_PAGES_DEFAULT:
            print(f"Document has {len(pageidxs)} pages; capping at {MAX_RENDER_PAGES_DEFAULT} "
                  f"(pass pages=1-{len(pageidxs)} explicitly to render them all)")
            pageidxs = pageidxs[:MAX_RENDER_PAGES_DEFAULT]

        zoom = dpi / 72.0
        matrix = fitz.Matrix(zoom, zoom)

        written = []
        for idx in pageidxs:
            page = doc[idx]
            pix = page.get_pixmap(matrix=matrix)
            pngpath = outdir / f"page_{idx + 1:03d}.png"
            pix.save(pngpath)
            written.append(pngpath)

    print(f"Rendered {len(written)} page(s) from {inpath} -> {outdir}")


