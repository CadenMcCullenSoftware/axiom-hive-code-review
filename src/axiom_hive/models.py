"""Small immutable data objects shared by the analyzer and renderers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

Severity = Literal["critical", "major", "minor", "info", "suggestion"]
Confidence = Literal["high", "medium", "low"]


@dataclass(frozen=True)
class Finding:
    id: str
    rule_id: str
    category: str
    severity: Severity
    confidence: Confidence
    file: str
    line: int
    message: str
    fix: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class ReviewReport:
    repo: str
    pr: int | None
    files_total: int
    files_analyzed: int
    truncated: bool
    summary: str
    assessment: str
    findings: tuple[Finding, ...]
    ai_assisted: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": "1.0",
            "metadata": {
                "repository": self.repo,
                "pull_request": self.pr,
                "files_total": self.files_total,
                "files_analyzed": self.files_analyzed,
                "truncated": self.truncated,
                "ai_assisted": self.ai_assisted,
            },
            "summary": self.summary,
            "assessment": self.assessment,
            "findings": [item.as_dict() for item in self.findings],
        }
