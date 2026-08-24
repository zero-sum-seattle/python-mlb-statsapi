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
