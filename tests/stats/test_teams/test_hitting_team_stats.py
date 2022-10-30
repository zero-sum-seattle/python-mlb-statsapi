from dataclasses import field
import unittest

from mlbstatsapi.mlbapi import Mlb
from mlbstatsapi import TheMlbStatsApiException

from mlbstatsapi.models.stats import (
    HittingSeason,
    HittingYBY,
    HittingExpectedStatistics,
    HittingAdvancedSeason 
)

class TestOpponentsFacedHitting(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.al_team = cls.mlb.get_team(133) # Oakland
        cls.nl_team = cls.mlb.get_team(143) # Philadelphia Phillies

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_hitting_opponents_faced_position(self):
        """mlb get stats should return none becaue 404 stats"""
        self.params = { 'stats': [ 'opponentsFaced' ], 'group': 'hitting' }
        al_opponents_faced = self.mlb.get_stats(self.al_team, self.params)

        # check for None, or NoneType
        self.assertIsNone(al_opponents_faced)


    def test_get_one_hitting_stats_for_player(self):
        """mlb get stats should return hitting stats"""
        self.params = { 'stats': [ 'season' ], 'group': 'hitting' }

        al_hitting_stats = self.mlb.get_stats(self.al_team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(al_hitting_stats)

        for stat in al_hitting_stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleHitting
            self.assertIsInstance(stat, HittingSeason)

        self.params = { 'stats': [ 'seasonAdvanced' ], 'group': 'hitting' }

        al_advanced_hitting = self.mlb.get_stats(self.al_team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(al_advanced_hitting)

        for stat in al_advanced_hitting:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be AdvancedHitting
            self.assertIsInstance(stat, HittingAdvancedSeason)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'totalbases'))

        nl_hitting_stats = self.mlb.get_stats(self.nl_team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(nl_hitting_stats)

        for stat in nl_hitting_stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleHitting
            self.assertIsInstance(stat, HittingAdvancedSeason)

        self.params = { 'stats': [ 'seasonAdvanced' ], 'group': 'hitting' }

        nl_hitting_stats = self.mlb.get_stats(self.nl_team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(nl_hitting_stats)

        for stat in nl_hitting_stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be AdvancedHitting
            self.assertIsInstance(stat, HittingAdvancedSeason)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'totalbases'))

    def test_yearbyyear_hitting_stats_for_player(self):
        """mlb get stats should return hitting stats"""
        self.params = { "stats": [ 'yearByYear' ], 'group': 'hitting' }
        al_yearbyyear_stats = self.mlb.get_stats(self.al_team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(al_yearbyyear_stats)

        # check objects is > 1
        self.assertTrue(len(al_yearbyyear_stats) > 2)
        for stat in al_yearbyyear_stats:
            # test that split is not NoneType
            self.assertTrue(stat)

            # split should be HittingSplits
            self.assertIsInstance(stat, HittingYBY)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, "hits"))

        nl_yearbyyear_stats = self.mlb.get_stats(self.nl_team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(nl_yearbyyear_stats)

        # check objects is > 1
        self.assertTrue(len(nl_yearbyyear_stats) > 2)

        for stat in nl_yearbyyear_stats:
            # test that split is not NoneType
            self.assertTrue(stat)

            # split should be HittingSplits
            self.assertIsInstance(stat, HittingYBY)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, "hits"))

    def test_get_multiple_stats_for_player(self):
        """mlb get stats should return two hitting stats"""
        self.params = { 'stats': [ 'seasonAdvanced', 'season', 'careerAdvanced' ], 'group': 'hitting' }

        stats = self.mlb.get_stats(self.al_team, self.params)

        self.assertIsNotNone(stats)

        print(len(stats))
        self.assertTrue(len(stats) > 2)

        stats = self.mlb.get_stats(self.nl_team, self.params)

        self.assertIsNotNone(stats)

        self.assertTrue(len(stats) > 2)    


    def test_hitting_pitch_arsenal_stat_on_position_player(self):
        """mlb get stats should return PitchArsenal object"""
        self.params = { 'stats': [ 'expectedStatistics' ], 'group': 'hitting' }
    
        al_expected_stats = self.mlb.get_stats(self.al_team, self.params)

        # pitch_arsenal_stats should not be None or NoneType
        self.assertIsNotNone(al_expected_stats)

        for stat in al_expected_stats:

            # stat should be PitchArsenal
            self.assertIsInstance(stat, HittingExpectedStatistics)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'wobacon'))
            self.assertTrue(hasattr(stat, 'woba'))

        nl_expected_stats = self.mlb.get_stats(self.nl_team, self.params)

        # pitch_arsenal_stats should not be None or NoneType
        self.assertIsNotNone(nl_expected_stats)

        for stat in nl_expected_stats:

            # stat should be PitchArsenal
            self.assertIsInstance(stat, HittingExpectedStatistics)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'wobacon'))
            self.assertTrue(hasattr(stat, 'woba'))


    def test_hitting_hot_cold_zone_on_teams(self):
        """mlb get stats should return none object object"""
        self.params = { 'stats': [ 'hotColdZones', 'pitchArsenal', 'opponentsFaced'  ], 'group': 'hitting' }
    
        al_hot_cold_zone = self.mlb.get_stats(self.al_team, self.params)

        # hot_cold_zone should be empty for teams
        self.assertIsNone(al_hot_cold_zone)


    def test_building_all_hitting_objects_for_teams(self):
        """this test will build all what should be working stat objects"""
        # Let's build this set of tests 
        self.params_one = { 'stats': [ 'homeAndAway', 'winLoss', 'yearByYear', 'byDayOfWeek',
        'byDateRange', 'byDateRangeAdvanced', 'byDayOfWeek', 'byMonth' ], 'group': 'hitting' }

        # make the calls to return a list of objects
        al_stat_group_one = self.mlb.get_stats(self.al_team, self.params_one)
        nl_stat_group_one = self.mlb.get_stats(self.nl_team, self.params_one)

        # the list should not be empty
        self.assertTrue(len(al_stat_group_one))
        self.assertTrue(len(nl_stat_group_one))

        # stat_group_one should be greater than 8
        self.assertTrue(len(al_stat_group_one) > 8)
        self.assertTrue(len(nl_stat_group_one) > 8)

        # let's now build play off stat types
        self.params_two = { 'stats': [ 'homeAndAwayPlayoffs', 'winLossPlayoffs', 'yearByYearPlayoffs', 
        'byMonthPlayoffs', 'byDayOfWeekPlayoffs' ], 'group': 'hitting' }

        # make the calls to return a list of objects
        al_stat_group_two = self.mlb.get_stats(self.al_team, self.params_two)
        nl_stat_group_two = self.mlb.get_stats(self.nl_team, self.params_two)

        # the list should not be empty
        self.assertTrue(len(al_stat_group_two))
        self.assertTrue(len(nl_stat_group_two))

        # stat_group_one should be greater than 8
        self.assertTrue(len(al_stat_group_two) > 8)
        self.assertTrue(len(nl_stat_group_two) > 8)

        # this returns 500 for team
        # self.params_three = { 'stats': [ 'pitchLog' ], 'group': 'hitting' }

        # # make the calls to return a list of objects
        # al_stat_group_one = self.mlb.get_stats(self.al_team, self.params_three)
        # nl_stat_group_one = self.mlb.get_stats(self.nl_team, self.params_three)

        # # the list should not be empty
        # self.assertTrue(len(al_stat_group_one))
        # self.assertTrue(len(nl_stat_group_one))

        # # stat_group_one should be greater than 8
        # self.assertTrue(len(al_stat_group_one) > 8)
        # self.assertTrue(len(nl_stat_group_one) > 8)

        self.params_three = { 'stats': [ 'expectedStatistics', 'sprayChart' ], 'group': 'hitting' }
        
        # make the calls to return a list of objects
        al_stat_group_three = self.mlb.get_stats(self.al_team, self.params_three)
        nl_stat_group_three = self.mlb.get_stats(self.nl_team, self.params_three)

        # the list should not be empty
        self.assertTrue(len(al_stat_group_three))
        self.assertTrue(len(nl_stat_group_three))

        # stat_group_one should be greater than 8
        self.assertTrue(len(nl_stat_group_three) > 8)
        self.assertTrue(len(nl_stat_group_three) > 8)

        self.params_four = { 'stats': [ 'seasonAdvanced', 'season', 'careerAdvanced' ], 'group': 'hitting' }

        # make the calls to return a list of objects
        al_stat_group_four = self.mlb.get_stats(self.al_team, self.params_four)
        nl_stat_group_four = self.mlb.get_stats(self.nl_team, self.params_four)

        # the list should not be empty
        self.assertTrue(len(al_stat_group_four))
        self.assertTrue(len(nl_stat_group_four))

        # stat_group_one should be greater than 8
        self.assertTrue(len(nl_stat_group_four) == 3)
        self.assertTrue(len(nl_stat_group_four) == 3)

        self.params_five = { 'stats': [  'gameLog' ], 'group': 'hitting' }

        # make the calls to return a list of objects
        al_stat_group_five = self.mlb.get_stats(self.al_team, self.params_five)
        nl_stat_group_five = self.mlb.get_stats(self.nl_team, self.params_five)

        # the list should not be empty
        self.assertTrue(len(al_stat_group_five))
        self.assertTrue(len(nl_stat_group_five))

        # stat_group_one should be greater than 8
        self.assertTrue(len(al_stat_group_five) > 8)
        self.assertTrue(len(nl_stat_group_five) > 8)


    def test_building_playlog_500(self):
        """playlog should return 500 error"""
        self.params_six = { 'stats': [  'playLog' ], 'group': 'hitting' }


        with self.assertRaises(TheMlbStatsApiException):
            al_stat_group_six = self.mlb.get_stats(self.al_team, self.params_six)
