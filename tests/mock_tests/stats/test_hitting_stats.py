import unittest
import requests_mock
import json
import os

from mlbstatsapi import Mlb


# Mocked JSON directory
# TODO Find a better way to structure and handle this :) 
path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_player_stats = os.path.join(current_directory, "../mock_json/stats/person/hitting_player_stats.json")
path_to_team_stats = os.path.join(current_directory, "../mock_json/stats/person/hitting_team_stats.json")
path_to_not_found = os.path.join(current_directory, "../mock_json/response/not_found_404.json")
path_to_error = os.path.join(current_directory, "../mock_json/response/error_500.json")

PLAYERSTATS = open(path_to_player_stats, "r", encoding="utf-8-sig").read()
TEAMSTATS = open(path_to_team_stats, "r", encoding="utf-8-sig").read()
NOT_FOUND_404 = open(path_to_not_found, "r", encoding="utf-8-sig").read()
ERROR_500 = open(path_to_error, "r", encoding="utf-8-sig").read()

@requests_mock.Mocker()
class TestMlbDataApiMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.player = cls.mlb.get_person(665742)
        cls.team = cls.mlb.get_team(133)
        cls.mock_player_stats = json.loads(PLAYERSTATS)
        cls.mock_team_stats = json.loads(TEAMSTATS)
        cls.error_500 = json.loads(ERROR_500)
        cls.mock_not_found = json.loads(NOT_FOUND_404)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_hitting_stat_attributes_player(self, m):
        """mlb get stats should return pitching stats"""
        m.get('https://statsapi.mlb.com/api/v1/people/665742/stats?stats=season&stats=career&stats=seasonAdvanced&stats=careerAdvanced&group=hitting', json=self.mock_player_stats,
        status_code=200)
        self.stats = ['season', 'career','seasonAdvanced', 'careerAdvanced']
        self.group = ['hitting']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.player.id, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)
        self.assertFalse('pitching' in stats)
        self.assertEqual(len(stats['hitting']), 4)

        # check for split objects
        self.assertTrue(stats['hitting']['season'])
        self.assertTrue(stats['hitting']['career'])
        self.assertTrue(stats['hitting']['seasonadvanced'])
        self.assertTrue(stats['hitting']['careeradvanced'])

        # let's pull out a object and test it
        season = stats['hitting']['season'][0]
        career = stats['hitting']['career'][0]
        season_advanced = stats['hitting']['seasonadvanced'][0]
        career_advanced = stats['hitting']['careeradvanced'][0]
        # check that attrs exist and contain data
        self.assertTrue(season.season)
        self.assertTrue(season.stat.avg)
        self.assertTrue(career.player)
        self.assertTrue(season_advanced.season)
        self.assertTrue(season_advanced.stat.plateappearances)
        self.assertTrue(career_advanced.player)

    def test_pitching_stat_attributes_team(self, m):
        """mlb get stats should return pitching stats"""
        m.get('https://statsapi.mlb.com/api/v1/teams/133/stats?stats=season&stats=career&stats=seasonAdvanced&stats=careerAdvanced&group=hitting', json=self.mock_team_stats,
        status_code=200)
        self.stats = ['season', 'career', 'seasonAdvanced', 'careerAdvanced']
        self.group = ['hitting']
        # let's get some stats
        stats = self.mlb.get_team_stats(self.team.id, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('hitting' in stats)
        self.assertFalse('pitching' in stats)
        self.assertEqual(len(stats['hitting']), 4)

        # check for split objects
        self.assertTrue(stats['hitting']['season'])
        self.assertTrue(stats['hitting']['career'])
        self.assertTrue(stats['hitting']['seasonadvanced'])
        self.assertTrue(stats['hitting']['careeradvanced'])

        # let's pull out a object and test it
        season = stats['hitting']['season'][0]
        career = stats['hitting']['career'][0]
        season_advanced = stats['hitting']['seasonadvanced'][0]
        career_advanced = stats['hitting']['careeradvanced'][0]

        # check that attrs exist and contain data
        self.assertTrue(season.season)
        self.assertTrue(season.stat.avg)
        self.assertTrue(career.team)
        self.assertTrue(season_advanced.season)
        self.assertTrue(season_advanced.stat.plateappearances)
        self.assertTrue(career_advanced.team)