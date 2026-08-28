from mlbstatsapi._parsers.games import (
    parse_boxscore,
    parse_game,
    parse_game_ids,
    parse_linescore,
    parse_plays,
)
from mlbstatsapi.models.game import BoxScore, Game, Linescore, Plays


GAME_PAYLOAD = {"gamePk": 717911, "link": "/api/v1.1/game/717911/feed/live"}

PLAY_PAYLOAD = {
    "result": {
        "type": "atBat",
        "event": "Single",
        "eventType": "single",
        "description": "x",
        "rbi": 0,
        "awayScore": 0,
        "homeScore": 0,
    },
    "about": {
        "atBatIndex": 0,
        "halfInning": "top",
        "isTopInning": True,
        "inning": 1,
        "isComplete": True,
        "isScoringPlay": False,
        "hasOut": True,
        "captivatingIndex": 0,
    },
    "count": {"balls": 0, "outs": 1, "strikes": 0},
    "matchup": {
        "batter": {"id": 1, "link": "/api/v1/people/1", "fullName": "x"},
        "batSide": {"code": "R", "description": "Right"},
        "pitcher": {"id": 2, "link": "/api/v1/people/2", "fullName": "y"},
        "pitchHand": {"code": "R", "description": "Right"},
        "batterHotColdZones": [],
        "pitcherHotColdZones": [],
        "splits": {"batter": "vs_RHP", "pitcher": "vs_RHB", "menOnBase": "Empty"},
    },
    "pitchIndex": [],
    "actionIndex": [],
    "runnerIndex": [],
    "atBatIndex": 0,
}
PLAYS_PAYLOAD = {"scoringPlays": [], "allPlays": [PLAY_PAYLOAD]}

TEAM_PAYLOAD = {"id": 133, "link": "/api/v1/teams/133", "name": "Athletics"}
LINESCORE_PAYLOAD = {
    "scheduledInnings": 9,
    "teams": {"home": {}, "away": {}},
    "defense": {"team": TEAM_PAYLOAD},
    "offense": {"team": TEAM_PAYLOAD},
}

BOXSCORE_SIDE = {
    "team": TEAM_PAYLOAD,
    "teamStats": {},
    "players": {},
    "batters": [],
    "pitchers": [],
    "bench": [],
    "bullpen": [],
    "battingOrder": [],
    "info": [],
}
BOXSCORE_PAYLOAD = {"teams": {"home": BOXSCORE_SIDE, "away": BOXSCORE_SIDE}}

SCHEDULE_WITH_GAMES_PAYLOAD = {
    "dates": [
        {"games": [{"gamePk": 1}, {"gamePk": 2}]},
        {"games": [{"gamePk": 3}]},
    ]
}


def test_parse_game():
    """parse_game only accepts a payload whose gamePk matches the requested id."""
    assert parse_game({}, 717911) is None
    assert parse_game({"gamePk": 1, "link": "x"}, 717911) is None

    game = parse_game(GAME_PAYLOAD, 717911)

    assert isinstance(game, Game)
    assert game.id == 717911


def test_parse_plays():
    """parse_plays requires a non-empty allPlays list."""
    assert parse_plays({}) is None
    assert parse_plays({"allPlays": []}) is None

    plays = parse_plays(PLAYS_PAYLOAD)

    assert isinstance(plays, Plays)
    assert len(plays.all_plays) == 1


def test_parse_linescore():
    """parse_linescore requires a non-empty teams object."""
    assert parse_linescore({}) is None
    assert parse_linescore({"teams": {}}) is None

    linescore = parse_linescore(LINESCORE_PAYLOAD)

    assert isinstance(linescore, Linescore)
    assert linescore.scheduled_innings == 9


def test_parse_boxscore():
    """parse_boxscore requires a non-empty teams object."""
    assert parse_boxscore({}) is None
    assert parse_boxscore({"teams": {}}) is None

    boxscore = parse_boxscore(BOXSCORE_PAYLOAD)

    assert isinstance(boxscore, BoxScore)


def test_parse_game_ids():
    """parse_game_ids flattens dates -> games -> gamePk."""
    assert parse_game_ids({}) == []
    assert parse_game_ids({"dates": []}) == []

    assert parse_game_ids(SCHEDULE_WITH_GAMES_PAYLOAD) == [1, 2, 3]
