# Axiom Hive Code Review

A local-first, read-only tool for surfacing possible issues in GitHub pull request diffs. The shipped analyzer is deterministic and model-free. It emits concise Markdown or JSON, does not change a repository, and leaves review decisions to a human.

## Requirements

Python 3.11 or newer. For GitHub pull requests, install GitHub CLI (`gh`) and authenticate it yourself with only the repository access you intend to grant. The local-diff workflow does not need GitHub credentials.

## Quick start

From the repository root:

```bash
python3 -m unittest discover -s tests -v
printf '%s\n' 'diff --git a/app.py b/app.py' '--- a/app.py' '+++ b/app.py' '@@ -0,0 +1 @@' '+def collect(items=[]):' | PYTHONPATH=src python3 -m axiom_hive --repo local/demo
```

To inspect an actual PR, use:

```bash
scripts/analyze-pr.sh OWNER/REPO 42
scripts/analyze-pr.sh OWNER/REPO 42 --json
```

The wrapper invokes `gh pr diff` in read-only mode, processes its response in memory, and writes the report to stdout. It does not checkout code, execute files, comment on a PR, change branches, or merge. For a saved patch, use `PYTHONPATH=src python3 -m axiom_hive --diff-file change.diff --repo OWNER/REPO --pr 42`.

Install locally if desired with `python3 -m pip install .`; then use `axiom-review --help`.

## What it detects

The initial heuristics look for certain credential-like literals, SQL-looking concatenation, Python mutable defaults, query-like calls near loops, blocking sleep in changed async functions, and unbounded `read()`/`readlines()` calls. Test/spec/fixture paths reduce confidence for most non-secret rules. The rule catalog distinguishes implemented checks from human-review guidance.

## Limits and safety

This is **not** a complete static-analysis engine, penetration test, security certification, legal review, or code-acceptance decision. It examines added diff lines only, recognizes a small number of patterns, may produce false positives and false negatives, and cannot establish whether a vulnerability is exploitable. A clean report does not mean the code is safe. Review surrounding code and tests, and use language-aware scanners where appropriate.

Diffs and paths are untrusted input. The CLI never executes code from a diff and caps input at 10 MiB and analysis at 300 changed-file sections. Oversized input fails with a concise error. More than 300 files is explicitly marked incomplete. Reported credentials are not echoed, but detection is incomplete; rotate any credential that may have been exposed.

This tool gives suggestions only. A person remains responsible for deciding whether findings are valid and what changes to make. It is not designed to rank people or decide employment, education, credit, housing, health, legal, or other high-impact outcomes.

## Data handling

The application itself has no account system, database, analytics, model provider, or persistent logging. It processes diff text in memory and writes only the requested report to stdout. The GitHub wrapper retrieves a diff through the user's configured `gh` client; GitHub and the local operating system/terminal have their own processing and retention practices. Do not include secrets or unrelated personal data in command arguments or reports. See [the privacy notice](docs/privacy-notice.md), [data inventory](docs/data-inventory.md), and [architecture](docs/architecture.md).

These statements describe the shipped code, not every agent host, shell, operating system, marketplace, or future hosted deployment. The privacy and compliance documents are operational drafts. Controller/processor roles, lawful basis, jurisdictional applicability, transfer arrangements, contact details, and any legal classification must be reviewed for the actual operator and deployment. No claim of GDPR or EU AI Act compliance is made.

## Development

```bash
make check
```

The project has no runtime third-party Python dependencies. GitHub Actions runs compile checks and unit tests with read-only repository permissions. See `CONTRIBUTING.md` and `SECURITY.md` before making changes.

## Repository guide

`SKILL.md` contains portable agent instructions. `src/axiom_hive/` implements the scanner. `assets/` contains the heuristic catalog, JSON schema, and report template. `references/` provides reviewer guidance. `docs/` records architecture, requirements, privacy, safety, threat assumptions, research sources, and operational procedures.

## Project status

Prototype / initial implementation. The red-team test plan has not been independently executed. Repository license and public security-reporting contact are not configured. Review these before external distribution.
