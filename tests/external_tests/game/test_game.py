import unittest
from mlbstatsapi.mlb_api import Mlb
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
        cls.game = cls.mlb.get_game(717911)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_game_creation(self):
        self.assertEqual(self.game.id, 717911)
        self.assertIsInstance(self.game, Game)

    def test_game_attrs(self):
        self.assertTrue(hasattr(self.game, "metadata"))
        self.assertTrue(hasattr(self.game, "game_data"))
        self.assertTrue(hasattr(self.game, "live_data"))

    def test_game_pythonic_field_names(self):
        """Test that Pythonic field names are accessible."""
        # Test top-level game attributes
        self.assertIsNotNone(self.game.game_pk)
        self.assertIsNotNone(self.game.metadata)
        self.assertIsNotNone(self.game.game_data)
        self.assertIsNotNone(self.game.live_data)

        # Test game_data nested attributes
        self.assertIsNotNone(self.game.game_data.game)
        self.assertIsNotNone(self.game.game_data.datetime)
        self.assertIsNotNone(self.game.game_data.status)
        self.assertIsNotNone(self.game.game_data.teams)
        self.assertIsNotNone(self.game.game_data.venue)
        self.assertIsNotNone(self.game.game_data.official_venue)
        self.assertIsNotNone(self.game.game_data.probable_pitchers)

        # Test live_data nested attributes
        self.assertIsNotNone(self.game.live_data.plays)
        self.assertIsNotNone(self.game.live_data.boxscore)
        self.assertIsNotNone(self.game.live_data.leaders)
