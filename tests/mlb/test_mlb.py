from typing import Dict, List
import unittest
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.schedules import Schedule
from mlbstatsapi import Mlb
from mlbstatsapi import MlbResult

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

    def test_mlbdataapi_get_people(self):
        mlbdata = self.mlb.get_people()
        self.assertIsInstance(mlbdata, List) # Test result is List
        self.assertIsInstance(mlbdata[0], Person) # Lazy Test to check the list contains instances of Person

    def test_mlb_get_person(self):
        person = self.mlb.get_person('664034')
        self.assertIsInstance(person, Person) # Return Ty France Person ID in a List
        self.assertEqual(person.id, 664034) # Confirm the ID is correct

    def test_mlb_failed_get_person(self):
        person = self.mlb.get_person('664')
        self.assertIsNone(person)

    def test_mlb_get_person_id(self):
        id = self.mlb.get_people_id('Ty France') # Return Ty France Person ID in a List
        self.assertEqual(id, [664034]) # Confirm the ID is correct

    def test_mlb_get_team_id(self):
        id = self.mlb.get_team_id('Mariners') # Return Mariners Team ID in a List
        self.assertEqual(id, [136])

    def test_mlb_get_team(self):
        team = self.mlb.get_team('133')
        self.assertIsInstance(team, Team)
        self.assertEqual(team.id, 133) # Confirm the ID is correct

    def test_mlbdataapi_get_teams(self):
        mlbdata = self.mlb.get_teams()
        self.assertIsInstance(mlbdata, List) # Test result is List
        self.assertIsInstance(mlbdata[0], Team) # Lazy test to check the list contains instance of Team

    def test_mlb_failed_get_team(self):
        team = self.mlb.get_team('19999')
        self.assertIsNone(team)

    def test_get_schedule(self):
        schedule = self.mlb.get_schedule() # Get all divisions as a list[Division]
        self.assertIsInstance(schedule, Schedule) # Test result is List

    def test_mlb_get_game(self):
        game = self.mlb.get_game(662242) # Return a game instance of gaem 662242
        self.assertIsInstance(game, Game) # Confirms that a Game instance is returned
        self.assertEqual(game.id, 662242) # Confirm the ID is correct

    def test_get_todays_games(self):
        todaysGames = self.mlb.get_todays_games() # Get all divisions as a list[Division]
        self.assertIsInstance(todaysGames, List) # Test result is List       

    def test_mlb_get_venue(self):
        venue = self.mlb.get_venue(31) # Return PNC Park venue instance
        self.assertIsInstance(venue, Venue) # Confirms that a venue instance is returned
        self.assertEqual(venue.id, 31) # Confirm the ID is correct

    def test_get_venues(self):
        venues = self.mlb.get_venues() # Get all venues as a list[Venue]
        self.assertIsInstance(venues, List) # Test result is List
        self.assertIsInstance(venues[0], Venue) # Lazy Test to check the list contains instances of Venue

    def test_mlb_get_venue_id(self):
        id = self.mlb.get_venue_id('PNC Park') # Get the id for PNC Park
        self.assertEqual(id, [31]) # Confirm the ID is correct

    def test_get_sport(self):
        sport = self.mlb.get_sport(1) # Return MLB sport instance
        self.assertIsInstance(sport, Sport) # Confirms that a sport instance is returned
        self.assertEqual(sport.id, 1) # Confirm the ID is correct

    def test_get_sports(self):
        sports = self.mlb.get_sports() # Get all sports as a list[Sport]
        self.assertIsInstance(sports, List) # Test result is List
        self.assertIsInstance(sports[0], Sport) # Lazy Test to check the list contains instances of Sport

    def test_get_sport_id(self):
        id = self.mlb.get_sport_id('Major League Baseball') # Get the id for MLB
        self.assertEqual(id, [1]) # Confirm the ID is correct

    def test_get_league(self):
        league = self.mlb.get_league(103) # Return American League League instance
        self.assertIsInstance(league, League) # Confirms that a League instance is returned
        self.assertEqual(league.id, 103) # Confirm the ID is correct

    def test_get_leagues(self):
        leagues = self.mlb.get_leagues()
        self.assertIsInstance(leagues, List) # Test result is List
        self.assertIsInstance(leagues[0], League) # Lazy Test to check the list contains instances of League

    def test_get_league_id(self):
        id = self.mlb.get_league_id('American League') # Get the id for American League West
        self.assertEqual(id, [103]) # Confirm the ID is correct

    def test_get_division(self):
        division = self.mlb.get_division(200) # Return MLB division instance
        self.assertIsInstance(division, Division) # Confirms that a division instance is returned
        self.assertEqual(division.id, 200) # Confirm the ID is correct

    def test_get_divisions(self):
        divisions = self.mlb.get_divisions() # Get all divisions as a list[Division]
        self.assertIsInstance(divisions, List) # Test result is List
        self.assertIsInstance(divisions[0], Division) # Lazy Test to check the list contains instances of Division

    def test_get_division_id(self):
        id = self.mlb.get_division_id('American League West') # Get the id for American League West
        self.assertEqual(id, [200]) # Confirm the ID is correct

    def test_get_attendance(self):
        attendance_team_away = self.mlb.get_attendance(teamId=113) # Cincinati Reds 134
        attendance_team_home = self.mlb.get_attendance(teamId=134)
        attendance_season = self.mlb.get_attendance(teamId=113, season=2022)
        self.assertEqual(attendance_team_away.records[0].team.id, 113)
        self.assertEqual(attendance_team_home.records[0].team.id, 134)
        self.assertEqual(attendance_season.records[0].team.id, 113)

    def test_get_object(self):
        test_sport = Sport(id=1,link="/api/v1/sports/1")
        poopulated_sport = self.mlb.get_object(test_sport)
        self.assertIsInstance(poopulated_sport, Sport) # Test result is List    
        self.assertEqual(poopulated_sport.id, 1)
        self.assertEqual(poopulated_sport.link, "/api/v1/sports/1")
        self.assertEqual(poopulated_sport.name, 'Major League Baseball')
        self.assertEqual(poopulated_sport.code, 'mlb')
        self.assertEqual(poopulated_sport.abbreviation, 'MLB')
        self.assertEqual(poopulated_sport.sortOrder, 11)
        self.assertEqual(poopulated_sport.activeStatus, True)