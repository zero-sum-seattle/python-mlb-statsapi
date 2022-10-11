from logging import exception
import unittest
from mlbstatsapi import MlbDataAdapter, MlbResult

class TestPerson(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb_adapter = MlbDataAdapter()

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlbadapter_class(self):
        pass
        # check passing basic arguments 

    def test_mlbadapter_logger(self):
        pass
        # write tests to test logger functions

    def test_mlbadapter_get(self):
        pass
        # write some test for basic return data

