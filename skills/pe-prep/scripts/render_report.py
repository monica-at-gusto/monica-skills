#!/usr/bin/env python3
"""Inject an AGENDA data JSON payload into templates/report.html, write it, open it.

The skill builds the JSON payload (see templates/report.html's own doc comment for
the shape); this script owns the mechanical part: substitute, write, open. Stdlib only.

Note: the template's doc comment ALSO contains the literal string "__AGENDA_DATA__"
(documenting the contract) — a naive whole-file replace of that token would corrupt
the wrong spot. This anchors to the full `const AGENDA = __AGENDA_DATA__;` line instead.

    python3 render_report.py <agenda-data.json> <output-html-path>
"""
import json
import subprocess
import sys
from pathlib import Path

TARGET_LINE = "const AGENDA = __AGENDA_DATA__;"


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("usage: render_report.py <agenda-data.json> <output-html-path>")

    data_path = Path(sys.argv[1]).expanduser()
    out_path = Path(sys.argv[2]).expanduser()

    data = json.loads(data_path.read_text())  # fail loud on malformed payloads

    template = (Path(__file__).resolve().parent.parent / "templates" / "report.html").read_text()

    if template.count(TARGET_LINE) != 1:
        sys.exit(f"expected exactly 1 occurrence of {TARGET_LINE!r} in template, "
                  f"found {template.count(TARGET_LINE)}")

    replacement = f"const AGENDA = {json.dumps(data, ensure_ascii=False)};"
    rendered = template.replace(TARGET_LINE, replacement)

    out_path.write_text(rendered)
    subprocess.run(["open", str(out_path)], check=False)
    print(f"Report opened: {out_path}")


if __name__ == "__main__":
    main()
