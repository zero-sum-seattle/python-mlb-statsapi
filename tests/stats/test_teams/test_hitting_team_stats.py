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
    ExpectedStatistics
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
        """mlb get stats should return hitting stats"""
        self.params = { 'stats': [ 'opponentsFaced' ], 'group': 'hitting' }
        al_opponents_faced = self.mlb.get_stats(self.al_team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(al_opponents_faced)

        # we should have a ton of objects
        self.assertTrue(len(al_opponents_faced) == 234)

        for stat in al_opponents_faced:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, OpponentsFacedHitting)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'fieldingteam'))
            self.assertTrue(hasattr(stat, 'batter'))

        nl_opponents_faced = self.mlb.get_stats(self.al_team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(nl_opponents_faced)

        # we should have a ton of objects
        self.assertTrue(len(nl_opponents_faced) == 234)

        for stat in nl_opponents_faced:
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
            self.assertIsInstance(stat, HittingSeason)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'totalbases'))

        nl_hitting_stats = self.mlb.get_stats(self.nl_team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(nl_hitting_stats)

        for stat in nl_hitting_stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleHitting
            self.assertIsInstance(stat, HittingSeason)

        self.params = { 'stats': [ 'seasonAdvanced' ], 'group': 'hitting' }

        nl_hitting_stats = self.mlb.get_stats(self.nl_team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(nl_hitting_stats)

        for stat in nl_hitting_stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be AdvancedHitting
            self.assertIsInstance(stat, HittingSeason)

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
            self.assertIsInstance(stat, ExpectedStatistics)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'wobacon'))
            self.assertTrue(hasattr(stat, 'woba'))

        nl_expected_stats = self.mlb.get_stats(self.nl_team, self.params)

        # pitch_arsenal_stats should not be None or NoneType
        self.assertIsNotNone(nl_expected_stats)

        for stat in nl_expected_stats:

            # stat should be PitchArsenal
            self.assertIsInstance(stat, ExpectedStatistics)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'wobacon'))
            self.assertTrue(hasattr(stat, 'woba'))


    def test_hitting_hot_cold_zone_on_teams(self):
        """mlb get stats should return PitchArsenal object"""
        self.params = { 'stats': [ 'hotColdZones' ], 'group': 'hitting' }
    
        al_hot_cold_zone = self.mlb.get_stats(self.al_team, self.params)

        # hot_cold_zone should not be empty
        self.assertTrue(len(al_hot_cold_zone))

        for stat in al_hot_cold_zone:
            # stat should be a HotColdZones
            self.assertIsInstance(stat, HotColdZones)

            for zone in stat.zones:
            # stat should be ZoneCodes
                self.assertIsInstance(zone, ZoneCodes)

                # stat should have attr set
                self.assertTrue(hasattr(zone, 'zone'))
                self.assertTrue(hasattr(zone, 'value'))

        nl_hot_cold_zone = self.mlb.get_stats(self.nl_team, self.params)

        # hot_cold_zone should not be empty
        self.assertTrue(len(nl_hot_cold_zone))

        for stat in nl_hot_cold_zone:
            # stat should be a HotColdZones
            self.assertIsInstance(stat, HotColdZones)

            for zone in stat.zones:
            # stat should be ZoneCodes
                self.assertIsInstance(zone, ZoneCodes)

                # stat should have attr set
                self.assertTrue(hasattr(zone, 'zone'))
                self.assertTrue(hasattr(zone, 'value'))


    def test_pitch_arsenal_stat_on_teams(self):
        """mlb get stats should return PitchArsenal object"""
        self.params = { 'stats': [ 'pitchArsenal' ], 'group': 'hitting' }
    
        al_pitch_arsenal_stats = self.mlb.get_stats(self.al_team, self.params)

        # pitch_arsenal_stats should not be None or NoneType
        self.assertIsNotNone(al_pitch_arsenal_stats)

        # pitch_arsenal_stats should be greater than 1
        self.assertTrue(len(al_pitch_arsenal_stats) > 1)

        for stat in al_pitch_arsenal_stats:

            # stat should be PitchArsenal
            self.assertIsInstance(stat, PitchArsenal)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'totalpitches'))
            self.assertTrue(hasattr(stat, 'percentage'))


        nl_pitch_arsenal_stats = self.mlb.get_stats(self.nl_team, self.params)

        # pitch_arsenal_stats should not be None or NoneType
        self.assertIsNotNone(nl_pitch_arsenal_stats)

        # pitch_arsenal_stats should be greater than 1
        self.assertTrue(len(nl_pitch_arsenal_stats) > 1)

        for stat in nl_pitch_arsenal_stats:

            # stat should be PitchArsenal
            self.assertIsInstance(stat, PitchArsenal)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'totalpitches'))
            self.assertTrue(hasattr(stat, 'percentage'))