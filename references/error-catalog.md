# Error Catalog

The CLI implements a small subset of these checks against added diff lines. Every item is a heuristic, not a proof of vulnerability or correctness.

## Security

- **Credential literals:** suspicious credential assignments and selected token prefixes are detected; values are omitted from output. False negatives are expected. Remove and rotate exposed credentials.
- **SQL construction:** SQL-like lines with string concatenation/interpolation are flagged. Use parameterized queries. The rule cannot establish whether the value is attacker-controlled.
- **Unvalidated redirects:** human-review guidance only. Validate targets with an allowlist and account for URL parsing edge cases.

## Logic

- **Mutable Python defaults:** list/dict literal defaults can be shared across invocations. Prefer `None` and initialize a fresh collection.
- **Off-by-one and race conditions:** review guidance only; inspect bounds, shared mutable state, synchronization, and tests.

## Performance

- **I/O in loops:** a nearby loop and query-like call are flagged as a possible N+1 pattern. Verify actual control flow and batching options.
- **Blocking sleep in async code:** a `time.sleep` call in a changed hunk with an added `async def` may block the event loop. Use asynchronous I/O where appropriate.
- **Unbounded reads:** `read()`/`readlines()` without a size may use excessive memory for untrusted or large inputs. Stream or bound input.

## Style

Nested conditions, magic numbers, and missing public API documentation are review prompts only; the diff-only CLI does not claim to detect them reliably.
