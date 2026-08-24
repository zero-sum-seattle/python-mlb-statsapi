from mlbstatsapi._parsers.stats import parse_split_stats
from mlbstatsapi.models.stats import Stat


HITTING_SEASON = {
    "type": {"displayName": "season"},
    "group": {"displayName": "hitting"},
    "totalSplits": 1,
    "splits": [
        {
            "season": "2022",
            "stat": {
                "gamesPlayed": 157,
                "atBats": 586,
                "hits": 160,
                "homeRuns": 34,
                "avg": ".273",
            },
            "team": {"id": 108, "name": "Los Angeles Angels", "link": "/api/v1/teams/108"},
            "player": {"id": 660271, "fullName": "Shohei Ohtani", "link": "/api/v1/people/660271"},
        }
    ],
}

PITCHING_SEASON = {
    "type": {"displayName": "season"},
    "group": {"displayName": "pitching"},
    "totalSplits": 1,
    "splits": [
        {
            "season": "2022",
            "stat": {"gamesPlayed": 28, "wins": 15, "losses": 9, "era": "2.33"},
            "team": {"id": 108, "name": "Los Angeles Angels", "link": "/api/v1/teams/108"},
            "player": {"id": 660271, "fullName": "Shohei Ohtani", "link": "/api/v1/people/660271"},
        }
    ],
}


def test_parses_a_single_group_and_type():
    stats = parse_split_stats({"stats": [HITTING_SEASON]})

    assert list(stats) == ["hitting"]
    assert list(stats["hitting"]) == ["season"]
    assert isinstance(stats["hitting"]["season"], Stat)


def test_keys_by_group_then_type():
    stats = parse_split_stats({"stats": [HITTING_SEASON, PITCHING_SEASON]})

    assert set(stats) == {"hitting", "pitching"}
    assert stats["hitting"]["season"].group == "hitting"
    assert stats["pitching"]["season"].group == "pitching"


def test_carries_the_split_payload_through():
    stats = parse_split_stats({"stats": [HITTING_SEASON]})

    split = stats["hitting"]["season"].splits[0]
    assert split.season == "2022"
    assert split.stat.home_runs == 34


def test_missing_stats_key_returns_an_empty_mapping():
    assert parse_split_stats({}) == {}


def test_empty_stats_list_returns_an_empty_mapping():
    assert parse_split_stats({"stats": []}) == {}


def test_empty_body_returns_an_empty_mapping():
    assert parse_split_stats(None) == {}


def test_a_group_with_no_splits_is_skipped():
    """create_split_data drops entries carrying no splits rather than keying an empty Stat."""
    empty = dict(HITTING_SEASON, splits=[])

    assert parse_split_stats({"stats": [empty]}) == {}


def test_a_group_with_no_splits_does_not_suppress_its_siblings():
    empty = dict(HITTING_SEASON, splits=[])

    stats = parse_split_stats({"stats": [empty, PITCHING_SEASON]})

    assert list(stats) == ["pitching"]
