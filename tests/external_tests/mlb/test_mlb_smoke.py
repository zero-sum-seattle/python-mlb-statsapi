from mlbstatsapi import Mlb
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.schedules import Schedule
from mlbstatsapi.models.teams import Team


def test_get_team():
    with Mlb() as mlb:
        team = mlb.get_team(133)

    assert isinstance(team, Team)
    assert team.id == 133


def test_get_person():
    with Mlb() as mlb:
        person = mlb.get_person(664034)

    assert isinstance(person, Person)
    assert person.id == 664034


def test_get_schedule():
    with Mlb() as mlb:
        schedule = mlb.get_schedule(date="2022-10-07")

    assert isinstance(schedule, Schedule)
    assert schedule.dates
