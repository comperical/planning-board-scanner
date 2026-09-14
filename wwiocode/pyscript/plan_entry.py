#!/opt/rawdata/pyworld/KitchenSink/bin/python3

import os
import sys

import plan_db as DB
import plan_util as UTIL


sys.path.append("/opt/userdata/crm/src/python/opsutil")

import ArgMap
import CodeSetup as SETUP



class ExtractDataTool:

    def run_op(self, argmap):
        
        def gendata():

            for basedir, _, fnames in os.walk(UTIL.FORMAT_DOC_DIR):

                for f in fnames:
                    print(f)
                    yield UTIL.FORMAT_DOC_DIR / f


        for formdoc in gendata():
            UTIL.extract_text_info(formdoc)

        #datalist = list(gendata())
        #UTIL.extract_text_info(docpath)

class ProcessDocTool:

    def run_op(self, argmap):


        docinfo = UTIL.load_doc_info()

        #print(docinfo)

        UTIL.insert_doc_info()


class BasicTool:

    def run_op(self, argmap):
        print("Study basic!!!")

        print(f"Work directory is {UTIL.WORK_DIR}")

        assert os.path.exists(UTIL.WORK_DIR)


# ---------------------------------------------------------------------------
# Single-file PDF analysis tools.
#
# Each tool takes the input PDF as pdf=<path>, checked - before any work
# happens - against two rules: it must start with "working/" and it must
# already exist as a file. Output still goes to a hardcoded canonical
# location inside working/, so there is no output path for a caller to
# inject:
#   - input  : pdf=working/<...>.pdf  (must start with "working/" and exist)
#   - output : working/OUTPUT.txt     (text or JSON-as-text, depending on tool)
#   - output : working/OUTPUT_PAGES/  (PdfRenderPages only, one PNG per page)
#
# Example:
#   plan_entry.py FetchUrl target=https://example.town.gov/2026.09.22_Materials.pdf
#   plan_entry.py PdfExtractText pdf=working/TARGET.pdf
#   cat working/OUTPUT.txt
# ---------------------------------------------------------------------------

class ListDirTool:
    """List files under a working/ directory (recursively), with size in
    bytes - a bare `ls`/`find` isn't in the plan_entry.py permission
    allowlist, so this is the way to see what's already in working/<town>/
    without leaving it.

    Args: dir=working/<town>  (must start with "working/" and already exist)
    """

    def run_op(self, argmap):
        dirarg = argmap.getStr("dir", "working")
        root = UTIL.resolve_dest_dir(dirarg)

        for path in sorted(root.rglob("*")):
            if path.is_file():
                relpath = path.relative_to(UTIL.PROJECT_ROOT)
                print(f"{path.stat().st_size:>10}  {relpath}")


class FetchUrlTool:
    """Download a URL using Python requests (a curl replacement, so no
    per-call permission prompt is needed). Sends a normal desktop-browser
    User-Agent.

    With no dest= given, writes straight to working/TARGET.pdf (overwriting
    any existing one). With dest=working/<dir>, that directory must already
    exist under working/, and the file is saved there under the same
    filename it has in the URL.

    Args: target=<url>  [dest=working/<dir>]
    """

    def run_op(self, argmap):
        target = argmap.getStr("target", "")
        dest = argmap.getStr("dest", "")
        UTIL.fetch_url(target, dest)


class PdfExtractTextTool:
    """Extract the full text of pdf= (OCR fallback per scanned page) to
    working/OUTPUT.txt.

    Args: pdf=working/<path>.pdf
    """

    def run_op(self, argmap):
        pdf = argmap.getStr("pdf", "")
        UTIL.extract_pdf_text(pdf)


class PdfInfoTool:
    """Write a JSON summary of pdf= - metadata, page count, file size, and
    per-page stats (dimensions, text length, whether it looks scanned) - to
    working/OUTPUT.txt.

    Args: pdf=working/<path>.pdf
    """

    def run_op(self, argmap):
        pdf = argmap.getStr("pdf", "")
        UTIL.extract_pdf_info(pdf)


class PdfKeywordScanTool:
    """Scan pdf='s text for development-project keywords (site plan,
    subdivision, residential, commercial, ...) and write JSON hits with page
    numbers and snippets to working/OUTPUT.txt. Pass keywords=...
    (comma-separated) to override the default list.

    Args: pdf=working/<path>.pdf  [keywords=a,b,c]
    """

    def run_op(self, argmap):
        pdf = argmap.getStr("pdf", "")
        keywords = argmap.getStr("keywords", UTIL.DEFAULT_SCAN_KEYWORDS)

        UTIL.scan_pdf_keywords(keywords, pdf)


class PdfRenderPagesTool:
    """Render pages of pdf= to PNG images (one file per page) inside
    working/OUTPUT_PAGES/. With no pages= given, renders the whole document
    up to a safety cap (see MAX_RENDER_PAGES_DEFAULT); pass an explicit page
    range to go beyond that on purpose.

    Args: pdf=working/<path>.pdf  [dpi=150]  [pages=1-6,10]
    """

    def run_op(self, argmap):
        pdf = argmap.getStr("pdf", "")
        dpi = argmap.getInt("dpi", 150)
        pages = argmap.getStr("pages", "")

        UTIL.render_pdf_pages(dpi, pages, pdf)


class IngestPdfTool:
    """Run PdfInfo + PdfKeywordScan (+ full text extraction, by default) on
    pdf= and record it all straight into the SQLite database (see
    plan_db.py) - the single-call equivalent of PdfInfoTool +
    PdfKeywordScanTool + UpdateDbTool, for wiring a scan's downloaded PDFs
    into the DB without leaving the plan_entry.py allowlist. Upserts by
    file_path (creating the town row as a side effect); safe to re-run - a
    re-scan replaces that document's previously recorded pages/keyword
    hits/text rather than duplicating them.

    Full-page text extraction (OCR fallback per scanned page, via
    plan_util.get_pdf_page_texts) is the slow step for a large scanned
    packet - pass with_text=false to skip it (PdfInfo/PdfKeywordScan still
    run) and extract text separately/later if needed.

    Args: pdf=working/<path>.pdf  [source_url=...]  [date=YYYY-MM-DD]
          [keywords=a,b,c]  [with_text=true]
    """

    def run_op(self, argmap):
        pdf = argmap.getStr("pdf", "")
        source_url = argmap.getStr("source_url", "") or None
        date = argmap.getStr("date", "") or None
        keywords = argmap.getStr("keywords", UTIL.DEFAULT_SCAN_KEYWORDS)
        with_text = argmap.getBit("with_text", True)

        conn = DB.get_connection()

        UTIL.extract_pdf_info(pdf)
        info = DB.load_json_output()
        DB.record_pdf_info(conn, pdf, info, source_url=source_url)

        UTIL.scan_pdf_keywords(keywords, pdf)
        scan = DB.load_json_output()
        DB.record_keyword_scan(conn, pdf, scan, source_url=source_url)

        if with_text:
            page_texts = UTIL.get_pdf_page_texts(pdf)
            DB.record_document_text(conn, pdf, page_texts, source_url=source_url)
            print(f"Recorded text for {len(page_texts)} page(s)")

        if date:
            DB.upsert_document(conn, pdf, source_url=source_url, doc_date=date)

        print(f"Ingested {pdf}: {info['page_count']} pages, "
              f"{len(scan.get('hits', []))} keyword hit(s)")


class CreateProjectTool:
    """Create a new row in the projects table (a real development spotted
    by hand from one or more documents - see plan_db.py) and print its id.
    Fills in just enough to identify the row - use ApplyProjectEdit
    afterward (working/project_edit/<id>.md + .json) to fill in short_desc
    and the full markdown write-up.

    Args: town=<slug>
    """

    def run_op(self, argmap):
        town = argmap.getStr("town", "")

        assert town, "town=<slug> is required"

        conn = DB.get_connection()
        project_id = DB.create_project(conn, town)
        print(f"Created project {project_id} ({town}). Edit working/project_edit/{project_id}.md "
              f"and/or .json, then run ApplyProjectEdit project_id={project_id}")


class ApplyProjectEditTool:
    """Apply working/project_edit/<project_id>.md (the full_md_text field -
    free-form markdown) and/or working/project_edit/<project_id>.json
    (every other updatable field - currently just {"short_desc": "..."})
    to an existing projects row. Either file may be absent (that side is
    left unchanged); at least one must exist. Once applied, both files are
    deleted - the DB is the source of truth after that point, so
    working/project_edit/ only ever holds edits not yet applied. To revise
    a project further, just write fresh .md/.json files and re-run this.

    Args: project_id=<id>
    """

    def run_op(self, argmap):
        project_id = argmap.getInt("project_id", -1)
        assert project_id != -1, "project_id=<id> is required"

        conn = DB.get_connection()
        DB.sync_project_from_files(conn, project_id)
        print(f"Synced project {project_id} from working/project_edit/{project_id}.md / .json")


class LinkProjectTool:
    """Link a project to a document that mentions it (project_documents
    table) - a project is typically referenced across several meetings'
    documents (an agenda, then minutes, then a later extension/approval).
    page= is optional: the 1-indexed page where the project's mention
    starts in this document (e.g. from a DocDetail keyword-hit or from
    reading working/OUTPUT.txt). Safe to call again later to add/update the
    page number - omitting page= leaves any existing value alone.

    Args: project_id=<id>  pdf=working/<path>.pdf  [page=<page_number>]
    """

    def run_op(self, argmap):
        project_id = argmap.getInt("project_id", -1)
        pdf = argmap.getStr("pdf", "")
        page = argmap.getInt("page", -1)

        assert project_id != -1, "project_id=<id> is required"

        conn = DB.get_connection()
        document_id = DB.upsert_document(conn, pdf)
        DB.link_project_document(conn, project_id, document_id, page_number=(page if page != -1 else None))
        pagesuffix = f", page {page}" if page != -1 else ""
        print(f"Linked project {project_id} <-> document {document_id} ({pdf}){pagesuffix}")


class LogAnalysisTool:
    """Record a timestamped note that a document has been manually
    analyzed (analysis_log table) - e.g. "checked pages 40-60, no new
    projects past #3". Always adds a new row (a log, not a field to
    overwrite) - repeated calls accumulate history.

    Args: pdf=working/<path>.pdf  [notes=...]
    """

    def run_op(self, argmap):
        pdf = argmap.getStr("pdf", "")
        notes = argmap.getStr("notes", "")

        conn = DB.get_connection()
        document_id = DB.log_analysis(conn, pdf, notes)
        print(f"Logged analysis for document {document_id} ({pdf}): {notes}")


class ClearAnalysisLogTool:
    """Delete every analysis_log row for pdf= - the undo for LogAnalysis.
    Once cleared, the document has no recorded analysis pass, so
    NextToAnalyze will surface it again. Does not remove any projects or
    project_documents links already created from this document - only the
    analysis_log rows themselves.

    Args: pdf=working/<path>.pdf
    """

    def run_op(self, argmap):
        pdf = argmap.getStr("pdf", "")

        conn = DB.get_connection()
        document_id, deleted = DB.clear_analysis_log(conn, pdf)
        print(f"Cleared {deleted} analysis_log row(s) for document {document_id} ({pdf}).")


class NextToAnalyzeTool:
    """Find the next document that has no analysis_log rows yet (i.e. has
    never been through LogAnalysis) and print its pdf= path plus enough
    context (town, date, keyword-hit count) to decide whether it's worth
    opening. Most recent doc_date first (documents with no known doc_date
    sort last, since recency can't be judged for them). Prints nothing if
    every document has already been analyzed at least once.

    Args: [town=<slug>]  (restrict to one town)
    """

    def run_op(self, argmap):
        town_filter = argmap.getStr("town", "")

        conn = DB.get_connection()
        query = """
            SELECT d.file_path, d.doc_date, t.slug,
                   (SELECT COUNT(*) FROM keyword_hits WHERE document_id = d.id)
            FROM documents d
            JOIN town t ON d.town_id = t.id
            WHERE (SELECT COUNT(*) FROM analysis_log WHERE document_id = d.id) = 0
        """
        params = ()
        if town_filter:
            query += " AND t.slug = ?"
            params = (town_filter,)
        query += " ORDER BY d.doc_date IS NULL, d.doc_date DESC, d.id DESC LIMIT 1"

        row = conn.execute(query, params).fetchone()

        if row is None:
            print("Nothing left to analyze" + (f" for {town_filter}" if town_filter else "") + ".")
            return

        file_path, doc_date, slug, hitcount = row
        print(f"pdf={file_path}")
        print(f"town={slug}  date={doc_date or '?'}  keyword_hits={hitcount}")


class DocDetailTool:
    """Print everything already known about pdf= - town/date/size/source,
    keyword hits, and the full extracted text (written to
    working/OUTPUT.txt, same convention as PdfExtractText, since it can be
    long) - without re-running any PDF extraction. Meant to be the one call
    an analysis pass needs after NextToAnalyze picks a document.

    Args: pdf=working/<path>.pdf
    """

    def run_op(self, argmap):
        pdf = argmap.getStr("pdf", "")

        conn = DB.get_connection()
        row = conn.execute(
            """
            SELECT d.id, d.doc_date, d.file_size_bytes, d.page_count, d.source_url, t.slug
            FROM documents d LEFT JOIN town t ON d.town_id = t.id
            WHERE d.file_path = ?
            """,
            (pdf,),
        ).fetchone()
        assert row is not None, f"No documents row for {pdf} - run IngestPdf on it first"
        document_id, doc_date, size, pages, source_url, slug = row

        print(f"town={slug}  date={doc_date or '?'}  pages={pages}  size={size} bytes")
        print(f"source_url={source_url or '?'}")

        hits = conn.execute(
            "SELECT page_number, keyword, count, snippet FROM keyword_hits "
            "WHERE document_id = ? ORDER BY page_number", (document_id,),
        ).fetchall()
        print(f"\n{len(hits)} keyword hit(s):")
        for page_number, keyword, count, snippet in hits:
            print(f"  p{page_number}  {keyword} x{count}  {snippet}")

        pages_text = conn.execute(
            "SELECT page_number, page_text FROM doc_pages WHERE document_id = ? ORDER BY page_number",
            (document_id,),
        ).fetchall()

        outpath = UTIL.get_output_path()
        with open(outpath, "w", encoding="utf-8") as fh:
            for page_number, page_text in pages_text:
                fh.write(f"--- Page {page_number} ---\n{page_text or ''}\n\n")

        print(f"\nFull text of {len(pages_text)} page(s) written to {outpath}")


class DbStatusTool:
    """Print a summary of what's in the SQLite DB (see plan_db.py) - every
    town, its document count, and the file_path/doc_date of each document -
    so DB/working/ state can be checked without ad-hoc sqlite3/python calls
    that fall outside the plan_entry.py permission allowlist.

    Args: [town=<slug>]  (filter to one town, e.g. town=rochester_nh)
    """

    def run_op(self, argmap):
        town_filter = argmap.getStr("town", "")

        conn = DB.get_connection()
        townrows = conn.execute("SELECT id, slug FROM town ORDER BY slug").fetchall()

        for town_id, slug in townrows:
            if town_filter and slug != town_filter:
                continue

            docrows = conn.execute(
                """
                SELECT file_path, doc_date, page_count,
                       (SELECT COUNT(*) FROM keyword_hits WHERE document_id = documents.id),
                       (SELECT COUNT(*) FROM doc_pages WHERE document_id = documents.id),
                       (SELECT COUNT(*) FROM analysis_log WHERE document_id = documents.id)
                FROM documents WHERE town_id = ? ORDER BY doc_date
                """,
                (town_id,),
            ).fetchall()

            print(f"=== {slug} ({len(docrows)} document(s)) ===")
            for file_path, doc_date, page_count, hitcount, textpagecount, logcount in docrows:
                print(f"  {doc_date or '?':10}  {file_path:60}  "
                      f"pages={page_count}  hits={hitcount}  text_pages={textpagecount}  analysis_log={logcount}")

            projrows = conn.execute(
                """
                SELECT id, short_desc, length(full_md_text),
                       (SELECT COUNT(*) FROM project_documents WHERE project_id = projects.id)
                FROM projects WHERE town_id = ? ORDER BY id
                """,
                (town_id,),
            ).fetchall()

            if projrows:
                print(f"  --- {len(projrows)} project(s) ---")
                for project_id, short_desc, mdlen, doccount in projrows:
                    print(f"  #{project_id:<4} {short_desc or '(no short_desc)':60}  "
                          f"md_chars={mdlen or 0}  linked_docs={doccount}")


class UpdateDbTool:
    """Load document registrations from the hardcoded JSON file at
    working/DB_UPDATE.json into the SQLite database (see plan_db.py) -
    a JSON list of {"file_path": "working/<town>/<file>.pdf",
    "source_url": "..." (optional), "date": "YYYY-MM-DD" (optional)}
    objects. Upserts by file_path (and creates each town's row as a side
    effect); safe to re-run.

    Args: (none - edit working/DB_UPDATE.json, then run this)
    """

    def run_op(self, argmap):
        conn = DB.get_connection()
        document_ids = DB.update_documents_from_json(conn)
        print(f"Updated {len(document_ids)} document(s) from {DB.DB_UPDATE_PATH}")


if __name__ == '__main__':

    SETUP.configure(globals())

    mytool, argmap = SETUP.driver_and_argmap()
    mytool.run_op(argmap)