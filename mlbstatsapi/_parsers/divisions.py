from mlbstatsapi.models.divisions import Division


def parse_divisions(data: dict) -> list[Division]:
    """Parse Division models from an MLB /divisions response body.

    Expects the full response, e.g. ``{"divisions": [...]}``, not the inner list.
    """
    if not data or not data.get("divisions"):
        return []
    return [Division(**division) for division in data["divisions"]]


def parse_division(data: dict) -> Division | None:
    """Parse a Division from a single division payload."""
    divisions = parse_divisions(data)

    if not divisions:
        return None

    return divisions[0]
