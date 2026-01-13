import unittest
from pydantic import ValidationError
from mlbstatsapi.models.sports import Sport
from mlbstatsapi import Mlb


class TestSport(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.sport = cls.mlb.get_sport(1)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_sport_instance_type_error(self):
        """Pydantic raises ValidationError when required fields are missing."""
        with self.assertRaises(ValidationError):
            sport = Sport()

    def test_sport_instance_position_arguments(self):
        self.assertEqual(self.sport.id, 1)
        self.assertEqual(self.sport.link, "/api/v1/sports/1")
        self.assertEqual(self.sport.name, "Major League Baseball")

    def test_sport_attributes(self):
        self.assertIsInstance(self.sport, Sport)
        self.assertTrue(hasattr(self.sport, "id"))
        self.assertTrue(hasattr(self.sport, "link"))
        self.assertTrue(hasattr(self.sport, "name"))
        self.assertTrue(hasattr(self.sport, "code"))
        self.assertTrue(hasattr(self.sport, "abbreviation"))
        self.assertTrue(hasattr(self.sport, "sort_order"))
        self.assertTrue(hasattr(self.sport, "active_status"))
