from dataclasses import field
import unittest

from mlbstatsapi.mlbapi import Mlb

from mlbstatsapi.models.stats import (
    PitchingSeason,
    PitchingSeasonAdvanced,
    PitchingSabermetrics,
    PitchingCareer,
    PitchingCareerAdvanced,
    PitchingYBY,
    PitchingLog,
    PitchingGameLog,
    PitchingHAA,
    PitchingOpponentsFaced,
    PitchingByDayOfWeek,
    PitchingWL,
    PitchingYBYAdvanced,
    PitchingPlayLog,
    PitchingYBYPlayoffs,
    PitchingWLPlayoffs
)
class TestOpponentsFacedHitting(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.position_player = cls.mlb.get_person(665742) # Juan Soto
        cls.pitching_player = cls.mlb.get_person(592662) # Robbie Ray

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_one_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'season', 'statsSingleSeason' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingSeason)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, 'season'))

        self.params = { 'stats': [ 'seasonAdvanced', 'statsSingleSeasonAdvanced' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingSeasonAdvanced)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, 'season'))


    def test_get_sabermetrics_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': ['sabermetrics'], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingSabermetrics)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, "fipminus"))

    def test_get_pitching_career_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'career' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingCareer)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, "player"))

        self.params = { 'stats': [ 'careerAdvanced' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingCareerAdvanced)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, 'player'))

    def test_get_yearbyyear_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': ['yearByYear'], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        # test that stat is not NoneType
        self.assertTrue(len(stats))

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingYBY)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, 'season'))

        self.params = { 'stats': ['yearByYearAdvanced' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)
        
        # test that stat is not NoneType
        self.assertTrue(len(stats))


        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingYBYAdvanced)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, 'season'))

        self.params = { 'stats': [ 'yearByYearPlayoffs' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        # test that stat is not NoneType
        self.assertTrue(len(stats))

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingYBYPlayoffs)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, 'season'))

    def test_get_dayofweek_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'byDayOfWeek' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingByDayOfWeek)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, 'season'))

    def test_get_gamelog_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'gameLog' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingGameLog)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, 'iswin'))

    def test_get_playlog_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'playLog' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)


        self.assertTrue(len(stats))

        for stat in stats:
            # test that stat in not NoneType

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingPlayLog)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, 'ishome'))

    def test_get_bydate_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'byDateRange', 'byDateRangeAdvanced', 'byMonth', 'byMonthPlayoffs', 
        'byDayOfWeek', 'byDayOfWeekPlayoffs' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)
        self.assertTrue(len(stats) == 18)

    def test_get_homeandaway_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'homeAndAway', 'homeAndAwayPlayoffs' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        self.assertTrue(len(stats) > 1)

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingHAA)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, 'ishome'))

    def test_get_winloss_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'winLoss' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        self.assertTrue(len(stats) > 1)

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingWL)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, 'iswin'))

    # def test_get_winloss_pitching_stats_for_player(self):
    #     """mlb get stats should return pitching stats"""
    #     self.params = { 'stats': [ 'winLossPlayoffs' ], 'group': 'pitching' }
    #     stats = self.mlb.get_stats(self.pitching_player, self.params)

    #     self.assertTrue(len(stats) == 1)

    #     for stat in stats:
    #         # test that stat is not NoneType
    #         self.assertTrue(stat)

    #         # stat should be SimplePitching
    #         self.assertIsInstance(stat, PitchingWLPlayoffs)

    #         # stat should have a attr set
    #         self.assertTrue(hasattr(stat, 'iswin'))

    def test_get_opponentfaced_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'opponentsFaced' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        # stats should not be empty
        self.assertNotEqual(stats, [])

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingOpponentsFaced)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, 'pitcher'))

    def test_building_all_hitting_objects(self):
        """this test will build all what should be working stat objects"""
        # Let's build this set of tests 
        self.params_one = { 'stats': [ 'homeAndAway', 'winLoss', 'yearByYear', 'byDayOfWeek',
        'byDateRange', 'byDateRangeAdvanced', 'byDayOfWeek', 'byMonth' ], 'group': 'pitching' }

        # make the calls to return a list of objects
        stat_group_one = self.mlb.get_stats(self.pitching_player, self.params_one)

        # the list should not be empty
        self.assertTrue(len(stat_group_one))

        # stat_group_one should be greater than 8
        self.assertTrue(len(stat_group_one) > 8)

        # let's now build play off stat types
        self.params_two = { 'stats': [ 'homeAndAwayPlayoffs', 'winLossPlayoffs', 'yearByYearPlayoffs', 
        'byMonthPlayoffs', 'byDayOfWeekPlayoffs' ], 'group': 'pitching' }

        # Let's build this set of tests 
        stat_group_two = self.mlb.get_stats(self.pitching_player, self.params_two)

        # the list should not be empty
        self.assertTrue(len(stat_group_two))

        # stat_group_two 
        self.assertTrue(len(stat_group_two) > 5)

        self.params_three = { 'stats': [ 'pitchLog', 'playLog', 'gameLog' ], 'group': 'pitching' }

        # Let's build this set of stat types log 
        stat_group_three = self.mlb.get_stats(self.pitching_player, self.params_three)

        # the list should not be empty
        self.assertTrue(len(stat_group_three))

        # stat_group_two 
        self.assertTrue(len(stat_group_three) > 5)

        self.params_four = { 'stats': [ 'hotColdZones', 'pitchArsenal', 'opponentsFaced' ], 'group': 'pitching' }

        # Let's build this set of stat types log 
        stat_group_four = self.mlb.get_stats(self.pitching_player, self.params_four)

        # the list should not be empty
        self.assertTrue(len(stat_group_four))

        # stat_group_two 
        self.assertTrue(len(stat_group_four) > 3)

        self.params_five = { 'stats': [ 'expectedStatistics', 'sprayChart' ], 'group': 'pitching' }

        # Let's build this set of stat types log 
        stat_group_five = self.mlb.get_stats(self.pitching_player, self.params_five)

        # the list should not be empty
        self.assertTrue(len(stat_group_five))

        print(len(stat_group_five))
        # stat_group_five 
        self.assertTrue(len(stat_group_five) == 2)

        self.params_six = { 'stats': [ 'seasonAdvanced', 'season', 'careerAdvanced' ], 'group': 'pitching' }

        # Let's build this set of stat types log 
        stat_group_six = self.mlb.get_stats(self.pitching_player, self.params_six)

        # the list should not be empty
        self.assertTrue(len(stat_group_six))

        # stat_group_six should be 3  
        self.assertTrue(len(stat_group_six) == 3)