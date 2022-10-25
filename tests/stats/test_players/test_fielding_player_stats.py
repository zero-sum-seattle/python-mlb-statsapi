from dataclasses import field
import unittest

from mlbstatsapi.mlbapi import Mlb

from mlbstatsapi.models.stats import (
    SimpleFielding,
    FieldingGameLog
)

class TestPlayerStatCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.position_player = cls.mlb.get_person(665742) # Juan Soto
        cls.pitching_player = cls.mlb.get_person(592662) # Robbie Ray
        cls.catching_player = cls.mlb.get_person(663728) # Cal Raleigh
        cls.utility_player = cls.mlb.get_person(647351) # Abraham Toro

    @classmethod
    def tearDownClass(cls) -> None:
        pass


    def test_fielding_season_stats_for_players(self):
        self.params = { "stats": [ "season" ], "group": "fielding" }

        # catching_player
        fielding = self.mlb.get_stats(self.catching_player, self.params)

        # check for None, or NoneType
        self.assertTrue(fielding, [])

        for stat in fielding:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, SimpleFielding)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'errors'))
            self.assertTrue(hasattr(stat, 'gamesplayed'))

        self.params = { "stats": [ "season" ], "group": "fielding" }

        # pitching_player
        fielding = self.mlb.get_stats(self.pitching_player, self.params)

        # check for None, or NoneType
        self.assertTrue(fielding, [])

        for stat in fielding:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, SimpleFielding)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'chances'))
            self.assertTrue(hasattr(stat, 'gamesplayed'))

        self.params = { "stats": [ "season" ], "group": "fielding" }

        # position_player
        fielding = self.mlb.get_stats(self.position_player, self.params)

        self.assertTrue(fielding, [])

        for stat in fielding:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, SimpleFielding)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'doubleplays'))
            self.assertTrue(hasattr(stat, 'fielding'))

    def test_fielding_gamelog_stats_for_player(self):
        """get stats should return game logs for players"""
        self.params = { 'stats': [ 'gameLog' ], 'group': 'fielding' }

        # let's get it 
        fielding_gamelogs = self.mlb.get_stats(self.catching_player, self.params)

        # make sure game log is not empty
        self.assertTrue(fielding_gamelogs, [])


        for gamelog in fielding_gamelogs:
            # test that stat is not NoneType
            self.assertTrue(gamelog)

            # stat should be SimpleCatching
            self.assertIsInstance(gamelog, FieldingGameLog)

            # stat should have attr set
            self.assertTrue(hasattr(gamelog, 'chances'))
            self.assertTrue(hasattr(gamelog, 'gamesplayed'))