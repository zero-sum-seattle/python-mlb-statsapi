import unittest
from mlbstatsapi.models.divisions import Division
from mlbstatsapi import Mlb
from pydantic import ValidationError


class TestDivision(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.division = cls.mlb.get_division(200)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_divisions_instance_type_error(self):
        with self.assertRaises(ValidationError):
            division = Division()

    def test_divisions_instance_position_arguments(self):
        self.assertEqual(self.division.id, 200)
        self.assertEqual(self.division.link, "/api/v1/divisions/200")
        self.assertEqual(self.division.name, "American League West")

    def test_divisions_has_attributes(self):
        self.assertIsInstance(self.division, Division)
        self.assertTrue(hasattr(self.division, "id"))
        self.assertTrue(hasattr(self.division, "name"))
        self.assertTrue(hasattr(self.division, "link"))
        self.assertTrue(hasattr(self.division, "season"))
        self.assertTrue(hasattr(self.division, "nameShort"))
        self.assertTrue(hasattr(self.division, "abbreviation"))
        self.assertTrue(hasattr(self.division, "league"))
        self.assertTrue(hasattr(self.division, "sport"))
        self.assertTrue(hasattr(self.division, "hasWildcard"))
        self.assertTrue(hasattr(self.division, "sortOrder"))
        self.assertTrue(hasattr(self.division, "numPlayoffTeams"))
        self.assertTrue(hasattr(self.division, "active"))
