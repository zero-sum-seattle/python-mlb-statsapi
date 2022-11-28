import unittest
import requests_mock
import json
import os

from mlbstatsapi import Mlb
from mlbstatsapi.models.schedules import Schedule, ScheduleGames

# Mocked JSON directory
# TODO Find a better way to structure and handle this :) 
path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_schedule_date = os.path.join(current_directory, "../mock_json/schedule/schedule_date.json")
path_to_schedule_start_end_dates = os.path.join(current_directory, "../mock_json/schedule/schedule_start_end_date.json")
path_to_not_found = os.path.join(current_directory, "../mock_json/response/not_found_404.json")
path_to_error = os.path.join(current_directory, "../mock_json/response/error_500.json")

SCHEDULES = open(path_to_schedule_date, "r", encoding="utf-8-sig").read()
SCHEDULE = open(path_to_schedule_start_end_dates, "r", encoding="utf-8-sig").read()
NOT_FOUND_404 = open(path_to_not_found, "r", encoding="utf-8-sig").read()
ERROR_500 = open(path_to_error, "r", encoding="utf-8-sig").read()

@requests_mock.Mocker()
class TestScheduleMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.al_team = 133

        cls.mock_schedule = json.loads(SCHEDULE)
        cls.mock_schedules = json.loads(SCHEDULE)

        cls.error_500 = json.loads(ERROR_500)
        cls.mock_not_found = json.loads(NOT_FOUND_404)

                    
    @classmethod
    def tearDownClass(cls) -> None:
        pass


    def test_get_schedule(self, m ):
        """get_schedule should return schedules for date, starDate, endDate"""
        m.get('https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=04/07/2022&endDate=04/07/2022', json=self.mock_schedule,
        status_code=200)
        self.date = '04/07/2022'
        self.sport_id = 1
        schedule = self.mlb.get_schedule(date=self.date)

        # get_schedule should return Schedule object
        self.assertIsInstance(schedule, Schedule)
        # get_schedule should return dates
        self.assertTrue(schedule.dates)

    def test_get_schedule_start_end_dates(self, m):
        """get_schedule should return a schedule object with start_date, end_date"""
        m.get('https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=10/10/2022&endDate=10/13/2022', json=self.mock_schedules,
        status_code=200)
        self.sport_id = 1
        self.start_date = '10/10/2022'
        self.end_date = '10/13/2022'
        schedule = self.mlb.get_schedule(date=self.start_date, end_date=self.end_date, sport_id=self.sport_id)

        # get_schedule should return Schedule object
        self.assertIsInstance(schedule, Schedule)

        # list should contain more than 1 object
        self.assertTrue(len(schedule.dates) > 1)


    def test_get_scheduled_games_by_date(self, m):
        """get_schedule should return a ScheduledGames object with start_date, end_date"""
        m.get('https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=10/10/2022&endDate=10/13/2022', json=self.mock_schedules,
        status_code=200)
        self.sport_id = 1
        self.start_date = '10/10/2022'
        self.end_date = '10/13/2022'
        
        scheduled_games = self.mlb.get_scheduled_games_by_date(date=self.start_date, end_date=self.end_date, sport_id=1)

        # scheduled games should not be none
        self.assertIsNotNone(scheduled_games)

        self.assertIsInstance(scheduled_games, list)

        # scheduled games should not be empty list
        self.assertNotEqual(scheduled_games, [])

        scheduled_game = scheduled_games[0]

        self.assertIsInstance(scheduled_game, ScheduleGames)