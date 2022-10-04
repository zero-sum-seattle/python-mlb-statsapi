from typing import Dict, List
import unittest
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team, Roster
from mlbstatsapi import Mlb
from mlbstatsapi import MlbResult



class TestMlbDataApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()


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

    def test_mlbdataapi_get_teams(self):
        mlbdata = self.mlb.get_teams()
        self.assertIsInstance(mlbdata, List) # Test result is List
        self.assertIsInstance(mlbdata[0], Team) # Lazy test to check the list contains instance of Team

    def test_mlb_get_person_id(self):
        id = self.mlb.get_people_id('Ty France') # Return Ty France Person ID in a List
        self.assertEqual(id, [664034]) # Confirm the ID is correct

    def test_mlb_get_team_id(self):
        id = self.mlb.get_team_id('Mariners') # Return Mariners Team ID in a List
        self.assertEqual(id, [136])

    def test_mlb_get_person(self):
        person = self.mlb.get_person('664034')
        self.assertIsInstance(person[0], Person)
        self.assertEqual(person[0].id, 664034)

    def test_mlb_get_team(self):
        team = self.mlb.get_team('133')
        self.assertIsInstance(team[0], Team)
        self.assertEqual(team[0].id, 133)

    def test_mlb_get_roster(self):
        roster = self.mlb.get_team_roster('133')
        self.assertIsInstance(roster, Roster)
        self.assertEqual(roster.teamId, 133)