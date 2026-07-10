#!/usr/bin/env python3
"""Resolve roster+window to merged PRs with Stage A metadata, deduped and noise-filtered.

Owns the mechanical part of curation-rubric.md Stage A: the per-login x per-repo
`gh pr list` loop (source-spine.md's "one query per login, then union" rule — a single
`gh search` with multiple --author flags silently drops authors), dedup, and dropping
obvious noise (dependency bumps, formatting-only, reverts) by title/file heuristics.

Does NOT score the six Stage A signals (new files under app/, packs touched, review
depth, spec changes, size, novelty-vs-history) — those are prose judgment calls for
Claude to apply over this already-deduped, already-filtered candidate set.

    python3 resolve_shipped_prs.py --repo Gusto/web --repo Gusto/zenpayroll \\
        --login iang-gusto --login monica-at-gusto --since 2026-06-15 --before 2026-06-29
"""
import argparse
import json
import re
import subprocess
import sys

FIELDS = "number,title,url,author,headRefName,files,additions,deletions,changedFiles,comments,latestReviews"

TICKET_RE = re.compile(r"\b([A-Z][A-Z0-9]{1,9}-\d+)\b")
NOISE_PATTERNS = [
    ("dependency bump", re.compile(r"(?i)^(bump|chore\(deps\)|deps:).*\b(from|to)\b")),
    ("revert", re.compile(r"(?i)^revert\b")),
    ("formatting-only", re.compile(r"(?i)(\b(rubocop|lint|format(ting)?)\b.*\bonly\b|^rubocop autofix)")),
]


def fetch_prs(repo: str, login: str, since: str, until: str) -> list:
    cmd = [
        "gh", "pr", "list",
        "--repo", repo,
        "--author", login,
        "--state", "merged",
        "--search", f"merged:{since}..{until}",
        "--json", FIELDS,
        "--limit", "200",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def extract_ticket(title: str, branch: str) -> str | None:
    m = TICKET_RE.search(title) or TICKET_RE.search(branch or "")
    return m.group(1) if m else None


def noise_reason(title: str) -> str | None:
    for reason, pattern in NOISE_PATTERNS:
        if pattern.search(title):
            return reason
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", action="append", required=True)
    parser.add_argument("--login", action="append", required=True)
    parser.add_argument("--since", required=True)
    parser.add_argument("--before", required=True)
    args = parser.parse_args()

    seen = {}  # (repo, number) -> pr, for dedup across logins (shouldn't collide, but be safe)
    candidates = []
    dropped = []

    for repo in args.repo:
        for login in args.login:
            for pr in fetch_prs(repo, login, args.since, args.before):
                key = (repo, pr["number"])
                if key in seen:
                    continue
                seen[key] = pr

                reason = noise_reason(pr["title"])
                if reason:
                    dropped.append({
                        "repo": repo, "number": pr["number"], "title": pr["title"], "reason": reason,
                    })
                    continue

                candidates.append({
                    "repo": repo,
                    "number": pr["number"],
                    "url": pr["url"],
                    "title": pr["title"],
                    "ticket": extract_ticket(pr["title"], pr.get("headRefName", "")),
                    "author": pr["author"]["login"],
                    "headRefName": pr.get("headRefName", ""),
                    "additions": pr.get("additions", 0),
                    "deletions": pr.get("deletions", 0),
                    "changedFiles": pr.get("changedFiles", 0),
                    "files": [
                        {"path": f["path"], "changeType": f.get("changeType", "")}
                        for f in pr.get("files", [])
                    ],
                    "commentsCount": len(pr.get("comments", [])),
                    "reviewCount": len(pr.get("latestReviews", [])),
                })

    print(json.dumps({"candidates": candidates, "dropped": dropped}, indent=2))


if __name__ == "__main__":
    main()
