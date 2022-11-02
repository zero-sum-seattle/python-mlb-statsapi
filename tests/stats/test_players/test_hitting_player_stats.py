from dataclasses import field
import unittest

from mlbstatsapi.mlbapi import Mlb


class TestPlayerHittingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.position_player = cls.mlb.get_person(665742) # Juan Soto

        cls.pitching_player = cls.mlb.get_person(592662) # Robbie Ray

        cls.catching_player = cls.mlb.get_person(663728) # Cal Raleigh

        cls.utility_player = cls.mlb.get_person(647351) # Abraham Toro

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_hitting_opponents_faced_position(self):
        """mlb get stats should return hitting stats"""
        self.params = { 'stats': [ 'opponentsFaced' ], 'group': [ 'hitting' ]}
        opponents_faced = self.mlb.get_stats(self.params, self.position_player)
        
        self.assertTrue(opponents_faced['hitting']['opponentsfaced'])

    def test_get_one_hitting_stats_for_player(self):
        """mlb get stats should return hitting stats"""
        self.params = { 'stats': [ 'season' ], 'group': ['hitting']}
        hitting_stats = self.mlb.get_stats(self.params, self.position_player)

        self.assertTrue(hitting_stats['hitting']['season'])

        self.params = { 'stats': [ 'seasonAdvanced' ], 'group': ['hitting'] }
        advanced_hitting = self.mlb.get_stats(self.params, self.position_player)
        self.assertTrue(advanced_hitting['hitting']['seasonadvanced'])

    def test_get_multiple_stats_for_player(self):
        """mlb get stats should return two hitting stats"""
        self.params = { 'stats': [ 'seasonAdvanced', 'season', 'careerAdvanced', 'yearByYear' ], 'group': ['hitting']}
        stats = self.mlb.get_stats(self.params, self.position_player)

        self.assertTrue(stats['hitting']['season'])
        self.assertTrue(stats['hitting']['seasonadvanced'])
        self.assertTrue(stats['hitting']['careeradvanced'])
        self.assertTrue(stats['hitting']['yearbyyear'])

    def test_hitting_pitch_arsenal_stat_on_position_player(self):
        """mlb get stats should return PitchArsenal object"""
        self.params = { 'stats': [ 'expectedStatistics', 'sprayChart' ], 'group': ['hitting'] }
        stats = self.mlb.get_stats(self.params, self.position_player)

        self.assertTrue(stats['hitting']['expectedstatistics'])
        self.assertTrue(stats['stats']['spraychart'])


    def test_building_all_hitting_objects(self):
        """this test will build all what should be working stat objects"""
        self.params_one = { 'stats': [ 'homeAndAway', 'winLoss', 'yearByYear', 'byDayOfWeek',
        'byDateRange', 'byDateRangeAdvanced', 'byDayOfWeek', 'byMonth' ], 'group': ['hitting'] }
        stat_group_one = self.mlb.get_stats(self.params_one, self.position_player)

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
        self.params = { 'stats': [ 'pitchArsenal', 'hotColdZones' ], 'group': ['hitting'] }
        stats = self.mlb.get_stats(self.params, self.position_player)

        self.assertTrue(stats['stats']['pitcharsenal'])
        self.assertTrue(stats['stats']['hotcoldzones'])

    def test_playlog_stat_on_position_player(self):
        """mlb get stats should return two hittinglog objects object"""
        self.params = { 'stats': [ 'playLog' ], 'group': ['hitting'] }    
        log_stats = self.mlb.get_stats(self.params, self.position_player)

        self.assertTrue(log_stats['hitting']['playlog'])
    
    def test_pitchlog_stat_on_position_player(self):
        """mlb get stats should return two hittinglog objects object"""
        self.params = { 'stats': [ 'pitchLog' ], 'group': ['hitting'] }    
        log_stats = self.mlb.get_stats(self.params, self.position_player)

        self.assertTrue(log_stats['hitting']['pitchlog'])

    def test_hitting_vs_team_stats_on_players(self):
        self.params = { 'stats': [ 'vsTeam' ], 'group': ['hitting'], 'opposingTeamId': '158' }
        vsteam_stats = self.mlb.get_stats(self.params, self.position_player)

        self.assertTrue(vsteam_stats['hitting']['vsteam'])

    # def test_hitting_log_stats_stat_on_position_player(self):
    #     """mlb get stats should return two hittinglog objects object"""
    #     self.params = { 'stats': [ 'byDateRange', 'byDateRangeAdvanced', 'byMonthPlayoffs', 
    #     'byMonth', 'byDayOfWeek', 'byDayOfWeekPlayoffs' ], 'group': ['hitting'] }    
    #     hitting_dates = self.mlb.get_stats(self.params, self.position_player)

    #     self.assertTrue(hitting_dates['hitting']['bydaterange'])
    #     self.assertTrue(hitting_dates['hitting']['bydaterangeadvanced'])
    #     self.assertTrue(hitting_dates['hitting']['bymonthplayoffs'])
    #     self.assertTrue(hitting_dates['hitting']['bymonth'])
    #     self.assertTrue(hitting_dates['hitting']['bydayofweek'])
    #     self.assertTrue(hitting_dates['hitting']['bydayofweekplayoffs'])

    # def test_hitting_winloss_on_position_player(self):
    #     """mlb get stats should return two hittinglog objects object"""
    #     self.params = { 'stats': [ 'winLoss', 'winLossPlayoffs' ], 'group': ['hitting'] }
    #     hitting_wl = self.mlb.get_stats(self.params, self.position_player)

    #     self.assertTrue(hitting_wl['hitting']['winloss'])
    #     self.assertTrue(hitting_wl['hitting']['winlossplayoffs'])

    # def test_hitting_log_stats_stat_on_position_player(self):
    #     """mlb get stats should return two hittinglog objects object"""
    #     self.params = { 'stats': [ 'homeAndAway', 'homeAndAwayPlayoffs' ], 'group': ['hitting'] }
    #     hitting_wl = self.mlb.get_stats(self.params, self.position_player)

    #     self.assertTrue(hitting_wl['hitting']['homeandaway'])
    #     self.assertTrue(hitting_wl['hitting']['homeandawayplayoffs'])

    # def test_building_all_hitting_objects(self):
    #     """this test will build all what should be working stat objects"""
    #     self.params_one = { 'stats': [ 'homeAndAway', 'winLoss', 'yearByYear', 'byDayOfWeek',
    #     'byDateRange', 'byDateRangeAdvanced', 'byDayOfWeek', 'byMonth' ], 'group': ['hitting'] }
    #     stat_group_one = self.mlb.get_stats(self.params_one, self.position_player)

    #     self.assertTrue(stat_group_one['hitting']['homeandaway'])
    #     self.assertTrue(stat_group_one['hitting']['winloss'])
    #     self.assertTrue(stat_group_one['hitting']['yearbyyear'])
    #     self.assertTrue(stat_group_one['hitting']['bydayofweek'])
    #     self.assertTrue(stat_group_one['hitting']['bydaterange'])
    #     self.assertTrue(stat_group_one['hitting']['bydaterangeadvanced'])
    #     self.assertTrue(stat_group_one['hitting']['bydayofweek'])
    #     self.assertTrue(stat_group_one['hitting']['bymonth'])


      

        

