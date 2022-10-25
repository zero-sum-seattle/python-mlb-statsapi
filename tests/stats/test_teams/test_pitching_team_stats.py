from dataclasses import field
import unittest

from mlbstatsapi.mlbapi import Mlb

from mlbstatsapi.models.stats import (
    HittingSeason,
    HittingYBY,
    SimplePitching,
    pitching
)

class TestTeamStatCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.team = cls.mlb.get_team(133) # Oakland A's

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_yearbyyear_hitting_stats_for_team(self):
        """mlb get stats should return hitting stats"""
        self.params = { "stats": [ 'yearByYear' ], "group": "hitting" }

        # let's get some stats
        yearbyyear_stats = self.mlb.get_stats(self.team, self.params)

        # check for None, or NoneType
        self.assertNotEqual(yearbyyear_stats, [])

        # check objects is > 1
        self.assertTrue(len(yearbyyear_stats) > 10)
        for stat in yearbyyear_stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleHitting
            self.assertIsInstance(stat, HittingYBY)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, "hits"))

    def test_get_one_pitching_stats_for_team(self):
        """mlb get stats should return pitching stats"""
        self.params = { "stats": [ "season" ], "group": "pitching" }
        
        pitching_splits = self.mlb.get_stats(self.team, self.params)

        # check for None, or NoneType
        self.assertNotEqual(pitching_splits, [])

        for stat in pitching_splits:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be HittingSplits
            self.assertIsInstance(stat, SimplePitching)

            # stat should have attr set
            self.assertTrue(hasattr(stat, "hits"))

    def test_multiple_pitching_stats_for_team(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'season', 'career', 'seasonAdvanced', 'careerAdvanced' ], 'group': 'pitching' }

        # let's get some stats
        pitching_splits = self.mlb.get_stats(self.team, self.params)

        # check for empty list
        self.assertNotEqual(pitching_splits, [])

        # the end point should give us 4 objects back
        self.assertEqual(len(pitching_splits), 4)
            

