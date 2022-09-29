import unittest
from unittest.mock import Mock, patch
from mlbstatsapi.mlbapi import *
from mlbstatsapi.mlb import *


# Game with id of 662242 is used for this testing.
#
# 662242 info:
#           Cincinnati Reds (id:113) at Pittsburgh Pirates (id:134)
#           2022-09-26 at 6:35 pm
#           8766 attended with duration of 185 minutes and 38 minutes of delay
#           Pirates win 8 - 3


class TestGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.game = cls.mlb.get_game(662242)
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_game_instance_type_error(self):
         with self.assertRaises(TypeError):
            game = Game()

    def test_player_instance_position_arguments(self):
        game = self.game
        self.assertEqual(game.id, 662242)
        self.assertIsInstance(game, Game)

    # def test_game_base_class(self):
    #     game = Game(662242)
    #     self.assertIsInstance(game, MlbObject)

    # def test_player_base_class_attributes(self):
    #     game = Game(662242)
    #     self.assertTrue(hasattr(game, "_mlb_adapter"))

    def test_game_attributes(self):
        game = self.game
        self.assertTrue(hasattr(game, "metaData"))
        self.assertTrue(hasattr(game, "gameData"))
        self.assertTrue(hasattr(game, "liveData"))


    def test_game_metaData_attributes(self):
        game = self.game
        self.assertTrue(hasattr(game.metaData, "wait"))
        self.assertTrue(hasattr(game.metaData, "timeStamp"))
        self.assertTrue(hasattr(game.metaData, "gameEvents"))
        self.assertTrue(hasattr(game.metaData, "logicalEvents"))
