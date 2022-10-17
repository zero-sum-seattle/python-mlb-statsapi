from dataclasses import field
import unittest

from mlbstatsapi.models.stats import SimpleHitting, AdvancedHitting, SimpleCatching, SimplePitching, AdvancedPitching
from mlbstatsapi.mlbapi import Mlb
from mlbstatsapi.models.stats import fielding
from mlbstatsapi.models.stats.fielding import SimpleFielding


class TestPlayerStatCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.position_player = cls.mlb.get_person(665742) # Juan Soto
        cls.pitching_player = cls.mlb.get_person(592662) # Robbie Ray
        cls.catching_player = cls.mlb.get_person(663728) # Cal Raleigh

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
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(stats)

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, SimplePitching)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, "hits"))

        self.params = { "stats": ["seasonAdvanced"], "group": "pitching" }
        stats = self.mlb.get_stats(self.pitching_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(stats)

        for stat in stats:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimplePitching
            self.assertIsInstance(stat, AdvancedPitching)

            # stat should have a attr set
            self.assertTrue(hasattr(stat, "homerunsper9"))

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

    def test_catching_season_stats_for_catcher(self):
        self.params = { "stats": ["season"], "group": "catching" }

        catching = self.mlb.get_stats(self.catching_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(catching)

        for stat in catching:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, SimpleCatching)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'passedball'))

    def test_fielding_season_stats_for_players(self):
        self.params = { "stats": ["season"], "group": "fielding" }

        # catching_player
        fielding = self.mlb.get_stats(self.catching_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(fielding)

        for stat in fielding:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, SimpleFielding)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'errors'))
            self.assertTrue(hasattr(stat, 'gamesplayed'))

        self.params = { "stats": ["season"], "group": "fielding" }

        # pitching_player
        fielding = self.mlb.get_stats(self.pitching_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(fielding)

        for stat in fielding:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, SimpleFielding)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'errors'))
            self.assertTrue(hasattr(stat, 'gamesplayed'))

        self.params = { "stats": ["season"], "group": "fielding" }

        # position_player
        fielding = self.mlb.get_stats(self.position_player, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(fielding)

        for stat in fielding:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, SimpleFielding)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'errors'))
            self.assertTrue(hasattr(stat, 'gamesplayed'))

    def test_get_multiple_stats_for_player(self):
        """mlb get stats should return two hitting stats"""
        self.params = { 'stats': [ "seasonAdvanced", "season", "careerAdvanced" ], 'group': 'hitting' }

        stats = self.mlb.get_stats(self.position_player, self.params)

        self.assertIsNotNone(stats)

        self.assertTrue(len(stats) > 2)

        self.params = { 'stats': [ "seasonAdvanced", "season" ], 'group': 'pitching' }

        stats = self.mlb.get_stats(self.pitching_player, self.params)

        self.assertIsNotNone(stats)

        self.assertTrue(len(stats) > 1)


class TestTeamStatCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.team = cls.mlb.get_team(133) # Oakland A's

    @classmethod
    def tearDownClass(cls) -> None:
        pass

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

    def test_fielding_season_stats_for_team(self):
        self.params = { "stats": ["season"], "group": "fielding" }

        # catching_player
        fielding = self.mlb.get_stats(self.team, self.params)

        # check for None, or NoneType
        self.assertIsNotNone(fielding)

        for stat in fielding:
            # test that stat is not NoneType
            self.assertTrue(stat)

            # stat should be SimpleCatching
            self.assertIsInstance(stat, SimpleFielding)

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'errors'))
            self.assertTrue(hasattr(stat, 'gamesplayed'))





