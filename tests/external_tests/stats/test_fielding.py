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
                    
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_fielding_stat_attributes_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['season', 'career']
        self.group = ['fielding']
        self.params = {'season': 2022}

        # let's get some stats
        stats = self.mlb.get_player_stats(self.utility_player, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('fielding' in stats)
        self.assertFalse('hitting' in stats)
        self.assertEqual(len(stats['fielding']), 2)

        # check for split objects
        self.assertTrue(stats['fielding']['season'])
        self.assertTrue(stats['fielding']['career'])

        # let's pull out a object and test it
        # check for split objects
        self.assertTrue(stats['fielding']['season'])
        self.assertTrue(stats['fielding']['career'])

        season = stats['fielding']['season']
        career = stats['fielding']['career']

        self.assertEqual(season.totalsplits, len(season.splits))
        self.assertEqual(season.group, 'fielding')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.totalsplits, len(career.splits))
        self.assertEqual(career.group, 'fielding')
        self.assertEqual(career.type, 'career')

    def test_fielding_stat_attributes_team(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['season', 'career', 'seasonAdvanced', 'careerAdvanced']
        self.group = ['fielding']
        self.params = {'season': 2022}
        # let's get some stats
        stats = self.mlb.get_team_stats(self.al_team, stats=self.stats, groups=self.group, **self.params)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('fielding' in stats)
        self.assertFalse('hitting' in stats)
        self.assertEqual(len(stats['fielding']), 4)
        # check for split objects
        self.assertTrue(stats['fielding']['season'])
        self.assertTrue(stats['fielding']['career'])
        self.assertTrue(stats['fielding']['seasonadvanced'])
        self.assertTrue(stats['fielding']['careeradvanced'])

        season = stats['fielding']['season']
        career = stats['fielding']['career']
        season_advanced = stats['fielding']['seasonadvanced']
        career_advanced = stats['fielding']['careeradvanced']

        self.assertEqual(season.totalsplits, len(season.splits))
        self.assertEqual(season.group, 'fielding')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.totalsplits, len(career.splits))
        self.assertEqual(career.group, 'fielding')
        self.assertEqual(career.type, 'career')

        self.assertEqual(season_advanced.totalsplits, len(season_advanced.splits))
        self.assertEqual(season_advanced.group, 'fielding')
        self.assertEqual(season_advanced.type, 'seasonAdvanced')

        self.assertEqual(career_advanced.totalsplits, len(career_advanced.splits))
        self.assertEqual(career_advanced.group, 'fielding')
        self.assertEqual(career_advanced.type, 'careerAdvanced')
