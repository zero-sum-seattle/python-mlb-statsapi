import unittest
import requests_mock
import json
import os

from mlbstatsapi import Mlb
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Coach, Player

# Mocked JSON directory
# TODO Find a better way to structure and handle this :) 
path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_team_coaches = os.path.join(current_directory, "../mock_json/teams/team_roster_coaches.json")
path_to_team_players = os.path.join(current_directory, "../mock_json/teams/team_roster_players.json")
path_to_not_found = os.path.join(current_directory, "../mock_json/response/not_found_404.json")
path_to_error = os.path.join(current_directory, "../mock_json/response/error_500.json")

COACHES = open(path_to_team_coaches, "r", encoding="utf-8-sig").read()
PLAYERS = open(path_to_team_players, "r", encoding="utf-8-sig").read()
NOT_FOUND_404 = open(path_to_not_found, "r", encoding="utf-8-sig").read()
ERROR_500 = open(path_to_error, "r", encoding="utf-8-sig").read()

@requests_mock.Mocker()
class TestTeamRosterMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.al_team_id = 133
        cls.mock_coaches = json.loads(COACHES)
        cls.mock_players = json.loads(PLAYERS)
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_team_roster_list_of_player_objects(self, m):
        """Default Team Roster should return a list of players"""
        m.get('https://statsapi.mlb.com/api/v1/teams/133/roster', json=self.mock_players,
        status_code=200)
        self.roster = self.mlb.get_team_roster(team_id=self.al_team_id)
        self.assertIsInstance(self.roster, list)
        # Roster should return a list
        self.assertIsInstance(self.roster, list)

        # Roster should not return a empty list
        self.assertNotEqual(self.roster, [])
        for player in self.roster:
            self.assertIsInstance(player, Player)

    def test_team_roster_list_of_coach_objects(self, m):
        """Default Team Roster should return a list of coaches"""
        m.get('https://statsapi.mlb.com/api/v1/teams/133/coaches', json=self.mock_coaches,
        status_code=200)
        self.roster = self.mlb.get_team_coaches(team_id=self.al_team_id)
        # Roster should return a list
        self.assertIsInstance(self.roster, list)

        # Roster should not return a empty list
        self.assertNotEqual(self.roster, [])

        # Roster should return a list of Coaches
        for player in self.roster:
            self.assertIsInstance(player, Coach)