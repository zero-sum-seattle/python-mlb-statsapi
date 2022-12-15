import unittest
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
        cls.soto = 665742
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
        season = stats['hitting']['season']
        career = stats['hitting']['career']
        season_advanced = stats['hitting']['seasonadvanced']
        career_advanced = stats['hitting']['careeradvanced']
        # check that attrs exist and contain data

        self.assertEqual(season.totalsplits, len(season.splits))
        self.assertEqual(season.group, 'hitting')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.totalsplits, len(career.splits))
        self.assertEqual(career.group, 'hitting')
        self.assertEqual(career.type, 'career')

        self.assertEqual(season_advanced.totalsplits, len(season_advanced.splits))
        self.assertEqual(season_advanced.group, 'hitting')
        self.assertEqual(season_advanced.type, 'seasonAdvanced')

        self.assertEqual(career_advanced.totalsplits, len(career_advanced.splits))
        self.assertEqual(career_advanced.group, 'hitting')
        self.assertEqual(career_advanced.type, 'careerAdvanced')

    def test_hitting_stat_attributes_team(self):
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
        season = stats['hitting']['season']
        career = stats['hitting']['career']
        season_advanced = stats['hitting']['seasonadvanced']
        career_advanced = stats['hitting']['careeradvanced']

        self.assertEqual(season.totalsplits, len(season.splits))
        self.assertEqual(season.group, 'hitting')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.totalsplits, len(career.splits))
        self.assertEqual(career.group, 'hitting')
        self.assertEqual(career.type, 'career')

        self.assertEqual(season_advanced.totalsplits, len(season_advanced.splits))
        self.assertEqual(season_advanced.group, 'hitting')
        self.assertEqual(season_advanced.type, 'seasonAdvanced')

        self.assertEqual(career_advanced.totalsplits, len(career_advanced.splits))
        self.assertEqual(career_advanced.group, 'hitting')
        self.assertEqual(career_advanced.type, 'careerAdvanced')



    def test_hitting_traded_stats_player(self):
        """mlb get stats should return multiple splits for being a traded player"""
        self.stats = ['season']
        self.group = ['hitting']
        self.params = {'season': 2022}
        # let's get some stats
        stats = self.mlb.get_player_stats(self.soto, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['season'])

        season = stats['hitting']['season']

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

    def test_hitting_vsteam_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['vsTeam']
        self.group = ['hitting']
        self.params = {'opposingTeamId': 133}

        # let's get some stats
        stats = self.mlb.get_player_stats(self.ty_france, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['vsteam'])

    def test_hitting_vsteam_stats_team(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['vsTeam']
        self.group = ['hitting']
        self.params = {'opposingTeamId': 136}

        # let's get some stats
        stats = self.mlb.get_team_stats(self.al_team, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['vsteam'])

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

        pitchlog = stats['hitting']['pitchlog']
        self.assertTrue(len(pitchlog.splits) > 1)
        self.assertEqual(pitchlog.totalsplits, len(pitchlog.splits))


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

        # playlogs should return multiple splits
        playlogs = stats['hitting']['playlog']
        self.assertTrue(len(playlogs.splits) > 1)
        self.assertEqual(playlogs.totalsplits, len(playlogs.splits))


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

        pitcharsenal = stats['stats']['pitcharsenal']
        self.assertTrue(len(pitcharsenal.splits) > 1)
        self.assertEqual(pitcharsenal.totalsplits, len(pitcharsenal.splits))

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

        # hotcoldzone should return 5 splits
        hotcoldzone = stats['stats']['hotcoldzones']
        self.assertEqual(len(hotcoldzone.splits), 5)
        self.assertEqual(hotcoldzone.totalsplits, len(hotcoldzone.splits))
