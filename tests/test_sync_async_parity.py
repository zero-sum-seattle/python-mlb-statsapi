"""Sync/async behavioral parity tests (issue #304, batch 1).

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

import pytest
import requests
import requests_mock

# The async client needs the optional HTTPX extra; without it there is no
# async side to compare against, so the whole module is skipped rather than
# failing a sync-only install at import time.
httpx = pytest.importorskip("httpx", reason="requires the async extra (HTTPX)")

from mlbstatsapi import Mlb  # noqa: E402
from mlbstatsapi.async_mlb import AsyncMlb  # noqa: E402
from mlbstatsapi.models.people import Person  # noqa: E402
from mlbstatsapi.models.teams import Team  # noqa: E402


TEAM_PAYLOAD = {"teams": [{"id": 133, "link": "/api/v1/teams/133", "name": "Athletics"}]}
PERSON_PAYLOAD = {
    "people": [{"id": 660271, "link": "/api/v1/people/660271", "fullName": "Shohei Ohtani"}]
}

# The two ways a call legitimately comes back with nothing to parse. Both
# clients are expected to answer None for get_team and get_person.
NO_RESULT_RESPONSES = {
    "empty 200": (200, {}),
    "404": (404, {}),
}


def call_sync(method: str, *args, status: int, payload: dict, **kwargs):
    """Call a method on `Mlb` against a canned response."""
    adapter = requests_mock.Adapter()
    adapter.register_uri("GET", requests_mock.ANY, status_code=status, json=payload)

    session = requests.Session()
    session.mount("https://", adapter)

    try:
        with Mlb(session=session) as mlb:
            return getattr(mlb, method)(*args, **kwargs)
    finally:
        session.close()


def call_async(method: str, *args, status: int, payload: dict, **kwargs):
    """Call the matching method on `AsyncMlb` against the same canned response."""
    client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(status, json=payload))
    )

    async def scenario():
        try:
            async with AsyncMlb(client=client) as mlb:
                return await getattr(mlb, method)(*args, **kwargs)
        finally:
            await client.aclose()

    return asyncio.run(scenario())


def call_both(method: str, *args, status: int = 200, payload: dict, **kwargs):
    """Return the sync and async results for one call, in that order.

    Both clients are handed an equivalent response through their own public
    constructor, so a failure below names the side that drifted.
    """
    return (
        call_sync(method, *args, status=status, payload=payload, **kwargs),
        call_async(method, *args, status=status, payload=payload, **kwargs),
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
