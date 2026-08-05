"""Validate the built python-mlb-statsapi distributions before a release.

Checks the artifacts in ``dist/``, then installs the wheel into a throwaway
virtual environment and runs a public-import smoke test against the *installed*
package.

The smoke test deliberately runs from a temporary directory so the repository
checkout cannot shadow the installed distribution.

Nothing here contacts the MLB API.

Usage::

    python scripts/validate_release.py
    python scripts/validate_release.py --dist dist --expected-version 0.9.0
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tarfile
import tempfile
import venv
import zipfile
from email.parser import Parser
from pathlib import Path

DISTRIBUTION_NAME = "python-mlb-statsapi"
NORMALIZED_DISTRIBUTION_NAME = "python_mlb_statsapi"
EXPECTED_REQUIRES_PYTHON = ">=3.10"

# Paths every source distribution must carry so the project can be rebuilt and
# read from the sdist alone.
REQUIRED_SDIST_PATHS = (
    "README.md",
    "pyproject.toml",
    "mlbstatsapi/__init__.py",
)

SMOKE_TEST_SOURCE = '''
"""Public import smoke test for an installed python-mlb-statsapi wheel."""

import importlib.metadata
import inspect
import sys
from pathlib import Path

import requests
from urllib3.util.retry import Retry

import mlbstatsapi
from mlbstatsapi import (
    Mlb,
    MlbDataAdapter,
    MlbDecodeError,
    MlbHttpCompatibilityWarning,
    MlbHttpError,
    MlbTimeoutError,
    MlbTransportError,
    TheMlbStatsApiException,
    create_retry_policy,
)

expected_version = sys.argv[1]

package_file = Path(mlbstatsapi.__file__).resolve()
assert "site-packages" in package_file.parts, (
    f"mlbstatsapi was imported from {package_file}, not from the installed wheel"
)

installed_version = importlib.metadata.version("python-mlb-statsapi")
assert installed_version == expected_version, (
    f"installed metadata reports {installed_version}, expected {expected_version}"
)

assert callable(create_retry_policy)
retry_policy = create_retry_policy()
assert isinstance(retry_policy, Retry), type(retry_policy)
assert create_retry_policy() is not retry_policy, (
    "create_retry_policy() must return a new Retry instance per call"
)

assert issubclass(MlbHttpCompatibilityWarning, FutureWarning)
assert issubclass(MlbHttpError, TheMlbStatsApiException)
assert issubclass(MlbTimeoutError, MlbTransportError)
assert issubclass(MlbTransportError, TheMlbStatsApiException)
assert issubclass(MlbDecodeError, TheMlbStatsApiException)

# Compatibility mode is the default in this release.
assert (
    inspect.signature(Mlb.__init__).parameters["strict_http"].default is False
)
assert (
    inspect.signature(MlbDataAdapter.__init__).parameters["strict_http"].default
    is False
)

# A library-created Session is library-owned, so reading its User-Agent through
# the private attribute is acceptable for internal release validation only.
expected_user_agent = f"python-mlb-statsapi/{expected_version}"
with Mlb() as mlb:
    user_agent = mlb._session.headers["User-Agent"]
    assert user_agent == expected_user_agent, user_agent

# Strict mode is constructible and injected Session headers stay untouched.
session = requests.Session()
session.headers.update(
    {
        "User-Agent": "release-smoke-test/1.0",
        "X-Release-Test": "preserved",
    }
)
try:
    with Mlb(session=session, strict_http=True):
        pass
    assert session.headers["User-Agent"] == "release-smoke-test/1.0"
    assert session.headers["X-Release-Test"] == "preserved"
finally:
    session.close()

print(f"smoke test passed for python-mlb-statsapi {installed_version}")
'''


class ValidationError(Exception):
    """A release validation check failed."""


def _log(message: str) -> None:
    print(message, flush=True)


def _read_expected_version(project_root: Path) -> str:
    """Read the declared project version from pyproject.toml.

    Uses tomllib when available and falls back to a narrow regex so the
    validator also runs on Python 3.10, which the package still supports.
    """
    pyproject = project_root / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")

    try:
        import tomllib
    except ModuleNotFoundError:
        match = re.search(
            r'^version\s*=\s*"([^"]+)"',
            text,
            flags=re.MULTILINE,
        )
        if match is None:
            raise ValidationError(f"could not find a version in {pyproject}")
        return match.group(1)

    data = tomllib.loads(text)
    project_version = data.get("project", {}).get("version")
    poetry_version = data.get("tool", {}).get("poetry", {}).get("version")
    version = project_version or poetry_version
    if not version:
        raise ValidationError(f"could not find a version in {pyproject}")
    return version


def _find_single(dist_dir: Path, pattern: str, label: str) -> Path:
    matches = sorted(dist_dir.glob(pattern))
    if not matches:
        raise ValidationError(
            f"no {label} matching {pattern!r} in {dist_dir}; run `poetry build` first"
        )
    if len(matches) > 1:
        names = ", ".join(path.name for path in matches)
        raise ValidationError(
            f"expected exactly one {label} in {dist_dir}, found: {names}. "
            "Remove stale artifacts and rebuild."
        )
    return matches[0]


def _check_wheel_metadata(wheel: Path, expected_version: str) -> None:
    with zipfile.ZipFile(wheel) as archive:
        metadata_names = [
            name
            for name in archive.namelist()
            if name.endswith(".dist-info/METADATA")
        ]
        if len(metadata_names) != 1:
            raise ValidationError(
                f"expected one METADATA file in {wheel.name}, found {metadata_names}"
            )
        raw_metadata = archive.read(metadata_names[0]).decode("utf-8")

    metadata = Parser().parsestr(raw_metadata)

    name = metadata.get("Name")
    if name != DISTRIBUTION_NAME:
        raise ValidationError(f"wheel Name is {name!r}, expected {DISTRIBUTION_NAME!r}")

    version = metadata.get("Version")
    if version != expected_version:
        raise ValidationError(
            f"wheel Version is {version!r}, expected {expected_version!r}"
        )

    requires_python = metadata.get("Requires-Python")
    if requires_python != EXPECTED_REQUIRES_PYTHON:
        raise ValidationError(
            f"wheel Requires-Python is {requires_python!r}, "
            f"expected {EXPECTED_REQUIRES_PYTHON!r}"
        )

    _log(
        f"  wheel metadata: Name={name} Version={version} "
        f"Requires-Python={requires_python}"
    )


def _check_sdist_contents(sdist: Path) -> None:
    with tarfile.open(sdist, "r:gz") as archive:
        members = archive.getnames()

    # Every path inside an sdist is prefixed with the versioned root directory.
    relative_paths = {name.split("/", 1)[1] for name in members if "/" in name}

    missing = [path for path in REQUIRED_SDIST_PATHS if path not in relative_paths]
    if missing:
        raise ValidationError(
            f"source distribution {sdist.name} is missing: {', '.join(missing)}"
        )

    _log(f"  sdist contains: {', '.join(REQUIRED_SDIST_PATHS)}")


def _venv_python(venv_dir: Path) -> Path:
    candidates = (
        venv_dir / "bin" / "python",
        venv_dir / "Scripts" / "python.exe",
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise ValidationError(f"no interpreter found in {venv_dir}")


def _run(command: list[str], *, cwd: Path) -> None:
    result = subprocess.run(command, cwd=cwd, check=False)
    if result.returncode != 0:
        printable = " ".join(command)
        raise ValidationError(f"command failed ({result.returncode}): {printable}")


def _check_clean_install(wheel: Path, expected_version: str) -> None:
    with tempfile.TemporaryDirectory(prefix="python-mlb-statsapi-release-") as tmp:
        workspace = Path(tmp)
        venv_dir = workspace / "venv"

        _log(f"  creating clean virtual environment in {venv_dir}")
        venv.EnvBuilder(with_pip=True, clear=True).create(venv_dir)
        python = _venv_python(venv_dir)

        _run(
            [str(python), "-m", "pip", "install", "--upgrade", "--quiet", "pip"],
            cwd=workspace,
        )
        _log(f"  installing {wheel.name}")
        _run(
            [str(python), "-m", "pip", "install", "--quiet", str(wheel.resolve())],
            cwd=workspace,
        )

        smoke_test = workspace / "release_smoke_test.py"
        smoke_test.write_text(SMOKE_TEST_SOURCE, encoding="utf-8")

        # Run from the temporary directory so the repository checkout is not on
        # sys.path and cannot shadow the installed distribution.
        _log("  running public import smoke test against the installed wheel")
        _run([str(python), str(smoke_test), expected_version], cwd=workspace)


def validate(dist_dir: Path, expected_version: str) -> None:
    _log(f"Validating release {expected_version} in {dist_dir}")

    wheel = _find_single(
        dist_dir,
        f"{NORMALIZED_DISTRIBUTION_NAME}-{expected_version}-*.whl",
        "wheel",
    )
    _log(f"  wheel: {wheel.name}")

    sdist = _find_single(
        dist_dir,
        f"{NORMALIZED_DISTRIBUTION_NAME}-{expected_version}.tar.gz",
        "source distribution",
    )
    _log(f"  source distribution: {sdist.name}")

    _check_wheel_metadata(wheel, expected_version)
    _check_sdist_contents(sdist)
    _check_clean_install(wheel, expected_version)

    _log(f"Release validation passed for {DISTRIBUTION_NAME} {expected_version}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root containing pyproject.toml",
    )
    parser.add_argument(
        "--dist",
        type=Path,
        default=None,
        help="directory holding the built artifacts (default: <project-root>/dist)",
    )
    parser.add_argument(
        "--expected-version",
        default=None,
        help="version to validate (default: the version declared in pyproject.toml)",
    )
    args = parser.parse_args(argv)

    project_root = args.project_root.resolve()
    dist_dir = (args.dist or project_root / "dist").resolve()

    try:
        expected_version = args.expected_version or _read_expected_version(project_root)
        if not dist_dir.is_dir():
            raise ValidationError(
                f"{dist_dir} does not exist; run `poetry build` first"
            )
        validate(dist_dir, expected_version)
    except ValidationError as exc:
        print(f"Release validation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
