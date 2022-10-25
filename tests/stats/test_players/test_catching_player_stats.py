from dataclasses import field
import unittest

from mlbstatsapi.mlbapi import Mlb

from mlbstatsapi.models.stats import (
    SimpleCatching,
)

class TestOpponentsFacedHitting(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.catching_player = cls.mlb.get_person(663728) # Cal Raleigh
        cls.utility_player = cls.mlb.get_person(647351) # Abraham Toro

    @classmethod
    def tearDownClass(cls) -> None:
        pass
    
    def test_catching_season_stats_for_catcher(self):
        self.params = { "stats": ["season"], "group": "catching" }

        catching = self.mlb.get_stats(self.catching_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(catching)

        for stat in catching:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, SimpleCatching)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'passedball'))