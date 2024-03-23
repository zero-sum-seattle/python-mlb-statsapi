import unittest
from mlbstatsapi.models.standings import Standings
from mlbstatsapi import Mlb


class TestStandings(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
    
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_standings(self):
        """This test should return a 200 and Round"""
        # set league id
        league_id = 103
        # set season
        season = 2018

        # call get_standings return list of standings
        standings = self.mlb.get_standings(league_id, season)

        # Gamepace should not be None
        self.assertIsNotNone(standings)        

        # list should not be empty
        self.assertNotEqual(standings, ["test"])

        # items in list should be standings
        self.assertIsInstance(standings[0], Standings)

        standing = standings[0]

        # sportgamepace should not be none
        self.assertIsNotNone(standing)


    def test_get_standings_404(self):
        """This test should return a 200 and """

        # set league id to invalid id
        league_id = 1032
        # set season to invlaid season
        season = 400

        # call get_standings return list of standings
        standings = self.mlb.get_standings(league_id, season)

        # standings should not be None
        self.assertIsNotNone(standings)

        # list should be empty
        self.assertEqual(standings, [])

    def test_get_standings_with_params(self):
        """this test should return results for standings"""

        # set league id
        league_id = 103
        # set season
        season = 2018
        standingsTypes='wildCard,regularSeason'

        # call get_standings return list of standings
        standings = self.mlb.get_standings(league_id, season, standingsTypes=standingsTypes)
        # standings should not be None
        self.assertIsNotNone(standings)
        # list should not be empty
        self.assertNotEqual(standings, [])
        
