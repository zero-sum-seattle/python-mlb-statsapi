import unittest
import time

from mlbstatsapi.mlb_api import Mlb


class TestHittingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.al_team = 133
        cls.shohei_ohtani = 660271
        cls.catching_player = 663728
        cls.ty_france = 664034
        cls.utility_player = 647351
        cls.soto = 665742

                    
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_hitting_stat_attributes_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['season', 'career','seasonAdvanced', 'careerAdvanced']
        self.group = ['hitting']
        self.params = {'season': 2022}
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)
        self.assertFalse('pitching' in stats)
        self.assertEqual(len(stats['hitting']), 4)

        # check for split objects
        self.assertTrue(stats['hitting']['season'])
        self.assertTrue(stats['hitting']['career'])
        self.assertTrue(stats['hitting']['seasonAdvanced'])
        self.assertTrue(stats['hitting']['careerAdvanced'])

        # let's pull out a object and test it
        season = stats['hitting']['season']
        career = stats['hitting']['career']
        season_advanced = stats['hitting']['seasonAdvanced']
        career_advanced = stats['hitting']['careerAdvanced']
        # check that attrs exist and contain data

        self.assertEqual(season.total_splits, len(season.splits))
        self.assertEqual(season.group, 'hitting')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.total_splits, len(career.splits))
        self.assertEqual(career.group, 'hitting')
        self.assertEqual(career.type, 'career')

        self.assertEqual(season_advanced.total_splits, len(season_advanced.splits))
        self.assertEqual(season_advanced.group, 'hitting')
        self.assertEqual(season_advanced.type, 'seasonAdvanced')

        self.assertEqual(career_advanced.total_splits, len(career_advanced.splits))
        self.assertEqual(career_advanced.group, 'hitting')
        self.assertEqual(career_advanced.type, 'careerAdvanced')

    def test_hitting_stat_attributes_team(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['season', 'career', 'seasonAdvanced', 'careerAdvanced']
        self.group = ['hitting']
        self.params = {'season': 2022}
        # let's get some stats
        # let's get some stats
        stats = self.mlb.get_team_stats(self.al_team, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)
        self.assertFalse('pitching' in stats)
        self.assertEqual(len(stats['hitting']), 4)

        # check for split objects
        self.assertTrue(stats['hitting']['season'])
        self.assertTrue(stats['hitting']['career'])
        self.assertTrue(stats['hitting']['seasonAdvanced'])
        self.assertTrue(stats['hitting']['careerAdvanced'])

        # let's pull out a object and test it
        season = stats['hitting']['season']
        career = stats['hitting']['career']
        season_advanced = stats['hitting']['seasonAdvanced']
        career_advanced = stats['hitting']['careerAdvanced']

        self.assertEqual(season.total_splits, len(season.splits))
        self.assertEqual(season.group, 'hitting')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.total_splits, len(career.splits))
        self.assertEqual(career.group, 'hitting')
        self.assertEqual(career.type, 'career')

        self.assertEqual(season_advanced.total_splits, len(season_advanced.splits))
        self.assertEqual(season_advanced.group, 'hitting')
        self.assertEqual(season_advanced.type, 'seasonAdvanced')

        self.assertEqual(career_advanced.total_splits, len(career_advanced.splits))
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
        self.params = {'season': 2022}
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['expectedStatistics'])

    def test_hitting_bydate_stats_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['byDateRange', 'byDateRangeAdvanced']
        self.group = ['hitting']
        self.params = {'season': 2022, 'startDate': '2022-05-07'}
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['byDateRange'])
        self.assertTrue(stats['hitting']['byDateRangeAdvanced'])

    def test_hitting_byMonth_stats_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['byMonth']
        self.group = ['hitting']
        self.params = {'season': 2022}

        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['byMonth'])

    def test_hitting_byDayOfWeek_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['byDayOfWeek']
        self.group = ['hitting']
        self.params = {'season': 2022}
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['byDayOfWeek'])

    def test_hitting_vsPlayer_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['vsPlayer']
        self.group = ['hitting']
        self.params = {'opposingPlayerId': 660271, 'season': 2022}
        # let's get some stats
        stats = self.mlb.get_player_stats(self.ty_france, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['vsPlayer'])

    def test_hitting_vsteam_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['vsTeam']
        self.group = ['hitting']
        self.params = {'opposingTeamId': 133, 'season': 2022}

        # let's get some stats
        stats = self.mlb.get_player_stats(self.ty_france, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['vsTeam'])

    def test_hitting_vsteam_stats_team(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['vsTeam']
        self.group = ['hitting']
        self.params = {'opposingTeamId': 136, 'season': 2022}

        # let's get some stats
        stats = self.mlb.get_team_stats(self.al_team, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['vsTeam'])

    def test_hitting_pitchLog_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['pitchLog']
        self.group = ['hitting']
        self.params = {'season': 2022}

        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['pitchLog'])

        pitchLog = stats['hitting']['pitchLog']
        self.assertTrue(len(pitchLog.splits) > 1)
        self.assertEqual(pitchLog.total_splits, len(pitchLog.splits))


    def test_hitting_pitchLog_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['playLog']
        self.group = ['hitting']
        self.params = {'season': 2022}

        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)

        # check for split objects
        self.assertTrue(stats['hitting']['playLog'])

        # playLogs should return multiple splits
        playLogs = stats['hitting']['playLog']
        self.assertTrue(len(playLogs.splits) > 1)
        self.assertEqual(playLogs.total_splits, len(playLogs.splits))


    def test_hitting_pitchArsenal_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['pitchArsenal']
        self.group = ['hitting']
        self.params = {'season': 2022}

        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('stats' in stats)

        # check for split objects
        self.assertTrue(stats['stats']['pitchArsenal'])

        pitcharsenal = stats['stats']['pitchArsenal']
        self.assertTrue(len(pitcharsenal.splits) > 1)
        self.assertEqual(pitcharsenal.total_splits, len(pitcharsenal.splits))

    def test_hitting_hotColdZones_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['hotColdZones']
        self.group = ['hitting']
        self.params = {'season': 2022}

        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('stats' in stats)

        # check for split objects
        self.assertTrue(stats['stats']['hotColdZones'])

        # hotcoldzone should return 5 splits
        hotcoldzone = stats['stats']['hotColdZones']
        self.assertEqual(len(hotcoldzone.splits), 5)
        self.assertEqual(hotcoldzone.total_splits, len(hotcoldzone.splits))
