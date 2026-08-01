import unittest

from mlbstatsapi import MlbDataAdapter


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
        """mlbadapter should return 404, and result.data should be empty"""

        # invalid endpoint
        result = self.mlb_adapter.get(endpoint="teams/19990")

        # result.status_code should be 404
        self.assertEqual(result.status_code, 404)

        # result.data should be empty
        self.assertEqual(result.data, {})

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
