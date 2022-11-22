import unittest
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.sports import Sport
from mlbstatsapi import Mlb


class TestTeam(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.team = cls.mlb.get_team(133)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_team_instance_type_error(self):
        with self.assertRaises(TypeError):
            team = Team()

    def test_team_instance_id_instance_success(self):
        self.assertEqual(self.team.id, 133)
        self.assertIsInstance(self.team, Team)
        self.assertEqual(self.team.name, "Oakland Athletics")
        self.assertEqual(self.team.link, "/api/v1/teams/133")

    def test_team_instances_attribute_classes(self):
        """Team should return attributes as instances of Classes"""

        # test team attributes classes
        self.assertIsInstance(self.team.sport, Sport)
        self.assertIsInstance(self.team.venue, Venue)
        self.assertIsInstance(self.team.division, Division)
