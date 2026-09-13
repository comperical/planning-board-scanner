#!/usr/bin/env python3
"""Standalone script to launch a `playwright-cli` browser session, configured
to match this project's conventions (see the `playwright-cli` skill and
towninfo/*.md notes).

This just shells out to the `playwright-cli` command line tool - it does not
use the Python `playwright` package. It's a plain script, not a
`plan_entry.py` tool: args are parsed with the same ArgMap key=value
convention used elsewhere in this codebase, but there's no
ArgMap/CodeSetup/tool-class dispatch - just a bare `main()`.

`playwright-cli` writes its snapshot/output files to `.playwright-cli/` in
the current working directory by default; this script instead points that
at working/playwright_output/ (a subdirectory of this project's gitignored
scratch area) via the PLAYWRIGHT_MCP_OUTPUT_DIR environment variable, so
browsing output ends up there rather than wherever the script happened to
be launched from.

Usage:

    wwiocode/pyscript/launch_browser.py
    wwiocode/pyscript/launch_browser.py session=planscan
    wwiocode/pyscript/launch_browser.py headed=false

Args (all optional):
    session=<name>    playwright-cli session name (-s=<name>). Default: planscan
    headed=True        run headed (default) - some town sites block headless
                       Chromium with a Cloudflare challenge but pass cleanly
                       headed; see towninfo/rochester_nh.md. Pass headed=false
                       to run headless instead.
"""

import os
import subprocess
import sys

from pathlib import Path

sys.path.append("/opt/userdata/crm/src/python/opsutil")

import ArgMap

PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "working" / "playwright_output"


def launch(argmap):
    """Build and run the `playwright-cli open [...]` command for the given
    ArgMap, returning the completed subprocess result."""

    session = argmap.getStr("session", "planscan")
    headed = argmap.getBit("headed", True)

    cmd = ["playwright-cli", f"-s={session}", "open"]

    if headed:
        cmd.append("--headed")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PLAYWRIGHT_MCP_OUTPUT_DIR=str(OUTPUT_DIR))

    print(f"Running: {' '.join(cmd)}  (PLAYWRIGHT_MCP_OUTPUT_DIR={OUTPUT_DIR})")
    return subprocess.run(cmd, env=env)


def main():

    argmap = ArgMap.getFromArgv(sys.argv)
    result = launch(argmap)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
