import unittest
from unittest.mock import Mock, patch
from pydantic import ValidationError
from mlbstatsapi.models.attendances import Attendance, attendance
from mlbstatsapi import Mlb


class TestAttendance(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        params = {'season': 2022}
        cls.attendance_team_away = cls.mlb.get_attendance(team_id=113)
        cls.attendance_team_home = cls.mlb.get_attendance(team_id=134)
        cls.attendance_season = cls.mlb.get_attendance(team_id=113, params=params)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_attendance_instance_validation_error(self):
        """Pydantic raises ValidationError when required fields are missing."""
        with self.assertRaises(ValidationError):
            attendance = Attendance()

    def test_attendance_instance_position_arguments(self):
        self.assertEqual(self.attendance_team_away.records[0].team.id, 113)
        self.assertEqual(self.attendance_team_home.records[0].team.id, 134)
        self.assertEqual(self.attendance_season.records[0].team.id, 113)

    def test_attendance_has_attributes(self):
        self.assertIsInstance(self.attendance_team_away, Attendance)
        self.assertIsInstance(self.attendance_team_home, Attendance)
        self.assertIsInstance(self.attendance_season, Attendance)
        self.assertTrue(hasattr(self.attendance_team_away, "records"))
        self.assertTrue(hasattr(self.attendance_team_away, "aggregate_totals"))
        self.assertTrue(hasattr(self.attendance_team_home, "records"))
        self.assertTrue(hasattr(self.attendance_team_home, "aggregate_totals"))
        self.assertTrue(hasattr(self.attendance_season, "records"))
        self.assertTrue(hasattr(self.attendance_season, "aggregate_totals"))

    def test_attendance_pythonic_field_names(self):
        """Test that Pythonic field names work correctly."""
        record = self.attendance_team_away.records[0]
        # Verify snake_case field names are accessible
        self.assertIsNotNone(record.openings_total)
        self.assertIsNotNone(record.games_total)
        self.assertIsNotNone(record.attendance_average_ytd)
        self.assertIsNotNone(record.game_type)
        
        # Verify aggregate totals use snake_case
        totals = self.attendance_team_away.aggregate_totals
        self.assertIsNotNone(totals.openings_total_away)
        self.assertIsNotNone(totals.attendance_total)
