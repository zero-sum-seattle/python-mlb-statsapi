from mlbstatsapi.models.schedules import Schedule, ScheduleGames


def parse_schedule(data: dict) -> Schedule | None:
    """Parse a Schedule from an MLB /schedule response body."""
    if not data or not data.get("dates"):
        return None

    return Schedule(**data)


def parse_scheduled_games(data: dict) -> list[ScheduleGames]:
    """Parse the games out of an MLB /schedule response body, flattened.

    The response nests games under one entry per date; this returns them as a
    single list, dropping the date grouping.
    """
    if not data or not data.get("dates"):
        return []

    return [
        ScheduleGames(**game)
        for date in data["dates"]
        for game in date["games"]
    ]
