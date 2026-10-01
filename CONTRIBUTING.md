# Contributing

## Development setup

Python 3.11+ is required. The runtime has no third-party dependencies. Run `make check` before submitting changes.

## Change expectations

Keep the CLI read-only and bounded. Never execute code from reviewed diffs. Never print detected credential values or add real secrets/personal data to tests. Changes to data flows, privileges, model use, retention, or external services require updating `docs/architecture.md`, `docs/threat-model.md`, the data inventory, privacy notice, and applicable safety tests.

Use neutral, evidence-based finding language. Separate detector confidence from issue impact. Add regression tests for both true and false positives when adjusting rules. Do not claim comprehensive scanning, compliance, certification, or absence of vulnerability based on a pattern match.

## Pull requests

A change should include a concise problem statement, a bounded implementation, tests, and documentation updates where behavior or data handling changes. The project does not auto-approve or merge contributions. Maintainers should review the diff and CI before release.

## Licensing

A repository license has not been selected. Do not assume contribution licensing terms; resolve the project license before broad external distribution.
