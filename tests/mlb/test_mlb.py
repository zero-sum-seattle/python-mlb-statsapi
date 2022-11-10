from typing import Dict, List
import unittest

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


class TestMlbDataApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlb_adapter_200(self):
        mlbdata = self.mlb._mlb_adapter_v1.get("/divisions")
        self.assertIsInstance(mlbdata, MlbResult)
        self.assertEqual(mlbdata.status_code, 200)
        self.assertIsInstance(mlbdata.data, Dict)

    def test_mlb_adapter_500(self):
        """mlb should raise a exception when adapter returns a 500"""
        with self.assertRaises(TheMlbStatsApiException):
            self.mlb._mlb_adapter_v1.get(endpoint="teams/133/stats?stats=vsPlayer&group=catching")

    def test_mlb_adapter_400(self):
        """mlb should return a MlbResult object with a empty data, and a status code"""
        # invalid endpoint 
        mlbdata = self.mlb._mlb_adapter_v1.get(endpoint="teams/19990")

        # result.status_code should be 404
        self.assertEqual(mlbdata.status_code, 404)

        # result.data should be None
        self.assertEqual(mlbdata.data, {})

    def test_get_object(self):
        """mlb get_object should return a poopulated object"""
        test_sport = Sport(id=1, link="/api/v1/sports/1")
        poopulated_sport = self.mlb.get_object(test_sport)
        self.assertIsInstance(poopulated_sport, Sport)
        self.assertEqual(poopulated_sport.id, 1)
        self.assertEqual(poopulated_sport.link, "/api/v1/sports/1")
        self.assertEqual(poopulated_sport.name, 'Major League Baseball')
        self.assertEqual(poopulated_sport.code, 'mlb')
        self.assertEqual(poopulated_sport.abbreviation, 'MLB')
        self.assertEqual(poopulated_sport.sortorder, 11)
        self.assertEqual(poopulated_sport.activestatus, True)


class TestMlbGetPeople(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlbdataapi_get_people(self):
        """mlb get_people should return a list of all sport 1 people"""
        mlbdata = self.mlb.get_people()
        self.assertIsInstance(mlbdata, List)
        self.assertIsInstance(mlbdata[0], Person)

    def test_mlbdataapi_get_people_with_sportid(self):
        """mlb get_people should return a list of all sport 1 people"""
        mlbdata = self.mlb.get_people(sport_id=11)
        self.assertIsInstance(mlbdata, List) 
        self.assertIsInstance(mlbdata[0], Person)

    def test_mlb_get_person(self):
        """mlb get_person should return a Person object"""
        person = self.mlb.get_person('664034')
        self.assertIsInstance(person, Person)
        self.assertEqual(person.id, 664034)

    def test_mlb_failed_get_person(self):
        """mlb get_person should return None for invalid id"""
        person = self.mlb.get_person('664')
        self.assertIsNone(person)

    def test_mlb_get_person_id(self):
        """mlb get_person_id should return a person id"""
        id = self.mlb.get_people_id('Ty France')
        self.assertEqual(id, [664034])

    def test_mlb_get_person_id_with_sportid(self):
        """mlb get_person_id should return a person id"""
        id = self.mlb.get_people_id('Fernando Abad', sportid=11) 
        self.assertEqual(id, [472551])

    def test_mlb_get_invalid_person_id(self):
        """mlb get_person_id should return empty list for invalid name"""
        id = self.mlb.get_people_id('Joe Blow')
        self.assertEqual(id, [])


class TestMlbGetTeam(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb() # Create instance of our baseclass
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlb_get_team(self):
        """mlb get_team should return Team object"""
        team = self.mlb.get_team('133')
        self.assertIsInstance(team, Team)
        self.assertEqual(team.id, 133)

    def test_mlbdataapi_get_teams(self):
        """mlb get_teams should return a list of Teams"""
        mlbdata = self.mlb.get_teams()
        self.assertIsInstance(mlbdata, List)
        self.assertIsInstance(mlbdata[0], Team)

    def test_mlbdataapi_get_teams_with_sportid(self):
        """mlb get_teams should return a list of Teams"""
        mlbdata = self.mlb.get_teams(sport_id=16)
        self.assertIsInstance(mlbdata, List)
        self.assertIsInstance(mlbdata[0], Team)

    def test_mlb_failed_get_team(self):
        """mlb get_team should return None for invalid team id"""
        team = self.mlb.get_team('19999')
        self.assertIsNone(team)

    def test_mlb_get_team_id(self):
        """mlb get_team_id should return a list of matching team id's"""
        id = self.mlb.get_team_id('Mariners')
        self.assertEqual(id, [136])

    def test_mlb_get_team_minor_id(self):
        """mlb get_team_id should return a list of matching team id's"""
        id = self.mlb.get_team_id('DSL Brewers 2')
        self.assertEqual(id, [2101])

    def test_mlb_get_bad_team_id(self):
        """mlb get_team_id should return a empty list for invalid team name"""
        id = self.mlb.get_team_id('Banananananana')
        self.assertEqual(id, [])


class TestMlbGetSport(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_sport(self):
        """mlb get_sport should return a Sport Object"""
        sport = self.mlb.get_sport(1)
        self.assertIsInstance(sport, Sport)
        self.assertEqual(sport.id, 1)

    def test_get_sports(self):
        """mlb get_sports should return a list of sport objects"""
        sports = self.mlb.get_sports()
        self.assertIsInstance(sports, List)
        self.assertIsInstance(sports[0], Sport)

    def test_get_sport_id(self):
        """mlb get_sport id should return a sport id"""
        id = self.mlb.get_sport_id('Major League Baseball')
        self.assertEqual(id, [1])

    def test_get_sport_invalid_name(self):
        """mlb get_sport should return a empty list for invalid sport name"""
        id = self.mlb.get_sport_id('NFL')
        self.assertEqual(id, [])


class TestMlbGetLeague(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_league(self):
        """mlb get_league should return a League object"""
        league = self.mlb.get_league(103)
        self.assertIsInstance(league, League)
        self.assertEqual(league.id, 103)

    def test_get_leagues(self):
        """mlb get_leagues should return a list of Leagues"""
        leagues = self.mlb.get_leagues()
        self.assertIsInstance(leagues, List)
        self.assertIsInstance(leagues[0], League)

    def test_get_league_id(self):
        """mlb get_league_id should return a league id"""
        id = self.mlb.get_league_id('American League')
        self.assertEqual(id, [103])

    def test_get_invalid_league_id(self):
        """mlb get_league_id should return a empty list with invalid league name"""
        id = self.mlb.get_league_id('Russian League')
        self.assertEqual(id, [])


class TestMlbGetDivision(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_division(self):
        """mlb get_division should return a Division object"""
        division = self.mlb.get_division(200)
        self.assertIsInstance(division, Division)
        self.assertEqual(division.id, 200)

    def test_get_divisions(self):
        """mlb get_divisions should return a list of Divisions"""
        divisions = self.mlb.get_divisions()
        self.assertIsInstance(divisions, List)
        self.assertIsInstance(divisions[0], Division)

    def test_get_division_id(self):
        """mlb get_division_id should return a division id"""
        id = self.mlb.get_division_id('American League West')
        self.assertEqual(id, [200])

    def test_get_division_fail_id(self):
        """mlb get_division_id should return a empty list for invalid division name"""
        id = self.mlb.get_division_id('Canada West')
        self.assertEqual(id, [])


class TestMlbGetVenue(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlb_get_venue(self):
        """mlb get_division should return a Division object"""
        venue = self.mlb.get_venue(31)
        self.assertIsInstance(venue, Venue)
        self.assertEqual(venue.id, 31)

    def test_get_venues(self):
        """mlb get_divisions should return a list of Divisions"""
        venues = self.mlb.get_venues()
        self.assertIsInstance(venues, List)
        self.assertIsInstance(venues[0], Venue)

    def test_mlb_get_venue_id(self):
        """mlb get_division_id should return a division id"""
        id = self.mlb.get_venue_id('PNC Park')
        self.assertEqual(id, [31])

    def test_get_venue_id(self):
        """mlb get_division_id should return a empty list for invalid venue name"""
        id = self.mlb.get_venue_id('Highschool Park')
        self.assertEqual(id, [])


class TestMlbGetGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlb_get_game(self):
        game = self.mlb.get_game(662242)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.id, 662242)

    def test_get_game_playByPlay(self):
        playbyplay = self.mlb.get_game_play_by_play(662242)
        self.assertIsInstance(playbyplay, Plays)

    def test_get_game_linescore(self):
        linescore = self.mlb.get_game_line_score(662242)
        self.assertIsInstance(linescore, Linescore)

    def test_get_game_boxscore(self):
        boxscore = self.mlb.get_game_box_score(662242)
        self.assertIsInstance(boxscore, BoxScore)

    def test_get_todays_games_id(self):
        todaysGames = self.mlb.get_todays_game_ids()
        self.assertIsInstance(todaysGames, List)

    def test_get_schedule(self):
        schedule = self.mlb.get_schedule()
        self.assertIsInstance(schedule, Schedule)

    def test_get_attendance(self):
        attendance_team_away = self.mlb.get_attendance(team_id=113)
        attendance_team_home = self.mlb.get_attendance(team_id=134)
        attendance_season = self.mlb.get_attendance(team_id=113, season=2022)
        self.assertEqual(attendance_team_away.records[0].team.id, 113)
        self.assertEqual(attendance_team_home.records[0].team.id, 134)
        self.assertEqual(attendance_season.records[0].team.id, 113)
