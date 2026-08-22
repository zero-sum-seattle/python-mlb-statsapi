"""Sync/async behavioral parity tests (issue #304, batches 1-2).

`Mlb` is the compatibility baseline. These tests prove that `AsyncMlb`'s
public endpoint behavior stays aligned with it: the same response produces the
same model type, the same parsed values, and the same "nothing to return"
answer.

The scope is deliberately narrow. Transport behavior — retries, timeouts,
strict-mode status mapping, exception translation — is already covered by
tests/test_http_contract.py, tests/test_mlb_dataadapter.py and
tests/test_async_mlb_dataadapter.py, and payload parsing by tests/parsers/.
None of that is re-asserted here, and nothing compares Requests internals with
HTTPX internals. Each test drives both public clients over an equivalent canned
response and compares only what a caller can see.

These tests must not contact the live MLB API.
"""

from __future__ import annotations

import asyncio
from urllib.parse import parse_qsl, urlsplit

import pytest
import requests
import requests_mock

# The async client needs the optional HTTPX extra; without it there is no
# async side to compare against, so the whole module is skipped rather than
# failing a sync-only install at import time.
httpx = pytest.importorskip("httpx", reason="requires the async extra (HTTPX)")

from mlbstatsapi import AsyncMlb, Mlb  # noqa: E402
from mlbstatsapi.models.people import Person  # noqa: E402
from mlbstatsapi.models.schedules import Schedule  # noqa: E402
from mlbstatsapi.models.teams import Team  # noqa: E402


TEAM_PAYLOAD = {"teams": [{"id": 133, "link": "/api/v1/teams/133", "name": "Athletics"}]}
PERSON_PAYLOAD = {
    "people": [{"id": 660271, "link": "/api/v1/people/660271", "fullName": "Shohei Ohtani"}]
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

# The two ways a call legitimately comes back with nothing to parse. Both
# clients are expected to answer None for get_team and get_person.
NO_RESULT_RESPONSES = {
    "empty 200": (200, {}),
    "404": (404, {}),
}
SCHEDULE_NO_RESULT_RESPONSES = {
    "empty 200": (
        200,
        {
            "totalItems": 0,
            "totalEvents": 0,
            "totalGames": 0,
            "totalGamesInProgress": 0,
            "dates": [],
        },
    ),
    "404": (404, {}),
}


def request_signature(method: str, url: str) -> tuple[str, str, dict[str, str]]:
    """Normalize one observed request for transport-independent comparison."""
    parsed_url = urlsplit(url)
    return method, parsed_url.path, dict(parse_qsl(parsed_url.query))


def call_sync(
    method: str,
    *args,
    status: int,
    payload: dict,
    request_signatures: list[tuple[str, str, dict[str, str]]] | None = None,
    **kwargs,
):
    """Call a method on `Mlb` against a canned response."""
    adapter = requests_mock.Adapter()
    adapter.register_uri("GET", requests_mock.ANY, status_code=status, json=payload)

    session = requests.Session()
    session.mount("https://", adapter)

    try:
        with Mlb(session=session) as mlb:
            result = getattr(mlb, method)(*args, **kwargs)

        if request_signatures is not None:
            assert len(adapter.request_history) == 1
            request = adapter.request_history[0]
            request_signatures.append(request_signature(request.method, request.url))

        return result
    finally:
        session.close()


def call_async(
    method: str,
    *args,
    status: int,
    payload: dict,
    request_signatures: list[tuple[str, str, dict[str, str]]] | None = None,
    **kwargs,
):
    """Call the matching method on `AsyncMlb` against the same canned response."""
    requests_seen = []

    def handler(request):
        requests_seen.append(request)
        return httpx.Response(status, json=payload)

    client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler)
    )

    async def scenario():
        try:
            async with AsyncMlb(client=client) as mlb:
                return await getattr(mlb, method)(*args, **kwargs)
        finally:
            await client.aclose()

    result = asyncio.run(scenario())

    if request_signatures is not None:
        assert len(requests_seen) == 1
        request = requests_seen[0]
        request_signatures.append(request_signature(request.method, str(request.url)))

    return result


def call_both(
    method: str,
    *args,
    status: int = 200,
    payload: dict,
    request_signatures: list[tuple[str, str, dict[str, str]]] | None = None,
    **kwargs,
):
    """Return the sync and async results for one call, in that order.

    Both clients are handed an equivalent response through their own public
    constructor, so a failure below names the side that drifted.
    """
    return (
        call_sync(
            method,
            *args,
            status=status,
            payload=payload,
            request_signatures=request_signatures,
            **kwargs,
        ),
        call_async(
            method,
            *args,
            status=status,
            payload=payload,
            request_signatures=request_signatures,
            **kwargs,
        ),
    )


# ---------------------------------------------------------------------------
# get_team
# ---------------------------------------------------------------------------


def test_get_team_success_parity():
    """A successful team response parses to the same Team on both clients."""
    sync_team, async_team = call_both("get_team", 133, payload=TEAM_PAYLOAD)

    assert isinstance(sync_team, Team), "sync get_team did not return a Team"
    assert isinstance(async_team, Team), "async get_team did not return a Team"

    expected = (133, "/api/v1/teams/133", "Athletics")
    assert (sync_team.id, sync_team.link, sync_team.name) == expected
    assert (async_team.id, async_team.link, async_team.name) == expected
    assert async_team == sync_team


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_team_no_result_parity(label):
    """An empty success and a 404 both return None on either client."""
    status, payload = NO_RESULT_RESPONSES[label]

    sync_team, async_team = call_both("get_team", 133, status=status, payload=payload)

    assert sync_team is None, f"sync get_team returned {sync_team!r} for {label}"
    assert async_team is None, f"async get_team returned {async_team!r} for {label}"


# ---------------------------------------------------------------------------
# get_person
# ---------------------------------------------------------------------------


def test_get_person_success_parity():
    """A successful person response parses to the same Person on both clients."""
    sync_person, async_person = call_both("get_person", 660271, payload=PERSON_PAYLOAD)

    assert isinstance(sync_person, Person), "sync get_person did not return a Person"
    assert isinstance(async_person, Person), "async get_person did not return a Person"

    expected = (660271, "/api/v1/people/660271", "Shohei Ohtani")
    assert (sync_person.id, sync_person.link, sync_person.full_name) == expected
    assert (async_person.id, async_person.link, async_person.full_name) == expected
    assert async_person == sync_person


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_person_no_result_parity(label):
    """An empty success and a 404 both return None on either client."""
    status, payload = NO_RESULT_RESPONSES[label]

    sync_person, async_person = call_both(
        "get_person", 660271, status=status, payload=payload
    )

    assert sync_person is None, f"sync get_person returned {sync_person!r} for {label}"
    assert async_person is None, f"async get_person returned {async_person!r} for {label}"


# ---------------------------------------------------------------------------
# get_schedule
# ---------------------------------------------------------------------------


def test_get_schedule_success_parity():
    """A successful date schedule parses identically and sends the same request."""
    requests_seen = []

    sync_schedule, async_schedule = call_both(
        "get_schedule",
        date="2022-10-07",
        payload=SCHEDULE_PAYLOAD,
        request_signatures=requests_seen,
    )

    assert isinstance(sync_schedule, Schedule), "sync get_schedule did not return a Schedule"
    assert isinstance(async_schedule, Schedule), "async get_schedule did not return a Schedule"

    expected = (1, 1, "2022-10-07", 1)
    assert (
        sync_schedule.total_items,
        sync_schedule.total_games,
        sync_schedule.dates[0].date,
        sync_schedule.dates[0].total_games,
    ) == expected
    assert (
        async_schedule.total_items,
        async_schedule.total_games,
        async_schedule.dates[0].date,
        async_schedule.dates[0].total_games,
    ) == expected
    assert async_schedule == sync_schedule

    expected_request = (
        "GET",
        "/api/v1/schedule",
        {"date": "2022-10-07", "sportId": "1"},
    )
    assert requests_seen == [expected_request, expected_request]


@pytest.mark.parametrize("label", list(SCHEDULE_NO_RESULT_RESPONSES))
def test_get_schedule_no_result_parity(label):
    """An empty success and a 404 both return None on either client."""
    status, payload = SCHEDULE_NO_RESULT_RESPONSES[label]

    sync_schedule, async_schedule = call_both(
        "get_schedule",
        date="2022-10-07",
        status=status,
        payload=payload,
    )

    assert sync_schedule is None, f"sync get_schedule returned {sync_schedule!r} for {label}"
    assert async_schedule is None, f"async get_schedule returned {async_schedule!r} for {label}"


def test_get_schedule_range_team_and_sport_request_parity():
    """A date range, team, and non-default sport produce equivalent requests."""
    requests_seen = []

    sync_schedule, async_schedule = call_both(
        "get_schedule",
        start_date="2022-10-07",
        end_date="2022-10-09",
        team_id=133,
        sport_id=11,
        payload=SCHEDULE_PAYLOAD,
        request_signatures=requests_seen,
    )

    assert async_schedule == sync_schedule
    expected_request = (
        "GET",
        "/api/v1/schedule",
        {
            "startDate": "2022-10-07",
            "endDate": "2022-10-09",
            "teamId": "133",
            "sportId": "11",
        },
    )
    assert requests_seen == [expected_request, expected_request]
