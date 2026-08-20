from mlbstatsapi.models.schedules import Schedule


def parse_schedule(data: dict) -> Schedule | None:
    """Parse a Schedule from an MLB /schedule response body."""
    if not data or not data.get("dates"):
        return None

    return Schedule(**data)

def build_schedule_params(
    date: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    sport_id: int = 1,
    team_id: int | None = None,
    **params,
) -> dict | None:
    if start_date and end_date:
        params["startDate"] = start_date
        params["endDate"] = end_date
    elif date and not (start_date or end_date):
        params["date"] = date
    elif "gamePks" not in params:
        return None

    if team_id:
        params["teamId"] = team_id

    params["sportId"] = sport_id

    return params
