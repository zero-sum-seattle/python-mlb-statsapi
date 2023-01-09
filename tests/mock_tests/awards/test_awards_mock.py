from typing import Dict, List
from unittest.mock import patch
import unittest
import requests_mock
import json
import os


from mlbstatsapi import Mlb
from mlbstatsapi.models.awards import Award


path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_awards = os.path.join(current_directory, "../mock_json/awards/awards.json")
AWARDS_JSON_FILE = open(path_to_awards, "r", encoding="utf-8-sig").read()

@requests_mock.Mocker()
class TestAwardsMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.awards_mock = json.loads(AWARDS_JSON_FILE)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_awards(self, m):
        """This test should return a 200 and Round"""
        m.get('https://statsapi.mlb.com/api/v1/awards/RETIREDUNI_108/recipients?', json=self.awards_mock,
        status_code=200)

        # set draft id
        award_id = "RETIREDUNI_108"

        # call get_draft return list
        awards = self.mlb.get_awards(award_id)

         # draft should not be None
        self.assertIsNotNone(awards)

        # list should not be empty
        self.assertNotEqual(awards, [])

        # items in list should be an award
        self.assertIsInstance(awards[0], Award)

        award = awards[0]

        # award should not be none
        self.assertIsNotNone(award)

        # award should have attrs set
        self.assertTrue(award.id)
        self.assertTrue(award.name)