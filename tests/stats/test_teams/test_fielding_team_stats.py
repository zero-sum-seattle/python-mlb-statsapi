import unittest

from mlbstatsapi.mlbapi import Mlb


class TestTeamFieldingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.team = cls.mlb.get_team(133) # Oakland A's

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_fielding_season_stats_for_team(self):
        self.params = {'stats': ['season'], 'group': ['fielding']}

        # catching_player
        stats = self.mlb.get_stats(self.params, self.team)

        self.assertIsNotNone(stats)
        self.assertNotEqual(stats, {})

        self.assertTrue(stats['fielding']['season'])
