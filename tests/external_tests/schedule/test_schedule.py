import unittest
from pydantic import ValidationError
from mlbstatsapi.models.schedules import Schedule
from mlbstatsapi import Mlb


class TestSchedule(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.schedule = cls.mlb.get_schedule(date='2022-10-07')

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_schedule_instance_validation_error(self):
        with self.assertRaises(ValidationError):
            schedule = Schedule()

    def test_schedule_instance_position_arguments(self):
        self.assertEqual(self.schedule.total_items, 4)
        self.assertEqual(self.schedule.total_events, 0)
        self.assertEqual(self.schedule.total_games, 4)

    def test_schedule_has_attributes(self):
        self.assertIsInstance(self.schedule, Schedule)
        self.assertTrue(hasattr(self.schedule, "total_items"))
        self.assertTrue(hasattr(self.schedule, "total_events"))
        self.assertTrue(hasattr(self.schedule, "total_games"))
        self.assertTrue(hasattr(self.schedule, "total_games_in_progress"))
        self.assertTrue(hasattr(self.schedule, "dates"))

    def test_schedule_pythonic_field_names(self):
        """Test that Pythonic field names are accessible."""
        self.assertIsNotNone(self.schedule.total_items)
        self.assertIsNotNone(self.schedule.dates)
        if self.schedule.dates:
            date = self.schedule.dates[0]
            self.assertIsNotNone(date.total_games)
            if date.games:
                game = date.games[0]
                self.assertIsNotNone(game.game_pk)
                self.assertIsNotNone(game.game_type)
                self.assertIsNotNone(game.game_date)
