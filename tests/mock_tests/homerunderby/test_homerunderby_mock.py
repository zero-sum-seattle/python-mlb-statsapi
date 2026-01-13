from typing import Dict, List
from unittest.mock import patch
import unittest
import requests_mock
import json
import os


from mlbstatsapi import Mlb
from mlbstatsapi.models.homerunderby import HomeRunDerby, Round


path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_homerunderby = os.path.join(current_directory, "../mock_json/homerunderby/homerunderby.json")
HOMERUNDERBY_JSON_FILE = open(path_to_homerunderby, "r", encoding="utf-8-sig").read()

@requests_mock.Mocker()
class TestHomerunderbyMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.homerunderby_mock = json.loads(HOMERUNDERBY_JSON_FILE)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_homerunderby(self, m):
        """This test should return a 200 and Round"""
        m.get('https://statsapi.mlb.com/api/v1/homeRunDerby/511101', json=self.homerunderby_mock,
        status_code=200)

         # set game id
        game_id = 511101

        # call get_homerun_derby return HomeRunDerby object
        derby = self.mlb.get_homerun_derby(game_id)

        # HomeRunDerby should not be None
        self.assertIsNotNone(derby)

        self.assertIsInstance(derby, HomeRunDerby)

        # list should not be empty
        self.assertNotEqual(derby.rounds, [])

        # items in list should be Round
        self.assertIsInstance(derby.rounds[0], Round)
