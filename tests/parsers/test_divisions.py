import pytest
from pydantic import ValidationError

from mlbstatsapi._parsers.divisions import parse_division, parse_divisions
from mlbstatsapi.models.divisions import Division


def test_parse_divisions():
    """parse_divisions reads the MLB divisions envelope and returns Division models."""
    assert parse_divisions({}) == []
    assert parse_divisions({"divisions": []}) == []

    divisions = parse_divisions(
        {
            "divisions": [
                {"id": 200, "link": "/api/v1/divisions/200", "name": "American League West"},
                {"id": 201, "link": "/api/v1/divisions/201", "name": "American League East"},
            ]
        }
    )

    assert divisions == [
        Division(id=200, link="/api/v1/divisions/200", name="American League West"),
        Division(id=201, link="/api/v1/divisions/201", name="American League East"),
    ]


def test_parse_division():
    """parse_division builds a Division from one division payload."""
    assert parse_division({}) is None

    division = parse_division(
        {
            "divisions": [
                {"id": 200, "link": "/api/v1/divisions/200", "name": "American League West"}
            ]
        }
    )

    assert isinstance(division, Division)
    assert division == Division(
        id=200, link="/api/v1/divisions/200", name="American League West"
    )


def test_parse_division_requires_link():
    """Division requires link, the same required field used by the MLB API."""
    with pytest.raises(ValidationError):
        parse_division({"divisions": [{"id": 200, "name": "American League West"}]})
