# Security Policy

## Current scope

This policy covers the source repository and local CLI prototype. No hosted API, account service, database, analytics, MCP endpoint, or production deployment is included. Controls appropriate to a hosted service must be designed before one is introduced.

## Engineering controls

The analyzer treats patches and filenames as untrusted, reads only bounded input, never executes diff content, and emits no matched secret value or code excerpt. The GitHub wrapper calls `gh pr diff` only. Runtime Python dependencies are zero. CI is limited to tests and syntax compilation; its token has `contents: read`, and its checkout action is pinned to a full commit SHA. Review dependency/action pin changes before merging.

Developers should avoid committing secrets, use MFA on repository accounts, keep GitHub access minimal, review code changes, test failure paths, and avoid placing real personal data or credentials in fixtures. No secret scanning, SAST, DAST, dependency audit service, encryption-at-rest system, RBAC application, or monitoring pipeline is claimed by this repository.

## Vulnerability reporting and response

GitHub private vulnerability reporting is the intended channel; repository enablement and maintainer notification coverage must be verified in settings before external distribution. No alternate email address or response-time commitment is published. Do not publish an unremediated exploit or submit credentials in a public issue.

On receiving a report, the responsible maintainer should acknowledge privately, reproduce only in an authorized isolated environment, assess impact, prepare a fix, test regression behavior, coordinate disclosure with the reporter, and document closure. If secrets are exposed, remove and rotate/revoke them. If any personal-data incident is suspected, involve the responsible organization and qualified counsel promptly; legal notification deadlines and duties are context-specific and are not decided by this codebase.

## Future hosted service gate

Before a hosted release, define identity/authentication, least-privilege RBAC, MFA for administrators, TLS, encryption and managed key lifecycle, network isolation, abuse/rate limiting, secure logging and retention, backups/deletion, processor agreements, incident ownership, vulnerability SLAs, monitoring, and independent testing. Update the architecture, threat model, inventory, privacy notice, RoPA, and release process. Do not claim these controls based solely on a planned design.
