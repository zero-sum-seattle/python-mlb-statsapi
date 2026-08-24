import pytest
from pydantic import ValidationError

from mlbstatsapi._parsers.sports import parse_sport, parse_sports
from mlbstatsapi.models.sports import Sport


def test_parse_sports():
    """parse_sports reads the MLB sports envelope and returns Sport models."""
    assert parse_sports({}) == []
    assert parse_sports({"sports": []}) == []

    sports = parse_sports(
        {
            "sports": [
                {"id": 1, "link": "/api/v1/sports/1", "name": "Major League Baseball"},
                {"id": 11, "link": "/api/v1/sports/11", "name": "Triple-A"},
            ]
        }
    )

    assert sports == [
        Sport(id=1, link="/api/v1/sports/1", name="Major League Baseball"),
        Sport(id=11, link="/api/v1/sports/11", name="Triple-A"),
    ]


def test_parse_sport():
    """parse_sport builds a Sport from one sport payload."""
    assert parse_sport({}) is None

    sport = parse_sport(
        {"sports": [{"id": 1, "link": "/api/v1/sports/1", "name": "Major League Baseball"}]}
    )

    assert isinstance(sport, Sport)
    assert sport == Sport(id=1, link="/api/v1/sports/1", name="Major League Baseball")


def test_parse_sport_requires_link():
    """Sport requires link, the same required field used by the MLB API."""
    with pytest.raises(ValidationError):
        parse_sport({"sports": [{"id": 1, "name": "Major League Baseball"}]})
