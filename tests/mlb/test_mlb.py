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
        cls.mlb = Mlb() # Create instance of our baseclass
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlb_adapter_200(self):
        mlbdata = self.mlb._mlb_adapter_v1.get("/divisions") # A static endpoint to just return JSON
        self.assertIsInstance(mlbdata, MlbResult) # Test result is MlbResult class
        self.assertEqual(mlbdata.status_code, 200) # Check HTTP Status 200
        self.assertIsInstance(mlbdata.data, Dict) # Check results are a Dict

    def test_mlb_adapter_500(self):
        """mlb should raise a exception when adapter returns a 500"""
        # bad endpoint should raise exception due to 500
        with self.assertRaises(TheMlbStatsApiException):
            result = self.mlb._mlb_adapter_v1.get(endpoint="teams/133/stats?stats=vsPlayer&group=catching")

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
        test_sport = Sport(id=1,link="/api/v1/sports/1")
        # LOL how did I miss this! let's keep this in for the timing being just for fun, poopulated.
        poopulated_sport = self.mlb.get_object(test_sport)
        self.assertIsInstance(poopulated_sport, Sport) # Test result is List    
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
        cls.mlb = Mlb() # Create instance of our baseclass
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlbdataapi_get_people(self):
        """mlb get_people should return a list of all sport 1 people"""
        mlbdata = self.mlb.get_people()
        self.assertIsInstance(mlbdata, List) # Test result is List
        self.assertIsInstance(mlbdata[0], Person) # Lazy Test to check the list contains instances of Person

    def test_mlb_get_person(self):
        """mlb get_person should return a Person object"""
        person = self.mlb.get_person('664034')
        self.assertIsInstance(person, Person) # Return Ty France Person ID in a List
        self.assertEqual(person.id, 664034) # Confirm the ID is correct

    def test_mlb_failed_get_person(self):
        """mlb get_person should return None for invalid id"""
        person = self.mlb.get_person('664')
        self.assertIsNone(person)

    def test_mlb_get_person_id(self):
        """mlb get_person_id should return a person id"""
        id = self.mlb.get_people_id('Ty France') # Return Ty France Person ID in a List
        self.assertEqual(id, [664034]) # Confirm the ID is correct

    def test_mlb_get_invalid_person_id(self):
        """mlb get_person_id should return empty list for invalid name"""
        id = self.mlb.get_people_id('Joe Blow') # Return Ty France Person ID in a List
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
        self.assertEqual(team.id, 133) # Confirm the ID is correct

    def test_mlbdataapi_get_teams(self):
        """mlb get_teams should return a list of Teams"""
        mlbdata = self.mlb.get_teams()
        self.assertIsInstance(mlbdata, List) # Test result is List
        self.assertIsInstance(mlbdata[0], Team) # Lazy test to check the list contains instance of Team

    def test_mlb_failed_get_team(self):
        """mlb get_team should return None for invalid team id"""
        team = self.mlb.get_team('19999')
        self.assertIsNone(team)

    def test_mlb_get_team_id(self):
        """mlb get_team_id should return a list of matching team id's"""
        id = self.mlb.get_team_id('Mariners') # Return Mariners Team ID in a List
        self.assertEqual(id, [136])

    def test_mlb_get_bad_team_id(self):
        """mlb get_team_id should return a empty list for invalid team name"""
        id = self.mlb.get_team_id('Banananananana') # Return Mariners Team ID in a List
        self.assertEqual(id, [])

class TestMlbGetSport(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb() # Create instance of our baseclass
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_sport(self):
        """mlb get_sport should return a Sport Object"""
        sport = self.mlb.get_sport(1) # Return MLB sport instance
        self.assertIsInstance(sport, Sport) # Confirms that a sport instance is returned
        self.assertEqual(sport.id, 1) # Confirm the ID is correct

    def test_get_sports(self):
        """mlb get_sports should return a list of sport objects"""
        sports = self.mlb.get_sports() # Get all sports as a list[Sport]
        self.assertIsInstance(sports, List) # Test result is List
        self.assertIsInstance(sports[0], Sport) # Lazy Test to check the list contains instances of Sport

    def test_get_sport_id(self):
        """mlb get_sport id should return a sport id"""
        id = self.mlb.get_sport_id('Major League Baseball') # Get the id for MLB
        self.assertEqual(id, [1]) # Confirm the ID is correct

    def test_get_sport_invalid_name(self):
        """mlb get_sport should return a empty list for invalid sport name"""
        id = self.mlb.get_sport_id('NFL') # Get the id for MLB
        self.assertEqual(id, []) # Confirm the ID is correct

class TestMlbGetLeague(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb() # Create instance of our baseclass
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_league(self):
        """mlb get_league should return a League object"""
        league = self.mlb.get_league(103) # Return American League League instance
        self.assertIsInstance(league, League) # Confirms that a League instance is returned
        self.assertEqual(league.id, 103) # Confirm the ID is correct

    def test_get_leagues(self):
        """mlb get_leagues should return a list of Leagues"""
        leagues = self.mlb.get_leagues()
        self.assertIsInstance(leagues, List) # Test result is List
        self.assertIsInstance(leagues[0], League) # Lazy Test to check the list contains instances of League

    def test_get_league_id(self):
        """mlb get_league_id should return a league id"""
        id = self.mlb.get_league_id('American League') # Get the id for American League West
        self.assertEqual(id, [103]) # Confirm the ID is correct

    def test_get_invalid_league_id(self):
        """mlb get_league_id should return a empty list with invalid league name"""
        id = self.mlb.get_league_id('Russian League')
        self.assertEqual(id, [])

class TestMlbGetDivision(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb() # Create instance of our baseclass
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_division(self):
        """mlb get_division should return a Division object"""
        division = self.mlb.get_division(200) # Return MLB division instance
        self.assertIsInstance(division, Division) # Confirms that a division instance is returned
        self.assertEqual(division.id, 200) # Confirm the ID is correct

    def test_get_divisions(self):
        """mlb get_divisions should return a list of Divisions"""
        divisions = self.mlb.get_divisions() # Get all divisions as a list[Division]
        self.assertIsInstance(divisions, List) # Test result is List
        self.assertIsInstance(divisions[0], Division) # Lazy Test to check the list contains instances of Division

    def test_get_division_id(self):
        """mlb get_division_id should return a division id"""
        id = self.mlb.get_division_id('American League West') # Get the id for American League West
        self.assertEqual(id, [200]) # Confirm the ID is correct

    def test_get_division_id(self):
        """mlb get_division_id should return a empty list for invalid division name"""
        id = self.mlb.get_division_id('Canada West') # Get the id for American League West
        self.assertEqual(id, []) # Confirm the ID is correct

class TestMlbGetVenue(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb() # Create instance of our baseclass
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlb_get_venue(self):
        """mlb get_division should return a Division object"""
        venue = self.mlb.get_venue(31) # Return PNC Park venue instance
        self.assertIsInstance(venue, Venue) # Confirms that a venue instance is returned
        self.assertEqual(venue.id, 31) # Confirm the ID is correct

    def test_get_venues(self):
        """mlb get_divisions should return a list of Divisions"""
        venues = self.mlb.get_venues() # Get all venues as a list[Venue]
        self.assertIsInstance(venues, List) # Test result is List
        self.assertIsInstance(venues[0], Venue) # Lazy Test to check the list contains instances of Venue

    def test_mlb_get_venue_id(self):
        """mlb get_division_id should return a division id"""
        id = self.mlb.get_venue_id('PNC Park') # Get the id for PNC Park
        self.assertEqual(id, [31]) # Confirm the ID is correct

    def test_get_venue_id(self):
        """mlb get_division_id should return a empty list for invalid venue name"""
        id = self.mlb.get_venue_id('Highschool Park') # Get the id for American League West
        self.assertEqual(id, []) # Confirm the ID is correct

class TestMlbGetGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb() # Create instance of our baseclass
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlb_get_game(self):
        game = self.mlb.get_game(662242) # Return a game instance of gaem 662242
        self.assertIsInstance(game, Game) # Confirms that a Game instance is returned
        self.assertEqual(game.id, 662242) # Confirm the ID is correct
    
    def test_get_game_playByPlay(self):
        playByPlay = self.mlb.get_game_playByPlay(662242) # Return a game instance of gaem 662242
        self.assertIsInstance(playByPlay, Plays) # Confirms that a Game instance is returned        
    
    def test_get_game_linescore(self):
        linescore = self.mlb.get_game_linescore(662242) # Return a game instance of gaem 662242
        self.assertIsInstance(linescore, Linescore) # Confirms that a Game instance is returned 
    
    def test_get_game_boxscore(self):
        boxscore = self.mlb.get_game_boxscore(662242) # Return a game instance of gaem 662242
        self.assertIsInstance(boxscore, BoxScore) # Confirms that a Game instance is returned 

    def test_get_todays_games_id(self):
        todaysGames = self.mlb.get_todays_game_ids() # Get all divisions as a list[Division]
        self.assertIsInstance(todaysGames, List) # Test result is List 

    def test_get_schedule(self):
        schedule = self.mlb.get_schedule() # Get all divisions as a list[Division]
        self.assertIsInstance(schedule, Schedule) # Test result is List

    def test_get_attendance(self):
        attendance_team_away = self.mlb.get_attendance(teamid=113) # Cincinati Reds 134
        attendance_team_home = self.mlb.get_attendance(teamid=134)
        attendance_season = self.mlb.get_attendance(teamid=113, season=2022)
        self.assertEqual(attendance_team_away.records[0].team.id, 113)
        self.assertEqual(attendance_team_home.records[0].team.id, 134)
        self.assertEqual(attendance_season.records[0].team.id, 113)