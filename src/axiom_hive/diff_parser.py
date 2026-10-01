"""Bounded parsing for unified Git diffs. Diff text is data and is never executed."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass

MAX_ANALYZED_FILES = 300
_HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


@dataclass(frozen=True)
class AddedLine:
    number: int
    text: str


@dataclass(frozen=True)
class ChangedFile:
    path: str
    added_lines: tuple[AddedLine, ...]
    is_new: bool = False


def _decode_git_path(value: str) -> str:
    value = value.strip()
    if value.startswith('"'):
        try:
            decoded = ast.literal_eval(value)
            if isinstance(decoded, str):
                value = decoded
        except (SyntaxError, ValueError):
            pass
    if value.startswith("b/"):
        value = value[2:]
    value = "".join(ch for ch in value if ch.isprintable())
    return value[:240] or "<unknown>"


def parse_unified_diff(text: str, max_files: int = MAX_ANALYZED_FILES) -> tuple[list[ChangedFile], int]:
    """Return analyzable files and total diff file sections, ignoring removed/context lines."""
    if not text.strip():
        return [], 0
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith("diff --git ")]
    if not starts:
        raise ValueError("Input is not a recognized unified Git diff.")

    files: list[ChangedFile] = []
    total = len(starts)
    for index, start in enumerate(starts[:max_files]):
        end = starts[index + 1] if index + 1 < len(starts) else len(lines)
        block = lines[start:end]
        path = "<unknown>"
        is_new = False
        for line in block:
            if line.startswith("new file mode "):
                is_new = True
            if line.startswith("+++ "):
                raw_path = line[4:]
                path = "<deleted>" if raw_path == "/dev/null" else _decode_git_path(raw_path)
                break

        added: list[AddedLine] = []
        new_line_number: int | None = None
        for line in block:
            hunk = _HUNK.match(line)
            if hunk:
                new_line_number = int(hunk.group(1))
                continue
            if new_line_number is None or line.startswith("\\ No newline"):
                continue
            if line.startswith("+") and not line.startswith("+++"):
                added.append(AddedLine(new_line_number, line[1:]))
                new_line_number += 1
            elif line.startswith(" "):
                new_line_number += 1
            elif line.startswith("-"):
                continue
        files.append(ChangedFile(path=path, added_lines=tuple(added), is_new=is_new))
    return files, total
