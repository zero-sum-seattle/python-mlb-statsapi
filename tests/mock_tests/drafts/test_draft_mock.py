from typing import Dict, List
from unittest.mock import patch
import unittest
import requests_mock
import json
import os


from mlbstatsapi import Mlb
from mlbstatsapi import MlbResult
from mlbstatsapi import TheMlbStatsApiException
from mlbstatsapi.models.drafts import Round


path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_drafts = os.path.join(current_directory, "../mock_json/drafts/draft.json")
DRAFTS = open(path_to_drafts, "r", encoding="utf-8-sig").read()

@requests_mock.Mocker()
class TestDraftMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.drafts_mock = json.loads(DRAFTS)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_draft_by_year_id(self, m):
        """This test should return a 200 and Round"""
        m.get('https://statsapi.mlb.com/api/v1/draft/2018', json=self.drafts_mock,
        status_code=200)
        # set draft id
        draft_id = "2018"

        # call get_draft return list
        draft = self.mlb.get_draft(draft_id)

        # draft should not be None
        self.assertIsNotNone(draft)

        # list should not be empty
        self.assertNotEqual(draft, [])

        # items in list should be Round
        self.assertIsInstance(draft[0], Round)

        draftpicks = draft[0].picks

        # draftpicks should not be none
        self.assertIsNotNone(draftpicks)

        # list should not be empty
        self.assertNotEqual(draftpicks, [])

        draftpick = draftpicks[0]

        # draft pick should have attrs set
        self.assertTrue(draftpick.pickround)