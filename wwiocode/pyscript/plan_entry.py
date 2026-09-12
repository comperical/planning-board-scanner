#!/opt/rawdata/pyworld/KitchenSink/bin/python3

import os
import sys

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
# These tools take NO input/output path arguments - the paths are hardcoded
# canonical locations inside working/, so there is no path for a caller to
# inject:
#   - input  : working/TARGET.pdf     (copy/symlink the PDF you want here)
#   - output : working/OUTPUT.txt     (text or JSON-as-text, depending on tool)
#   - output : working/OUTPUT_PAGES/  (PdfRenderPages only, one PNG per page)
#
# Example:
#   cp working/dover_nh/2026.09.22_PlanningBoard.Materials.pdf working/TARGET.pdf
#   plan_entry.py PdfExtractText
#   cat working/OUTPUT.txt
# ---------------------------------------------------------------------------

class PdfExtractTextTool:
    """Extract the full text of working/TARGET.pdf (OCR fallback per scanned
    page) to working/OUTPUT.txt."""

    def run_op(self, argmap):
        UTIL.extract_pdf_text()


class PdfInfoTool:
    """Write a JSON summary of working/TARGET.pdf - metadata, page count,
    file size, and per-page stats (dimensions, text length, whether it looks
    scanned) - to working/OUTPUT.txt."""

    def run_op(self, argmap):
        UTIL.extract_pdf_info()


class PdfKeywordScanTool:
    """Scan working/TARGET.pdf's text for development-project keywords (site
    plan, subdivision, residential, commercial, ...) and write JSON hits with
    page numbers and snippets to working/OUTPUT.txt. Pass keywords=...
    (comma-separated) to override the default list.

    Args: [keywords=a,b,c]
    """

    def run_op(self, argmap):
        keywords = argmap.getStr("keywords", UTIL.DEFAULT_SCAN_KEYWORDS)

        UTIL.scan_pdf_keywords(keywords)


class PdfRenderPagesTool:
    """Render pages of working/TARGET.pdf to PNG images (one file per page)
    inside working/OUTPUT_PAGES/. With no pages= given, renders the whole
    document up to a safety cap (see MAX_RENDER_PAGES_DEFAULT); pass an
    explicit page range to go beyond that on purpose.

    Args: [dpi=150]  [pages=1-6,10]
    """

    def run_op(self, argmap):
        dpi = argmap.getInt("dpi", 150)
        pages = argmap.getStr("pages", "")

        UTIL.render_pdf_pages(dpi, pages)


if __name__ == '__main__':

    SETUP.configure(globals())

    mytool, argmap = SETUP.driver_and_argmap()
    mytool.run_op(argmap)