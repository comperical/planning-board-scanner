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

# Naming convention for editing a project by hand (see the ApplyProjectEdit
# tool in plan_entry.py / sync_project_from_files() below): to update
# project <id>, write working/project_edit/<id>.md (the full_md_text field
# - free-form markdown) and/or working/project_edit/<id>.json (every other
# updatable field, currently just {"short_desc": "..."}), then run the tool
# to apply both to the DB. Either file may be omitted to leave that side
# unchanged.
PROJECT_EDIT_DIR = WORK_DIR / "project_edit"


SCHEMA = """
CREATE TABLE IF NOT EXISTS town (
    id                  INTEGER PRIMARY KEY,
    slug                TEXT NOT NULL UNIQUE,  -- e.g. "dover_nh", matches working/<slug>/ and towninfo/<slug>.md
    name                TEXT,                  -- e.g. "Dover"
    state               TEXT                   -- e.g. "NH"
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
    keywords_scanned_at TEXT                   -- UTC timestamp of the last keyword-scan recording
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
    full_md_text        TEXT               -- full markdown write-up: description, status, addresses, applicant, etc.
);

-- Links a project to every document that mentions it (a project is
-- typically referenced across several meetings - an agenda, then minutes,
-- then a later extension/approval).
CREATE TABLE IF NOT EXISTS project_documents (
    id                  INTEGER PRIMARY KEY,
    project_id          INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    document_id         INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
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

CREATE INDEX IF NOT EXISTS idx_documents_town ON documents(town_id);
CREATE INDEX IF NOT EXISTS idx_pages_document ON pages(document_id);
CREATE INDEX IF NOT EXISTS idx_keyword_hits_document ON keyword_hits(document_id);
CREATE INDEX IF NOT EXISTS idx_keyword_hits_keyword ON keyword_hits(keyword);
CREATE INDEX IF NOT EXISTS idx_doc_pages_document ON doc_pages(document_id);
CREATE INDEX IF NOT EXISTS idx_projects_town ON projects(town_id);
CREATE INDEX IF NOT EXISTS idx_project_documents_project ON project_documents(project_id);
CREATE INDEX IF NOT EXISTS idx_project_documents_document ON project_documents(document_id);
CREATE INDEX IF NOT EXISTS idx_analysis_log_document ON analysis_log(document_id);
"""


def get_connection(db_path=DB_PATH):
    """Open (creating if needed) the SQLite database and ensure the schema
    exists. Enables foreign keys, since SQLite leaves that off by default."""

    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


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


def upsert_document(conn, file_path, *, source_url=None, doc_date=None):
    """Ensure a documents row exists for file_path and return its id.
    Safe to call repeatedly - later calls don't clobber fields already set
    by record_pdf_info/record_keyword_scan unless source_url/doc_date are
    newly given. doc_date, if given, must be ISO "YYYY-MM-DD"."""

    assert doc_date is None or DATE_RE.match(doc_date), \
        f"doc_date must be ISO YYYY-MM-DD, got {doc_date!r}"

    file_path = str(file_path)
    slug = _town_slug_from_path(file_path)
    town_id = get_or_create_town(conn, slug) if slug else None

    conn.execute(
        """
        INSERT INTO documents (file_path, town_id, source_url, doc_date)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(file_path) DO UPDATE SET
            source_url = COALESCE(excluded.source_url, documents.source_url),
            doc_date = COALESCE(excluded.doc_date, documents.doc_date)
        """,
        (file_path, town_id, source_url, doc_date),
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


def update_project(conn, project_id, *, short_desc=None, full_md_text=None):
    """Update short_desc and/or full_md_text on an existing project row.
    Only the fields given (not None) are changed."""

    fields, values = [], []
    if short_desc is not None:
        fields.append("short_desc = ?")
        values.append(short_desc)
    if full_md_text is not None:
        fields.append("full_md_text = ?")
        values.append(full_md_text)

    assert fields, "Nothing to update - pass short_desc and/or full_md_text"

    values.append(project_id)
    conn.execute(f"UPDATE projects SET {', '.join(fields)} WHERE id = ?", values)
    conn.commit()


def link_project_document(conn, project_id, document_id):
    """Record that document_id mentions project_id (a project is typically
    referenced across several meetings' documents). Safe to call repeatedly
    - the (project_id, document_id) pair is unique, so a duplicate link is
    silently ignored rather than erroring."""

    conn.execute(
        "INSERT OR IGNORE INTO project_documents (project_id, document_id) VALUES (?, ?)",
        (project_id, document_id),
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


def sync_project_from_files(conn, project_id):
    """Apply working/project_edit/<project_id>.md (full_md_text) and
    working/project_edit/<project_id>.json (every other updatable field -
    currently just short_desc) to the projects row - see PROJECT_EDIT_DIR
    above for the naming convention. Either file may be absent, in which
    case that side is left unchanged; at least one must exist. Once applied,
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

    update_project(conn, project_id, short_desc=fields.get("short_desc"), full_md_text=full_md_text)

    if mdpath.exists():
        mdpath.unlink()
    if jsonpath.exists():
        jsonpath.unlink()

    return project_id


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
