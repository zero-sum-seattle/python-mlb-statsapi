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
path_to_team_stats = os.path.join(current_directory, "../mock_json/stats/team/hitting_team_stats.json")
path_to_not_found = os.path.join(current_directory, "../mock_json/response/not_found_404.json")
path_to_error = os.path.join(current_directory, "../mock_json/response/error_500.json")
path_to_hotcoldzone_file = os.path.join(current_directory, "../mock_json/stats/person/hotcoldzone.json")
path_to_hitting_playLog_file = os.path.join(current_directory, "../mock_json/stats/person/hitting_player_playlog.json")
path_to_hitting_pitchLog_file = os.path.join(current_directory, "../mock_json/stats/person/hitting_player_pitchlog.json")
path_to_sprayChart_file = os.path.join(current_directory, "../mock_json/stats/person/spraychart.json")

SPRAYCHART = open(path_to_sprayChart_file, "r", encoding="utf-8-sig").read()
HOTCOLDZONE = open(path_to_hotcoldzone_file, "r", encoding="utf-8-sig").read()
PLAYERSTATS = open(path_to_player_stats, "r", encoding="utf-8-sig").read()
TEAMSTATS = open(path_to_team_stats, "r", encoding="utf-8-sig").read()
NOT_FOUND_404 = open(path_to_not_found, "r", encoding="utf-8-sig").read()
ERROR_500 = open(path_to_error, "r", encoding="utf-8-sig").read()
HITTING_PLAY_LOG = open(path_to_hitting_playLog_file, "r", encoding="utf-8-sig").read()
HITTING_PITCH_LOG = open(path_to_hitting_pitchLog_file, "r", encoding="utf-8-sig").read()

@requests_mock.Mocker()
class TestHittingStatsMock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.player = cls.mlb.get_person(665742)
        cls.team = cls.mlb.get_team(133)
        cls.mock_player_stats = json.loads(PLAYERSTATS)
        cls.mock_team_stats = json.loads(TEAMSTATS)
        cls.mock_hotcoldzone = json.loads(HOTCOLDZONE)
        cls.error_500 = json.loads(ERROR_500)
        cls.mock_not_found = json.loads(NOT_FOUND_404)
        cls.mock_hitting_playLog = json.loads(HITTING_PLAY_LOG)
        cls.mock_hitting_pitchLog = json.loads(HITTING_PITCH_LOG)
        cls.mock_sprayCharts = json.loads(SPRAYCHART)

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
        self.assertTrue(stats['hitting']['seasonAdvanced'])
        self.assertTrue(stats['hitting']['careerAdvanced'])

        # let's pull out a object and test it
        season = stats['hitting']['season']
        career = stats['hitting']['career']
        season_advanced = stats['hitting']['seasonAdvanced']
        career_advanced = stats['hitting']['careerAdvanced']
        # check that attrs exist and contain data

        self.assertEqual(season.total_splits, len(season.splits))
        self.assertEqual(season.group, 'hitting')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.total_splits, len(career.splits))
        self.assertEqual(career.group, 'hitting')
        self.assertEqual(career.type, 'career')

        self.assertEqual(season_advanced.total_splits, len(season_advanced.splits))
        self.assertEqual(season_advanced.group, 'hitting')
        self.assertEqual(season_advanced.type, 'seasonAdvanced')

        self.assertEqual(career_advanced.total_splits, len(career_advanced.splits))
        self.assertEqual(career_advanced.group, 'hitting')
        self.assertEqual(career_advanced.type, 'careerAdvanced')

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
        self.assertTrue(stats['hitting']['seasonAdvanced'])
        self.assertTrue(stats['hitting']['careerAdvanced'])

        # let's pull out a object and test it
        season = stats['hitting']['season']
        career = stats['hitting']['career']
        season_advanced = stats['hitting']['seasonAdvanced']
        career_advanced = stats['hitting']['careerAdvanced']
        # check that attrs exist and contain data

        self.assertEqual(season.total_splits, len(season.splits))
        self.assertEqual(season.group, 'hitting')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.total_splits, len(career.splits))
        self.assertEqual(career.group, 'hitting')
        self.assertEqual(career.type, 'career')

        self.assertEqual(season_advanced.total_splits, len(season_advanced.splits))
        self.assertEqual(season_advanced.group, 'hitting')
        self.assertEqual(season_advanced.type, 'seasonAdvanced')

        self.assertEqual(career_advanced.total_splits, len(career_advanced.splits))
        self.assertEqual(career_advanced.group, 'hitting')
        self.assertEqual(career_advanced.type, 'careerAdvanced')

    def test_hitting_hotColdZones_for_player(self, m):
        """get_player_game_stats should return a dict with stats"""
        m.get('https://statsapi.mlb.com/api/v1/people/665742/stats?stats=hotColdZones&group=hitting', json=self.mock_hotcoldzone,
        status_code=200)
        self.stats = ['hotColdZones']
        self.groups = ['hitting']
        stats = self.mlb.get_player_stats(self.player.id, stats=self.stats, groups=self.groups)

        # game_stats should not be None
        self.assertIsNotNone(stats)
        
        # game_stats should not be empty dic
        self.assertNotEqual(stats, {})

        self.assertTrue(stats['stats']['hotColdZones'])

        # hotcoldzone should return 5 splits
        hotcoldzone = stats['stats']['hotColdZones']
        self.assertEqual(len(hotcoldzone.splits), 5)
        self.assertEqual(hotcoldzone.total_splits, len(hotcoldzone.splits))

        # hot cold zone should have 13 zones for each zone type
        for split in hotcoldzone.splits:
            self.assertTrue(split.stat.name)
            self.assertEqual(len(split.stat.zones), 13)

    def test_hitting_pitchLog_for_player(self, m):
        """get_player_game_stats should return a dict with stats"""
        m.get('https://statsapi.mlb.com/api/v1/people/665742/stats?stats=pitchLog&group=hitting', json=self.mock_hitting_pitchLog,
        status_code=200)
        self.stats = ['pitchLog']
        self.groups = ['hitting']
        stats = self.mlb.get_player_stats(self.player.id, stats=self.stats, groups=self.groups)

        # game_stats should not be None
        self.assertIsNotNone(stats)
        
        # game_stats should not be empty dic
        self.assertNotEqual(stats, {})

        # playLog key should be populated
        self.assertTrue('hitting' in stats)
        self.assertTrue(stats['hitting']['pitchLog'])

        # pitchLog should have 2 splits from mock
        pitchLogs = stats['hitting']['pitchLog']
        self.assertEqual(len(pitchLogs.splits), 6)
        self.assertEqual(pitchLogs.total_splits, len(pitchLogs.splits))

        for pitchLog in pitchLogs.splits:
            self.assertTrue(pitchLog.stat.details)
            self.assertTrue(pitchLog.stat.count)


    def test_hitting_playLog_for_player(self, m):
        """get_player_game_stats should return a dict with stats"""
        m.get('https://statsapi.mlb.com/api/v1/people/665742/stats?stats=playLog&group=hitting', json=self.mock_hitting_playLog,
        status_code=200)
        self.stats = ['playLog']
        self.groups = ['hitting']
        stats = self.mlb.get_player_stats(self.player.id, stats=self.stats, groups=self.groups)

        # game_stats should not be None
        self.assertIsNotNone(stats)
        
        # game_stats should not be empty dic
        self.assertNotEqual(stats, {})

        # playLog key should be populated
        self.assertTrue('hitting' in stats)
        self.assertTrue(stats['hitting']['playLog'])

        # pitchLog items should have 2 splits
        pitchLogs = stats['hitting']['playLog']
        self.assertEqual(len(pitchLogs.splits), 2)
        self.assertEqual(pitchLogs.total_splits, len(pitchLogs.splits))

        for pitchLog in pitchLogs.splits:
            self.assertTrue(pitchLog.stat)

    def test_hitting_sprayChart_for_player(self, m):
        """get_player_game_stats should return a dict with stats"""
        m.get('https://statsapi.mlb.com/api/v1/people/665742/stats?stats=sprayChart&group=hitting', json=self.mock_sprayCharts,
        status_code=200)
        self.stats = ['sprayChart']
        self.groups = ['hitting']
        sprayChart = self.mlb.get_player_stats(self.player.id, stats=self.stats, groups=self.groups)

        # game_stats should not be None
        self.assertIsNotNone(sprayChart)
        
        # game_stats should not be empty dic
        self.assertNotEqual(sprayChart, {})

        self.assertTrue(sprayChart['stats']['sprayChart'])

        sprayChart = sprayChart['stats']['sprayChart']
        self.assertEqual(len(sprayChart.splits), 1)
        self.assertEqual(sprayChart.total_splits, len(sprayChart.splits))

        for pitchLog in sprayChart.splits:
            self.assertTrue(pitchLog.stat)