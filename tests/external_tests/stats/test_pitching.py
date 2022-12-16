import unittest
import time

from mlbstatsapi.mlb_api import Mlb


class TestPitchingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.al_team = 133
        cls.shoei_ohtani = 660271
        cls.utility_player = 647351
        cls.ty_france = 664034
        cls.stats_200_blank = ('projected', 'projectedRos', 'standard', 'advanced', 'firstYearStats', 'lastYearStats',
        'vsOpponents', 'outsAboveAverage', 'tracking', 'availableStats', 'gameTypeStats', 'vsOpponents')
        cls.pitching = 'pitching'
        cls.stats_500 = ('careerStatSplits', 'metricLog', 'metricAverages', 'statSplits', 'statSplitsAdvanced')
        # these stat groups require a team with recent playoff appearences 
        cls.stats_playoffs = ('byMonthPlayoffs', 'bydayofweekPlayoffs', 'homeAndAwayPlayoffs', 'winLossPlayoffs')
        # These stat groups require addition params passed like playerid or teamid
        cls.stats_require_params = ('vsTeam', 'vsTeam5Y', 'vsTeamTotal', 'vsPlayer', 'vsPlayerTotal', 'vsPlayer5Y')
        # These stat types should all return a stat split object for hitting and pitching stat groups
        cls.pitching = (
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

    def test_pitching_stat_attributes_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['season', 'career', 'seasonAdvanced', 'careerAdvanced']
        self.group = ['pitching']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)
        self.assertFalse('hitting' in stats)
        self.assertEqual(len(stats['pitching']), 4)

        # check for split objects
        self.assertTrue(stats['pitching']['season'])
        self.assertTrue(stats['pitching']['career'])
        self.assertTrue(stats['pitching']['seasonadvanced'])
        self.assertTrue(stats['pitching']['careeradvanced'])

        season = stats['pitching']['season']
        career = stats['pitching']['career']
        season_advanced = stats['pitching']['seasonadvanced']
        career_advanced = stats['pitching']['careeradvanced']

        self.assertEqual(season.totalsplits, len(season.splits))
        self.assertEqual(season.group, 'pitching')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.totalsplits, len(career.splits))
        self.assertEqual(career.group, 'pitching')
        self.assertEqual(career.type, 'career')

        self.assertEqual(season_advanced.totalsplits, len(season_advanced.splits))
        self.assertEqual(season_advanced.group, 'pitching')
        self.assertEqual(season_advanced.type, 'seasonAdvanced')

        self.assertEqual(career_advanced.totalsplits, len(career_advanced.splits))
        self.assertEqual(career_advanced.group, 'pitching')
        self.assertEqual(career_advanced.type, 'careerAdvanced')

    def test_pitching_stat_attributes_team(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['season', 'career','seasonAdvanced', 'careerAdvanced']
        self.group = ['pitching']
        # let's get some stats
        stats = self.mlb.get_team_stats(self.al_team, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)
        self.assertFalse('hitting' in stats)
        self.assertEqual(len(stats['pitching']), 4)

        # check for split objects
        self.assertTrue(stats['pitching']['season'])
        self.assertTrue(stats['pitching']['career'])
        self.assertTrue(stats['pitching']['seasonadvanced'])
        self.assertTrue(stats['pitching']['careeradvanced'])

        season = stats['pitching']['season']
        career = stats['pitching']['career']
        season_advanced = stats['pitching']['seasonadvanced']
        career_advanced = stats['pitching']['careeradvanced']

        self.assertEqual(season.totalsplits, len(season.splits))
        self.assertEqual(season.group, 'pitching')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.totalsplits, len(career.splits))
        self.assertEqual(career.group, 'pitching')
        self.assertEqual(career.type, 'career')

        self.assertEqual(season_advanced.totalsplits, len(season_advanced.splits))
        self.assertEqual(season_advanced.group, 'pitching')
        self.assertEqual(season_advanced.type, 'seasonAdvanced')

        self.assertEqual(career_advanced.totalsplits, len(career_advanced.splits))
        self.assertEqual(career_advanced.group, 'pitching')
        self.assertEqual(career_advanced.type, 'careerAdvanced')

    def test_pitching_excepected_stats_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['expectedStatistics']
        self.group = ['pitching']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)

        # check for split objects
        self.assertTrue(stats['pitching']['expectedstatistics'])


    def test_pitching_bydate_stats_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['byDateRange', 'byDateRangeAdvanced']
        self.group = ['pitching']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)

        # check for split objects
        self.assertTrue(stats['pitching']['bydaterange'])
        self.assertTrue(stats['pitching']['bydaterangeadvanced'])

    def test_pitching_bymonth_stats_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['byMonth']
        self.group = ['pitching']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)

        # check for split objects
        self.assertTrue(stats['pitching']['bymonth'])

    def test_pitching_bydayofweek_stats_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['byDayOfWeek']
        self.group = ['pitching']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)

        # check for split objects
        self.assertTrue(stats['pitching']['bydayofweek'])

    def test_pitching_vsplayer_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['vsPlayer']
        self.group = ['pitching']
        self.params = {'opposingPlayerId': 664034}
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)

        # check for split objects
        self.assertTrue(stats['pitching']['vsplayer'])

    def test_pitching_pitchlog_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['pitchLog']
        self.group = ['pitching']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)

        # check for split objects
        self.assertTrue(stats['pitching']['pitchlog'])

    def test_pitching_playlog_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['playLog']
        self.group = ['pitching']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)

        # check for split objects
        self.assertTrue(stats['pitching']['playlog'])

    def test_pitching_pitchArsenal_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['pitchArsenal']
        self.group = ['pitching']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('stats' in stats)

        # check for split objects
        self.assertTrue(stats['stats']['pitcharsenal'])

    def test_pitching_hotcoldzones_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['hotColdZones']
        self.group = ['pitching']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('stats' in stats)

        # check for split objects
        self.assertTrue(stats['stats']['hotcoldzones'])