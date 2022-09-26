import unittest
from unittest.mock import Mock, patch
from mlbstatsapi.mlb import *


class TestTeam(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

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

    def test_team_base_class(self):
        team = Team(133, "Oakland Athletrics", "/api/v1/teams/133")
        self.assertIsInstance(team, MlbObject)

    def test_team_base_class_attributes(self):
        team = Team(133, "Oakland Athletrics", "/api/v1/teams/133")
        self.assertTrue(hasattr(team, "_mlb_adapter"))

    def test_team_stats_generate(self):
        team = Team(133, "Oakland Athletrics", "/api/v1/teams/133")
        team.generate_stats()
        self.assertTrue(hasattr(team, "stats"))
        self.assertIsInstance(team.stats, List)
        self.assertIsInstance(team.stats[0], Stats)




