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

        season = stats['pitching']['season']
        career = stats['pitching']['career']
        season_advanced = stats['pitching']['seasonadvanced']
        career_advanced = stats['pitching']['careeradvanced']

        self.assertEqual(season.totalsplits, len(season.splits))
        self.assertEqual(season.group, 'pitching')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.totalsplits, len(career.splits))
        self.assertEqual(career.group, 'pitching')
        self.assertEqual(career.type, 'career')

        self.assertEqual(season_advanced.totalsplits, len(season_advanced.splits))
        self.assertEqual(season_advanced.group, 'pitching')
        self.assertEqual(season_advanced.type, 'seasonAdvanced')

        self.assertEqual(career_advanced.totalsplits, len(career_advanced.splits))
        self.assertEqual(career_advanced.group, 'pitching')
        self.assertEqual(career_advanced.type, 'careerAdvanced')

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

        season = stats['pitching']['season']
        career = stats['pitching']['career']
        season_advanced = stats['pitching']['seasonadvanced']
        career_advanced = stats['pitching']['careeradvanced']

        self.assertEqual(season.totalsplits, len(season.splits))
        self.assertEqual(season.group, 'pitching')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.totalsplits, len(career.splits))
        self.assertEqual(career.group, 'pitching')
        self.assertEqual(career.type, 'career')

        self.assertEqual(season_advanced.totalsplits, len(season_advanced.splits))
        self.assertEqual(season_advanced.group, 'pitching')
        self.assertEqual(season_advanced.type, 'seasonAdvanced')

        self.assertEqual(career_advanced.totalsplits, len(career_advanced.splits))
        self.assertEqual(career_advanced.group, 'pitching')
        self.assertEqual(career_advanced.type, 'careerAdvanced')

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

        hotcoldzone = stats['stats']['hotcoldzones']

        # check for split objects
        self.assertTrue(stats['stats']['hotcoldzones'])

        # hotcoldzone should return 5 splits
        hotcoldzone = stats['stats']['hotcoldzones']
        self.assertEqual(len(hotcoldzone.splits), 5)
        self.assertEqual(hotcoldzone.totalsplits, len(hotcoldzone.splits))

        # hot cold zone should have 13 zones for each zone type
        for split in hotcoldzone.splits:
            self.assertTrue(split.stat.name)
            self.assertEqual(len(split.stat.zones), 13)

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

        # pitchlog should have 2 splits from mock
        pitchlogs = stats['pitching']['pitchlog']
        self.assertEqual(len(pitchlogs.splits), 2)
        self.assertEqual(pitchlogs.totalsplits, len(pitchlogs.splits))

        for pitchlog in pitchlogs.splits:
            self.assertTrue(pitchlog.stat.details)
            self.assertTrue(pitchlog.stat.count)

    
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

        # pitchlog items should have 2 splits
        pitchlogs = stats['pitching']['playlog']
        self.assertEqual(len(pitchlogs.splits), 2)
        self.assertEqual(pitchlogs.totalsplits, len(pitchlogs.splits))

        for pitchlog in pitchlogs.splits:
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


        spraychart = spraychart['stats']['spraychart']
        self.assertEqual(len(spraychart.splits), 1)
        self.assertEqual(spraychart.totalsplits, len(spraychart.splits))

        for pitchlog in spraychart.splits:
            self.assertTrue(pitchlog.stat)