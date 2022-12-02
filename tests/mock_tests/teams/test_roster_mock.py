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
path_to_player_roster = os.path.join(current_directory, "../mock_json/teams/team_roster_players.json")
path_to_coaches_roster = os.path.join(current_directory, "../mock_json/teams/team_coaches.json")


PLAYERS = open(path_to_player_roster, "r", encoding="utf-8-sig").read()
COACHES = open(path_to_coaches_roster, "r", encoding="utf-8-sig").read()





@requests_mock.Mocker()
class TestTeamRoster(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.mock_players = json.loads(PLAYERS)
        cls.mock_coaches = json.loads(COACHES)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_team_roster_list_of_player_objects(self, m):
        """Default Team Roster should return a list of players"""
        m.get('https://statsapi.mlb.com/api/v1/teams/133/roster', json=self.mock_players,
        status_code=200)

        roster = self.mlb.get_team_roster(133)

        # roster should not be None
        self.assertIsNotNone(roster)

        # roster should be a list 
        self.assertIsInstance(roster, list)

        # roster should not be a empty list
        self.assertNotEqual(roster, [])

    def test_team_roster_list_of_coach_objects(self, m):
        """Default Team Roster should return a list of players"""
        m.get('https://statsapi.mlb.com/api/v1/teams/133/coaches', json=self.mock_coaches,
        status_code=200)

        roster = self.mlb.get_team_coaches(133)

        # roster should not be None
        self.assertIsNotNone(roster)

        # roster should be a list 
        self.assertIsInstance(roster, list)

        # roster should not be a empty list
        self.assertNotEqual(roster, [])