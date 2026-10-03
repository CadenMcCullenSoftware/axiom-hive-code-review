# Governance and Compliance Alignment

This document maps engineering choices to the supplied specification and selected public references. It is not legal advice, an audit report, a conformity assessment, or a certification. Applicable obligations depend on the actual operator, intended purpose, users, jurisdiction, data flows, and deployment.

## Privacy and data protection

The local CLI follows privacy-by-design engineering choices: no product account, database, analytics, model provider, or app logging; bounded in-memory diff processing; no source snippets in findings; and disclosure that external runtime/terminal/GitHub handling is not controlled by this repository. These choices support minimization and storage limitation but do not establish a GDPR lawful basis, controller/processor role, rights process, or compliance outcome. Consult `docs/privacy-notice.md`, `docs/data-inventory.md`, and `docs/ropa.md`.

The source specification's suggested basis of contract necessity for review, legitimate interests for monitoring, and consent for analytics is not adopted as a legal determination. Analytics are absent. No broad claim that the app processes “no personal data” is made; repository diffs can contain personal data.

## Cybersecurity

The repository uses a small attack surface, read-only GitHub diff retrieval, no code execution, bounded input, no runtime Python dependencies, tests, least-privilege CI permissions, and a pinned checkout action. These are baseline engineering controls, not a full NIST CSF program, formal risk acceptance, penetration test, or certification. See the threat model, security policy, and NIST sources in `research-and-design-basis.md`.

Hosted controls listed in the source PDF—MFA/RBAC for administrators, KMS, WAF, network segmentation, DDoS mitigation, and encryption at rest—are not applicable to the shipped code-only CLI because no hosted service/storage is present. They become design requirements if hosted components are added.

## AI governance and human rights

The CLI is deterministic, and reports identify AI assistance as false. Agent skill text is guidance for compatible human-operated agent environments; it cannot guarantee another host's behavior. No AI Act classification is claimed. A future LLM-backed system or a use in employment, education, credit, housing, health, law enforcement, migration, or other high-impact contexts requires a specific legal and human-rights assessment before use.

The product does not rank contributors, infer intent or traits, profile people, or make decisions about individuals. Findings concern code behaviors and include confidence. A reviewer remains responsible for verification and action. Transparency requirements and their timing should be checked against current official guidance at deployment.

## Governance status

The privacy notice, inventory, RoPA, threat model, safety spec, and incident playbook are working documents. A proprietary rights notice names the rights holders supplied by the owner; customer license terms, pricing, jurisdiction-specific legal review, and sales/support contact are not established here. GitHub private vulnerability reporting is enabled; maintainers must still verify that notifications reach a monitored account. No independent legal review, security audit, or red-team sign-off is claimed.
