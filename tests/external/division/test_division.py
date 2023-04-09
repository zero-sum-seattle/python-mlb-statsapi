import unittest
from mlbstatsapi.models.divisions import Division
from mlbstatsapi import Mlb


class TestDivision(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_divisions_instance_type_error(self):
        with self.assertRaises(TypeError):
            division = Division()

    def test_divisions_instance_position_arguments(self):
        self.division = self.mlb.get_division(200)

        self.assertEqual(self.division.id, 200)
        self.assertEqual(self.division.link, "/api/v1/divisions/200")
        self.assertEqual(self.division.name, "American League West")

    def test_divisions_has_attributes(self):
        self.division = self.mlb.get_division(200)

        self.assertIsInstance(self.division, Division)

        self.assertTrue(self.division.numPlayoffTeams)
        self.assertTrue(self.division.nameShort)


