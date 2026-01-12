import unittest
from pydantic import ValidationError
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
        """Pydantic raises ValidationError when required fields are missing."""
        with self.assertRaises(ValidationError):
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
        self.assertTrue(hasattr(self.league, "name_short"))
        self.assertTrue(hasattr(self.league, "season_state"))
        self.assertTrue(hasattr(self.league, "has_wildcard"))
        self.assertTrue(hasattr(self.league, "has_split_season"))
        self.assertTrue(hasattr(self.league, "num_games"))
        self.assertTrue(hasattr(self.league, "has_playoff_points"))
        self.assertTrue(hasattr(self.league, "num_teams"))
        self.assertTrue(hasattr(self.league, "num_wildcard_teams"))
        self.assertTrue(hasattr(self.league, "season_date_info"))
        self.assertTrue(hasattr(self.league, "season"))
        self.assertTrue(hasattr(self.league, "org_code"))
        self.assertTrue(hasattr(self.league, "conferences_in_use"))
        self.assertTrue(hasattr(self.league, "divisions_in_use"))
        self.assertTrue(hasattr(self.league, "sport"))
        self.assertTrue(hasattr(self.league, "sort_order"))
        self.assertTrue(hasattr(self.league, "active"))
