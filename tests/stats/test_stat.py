import unittest

from mlbstatsapi.models.stats import SeasonHitting, SeasonAdvancedHitting, SeasonPitching
from mlbstatsapi.mlbapi import Mlb


class TestStatCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.team = cls.mlb.get_team(133)
        cls.position_player = cls.mlb.get_person(665742)
        cls.pitching_player = cls.mlb.get_person(592662)


    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_hitting_stats_for_player(self):
        """mlb get stats should return hitting splits"""
        self.params = { "stats": "season", "group": "hitting" }

        hitting_splits = self.mlb.get_stats(self.position_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(hitting_splits)

        for split in hitting_splits:
            # test that split is not NoneType
            self.assertTrue(split)

            # split should be HittingSplits
            self.assertIsInstance(split, SeasonHitting)

    def test_get_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { "stats": "season", "group": "pitching" }
        hitting_splits = self.mlb.get_stats(self.pitching_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(hitting_splits)

        for split in hitting_splits:
            # test that split is not NoneType
            self.assertTrue(split)

            # split should be HittingSplits
            self.assertIsInstance(split, SeasonPitching)
        
    def test_hitting_stats_for_team(self):
        """mlb get stats should return hitting splits"""
        self.params = { "stats": "season", "group": "hitting" }
            
        hitting_splits = self.mlb.get_stats(self.team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(hitting_splits)

        for split in hitting_splits:
            # test that split is not NoneType
            self.assertTrue(split)

            # split should be HittingSplits
            self.assertIsInstance(split, SeasonHitting)

    def test_get_pitching_stats_for_team(self):
        """mlb get stats should return pitching stats"""
        self.params = { "stats": "season", "group": "pitching" }
        
        pitching_splits = self.mlb.get_stats(self.team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(pitching_splits)

        for split in pitching_splits:
            # test that split is not NoneType
            self.assertTrue(split)

            # split should be HittingSplits
            self.assertIsInstance(split, SeasonPitching)
