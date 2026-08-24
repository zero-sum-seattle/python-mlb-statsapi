from mlbstatsapi._parsers.standings import parse_standings
from mlbstatsapi.models.standings import Standings


STANDINGS_RECORD = {
    "standingsType": "regularSeason",
    "league": {"id": 103, "link": "/api/v1/league/103"},
    "division": {"id": 201, "link": "/api/v1/divisions/201"},
    "sport": {"id": 1, "link": "/api/v1/sports/1"},
    "roundRobin": {"status": "false"},
    "lastUpdated": "2025-10-16T23:15:55.082Z",
    "teamRecords": [
        {
            "team": {"id": 147, "name": "Yankees", "link": "/api/v1/teams/147"},
            "season": "2022",
            "streak": {"streakCode": "L2", "streakType": "losses", "streakNumber": 2},
            "clinchIndicator": "y",
            "divisionRank": "1",
            "leagueRank": "2",
            "sportRank": "5",
            "gamesPlayed": 162,
            "gamesBack": "-",
            "wildCardGamesBack": "-",
            "leagueGamesBack": "7.0",
            "springLeagueGamesBack": "-",
            "sportGamesBack": "7.0",
            "divisionGamesBack": "-",
            "conferenceGamesBack": "-",
            "leagueRecord": {"wins": 99, "losses": 63, "ties": 0, "pct": ".611"},
            "lastUpdated": "2025-10-16T23:14:26Z",
            "records": {
                "splitRecords": [{"wins": 57, "losses": 24, "type": "home", "pct": ".704"}],
                "divisionRecords": [
                    {
                        "wins": 17,
                        "losses": 16,
                        "pct": ".515",
                        "division": {
                            "id": 200,
                            "name": "American League West",
                            "link": "/api/v1/divisions/200",
                        },
                    }
                ],
                "overallRecords": [{"wins": 57, "losses": 24, "type": "home", "pct": ".704"}],
                "leagueRecords": [
                    {
                        "wins": 89,
                        "losses": 53,
                        "pct": ".627",
                        "league": {
                            "id": 103,
                            "name": "American League",
                            "link": "/api/v1/league/103",
                        },
                    }
                ],
                "expectedRecords": [
                    {"wins": 106, "losses": 56, "type": "xWinLoss", "pct": ".654"}
                ],
            },
            "runsAllowed": 567,
            "runsScored": 807,
            "divisionChamp": True,
            "divisionLeader": True,
            "hasWildcard": True,
            "clinched": True,
            "eliminationNumber": "-",
            "eliminationNumberSport": "E",
            "eliminationNumberLeague": "E",
            "eliminationNumberDivision": "-",
            "eliminationNumberConference": "E",
            "wildCardEliminationNumber": "-",
            "magicNumber": "-",
            "wins": 99,
            "losses": 63,
            "runDifferential": 240,
            "winningPercentage": ".611",
        }
    ],
}


def test_parse_standings():
    """parse_standings reads the MLB standings envelope and returns Standings models."""
    assert parse_standings({}) == []
    assert parse_standings({"records": []}) == []

    standings = parse_standings({"records": [STANDINGS_RECORD]})

    assert standings == [Standings(**STANDINGS_RECORD)]
    assert standings[0].team_records[0].team.name == "Yankees"
