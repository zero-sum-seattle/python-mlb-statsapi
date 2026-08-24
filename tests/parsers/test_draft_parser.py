from mlbstatsapi._parsers.draft import parse_draft
from mlbstatsapi.models.drafts import Round


def test_parse_draft():
    """parse_draft reads the nested drafts.rounds envelope and returns Round models."""
    assert parse_draft({}) == []
    assert parse_draft({"drafts": {}}) == []
    assert parse_draft({"drafts": {"rounds": []}}) == []

    rounds = parse_draft({"drafts": {"rounds": [{"round": "1"}, {"round": "1B"}]}})

    assert rounds == [Round(round="1"), Round(round="1B")]
