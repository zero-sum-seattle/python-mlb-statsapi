from mlbstatsapi.models.drafts import Round


def parse_draft(data: dict) -> list[Round]:
    """Parse Round models from an MLB /draft/{year} response body.

    Expects the full response, e.g. ``{"drafts": {"rounds": [...]}}``.
    """
    if not data or not data.get("drafts"):
        return []

    rounds = data["drafts"].get("rounds")
    if not rounds:
        return []

    return [Round(**round_data) for round_data in rounds]
