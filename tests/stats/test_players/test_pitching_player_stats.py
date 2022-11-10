from dataclasses import field
import unittest

from mlbstatsapi.mlb_api import Mlb

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
        self.params = {'stats': ['season', 'statsSingleSeason'], 'group': ['pitching']}
        stats = self.mlb.get_stats(self.params, self.pitching_player)

        self.assertTrue(stats['pitching']['season'])
        self.assertTrue(stats['pitching']['statssingleseason'])

        self.params = {'stats': ['seasonAdvanced', 'statsSingleSeasonAdvanced'], 'group': ['pitching']}
        stats = self.mlb.get_stats(self.params, self.pitching_player)

        self.assertTrue(stats['pitching']['seasonadvanced'])
        self.assertTrue(stats['pitching']['statssingleseasonadvanced'])

    def test_get_sabermetrics_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = {'stats': ['sabermetrics'], 'group': ['pitching']}
        stats = self.mlb.get_stats(self.params, self.pitching_player)

        self.assertTrue(stats['pitching']['sabermetrics'])

    def test_get_pitching_career_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = {'stats': ['career', 'careerAdvanced'], 'group': ['pitching']}
        stats = self.mlb.get_stats(self.params, self.pitching_player)

        self.assertTrue(stats['pitching']['career'])
        self.assertTrue(stats['pitching']['careeradvanced'])

    def test_get_gamelog_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = {'stats': ['gameLog'], 'group': ['pitching']}
        stats = self.mlb.get_stats(self.params, self.pitching_player)

        self.assertTrue(stats['pitching']['gamelog'])

    def test_get_playlog_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = {'stats': ['playLog'], 'group': ['pitching']}
        stats = self.mlb.get_stats(self.params, self.pitching_player)

        self.assertTrue(stats['pitching']['playlog'])

    def test_get_yearbyyear_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = {'stats': ['yearByYear'], 'group': ['pitching']}
        stats = self.mlb.get_stats(self.params, self.pitching_player)

        self.assertTrue(stats['pitching']['yearbyyear'])





   