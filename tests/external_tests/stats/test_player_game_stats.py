import unittest
import time

from mlbstatsapi.mlb_api import Mlb


class TestHittingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.al_team = 133
        cls.shoei_ohtani = 660271
        cls.game_id = 531368
                    
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    
    def test_get_players_stats_for_game(self, m):
        """return player stat objects"""

        game_stats = self.mlb.get_players_stats_for_game(person_id=self.shoei_ohtani,
                                                         game_id=self.game_id)

        # game stats should not be None
        self.assertIsNotNone(game_stats)

        # game_stats should be a dict
        self.assertIsInstance(game_stats, dict)

        # vsPlayer5Y hitting
        # vsPlayer5Y pitching
