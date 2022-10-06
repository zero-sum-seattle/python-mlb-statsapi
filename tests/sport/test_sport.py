import unittest
from unittest.mock import Mock, patch
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
        with self.assertRaises(TypeError):
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
        self.assertTrue(hasattr(self.sport, "sortOrder"))
        self.assertTrue(hasattr(self.sport, "activeStatus"))
