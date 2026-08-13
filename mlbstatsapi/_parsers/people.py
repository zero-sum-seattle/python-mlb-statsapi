from mlbstatsapi.models.people import Person


def parse_people(data: dict) -> list[Person]:
    """Parse Person models from an MLB /people response body."""
    if not data or not data.get("people"):
        return []
    return [Person(**person) for person in data["people"]]


def parse_person(data: dict) -> Person | None:
    """Parse a Person from a single person payload."""
    if not data:
        return None
    return Person(**data)
