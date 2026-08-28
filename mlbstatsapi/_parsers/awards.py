from mlbstatsapi.models.awards import Award


def parse_awards(data: dict) -> list[Award]:
    """Parse Award models from an MLB /awards/{id}/recipients response body."""
    if not data or not data.get("awards"):
        return []
    return [Award(**award) for award in data["awards"]]
