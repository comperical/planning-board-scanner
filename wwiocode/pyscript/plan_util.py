
import os
import re
import sys
import json

sys.path.append("/opt/userdata/busicode/clientscript")

import client_util as CSUTIL
import fitz  # PyMuPDF

from pathlib import Path

WORK_DIR = Path(__file__).parent.parent.parent / "working"

FORMAT_DOC_DIR = WORK_DIR / "formatted"
TEXT_DIR = WORK_DIR / "text"


# ---------------------------------------------------------------------------
# Strict path access control
#
# The single-file PDF analysis tools below do not accept any input/output
# path from the caller. They are hardcoded to a single canonical input file
# and a single canonical output file inside WORK_DIR, so there is no path to
# inject: to analyze a PDF, copy/symlink it to TARGET_PDF first.
# ---------------------------------------------------------------------------

TARGET_PDF = WORK_DIR / "TARGET.pdf"
OUTPUT_PATH = WORK_DIR / "OUTPUT.txt"

# The page-render tool can't fit its output into a single text file (it
# writes one PNG per page), so it gets its own fixed, hardcoded directory.
OUTPUT_PAGES_DIR = WORK_DIR / "OUTPUT_PAGES"


def get_target_pdf():
    """Return the canonical input PDF path, asserting it actually exists there."""

    assert TARGET_PDF.exists(), f"Expected the input PDF at {TARGET_PDF} - copy/symlink the file you want to analyze there first"
    assert TARGET_PDF.is_file(), f"{TARGET_PDF} is not a file"
    return TARGET_PDF


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



def _gen_page_text(pdfpath, *, ocr_fallback=True):
    """Yield the text of each page of pdfpath in order. Falls back to OCR for
    scanned/image-only pages (no selectable text layer) when ocr_fallback is set."""

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
# Single-file PDF analysis tools. Each one reads the hardcoded TARGET_PDF and
# writes to the hardcoded OUTPUT_PATH (or OUTPUT_PAGES_DIR) - see plan_entry.py.
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


def extract_pdf_text():
    """Extract the full text of TARGET_PDF (with OCR fallback per page) to OUTPUT_PATH."""

    inpath = get_target_pdf()
    outpath = get_output_path()

    fulltext = "\n\n".join(_gen_page_text(inpath))

    with open(outpath, "w", encoding="utf-8") as fh:
        fh.write(fulltext)

    print(f"Extracted text for {inpath} -> {outpath} ({len(fulltext)} chars)")


def extract_pdf_info():
    """Write a JSON summary of TARGET_PDF to OUTPUT_PATH: metadata, page
    count/size, and per-page stats (dimensions, text length, whether OCR
    would be needed)."""

    inpath = get_target_pdf()
    outpath = get_output_path()

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


def scan_pdf_keywords(keywords_str, *, context_chars=80):
    """Scan TARGET_PDF's text (page by page, no OCR - keyword scans are meant
    to be fast) for the given comma-separated keywords, and write a JSON list
    of hits (page, keyword, count, and a short surrounding snippet) to
    OUTPUT_PATH."""

    inpath = get_target_pdf()
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


def render_pdf_pages(dpi, pages_str):
    """Render pages of TARGET_PDF to PNG files inside OUTPUT_PAGES_DIR (one
    file per page, page_NNN.png). With no explicit pages_str, renders the
    whole document up to MAX_RENDER_PAGES_DEFAULT pages, to avoid an
    accidental huge/unbounded write - pass an explicit pages_str to go
    further."""

    inpath = get_target_pdf()
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


