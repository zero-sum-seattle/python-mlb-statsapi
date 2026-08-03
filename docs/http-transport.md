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

## User-Agent

Library-created Sessions send a package-specific User-Agent:

```text
python-mlb-statsapi/<installed-version>
```

The version comes from the installed package metadata, so it always matches the
installed release without a separately maintained version string.

Notes:

* The header helps identify package traffic while debugging
* Other Requests default headers such as `Accept-Encoding`, `Accept`, and `Connection` remain intact
* Only `User-Agent` is set; the full header mapping is never replaced
* Caller-injected Sessions are never modified
* Applications using an injected Session may set their own User-Agent
* The header contains no machine identifiers, installation identifiers, hostnames, or user tracking data
* This is not telemetry and sends no analytics

If the distribution metadata is unavailable, for example in an unusual
source-only environment, the header falls back to:

```text
python-mlb-statsapi/unknown
```

Callers who inject a Session control the User-Agent themselves:

```python
import requests
import mlbstatsapi

session = requests.Session()
session.headers.update(
    {
        "User-Agent": "my-baseball-project/1.0",
    }
)

try:
    with mlbstatsapi.Mlb(session=session) as mlb:
        player = mlb.get_person(664034)
finally:
    session.close()
```

## Default retry policy

Library-created Sessions mount a bounded retry policy for GET requests automatically.

Caller-injected Sessions are never automatically reconfigured. Retry settings on an
injected Session remain under the caller's control unless the caller opts in.

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
* A final 429 preserves existing 4xx compatibility by default
* A final 5xx raises `MlbHttpError`
* In strict mode, a final non-404 4xx (including a final 429) raises `MlbHttpError`

Retries improve resilience for transient failures. They do not guarantee success.

## HTTP compatibility modes

Compatibility mode remains the default:

```python
mlb = mlbstatsapi.Mlb()
```

or:

```python
mlb = mlbstatsapi.Mlb(
    strict_http=False,
)
```

Callers may explicitly enable strict mode:

```python
mlb = mlbstatsapi.Mlb(
    strict_http=True,
)
```

Behavior:

| Response    | Compatibility                    | Strict                     |
| ----------- | -------------------------------- | -------------------------- |
| Non-404 4xx | Empty endpoint-compatible result | `MlbHttpError`             |
| 404         | Existing endpoint behavior       | Existing endpoint behavior |
| Final 429   | Empty result                     | `MlbHttpError`             |
| Final 5xx   | `MlbHttpError`                   | `MlbHttpError`             |

Notes:

* Compatibility mode remains the default
* Strict mode is explicitly opt-in
* Strict mode applies only after retries are exhausted
* Strict mode does not make 404 raise
* Strict mode does not change transport or decode exceptions
* Strict-mode exceptions include the richer context from `MlbHttpError`
* Existing constructor usage remains valid
* Compatibility mode emits `MlbHttpCompatibilityWarning` for a suppressed non-404 4xx

Example:

```python
import mlbstatsapi

try:
    with mlbstatsapi.Mlb(strict_http=True) as mlb:
        player = mlb.get_person(664034)
except mlbstatsapi.MlbHttpError as exc:
    print(exc.method)
    print(exc.status_code)
    print(exc.reason)
    print(exc.url)
    print(exc.response_data)
    print(exc.body_excerpt)
```

## Compatibility warnings

Version 0.9.0 emits `MlbHttpCompatibilityWarning` when compatibility mode returns the
historical empty result for a final non-404 4xx response.

The warning means strict mode would have raised `MlbHttpError` for the same response.

```python
import mlbstatsapi

mlb = mlbstatsapi.Mlb()
sports = mlb.get_sports()
```

A representative warning looks like:

```text
HTTP 403 for https://statsapi.mlb.com/api/v1/sports was handled through
compatibility mode and returned the historical empty result. Pass
strict_http=True to raise MlbHttpError. This compatibility behavior may
change in version 1.0.
```

The category inherits from `FutureWarning` so the migration notice stays visible under
default Python warning filters.

When the warning is emitted:

| Response                  | Warning |
| ------------------------- | ------- |
| Non-404 4xx, compatibility mode | Yes |
| Final 429, compatibility mode, after retries | Yes |
| Non-404 4xx, strict mode  | No, `MlbHttpError` is raised instead |
| 404, either mode          | No      |
| Successful 2xx            | No      |
| Final 5xx                 | No, `MlbHttpError` is raised in both modes |
| Timeout, transport, decode, or validation failure | No |

Additional rules:

* The warning never changes the return value; compatibility mode still returns the
  historical empty result in version 0.9.0
* A final 404 remains warning-free and keeps existing `None` / `[]` / `{}` behavior
* Warnings are emitted only after retries are exhausted, so a retried 429 warns once
* Strict mode does not warn because it raises `MlbHttpError` directly
* Warning messages contain only the status code and request URL, never response
  bodies, headers, or credentials
* Stricter defaults may be introduced in version 1.0

Enabling strict mode is the recommended migration:

```python
import mlbstatsapi

mlb = mlbstatsapi.Mlb(
    strict_http=True,
)
```

Applications may also turn only this package warning into an exception:

```python
import warnings
import mlbstatsapi

warnings.filterwarnings(
    "error",
    category=mlbstatsapi.MlbHttpCompatibilityWarning,
)
```

Or silence only this category:

```python
import warnings
import mlbstatsapi

warnings.filterwarnings(
    "ignore",
    category=mlbstatsapi.MlbHttpCompatibilityWarning,
)
```

Prefer enabling strict mode over permanently ignoring the warning when the application
wants explicit HTTP failures. Filter by `mlbstatsapi.MlbHttpCompatibilityWarning` rather
than disabling all `FutureWarning` or all warnings, which would also hide unrelated
notices from other libraries.

## Reusing the retry policy on a caller-managed Session

`create_retry_policy()` returns a new instance of the same tested retry policy used
internally for library-created Sessions.

Callers who inject a Session must mount the policy themselves. The library does not
install or replace adapters on caller-injected Sessions.

Callers retain control over connection-pool sizes and other `HTTPAdapter` options.
The caller remains responsible for closing an injected Session.

```python
import requests
import mlbstatsapi

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(
    max_retries=mlbstatsapi.create_retry_policy(),
    pool_connections=10,
    pool_maxsize=20,
)
session.mount("https://", adapter)
session.mount("http://", adapter)

try:
    with mlbstatsapi.Mlb(session=session) as mlb:
        player = mlb.get_person(664034)
finally:
    session.close()
```

Mounting the same adapter instance for both schemes is valid. Callers may also mount
separate adapters when they need different settings for HTTP and HTTPS.

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
