import unittest
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.sports import Sport
from mlbstatsapi import Mlb
from pydantic import ValidationError





class TestTeam(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()


    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_team_instance_type_error(self):
        with self.assertRaises(ValidationError):
            team = Team()

    def test_team_instance_id_instance_success(self):
        """get_team should return a Team object"""
        self.team = self.mlb.get_team(133)

        # team should not be None
        self.assertIsNotNone(self.team)

        # Team object should have attrs set
        self.assertEqual(self.team.id, 133)
        self.assertIsInstance(self.team, Team)
        self.assertEqual(self.team.name, "Oakland Athletics")
        self.assertEqual(self.team.link, "/api/v1/teams/133")
        self.assertIsInstance(self.team.sport, Sport)
        self.assertIsInstance(self.team.venue, Venue)
        self.assertIsInstance(self.team.division, Division)

    def test_get_teams_for_sport(self):
        """get_teams should return a list of teams"""
        self.teams = self.mlb.get_teams(sport_id=1)

        # teams should not be none
        self.assertIsNotNone(self.teams)

        # teams should be a list
        self.assertIsInstance(self.teams, list)

        # teams should not be empty list
        self.assertNotEqual(self.teams, [])

        self.teams = self.mlb.get_teams(sport_id=11)

        # teams should not be none
        self.assertIsNotNone(self.teams)

        # teams should be a list
        self.assertIsInstance(self.teams, list)

        # teams should not be empty list
        self.assertNotEqual(self.teams, [])