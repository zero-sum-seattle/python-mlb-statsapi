# AGENTS.md

## Project overview

`python-mlb-statsapi` is an unofficial Python wrapper for the MLB Stats API.

The package provides synchronous access to MLB data such as:

* People and players
* Teams and rosters
* Schedules
* Games
* Box scores
* Play-by-play data
* Standings
* Venues
* Drafts
* Awards
* Player and team statistics

API responses are converted into Pydantic models with Python-style `snake_case` field names.

This package is not affiliated with Major League Baseball.

## Supported environment

The package supports:

* Python 3.10
* Python 3.11
* Python 3.12
* Poetry
* Pydantic v2
* Requests

Do not introduce a new runtime dependency unless the task clearly requires it and the benefit justifies increasing the package footprint.

## Repository structure

Important paths include:

```text
mlbstatsapi/
    mlb_api.py
    mlb_dataadapter.py
    mlb_module.py
    exceptions.py
    models/

tests/
    external_tests/
    fixtures/
    tools/
```

General responsibilities:

* `mlb_api.py` contains the public `Mlb` client and endpoint methods.
* `mlb_dataadapter.py` handles communication with the MLB Stats API.
* `exceptions.py` contains package exceptions.
* `models/` contains Pydantic models for MLB response data.
* `tests/external_tests/` contains tests that intentionally call the live MLB API.
* Offline tests must remain outside `tests/external_tests/`.

## Development setup

Install dependencies with:

```bash
poetry install
```

Run the complete test suite with:

```bash
poetry run pytest tests/
```

Run only offline tests with:

```bash
poetry run pytest tests/ --ignore=tests/external_tests
```

Run live MLB API tests with:

```bash
poetry run pytest tests/external_tests/
```

Build the package with:

```bash
poetry build
```

Run offline tests before submitting any change.

Run external tests when changing:

* MLB endpoint behavior
* Request parameters
* Response parsing
* Pydantic aliases
* Model field types
* Hydration behavior
* Schedule, game, roster, or statistics logic

## Testing rules

Do not rely exclusively on the live MLB API for test coverage.

Live API tests can fail because of:

* MLB API availability
* Data changing over time
* Seasonal data availability
* Undocumented response changes
* Historical games returning unusual payloads

Use deterministic mocked responses or recorded fixtures for behavior that does not require the live service.

Mocked HTTP tests must not be placed under `tests/external_tests/`.

Tests should verify actual values whenever possible.

Do not write tests that only use `hasattr()` on Pydantic models. A declared field can exist while silently remaining `None` because its alias does not match the MLB response key.

When fixing a reported game or player response, add a regression test that reproduces the original failure.

## Backward compatibility

Preserve the existing public API unless the task explicitly authorizes a breaking change.

Existing usage such as the following must continue to work:

```python
import mlbstatsapi

mlb = mlbstatsapi.Mlb()
player = mlb.get_person(664034)
```

Do not casually change:

* Public method names
* Public method arguments
* Return types
* Model attribute names
* Exported classes
* Exception inheritance
* Existing not-found behavior

The library currently maps many 404 responses to domain-level empty results such as:

* `None`
* `[]`
* `{}`

Do not change this behavior as part of unrelated work.

Any new package exception must inherit from:

```python
TheMlbStatsApiException
```

## MLB API model rules

The MLB Stats API is undocumented and inconsistent.

Do not assume every key follows ordinary camelCase rules.

Examples of unusual MLB capitalization may include:

```text
strikeOuts
groundOuts
calendarEventID
startTimeTBD
fullFMLName
aX
aY
aZ
```

Use explicit Pydantic aliases when the actual MLB response key cannot be derived safely.

When accepting multiple observed spellings, use Pydantic validation aliases such as `AliasChoices` rather than duplicating fields.

The base models intentionally ignore unknown fields to remain resilient to MLB API changes. Because of this, alias mistakes can silently discard data.

Tests for model changes must confirm that incoming values populate the intended model field.

Do not change a model field type based on one response without checking:

* Current data
* Historical data
* Missing values
* Null values
* Numeric strings
* Integer and floating-point variations

Prefer tolerant parsing when MLB returns inconsistent but logically equivalent values.

## HTTP adapter rules

All network calls must remain bounded.

Every HTTP request must use an explicit timeout.

Retries must be:

* Bounded
* Limited to safe HTTP methods
* Limited to transient failures
* Implemented with backoff
* Respectful of `Retry-After` when available

Do not retry ordinary client errors such as:

* 400
* 401
* 403
* 404

Do not retry Pydantic validation failures or JSON decoding failures.

Do not introduce default response caching without explicit approval. Live games, schedules, rosters, and historical data have different freshness requirements.

Do not introduce hardcoded global rate limiting without explicit approval.

Do not convert the existing synchronous public API into an asynchronous API.

A future async client should be additive rather than replacing `Mlb`.

When supporting injected HTTP sessions or transports:

* Do not close resources owned by the caller.
* Close resources created by the library.
* Make ownership behavior explicit and test it.

Do not configure the consuming application's global logging level from inside the library.

## Error handling

Distinguish between:

* Connection failures
* Timeouts
* HTTP failures
* Invalid JSON
* Model validation failures
* Domain-level not-found results

Do not hide server failures by returning empty successful results.

Do not classify an HTML 500 or 502 response as only a JSON decoding error.

Exceptions should preserve useful context where possible, including:

* Status code
* Request URL
* Response message
* Original exception

Avoid logging full response data when it may be extremely large.

## Code style

Follow the existing project style unless a dedicated formatting configuration is added.

Use:

* Type annotations
* Clear method and variable names
* Small focused functions
* Standard-library types such as `list`, `dict`, and `tuple`
* Pydantic v2 APIs
* Specific exception handling

Avoid:

* Mutable default arguments
* Bare `except` clauses
* Unbounded network operations
* Large unrelated refactors
* Adding abstractions before they are needed
* Reformatting unrelated files
* Changing public behavior without tests

Comments should explain why behavior is necessary, especially when working around an unusual MLB API response.

Do not add comments that only restate the code.

## Pull request scope

Keep pull requests focused.

A pull request should ideally address one of the following:

* Tests
* A bug fix
* Transport behavior
* Model corrections
* Documentation
* CI
* Release preparation

Do not combine unrelated endpoint fixes, model refactors, CI changes, and release publishing changes into one large pull request unless they cannot be separated safely.

Every pull request should explain:

* Why the change is needed
* What changed
* How it was tested
* Risk level
* Possible impact
* What was intentionally left out

## Branch conventions

Use descriptive branch prefixes:

```text
feat/
fix/
test/
docs/
refactor/
chore/
release/
```

Examples:

```text
test/http-adapter-contract
fix/http-adapter-correctness
feat/shared-http-session
feat/http-retries-errors
docs/http-transport
release/0.8.0
```

Do not push unfinished release work directly to `main`.

For version-specific release work, follow the plan in:

```text
docs/releases/0.8.0.md
```

The version 0.8.0 integration flow is:

```text
feature branch
    ↓
release/0.8.0
    ↓
main
    ↓
v0.8.0
```

Feature branches for version 0.8.0 should start from and target `release/0.8.0`.

## Publishing safety

Do not:

* Publish to PyPI
* Publish to TestPyPI
* Create a release
* Create or push a version tag
* Change package credentials
* Merge a release into `main`

unless the user explicitly requests that action.

Building a local package with `poetry build` is allowed and expected.

Before publishing a release:

1. Run the complete offline test suite.
2. Run the external MLB API test suite.
3. Build the package.
4. Install the built wheel in a clean virtual environment.
5. Run public API smoke tests.
6. Confirm the package version.
7. Review the complete release diff.
8. Confirm the release notes are accurate.

## Definition of done

A change is complete when:

* Relevant offline tests pass.
* Relevant external tests pass when required.
* Existing public behavior remains compatible.
* New behavior has regression coverage.
* The built package succeeds when packaging behavior changed.
* Documentation is updated when public usage changed.
* No unrelated files were modified.
* No publishing or release action occurred without explicit authorization.
