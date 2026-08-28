from mlbstatsapi.models.venues import Venue


def parse_venues(data: dict) -> list[Venue]:
    """Parse Venue models from an MLB /venues response body.

    Expects the full response, e.g. ``{"venues": [...]}``, not the inner list.
    """
    if not data or not data.get("venues"):
        return []
    return [Venue(**venue) for venue in data["venues"]]


def parse_venue(data: dict) -> Venue | None:
    """Parse a Venue from a single venue payload."""
    venues = parse_venues(data)

    if not venues:
        return None

    return venues[0]
