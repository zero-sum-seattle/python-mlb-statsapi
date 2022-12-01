import unittest
import requests_mock
import json
import os

from mlbstatsapi import Mlb
from mlbstatsapi.models.teams import Team

# Mocked JSON directory
# TODO Find a better way to structure and handle this :) 
path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_teams = os.path.join(current_directory, "../mock_json/teams/team.json")
path_to_team = os.path.join(current_directory, "../mock_json/teams/teams.json")
path_to_not_found = os.path.join(current_directory, "../mock_json/response/not_found_404.json")
path_to_error = os.path.join(current_directory, "../mock_json/response/error_500.json")

TEAMS = open(path_to_teams, "r", encoding="utf-8-sig").read()
TEAM = open(path_to_team, "r", encoding="utf-8-sig").read()
NOT_FOUND_404 = open(path_to_not_found, "r", encoding="utf-8-sig").read()
ERROR_500 = open(path_to_error, "r", encoding="utf-8-sig").read()

@requests_mock.Mocker()
class TestScheduleMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.al_team = 133
        cls.mock_team = json.loads(TEAMS)
        cls.mock_teams = json.loads(TEAMS)

                    
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_team_instance_id_instance_success(self, m):
        """get_team should return a Team object"""
        m.get('https://statsapi.mlb.com/api/v1/teams/133', json=self.mock_team,
        status_code=200)
        self.team = self.mlb.get_team(133)

        # team should not be None
        self.assertIsNotNone(self.team)

        # Team object should have attrs set
        self.assertEqual(self.team.id, 133)
        self.assertIsInstance(self.team, Team)
        self.assertEqual(self.team.name, "Oakland Athletics")
        self.assertEqual(self.team.link, "/api/v1/teams/133")


    def test_get_teams_for_sport(self, m):
        """get_teams should return a list of teams"""
        m.get('https://statsapi.mlb.com/api/v1/teams', json=self.mock_teams,
        status_code=200)
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