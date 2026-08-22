from mlbstatsapi.models.game import BoxScore, Game, Linescore, Plays


def parse_game(data: dict, game_id: int) -> Game | None:
    """Parse a Game from an MLB /game/{id}/feed/live response body."""
    if not data or data.get("gamePk") != game_id:
        return None
    return Game(**data)


def parse_plays(data: dict) -> Plays | None:
    """Parse Plays from an MLB /game/{id}/playByPlay response body."""
    if not data or not data.get("allPlays"):
        return None
    return Plays(**data)


def parse_linescore(data: dict) -> Linescore | None:
    """Parse a Linescore from an MLB /game/{id}/linescore response body."""
    if not data or not data.get("teams"):
        return None
    return Linescore(**data)


def parse_boxscore(data: dict) -> BoxScore | None:
    """Parse a BoxScore from an MLB /game/{id}/boxscore response body."""
    if not data or not data.get("teams"):
        return None
    return BoxScore(**data)


def parse_game_ids(data: dict) -> list[int]:
    """Parse gamePks out of an MLB /schedule response body."""
    if not data or not data.get("dates"):
        return []
    return [
        game["gamePk"]
        for date in data["dates"]
        for game in date["games"]
    ]
