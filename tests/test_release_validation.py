"""Offline checks that the release documentation stays consistent with the package.

These tests do not build or install anything. Packaging itself is validated by
``scripts/validate_release.py``, which runs against ``dist/`` and a clean
virtual environment.
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
README = PROJECT_ROOT / "README.md"
TRANSPORT_DOC = PROJECT_ROOT / "docs" / "http-transport.md"
RELEASE_NOTES = PROJECT_ROOT / "docs" / "releases" / "0.9.0.md"

PYTHON_BLOCK_PATTERN = re.compile(
    r"^```python\n(.*?)^```",
    re.MULTILINE | re.DOTALL,
)


def _project_version() -> str:
    text = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, flags=re.MULTILINE)
    assert match is not None, "no version found in pyproject.toml"
    return match.group(1)


def _python_blocks(path: Path) -> list[tuple[int, str]]:
    """Return (line number, source) for every non-REPL ```python block."""
    text = path.read_text(encoding="utf-8")
    blocks = []
    for match in PYTHON_BLOCK_PATTERN.finditer(text):
        source = match.group(1)
        stripped = source.lstrip()
        # Interactive blocks interleave prompts and output, so they are not
        # compilable source and are excluded from syntax validation.
        if stripped.startswith(">>>"):
            continue
        line_number = text.count("\n", 0, match.start()) + 1
        blocks.append((line_number, source))
    return blocks


def _documented_paths() -> list[Path]:
    return [README, TRANSPORT_DOC, RELEASE_NOTES]


@pytest.mark.parametrize(
    "path",
    _documented_paths(),
    ids=lambda path: path.name,
)
def test_documentation_python_examples_are_valid_syntax(path: Path) -> None:
    blocks = _python_blocks(path)
    assert blocks, f"expected at least one python example in {path.name}"

    for line_number, source in blocks:
        compile(source, f"{path.name}:{line_number}", "exec")


@pytest.mark.parametrize(
    "path",
    _documented_paths(),
    ids=lambda path: path.name,
)
def test_documentation_examples_use_public_api_only(path: Path) -> None:
    """User-facing examples must not reach into private package internals.

    ``scripts/validate_release.py`` is allowed to read ``Mlb._session`` for
    release validation; documentation is not.
    """
    for line_number, source in _python_blocks(path):
        assert "_session" not in source, (
            f"{path.name}:{line_number} uses the private _session attribute"
        )
        assert "mlbstatsapi.mlb_dataadapter" not in source, (
            f"{path.name}:{line_number} imports an internal module"
        )


def test_release_notes_exist_for_the_declared_version() -> None:
    version = _project_version()
    notes = PROJECT_ROOT / "docs" / "releases" / f"{version}.md"
    assert notes.is_file(), f"missing release notes for version {version}"
    assert notes.read_text(encoding="utf-8").startswith(
        f"# python-mlb-statsapi {version}"
    )


def test_documented_user_agent_matches_the_declared_version() -> None:
    """The documented User-Agent must track the version the build will produce."""
    version = _project_version()
    expected = f"python-mlb-statsapi/{version}"

    for path in (README, TRANSPORT_DOC, RELEASE_NOTES):
        text = path.read_text(encoding="utf-8")
        documented = set(re.findall(r"python-mlb-statsapi/[0-9][^\s`\"']*", text))
        assert documented == {expected}, (
            f"{path.name} documents User-Agent versions {sorted(documented)}, "
            f"expected only {expected!r}"
        )


def test_ci_watches_the_current_release_branch() -> None:
    workflow = PROJECT_ROOT / ".github" / "workflows" / "build-and-test.yml"
    text = workflow.read_text(encoding="utf-8")
    major, minor, _ = _project_version().split(".")

    assert f"release/{major}.{minor}.0" in text
    assert "- main" in text
