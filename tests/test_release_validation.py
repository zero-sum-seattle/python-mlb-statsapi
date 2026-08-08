"""Offline checks for the release validator, deterministic CI, and release docs.

Three groups of checks live here:

* documentation consistency for the current release
* unit coverage for ``scripts/validate_release.py`` helpers and failure messages
* the deterministic CI contract (release branch triggers, Python matrix, twine)

Nothing here builds the real package, creates a virtual environment, installs
an artifact, or makes a network request. Synthetic wheel ZIPs and
source-distribution tarballs stand in for real artifacts, and clean-install
steps are stubbed. Real packaging is validated by running
``scripts/validate_release.py`` against ``dist/``.
"""

from __future__ import annotations

import importlib.util
import io
import re
import sys
import tarfile
import types
import zipfile
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
README = PROJECT_ROOT / "README.md"
TRANSPORT_DOC = PROJECT_ROOT / "docs" / "http-transport.md"
PUBLIC_API_DOC = PROJECT_ROOT / "docs" / "public-api.md"
RELEASE_NOTES_DIR = PROJECT_ROOT / "docs" / "releases"
PYPROJECT = PROJECT_ROOT / "pyproject.toml"
POETRY_LOCK = PROJECT_ROOT / "poetry.lock"
VALIDATE_RELEASE = PROJECT_ROOT / "scripts" / "validate_release.py"
OFFLINE_WORKFLOW = PROJECT_ROOT / ".github" / "workflows" / "build-and-test.yml"
EXTERNAL_WORKFLOW = PROJECT_ROOT / ".github" / "workflows" / "external-tests.yml"

# Release notes for the version this branch is preparing. Kept explicit so the
# current-document checks do not depend on the pyproject version bump, which is
# owned by a separate issue.
CURRENT_RELEASE_NOTES = RELEASE_NOTES_DIR / "1.0.0.md"

# Historical notes keep their own version-specific statements and must not be
# rewritten to match the current release.
HISTORICAL_RELEASE_NOTES = (
    RELEASE_NOTES_DIR / "0.7.1.md",
    RELEASE_NOTES_DIR / "0.8.0.md",
    RELEASE_NOTES_DIR / "0.9.0.md",
)

# Deterministic CI contract for the 1.0 release.
RELEASE_BRANCH = "release/1.0.0"
STALE_RELEASE_BRANCH = "release/0.9.0"
SUPPORTED_PYTHON_VERSIONS = ("3.10", "3.11", "3.12", "3.13", "3.14")
CI_VALIDATED_PYTHON_RANGE = "3.10 through 3.14"
# Prerelease during this work, so it is deliberately excluded from the matrix.
UNSUPPORTED_PRERELEASE_PYTHON = "3.15"
BUILD_JOB_PYTHON = "3.14"
DECLARED_PYTHON_REQUIREMENT = ">=3.10"

PYTHON_BLOCK_PATTERN = re.compile(
    r"^```python\n(.*?)^```",
    re.MULTILINE | re.DOTALL,
)

USER_AGENT_PATTERN = re.compile(r"python-mlb-statsapi/[0-9][^\s`\"']*")


def _load_validator() -> types.ModuleType:
    """Import scripts/validate_release.py, which is not an installable package."""
    spec = importlib.util.spec_from_file_location(
        "validate_release_under_test",
        VALIDATE_RELEASE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = _load_validator()

# Synthetic version used only as an expected-version fixture. The validator
# itself must keep reading the real expected version from pyproject.toml.
SYNTHETIC_VERSION = "1.0.0"


def _project_version() -> str:
    text = PYPROJECT.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, flags=re.MULTILINE)
    assert match is not None, "no version found in pyproject.toml"
    return match.group(1)


# ---------------------------------------------------------------------------
# Documentation consistency
# ---------------------------------------------------------------------------


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


def _release_notes_paths() -> list[Path]:
    return sorted(RELEASE_NOTES_DIR.glob("*.md"))


def _current_document_paths() -> list[Path]:
    """Documents that must describe the current release, not history."""
    return [README, TRANSPORT_DOC, PUBLIC_API_DOC, CURRENT_RELEASE_NOTES]


def _documented_paths() -> list[Path]:
    """Every Markdown document whose Python examples must stay valid."""
    return [README, TRANSPORT_DOC, PUBLIC_API_DOC, *_release_notes_paths()]


def _documented_user_agents(path: Path) -> set[str]:
    return set(USER_AGENT_PATTERN.findall(path.read_text(encoding="utf-8")))


def test_release_notes_directory_is_fully_covered() -> None:
    """Every release-notes file is classified as current or historical."""
    classified = {CURRENT_RELEASE_NOTES, *HISTORICAL_RELEASE_NOTES}
    assert set(_release_notes_paths()) == classified


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
    notes = RELEASE_NOTES_DIR / f"{version}.md"
    assert notes.is_file(), f"missing release notes for version {version}"
    assert notes.read_text(encoding="utf-8").startswith(
        f"# python-mlb-statsapi {version}"
    )


def test_documented_user_agent_matches_the_declared_version() -> None:
    """Current docs must track the version the build will produce."""
    expected = f"python-mlb-statsapi/{_project_version()}"

    for path in (README, TRANSPORT_DOC):
        documented = _documented_user_agents(path)
        assert documented == {expected}, (
            f"{path.name} documents User-Agent versions {sorted(documented)}, "
            f"expected only {expected!r}"
        )

    # The current release notes need not repeat a User-Agent example, but any
    # example they do carry must match the declared version.
    documented = _documented_user_agents(CURRENT_RELEASE_NOTES)
    assert documented <= {expected}, (
        f"{CURRENT_RELEASE_NOTES.name} documents User-Agent versions "
        f"{sorted(documented)}, expected only {expected!r}"
    )


@pytest.mark.parametrize(
    "path",
    HISTORICAL_RELEASE_NOTES,
    ids=lambda path: path.name,
)
def test_historical_release_notes_keep_their_own_user_agent(path: Path) -> None:
    """Historical notes document the version they shipped, not the current one."""
    documented = _documented_user_agents(path)
    assert documented <= {f"python-mlb-statsapi/{path.stem}"}, (
        f"{path.name} documents User-Agent versions {sorted(documented)}"
    )


def test_public_api_contract_document_exists() -> None:
    assert PUBLIC_API_DOC.is_file()
    text = PUBLIC_API_DOC.read_text(encoding="utf-8")
    assert text.startswith("# Public API Contract (1.x)")
    assert "Stability policy" in text
    assert "Session ownership" in text
    assert "Python support" in text


@pytest.mark.parametrize(
    "path",
    (README, PUBLIC_API_DOC, CURRENT_RELEASE_NOTES),
    ids=lambda path: path.name,
)
def test_current_documents_state_the_validated_python_versions(path: Path) -> None:
    """Support wording must match the CI matrix this branch establishes."""
    text = path.read_text(encoding="utf-8")

    assert DECLARED_PYTHON_REQUIREMENT in text, (
        f"{path.name} does not state the declared Python requirement"
    )
    assert CI_VALIDATED_PYTHON_RANGE in text, (
        f"{path.name} does not state the CI-validated Python range"
    )
    for version in SUPPORTED_PYTHON_VERSIONS:
        assert version in text, f"{path.name} does not mention Python {version}"
    assert UNSUPPORTED_PRERELEASE_PYTHON not in text, (
        f"{path.name} must not mention Python {UNSUPPORTED_PRERELEASE_PYTHON}, "
        "which is a prerelease and is not a supported version"
    )


# ---------------------------------------------------------------------------
# Synthetic artifacts
# ---------------------------------------------------------------------------


def _metadata_text(
    *,
    name: str = "python-mlb-statsapi",
    version: str = SYNTHETIC_VERSION,
    requires_python: str = DECLARED_PYTHON_REQUIREMENT,
) -> str:
    return (
        "Metadata-Version: 2.1\n"
        f"Name: {name}\n"
        f"Version: {version}\n"
        f"Requires-Python: {requires_python}\n"
        "\n"
        "Synthetic metadata for release-validator tests.\n"
    )


def _write_wheel(
    dist_dir: Path,
    *,
    version: str = SYNTHETIC_VERSION,
    tag: str = "py3-none-any",
    metadata_name: str = "python-mlb-statsapi",
    metadata_version: str | None = None,
    requires_python: str = DECLARED_PYTHON_REQUIREMENT,
    metadata_files: int = 1,
) -> Path:
    """Write a synthetic wheel ZIP with controllable ``.dist-info`` metadata."""
    dist_dir.mkdir(parents=True, exist_ok=True)
    wheel = dist_dir / f"python_mlb_statsapi-{version}-{tag}.whl"
    raw_metadata = _metadata_text(
        name=metadata_name,
        version=metadata_version or version,
        requires_python=requires_python,
    )
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr("mlbstatsapi/__init__.py", "")
        for index in range(metadata_files):
            suffix = "" if index == 0 else f".extra{index}"
            dist_info = f"python_mlb_statsapi-{version}{suffix}.dist-info"
            archive.writestr(f"{dist_info}/METADATA", raw_metadata)
            archive.writestr(f"{dist_info}/WHEEL", "Wheel-Version: 1.0\n")
    return wheel


def _write_sdist(
    dist_dir: Path,
    *,
    version: str = SYNTHETIC_VERSION,
    paths: tuple[str, ...] | None = None,
) -> Path:
    """Write a synthetic source-distribution tarball with a versioned root."""
    dist_dir.mkdir(parents=True, exist_ok=True)
    sdist = dist_dir / f"python_mlb_statsapi-{version}.tar.gz"
    root = f"python_mlb_statsapi-{version}"
    contents = validator.REQUIRED_SDIST_PATHS if paths is None else paths
    with tarfile.open(sdist, "w:gz") as archive:
        for relative in contents:
            payload = b"synthetic\n"
            info = tarfile.TarInfo(f"{root}/{relative}")
            info.size = len(payload)
            archive.addfile(info, io.BytesIO(payload))
    return sdist


def _classify_command(command) -> str:
    parts = [str(part) for part in command]
    joined = " ".join(parts)
    if "release_smoke_test.py" in joined:
        return "smoke"
    if "--upgrade" in parts:
        return "pip-upgrade"
    if "install" in parts:
        return "install"
    return "other"


class _CompletedProcess:
    def __init__(self, returncode: int):
        self.returncode = returncode


def _stub_clean_install(monkeypatch, *, failing: str | None = None) -> list[list[str]]:
    """Stub environment creation and subprocess execution for install tests.

    ``failing`` selects the step that returns a non-zero exit code: ``install``
    for the artifact installation or ``smoke`` for the installed-package smoke
    test. Only the validator's own ``subprocess`` reference is replaced, so no
    real interpreter, environment, or download is involved.
    """
    commands: list[list[str]] = []

    monkeypatch.setattr(
        validator,
        "_create_clean_environment",
        lambda venv_dir: Path(sys.executable),
    )

    def fake_run(command, cwd=None, check=False, **kwargs):
        commands.append([str(part) for part in command])
        returncode = 1 if _classify_command(command) == failing else 0
        return _CompletedProcess(returncode)

    monkeypatch.setattr(validator, "subprocess", types.SimpleNamespace(run=fake_run))
    return commands


# ---------------------------------------------------------------------------
# Expected-version handling
# ---------------------------------------------------------------------------


def test_expected_version_is_read_from_pyproject(tmp_path: Path) -> None:
    """The validator stays version-aware instead of pinning one release."""
    (tmp_path / "pyproject.toml").write_text(
        '[tool.poetry]\nname = "python-mlb-statsapi"\nversion = "2.3.4"\n',
        encoding="utf-8",
    )

    assert validator._read_expected_version(tmp_path) == "2.3.4"


def test_declared_project_version_is_the_default_expected_version() -> None:
    assert validator._read_expected_version(PROJECT_ROOT) == _project_version()


def test_missing_project_version_is_reported(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[tool.poetry]\nname = "python-mlb-statsapi"\n',
        encoding="utf-8",
    )

    with pytest.raises(validator.ValidationError, match="could not find a version"):
        validator._read_expected_version(tmp_path)


def test_missing_dist_directory_is_reported(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "dist"

    exit_code = validator.main(
        ["--dist", str(missing), "--expected-version", SYNTHETIC_VERSION]
    )

    assert exit_code == 1
    message = capsys.readouterr().err
    assert str(missing) in message
    assert "does not exist" in message
    assert "poetry build" in message


# ---------------------------------------------------------------------------
# Artifact discovery failures
# ---------------------------------------------------------------------------


def test_missing_wheel_is_reported(tmp_path: Path) -> None:
    _write_sdist(tmp_path)

    with pytest.raises(validator.ValidationError) as exc_info:
        validator.validate(tmp_path, SYNTHETIC_VERSION)

    message = str(exc_info.value)
    assert validator.WHEEL_LABEL in message
    assert f"python_mlb_statsapi-{SYNTHETIC_VERSION}-*.whl" in message
    assert "poetry build" in message


def test_missing_source_distribution_is_reported(tmp_path: Path) -> None:
    wheel = _write_wheel(tmp_path)

    with pytest.raises(validator.ValidationError) as exc_info:
        validator.validate(tmp_path, SYNTHETIC_VERSION)

    message = str(exc_info.value)
    assert validator.SDIST_LABEL in message
    assert f"python_mlb_statsapi-{SYNTHETIC_VERSION}.tar.gz" in message
    # The wheel is present, so the actual directory contents are reported.
    assert wheel.name in message


def test_multiple_stale_wheels_are_reported(tmp_path: Path) -> None:
    first = _write_wheel(tmp_path, tag="py3-none-any")
    second = _write_wheel(tmp_path, tag="py310-none-any")
    _write_sdist(tmp_path)

    with pytest.raises(validator.ValidationError) as exc_info:
        validator.validate(tmp_path, SYNTHETIC_VERSION)

    message = str(exc_info.value)
    assert validator.WHEEL_LABEL in message
    assert first.name in message
    assert second.name in message
    assert "Remove stale artifacts" in message


def test_multiple_stale_source_distributions_are_reported(tmp_path: Path) -> None:
    """Two sdists matching one lookup pattern must be rejected, not guessed.

    ``validate()`` looks the sdist up by its exact versioned filename, so this
    exercises the shared discovery helper directly with a wildcard pattern.
    """
    first = _write_sdist(tmp_path, version=SYNTHETIC_VERSION)
    second = _write_sdist(tmp_path, version=f"{SYNTHETIC_VERSION}rc1")

    with pytest.raises(validator.ValidationError) as exc_info:
        validator._find_single(
            tmp_path,
            "python_mlb_statsapi-*.tar.gz",
            validator.SDIST_LABEL,
        )

    message = str(exc_info.value)
    assert validator.SDIST_LABEL in message
    assert first.name in message
    assert second.name in message
    assert "Remove stale artifacts" in message


# ---------------------------------------------------------------------------
# Wheel metadata failures
# ---------------------------------------------------------------------------


def test_wheel_metadata_is_accepted_when_correct(tmp_path: Path) -> None:
    wheel = _write_wheel(tmp_path)

    validator._check_wheel_metadata(wheel, SYNTHETIC_VERSION)


def test_incorrect_wheel_name_metadata_is_reported(tmp_path: Path) -> None:
    wheel = _write_wheel(tmp_path, metadata_name="mlb-statsapi")

    with pytest.raises(validator.ValidationError) as exc_info:
        validator._check_wheel_metadata(wheel, SYNTHETIC_VERSION)

    message = str(exc_info.value)
    assert validator.WHEEL_LABEL in message
    assert wheel.name in message
    assert "Name" in message
    assert "'mlb-statsapi'" in message
    assert "'python-mlb-statsapi'" in message


def test_incorrect_wheel_version_metadata_is_reported(tmp_path: Path) -> None:
    wheel = _write_wheel(tmp_path, metadata_version="0.9.0")

    with pytest.raises(validator.ValidationError) as exc_info:
        validator._check_wheel_metadata(wheel, SYNTHETIC_VERSION)

    message = str(exc_info.value)
    assert validator.WHEEL_LABEL in message
    assert wheel.name in message
    assert "Version" in message
    assert "'0.9.0'" in message
    assert f"'{SYNTHETIC_VERSION}'" in message


def test_incorrect_requires_python_metadata_is_reported(tmp_path: Path) -> None:
    wheel = _write_wheel(tmp_path, requires_python=">=3.8")

    with pytest.raises(validator.ValidationError) as exc_info:
        validator._check_wheel_metadata(wheel, SYNTHETIC_VERSION)

    message = str(exc_info.value)
    assert validator.WHEEL_LABEL in message
    assert wheel.name in message
    assert "Requires-Python" in message
    assert "'>=3.8'" in message
    assert f"'{DECLARED_PYTHON_REQUIREMENT}'" in message


def test_ambiguous_wheel_metadata_is_reported(tmp_path: Path) -> None:
    wheel = _write_wheel(tmp_path, metadata_files=2)

    with pytest.raises(validator.ValidationError) as exc_info:
        validator._check_wheel_metadata(wheel, SYNTHETIC_VERSION)

    message = str(exc_info.value)
    assert validator.WHEEL_LABEL in message
    assert wheel.name in message
    assert "METADATA" in message


def test_expected_requires_python_matches_pyproject() -> None:
    assert validator.EXPECTED_REQUIRES_PYTHON == DECLARED_PYTHON_REQUIREMENT
    assert (
        f'python = "{DECLARED_PYTHON_REQUIREMENT}"'
        in PYPROJECT.read_text(encoding="utf-8")
    )


# ---------------------------------------------------------------------------
# Source-distribution content failures
# ---------------------------------------------------------------------------


def test_source_distribution_contents_are_accepted_when_complete(
    tmp_path: Path,
) -> None:
    sdist = _write_sdist(tmp_path)

    validator._check_sdist_contents(sdist)


@pytest.mark.parametrize("omitted", validator.REQUIRED_SDIST_PATHS)
def test_missing_required_source_distribution_path_is_reported(
    tmp_path: Path,
    omitted: str,
) -> None:
    remaining = tuple(
        path for path in validator.REQUIRED_SDIST_PATHS if path != omitted
    )
    sdist = _write_sdist(tmp_path, paths=remaining)

    with pytest.raises(validator.ValidationError) as exc_info:
        validator._check_sdist_contents(sdist)

    message = str(exc_info.value)
    assert validator.SDIST_LABEL in message
    assert sdist.name in message
    assert omitted in message


def test_required_source_distribution_paths_cover_the_package_entry_points() -> None:
    """The required list must include the files needed to rebuild and import."""
    required = set(validator.REQUIRED_SDIST_PATHS)

    assert {"README.md", "pyproject.toml", "mlbstatsapi/__init__.py"} <= required
    assert "mlbstatsapi/mlb_api.py" in required
    assert "mlbstatsapi/mlb_dataadapter.py" in required
    # Tests, docs, and scripts are intentionally absent from the sdist.
    assert not any(path.startswith(("tests/", "docs/", "scripts/")) for path in required)


# ---------------------------------------------------------------------------
# Clean-install and smoke-test failures
# ---------------------------------------------------------------------------


def test_wheel_installation_failure_identifies_the_artifact(
    monkeypatch,
    tmp_path: Path,
) -> None:
    wheel = _write_wheel(tmp_path)
    _stub_clean_install(monkeypatch, failing="install")

    with pytest.raises(validator.ValidationError) as exc_info:
        validator._check_clean_install(
            wheel,
            SYNTHETIC_VERSION,
            label=validator.WHEEL_LABEL,
        )

    message = str(exc_info.value)
    assert f"{validator.WHEEL_LABEL} installation" in message
    assert wheel.name in message
    assert "exit code 1" in message


def test_source_distribution_installation_failure_identifies_the_artifact(
    monkeypatch,
    tmp_path: Path,
) -> None:
    sdist = _write_sdist(tmp_path)
    _stub_clean_install(monkeypatch, failing="install")

    with pytest.raises(validator.ValidationError) as exc_info:
        validator._check_clean_install(
            sdist,
            SYNTHETIC_VERSION,
            label=validator.SDIST_LABEL,
        )

    message = str(exc_info.value)
    assert f"{validator.SDIST_LABEL} installation" in message
    assert sdist.name in message
    assert "exit code 1" in message


@pytest.mark.parametrize(
    "label",
    (validator.WHEEL_LABEL, validator.SDIST_LABEL),
)
def test_smoke_test_failure_identifies_the_artifact(
    monkeypatch,
    tmp_path: Path,
    label: str,
) -> None:
    artifact = (
        _write_wheel(tmp_path)
        if label == validator.WHEEL_LABEL
        else _write_sdist(tmp_path)
    )
    _stub_clean_install(monkeypatch, failing="smoke")

    with pytest.raises(validator.ValidationError) as exc_info:
        validator._check_clean_install(artifact, SYNTHETIC_VERSION, label=label)

    message = str(exc_info.value)
    assert f"{label} smoke test" in message
    assert "exit code 1" in message


def test_clean_install_runs_the_artifact_and_smoke_test_from_a_temp_workspace(
    monkeypatch,
    tmp_path: Path,
) -> None:
    wheel = _write_wheel(tmp_path)
    commands = _stub_clean_install(monkeypatch)

    validator._check_clean_install(
        wheel,
        SYNTHETIC_VERSION,
        label=validator.WHEEL_LABEL,
    )

    steps = [_classify_command(command) for command in commands]
    assert steps == ["pip-upgrade", "install", "smoke"]

    install_command = commands[steps.index("install")]
    assert str(wheel.resolve()) in install_command

    smoke_command = commands[steps.index("smoke")]
    assert smoke_command[-1] == SYNTHETIC_VERSION
    smoke_script = Path(smoke_command[-2])
    # The script is written into a throwaway workspace, never the checkout.
    assert smoke_script.name == "release_smoke_test.py"
    assert PROJECT_ROOT not in smoke_script.parents


def test_each_artifact_is_installed_into_its_own_environment(
    monkeypatch,
    tmp_path: Path,
) -> None:
    wheel = _write_wheel(tmp_path)
    sdist = _write_sdist(tmp_path)
    created: list[Path] = []

    def record_environment(venv_dir: Path) -> Path:
        created.append(venv_dir)
        return Path(sys.executable)

    monkeypatch.setattr(validator, "_create_clean_environment", record_environment)
    monkeypatch.setattr(
        validator,
        "subprocess",
        types.SimpleNamespace(run=lambda *args, **kwargs: _CompletedProcess(0)),
    )

    validator._check_clean_install(
        wheel,
        SYNTHETIC_VERSION,
        label=validator.WHEEL_LABEL,
    )
    validator._check_clean_install(
        sdist,
        SYNTHETIC_VERSION,
        label=validator.SDIST_LABEL,
    )

    assert len(created) == 2
    assert created[0] != created[1]


def test_validate_clean_installs_both_artifacts(monkeypatch, tmp_path: Path) -> None:
    """validate() must clean-install the wheel and the source distribution."""
    wheel = _write_wheel(tmp_path)
    sdist = _write_sdist(tmp_path)
    installs: list[tuple[Path, str, str]] = []

    def record_install(artifact: Path, expected_version: str, *, label: str) -> None:
        installs.append((artifact, expected_version, label))

    monkeypatch.setattr(validator, "_check_clean_install", record_install)

    validator.validate(tmp_path, SYNTHETIC_VERSION)

    assert installs == [
        (wheel, SYNTHETIC_VERSION, validator.WHEEL_LABEL),
        (sdist, SYNTHETIC_VERSION, validator.SDIST_LABEL),
    ]


def test_validate_reports_success_for_both_artifacts(
    monkeypatch,
    tmp_path: Path,
    capsys,
) -> None:
    _write_wheel(tmp_path)
    _write_sdist(tmp_path)
    _stub_clean_install(monkeypatch)

    validator.validate(tmp_path, SYNTHETIC_VERSION)

    output = capsys.readouterr().out
    assert f"installing {validator.WHEEL_LABEL}" in output
    assert f"running {validator.WHEEL_LABEL} smoke test" in output
    assert f"installing {validator.SDIST_LABEL}" in output
    assert f"running {validator.SDIST_LABEL} smoke test" in output
    assert "Release validation passed" in output


def test_missing_interpreter_in_environment_is_reported(tmp_path: Path) -> None:
    with pytest.raises(validator.ValidationError, match="no interpreter found"):
        validator._venv_python(tmp_path / "venv")


# ---------------------------------------------------------------------------
# Installed smoke-test contract
# ---------------------------------------------------------------------------


def test_smoke_test_source_is_valid_python() -> None:
    compile(validator.SMOKE_TEST_SOURCE, "release_smoke_test.py", "exec")


def test_smoke_test_labels_reverted_strict_defaults() -> None:
    """A reverted strict default must fail with an explanatory message.

    An unlabelled AssertionError would not tell a release engineer which
    constructor regressed, so both messages are asserted here and in the
    generated smoke test.
    """
    assert validator.MLB_STRICT_DEFAULT_MESSAGE == (
        "Mlb.strict_http must default to True for the 1.0 contract"
    )
    assert validator.ADAPTER_STRICT_DEFAULT_MESSAGE == (
        "MlbDataAdapter.strict_http must default to True for the 1.0 contract"
    )

    source = validator.SMOKE_TEST_SOURCE
    assert (
        'assert mlb_init["strict_http"].default is True, MLB_STRICT_DEFAULT_MESSAGE'
        in source
    )
    assert (
        'assert adapter_init["strict_http"].default is True, '
        "ADAPTER_STRICT_DEFAULT_MESSAGE" in source
    )
    for message in (
        validator.MLB_STRICT_DEFAULT_MESSAGE,
        validator.ADAPTER_STRICT_DEFAULT_MESSAGE,
    ):
        assert message in source


def test_smoke_test_asserts_strict_http_default() -> None:
    """The installed-artifact smoke test must match the 1.0 strict default."""
    text = VALIDATE_RELEASE.read_text(encoding="utf-8")
    assert 'mlb_init["strict_http"].default is True' in text
    assert 'adapter_init["strict_http"].default is True' in text
    assert "Compatibility mode is the default in this release." not in text


def test_smoke_test_checks_strict_behavior_not_only_signatures() -> None:
    """Signature defaults alone cannot prove a final 403 raises."""
    source = validator.SMOKE_TEST_SOURCE

    assert "status_code = 403" in source
    assert 'reason = "Forbidden"' in source
    assert "https://statsapi.mlb.com/api/v1/sports" in source
    assert "https://statsapi.mlb.com/api/v1.1/sports" in source
    assert "get_sports" in source
    assert "Mlb(session=session, strict_http=True)" in source
    assert "Mlb(session=session, strict_http=False)" in source
    assert "strict_http=True," in source
    assert "strict_http=False," in source
    assert "MlbHttpCompatibilityWarning" in source
    assert "strict_http=False" in source


def test_smoke_test_checks_injected_session_ownership_and_configuration() -> None:
    source = validator.SMOKE_TEST_SOURCE

    assert "class OwnershipSession(requests.Session):" in source
    assert "release-smoke-test/1.0" in source
    assert "X-Release-Test" in source
    assert "injected_https_adapter" in source
    assert "injected_http_adapter" in source
    assert "is injected_https_adapter" in source
    assert "is injected_http_adapter" in source
    assert "must not close a caller-injected Session" in source
    assert "must not mount its retry policy on an injected" in source
    assert "finally:\n    session.close()" in source


def test_smoke_test_checks_library_created_session_configuration() -> None:
    source = validator.SMOKE_TEST_SOURCE

    assert 'f"python-mlb-statsapi/{expected_version}"' in source
    assert "assert_documented_retry_policy" in source
    assert "create_retry_policy() must return a new Retry instance per call" in source


@pytest.mark.parametrize(
    "symbol",
    (
        "Mlb",
        "MlbDataAdapter",
        "MlbResult",
        "create_retry_policy",
        "TheMlbStatsApiException",
        "MlbTransportError",
        "MlbTimeoutError",
        "MlbHttpError",
        "MlbDecodeError",
        "MlbHttpCompatibilityWarning",
        "return_splits",
        "get_stat_attributes",
    ),
)
def test_smoke_test_imports_the_supported_public_symbol(symbol: str) -> None:
    assert f"    {symbol},\n" in validator.SMOKE_TEST_SOURCE


def test_smoke_test_does_not_promote_accidental_submodules() -> None:
    """Accidentally exposed submodules stay outside the supported surface."""
    source = validator.SMOKE_TEST_SOURCE

    for submodule in ("mlb_api", "mlb_module", "models"):
        assert f"from mlbstatsapi import {submodule}" not in source
        assert f"import mlbstatsapi.{submodule}" not in source


def test_smoke_test_runs_against_the_installed_distribution() -> None:
    source = validator.SMOKE_TEST_SOURCE

    assert "sys.prefix != sys.base_prefix" in source
    assert 'sysconfig.get_paths()["purelib"]' in source
    assert "is_relative_to(site_packages)" in source


def test_smoke_test_makes_no_live_mlb_request() -> None:
    source = validator.SMOKE_TEST_SOURCE

    assert "requests.get(" not in source
    assert "session.request(" not in source
    assert "class ForbiddenSession:" in source
    assert "never reaches the MLB API" in source


def test_validator_is_not_pinned_to_a_single_release_version() -> None:
    """1.0.0 may appear as a usage example, never as the only accepted version."""
    source = VALIDATE_RELEASE.read_text(encoding="utf-8")

    assert 'EXPECTED_VERSION = "1.0.0"' not in source
    assert "_read_expected_version" in source
    assert "--expected-version" in source
    # Terminology now covers both artifacts, not just the wheel.
    assert "installed distribution artifact" in source
    assert "clean wheel installation" not in source
    assert "installed wheel" not in source


# ---------------------------------------------------------------------------
# Deterministic CI contract
# ---------------------------------------------------------------------------


def _matrix_python_versions() -> list[str]:
    text = OFFLINE_WORKFLOW.read_text(encoding="utf-8")
    match = re.search(
        r"^\s+python-version:\n((?:\s+- \"[^\"]+\"\n)+)",
        text,
        flags=re.MULTILINE,
    )
    assert match is not None, "no python-version matrix found in the offline workflow"
    return re.findall(r'- "([^"]+)"', match.group(1))


def test_ci_watches_the_current_release_branch() -> None:
    """Pull requests and pushes must watch main and release/1.0.0.

    The trigger is asserted literally instead of being derived from the package
    version, which is still 0.9.0 until the release bump lands.
    """
    text = OFFLINE_WORKFLOW.read_text(encoding="utf-8")

    assert text.count(f"- {RELEASE_BRANCH}") == 2, text
    assert text.count("- main") == 2, text
    assert STALE_RELEASE_BRANCH not in text, (
        f"the stale {STALE_RELEASE_BRANCH} trigger must be removed"
    )
    assert "workflow_dispatch:" in text


def test_ci_matrix_covers_every_supported_python_version() -> None:
    assert _matrix_python_versions() == list(SUPPORTED_PYTHON_VERSIONS)


def test_ci_matrix_excludes_prerelease_python() -> None:
    """No job may set up a prerelease interpreter, matrix or otherwise."""
    text = OFFLINE_WORKFLOW.read_text(encoding="utf-8")

    assert UNSUPPORTED_PRERELEASE_PYTHON not in _matrix_python_versions()
    assert f'- "{UNSUPPORTED_PRERELEASE_PYTHON}"' not in text
    assert f'python-version: "{UNSUPPORTED_PRERELEASE_PYTHON}"' not in text


def test_ci_minimum_python_matches_the_declared_requirement() -> None:
    versions = _matrix_python_versions()

    assert versions[0] == "3.10"
    assert (
        f'python = "{DECLARED_PYTHON_REQUIREMENT}"'
        in PYPROJECT.read_text(encoding="utf-8")
    )


def test_ci_build_job_validates_and_twine_checks_the_artifacts() -> None:
    text = OFFLINE_WORKFLOW.read_text(encoding="utf-8")

    assert "rm -rf dist" in text
    assert "poetry build" in text
    assert "python scripts/validate_release.py" in text
    assert "poetry run twine check dist/*" in text
    assert f'python-version: "{BUILD_JOB_PYTHON}"' in text


def test_ci_runs_offline_tests_without_the_live_suite() -> None:
    text = OFFLINE_WORKFLOW.read_text(encoding="utf-8")

    assert "--ignore=tests/external_tests" in text
    assert "tests/external_tests/" not in text


def test_live_tests_stay_in_a_separate_workflow() -> None:
    text = EXTERNAL_WORKFLOW.read_text(encoding="utf-8")

    assert "tests/external_tests/" in text
    assert "workflow_dispatch:" in text
    assert "schedule:" in text
    # Live tests must not be attached to ordinary pushes or pull requests.
    assert "pull_request:" not in text
    assert "push:" not in text


@pytest.mark.parametrize(
    "forbidden",
    (
        "poetry publish",
        "twine upload",
        "PYPI_TOKEN",
        "PYPI_API_TOKEN",
        "POETRY_PYPI_TOKEN",
        "TEST_PYPI",
        "TESTPYPI",
        "pypa/gh-action-pypi-publish",
        "softprops/action-gh-release",
        "gh release create",
        "git tag",
    ),
)
def test_no_workflow_publishes_or_tags(forbidden: str) -> None:
    for workflow in (OFFLINE_WORKFLOW, EXTERNAL_WORKFLOW):
        text = workflow.read_text(encoding="utf-8")
        assert forbidden not in text, f"{workflow.name} contains {forbidden!r}"


def test_twine_is_a_development_dependency_only() -> None:
    text = PYPROJECT.read_text(encoding="utf-8")
    sections = dict(
        re.findall(r"^\[([^\]]+)\]\n((?:(?!\[)[^\n]*\n)*)", text, flags=re.MULTILINE)
    )

    runtime = sections["tool.poetry.dependencies"]
    development = sections["tool.poetry.group.dev.dependencies"]

    assert "twine" not in runtime, "twine must not become a runtime dependency"
    assert re.search(r"^twine = ", development, flags=re.MULTILINE), development


def test_twine_is_locked() -> None:
    assert 'name = "twine"' in POETRY_LOCK.read_text(encoding="utf-8")
