# Data Inventory and Data Flow

**Scope:** shipped local CLI and optional user-run GitHub diff wrapper. No hosted service is part of this release.

## Data inventory

| Category | Source and purpose | Application handling | Retention / recipient boundary |
| --- | --- | --- | --- |
| Unified PR diff | User input or `gh pr diff`; needed to run heuristics | Bounded in-memory parsing, max 10 MiB; text is not executed | No application-owned persistence; local runtime and GitHub CLI/GitHub have independent handling. |
| PR/repository labels | CLI arguments for report context | Included in report metadata | Output on stdout; caller controls redirection and storage. |
| File paths and added-line numbers | Parsed from diff for locating findings | Sanitized and included in report | Output on stdout; path itself can contain sensitive data and is capped but not semantically redacted. |
| Findings | Produced by deterministic rules | Contains rule/location/message/fix; excludes source snippets and recognized credential values | Only returned to caller; no database or logs. |
| GitHub CLI credentials | User's existing `gh` authentication state | Not read by the analyzer or printed; used by `gh` for requested diff retrieval | User-managed and governed by GitHub/local environment. Never provide token values to this tool. |
| Telemetry, account data, model prompts | Not collected/created by shipped app | None | None in application code. An integrating agent/host may have separate processing. |

## Data flow

`Human/operator → local CLI → in-memory parser and rules → stdout report → human`

For GitHub mode: `local wrapper → gh pr diff (authenticated GitHub API read) → stdout pipe → local analyzer → stdout report`.

The application has no model provider or outbound network client. It has no report persistence, security logs, usage analytics, or deletion service. Shell history may contain the command arguments but should not contain the diff unless a user deliberately places data there. The local OS, terminal/agent host, CI provider, and GitHub are outside the application's storage controls.

## Retention and deletion

Diff content is processed for the duration of the process; this project creates no diff/report files. A report exists wherever the user directs stdout. The project cannot erase shell, terminal, CI, provider, GitHub, backup, or user-created copies. Do not describe the broader environment as “no retention” without reviewing those systems.

## Change triggers

Any added database, analytics, account, telemetry, hosted model, MCP endpoint, automatic PR comment, or persistent report changes the inventory and threat model. Update this file, privacy notice, RoPA draft, processor list, rights procedures, and security controls before deployment.
