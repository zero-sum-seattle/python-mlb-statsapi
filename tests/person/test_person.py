import unittest
from mlbstatsapi.models.person import Person

class TestPerson(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_player_instance_type_error(self):
         with self.assertRaises(TypeError):
            player = Person()

    def test_player_instance_position_arguments(self):
        player = Person(664034, "/api/v1/people/664034", "Ty France")
        self.assertEqual(player.id, 664034)
        self.assertIsInstance(player, Person)
        self.assertEqual(player.full_name, "Ty France")
        self.assertEqual(player.link, "/api/v1/people/664034")

    def test_player_base_class_attributes(self):
        player = Person(664034, "Ty France", "/api/v1/people/664034")
        self.assertTrue(hasattr(player, "_mlb_adapter"))


