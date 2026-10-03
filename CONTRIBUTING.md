# Contributing to python-mlb-statsapi
We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with Github
We use github to host code, to track issues and feature requests, as well as accept pull requests.

## All Code Changes Happen Through Pull Requests
Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `development`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Issue that pull request!

## Development

Install dependencies:

```bash
poetry install -E async
```

Offline tests are deterministic and should run before every pull request:

```bash
poetry run pytest \
  tests/ \
  --ignore=tests/external_tests
```

External tests contact the live MLB API. They require internet access and are separate from normal offline CI:

```bash
poetry run pytest \
  tests/external_tests/
```

These live tests may fail because the MLB service is unavailable or because MLB changes undocumented payloads.

Full local validation:

```bash
poetry run pytest tests/
rm -rf dist
poetry build
python3 scripts/validate_release.py
poetry run twine check dist/*
```

`scripts/validate_release.py` is the same release check offline CI runs. It inspects the built wheel and source distribution, clean-installs each artifact into its own temporary virtual environment, and runs the same public-API smoke test against both installed artifacts. Every response it observes comes from injected fake HTTP clients, so it never contacts the MLB API.

Offline CI is the normal pull-request gate. External tests are available manually, on a weekly schedule, and before releases.

## Preparing a release

Release preparation starts with one command:

```bash
python scripts/prepare_release.py <version>
```

The version must be a plain `MAJOR.MINOR.PATCH` newer than the version in `pyproject.toml`. The script makes the version-specific edits every release needs:

- bumps the version in `pyproject.toml`
- creates a release-notes skeleton at `docs/releases/<version>.md`
- lists the release first in `docs/releases.md` and in the Release Notes section of `mkdocs.yml`
- updates the current User-Agent version in `README.md`
- updates the current version, release-notes link, and User-Agent in `docs/http-transport.md`
- points `CURRENT_RELEASE_NOTES` in `tests/test_release_validation.py` at the new notes and moves the previous release into `HISTORICAL_RELEASE_NOTES`

Preview the same checks and the exact diff without changing any file:

```bash
python scripts/prepare_release.py <version> --dry-run
```

`--check` is an alias for `--dry-run`. Both exit with status 0 when preparation would succeed and 1 when it would be refused.

The script refuses, without changing anything, when the version is invalid, not newer than the current version, already prepared, or partially prepared, or when any file no longer has the exact structure it expects. Every edit is computed before anything is written, so a refusal never leaves the repository half-updated. When it reports a partially prepared release, restore the listed files and run it again.

After the script runs:

1. Write the release notes. Replace every `TODO(release)` marker in `docs/releases/<version>.md` and the summary line in `docs/releases.md`, and confirm the `Python support` section carried over from the previous release is still accurate. Offline tests fail while any `TODO(release)` marker remains.
2. Review the complete diff.
3. Run the full validation:

   ```bash
   poetry run pytest tests/ --ignore=tests/external_tests
   poetry run pytest tests/external_tests/
   rm -rf dist
   poetry build
   python3 scripts/validate_release.py
   poetry run twine check dist/*
   ```

4. Commit and open the release pull request.

`prepare_release.py` only edits files in the working tree. It does not commit, push, tag, publish to PyPI, or create a GitHub Release; those steps remain manual.

## Pull Request Guidelines

- Run offline tests before submitting a PR
- Use the [PR template](.github/pull_request_template.md) when creating your pull request
- Follow the branch naming convention:
  - `feat/` - New features
  - `fix/` - Bug fixes
  - `docs/` - Documentation updates
  - `refactor/` - Code improvements

## Any contributions you make will be under the MIT Software License
In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issues](https://github.com/zero-sum-seattle/python-mlb-statsapi/issues)
We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/zero-sum-seattle/python-mlb-statsapi/issues/new).

## Write bug reports with detail, background, and sample code
**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Use a Consistent Coding Style
* Adhere to this project's coding style

## License
By contributing, you agree that your contributions will be licensed under its MIT License.
