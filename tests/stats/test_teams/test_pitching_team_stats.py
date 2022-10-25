from dataclasses import field
import unittest

from mlbstatsapi.mlbapi import Mlb

from mlbstatsapi.models.stats import (
    PitchingYBY,
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
        self.params = { 'stats': [ 'yearByYear' ], 'group': 'hitting' }

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
            self.assertIsInstance(stat, PitchingYBY)

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
            self.assertIsInstance(stat, PitchingYBY)

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
            

