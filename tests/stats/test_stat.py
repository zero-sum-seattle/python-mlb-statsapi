from dataclasses import field
import unittest

from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team
from mlbstatsapi.mlbapi import Mlb

from mlbstatsapi.models.stats import (
    SimpleHitting,
    AdvancedHitting,
    SimpleCatching,
    SimplePitching,
    AdvancedPitching,
    SimpleFielding,
    OpponentsFacedHitting,
    HotColdZones,
    ZoneCodes,
    PitchArsenal
)


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
            self.assertTrue(hasattr(stat, 'chances'))
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
            self.assertTrue(hasattr(stat, 'doubleplays'))
            self.assertTrue(hasattr(stat, 'fielding'))

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

class TestOpponentsFacedHitting(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.position_player = cls.mlb.get_person(665742) # Juan Soto
        cls.pitching_player = cls.mlb.get_person(592662) # Robbie Ray
        cls.catching_player = cls.mlb.get_person(663728) # Cal Raleigh

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_opponents_faced_position(self):
        """mlb get stats should return hitting stats"""
        self.params = { "stats": [ "opponentsFaced" ], "group": "hitting" }
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

            # attr should be classes
            self.assertIsInstance(stat.batter, Person)
            self.assertIsInstance(stat.fieldingteam, Team)

class TestHittingLogStatTypes(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.position_player = cls.mlb.get_person(665742) # Juan Soto

    @classmethod
    def tearDownClass(cls) -> None:
        pass

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

class TestHittingLogStatTypes(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.position_player = cls.mlb.get_person(665742) # Juan Soto

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_pitch_arsenal_stat_on_position_player(self):
        """mlb get stats should return PitchArsenal object"""
        self.params = { 'stats': [ 'expectedStatistics' ], 'group': 'hitting' }
    
        expected_stats = self.mlb.get_stats(self.position_player, self.params)

        # pitch_arsenal_stats should not be None or NoneType
        self.assertIsNotNone(expected_stats)

        for stat in expected_stats:

            # stat should be PitchArsenal
            self.assertIsInstance(stat, )

            # stat should have attr set
            self.assertTrue(hasattr(stat, 'wobacon'))
            self.assertTrue(hasattr(stat, 'woba'))

class TestHotCodeZones(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.position_player = cls.mlb.get_person(665742) # Juan Soto

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_pitch_arsenal_stat_on_position_player(self):
        """mlb get stats should return PitchArsenal object"""
        self.params = { 'stats': [ 'hotColdZones' ], 'group': 'hitting' }
    
        hot_code_zone = self.mlb.get_stats(self.position_player, self.params)

        # hot_code_zone should not be None or NoneType
        self.assertIsNotNone(hot_code_zone)


        for stat in hot_code_zone:
            self.assertIsInstance(stat, HotColdZones)
            for zone in stat.zones:
            # stat should be ZoneCodes
                self.assertIsInstance(zone, ZoneCodes)

                # stat should have attr set
                self.assertTrue(hasattr(zone, 'zone'))
                self.assertTrue(hasattr(zone, 'value'))