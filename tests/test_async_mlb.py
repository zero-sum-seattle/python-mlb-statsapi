"""Focused offline tests for the AsyncMlb client (issue #303).

AsyncMlb is deliberately thin: it builds a request, hands it to
AsyncMlbDataAdapter, and hands the response to a shared parser. So this module
asserts only what the client itself is responsible for — the package-root
import, the async lifecycle contract, and, per endpoint, the request built and
the value parsed back.

Everything below the client belongs to other modules and is not retested here:
HTTP status mapping, retries, timeouts and exception translation live in
tests/test_async_mlb_dataadapter.py and the #302 transport matrix, and payload
parsing lives in tests/parsers/.

Endpoint tests drive the real adapter over an ``httpx.MockTransport`` rather
than mocking the adapter away, so a method that stopped issuing a request would
fail rather than pass against a mock. Where an endpoint exists to mirror one on
the synchronous client, the expected request is derived from ``Mlb`` itself
rather than hardcoded, so drift shows up here instead of in production.

These tests must not contact the live MLB API.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock

import pytest

# These tests drive the real HTTPX-backed adapter, so a sync-only install has
# nothing here to run. Skipping at collection keeps ``pytest tests/`` working
# without the ``async`` extra instead of erroring on the import. The
# optional-dependency contract itself is asserted in
# tests/test_async_optional_dependency.py.
httpx = pytest.importorskip("httpx", reason="requires the async extra (HTTPX)")

from mlbstatsapi import Mlb  # noqa: E402
from mlbstatsapi.async_mlb import AsyncMlb  # noqa: E402
from mlbstatsapi.mlb_dataadapter import MlbResult  # noqa: E402
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

EXPECTED_TEAM = Team(id=133, link="/api/v1/teams/133", name="Athletics")
EXPECTED_PERSON = Person(
    id=660271, link="/api/v1/people/660271", full_name="Shohei Ohtani"
)

# The two ways an endpoint legitimately comes back with nothing to parse.
NO_RESULT_RESPONSES = {
    "404": httpx.Response(404, json={}),
    "empty 200": httpx.Response(200, json={}),
}


def _json(payload: dict) -> httpx.Response:
    return httpx.Response(200, json=payload)


class _Handler:
    """Serve a canned response and record the requests that arrive."""

    def __init__(self, responses: httpx.Response | dict[str, httpx.Response]):
        # A bare Response answers any path; a dict is keyed by endpoint,
        # e.g. {"teams/133": ...}.
        self._responses = responses
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if isinstance(self._responses, httpx.Response):
            return self._responses
        return self._responses[request.url.path.split("/api/v1/", 1)[-1]]

    @property
    def request(self) -> httpx.Request:
        """The single request the call made.

        Asserting the count here means every test using it also rules out a
        client that quietly fanned one call out into several.
        """
        assert len(self.requests) == 1, f"expected 1 request, got {len(self.requests)}"
        return self.requests[0]


@asynccontextmanager
async def async_mlb(handler: _Handler):
    """Yield an AsyncMlb whose own client talks to ``handler``, then close it.

    AsyncMlb builds its adapter and client through the production path; only
    the transport is swapped. Teardown closes the adapter's client directly
    rather than calling AsyncMlb.aclose(), so the lifecycle tests that replace
    aclose with a mock still get their real client closed.
    """
    real_async_client = httpx.AsyncClient

    def mock_transport_client(**client_kwargs) -> httpx.AsyncClient:
        return real_async_client(
            transport=httpx.MockTransport(handler), **client_kwargs
        )

    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(
            "mlbstatsapi.async_mlb_dataadapter.httpx.AsyncClient",
            mock_transport_client,
        )
        mlb = AsyncMlb()

    try:
        yield mlb
    finally:
        await mlb._mlb_adapter_v1._client.aclose()


def sync_request_for(method: str, *args, **kwargs) -> tuple[str, dict]:
    """Return the endpoint and params ``Mlb`` builds for a call.

    The adapter is stubbed, so this reaches no network; it just reads back what
    the synchronous client asked for.
    """
    with Mlb() as sync_mlb:
        sync_mlb._mlb_adapter_v1.get = MagicMock(
            return_value=MlbResult(status_code=200, message=None, data={})
        )
        getattr(sync_mlb, method)(*args, **kwargs)
        call = sync_mlb._mlb_adapter_v1.get.call_args

    return call.kwargs["endpoint"], call.kwargs["ep_params"]


def assert_matches_sync(request: httpx.Request, method: str, *args, **kwargs) -> None:
    """Assert an observed request is the one ``Mlb`` would have made."""
    endpoint, params = sync_request_for(method, *args, **kwargs)

    assert request.url.path == f"/api/v1/{endpoint}"
    # Query values arrive as strings, whatever type the client passed in.
    assert dict(request.url.params) == {k: str(v) for k, v in params.items()}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def test_async_mlb_is_importable_from_the_package_root():
    """AsyncMlb resolves through the package root's lazy async export."""
    from mlbstatsapi import AsyncMlb as RootAsyncMlb

    assert RootAsyncMlb is AsyncMlb


# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------


def test_aenter_returns_self():
    async def scenario():
        async with async_mlb(_Handler(_json(TEAM_PAYLOAD))) as mlb:
            async with mlb as entered:
                assert entered is mlb

    asyncio.run(scenario())


def test_context_exit_closes_the_owned_client():
    async def scenario():
        async with async_mlb(_Handler(_json(TEAM_PAYLOAD))) as mlb:
            client = mlb._mlb_adapter_v1._client

            async with mlb:
                await mlb.get_team(133)

            assert client.is_closed

    asyncio.run(scenario())


def test_context_exit_closes_the_owned_client_when_the_body_raises():
    async def scenario():
        async with async_mlb(_Handler(_json(TEAM_PAYLOAD))) as mlb:
            client = mlb._mlb_adapter_v1._client

            with pytest.raises(ValueError, match="boom"):
                async with mlb:
                    raise ValueError("boom")

            assert client.is_closed

    asyncio.run(scenario())


def test_cleanup_failure_does_not_replace_the_original_exception():
    """A failure while closing must not mask what actually went wrong.

    With no original exception to protect, the cleanup failure is the only
    thing to report and does surface.
    """

    async def scenario():
        async with async_mlb(_Handler(_json(TEAM_PAYLOAD))) as mlb:
            mlb._mlb_adapter_v1.aclose = AsyncMock(
                side_effect=RuntimeError("cleanup failed")
            )

            with pytest.raises(ValueError, match="original"):
                async with mlb:
                    raise ValueError("original")

            with pytest.raises(RuntimeError, match="cleanup failed"):
                async with mlb:
                    pass

    asyncio.run(scenario())


def test_cancellation_is_preserved_through_cleanup():
    """Cleanup must not swallow a cancellation that arrived from outside."""

    async def scenario():
        async with async_mlb(_Handler(_json(TEAM_PAYLOAD))) as mlb:
            client = mlb._mlb_adapter_v1._client

            async def worker():
                async with mlb:
                    await asyncio.sleep(60)

            task = asyncio.create_task(worker())
            await asyncio.sleep(0)
            task.cancel()

            with pytest.raises(asyncio.CancelledError):
                await task

            assert client.is_closed

    asyncio.run(scenario())


def test_caller_injected_client_is_left_open():
    """A client the caller supplied is the caller's to close, not the library's."""
    handler = _Handler(_json(TEAM_PAYLOAD))
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))

    async def scenario():
        try:
            async with AsyncMlb(client=client) as mlb:
                await mlb.get_team(133)

            assert client.is_closed is False
        finally:
            await client.aclose()

    asyncio.run(scenario())


def test_aclose_is_idempotent():
    """Closing more than once, however the caller mixes the forms, is safe."""

    async def scenario():
        async with async_mlb(_Handler(_json(TEAM_PAYLOAD))) as mlb:
            async with mlb:
                await mlb.get_team(133)

            await mlb.aclose()
            await mlb.aclose()

    asyncio.run(scenario())


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


def test_get_team_requests_the_team_endpoint_and_parses_the_result():
    handler = _Handler(_json(TEAM_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_team(133, season="2022")

    team = asyncio.run(scenario())

    assert_matches_sync(handler.request, "get_team", 133, season="2022")
    assert team == EXPECTED_TEAM


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_team_returns_none_when_there_is_no_team(label):
    handler = _Handler(NO_RESULT_RESPONSES[label])

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_team(1)

    assert asyncio.run(scenario()) is None


def test_get_person_requests_the_person_endpoint_and_parses_the_result():
    handler = _Handler(_json(PERSON_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_person(660271, hydrate="currentTeam")

    person = asyncio.run(scenario())

    assert_matches_sync(handler.request, "get_person", 660271, hydrate="currentTeam")
    assert person == EXPECTED_PERSON


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_person_returns_none_when_there_is_no_person(label):
    handler = _Handler(NO_RESULT_RESPONSES[label])

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_person(1)

    assert asyncio.run(scenario()) is None


def test_get_schedule_requests_the_schedule_endpoint_and_parses_the_result():
    """A date range with a team is representative of the schedule params."""
    handler = _Handler(_json(SCHEDULE_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_schedule(
                start_date="2021-08-01", end_date="2021-08-11", team_id=133
            )

    schedule = asyncio.run(scenario())

    assert_matches_sync(
        handler.request,
        "get_schedule",
        start_date="2021-08-01",
        end_date="2021-08-11",
        team_id=133,
    )
    assert schedule == Schedule(**SCHEDULE_PAYLOAD)


def test_get_schedule_without_a_selector_returns_none_without_requesting():
    """No date and no gamePks is unanswerable, so nothing is sent."""
    handler = _Handler(_json(SCHEDULE_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_schedule()

    assert asyncio.run(scenario()) is None
    assert handler.requests == []


def test_get_teams_request_matches_the_sync_client():
    """get_teams promotes sport_id into sportId exactly as Mlb.get_teams does."""
    handler = _Handler(_json({"teams": []}))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_teams(11, season="2021")

    assert asyncio.run(scenario()) == []
    assert_matches_sync(handler.request, "get_teams", 11, season="2021")


def test_get_people_request_matches_the_sync_client():
    """get_people reads sports/{sport_id}/players, like Mlb.get_people.

    The sport id belongs in the path, not the query; sending it as personIds
    against ``people`` would be the get_persons endpoint instead.
    """
    handler = _Handler(_json({"people": []}))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_people(11, season="2021")

    assert asyncio.run(scenario()) == []
    assert_matches_sync(handler.request, "get_people", 11, season="2021")


# ---------------------------------------------------------------------------
# Parity and concurrency
# ---------------------------------------------------------------------------


def test_public_signatures_match_the_sync_client():
    """Argument names, kinds, and defaults must not drift from Mlb's."""
    import inspect

    for name in ("get_team", "get_teams", "get_person", "get_people", "get_schedule"):
        sync_params = inspect.signature(getattr(Mlb, name)).parameters
        async_params = inspect.signature(getattr(AsyncMlb, name)).parameters

        assert [(p.name, p.kind, p.default) for p in sync_params.values()] == [
            (p.name, p.kind, p.default) for p in async_params.values()
        ], f"AsyncMlb.{name} drifted from Mlb.{name}"


def test_concurrent_calls_on_one_client_do_not_cross_results():
    """Sharing one client is the point of AsyncMlb; results must stay distinct."""
    handler = _Handler(
        {
            "teams/133": _json(TEAM_PAYLOAD),
            "people/660271": _json(PERSON_PAYLOAD),
        }
    )

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await asyncio.gather(mlb.get_team(133), mlb.get_person(660271))

    team, person = asyncio.run(scenario())

    assert team == EXPECTED_TEAM
    assert person == EXPECTED_PERSON
