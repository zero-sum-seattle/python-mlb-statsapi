import unittest
import requests_mock
import json
import os

from mlbstatsapi import Mlb


# Mocked JSON directory
# TODO Find a better way to structure and handle this :) 
path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(path_to_current_file)
path_to_hotcoldzone_file = os.path.join(current_directory, "../mock_json/stats/person/hotcoldzone.json")
path_to_not_found = os.path.join(current_directory, "../mock_json/response/not_found_404.json")
path_to_error = os.path.join(current_directory, "../mock_json/response/error_500.json")
path_to_player_stats = os.path.join(current_directory, "../mock_json/stats/person/pitching_player_stats.json")
path_to_team_stats = os.path.join(current_directory, "../mock_json/stats/team/pitching_team_stats.json")
path_to_pitching_playlog_file = os.path.join(current_directory, "../mock_json/stats/person/pitching_player_playlog.json")
path_to_pitching_pitchlog_file = os.path.join(current_directory, "../mock_json/stats/person/pitching_player_pitchlog.json")
path_to_spraychart_file = os.path.join(current_directory, "../mock_json/stats/person/spraychart.json")

HOTCOLDZONE = open(path_to_hotcoldzone_file, "r", encoding="utf-8-sig").read()
NOT_FOUND_404 = open(path_to_not_found, "r", encoding="utf-8-sig").read()
ERROR_500 = open(path_to_error, "r", encoding="utf-8-sig").read()
PLAYERSTATS = open(path_to_player_stats, "r", encoding="utf-8-sig").read()
TEAMSTATS = open(path_to_team_stats, "r", encoding="utf-8-sig").read()
PITCHING_PLAY_LOG = open(path_to_pitching_playlog_file, "r", encoding="utf-8-sig").read()
PITCHING_PITCH_LOG = open(path_to_pitching_pitchlog_file, "r", encoding="utf-8-sig").read()
SPRAYCHART = open(path_to_spraychart_file, "r", encoding="utf-8-sig").read()


@requests_mock.Mocker()
class TestPitchingStatsMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.pitcher = cls.mlb.get_person(660271)
        cls.al_team = cls.mlb.get_team(133)
        cls.mock_hotcoldzone = json.loads(HOTCOLDZONE)
        cls.error_500 = json.loads(ERROR_500)
        cls.mock_not_found = json.loads(NOT_FOUND_404)
        cls.mock_player_stats = json.loads(PLAYERSTATS)
        cls.mock_team_stats = json.loads(TEAMSTATS)
        cls.mock_pitching_playlog = json.loads(PITCHING_PLAY_LOG)
        cls.mock_pitching_pitchlog = json.loads(PITCHING_PITCH_LOG)
        cls.mock_spraycharts = json.loads(SPRAYCHART)


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
        stats = self.mlb.get_player_stats(self.pitcher.id, stats=self.stats, groups=self.group)

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
        stats = self.mlb.get_team_stats(self.al_team.id, stats=self.stats, groups=self.group)

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

    def test_pitching_play_log_for_player(self, m):
        """get_player_game_stats should return a dict with stats"""
        m.get('https://statsapi.mlb.com/api/v1/people/660271/stats?stats=hotColdZones&group=pitching', json=self.mock_hotcoldzone,
        status_code=200)
        self.stats = ['hotColdZones']
        self.groups = ['pitching']
        stats = self.mlb.get_player_stats(self.pitcher.id, stats=self.stats, groups=self.groups)

        # game_stats should not be None
        self.assertIsNotNone(stats)

        # game_stats should not be empty dic
        self.assertNotEqual(stats, {})

        # should not be empty
        self.assertTrue(stats['stats']['hotcoldzones'])

        hotcoldzone = stats['stats']['hotcoldzones'][0]

        # should not be empty
        self.assertTrue(hotcoldzone.stat)

        for zone in hotcoldzone.stat.zones:
            self.assertTrue(zone.zone)

    def test_pitching_pitchlog_for_pitcher(self, m):
        """get_player_game_stats should return a dict with stats"""
        m.get('https://statsapi.mlb.com/api/v1/people/660271/stats?stats=pitchLog&group=pitching', json=self.mock_pitching_pitchlog,
        status_code=200)
        self.stats = ['pitchLog']
        self.groups = ['pitching']
        stats = self.mlb.get_player_stats(self.pitcher.id, stats=self.stats, groups=self.groups)

        # game_stats should not be None
        self.assertIsNotNone(stats)

        # game_stats should not be empty dic
        self.assertNotEqual(stats, {})

        # playlog key should be populated
        self.assertTrue('pitching' in stats)
        self.assertTrue(stats['pitching']['pitchlog'])

        # pitchlog items should have attr set
        pitchlogs = stats['pitching']['pitchlog']

        for pitchlog in pitchlogs:
            self.assertTrue(pitchlog.stat)
    
    def test_pitching_playlog_for_pitcher(self, m):
        """get_player_game_stats should return a dict with stats"""
        m.get('https://statsapi.mlb.com/api/v1/people/660271/stats?stats=playLog&group=pitching', json=self.mock_pitching_playlog,
        status_code=200)
        self.stats = ['playLog']
        self.groups = ['pitching']
        stats = self.mlb.get_player_stats(self.pitcher.id, stats=self.stats, groups=self.groups)

        # game_stats should not be None
        self.assertIsNotNone(stats)

        # game_stats should not be empty dic
        self.assertNotEqual(stats, {})

        # playlog key should be populated
        self.assertTrue('pitching' in stats)
        self.assertTrue(stats['pitching']['playlog'])

        # pitchlog items should have attr set
        pitchlogs = stats['pitching']['playlog']

        for pitchlog in pitchlogs:
            self.assertTrue(pitchlog.stat)
    
    def test_pitching_play_log_for_player(self, m):
        """get_player_game_stats should return a dict with stats"""
        m.get('https://statsapi.mlb.com/api/v1/people/660271/stats?stats=sprayChart&group=pitching', json=self.mock_spraycharts,
        status_code=200)
        self.stats = ['sprayChart']
        self.groups = ['pitching']
        spraychart = self.mlb.get_player_stats(self.pitcher.id, stats=self.stats, groups=self.groups)

        # game_stats should not be None
        self.assertIsNotNone(spraychart)

        # game_stats should not be empty dic
        self.assertNotEqual(spraychart, {})

        self.assertTrue(spraychart['stats']['spraychart'])