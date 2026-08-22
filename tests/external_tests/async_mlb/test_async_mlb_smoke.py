import asyncio

from mlbstatsapi import AsyncMlb
from mlbstatsapi.models.attendances import Attendance
from mlbstatsapi.models.awards import Award
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.drafts import Round
from mlbstatsapi.models.game import BoxScore, Game, Linescore, Plays
from mlbstatsapi.models.homerunderby import HomeRunDerby
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.people import Coach, Person, Player
from mlbstatsapi.models.schedules import Schedule
from mlbstatsapi.models.seasons import Season
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.standings import Standings
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.venues import Venue


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


def test_async_get_venue():
    async def scenario():
        async with AsyncMlb() as mlb:
            venue = await mlb.get_venue(31)

        assert isinstance(venue, Venue)
        assert venue.id == 31

    asyncio.run(scenario())


def test_async_get_standings():
    async def scenario():
        async with AsyncMlb() as mlb:
            standings = await mlb.get_standings(103, "2022")

        assert standings
        assert isinstance(standings[0], Standings)

    asyncio.run(scenario())


def test_async_get_attendance():
    async def scenario():
        async with AsyncMlb() as mlb:
            attendance = await mlb.get_attendance(team_id=133, season=2022)

        assert isinstance(attendance, Attendance)

    asyncio.run(scenario())


def test_async_get_draft():
    async def scenario():
        async with AsyncMlb() as mlb:
            rounds = await mlb.get_draft(2019)

        assert rounds
        assert isinstance(rounds[0], Round)

    asyncio.run(scenario())


def test_async_get_awards():
    async def scenario():
        async with AsyncMlb() as mlb:
            awards = await mlb.get_awards("ALMVP")

        assert awards
        assert isinstance(awards[0], Award)

    asyncio.run(scenario())


def test_async_get_homerun_derby():
    async def scenario():
        async with AsyncMlb() as mlb:
            derby = await mlb.get_homerun_derby(511101)

        assert isinstance(derby, HomeRunDerby)

    asyncio.run(scenario())


def test_async_get_team_id():
    async def scenario():
        async with AsyncMlb() as mlb:
            ids = await mlb.get_team_id("Athletics")

        assert ids == [133]

    asyncio.run(scenario())


def test_async_get_people_id():
    async def scenario():
        async with AsyncMlb() as mlb:
            ids = await mlb.get_people_id("Ty France")

        assert ids == [664034]

    asyncio.run(scenario())


def test_async_get_sport_id():
    async def scenario():
        async with AsyncMlb() as mlb:
            ids = await mlb.get_sport_id("Major League Baseball")

        assert ids == [1]

    asyncio.run(scenario())


def test_async_get_league_id():
    async def scenario():
        async with AsyncMlb() as mlb:
            ids = await mlb.get_league_id("American League")

        assert ids == [103]

    asyncio.run(scenario())


def test_async_get_division_id():
    async def scenario():
        async with AsyncMlb() as mlb:
            ids = await mlb.get_division_id("American League West")

        assert ids == [200]

    asyncio.run(scenario())


def test_async_get_venue_id():
    async def scenario():
        async with AsyncMlb() as mlb:
            ids = await mlb.get_venue_id("PNC Park")

        assert ids == [31]

    asyncio.run(scenario())


def test_async_get_game():
    async def scenario():
        async with AsyncMlb() as mlb:
            game = await mlb.get_game(717911)

        assert isinstance(game, Game)
        assert game.id == 717911

    asyncio.run(scenario())


def test_async_get_game_play_by_play():
    async def scenario():
        async with AsyncMlb() as mlb:
            plays = await mlb.get_game_play_by_play(717911)

        assert isinstance(plays, Plays)
        assert plays.all_plays

    asyncio.run(scenario())


def test_async_get_game_line_score():
    async def scenario():
        async with AsyncMlb() as mlb:
            linescore = await mlb.get_game_line_score(717911)

        assert isinstance(linescore, Linescore)

    asyncio.run(scenario())


def test_async_get_game_box_score():
    async def scenario():
        async with AsyncMlb() as mlb:
            boxscore = await mlb.get_game_box_score(717911)

        assert isinstance(boxscore, BoxScore)

    asyncio.run(scenario())


def test_async_get_game_ids():
    async def scenario():
        async with AsyncMlb() as mlb:
            ids = await mlb.get_game_ids(date="2023-06-03")

        assert 717911 in ids

    asyncio.run(scenario())
