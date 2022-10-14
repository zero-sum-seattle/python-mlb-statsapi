import unittest
from unittest.mock import Mock, patch
from mlbstatsapi.models.schedules import Schedule
from mlbstatsapi import Mlb

class TestSchedule(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.schedule = cls.mlb.get_schedule_date('2022-10-07')

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_schedule_instance_type_error(self):
        with self.assertRaises(TypeError):
            schedule = Schedule()

    def test_schedule_instance_position_arguments(self):
        self.assertEqual(self.schedule.totalItems, 4)
        self.assertEqual(self.schedule.totalEvents, 0)
        self.assertEqual(self.schedule.totalGames, 4)

    def test_schedule_has_attributes(self):
        self.assertIsInstance(self.schedule, Schedule)
        self.assertTrue(hasattr(self.schedule, "totalItems"))
        self.assertTrue(hasattr(self.schedule, "totalEvents"))
        self.assertTrue(hasattr(self.schedule, "totalGames"))
        self.assertTrue(hasattr(self.schedule, "totalGamesInProgress"))
        self.assertTrue(hasattr(self.schedule, "dates"))
       
    def test_schedule_get_games_with_status(self):
        self.assertEqual(self.schedule.get_games_with_status(detailedState="In Progress"), [])
        self.assertEqual(self.schedule.get_games_with_status(abstractGameState="Final"), [715770, 715764, 715767, 715761])
        self.assertEqual(self.schedule.get_games_with_status(), [])

    # def test_schedule_get_games_inProgress(self):

    def test_schedule_get_games_finished(self):
        self.assertEqual(self.schedule.get_games_finished(), [715770, 715764, 715767, 715761])
