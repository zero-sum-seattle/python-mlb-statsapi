from mlbstatsapi.models.seasons import Season


def parse_seasons(data: dict) -> list[Season]:
    """Parse Season models from an MLB /seasons response body.

    Expects the full response, e.g. ``{"seasons": [...]}``, not the inner list.
    """
    if not data or not data.get("seasons"):
        return []
    return [Season(**season) for season in data["seasons"]]


def parse_season(data: dict) -> Season | None:
    """Parse a Season from a single season payload."""
    seasons = parse_seasons(data)

    if not seasons:
        return None

    return seasons[0]
