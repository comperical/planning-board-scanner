
import os
import sys
import json

sys.path.append("/opt/userdata/busicode/clientscript")

import client_util as CSUTIL

from pathlib import Path

WORK_DIR = Path(__file__).parent.parent.parent / "working"


def load_doc_info():

    def probe():
        for basedir, _, fnames in os.walk(WORK_DIR):
            for f in fnames:
                if f == "document_info.json":
                    yield Path(basedir) / f

    probelist = list(probe())
    assert len(probelist) == 1, f"Expected exactly 1 document_info file"

    jsonpath = probelist[0]
    with open(jsonpath) as fh:
        doclist = json.load(fh)

    return jsonpath.parent, doclist


def insert_doc_info():

    basedir, docinfo = load_doc_info()

    CSUTIL.direct_init_db("dburfoot", "planscan")

    textdir = basedir / "text"
    idgen = CSUTIL.gen_valid_assign_id("doc_info")

    def gen_records():
        for entry in docinfo:
            filename = entry["filename"]
            textpath = textdir / (Path(filename).stem + ".txt")

            extracted_text = ""
            if textpath.exists():
                with open(textpath, encoding="utf-8") as fh:
                    extracted_text = fh.read()

            yield {
                "id": next(idgen),
                "doc_link": entry["url"],
                "location": str(basedir),
                "extracted_text": extracted_text,
                "file_name": filename,
                "day_code": entry["date"],
            }

    CSUTIL.bulk_insert("doc_info", list(gen_records()))


