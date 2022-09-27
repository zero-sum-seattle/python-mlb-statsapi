from typing import Dict, List
import unittest
from mlbstatsapi.mlbapi import *
from mlbstatsapi.mlb import *
from mlbstatsapi.exceptions import TheMlbStatsApiException



class TestMlbDataApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass


    def test_mlb_adapter_200(self):
        mlb = Mlb() # Create instance of our baseclass
        mlbdata = mlb._mlb_adapter_v1.get("/divisions") # A static endpoint to just return JSON
        self.assertIsInstance(mlbdata, MlbResult) # Test result is MlbResult class
        self.assertEqual(mlbdata.status_code, 200) # Check HTTP Status 200
        self.assertIsInstance(mlbdata.data, Dict) # Check results are a Dict

    def test_mlb_adapter_400(self):
        mlb = Mlb() # Create instance of our baseclass
        mlbdata = mlb._mlb_adapter_v1.get("/notaendpoint") # A static endpoint to just return JSON
        self.assertEqual(mlbdata.status_code, 404)
        self.assertEqual(mlbdata.message, "Not Found")
        self.assertEqual(mlbdata.data, [])

    def test_mlbdataapi_get_people(self):
        mlb = Mlb()
        mlbdata = mlb.get_people()
        self.assertIsInstance(mlbdata, List) # Test result is List
        self.assertIsInstance(mlbdata[0], Person) # Lazy Test to check the list contains instances of Person

    def test_mlbdataapi_get_teams(self):
        mlb = Mlb()
        mlbdata = mlb.get_teams()
        self.assertIsInstance(mlbdata, List) # Test result is List
        self.assertIsInstance(mlbdata[0], Team) # Lazy test to check the list contains instance of Team

    def test_mlb_get_person_id(self):
        mlb = Mlb()
        id = mlb.get_people_id('Ty France') # Return Ty France Person ID in a List
        self.assertEqual(id, [664034]) # Confirm the ID is correct

    def test_mlb_get_team_id(self):
        mlb = Mlb()
        id = mlb.get_team_id('Mariners') # Return Mariners Team ID in a List
        self.assertEqual(id, [136])

    def test_mlb_get_person(self):
        mlb = Mlb()
        person = mlb.get_person('664034')
        self.assertIsInstance(person[0], Person)
        self.assertEqual(person[0].id, 664034)

    def test_mlb_get_team(self):
        mlb = Mlb()
        team = mlb.get_team('133')
        self.assertIsInstance(team[0], Team)
        self.assertEqual(team[0].id, 133)

    def test_mlb_get_game(self):
        mlb = Mlb()
        game = mlb.get_game(662242)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.id, 662242)
