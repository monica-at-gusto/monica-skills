#!/usr/bin/env bash
set -euo pipefail

# Trims a raw searchJiraIssuesUsingJql response down to a lean TSV: key, issuetype,
# priority, status, assignee, parent key, parent summary, summary.
# Usage: trim-jira-index.sh <raw-response.json> >> lean.tsv
# Run once per page when paginating; concatenate outputs across pages.

if [ $# -ne 1 ]; then
  echo "usage: $(basename "$0") <raw-jql-response.json>" >&2
  exit 1
fi

jq -r '.issues[] | [.key, .fields.issuetype.name, .fields.priority.name, .fields.status.name,
  (.fields.assignee.displayName // "UNASSIGNED"), (.fields.parent.key // "-"),
  (.fields.parent.fields.summary // "-"), .fields.summary] | @tsv' "$1"
