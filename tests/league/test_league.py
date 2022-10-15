import unittest
from unittest.mock import Mock, patch
from mlbstatsapi.models.leagues import League
from mlbstatsapi import Mlb

class TestLeague(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.league = cls.mlb.get_league(103)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_league_instance_type_error(self):
        with self.assertRaises(TypeError):
            league = League()

    def test_league_instance_position_arguments(self):
        self.assertEqual(self.league.id, 103)
        self.assertEqual(self.league.link, "/api/v1/league/103")
        self.assertEqual(self.league.name, "American League")

    def test_league_has_attributes(self):
        self.assertIsInstance(self.league, League)
        self.assertTrue(hasattr(self.league, "id"))
        self.assertTrue(hasattr(self.league, "name"))
        self.assertTrue(hasattr(self.league, "link"))
        self.assertTrue(hasattr(self.league, "abbreviation"))
        self.assertTrue(hasattr(self.league, "nameshort"))
        self.assertTrue(hasattr(self.league, "seasonstate"))
        self.assertTrue(hasattr(self.league, "haswildcard"))
        self.assertTrue(hasattr(self.league, "hassplitseason"))
        self.assertTrue(hasattr(self.league, "numgames"))
        self.assertTrue(hasattr(self.league, "hasplayoffpoints"))
        self.assertTrue(hasattr(self.league, "numteams"))
        self.assertTrue(hasattr(self.league, "numwildcardteams"))
        self.assertTrue(hasattr(self.league, "seasondateinfo"))
        self.assertTrue(hasattr(self.league, "season"))
        self.assertTrue(hasattr(self.league, "orgcode"))
        self.assertTrue(hasattr(self.league, "conferencesinuse"))
        self.assertTrue(hasattr(self.league, "divisionsinuse"))
        self.assertTrue(hasattr(self.league, "sport"))
        self.assertTrue(hasattr(self.league, "sortorder"))
        self.assertTrue(hasattr(self.league, "active"))
