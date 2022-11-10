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
        """get a basic season stat split"""
        self.params = {'stats': ['season'], 'group': ['catching']}

        al_catching = self.mlb.get_stats(self.params, self.al_team)
        nl_catching = self.mlb.get_stats(self.params, self.nl_team)

        self.assertTrue(al_catching['catching']['season'])
        self.assertTrue(nl_catching['catching']['season'])

    def test_catching_yearbyyear_stats_team(self):
        """yearbyyear stats should return list of yearbyyear stats"""
        self.params = {'stats': ['yearByYear', 'yearByYearPlayoffs'], 'group':['catching']}
        nl_catching = self.mlb.get_stats(self.params, self.nl_team)

        self.assertTrue(nl_catching['catching']['yearbyyear'])
        self.assertTrue(nl_catching['catching']['yearbyyearplayoffs'])

    def test_catching_career_stats_team(self):
        """career stats should return list of career stats"""
        self.params = {'stats': ['career', 'careerRegularSeason'], 'group':['catching']}

        al_catching = self.mlb.get_stats(self.params, self.al_team)
        nl_catching = self.mlb.get_stats(self.params, self.nl_team)

        # check if lists are not empty
        self.assertTrue(al_catching['catching']['career'])
        self.assertTrue(nl_catching['catching']['careerregularseason'])

    def test_catching_homeandaway_winloss_stats_team(self):
        """homeandaway and winloss stats should return 404"""
        self.params = {'stats': ['homeAndAway', 'winLoss', ], 'group':['catching']}

        # check if lists are empty
        al_catching = self.mlb.get_stats(self.params, self.al_team)

        self.assertEqual({}, al_catching)

    def test_catching_byDateRange_byDayOfWeek_stats_team(self):
        self.params = {'stats': ['byDateRange', 'byDayOfWeek'], 'group':['catching']}

        # check if lists are not empty
        al_catching = self.mlb.get_stats(self.params, self.al_team)
        nl_catching = self.mlb.get_stats(self.params, self.nl_team)
        self.assertTrue(al_catching['catching']['bydaterange'])
        self.assertTrue(nl_catching['catching']['bydayofweek'])

    def test_catching_gamelog_stats_team(self):
        self.params = {'stats': ['gameLog'], 'group':['catching']}

        # check if lists are not empty
        al_catching = self.mlb.get_stats(self.params, self.al_team)
        nl_catching = self.mlb.get_stats(self.params, self.nl_team)
        self.assertTrue(al_catching['catching']['gamelog'])
        self.assertTrue(nl_catching['catching']['gamelog'])

    def test_catching_lastXGames_stats_team(self):
        self.params = {'stats': ['lastXGames'], 'group': ['catching']}

        # check if lists are not empty
        al_catching = self.mlb.get_stats(self.params, self.al_team)
        nl_catching = self.mlb.get_stats(self.params, self.nl_team)
        self.assertTrue(al_catching['catching']['lastxgames'])
        self.assertTrue(nl_catching['catching']['lastxgames'])
        