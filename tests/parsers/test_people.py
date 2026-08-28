import pytest
from pydantic import ValidationError

from mlbstatsapi._parsers.people import parse_people, parse_person
from mlbstatsapi.models.people import Person


def test_parse_people():
    """parse_people reads the MLB people envelope and returns Person models."""
    assert parse_people({}) == []
    assert parse_people({"people": []}) == []

    people = parse_people(
        {
            "people": [
                {"id": 1, "link": "/api/v1/people/1", "fullName": "Person 1"},
                {"id": 2, "link": "/api/v1/people/2", "fullName": "Person 2"},
            ]
        }
    )

    assert people == [
        Person(id=1, link="/api/v1/people/1", full_name="Person 1"),
        Person(id=2, link="/api/v1/people/2", full_name="Person 2"),
    ]


def test_parse_person():
    """parse_person builds a Person from one person payload."""
    assert parse_person({}) is None

    person = parse_person(
        {"people": [{"id": 1, "link": "/api/v1/people/1", "fullName": "Person 1"}]} 
    )

    assert isinstance(person, Person)
    assert person == Person(id=1, link="/api/v1/people/1", full_name="Person 1")


def test_parse_person_requires_link():
    """Person requires link, the same required field used by the MLB API."""
    with pytest.raises(ValidationError):
        parse_person({"people": [{"id": 1, "fullName": "Person 1"}]})
