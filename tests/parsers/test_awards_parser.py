from mlbstatsapi._parsers.awards import parse_awards
from mlbstatsapi.models.awards import Award


AWARD_PAYLOAD = {
    "id": "ALMVP",
    "name": "AL Most Valuable Player",
    "date": "2022-11-17",
    "season": "2022",
    "team": {"id": 147, "link": "/api/v1/teams/147", "name": "Yankees"},
    "player": {"id": 592450, "link": "/api/v1/people/592450", "fullName": "Aaron Judge"},
}


def test_parse_awards():
    """parse_awards reads the MLB awards envelope and returns Award models."""
    assert parse_awards({}) == []
    assert parse_awards({"awards": []}) == []

    awards = parse_awards({"awards": [AWARD_PAYLOAD]})

    assert awards == [Award(**AWARD_PAYLOAD)]
    assert awards[0].player.full_name == "Aaron Judge"


def test_parse_awards_without_team():
    """Recipients such as Hall of Fame executives come back without a team."""
    payload = {
        "id": "MLBHOF",
        "name": "Hall Of Fame",
        "date": "2021-12-05",
        "season": "2021",
        "player": {"id": 650067, "link": "/api/v1/people/650067", "nameFirstLast": "Buck O'Neil"},
    }

    awards = parse_awards({"awards": [AWARD_PAYLOAD, payload]})

    assert len(awards) == 2
    assert awards[1].team is None
    assert awards[1].player.id == 650067
