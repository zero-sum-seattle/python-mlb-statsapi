from typing import Dict, List
from unittest.mock import patch
import unittest
import requests_mock
import json
import os


from mlbstatsapi import Mlb
from mlbstatsapi.models.gamepace import Gamepace, Gamepacedata


path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_gamepace = os.path.join(current_directory, "../mock_json/gamepace/gamepace.json")
GAMEPACE_JSON_FILE = open(path_to_gamepace, "r", encoding="utf-8-sig").read()

@requests_mock.Mocker()
class TestGamepaceMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.gamepace_mock = json.loads(GAMEPACE_JSON_FILE)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_gamepace(self, m):
        """This test should return a 200 and Round"""
        m.get('https://statsapi.mlb.com/api/v1/gamePace?season=2021', json=self.gamepace_mock,
        status_code=200)

        # set draft id
        season_id = 2021

        # call get_gamepace return Gamepace object
        gamepace = self.mlb.get_gamepace(season_id)

        # Gamepace should not be None
        self.assertIsNotNone(gamepace)

        self.assertIsInstance(gamepace, Gamepace)

        # list should not be empty
        self.assertNotEqual(gamepace.sports, [])

        # items in list should be gamepace data
        self.assertIsInstance(gamepace.sports[0], Gamepacedata)

        sportgamepace = gamepace.sports[0]

        # sportgamepace should not be none
        self.assertIsNotNone(sportgamepace)

        # sportgamepace should have attrs set
        self.assertTrue(sportgamepace.hitspergame)
        self.assertTrue(sportgamepace.totalgames)