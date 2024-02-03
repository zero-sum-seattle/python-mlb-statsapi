import unittest
import time

from mlbstatsapi.mlb_api import Mlb


class TestHittingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.al_team = 133
        cls.ty_france = 664034
        cls.ty_game_id = 715757
        cls.cal_realeigh = 663728
        cls.cal_game_id = 715757
             
    @classmethod
    def tearDownClass(cls) -> None:
        pass


    def test_get_players_stats_for_ty_france(self):
        """return player stat objects"""

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

        stat = game_stats['hitting']['vsplayer5y']

        for split in stat.splits:
            self.assertTrue(split.team)
            self.assertTrue(split.stat)

    def test_get_players_stats_for_cal_r(self):
        """return player stat objects"""

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



