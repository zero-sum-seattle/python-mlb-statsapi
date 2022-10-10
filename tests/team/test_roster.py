# import unittest
# from unittest.mock import Mock, patch
# from mlbstatsapi.models.people import Player, Coach, Person, PrimaryPosition
# from mlbstatsapi import Mlb


# class TestTeamRoster(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls) -> None:
#         cls.mlb = Mlb()
#         cls.team = cls.mlb.get_team(133)
#         cls.roster = cls.mlb.get_team_roster('133')

#     @classmethod
#     def tearDownClass(cls) -> None:
#         pass

#     def test_roster_attr(self):
#         """let's test a couple roster attributes"""
#         # check team Id
#         self.assertEqual(self.roster.teamId, 133)

#         # check roster list 
#         self.assertEqual(type(self.roster.roster), list)

#     def test_roster_players(self):
#         players = self.roster.roster
#         for active_player in players:
#             # Let's make sure every active_player is a Player
#             self.assertIsInstance(active_player, Player)

#             # every active_player should have a jersey number
#             self.assertTrue(hasattr(active_player, 'jerseyNumber'))

#             self.assertIsInstance(active_player.position, PrimaryPosition)

# class TestTeamCoaches(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls) -> None:
#         cls.mlb = Mlb()
#         cls.team = cls.mlb.get_team(133)
#         cls.roster = cls.mlb.get_team_roster('133')

#     @classmethod
#     def tearDownClass(cls) -> None:
#         pass

#     def test_roster_attr(self):
#         """let's test a couple roster attributes"""
#         # check team Id
#         self.assertEqual(self.roster.teamId, 133)

#         # check roster list 
#         self.assertEqual(type(self.roster.roster), list)

#     def test_roster_players(self):
#         players = self.roster.roster
#         for active_player in players:
#             # Let's make sure every active_player is a Player
#             self.assertIsInstance(active_player, Player)

#             # every active_player should have a jersey number
#             self.assertTrue(hasattr(active_player, 'jerseyNumber'))

#             self.assertIsInstance(active_player.position, PrimaryPosition)