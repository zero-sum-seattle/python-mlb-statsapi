# HTTP Transport

This document describes the HTTP transport behavior introduced in version 0.8.0.

The public client remains synchronous. Ordinary usage does not need to configure sessions or retries.

## Existing usage

Existing construction continues to work:

```python
import mlbstatsapi

mlb = mlbstatsapi.Mlb()
player = mlb.get_person(664034)
```

The client remains synchronous. Async support is not part of version 0.8.0.

## Context manager

Prefer a context manager when you want automatic cleanup of a library-created Session:

```python
import mlbstatsapi

with mlbstatsapi.Mlb() as mlb:
    player = mlb.get_person(664034)
```

Exiting the block closes a Session created by the library.

It does not close a caller-owned injected Session.

## Explicit cleanup

You can also close the client explicitly:

```python
mlb = mlbstatsapi.Mlb()

try:
    player = mlb.get_person(664034)
finally:
    mlb.close()
```

Repeated `close()` calls are safe.

## Default timeout

Every request uses an explicit timeout.

The default is:

```python
DEFAULT_TIMEOUT = (3.05, 30.0)
```

That means:

```text
3.05 seconds: connection timeout
30 seconds: read timeout
```

The read timeout is the maximum wait while reading response data. It is not one total wall-clock duration for the complete request.

## Custom timeout

A scalar applies the same value to both connect and read phases:

```python
mlb = mlbstatsapi.Mlb(timeout=10)
```

A tuple provides separate connect and read values:

```python
mlb = mlbstatsapi.Mlb(
    timeout=(5.0, 60.0),
)
```

## Shared Session model

One `requests.Session` is shared by the client's adapters:

```text
Mlb client
├── v1 adapter ────┐
│                  ├── shared requests.Session
└── v1.1 adapter ──┘
```

A Session manages:

* Reusable connection pools
* Shared HTTP configuration
* Mounted retry adapters on library-created Sessions

A Session is not:

* A response cache
* One guaranteed permanent TCP connection
* An async transport

## Session injection

Advanced callers may inject a Session:

```python
import requests
import mlbstatsapi

session = requests.Session()

try:
    mlb = mlbstatsapi.Mlb(session=session)
    player = mlb.get_person(664034)
finally:
    session.close()
```

Ownership rules:

```text
Library-created Session
    The library owns and closes it

Caller-injected Session
    The caller owns and closes it
```

The library does not install or replace retry adapters on caller-injected Sessions.

Callers who inject a Session control its retry, TLS, proxy, and adapter configuration.

## Default retry policy

Library-created Sessions mount a bounded retry policy for GET requests.

```text
Initial request: 1
Maximum retries: 3
Maximum total attempts: 4
Allowed method: GET
Backoff factor: 0.5
Retry-After respected: yes
```

Retryable HTTP statuses:

```text
429
500
502
503
504
```

Non-retryable ordinary client statuses:

```text
400
401
403
404
```

Additional rules:

* Retries are bounded
* Only GET requests are retried
* Invalid JSON is not retried
* Pydantic validation failures are not retried
* Application parsing failures are not retried
* A final 404 preserves existing not-found behavior
* A final 429 preserves existing 4xx compatibility
* A final 5xx raises `MlbHttpError`

Retries improve resilience for transient failures. They do not guarantee success.

## Structured exceptions

```text
TheMlbStatsApiException
├── MlbTransportError
│   └── MlbTimeoutError
├── MlbHttpError
└── MlbDecodeError
```

Imports:

```python
from mlbstatsapi import (
    MlbDecodeError,
    MlbHttpError,
    MlbTimeoutError,
    MlbTransportError,
    TheMlbStatsApiException,
)
```

Precise handling:

```python
try:
    player = mlb.get_person(664034)
except MlbTimeoutError:
    print("The MLB API timed out")
except MlbTransportError:
    print("The request could not reach the MLB API")
except MlbHttpError as exc:
    print(
        exc.status_code,
        exc.reason,
        exc.url,
    )
except MlbDecodeError:
    print("The MLB API returned invalid JSON")
```

Backward-compatible handling remains valid because all new errors inherit from `TheMlbStatsApiException`:

```python
try:
    player = mlb.get_person(664034)
except TheMlbStatsApiException:
    print("The MLB request failed")
```

Notes:

* `MlbTimeoutError` is a subtype of `MlbTransportError`
* All new errors inherit from `TheMlbStatsApiException`
* Existing broad exception handling remains valid
* Original Requests or JSON decoding failures are preserved through exception chaining

## HTTP exception attributes

`MlbHttpError` exposes:

```text
method
status_code
reason
url
response_data
body_excerpt
```

Existing attributes remain compatible:

```text
status_code
reason
url
```

Additional context:

* `method` is the HTTP method when the adapter raises the error (`GET` today). Manually constructed exceptions without a method leave `method` as `None`.
* `response_data` contains a decoded JSON dictionary or list when the error body is valid JSON of that shape.
* `response_data` is `None` for invalid JSON, HTML, plain text, empty bodies, or JSON scalars such as strings, numbers, booleans, or null.
* `body_excerpt` contains at most 500 characters of the response text for non-empty bodies.
* `body_excerpt` is `None` for an empty body.
* Error-context extraction is best-effort. A parsing or decoding failure while collecting context must not replace the original HTTP error.
* Complete `requests.Response` objects are not exposed.
* Complete large response bodies are not preserved beyond the excerpt limit.
* Response bodies are not automatically logged.
* `str(exc)` remains concise, for example `500: Internal Server Error`, and does not include the response body, excerpt, or `response_data`.

Usage:

```python
try:
    player = mlb.get_person(664034)
except mlbstatsapi.MlbHttpError as exc:
    print(exc.method)
    print(exc.status_code)
    print(exc.reason)
    print(exc.url)
    print(exc.response_data)
    print(exc.body_excerpt)
```

Precise handling with the expanded attributes:

```python
try:
    player = mlb.get_person(664034)
except MlbHttpError as exc:
    print(
        exc.method,
        exc.status_code,
        exc.reason,
        exc.url,
        exc.response_data,
        exc.body_excerpt,
    )
```

## Existing 404 behavior

Version 0.8.0 preserves endpoint-specific not-found behavior.

Depending on the endpoint, a 404 may become:

```text
None
[]
{}
```

Not every 404 raises `MlbHttpError`.

## No response caching

Shared Sessions pool network connections. They do not cache MLB response bodies.

The client has no default response cache.

## No async support

The client remains synchronous.

Async support is not part of version 0.8.0.
