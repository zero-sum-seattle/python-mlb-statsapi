# HTTP Transport

This document describes the HTTP transport behavior of the current release,
version 1.0.0.

Version 0.8.0 introduced shared Sessions, explicit timeouts, bounded retries,
and structured exceptions. Version 0.9.0 introduced configurable strict
behavior and compatibility warnings. Version 1.0.0 makes strict handling the
default and defines the stable public contract.

The public client remains synchronous. Ordinary usage does not need to
configure sessions or retries.

See [the 1.0.0 release notes](releases/1.0.0.md) for a shorter summary of what
changed. For the authoritative public API boundary see
[the public API contract](public-api.md).

## Public transport API

Everything this document describes is reachable from the package root:

```python
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
```

Names that are not exported from `mlbstatsapi` are internal and may change
without a deprecation cycle. See [public-api.md](public-api.md) for the
complete stability classification.

## Existing usage

Existing construction continues to work:

```python
import mlbstatsapi

mlb = mlbstatsapi.Mlb()
player = mlb.get_person(664034)
```

In version 1.0.0 that construction uses strict HTTP handling by default. The
client remains synchronous. Async support is not part of version 1.0.0.

## Context manager

Prefer a context manager when you want automatic cleanup of a library-created
Session:

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

```text
(3.05, 30.0)
```

That means:

```text
3.05 seconds: connection timeout
30 seconds: read timeout
```

The read timeout is the maximum wait while reading response data. It is not
one total wall-clock duration for the complete request.

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

## Session ownership

Session ownership is the single most important rule in this document. Whoever
creates the Session configures it and closes it.

```text
Library-created Session
    Configured and closed by the library
    Receives retry adapters
    Receives the package User-Agent

Caller-injected Session
    Configured and closed by the caller
    Existing adapters remain untouched
    Existing headers remain untouched
```

The library never installs adapters, replaces headers, or closes a Session it
did not create. `Mlb.close()` and exiting `with Mlb(session=session)` both
leave an injected Session open.

The version 1.0 strict default does not change Session ownership, injection,
or cleanup behavior.

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

Callers who inject a Session control its retry, TLS, proxy, header, and
adapter configuration. See [Reusing the retry policy on a caller-managed
Session](#reusing-the-retry-policy-on-a-caller-managed-session) for opting in
to the library's tested retry policy.

## User-Agent

Library-created Sessions send a package-specific User-Agent:

```text
python-mlb-statsapi/<installed-version>
```

With the package version currently declared in project metadata that resolves to:

```text
python-mlb-statsapi/1.0.1
```

The version comes from the installed package metadata, so it always matches
the installed release without a separately maintained version string.

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

Library-created Sessions mount a bounded retry policy for GET requests
automatically.

Caller-injected Sessions are never automatically reconfigured. Retry settings
on an injected Session remain under the caller's control unless the caller
opts in.

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
* A final non-404 4xx, including a final 429, raises `MlbHttpError` under the default
* A final 5xx raises `MlbHttpError`
* Explicit `strict_http=False` preserves the historical empty result for final non-404 4xx and warns

Retries improve resilience for transient failures. They do not guarantee
success. The version 1.0 strict default does not change retry values or which
statuses are retried.

## Default HTTP behavior

Version 1.0.0 defaults to strict HTTP handling. These constructions are
equivalent:

```python
mlb = mlbstatsapi.Mlb()
mlb = mlbstatsapi.Mlb(strict_http=True)
```

Default behavior:

```text
Successful 2xx
    Return the normal endpoint result

Final non-404 4xx
    Raise MlbHttpError by default

404
    Preserve endpoint-specific None, [], or {} behavior

Final 429
    Retry first, then raise MlbHttpError under the default

Final 5xx
    Retry where configured, then raise MlbHttpError

Timeout
    Raise MlbTimeoutError

Transport failure
    Raise MlbTransportError

Successful malformed JSON
    Raise MlbDecodeError
```

"Final" means the response remaining after the bounded retry policy has
completed. Intermediate retried responses neither raise nor warn.

## Behavior table

| Final response | Default 1.0 behavior         | Explicit `strict_http=False`                      |
| -------------- | ---------------------------- | ------------------------------------------------- |
| Successful 2xx | Normal result                | Normal result                                     |
| Non-404 4xx    | `MlbHttpError`               | Warning and historical empty result               |
| 404            | Existing endpoint behavior   | Existing endpoint behavior                        |
| Final 429      | `MlbHttpError` after retries | Warning and historical empty result after retries |
| Final 5xx      | `MlbHttpError`               | `MlbHttpError`                                    |

Notes:

* `Mlb()` and `Mlb(strict_http=True)` are equivalent spellings of the default
* `strict_http=False` is an explicit compatibility opt-out, not the preferred long-term configuration
* Strict handling applies only after retries are exhausted
* Strict handling does not make 404 raise
* Strict handling does not change transport or decode exceptions
* Raised `MlbHttpError` instances include the richer response context attributes

Recommended default usage:

```python
import mlbstatsapi

try:
    with mlbstatsapi.Mlb() as mlb:
        player = mlb.get_person(664034)
except mlbstatsapi.MlbHttpError as exc:
    print(exc.method)
    print(exc.status_code)
    print(exc.reason)
    print(exc.url)
    print(exc.response_data)
    print(exc.body_excerpt)
```

## Compatibility mode

```python
mlb = mlbstatsapi.Mlb(strict_http=False)
```

is an explicit compatibility opt-out. It:

* Preserves the historical empty result for final non-404 4xx responses
* Emits `MlbHttpCompatibilityWarning` exactly once per suppressed final response
* Does not change 404 behavior
* Does not suppress final 5xx errors
* Does not alter timeout, transport, or decode failures
* Runs only after retry exhaustion

`strict_http=False` is a compatibility mode for users migrating from pre-1.0
behavior. It will remain available throughout the 1.x release series and may
be removed in 2.0. New code should use the default `strict_http=True` behavior
and handle `MlbHttpError`.

## Compatibility warnings

When `strict_http=False` converts a final non-404 4xx response into the
historical empty result, the library emits `MlbHttpCompatibilityWarning`.

The warning means the default strict path would have raised `MlbHttpError` for
the same response. It is emitted once per suppressed final response and is
attributed to the public caller frame outside the `mlbstatsapi` package
namespace.

The warning's semantic content includes:

```text
Status code
Request URL
strict_http=False selected compatibility mode
Historical empty result was returned
Strict handling is the version 1.0 default
How to receive MlbHttpError instead
```

Warning messages contain only the status code and request URL from the
response. Response bodies, headers, credentials, cookies, and tokens are never
included. Do not treat the complete prose string as a stable public contract;
filter and handle the warning by category.

The category inherits from `FutureWarning` so the migration notice stays
visible under default Python warning filters.

A warning is emitted only when all three of the following are true:

* Compatibility mode is active (`strict_http=False`)
* The final response is a non-404 4xx
* The default strict path would have raised `MlbHttpError` for the same response

No warning is emitted for:

```text
Successful responses
404
Default strict handling
Intermediate retries
Final 5xx
Timeouts
Transport failures
Decode failures
Pydantic validation failures
```

When the warning is emitted:

| Response                                           | Warning |
| -------------------------------------------------- | ------- |
| Non-404 4xx, `strict_http=False`                   | Yes     |
| Final 429, `strict_http=False`, after retries      | Yes     |
| Non-404 4xx, default / `strict_http=True`          | No, `MlbHttpError` is raised instead |
| 404, either mode                                   | No      |
| Successful 2xx                                     | No      |
| Final 5xx                                          | No, `MlbHttpError` is raised in both modes |
| Timeout, transport, decode, or validation failure  | No      |

Additional rules:

* The warning never changes the return value; compatibility mode still returns the historical empty result
* A final 404 remains warning-free and keeps existing `None` / `[]` / `{}` behavior
* Warnings are emitted only after retries are exhausted, so a retried 429 warns once
* Default strict handling does not warn because it raises `MlbHttpError` directly

## Warning-as-error environments

Applications may treat warnings as exceptions:

```python
import warnings
import mlbstatsapi

warnings.filterwarnings(
    "error",
    category=mlbstatsapi.MlbHttpCompatibilityWarning,
)
```

Under `strict_http=False`, this can turn a suppressed 4xx into a warning
exception. The preferred migration is to remove `strict_http=False` and catch
`MlbHttpError`. A temporary targeted warning filter is acceptable.

Temporary targeted ignore, labeled as migration-only behavior:

```python
import warnings
import mlbstatsapi

warnings.filterwarnings(
    "ignore",
    category=mlbstatsapi.MlbHttpCompatibilityWarning,
)
```

Ignoring the warning is temporary migration behavior. Disabling every warning
or every `FutureWarning` is not recommended; that would also hide unrelated
notices from other libraries. Filter by
`mlbstatsapi.MlbHttpCompatibilityWarning` specifically.

## Migrating from 0.9.x to 1.0

Recommended process:

1. Identify code that relied on empty results for failed non-404 4xx responses
2. Add handling for `MlbHttpError`
3. Distinguish 404 domain results from other HTTP failures
4. Use `strict_http=False` only where migration cannot happen immediately
5. Test warning-as-error configurations
6. Remove `strict_http=False`
7. Confirm injected Session and retry behavior remain correct

Version 0.9-style compatibility:

```python
import mlbstatsapi

with mlbstatsapi.Mlb(strict_http=False) as mlb:
    player = mlb.get_person(664034)
```

Recommended 1.0 state:

```python
import mlbstatsapi

try:
    with mlbstatsapi.Mlb() as mlb:
        player = mlb.get_person(664034)
except mlbstatsapi.MlbHttpError as exc:
    print(exc.status_code)
    print(exc.url)
```

A missing person may still return `None` on a 404 and is not necessarily an
exception. Catch `MlbHttpError` for unexpected HTTP failures; continue treating
endpoint-specific 404 empty results as domain-level not-found outcomes.

## Public API stability

Version 1.0.0 documents the stable public API in
[public-api.md](public-api.md). That contract covers package-root imports,
constructor signatures, the exception hierarchy, Session ownership, documented
endpoint methods, Python support, and the boundary between public and
internal APIs.

This transport guide does not duplicate that contract. In particular, version
1.0 does not promise that:

* Every upstream MLB response field is frozen
* Every class in `mlbstatsapi.models` is permanently stable
* The unofficial MLB API itself will never change
* Private underscore-prefixed names are public

## Reusing the retry policy on a caller-managed Session

`create_retry_policy()` returns a new instance of the same tested retry policy
used internally for library-created Sessions.

Callers who inject a Session must mount the policy themselves. The library
does not install or replace adapters on caller-injected Sessions.

Callers retain control over connection-pool sizes and other `HTTPAdapter`
options. The caller remains responsible for closing an injected Session.

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

Mounting the same adapter instance for both schemes is valid. Callers may also
mount separate adapters when they need different settings for HTTP and HTTPS.

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

Backward-compatible handling remains valid because all new errors inherit from
`TheMlbStatsApiException`:

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

Version 1.0.0 preserves endpoint-specific not-found behavior under both the
default and `strict_http=False`.

Depending on the endpoint, a 404 may become:

```text
None
[]
{}
```

Not every 404 raises `MlbHttpError`. The strict default does not change this,
and a 404 never emits `MlbHttpCompatibilityWarning`.

## No response caching

Shared Sessions pool network connections. They do not cache MLB response
bodies.

The client has no default response cache.

## Async client environment proxies

Library-created `AsyncMlb` / `AsyncMlbDataAdapter` clients honor
`HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, and `NO_PROXY` (any case), the same
environment variables HTTPX itself discovers for a plain `httpx.AsyncClient()`.

```text
Library-created async client
    Reads HTTP_PROXY / HTTPS_PROXY / ALL_PROXY / NO_PROXY from the environment
    Routes matching requests through the proxy
    Applies the library retry policy to proxied and direct requests alike

Caller-injected async client
    Keeps exactly whatever transport and mounts its caller configured
    The library never reads proxy environment variables for it
```

This mirrors [Session ownership](#session-ownership) on the sync side: the
library only ever configures a client it created itself. See
[async.md](async.md#custom-httpx-client) for injecting a client, including one
configured with its own proxy settings.

## Scope of this document

The retry, timeout, User-Agent, and strict-HTTP behavior documented above
apply to the synchronous `Mlb` client. For the asynchronous client, see
[async.md](async.md); it shares this document's retry, timeout, and
error-handling contract except where noted above.
