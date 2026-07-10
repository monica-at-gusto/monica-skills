#!/usr/bin/env python3
"""Render the Ticket Comprehension Drill's fixed scaffold (SKILL.md Step 4b), verbatim.

The three questions and blank answer lines are FIXED — never invented, never filled in.
This script guarantees that structurally instead of relying on prose emphasis alone.
Deciding which tickets go in the drill, and whether each merits the pushback flag
(no clear business rationale), stays Claude's judgment call — this only renders.

    python3 render_drill.py <tickets.json>

<tickets.json> is a JSON array of {id, title, pushback (bool), answer_key (str)}.
"""
import json
import sys
from pathlib import Path

BLOCK = """### {header}
1. What does this ticket do, in one sentence?
   -
2. Why does it exist — whose ask, what product/business problem, what happens if it isn't built?
   -
3. Do you agree it's worth building? If not, what's your counterargument?
   -

<details><summary>Answer key — open only after you've tried from memory</summary>
{answer_key}
</details>"""


def render_one(ticket: dict) -> str:
    header = f"{ticket['id']} — {ticket['title']}"
    if ticket.get("pushback"):
        header += "   ⚑ Possible pushback opportunity"
    return BLOCK.format(header=header, answer_key=ticket["answer_key"])


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: render_drill.py <tickets.json>")

    tickets = json.loads(Path(sys.argv[1]).read_text())
    if not tickets:
        sys.exit("no tickets given — omit the drill section entirely rather than calling this")

    print("\n\n".join(render_one(t) for t in tickets))


if __name__ == "__main__":
    main()
