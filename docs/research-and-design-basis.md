# Research and Design Basis

This design uses the supplied Axiom-01 specification as the product requirement source and checks implementation choices against authoritative standards and platform documentation. The references guide engineering; they do not make this project legally compliant or certified.

## Findings that shape the architecture

**Secure software development.** NIST SP 800-218 describes a core set of secure development practices that can be integrated into different SDLCs to reduce vulnerabilities and their impacts. For this small local-first repository, that supports threat modeling, constrained dependencies, code review, tests, and an explicit vulnerability process. The framework does not mandate this exact architecture. [1]

**Cybersecurity risk management.** NIST CSF 2.0 organizes outcomes under Govern, Identify, Protect, Detect, Respond, and Recover, and says the framework should be tailored to organizational risk and mission. This repository records governance assumptions, a data inventory, protective defaults, and an incident-response starting point; an operator must supply organizational processes. [2]

**Privacy by design.** The European Commission describes GDPR principles including purpose limitation, data minimization, storage limitation, accuracy, integrity/confidentiality, and accountability. Those principles motivate in-memory bounded processing, no default analytics/logging, no code excerpts in reports, and clear limitations. Whether a particular operator's processing has a lawful basis or meets GDPR obligations is not determined by these controls. [3]

**Prompt injection.** OWASP identifies indirect prompt injection from external files as a risk and recommends reducing impact by constraining behavior, validating output, limiting privileges, segregating external content, and testing adversarially; no foolproof prevention is promised. The shipped CLI avoids an LLM entirely and never executes the diff. Agent instructions set a trust boundary, but instructions alone are not a technical guarantee for other agent hosts. [4]

**Agent packaging.** The Agent Skills specification requires a `SKILL.md` with YAML frontmatter and supports optional scripts, references, and assets. It recommends progressive disclosure and provides a validator. The repository follows the directory/frontmatter convention; an external skills-ref validator is not installed by default. [5]

**GitHub retrieval.** The GitHub CLI manual documents `gh pr diff [number]` and repository selection with `--repo`. The wrapper uses this read-only diff command and pipes output to the local scanner. GitHub retrieval and `gh` authentication remain under the user's account and GitHub's service terms. [6]

**AI governance.** The European Commission describes a risk-based AI Act with different categories and transparency duties, including Article 50 provisions. The original PDF's “minimal risk” conclusion cannot be adopted as a blanket legal classification: purpose, deployment, intended users, use context, and current law matter. No legal classification is asserted here. The CLI is deterministic and labels its output accordingly. [7]

**Privacy-framework currency.** NIST presents the Privacy Framework as a voluntary risk-management tool and now lists a version 1.1 initial public draft alongside the earlier framework. Documents should verify the applicable version at each review rather than treating a version number in the source PDF as permanently current. [8]

## Architecture conclusion

A local, deterministic, read-only analyzer is the lowest-complexity useful implementation of the supplied first-phase scope. It keeps the user in control and avoids a hosted database, service credentials, model provider, logging pipeline, or write-capable GitHub app. Size caps make the limits explicit. Human review remains necessary because text heuristics cannot prove correctness or safety.

Adding hosted inference, analytics, user accounts, persisted reports, or PR write actions materially changes data flows, privilege boundaries, legal roles, risk classification, and impact on affected people. Those changes require a new threat model, privacy notice and inventory, processor review, user authorization/oversight design, and regression/red-team tests before release.

## References

[1]: https://csrc.nist.gov/pubs/sp/800/218/final "NIST SP 800-218 Secure Software Development Framework"
[2]: https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf "NIST Cybersecurity Framework 2.0"
[3]: https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr_en "European Commission: GDPR principles"
[4]: https://genai.owasp.org/llmrisk/llm01-prompt-injection/ "OWASP LLM01:2025 Prompt Injection"
[5]: https://agentskills.io/specification "Agent Skills specification"
[6]: https://cli.github.com/manual/gh_pr_diff "GitHub CLI manual: gh pr diff"
[7]: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai "European Commission: AI regulatory framework"
[8]: https://www.nist.gov/privacy-framework "NIST Privacy Framework"
