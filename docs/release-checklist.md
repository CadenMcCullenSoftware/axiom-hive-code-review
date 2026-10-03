# Release Checklist

Before a tagged or distributed release:

- [ ] Run `make check`; record Python version and commit.
- [ ] Review the diff for credentials, personal data, license compliance, and unexpected network/write actions.
- [ ] Confirm runtime dependency changes (currently none) and action commit pins.
- [ ] Verify Markdown and JSON output, including secret-value non-disclosure and the incomplete-file indicator.
- [ ] Update version, changelog, report schema, skill metadata, and documentation for material behavior/data-flow changes.
- [ ] Reassess threat model, privacy notice, data inventory, RoPA draft, safety, and human-rights impact for new services or data use.
- [ ] Confirm customer-facing commercial terms with the rights holders; the repository's proprietary notice is not a customer agreement.
- [x] Enable GitHub private vulnerability reporting in repository settings.
- [ ] Verify at least one maintainer receives and monitors its notifications before broad external distribution.
- [ ] Do not claim independent red-team, legal review, compliance, or certification unless actually completed and documented.
- [ ] Keep release and any PR publication decisions under human control.
