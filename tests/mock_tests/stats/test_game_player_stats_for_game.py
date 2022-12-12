import unittest
import time

from mlbstatsapi.mlb_api import Mlb

import unittest
import requests_mock
import json
import os

from mlbstatsapi import Mlb


# Mocked JSON directory
# TODO Find a better way to structure and handle this :) 
path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_not_found = os.path.join(current_directory, "../mock_json/response/not_found_404.json")
path_to_error = os.path.join(current_directory, "../mock_json/response/error_500.json")
path_to_hotcoldzone_file = os.path.join(current_directory, "../mock_json/stats/person/hotcoldzone.json")
path_to_hitting_playlog_file = os.path.join(current_directory, "../mock_json/stats/person/hitting_player_playlog.json")
path_to_shoei_ohtani = os.path.join(current_directory, "../mock_json/stats/person/game_stats_player_shoei_ohtani.json")
path_to_ty_france = os.path.join(current_directory, "../mock_json/stats/person/game_stats_player_ty_france.json")
path_to_cal = os.path.join(current_directory, "../mock_json/stats/person/game_stats_player_cal.json")
path_to_archie = os.path.join(current_directory, "../mock_json/stats/person/game_stats_player_archie.json")
NOT_FOUND_404 = open(path_to_not_found, "r", encoding="utf-8-sig").read()
ERROR_500 = open(path_to_error, "r", encoding="utf-8-sig").read()
SHOEI_ENDPOINT = open(path_to_shoei_ohtani, "r", encoding="utf-8-sig").read()
TY_ENDPOINT = open(path_to_ty_france, "r", encoding="utf-8-sig").read()
CAL_ENDPOINT = open(path_to_cal, "r", encoding="utf-8-sig").read()
ARCHIE_ENDPOINT = open(path_to_archie, "r", encoding="utf-8-sig").read()


@requests_mock.Mocker()
class TestHittingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.al_team = 133
        cls.shoei_ohtani = 660271
        cls.ty_france = 664034
        cls.shoei_game_id = 531368
        cls.ty_game_id = 715757
        cls.cal_realeigh = 663728
        cls.cal_game_id = 715757
        cls.archie_bradley = 605151
        cls.archie_game_id = 531368
        cls.mock_ty_france_stats = json.loads(TY_ENDPOINT)
        cls.mock_shoei_stats = json.loads(SHOEI_ENDPOINT)
        cls.mock_cal_stats = json.loads(CAL_ENDPOINT)
        cls.mock_archie_stats = json.loads(ARCHIE_ENDPOINT)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    
    def test_get_players_stats_for_shoei_ohtana(self, m):
        """return player stat objects"""
        m.get('https://statsapi.mlb.com/api/v1/people/660271/stats/game/531368', json=self.mock_shoei_stats,
        status_code=200)
        game_stats = self.mlb.get_players_stats_for_game(person_id=self.shoei_ohtani,
                                                         game_id=self.shoei_game_id)

        # game stats should not be None
        self.assertIsNotNone(game_stats)

        # game_stats should be a dict
        self.assertIsInstance(game_stats, dict)

        # game_stats should have hitting stats
        self.assertTrue(game_stats['pitching'])

        # game_stats should have vsplayer5y and playlog stats
        self.assertTrue(game_stats['pitching']['vsplayer5y'])

        splits = game_stats['pitching']['vsplayer5y']

        for split in splits:
            self.assertTrue(split.team)
            self.assertTrue(split.stat)

    def test_get_players_stats_for_ty_france(self, m):
        """return player stat objects"""
        m.get('https://statsapi.mlb.com/api/v1/people/664034/stats/game/715757', json=self.mock_ty_france_stats,
        status_code=200)
        game_stats = self.mlb.get_players_stats_for_game(person_id=self.ty_france,
                                                         game_id=self.ty_game_id)

        # game stats should not be None
        self.assertIsNotNone(game_stats)

        # game_stats should be a dict
        self.assertIsInstance(game_stats, dict)

        # game_stats should have hitting stats
        self.assertTrue(game_stats['hitting'])

        # game_stats should have vsplayer5y and playlog stats
        self.assertTrue(game_stats['hitting']['vsplayer5y'])
        self.assertTrue(game_stats['hitting']['playlog'])
        self.assertTrue(game_stats['stats']['gamelog'])

        splits = game_stats['hitting']['vsplayer5y']

        for split in splits:
            self.assertTrue(split.team)
            self.assertTrue(split.stat)

    def test_get_players_stats_for_cal_r(self, m):
        """return player stat objects"""
        m.get('https://statsapi.mlb.com/api/v1/people/663728/stats/game/715757', json=self.mock_cal_stats,
        status_code=200)
        game_stats = self.mlb.get_players_stats_for_game(person_id=self.cal_realeigh,
                                                         game_id=self.cal_game_id)

        # game stats should not be None
        self.assertIsNotNone(game_stats)

        # game_stats should be a dict
        self.assertIsInstance(game_stats, dict)

        # game_stats should have hitting stats
        self.assertTrue(game_stats['hitting'])

        # game_stats should have vsplayer5y and playlog stats
        self.assertTrue(game_stats['hitting']['vsplayer5y'])
        self.assertTrue(game_stats['hitting']['playlog'])
        self.assertTrue(game_stats['stats']['gamelog'])
        
        splits = game_stats['hitting']['vsplayer5y']

        for split in splits:
            self.assertTrue(split.team)
            self.assertTrue(split.stat)

    def test_get_players_stats_for_archie(self, m):
        """return player stat objects"""
        m.get('https://statsapi.mlb.com/api/v1/people/605151/stats/game/531368', json=self.mock_archie_stats,
        status_code=200)
        self.game_stats = self.mlb.get_players_stats_for_game(person_id=self.archie_bradley,
                                                         game_id=self.archie_game_id)

        # game stats should not be None
        self.assertIsNotNone(self.game_stats)

        # game_stats should be a dict
        self.assertIsInstance(self.game_stats, dict)

        # game_stats should have hitting stats
        self.assertTrue(self.game_stats['pitching'])

        # game_stats should have vsplayer5y and playlog stats
        self.assertTrue(self.game_stats['pitching']['vsplayer5y'])
        self.assertTrue(self.game_stats['stats']['gamelog'])

        self.assertNotEqual(self.game_stats['stats']['gamelog'], [])
        print(self.game_stats['stats']['gamelog'])
        self.assertTrue(len(self.game_stats['stats']['gamelog']) == 3)
        splits = self.game_stats['pitching']['vsplayer5y']

        for split in splits:
            self.assertTrue(split.team)
            self.assertTrue(split.stat)