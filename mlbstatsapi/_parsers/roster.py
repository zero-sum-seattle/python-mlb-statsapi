from mlbstatsapi import mlb_module
from mlbstatsapi.models.people import Coach, Player


def parse_roster_players(data: dict) -> list[Player]:
    """Parse Player models from an MLB /teams/{id}/roster response body."""
    if not data or not data.get("roster"):
        return []
    return [
        Player(**mlb_module.merge_keys(player, ["person"])) for player in data["roster"]
    ]


def parse_roster_coaches(data: dict) -> list[Coach]:
    """Parse Coach models from an MLB /teams/{id}/coaches response body.

    The coaches endpoint reuses the same ``roster`` envelope as the player
    roster endpoint.
    """
    if not data or not data.get("roster"):
        return []
    return [
        Coach(**mlb_module.merge_keys(coach, ["person"])) for coach in data["roster"]
    ]
