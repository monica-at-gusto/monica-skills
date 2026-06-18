#!/usr/bin/env python3
"""Extract Mermaid blocks from a markdown file, render a standalone HTML preview, open it.

The markdown is the canonical artifact; this HTML is a throwaway, derived view. Stdlib only.

    python3 render_preview.py <path-to-markdown>
"""
import html
import re
import subprocess
import sys
from pathlib import Path

MERMAID_BLOCK = re.compile(r"```mermaid\n(.*?)\n```", re.DOTALL)


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: render_preview.py <path-to-markdown>")

    md_path = Path(sys.argv[1]).expanduser()
    md = md_path.read_text()

    blocks = MERMAID_BLOCK.findall(md)
    if not blocks:
        sys.exit(f"No ```mermaid blocks found in {md_path}")

    template = (Path(__file__).resolve().parent.parent / "templates" / "preview.html").read_text()

    # Escape <, >, & so the browser hands Mermaid the literal diagram text via textContent.
    charts = "\n".join(
        f'<div class="chart"><pre class="mermaid">{html.escape(block)}</pre></div>'
        for block in blocks
    )

    # Title = "<JIRA-TICKET> · <chart slug>". The ticket is the notes parent dir (…/notes/USPDS-592/);
    # fall back to "control-flow-chart" for ad-hoc charts (e.g. in /tmp) where the parent isn't a ticket.
    parent = md_path.parent.name
    ticket = parent if re.fullmatch(r"[A-Z][A-Z0-9]+-\d+", parent) else "control-flow-chart"
    title = f"{ticket} · {md_path.stem}"

    out = Path("/tmp") / f"control-flow-{md_path.stem}.html"
    out.write_text(template.replace("<!--CHARTS-->", charts).replace("__TITLE__", title))

    subprocess.run(["open", str(out)], check=False)
    print(f"Preview opened: {out}  ({len(blocks)} chart{'s' if len(blocks) != 1 else ''})")


if __name__ == "__main__":
    main()
