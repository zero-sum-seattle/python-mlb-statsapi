import pytest
from pydantic import ValidationError
from mlbstatsapi._parsers.people import parse_people, parse_person
from mlbstatsapi.models.people import Person


def test_parse_people():
    """Test the parse_people function"""
    assert parse_people({}) == []
    assert parse_people({"people": []}) == []

    people = parse_people(
        {
            "people": [
                {"id": 1, "name": "Person 1"},
                {"id": 2, "name": "Person 2"},
            ]
        }
    )

    assert people == [
        Person(id=1, name="Person 1"),
        Person(id=2, name="Person 2"),
    ]

def test_parse_person():
    """Test the parse_person function"""
    assert parse_person({}) is None

    person = parse_person({"id": 1, "name": "Person 1"})

    assert isinstance(person, Person)
    assert person == Person(id=1, name="Person 1")

def test_parse_person_requires_name():
    """Test the parse_person function requires name"""
    with pytest.raises(ValidationError):
        parse_person({"id": 1})