import unittest
from unittest.mock import Mock, patch
from mlbstatsapi.mlb import *


# class TestPersonStats(unittest.TestCase):
#     def test_player_generate_stats_default(self):
#         player = Person(664034, "Ty France", "/api/v1/people/664034")
#         self.assertTrue(hasattr(player, "_mlb_adapter"))
#         player.generate_stats()
#         self.assertTrue(hasattr(player, "stats"))
#         self.assertIsInstance(player.stats, List)
#         self.assertIsInstance(player.stats[0], Stats)


    # def test_player_generate_stats_select_group(self):
    #     player = Person(664034, "Ty France", "/api/v1/people/664034")
    #     self.assertTrue(hasattr(player, "_mlb_adapter"))
    #     stattypes = ["projected", "projectedRos", "season", "standard", "advanced", "career"]
    #     player.generate_stats(stattypes=stattypes)
    #     self.assertTrue(hasattr(player, "stats"))
    #     self.assertIsInstance(player.stats, List)
    #     self.assertIsInstance(player.stats[0], Stats)
