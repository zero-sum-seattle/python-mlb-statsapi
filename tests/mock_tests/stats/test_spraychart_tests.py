from typing import Dict, List
from unittest.mock import patch
import unittest
import requests_mock
import json
import os

from mlbstatsapi import Mlb
from mlbstatsapi import MlbResult
from mlbstatsapi import TheMlbStatsApiException

# Mocked JSON directory
# TODO Find a better way to structure and handle this :) 
path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_spraychart_file = os.path.join(current_directory, "../mock_json/stats/person/spraychart.json")
path_to_not_found = os.path.join(current_directory, "../mock_json/response/not_found_404.json")
path_to_error = os.path.join(current_directory, "../mock_json/response/error_500.json")

SPRAYCHART = open(path_to_spraychart_file, "r", encoding="utf-8-sig").read()
NOT_FOUND_404 = open(path_to_not_found, "r", encoding="utf-8-sig").read()
ERROR_500 = open(path_to_error, "r", encoding="utf-8-sig").read()

@requests_mock.Mocker()
class TestMlbDataApiMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.player = cls.mlb.get_person(665742)
        cls.pitcher = cls.mlb.get_person(660271)
        cls.mock_hotcoldzone = json.loads(SPRAYCHART)
        cls.error_500 = json.loads(ERROR_500)
        cls.mock_not_found = json.loads(NOT_FOUND_404)

    @classmethod
    def tearDownClass(cls) -> None:
        pass
        
    def test_hitting_play_log_for_player(self, m):
        """get_player_game_stats should return a dict with stats"""
        m.get('https://statsapi.mlb.com/api/v1/people/665742/stats?stats=sprayChart&group=hitting', json=self.mock_hotcoldzone,
        status_code=200)
        self.stats = ['sprayChart']
        self.groups = ['hitting']
        spraychart = self.mlb.get_player_stats(self.player.id, stats=self.stats, groups=self.groups)

        # game_stats should not be None
        self.assertIsNotNone(spraychart)
        
        # game_stats should not be empty dic
        self.assertNotEqual(spraychart, {})

        self.assertTrue(spraychart['stats']['spraychart'])

    def test_pitching_play_log_for_player(self, m):
        """get_player_game_stats should return a dict with stats"""
        m.get('https://statsapi.mlb.com/api/v1/people/660271/stats?stats=sprayChart&group=pitching', json=self.mock_hotcoldzone,
        status_code=200)
        self.stats = ['sprayChart']
        self.groups = ['pitching']
        spraychart = self.mlb.get_player_stats(self.pitcher.id, stats=self.stats, groups=self.groups)

        # game_stats should not be None
        self.assertIsNotNone(spraychart)

        # game_stats should not be empty dic
        self.assertNotEqual(spraychart, {})

        self.assertTrue(spraychart['stats']['spraychart'])