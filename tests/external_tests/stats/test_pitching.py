import unittest
import time

from mlbstatsapi.mlb_api import Mlb


class TestPitchingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.al_team = 133
        cls.shohei_ohtani = 660271
        cls.utility_player = 647351
        cls.ty_france = 664034
                    
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_pitching_stat_attributes_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['season', 'career', 'seasonAdvanced', 'careerAdvanced']
        self.group = ['pitching']
        self.params = {'season': 2022}

        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)
        self.assertFalse('hitting' in stats)
        self.assertEqual(len(stats['pitching']), 4)

        # check for split objects
        self.assertTrue(stats['pitching']['season'])
        self.assertTrue(stats['pitching']['career'])
        self.assertTrue(stats['pitching']['seasonAdvanced'])
        self.assertTrue(stats['pitching']['careerAdvanced'])

        season = stats['pitching']['season']
        career = stats['pitching']['career']
        season_advanced = stats['pitching']['seasonAdvanced']
        career_advanced = stats['pitching']['careerAdvanced']

        self.assertEqual(season.total_splits, len(season.splits))
        self.assertEqual(season.group, 'pitching')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.total_splits, len(career.splits))
        self.assertEqual(career.group, 'pitching')
        self.assertEqual(career.type, 'career')

        self.assertEqual(season_advanced.total_splits, len(season_advanced.splits))
        self.assertEqual(season_advanced.group, 'pitching')
        self.assertEqual(season_advanced.type, 'seasonAdvanced')

        self.assertEqual(career_advanced.total_splits, len(career_advanced.splits))
        self.assertEqual(career_advanced.group, 'pitching')
        self.assertEqual(career_advanced.type, 'careerAdvanced')

    def test_pitching_stat_attributes_team(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['season', 'career','seasonAdvanced', 'careerAdvanced']
        self.group = ['pitching']
        self.params = {'season': 2022}

        # let's get some stats
        stats = self.mlb.get_team_stats(self.al_team, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)
        self.assertFalse('hitting' in stats)
        self.assertEqual(len(stats['pitching']), 4)

        # check for split objects
        self.assertTrue(stats['pitching']['season'])
        self.assertTrue(stats['pitching']['career'])
        self.assertTrue(stats['pitching']['seasonAdvanced'])
        self.assertTrue(stats['pitching']['careerAdvanced'])

        season = stats['pitching']['season']
        career = stats['pitching']['career']
        season_advanced = stats['pitching']['seasonAdvanced']
        career_advanced = stats['pitching']['careerAdvanced']

        self.assertEqual(season.total_splits, len(season.splits))
        self.assertEqual(season.group, 'pitching')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.total_splits, len(career.splits))
        self.assertEqual(career.group, 'pitching')
        self.assertEqual(career.type, 'career')

        self.assertEqual(season_advanced.total_splits, len(season_advanced.splits))
        self.assertEqual(season_advanced.group, 'pitching')
        self.assertEqual(season_advanced.type, 'seasonAdvanced')

        self.assertEqual(career_advanced.total_splits, len(career_advanced.splits))
        self.assertEqual(career_advanced.group, 'pitching')
        self.assertEqual(career_advanced.type, 'careerAdvanced')

    def test_pitching_excepected_stats_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['expectedStatistics']
        self.group = ['pitching']
        self.params = {'season': 2022}

        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)

        # check for split objects
        self.assertTrue(stats['pitching']['expectedStatistics'])


    def test_pitching_bydate_stats_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['byDateRange', 'byDateRangeAdvanced']
        self.group = ['pitching']
        self.params = {'season': 2022, 'startDate': '2022-05-07'}

        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)

        # check for split objects
        self.assertTrue(stats['pitching']['byDateRange'])
        self.assertTrue(stats['pitching']['byDateRangeAdvanced'])

    def test_pitching_byMonth_stats_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['byMonth']
        self.group = ['pitching']
        self.params = {'season': 2022}
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)

        # check for split objects
        self.assertTrue(stats['pitching']['byMonth'])

    def test_pitching_byDayOfWeek_stats_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['byDayOfWeek']
        self.group = ['pitching']
        self.params = {'season': 2022}
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)

        # check for split objects
        self.assertTrue(stats['pitching']['byDayOfWeek'])

    def test_pitching_vsPlayer_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['vsPlayer']
        self.group = ['pitching']
        self.params = {'opposingPlayerId': 664034}
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)

        # check for split objects
        self.assertTrue(stats['pitching']['vsPlayer'])

    def test_pitching_pitchLog_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['pitchLog']
        self.group = ['pitching']
        self.params = {'season': 2022}
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)

        # check for split objects
        self.assertTrue(stats['pitching']['pitchLog'])

    def test_pitching_playLog_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['playLog']
        self.group = ['pitching']
        self.params = {'season': 2022}
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)

        # check for split objects
        self.assertTrue(stats['pitching']['playLog'])

    def test_pitching_pitchArsenal_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['pitchArsenal']
        self.group = ['pitching']
        self.params = {'season': 2022}
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('stats' in stats)

        # check for split objects
        self.assertTrue(stats['stats']['pitchArsenal'])

    def test_pitching_hotColdZones_stats_player(self):
        """mlb get stats should return hitting stats"""
        self.stats = ['hotColdZones']
        self.group = ['pitching']
        self.params = {'season': 2022}
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shohei_ohtani, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('stats' in stats)

        # check for split objects
        self.assertTrue(stats['stats']['hotColdZones'])