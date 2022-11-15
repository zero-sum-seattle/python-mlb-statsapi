import unittest

from mlbstatsapi.mlb_api import Mlb
from mlbstatsapi import TheMlbStatsApiException


class TestTeamHitting(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()

        # Oakland
        cls.al_team = 133

        # Philadelphia Phillies
        cls.nl_team = 143

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_hitting_stats_for_teams(self):
        """mlb get stats should return hitting stats"""
        self.params = {'stats': ['season', 'seasonAdvanced'], 'group': ['hitting']}
        al_stats = self.mlb.get_team_stats(self.al_team, self.params)
        nl_stats = self.mlb.get_team_stats(self.nl_team, self.params)

        self.assertTrue(al_stats['hitting']['season'])
        self.assertTrue(al_stats['hitting']['seasonadvanced'])

        self.assertTrue(nl_stats['hitting']['season'])
        self.assertTrue(nl_stats['hitting']['seasonadvanced'])

    def test_get_multiple_stats_for_teams(self):
        """mlb get stats should return two hitting stats"""
        self.params = {'stats': ['seasonAdvanced', 'season', 'careerAdvanced', 'yearByYear'], 'group': ['hitting']}
        al_stats = self.mlb.get_team_stats(self.al_team, self.params)
        nl_stats = self.mlb.get_team_stats(self.nl_team, self.params)

        self.assertTrue(al_stats['hitting']['season'])
        self.assertTrue(al_stats['hitting']['seasonadvanced'])
        self.assertTrue(al_stats['hitting']['careeradvanced'])
        self.assertTrue(al_stats['hitting']['yearbyyear'])

        self.assertTrue(nl_stats['hitting']['season'])
        self.assertTrue(nl_stats['hitting']['seasonadvanced'])
        self.assertTrue(nl_stats['hitting']['careeradvanced'])
        self.assertTrue(nl_stats['hitting']['yearbyyear'])

    def test_hitting_pitch_arsenal_stat_on_teams(self):
        """mlb get stats should return PitchArsenal object"""
        self.params = {'stats': ['expectedStatistics'], 'group': ['hitting']}
        al_stats = self.mlb.get_team_stats(self.al_team, self.params)
        nl_stats = self.mlb.get_team_stats(self.nl_team, self.params)

        self.assertTrue(al_stats['hitting']['expectedstatistics'])
        self.assertTrue(nl_stats['hitting']['expectedstatistics'])

    def test_building_playlog_500(self):
        """playlog should return 500 error"""
        self.params = {'stats': ['playLog'], 'group': ['hitting']}

        with self.assertRaises(TheMlbStatsApiException):
            stats = self.mlb.get_team_stats(self.al_team, self.params)
    
    def test_hitting_vs_team_stats_on_team(self):
        self.params = {'stats': ['vsTeam'], 'group': ['hitting'], 'opposingTeamId': '158'}
        vsteam_stats = self.mlb.get_team_stats(self.nl_team, self.params)

        self.assertTrue(vsteam_stats['hitting']['vsteam'])

    def test_hitting_vs_team5y_stats_on_teams(self):
        self.params = {'stats': ['vsTeam5Y', 'vsTeamTotal'], 'group': ['hitting'], 'opposingTeamId': '158'}
        vsteam_stats = self.mlb.get_team_stats(self.nl_team, self.params)

        self.assertTrue(vsteam_stats['hitting']['vsteam5y'])
        self.assertTrue(vsteam_stats['hitting']['vsteamtotal'])
