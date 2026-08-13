from mlbstatsapi.models.teams import Team


def parse_teams(data: dict) -> list[Team]:
    """Parse Team models from an MLB /teams response body.

    Expects the full response, e.g. ``{"teams": [...]}``, not the inner list.
    """
    if not data or not data.get("teams"):
        return []
    return [Team(**team) for team in data["teams"]]


def parse_team(data: dict) -> Team | None:
    """Parse a Team from a single team payload."""
    if not data:
        return None
    return Team(**data)
