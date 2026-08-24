from mlbstatsapi._parsers.seasons import parse_season, parse_seasons
from mlbstatsapi.models.seasons import Season


def test_parse_seasons():
    """parse_seasons reads the MLB seasons envelope and returns Season models."""
    assert parse_seasons({}) == []
    assert parse_seasons({"seasons": []}) == []

    seasons = parse_seasons(
        {
            "seasons": [
                {"seasonId": "2021", "hasWildcard": True},
                {"seasonId": "2022", "hasWildcard": True},
            ]
        }
    )

    assert seasons == [
        Season(seasonId="2021", hasWildcard=True),
        Season(seasonId="2022", hasWildcard=True),
    ]


def test_parse_season():
    """parse_season builds a Season from one season payload."""
    assert parse_season({}) is None

    season = parse_season({"seasons": [{"seasonId": "2021", "hasWildcard": True}]})

    assert isinstance(season, Season)
    assert season == Season(seasonId="2021", hasWildcard=True)
