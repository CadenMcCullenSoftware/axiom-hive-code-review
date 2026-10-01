# Records of Processing Activities — Working Draft

This is an engineering inventory for the local prototype, not a completed GDPR Article 30 record or a legal determination. The responsible organization must identify controller/processor roles and complete applicable fields before deployment.

## Activity: local code-diff analysis

| Field | Current technical fact / open question |
| --- | --- |
| Purpose | User-requested, advisory analysis of a unified code diff. |
| Data subjects | Potential repository contributors if a diff contains identifiable information; not known by the application. |
| Data categories | Code/comments, file paths, incidental personal data or credentials, PR/repository labels. |
| Data sources | User-supplied diff, or GitHub PR diff retrieved through the user's configured `gh` client. |
| Recipients | Local process and caller; the GitHub API is contacted only when the wrapper is used. The application has no model provider. |
| Storage / retention | In-memory during execution; the application does not persist diffs or reports. Output destinations and platform logs are operator-controlled/external. |
| Security controls | Read-only PR diff, size/file caps, no code execution, no source excerpts in findings, no app logs, no runtime dependencies. |
| Controller / processor | Must be determined by the actual operator, service terms, and deployment. Not asserted here. |
| Lawful basis | Not determined by this repository. Seek qualified legal advice for the actual processing context. |
| International transfers / subprocessors | GitHub retrieval may involve GitHub processing under the user's account and applicable service terms. Region, transfer mechanism, contract status, and roles require operator verification. No other app subprocessor is configured. |
| DPIA | Not determined here. Assess based on actual intended purpose, scale, affected people, data, and applicable law; revisit on material change. |
| Rights handling | The CLI has no persistent personal-data store or account interface; external operator/platform rights channels are separate. A service deployment requires an explicit procedure. |

## Review checklist before distribution or hosting

Identify the legal entity and contact; determine controller/processor roles; validate purpose and lawful basis; identify all vendors/regions and contractual safeguards; set actual retention and deletion procedures; assess rights handling and DPIA need; test security and incident response; and update the public notice. Do not reuse generic values from the source specification as if they were verified for a new deployment.
