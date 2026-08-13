import pytest
from pydantic import ValidationError

from mlbstatsapi._parsers.schedules import parse_schedule
from mlbstatsapi.models.schedules import Schedule


def test_parse_schedule():
    """parse_schedule builds a Schedule from the full MLB schedule body."""
    assert parse_schedule({}) is None

    payload = {
        "totalItems": 1,
        "totalEvents": 0,
        "totalGames": 1,
        "totalGamesInProgress": 0,
        "dates": [],
    }
    schedule = parse_schedule(payload)

    assert isinstance(schedule, Schedule)
    assert schedule == Schedule(**payload)


def test_parse_schedule_requires_totals():
    """Schedule requires the MLB total* fields from the response body."""
    with pytest.raises(ValidationError):
        parse_schedule({"dates": []})
