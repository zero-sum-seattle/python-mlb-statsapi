"""Focused offline tests for the AsyncMlb client (issue #303).

Covers what the vertical slice actually promises: the package-root import, the
async context-manager and cleanup contract, and — for each endpoint on the
client — the request it builds and the parsed value it returns.

AsyncMlb is deliberately thin: HTTP behavior belongs to AsyncMlbDataAdapter and
is asserted in tests/test_async_mlb_dataadapter.py, with the exhaustive
transport-contract matrix in #302. Nothing here re-tests retries, status
mapping, timeouts, or exception translation. What is tested here instead is
that the client hands the adapter the right endpoint and params, hands the
response to the shared parsers, and adds nothing of its own between the two.

The endpoint tests therefore drive the real adapter over an
``httpx.MockTransport`` rather than mocking the adapter away, so an endpoint
that stopped producing a real HTTP request would fail rather than pass against
a mock. Request construction is additionally pinned to the synchronous client
in test_request_construction_matches_sync_client, because the async surface is
only correct insofar as it matches ``Mlb``.

These tests must not contact the live MLB API.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

# The endpoint tests drive the real HTTPX-backed adapter, so a sync-only
# install has nothing here to run. Skipping at collection keeps
# ``pytest tests/`` working without the ``async`` extra instead of erroring on
# the import, matching tests/test_async_mlb_dataadapter.py.
httpx = pytest.importorskip("httpx", reason="requires the async extra (HTTPX)")

from mlbstatsapi.async_mlb import AsyncMlb  # noqa: E402
from mlbstatsapi.models.people import Person  # noqa: E402
from mlbstatsapi.models.schedules import Schedule  # noqa: E402
from mlbstatsapi.models.teams import Team  # noqa: E402


# Patched only while a client is constructed, so AsyncMlb builds its own
# adapter and client through the production path and only the transport is
# swapped. Mirrors tests/test_async_mlb_dataadapter.py.
CLIENT_TARGET = "mlbstatsapi.async_mlb_dataadapter.httpx.AsyncClient"

# Failure guard for the concurrency test: a request that should never wait is
# bounded so a serializing regression fails fast instead of hanging CI.
BLOCKED_REQUEST_TIMEOUT = 10

TEAM_PAYLOAD = {"teams": [{"id": 133, "link": "/api/v1/teams/133", "name": "Athletics"}]}
TEAMS_PAYLOAD = {
    "teams": [
        {"id": 133, "link": "/api/v1/teams/133", "name": "Athletics"},
        {"id": 134, "link": "/api/v1/teams/134", "name": "Team 134"},
    ]
}
PERSON_PAYLOAD = {
    "people": [{"id": 660271, "link": "/api/v1/people/660271", "fullName": "Shohei Ohtani"}]
}
PEOPLE_PAYLOAD = {
    "people": [
        {"id": 660271, "link": "/api/v1/people/660271", "fullName": "Shohei Ohtani"},
        {"id": 605151, "link": "/api/v1/people/605151", "fullName": "Person 605151"},
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


# Clients built by _owned_client(); run_async() closes them inside the same
# event loop that used them, so no AsyncClient is left open by a test.
_CLIENTS_TO_CLOSE: list[AsyncMlb] = []


def run_async(coro):
    async def runner():
        try:
            return await coro
        finally:
            while _CLIENTS_TO_CLOSE:
                await _CLIENTS_TO_CLOSE.pop().aclose()

    return asyncio.run(runner())


class _RecordingHandler:
    """Serve one response per endpoint path and record every request seen."""

    def __init__(self, responses: dict[str, httpx.Response] | httpx.Response):
        self._responses = responses
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if isinstance(self._responses, httpx.Response):
            return self._responses
        # Keyed by the path after ``/api/v1/``, e.g. "teams/133".
        endpoint = request.url.path.split("/api/v1/", 1)[-1]
        return self._responses[endpoint]

    @property
    def call_count(self) -> int:
        return len(self.requests)

    def params_for(self, endpoint: str) -> dict[str, str]:
        for request in self.requests:
            if request.url.path.endswith(endpoint):
                return dict(request.url.params)
        raise AssertionError(f"no request was made to {endpoint!r}")


def _owned_client(handler, **kwargs) -> AsyncMlb:
    """Build an AsyncMlb that owns its client, over a MockTransport.

    Call this from inside a run_async() scenario; run_async() closes what it
    creates.
    """
    real_async_client = httpx.AsyncClient

    def mock_transport_client(**client_kwargs) -> httpx.AsyncClient:
        return real_async_client(
            transport=httpx.MockTransport(handler),
            **client_kwargs,
        )

    with patch(CLIENT_TARGET, mock_transport_client):
        mlb = AsyncMlb(**kwargs)

    _CLIENTS_TO_CLOSE.append(mlb)
    return mlb


def _json(payload: dict) -> httpx.Response:
    return httpx.Response(200, json=payload)


# ---------------------------------------------------------------------------
# Package-root import
# ---------------------------------------------------------------------------


def test_async_mlb_is_importable_from_the_package_root():
    """AsyncMlb is reachable as ``from mlbstatsapi import AsyncMlb``.

    It resolves through the package-root lazy __getattr__, so this also proves
    the lazy async export still works and is the same class the module exposes.
    """
    from mlbstatsapi import AsyncMlb as RootAsyncMlb

    assert RootAsyncMlb is AsyncMlb


def test_async_mlb_is_advertised_by_package_dir():
    """dir(mlbstatsapi) advertises the lazily exported async names."""
    import mlbstatsapi

    assert "AsyncMlb" in dir(mlbstatsapi)
    assert "AsyncMlbDataAdapter" in dir(mlbstatsapi)


# ---------------------------------------------------------------------------
# Lifecycle: context manager, cleanup, cancellation, ownership
# ---------------------------------------------------------------------------


def test_async_mlb_context_manager_returns_self():
    async def scenario():
        mlb = AsyncMlb()

        async with mlb as entered:
            assert entered is mlb

        return mlb

    run_async(scenario())


def test_async_mlb_aclose_delegates_to_adapter():
    async def scenario():
        mlb = AsyncMlb()

        mlb._mlb_adapter_v1.aclose = AsyncMock()

        await mlb.aclose()

        mlb._mlb_adapter_v1.aclose.assert_awaited_once()

    run_async(scenario())


def test_async_mlb_context_manager_closes_on_normal_exit():
    async def scenario():
        mlb = AsyncMlb()

        mlb._mlb_adapter_v1.aclose = AsyncMock()

        async with mlb:
            pass

        mlb._mlb_adapter_v1.aclose.assert_awaited_once()

    run_async(scenario())


def test_async_mlb_context_manager_closes_when_body_raises():
    async def scenario():
        mlb = AsyncMlb()

        mlb._mlb_adapter_v1.aclose = AsyncMock()

        with pytest.raises(ValueError, match="boom"):
            async with mlb:
                raise ValueError("boom")

        mlb._mlb_adapter_v1.aclose.assert_awaited_once()

    run_async(scenario())


def test_async_mlb_preserves_original_exception_if_cleanup_fails():
    async def scenario():
        mlb = AsyncMlb()

        mlb._mlb_adapter_v1.aclose = AsyncMock(
            side_effect=RuntimeError("cleanup failed")
        )

        with pytest.raises(ValueError, match="original"):
            async with mlb:
                raise ValueError("original")

    run_async(scenario())


def test_async_mlb_cleanup_failure_raises_when_no_original_exception():
    async def scenario():
        mlb = AsyncMlb()

        mlb._mlb_adapter_v1.aclose = AsyncMock(
            side_effect=RuntimeError("cleanup failed")
        )

        with pytest.raises(RuntimeError, match="cleanup failed"):
            async with mlb:
                pass

    run_async(scenario())


def test_async_mlb_preserves_cancellation_during_cleanup():
    async def scenario():
        mlb = AsyncMlb()

        mlb._mlb_adapter_v1.aclose = AsyncMock()

        async def worker():
            async with mlb:
                await asyncio.sleep(60)

        task = asyncio.create_task(worker())

        await asyncio.sleep(0)
        task.cancel()

        with pytest.raises(asyncio.CancelledError):
            await task

        mlb._mlb_adapter_v1.aclose.assert_awaited_once()

    run_async(scenario())


def test_async_mlb_closes_the_client_it_owns():
    """Exiting the context manager really closes the underlying HTTPX client."""
    handler = _RecordingHandler(_json(TEAM_PAYLOAD))

    async def scenario():
        mlb = _owned_client(handler)
        client = mlb._mlb_adapter_v1._client

        async with mlb:
            await mlb.get_team(133)

        assert client.is_closed

    run_async(scenario())


def test_async_mlb_leaves_a_caller_injected_client_open():
    """A client the caller supplied is the caller's to close, not the library's.

    AsyncMlb must pass ownership through to the adapter unchanged: closing an
    injected client would break a caller reusing it for its own requests after
    the ``async with`` block.
    """
    handler = _RecordingHandler(_json(TEAM_PAYLOAD))
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))

    async def scenario():
        mlb = AsyncMlb(client=client)

        assert mlb._mlb_adapter_v1._owns_client is False

        async with mlb:
            await mlb.get_team(133)

        assert client.is_closed is False

        # Still usable afterwards, which is the point of injecting it.
        await client.get("https://statsapi.mlb.com/api/v1/teams/133")

        await client.aclose()

    run_async(scenario())


def test_async_mlb_cleanup_is_idempotent():
    """Repeated cleanup is safe, however the caller mixes the two forms."""
    handler = _RecordingHandler(_json(TEAM_PAYLOAD))

    async def scenario():
        mlb = _owned_client(handler)

        async with mlb:
            await mlb.get_team(133)

        # Already closed by __aexit__; neither of these may raise.
        await mlb.aclose()
        await mlb.aclose()

        async with mlb:
            pass

    run_async(scenario())


# ---------------------------------------------------------------------------
# Endpoints: request construction and parsed results
# ---------------------------------------------------------------------------


def test_get_team_requests_the_team_endpoint_and_parses_the_result():
    handler = _RecordingHandler(_json(TEAM_PAYLOAD))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_team(133, season="2022")

    team = run_async(scenario())

    assert handler.call_count == 1
    assert handler.requests[0].url.path == "/api/v1/teams/133"
    assert handler.params_for("teams/133") == {"season": "2022"}
    assert team == Team(id=133, link="/api/v1/teams/133", name="Athletics")


def test_get_team_returns_none_for_an_unknown_team():
    """A 404 is the adapter's empty result, which the client turns into None."""
    handler = _RecordingHandler(httpx.Response(404, json={}))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_team(1)

    assert run_async(scenario()) is None


def test_get_team_returns_none_for_an_empty_payload():
    """An empty 200 body has no team to parse, so there is no Team to return."""
    handler = _RecordingHandler(_json({"teams": []}))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_team(133)

    assert run_async(scenario()) is None


def test_get_teams_sends_sport_id_and_parses_every_team():
    """get_teams defaults to sportId=1 and promotes sport_id into the query."""
    handler = _RecordingHandler(_json(TEAMS_PAYLOAD))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_teams()

    teams = run_async(scenario())

    assert handler.params_for("teams") == {"sportId": "1"}
    assert teams == [
        Team(id=133, link="/api/v1/teams/133", name="Athletics"),
        Team(id=134, link="/api/v1/teams/134", name="Team 134"),
    ]


def test_get_teams_passes_an_explicit_sport_id_and_extra_params():
    handler = _RecordingHandler(_json({"teams": []}))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_teams(11, season="2021")

    teams = run_async(scenario())

    assert handler.params_for("teams") == {"sportId": "11", "season": "2021"}
    assert teams == []


def test_get_teams_returns_empty_list_for_an_unknown_sport():
    handler = _RecordingHandler(httpx.Response(404, json={}))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_teams(999)

    assert run_async(scenario()) == []


def test_get_person_requests_the_people_endpoint_and_parses_the_result():
    handler = _RecordingHandler(_json(PERSON_PAYLOAD))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_person(660271, hydrate="currentTeam")

    person = run_async(scenario())

    assert handler.call_count == 1
    assert handler.requests[0].url.path == "/api/v1/people/660271"
    assert handler.params_for("people/660271") == {"hydrate": "currentTeam"}
    assert person == Person(
        id=660271, link="/api/v1/people/660271", full_name="Shohei Ohtani"
    )


def test_get_person_returns_none_for_an_unknown_person():
    handler = _RecordingHandler(httpx.Response(404, json={}))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_person(1)

    assert run_async(scenario()) is None


def test_get_person_returns_none_for_an_empty_payload():
    handler = _RecordingHandler(_json({"people": []}))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_person(660271)

    assert run_async(scenario()) is None


def test_get_people_requests_the_sport_players_endpoint():
    """get_people reads sports/{sport_id}/players, exactly like Mlb.get_people.

    The sport id goes in the path, not the query, which is what separates this
    endpoint from get_persons' ``people?personIds=`` form.
    """
    handler = _RecordingHandler(_json(PEOPLE_PAYLOAD))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_people()

    people = run_async(scenario())

    assert handler.requests[0].url.path == "/api/v1/sports/1/players"
    assert handler.params_for("sports/1/players") == {}
    assert people == [
        Person(id=660271, link="/api/v1/people/660271", full_name="Shohei Ohtani"),
        Person(id=605151, link="/api/v1/people/605151", full_name="Person 605151"),
    ]


def test_get_people_passes_an_explicit_sport_id_and_extra_params():
    handler = _RecordingHandler(_json({"people": []}))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_people(11, season="2021")

    people = run_async(scenario())

    assert handler.requests[0].url.path == "/api/v1/sports/11/players"
    assert handler.params_for("sports/11/players") == {"season": "2021"}
    assert people == []


def test_get_people_returns_empty_list_for_an_unknown_sport():
    handler = _RecordingHandler(httpx.Response(404, json={}))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_people(999)

    assert run_async(scenario()) == []


def test_get_schedule_sends_date_and_sport_id_and_parses_the_result():
    handler = _RecordingHandler(_json(SCHEDULE_PAYLOAD))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_schedule(date="2022-10-07")

    schedule = run_async(scenario())

    assert handler.requests[0].url.path == "/api/v1/schedule"
    assert handler.params_for("schedule") == {"date": "2022-10-07", "sportId": "1"}
    assert isinstance(schedule, Schedule)
    assert schedule == Schedule(**SCHEDULE_PAYLOAD)


def test_get_schedule_sends_a_date_range_and_team_id():
    handler = _RecordingHandler(_json(SCHEDULE_PAYLOAD))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_schedule(
            start_date="2021-08-01",
            end_date="2021-08-11",
            team_id=133,
        )

    run_async(scenario())

    assert handler.params_for("schedule") == {
        "startDate": "2021-08-01",
        "endDate": "2021-08-11",
        "teamId": "133",
        "sportId": "1",
    }


def test_get_schedule_allows_game_pks_without_a_date():
    """gamePks is the one way to ask for a schedule with no date at all."""
    handler = _RecordingHandler(_json(SCHEDULE_PAYLOAD))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_schedule(gamePks=531493)

    run_async(scenario())

    assert handler.params_for("schedule") == {"gamePks": "531493", "sportId": "1"}


def test_get_schedule_without_dates_or_game_pks_makes_no_request():
    """An unanswerable schedule request returns None without touching the API."""
    handler = _RecordingHandler(_json(SCHEDULE_PAYLOAD))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_schedule()

    assert run_async(scenario()) is None
    assert handler.call_count == 0


def test_get_schedule_returns_none_for_an_unknown_schedule():
    handler = _RecordingHandler(httpx.Response(404, json={}))

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_schedule(date="2022-10-07")

    assert run_async(scenario()) is None


def test_get_schedule_returns_none_when_no_games_are_scheduled():
    """An empty ``dates`` list is a valid 200 that parses to no Schedule."""
    handler = _RecordingHandler(
        _json(
            {
                "totalItems": 0,
                "totalEvents": 0,
                "totalGames": 0,
                "totalGamesInProgress": 0,
                "dates": [],
            }
        )
    )

    async def scenario():
        mlb = _owned_client(handler)
        return await mlb.get_schedule(date="2022-12-25")

    assert run_async(scenario()) is None


# ---------------------------------------------------------------------------
# Parity with the synchronous client
# ---------------------------------------------------------------------------


SYNC_PARITY_CASES = [
    ("get_team", (133,), {}),
    ("get_team", (133,), {"season": "2022"}),
    ("get_teams", (), {}),
    ("get_teams", (11,), {"season": "2021"}),
    ("get_person", (660271,), {}),
    ("get_people", (), {}),
    ("get_people", (11,), {"season": "2021"}),
    ("get_schedule", (), {"date": "2022-10-07"}),
    ("get_schedule", (), {"start_date": "2021-08-01", "end_date": "2021-08-11"}),
    ("get_schedule", (), {"team_id": 133, "date": "2022-10-07"}),
    ("get_schedule", (), {"gamePks": 531493}),
    ("get_schedule", (), {}),
]


@pytest.mark.parametrize("method, args, kwargs", SYNC_PARITY_CASES)
def test_request_construction_matches_sync_client(method, args, kwargs):
    """AsyncMlb asks the adapter for exactly what Mlb asks for.

    The async surface is a port of the sync one, so a drift in endpoint,
    parameter name, or default belongs in this test rather than in a live
    failure. Both adapters are stubbed, so nothing here reaches the network.
    """
    from unittest.mock import MagicMock

    from mlbstatsapi import Mlb
    from mlbstatsapi.mlb_dataadapter import MlbResult

    empty = MlbResult(status_code=200, message=None, data={})

    sync_mlb = Mlb()
    sync_mlb._mlb_adapter_v1.get = MagicMock(return_value=empty)
    sync_result = getattr(sync_mlb, method)(*args, **kwargs)

    async def scenario():
        async_mlb = AsyncMlb()
        async_mlb._mlb_adapter_v1.get = AsyncMock(return_value=empty)
        result = await getattr(async_mlb, method)(*args, **kwargs)
        return result, async_mlb._mlb_adapter_v1.get.call_args

    async_result, async_call = run_async(scenario())

    assert async_call == sync_mlb._mlb_adapter_v1.get.call_args
    assert async_result == sync_result


def test_signatures_match_the_sync_client():
    """Names, kinds, and defaults are identical to the sync client's."""
    import inspect

    from mlbstatsapi import Mlb

    for name in ("get_team", "get_teams", "get_person", "get_people", "get_schedule"):
        sync_params = inspect.signature(getattr(Mlb, name)).parameters
        async_params = inspect.signature(getattr(AsyncMlb, name)).parameters

        assert [
            (p.name, p.kind, p.default) for p in sync_params.values()
        ] == [
            (p.name, p.kind, p.default) for p in async_params.values()
        ], f"{name} drifted from Mlb.{name}"


# ---------------------------------------------------------------------------
# Concurrency and the absence of hidden work
# ---------------------------------------------------------------------------


def test_concurrent_endpoint_calls_share_one_client_without_crossing_results():
    """Two endpoints on one client keep their own request and their own result.

    Sharing an AsyncClient is the reason AsyncMlb exists; a client that mixed
    up two in-flight responses would be worse than useless.
    """
    handler = _RecordingHandler(
        {
            "teams/133": _json(TEAM_PAYLOAD),
            "people/660271": _json(PERSON_PAYLOAD),
            "schedule": _json(SCHEDULE_PAYLOAD),
        }
    )

    async def scenario():
        mlb = _owned_client(handler)
        return await asyncio.gather(
            mlb.get_team(133),
            mlb.get_person(660271),
            mlb.get_schedule(date="2022-10-07"),
        )

    team, person, schedule = run_async(scenario())

    assert team == Team(id=133, link="/api/v1/teams/133", name="Athletics")
    assert person == Person(
        id=660271, link="/api/v1/people/660271", full_name="Shohei Ohtani"
    )
    assert schedule == Schedule(**SCHEDULE_PAYLOAD)
    assert handler.call_count == 3


def test_one_endpoint_call_does_not_block_another_on_the_same_client():
    """A slow endpoint must not serialize the rest of the client.

    Without real concurrency the fast call could not finish while the slow one
    is still waiting, so the gate would never open and the test would hit its
    timeout instead of passing.
    """
    fast_call_completed = asyncio.Event()

    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("teams/133"):
            await asyncio.wait_for(
                fast_call_completed.wait(),
                timeout=BLOCKED_REQUEST_TIMEOUT,
            )
            return _json(TEAM_PAYLOAD)
        return _json(PERSON_PAYLOAD)

    async def scenario():
        mlb = _owned_client(handler)

        slow = asyncio.ensure_future(mlb.get_team(133))
        await asyncio.sleep(0)

        person = await mlb.get_person(660271)
        fast_call_completed.set()

        return await slow, person

    team, person = run_async(scenario())

    assert team == Team(id=133, link="/api/v1/teams/133", name="Athletics")
    assert person == Person(
        id=660271, link="/api/v1/people/660271", full_name="Shohei Ohtani"
    )


def test_an_endpoint_call_issues_exactly_one_request():
    """No hidden fan-out: one call to one endpoint is one HTTP request.

    A successful call must not prefetch, hydrate, or otherwise widen itself
    into extra traffic behind the caller's back.
    """
    handler = _RecordingHandler(_json(TEAMS_PAYLOAD))

    async def scenario():
        mlb = _owned_client(handler)
        await mlb.get_teams()

    run_async(scenario())

    assert handler.call_count == 1
    assert [request.url.path for request in handler.requests] == ["/api/v1/teams"]


def test_endpoint_calls_leave_no_background_tasks_behind():
    """No hidden background work: nothing outlives the awaited call.

    A stray task would keep running after the client is closed and surface as
    an unpredictable warning or error somewhere else entirely.
    """
    handler = _RecordingHandler(
        {
            "teams": _json(TEAMS_PAYLOAD),
            "teams/133": _json(TEAM_PAYLOAD),
            "people/660271": _json(PERSON_PAYLOAD),
            "sports/1/players": _json(PEOPLE_PAYLOAD),
            "schedule": _json(SCHEDULE_PAYLOAD),
        }
    )

    async def scenario():
        mlb = _owned_client(handler)

        before = asyncio.all_tasks()

        # Every endpoint on the client, so none of them may leak a task.
        await mlb.get_team(133)
        await mlb.get_teams()
        await mlb.get_person(660271)
        await mlb.get_people()
        await mlb.get_schedule(date="2022-10-07")
        await mlb.aclose()

        # Let anything that was scheduled get a chance to appear.
        await asyncio.sleep(0)

        assert asyncio.all_tasks() - before == set()

    run_async(scenario())


def test_construction_starts_no_work():
    """Building a client is inert: no request, no task, until an endpoint is called."""
    handler = _RecordingHandler(_json(TEAM_PAYLOAD))

    async def scenario():
        before = asyncio.all_tasks()

        _owned_client(handler)

        await asyncio.sleep(0)

        assert handler.call_count == 0
        assert asyncio.all_tasks() - before == set()

    run_async(scenario())
