from dataclasses import field
import unittest

from mlbstatsapi.mlb_api import Mlb


class TestPlayerHittingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        # Juan Soto
        cls.position_player = 665742
        # Robbie Ray
        cls.pitching_player = 592662
        # Cal Raleigh
        cls.catching_player = 663728

        cls.utility_player = 647351

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_hitting_opponents_faced_position(self):
        """mlb get stats should return hitting stats"""
        self.params = {'stats': ['opponentsFaced'], 'group': ['hitting']}
        opponents_faced = self.mlb.get_player_stats(self.position_player, self.params)
        print(opponents_faced)
        self.assertTrue(opponents_faced['hitting']['opponentsfaced'])

    def test_get_one_hitting_stats_for_player(self):
        """mlb get stats should return hitting stats"""
        self.params = {'stats': ['season'], 'group': ['hitting']}
        hitting_stats = self.mlb.get_player_stats(self.position_player, self.params)

        self.assertTrue(hitting_stats['hitting']['season'])

        self.params = {'stats': ['seasonAdvanced'], 'group': ['hitting']}
        advanced_hitting = self.mlb.get_player_stats(self.position_player, self.params)
        self.assertTrue(advanced_hitting['hitting']['seasonadvanced'])

    def test_get_multiple_stats_for_player(self):
        """mlb get stats should return two hitting stats"""
        self.params = {'stats': ['seasonAdvanced', 'season', 'careerAdvanced', 'yearByYear'], 'group': ['hitting']}
        stats = self.mlb.get_player_stats(self.position_player, self.params)

        self.assertTrue(stats['hitting']['season'])
        self.assertTrue(stats['hitting']['seasonadvanced'])
        self.assertTrue(stats['hitting']['careeradvanced'])
        self.assertTrue(stats['hitting']['yearbyyear'])

    def test_hitting_pitch_arsenal_stat_on_position_player(self):
        """mlb get stats should return PitchArsenal object"""
        self.params = {'stats': ['expectedStatistics', 'sprayChart'], 'group': ['hitting']}
        stats = self.mlb.get_player_stats(self.position_player, self.params)

        self.assertTrue(stats['hitting']['expectedstatistics'])
        self.assertTrue(stats['stats']['spraychart'])


    def test_building_all_hitting_objects(self):
        """this test will build all what should be working stat objects"""
        self.params_one = {'stats': ['homeAndAway', 'winLoss', 'yearByYear', 'byDayOfWeek',
        'byDateRange', 'byDateRangeAdvanced', 'byDayOfWeek', 'byMonth'], 'group': ['hitting']}
        stat_group_one = self.mlb.get_player_stats(self.position_player, self.params_one)

        self.assertTrue(stat_group_one['hitting']['homeandaway'])
        self.assertTrue(stat_group_one['hitting']['winloss'])
        self.assertTrue(stat_group_one['hitting']['yearbyyear'])
        self.assertTrue(stat_group_one['hitting']['bydayofweek'])
        self.assertTrue(stat_group_one['hitting']['bydaterange'])
        self.assertTrue(stat_group_one['hitting']['bydaterangeadvanced'])
        self.assertTrue(stat_group_one['hitting']['bydayofweek'])
        self.assertTrue(stat_group_one['hitting']['bymonth'])

    def test_pitch_arsenal_stat_on_position_player(self):
        """mlb get stats should return PitchArsenal object"""
        self.params = {'stats': ['pitchArsenal', 'hotColdZones'], 'group': ['hitting']}
        stats = self.mlb.get_player_stats(self.position_player, self.params)

        self.assertTrue(stats['stats']['pitcharsenal'])
        self.assertTrue(stats['stats']['hotcoldzones'])

    def test_playlog_stat_on_position_player(self):
        """mlb get stats should return two hittinglog objects object"""
        self.params = {'stats': ['playLog'], 'group': ['hitting']}    
        log_stats = self.mlb.get_player_stats(self.position_player, self.params)

        self.assertTrue(log_stats['hitting']['playlog'])
    
    def test_pitchlog_stat_on_position_player(self):
        """mlb get stats should return two hittinglog objects object"""
        self.params = {'stats': ['pitchLog'], 'group': ['hitting']}
        log_stats = self.mlb.get_player_stats(self.position_player, self.params)

        self.assertTrue(log_stats['hitting']['pitchlog'])

    def test_hitting_vs_team_stats_on_players(self):
        self.params = {'stats': ['vsTeam'], 'group': ['hitting'], 'opposingTeamId': '158'}
        vsteam_stats = self.mlb.get_player_stats(self.position_player, self.params)

        self.assertTrue(vsteam_stats['hitting']['vsteam'])

    def test_hitting_vs_team5y_stats_on_players(self):
        self.params = {'stats': ['vsTeam5Y', 'vsTeamTotal'], 'group': ['hitting'], 'opposingTeamId': '158'}
        vsteam_stats = self.mlb.get_player_stats(self.position_player, self.params)

        self.assertTrue(vsteam_stats['hitting']['vsteam5y'])
        self.assertTrue(vsteam_stats['hitting']['vsteamtotal'])

    def test_hitting_vs_player_stats_on_players(self):
        self.params = {'stats': ['vsPlayer'], 'group': ['hitting'], 'opposingPlayerId': '660271'}
        vsteam_stats = self.mlb.get_player_stats(self.catching_player, self.params)

        self.assertTrue(vsteam_stats['hitting']['vsplayer'])

        

