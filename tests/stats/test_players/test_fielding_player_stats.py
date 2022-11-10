import unittest

from mlbstatsapi.mlbapi import Mlb


class TestPlayerFieldingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        # Juan Soto
        cls.position_player = cls.mlb.get_person(665742)
        # Robbie Ray
        cls.pitching_player = cls.mlb.get_person(592662)
        # Cal Raleigh
        cls.catching_player = cls.mlb.get_person(663728)
        # Abraham Toro
        cls.utility_player = cls.mlb.get_person(647351)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_fielding_season_stats_for_players(self):
        self.params = {'stats': ['season'], 'group': ['fielding']}

        # get stats
        fielding_catching = self.mlb.get_stats(self.params, self.catching_player)
        fielding_pitching = self.mlb.get_stats(self.params, self.pitching_player)
        fielding_position = self.mlb.get_stats(self.params, self.position_player)
        fielding_utility = self.mlb.get_stats(self.params, self.utility_player)

        # let's check if season is not Empty
        self.assertTrue(fielding_catching['fielding']['season'])
        self.assertTrue(fielding_pitching['fielding']['season'])
        self.assertTrue(fielding_position['fielding']['season'])
        self.assertTrue(fielding_utility['fielding']['season'])

    def test_fielding_gamelog_stats_for_player(self):
        """get stats should return game logs for players"""
        self.params = {'stats': ['gameLog'], 'group': ['fielding']}
        fielding_gamelogs = self.mlb.get_stats(self.params, self.catching_player)
        self.assertTrue(fielding_gamelogs['fielding']['gamelog'])

    def test_building_all_fielding_objects(self):
        """this test will build all what should be working stat objects"""
        # Let's build this set of tests 
        self.params_one = {'stats': ['homeAndAway', 'yearByYear', 'byDayOfWeek', 'byMonth'], 'group': ['fielding']}
        stat_group_one = self.mlb.get_stats(self.params_one, self.utility_player)

        self.assertTrue(stat_group_one['fielding']['homeandaway'])
        self.assertTrue(stat_group_one['fielding']['yearbyyear'])
        self.assertTrue(stat_group_one['fielding']['bydayofweek'])
        self.assertTrue(stat_group_one['fielding']['bymonth'])

        self.params_two = {'stats': ['statsSingleSeason', 'season'], 'group': ['fielding']}
        stat_group_two = self.mlb.get_stats(self.params_two, self.utility_player)

        self.assertTrue(stat_group_two['fielding']['statssingleseason'])
        self.assertTrue(stat_group_two['fielding']['season'])

        self.params_three = {'stats': ['career'], 'group': ['fielding']}
        stat_group_three = self.mlb.get_stats(self.params_three, self.utility_player)

        self.assertTrue(stat_group_three['fielding']['career'])
