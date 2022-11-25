import unittest
import requests_mock
import json
import os

from mlbstatsapi import Mlb


# Mocked JSON directory
# TODO Find a better way to structure and handle this :) 
path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_hotcoldzone_file = os.path.join(current_directory, "../mock_json/stats/person/hotcoldzone.json")
path_to_not_found = os.path.join(current_directory, "../mock_json/response/not_found_404.json")
path_to_error = os.path.join(current_directory, "../mock_json/response/error_500.json")

HOTCOLDZONE = open(path_to_hotcoldzone_file, "r", encoding="utf-8-sig").read()
NOT_FOUND_404 = open(path_to_not_found, "r", encoding="utf-8-sig").read()
ERROR_500 = open(path_to_error, "r", encoding="utf-8-sig").read()

@requests_mock.Mocker()
class TestMlbDataApiMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.player = cls.mlb.get_person(665742)
        cls.pitcher = cls.mlb.get_person(660271)
        cls.mock_hotcoldzone = json.loads(HOTCOLDZONE)
        cls.error_500 = json.loads(ERROR_500)
        cls.mock_not_found = json.loads(NOT_FOUND_404)

    @classmethod
    def tearDownClass(cls) -> None:
        pass
        
    def test_hitting_play_log_for_player(self, m):
        """get_player_game_stats should return a dict with stats"""
        m.get('https://statsapi.mlb.com/api/v1/people/665742/stats?stats=hotColdZones&group=hitting', json=self.mock_hotcoldzone,
        status_code=200)
        self.stats = ['hotColdZones']
        self.groups = ['hitting']
        hotcoldzones = self.mlb.get_player_stats(self.player.id, stats=self.stats, groups=self.groups)

        # game_stats should not be None
        self.assertIsNotNone(hotcoldzones)
        
        # game_stats should not be empty dic
        self.assertNotEqual(hotcoldzones, {})

        self.assertTrue(hotcoldzones['stats']['hotcoldzones'])

        hotcoldzone = hotcoldzones['stats']['hotcoldzones'][0]

        # should not be empty
        self.assertTrue(hotcoldzone.stat)

        for zone in hotcoldzone.zones:
            self.assertTrue(zone.zone)

    def test_pitching_play_log_for_player(self, m):
        """get_player_game_stats should return a dict with stats"""
        m.get('https://statsapi.mlb.com/api/v1/people/660271/stats?stats=hotColdZones&group=pitching', json=self.mock_hotcoldzone,
        status_code=200)
        self.stats = ['hotColdZones']
        self.groups = ['pitching']
        hotcoldzones = self.mlb.get_player_stats(self.pitcher.id, stats=self.stats, groups=self.groups)

        # game_stats should not be None
        self.assertIsNotNone(hotcoldzones)

        # game_stats should not be empty dic
        self.assertNotEqual(hotcoldzones, {})

        # should not be empty
        self.assertTrue(hotcoldzones['stats']['hotcoldzones'])

        hotcoldzone = hotcoldzones['stats']['hotcoldzones'][0]

        # should not be empty
        self.assertTrue(hotcoldzone.stat)

        for zone in hotcoldzone.zones:
            self.assertTrue(zone.zone)



