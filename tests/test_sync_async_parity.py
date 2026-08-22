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
from mlbstatsapi.models.attendances import Attendance  # noqa: E402
from mlbstatsapi.models.divisions import Division  # noqa: E402
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
# keyword arguments that produce it. Both clients are expected to answer None.
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


def test_get_sport_success_parity():
    """A successful sport response parses to the same Sport on both clients."""
    result = call_both("get_sport", 1, payload=SPORT_PAYLOAD)

    assert isinstance(result.sync, Sport), "sync get_sport did not return a Sport"
    assert (result.sync.id, result.sync.link, result.sync.name) == (
        1,
        "/api/v1/sports/1",
        "Major League Baseball",
    )
    assert result.asynchronous == result.sync
    assert result.request == ("GET", "/api/v1/sports/1", {})


def test_get_league_success_parity():
    """A successful league response parses to the same League on both clients."""
    result = call_both("get_league", 103, payload=LEAGUE_PAYLOAD)

    assert isinstance(result.sync, League), "sync get_league did not return a League"
    assert (result.sync.id, result.sync.link, result.sync.name) == (
        103,
        "/api/v1/leagues/103",
        "American League",
    )
    assert result.asynchronous == result.sync
    assert result.request == ("GET", "/api/v1/leagues/103", {})


def test_get_division_success_parity():
    """A successful division response parses to the same Division on both clients."""
    result = call_both("get_division", 200, payload=DIVISION_PAYLOAD)

    assert isinstance(result.sync, Division), "sync get_division did not return a Division"
    assert (result.sync.id, result.sync.link, result.sync.name) == (
        200,
        "/api/v1/divisions/200",
        "American League West",
    )
    assert result.asynchronous == result.sync
    assert result.request == ("GET", "/api/v1/divisions/200", {})


def test_get_team_roster_success_parity():
    """A successful roster response parses to the same Players on both clients."""
    result = call_both("get_team_roster", 133, payload=ROSTER_PLAYER_PAYLOAD)

    assert isinstance(result.sync, list) and isinstance(result.sync[0], Player), (
        "sync get_team_roster did not return a list of Player"
    )
    assert (result.sync[0].id, result.sync[0].full_name, result.sync[0].jersey_number) == (
        675961,
        "Alika Williams",
        "12",
    )
    assert result.asynchronous == result.sync
    assert result.request == ("GET", "/api/v1/teams/133/roster", {})


def test_get_team_coaches_success_parity():
    """A successful coaches response parses to the same Coaches on both clients."""
    result = call_both("get_team_coaches", 133, payload=ROSTER_COACH_PAYLOAD)

    assert isinstance(result.sync, list) and isinstance(result.sync[0], Coach), (
        "sync get_team_coaches did not return a list of Coach"
    )
    assert (result.sync[0].id, result.sync[0].full_name, result.sync[0].job) == (
        117276,
        "Mark Kotsay",
        "Manager",
    )
    assert result.asynchronous == result.sync
    assert result.request == ("GET", "/api/v1/teams/133/coaches", {})


def test_get_season_success_parity():
    """A successful season response parses to the same Season on both clients."""
    result = call_both("get_season", "2021", payload=SEASON_PAYLOAD)

    assert isinstance(result.sync, Season), "sync get_season did not return a Season"
    assert (result.sync.season_id, result.sync.has_wildcard) == ("2021", True)
    assert result.asynchronous == result.sync
    assert result.request == ("GET", "/api/v1/seasons/2021", {"sportId": "1"})


def test_get_venue_success_parity():
    """A successful venue response parses to the same Venue on both clients."""
    result = call_both("get_venue", 31, payload=VENUE_PAYLOAD)

    assert isinstance(result.sync, Venue), "sync get_venue did not return a Venue"
    assert (result.sync.id, result.sync.link, result.sync.name) == (
        31,
        "/api/v1/venues/31",
        "PNC Park",
    )
    assert result.asynchronous == result.sync
    # hydrate is sent as a repeated query param (?hydrate=a&hydrate=b&...);
    # request_signature's dict(parse_qsl(...)) keeps only the last value, so
    # this only proves the two clients agree, not the full query string.
    assert result.request == ("GET", "/api/v1/venues/31", {"hydrate": "timezone"})


def test_get_standings_success_parity():
    """A successful standings response parses to the same Standings on both clients."""
    result = call_both("get_standings", 103, "2022", payload=STANDINGS_PAYLOAD)

    assert isinstance(result.sync, list) and isinstance(result.sync[0], Standings), (
        "sync get_standings did not return a list of Standings"
    )
    assert result.sync[0].team_records[0].team.name == "Yankees"
    assert result.asynchronous == result.sync
    assert result.request == ("GET", "/api/v1/standings", {"leagueId": "103", "season": "2022"})


def test_get_attendance_success_parity():
    """A successful attendance response parses to the same Attendance on both clients."""
    result = call_both("get_attendance", team_id=133, payload=ATTENDANCE_PAYLOAD)

    assert isinstance(result.sync, Attendance), "sync get_attendance did not return an Attendance"
    assert result.sync.aggregate_totals.attendance_total == 2896460
    assert result.asynchronous == result.sync
    assert result.request == ("GET", "/api/v1/attendance", {"teamId": "133"})


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


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_sport_no_result_parity(label):
    """Every no-result response returns None on either client."""
    result = call_both("get_sport", 1, **NO_RESULT_RESPONSES[label])

    assert result.sync is None, f"sync get_sport returned {result.sync!r} for {label}"
    assert result.asynchronous is None, (
        f"async get_sport returned {result.asynchronous!r} for {label}"
    )


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_league_no_result_parity(label):
    """Every no-result response returns None on either client."""
    result = call_both("get_league", 103, **NO_RESULT_RESPONSES[label])

    assert result.sync is None, f"sync get_league returned {result.sync!r} for {label}"
    assert result.asynchronous is None, (
        f"async get_league returned {result.asynchronous!r} for {label}"
    )


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_division_no_result_parity(label):
    """Every no-result response returns None on either client."""
    result = call_both("get_division", 200, **NO_RESULT_RESPONSES[label])

    assert result.sync is None, f"sync get_division returned {result.sync!r} for {label}"
    assert result.asynchronous is None, (
        f"async get_division returned {result.asynchronous!r} for {label}"
    )


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_team_roster_no_result_parity(label):
    """Every no-result response returns an empty list on either client."""
    result = call_both("get_team_roster", 133, **NO_RESULT_RESPONSES[label])

    assert result.sync == [], f"sync get_team_roster returned {result.sync!r} for {label}"
    assert result.asynchronous == [], (
        f"async get_team_roster returned {result.asynchronous!r} for {label}"
    )


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_team_coaches_no_result_parity(label):
    """Every no-result response returns an empty list on either client."""
    result = call_both("get_team_coaches", 133, **NO_RESULT_RESPONSES[label])

    assert result.sync == [], f"sync get_team_coaches returned {result.sync!r} for {label}"
    assert result.asynchronous == [], (
        f"async get_team_coaches returned {result.asynchronous!r} for {label}"
    )


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_season_no_result_parity(label):
    """Every no-result response returns None on either client."""
    result = call_both("get_season", "2021", **NO_RESULT_RESPONSES[label])

    assert result.sync is None, f"sync get_season returned {result.sync!r} for {label}"
    assert result.asynchronous is None, (
        f"async get_season returned {result.asynchronous!r} for {label}"
    )


def test_get_venue_no_result_parity_404():
    """404 hits Mlb.get_venue's documented quirk: [] rather than None."""
    result = call_both("get_venue", 1, status=404, payload={})

    assert result.sync == [], f"sync get_venue returned {result.sync!r} for 404"
    assert result.asynchronous == [], (
        f"async get_venue returned {result.asynchronous!r} for 404"
    )


@pytest.mark.parametrize("label", ["empty 200", "empty body"])
def test_get_venue_no_result_parity_non_4xx(label):
    """Unlike the 404 quirk, a non-4xx empty response falls through to None."""
    result = call_both("get_venue", 1, **NO_RESULT_RESPONSES[label])

    assert result.sync is None, f"sync get_venue returned {result.sync!r} for {label}"
    assert result.asynchronous is None, (
        f"async get_venue returned {result.asynchronous!r} for {label}"
    )


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_standings_no_result_parity(label):
    """Every no-result response returns an empty list on either client."""
    result = call_both("get_standings", 103, "2022", **NO_RESULT_RESPONSES[label])

    assert result.sync == [], f"sync get_standings returned {result.sync!r} for {label}"
    assert result.asynchronous == [], (
        f"async get_standings returned {result.asynchronous!r} for {label}"
    )


@pytest.mark.parametrize("label", list(NO_RESULT_RESPONSES))
def test_get_attendance_no_result_parity(label):
    """Every no-result response returns None on either client."""
    result = call_both("get_attendance", team_id=133, **NO_RESULT_RESPONSES[label])

    assert result.sync is None, f"sync get_attendance returned {result.sync!r} for {label}"
    assert result.asynchronous is None, (
        f"async get_attendance returned {result.asynchronous!r} for {label}"
    )


def test_get_attendance_without_an_identifier_parity():
    """Regression coverage: the any(dict) vs any(dict.values()) guard bug fix."""
    sync_requests: list = []
    async_requests: list = []

    sync_result = call_sync("get_attendance", observed=sync_requests)
    async_result = call_async("get_attendance", observed=async_requests)

    assert sync_result is None
    assert async_result is None
    assert sync_requests == []
    assert async_requests == []


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
