# from typing import Dict, List
# from unittest.mock import patch
# import unittest
# import requests_mock
# import json
# import os


# from mlbstatsapi import Mlb
# from mlbstatsapi import MlbResult
# from mlbstatsapi import TheMlbStatsApiException

# path_to_not_found = os.path.join(current_directory, "../mock_json/response/not_found_404.json")
# path_to_error = os.path.join(current_directory, "../mock_json/response/error_500.json")
# NOT_FOUND_404 = open(path_to_not_found, "r", encoding="utf-8-sig").read()
# ERROR_500 = open(path_to_error, "r", encoding="utf-8-sig").read()

# @requests_mock.Mocker()
# class TestDraftMock(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls) -> None:
#         cls.mlb = Mlb()
#         cls.mock_divisions = json.loads(DIVISIONS_JSON_FILE)
#         cls.error_500 = json.loads(ERROR_500)
#         cls.mock_not_found = json.loads(NOT_FOUND_404)

#     @classmethod
#     def tearDownClass(cls) -> None:
#         pass
