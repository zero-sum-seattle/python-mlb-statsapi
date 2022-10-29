from dataclasses import field
import unittest

from mlbstatsapi.mlbapi import Mlb

from mlbstatsapi.models.stats import (
    SimpleCatching,
    CatchingYearByYear
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
        self.params = { 'stats': [ 'season' ], 'group': 'catching' }

        catching = self.mlb.get_stats(self.catching_player, self.params)

        # check for None, or NoneType
        self.assertTrue(len(catching))

        for stat in catching:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, SimpleCatching)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'passedball'))

    def test_catching_yearbyyear_stats_for_catcher(self):
        self.params = { 'stats': [ 'yearByYear' ], 'group': 'catching' }

        catching = self.mlb.get_stats(self.catching_player, self.params)

        # check for None, or NoneType
        self.assertTrue(len(catching))

        for stat in catching:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, CatchingYearByYear)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'passedball'))

    def test_catching_all_supported_stats_for_catcher(self):

        self.params_one = { 'stats': [ 'season', 'statsSingleSeason' ], 'group': 'catching' }

        stat_group_one = self.mlb.get_stats(self.catching_player, self.params_one)

        # check for None, or NoneType
        self.assertTrue(len(stat_group_one))

        # stat_group_two 
        self.assertTrue(len(stat_group_one) == 2)

        self.params_two = { 'stats': [ 'yearByYear', 'yearByYearPlayoffs' ], 'group': 'catching' }

        stat_group_two = self.mlb.get_stats(self.catching_player, self.params_two)

        # check for None, or NoneType
        self.assertTrue(len(stat_group_two))

        # stat_group_two 
        self.assertTrue(len(stat_group_two) > 2)

        self.params_three = { 'stats': [ 'career', 'careerRegularSeason' ], 'group': 'catching' }

        stat_group_three = self.mlb.get_stats(self.catching_player, self.params_three)

        # check for None, or NoneType
        self.assertTrue(len(stat_group_three))

        # stat_group_two 
        self.assertTrue(len(stat_group_three) == 2)

        self.params_four = { 'stats': [ 'homeAndAway', 'winLoss',  ], 'group': 'catching' }

        stat_group_four = self.mlb.get_stats(self.catching_player, self.params_four)

        # check for None, or NoneType
        self.assertTrue(len(stat_group_four))

        # stat_group_two 
        self.assertTrue(len(stat_group_four) > 2)

        self.params_five = { 'stats': [ 'byDateRange', 'byDayOfWeek',  ], 'group': 'catching' }

        stat_group_five = self.mlb.get_stats(self.catching_player, self.params_five)

        # check for None, or NoneType
        self.assertTrue(len(stat_group_five))

        # stat_group_two 
        self.assertTrue(len(stat_group_five) > 2)

        self.params_six = { 'stats': [ 'gameLog' ], 'group': 'catching' }

        stat_group_six = self.mlb.get_stats(self.catching_player, self.params_six)

        # check for None, or NoneType
        self.assertTrue(len(stat_group_six))

        # stat_group_two 
        self.assertTrue(len(stat_group_six) > 2)

        self.params_seven = { 'stats': [ 'lastXGames' ], 'group': 'catching' }

        stat_group_seven = self.mlb.get_stats(self.catching_player, self.params_seven)

        # check for None, or NoneType
        self.assertTrue(len(stat_group_seven))
 


