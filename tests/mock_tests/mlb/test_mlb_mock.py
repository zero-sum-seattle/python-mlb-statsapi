from typing import Dict, List
from unittest.mock import patch
import unittest
import requests_mock
import json
import os

from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game, Plays, Linescore, BoxScore
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.schedules import Schedule

from mlbstatsapi import Mlb
from mlbstatsapi import MlbResult
from mlbstatsapi import TheMlbStatsApiException

# Mocked JSON directory
# TODO Find a better way to structure and handle this :) 
path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_teams_file = os.path.join(current_directory, "../mock_json/teams/teams.json")
path_to_oakland_file = os.path.join(current_directory, "../mock_json/teams/team.json")
path_to_players_file = os.path.join(current_directory, "../mock_json/people/players.json")
path_to_person_file = os.path.join(current_directory, "../mock_json/people/person_mock.json")
path_to_not_found = os.path.join(current_directory, "../mock_json/response/not_found_404.json")
path_to_error = os.path.join(current_directory, "../mock_json/response/error_500.json")
path_to_divisions = os.path.join(current_directory, "../mock_json/divisions/divisions.json")
path_to_division = os.path.join(current_directory, "../mock_json/divisions/division.json")
path_to_sports = os.path.join(current_directory, "../mock_json/sports/sports.json")
path_to_sports = os.path.join(current_directory, "../mock_json/sports/sport.json")
path_to_leagues = os.path.join(current_directory, "../mock_json/leagues/leagues.json")
path_to_league = os.path.join(current_directory, "../mock_json/leagues/league.json")
path_to_venues = os.path.join(current_directory, "../mock_json/venues/venues.json")
path_to_venue = os.path.join(current_directory, "../mock_json/venues/venue.json")
path_to_game = os.path.join(current_directory, "../mock_json/games/game.json")


LEAGUES_JSON_FILE = open(path_to_leagues, "r", encoding="utf-8-sig").read()
LEAGUE_JSON_FILE = open(path_to_league, "r", encoding="utf-8-sig").read()
SPORTS_JSON_FILE = open(path_to_sports, "r", encoding="utf-8-sig").read()
SPORT_JSON_FILE = open(path_to_sports, "r", encoding="utf-8-sig").read()
TEAMS_JSON_FILE = open(path_to_teams_file, "r", encoding="utf-8-sig").read()
TEAM_JSON_FILE = open(path_to_oakland_file, "r", encoding="utf-8-sig").read()
PEOPLE_JSON_FILE = open(path_to_players_file, "r", encoding="utf-8-sig").read()
PERSON_JSON_FILE = open(path_to_person_file, "r", encoding="utf-8-sig").read()
DIVISIONS_JSON_FILE = open(path_to_divisions, "r", encoding="utf-8-sig").read()
DIVISION_JSON_FILE = open(path_to_division, "r", encoding="utf-8-sig").read()
VENUES_JSON_FILE = open(path_to_venues, "r", encoding="utf-8-sig").read()
VENUE_JSON_FILE = open(path_to_venue, "r", encoding="utf-8-sig").read()
GAME_JSON_FILE = open(path_to_game, "r", encoding="utf-8-sig").read()
NOT_FOUND_404 = open(path_to_not_found, "r", encoding="utf-8-sig").read()
ERROR_500 = open(path_to_error, "r", encoding="utf-8-sig").read()


@requests_mock.Mocker()
class TestMlbDataApiMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.mock_divisions = json.loads(DIVISIONS_JSON_FILE)
        cls.error_500 = json.loads(ERROR_500)
        cls.mock_not_found = json.loads(NOT_FOUND_404)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlb_adapter_200(self, m):
        m.get('https://statsapi.mlb.com/api/v1/divisions', json=self.mock_divisions,
        status_code=200)

        mlbdata = self.mlb._mlb_adapter_v1.get("divisions")
        self.assertIsInstance(mlbdata, MlbResult)
        self.assertEqual(mlbdata.status_code, 200)
        self.assertIsInstance(mlbdata.data, Dict)

    def test_mlb_adapter_500(self, m):
        """mlb should raise a exception when adapter returns a 500"""
        m.get('https://statsapi.mlb.com/api/v1/teams/133/stats?stats=vsPlayer&group=catching',
        json=self.mock_divisions, status_code=500)
        with self.assertRaises(TheMlbStatsApiException):
            self.mlb._mlb_adapter_v1.get(endpoint="teams/133/stats?stats=vsPlayer&group=catching")

    def test_mlb_adapter_400(self, m):
        """mlb should return a MlbResult object with a empty data, and a status code"""
        m.get('https://statsapi.mlb.com/api/v1/teams/19990', json=self.mock_not_found,
        status_code=404)
        # invalid endpoint 
        mlbdata = self.mlb._mlb_adapter_v1.get(endpoint="teams/19990")

        # result.status_code should be 404
        self.assertEqual(mlbdata.status_code, 404)

        # result.data should be None
        self.assertEqual(mlbdata.data, {})


@requests_mock.Mocker()
class TestMlbGetPeopleMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.mock_people = json.loads(PEOPLE_JSON_FILE)
        cls.mock_person = json.loads(PERSON_JSON_FILE)
        cls.mock_not_found = json.loads(NOT_FOUND_404)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlbdataapi_get_people(self, m):
        """mlb get_people should return a list of all sport 1 people"""
        m.get('https://statsapi.mlb.com/api/v1/sports/1/players', json=self.mock_people,
        status_code=200)
        mlbdata = self.mlb.get_people()
        self.assertIsInstance(mlbdata, List)
        self.assertIsInstance(mlbdata[0], Person)

    def test_mlbdataapi_get_people_with_sportid(self, m):
        """mlb get_people should return a list of all sport 1 people"""
        m.get('https://statsapi.mlb.com/api/v1/sports/11/players', json=self.mock_people,
        status_code=200)
        mlbdata = self.mlb.get_people(sport_id=11)
        self.assertIsInstance(mlbdata, List)
        self.assertIsInstance(mlbdata[0], Person)

    def test_mlb_get_person(self, m):
        """mlb get_person should return a Person object"""
        m.get('https://statsapi.mlb.com/api/v1/people/676265', json=self.mock_people,
        status_code=200)
        person = self.mlb.get_person('676265')
        self.assertIsInstance(person, Person)
        self.assertEqual(person.id, 676265)

    def test_mlb_failed_get_person(self, m):
        """mlb get_person should return None and 404 for invalid id"""
        m.get('https://statsapi.mlb.com/api/v1/people/664', json=self.mock_not_found,
        status_code=404)
        person = self.mlb.get_person('664')
        self.assertIsNone(person)

    def test_mlb_get_person_id(self, m):
        """mlb get_person_id should return a person id"""
        m.get('https://statsapi.mlb.com/api/v1/sports/1/players', json=self.mock_people,
        status_code=200)
        id = self.mlb.get_people_id('CJ Abrams')
        self.assertEqual(id, [682928])

    def test_mlb_get_person_id_with_sportid(self, m):
        """mlb get_person_id should return a person id"""
        m.get('https://statsapi.mlb.com/api/v1/sports/11/players', json=self.mock_people,
        status_code=200)
        id = self.mlb.get_people_id('Albert Abreu', sport_id=11)
        self.assertEqual(id, [656061])

    def test_mlb_get_invalid_person_id(self, m):
        m.get('https://statsapi.mlb.com/api/v1/sports/1/players', json=self.mock_people,
        status_code=200)
        """mlb get_person_id should return empty list for invalid name"""
        id = self.mlb.get_people_id('Joe Blow')
        self.assertEqual(id, [])


@requests_mock.Mocker()
class TestMlbGetTeamMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.mock_teams = json.loads(TEAMS_JSON_FILE)
        cls.mock_team = json.loads(TEAM_JSON_FILE)
        cls.mock_not_found = json.loads(NOT_FOUND_404)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlb_get_team(self, m):
        """mlb get_team should return Team object"""
        m.get('https://statsapi.mlb.com/api/v1/teams/133', json=self.mock_team,
        status_code=200)

        team = self.mlb.get_team('133')
        self.assertIsInstance(team, Team)
        self.assertEqual(team.id, 133)

    def test_mlbdataapi_get_teams(self, m):
        """mlb get_teams should return a list of Teams"""
        m.get('https://statsapi.mlb.com/api/v1/teams', json=self.mock_teams)

        mlbdata = self.mlb.get_teams()
        self.assertIsInstance(mlbdata, List)
        self.assertIsInstance(mlbdata[0], Team)

    def test_mlbdataapi_get_teams_with_sportid(self, m):
        """mlb get_teams should return a list of Teams"""
        m.get('https://statsapi.mlb.com/api/v1/teams', json=self.mock_teams)
        mlbdata = self.mlb.get_teams(sport_id=16)
        self.assertIsInstance(mlbdata, List)
        self.assertIsInstance(mlbdata[0], Team)

    def test_mlb_failed_get_team(self, m):
        """mlb get_team should return None for invalid team id"""
        m.get('https://statsapi.mlb.com/api/v1/teams/19999', json=self.mock_not_found,
        status_code=404)
        team = self.mlb.get_team('19999')
        self.assertIsNone(team)

    def test_mlb_get_team_id(self, m):
        """mlb get_team_id should return a list of matching team id's"""
        m.get('https://statsapi.mlb.com/api/v1/teams', json=self.mock_teams,
        status_code=200)

        id = self.mlb.get_team_id('Seattle Mariners')
        self.assertEqual(id, [136])

    def test_mlb_get_team_minor_id(self, m):
        """mlb get_team_id should return a list of matching team id's"""
        m.get('https://statsapi.mlb.com/api/v1/teams', json=self.mock_teams,
        status_code=200)

        id = self.mlb.get_team_id('DSL Brewers 2')
        self.assertEqual(id, [2101])

    def test_mlb_get_bad_team_id(self, m):
        """mlb get_team_id should return a empty list for invalid team name"""
        m.get('https://statsapi.mlb.com/api/v1/teams', json=self.mock_teams,
        status_code=200)
        id = self.mlb.get_team_id('Banananananana')
        self.assertEqual(id, [])


@requests_mock.Mocker()
class TestMlbGetSport(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.mock_sports = json.loads(SPORTS_JSON_FILE)
        cls.mock_sport = json.loads(SPORT_JSON_FILE)
        cls.mock_not_found = json.loads(NOT_FOUND_404)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_sport(self, m):
        """mlb get_sport should return a Sport Object"""
        m.get('https://statsapi.mlb.com/api/v1/sports/1', json=self.mock_sport,
        status_code=200)
        sport = self.mlb.get_sport(1)
        self.assertIsInstance(sport, Sport)
        self.assertEqual(sport.id, 1)

    def test_get_sports(self, m):
        """mlb get_sports should return a list of sport objects"""
        m.get('https://statsapi.mlb.com/api/v1/sports', json=self.mock_sports,
        status_code=200)
        sports = self.mlb.get_sports()
        self.assertIsInstance(sports, List)
        self.assertIsInstance(sports[0], Sport)

    def test_get_sport_id(self, m):
        """mlb get_sport id should return a sport id"""
        m.get('https://statsapi.mlb.com/api/v1/sports', json=self.mock_sports,
        status_code=200)
        id = self.mlb.get_sport_id('Major League Baseball')
        self.assertEqual(id, [1])

    def test_get_sport_invalid_name(self, m):
        """mlb get_sport should return a empty list for invalid sport name"""
        m.get('https://statsapi.mlb.com/api/v1/sports', json=self.mock_sports,
        status_code=200)
        id = self.mlb.get_sport_id('NFL')
        self.assertEqual(id, [])


@requests_mock.Mocker()
class TestMlbGetLeagueMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.mock_leagues = json.loads(LEAGUES_JSON_FILE)
        cls.mock_league = json.loads(LEAGUE_JSON_FILE)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_league(self, m):
        """mlb get_league should return a League object"""
        m.get('https://statsapi.mlb.com/api/v1/leagues/103', json=self.mock_league,
        status_code=200)
        league = self.mlb.get_league(103)
        self.assertIsInstance(league, League)
        self.assertEqual(league.id, 103)

    def test_get_leagues(self, m):
        """mlb get_leagues should return a list of Leagues"""
        m.get('https://statsapi.mlb.com/api/v1/leagues', json=self.mock_leagues,
        status_code=200)
        leagues = self.mlb.get_leagues()
        self.assertIsInstance(leagues, List)
        self.assertIsInstance(leagues[0], League)

    def test_get_league_id(self, m):
        """mlb get_league_id should return a league id"""
        m.get('https://statsapi.mlb.com/api/v1/leagues', json=self.mock_leagues,
        status_code=200)
        id = self.mlb.get_league_id('American League')
        self.assertEqual(id, [103])

    def test_get_invalid_league_id(self, m):
        """mlb get_league_id should return a empty list with invalid league name"""
        m.get('https://statsapi.mlb.com/api/v1/leagues', json=self.mock_leagues,
        status_code=200)
        id = self.mlb.get_league_id('Russian League')
        self.assertEqual(id, [])


@requests_mock.Mocker()
class TestMlbGetDivision(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.mock_divisions = json.loads(DIVISIONS_JSON_FILE)
        cls.mock_division = json.loads(DIVISION_JSON_FILE)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_division(self, m):
        """mlb get_division should return a Division object"""
        m.get('https://statsapi.mlb.com/api/v1/divisions/200', json=self.mock_division,
        status_code=200)
        division = self.mlb.get_division(200)
        self.assertIsInstance(division, Division)
        self.assertEqual(division.id, 200)

    def test_get_divisions(self, m):
        """mlb get_divisions should return a list of Divisions"""
        m.get('https://statsapi.mlb.com/api/v1/divisions', json=self.mock_divisions,
        status_code=200)
        divisions = self.mlb.get_divisions()
        self.assertIsInstance(divisions, List)
        self.assertIsInstance(divisions[0], Division)

    def test_get_division_id(self, m):
        """mlb get_division_id should return a division id"""
        m.get('https://statsapi.mlb.com/api/v1/divisions', json=self.mock_divisions,
        status_code=200)
        id = self.mlb.get_division_id('American League West')
        self.assertEqual(id, [200])

    def test_get_division_fail_id(self, m):
        m.get('https://statsapi.mlb.com/api/v1/divisions', json=self.mock_divisions,
        status_code=200)
        """mlb get_division_id should return a empty list for invalid division name"""
        id = self.mlb.get_division_id('Canada West')
        self.assertEqual(id, [])


@requests_mock.Mocker()
class TestMlbGetVenue(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.mock_venues = json.loads(VENUES_JSON_FILE)
        cls.mock_venue = json.loads(VENUE_JSON_FILE)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlb_get_venue(self, m):
        """mlb get_division should return a Division object"""
        m.get('https://statsapi.mlb.com/api/v1/venues/31', json=self.mock_venue,
        status_code=200)
        venue = self.mlb.get_venue(31)
        self.assertIsInstance(venue, Venue)
        self.assertEqual(venue.id, 31)

    def test_get_venues(self, m):
        """mlb get_divisions should return a list of Divisions"""
        m.get('https://statsapi.mlb.com/api/v1/venues', json=self.mock_venues,
        status_code=200)
        venues = self.mlb.get_venues()
        self.assertIsInstance(venues, List)
        self.assertIsInstance(venues[0], Venue)

    def test_mlb_get_venue_id(self, m):
        """mlb get_division_id should return a division id"""
        """mlb get_divisions should return a list of Divisions"""
        m.get('https://statsapi.mlb.com/api/v1/venues', json=self.mock_venues,
        status_code=200)
        id = self.mlb.get_venue_id('PNC Park')
        self.assertEqual(id, [31])

    def test_get_venue_id(self, m):
        """mlb get_division_id should return a empty list for invalid venue name"""
        """mlb get_divisions should return a list of Divisions"""
        m.get('https://statsapi.mlb.com/api/v1/venues', json=self.mock_venues,
        status_code=200)
        id = self.mlb.get_venue_id('Highschool Park')
        self.assertEqual(id, [])

@requests_mock.Mocker()
class TestMlbGetGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.mock_game = json.loads(GAME_JSON_FILE)
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlb_get_game(self, m):
        """mlb get_game should return a Game object"""
        m.get('https://statsapi.mlb.com/api/v1.1/game/715720/feed/live', json=self.mock_game,
        status_code=200)
        game = self.mlb.get_game(715720)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.id, 715720)

    # def test_get_game_playByPlay(self):
    #     playbyplay = self.mlb.get_game_play_by_play(662242)
    #     self.assertIsInstance(playbyplay, Plays)

    # def test_get_game_linescore(self):
    #     linescore = self.mlb.get_game_line_score(662242)
    #     self.assertIsInstance(linescore, Linescore)

    # def test_get_game_boxscore(self):
    #     boxscore = self.mlb.get_game_box_score(662242)
    #     self.assertIsInstance(boxscore, BoxScore)

    # def test_get_todays_games_id(self):
    #     todaysGames = self.mlb.get_todays_game_ids()
    #     self.assertIsInstance(todaysGames, List)

    # def test_get_attendance(self):
    #     params = {'season': 2022}
    #     attendance_team_away = self.mlb.get_attendance(team_id=113)
    #     attendance_team_home = self.mlb.get_attendance(team_id=134)
    #     attendance_season = self.mlb.get_attendance(team_id=113, params=params)
    #     self.assertEqual(attendance_team_away.records[0].team.id, 113)
    #     self.assertEqual(attendance_team_home.records[0].team.id, 134)
    #     self.assertEqual(attendance_season.records[0].team.id, 113)
