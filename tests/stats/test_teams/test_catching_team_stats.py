from dataclasses import field
import unittest

from mlbstatsapi import Mlb, MlbResult, TheMlbStatsApiException


class TestTeamCatchingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.al_team = cls.mlb.get_team(133) # Oakland
        cls.nl_team = cls.mlb.get_team(143) # Philadelphia Phillies

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_catching_season_stats_team(self):
        self.params = { 'stats': [ 'season' ], 'group': 'catching' }

        al_catching = self.mlb.get_stats(self.al_team, self.params)
        nl_catching = self.mlb.get_stats(self.nl_team, self.params)

        self.assertTrue(len(al_catching))
        self.assertTrue(len(nl_catching))

        self.assertTrue(len(al_catching) == 1)
        self.assertTrue(len(nl_catching) == 1)

    def test_catching_yearbyyear_stats_team(self):
        """yearbyyear stats should return list of yearbyyear stats"""
        self.params = { 'stats': [ 'yearByYear', 'yearByYearPlayoffs' ], 'group': 'catching' }

        nl_catching = self.mlb.get_stats(self.nl_team, self.params)

        self.assertTrue(len(nl_catching))

        self.assertTrue(len(nl_catching) > 2)

    def test_catching_career_stats_team(self):
        """career stats should return list of career stats"""

        self.params = { 'stats': [ 'career', 'careerRegularSeason' ], 'group': 'catching' }

        al_catching = self.mlb.get_stats(self.al_team, self.params)
        nl_catching = self.mlb.get_stats(self.nl_team, self.params)

        self.assertTrue(len(al_catching))
        self.assertTrue(len(nl_catching))

        self.assertTrue(len(al_catching) > 1)
        self.assertTrue(len(nl_catching) > 1)

    def test_catching_homeandaway_winloss_stats_team(self):
        """homeandaway and winloss stats should return 404"""
        self.params = { 'stats': [ 'homeAndAway', 'winLoss',  ], 'group': 'catching' }

        al_catching = self.mlb.get_stats(self.al_team, self.params)
        nl_catching = self.mlb.get_stats(self.nl_team, self.params)

        self.assertListEqual(al_catching, [])
        self.assertListEqual(nl_catching, [])

    def test_catching_byDateRange_byDayOfWeek_stats_team(self):
        self.params = { 'stats': [ 'byDateRange', 'byDayOfWeek',  ], 'group': 'catching' }

        al_catching = self.mlb.get_stats(self.al_team, self.params)
        nl_catching = self.mlb.get_stats(self.nl_team, self.params)

        self.assertTrue(len(al_catching))
        self.assertTrue(len(nl_catching))

        self.assertTrue(len(al_catching) > 2)
        self.assertTrue(len(nl_catching) > 2)

    def test_catching_gamelog_stats_team(self):
        self.params = { 'stats': [ 'gameLog' ], 'group': 'catching' }

        al_catching = self.mlb.get_stats(self.al_team, self.params)
        nl_catching = self.mlb.get_stats(self.nl_team, self.params)

        self.assertTrue(len(al_catching))
        self.assertTrue(len(nl_catching))

        self.assertTrue(len(al_catching) > 2)
        self.assertTrue(len(nl_catching) > 2)

    def test_catching_lastXGames_stats_team(self):
        self.params = { 'stats': [ 'lastXGames' ], 'group': 'catching' }

        al_catching = self.mlb.get_stats(self.al_team, self.params)
        nl_catching = self.mlb.get_stats(self.nl_team, self.params)

        self.assertTrue(len(al_catching))
        self.assertTrue(len(nl_catching))

        self.assertTrue(len(al_catching) == 1)
        self.assertTrue(len(nl_catching) == 1)

        # # check for None, or NoneType
        # self.assertTrue(len(stat_group_six))

        # # stat_group_two 
        # self.assertTrue(len(stat_group_six) > 2)

        # self.params_seven = { 'stats': [ 'lastXGames' ], 'group': 'catching' }

        # stat_group_seven = self.mlb.get_stats(self.catching_player, self.params_seven)

        # # check for None, or NoneType
        # self.assertTrue(len(stat_group_seven))