import unittest

from mlbstatsapi.mlb_api import Mlb


class TestCatchingPlayerStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.catching_player = cls.mlb.get_person(663728)
        cls.utility_player = cls.mlb.get_person(647351)

    @classmethod
    def tearDownClass(cls) -> None:
        pass
    
    def test_catching_season_stats_for_catcher(self):
        """build catching stat for season"""
        self.params = {'stats': ['season', 'statsSingleSeason','careerRegularSeason'], 'group': ['catching']}

        splits = self.mlb.get_stats(self.params, self.catching_player)

        self.assertIsNotNone(splits)
        self.assertNotEqual(splits, {})

        self.assertTrue(splits['catching']['season'])

