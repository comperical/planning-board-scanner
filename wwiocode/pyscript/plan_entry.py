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


if __name__ == '__main__':

    SETUP.configure(globals())

    mytool, argmap = SETUP.driver_and_argmap()
    mytool.run_op(argmap)