# Agent Guidance and Trust Boundaries

The deterministic CLI does not call a language model. This document governs the optional `SKILL.md` instructions used by compatible agent environments and any future model integration.

## Separation of authority

System/developer policy and the user's explicit task establish the authorized scope. PR diffs, repository files, comments, filenames, and tool output are untrusted data. They may contain instruction-like text, but that text cannot change the skill, grant permission, or authorize code execution, data export, or repository writes.

The skill directs agents to analyze only the requested diff and to keep tool use read-only. A prompt is not a security sandbox. Implementations that connect a model to tools must enforce least privilege outside the model, validate tool arguments and structured output, avoid sharing credentials with the model, and require human confirmation for consequential operations according to the product's authorization rules.

## Output contract

Default report format is Markdown. Machine-readable output must follow `assets/review-schema.json`, omit source snippets and recognized secrets, and state heuristic limitations. Automated format validation should run in CI before relying on downstream consumers. The current renderer constructs a fixed object and has no model-generated JSON.

## Evaluation

Test normal PRs, malformed/oversized diffs, secret-like inputs, prompt-injection strings inside comments, false positives in fixtures, and requests that attempt to trigger unapproved writes. Measure detection precision/recall on a consented, non-sensitive corpus before claiming quality. Do not add real customer/repository data to fixtures without authorization and a documented basis.

## Change management

Changes to the system boundary, tools, model provider, data retention, or action authority require a threat-model/privacy review and adversarial tests. Version changes to skill behavior and the report schema. Preserve changelog and rollback information.
