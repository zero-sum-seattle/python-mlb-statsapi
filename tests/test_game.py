import unittest
from unittest.mock import Mock, patch
from mlbstatsapi.mlbapi import *
from mlbstatsapi.mlb import *


class TestGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_game_instance_type_error(self):
         with self.assertRaises(TypeError):
            game = Game()

    def test_player_instance_position_arguments(self):
        game = Game(662242)
        self.assertEqual(game.id, 662242)
        self.assertIsInstance(game, Game)

    # def test_game_base_class(self):
    #     game = Game(662242)
    #     self.assertIsInstance(game, MlbObject)

    # def test_player_base_class_attributes(self):
    #     game = Game(662242)
    #     self.assertTrue(hasattr(game, "_mlb_adapter"))

    def test_game_attributes(self):
        mlb = Mlb()
        game = mlb.get_game(662242)
        self.assertTrue(hasattr(game, "metaData"))
        self.assertTrue(hasattr(game, "gameData"))
        self.assertTrue(hasattr(game, "liveData"))
