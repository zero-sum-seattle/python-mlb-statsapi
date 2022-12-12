﻿import unittest
import time

from mlbstatsapi.mlb_api import Mlb


class TestHittingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.al_team = 133
        cls.shoei_ohtani = 660271
        cls.catching_player = 663728
        cls.ty_france = 664034
        cls.utility_player = 647351
        cls.stats_200_blank = ('projected', 'projectedRos', 'standard', 'advanced', 'firstYearStats', 'lastYearStats',
        'vsOpponents', 'outsAboveAverage', 'tracking', 'availableStats', 'gameTypeStats', 'vsOpponents')
        cls.hitting = 'hitting'
        cls.stats_500 = ('careerStatSplits', 'metricLog', 'metricAverages', 'statSplits', 'statSplitsAdvanced')
        # these stat groups require a team with recent playoff appearences 
        cls.stats_playoffs = ('byMonthPlayoffs', 'byDayOfWeekPlayoffs', 'homeAndAwayPlayoffs', 'winLossPlayoffs')
        # These stat groups require addition params passed like playerid or teamid
        cls.stats_require_params = ('vsTeam', 'vsTeam5Y', 'vsTeamTotal', 'vsPlayer', 'vsPlayerTotal', 'vsPlayer5Y')
        # These stat types should all return a stat split object for hitting and pitching stat groups
        cls.hitting = (
                    "yearByYear", "yearByYearAdvanced", "yearByYearPlayoffs", "season",
                    "career", "careerRegularSeason", "careerAdvanced", "seasonAdvanced", "careerPlayoffs",
                    "gameLog", "playLog", "pitchLog", "pitchArsenal", "expectedStatistics", "sabermetrics",
                    "sprayChart", "lastXGames", "byDateRange", "byDateRangeAdvanced", "byMonth", "byDayOfWeek",
                    "homeAndAway", "winLoss", "rankings", "rankingsByYear", "statsSingleSeason", "statsSingleSeasonAdvanced",
                    "hotColdZones", "opponentsFaced", "atGameStart"
                    )
                    
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_hitting_stat_attributes_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['season', 'career','seasonAdvanced', 'careerAdvanced']
        self.group = ['hitting']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)
        self.assertFalse('pitching' in stats)
        self.assertEqual(len(stats['hitting']), 4)

        # check for split objects
        self.assertTrue(stats['hitting']['season'])
        self.assertTrue(stats['hitting']['career'])
        self.assertTrue(stats['hitting']['seasonadvanced'])
        self.assertTrue(stats['hitting']['careeradvanced'])

        # let's pull out a object and test it
        season = stats['hitting']['season'][0]
        career = stats['hitting']['career'][0]
        season_advanced = stats['hitting']['seasonadvanced'][0]
        career_advanced = stats['hitting']['careeradvanced'][0]
        # check that attrs exist and contain data
        self.assertTrue(season.season)
        self.assertTrue(season.stat.avg)
        self.assertTrue(career.player)
        self.assertTrue(season_advanced.season)
        self.assertTrue(season_advanced.stat.plateappearances)
        self.assertTrue(career_advanced.player)

    def test_pitching_stat_attributes_team(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['season', 'career', 'seasonAdvanced', 'careerAdvanced']
        self.group = ['hitting']
        # let's get some stats
        # let's get some stats
        stats = self.mlb.get_team_stats(self.al_team, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)
        self.assertFalse('pitching' in stats)
        self.assertEqual(len(stats['hitting']), 4)

        # check for split objects
        self.assertTrue(stats['hitting']['season'])
        self.assertTrue(stats['hitting']['career'])
        self.assertTrue(stats['hitting']['seasonadvanced'])
        self.assertTrue(stats['hitting']['careeradvanced'])

        # let's pull out a object and test it
        season = stats['hitting']['season'][0]
        career = stats['hitting']['career'][0]
        season_advanced = stats['hitting']['seasonadvanced'][0]
        career_advanced = stats['hitting']['careeradvanced'][0]

        # check that attrs exist and contain data
        self.assertTrue(season.season)
        self.assertTrue(season.stat.avg)
        self.assertTrue(career.team)
        self.assertTrue(season_advanced.season)
        self.assertTrue(season_advanced.stat.plateappearances)
        self.assertTrue(career_advanced.team)

    def test_hitting_excepected_stats_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['expectedStatistics']
        self.group = ['hitting']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['expectedstatistics'])

    def test_hitting_bydate_stats_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['byDateRange', 'byDateRangeAdvanced']
        self.group = ['hitting']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['bydaterange'])
        self.assertTrue(stats['hitting']['bydaterangeadvanced'])

    def test_hitting_bymonth_stats_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['byMonth']
        self.group = ['hitting']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['bymonth'])

    def test_hitting_bydayofweek_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['byDayOfWeek']
        self.group = ['hitting']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['bydayofweek'])

    def test_hitting_vsplayer_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['vsPlayer']
        self.group = ['hitting']
        self.params = {'opposingPlayerId': 660271}
        # let's get some stats
        stats = self.mlb.get_player_stats(self.ty_france, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['vsplayer'])

    def test_hitting_pitchlog_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['pitchLog']
        self.group = ['hitting']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['pitchlog'])

    def test_hitting_pitchlog_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['playLog']
        self.group = ['hitting']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['playlog'])

    def test_hitting_pitchArsenal_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['pitchArsenal']
        self.group = ['hitting']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('stats' in stats)

        # check for split objects
        self.assertTrue(stats['stats']['pitcharsenal'])

    def test_hitting_hotcoldzones_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['hotColdZones']
        self.group = ['hitting']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('stats' in stats)

        # check for split objects
        self.assertTrue(stats['stats']['hotcoldzones'])