# Architecture and Security Rationale

## Deployment boundary

Version 0.1 is a local command-line tool and portable agent skill. The deterministic analyzer is deliberately model-free. It reads a caller-provided unified diff or receives a diff from the user's authenticated `gh` CLI. It processes at most 10 MiB of patch text and analyzes at most 300 changed-file sections. It writes no repository data or logs. Output is returned on stdout. The optional shell wrapper uses `gh pr diff` in read-only mode and pipes the response directly into the scanner; no temporary patch file is created.

```text
Human reviewer
  ├─ local diff ───────────────┐
  └─ analyze-pr.sh → gh CLI → GitHub API (read-only PR diff)
                                ↓
                         bounded parser
                                ↓
                       deterministic rules
                                ↓
                 Markdown or strict-shape JSON → human
```

## Components

- `scripts/analyze-pr.sh` validates repository and PR identifiers, invokes only `gh pr diff`, and pipes its output to the local scanner. It has no PR-comment, checkout, merge, or write operation.
- `src/axiom_hive/diff_parser.py` identifies file sections and added-line numbers; diff text and paths remain untrusted data.
- `src/axiom_hive/analyzer.py` applies bounded, static heuristics. It does not import, evaluate, execute, or compile reviewed code and makes no model/API calls.
- `src/axiom_hive/report.py` emits stable Markdown or JSON and does not include source snippets or matched secret values.
- `SKILL.md` guides compatible agents to preserve human authority, avoid following diff-embedded instructions, minimize sensitive data, and distinguish facts from hypotheses.

## Requirement-to-control rationale

| Requirement | Design control | Reason |
| --- | --- | --- |
| Human review and no autonomous changes | Read-only retrieval; no GitHub write scope or code-modifying command | Keeps acceptance, fixes, comments, and merge decisions with the human. |
| Prompt injection / untrusted content | Diffs are parsed only as text; no content can authorize a tool or override agent instructions | An indirect instruction in a file must not gain authority over system policy or tools. |
| Privacy minimization | No persistent diff/report/log storage; no analytics; no source excerpts in findings | Reduces unnecessary collection, retention, and accidental secret replication. |
| Credential exposure | Recognized values are detected but never rendered; remediation advises rotation | Prevents a review report from duplicating an exposed value. Detection remains incomplete. |
| Robustness | 10 MiB byte cap, 300-file cap, validated identifiers, malformed-diff errors | Bounds resource use and makes partial coverage visible instead of silently claiming completeness. |
| Evidence and fairness | Finding has rule, location, confidence, neutral wording; test paths lower confidence for non-secret rules | Makes heuristic uncertainty visible and avoids judgments about contributors. |
| Structured output | Fixed JSON shape and schema artifact; deterministic rendering | Allows consumers to parse results without executing model-produced markup or code. |
| Supply chain | No runtime dependencies; CI uses a full commit SHA for checkout; CI permissions are read-only | Shrinks dependency and workflow privilege surface. |

## Deliberate constraints

The first version does not use an LLM, GitHub App, MCP service, database, analytics, user accounts, or automated decisioning. It does not post results to pull requests. Those choices are not a claim that these systems are intrinsically unsafe; they avoid adding data retention, third-party processing, credentials, privileges, and governance obligations before they are required.

The implementation does not perform complete language-aware analysis. It scans additions only, uses simple textual patterns, and cannot reliably determine exploitability, control flow, authorization, or project context. The review is advisory and must be combined with full-code review, tests, and purpose-built security tools.

## Security assumptions and future changes

The operator controls the local machine, Python installation, and `gh` authentication. GitHub performs the requested API retrieval. Any model or hosted processing feature would change the data flow and threat model and must not be enabled by merely adding a prompt or dependency. Before such a feature, document the processor, data regions, retention, authentication scopes, incident handling, user notice, and applicable legal review; then update this design and its tests.
