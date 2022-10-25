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
    PitchingDBD,
    PitchingLog,
    PitchingGameLog,
    PitchingHAA
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
        self.params = { stats: [ 'season', 'statsSingleSeason' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingSeason)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, 'season'))

        self.params = { 'stats': [ 'seasonAdvanced', 'yearByYearAdvanced', 'statsSingleSeasonAdvanced' ], 'group': 'pitching' }
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
            self.assertTrue(hasattr(stat, "hits"))

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
        self.params = { 'stats': ['yearByYear', 'yearByYearPlayoffs'], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingYBY)

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
            self.assertIsInstance(stat, PitchingDBD)

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
        self.params = { 'stats': [ 'playLog', 'pitchLog' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingLog)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, 'ishome'))

    def test_get_bydate_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'byDateRange', 'byDateRangeAdvanced', 'byMonth', 'byMonthPlayoffs', 
        'byDayOfWeek', 'byDayOfWeekPlayoffs' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        self.assertTrue(len(stats) == 6)

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
        self.params = { 'stats': [ 'winLoss', 'winLossPlayoffs' ], 'group': 'pitching' }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        self.assertTrue(len(stats) > 1)

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, PitchingHAA)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, 'iswin'))