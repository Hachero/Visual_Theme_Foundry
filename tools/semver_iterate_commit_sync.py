"""
tools/semver_iterate_commit_sync.py - SemVer version bump utility for VisualThemeFoundry.

Purpose:
    Inventory project-owned text files, find SemVer references, enforce a
    single canonical version stream, bump MAJOR/MINOR/PATCH, update files, and
    optionally create a commit.

SemVer alignment (source: semver.org, npm docs, Cargo docs):
    - Canonical release format is MAJOR.MINOR.PATCH (x.y.z).
    - PATCH increments for backward-compatible bug fixes.
    - MINOR increments for backward-compatible feature additions.
    - MAJOR increments for backward-incompatible API changes.

Scope and safety:
    - The script scans only project-owned files and excludes vendored/tooling
      directories to avoid unrelated version noise.
    - It aborts if multiple SemVer values are discovered.
    - It rewrites only version-shaped tokens, preserving local text context.

Discovery patterns:
    1) version/ver labels on the same line, with optional v-prefix.
       Example: "Version: 1.4.0" or "ver v1.4.0"
    2) v-prefixed SemVer tokens.
       Example: "v1.4.0"
    3) JSON root-style version field.
       Example: "version": "1.4.0"

Usage examples:
    python tools/semver_iterate_commit_sync.py --dry-run
    python tools/semver_iterate_commit_sync.py --part patch
    python tools/semver_iterate_commit_sync.py --part minor
    python tools/semver_iterate_commit_sync.py --part major --no-commit

Exit behavior:
    Returns non-zero on validation failures, ambiguous versions, git failures,
    or write issues.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".rst",
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".scss",
    ".sass",
    ".css",
    ".html",
    ".htm",
    ".xml",
    ".ps1",
    ".sh",
    ".bat",
    ".cmd",
}

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".vscode",
    "_imports",
    "quarantine",
    "_references",
}

SKIP_PATH_PREFIXES = {
    "_docs/Licenses/",
}

SKIP_FILES = {
    "tools/semver_iterate_commit_sync.py",
    "_docs/agent_notes_log.md",
}

# SemVer core x.y.z (no prerelease/build metadata for this repository policy).
SEMVER_CORE = r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"

# NOTE: These regexes intentionally avoid generic numeric matches like 0.12
# unless the token is version-shaped by context.
PATTERN_LABELLED = re.compile(
    rf"(?i)\b(?P<label>version|ver)\b(?P<between>[^\n]{{0,40}}?)(?P<prefix>[vV]?)(?P<value>{SEMVER_CORE})\b"
)
PATTERN_V_PREFIX = re.compile(rf"(?P<prefix>\b[vV])(?P<value>{SEMVER_CORE})\b")
PATTERN_JSON_VERSION = re.compile(rf'"(?P<key>version)"\s*:\s*"(?P<value>{SEMVER_CORE})"')
SEMVER_EXACT = re.compile(rf"^{SEMVER_CORE}$")


@dataclass(frozen=True)
class MatchRecord:
    """
    Represent one discovered version match.

    Attributes:
        file_path: Path to file containing the match.
        line_number: 1-based line number for quick inspection.
        matched_text: Raw text matched by the regex.
        version: Parsed x.y.z version token.
    """

    file_path: Path
    line_number: int
    matched_text: str
    version: str


def iter_candidate_files(repo_root: Path) -> Iterable[Path]:
    """
    Yield text-like files under repo root, skipping known cache/tool folders.
    """
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        rel_path = path.relative_to(repo_root).as_posix()
        if rel_path in SKIP_FILES:
            continue
        if any(rel_path.startswith(prefix) for prefix in SKIP_PATH_PREFIXES):
            continue

        parts = path.relative_to(repo_root).parts
        if any(part in SKIP_DIRS for part in parts):
            continue
        if any(part.startswith(".") and part not in {".", ".."} for part in parts):
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS or path.name in {"README", "LICENSE", "Dockerfile"}:
            yield path


def read_text(path: Path) -> str:
    """
    Read file as UTF-8 with replacement for undecodable bytes.
    """
    return path.read_text(encoding="utf-8", errors="replace")


def line_number_from_offset(text: str, offset: int) -> int:
    """
    Convert a character offset into a 1-based line number.
    """
    return text.count("\n", 0, offset) + 1


def find_version_matches(file_path: Path, text: str) -> list[MatchRecord]:
    """
    Find all version-like matches governed by discovery patterns.
    """
    matches: list[MatchRecord] = []
    for regex in (PATTERN_LABELLED, PATTERN_V_PREFIX, PATTERN_JSON_VERSION):
        for m in regex.finditer(text):
            value = m.group("value")
            matches.append(
                MatchRecord(
                    file_path=file_path,
                    line_number=line_number_from_offset(text, m.start()),
                    matched_text=m.group(0),
                    version=value,
                )
            )
    return matches


def parse_semver_core(version_text: str) -> tuple[int, int, int]:
    """
    Parse x.y.z SemVer core string into numeric tuple.
    """
    if not SEMVER_EXACT.match(version_text):
        raise ValueError(f"Invalid SemVer core token: {version_text}")
    major_s, minor_s, patch_s = version_text.split(".")
    return int(major_s), int(minor_s), int(patch_s)


def bump_version(version_text: str, part: str) -> str:
    """
    Bump SemVer core value by part.

    Examples:
        bump patch: 1.4.0 -> 1.4.1
        bump minor: 1.4.9 -> 1.5.0
        bump major: 1.9.9 -> 2.0.0
    """
    major, minor, patch = parse_semver_core(version_text)
    if part == "patch":
        patch += 1
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError(f"Unsupported bump part: {part}")
    return f"{major}.{minor}.{patch}"


def rewrite_text(content: str, current_version: str, next_version: str) -> tuple[str, int]:
    """
    Rewrite occurrences of current_version only where discovery patterns match.

    Returns:
        (new_content, replacement_count)
    """
    replacement_count = 0

    def repl_labelled(m: re.Match[str]) -> str:
        nonlocal replacement_count
        if m.group("value") != current_version:
            return m.group(0)
        replacement_count += 1
        return f"{m.group('label')}{m.group('between')}{m.group('prefix')}{next_version}"

    def repl_vprefix(m: re.Match[str]) -> str:
        nonlocal replacement_count
        if m.group("value") != current_version:
            return m.group(0)
        replacement_count += 1
        return f"{m.group('prefix')}{next_version}"

    def repl_json(m: re.Match[str]) -> str:
        nonlocal replacement_count
        if m.group("value") != current_version:
            return m.group(0)
        replacement_count += 1
        return f'"{m.group("key")}": "{next_version}"'

    out = PATTERN_LABELLED.sub(repl_labelled, content)
    out = PATTERN_V_PREFIX.sub(repl_vprefix, out)
    out = PATTERN_JSON_VERSION.sub(repl_json, out)
    return out, replacement_count


def run_git(repo_root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    """
    Run a git command in repo root and return completed process.
    """
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )


def commit_changes(repo_root: Path, files: list[Path], current_version: str, next_version: str, commit_message: str | None) -> None:
    """
    Stage and commit only touched files.
    """
    inside_repo = run_git(repo_root, ["rev-parse", "--is-inside-work-tree"])
    if inside_repo.returncode != 0 or inside_repo.stdout.strip().lower() != "true":
        raise RuntimeError("Not inside a git repository; cannot create commit.")

    rel_files = [str(path.relative_to(repo_root)) for path in files]
    add_result = run_git(repo_root, ["add", "--", *rel_files])
    if add_result.returncode != 0:
        raise RuntimeError(f"git add failed:\n{add_result.stderr.strip()}")

    message = commit_message or next_version
    commit_result = run_git(repo_root, ["commit", "-m", message, "--", *rel_files])
    if commit_result.returncode != 0:
        stderr = commit_result.stderr.strip()
        stdout = commit_result.stdout.strip()
        details = stderr or stdout or "Unknown git commit error"
        raise RuntimeError(f"git commit failed:\n{details}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(description="Bump SemVer x.y.z version across repository files.")
    parser.add_argument("--root", default=".", help="Project root to scan (default: current directory).")
    parser.add_argument(
        "--part",
        choices=("patch", "minor", "major"),
        default="patch",
        help="Which SemVer part to increment (default: patch).",
    )
    parser.add_argument("--dry-run", action="store_true", help="Inventory and report changes without writing files.")
    parser.add_argument("--no-commit", action="store_true", help="Write files but skip git commit.")
    parser.add_argument("--commit-message", default=None, help="Override commit message.")
    return parser.parse_args(argv)


def resolve_commit_message(next_version: str, override_message: str | None) -> tuple[str, str]:
    """
    Resolve commit message and indicate whether it is auto-generated or user-supplied.

    Returns:
        (message, source_label)
    """
    if override_message is not None:
        return override_message, "custom"
    return next_version, "auto"


def main(argv: list[str]) -> int:
    """
    Entry point.
    """
    args = parse_args(argv)
    repo_root = Path(args.root).resolve()

    if not repo_root.exists() or not repo_root.is_dir():
        print(f"ERROR: Root path does not exist or is not a directory: {repo_root}")
        return 2

    print(f"Scanning repository root: {repo_root}")

    all_matches: list[MatchRecord] = []
    file_cache: dict[Path, str] = {}

    for file_path in iter_candidate_files(repo_root):
        text = read_text(file_path)
        file_cache[file_path] = text
        all_matches.extend(find_version_matches(file_path, text))

    if not all_matches:
        print("ERROR: No SemVer x.y.z matches found with the configured patterns.")
        return 3

    unique_versions = sorted({m.version for m in all_matches})
    print(f"Discovered version tokens: {', '.join(unique_versions)}")

    if len(unique_versions) != 1:
        print("ERROR: Multiple SemVer x.y.z versions detected. Aborting to prevent inconsistent bump.")
        for version in unique_versions:
            sample = next((m for m in all_matches if m.version == version), None)
            if sample is not None:
                rel = sample.file_path.relative_to(repo_root)
                print(f"  - {version} (example: {rel}:{sample.line_number} -> {sample.matched_text})")
        return 4

    current_version = unique_versions[0]
    try:
        next_version = bump_version(current_version, args.part)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 5

    print(f"Bump target: {current_version} -> {next_version} ({args.part})")

    commit_message, commit_message_source = resolve_commit_message(next_version, args.commit_message)
    print(f"Commit message ({commit_message_source}): {commit_message}")

    changed_files: list[Path] = []
    total_replacements = 0

    for file_path, original in file_cache.items():
        rewritten, count = rewrite_text(original, current_version, next_version)
        if count <= 0:
            continue

        # Verify no stale current-version matches remain in this file.
        stale = [m for m in find_version_matches(file_path, rewritten) if m.version == current_version]
        if stale:
            rel = file_path.relative_to(repo_root)
            print(f"ERROR: Stale version matches remained after rewrite in {rel}")
            return 7

        total_replacements += count
        changed_files.append(file_path)
        if not args.dry_run:
            file_path.write_text(rewritten, encoding="utf-8", newline="")

    if not changed_files:
        print("No files needed updates.")
        return 0

    print(f"Updated files: {len(changed_files)}")
    print(f"Total replacements: {total_replacements}")
    for path in changed_files:
        print(f"  - {path.relative_to(repo_root)}")

    if args.dry_run:
        print("Dry run complete; no files were written and no commit was created.")
        return 0

    if args.no_commit:
        print("Write complete; commit skipped (--no-commit).")
        return 0

    try:
        commit_changes(repo_root, changed_files, current_version, next_version, commit_message)
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        return 8

    print("Commit created successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
