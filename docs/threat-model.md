# Threat Model

**Scope:** v0.1 local CLI, agent instructions, and GitHub diff retrieval wrapper. This is a design baseline, not a penetration-test result.

## Assets and trust boundaries

Assets include source diff contents, incidental personal data, GitHub authentication managed by `gh`, review findings, and the integrity of the installed code. The human/operator, local OS, Python runtime, `gh`, and GitHub API are separate trust domains. Repository diff content, PR titles, and filenames are untrusted, even when fetched from an authenticated repository.

## Threats and controls

| Threat | Potential impact | Controls | Residual risk |
| --- | --- | --- | --- |
| Indirect prompt injection in code/comments | Agent follows data as instruction; disclosure or unauthorized action | CLI has no LLM/tools beyond `gh`; code is never executed; skill labels retrieved content untrusted and forbids following embedded instructions | Agent host may have independent tool authority; prompt wording alone is not a complete security boundary. |
| Accidental secret or personal-data disclosure | Credential leak or unnecessary repetition in output | No code excerpts; common credential heuristics; no logs; no app-owned persistence | Detection is incomplete; input itself still resides in the caller's memory/terminal/GitHub. Rotate exposed credentials. |
| Malicious/oversized/malformed diff | Crash, resource exhaustion, parser confusion | 10 MiB byte limit, 300-file cap, simple regex rules, controlled errors | Within-bound pathological text and semantic false positives remain possible. |
| Privilege misuse or unsafe side effects | Repository modification, comments, merge | Wrapper runs read-only `gh pr diff`; no checkout, push, PR review, or write API | User-supplied substitute `gh` binary or compromised host is out of scope. |
| Untrusted path/terminal control characters | Terminal/report manipulation | Strip control characters, cap paths, render code-span metadata only | Markdown path formatting is not a universal escaping boundary for every renderer. |
| Dependency/workflow compromise | Malicious package/action runs in CI | Zero runtime dependencies; checkout action pinned to a reviewed commit SHA; CI `contents: read` | Python/build tooling and GitHub-hosted runner remain dependencies; update pins through review. |
| False assurance / biased or unfair evaluation | Reviewer over-trusts findings; contributors treated unfairly | Advisory language, confidence, no person scoring, human review, no automated employment/credit/education decisions | Reviewers can still over-rely on tool output; organizational controls and training matter. |

## Security response priorities

If a finding indicates a credential exposure, do not copy the value into tickets or chat; remove it and rotate/revoke it through the credential owner. If a vulnerability in this repository is suspected, follow `SECURITY.md`. Do not test against systems without authorization.

## Out of scope

Hosted service controls such as encryption-at-rest, RBAC, MFA, WAF, backups, deletion workflows, and production incident monitoring do not apply to this code-only local release because it has no hosted service or app database. If introduced, they become mandatory design inputs rather than assumed capabilities.
