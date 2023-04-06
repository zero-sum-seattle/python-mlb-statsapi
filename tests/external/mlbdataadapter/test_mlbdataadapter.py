import unittest
import requests
from unittest.mock import patch
from typing import List, Dict
from mlbstatsapi import MlbDataAdapter, TheMlbStatsApiException


class TestMlbAdapter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb_adapter = MlbDataAdapter()

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlbadapter_get_200(self):
        """mlbadapter should return 200 and data for sports endpoint"""

        # pretty stable external
        result = self.mlb_adapter.get(endpoint="sports")

        # status code should be 200
        self.assertEqual(result.status_code, 200)

        # data should not be None
        self.assertTrue(result.data)

    def test_mlbadapter_get_400(self):
        """mlbadapter should return 404, and result.data should be None"""

        # invalid endpoint 
        result = self.mlb_adapter.get(endpoint="teams/19990")

        # result.status_code should be 404
        self.assertEqual(result.status_code, 404)