import unittest
from mlbstatsapi.models.awards import Award
from mlbstatsapi import Mlb


class TestAwards(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
    
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_awards(self):
        """This test should return a 200 and Round"""

        # set draft id
        award_id = "RETIREDUNI_108"

        # call get_draft return list
        awards = self.mlb.get_awards(award_id)

        # draft should not be None
        self.assertIsNotNone(awards)

        # list should not be empty
        self.assertNotEqual(awards, [])

        # items in list should be an award
        self.assertIsInstance(awards[0], Award)

        award = awards[0]

        # award should not be none
        self.assertIsNotNone(award)

        # award should have attrs set
        self.assertTrue(award.id)
        self.assertTrue(award.name)

    def test_get_awards_404(self):
        """This test should return a 200 and """

        # set award id to invalid award
        award_id = "THIS_IS_NOT_AN_AWARDID"

        # call get_awards return list
        awards = self.mlb.get_awards(award_id)

        # awards should not be None
        self.assertIsNotNone(awards)

        # list should be empty
        self.assertEqual(awards, [])


    def test_get_awards_with_params(self):
        """this test should return results for draft round 1 2019"""

        award_id = "RETIREDUNI_108"
        leagueId = "103"

        # call get_awards return list
        awards = self.mlb.get_awards(award_id, leagueId=leagueId)
        # awards should not be None
        self.assertIsNotNone(awards)
        # list should not be empty
        self.assertNotEqual(awards, [])
