#!/usr/bin/env python3
"""Inject a PRC data JSON payload into templates/report.html, write it, open it.

The skill builds the JSON payload (see references/html-report.md for the shape);
this script owns the mechanical part: substitute, write, open. Stdlib only.

    python3 render_report.py <prc-data.json> <output-html-path>
"""
import json
import re
import subprocess
import sys
from pathlib import Path

DATA_BLOCK = re.compile(
    r"/\* __PRC_DATA_START__ \*/.*?/\* __PRC_DATA_END__ \*/", re.DOTALL
)


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("usage: render_report.py <prc-data.json> <output-html-path>")

    data_path = Path(sys.argv[1]).expanduser()
    out_path = Path(sys.argv[2]).expanduser()

    data = json.loads(data_path.read_text())  # fail loud on malformed payloads

    template = (Path(__file__).resolve().parent.parent / "templates" / "report.html").read_text()

    replacement = (
        "/* __PRC_DATA_START__ */\n"
        f"const PRC = {json.dumps(data, ensure_ascii=False)};\n"
        "/* __PRC_DATA_END__ */"
    )
    # Pass a function, not the string itself, as repl — otherwise re treats backslashes
    # in the JSON (e.g. from escaped quotes) as template escape sequences and errors out.
    rendered, count = DATA_BLOCK.subn(lambda _match: replacement, template)
    if count != 1:
        sys.exit(f"expected exactly 1 data block in template, found {count}")

    out_path.write_text(rendered)
    subprocess.run(["open", str(out_path)], check=False)
    print(f"Report opened: {out_path}")


if __name__ == "__main__":
    main()
