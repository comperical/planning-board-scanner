#!/opt/rawdata/pyworld/KitchenSink/bin/python3

import os
import re
import sys
import warnings

# urllib3 2.x warns on every import that this Python's ssl module is
# LibreSSL - two lines of noise on every tool call. Filtered by message so
# urllib3 needn't be imported here first.
warnings.filterwarnings("ignore", message=r"urllib3 v2\.0 only supports OpenSSL")

import plan_db as DB
import plan_util as UTIL


sys.path.append("/opt/userdata/crm/src/python/opsutil")

import ArgMap
import CodeSetup as SETUP


# ---------------------------------------------------------------------------
# File and document tools.
#
# Each tool takes its input file as pdf=<path>, checked - before any work
# happens - against two rules: it must start with "working/" and it must
# already exist as a file. Output goes to a hardcoded location inside
# working/, so there is no output path for a caller to inject:
#   - working/OUTPUT.txt     (DocDetail's full page text)
#   - working/OUTPUT_PAGES/  (PdfRenderPages, one PNG per page)
#
# Example:
#   plan_entry.py FetchUrl target=https://example.town.gov/2026.09.22_Materials.pdf
#   plan_entry.py DocDetail pdf=working/TARGET.pdf
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
    """Record pdf= in the SQLite database (see plan_db.py): file/page
    stats, development-keyword hits and (by default) the full page text -
    the usual way to register a file found during a scan pass. Upserts by file_path (creating the town row as a side effect); safe to
    re-run - a re-scan replaces that document's previously recorded
    pages/keyword hits/text rather than duplicating them.

    Also accepts a .docx file (e.g. towns whose site posts Word documents
    instead of PDFs) - it's read directly (no OCR) and recorded as a
    single-page document, since .docx has no real page boundaries.

    Full-page text extraction (OCR fallback per scanned PDF page, via
    plan_util.get_pdf_page_texts) is the slow step for a large scanned
    packet - pass with_text=false to skip it (stats and keyword hits are
    still recorded) and re-run later with the text if needed.

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

        info = UTIL.extract_pdf_info(pdf)
        DB.record_pdf_info(conn, pdf, info, source_url=source_url)

        scan = UTIL.scan_pdf_keywords(keywords, pdf)
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

    If the site couldn't be checked (down, blocked, layout changed beyond
    what towninfo describes), start notes with "FAILED" (e.g.
    notes="FAILED: Cloudflare challenge never cleared") - NextToScan
    ignores such passes, so the town is retried on the next run.

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
    afterward (working/project_edit/<id>.md + .json) to fill in short_desc,
    address and the full markdown write-up.

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
    (every other updatable field: {"short_desc": "...", "address": "...",
    "tag_set": [...]} -
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


def _print_contacts(rows, *, reason=False, projects=False):
    """Print contact rows of (id, name, company, phone, email, web_site,
    extra) - extra is a match reason (reason=True) or a CSV of linked
    project ids (projects=True)."""

    for cid, name, company, phone, email, web_site, extra in rows:
        print(f"  #{cid:<4} {DB.contact_label(name, company)}")
        tail = ""
        if reason:
            tail = f"  [{extra}]"
        elif projects:
            tail = f"  projects={extra or '-'}"
        print(f"        phone={phone or '-'}  email={email or '-'}  web_site={web_site or '-'}{tail}")


class FindContactTool:
    """Look up existing contacts before creating one.
      - q=<text>: case-insensitive substring search over name, company,
        phone, email and web site.
      - town=<slug>: contacts linked to at least one project in that town
        (combine with q= to narrow).
      - name=/company=: the fuzzy duplicate check CreateContact runs
        (shared distinctive company word or surname).
    q=/town= hits list each contact's linked projects.

    Args: [q=<text>] [town=<slug>] | [name=...] [company=...]
    """

    def run_op(self, argmap):
        text = argmap.getStr("q", "")
        town = argmap.getStr("town", "")
        name = argmap.getStr("name", "")
        company = argmap.getStr("company", "")
        assert bool(text or town) != bool(name or company), \
            "Pass q=/town=, or name=/company= (not both)"

        conn = DB.get_connection()
        if text or town:
            if town:
                assert conn.execute("SELECT 1 FROM town WHERE slug = ?", (town,)).fetchone(), \
                    f"No town with slug {town}"
            rows = DB.search_contacts(conn, text, town)
            scope = " and ".join(x for x in (f"matching {text!r}" if text else "", f"used in {town}" if town else "") if x)
            print(f"{len(rows)} contact(s) {scope}:")
            _print_contacts(rows, projects=True)
        else:
            rows = DB.find_similar_contacts(conn, name, company)
            print(f"{len(rows)} possibly-matching contact(s):")
            _print_contacts(rows, reason=True)


class CreateContactTool:
    """Create a new row in the contact_info table (a person or organization
    involved in projects - applicant, owner, engineer, etc) and print its
    id. name= is the person and company= their firm - for an organization
    with no known person, fill in company= and leave name= blank. All
    fields are optional; link it to projects with LinkContact.

    Before creating, checks for existing contacts that look like the same
    person or firm (a shared distinctive company word or surname - see
    FindContact). If any turn up, nothing is created and they're listed:
    reuse one with LinkContact, or re-run with force=true when it really is
    new (e.g. a new person at a firm already on file).

    Args: [name=...]  [company=...]  [phone=...]  [email=...]  [web_site=...]  [force=true]
    """

    def run_op(self, argmap):
        name = argmap.getStr("name", "")
        company = argmap.getStr("company", "")
        phone = argmap.getStr("phone", "")
        email = argmap.getStr("email", "")
        web_site = argmap.getStr("web_site", "")
        force = argmap.getStr("force", "false").lower() == "true"

        assert name or company or phone or email or web_site, \
            "Pass at least one of name=, company=, phone=, email=, web_site="

        conn = DB.get_connection()
        if not force:
            similar = DB.find_similar_contacts(conn, name, company)
            if similar:
                print("NOT created - possible existing contact(s):")
                _print_contacts(similar, reason=True)
                print("Reuse one with LinkContact, or re-run with force=true if this is really new "
                      "(e.g. a new person at an existing firm - copy its phone/web_site).")
                sys.exit(1)

        contact_id = DB.create_contact(conn, name, phone, email, web_site, company=company)
        print(f"Created contact {contact_id} ({DB.contact_label(name, company)}). Link it with "
              f"LinkContact project_id=<id> contact_ids={contact_id}")


class LinkContactTool:
    """Link one project to one or more contacts (contact_project table).
    Every id is checked to exist before anything is written, so a bad id
    links nothing. Safe to re-run - existing links are left as they are.

    Args: project_id=<id>  contact_ids=<id>[,<id>,...]
    """

    def run_op(self, argmap):
        project_id = argmap.getInt("project_id", -1)
        contact_ids = DB.parse_ids(argmap.getStr("contact_ids", ""), "contact_ids")

        conn = DB.get_connection()
        DB.require_projects(conn, [project_id])
        DB.require_contacts(conn, contact_ids)

        for contact_id in contact_ids:
            DB.link_contact_project(conn, contact_id, project_id)
        print(f"Linked project {project_id} <-> contact(s) {contact_ids}")


class UnlinkContactTool:
    """Remove links between one project and one or more contacts - to undo
    a wrong LinkContact. The contacts themselves are kept.

    Args: project_id=<id>  contact_ids=<id>[,<id>,...]
    """

    def run_op(self, argmap):
        project_id = argmap.getInt("project_id", -1)
        contact_ids = DB.parse_ids(argmap.getStr("contact_ids", ""), "contact_ids")

        conn = DB.get_connection()
        DB.require_projects(conn, [project_id])
        for contact_id in contact_ids:
            removed = DB.unlink_contact_project(conn, contact_id, project_id)
            print(f"{'Unlinked' if removed else 'No link between'} project {project_id} and contact {contact_id}")


class MergeContactsTool:
    """Fold a duplicate contact into another: drop='s project links move to
    keep=, any field blank on keep= is filled from drop=, then drop= is
    deleted. To change a contact's fields directly, use Upsert
    table=contact_info with an "id" key instead.

    Args: keep=<id>  drop=<id>
    """

    def run_op(self, argmap):
        keep_id = argmap.getInt("keep", -1)
        drop_id = argmap.getInt("drop", -1)
        assert keep_id != -1 and drop_id != -1, "keep=<id> and drop=<id> are required"

        conn = DB.get_connection()
        moved, filled = DB.merge_contacts(conn, keep_id, drop_id)
        print(f"Merged contact {drop_id} into {keep_id}: moved {len(moved)} project link(s) {moved}"
              + (f", filled {filled}" if filled else "") + f"; deleted {drop_id}")


class BatchContactOpsTool:
    """Apply many contact-search writes at once from the hardcoded JSON file
    working/CONTACT_OPS.json - a list of create / link / log operations,
    validated in full and then applied in one transaction (a bad batch
    writes nothing). Creates get the same duplicate check as CreateContact
    ("force": true to override) and can carry a "ref" that later link ops
    use in place of the new id:

        [
          {"op": "create", "ref": "gpi", "name": "Pat McLaughlin, PE",
           "company": "GPI / Greenman-Pedersen, Inc.", "web_site": "https://www.gpinet.com"},
          {"op": "link", "project_id": 164, "contact_ids": ["gpi", 204]},
          {"op": "log", "project_id": 164, "outcome": "found", "notes": "GPI (new), Volta Oil (reused)"},
          {"op": "log", "project_ids": [502, 501, 486], "outcome": "skipped",
           "notes": "non-construction"}
        ]

    Args: (none - write working/CONTACT_OPS.json, then run this)
    """

    def run_op(self, argmap):
        ops = DB.read_input(DB.CONTACT_OPS_PATH, as_json=True)
        conn = DB.get_connection()
        try:
            results = DB.apply_contact_ops(conn, ops)
        except AssertionError as err:
            print(err)
            sys.exit(1)
        for line in results:
            print(line)
        print(f"Applied {len(results)} op(s) from {DB.CONTACT_OPS_PATH}")


class LogContactSearchTool:
    """Record a contact-search pass over a project (contact_search_log
    table) - call it once per project at the end of every contact-search
    pass, whatever the result. outcome= is 'found' (contacts created or
    linked), 'none_found' (searched, nothing usable) or 'skipped' (not
    worth searching, e.g. a bare trust name on a lot line adjustment).
    NextForContactSearch holds back none_found/skipped projects until
    retry_days pass or a new document is linked to them.

    project_ids= logs the same outcome and notes for several projects at
    once (e.g. a run of non-construction skips); every id is checked
    first, so a bad id logs nothing.

    Args: project_id=<id> | project_ids=<id>,<id>,...  outcome=found|none_found|skipped  [notes=...]
    """

    def run_op(self, argmap):
        project_id = argmap.getInt("project_id", -1)
        idstr = argmap.getStr("project_ids", "")
        outcome = argmap.getStr("outcome", "")
        notes = argmap.getStr("notes", "")

        assert (project_id != -1) != bool(idstr), "Pass exactly one of project_id=<id> or project_ids=<ids>"
        project_ids = [project_id] if project_id != -1 else DB.parse_ids(idstr, "project_ids")

        conn = DB.get_connection()
        DB.require_projects(conn, project_ids)
        assert outcome in DB.CONTACT_SEARCH_OUTCOMES, \
            f"outcome must be one of {DB.CONTACT_SEARCH_OUTCOMES}, got {outcome!r}"

        with conn:
            for pid in project_ids:
                DB.log_contact_search(conn, pid, outcome, notes, commit=False)
        label = f"project {project_ids[0]}" if len(project_ids) == 1 else f"{len(project_ids)} projects {project_ids}"
        print(f"Logged contact search for {label}: {outcome}" + (f" - {notes}" if notes else ""))


class NextForContactSearchTool:
    """List projects due for a contact search: no linked contacts, not
    tagged non-construction, and either never searched, last searched
    retry_days= or more ago, or linked to a new document since the last
    search. Never-searched projects first, newest project first within
    each group; large_first=true puts `large` projects ahead of everything.
    Prints the last search's outcome/notes for retries.

    Args: [limit=<n>] (default 10)  [retry_days=<n>] (default 30)
          [large_first=true]  [include_noncon=true]  [town=<slug>]
    """

    def run_op(self, argmap):
        limit = argmap.getInt("limit", 10)
        retry_days = argmap.getInt("retry_days", 30)
        large_first = argmap.getBit("large_first", False)
        include_noncon = argmap.getBit("include_noncon", False)
        town = argmap.getStr("town", "")

        conn = DB.get_connection()
        rows = DB.contact_search_candidates(
            conn, limit=limit, retry_days=retry_days, large_first=large_first,
            include_noncon=include_noncon, town=town)

        if not rows:
            print("No projects due for a contact search" + (f" in {town}" if town else "") + ".")
            return

        print(f"{len(rows)} project(s) due for a contact search:")
        for project_id, slug, tags, desc, last_at, last_outcome, last_notes in rows:
            print(f"  #{project_id:<4} {slug:<20} {desc}")
            print(f"        tags={tags or '-'}")
            if last_at:
                print(f"        last search {last_at}: {last_outcome}" + (f" - {last_notes}" if last_notes else ""))


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
    recent *good* scan pass (alpha_time_est). A pass only counts as good if
    it was closed with EndScanLog and its notes don't start with "FAILED" -
    so a town whose site was down or blocked comes straight back up next
    time. The scan-side counterpart of NextToAnalyze. Also lists
    towninfo/<slug>.md write-ups that have no town row in the DB yet, since
    those have never been scanned either.

    Args: [limit=<n>]  (default 10; 0 = all towns)
          [due_days=<n>]  (only towns whose last good scan is at least n days old; default 0 = no filter)
          [daily=true]  (the daily-update quota: the ceil(N/7) stalest towns, N = towns
                      in the DB, skipping any with a good scan in the last 24h - so
                      fewer only when nearly every town was scanned that recently.
                      Overrides limit= and due_days=)
    """

    def run_op(self, argmap):
        limit = argmap.getInt("limit", 10)
        due_days = argmap.getInt("due_days", 0)
        daily = argmap.getBit("daily", False)

        conn = DB.get_connection()
        rows = conn.execute(
            """
            SELECT t.slug, MAX(s.alpha_time_est), COUNT(s.id),
                   julianday('now') - julianday(MAX(s.alpha_time_est))
            FROM town t LEFT JOIN scan_log s ON s.town_id = t.id
                 AND s.omega_time_est IS NOT NULL
                 AND COALESCE(s.notes, '') NOT LIKE 'FAILED%'
            GROUP BY t.id
            ORDER BY MAX(s.alpha_time_est) IS NOT NULL, MAX(s.alpha_time_est), t.slug
            """
        ).fetchall()
        knownset = {slug for slug, _, _, _ in rows}
        if daily:
            limit = -(-len(rows) // 7)
            due_days = 0
            rows = [r for r in rows if r[3] is None or r[3] >= 1]
        # 0.25 day of slack, so a town scanned at 10am a week ago still counts as
        # due at 7am today (daily runs won't start at the same time every day).
        if due_days > 0:
            rows = [r for r in rows if r[3] is None or r[3] >= due_days - 0.25]
        rows = [(slug, last, count, None if days is None else int(days)) for slug, last, count, days in rows]

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
        duenote = f", due = last good scan >= {due_days}d ago" if due_days > 0 else ""
        if daily:
            duenote = f", daily quota = ceil({len(knownset)}/7) = {limit}, skipping towns scanned in the last 24h"
        print(f"Towns by scan staleness ({len(shown)} of {len(rows)}{duenote}):")
        for slug, lastscan, scancount, daysago in shown:
            if lastscan is None:
                print(f"  {slug:30}  never scanned")
            else:
                print(f"  {slug:30}  last good scan {lastscan}  ({daysago}d ago, {scancount} good pass(es))")


class DailyReportTool:
    """Summarize the last hours= of activity (default 24) - the closing
    step of the daily-update skill: every scan pass (FAILED/unclosed ones
    first), documents newly discovered by those passes and whether they've
    been analyzed, projects created, projects whose tags/short_desc changed
    (e.g. a stage tag moving in-review -> approved), contact searches
    (contact_search_log, with the none_found/skipped ones listed), and
    what's still outstanding (unanalyzed documents, towns still due for a
    scan, projects due for a contact search).

    Args: [hours=<n>]  (default 24)  [due_days=<n>]  (default 7, for the "still due" count)
    """

    def run_op(self, argmap):
        hours = argmap.getInt("hours", 24)
        due_days = argmap.getInt("due_days", 7)
        since = f"-{hours} hours"

        conn = DB.get_connection()

        scans = conn.execute(
            """
            SELECT s.id, t.slug, s.alpha_time_est, s.omega_time_est, COALESCE(s.notes, ''),
                   (SELECT COUNT(*) FROM documents d WHERE d.first_scan_id = s.id)
            FROM scan_log s JOIN town t ON s.town_id = t.id
            WHERE s.alpha_time_est >= datetime('now', ?)
            ORDER BY s.alpha_time_est
            """, (since,)).fetchall()

        def isbad(scan):
            return scan[3] is None or scan[4].startswith("FAILED")

        bad = [sc for sc in scans if isbad(sc)]
        print(f"# Daily report - last {hours}h")
        print()
        print(f"## Scans: {len(scans)} pass(es), {len(bad)} failed/unclosed, "
              f"{sum(sc[5] for sc in scans)} new document(s)")
        for scan_id, slug, _, omega, notes, newdocs in bad + [sc for sc in scans if not isbad(sc)]:
            flag = "UNCLOSED " if omega is None else ""
            print(f"- {flag}{slug} (scan {scan_id}, {newdocs} new): {notes}")
        print()

        docs = conn.execute(
            """
            SELECT d.file_path, t.slug, d.doc_date,
                   (SELECT COUNT(*) FROM analysis_log a WHERE a.document_id = d.id),
                   (SELECT notes FROM analysis_log a WHERE a.document_id = d.id ORDER BY a.id DESC LIMIT 1)
            FROM documents d JOIN town t ON d.town_id = t.id
            JOIN scan_log s ON d.first_scan_id = s.id
            WHERE s.alpha_time_est >= datetime('now', ?)
            ORDER BY t.slug, d.doc_date
            """, (since,)).fetchall()
        print(f"## New documents: {len(docs)}")
        for path, slug, docdate, nanalysis, notes in docs:
            status = f"analyzed: {notes}" if nanalysis else "NOT YET ANALYZED"
            print(f"- {slug} {docdate or '?'} {path} - {status}")
        print()

        newprojects = conn.execute(
            """
            SELECT p.id, t.slug, COALESCE(p.short_desc, ''), COALESCE(p.tag_set, '')
            FROM projects p JOIN town t ON p.town_id = t.id
            WHERE p.created_at >= datetime('now', ?)
            ORDER BY t.slug, p.id
            """, (since,)).fetchall()
        print(f"## New projects: {len(newprojects)}")
        for project_id, slug, desc, tags in newprojects:
            print(f"- #{project_id} {slug}: {desc}  [{tags}]")
        print()

        # First and last value per (project, field) within the window, for
        # projects that existed before it (new ones are covered above).
        changes = conn.execute(
            """
            SELECT h.project_id, t.slug, COALESCE(p.short_desc, ''), h.field,
                   (SELECT old_value FROM project_history h2 WHERE h2.project_id = h.project_id
                        AND h2.field = h.field AND h2.changed_at >= datetime('now', ?) ORDER BY h2.id LIMIT 1),
                   (SELECT new_value FROM project_history h2 WHERE h2.project_id = h.project_id
                        AND h2.field = h.field AND h2.changed_at >= datetime('now', ?) ORDER BY h2.id DESC LIMIT 1)
            FROM project_history h
            JOIN projects p ON h.project_id = p.id
            JOIN town t ON p.town_id = t.id
            WHERE h.changed_at >= datetime('now', ?)
              AND (p.created_at IS NULL OR p.created_at < datetime('now', ?))
            GROUP BY h.project_id, h.field
            ORDER BY t.slug, h.project_id, h.field DESC
            """, (since, since, since, since)).fetchall()
        changedids = sorted({c[0] for c in changes})
        print(f"## Updated projects: {len(changedids)}")
        for project_id, slug, desc, field, oldval, newval in changes:
            if oldval == newval:
                continue
            if field == "tag_set":
                oldset = set(filter(None, (oldval or "").split(",")))
                newset = set(filter(None, (newval or "").split(",")))
                diff = " ".join([f"+{t}" for t in sorted(newset - oldset)] + [f"-{t}" for t in sorted(oldset - newset)])
                print(f"- #{project_id} {slug}: {desc}  tags {diff}")
            else:
                print(f"- #{project_id} {slug}: short_desc was \"{oldval}\"")
        print()

        searches = conn.execute(
            """
            SELECT l.project_id, t.slug, COALESCE(p.short_desc, ''), l.outcome, COALESCE(l.notes, '')
            FROM contact_search_log l
            JOIN projects p ON l.project_id = p.id
            JOIN town t ON p.town_id = t.id
            WHERE l.searched_at >= datetime('now', ?)
            ORDER BY l.outcome, t.slug, l.project_id
            """, (since,)).fetchall()
        bytype = {o: sum(1 for s in searches if s[3] == o) for o in DB.CONTACT_SEARCH_OUTCOMES}
        print(f"## Contact searches: {len(searches)} "
              f"({bytype['found']} found, {bytype['none_found']} none found, {bytype['skipped']} skipped)")
        for project_id, slug, desc, outcome, notes in searches:
            if outcome != "found":
                print(f"- #{project_id} {slug}: {outcome}" + (f" - {notes}" if notes else ""))
        print()

        unanalyzed = conn.execute(
            "SELECT COUNT(*) FROM documents d WHERE NOT EXISTS (SELECT 1 FROM analysis_log a WHERE a.document_id = d.id)"
        ).fetchone()[0]
        contactdue = len(DB.contact_search_candidates(conn, limit=-1))
        stilldue = conn.execute(
            """
            SELECT COUNT(*) FROM (
                SELECT t.id, MAX(s.alpha_time_est) AS lastgood
                FROM town t LEFT JOIN scan_log s ON s.town_id = t.id
                     AND s.omega_time_est IS NOT NULL
                     AND COALESCE(s.notes, '') NOT LIKE 'FAILED%'
                GROUP BY t.id)
            WHERE lastgood IS NULL OR julianday('now') - julianday(lastgood) >= ? - 0.25
            """, (due_days,)).fetchone()[0]
        print("## Outstanding")
        print(f"- {unanalyzed} document(s) not yet analyzed")
        print(f"- {stilldue} town(s) still due for a scan (last good scan >= {due_days}d ago)")
        print(f"- {contactdue} project(s) due for a contact search")


class DocDetailTool:
    """Print what's known about pdf= - town/date/size/source and keyword
    hits - and write its full page text to working/OUTPUT.txt (it can be
    long; Read that file). The one call an analysis pass needs after
    NextToAnalyze picks a document.

    For an ingested document everything comes from the DB (no PDF work).
    For a file not ingested yet - e.g. working/TARGET.pdf fetched to check
    whether it's worth keeping - it's read live instead (page stats, a
    keyword scan, and text with OCR fallback) and nothing is recorded; run
    IngestPdf to keep it.

    Args: pdf=working/<path>.pdf|.docx  [keywords=a,b,c]  (live read only)
    """

    def run_op(self, argmap):
        pdf = argmap.getStr("pdf", "")
        keywords = argmap.getStr("keywords", UTIL.DEFAULT_SCAN_KEYWORDS)

        conn = DB.get_connection()
        row = conn.execute(
            """
            SELECT d.id, d.doc_date, d.file_size_bytes, d.page_count, d.source_url, t.slug
            FROM documents d LEFT JOIN town t ON d.town_id = t.id
            WHERE d.file_path = ?
            """,
            (pdf,),
        ).fetchone()

        if row is not None:
            document_id, doc_date, size, pages, source_url, slug = row
            print(f"town={slug}  date={doc_date or '?'}  pages={pages}  size={size} bytes")
            print(f"source_url={source_url or '?'}")
            hits = conn.execute(
                "SELECT page_number, keyword, count, snippet FROM keyword_hits "
                "WHERE document_id = ? ORDER BY page_number", (document_id,),
            ).fetchall()
            page_texts = [(num, text or "") for num, text in conn.execute(
                "SELECT page_number, page_text FROM doc_pages WHERE document_id = ? ORDER BY page_number",
                (document_id,))]
        else:
            info = UTIL.extract_pdf_info(pdf)
            scanned = sum(1 for pg in info["pages"] if not pg["has_selectable_text"])
            print(f"NOT INGESTED - read live from the file (run IngestPdf pdf={pdf} to record it)")
            print(f"pages={info['page_count']}  scanned_pages={scanned}  size={info['file_size_bytes']} bytes")
            hits = [(h["page"], h["keyword"], h["count"], h["snippet"])
                    for h in UTIL.scan_pdf_keywords(keywords, pdf)["hits"]]
            page_texts = list(enumerate(UTIL.get_pdf_page_texts(pdf), 1))

        print(f"\n{len(hits)} keyword hit(s):")
        for page_number, keyword, count, snippet in hits:
            print(f"  p{page_number}  {keyword} x{count}  {snippet}")

        outpath = UTIL.get_output_path()
        with open(outpath, "w", encoding="utf-8") as fh:
            for page_number, page_text in page_texts:
                fh.write(f"--- Page {page_number} ---\n{page_text}\n\n")

        print(f"\nFull text of {len(page_texts)} page(s) written to {outpath}")


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


class UpsertTool:
    """Create or update one row of table= from the hardcoded JSON file
    working/UPSERT.json - a single object whose keys are exactly that
    table's column names, e.g. for table=contact_info:

        {"name": "Jane Smith, PE", "company": "Acme Engineering, LLC", "phone": "(603) 555-1234"}

    With an "id" key, that existing row is updated (only the columns given
    change). Without one, a new row is created with id = MAX(id) + 1, and
    the new id is printed. Unknown column names are rejected.

    Args: table=<table name>
    """

    def run_op(self, argmap):
        table = argmap.getStr("table", "")
        assert table, "table=<table name> is required"

        record = DB.read_input(DB.UPSERT_PATH, as_json=True)
        conn = DB.get_connection()
        row_id, created = DB.upsert_row(conn, table, record)

        if created:
            print(f"Created {table} row with id {row_id}")
        else:
            print(f"Updated {table} row {row_id}: {', '.join(k for k in record if k != 'id')}")


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