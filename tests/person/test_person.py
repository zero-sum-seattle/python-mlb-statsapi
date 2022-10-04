from logging import exception
import unittest
from mlbstatsapi.models.people import Person, PrimaryPosition
from mlbstatsapi import Mlb

class TestPerson(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.player = cls.mlb.get_person(664034)[0]

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_player_instance_type_error(self):
         with self.assertRaises(TypeError):
            player = Person()

    def test_player_instance_position_arguments(self):
        self.assertEqual(self.player.id, 664034)
        self.assertIsInstance(self.player, Person)
        self.assertEqual(self.player.fullName, "Ty France")
        self.assertEqual(self.player.link, "/api/v1/people/664034")

    def test_player_base_class_attributes(self):
        self.assertTrue(hasattr(self.player, "_mlb_adapter"))


class TestPersonPrimaryPosition(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.position_player = cls.mlb.get_person(664034)[0]

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_player_position_player_position(self):
        self.assertIsInstance(self.position_player.primaryPosition, PrimaryPosition)
        self.assertTrue(hasattr(self.position_player.primaryPosition, "code"))
