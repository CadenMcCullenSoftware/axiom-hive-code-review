# Requirements Traceability

This map translates the supplied Axiom-01 / Axiom Hive Code Review specification into v0.1 repository controls. “Implemented” means implemented in this local codebase, not independently audited or certified.

| Requirement | Implementation / evidence | Status and limitation |
| --- | --- | --- |
| Human-in-the-loop; no code modification or auto-approval | Read-only `gh pr diff`; SKILL.md; no write-capable PR API | Implemented for shipped CLI. Agent host may have separate powers; skill explicitly limits their use. |
| Accurate, neutral, evidence-based review | Finding locations, rule IDs, confidence; neutral messages; no character judgments | Implemented as format and heuristics. Accuracy still requires human validation. |
| Minimize sensitive data; avoid echoing credentials | CLI emits no code snippets or credential match; no logs or analytics | Implemented for recognized credential patterns only; incomplete detection is documented. |
| Ephemeral processing by default | In-memory capped input and stdout output; no app-owned storage | Implemented in application code. OS, terminal, GitHub, or agent-host retention is outside this tool's control and disclosed. |
| Prompt injection in retrieved diffs | Text-only parser; no model or content-driven tool execution; explicit skill trust-boundary rules | Implemented for CLI; future LLM integration would require separate adversarial evaluation. |
| Malformed and large diffs | Controlled invalid-diff error; 10 MiB limit; 300-file cap with explicit incomplete status | Implemented. Input above 10 MiB is rejected rather than summarized. |
| Structured report | JSON renderer and `assets/review-schema.json`; unit tests | Implemented; schema artifact needs external validator in release CI if consumers depend on strict conformance. |
| Security and privacy governance docs | `docs/security-policy.md`, privacy notice, inventory, RoPA draft, threat model, incident process | Drafted for this architecture. Operational owners, contact details, legal basis, processor contracts, and response performance require deployment-specific completion. |
| Red-team and ongoing safety evaluation | Test cases and CI regression tests | Initial tests included. No independent penetration test or production red-team exercise has been conducted. |
| NIST SSDF / CSF-aligned development | Pinned CI checkout, no runtime dependencies, tests, restricted GitHub workflow permissions | Baseline only; no organizational program, SAST/DAST service, formal SBOM, or third-party audit is claimed. |
| GDPR rights and lawful basis | Data flow is documented as local and ephemeral | This CLI has no account or persistent data store to export/erase. Controller/processor roles and lawful basis are not established by code; seek counsel for a service deployment. |
| EU AI Act transparency and risk classification | AI-generation field in report is false for shipped CLI; docs avoid declaring a legal risk class | Classification depends on intended purpose, deployment, users, and applicable law; not concluded here. |
| Human rights / non-discrimination | No contributor ranking, profiling, or high-impact recommendations; confidence visible; human decides | Implemented as product boundary and communication guidance; no formal human-rights impact assessment has been performed. |
