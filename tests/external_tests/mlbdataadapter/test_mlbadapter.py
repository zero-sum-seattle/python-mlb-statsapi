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

    # I don't know if this is best practice
    def lower_keys_in_response(self, data):
        if isinstance(data, Dict):
            for key, value in data.items():
                self.assertTrue(key.islower())
                self.lower_keys_in_response(value)

        elif isinstance(data, List):        
            for item in data:
                self.lower_keys_in_response(item)

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
        self.params = {"stats": "season", "group": "hitting", "season": 2022}

        # use team stats end point for params
        result = self.mlb_adapter.get(endpoint="teams/133/stats", ep_params=self.params)

        # result should return 200
        self.assertEqual(result.status_code, 200)

        # result should have data
        self.assertTrue(result.data)

    def test_mlbadapter_transform_keys_in_data(self):
        """mlbadapter transform keys should make all keys lowercase"""

        # pretty stable external
        result = self.mlb_adapter.get(endpoint="sports")

        # status code should be 200
        self.assertEqual(result.status_code, 200)

        # data should not be None
        self.assertTrue(result.data)

        # data should all be lowercase
        self.lower_keys_in_response(result.data)


class MlbAdapterMockTesting(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb_adapter = MlbDataAdapter()
        cls.response = requests.Response()

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlbadapter_mock_bad_json(self):
        """mlbadapter should raise TheMlbStatsApiException"""
        # setting up mock
        self.response.status_code = 200
        self.response._content = '{"some bad json": sdfsd'.encode()

        # params to pass
        self.params = {"stats": "season", "group": "hitting"}

        # patch mlbdataadapter to return bad JSON
        with patch("mlbstatsapi.mlb_dataadapter.requests.get", return_value=self.response):

            # mlb_adapter should raise exception due to bad JSON
            with self.assertRaises(TheMlbStatsApiException):
                result = self.mlb_adapter.get(endpoint="teams/133/stats", ep_params=self.params)

    def test_mlbadapter_mock_404_json(self):
        """mlbadapter should raise TheMlbStatsApiException"""
        # setting up mock
        self.response.status_code = 404
        self.response._content = '{ "messageNumber": 10, "message": "Object not found", "timestamp": "2022-10-13T18:16:41.886604Z", "traceId": null }'.encode()

        # params to pass
        self.params = { "stats": "standard", "group": "hitting" }

        # patch mlbdataadapter to return 404 response
        with patch("mlbstatsapi.mlb_dataadapter.requests.get", return_value=self.response):

            # mlb_adapter should raise exception due to bad JSON
            result = self.mlb_adapter.get(endpoint="teams/133/stats", ep_params=self.params)
            
            # result.status_code should be 404
            self.assertEqual(result.status_code, 404)
     
            # result.data should be None
            self.assertEqual(result.data, {})

    def test_mlbadapter_mock_500_json(self):
        """mlbadapter should raise TheMlbStatsApiException"""
        # setting up mock
        self.response.status_code = 500
        self.response._content = '{ "messageNumber" : 1, "message" : "Internal error occurred", "timestamp" : "2022-10-13T18:37:47.600274Z", "traceId" : "9318607c0b50f493e9056648614a5cea" }'.encode()

        # params to pass
        self.params = {"stats": "standard", "group": "hitting"}

        # patch mlbdataadapter to return mocked response
        with patch("mlbstatsapi.mlb_dataadapter.requests.get", return_value=self.response):

            # mlb_adapter should raise exception due to 500 status code
            with self.assertRaises(TheMlbStatsApiException):
                result = self.mlb_adapter.get(endpoint="teams/133/stats", ep_params=self.params)