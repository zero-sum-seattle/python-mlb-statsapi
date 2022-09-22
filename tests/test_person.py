import unittest
from unittest.mock import Mock, patch
from src.mlb import Player, Stats

class TestPerson(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls) -> None:
    #     cls.mock_get_patcher = patch('src.mlb.requests.get')
    #     cls.mock_get = cls.mock_get_patcher.start()

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     cls.mock_get_patcher.stop()

    def test_player_instance_type_error(self):        
        with self.assertRaises(TypeError):
            player = Person()

    def test_player_instance_type_error(self):        
        with self.assertRaises(AttributeError):
            player = Person("Ty France")

class TestStats(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls) -> None:
    #     cls.mock_get_patcher = patch('src.mlb.requests.get')
    #     cls.mock_get = cls.mock_get_patcher.start()

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     cls.mock_get_patcher.stop()

    def test_stat_instance_type_error(self):
        with self.assertRaises(TypeError):
            stat = Stats()

    def test_stat_instance_attribute_error(self):        
        with self.assertRaises(AttributeError):
            stat = Stats("Ty France")