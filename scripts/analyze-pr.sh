#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s OWNER/REPO PR_NUMBER [--json]\n' "$0" >&2
  exit 64
}

[[ $# -ge 2 && $# -le 3 ]] || usage
repo=$1
pr=$2
format=markdown
if [[ $# -eq 3 ]]; then
  [[ $3 == --json ]] || usage
  format=json
fi
[[ $repo =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]] || { echo 'Invalid repository; expected OWNER/REPO.' >&2; exit 64; }
[[ $pr =~ ^[1-9][0-9]{0,8}$ ]] || { echo 'PR number must be a positive integer.' >&2; exit 64; }
command -v gh >/dev/null 2>&1 || { echo 'GitHub CLI (gh) is required.' >&2; exit 69; }

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$root"
# Read-only retrieval; direct pipe means no patch file or persistent diff storage.
gh pr diff "$pr" --repo "$repo" --color never | PYTHONPATH="$root/src${PYTHONPATH:+:$PYTHONPATH}" python3 -m axiom_hive --repo "$repo" --pr "$pr" --format "$format" --require-nonempty
