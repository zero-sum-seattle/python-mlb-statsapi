"""Offline tests for ``scripts/prepare_release.py``.

Every test that prepares a release works on a temporary copy of the release
files, so the repository checkout is never modified. Synthetic fixtures pin
exact transformation output; copies of the real files prove the script still
matches the repository's current structure.
"""

from __future__ import annotations

import ast
import importlib.util
import re
import shutil
import sys
import types
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PREPARE_RELEASE = PROJECT_ROOT / "scripts" / "prepare_release.py"
RELEASE_NOTES_DIR = PROJECT_ROOT / "docs" / "releases"

USER_AGENT_PATTERN = re.compile(r"python-mlb-statsapi/[0-9][^\s`\"']*")


def _load_script() -> types.ModuleType:
    """Import scripts/prepare_release.py, which is not an installable package."""
    spec = importlib.util.spec_from_file_location(
        "prepare_release_under_test",
        PREPARE_RELEASE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    # dataclasses resolve string annotations through sys.modules.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


prepare = _load_script()
Version = prepare.Version
PrepareReleaseError = prepare.PrepareReleaseError

CURRENT = Version(2, 3, 4)
TARGET = Version(2, 3, 5)

PYTHON_SUPPORT = """\
## Python support

python-mlb-statsapi requires Python >=3.10.

CI validates Python 3.10 through 3.14.
"""

SYNTHETIC_PYPROJECT = """\
[tool.poetry]
name = "python-mlb-statsapi"
version = "2.3.4"

[tool.poetry.dependencies]
python = ">=3.10"
httpx = { version = ">=0.28.1,<1.0", optional = true }
"""

SYNTHETIC_RELEASE_INDEX = """\
# Release Notes

Release notes describe each published version.

## Releases

- [2.3.4](releases/2.3.4.md) — current fixes
- [2.3.3](releases/2.3.3.md) — older fixes
"""

SYNTHETIC_MKDOCS = """\
site_name: Example
nav:
  - Home: index.md
  - Release Notes:
      - Overview: releases.md
      - 2.3.4: releases/2.3.4.md
      - 2.3.3: releases/2.3.3.md

plugins:
  - search
"""

SYNTHETIC_README = """\
# python-mlb-statsapi

Library-created clients send a versioned User-Agent. The current package version sends `python-mlb-statsapi/2.3.4`. See the docs.
"""

SYNTHETIC_TRANSPORT_DOC = """\
# HTTP Transport

This document describes the HTTP transport behavior of the current release,
version 2.3.4.

Version 2.3.3 introduced something else.

See [the 2.3.4 release notes](releases/2.3.4.md) for a shorter summary of what
changed in the current release.

```text
python-mlb-statsapi/2.3.4
```
"""

SYNTHETIC_RELEASE_TESTS = """\
from pathlib import Path

RELEASE_NOTES_DIR = Path("docs") / "releases"

CURRENT_RELEASE_NOTES = RELEASE_NOTES_DIR / "2.3.4.md"

# Historical notes.

HISTORICAL_RELEASE_NOTES = (
    RELEASE_NOTES_DIR / "2.3.2.md",
    RELEASE_NOTES_DIR / "2.3.3.md",
)

OTHER = 1
"""

SYNTHETIC_CURRENT_NOTES = f"""\
# python-mlb-statsapi 2.3.4

Version 2.3.4 fixes things.

```python
import mlbstatsapi
```

{PYTHON_SUPPORT}"""


def _write_synthetic_repo(root: Path) -> Path:
    files = {
        "pyproject.toml": SYNTHETIC_PYPROJECT,
        "README.md": SYNTHETIC_README,
        "mkdocs.yml": SYNTHETIC_MKDOCS,
        "docs/releases.md": SYNTHETIC_RELEASE_INDEX,
        "docs/http-transport.md": SYNTHETIC_TRANSPORT_DOC,
        "docs/releases/2.3.2.md": "# python-mlb-statsapi 2.3.2\n",
        "docs/releases/2.3.3.md": "# python-mlb-statsapi 2.3.3\n",
        "docs/releases/2.3.4.md": SYNTHETIC_CURRENT_NOTES,
        "tests/test_release_validation.py": SYNTHETIC_RELEASE_TESTS,
    }
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return root


def _copy_real_repo(root: Path) -> Path:
    """Copy only the files release preparation reads or writes."""
    for relative in (
        "pyproject.toml",
        "README.md",
        "mkdocs.yml",
        "docs/releases.md",
        "docs/http-transport.md",
        "tests/test_release_validation.py",
    ):
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PROJECT_ROOT / relative, destination)
    shutil.copytree(RELEASE_NOTES_DIR, root / "docs" / "releases")
    return root


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _next_patch(version) -> Version:
    return Version(version.major, version.minor, version.patch + 1)


def _classified_release_notes(test_source: str) -> tuple[str, set[str]]:
    """Return (current, historical) note file names from the validation tests."""
    current = None
    historical: set[str] = set()
    for node in ast.parse(test_source).body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        name = getattr(node.targets[0], "id", None)
        if name == "CURRENT_RELEASE_NOTES":
            current = node.value.right.value
        elif name == "HISTORICAL_RELEASE_NOTES":
            historical = {element.right.value for element in node.value.elts}
    assert current is not None
    return current, historical


# ---------------------------------------------------------------------------
# Version parsing
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1.1.3", Version(1, 1, 3)),
        ("0.0.0", Version(0, 0, 0)),
        ("2.0.0", Version(2, 0, 0)),
        ("10.20.30", Version(10, 20, 30)),
    ],
)
def test_valid_versions_are_parsed(text: str, expected) -> None:
    version = prepare.parse_version(text)

    assert version == expected
    assert str(version) == text


@pytest.mark.parametrize(
    "text",
    [
        "",
        "1",
        "1.1",
        "1.1.3.4",
        "v1.1.3",
        "1.1.3rc1",
        "1.1.3-rc.1",
        "1.1.3.dev0",
        "1.1.3.post1",
        "1.1.3+local",
        "01.1.3",
        "1.01.3",
        "1.1.03",
        " 1.1.3",
        "1.1.3\n",
        "1..3",
        "a.b.c",
        "１.1.3",
    ],
)
def test_invalid_versions_are_rejected(text: str) -> None:
    with pytest.raises(PrepareReleaseError, match="invalid version"):
        prepare.parse_version(text)


def test_versions_compare_numerically() -> None:
    assert prepare.parse_version("1.10.0") > prepare.parse_version("1.9.9")
    assert prepare.parse_version("2.0.0") > prepare.parse_version("1.99.99")


# ---------------------------------------------------------------------------
# Individual transformations
# ---------------------------------------------------------------------------


def test_pyproject_version_is_updated_without_touching_dependency_versions() -> None:
    updated = prepare.update_pyproject(SYNTHETIC_PYPROJECT, CURRENT, TARGET)

    assert updated == SYNTHETIC_PYPROJECT.replace(
        'version = "2.3.4"', 'version = "2.3.5"'
    )
    assert 'httpx = { version = ">=0.28.1,<1.0", optional = true }' in updated


@pytest.mark.parametrize(
    "text",
    [
        SYNTHETIC_PYPROJECT.replace('version = "2.3.4"', 'version = "9.9.9"'),
        SYNTHETIC_PYPROJECT + '\n[project]\nversion = "2.3.4"\n',
    ],
    ids=["missing", "duplicated"],
)
def test_pyproject_requires_exactly_one_current_version(text: str) -> None:
    with pytest.raises(PrepareReleaseError, match="pyproject.toml: expected exactly one"):
        prepare.update_pyproject(text, CURRENT, TARGET)


def test_release_notes_skeleton_has_no_invented_content() -> None:
    notes = prepare.render_release_notes(TARGET, PYTHON_SUPPORT)

    assert notes.startswith("# python-mlb-statsapi 2.3.5\n")
    assert notes.endswith(PYTHON_SUPPORT)
    assert notes.count(prepare.PLACEHOLDER) == 3
    # The release-notes tests require a compilable python example per file.
    block = re.search(r"^```python\n(.*?)^```", notes, re.MULTILINE | re.DOTALL)
    assert block is not None
    compile(block.group(1), "skeleton", "exec")


def test_python_support_section_is_carried_forward_up_to_the_next_heading() -> None:
    notes = (
        "# python-mlb-statsapi 2.3.4\n\n"
        f"{PYTHON_SUPPORT}\n### Detail\n\nKept.\n\n## Thanks\n\nNot carried.\n"
    )

    section = prepare.extract_python_support(notes, path=Path("x.md"))

    assert section == PYTHON_SUPPORT + "\n### Detail\n\nKept.\n"


@pytest.mark.parametrize(
    "notes",
    ["# python-mlb-statsapi 2.3.4\n", PYTHON_SUPPORT + "\n" + PYTHON_SUPPORT],
    ids=["missing", "duplicated"],
)
def test_python_support_section_must_exist_exactly_once(notes: str) -> None:
    with pytest.raises(PrepareReleaseError, match="'## Python support' heading"):
        prepare.extract_python_support(notes, path=Path("x.md"))


def test_release_index_gets_the_new_release_first() -> None:
    updated = prepare.update_release_index(SYNTHETIC_RELEASE_INDEX, CURRENT, TARGET)

    assert updated == SYNTHETIC_RELEASE_INDEX.replace(
        "## Releases\n\n",
        "## Releases\n\n- [2.3.5](releases/2.3.5.md) — TODO(release): one-line summary\n",
    )


@pytest.mark.parametrize(
    "text",
    [
        SYNTHETIC_RELEASE_INDEX.replace("- [2.3.4](releases/2.3.4.md) — current fixes\n", ""),
        SYNTHETIC_RELEASE_INDEX.replace(
            "- [2.3.4](releases/2.3.4.md) — current fixes\n"
            "- [2.3.3](releases/2.3.3.md) — older fixes\n",
            "- [2.3.3](releases/2.3.3.md) — older fixes\n"
            "- [2.3.4](releases/2.3.4.md) — current fixes\n",
        ),
        SYNTHETIC_RELEASE_INDEX.replace("## Releases", "## Versions"),
    ],
    ids=["current-missing", "current-not-first", "heading-renamed"],
)
def test_release_index_rejects_unexpected_structure(text: str) -> None:
    with pytest.raises(PrepareReleaseError, match="docs/releases.md: expected exactly one"):
        prepare.update_release_index(text, CURRENT, TARGET)


def test_mkdocs_nav_gets_the_new_release_page_first() -> None:
    updated = prepare.update_mkdocs_nav(SYNTHETIC_MKDOCS, CURRENT, TARGET)

    assert updated == SYNTHETIC_MKDOCS.replace(
        "      - Overview: releases.md\n",
        "      - Overview: releases.md\n      - 2.3.5: releases/2.3.5.md\n",
    )


@pytest.mark.parametrize(
    "text",
    [
        SYNTHETIC_MKDOCS.replace("      - 2.3.4: releases/2.3.4.md\n", ""),
        SYNTHETIC_MKDOCS.replace("      - Overview: releases.md\n", ""),
        SYNTHETIC_MKDOCS
        + "  - Again:\n      - Overview: releases.md\n      - 2.3.4: releases/2.3.4.md\n",
    ],
    ids=["current-missing", "overview-missing", "duplicated"],
)
def test_mkdocs_nav_rejects_unexpected_structure(text: str) -> None:
    with pytest.raises(PrepareReleaseError, match="mkdocs.yml: expected exactly one"):
        prepare.update_mkdocs_nav(text, CURRENT, TARGET)


def test_readme_user_agent_version_is_updated() -> None:
    updated = prepare.update_readme(SYNTHETIC_README, CURRENT, TARGET)

    assert updated == SYNTHETIC_README.replace(
        "python-mlb-statsapi/2.3.4", "python-mlb-statsapi/2.3.5"
    )


@pytest.mark.parametrize(
    "text",
    [
        SYNTHETIC_README.replace("python-mlb-statsapi/2.3.4", "python-mlb-statsapi/2.3.3"),
        SYNTHETIC_README + SYNTHETIC_README,
    ],
    ids=["stale-version", "duplicated"],
)
def test_readme_rejects_unexpected_structure(text: str) -> None:
    with pytest.raises(PrepareReleaseError, match="README.md: expected exactly one"):
        prepare.update_readme(text, CURRENT, TARGET)


def test_transport_doc_version_link_and_user_agent_are_updated() -> None:
    updated = prepare.update_transport_doc(SYNTHETIC_TRANSPORT_DOC, CURRENT, TARGET)

    assert updated == (
        SYNTHETIC_TRANSPORT_DOC.replace("version 2.3.4.", "version 2.3.5.")
        .replace(
            "[the 2.3.4 release notes](releases/2.3.4.md)",
            "[the 2.3.5 release notes](releases/2.3.5.md)",
        )
        .replace("python-mlb-statsapi/2.3.4", "python-mlb-statsapi/2.3.5")
    )
    # Historical statements about other versions are left alone.
    assert "Version 2.3.3 introduced something else." in updated


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("version 2.3.4.", "version 2.3.3."),
        ("[the 2.3.4 release notes](releases/2.3.4.md)", "the release notes"),
        ("python-mlb-statsapi/2.3.4\n", "python-mlb-statsapi/<version>\n"),
    ],
    ids=["version-statement", "notes-link", "user-agent"],
)
def test_transport_doc_rejects_unexpected_structure(old: str, new: str) -> None:
    text = SYNTHETIC_TRANSPORT_DOC.replace(old, new)

    with pytest.raises(PrepareReleaseError, match="docs/http-transport.md: expected exactly one"):
        prepare.update_transport_doc(text, CURRENT, TARGET)


def test_release_validation_tests_track_the_new_current_notes() -> None:
    updated = prepare.update_release_validation_tests(SYNTHETIC_RELEASE_TESTS, CURRENT, TARGET)

    assert updated == SYNTHETIC_RELEASE_TESTS.replace(
        'CURRENT_RELEASE_NOTES = RELEASE_NOTES_DIR / "2.3.4.md"',
        'CURRENT_RELEASE_NOTES = RELEASE_NOTES_DIR / "2.3.5.md"',
    ).replace(
        '    RELEASE_NOTES_DIR / "2.3.3.md",\n)',
        '    RELEASE_NOTES_DIR / "2.3.3.md",\n    RELEASE_NOTES_DIR / "2.3.4.md",\n)',
    )
    assert _classified_release_notes(updated) == ("2.3.5.md", {"2.3.2.md", "2.3.3.md", "2.3.4.md"})


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        ('/ "2.3.4.md"\n\n#', '/ "2.3.3.md"\n\n#', "CURRENT_RELEASE_NOTES"),
        (
            '    RELEASE_NOTES_DIR / "2.3.3.md",\n)',
            '    RELEASE_NOTES_DIR / "2.3.3.md",\n    RELEASE_NOTES_DIR / "2.3.4.md",\n)',
            "already listed",
        ),
        (
            "HISTORICAL_RELEASE_NOTES = (",
            "HISTORICAL_RELEASE_NOTES = tuple(",
            "HISTORICAL_RELEASE_NOTES tuple",
        ),
    ],
    ids=["current-mismatch", "current-already-historical", "historical-reshaped"],
)
def test_release_validation_tests_reject_unexpected_structure(
    old: str, new: str, message: str
) -> None:
    text = SYNTHETIC_RELEASE_TESTS.replace(old, new)
    assert text != SYNTHETIC_RELEASE_TESTS

    with pytest.raises(PrepareReleaseError, match=message):
        prepare.update_release_validation_tests(text, CURRENT, TARGET)


# ---------------------------------------------------------------------------
# End-to-end preparation on temporary copies
# ---------------------------------------------------------------------------


def test_preparing_a_copy_of_the_real_repository(tmp_path: Path, capsys) -> None:
    root = _copy_real_repo(tmp_path)
    current = prepare.read_current_version(root)
    target = _next_patch(current)
    historical_before = {
        path.name: path.read_bytes() for path in (root / "docs" / "releases").glob("*.md")
    }

    assert prepare.main([str(target), "--project-root", str(root)]) == 0

    output = capsys.readouterr().out
    assert f"Prepared release {target} (previous release {current})" in output
    assert f"created   docs/releases/{target}.md" in output
    assert "Remaining manual steps" in output
    assert "python scripts/validate_release.py" in output

    assert prepare.read_current_version(root) == target

    # Existing notes, including the previous current release, stay byte-identical.
    for name, content in historical_before.items():
        assert (root / "docs" / "releases" / name).read_bytes() == content
    notes = (root / "docs" / "releases" / f"{target}.md").read_text(encoding="utf-8")
    assert notes.startswith(f"# python-mlb-statsapi {target}\n")
    assert prepare.PLACEHOLDER in notes

    index = (root / "docs" / "releases.md").read_text(encoding="utf-8")
    entries = re.findall(r"^- \[([^\]]+)\]", index, re.MULTILINE)
    assert entries[:2] == [str(target), str(current)]

    mkdocs = (root / "mkdocs.yml").read_text(encoding="utf-8")
    assert (
        "      - Overview: releases.md\n"
        f"      - {target}: releases/{target}.md\n"
        f"      - {current}: releases/{current}.md\n"
    ) in mkdocs

    expected_agent = {f"python-mlb-statsapi/{target}"}
    for relative in ("README.md", "docs/http-transport.md"):
        text = (root / relative).read_text(encoding="utf-8")
        assert set(USER_AGENT_PATTERN.findall(text)) == expected_agent, relative
    transport = (root / "docs" / "http-transport.md").read_text(encoding="utf-8")
    assert f"current release,\nversion {target}." in transport
    assert f"[the {target} release notes](releases/{target}.md)" in transport

    # Every notes file stays classified exactly once, as test_release_validation requires.
    test_source = (root / "tests" / "test_release_validation.py").read_text(encoding="utf-8")
    current_notes, historical_notes = _classified_release_notes(test_source)
    assert current_notes == f"{target}.md"
    assert f"{current}.md" in historical_notes
    assert {path.name for path in (root / "docs" / "releases").glob("*.md")} == {
        current_notes,
        *historical_notes,
    }


@pytest.mark.parametrize("flag", ["--dry-run", "--check"])
def test_dry_run_reports_changes_without_writing(tmp_path: Path, capsys, flag: str) -> None:
    root = _write_synthetic_repo(tmp_path)
    before = _snapshot(root)

    assert prepare.main(["2.3.5", flag, "--project-root", str(root)]) == 0

    assert _snapshot(root) == before
    output = capsys.readouterr().out
    assert "Nothing was written" in output
    assert "--- /dev/null\n+++ b/docs/releases/2.3.5.md" in output
    assert '-version = "2.3.4"\n+version = "2.3.5"' in output
    assert "create    docs/releases/2.3.5.md" in output


def test_dry_run_reports_refusal_without_writing(tmp_path: Path, capsys) -> None:
    root = _write_synthetic_repo(tmp_path)
    (root / "README.md").write_text("# no user agent sentence\n", encoding="utf-8")
    before = _snapshot(root)

    assert prepare.main(["2.3.5", "--dry-run", "--project-root", str(root)]) == 1

    assert _snapshot(root) == before
    assert "README.md: expected exactly one" in capsys.readouterr().err


@pytest.mark.parametrize("version", ["2.3.4", "2.3.3", "2.3.2", "1.0.0"])
def test_existing_or_older_versions_are_refused(tmp_path: Path, capsys, version: str) -> None:
    root = _write_synthetic_repo(tmp_path)
    before = _snapshot(root)

    assert prepare.main([version, "--project-root", str(root)]) == 1

    assert _snapshot(root) == before
    message = capsys.readouterr().err
    assert "already exists" in message or "older than the current version 2.3.4" in message


def test_rerunning_a_completed_preparation_is_refused(tmp_path: Path, capsys) -> None:
    root = _write_synthetic_repo(tmp_path)
    assert prepare.main(["2.3.5", "--project-root", str(root)]) == 0
    prepared = _snapshot(root)
    capsys.readouterr()

    assert prepare.main(["2.3.5", "--project-root", str(root)]) == 1

    assert _snapshot(root) == prepared
    assert "2.3.5 already exists" in capsys.readouterr().err


def test_invalid_version_is_refused_by_the_cli(tmp_path: Path, capsys) -> None:
    root = _write_synthetic_repo(tmp_path)
    before = _snapshot(root)

    assert prepare.main(["v2.3.5", "--project-root", str(root)]) == 1

    assert _snapshot(root) == before
    assert "invalid version 'v2.3.5'" in capsys.readouterr().err


@pytest.mark.parametrize(
    "applied",
    [
        "pyproject.toml",
        "docs/releases/2.3.5.md",
        "docs/releases.md",
        "mkdocs.yml",
        "README.md",
        "docs/http-transport.md",
        "tests/test_release_validation.py",
    ],
)
def test_partially_prepared_release_is_refused(tmp_path: Path, capsys, applied: str) -> None:
    """A release started by hand or interrupted is reported, never compounded."""
    root = _write_synthetic_repo(tmp_path)
    plan = prepare.plan_release(root, TARGET)
    (change,) = [change for change in plan.changes if change.path.as_posix() == applied]
    (root / change.path).write_text(change.updated, encoding="utf-8")
    before = _snapshot(root)

    assert prepare.main(["2.3.5", "--project-root", str(root)]) == 1

    assert _snapshot(root) == before
    message = capsys.readouterr().err
    assert "looks partially prepared" in message
    already, missing = message.split("Does not refer to it yet:")
    assert applied in already
    assert applied not in missing


def test_unexpected_structure_writes_nothing(tmp_path: Path, capsys) -> None:
    """A late structural failure must not leave earlier files edited."""
    root = _write_synthetic_repo(tmp_path)
    tests_file = root / "tests" / "test_release_validation.py"
    tests_file.write_text(
        SYNTHETIC_RELEASE_TESTS.replace("HISTORICAL_RELEASE_NOTES = (", "HISTORICAL = ("),
        encoding="utf-8",
    )
    before = _snapshot(root)

    assert prepare.main(["2.3.5", "--project-root", str(root)]) == 1

    assert _snapshot(root) == before
    assert "HISTORICAL_RELEASE_NOTES tuple" in capsys.readouterr().err


def test_missing_previous_release_notes_are_refused(tmp_path: Path, capsys) -> None:
    root = _write_synthetic_repo(tmp_path)
    (root / "docs" / "releases" / "2.3.4.md").unlink()

    assert prepare.main(["2.3.5", "--project-root", str(root)]) == 1

    assert "docs/releases/2.3.4.md: file not found" in capsys.readouterr().err
    assert not (root / "docs" / "releases" / "2.3.5.md").exists()


def test_failed_write_restores_every_file(tmp_path: Path, monkeypatch) -> None:
    root = _write_synthetic_repo(tmp_path)
    before = _snapshot(root)
    plan = prepare.plan_release(root, TARGET)
    real_write = prepare._write_atomically
    calls = {"count": 0}

    def failing_write(path: Path, content: str) -> None:
        calls["count"] += 1
        if calls["count"] == 4:
            raise OSError(28, "No space left on device", str(path))
        real_write(path, content)

    monkeypatch.setattr(prepare, "_write_atomically", failing_write)

    with pytest.raises(PrepareReleaseError, match="restored"):
        prepare.apply_plan(root, plan)

    assert _snapshot(root) == before


def test_rewritten_files_keep_their_permissions(tmp_path: Path) -> None:
    root = _write_synthetic_repo(tmp_path)
    readme = root / "README.md"
    readme.chmod(0o644)

    assert prepare.main(["2.3.5", "--project-root", str(root)]) == 0

    assert readme.stat().st_mode & 0o777 == 0o644


def test_line_endings_and_unrelated_formatting_are_preserved(tmp_path: Path) -> None:
    root = _write_synthetic_repo(tmp_path)
    readme = root / "README.md"
    readme.write_bytes(SYNTHETIC_README.encode("utf-8") + b"\n\n  trailing  \n")

    assert prepare.main(["2.3.5", "--project-root", str(root)]) == 0

    assert readme.read_bytes() == (
        SYNTHETIC_README.replace("2.3.4", "2.3.5").encode("utf-8") + b"\n\n  trailing  \n"
    )


# ---------------------------------------------------------------------------
# Real repository (read-only)
# ---------------------------------------------------------------------------


def test_real_repository_can_plan_the_next_release() -> None:
    """Fails if a release file drifts from the structure the script edits."""
    current = prepare.read_current_version(PROJECT_ROOT)

    plan = prepare.plan_release(PROJECT_ROOT, _next_patch(current))

    assert len(plan.changes) == 7


@pytest.mark.parametrize(
    "path",
    [PROJECT_ROOT / "docs" / "releases.md", *sorted(RELEASE_NOTES_DIR.glob("*.md"))],
    ids=lambda path: path.name,
)
def test_release_notes_have_no_unfilled_placeholders(path: Path) -> None:
    """Notes generated by prepare_release.py must be written before release."""
    assert prepare.PLACEHOLDER not in path.read_text(encoding="utf-8"), (
        f"{path.relative_to(PROJECT_ROOT)} still contains {prepare.PLACEHOLDER} "
        "placeholders from scripts/prepare_release.py"
    )
