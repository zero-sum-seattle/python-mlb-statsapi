from mlbstatsapi.models.standings import Standings


def parse_standings(data: dict) -> list[Standings]:
    """Parse Standings models from an MLB /standings response body."""
    if not data or not data.get("records"):
        return []
    return [Standings(**standing) for standing in data["records"]]
