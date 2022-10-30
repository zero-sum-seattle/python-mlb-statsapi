from dataclasses import field
import unittest

from mlbstatsapi.mlbapi import Mlb
from mlbstatsapi import TheMlbStatsApiException

from mlbstatsapi.models.stats import (
    PitchingYearByYear,
    PitchingSeason,
)


class TestTeamStatCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.al_team = cls.mlb.get_team(133) # Oakland
        cls.nl_team = cls.mlb.get_team(143) # Philadelphia Phillies

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_yearbyyear_hitting_stats_for_team(self):
        """mlb get stats should return hitting stats"""
        self.params = { 'stats': [ 'yearByYear' ], 'group': 'pitching' }

        # let's get some stats
        al_yearbyyear_stats = self.mlb.get_stats(self.al_team, self.params)

        # check for None, or NoneType
        self.assertNotEqual(al_yearbyyear_stats, [])

        # check objects is > 1
        self.assertTrue(len(al_yearbyyear_stats) > 10)
        for stat in al_yearbyyear_stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleHitting
            self.assertIsInstance(stat, PitchingYearByYear)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, "hits"))

        # let's get some stats
        nl_yearbyyear_stats = self.mlb.get_stats(self.nl_team, self.params)

        # check for None, or NoneType
        self.assertNotEqual(nl_yearbyyear_stats, [])

        # check objects is > 1
        self.assertTrue(len(nl_yearbyyear_stats) > 10)
        for stat in nl_yearbyyear_stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleHitting
            self.assertIsInstance(stat, PitchingYearByYear)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, "hits"))

    def test_get_one_pitching_stats_for_team(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'season' ], 'group': 'pitching' }
        
        pitching_splits = self.mlb.get_stats(self.al_team, self.params)

        # check for None, or NoneType
        self.assertNotEqual(pitching_splits, [])

        for stat in pitching_splits:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be HittingSplits
            self.assertIsInstance(stat, PitchingSeason)

            # stat should have attr set
            self.assertTrue(hasattr(stat, "hits"))

        pitching_splits = self.mlb.get_stats(self.nl_team, self.params)

        # check for None, or NoneType
        self.assertNotEqual(pitching_splits, [])

        for stat in pitching_splits:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be HittingSplits
            self.assertIsInstance(stat, PitchingSeason)

            # stat should have attr set
            self.assertTrue(hasattr(stat, "hits"))

    def test_multiple_pitching_stats_for_team(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'season', 'career', 'seasonAdvanced', 'careerAdvanced' ], 'group': 'pitching' }

        # let's get some stats
        pitching_splits = self.mlb.get_stats(self.al_team, self.params)

        # check for empty list
        self.assertNotEqual(pitching_splits, [])

        # the end point should give us 4 objects back
        self.assertEqual(len(pitching_splits), 4)
            

    def test_building_all_pitching_objects_for_teams(self):
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
        'byMonthPlayoffs', 'byDayOfWeekPlayoffs' ], 'group': 'pitching' }

        # make the calls to return a list of objects
        al_stat_group_two = self.mlb.get_stats(self.al_team, self.params_two)
        nl_stat_group_two = self.mlb.get_stats(self.nl_team, self.params_two)

        # the list should not be empty
        self.assertTrue(len(al_stat_group_two))
        self.assertTrue(len(nl_stat_group_two))

        # stat_group_one should be greater than 8
        self.assertTrue(len(al_stat_group_two) > 8)
        self.assertTrue(len(nl_stat_group_two) > 8)

        self.params_three = { 'stats': [  'gameLog' ], 'group': 'hitting' }

        # make the calls to return a list of objects
        al_stat_group_three = self.mlb.get_stats(self.al_team, self.params_three)
        nl_stat_group_three = self.mlb.get_stats(self.nl_team, self.params_three)

        # the list should not be empty
        self.assertTrue(len(al_stat_group_three))
        self.assertTrue(len(nl_stat_group_three))

        # stat_group_one should be greater than 8
        self.assertTrue(len(al_stat_group_three) > 8)
        self.assertTrue(len(nl_stat_group_three) > 8)

        self.params_four = { 'stats': [ 'expectedStatistics', 'sprayChart' ], 'group': 'hitting' }
        
        # make the calls to return a list of objects
        al_stat_group_four = self.mlb.get_stats(self.al_team, self.params_four)
        nl_stat_group_four = self.mlb.get_stats(self.nl_team, self.params_four)

        # the list should not be empty
        self.assertTrue(len(al_stat_group_four))
        self.assertTrue(len(nl_stat_group_four))

        # stat_group_one should be greater than 8
        self.assertTrue(len(al_stat_group_four) > 8)
        self.assertTrue(len(nl_stat_group_four) > 8)

        self.params_five = { 'stats': [ 'seasonAdvanced', 'season', 'careerAdvanced' ], 'group': 'hitting' }

        # make the calls to return a list of objects
        al_stat_group_five = self.mlb.get_stats(self.al_team, self.params_five)
        nl_stat_group_five = self.mlb.get_stats(self.nl_team, self.params_five)

        # the list should not be empty
        self.assertTrue(len(al_stat_group_five))
        self.assertTrue(len(nl_stat_group_five))

        # stat_group_one should be greater than 8
        self.assertTrue(len(al_stat_group_five) == 3)
        self.assertTrue(len(nl_stat_group_five) == 3)
        
    def test_building_playlog_500(self):
        """playlog should return 500 error"""
        self.params_four = { 'stats': [  'playLog' ], 'group': 'hitting' }

        with self.assertRaises(TheMlbStatsApiException):
            al_stat_group_six = self.mlb.get_stats(self.al_team, self.params_four)