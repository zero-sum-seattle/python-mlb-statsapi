<div align="center">

# Python MLB Stats API

**The Unofficial Python Wrapper for the MLB Stats API**

[![PyPI version](https://badge.fury.io/py/python-mlb-statsapi.svg)](https://badge.fury.io/py/python-mlb-statsapi)
[![Offline CI](https://github.com/zero-sum-seattle/python-mlb-statsapi/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/zero-sum-seattle/python-mlb-statsapi/actions/workflows/build-and-test.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-mlb-statsapi)
![GitHub](https://img.shields.io/github/license/zero-sum-seattle/python-mlb-statsapi)

### [Wiki](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki) | [Examples](docs/examples.md) | [Documentation](#documentation) | [MLB Stats API](https://statsapi.mlb.com/)

<div align="left">

*Python-mlb-statsapi* is a Python library that provides access to the MLB Stats API, allowing developers to retrieve information related to MLB teams, players, stats, and more. Written in Python 3.10+.

All models are built with [Pydantic](https://docs.pydantic.dev/) for robust data validation and serialization. Field names follow Python's `snake_case` convention for a more Pythonic experience.

### *Copyright Notice*

This package and its authors are not affiliated with MLB or any MLB team. This API wrapper interfaces with MLB's Stats API. Use of MLB data is subject to the notice posted at http://gdx.mlb.com/components/copyright.txt.

###### This is an educational project - Not for commercial use.

![MLB Stats API](https://user-images.githubusercontent.com/2068393/203456246-dfdbdf0f-1e43-4329-aaa9-1c4008f9800d.jpg)

## Installation

```bash
python3 -m pip install python-mlb-statsapi
```

The declared requirement is `>=3.10`. CI validates Python 3.10, 3.11, 3.12, 3.13, and 3.14 (3.10 through 3.14), and there is no upper Python bound. See [Python support](docs/public-api.md#python-support) for the full policy.

An optional `async` extra is declared for the upcoming asynchronous client:

```bash
python3 -m pip install "python-mlb-statsapi[async]"
```

Today that extra only installs the optional HTTPX dependency. The async client itself is not part of this release — see [Async usage](#async-usage).

## Quick Start

```python
import mlbstatsapi

with mlbstatsapi.Mlb() as mlb:
    team = mlb.get_team(136)
    print(team.name, team.franchise_name)

    player_id = mlb.get_people_id("Ty France")[0]
    player = mlb.get_person(player_id)
    print(player.full_name)
```

A context manager closes the HTTP resources the library created when the block exits, including when it exits because of an exception. Callers who do not use a context manager can call `mlb.close()` instead. Requests sent through a library-created Session identify as `python-mlb-statsapi/1.0.1`; see [User-Agent](docs/http-transport.md#user-agent) for the details and for injected-Session behavior.

Looking up stats:

```python
>>> stats = ['season', 'seasonAdvanced']
>>> groups = ['hitting']
>>> params = {'season': 2022}
>>> mlb.get_player_stats(664034, stats, groups, **params)
{'hitting': {'season': Stat, 'seasonAdvanced': Stat }}
```

More endpoint examples live in the [usage examples](docs/examples.md) and the [Wiki](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki).

## Async Usage

An asynchronous client (`AsyncMlb`) is planned for version 1.1 and tracked by [issue #303](https://github.com/zero-sum-seattle/python-mlb-statsapi/issues/303). It is **not** available yet, and the synchronous `Mlb` client is unchanged by that work.

The async quick start will live here once the client ships. See [docs/async.md](docs/async.md) for the current status.

## Common Error Handling

`Mlb()` uses strict HTTP handling by default: a final non-404 4xx or 5xx response raises `MlbHttpError`, while a 404 keeps existing endpoint-specific `None` / `[]` / `{}` behavior.

```python
import mlbstatsapi

try:
    with mlbstatsapi.Mlb() as mlb:
        player = mlb.get_person(664034)
except mlbstatsapi.MlbTimeoutError:
    print("The MLB API timed out")
except mlbstatsapi.MlbHttpError as exc:
    print(exc.status_code, exc.reason, exc.url)
```

All package exceptions inherit from `TheMlbStatsApiException`, so broad `except TheMlbStatsApiException` handling stays valid.

For the complete behavior — timeouts, the retry policy, the full status decision table, `strict_http=False` compatibility mode and its warning, Session ownership and injection, exception attributes, and migration guidance — see the [HTTP transport documentation](docs/http-transport.md).

## Working with Models

Every returned object is a Pydantic model with `snake_case` field names:

```python
>>> player = mlb.get_person(664034)
>>> player.full_name          # Not fullName
'Ty France'
>>> player.model_dump(exclude_none=True)
{'id': 664034, 'full_name': 'Ty France', 'link': '/api/v1/people/664034', ...}
```

`model_dump_json()`, field filtering, and longer serialization examples are covered in the [usage examples](docs/examples.md#working-with-pydantic-models).

## Documentation

| Document | Contents |
| --- | --- |
| [Wiki](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki) | Endpoint reference, return objects, and data-type documentation |
| [Usage examples](docs/examples.md) | Extended examples for stats, schedules, games, teams, and more |
| [Async usage](docs/async.md) | Asynchronous client guide (pending [#303](https://github.com/zero-sum-seattle/python-mlb-statsapi/issues/303)) |
| [HTTP transport](docs/http-transport.md) | Timeouts, retries, strict HTTP, 404 handling, compatibility mode, exceptions, Session ownership, User-Agent |
| [Public API contract](docs/public-api.md) | Supported symbols, constructor signatures, endpoint methods and return shapes, stability policy |
| [Release notes](docs/releases/) | Per-release changes and migration guidance |

Upgrading? See the [release notes](docs/releases/) and the [migration guidance](docs/http-transport.md#migrating-from-09x-to-10).

## Contributing

Contributions are welcome! Whether it's bug fixes, new features, or documentation improvements, we appreciate your help.

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/python-mlb-statsapi.git`
3. Install dependencies: `poetry install`
4. Create a branch: `git checkout -b feat/your-feature`

Offline tests are deterministic and should run before every pull request:

```bash
poetry run pytest tests/ --ignore=tests/external_tests
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the external test suite, full local release validation, pull request guidelines, and branch naming conventions.

Found a bug or have a feature request? Please [open an issue](https://github.com/zero-sum-seattle/python-mlb-statsapi/issues/new) with a clear description, steps to reproduce, expected versus actual behavior, and your Python and package versions.

## License

Released under the [MIT License](LICENSE).

This package and its authors are not affiliated with MLB or any MLB team. Use of MLB data is subject to the notice posted at http://gdx.mlb.com/components/copyright.txt.
