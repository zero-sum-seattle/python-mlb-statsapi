from dataclasses import field
import unittest

from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team
from mlbstatsapi.mlbapi import Mlb



class TestCatchingPlayerStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.catching_player = cls.mlb.get_person(663728) # Cal Raleigh
        cls.utility_player = cls.mlb.get_person(647351) # Abraham Toro
        cls.al_team = cls.mlb.get_team(133) # Oakland
        cls.nl_team = cls.mlb.get_team(143) # Philadelphia Phillies

    @classmethod
    def tearDownClass(cls) -> None:
        pass


    def test_multiple_pitching_stats_for_player(self):
        """mlb get stats should return pitching stats"""
        self.params = { 'stats': [ 'season', 'career', 'seasonAdvanced', 'careerAdvanced' ], 'group': 'pitching' }

        # let's get some stats
        pitching_splits = self.mlb.get_stats(self.al_team, self.params)

        # check for empty list
        self.assertNotEqual(pitching_splits, [])

        # the end point should give us 4 objects back
        self.assertEqual(len(pitching_splits), 4)












