from mlbstatsapi.models.sports import Sport


def parse_sports(data: dict) -> list[Sport]:
    """Parse Sport models from an MLB /sports response body.

    Expects the full response, e.g. ``{"sports": [...]}``, not the inner list.
    """
    if not data or not data.get("sports"):
        return []
    return [Sport(**sport) for sport in data["sports"]]


def parse_sport(data: dict) -> Sport | None:
    """Parse a Sport from a single sport payload."""
    sports = parse_sports(data)

    if not sports:
        return None

    return sports[0]
