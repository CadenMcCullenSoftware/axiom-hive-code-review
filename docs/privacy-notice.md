# Privacy Notice — Axiom Hive Code Review

**Status:** Draft for the local CLI prototype. This notice describes the shipped code and is not legal advice.

## What the application processes

When run, the local CLI temporarily reads unified diff text supplied through standard input or a named diff file. The optional PR wrapper asks the user's installed GitHub CLI to retrieve a pull-request diff from GitHub. A diff may contain personal data or credentials even though the tool does not request them. The analyzer emits a report containing repository/PR labels supplied by the caller, changed-file paths, line locations, heuristic descriptions, and suggested next steps. It intentionally does not include source excerpts or recognized credential values.

## Purpose and storage

The only application purpose is to produce an advisory code-review report requested by the operator. The CLI has no product account, database, telemetry, analytics, or application log. Diff data is processed in memory and is not persisted by this code; the requested report is written to standard output. The local OS, terminal, shell, agent host, CI system, and GitHub may independently retain data under their own settings and policies. The tool cannot promise those external systems are ephemeral.

The GitHub wrapper uses the operator's existing `gh` authentication and GitHub API access. It does not transmit the report or add PR comments. No third-party model provider is used in this release.

## Choices and precautions

Do not paste credentials or unrelated personal data into a diff. If a credential appears in code, remove it and rotate/revoke it. Secret matching is incomplete and can produce false positives; a missing warning does not prove the diff contains no secret. Avoid saving report output where it can be accessed by unintended people.

## Rights and legal roles

This local prototype does not maintain an account or persistent personal-data store that it can export, correct, or erase. Processing undertaken by a repository operator, GitHub, a terminal/agent host, or a future service may have separate controllers, processors, legal bases, notices, rights procedures, and retention. Those roles and lawful bases depend on the deployment and are not decided by this repository. Operators should obtain jurisdiction-specific advice before processing personal data at scale or deploying a hosted service.

## Contact and changes

A data-protection contact has not been configured. Before external distribution, the responsible operator should add a monitored privacy contact and verify the notice against the actual deployment. Material product changes to storage, providers, analytics, or PR write actions require a review of this notice and the data inventory.
