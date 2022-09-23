﻿from typing import Dict, List
import unittest
from mlbstatsapi.mlb import MlbDataAdapter, Mlb, MlbResult
from mlbstatsapi.team import Team
from mlbstatsapi.person import Person
from mlbstatsapi.exceptions import TheMlbStatsApiException



class TestMlbDataApi(unittest.TestCase):
    def test_mlb_adapter_200(self):
        mlb = Mlb() # Create instance of our baseclass
        mlbdata = mlb._mlb_adapter.get("/divisions") # A static endpoint to just return JSON
        self.assertIsInstance(mlbdata, MlbResult) # Test result is MlbResult class
        self.assertEqual(mlbdata.status_code, 200) # Check HTTP Status 200
        self.assertIsInstance(mlbdata.data, Dict) # Check results are a Dict

    def test_mlb_adapter_400(self):
        with self.assertRaises(TheMlbStatsApiException): # Fix my damn imports
            mlb = Mlb() # Create instance of our baseclass
            mlbdata = mlb._mlb_adapter.get("/notaendpoint") # A static endpoint to just return JSON

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

