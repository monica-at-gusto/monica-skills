#!/usr/bin/env python3
"""Merge/tier/cap findings + reconcile deferrals, per finding-schema.md and deferrals.md.

Owns the fully deterministic half of Step 4: dedupe by (file, line) within a 3-line
window, drop confidence:low (and introduced_by_pr:false in --remote mode), tier by
severity, cap issue findings, and reconcile against the deferral ledger by exact
match key.

Does NOT drop findings already raised in the PR's existing human review comments —
that requires reading comment text semantically and stays Claude's judgment call;
pre-filter those out of the input before calling this script.

Fuzzy-titled deferral matches (same file, similar-but-not-identical title) are
surfaced in `fuzzy_candidates`, never auto-reconciled — finding-schema.md says ask
Monica, don't guess.

    python3 merge_findings.py <findings.json> [--deferrals <ledger.json>] [--remote] [--cap 5]

<findings.json> is a JSON array of finding objects (finding-schema.md shape).
<ledger.json> is the deferrals.md ledger shape; omit --deferrals to skip reconcile.
"""
import argparse
import difflib
import json
import re
import sys
from pathlib import Path

SEVERITY_RANK = {"critical": 3, "important": 2, "suggestion": 1, "strength": 0}
CONFIDENCE_RANK = {"high": 2, "medium": 1, "low": 0}
WINDOW = 3


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def match_key(f: dict) -> str:
    return f"{f['file']}::{slug(f['title'])}"


def dedupe(findings: list) -> list:
    """Group by (file, line) within a WINDOW-line chain; keep highest severity per group,
    union incident_refs, note every lens that hit it."""
    by_file = {}
    for f in findings:
        by_file.setdefault(f["file"], []).append(f)

    merged = []
    for file, group in by_file.items():
        group.sort(key=lambda f: f["line"] if f["line"] is not None else -1)
        cluster = []
        for f in group:
            if cluster and f["line"] is not None and cluster[-1]["line"] is not None \
                    and f["line"] - cluster[-1]["line"] <= WINDOW:
                cluster.append(f)
            else:
                if cluster:
                    merged.append(_merge_cluster(cluster))
                cluster = [f]
        if cluster:
            merged.append(_merge_cluster(cluster))
    return merged


def _merge_cluster(cluster: list) -> dict:
    best = max(cluster, key=lambda f: SEVERITY_RANK.get(f["severity"], 0))
    best = dict(best)
    best["incident_refs"] = sorted(set(sum((f.get("incident_refs", []) for f in cluster), [])))
    lenses = sorted(set(f["lens"] for f in cluster))
    if len(lenses) > 1:
        best["merged_from"] = lenses
    return best


def filter_findings(findings: list, remote: bool) -> list:
    kept = [f for f in findings if f.get("confidence") != "low"]
    if remote:
        kept = [f for f in kept if f.get("introduced_by_pr", True)]
    return kept


def reconcile_deferrals(findings: list, ledger: dict) -> tuple:
    entries = {e["key"]: e for e in ledger.get("deferrals", [])}
    matched_keys = set()
    fuzzy_matched_keys = set()
    deferred = []
    open_findings = []
    fuzzy_candidates = []

    for f in findings:
        key = match_key(f)
        entry = entries.get(key)
        if entry:
            matched_keys.add(key)
            f = dict(f)
            f["status"] = "acknowledged-deferred"
            f["deferral"] = {
                "rationale": entry["rationale"],
                "follow_up": entry.get("follow_up"),
                "decided_at": entry["decided_at"],
            }
            deferred.append(f)
            continue

        # Fuzzy check: same file, unmatched ledger entry, similar title. Still open — a
        # fuzzy match is surfaced for confirmation, never auto-reconciled or treated as resolved.
        for e_key, entry in entries.items():
            if e_key in matched_keys or entry["file"] != f["file"]:
                continue
            ratio = difflib.SequenceMatcher(None, slug(f["title"]), slug(entry["title"])).ratio()
            if ratio > 0.6:
                fuzzy_candidates.append({"finding": f, "ledger_entry": entry, "similarity": round(ratio, 2)})
                fuzzy_matched_keys.add(e_key)
                break
        open_findings.append(f)

    resolved = [e for k, e in entries.items() if k not in matched_keys and k not in fuzzy_matched_keys]
    return open_findings, deferred, fuzzy_candidates, resolved


def tier_and_cap(findings: list, cap: int) -> dict:
    tiers = {"critical": [], "important": [], "suggestion": [], "strength": []}
    for f in findings:
        tiers.setdefault(f["severity"], []).append(f)

    issues = tiers["critical"] + tiers["important"] + tiers["suggestion"]
    issues.sort(key=lambda f: (SEVERITY_RANK.get(f["severity"], 0),
                                CONFIDENCE_RANK.get(f.get("confidence"), 0)), reverse=True)
    trimmed = max(0, len(issues) - cap)
    kept_issues = set(id(f) for f in issues[:cap])
    for sev in ("critical", "important", "suggestion"):
        tiers[sev] = [f for f in tiers[sev] if id(f) in kept_issues]

    counts = {sev: len(fs) for sev, fs in tiers.items()}
    return {"tiers": tiers, "counts": counts, "trimmed": trimmed}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("findings_path")
    parser.add_argument("--deferrals")
    parser.add_argument("--remote", action="store_true")
    parser.add_argument("--cap", type=int, default=5)
    args = parser.parse_args()

    findings = json.loads(Path(args.findings_path).read_text())
    findings = dedupe(findings)
    findings = filter_findings(findings, args.remote)

    deferred, fuzzy_candidates, resolved = [], [], []
    if args.deferrals and Path(args.deferrals).exists():
        ledger = json.loads(Path(args.deferrals).read_text())
        findings, deferred, fuzzy_candidates, resolved = reconcile_deferrals(findings, ledger)

    result = tier_and_cap(findings, args.cap)
    result["deferred"] = deferred
    result["fuzzy_candidates"] = fuzzy_candidates
    result["resolved_deferrals"] = resolved
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
