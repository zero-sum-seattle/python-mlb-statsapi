import pytest
from pydantic import ValidationError

from mlbstatsapi._parsers.schedules import parse_schedule, parse_scheduled_games
from mlbstatsapi.models.schedules import Schedule, ScheduleGames


def test_parse_schedule():
    """parse_schedule builds a Schedule from the full MLB schedule body."""
    assert parse_schedule({}) is None

    payload = {
        "totalItems": 1,
        "totalEvents": 0,
        "totalGames": 1,
        "totalGamesInProgress": 0,
        "dates": [
            {
                "date": "2026-08-12",
                "totalItems": 1,
                "totalEvents": 0,
                "totalGames": 1,
                "totalGamesInProgress": 0,
                "games": [],
            }
        ]
    }
    schedule = parse_schedule(payload)

    assert isinstance(schedule, Schedule)
    assert schedule == Schedule(**payload)


def test_parse_schedule_requires_totals():
    """Schedule requires the MLB total* fields from the response body."""
    with pytest.raises(ValidationError):
        parse_schedule(
            {
                "dates": [
                    {
                        "date": "2026-08-12",
                        "totalItems": 0,
                        "totalEvents": 0,
                        "totalGames": 0,
                        "totalGamesInProgress": 0,
                        "games": [],
                    }
                ]
            }
        )


def _game(game_pk: int) -> dict:
    return {
        "gamePk": game_pk,
        "gameGuid": "d344c53c-9e37-4c4b-86ae-f20e769115fc",
        "link": f"/api/v1.1/game/{game_pk}/feed/live",
        "gameType": "D",
        "season": "2022",
        "gameDate": "2022-10-13T19:37:00Z",
        "officialDate": "2022-10-13",
        "status": {
            "abstractGameState": "Final",
            "codedGameState": "F",
            "detailedState": "Final",
            "statusCode": "F",
            "startTimeTBD": False,
            "abstractGameCode": "F",
        },
        "teams": {
            "away": {
                "team": {"id": 136, "name": "Seattle Mariners", "link": "/api/v1/teams/136"},
                "leagueRecord": {"wins": 0, "losses": 2, "ties": 0, "pct": ".000"},
                "score": 2,
                "isWinner": False,
                "splitSquad": False,
                "seriesNumber": 1,
            },
            "home": {
                "team": {"id": 117, "name": "Houston Astros", "link": "/api/v1/teams/117"},
                "leagueRecord": {"wins": 2, "losses": 0, "ties": 0, "pct": "1.000"},
                "score": 4,
                "isWinner": True,
                "splitSquad": False,
                "seriesNumber": 1,
            },
        },
        "venue": {"id": 2392, "name": "Minute Maid Park", "link": "/api/v1/venues/2392"},
        "content": {"link": f"/api/v1/game/{game_pk}/content"},
        "isTie": False,
        "gameNumber": 1,
        "publicFacing": True,
        "doubleHeader": "N",
        "gamedayType": "P",
        "tiebreaker": "N",
        "calendarEventID": f"14-{game_pk}-2022-10-13",
        "seasonDisplay": "2022",
        "dayNight": "day",
        "description": "ALDS Game 2",
        "scheduledInnings": 9,
        "reverseHomeAwayStatus": False,
        "inningBreakLength": 120,
        "gamesInSeries": 5,
        "seriesGameNumber": 2,
        "seriesDescription": "AL Division Series",
        "recordSource": "S",
        "ifNecessary": "N",
        "ifNecessaryDescription": "Normal Game",
    }


def _date(date: str, *games: dict) -> dict:
    return {
        "date": date,
        "totalItems": len(games),
        "totalEvents": 0,
        "totalGames": len(games),
        "totalGamesInProgress": 0,
        "games": list(games),
    }


def test_parse_scheduled_games_builds_models():
    games = parse_scheduled_games({"dates": [_date("2022-10-13", _game(715757))]})

    assert len(games) == 1
    assert isinstance(games[0], ScheduleGames)
    assert games[0].game_pk == 715757


def test_parse_scheduled_games_flattens_across_dates():
    """The response groups games by date; the parser drops that grouping."""
    games = parse_scheduled_games(
        {
            "dates": [
                _date("2022-10-13", _game(715757), _game(715758)),
                _date("2022-10-14", _game(715759)),
            ]
        }
    )

    assert [game.game_pk for game in games] == [715757, 715758, 715759]


def test_parse_scheduled_games_with_no_dates_returns_empty_list():
    assert parse_scheduled_games({"dates": []}) == []
    assert parse_scheduled_games({}) == []
    assert parse_scheduled_games(None) == []


def test_parse_scheduled_games_with_a_date_carrying_no_games_returns_empty_list():
    assert parse_scheduled_games({"dates": [_date("2022-10-13")]}) == []
