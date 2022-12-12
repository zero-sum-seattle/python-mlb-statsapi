from unittest.mock import patch
import unittest
import requests_mock
import json
import os

from mlbstatsapi.models.standings import Standings
from mlbstatsapi import Mlb

path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_standings = os.path.join(current_directory, "../mock_json/standings/standings.json")
STANDINGS_JSON_FILE = open(path_to_standings, "r", encoding="utf-8-sig").read()

@requests_mock.Mocker()
class TestStandingsMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.standings_mock = json.loads(STANDINGS_JSON_FILE)
    
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_standings(self, m):
        """This test should return a 200 and Round"""

        m.get('https://statsapi.mlb.com/api/v1/standings?leagueId=103&season=2018', json=self.standings_mock,
        status_code=200)
        
        # set league id
        league_id = 103
        # set season
        season = 2018

        # call get_standings return list of standings
        standings = self.mlb.get_standings(league_id, season)

        # Gamepace should not be None
        self.assertIsNotNone(standings)        

        # list should not be empty
        self.assertNotEqual(standings, [])

        # items in list should be standings
        self.assertIsInstance(standings[0], Standings)

        standing = standings[0]

        # sportgamepace should not be none
        self.assertIsNotNone(standing)

        # sportgamepace should have attrs set
        self.assertTrue(standing.standingstype)
        self.assertTrue(standing.lastupdated)