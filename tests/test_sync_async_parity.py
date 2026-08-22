"""Sync/async behavioral parity tests (issue #304).

`Mlb` is the compatibility baseline. These tests prove that `AsyncMlb`'s
public endpoint behavior stays aligned with it: the same response produces the
same request, the same model type, the same parsed values, and the same
"nothing to return" answer.

The scope is deliberately narrow. Detailed transport behavior — retries,
timing, backoff, and transport-specific context — is already covered by
tests/test_http_contract.py, tests/test_mlb_dataadapter.py and
tests/test_async_mlb_dataadapter.py, and payload parsing by tests/parsers/.
None of that is re-asserted here, and nothing compares Requests internals with
HTTPX internals. Each test drives both public clients over an equivalent canned
response or failure and compares only what a caller can see.

These tests must not contact the live MLB API.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any
from urllib.parse import parse_qsl, urlsplit

import pytest
import requests
import requests_mock

# The async client needs the optional HTTPX extra; without it there is no
# async side to compare against, so the whole module is skipped rather than
# failing a sync-only install at import time.
httpx = pytest.importorskip("httpx", reason="requires the async extra (HTTPX)")

from mlbstatsapi import (  # noqa: E402
    AsyncMlb,
    Mlb,
    MlbDecodeError,
    MlbHttpCompatibilityWarning,
    MlbHttpError,
    MlbTimeoutError,
    MlbTransportError,
)
from mlbstatsapi.models.people import Person  # noqa: E402
from mlbstatsapi.models.schedules import Schedule  # noqa: E402
from mlbstatsapi.models.teams import Team  # noqa: E402


TEAM_PAYLOAD = {"teams": [{"id": 133, "link": "/api/v1/teams/133", "name": "Athletics"}]}
PERSON_PAYLOAD = {
    "people": [{"id": 660271, "link": "/api/v1/people/660271", "fullName": "Shohei Ohtani"}]
}
PEOPLE_PAYLOAD = {
    "people": [
        {"id": 660271, "link": "/api/v1/people/660271", "fullName": "Shohei Ohtani"},
        {"id": 664034, "link": "/api/v1/people/664034", "fullName": "Ty France"},
    ]
}
# The lookup endpoints request reduced fields, so their payloads carry only the
# id and the searchable names. The second row is missing the alternate search
# key on purpose: a row without it is skipped rather than raising.
PEOPLE_LOOKUP_PAYLOAD = {
    "people": [
        {"id": 664034, "fullName": "Ty France", "lastName": "France"},
        {"id": 660271, "fullName": "Shohei Ohtani"},
    ]
}
TEAMS_LOOKUP_PAYLOAD = {
    "teams": [
        {"id": 133, "name": "Athletics", "abbreviation": "OAK"},
        {"id": 136, "name": "Seattle Mariners"},
    ]
}
SCHEDULE_PAYLOAD = {
    "totalItems": 1,
    "totalEvents": 0,
    "totalGames": 1,
    "totalGamesInProgress": 0,
    "dates": [
        {
            "date": "2022-10-07",
            "totalItems": 1,
            "totalEvents": 0,
            "totalGames": 1,
            "totalGamesInProgress": 0,
            "games": [],
        }
    ],
}

# Every way a call legitimately comes back with nothing to parse, held as the
# keyword arguments that produce it. Both clients are expected to answer the
# method's documented empty result: None, or an empty list.
NO_RESULT_RESPONSES = {
    "empty 200": {"payload": {}},
    "empty body": {"raw_body": b""},
    "404": {"status": 404, "payload": {}},
}
# A schedule can also answer with a well-formed envelope holding no dates.
SCHEDULE_NO_RESULT_RESPONSES = NO_RESULT_RESPONSES | {
    "no dates": {
        "payload": {
            "totalItems": 0,
            "totalEvents": 0,
            "totalGames": 0,
            "totalGamesInProgress": 0,
            "dates": [],
        }
    },
}

# What each lookup method is expected to answer for one canned payload, held
# as the keyword arguments that produce it. The two tables are deliberately
# parallel: people and teams differ only in the names being matched.
PEOPLE_ID_LOOKUPS = {
    "exact match": ({"fullname": "Ty France"}, [664034]),
    "case-insensitive match": ({"fullname": "tY fRaNcE"}, [664034]),
    "alternate search key": (
        {"fullname": "France", "search_key": "lastName"},
        [664034],
    ),
    "no match": ({"fullname": "Nobody At All"}, []),
}
TEAM_ID_LOOKUPS = {
    "exact match": ({"team_name": "Athletics"}, [133]),
    "case-insensitive match": ({"team_name": "aThLeTiCs"}, [133]),
    "alternate search key": (
        {"team_name": "OAK", "search_key": "abbreviation"},
        [133],
    ),
    "no match": ({"team_name": "Nobody At All"}, []),
}

# The canned transport failures, per client. Each pair is the closest
# equivalent the two libraries offer, so the public exception is the only
# thing being compared.
SYNC_FAILURES = {
    "timeout": requests.exceptions.Timeout("timed out"),
    "transport": requests.exceptions.ConnectionError("connection refused"),
}
ASYNC_FAILURES = {
    "timeout": lambda request: httpx.ReadTimeout("timed out", request=request),
    "transport": lambda request: httpx.ConnectError(
        "connection refused", request=request
    ),
}

RequestSignature = tuple[str, str, dict[str, str]]


def request_signature(method: str, url: str) -> RequestSignature:
    """Normalize one observed request for transport-independent comparison."""
    parsed_url = urlsplit(url)
    return method, parsed_url.path, dict(parse_qsl(parsed_url.query))


def call_sync(
    method: str,
    *args,
    status: int = 200,
    payload: dict | None = None,
    raw_body: bytes | None = None,
    failure: str | None = None,
    mlb_options: dict | None = None,
    observed: list[RequestSignature] | None = None,
    **kwargs,
):
    """Call a method on `Mlb` against a canned response."""
    adapter = requests_mock.Adapter()
    if failure is not None:
        adapter.register_uri("GET", requests_mock.ANY, exc=SYNC_FAILURES[failure])
    else:
        body = {"content": raw_body} if raw_body is not None else {"json": payload}
        adapter.register_uri(
            "GET",
            requests_mock.ANY,
            status_code=status,
            reason=HTTPStatus(status).phrase,
            **body,
        )

    session = requests.Session()
    session.mount("https://", adapter)

    try:
        with Mlb(session=session, **(mlb_options or {})) as mlb:
            return getattr(mlb, method)(*args, **kwargs)
    finally:
        if observed is not None:
            observed.extend(
                request_signature(request.method, request.url)
                for request in adapter.request_history
            )
        # Mlb leaves a caller-injected session open, so closing it is this
        # helper's job.
        session.close()


def call_async(
    method: str,
    *args,
    status: int = 200,
    payload: dict | None = None,
    raw_body: bytes | None = None,
    failure: str | None = None,
    mlb_options: dict | None = None,
    observed: list[RequestSignature] | None = None,
    **kwargs,
):
    """Call the matching method on `AsyncMlb` against the same canned response."""
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if failure is not None:
            raise ASYNC_FAILURES[failure](request)
        if raw_body is not None:
            return httpx.Response(status, content=raw_body)
        return httpx.Response(status, json=payload)

    async def scenario():
        client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        try:
            async with AsyncMlb(client=client, **(mlb_options or {})) as mlb:
                return await getattr(mlb, method)(*args, **kwargs)
        finally:
            # AsyncMlb leaves a caller-injected client open, as Mlb does above.
            await client.aclose()

    try:
        return asyncio.run(scenario())
    finally:
        if observed is not None:
            observed.extend(
                request_signature(request.method, str(request.url))
                for request in seen
            )


@dataclass(frozen=True)
class ParityResult:
    """What each client returned, plus the one request they both sent."""

    sync: Any
    asynchronous: Any
    request: RequestSignature


def call_both(method: str, *args, **kwargs) -> ParityResult:
    """Drive both public clients over one canned response.

    Each client is handed an equivalent response through its own public
    constructor, so a failure below names the side that drifted. Request
    parity is asserted here rather than per test, which also rules out a
    client that quietly fanned one call out into several.
    """
    sync_requests: list[RequestSignature] = []
    async_requests: list[RequestSignature] = []

    sync_result = call_sync(method, *args, observed=sync_requests, **kwargs)
    async_result = call_async(method, *args, observed=async_requests, **kwargs)

    assert len(sync_requests) == 1, f"sync sent {len(sync_requests)} requests"
    assert async_requests == sync_requests, "the clients sent different requests"

    return ParityResult(sync_result, async_result, sync_requests[0])


def raise_both(expected: type[BaseException], method: str, *args, **kwargs):
    """Return the exception each client raised for one canned failure."""
    with pytest.raises(expected) as sync_exc:
        call_sync(method, *args, **kwargs)
    with pytest.raises(expected) as async_exc:
        call_async(method, *args, **kwargs)

    # pytest.raises accepts subclasses, so pin the exact type on both sides:
    # MlbTimeoutError is itself an MlbTransportError.
    assert type(sync_exc.value) is type(async_exc.value) is expected

    return sync_exc.value, async_exc.value


# ---------------------------------------------------------------------------
# Successful responses
# ---------------------------------------------------------------------------


def test_get_team_success_parity():
    """A successful team response parses to the same Team on both clients."""
    result = call_both("get_team", 133, payload=TEAM_PAYLOAD)

    assert isinstance(result.sync, Team), "sync get_team did not return a Team"
    assert (result.sync.id, result.sync.link, result.sync.name) == (
        133,
        "/api/v1/teams/133",
        "Athletics",
    )
    # Pydantic equality compares the model class too, so this pins the async
    # return type as well as every parsed field.
    assert result.asynchronous == result.sync
    assert result.request == ("GET", "/api/v1/teams/133", {})


def test_get_person_success_parity():
    """A successful person response parses to the same Person on both clients."""
    result = call_both("get_person", 660271, payload=PERSON_PAYLOAD)

    assert isinstance(result.sync, Person), "sync get_person did not return a Person"
    assert (result.sync.id, result.sync.link, result.sync.full_name) == (
        660271,
        "/api/v1/people/660271",
        "Shohei Ohtani",
    )
    assert result.asynchronous == result.sync
    assert result.request == ("GET", "/api/v1/people/660271", {})


def test_get_persons_success_parity():
    """A successful people response parses to the same People on both clients."""
    result = call_both("get_persons", "660271,664034", payload=PEOPLE_PAYLOAD)

    assert all(isinstance(person, Person) for person in result.sync), (
        "sync get_persons did not return People"
    )
    assert [(person.id, person.full_name) for person in result.sync] == [
        (660271, "Shohei Ohtani"),
        (664034, "Ty France"),
    ]
    assert result.asynchronous == result.sync
    assert result.request == (
        "GET",
        "/api/v1/people",
        {"personIds": "660271,664034"},
    )


def test_get_persons_id_list_request_parity():
    """A list of person ids produces equivalent requests on both clients."""
    result = call_both("get_persons", [660271, 664034], payload=PEOPLE_PAYLOAD)

    assert result.asynchronous == result.sync
    # Both clients repeat the query pair rather than joining the ids, and
    # `request_signature` keeps the last value of a repeated pair. `call_both`
    # has already compared the two full query strings.
    assert result.request == ("GET", "/api/v1/people", {"personIds": "664034"})


@pytest.mark.parametrize("label", list(PEOPLE_ID_LOOKUPS))
def test_get_people_id_lookup_parity(label):
    """Each lookup answers with the same person ids on either client."""
    kwargs, expected = PEOPLE_ID_LOOKUPS[label]
    result = call_both("get_people_id", payload=PEOPLE_LOOKUP_PAYLOAD, **kwargs)

    assert result.sync == expected, f"sync get_people_id returned {result.sync!r}"
    assert result.asynchronous == result.sync
    assert result.request == (
        "GET",
        "/api/v1/sports/1/players",
        {"fields": "people,id,fullName"},
    )


@pytest.mark.parametrize("label", list(TEAM_ID_LOOKUPS))
def test_get_team_id_lookup_parity(label):
    """Each lookup answers with the same team ids on either client."""
    kwargs, expected = TEAM_ID_LOOKUPS[label]
    result = call_both("get_team_id", payload=TEAMS_LOOKUP_PAYLOAD, **kwargs)

    assert result.sync == expected, f"sync get_team_id returned {result.sync!r}"
    assert result.asynchronous == result.sync
    assert result.request == (
        "GET",
        "/api/v1/teams",
        {"fields": "teams,id,name"},
    )


def test_get_schedule_success_parity():
    """A successful date schedule parses identically and sends the same request."""
    result = call_both("get_schedule", date="2022-10-07", payload=SCHEDULE_PAYLOAD)

    assert isinstance(result.sync, Schedule), "sync get_schedule did not return a Schedule"
    assert (
        result.sync.total_items,
        result.sync.total_games,
        result.sync.dates[0].date,
        result.sync.dates[0].total_games,
    ) == (1, 1, "2022-10-07", 1)
    assert result.asynchronous == result.sync
    assert result.request == (
        "GET",
        "/api/v1/schedule",
        {"date": "2022-10-07", "sportId": "1"},
    )


def test_get_schedule_range_team_and_sport_request_parity():
    """A date range, team, and non-default sport produce equivalent requests."""
    result = call_both(
        "get_schedule",
        start_date="2022-10-07",
        end_date="2022-10-09",
        team_id=133,
        sport_id=11,
        payload=SCHEDULE_PAYLOAD,
    )

    assert result.asynchronous == result.sync
    assert result.request == (
        "GET",
        "/api/v1/schedule",
        {
            "startDate": "2022-10-07",
            "endDate": "2022-10-09",
            "teamId": "133",
            "sportId": "11",
        },
    )


# ---------------------------------------------------------------------------
# Nothing to return
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_team_no_result_parity(label):
    """Every no-result response returns None on either client."""
    result = call_both("get_team", 133, **NO_RESULT_RESPONSES[label])

    assert result.sync is None, f"sync get_team returned {result.sync!r} for {label}"
    assert result.asynchronous is None, (
        f"async get_team returned {result.asynchronous!r} for {label}"
    )


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_person_no_result_parity(label):
    """Every no-result response returns None on either client."""
    result = call_both("get_person", 660271, **NO_RESULT_RESPONSES[label])

    assert result.sync is None, f"sync get_person returned {result.sync!r} for {label}"
    assert result.asynchronous is None, (
        f"async get_person returned {result.asynchronous!r} for {label}"
    )


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_persons_no_result_parity(label):
    """Every no-result response returns an empty list on either client."""
    result = call_both("get_persons", "660271", **NO_RESULT_RESPONSES[label])

    assert result.sync == [], f"sync get_persons returned {result.sync!r} for {label}"
    assert result.asynchronous == result.sync


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_people_id_no_result_parity(label):
    """Every no-result response returns an empty list on either client."""
    result = call_both("get_people_id", "Ty France", **NO_RESULT_RESPONSES[label])

    assert result.sync == [], f"sync get_people_id returned {result.sync!r} for {label}"
    assert result.asynchronous == result.sync


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_team_id_no_result_parity(label):
    """Every no-result response returns an empty list on either client."""
    result = call_both("get_team_id", "Athletics", **NO_RESULT_RESPONSES[label])

    assert result.sync == [], f"sync get_team_id returned {result.sync!r} for {label}"
    assert result.asynchronous == result.sync


@pytest.mark.parametrize("label", list(SCHEDULE_NO_RESULT_RESPONSES))
def test_get_schedule_no_result_parity(label):
    """Every no-result response returns None on either client."""
    result = call_both(
        "get_schedule", date="2022-10-07", **SCHEDULE_NO_RESULT_RESPONSES[label]
    )

    assert result.sync is None, f"sync get_schedule returned {result.sync!r} for {label}"
    assert result.asynchronous is None, (
        f"async get_schedule returned {result.asynchronous!r} for {label}"
    )


# ---------------------------------------------------------------------------
# Representative public failure behavior (get_team)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "status, reason",
    [
        # A final non-404 4xx under the strict_http default, and one
        # representative 5xx.
        (403, "Forbidden"),
        (500, "Internal Server Error"),
    ],
)
def test_get_team_http_error_parity(status, reason):
    """Both clients expose the same stable public HTTP error context."""
    payload = {"message": "no"}

    sync_error, async_error = raise_both(
        MlbHttpError, "get_team", 133, status=status, payload=payload
    )

    expected = (
        status,
        reason,
        "GET",
        "https://statsapi.mlb.com/api/v1/teams/133",
        payload,
    )
    attributes = ("status_code", "reason", "method", "url", "response_data")
    assert tuple(getattr(sync_error, name) for name in attributes) == expected
    assert tuple(getattr(async_error, name) for name in attributes) == expected


def test_get_team_compatibility_client_error_parity():
    """Compatibility mode warns and returns None on both public clients."""
    response = {
        "status": 403,
        "payload": {"message": "access denied"},
        "mlb_options": {"strict_http": False},
    }

    with pytest.warns(MlbHttpCompatibilityWarning) as sync_warnings:
        sync_team = call_sync("get_team", 133, **response)
    with pytest.warns(MlbHttpCompatibilityWarning) as async_warnings:
        async_team = call_async("get_team", 133, **response)

    assert sync_team is None
    assert async_team is None
    assert len(sync_warnings) == len(async_warnings) == 1


@pytest.mark.parametrize(
    "failure, expected",
    [
        ("timeout", MlbTimeoutError),
        ("transport", MlbTransportError),
    ],
)
def test_get_team_transport_failure_parity(failure, expected):
    """A deterministic transport failure raises the same exception on both."""
    raise_both(expected, "get_team", 133, failure=failure)


def test_get_team_invalid_json_parity():
    """Invalid JSON in a successful response raises on both public clients."""
    raise_both(MlbDecodeError, "get_team", 133, raw_body=b'{"teams": [')
