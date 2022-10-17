import unittest
from mlbstatsapi.mlbapi import Mlb
from mlbstatsapi.models.game import Game

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

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_game_creation(self):
        self.assertEqual(self.game.id, 662242)
        self.assertIsInstance(self.game, Game)

    def test_game_attrs(self):
        self.assertTrue(hasattr(self.game, "metadata"))
        self.assertTrue(hasattr(self.game, "gamedata"))
        self.assertTrue(hasattr(self.game, "livedata"))
 