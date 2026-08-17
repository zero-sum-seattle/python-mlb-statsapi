# Async Usage

> **Status: not available yet.**
>
> The asynchronous client (`AsyncMlb`) is planned for version 1.1 and is
> tracked by [issue #303](https://github.com/zero-sum-seattle/python-mlb-statsapi/issues/303).
> It is **not** implemented in this branch, so this document is currently a
> placeholder rather than a usage guide.
>
> Nothing below should be read as describing shipped behavior. The sections are
> reserved so the guide can be filled in against the implemented contract once
> #303 lands, instead of being written speculatively.

The synchronous [`Mlb`](../README.md#quick-start) client is unaffected by this
work and remains the supported client today. See the
[HTTP transport documentation](http-transport.md) for its precise transport
semantics and the [public API contract](public-api.md) for the stable surface.

## What exists today

Only the packaging half of async support has landed:

```toml
[tool.poetry.dependencies]
httpx = { version = ">=0.28.1,<1.0", optional = true }

[tool.poetry.extras]
async = ["httpx"]
```

That means `pip install "python-mlb-statsapi[async]"` currently installs the
optional HTTPX dependency and nothing else. There is no `AsyncMlb`,
`AsyncMlbDataAdapter`, `async with` support, or `aclose()` in the package yet;
importing them will fail.

## Sections reserved for #303

These headings are intentionally empty. Each will be written from the
implemented and tested behavior, and kept consistent with the contract in
[issue #298](https://github.com/zero-sum-seattle/python-mlb-statsapi/issues/298).

* Installing async support with the `async` extra
* Basic sequential async usage
* `async with AsyncMlb()` lifecycle
* Explicit `await mlb.aclose()` outside a context manager, and idempotent cleanup
* Library-owned versus caller-injected async clients, and the rule that
  caller-injected clients are never closed or silently reconfigured
* The initial supported endpoint set, and endpoints that remain unsupported
* Simple concurrent usage with ordinary asyncio orchestration
* Cancellation expectations
* Timeout usage at the public API level
* A short exception overview, with the precise retry and error semantics left
  to [http-transport.md](http-transport.md)

## Documentation boundaries

When this guide is written it should stay a usage guide:

* Precise transport semantics — timeouts, retry policy, retryable statuses,
  `Retry-After`, strict HTTP handling, 404 behavior, compatibility mode,
  exception mapping, client ownership, and User-Agent behavior — belong in
  [http-transport.md](http-transport.md).
* The stable public async surface — `AsyncMlb`, `AsyncMlbDataAdapter`,
  constructor signatures, and compatibility promises — belongs in
  [public-api.md](public-api.md).
* Release-specific migration guidance belongs in [releases/](releases/).
