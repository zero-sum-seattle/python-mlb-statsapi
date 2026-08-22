import asyncio

from mlbstatsapi import AsyncMlb
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.people import Coach, Person, Player
from mlbstatsapi.models.schedules import Schedule
from mlbstatsapi.models.seasons import Season
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.teams import Team


def test_async_get_team():
    async def scenario():
        async with AsyncMlb() as mlb:
            team = await mlb.get_team(133)

        assert isinstance(team, Team)
        assert team.id == 133

    asyncio.run(scenario())


def test_async_get_team_roster():
    async def scenario():
        async with AsyncMlb() as mlb:
            roster = await mlb.get_team_roster(133)

        assert roster
        assert isinstance(roster[0], Player)

    asyncio.run(scenario())


def test_async_get_team_coaches():
    async def scenario():
        async with AsyncMlb() as mlb:
            coaches = await mlb.get_team_coaches(133)

        assert coaches
        assert isinstance(coaches[0], Coach)

    asyncio.run(scenario())


def test_async_get_person():
    async def scenario():
        async with AsyncMlb() as mlb:
            person = await mlb.get_person(664034)

        assert isinstance(person, Person)
        assert person.id == 664034

    asyncio.run(scenario())


def test_async_get_schedule():
    async def scenario():
        async with AsyncMlb() as mlb:
            schedule = await mlb.get_schedule(date="2022-10-07")

        assert isinstance(schedule, Schedule)
        assert schedule.dates

    asyncio.run(scenario())


def test_async_get_sport():
    async def scenario():
        async with AsyncMlb() as mlb:
            sport = await mlb.get_sport(1)

        assert isinstance(sport, Sport)
        assert sport.id == 1

    asyncio.run(scenario())


def test_async_get_league():
    async def scenario():
        async with AsyncMlb() as mlb:
            league = await mlb.get_league(103)

        assert isinstance(league, League)
        assert league.id == 103

    asyncio.run(scenario())


def test_async_get_division():
    async def scenario():
        async with AsyncMlb() as mlb:
            division = await mlb.get_division(200)

        assert isinstance(division, Division)
        assert division.id == 200

    asyncio.run(scenario())


def test_async_get_season():
    async def scenario():
        async with AsyncMlb() as mlb:
            season = await mlb.get_season("2021")

        assert isinstance(season, Season)
        assert season.season_id == "2021"

    asyncio.run(scenario())
