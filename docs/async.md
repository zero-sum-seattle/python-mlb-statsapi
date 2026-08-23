# Async Usage

`AsyncMlb` is the public asynchronous client for `python-mlb-statsapi` 1.1.
It requires the optional `async` extra.

## Installation

```bash
python3 -m pip install "python-mlb-statsapi[async]"
```

A synchronous-only install remains unchanged and does not require HTTPX.

## Quick start

```python
import asyncio

from mlbstatsapi import AsyncMlb


async def main():
    async with AsyncMlb() as mlb:
        player = await mlb.get_person(664034)
        team = await mlb.get_team(136)

        print(player.full_name)
        print(team.name)


asyncio.run(main())
```

Use `async with` when possible so library-owned HTTP resources are closed when
the block exits. If a context manager is not practical, explicit cleanup is
also supported:

```python
mlb = AsyncMlb()
try:
    player = await mlb.get_person(664034)
finally:
    await mlb.aclose()
```

Repeated `aclose()` calls are safe.

## Concurrent requests

One `AsyncMlb` instance supports concurrent in-flight requests on the same
event loop. Concurrency is controlled by the caller.

```python
import asyncio

from mlbstatsapi import AsyncMlb


async def main():
    async with AsyncMlb() as mlb:
        player, team = await asyncio.gather(
            mlb.get_person(664034),
            mlb.get_team(136),
        )

        return player, team


player, team = asyncio.run(main())
```

`AsyncMlb` does not create hidden background tasks or automatic request fanout.
Cross-event-loop use of the same client is not promised.

## Supported endpoints

The async surface is intentionally smaller than the synchronous `Mlb` surface
while 1.1 support is being expanded. The currently supported awaitable endpoint
methods on `release/1.1.0` are:

```text
get_team(...)
get_teams(...)
get_person(...)
get_people(...)
get_schedule(...)
```

Where an async endpoint is supported, it returns the same Pydantic model types
and follows the same public HTTP/error behavior as the matching synchronous
method.

For the authoritative list and signatures, see the
[public API contract](public-api.md#asyncmlb-public-client).

## Error handling

The public exception hierarchy is shared with the synchronous client:

```python
from mlbstatsapi import (
    AsyncMlb,
    MlbDecodeError,
    MlbHttpError,
    MlbTimeoutError,
    MlbTransportError,
)


async def get_player():
    try:
        async with AsyncMlb() as mlb:
            return await mlb.get_person(664034)
    except MlbTimeoutError:
        print("The MLB API timed out")
    except MlbTransportError:
        print("The request could not reach the MLB API")
    except MlbHttpError as exc:
        print(exc.status_code, exc.reason)
    except MlbDecodeError:
        print("The MLB API returned invalid JSON")
```

`strict_http=True` is the default. Existing endpoint-specific 404 behavior is
preserved. See the [HTTP transport documentation](http-transport.md) for the
complete status, timeout, retry, and compatibility-mode contract.

## Custom HTTPX client

Advanced callers may inject their own `httpx.AsyncClient`:

```python
import httpx

from mlbstatsapi import AsyncMlb


client = httpx.AsyncClient()
try:
    async with AsyncMlb(client=client) as mlb:
        player = await mlb.get_person(664034)
finally:
    await client.aclose()
```

An injected client remains caller-owned and is not closed by `AsyncMlb`.

## Documentation boundaries

- [README](../README.md) — installation and quick-start examples
- [Usage examples](examples.md) — longer synchronous examples
- [Public API contract](public-api.md) — supported symbols, signatures, and endpoint coverage
- [HTTP transport](http-transport.md) — timeouts, retries, errors, and compatibility behavior
