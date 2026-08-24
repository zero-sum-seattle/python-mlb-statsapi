from mlbstatsapi._parsers.gamepace import parse_gamepace
from mlbstatsapi.models.gamepace import GamePace


SPORT_PACE = {
    "hitsPer9Inn": 16.68,
    "runsPer9Inn": 9.3,
    "pitchesPer9Inn": 299.83,
    "totalGames": 2429,
    "timePerGame": "03:11:26",
    "season": "2021",
    "sport": {"id": 1, "code": "mlb", "link": "/api/v1/sports/1"},
}

TEAM_PACE = dict(
    SPORT_PACE,
    team={"id": 133, "name": "Athletics", "link": "/api/v1/teams/133"},
)

LEAGUE_PACE = dict(
    SPORT_PACE,
    league={"id": 103, "name": "American League", "link": "/api/v1/league/103"},
)


def test_parses_sports_pace():
    gamepace = parse_gamepace({"sports": [SPORT_PACE]})

    assert isinstance(gamepace, GamePace)
    assert len(gamepace.sports) == 1
    assert gamepace.sports[0].season == "2021"


def test_parses_teams_pace():
    gamepace = parse_gamepace({"teams": [TEAM_PACE]})

    assert isinstance(gamepace, GamePace)
    assert len(gamepace.teams) == 1


def test_parses_leagues_pace():
    gamepace = parse_gamepace({"leagues": [LEAGUE_PACE]})

    assert isinstance(gamepace, GamePace)
    assert len(gamepace.leagues) == 1


def test_any_one_populated_key_is_enough():
    """The endpoint keys metrics by orgType, so only one of the three arrives."""
    gamepace = parse_gamepace({"teams": [], "leagues": [], "sports": [SPORT_PACE]})

    assert isinstance(gamepace, GamePace)


def test_a_body_with_none_of_the_three_keys_returns_none():
    assert parse_gamepace({"copyright": "NOTICE"}) is None


def test_a_body_whose_keys_are_all_empty_returns_none():
    assert parse_gamepace({"teams": [], "leagues": [], "sports": []}) is None


def test_empty_body_returns_none():
    assert parse_gamepace({}) is None
    assert parse_gamepace(None) is None
