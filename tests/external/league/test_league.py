import unittest
from mlbstatsapi.models.leagues import League
from mlbstatsapi import Mlb


class TestLeague(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_league_instance_type_error(self):
        with self.assertRaises(TypeError):
            league = League()

    def test_league_instance_position_arguments(self):
        self.league = self.mlb.get_league(103)

        self.assertEqual(self.league.id, 103)
        self.assertEqual(self.league.link, "/api/v1/league/103")
        self.assertEqual(self.league.name, "American League")

    def test_league_has_attributes(self):
        self.league = self.mlb.get_league(103)
       
        self.assertIsInstance(self.league, League)

        self.assertTrue(self.league.numWildcardTeams)
        self.assertTrue(self.league.numGames)

