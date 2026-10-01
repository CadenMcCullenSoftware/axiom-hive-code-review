# Incident Response Runbook

This is a lightweight prototype response procedure, not a staffed 24/7 service plan. Assign an owner and backup contact before external distribution.

## Triage

1. Record a minimal incident identifier, report time, affected release/component, and reporter contact if voluntarily provided. Do not copy a credential or unnecessary personal data into the incident record.
2. Classify the report as credential exposure, suspected personal-data disclosure, software vulnerability, service disruption, or other. Treat unverified claims as reports, not established facts.
3. Restrict access to any evidence and use private channels. Do not ask for live secrets; use redacted reproduction data.

## Containment and remediation

For an exposed credential, notify the credential owner, revoke/rotate it, remove it from active source where feasible, and assess repository history and downstream copies. For a software issue, prepare a minimal fix, add a regression test, and release through review. Test reproduction only on systems for which authorization is explicit. Preserve only evidence necessary for response and set a deletion point.

If personal data may be involved, escalate promptly to the responsible organization's privacy/security lead and qualified counsel. Assess legal duties and timelines based on the real controller, affected data, jurisdiction, and facts. Do not make a generic promise that a notification deadline applies in every case.

## Recovery and learning

Verify the corrective action, monitor for recurrence where a legitimate monitoring system exists, notify affected parties through the responsible organization when required, and record root cause and follow-up tasks without embedding secrets. Update tests, threat model, and privacy/security documentation after material changes.

## Operational gaps

Owner, backup, private intake URL, communications template, escalation roster, and service-level targets are not configured in this repository. Complete them before distribution or hosting.
