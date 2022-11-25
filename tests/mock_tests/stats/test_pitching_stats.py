import unittest
import requests_mock
import json
import os

from mlbstatsapi import Mlb


# Mocked JSON directory
# TODO Find a better way to structure and handle this :) 
path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_player_stats = os.path.join(current_directory, "../mock_json/stats/person/pitching_player_stats.json")
path_to_team_stats = os.path.join(current_directory, "../mock_json/stats/team/pitching_team_stats.json")
path_to_not_found = os.path.join(current_directory, "../mock_json/response/not_found_404.json")
path_to_error = os.path.join(current_directory, "../mock_json/response/error_500.json")

PLAYERSTATS = open(path_to_player_stats, "r", encoding="utf-8-sig").read()
TEAMSTATS = open(path_to_team_stats, "r", encoding="utf-8-sig").read()
NOT_FOUND_404 = open(path_to_not_found, "r", encoding="utf-8-sig").read()
ERROR_500 = open(path_to_error, "r", encoding="utf-8-sig").read()

@requests_mock.Mocker()
class TestPitchingStatsMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.al_team = 133
        cls.shoei_ohtani = 660271
        cls.utility_player = 647351
        cls.mock_player_stats = json.loads(PLAYERSTATS)
        cls.mock_team_stats = json.loads(TEAMSTATS)
        cls.error_500 = json.loads(ERROR_500)
        cls.mock_not_found = json.loads(NOT_FOUND_404)

                    
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_pitching_stat_attributes_player(self, m):
        """mlb get stats should return pitching stats"""
        m.get('https://statsapi.mlb.com/api/v1/people/660271/stats?stats=season&stats=career&stats=seasonAdvanced&stats=careerAdvanced&group=pitching', json=self.mock_player_stats,
        status_code=200)
        self.stats = ['season', 'career', 'seasonAdvanced', 'careerAdvanced']
        self.group = ['pitching']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.shoei_ohtani, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)
        self.assertFalse('hitting' in stats)
        self.assertEqual(len(stats['pitching']), 4)

        # check for split objects
        self.assertTrue(stats['pitching']['season'])
        self.assertTrue(stats['pitching']['career'])
        self.assertTrue(stats['pitching']['seasonadvanced'])
        self.assertTrue(stats['pitching']['careeradvanced'])

        # let's pull out a object and test it
        season = stats['pitching']['season'][0]
        career = stats['pitching']['career'][0]
        season_advanced = stats['pitching']['seasonadvanced'][0]
        career_advanced = stats['pitching']['careeradvanced'][0]
        # check that attrs exist and contain data
        self.assertTrue(season.season)
        self.assertTrue(career.player)
        self.assertTrue(season.stat.strikeoutsper9inn)
        self.assertTrue(season_advanced.season)
        self.assertTrue(season_advanced.stat.strikeoutsper9)
        self.assertTrue(career_advanced.player)

    def test_pitching_stat_attributes_team(self, m):
        """mlb get stats should return pitching stats"""
        m.get('https://statsapi.mlb.com/api/v1/teams/133/stats?stats=season&stats=career&stats=seasonAdvanced&stats=careerAdvanced&group=pitching', json=self.mock_team_stats,
        status_code=200)
        self.stats = ['season', 'career','seasonAdvanced', 'careerAdvanced']
        self.group = ['pitching']
        # let's get some stats
        stats = self.mlb.get_team_stats(self.al_team, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('pitching' in stats)
        self.assertFalse('hitting' in stats)
        self.assertEqual(len(stats['pitching']), 4)

        # check for split objects
        self.assertTrue(stats['pitching']['season'])
        self.assertTrue(stats['pitching']['career'])
        self.assertTrue(stats['pitching']['seasonadvanced'])
        self.assertTrue(stats['pitching']['careeradvanced'])

        # let's pull out a object and test it
        season = stats['pitching']['season'][0]
        career = stats['pitching']['career'][0]
        season_advanced = stats['pitching']['seasonadvanced'][0]
        career_advanced = stats['pitching']['careeradvanced'][0]

        # check that attrs exist and contain data
        self.assertTrue(season.season)
        self.assertTrue(career.team)
        self.assertTrue(season.stat.strikeoutsper9inn)
        self.assertTrue(season_advanced.season)
        self.assertTrue(season_advanced.stat.strikeoutsper9)
        self.assertTrue(career_advanced.team)
