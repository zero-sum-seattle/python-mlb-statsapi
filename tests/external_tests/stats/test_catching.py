import unittest
import time

from mlbstatsapi.mlb_api import Mlb


class TestCatchingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.al_team = 133
        cls.shoei_ohtani = 660271
        cls.catching_player = 663728
        cls.stats_200_blank = ('projected', 'projectedRos', 'standard', 'advanced', 'firstYearStats', 'lastYearStats',
        'vsOpponents', 'outsAboveAverage', 'tracking', 'availableStats', 'gameTypeStats', 'vsOpponents')
        cls.catching = 'catching'
        cls.stats_500 = ('careerStatSplits', 'metricLog', 'metricAverages', 'statSplits', 'statSplitsAdvanced')
        # these stat groups require a team with recent playoff appearences 
        cls.stats_playoffs = ('byMonthPlayoffs', 'byDayOfWeekPlayoffs', 'homeAndAwayPlayoffs', 'winLossPlayoffs')
        # These stat groups require addition params passed like playerid or teamid
        cls.stats_require_params = ('vsTeam', 'vsTeam5Y', 'vsTeamTotal', 'vsPlayer', 'vsPlayerTotal', 'vsPlayer5Y')
        # These stat types should all return a stat split object for hitting and pitching stat groups
        cls.catching = (
                    "yearByYear", "yearByYearPlayoffs", "season", "career", "careerRegularSeason",
                    "careerPlayoffs", "gameLog", "lastXGames", "byDateRange", "byDateRangeAdvanced",
                    "byMonth", "byDayOfWeek", "homeAndAway", "winLoss", "atGameStart"
                    )
                    
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_catching_stat_attributes_player(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['season', 'career']
        self.group = ['catching']
        # let's get some stats
        stats = self.mlb.get_player_stats(self.catching_player, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('catching' in stats)
        self.assertFalse('hitting' in stats)
        self.assertEqual(len(stats['catching']), 2)

        # check for split objects
        self.assertTrue(stats['catching']['season'])
        self.assertTrue(stats['catching']['career'])

        season = stats['catching']['season']
        career = stats['catching']['career']

        self.assertEqual(season.totalsplits, len(season.splits))
        self.assertEqual(season.group, 'catching')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.totalsplits, len(career.splits))
        self.assertEqual(career.group, 'catching')
        self.assertEqual(career.type, 'career')

    def test_catching_stat_attributes_team(self):
        """mlb get stats should return pitching stats"""
        self.stats = ['season', 'career']
        self.group = ['catching']
        # let's get some stats
        stats = self.mlb.get_team_stats(self.al_team, stats=self.stats, groups=self.group)

        # check for empty dict
        self.assertNotEqual(stats, {})

        # the end point should give us 2 hitting
        self.assertTrue('catching' in stats)
        self.assertFalse('hitting' in stats)
        self.assertEqual(len(stats['catching']), 2)

        # check for split objects
        self.assertTrue(stats['catching']['season'])
        self.assertTrue(stats['catching']['career'])

        season = stats['catching']['season']
        career = stats['catching']['career']

        self.assertEqual(season.totalsplits, len(season.splits))
        self.assertEqual(season.group, 'catching')
        self.assertEqual(season.type, 'season')

        self.assertEqual(career.totalsplits, len(career.splits))
        self.assertEqual(career.group, 'catching')
        self.assertEqual(career.type, 'career')
