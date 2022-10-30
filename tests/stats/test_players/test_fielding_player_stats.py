from dataclasses import field
import unittest

from mlbstatsapi.mlbapi import Mlb

from mlbstatsapi.models.stats import (
    SimpleFielding,
    FieldingGameLog
)

class TestPlayerFieldingStats(unittest.TestCase):
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
        self.params = { 'stats': [ 'season' ], 'group': 'fielding' }

        # catching_player
        fielding = self.mlb.get_stats(self.catching_player, self.params)

        # check for None, or NoneType
        self.assertTrue(len(fielding))

        for stat in fielding:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, SimpleFielding)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'errors'))
            self.assertTrue(hasattr(stat, 'gamesplayed'))

        self.params = { 'stats': [ 'season' ], 'group': 'fielding' }

        # pitching_player
        fielding = self.mlb.get_stats(self.pitching_player, self.params)

        # check for None, or NoneType
        self.assertTrue(len(fielding))

        for stat in fielding:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, SimpleFielding)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'chances'))
            self.assertTrue(hasattr(stat, 'gamesplayed'))

        self.params = { 'stats': [ 'season' ], 'group': 'fielding' }

        # position_player
        fielding = self.mlb.get_stats(self.position_player, self.params)

        self.assertTrue(len(fielding))

        for stat in fielding:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, SimpleFielding)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'doubleplays'))
            self.assertTrue(hasattr(stat, 'fielding'))
            
        self.params = { 'stats': [ 'season' ], 'group': 'fielding' }

        # position_player
        fielding = self.mlb.get_stats(self.utility_player, self.params)

        self.assertTrue(len(fielding))

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
        self.assertTrue(len(fielding_gamelogs))

        for gamelog in fielding_gamelogs:
            # test that stat is not NoneType
            self.assertTrue(gamelog)

            # stat should be SimpleCatching
            self.assertIsInstance(gamelog, FieldingGameLog)

            # stat should have attr set
            self.assertTrue(hasattr(gamelog, 'chances'))
            self.assertTrue(hasattr(gamelog, 'gamesplayed'))

    def test_building_all_fielding_objects(self):
        """this test will build all what should be working stat objects"""
        # Let's build this set of tests 
        self.params_one = { 'stats': [ 'homeAndAway', 'yearByYear',
         'byDayOfWeek', 'byMonth' ], 'group': 'fielding' }

        # make the calls to return a list of objects
        stat_group_one = self.mlb.get_stats(self.utility_player, self.params_one)

        # the list should not be empty
        self.assertTrue(len(stat_group_one))

        # stat_group_one should be greater than 8
        self.assertTrue(len(stat_group_one) > 4)

        # Let's build this set of tests 
        self.params_two = { 'stats': [ 'careerRegularSeason', 'yearByYearAdvanced', 'statsSingleSeasonAdvanced',
        'byDateRangeAdvanced' ], 'group': 'fielding' }

        # make the calls to return a list of objects
        stat_group_two = self.mlb.get_stats(self.utility_player, self.params_two)

        # the list should not be empty
        self.assertTrue(len(stat_group_two))

        # stat_group_one should be greater than 8
        self.assertTrue(len(stat_group_two) > 4)
        # let's now build play off stat types

        # Let's build this set of tests 
        self.params_three = { 'stats': [ 'seasonAdvanced', 'statsSingleSeason', 'season',
         ], 'group': 'fielding' }

        # make the calls to return a list of objects
        stat_group_three = self.mlb.get_stats(self.utility_player, self.params_three)

        # the list should not be empty
        self.assertTrue(len(stat_group_three))

        # stat_group_one should be greater than 8
        self.assertTrue(len(stat_group_three) > 4)
        # let's now build play off stat types

        # Let's build this set of tests 
        self.params_four = { 'stats': [ 'careerPlayoffs', 'homeAndAwayPlayoffs', 'winLossPlayoffs',
         'byMonthPlayoffs' ], 'group': 'fielding' }

        # make the calls to return a list of objects
        stat_group_four = self.mlb.get_stats(self.utility_player, self.params_four)

        # the list should not be empty
        self.assertTrue(len(stat_group_four))

        # stat_group_one should be greater than 8
        self.assertTrue(len(stat_group_four) > 4)




    # type_ = [ 'lastXGames' ]
    # type_ = [ 'gameLog' ]


# winLoss
# byDateRange