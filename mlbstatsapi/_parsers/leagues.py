from mlbstatsapi.models.leagues import League


def parse_leagues(data: dict) -> list[League]:
    """Parse League models from an MLB /leagues response body.

    Expects the full response, e.g. ``{"leagues": [...]}``, not the inner list.
    """
    if not data or not data.get("leagues"):
        return []
    return [League(**league) for league in data["leagues"]]


def parse_league(data: dict) -> League | None:
    """Parse a League from a single league payload."""
    leagues = parse_leagues(data)

    if not leagues:
        return None

    return leagues[0]
