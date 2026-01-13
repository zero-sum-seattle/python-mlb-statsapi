import unittest
from mlbstatsapi.models.gamepace import GamePace, GamePaceData
from mlbstatsapi import Mlb


# class TestGamepace(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls) -> None:
#         cls.mlb = Mlb()

#     @classmethod
#     def tearDownClass(cls) -> None:
#         pass

#     def test_get_gamepace(self):
#         """This test should return a 200 and Round"""

#         # set draft id
#         season_id = 2021        

#         # call get_gamepace return GamePace object
#         gamepace = self.mlb.get_gamepace(season_id)

#         # GamePace should not be None
#         self.assertIsNotNone(gamepace)

#         self.assertIsInstance(gamepace, GamePace)

#         # list should not be empty
#         self.assertNotEqual(gamepace.sports, [])

#         # items in list should be gamepace data
#         self.assertIsInstance(gamepace.sports[0], GamePaceData)

#         sportgamepace = gamepace.sports[0]

#         # sportgamepace should not be none
#         self.assertIsNotNone(sportgamepace)

#         # sportgamepace should have attrs set
#         self.assertTrue(sportgamepace.hits_per_game)
#         self.assertTrue(sportgamepace.total_games)

#     def test_get_gamepace_404(self):
#         """This test should return a 200 and """

#         # set gamepace season to invalid year
#         season_id = '2040,21'

#         # call get_gamepace return GamePace object
#         gamepace = self.mlb.get_gamepace(season_id)

#         # gamepace should be None
#         self.assertIsNone(gamepace)

#     def test_get_gamepace_with_params(self):
#         """this test should return results for gamepace with leagueid 103"""

#         season_id = 2021
#         leagueId = "103"

#         # call get_gamepace return gamepace object
#         gamepace = self.mlb.get_gamepace(season_id, leagueId=leagueId)
#         # gamepace should not be None
#         self.assertIsNotNone(gamepace)
#         # list should not be empty
#         self.assertNotEqual(gamepace.leagues, [])
