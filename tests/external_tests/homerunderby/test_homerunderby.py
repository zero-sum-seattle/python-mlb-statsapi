import unittest
from mlbstatsapi.models.homerunderby import HomeRunDerby, Round
from mlbstatsapi import Mlb


class TestHomerunderby(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
    
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_homerunderby(self):
        """This test should return a 200 and Round"""

        # set game id
        game_id = 511101

        # call get_homerun_derby return HomeRunDerby object
        derby = self.mlb.get_homerun_derby(game_id)

        # HomeRunDerby should not be None
        self.assertIsNotNone(derby)

        self.assertIsInstance(derby, HomeRunDerby)

        # list should not be empty
        self.assertNotEqual(derby.rounds, [])

        # items in list should be Round
        self.assertIsInstance(derby.rounds[0], Round)

    def test_get_homerunderby_404(self):
        """This test should return None for invalid game id"""

        # set gameid to invalid id
        game_id = '100394810242'

        # call get_homerun_derby return HomeRunDerby object
        derby = self.mlb.get_homerun_derby(game_id)

        # derby should be None
        self.assertIsNone(derby)
