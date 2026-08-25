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
the block exits.

## Without a context manager

If a context manager is not practical, create `AsyncMlb` directly and call
`await mlb.aclose()` when finished:

```python
import asyncio

from mlbstatsapi import AsyncMlb


async def main():
    mlb = AsyncMlb()
    try:
        player = await mlb.get_person(664034)
        team = await mlb.get_team(136)

        print(player.full_name)
        print(team.name)
    finally:
        await mlb.aclose()


asyncio.run(main())
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


async def get_person_with_custom_client(client: httpx.AsyncClient, person_id: int):
    async with AsyncMlb(client=client) as mlb:
        return await mlb.get_person(person_id)
```

`async with` and `await` are only valid inside an `async def`, so this is
written as a plain, reusable function rather than a top-level script. Call it
however your application already enters async code — `asyncio.run(...)`, a
web framework's request handler, an existing event loop, and so on. Nothing
here requires restructuring your application around a `main()` entry point;
`get_person_with_custom_client()` itself has no opinion on how it is invoked.

Below are a few ways to invoke it, depending on how your application already
enters async code.

**Script entry point**

```python
import asyncio


async def main():
    async with httpx.AsyncClient() as client:
        return await get_person_with_custom_client(client, 664034)


asyncio.run(main())
```

**Inside an application that already runs on an event loop** — a web
framework's request handler, a worker task, and so on — just `await` it
directly with a client your application already owns:

```python
async def handle_request(client: httpx.AsyncClient, person_id: int):
    return await get_person_with_custom_client(client, person_id)
```

**FastAPI (or another ASGI framework)**

```python
from fastapi import FastAPI

app = FastAPI()
http_client = httpx.AsyncClient()


@app.get("/players/{person_id}")
async def read_player(person_id: int):
    return await get_person_with_custom_client(http_client, person_id)
```

**Interactively, with no wrapper at all** — Jupyter/IPython and the
`python -m asyncio` REPL both support top-level `await`:

```pycon
>>> import httpx
>>> client = httpx.AsyncClient()
>>> player = await get_person_with_custom_client(client, 664034)
>>> await client.aclose()
```

An injected client remains caller-owned and is not closed by `AsyncMlb`. In a
real application the client is typically created once, reused across calls,
and closed by whatever code owns its lifecycle — the examples above show a
few ways to run this, not the required shape of your application.

## Documentation boundaries

- [README](../README.md) — installation and quick-start examples
- [Usage examples](examples.md) — longer synchronous examples
- [Public API contract](public-api.md) — supported symbols, signatures, and endpoint coverage
- [HTTP transport](http-transport.md) — timeouts, retries, errors, and compatibility behavior
