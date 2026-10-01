"""CLI interface for local diff review."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .analyzer import MAX_DIFF_BYTES, analyze_diff
from .report import render_json, render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze a unified diff with bounded, deterministic heuristics.")
    parser.add_argument("--repo", default="local/input", help="Repository label for report metadata (default: local/input).")
    parser.add_argument("--pr", type=int, help="Pull request number for report metadata.")
    parser.add_argument("--diff-file", type=Path, help="Read a unified diff from this file; otherwise read stdin.")
    parser.add_argument("--require-nonempty", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="Report format (default: markdown).")
    return parser


def _read_input(path: Path | None) -> str:
    if path is None:
        data = sys.stdin.buffer.read(MAX_DIFF_BYTES + 1)
    else:
        with path.open("rb") as source:
            data = source.read(MAX_DIFF_BYTES + 1)
    if len(data) > MAX_DIFF_BYTES:
        raise ValueError(f"Diff exceeds the {MAX_DIFF_BYTES // (1024 * 1024)} MiB processing limit.")
    return data.decode("utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.pr is not None and args.pr <= 0:
        parser.error("--pr must be a positive integer")
    if not args.repo or len(args.repo) > 200 or any(not ch.isprintable() for ch in args.repo):
        parser.error("--repo must be a short, printable label")
    try:
        diff = _read_input(args.diff_file)
        if args.require_nonempty and not diff.strip():
            raise ValueError("GitHub returned no diff; verify the PR number, repository, and access.")
        report = analyze_diff(diff, repo=args.repo, pr=args.pr)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"axiom-review: {exc}", file=sys.stderr)
        return 2
    output = render_json(report) if args.format == "json" else render_markdown(report)
    sys.stdout.write(output)
    return 0
