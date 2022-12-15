import unittest
import time

from mlbstatsapi.mlb_api import Mlb


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
             
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    
    def test_get_players_stats_for_shoei_ohtana(self):
        """return player stat objects"""

        game_stats = self.mlb.get_players_stats_for_game(person_id=self.shoei_ohtani,
                                                         game_id=self.shoei_game_id)

        # game stats should not be None
        self.assertIsNotNone(game_stats)

        # game_stats should be a dict
        self.assertIsInstance(game_stats, dict)

        print(game_stats)
        # game_stats should have hitting stats
        self.assertTrue(game_stats['pitching'])

        # game_stats should have vsplayer5y and playlog stats
        self.assertTrue(game_stats['pitching']['vsplayer5y'])

        stat = game_stats['pitching']['vsplayer5y']

        for split in stat.splits:
            self.assertTrue(split.team)
            self.assertTrue(split.stat)

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

        stat = game_stats['stats']['gamelog']


    def test_get_players_stats_for_archie(self):
        """return player stat objects"""

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

        game_log_stat = self.game_stats['stats']['gamelog']
        self.assertTrue(len(game_log_stat.splits) == 3)
        stat = self.game_stats['pitching']['vsplayer5y']

        for split in stat.splits:
            self.assertTrue(split.team)
            self.assertTrue(split.stat)