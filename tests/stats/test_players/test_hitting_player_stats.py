from dataclasses import field
import unittest

from mlbstatsapi.mlbapi import Mlb

from mlbstatsapi.models.stats import (
    HittingSeason,
    OpponentsFacedHitting,
    HotColdZones,
    ZoneCodes,
    HittingYBY,
    PitchArsenal,
    ExpectedStatistics,
    HittingLog,
    HittingWL,
    HittingHAA,
    HittingAdvancedSeason
)

class TestOpponentsFacedHitting(unittest.TestCase):
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
            self.assertIsInstance(stat, HittingAdvancedSeason)

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
            self.assertIsInstance(stat, HittingYBY)

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
            self.assertIsInstance(stat, ExpectedStatistics)

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
        self.params = { 'stats': [ 'playLog', 'pitchLog' ], 'group': 'hitting' }
    
        log_stats = self.mlb.get_stats(self.position_player, self.params)

        # pitch_arsenal_stats should not be None or NoneType
        self.assertIsNotNone(log_stats)

        # pitch_arsenal_stats should be greater than 1
        self.assertTrue(len(log_stats) == 2)

        for stat in log_stats:

            # stat should be PitchArsenal
            self.assertIsInstance(stat, HittingLog)

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
            self.assertIsInstance(stat, HittingWL)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'iswin'))

    def test_hitting_log_stats_stat_on_position_player(self):
        """mlb get stats should return two hittinglog objects object"""
        self.params = { 'stats': [ 'homeAndAway', 'homeAndAwayPlayoffs' ], 'group': 'hitting' }
    
        hitting_wl = self.mlb.get_stats(self.position_player, self.params)

        # hot_cold_zone should not be empty
        self.assertTrue(len(hitting_wl))

        # pitch_arsenal_stats should be greater than 1
        self.assertTrue(len(hitting_wl) == 2)

        for stat in hitting_wl:

            # stat should be HittingWL
            self.assertIsInstance(stat, HittingHAA)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'ishome'))