# Review Best Practices

Use these as human-review prompts alongside the deterministic findings. They are not a substitute for understanding the changed code or its surrounding system.

## Correctness and maintainability

- Verify the behavior against the stated requirement and adjacent call sites.
- Check input validation, error handling, resource cleanup, and meaningful tests.
- Prefer names and abstractions that make data flow and authorization boundaries clear.

## Security and privacy

- Trace untrusted input into SQL, shell commands, HTML, templates, paths, and redirects.
- Check authentication and authorization before sensitive operations; verify tenant/object-level access.
- Never commit credentials. Use established cryptographic libraries and sound key-management practices.
- Minimize personal data in logs and outputs; avoid copying identifiers into review comments.
- Review dependency provenance, supported versions, and vulnerability advisories.

## Performance and resilience

- Look for N+1 database or network calls, unbounded reads, blocking I/O in async paths, and unbounded loops.
- Consider timeouts, retries, rate limits, cancellation, idempotency, and graceful failure.

## Framework notes (context-dependent)

- **React:** follow Hooks rules, include required effect dependencies, use stable keys, and escape untrusted output.
- **FastAPI:** validate request/response models, enforce authorization, and avoid slow work in request handlers.
- **SQLAlchemy:** scope sessions appropriately and parameterize raw SQL.

## Heuristic caveat

A pattern match is a review lead, not proof. Test fixtures, generated code, context, language semantics, and the rest of the repository can change severity and confidence. Conversely, absence of matches does not establish safety.
