"""Deterministic heuristic review. No model calls, network access, writes, or code execution."""

from __future__ import annotations

import re

from .diff_parser import ChangedFile, parse_unified_diff
from .models import Confidence, Finding, ReviewReport, Severity

MAX_DIFF_BYTES = 10 * 1024 * 1024
_PLACEHOLDERS = {"example", "placeholder", "changeme", "change-me", "dummy", "redacted", "your-key", "your-token", "test", "none", "null"}
_SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(password|passwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret)\b\s*[:=]\s*(['\"])([^'\"\n]{4,})['\"]"
)
_KNOWN_SECRET = re.compile(r"(?i)\b(?:AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk_(?:live|test)_[A-Za-z0-9]{16,})\b")
_SQL = re.compile(r"(?i)\b(?:SELECT|INSERT|UPDATE|DELETE)\b")
_MUTABLE_DEFAULT = re.compile(r"^\s*def\s+\w+\s*\([^\n)]*(?:=\s*(?:\[\s*\]|\{\s*\}))[\s,)]")
_DB_CALL = re.compile(r"(?i)\b(?:execute|fetch|query|select|insert|update|delete)\s*\(")
_LOOP = re.compile(r"^\s*(?:for\s+.+\s+in\s+.+:|while\s+.+:)")
_SLEEP = re.compile(r"\btime\.sleep\s*\(")
_READ_ALL = re.compile(r"\.(?:read|readlines)\s*\(\s*\)")

_RULES: dict[str, tuple[str, Severity, str, str]] = {
    "secret.literal": ("security", "critical", "Hard-coded credential-like value detected; the value was not copied into this report.", "Remove the credential from source, rotate it if it may have been exposed, and use a secret manager or environment-based configuration."),
    "sql.concat": ("security", "major", "SQL-like statement appears to be assembled with string concatenation or interpolation.", "Use parameterized queries or safe ORM query construction; verify the query behavior with tests."),
    "python.mutable-default": ("logic", "major", "Mutable list or dictionary default argument may be shared across calls.", "Use a None default and initialize a fresh collection inside the function."),
    "query.in-loop": ("performance", "major", "A loop and a database/API-like call occur close together; this may indicate repeated per-item I/O.", "Check the call path and consider batching or eager loading if it performs one request per item."),
    "async.blocking-sleep": ("performance", "major", "A blocking time.sleep call appears in a changed async function.", "Use an asynchronous wait or move blocking work out of the event loop."),
    "large.read": ("performance", "minor", "An unbounded read/readlines call may load a large resource into memory.", "If input size can be large, stream or process bounded chunks."),
}
_SEVERITY_ORDER = {"critical": 0, "major": 1, "minor": 2, "info": 3, "suggestion": 4}


def _is_placeholder(value: str) -> bool:
    normalized = re.sub(r"[^a-z0-9_-]", "", value.lower())
    return normalized in _PLACEHOLDERS or (len(normalized) >= 4 and set(normalized) <= {"x"})


def _test_context(path: str) -> bool:
    return bool(re.search(r"(?:^|[/_.-])(?:tests?|specs?|fixtures?)(?:[/_.-]|$)", path, re.I))


def _safe_path(path: str) -> str:
    path = "".join(ch for ch in path if ch >= " " and ch != "\x7f")
    return path[:240] or "<unknown>"


def _finding(rule_id: str, path: str, line: int, test_file: bool, counter: int) -> Finding:
    category, severity, message, fix = _RULES[rule_id]
    confidence: Confidence = "high" if rule_id == "secret.literal" else "medium"
    if test_file:
        confidence = "low" if rule_id != "secret.literal" else "medium"
    return Finding(
        id=f"F{counter:04d}", rule_id=rule_id, category=category,
        severity=severity, confidence=confidence, file=_safe_path(path), line=line,
        message=message, fix=fix,
    )


def _rules_for_line(text: str, path: str) -> list[str]:
    found: list[str] = []
    for match in _SECRET_ASSIGNMENT.finditer(text):
        if not _is_placeholder(match.group(3)):
            found.append("secret.literal")
            break
    if _KNOWN_SECRET.search(text):
        found.append("secret.literal")
    if _SQL.search(text) and ("+" in text or re.search(r"(?i)\bf\s*['\"]", text)):
        found.append("sql.concat")
    if path.lower().endswith(".py") and _MUTABLE_DEFAULT.search(text):
        found.append("python.mutable-default")
    if _READ_ALL.search(text):
        found.append("large.read")
    return found


def analyze_diff(text: str, repo: str = "local/input", pr: int | None = None) -> ReviewReport:
    if len(text.encode("utf-8", errors="replace")) > MAX_DIFF_BYTES:
        raise ValueError(f"Diff exceeds the {MAX_DIFF_BYTES // (1024 * 1024)} MiB processing limit.")
    files, total_files = parse_unified_diff(text)
    findings: list[Finding] = []
    counter = 1
    for changed_file in files:
        added = changed_file.added_lines
        test_file = _test_context(changed_file.path)
        async_context = any(re.search(r"\basync\s+def\b", item.text) for item in added)
        loop_lines = [i for i, item in enumerate(added) if _LOOP.search(item.text)]
        for index, item in enumerate(added):
            for rule_id in _rules_for_line(item.text, changed_file.path):
                findings.append(_finding(rule_id, changed_file.path, item.number, test_file, counter))
                counter += 1
            if async_context and _SLEEP.search(item.text):
                findings.append(_finding("async.blocking-sleep", changed_file.path, item.number, test_file, counter))
                counter += 1
            if _DB_CALL.search(item.text) and any(0 <= index - loop_index <= 5 for loop_index in loop_lines):
                findings.append(_finding("query.in-loop", changed_file.path, item.number, test_file, counter))
                counter += 1
    unique: dict[tuple[str, int, str], Finding] = {}
    for item in findings:
        unique.setdefault((item.file, item.line, item.rule_id), item)
    findings = list(unique.values())
    findings.sort(key=lambda item: (_SEVERITY_ORDER[item.severity], item.file.casefold(), item.line, item.rule_id))
    findings = [Finding(
        id=f"F{index:04d}", rule_id=item.rule_id, category=item.category,
        severity=item.severity, confidence=item.confidence, file=item.file,
        line=item.line, message=item.message, fix=item.fix,
    ) for index, item in enumerate(findings, start=1)]
    analyzed = min(total_files, len(files))
    truncated = total_files > analyzed
    if total_files == 0:
        summary = "No changes to review."
        assessment = "no_changes"
    elif findings:
        summary = f"Analyzed {analyzed} of {total_files} changed file(s); detected {len(findings)} heuristic finding(s)."
        assessment = "incomplete" if truncated else "findings_present"
    else:
        summary = f"Analyzed {analyzed} of {total_files} changed file(s); no configured heuristic matched."
        assessment = "incomplete" if truncated else "no_configured_findings"
    return ReviewReport(
        repo=repo, pr=pr, files_total=total_files, files_analyzed=analyzed,
        truncated=truncated, summary=summary, assessment=assessment,
        findings=tuple(findings),
    )
