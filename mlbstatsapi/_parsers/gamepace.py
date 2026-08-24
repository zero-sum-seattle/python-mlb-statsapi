from mlbstatsapi.models.gamepace import GamePace


def parse_gamepace(data: dict) -> GamePace | None:
    """Parse a GamePace from an MLB /gamePace response body.

    The endpoint keys its metrics by whichever of ``teams``, ``leagues`` or
    ``sports`` the caller's ``orgType`` selected, so a body carrying none of
    them has nothing to build from.
    """
    if not data:
        return None

    if not (data.get("teams") or data.get("leagues") or data.get("sports")):
        return None

    return GamePace(**data)
