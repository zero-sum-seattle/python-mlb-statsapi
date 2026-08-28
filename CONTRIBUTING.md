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
