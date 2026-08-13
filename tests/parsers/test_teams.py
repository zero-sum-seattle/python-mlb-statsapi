import pytest
from pydantic import ValidationError

from mlbstatsapi._parsers.teams import parse_team, parse_teams
from mlbstatsapi.models.teams import Team


def test_parse_teams():
    """parse_teams reads the MLB teams envelope and returns Team models."""
    assert parse_teams({}) == []
    assert parse_teams({"teams": []}) == []

    teams = parse_teams(
        {
            "teams": [
                {"id": 1, "link": "/api/v1/teams/1", "name": "Team 1"},
                {"id": 2, "link": "/api/v1/teams/2", "name": "Team 2"},
            ]
        }
    )

    assert teams == [
        Team(id=1, link="/api/v1/teams/1", name="Team 1"),
        Team(id=2, link="/api/v1/teams/2", name="Team 2"),
    ]


def test_parse_team():
    """parse_team builds a Team from one team payload."""
    assert parse_team({}) is None

    team = parse_team({"teams": [{"id": 1, "link": "/api/v1/teams/1", "name": "Team 1"}]})

    assert isinstance(team, Team)
    assert team == Team(id=1, link="/api/v1/teams/1", name="Team 1")


def test_parse_team_requires_link():
    """Team requires link, the same required field used by the MLB API."""
    with pytest.raises(ValidationError):
        parse_team({"teams": [{"id": 1, "name": "Team 1"}]})
