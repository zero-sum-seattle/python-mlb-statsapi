import unittest
from unittest.mock import Mock, patch
from mlbstatsapi.models.teams import Team
from mlbstatsapi import Mlb

class TestTeam(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.team = cls.mlb.get_team(133)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_player_instance_type_error(self):
        with self.assertRaises(TypeError):
            team = Team()

    def test_player_instance_id_instance_success(self):
        team = Team(133, "Oakland Athletics", "/api/v1/teams/133")
        self.assertEqual(team.id, 133)
        self.assertIsInstance(team, Team)
        self.assertEqual(team.name, "Oakland Athletics")
        self.assertEqual(team.link, "/api/v1/teams/133")


