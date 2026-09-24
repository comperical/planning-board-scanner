#!/opt/rawdata/pyworld/KitchenSink/bin/python3

import os
import re
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

    Fails without writing anything if the response isn't a PDF or .docx.
    A 403 "Just a moment..." response means the site blocks non-browser
    requests (Cloudflare) - use a browser download + ClaimDownload instead.

    Args: target=<url>  [dest=working/<dir>]
    """

    def run_op(self, argmap):
        target = argmap.getStr("target", "")
        dest = argmap.getStr("dest", "")
        UTIL.fetch_url(target, dest)


class ClaimDownloadTool:
    """Move a file the playwright-cli browser downloaded (saved under
    working/playwright_output/) into working/<town>/, after checking it's a
    real PDF/.docx and not an error/challenge page. The fallback for sites
    that block FetchUrl outright (Cloudflare "Just a moment..." on every
    non-browser request - kingston, madbury, brentwood): trigger the
    download in-page with a native link click, e.g.

        playwright-cli -s=planscan eval "() => { const a = document.createElement('a'); a.href = '/media/21201'; a.download = ''; document.body.appendChild(a); a.click(); }"

    (a script fetch() gets challenged; a download-attribute link click
    doesn't), then claim the file named in the "Downloaded file ... to"
    event. Prints the new pdf= path for IngestPdfTool.

    Args: file=working/playwright_output/<file>  dest=working/<town>  [name=<new filename>]
    """

    def run_op(self, argmap):
        filearg = argmap.getStr("file", "")
        dest = argmap.getStr("dest", "")
        name = argmap.getStr("name", "")

        outpath = UTIL.claim_download(filearg, dest, name)
        print(f"Moved {filearg} -> pdf={outpath}")


class PdfExtractTextTool:
    """Extract the full text of pdf= (OCR fallback per scanned page; a
    .docx is read directly, no OCR involved) to working/OUTPUT.txt.

    Args: pdf=working/<path>.pdf|.docx
    """

    def run_op(self, argmap):
        pdf = argmap.getStr("pdf", "")
        UTIL.extract_pdf_text(pdf)


class PdfInfoTool:
    """Write a JSON summary of pdf= - metadata, page count, file size, and
    per-page stats (dimensions, text length, whether it looks scanned) - to
    working/OUTPUT.txt. A .docx has no page geometry, so it's always
    reported as a single page.

    Args: pdf=working/<path>.pdf|.docx
    """

    def run_op(self, argmap):
        pdf = argmap.getStr("pdf", "")
        UTIL.extract_pdf_info(pdf)


class PdfKeywordScanTool:
    """Scan pdf='s text for development-project keywords (site plan,
    subdivision, residential, commercial, ...) and write JSON hits with page
    numbers and snippets to working/OUTPUT.txt. Pass keywords=...
    (comma-separated) to override the default list. A .docx has no real
    pages, so any hits are reported as page 1.

    Args: pdf=working/<path>.pdf|.docx  [keywords=a,b,c]
    """

    def run_op(self, argmap):
        pdf = argmap.getStr("pdf", "")
        keywords = argmap.getStr("keywords", UTIL.DEFAULT_SCAN_KEYWORDS)

        UTIL.scan_pdf_keywords(keywords, pdf)


class PdfRenderPagesTool:
    """Render pages of pdf= to PNG images (one file per page) inside
    working/OUTPUT_PAGES/. With no pages= given, renders the whole document
    up to a safety cap (see MAX_RENDER_PAGES_DEFAULT); pass an explicit page
    range to go beyond that on purpose. PDF only - no page-image equivalent
    for .docx.

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
    PdfKeywordScanTool + UpdateDbTool, for wiring a scan's downloaded
    PDFs/docx into the DB without leaving the plan_entry.py allowlist.
    Upserts by file_path (creating the town row as a side effect); safe to
    re-run - a re-scan replaces that document's previously recorded
    pages/keyword hits/text rather than duplicating them.

    Also accepts a .docx file (e.g. towns whose site posts Word documents
    instead of PDFs) - it's read directly (no OCR) and recorded as a
    single-page document, since .docx has no real page boundaries.

    Full-page text extraction (OCR fallback per scanned PDF page, via
    plan_util.get_pdf_page_texts) is the slow step for a large scanned
    packet - pass with_text=false to skip it (PdfInfo/PdfKeywordScan still
    run) and extract text separately/later if needed.

    Pass scan_id=<id> (from StartScanLog) if this file was just discovered
    during a scan pass - it's recorded as documents.first_scan_id, and only
    ever set once (a later re-run without scan_id, or with a different one,
    won't overwrite it).

    Args: pdf=working/<path>.pdf|.docx  [source_url=...]  [date=YYYY-MM-DD]
          [keywords=a,b,c]  [with_text=true]  [scan_id=<id>]
    """

    def run_op(self, argmap):
        pdf = argmap.getStr("pdf", "")
        source_url = argmap.getStr("source_url", "") or None
        date = argmap.getStr("date", "") or None
        keywords = argmap.getStr("keywords", UTIL.DEFAULT_SCAN_KEYWORDS)
        with_text = argmap.getBit("with_text", True)
        scan_id = argmap.getInt("scan_id", -1)

        conn = DB.get_connection()

        if scan_id != -1:
            DB.upsert_document(conn, pdf, source_url=source_url, first_scan_id=scan_id)

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


class StartScanLogTool:
    """Start a new scan_log row for town= - marks the beginning of one pass
    of visiting that town's site and looking for new files to download
    (see plan_db.py's scan_log table; distinct from analysis_log, which
    tracks analyzing an already-downloaded document for projects).
    alpha_time_est is stamped as the current time. Creates the town row as
    a side effect if it doesn't exist yet.

    Prints the new scan_id - pass it as scan_id=<id> to IngestPdfTool for
    every file discovered during this pass (so documents.first_scan_id
    records which scan found it), then run EndScanLog scan_id=<id> once the
    pass is done.

    Args: town=<slug>  [notes=...]
    """

    def run_op(self, argmap):
        town = argmap.getStr("town", "")
        notes = argmap.getStr("notes", "")

        assert town, "town=<slug> is required"

        conn = DB.get_connection()
        scan_id = DB.create_scan_log(conn, town, notes=notes)
        print(f"Started scan_log {scan_id} for {town}. Pass scan_id={scan_id} to IngestPdfTool "
              f"for each newly discovered file, then run EndScanLog scan_id={scan_id} when done.")


class EndScanLogTool:
    """Close out scan_id= (from StartScanLog) - stamps omega_time_est as
    the current time. Pass notes=... to overwrite the scan_log row's notes
    with a summary of what the pass found (e.g. "checked Agenda Center back
    to Jan 2026, found 3 new PDFs") - omitting it leaves any notes already
    set (e.g. from StartScanLog) unchanged.

    Args: scan_id=<id>  [notes=...]
    """

    def run_op(self, argmap):
        scan_id = argmap.getInt("scan_id", -1)
        notes = argmap.getStr("notes", "") or None

        assert scan_id != -1, "scan_id=<id> is required"

        conn = DB.get_connection()
        DB.close_scan_log(conn, scan_id, notes=notes)
        print(f"Closed scan_log {scan_id}" + (f": {notes}" if notes else ""))


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
    (every other updatable field: {"short_desc": "...", "tag_set": [...]} -
    tag_set replaces the project's whole tag set and is validated against
    PROJECT_TAGS.md: known tags only, exactly one sector and one stage tag)
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


class CreateContactTool:
    """Create a new row in the contact_info table (a person or organization
    involved in projects - applicant, owner, engineer, etc) and print its
    id. All fields are optional; link it to projects with LinkContact.

    Args: [name=...]  [phone=...]  [email=...]  [web_site=...]
    """

    def run_op(self, argmap):
        name = argmap.getStr("name", "")
        phone = argmap.getStr("phone", "")
        email = argmap.getStr("email", "")
        web_site = argmap.getStr("web_site", "")

        assert name or phone or email or web_site, \
            "Pass at least one of name=, phone=, email=, web_site="

        conn = DB.get_connection()
        contact_id = DB.create_contact(conn, name, phone, email, web_site)
        print(f"Created contact {contact_id} ({name or '(no name)'}). Link it with "
              f"LinkContact project_id=<id> contact_ids={contact_id}")


class LinkContactTool:
    """Link one project to one or more contacts (contact_project table).
    Every id is checked to exist before anything is written, so a bad id
    links nothing. Safe to re-run - existing links are left as they are.

    Args: project_id=<id>  contact_ids=<id>[,<id>,...]
    """

    def run_op(self, argmap):
        project_id = argmap.getInt("project_id", -1)
        idstr = argmap.getStr("contact_ids", "")

        assert project_id != -1, "project_id=<id> is required"
        contact_ids = [int(s.strip()) for s in idstr.split(",") if s.strip()]
        assert contact_ids, "contact_ids=<id>[,<id>,...] is required"

        conn = DB.get_connection()
        assert conn.execute("SELECT 1 FROM projects WHERE id = ?", (project_id,)).fetchone(), \
            f"No project with id {project_id}"
        missing = [cid for cid in contact_ids
                   if not conn.execute("SELECT 1 FROM contact_info WHERE id = ?", (cid,)).fetchone()]
        assert not missing, f"No contact(s) with id {missing}"

        for contact_id in contact_ids:
            DB.link_contact_project(conn, contact_id, project_id)
        print(f"Linked project {project_id} <-> contact(s) {contact_ids}")


class ShowContactForTownTool:
    """List every contact linked (via contact_project) to at least one
    project in town_id=, with the ids of those projects - so an existing
    contact can be reused with LinkContact instead of creating a duplicate.
    Contacts not yet linked to any project don't appear. Identify the town
    by town= (slug) or town_id= - exactly one of the two.

    Args: town=<slug> | town_id=<id>
    """

    def run_op(self, argmap):
        town = argmap.getStr("town", "")
        town_id = argmap.getInt("town_id", -1)
        assert bool(town) != (town_id != -1), "Pass exactly one of town=<slug> or town_id=<id>"

        conn = DB.get_connection()
        if town:
            townrow = conn.execute("SELECT id, slug FROM town WHERE slug = ?", (town,)).fetchone()
            assert townrow, f"No town with slug {town}"
        else:
            townrow = conn.execute("SELECT id, slug FROM town WHERE id = ?", (town_id,)).fetchone()
            assert townrow, f"No town with id {town_id}"
        town_id, slug = townrow

        rows = conn.execute(
            """
            SELECT c.id, c.name, c.phone, c.email, c.web_site,
                   GROUP_CONCAT(p.id, ',')
            FROM contact_info c
            JOIN contact_project cp ON cp.contact_id = c.id
            JOIN projects p ON p.id = cp.project_id
            WHERE p.town_id = ?
            GROUP BY c.id
            ORDER BY c.name, c.id
            """,
            (town_id,),
        ).fetchall()

        print(f"{len(rows)} contact(s) for town {town_id} ({slug}):")
        for contact_id, name, phone, email, web_site, projids in rows:
            print(f"  #{contact_id:<4} {name or '(no name)'}")
            print(f"        phone={phone or '-'}  email={email or '-'}  web_site={web_site or '-'}  projects={projids}")


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


class NextToScanTool:
    """List towns in the order they should next be re-scanned (checked for
    new files): towns with no scan_log rows first, then by oldest most
    recent scan pass (alpha_time_est). The scan-side counterpart of
    NextToAnalyze. Also lists towninfo/<slug>.md write-ups that have no
    town row in the DB yet, since those have never been scanned either.

    Args: [limit=<n>]  (default 10; 0 = all towns)
    """

    def run_op(self, argmap):
        limit = argmap.getInt("limit", 10)

        conn = DB.get_connection()
        rows = conn.execute(
            """
            SELECT t.slug, MAX(s.alpha_time_est), COUNT(s.id),
                   CAST(julianday('now') - julianday(MAX(s.alpha_time_est)) AS INTEGER)
            FROM town t LEFT JOIN scan_log s ON s.town_id = t.id
            GROUP BY t.id
            ORDER BY MAX(s.alpha_time_est) IS NOT NULL, MAX(s.alpha_time_est), t.slug
            """
        ).fetchall()

        knownset = {slug for slug, _, _, _ in rows}
        infodir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "towninfo")
        # Only <town>_<st>.md files - skips non-town notes like PATTERNS.md
        missing = sorted(fname[:-3] for fname in os.listdir(infodir)
                         if re.fullmatch(r"[a-z_]+_[a-z]{2}\.md", fname) and fname[:-3] not in knownset)

        if missing:
            print(f"{len(missing)} towninfo write-up(s) with no town row in the DB (never scanned):")
            for slug in missing:
                print(f"  {slug}")
            print()

        shown = rows if limit == 0 else rows[:limit]
        print(f"Towns by scan staleness ({len(shown)} of {len(rows)}):")
        for slug, lastscan, scancount, daysago in shown:
            if lastscan is None:
                print(f"  {slug:30}  never scanned")
            else:
                print(f"  {slug:30}  last scan {lastscan}  ({daysago}d ago, {scancount} pass(es))")


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
                       (SELECT COUNT(*) FROM project_documents WHERE project_id = projects.id),
                       tag_set
                FROM projects WHERE town_id = ? ORDER BY id
                """,
                (town_id,),
            ).fetchall()

            if projrows:
                print(f"  --- {len(projrows)} project(s) ---")
                for project_id, short_desc, mdlen, doccount, tag_set in projrows:
                    print(f"  #{project_id:<4} {short_desc or '(no short_desc)':60}  "
                          f"md_chars={mdlen or 0}  linked_docs={doccount}  tags={tag_set or '(untagged)'}")


class RunQueryTool:
    """Run the SQL statement in the hardcoded file working/QUERY.sql against
    the SQLite DB (see plan_db.py for the schema) and print the results as
    tab-separated rows under a header line. The connection is read-only,
    so only SELECT-style queries work - use the dedicated tools to write.
    One statement per file.

    Args: (none - write working/QUERY.sql, then run this)
    """

    def run_op(self, argmap):
        columns, rows = DB.run_query()

        print("\t".join(columns))
        for row in rows:
            print("\t".join("" if v is None else str(v) for v in row))
        print(f"({len(rows)} row(s))")


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

    mytool, _ = SETUP.driver_and_argmap()

    # Re-parse args splitting on the first "=" only - ArgMap.getFromArgv
    # splits on every "=", which truncates URL values with query strings
    # (target=...View.ashx?M=A&ID=... became target=...View.ashx?M).
    argmap = ArgMap.ArgMap()
    for onearg in sys.argv[2:]:
        if "=" in onearg:
            key, val = onearg.split("=", 1)
            argmap.put(key, val)

    mytool.run_op(argmap)