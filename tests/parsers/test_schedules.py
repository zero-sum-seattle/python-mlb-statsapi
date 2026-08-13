import pytest
from pydantic import ValidationError
from mlbstatsapi._parsers.schedules import parse_schedules, parse_schedule
from mlbstatsapi.models.schedules import Schedule

def test_parse_schedules():
    """Test the parse_schedules function"""
    assert parse_schedules({}) == []
    assert parse_schedules({"schedules": []}) == []

    schedules = parse_schedules(
        {
            "schedules": [
                {"id": 1, "name": "Schedule 1"},
                {"id": 2, "name": "Schedule 2"},
            ]
        }
    )

    assert schedules == [
        Schedule(id=1, name="Schedule 1"),
        Schedule(id=2, name="Schedule 2"),
    ]

def test_parse_schedule():
    """Test the parse_schedule function"""
    assert parse_schedule({}) is None

    schedule = parse_schedule({"id": 1, "name": "Schedule 1"})

    assert isinstance(schedule, Schedule)
    assert schedule == Schedule(id=1, name="Schedule 1")

def test_parse_schedule_requires_name():
    """Test the parse_schedule function requires name"""
    with pytest.raises(ValidationError):
        parse_schedule({"id": 1})