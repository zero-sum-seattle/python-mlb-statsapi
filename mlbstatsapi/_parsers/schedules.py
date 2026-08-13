from mlbstatsapi.models.schedules import Schedule


def parse_schedule(data: dict) -> Schedule | None:
    """Parse a Schedule from an MLB /schedule response body."""
    if not data or not data.get("dates"):
        return None

    return Schedule(**data)
