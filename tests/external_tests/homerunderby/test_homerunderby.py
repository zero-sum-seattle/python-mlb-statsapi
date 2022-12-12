import unittest
from mlbstatsapi.models.homerunderby import Homerunderby, Round
from mlbstatsapi import Mlb


class TestHomerunderby(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
    
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_gamepace(self):
        """This test should return a 200 and Round"""

        # set draft id
        game_id = 511101

        # call get_gamepace return Gamepace object
        derby = self.mlb.get_homerun_derby(game_id)

        # Gamepace should not be None
        self.assertIsNotNone(derby)

        self.assertIsInstance(derby, Homerunderby)

        # list should not be empty
        self.assertNotEqual(derby.rounds, [])

        # items in list should be gamepace data
        self.assertIsInstance(derby.rounds[0], Round)

    def test_get_homerunderby_404(self):
        """This test should return a 200 and """

        # set gameid to invalid id
        game_id = '100394810242'

        # call get_gamepace return Gamepace object
        derby = self.mlb.get_homerun_derby(game_id)

        # gamepace should be None
        self.assertIsNone(derby)