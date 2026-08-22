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
from mlbstatsapi.models.attendances import Attendance  # noqa: E402
from mlbstatsapi.models.awards import Award  # noqa: E402
from mlbstatsapi.models.divisions import Division  # noqa: E402
from mlbstatsapi.models.drafts import Round  # noqa: E402
from mlbstatsapi.models.leagues import League  # noqa: E402
from mlbstatsapi.models.people import Coach, Person, Player  # noqa: E402
from mlbstatsapi.models.schedules import Schedule  # noqa: E402
from mlbstatsapi.models.seasons import Season  # noqa: E402
from mlbstatsapi.models.sports import Sport  # noqa: E402
from mlbstatsapi.models.standings import Standings  # noqa: E402
from mlbstatsapi.models.teams import Team  # noqa: E402
from mlbstatsapi.models.venues import Venue  # noqa: E402


TEAM_PAYLOAD = {"teams": [{"id": 133, "link": "/api/v1/teams/133", "name": "Athletics"}]}
PERSON_PAYLOAD = {
    "people": [{"id": 660271, "link": "/api/v1/people/660271", "fullName": "Shohei Ohtani"}]
}
SPORT_PAYLOAD = {
    "sports": [{"id": 1, "link": "/api/v1/sports/1", "name": "Major League Baseball"}]
}
LEAGUE_PAYLOAD = {
    "leagues": [{"id": 103, "link": "/api/v1/leagues/103", "name": "American League"}]
}
DIVISION_PAYLOAD = {
    "divisions": [
        {"id": 200, "link": "/api/v1/divisions/200", "name": "American League West"}
    ]
}
ROSTER_PLAYER_PAYLOAD = {
    "roster": [
        {
            "person": {"id": 675961, "fullName": "Alika Williams", "link": "/api/v1/people/675961"},
            "jerseyNumber": "12",
            "status": {"code": "A", "description": "Active"},
            "parentTeamId": 133,
        }
    ]
}
ROSTER_COACH_PAYLOAD = {
    "roster": [
        {
            "person": {"id": 117276, "fullName": "Mark Kotsay", "link": "/api/v1/people/117276"},
            "jerseyNumber": "7",
            "job": "Manager",
            "jobId": "MNGR",
            "title": "Manager",
        }
    ]
}
SEASON_PAYLOAD = {"seasons": [{"seasonId": "2021", "hasWildcard": True}]}
VENUE_PAYLOAD = {"venues": [{"id": 31, "link": "/api/v1/venues/31", "name": "PNC Park"}]}
STANDINGS_RECORD = {
    "standingsType": "regularSeason",
    "league": {"id": 103, "link": "/api/v1/league/103"},
    "division": {"id": 201, "link": "/api/v1/divisions/201"},
    "sport": {"id": 1, "link": "/api/v1/sports/1"},
    "roundRobin": {"status": "false"},
    "lastUpdated": "2025-10-16T23:15:55.082Z",
    "teamRecords": [
        {
            "team": {"id": 147, "name": "Yankees", "link": "/api/v1/teams/147"},
            "season": "2022",
            "streak": {"streakCode": "L2", "streakType": "losses", "streakNumber": 2},
            "clinchIndicator": "y",
            "divisionRank": "1",
            "leagueRank": "2",
            "sportRank": "5",
            "gamesPlayed": 162,
            "gamesBack": "-",
            "wildCardGamesBack": "-",
            "leagueGamesBack": "7.0",
            "springLeagueGamesBack": "-",
            "sportGamesBack": "7.0",
            "divisionGamesBack": "-",
            "conferenceGamesBack": "-",
            "leagueRecord": {"wins": 99, "losses": 63, "ties": 0, "pct": ".611"},
            "lastUpdated": "2025-10-16T23:14:26Z",
            "records": {
                "splitRecords": [{"wins": 57, "losses": 24, "type": "home", "pct": ".704"}],
                "divisionRecords": [
                    {
                        "wins": 17,
                        "losses": 16,
                        "pct": ".515",
                        "division": {
                            "id": 200,
                            "name": "American League West",
                            "link": "/api/v1/divisions/200",
                        },
                    }
                ],
                "overallRecords": [{"wins": 57, "losses": 24, "type": "home", "pct": ".704"}],
                "leagueRecords": [
                    {
                        "wins": 89,
                        "losses": 53,
                        "pct": ".627",
                        "league": {
                            "id": 103,
                            "name": "American League",
                            "link": "/api/v1/league/103",
                        },
                    }
                ],
                "expectedRecords": [
                    {"wins": 106, "losses": 56, "type": "xWinLoss", "pct": ".654"}
                ],
            },
            "runsAllowed": 567,
            "runsScored": 807,
            "divisionChamp": True,
            "divisionLeader": True,
            "hasWildcard": True,
            "clinched": True,
            "eliminationNumber": "-",
            "eliminationNumberSport": "E",
            "eliminationNumberLeague": "E",
            "eliminationNumberDivision": "-",
            "eliminationNumberConference": "E",
            "wildCardEliminationNumber": "-",
            "magicNumber": "-",
            "wins": 99,
            "losses": 63,
            "runDifferential": 240,
            "winningPercentage": ".611",
        }
    ],
}
STANDINGS_PAYLOAD = {"records": [STANDINGS_RECORD]}
ATTENDANCE_PAYLOAD = {
    "records": [
        {
            "openingsTotal": 160,
            "openingsTotalAway": 81,
            "openingsTotalHome": 79,
            "openingsTotalLost": 2,
            "gamesTotal": 162,
            "gamesAwayTotal": 82,
            "gamesHomeTotal": 80,
            "year": "2022",
            "attendanceAverageYtd": 18103,
            "attendanceHigh": 40065,
            "attendanceHighDate": "2022-08-06T00:00:00",
            "attendanceTotal": 2896460,
            "attendanceTotalAway": 2108558,
            "attendanceTotalHome": 787902,
            "gameType": {"id": "R", "description": "Regular Season"},
            "team": {"id": 133, "name": "Oakland Athletics", "link": "/api/v1/teams/133"},
        }
    ],
    "aggregateTotals": {
        "openingsTotalAway": 81,
        "openingsTotalHome": 79,
        "openingsTotalLost": 2,
        "openingsTotalYtd": 0,
        "attendanceAverageYtd": 18103,
        "attendanceHigh": 40065,
        "attendanceHighDate": "2022-08-06T00:00:00",
        "attendanceTotal": 2896460,
        "attendanceTotalAway": 2108558,
        "attendanceTotalHome": 787902,
    },
}
DRAFT_PAYLOAD = {"drafts": {"rounds": [{"round": "1"}]}}
AWARD_PAYLOAD = {
    "id": "ALMVP",
    "name": "AL Most Valuable Player",
    "date": "2022-11-17",
    "season": "2022",
    "team": {"id": 147, "link": "/api/v1/teams/147", "name": "Yankees"},
    "player": {"id": 592450, "link": "/api/v1/people/592450", "fullName": "Aaron Judge"},
}
AWARDS_PAYLOAD = {"awards": [AWARD_PAYLOAD]}
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
EXPECTED_SPORT = Sport(id=1, link="/api/v1/sports/1", name="Major League Baseball")
EXPECTED_LEAGUE = League(id=103, link="/api/v1/leagues/103", name="American League")
EXPECTED_DIVISION = Division(
    id=200, link="/api/v1/divisions/200", name="American League West"
)
EXPECTED_ROSTER_PLAYER = Player(
    id=675961,
    full_name="Alika Williams",
    link="/api/v1/people/675961",
    jersey_number="12",
    status={"code": "A", "description": "Active"},
    parent_team_id=133,
)
EXPECTED_ROSTER_COACH = Coach(
    id=117276,
    full_name="Mark Kotsay",
    link="/api/v1/people/117276",
    jersey_number="7",
    job="Manager",
    job_id="MNGR",
    title="Manager",
)
EXPECTED_SEASON = Season(seasonId="2021", hasWildcard=True)
EXPECTED_VENUE = Venue(id=31, link="/api/v1/venues/31", name="PNC Park")

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

    # Most Mlb methods pass endpoint as a keyword; get_attendance passes it
    # positionally, so fall back to the first positional argument.
    endpoint = call.kwargs["endpoint"] if "endpoint" in call.kwargs else call.args[0]
    return endpoint, call.kwargs["ep_params"]


def _flatten_params(params: dict) -> list[tuple[str, str]]:
    """Expand a params dict into (key, str(value)) pairs, list values repeated.

    Mirrors how both Requests and HTTPX serialize a list-valued query
    parameter: as the same key repeated once per item, e.g.
    ``?hydrate=a&hydrate=b`` rather than a single comma-joined value.
    """
    pairs: list[tuple[str, str]] = []
    for key, value in params.items():
        if isinstance(value, list):
            pairs.extend((key, str(item)) for item in value)
        else:
            pairs.append((key, str(value)))
    return sorted(pairs)


def assert_matches_sync(request: httpx.Request, method: str, *args, **kwargs) -> None:
    """Assert an observed request is the one ``Mlb`` would have made."""
    endpoint, params = sync_request_for(method, *args, **kwargs)

    # get_awards's endpoint string has a trailing "?" (harmless legacy cruft
    # both Requests and HTTPX strip as an empty query separator), which never
    # shows up in url.path.
    assert request.url.path == f"/api/v1/{endpoint}".rstrip("?")
    assert sorted(request.url.params.multi_items()) == _flatten_params(params)


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


def test_get_sport_requests_the_sport_endpoint_and_parses_the_result():
    handler = _Handler(_json(SPORT_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_sport(1)

    sport = asyncio.run(scenario())

    assert_matches_sync(handler.request, "get_sport", 1)
    assert sport == EXPECTED_SPORT


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_sport_returns_none_when_there_is_no_sport(label):
    handler = _Handler(NO_RESULT_RESPONSES[label])

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_sport(1)

    assert asyncio.run(scenario()) is None


def test_get_sports_request_matches_the_sync_client():
    handler = _Handler(_json({"sports": []}))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_sports()

    assert asyncio.run(scenario()) == []
    assert_matches_sync(handler.request, "get_sports")


def test_get_league_requests_the_league_endpoint_and_parses_the_result():
    handler = _Handler(_json(LEAGUE_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_league(103)

    league = asyncio.run(scenario())

    assert_matches_sync(handler.request, "get_league", 103)
    assert league == EXPECTED_LEAGUE


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_league_returns_none_when_there_is_no_league(label):
    handler = _Handler(NO_RESULT_RESPONSES[label])

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_league(103)

    assert asyncio.run(scenario()) is None


def test_get_leagues_request_matches_the_sync_client():
    handler = _Handler(_json({"leagues": []}))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_leagues()

    assert asyncio.run(scenario()) == []
    assert_matches_sync(handler.request, "get_leagues")


def test_get_division_requests_the_division_endpoint_and_parses_the_result():
    handler = _Handler(_json(DIVISION_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_division(200)

    division = asyncio.run(scenario())

    assert_matches_sync(handler.request, "get_division", 200)
    assert division == EXPECTED_DIVISION


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_division_returns_none_when_there_is_no_division(label):
    handler = _Handler(NO_RESULT_RESPONSES[label])

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_division(200)

    assert asyncio.run(scenario()) is None


def test_get_divisions_request_matches_the_sync_client():
    handler = _Handler(_json({"divisions": []}))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_divisions()

    assert asyncio.run(scenario()) == []
    assert_matches_sync(handler.request, "get_divisions")


def test_get_team_roster_requests_the_roster_endpoint_and_parses_the_result():
    handler = _Handler(_json(ROSTER_PLAYER_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_team_roster(133, rosterType="40Man")

    roster = asyncio.run(scenario())

    assert_matches_sync(handler.request, "get_team_roster", 133, rosterType="40Man")
    assert roster == [EXPECTED_ROSTER_PLAYER]


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_team_roster_returns_empty_list_when_there_is_no_roster(label):
    handler = _Handler(NO_RESULT_RESPONSES[label])

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_team_roster(133)

    assert asyncio.run(scenario()) == []


def test_get_team_coaches_requests_the_coaches_endpoint_and_parses_the_result():
    handler = _Handler(_json(ROSTER_COACH_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_team_coaches(133)

    coaches = asyncio.run(scenario())

    assert_matches_sync(handler.request, "get_team_coaches", 133)
    assert coaches == [EXPECTED_ROSTER_COACH]


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_team_coaches_returns_empty_list_when_there_are_no_coaches(label):
    handler = _Handler(NO_RESULT_RESPONSES[label])

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_team_coaches(133)

    assert asyncio.run(scenario()) == []


def test_get_season_requests_the_season_endpoint_and_parses_the_result():
    handler = _Handler(_json(SEASON_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_season("2021")

    season = asyncio.run(scenario())

    assert_matches_sync(handler.request, "get_season", "2021")
    assert season == EXPECTED_SEASON


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_season_returns_none_when_there_is_no_season(label):
    handler = _Handler(NO_RESULT_RESPONSES[label])

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_season("2021")

    assert asyncio.run(scenario()) is None


def test_get_seasons_request_matches_the_sync_client():
    handler = _Handler(_json({"seasons": []}))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_seasons(11)

    assert asyncio.run(scenario()) == []
    assert_matches_sync(handler.request, "get_seasons", 11)


def test_get_venue_requests_the_venue_endpoint_and_parses_the_result():
    handler = _Handler(_json(VENUE_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_venue(31)

    venue = asyncio.run(scenario())

    assert_matches_sync(handler.request, "get_venue", 31)
    assert venue == EXPECTED_VENUE


def test_get_venue_returns_empty_list_on_404():
    """get_venue mirrors Mlb's documented quirk: [] rather than None on 4xx."""
    handler = _Handler(NO_RESULT_RESPONSES["404"])

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_venue(1)

    assert asyncio.run(scenario()) == []


def test_get_venue_returns_none_on_empty_200():
    """Unlike the 4xx quirk, an empty 200 falls through to the normal None."""
    handler = _Handler(NO_RESULT_RESPONSES["empty 200"])

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_venue(1)

    assert asyncio.run(scenario()) is None


def test_get_venues_request_matches_the_sync_client():
    handler = _Handler(_json({"venues": []}))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_venues()

    assert asyncio.run(scenario()) == []
    assert_matches_sync(handler.request, "get_venues")


def test_get_standings_requests_the_standings_endpoint_and_parses_the_result():
    handler = _Handler(_json(STANDINGS_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_standings(103, "2022")

    standings = asyncio.run(scenario())

    assert_matches_sync(handler.request, "get_standings", 103, "2022")
    assert standings == [Standings(**STANDINGS_RECORD)]


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_standings_returns_empty_list_when_there_are_no_standings(label):
    handler = _Handler(NO_RESULT_RESPONSES[label])

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_standings(103, "2022")

    assert asyncio.run(scenario()) == []


def test_get_attendance_requests_the_attendance_endpoint_and_parses_the_result():
    handler = _Handler(_json(ATTENDANCE_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_attendance(team_id=133)

    attendance = asyncio.run(scenario())

    assert_matches_sync(handler.request, "get_attendance", team_id=133)
    assert isinstance(attendance, Attendance)
    assert attendance.aggregate_totals.attendance_total == 2896460


def test_get_attendance_without_an_identifier_returns_none_without_requesting():
    """Regression coverage for the any(dict) vs any(dict.values()) guard bug."""
    handler = _Handler(_json(ATTENDANCE_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_attendance()

    assert asyncio.run(scenario()) is None
    assert handler.requests == []


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_attendance_returns_none_when_there_is_no_attendance(label):
    handler = _Handler(NO_RESULT_RESPONSES[label])

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_attendance(team_id=133)

    assert asyncio.run(scenario()) is None


def test_get_draft_requests_the_draft_endpoint_and_parses_the_result():
    handler = _Handler(_json(DRAFT_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_draft(2019)

    rounds = asyncio.run(scenario())

    assert_matches_sync(handler.request, "get_draft", 2019)
    assert rounds == [Round(round="1")]


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_draft_returns_empty_list_when_there_is_no_draft(label):
    handler = _Handler(NO_RESULT_RESPONSES[label])

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_draft(2019)

    assert asyncio.run(scenario()) == []


def test_get_awards_requests_the_awards_endpoint_and_parses_the_result():
    handler = _Handler(_json(AWARDS_PAYLOAD))

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_awards("ALMVP")

    awards = asyncio.run(scenario())

    assert_matches_sync(handler.request, "get_awards", "ALMVP")
    assert awards == [Award(**AWARD_PAYLOAD)]


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_awards_returns_empty_list_when_there_are_no_awards(label):
    handler = _Handler(NO_RESULT_RESPONSES[label])

    async def scenario():
        async with async_mlb(handler) as mlb:
            return await mlb.get_awards("ALMVP")

    assert asyncio.run(scenario()) == []


# ---------------------------------------------------------------------------
# Parity and concurrency
# ---------------------------------------------------------------------------


def test_public_signatures_match_the_sync_client():
    """Argument names, kinds, and defaults must not drift from Mlb's."""
    import inspect

    for name in (
        "get_team",
        "get_teams",
        "get_team_roster",
        "get_team_coaches",
        "get_person",
        "get_people",
        "get_schedule",
        "get_sport",
        "get_sports",
        "get_league",
        "get_leagues",
        "get_division",
        "get_divisions",
        "get_season",
        "get_seasons",
        "get_venue",
        "get_venues",
        "get_standings",
        "get_attendance",
        "get_draft",
        "get_awards",
    ):
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
