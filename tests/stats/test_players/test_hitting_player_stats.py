from dataclasses import field
import unittest

from mlbstatsapi.mlbapi import Mlb

from mlbstatsapi.models.stats import (
    HittingSeason,
    OpponentsFacedHitting,
    HotColdZones,
    ZoneCodes,
    HittingYearByYear,
    PitchArsenal,
    HittingExpectedStatistics,
    HittingSeasonAdvanced,
    HittingPitchLog,
    HittingPlayLog,
    HittingWinLoss,
    HittingHomeAndAway
)

class TestPlayerHittingStats(unittest.TestCase):
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

    def test_hitting_opponents_faced_position(self):
        """mlb get stats should return hitting stats"""
        self.params = { 'stats': [ 'opponentsFaced' ], 'group': 'hitting' }
        opponents_faced = self.mlb.get_stats(self.position_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(opponents_faced)

        # we should have a ton of objects
        self.assertTrue(len(opponents_faced) == 234)

        for stat in opponents_faced:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, OpponentsFacedHitting)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'fieldingteam'))
            self.assertTrue(hasattr(stat, 'batter'))

    def test_get_one_hitting_stats_for_player(self):
        """mlb get stats should return hitting stats"""
        self.params = { 'stats': [ 'season' ], 'group': 'hitting' }

        hitting_stats = self.mlb.get_stats(self.position_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(hitting_stats)

        for stat in hitting_stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleHitting
            self.assertIsInstance(stat, HittingSeason)

        self.params = { 'stats': [ 'seasonAdvanced' ], 'group': 'hitting' }

        advanced_hitting = self.mlb.get_stats(self.position_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(advanced_hitting)

        for stat in advanced_hitting:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be AdvancedHitting
            self.assertIsInstance(stat, HittingSeasonAdvanced)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'totalbases'))

    def test_yearbyyear_hitting_stats_for_player(self):
        """mlb get stats should return hitting stats"""
        self.params = { "stats": [ 'yearByYear' ], 'group': 'hitting' }
        yearbyyear_stats = self.mlb.get_stats(self.position_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(yearbyyear_stats)

        # check objects is > 1
        self.assertTrue(len(yearbyyear_stats) > 2)
        
        for stat in yearbyyear_stats:
            # test that split is not NoneType
            self.assertTrue(stat)

            # split should be HittingSplits
            self.assertIsInstance(stat, HittingYearByYear)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, "hits"))

    def test_get_multiple_stats_for_player(self):
        """mlb get stats should return two hitting stats"""
        self.params = { 'stats': [ 'seasonAdvanced', 'season', 'careerAdvanced', 'hotColdZones', 'yearByYear' ], 'group': 'hitting' }

        stats = self.mlb.get_stats(self.position_player, self.params)

        self.assertIsNotNone(stats)

        self.assertTrue(len(stats) > 4)

    def test_hitting_pitch_arsenal_stat_on_position_player(self):
        """mlb get stats should return PitchArsenal object"""
        self.params = { 'stats': [ 'expectedStatistics' ], 'group': 'hitting' }
    
        expected_stats = self.mlb.get_stats(self.position_player, self.params)

        # pitch_arsenal_stats should not be None or NoneType
        self.assertIsNotNone(expected_stats)

        for stat in expected_stats:

            # stat should be PitchArsenal
            self.assertIsInstance(stat, HittingExpectedStatistics)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'wobacon'))
            self.assertTrue(hasattr(stat, 'woba'))

    def test_hitting_hot_cold_zone_on_position_player(self):
        """mlb get stats should return PitchArsenal object"""
        self.params = { 'stats': [ 'hotColdZones' ], 'group': 'hitting' }
    
        hot_cold_zone = self.mlb.get_stats(self.position_player, self.params)

        # hot_cold_zone should not be empty
        self.assertTrue(len(hot_cold_zone))

        for stat in hot_cold_zone:
            # stat should be a HotColdZones
            self.assertIsInstance(stat, HotColdZones)

            for zone in stat.zones:
            # stat should be ZoneCodes
                self.assertIsInstance(zone, ZoneCodes)

                # stat should have attr set
                self.assertTrue(hasattr(zone, 'zone'))
                self.assertTrue(hasattr(zone, 'value'))

    def test_pitch_arsenal_stat_on_position_player(self):
        """mlb get stats should return PitchArsenal object"""
        self.params = { 'stats': [ 'pitchArsenal' ], 'group': 'hitting' }
    
        pitch_arsenal_stats = self.mlb.get_stats(self.position_player, self.params)

        # pitch_arsenal_stats should not be None or NoneType
        self.assertIsNotNone(pitch_arsenal_stats)

        # pitch_arsenal_stats should be greater than 1
        self.assertTrue(len(pitch_arsenal_stats) > 1)

        for stat in pitch_arsenal_stats:

            # stat should be PitchArsenal
            self.assertIsInstance(stat, PitchArsenal)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'totalpitches'))
            self.assertTrue(hasattr(stat, 'percentage'))

    def test_pitch_arsenal_stat_on_position_player(self):
        """mlb get stats should return two hittinglog objects object"""
        self.params = { 'stats': [ 'playLog' ], 'group': 'hitting' }
    
        log_stats = self.mlb.get_stats(self.position_player, self.params)

        # pitch_arsenal_stats should not be None or NoneType
        self.assertIsNotNone(log_stats)

        # pitch_arsenal_stats should be greater than 1
        self.assertTrue(len(log_stats) == 1)

        for stat in log_stats:

            # stat should be PitchArsenal
            self.assertIsInstance(stat, HittingPlayLog)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'pitchnumber'))
            self.assertTrue(hasattr(stat, 'atbatnumber'))

    def test_pitch_arsenal_stat_on_position_player(self):
        """mlb get stats should return two hittinglog objects object"""
        self.params = { 'stats': [ 'pitchLog' ], 'group': 'hitting' }
    
        log_stats = self.mlb.get_stats(self.position_player, self.params)

        # pitch_arsenal_stats should not be None or NoneType
        self.assertIsNotNone(log_stats)

        # pitch_arsenal_stats should be greater than 1
        self.assertTrue(len(log_stats) > 1)

        for stat in log_stats:

            # stat should be PitchArsenal
            self.assertIsInstance(stat, HittingPitchLog)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'pitchnumber'))
            self.assertTrue(hasattr(stat, 'atbatnumber'))

    def test_hitting_log_stats_stat_on_position_player(self):
        """mlb get stats should return two hittinglog objects object"""
        self.params = { 'stats': [ 'byDateRange', 'byDateRangeAdvanced', 'byMonthPlayoffs', 
        'byMonth', 'byDayOfWeek', 'byDayOfWeekPlayoffs' ], 'group': 'hitting' }
    
        hitting_dates = self.mlb.get_stats(self.position_player, self.params)

        # pitch_arsenal_stats should not be None or NoneType
        self.assertIsNotNone(hitting_dates)

        # pitch_arsenal_stats should be greater than 1
        self.assertTrue(len(hitting_dates) == 6)

        for stat in hitting_dates:

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'numteams'))

    def test_hitting_winloss_on_position_player(self):
        """mlb get stats should return two hittinglog objects object"""
        self.params = { 'stats': [ 'winLoss', 'winLossPlayoffs' ], 'group': 'hitting' }
    
        hitting_wl = self.mlb.get_stats(self.position_player, self.params)

        # hot_cold_zone should not be empty
        self.assertTrue(len(hitting_wl))

        # pitch_arsenal_stats should be greater than 1
        self.assertTrue(len(hitting_wl) == 2)

        for stat in hitting_wl:

            # stat should be HittingWL
            self.assertIsInstance(stat, HittingWinLoss)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'iswin'))

    def test_hitting_log_stats_stat_on_position_player(self):
        """mlb get stats should return two hittinglog objects object"""
        self.params = { 'stats': [ 'homeAndAway', 'homeAndAwayPlayoffs' ], 'group': 'hitting' }
    
        hitting_wl = self.mlb.get_stats(self.position_player, self.params)

        for stat in hitting_wl:

            # stat should be HittingWL
            self.assertIsInstance(stat, HittingHomeAndAway)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'ishome'))

    def test_building_all_hitting_objects(self):
        """this test will build all what should be working stat objects"""
        # Let's build this set of tests 
        self.params_one = { 'stats': [ 'homeAndAway', 'winLoss', 'yearByYear', 'byDayOfWeek',
        'byDateRange', 'byDateRangeAdvanced', 'byDayOfWeek', 'byMonth' ], 'group': 'hitting' }

        # make the calls to return a list of objects
        stat_group_one = self.mlb.get_stats(self.position_player, self.params_one)

        # the list should not be empty
        self.assertTrue(len(stat_group_one))

        # stat_group_one should be greater than 8
        self.assertTrue(len(stat_group_one) > 8)

        # let's now build play off stat types
        self.params_two = { 'stats': [ 'homeAndAwayPlayoffs', 'winLossPlayoffs', 'yearByYearPlayoffs', 
        'byMonthPlayoffs', 'byDayOfWeekPlayoffs' ], 'group': 'hitting' }

        # Let's build this set of tests 
        stat_group_two = self.mlb.get_stats(self.position_player, self.params_two)

        # the list should not be empty
        self.assertTrue(len(stat_group_two))

        # stat_group_two 
        self.assertTrue(len(stat_group_two) > 5)

        self.params_three = { 'stats': [ 'pitchLog', 'playLog', 'gameLog' ], 'group': 'hitting' }

        # Let's build this set of stat types log 
        stat_group_three = self.mlb.get_stats(self.position_player, self.params_three)

        # the list should not be empty
        self.assertTrue(len(stat_group_three))

        # stat_group_two 
        self.assertTrue(len(stat_group_three) > 5)

        self.params_four = { 'stats': [ 'hotColdZones', 'pitchArsenal', 'opponentsFaced' ], 'group': 'hitting' }

        # Let's build this set of stat types log 
        stat_group_four = self.mlb.get_stats(self.position_player, self.params_four)

        # the list should not be empty
        self.assertTrue(len(stat_group_four))

        # stat_group_two 
        self.assertTrue(len(stat_group_four) > 3)

        self.params_five = { 'stats': [ 'expectedStatistics', 'sprayChart' ], 'group': 'hitting' }

        # Let's build this set of stat types log 
        stat_group_five = self.mlb.get_stats(self.position_player, self.params_five)

        # the list should not be empty
        self.assertTrue(len(stat_group_five))

        print(len(stat_group_five))
        # stat_group_five 
        self.assertTrue(len(stat_group_five) == 2)

        self.params_six = { 'stats': [ 'seasonAdvanced', 'season', 'careerAdvanced' ], 'group': 'hitting' }

        # Let's build this set of stat types log 
        stat_group_six = self.mlb.get_stats(self.position_player, self.params_six)

        # the list should not be empty
        self.assertTrue(len(stat_group_six))

        # stat_group_six should be 3  
        self.assertTrue(len(stat_group_six) > 3)

        

        

