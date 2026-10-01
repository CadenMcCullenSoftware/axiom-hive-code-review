"""Human-readable and machine-readable report renderers."""

from __future__ import annotations

import json

from .models import ReviewReport


def render_json(report: ReviewReport) -> str:
    return json.dumps(report.as_dict(), ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def _inline_code(value: str) -> str:
    """Escape untrusted metadata before placing it inside Markdown inline code."""
    value = "".join(ch for ch in value if ch.isprintable())
    return value.replace("\\", "\\\\").replace("`", "\\`").replace("\n", " ").replace("\r", " ")


def render_markdown(report: ReviewReport) -> str:
    pr = f"#{report.pr}" if report.pr is not None else "not specified"
    status = "INCOMPLETE — file limit reached" if report.truncated else report.assessment.replace("_", " ").upper()
    lines = [
        "# Axiom Hive Code Review",
        "",
        "> Automated heuristic analysis only. Findings require human verification; no finding is a certification or a guarantee that code is safe.",
        "",
        f"- **Repository:** `{_inline_code(report.repo)}`",
        f"- **Pull request:** {pr}",
        f"- **Changed files:** {report.files_analyzed}/{report.files_total}",
        f"- **Assessment:** {status}",
        f"- **AI-generated:** {'yes' if report.ai_assisted else 'no (deterministic rules only)'}",
        "",
        "## Summary",
        "",
        report.summary,
        "",
        "## Findings",
        "",
    ]
    if not report.findings:
        lines.append("No configured heuristic findings.")
    else:
        for finding in report.findings:
            lines.extend([
                f"### {finding.id} · {finding.severity.upper()} · {finding.category}",
                "",
                f"- **Location:** `{_inline_code(finding.file)}:{finding.line}`",
                f"- **Rule:** `{_inline_code(finding.rule_id)}` · **Confidence:** {finding.confidence}",
                f"- **Observation:** {finding.message}",
                f"- **Suggested next step:** {finding.fix}",
                "",
            ])
    lines.extend([
        "## Limitations",
        "",
        "This report evaluates only added lines in the supplied diff with a small set of regular-expression and context heuristics. It does not execute code, inspect the full repository, verify exploitability, or prove the absence of defects. Secret detection is incomplete; rotate any credential that may have been exposed. Review the complete change and test it in an authorized environment.",
        "",
    ])
    return "\n".join(lines)
