import unittest
from mlbstatsapi.models.homerunderby import HomeRunDerby, Round
from mlbstatsapi import Mlb, MlbHttpError


class TestHomerunderby(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.mlb.close()

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

    def test_get_homerunby_invalid_game_id(self):
        """An invalid game ID currently produces a 400 from a live MLB API."""

        game_id = "100394810242"

        with self.assertRaises(MlbHttpError) as raised:
            self.mlb.get_homerun_derby(game_id)

        self.assertEqual(raised.exception.status_code, 400)


