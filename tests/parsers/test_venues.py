from mlbstatsapi._parsers.venues import parse_venue, parse_venues
from mlbstatsapi.models.venues import Venue


def test_parse_venues():
    """parse_venues reads the MLB venues envelope and returns Venue models."""
    assert parse_venues({}) == []
    assert parse_venues({"venues": []}) == []

    venues = parse_venues(
        {
            "venues": [
                {"id": 31, "link": "/api/v1/venues/31", "name": "PNC Park"},
                {"id": 1, "link": "/api/v1/venues/1", "name": "Angel Stadium"},
            ]
        }
    )

    assert venues == [
        Venue(id=31, link="/api/v1/venues/31", name="PNC Park"),
        Venue(id=1, link="/api/v1/venues/1", name="Angel Stadium"),
    ]


def test_parse_venue():
    """parse_venue builds a Venue from one venue payload."""
    assert parse_venue({}) is None

    venue = parse_venue({"venues": [{"id": 31, "link": "/api/v1/venues/31", "name": "PNC Park"}]})

    assert isinstance(venue, Venue)
    assert venue == Venue(id=31, link="/api/v1/venues/31", name="PNC Park")
