from mlbstatsapi import mlb_module


def parse_split_stats(data: dict) -> dict:
    """Parse split stat data from an MLB stats response body.

    Shared by every stats endpoint -- ``/stats``, ``/people/{id}/stats``,
    ``/teams/{id}/stats``, and ``/people/{id}/stats/game/{game_id}`` -- all of
    which return the same ``stats`` envelope.

    Returns a dict keyed by stat group, then by stat type, or ``{}`` when the
    response carries no stats.
    """
    if not data or not data.get("stats"):
        return {}
    return mlb_module.create_split_data(data["stats"])
