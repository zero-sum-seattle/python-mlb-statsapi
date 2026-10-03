"""Prepare the version-specific files for a new python-mlb-statsapi release.

Applies the same edits every release has needed so far (see the 1.1.2
preparation commit for the reference set):

* bump the version in ``pyproject.toml``
* create a release-notes skeleton at ``docs/releases/<version>.md``
* list the release first in ``docs/releases.md``
* add the notes page to the Release Notes section of ``mkdocs.yml``
* update the current User-Agent version in ``README.md``
* update the current version, release-notes link, and User-Agent in
  ``docs/http-transport.md``
* point ``CURRENT_RELEASE_NOTES`` in ``tests/test_release_validation.py`` at
  the new notes and move the previous release into ``HISTORICAL_RELEASE_NOTES``

Every edit is computed in memory first. Each one must find its expected source
text exactly once; otherwise nothing is written and the script explains which
file did not match. The script never commits, tags, pushes, or publishes.

Usage::

    python scripts/prepare_release.py 1.1.3
    python scripts/prepare_release.py 1.1.3 --dry-run

``--dry-run`` (alias ``--check``) runs every version and structure check and
prints the diff that would be applied without changing any file. Exit status
is 0 when preparation succeeds (or would succeed) and 1 when it is refused.
"""

from __future__ import annotations

import argparse
import difflib
import importlib.util
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable, NamedTuple

# Repository-relative paths. POSIX paths keep messages identical on every OS.
PYPROJECT = PurePosixPath("pyproject.toml")
README = PurePosixPath("README.md")
MKDOCS = PurePosixPath("mkdocs.yml")
RELEASE_INDEX = PurePosixPath("docs/releases.md")
TRANSPORT_DOC = PurePosixPath("docs/http-transport.md")
RELEASE_NOTES_DIR = PurePosixPath("docs/releases")
RELEASE_VALIDATION_TESTS = PurePosixPath("tests/test_release_validation.py")

# Marks text a maintainer must replace before the release ships. An offline
# test fails while any release notes still contain it.
PLACEHOLDER = "TODO(release)"

# Every published version so far is a plain MAJOR.MINOR.PATCH with no prefix,
# prerelease, or local segment, so nothing broader is accepted. [0-9] rather
# than \d keeps non-ASCII digits out.
VERSION_PATTERN = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")

PYTHON_SUPPORT_HEADING = "## Python support"


class PrepareReleaseError(Exception):
    """Release preparation was refused; no files were changed."""


class Version(NamedTuple):
    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass(frozen=True)
class FileChange:
    """New content for one repository file; ``original`` is None when created."""

    path: PurePosixPath
    original: str | None
    updated: str


@dataclass(frozen=True)
class ReleasePlan:
    current: Version
    target: Version
    changes: tuple[FileChange, ...]


# ---------------------------------------------------------------------------
# Version parsing
# ---------------------------------------------------------------------------


def parse_version(text: str) -> Version:
    match = VERSION_PATTERN.fullmatch(text)
    if match is None:
        raise PrepareReleaseError(
            f"invalid version {text!r}: expected MAJOR.MINOR.PATCH such as 1.1.3 "
            "(no 'v' prefix, prerelease suffix, or leading zeros)"
        )
    major, minor, patch = (int(part) for part in match.groups())
    return Version(major, minor, patch)


def _version_ref(version: Version) -> str:
    """Regex for *version* that does not also match e.g. 1.1.30 or 11.1.3."""
    return rf"(?<![0-9.]){re.escape(str(version))}(?!\.?[0-9])"


# ---------------------------------------------------------------------------
# Text transformations
# ---------------------------------------------------------------------------


def _replace_once(
    text: str,
    pattern: str,
    replacement: str | Callable[[re.Match[str]], str],
    *,
    path: PurePosixPath,
    expected: str,
) -> str:
    """Apply *replacement* to the single match of *pattern* in *text*.

    Zero or several matches mean the file no longer has the structure this
    script was written against, so the caller must fix it by hand.
    """
    compiled = re.compile(pattern, re.MULTILINE)
    count = len(compiled.findall(text))
    if count != 1:
        raise PrepareReleaseError(
            f"{path}: expected exactly one {expected}, found {count}"
        )
    return compiled.sub(replacement, text, count=1)


def _require_once(text: str, pattern: str, *, path: PurePosixPath, expected: str) -> None:
    count = len(re.findall(pattern, text, flags=re.MULTILINE))
    if count != 1:
        raise PrepareReleaseError(
            f"{path}: expected exactly one {expected}, found {count}"
        )


def update_pyproject(text: str, current: Version, target: Version) -> str:
    # The version is the only top-level `version = "..."` line; dependency
    # tables such as httpx's carry `version` inline and are not matched.
    return _replace_once(
        text,
        rf'^version = "{re.escape(str(current))}"$',
        f'version = "{target}"',
        path=PYPROJECT,
        expected=f'line `version = "{current}"`',
    )


def update_release_index(text: str, current: Version, target: Version) -> str:
    escaped = re.escape(str(current))
    current_entry = rf"- \[{escaped}\]\(releases/{escaped}\.md\) "
    _require_once(
        text,
        rf"^{current_entry}",
        path=RELEASE_INDEX,
        expected=f"list entry for {current}",
    )
    new_entry = f"- [{target}](releases/{target}.md) — {PLACEHOLDER}: one-line summary\n"
    return _replace_once(
        text,
        rf"^## Releases\n\n(?={current_entry})",
        lambda match: match.group(0) + new_entry,
        path=RELEASE_INDEX,
        expected=f"'## Releases' section whose first entry is {current}",
    )


def update_mkdocs_nav(text: str, current: Version, target: Version) -> str:
    current_page = rf"- {re.escape(str(current))}: releases/{re.escape(str(current))}\.md\n"
    return _replace_once(
        text,
        rf"^(?P<indent>[ ]+)- Overview: releases\.md\n(?=(?P=indent){current_page})",
        lambda match: (
            match.group(0) + f"{match.group('indent')}- {target}: releases/{target}.md\n"
        ),
        path=MKDOCS,
        expected=(
            f"Release Notes nav entry 'Overview: releases.md' followed directly "
            f"by '{current}: releases/{current}.md'"
        ),
    )


def update_readme(text: str, current: Version, target: Version) -> str:
    sentence = "The current package version sends `python-mlb-statsapi/"
    return _replace_once(
        text,
        rf"({re.escape(sentence)}){re.escape(str(current))}(`)",
        rf"\g<1>{target}\g<2>",
        path=README,
        expected=f"'{sentence}{current}`' sentence",
    )


def update_transport_doc(text: str, current: Version, target: Version) -> str:
    escaped = re.escape(str(current))
    text = _replace_once(
        text,
        # The sentence is wrapped, so any whitespace may separate the words.
        rf"(behavior of the current release,\s+version ){escaped}(\.)",
        rf"\g<1>{target}\g<2>",
        path=TRANSPORT_DOC,
        expected=f"'current release, version {current}.' statement",
    )
    text = _replace_once(
        text,
        rf"\[the {escaped} release notes\]\(releases/{escaped}\.md\)",
        f"[the {target} release notes](releases/{target}.md)",
        path=TRANSPORT_DOC,
        expected=f"'[the {current} release notes](releases/{current}.md)' link",
    )
    return _replace_once(
        text,
        rf"^python-mlb-statsapi/{escaped}$",
        f"python-mlb-statsapi/{target}",
        path=TRANSPORT_DOC,
        expected=f"'python-mlb-statsapi/{current}' User-Agent example line",
    )


_HISTORICAL_BLOCK = re.compile(
    r"^HISTORICAL_RELEASE_NOTES = \(\n"
    r"(?P<entries>(?:[ ]+RELEASE_NOTES_DIR / \"[^\"\n]+\.md\",\n)+)"
    r"\)$",
    re.MULTILINE,
)
_HISTORICAL_ENTRY = re.compile(
    r"^(?P<indent>[ ]+)RELEASE_NOTES_DIR / \"(?P<name>[^\"\n]+)\",$",
    re.MULTILINE,
)


def update_release_validation_tests(
    text: str, current: Version, target: Version
) -> str:
    text = _replace_once(
        text,
        rf'^CURRENT_RELEASE_NOTES = RELEASE_NOTES_DIR / "{re.escape(str(current))}\.md"$',
        f'CURRENT_RELEASE_NOTES = RELEASE_NOTES_DIR / "{target}.md"',
        path=RELEASE_VALIDATION_TESTS,
        expected=f'line `CURRENT_RELEASE_NOTES = RELEASE_NOTES_DIR / "{current}.md"`',
    )

    blocks = list(_HISTORICAL_BLOCK.finditer(text))
    if len(blocks) != 1:
        raise PrepareReleaseError(
            f"{RELEASE_VALIDATION_TESTS}: expected exactly one "
            "HISTORICAL_RELEASE_NOTES tuple of RELEASE_NOTES_DIR / \"<version>.md\" "
            f"entries, found {len(blocks)}"
        )
    block = blocks[0]
    entries = list(_HISTORICAL_ENTRY.finditer(block.group("entries")))
    if f"{current}.md" in {entry.group("name") for entry in entries}:
        raise PrepareReleaseError(
            f"{RELEASE_VALIDATION_TESTS}: {current}.md is already listed in "
            "HISTORICAL_RELEASE_NOTES while it is also the current release"
        )
    indent = entries[-1].group("indent")
    new_entry = f'{indent}RELEASE_NOTES_DIR / "{current}.md",\n'
    insert_at = block.end("entries")
    return text[:insert_at] + new_entry + text[insert_at:]


def extract_python_support(notes: str, *, path: PurePosixPath) -> str:
    """Return the '## Python support' section, carried forward unchanged.

    The current release notes must state the CI-validated Python range, so the
    previous release's wording is reused instead of being invented here.
    """
    heading_pattern = rf"^{re.escape(PYTHON_SUPPORT_HEADING)}$"
    _require_once(
        notes,
        heading_pattern,
        path=path,
        expected=f"'{PYTHON_SUPPORT_HEADING}' heading",
    )
    heading = re.search(heading_pattern, notes, re.MULTILINE)
    # The section runs until the next level-one or level-two heading.
    next_heading = re.compile(r"^#{1,2} ", re.MULTILINE).search(notes, heading.end())
    end = len(notes) if next_heading is None else next_heading.start()
    return notes[heading.start() : end].strip() + "\n"


def render_release_notes(target: Version, python_support: str) -> str:
    # Release-notes tests require a compilable python block in every notes
    # file, so the skeleton carries a placeholder one.
    return (
        f"# python-mlb-statsapi {target}\n"
        "\n"
        f"{PLACEHOLDER}: Summarize version {target} in one or two sentences.\n"
        "\n"
        "## Changes\n"
        "\n"
        f"{PLACEHOLDER}: Describe each user-visible change and link the pull "
        "requests that introduced it.\n"
        "\n"
        "```python\n"
        f"# {PLACEHOLDER}: Replace with an example relevant to this release.\n"
        "from mlbstatsapi import Mlb\n"
        "```\n"
        "\n"
        f"{python_support}"
    )


# ---------------------------------------------------------------------------
# Repository inspection
# ---------------------------------------------------------------------------


def _read(root: Path, relative: PurePosixPath) -> str:
    path = root / relative
    if not path.is_file():
        raise PrepareReleaseError(f"{relative}: file not found under {root}")
    # newline="" keeps the existing line endings byte-for-byte.
    with path.open(encoding="utf-8", newline="") as handle:
        return handle.read()


def _load_validator():
    """Import scripts/validate_release.py so both scripts read one version."""
    module_path = Path(__file__).resolve().with_name("validate_release.py")
    spec = importlib.util.spec_from_file_location("_validate_release", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_current_version(root: Path) -> Version:
    validator = _load_validator()
    try:
        declared = validator._read_expected_version(root)
    except validator.ValidationError as exc:
        raise PrepareReleaseError(str(exc)) from exc
    try:
        return parse_version(declared)
    except PrepareReleaseError as exc:
        raise PrepareReleaseError(
            f"{PYPROJECT}: declared version is not usable: {exc}"
        ) from exc


def find_target_references(root: Path, target: Version) -> dict[str, bool]:
    """Report, per release file, whether it already refers to *target*."""
    ref = _version_ref(target)
    escaped = re.escape(str(target))
    notes = RELEASE_NOTES_DIR / f"{target}.md"

    def contains(relative: PurePosixPath, pattern: str) -> bool:
        path = root / relative
        if not path.is_file():
            return False
        return re.search(pattern, path.read_text(encoding="utf-8"), re.MULTILINE) is not None

    return {
        str(PYPROJECT): contains(PYPROJECT, rf'^version = "{escaped}"$'),
        str(notes): (root / notes).exists(),
        str(RELEASE_INDEX): contains(RELEASE_INDEX, rf"releases/{escaped}\.md"),
        str(MKDOCS): contains(MKDOCS, rf"releases/{escaped}\.md"),
        str(README): contains(README, rf"python-mlb-statsapi/{ref}"),
        str(TRANSPORT_DOC): contains(
            TRANSPORT_DOC,
            rf"current release,\s+version {ref}"
            rf"|releases/{escaped}\.md"
            rf"|python-mlb-statsapi/{ref}",
        ),
        str(RELEASE_VALIDATION_TESTS): contains(RELEASE_VALIDATION_TESTS, rf'"{escaped}\.md"'),
    }


def _refuse_existing_target(target: Version, references: dict[str, bool]) -> None:
    present = [name for name, found in references.items() if found]
    if not present:
        return
    missing = [name for name, found in references.items() if not found]
    if not missing:
        raise PrepareReleaseError(
            f"{target} already exists: every release file already refers to it. "
            "Nothing was changed. Choose a newer version."
        )
    lines = [
        f"{target} looks partially prepared, so nothing was changed.",
        "Already refers to it:",
        *(f"  - {name}" for name in present),
        "Does not refer to it yet:",
        *(f"  - {name}" for name in missing),
        "Restore the files above to the previous release (for example with "
        "`git restore` and by removing a new notes file) and re-run, or finish "
        "the remaining edits by hand.",
    ]
    raise PrepareReleaseError("\n".join(lines))


def plan_release(root: Path, target: Version) -> ReleasePlan:
    """Validate the repository and compute every edit without writing."""
    current = read_current_version(root)
    if target < current:
        raise PrepareReleaseError(
            f"{target} is older than the current version {current}; "
            "only a newer version can be prepared"
        )
    # Checked before the structural edits so a re-run or a hand-started
    # release is reported as such rather than as a confusing mismatch.
    _refuse_existing_target(target, find_target_references(root, target))
    if target == current:
        raise PrepareReleaseError(f"{target} is already the current version")

    previous_notes_path = RELEASE_NOTES_DIR / f"{current}.md"
    previous_notes = _read(root, previous_notes_path)
    python_support = extract_python_support(previous_notes, path=previous_notes_path)

    edits = (
        (PYPROJECT, update_pyproject),
        (RELEASE_INDEX, update_release_index),
        (MKDOCS, update_mkdocs_nav),
        (README, update_readme),
        (TRANSPORT_DOC, update_transport_doc),
        (RELEASE_VALIDATION_TESTS, update_release_validation_tests),
    )
    changes = []
    for relative, transform in edits:
        original = _read(root, relative)
        changes.append(
            FileChange(relative, original, transform(original, current, target))
        )
    changes.insert(
        1,
        FileChange(
            RELEASE_NOTES_DIR / f"{target}.md",
            None,
            render_release_notes(target, python_support),
        ),
    )
    return ReleasePlan(current, target, tuple(changes))


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------


def _write_atomically(path: Path, content: str) -> None:
    fd, temp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
        # mkstemp creates the file as 0600; keep the original permissions.
        shutil.copymode(path, temp_name)
        os.replace(temp_name, path)
    except BaseException:
        Path(temp_name).unlink(missing_ok=True)
        raise


def apply_plan(root: Path, plan: ReleasePlan) -> None:
    """Write every change, restoring the original files if any write fails."""
    written: list[FileChange] = []
    try:
        for change in plan.changes:
            path = root / change.path
            if change.original is None:
                # "x" refuses to overwrite a file that appeared after planning.
                with path.open("x", encoding="utf-8", newline="") as handle:
                    written.append(change)
                    handle.write(change.updated)
            else:
                _write_atomically(path, change.updated)
                written.append(change)
    except BaseException as exc:
        for change in reversed(written):
            path = root / change.path
            if change.original is None:
                path.unlink(missing_ok=True)
            else:
                _write_atomically(path, change.original)
        if not isinstance(exc, OSError):
            raise
        raise PrepareReleaseError(
            f"writing {exc.filename or 'a release file'} failed ({exc.strerror or exc}); "
            "every file written so far was restored"
        ) from exc


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def format_diff(plan: ReleasePlan) -> str:
    chunks = []
    for change in plan.changes:
        before = "/dev/null" if change.original is None else f"a/{change.path.as_posix()}"
        chunks.extend(
            difflib.unified_diff(
                (change.original or "").splitlines(keepends=True),
                change.updated.splitlines(keepends=True),
                fromfile=before,
                tofile=f"b/{change.path.as_posix()}",
            )
        )
    return "".join(chunks)


def format_summary(plan: ReleasePlan, *, dry_run: bool) -> str:
    target, current = plan.target, plan.current
    notes = (RELEASE_NOTES_DIR / f"{target}.md").as_posix()
    heading = (
        f"Dry run: preparing {target} (current release {current}) would change "
        "the files below. Nothing was written."
        if dry_run
        else f"Prepared release {target} (previous release {current})."
    )
    lines = [heading, "", "Files:"]
    for change in plan.changes:
        action = "create" if change.original is None else "modify"
        if not dry_run:
            action += "d"
        lines.append(f"  {action:<9} {change.path.as_posix()}")
    lines += [
        "",
        "Remaining manual steps:",
        f"  1. Write the release notes in {notes}: replace every {PLACEHOLDER} "
        f"marker and confirm the Python support section copied from {current} "
        "is still accurate.",
        f"  2. Replace the {PLACEHOLDER} summary for {target} in {RELEASE_INDEX.as_posix()}.",
        "  3. Review the complete diff (git diff).",
        "  4. Validate:",
        "       poetry run pytest tests/ --ignore=tests/external_tests",
        "       poetry run pytest tests/external_tests/",
        "       rm -rf dist && poetry build",
        "       python scripts/validate_release.py",
        "       poetry run twine check dist/*",
        "  5. Commit and open the release pull request. Tagging, publishing, and "
        "GitHub Releases stay manual; this script does none of them.",
    ]
    if dry_run:
        lines += [
            "",
            f"Run without --dry-run to apply: python scripts/prepare_release.py {target}",
        ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("version", help="release to prepare, e.g. 1.1.3")
    parser.add_argument(
        "--dry-run",
        "--check",
        dest="dry_run",
        action="store_true",
        help="run every check and print the diff without changing any file",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root containing pyproject.toml",
    )
    args = parser.parse_args(argv)
    root = args.project_root.resolve()

    try:
        plan = plan_release(root, parse_version(args.version))
        if args.dry_run:
            print(format_diff(plan))
        else:
            apply_plan(root, plan)
    except PrepareReleaseError as exc:
        print(f"Release preparation refused: {exc}", file=sys.stderr)
        return 1

    print(format_summary(plan, dry_run=args.dry_run))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
