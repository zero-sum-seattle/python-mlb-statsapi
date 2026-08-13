from mlbstatsapi.models.people import Person

def parse_people(data: dict) -> list[Person]:
    """Parse a list of people from the data"""
    return [Person(**person) for person in data['people']] if data['people'] else []

def parse_person(data: dict) -> Person:
    """Parse a person from the data"""
    return Person(**data) if data else None