
import os
import sys
import json

sys.path.append("/opt/userdata/busicode/clientscript")

import client_util as CSUTIL
import fitz  # PyMuPDF

from pathlib import Path

WORK_DIR = Path(__file__).parent.parent.parent / "working"

FORMAT_DOC_DIR = WORK_DIR / "formatted"
TEXT_DIR = WORK_DIR / "text"


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



def extract_text_info(mainpath):

    mainpath = Path(mainpath)
    textpath = TEXT_DIR / (mainpath.stem + ".txt")

    if textpath.exists():
        print(f"Text file {textpath} already exists, skipping")
        return

    TEXT_DIR.mkdir(parents=True, exist_ok=True)

    def gen_page_text():
        with fitz.open(mainpath) as doc:
            for page in doc:
                pagetext = page.get_text().strip()

                if not pagetext:
                    # Scanned/image-only page, fall back to OCR
                    pagetext = page.get_textpage_ocr(full=True).extractTEXT().strip()

                yield pagetext

    fulltext = "\n\n".join(gen_page_text())

    with open(textpath, "w", encoding="utf-8") as fh:
        fh.write(fulltext)

    print(f"Extracted text for {mainpath} -> {textpath}")


