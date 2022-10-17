import unittest
from unittest.mock import Mock, patch
from mlbstatsapi.models.people import Player, Coach
from mlbstatsapi import Mlb


class TestTeamRoster(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.team = cls.mlb.get_team(133)
        cls.roster = cls.mlb.get_team_roster('133')

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_team_roster_list_of_player_objects(self):
        """Default Team Roster should return a list of players"""
        self.assertIsInstance(self.roster, list)
        for player in self.roster:
            self.assertIsInstance(player, Player)

    def test_team_roster_fail_list_of_player_objects(self):
        """This should return a empty list"""
        roster = self.mlb.get_team_roster('1333')
        self.assertListEqual(roster, [])

class TestCoachRoster(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.team = cls.mlb.get_team(133)
        cls.roster = cls.mlb.get_team_coaches('133')

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_team_roster_list_of_coach_objects(self):
        """Default Team Roster should return a list of coaches"""
        self.assertIsInstance(self.roster, list)
        for player in self.roster:
            self.assertIsInstance(player, Coach)

    def test_team_roster_fail_list_of_coach_objects(self):
        """This should return a empty list"""
        roster = self.mlb.get_team_coaches('1333')
        self.assertListEqual(roster, [])