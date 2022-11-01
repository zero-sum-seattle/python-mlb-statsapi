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

        self.groups = self.params['group']

        # let's get some stats
        stats = self.mlb.get_stats(self.shoei_ohtani, self.params)

        # check for empty list
        self.assertNotEqual(stats, [])

        # the end point should give us 2 hitting and pitching stat objects back
        self.assertEqual(len(stats), 2)
        self.assertTrue('hitting' in stats)
        self.assertTrue('pitching' in stats)

        # let's check to make sure the two objects have four stat type classes and are populated lists
        for group in self.groups:

            # check for split objects
            self.assertTrue(stats[group]['season'])
            self.assertTrue(stats[group]['career'])
            self.assertTrue(stats[group]['seasonadvanced'])
            self.assertTrue(stats[group]['careeradvanced'])

            # let's make sure they aren't empty
            self.assertNotEqual(stats[group]['season'], [])
            self.assertNotEqual(stats[group]['career'], [])
            self.assertNotEqual(stats[group]['seasonadvanced'], [])
            self.assertNotEqual(stats[group]['careeradvanced'], [])

            # let's pull out a object and test it
            season = stats[group]['season'][0]
            career = stats[group]['career'][0]
            season_advanced = stats[group]['seasonadvanced'][0]
            career_advanced = stats[group]['careeradvanced'][0]

            # check that attrs exist and contain data
            self.assertTrue(season.season)
            self.assertTrue(career.player)
            self.assertTrue(season_advanced.season)
            self.assertTrue(career_advanced.player)



