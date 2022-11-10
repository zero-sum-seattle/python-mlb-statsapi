from dataclasses import field
import unittest

from mlbstatsapi.mlb_api import Mlb
from mlbstatsapi import TheMlbStatsApiException


class TestPitchingTeamStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        # Oakland
        cls.al_team = cls.mlb.get_team(133)
        # Philadelphia Phillies
        cls.nl_team = cls.mlb.get_team(143)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_one_pitching_stats_for_teams(self):
        """mlb get stats should return pitching stats"""
        self.params = {'stats': ['season', 'seasonAdvanced'], 'group': ['pitching']}
        al_stats = self.mlb.get_stats(self.params, self.al_team)
        nl_stats = self.mlb.get_stats(self.params, self.nl_team)

        self.assertTrue(al_stats['pitching']['season'])
        self.assertTrue(al_stats['pitching']['seasonadvanced'])

        self.assertTrue(nl_stats['pitching']['season'])
        self.assertTrue(nl_stats['pitching']['seasonadvanced'])



    def test_get_pitching_career_stats_for_teams(self):
        """mlb get stats should return pitching stats"""
        self.params = {'stats': ['career', 'careerAdvanced'], 'group': ['pitching']}
        al_stats = self.mlb.get_stats(self.params, self.al_team)
        nl_stats = self.mlb.get_stats(self.params, self.nl_team)

        self.assertTrue(al_stats['pitching']['career'])
        self.assertTrue(al_stats['pitching']['careeradvanced'])

        self.assertTrue(nl_stats['pitching']['career'])
        self.assertTrue(nl_stats['pitching']['careeradvanced'])

    def test_building_playlog_500(self):
        """playlog should return 500 error"""
        self.params = {'stats': [ 'playLog'], 'group': 'hitting'}

        with self.assertRaises(TheMlbStatsApiException):
            al_stat_group_six = self.mlb.get_stats(self.params, self.al_team)

        self.params = { 'stats': ['sabermetrics'], 'group': ['pitching'] }
        with self.assertRaises(TheMlbStatsApiException):
            al_stats = self.mlb.get_stats(self.params, self.al_team)