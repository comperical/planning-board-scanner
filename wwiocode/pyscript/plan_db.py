"""SQLite storage for planning-board-scanner results.

This is deliberately separate from plan_util.py (which does the PDF work
itself, driven by plan_entry.py's tools). This module owns the database:
schema, connection handling, and functions to record the JSON that
PdfInfoTool / PdfKeywordScanTool write to working/OUTPUT.txt.

Nothing here is wired into plan_entry.py yet - call these functions
directly (e.g. from a one-off script or a Python REPL) for now:

    import plan_db as DB
    conn = DB.get_connection()
    DB.record_pdf_info(conn, "working/dover_nh/2026.09.22.Materials.pdf",
                        json.load(open("working/OUTPUT.txt")))

The database file lives at /opt/userdata/db4widget/dburfoot/PLANSCAN_DB.sqlite
- outside the repo entirely, alongside this user's other db4widget SQLite
databases (FINANCE_DB, LIFE_DB, etc). It holds *raw* scan output (one row
per document, one row per keyword hit) so scans are queryable and
de-duplicated - no manual curation step.

Schema policy (for compatibility with another system that consumes these
DBs): every table's single primary key column must be named exactly "id"
(INTEGER PRIMARY KEY, so it's also the SQLite rowid). Any other uniqueness
requirement (e.g. one row per document+page) must be a plain UNIQUE
constraint, never a composite/renamed primary key - keep this in mind when
adding tables or columns here.
"""

import json
import re
import sqlite3

from pathlib import Path

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

PROJECT_ROOT = Path(__file__).parent.parent.parent
WORK_DIR = PROJECT_ROOT / "working"

DB_PATH = Path("/opt/userdata/db4widget/dburfoot/PLANSCAN_DB.sqlite")

# Hardcoded input for the UpdateDb tool (plan_entry.py) - a JSON list of
# document registrations to load into the documents table. See
# update_documents_from_json() for the expected shape.
DB_UPDATE_PATH = WORK_DIR / "DB_UPDATE.json"

# Hardcoded input for the RunQuery tool (plan_entry.py) - one SQL statement,
# run against a read-only connection.
QUERY_PATH = WORK_DIR / "QUERY.sql"

# Naming convention for editing a project by hand (see the ApplyProjectEdit
# tool in plan_entry.py / sync_project_from_files() below): to update
# project <id>, write working/project_edit/<id>.md (the full_md_text field
# - free-form markdown) and/or working/project_edit/<id>.json (every other
# updatable field: {"short_desc": "...", "tag_set": [...]}), then run the tool
# to apply both to the DB. Either file may be omitted to leave that side
# unchanged.
PROJECT_EDIT_DIR = WORK_DIR / "project_edit"

# The controlled vocabulary for projects.tag_set - parsed from this file's
# tag tables (see load_tag_vocabulary), so the doc is the single source of
# truth for which tags exist.
PROJECT_TAGS_PATH = WORK_DIR.parent / "PROJECT_TAGS.md"

# Tag groups (the "### N. ..." sections of PROJECT_TAGS.md) that must have
# exactly one tag on every tagged project.
EXACTLY_ONE_TAG_GROUPS = {1: "sector", 4: "stage"}


SCHEMA = """
CREATE TABLE IF NOT EXISTS town (
    id                  INTEGER PRIMARY KEY,
    slug                TEXT NOT NULL UNIQUE,  -- e.g. "dover_nh", matches working/<slug>/ and towninfo/<slug>.md
    name                TEXT,                  -- e.g. "Dover"
    state               TEXT                   -- e.g. "NH"
);

-- One row per pass of scanning a town's site: visiting its pages and
-- looking for new files to download - as opposed to analysis_log, which is
-- about analyzing an already-downloaded document for real estate projects.
-- alpha_time_est/omega_time_est are the estimated start/end of the scan
-- (Greek alpha/omega, i.e. "first"/"last") - estimates, not necessarily
-- exact, since a scan is an interactive process (clicking through pages,
-- following links) rather than one atomic operation with a precise
-- start/end timestamp.
CREATE TABLE IF NOT EXISTS scan_log (
    id                  INTEGER PRIMARY KEY,
    town_id             INTEGER NOT NULL REFERENCES town(id),
    alpha_time_est      TEXT,              -- UTC estimate of when the scan pass began
    omega_time_est      TEXT,              -- UTC estimate of when the scan pass ended
    notes               TEXT               -- e.g. "checked Agenda Center back to Jan 2026, found 3 new PDFs"
);

CREATE TABLE IF NOT EXISTS documents (
    id                  INTEGER PRIMARY KEY,
    file_path           TEXT NOT NULL UNIQUE,  -- e.g. "working/dover_nh/2026.09.22.Materials.pdf"
    town_id             INTEGER REFERENCES town(id),
    doc_date            TEXT,                  -- ISO "YYYY-MM-DD", e.g. the meeting date
    source_url          TEXT,                  -- original download URL, if known
    file_size_bytes     INTEGER,
    page_count          INTEGER,
    metadata_json       TEXT,                  -- PDF metadata dict (PdfInfo), as JSON text
    info_scanned_at     TEXT,                  -- UTC timestamp of the last PdfInfo recording
    keywords_scanned_at TEXT,                  -- UTC timestamp of the last keyword-scan recording
    first_scan_id       INTEGER REFERENCES scan_log(id)  -- the scan_log pass that first discovered this file
);

CREATE TABLE IF NOT EXISTS pages (
    id                  INTEGER PRIMARY KEY,
    document_id         INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    page_number         INTEGER NOT NULL,  -- 1-indexed
    width               REAL,
    height              REAL,
    text_chars          INTEGER,
    has_selectable_text INTEGER,           -- 0/1
    UNIQUE(document_id, page_number)
);

CREATE TABLE IF NOT EXISTS keyword_hits (
    id                  INTEGER PRIMARY KEY,
    document_id         INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    page_number         INTEGER NOT NULL,  -- 1-indexed
    keyword             TEXT NOT NULL,
    count               INTEGER NOT NULL,
    snippet             TEXT
);

CREATE TABLE IF NOT EXISTS doc_pages (
    id                  INTEGER PRIMARY KEY,
    document_id         INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    page_number         INTEGER NOT NULL,  -- 1-indexed
    page_text           TEXT,              -- full extracted text of this page (OCR fallback if scanned)
    UNIQUE(document_id, page_number)
);

-- A "project" is a real development (a specific site plan, subdivision,
-- etc.) identified by hand from one or more documents/keyword hits - unlike
-- every other table above, these rows aren't produced automatically by a
-- scan tool. short_desc/full_md_text are curated by whoever spots the
-- project (e.g. "150 Portsmouth Blvd - 3-building 6-story multifamily").
CREATE TABLE IF NOT EXISTS projects (
    id                  INTEGER PRIMARY KEY,
    town_id             INTEGER REFERENCES town(id),
    short_desc          TEXT,              -- one-line summary, e.g. "150 Portsmouth Blvd - 3-building multifamily"
    full_md_text        TEXT,              -- full markdown write-up: description, status, addresses, applicant, etc.
    tag_set             TEXT DEFAULT ''    -- comma-separated set of tags, e.g. "residential,multifamily"; '' = no tags
);

-- Links a project to every document that mentions it (a project is
-- typically referenced across several meetings - an agenda, then minutes,
-- then a later extension/approval).
CREATE TABLE IF NOT EXISTS project_documents (
    id                  INTEGER PRIMARY KEY,
    project_id          INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    document_id         INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    page_number         INTEGER,           -- 1-indexed page where the project is first mentioned in this document
    UNIQUE(project_id, document_id)
);

-- One row per pass of manual/human analysis over a document (as opposed to
-- keyword_hits/doc_pages, which are produced automatically by a scan) -
-- e.g. "read pages 40-60 for the site plan, nothing new past project #3".
CREATE TABLE IF NOT EXISTS analysis_log (
    id                  INTEGER PRIMARY KEY,
    document_id         INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    logged_at           TEXT NOT NULL,  -- UTC timestamp, datetime('now')
    notes               TEXT
);

-- A person or organization involved in projects (applicant, owner,
-- engineer, attorney, etc). Curated by hand, like projects.
CREATE TABLE IF NOT EXISTS contact_info (
    id                  INTEGER PRIMARY KEY,
    name                TEXT,              -- e.g. "Jane Smith" or "Acme Engineering LLC"
    phone               TEXT,
    email               TEXT,
    web_site            TEXT
);

-- Many-to-many link between contacts and projects.
CREATE TABLE IF NOT EXISTS contact_project (
    id                  INTEGER PRIMARY KEY,
    contact_id          INTEGER NOT NULL REFERENCES contact_info(id) ON DELETE CASCADE,
    project_id          INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE(contact_id, project_id)
);

CREATE INDEX IF NOT EXISTS idx_scan_log_town ON scan_log(town_id);
CREATE INDEX IF NOT EXISTS idx_documents_town ON documents(town_id);
CREATE INDEX IF NOT EXISTS idx_pages_document ON pages(document_id);
CREATE INDEX IF NOT EXISTS idx_keyword_hits_document ON keyword_hits(document_id);
CREATE INDEX IF NOT EXISTS idx_keyword_hits_keyword ON keyword_hits(keyword);
CREATE INDEX IF NOT EXISTS idx_doc_pages_document ON doc_pages(document_id);
CREATE INDEX IF NOT EXISTS idx_projects_town ON projects(town_id);
CREATE INDEX IF NOT EXISTS idx_project_documents_project ON project_documents(project_id);
CREATE INDEX IF NOT EXISTS idx_project_documents_document ON project_documents(document_id);
CREATE INDEX IF NOT EXISTS idx_analysis_log_document ON analysis_log(document_id);
CREATE INDEX IF NOT EXISTS idx_contact_project_contact ON contact_project(contact_id);
CREATE INDEX IF NOT EXISTS idx_contact_project_project ON contact_project(project_id);
"""


def get_connection(db_path=DB_PATH):
    """Open (creating if needed) the SQLite database and ensure the schema
    exists. Enables foreign keys, since SQLite leaves that off by default."""

    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    _run_migrations(conn)
    conn.commit()
    return conn


def _run_migrations(conn):
    """CREATE TABLE IF NOT EXISTS (in SCHEMA above) only helps brand-new
    databases - it does nothing for a column added to a table that already
    exists on disk. Any such column gets a one-off ALTER TABLE here, guarded
    by a check so it's safe to call on every connection."""

    cols = {row[1] for row in conn.execute("PRAGMA table_info(project_documents)")}
    if "page_number" not in cols:
        conn.execute("ALTER TABLE project_documents ADD COLUMN page_number INTEGER")

    cols = {row[1] for row in conn.execute("PRAGMA table_info(documents)")}
    if "first_scan_id" not in cols:
        conn.execute("ALTER TABLE documents ADD COLUMN first_scan_id INTEGER REFERENCES scan_log(id)")

    cols = {row[1] for row in conn.execute("PRAGMA table_info(projects)")}
    if "tag_set" not in cols:
        conn.execute("ALTER TABLE projects ADD COLUMN tag_set TEXT DEFAULT ''")

    # Index creation deferred here (rather than in SCHEMA) since the column
    # above may not exist yet on an older database at the point SCHEMA runs.
    conn.execute("CREATE INDEX IF NOT EXISTS idx_documents_first_scan ON documents(first_scan_id)")


def _town_slug_from_path(file_path):
    """Best-effort town slug from a "working/<town>/<file>.pdf" path, e.g.
    "working/dover_nh/x.pdf" -> "dover_nh". Returns None for paths that
    don't fit that shape (e.g. "working/TARGET.pdf")."""

    parts = Path(file_path).parts
    if len(parts) >= 3 and parts[0] == "working":
        return parts[1]
    return None


def get_or_create_town(conn, slug):
    """Ensure a town row exists for slug (e.g. "dover_nh") and return its
    id. name/state are guessed from the slug's "..._<state>" shape on first
    creation (e.g. "north_hampton_nh" -> name "North Hampton", state "NH")
    - edit the row by hand afterward if that guess is wrong."""

    row = conn.execute("SELECT id FROM town WHERE slug = ?", (slug,)).fetchone()
    if row:
        return row[0]

    words = slug.split("_")
    state = words[-1].upper() if len(words) > 1 else None
    name = " ".join(w.capitalize() for w in (words[:-1] if state else words))

    cur = conn.execute(
        "INSERT INTO town (slug, name, state) VALUES (?, ?, ?)",
        (slug, name, state),
    )
    return cur.lastrowid


def create_scan_log(conn, town_slug, *, alpha_time_est=None, notes=""):
    """Create a new scan_log row for town_slug (creates the town row as a
    side effect, like create_project) and return its id - the start of one
    pass of visiting that town's site and looking for new files to
    download, distinct from analysis_log (which is about analyzing an
    already-downloaded document for real estate projects). alpha_time_est
    defaults to the current UTC time (per SQLite's datetime('now')) unless
    given explicitly. Close the pass out with close_scan_log/
    update_scan_log once it's done."""

    town_id = get_or_create_town(conn, town_slug)

    cur = conn.execute(
        "INSERT INTO scan_log (town_id, alpha_time_est, notes) "
        "VALUES (?, COALESCE(?, datetime('now')), ?)",
        (town_id, alpha_time_est, notes),
    )
    conn.commit()
    return cur.lastrowid


def close_scan_log(conn, scan_id, *, notes=None):
    """Convenience for the common end-of-scan case: stamp omega_time_est as
    the current UTC time, and overwrite notes if given (leaves any existing
    notes alone otherwise). For anything other than "close it out now", use
    update_scan_log directly."""

    if notes is not None:
        conn.execute(
            "UPDATE scan_log SET omega_time_est = datetime('now'), notes = ? WHERE id = ?",
            (notes, scan_id),
        )
    else:
        conn.execute(
            "UPDATE scan_log SET omega_time_est = datetime('now') WHERE id = ?",
            (scan_id,),
        )
    conn.commit()


def update_scan_log(conn, scan_id, *, alpha_time_est=None, omega_time_est=None, notes=None):
    """Update alpha_time_est/omega_time_est/notes on an existing scan_log
    row - for manual correction of a scan pass's recorded times (e.g. it was
    logged late). For the ordinary "mark this scan done now" case, prefer
    close_scan_log. Only the fields given (not None) are changed."""

    fields, values = [], []
    if alpha_time_est is not None:
        fields.append("alpha_time_est = ?")
        values.append(alpha_time_est)
    if omega_time_est is not None:
        fields.append("omega_time_est = ?")
        values.append(omega_time_est)
    if notes is not None:
        fields.append("notes = ?")
        values.append(notes)

    assert fields, "Nothing to update - pass alpha_time_est/omega_time_est/notes"

    values.append(scan_id)
    conn.execute(f"UPDATE scan_log SET {', '.join(fields)} WHERE id = ?", values)
    conn.commit()


def upsert_document(conn, file_path, *, source_url=None, doc_date=None, first_scan_id=None):
    """Ensure a documents row exists for file_path and return its id.
    Safe to call repeatedly - later calls don't clobber fields already set
    by record_pdf_info/record_keyword_scan unless source_url/doc_date are
    newly given. doc_date, if given, must be ISO "YYYY-MM-DD". first_scan_id,
    if given, is only ever set once - it records the scan_log pass that
    first discovered this file, so a later call can't overwrite an
    already-set value (COALESCE keeps the existing one)."""

    assert doc_date is None or DATE_RE.match(doc_date), \
        f"doc_date must be ISO YYYY-MM-DD, got {doc_date!r}"

    file_path = str(file_path)
    slug = _town_slug_from_path(file_path)
    town_id = get_or_create_town(conn, slug) if slug else None

    conn.execute(
        """
        INSERT INTO documents (file_path, town_id, source_url, doc_date, first_scan_id)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(file_path) DO UPDATE SET
            source_url = COALESCE(excluded.source_url, documents.source_url),
            doc_date = COALESCE(excluded.doc_date, documents.doc_date),
            first_scan_id = COALESCE(documents.first_scan_id, excluded.first_scan_id)
        """,
        (file_path, town_id, source_url, doc_date, first_scan_id),
    )
    conn.commit()
    row = conn.execute(
        "SELECT id FROM documents WHERE file_path = ?", (file_path,)
    ).fetchone()
    return row[0]


def record_pdf_info(conn, file_path, info, *, source_url=None):
    """Store the JSON produced by PdfInfoTool (see plan_util.extract_pdf_info)
    for file_path: file size, page count, metadata, and per-page stats.
    Replaces any previously recorded pages for this document."""

    document_id = upsert_document(conn, file_path, source_url=source_url)

    conn.execute(
        """
        UPDATE documents SET
            file_size_bytes = ?,
            page_count = ?,
            metadata_json = ?,
            info_scanned_at = datetime('now')
        WHERE id = ?
        """,
        (
            info.get("file_size_bytes"),
            info.get("page_count"),
            json.dumps(info.get("metadata") or {}),
            document_id,
        ),
    )

    conn.execute("DELETE FROM pages WHERE document_id = ?", (document_id,))
    conn.executemany(
        """
        INSERT INTO pages (document_id, page_number, width, height, text_chars, has_selectable_text)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                document_id,
                page["page"],
                page.get("width"),
                page.get("height"),
                page.get("text_chars"),
                int(bool(page.get("has_selectable_text"))),
            )
            for page in info.get("pages", [])
        ],
    )

    conn.commit()
    return document_id


def record_document_text(conn, file_path, page_texts, *, source_url=None):
    """Store per-page extracted text (see plan_util.get_pdf_page_texts) for
    file_path: one doc_pages row per page. Replaces any previously recorded
    text for this document (a re-extraction supersedes the old text rather
    than accumulating duplicates). page_texts is a list of page text
    strings, 1-indexed by position."""

    document_id = upsert_document(conn, file_path, source_url=source_url)

    conn.execute("DELETE FROM doc_pages WHERE document_id = ?", (document_id,))
    conn.executemany(
        """
        INSERT INTO doc_pages (document_id, page_number, page_text)
        VALUES (?, ?, ?)
        """,
        [
            (document_id, pagenum, pagetext)
            for pagenum, pagetext in enumerate(page_texts, start=1)
        ],
    )

    conn.commit()
    return document_id


def record_keyword_scan(conn, file_path, result, *, source_url=None):
    """Store the JSON produced by PdfKeywordScanTool (see
    plan_util.scan_pdf_keywords) for file_path: one row per hit. Replaces
    any previously recorded hits for this document (a re-scan supersedes
    the old results rather than accumulating duplicates)."""

    document_id = upsert_document(conn, file_path, source_url=source_url)

    conn.execute(
        "UPDATE documents SET keywords_scanned_at = datetime('now') WHERE id = ?",
        (document_id,),
    )

    conn.execute("DELETE FROM keyword_hits WHERE document_id = ?", (document_id,))
    conn.executemany(
        """
        INSERT INTO keyword_hits (document_id, page_number, keyword, count, snippet)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (document_id, hit["page"], hit["keyword"], hit["count"], hit.get("snippet"))
            for hit in result.get("hits", [])
        ],
    )

    conn.commit()
    return document_id


def create_project(conn, town_slug, short_desc="", full_md_text=""):
    """Create a new projects row for town_slug (e.g. "portsmouth_nh" -
    creates the town row as a side effect, like upsert_document) and return
    its id. Projects are curated by hand, not produced by a scan tool, so
    unlike documents there's no upsert-by-key here - each call makes a new
    row; use update_project/link_project_document to fill it in further."""

    town_id = get_or_create_town(conn, town_slug)

    cur = conn.execute(
        "INSERT INTO projects (town_id, short_desc, full_md_text) VALUES (?, ?, ?)",
        (town_id, short_desc, full_md_text),
    )
    conn.commit()
    return cur.lastrowid


def load_tag_vocabulary(path=PROJECT_TAGS_PATH):
    """Return {tag: group_number} parsed from PROJECT_TAGS.md: every
    backticked tag in the first column of a table row, under a
    "### <N>. ..." group heading. Dict order follows the file, which is the
    canonical tag order."""

    vocab = {}
    group = None
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"###\s+(\d+)\.", line)
        if heading:
            group = int(heading.group(1))
            continue
        cell = re.match(r"\|\s*`([a-z0-9-]+)`\s*\|", line)
        if cell and group is not None:
            vocab[cell.group(1)] = group

    assert vocab, f"No tags found in {path}"
    return vocab


def normalize_tag_set(tags, vocab=None):
    """Validate tags (a list, or a comma-separated string) against the
    PROJECT_TAGS.md vocabulary and return the canonical comma-separated
    tag_set string, in vocabulary order. Rejects unknown tags, and requires
    exactly one tag from each EXACTLY_ONE_TAG_GROUPS group. An empty list
    or string is allowed (returns '' = untagged)."""

    vocab = vocab or load_tag_vocabulary()

    if isinstance(tags, str):
        tags = tags.split(",")
    tagset = {t.strip() for t in tags if t.strip()}
    if not tagset:
        return ""

    unknown = sorted(tagset - set(vocab))
    assert not unknown, f"Unknown tag(s) {unknown} - see {PROJECT_TAGS_PATH.name}"

    for groupnum, groupname in EXACTLY_ONE_TAG_GROUPS.items():
        ingroup = sorted(t for t in tagset if vocab[t] == groupnum)
        assert len(ingroup) == 1, \
            f"Need exactly one {groupname} tag, got {ingroup or 'none'}"

    return ",".join(t for t in vocab if t in tagset)


def update_project(conn, project_id, *, short_desc=None, full_md_text=None, tag_set=None):
    """Update short_desc, full_md_text and/or tag_set on an existing
    project row. Only the fields given (not None) are changed. tag_set must
    already be normalized (see normalize_tag_set)."""

    fields, values = [], []
    if short_desc is not None:
        fields.append("short_desc = ?")
        values.append(short_desc)
    if full_md_text is not None:
        fields.append("full_md_text = ?")
        values.append(full_md_text)
    if tag_set is not None:
        fields.append("tag_set = ?")
        values.append(tag_set)

    assert fields, "Nothing to update - pass short_desc, full_md_text and/or tag_set"

    values.append(project_id)
    conn.execute(f"UPDATE projects SET {', '.join(fields)} WHERE id = ?", values)
    conn.commit()


def link_project_document(conn, project_id, document_id, page_number=None):
    """Record that document_id mentions project_id (a project is typically
    referenced across several meetings' documents), optionally noting the
    1-indexed page where that mention starts. Safe to call repeatedly - the
    (project_id, document_id) pair is unique, so calling again just updates
    page_number (when a new one is supplied; page_number=None leaves an
    existing value alone rather than clearing it)."""

    conn.execute(
        """
        INSERT INTO project_documents (project_id, document_id, page_number)
        VALUES (?, ?, ?)
        ON CONFLICT(project_id, document_id) DO UPDATE SET
            page_number = COALESCE(excluded.page_number, project_documents.page_number)
        """,
        (project_id, document_id, page_number),
    )
    conn.commit()


def create_contact(conn, name="", phone="", email="", web_site=""):
    """Create a new contact_info row and return its id. Like create_project,
    there's no upsert-by-key - each call makes a new row."""

    cur = conn.execute(
        "INSERT INTO contact_info (name, phone, email, web_site) VALUES (?, ?, ?, ?)",
        (name, phone, email, web_site),
    )
    conn.commit()
    return cur.lastrowid


def link_contact_project(conn, contact_id, project_id):
    """Record that contact_id is involved in project_id. Safe to call
    repeatedly - the (contact_id, project_id) pair is unique."""

    conn.execute(
        "INSERT OR IGNORE INTO contact_project (contact_id, project_id) VALUES (?, ?)",
        (contact_id, project_id),
    )
    conn.commit()


def log_analysis(conn, file_path, notes="", *, source_url=None):
    """Record a pass of manual analysis over file_path - a timestamped
    analysis_log row with a short free-text note (e.g. "checked pages
    40-60, no new projects past #3"). Always inserts a new row (this is a
    log, not a upserted field) - repeated calls accumulate history rather
    than overwriting."""

    document_id = upsert_document(conn, file_path, source_url=source_url)

    conn.execute(
        "INSERT INTO analysis_log (document_id, logged_at, notes) VALUES (?, datetime('now'), ?)",
        (document_id, notes),
    )
    conn.commit()
    return document_id


def clear_analysis_log(conn, file_path):
    """Delete every analysis_log row for file_path - the undo for
    log_analysis(). Once cleared, the document has zero analysis_log rows
    again, so NextToAnalyze will surface it as unanalyzed. Does not touch
    projects or project_documents - any projects already recorded from this
    document stay linked. Returns (document_id, rows_deleted)."""

    document_id = upsert_document(conn, file_path)

    cur = conn.execute(
        "DELETE FROM analysis_log WHERE document_id = ?",
        (document_id,),
    )
    conn.commit()
    return document_id, cur.rowcount


def sync_project_from_files(conn, project_id):
    """Apply working/project_edit/<project_id>.md (full_md_text) and
    working/project_edit/<project_id>.json (every other updatable field:
    short_desc, and tag_set as a list of tags that replaces the whole set -
    see normalize_tag_set) to the projects row - see PROJECT_EDIT_DIR above
    for the naming convention. Either file may be absent, and a field
    missing from the .json is left unchanged; at least one file must exist.
    Everything is validated before anything is written. Once applied,
    both files are deleted (whichever existed) so working/project_edit/
    doesn't accumulate stale edits already committed to the DB."""

    mdpath = PROJECT_EDIT_DIR / f"{project_id}.md"
    jsonpath = PROJECT_EDIT_DIR / f"{project_id}.json"

    assert mdpath.exists() or jsonpath.exists(), \
        f"Neither {mdpath} nor {jsonpath} exists - nothing to sync"

    full_md_text = mdpath.read_text(encoding="utf-8") if mdpath.exists() else None

    fields = {}
    if jsonpath.exists():
        with open(jsonpath, encoding="utf-8") as fh:
            fields = json.load(fh)

    unknown = sorted(set(fields) - {"short_desc", "tag_set"})
    assert not unknown, f"Unknown field(s) {unknown} in {jsonpath.name} - allowed: short_desc, tag_set"

    tag_set = normalize_tag_set(fields["tag_set"]) if "tag_set" in fields else None

    update_project(conn, project_id, short_desc=fields.get("short_desc"),
                   full_md_text=full_md_text, tag_set=tag_set)

    if mdpath.exists():
        mdpath.unlink()
    if jsonpath.exists():
        jsonpath.unlink()

    return project_id


def run_query(path=QUERY_PATH, db_path=DB_PATH):
    """Run the single SQL statement in path against a read-only connection
    (so it can't modify the DB - use the dedicated tools for writes) and
    return (column_names, rows)."""

    sql = Path(path).read_text(encoding="utf-8").strip()
    assert sql, f"{path} is empty"

    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        cur = conn.execute(sql)
        columns = [d[0] for d in cur.description or []]
        return columns, cur.fetchall()
    finally:
        conn.close()


def load_json_output(path=WORK_DIR / "OUTPUT.txt"):
    """Convenience: load the JSON that PdfInfoTool/PdfKeywordScanTool most
    recently wrote to working/OUTPUT.txt."""

    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def update_documents_from_json(conn, path=DB_UPDATE_PATH):
    """Register/update documents rows from a JSON file at path: a list of
    objects, each {"file_path": "working/<town>/<file>.pdf", "source_url":
    "..." (optional), "date": "YYYY-MM-DD" (optional)}. Returns the list of
    document ids touched.

    This only registers documents (and creates their town row as a side
    effect) - it does not touch pages/keyword_hits. Re-running is safe:
    entries are upserted by file_path, never duplicated."""

    with open(path, encoding="utf-8") as fh:
        entries = json.load(fh)

    assert isinstance(entries, list), f"{path} must contain a JSON list of document objects"

    document_ids = []
    for entry in entries:
        file_path = entry["file_path"]
        document_ids.append(
            upsert_document(
                conn,
                file_path,
                source_url=entry.get("source_url"),
                doc_date=entry.get("date"),
            )
        )

    conn.commit()
    return document_ids


if __name__ == "__main__":
    conn = get_connection()
    print(f"Database ready at {DB_PATH}")
    doc_count = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    print(f"{doc_count} document(s) currently recorded")
