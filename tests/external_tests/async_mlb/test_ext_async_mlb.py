import asyncio

from mlbstatsapi import AsyncMlb
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.schedules import Schedule
from mlbstatsapi.models.teams import Team


def test_async_get_team():
    async def scenario():
        async with AsyncMlb() as mlb:
            team = await mlb.get_team(133)

        assert isinstance(team, Team)
        assert team.id == 133

    asyncio.run(scenario())

def test_async_get_teams():
    async def scenario():
        async with AsyncMlb() as mlb:
            teams = await mlb.get_teams()

        assert isinstance(teams, list)
        assert teams
        assert all(isinstance(team, Team) for team in teams)

    asyncio.run(scenario())


def test_async_get_person():
    async def scenario():
        async with AsyncMlb() as mlb:
            person = await mlb.get_person(664034)

        assert isinstance(person, Person)
        assert person.id == 664034

    asyncio.run(scenario())

def test_async_get_people():
    async def scenario():
        async with AsyncMlb() as mlb:
            people = await mlb.get_people()

        assert isinstance(people, list)
        assert people
        assert all(isinstance(person, Person) for person in people)

    asyncio.run(scenario())


def test_async_get_schedule():
    async def scenario():
        async with AsyncMlb() as mlb:
            schedule = await mlb.get_schedule(date="2022-10-07")

        assert isinstance(schedule, Schedule)
        assert schedule.dates

    asyncio.run(scenario())
