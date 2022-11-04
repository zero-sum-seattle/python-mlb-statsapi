from dataclasses import field
import unittest

from mlbstatsapi.mlbapi import Mlb

class TestPlayerPitchingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.pitching_player = cls.mlb.get_person(592662) # Robbie Ray

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_one_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'season', 'statsSingleSeason' ], 'group': ['pitching'] }
        stats = self.mlb.get_stats(self.params, self.pitching_player)

        self.assertTrue(stats['pitching']['season'])
        self.assertTrue(stats['pitching']['statssingleseason'])

        self.params = { 'stats': [ 'seasonAdvanced', 'statsSingleSeasonAdvanced' ], 'group': ['pitching'] }
        stats = self.mlb.get_stats(self.params, self.pitching_player)

        self.assertTrue(stats['pitching']['seasonadvanced'])
        self.assertTrue(stats['pitching']['statssingleseasonadvanced'])

    def test_get_sabermetrics_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': ['sabermetrics'], 'group': ['pitching'] }
        stats = self.mlb.get_stats(self.params, self.pitching_player)

        self.assertTrue(stats['pitching']['sabermetrics'])

    def test_get_pitching_career_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'career', 'careerAdvanced' ], 'group': ['pitching'] }
        stats = self.mlb.get_stats(self.params, self.pitching_player)

        self.assertTrue(stats['pitching']['career'])
        self.assertTrue(stats['pitching']['careeradvanced'])


    # def test_get_yearbyyear_pitching_stats_for_player(self):
    #     """mlb get stats should return pitching stats"""
    #     self.params = { 'stats': ['yearByYear'], 'group': 'pitching' }
    #     stats = self.mlb.get_stats(self.pitching_player, self.params)

    #     self.params = { 'stats': ['yearByYearAdvanced' ], 'group': 'pitching' }
    #     stats = self.mlb.get_stats(self.pitching_player, self.params)

    #     self.params = { 'stats': [ 'yearByYearPlayoffs' ], 'group': 'pitching' }
    #     stats = self.mlb.get_stats(self.pitching_player, self.params)

    # def test_get_dayofweek_pitching_stats_for_player(self):
    #     """mlb get stats should return pitching stats"""
    #     self.params = { 'stats': [ 'byDayOfWeek' ], 'group': 'pitching' }
    #     stats = self.mlb.get_stats(self.pitching_player, self.params)

    # def test_get_gamelog_pitching_stats_for_player(self):
    #     """mlb get stats should return pitching stats"""
    #     self.params = { 'stats': [ 'gameLog' ], 'group': 'pitching' }
    #     stats = self.mlb.get_stats(self.pitching_player, self.params)

    # def test_get_playlog_pitching_stats_for_player(self):
    #     """mlb get stats should return pitching stats"""
    #     self.params = { 'stats': [ 'playLog' ], 'group': 'pitching' }
    #     stats = self.mlb.get_stats(self.pitching_player, self.params)

    # def test_get_bydate_pitching_stats_for_player(self):
    #     """mlb get stats should return pitching stats"""
    #     self.params = { 'stats': [ 'byDateRange', 'byDateRangeAdvanced', 'byMonth', 'byMonthPlayoffs', 
    #     'byDayOfWeek', 'byDayOfWeekPlayoffs' ], 'group': 'pitching' }
    #     stats = self.mlb.get_stats(self.pitching_player, self.params)
    #     self.assertTrue(len(stats) == 18)

    # def test_get_homeandaway_pitching_stats_for_player(self):
    #     """mlb get stats should return pitching stats"""
    #     self.params = { 'stats': [ 'homeAndAway', 'homeAndAwayPlayoffs' ], 'group': 'pitching' }
    #     stats = self.mlb.get_stats(self.pitching_player, self.params)


    # def test_get_winloss_pitching_stats_for_player(self):
    #     """mlb get stats should return pitching stats"""
    #     self.params = { 'stats': [ 'winLoss' ], 'group': 'pitching' }
    #     stats = self.mlb.get_stats(self.pitching_player, self.params)

    # def test_get_opponentfaced_pitching_stats_for_player(self):
    #     """mlb get stats should return pitching stats"""
    #     self.params = { 'stats': [ 'opponentsFaced' ], 'group': 'pitching' }
    #     stats = self.mlb.get_stats(self.pitching_player, self.params)


    # def test_hitting_vs_team_stats_on_players(self):
    #     self.params = { 'stats': [ 'vsTeam' ], 'group': 'pitching', 'opposingTeamId': '133' }
    #     pitching_vsteam_stats = self.mlb.get_stats(self.pitching_player, self.params)


    # def test_building_all_hitting_objects(self):
    #     """this test will build all what should be working stat objects"""
    #     self.params_one = { 'stats': [ 'homeAndAway', 'winLoss', 'yearByYear', 'byDayOfWeek',
    #     'byDateRange', 'byDateRangeAdvanced', 'byDayOfWeek', 'byMonth' ], 'group': 'pitching' }
    #     stat_group_one = self.mlb.get_stats(self.pitching_player, self.params_one)

    #     self.params_two = { 'stats': [ 'homeAndAwayPlayoffs', 'winLossPlayoffs', 'yearByYearPlayoffs', 
    #     'byMonthPlayoffs', 'byDayOfWeekPlayoffs' ], 'group': 'pitching' }

    #     self.params_three = { 'stats': [ 'pitchLog', 'playLog', 'gameLog' ], 'group': 'pitching' }

    #     stat_group_three = self.mlb.get_stats(self.pitching_player, self.params_three)

    #     self.params_four = { 'stats': [ 'hotColdZones', 'pitchArsenal', 'opponentsFaced' ], 'group': 'pitching' }

    #     stat_group_four = self.mlb.get_stats(self.pitching_player, self.params_four)

    #     self.params_five = { 'stats': [ 'expectedStatistics', 'sprayChart' ], 'group': 'pitching' }

    #     stat_group_five = self.mlb.get_stats(self.pitching_player, self.params_five)

    #     self.params_six = { 'stats': [ 'seasonAdvanced', 'season', 'careerAdvanced' ], 'group': 'pitching' }

    #     stat_group_six = self.mlb.get_stats(self.pitching_player, self.params_six)
