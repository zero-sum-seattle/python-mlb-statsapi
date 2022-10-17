import unittest

from mlbstatsapi.models.stats import SimpleHitting, AdvancedHitting, SimplePitching
from mlbstatsapi.mlbapi import Mlb
from mlbstatsapi.models.stats.pitching import SimplePitching


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

    def test_get_one_hitting_stats_for_player(self):
        """mlb get stats should return hitting stats"""
        self.params = { "stats": ["season"], "group": "hitting" }

        hitting_stats = self.mlb.get_stats(self.position_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(hitting_stats)

        for stat in hitting_stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleHitting
            self.assertIsInstance(stat, SimpleHitting)

        self.params = { "stats": ["seasonAdvanced"], "group": "hitting" }

        advanced_hitting = self.mlb.get_stats(self.position_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(advanced_hitting)

        for stat in advanced_hitting:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be AdvancedHitting
            self.assertIsInstance(stat, AdvancedHitting)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'totalbases'))

    def test_get_one_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { "stats": ["season"], "group": "pitching" }
        hitting_stats = self.mlb.get_stats(self.pitching_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(hitting_stats)

        for stat in hitting_stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, SimplePitching)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, "hits"))
        
    def test_one_hitting_stats_for_team(self):
        """mlb get stats should return hitting stats"""
        self.params = { "stats": ["season"], "group": "hitting" }
            
        hitting_stats = self.mlb.get_stats(self.team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(hitting_stats)

        for stat in hitting_stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleHitting
            self.assertIsInstance(stat, SimpleHitting)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, "hits"))

    def test_yearbyyear_hitting_stats_for_team(self):
        """mlb get stats should return hitting stats"""
        self.params = { "stats": [ 'yearByYear' ], "group": "hitting" }
        yearbyyear_stats = self.mlb.get_stats(self.team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(yearbyyear_stats)

        # check objects is > 1
        self.assertTrue(len(yearbyyear_stats) > 10)
        for stat in yearbyyear_stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleHitting
            self.assertIsInstance(stat, SimpleHitting)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, "hits"))
        

    def test_yearbyyear_hitting_stats_for_player(self):
        """mlb get stats should return hitting stats"""
        self.params = { "stats": [ 'yearByYear' ], "group": "hitting" }
        yearbyyear_stats = self.mlb.get_stats(self.position_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(yearbyyear_stats)

        # check objects is > 1
        self.assertTrue(len(yearbyyear_stats) > 2)
        for stat in yearbyyear_stats:
            # test that split is not NoneType
            self.assertTrue(stat)

            # split should be HittingSplits
            self.assertIsInstance(stat, SimpleHitting)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, "hits"))

    def test_get_one_pitching_stats_for_team(self):
        """mlb get stats should return pitching stats"""
        self.params = { "stats": [ "season" ], "group": "pitching" }
        
        pitching_splits = self.mlb.get_stats(self.team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(pitching_splits)

        for stat in pitching_splits:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be HittingSplits
            self.assertIsInstance(stat, SimplePitching)

            # stat should have attr set
            self.assertTrue(hasattr(stat, "hits"))

    def test_get_multiple_stats(self):
        """mlb get stats should return two hitting stats"""
        self.params = { 'stats': [ "seasonAdvanced", "season" ], 'group': 'hitting' }

        hitting_stats = self.mlb.get_stats(self.position_player, self.params)

        self.assertIsNotNone(hitting_stats)

        self.assertTrue(len(hitting_stats) > 1)

        self.params = { 'stats': [ "seasonAdvanced", "season" ], 'group': 'pitching' }

        hitting_stats = self.mlb.get_stats(self.pitching_player, self.params)

        self.assertIsNotNone(hitting_stats)

        self.assertTrue(len(hitting_stats) > 1)



