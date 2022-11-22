import unittest
from mlbstatsapi.models.people import Person, Position
from mlbstatsapi import Mlb


class TestPerson(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.player = cls.mlb.get_person(664034)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_player_instance_type_error(self):
        with self.assertRaises(TypeError):
            player = Person()

    def test_player_instance_position_arguments(self):
        self.assertEqual(self.player.id, 664034)
        self.assertIsInstance(self.player, Person)
        self.assertEqual(self.player.fullname, "Ty France")
        self.assertEqual(self.player.link, "/api/v1/people/664034")


class TestPersonPrimaryPosition(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.position_player = cls.mlb.get_person(664034)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_player_position_player_position(self):
        self.assertIsInstance(self.position_player.primaryposition, Position)
        self.assertTrue(hasattr(self.position_player.primaryposition, "code"))
