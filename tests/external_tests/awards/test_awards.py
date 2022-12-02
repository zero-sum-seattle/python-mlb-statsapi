import unittest
from mlbstatsapi.models.awards import Awards
from mlbstatsapi import Mlb


class TestAwards(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
    
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_awards(self):
        """get_awards should return a Award"""
        awards = self.mlb.get_awards(award_id='RETIREDUNI_108')
        self.assertIsInstance(awards, Awards)