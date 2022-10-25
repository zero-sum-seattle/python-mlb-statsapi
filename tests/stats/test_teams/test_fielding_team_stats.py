from dataclasses import field
import unittest

from mlbstatsapi.mlbapi import Mlb

from mlbstatsapi.models.stats import (
    SimpleFielding
)

class TestTeamStatCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.team = cls.mlb.get_team(133) # Oakland A's

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_fielding_season_stats_for_team(self):
        self.params = { 'stats': [ 'season' ], 'group': 'fielding' }

        # catching_player
        fielding = self.mlb.get_stats(self.team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(fielding)

        for stat in fielding:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, SimpleFielding)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'errors'))
            self.assertTrue(hasattr(stat, 'gamesplayed'))