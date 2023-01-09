import unittest
from mlbstatsapi import Mlb
from mlbstatsapi.models.drafts import Round


class TestRound(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_draft_by_year_id(self):
        """This test should return a 200 and Round"""

        # set draft id
        draft_id = "2019"

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

    def test_get_draft_by_year_id_404(self):
        """This test should return a 200 and """

        # set draft id to invalid year
        draft_id = "20192"

        # call get_draft return list
        draft = self.mlb.get_draft(draft_id)

        # draft should not be None
        self.assertIsNotNone(draft)

        # list should be empty
        self.assertEqual(draft, [])


    def test_get_draft_with_params(self):
        """this test should return results for draft round 1 2019"""

        draft_id = "2019"
        round = "1"

        # call get_draft return list
        draft = self.mlb.get_draft(draft_id, round=round)
        # draft should not be None
        self.assertIsNotNone(draft)
        # list should not be empty and return len one
        self.assertNotEqual(draft, [])
        self.assertTrue(len(draft) == 1)

        # round attr should equal 1
        one_round = draft[0]
        self.assertTrue(one_round.round == "1")

