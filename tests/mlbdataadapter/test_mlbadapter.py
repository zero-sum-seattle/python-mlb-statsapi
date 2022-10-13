from logging import exception
import unittest
import requests
from unittest.mock import Mock, patch
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

        # result.data should be None
        self.assertEqual(result.data, {})


    def test_mlbadapter_get_500(self):
        """mlbadapter should raise TheMlbStatsApiException for 500"""

        # bad endpoint should raise exception due to 500
        with self.assertRaises(TheMlbStatsApiException):
            result = self.mlb_adapter.get(endpoint="teams/133/stats?stats=vsPlayer&group=catching")

    def test_mlbadapter_get_params(self):
        """mlbadapter should accept params and parse them to the url"""

        # stat type season, stat group hitting
        self.params = { "stats": "season", "group": "hitting" }
        
        # use team stats end point for params
        result = self.mlb_adapter.get(endpoint="teams/133/stats", ep_params=self.params)

        # result should return 200
        self.assertEqual(result.status_code, 200)

        # result should have data
        self.assertTrue(result.data)


    # def test_mlbadapter_bad_json(self):
    #     """mlbadapter should raise TheMlbStatsApiException"""

    #     self.mock_get_patcher = patch('mlbstatsapi.mlbdataadapter.requests.get')
    #     self.mock_get = self.mock_get_patcher.start()

    #     # This test requires bad JSON, and a mock
    #     self.response._content = '{"some bad json": '
    #     self.response.status_code = 200
    #     self.params = { "stats": "season", "group": "hitting" }

    #     # mock patch requests and set return_value as mock response
 
    #         # mlbdataadapter should raise exception
    #     with self.assertRaises(TheMlbStatsApiException):
    #         result = self.mlb_adapter.get(endpoint="teams/133/stats", ep_params=self.params)
        
    #     # stop mock
    #     self.mock_get_patcher.stop()



