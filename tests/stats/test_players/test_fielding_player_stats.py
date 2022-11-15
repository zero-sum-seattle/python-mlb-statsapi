import unittest

from mlbstatsapi.mlb_api import Mlb


class TestPlayerFieldingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        # Juan Soto
        cls.position_player = 665742
        # Robbie Ray
        cls.pitching_player = 592662
        # Cal Raleigh
        cls.catching_player = 663728
        # Abraham Toro
        cls.utility_player = 647351

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_fielding_season_stats_for_players(self):
        self.params = {'stats': ['season'], 'group': ['fielding']}

        # get stats
        fielding_catching = self.mlb.get_player_stats(self.catching_player, self.params)
        fielding_pitching = self.mlb.get_player_stats(self.pitching_player, self.params)
        fielding_position = self.mlb.get_player_stats(self.position_player, self.params)
        fielding_utility = self.mlb.get_player_stats(self.utility_player, self.params)

        # let's check if season is not Empty
        self.assertTrue(fielding_catching['fielding']['season'])
        self.assertTrue(fielding_pitching['fielding']['season'])
        self.assertTrue(fielding_position['fielding']['season'])
        self.assertTrue(fielding_utility['fielding']['season'])

    def test_fielding_gamelog_stats_for_player(self):
        """get stats should return game logs for players"""
        self.params = {'stats': ['gameLog'], 'group': ['fielding']}
        fielding_gamelogs = self.mlb.get_player_stats(self.catching_player, self.params)
        self.assertTrue(fielding_gamelogs['fielding']['gamelog'])

    def test_building_all_fielding_objects(self):
        """this test will build all what should be working stat objects"""
        # Let's build this set of tests 
        self.params = {'stats': ['homeAndAway', 'yearByYear', 'byDayOfWeek', 'byMonth'], 'group': ['fielding']}
        stats = self.mlb.get_player_stats(self.utility_player, self.params)

        self.assertTrue(stats['fielding']['homeandaway'])
        self.assertTrue(stats['fielding']['yearbyyear'])
        self.assertTrue(stats['fielding']['bydayofweek'])
        self.assertTrue(stats['fielding']['bymonth'])

        self.params = {'stats': ['statsSingleSeason', 'season'], 'group': ['fielding']}
        stats = self.mlb.get_player_stats(self.utility_player, self.params)

        self.assertTrue(stats['fielding']['statssingleseason'])
        self.assertTrue(stats['fielding']['season'])

        self.params = {'stats': ['career'], 'group': ['fielding']}
        stats = self.mlb.get_player_stats(self.utility_player, self.params)

        self.assertTrue(stats['fielding']['career'])
