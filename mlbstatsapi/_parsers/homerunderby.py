from mlbstatsapi.models.homerunderby import HomeRunDerby


def parse_homerun_derby(data: dict) -> HomeRunDerby | None:
    """Parse a HomeRunDerby from an MLB /homeRunDerby/{gamePk} response body."""
    if not data or not data.get("status"):
        return None
    return HomeRunDerby(**data)
