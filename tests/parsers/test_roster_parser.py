from mlbstatsapi._parsers.roster import parse_roster_coaches, parse_roster_players
from mlbstatsapi.models.people import Coach, Player


PLAYER_ROSTER_PAYLOAD = {
    "roster": [
        {
            "person": {"id": 675961, "fullName": "Alika Williams", "link": "/api/v1/people/675961"},
            "jerseyNumber": "12",
            "status": {"code": "A", "description": "Active"},
            "parentTeamId": 133,
        }
    ]
}

COACH_ROSTER_PAYLOAD = {
    "roster": [
        {
            "person": {"id": 117276, "fullName": "Mark Kotsay", "link": "/api/v1/people/117276"},
            "jerseyNumber": "7",
            "job": "Manager",
            "jobId": "MNGR",
            "title": "Manager",
        }
    ]
}


def test_parse_roster_players():
    """parse_roster_players merges the nested person dict and returns Players."""
    assert parse_roster_players({}) == []
    assert parse_roster_players({"roster": []}) == []

    players = parse_roster_players(PLAYER_ROSTER_PAYLOAD)

    assert players == [
        Player(
            id=675961,
            full_name="Alika Williams",
            link="/api/v1/people/675961",
            jersey_number="12",
            status={"code": "A", "description": "Active"},
            parent_team_id=133,
        )
    ]


def test_parse_roster_coaches():
    """parse_roster_coaches merges the nested person dict and returns Coaches."""
    assert parse_roster_coaches({}) == []
    assert parse_roster_coaches({"roster": []}) == []

    coaches = parse_roster_coaches(COACH_ROSTER_PAYLOAD)

    assert coaches == [
        Coach(
            id=117276,
            full_name="Mark Kotsay",
            link="/api/v1/people/117276",
            jersey_number="7",
            job="Manager",
            job_id="MNGR",
            title="Manager",
        )
    ]
