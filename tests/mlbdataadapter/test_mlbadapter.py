from logging import exception
import unittest
from mlbstatsapi import MlbDataAdapter, MlbResult, TheMlbStatsApiException

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

    def test_mlbadapter_get_200(self):
        """mlbadapter should return 200 and data for sports endpoint"""
        result = self.mlb_adapter.get(endpoint="sports")

        # status code should be 200
        self.assertEqual(result.status_code, 200)

        # data should not be None
        self.assertTrue(result.data)

    def test_mlbadapter_get_400(self):
        """mlbadapter should return 404, and result.data should be None"""
        result = self.mlb_adapter.get(endpoint="teams/19990")
        # write some test for basic return data

        # result.status_code should be 404
        self.assertEqual(result.status_code, 404)

        # result.data should be None
        self.assertIsNone(result.data)


    def test_mlbadapter_get_500(self):
        """mlbadapter should raise TheMlbStatsApiException for 500"""
        with self.assertRaises(TheMlbStatsApiException):
            result = self.mlb_adapter.get(endpoint="teams/133/stats?stats=vsPlayer&group=catching")
        
    def test_mlbadapter_bad_json(self):
        # This test requires bad JSON, and a mock
        pass 
