import unittest
from unittest.mock import Mock, patch
from mlbstatsapi.models.attendances import Attendance, attendance
from mlbstatsapi import Mlb

class TestAttendance(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.attendance_team_away = cls.mlb.get_attendance(teamid=113) # Cincinati Reds 134
        cls.attendance_team_home = cls.mlb.get_attendance(teamid=134)
        # cls.attendance_league = cls.mlb.get_attendance(leagueId=103) # American League
        cls.attendance_season = cls.mlb.get_attendance(teamid=113, season=2022)


    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_attendance_instance_type_error(self):
        with self.assertRaises(TypeError):
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
        self.assertTrue(hasattr(self.attendance_team_away, "aggregatetotals"))
        self.assertTrue(hasattr(self.attendance_team_home, "records"))
        self.assertTrue(hasattr(self.attendance_team_home, "aggregatetotals"))
        self.assertTrue(hasattr(self.attendance_season, "records"))
        self.assertTrue(hasattr(self.attendance_season, "aggregatetotals"))