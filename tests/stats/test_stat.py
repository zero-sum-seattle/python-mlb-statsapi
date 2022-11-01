from dataclasses import field
import unittest

from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team
from mlbstatsapi.mlbapi import Mlb



class TestCatchingPlayerStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.shoei_ohtani = cls.mlb.get_person(660271) # Cal Raleigh

    @classmethod
    def tearDownClass(cls) -> None:
        pass


    def test_multiple_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'season', 'career', 'seasonAdvanced', 'careerAdvanced' ], 'group': [ 'pitching', 'hitting' ] }

        # let's get some stats
        hitting_pitching_stats = self.mlb.get_stats(self.shoei_ohtani, self.params)

        # check for empty list
        self.assertNotEqual(hitting_pitching_stats, [])

        # the end point should give us 2 hitting and pitching stat objects back
        self.assertEqual(len(hitting_pitching_stats), 2)
        self.assertTrue('hitting' in hitting_pitching_stats)
        self.assertTrue('pitching' in hitting_pitching_stats)

        # let's check to make sure the two objects have four stat type classes and are populated lists
        for stat in hitting_pitching_stats:

            # check for split objects
            self.assertTrue(stat['seasons'])
            self.assertTrue(stat['careers'])
            self.assertTrue(stat['seasonsadvanced'])
            self.assertTrue(stat['careersadvanced'])

            # let's make sure they aren't empty
            self.assertNotEqual(stat['seasons'], [])
            self.assertNotEqual(stat['careers'], [])
            self.assertNotEqual(stat['seasonsadvanced'], [])
            self.assertNotEqual(stat['careersadvanced'], [])

            # let's pull out a object and test it
            season = stat['seasons'][0]
            career = stat['careers'][0]
            season_advanced = stat['seasonsadvanced'][0]
            career_advanced = stat['careersadvanced'][0]

            # check that attrs exist and contain data
            self.assertTrue(season.season)
            self.assertTrue(career.player)
            self.assertTrue(season_advanced.season)
            self.assertTrue(career_advanced.player)


