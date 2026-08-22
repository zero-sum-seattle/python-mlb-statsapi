import pytest
from pydantic import ValidationError

from mlbstatsapi._parsers.leagues import parse_league, parse_leagues
from mlbstatsapi.models.leagues import League


def test_parse_leagues():
    """parse_leagues reads the MLB leagues envelope and returns League models."""
    assert parse_leagues({}) == []
    assert parse_leagues({"leagues": []}) == []

    leagues = parse_leagues(
        {
            "leagues": [
                {"id": 103, "link": "/api/v1/leagues/103", "name": "American League"},
                {"id": 104, "link": "/api/v1/leagues/104", "name": "National League"},
            ]
        }
    )

    assert leagues == [
        League(id=103, link="/api/v1/leagues/103", name="American League"),
        League(id=104, link="/api/v1/leagues/104", name="National League"),
    ]


def test_parse_league():
    """parse_league builds a League from one league payload."""
    assert parse_league({}) is None

    league = parse_league(
        {"leagues": [{"id": 103, "link": "/api/v1/leagues/103", "name": "American League"}]}
    )

    assert isinstance(league, League)
    assert league == League(id=103, link="/api/v1/leagues/103", name="American League")


def test_parse_league_requires_link():
    """League requires link, the same required field used by the MLB API."""
    with pytest.raises(ValidationError):
        parse_league({"leagues": [{"id": 103, "name": "American League"}]})
