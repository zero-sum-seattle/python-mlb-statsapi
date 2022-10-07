import unittest
from unittest.mock import Mock, patch
from mlbstatsapi.models.leagues import League, LeagueSeasonDateInfo
from mlbstatsapi import Mlb

class TestLeague(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.league = cls.mlb.get_league(103)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_league_instance_type_error(self):
        with self.assertRaises(TypeError):
            league = League()

    def test_league_instance_position_arguments(self):
        self.assertEqual(self.league.id, 103)
        self.assertEqual(self.league.link, "/api/v1/league/103")
        self.assertEqual(self.league.name, "American League")

    def test_league_has_attributes(self):
        self.assertIsInstance(self.league, League)
        self.assertTrue(hasattr(self.league, "id"))
        self.assertTrue(hasattr(self.league, "name"))
        self.assertTrue(hasattr(self.league, "link"))
        self.assertTrue(hasattr(self.league, "abbreviation"))
        self.assertTrue(hasattr(self.league, "nameShort"))
        self.assertTrue(hasattr(self.league, "seasonState"))
        self.assertTrue(hasattr(self.league, "hasWildCard"))
        self.assertTrue(hasattr(self.league, "hasSplitSeason"))
        self.assertTrue(hasattr(self.league, "numGames"))
        self.assertTrue(hasattr(self.league, "hasPlayoffPoints"))
        self.assertTrue(hasattr(self.league, "numTeams"))
        self.assertTrue(hasattr(self.league, "numWildcardTeams"))
        self.assertTrue(hasattr(self.league, "seasonDateInfo"))
        self.assertTrue(hasattr(self.league, "season"))
        self.assertTrue(hasattr(self.league, "orgCode"))
        self.assertTrue(hasattr(self.league, "conferencesInUse"))
        self.assertTrue(hasattr(self.league, "divisionsInUse"))
        self.assertTrue(hasattr(self.league, "sport"))
        self.assertTrue(hasattr(self.league, "sortOrder"))
        self.assertTrue(hasattr(self.league, "active"))

    def test_league_seasonDateInfo_has_attributes(self):
        seasonDateInfo = self.league.seasonDateInfo
        self.assertIsInstance(seasonDateInfo, LeagueSeasonDateInfo)
        self.assertTrue(hasattr(seasonDateInfo, "seasonId"))
        self.assertTrue(hasattr(seasonDateInfo, "preSeasonStartDate"))
        self.assertTrue(hasattr(seasonDateInfo, "preSeasonEndDate"))
        self.assertTrue(hasattr(seasonDateInfo, "seasonStartDate"))
        self.assertTrue(hasattr(seasonDateInfo, "springStartDate"))
        self.assertTrue(hasattr(seasonDateInfo, "springEndDate"))
        self.assertTrue(hasattr(seasonDateInfo, "regularSeasonStartDate"))
        self.assertTrue(hasattr(seasonDateInfo, "lastDate1stHalf"))
        self.assertTrue(hasattr(seasonDateInfo, "allStarDate"))
        self.assertTrue(hasattr(seasonDateInfo, "firstDate2ndHalf"))
        self.assertTrue(hasattr(seasonDateInfo, "regularSeasonEndDate"))
        self.assertTrue(hasattr(seasonDateInfo, "postSeasonStartDate"))
        self.assertTrue(hasattr(seasonDateInfo, "postSeasonEndDate"))
        self.assertTrue(hasattr(seasonDateInfo, "seasonEndDate"))
        self.assertTrue(hasattr(seasonDateInfo, "offseasonStartDate"))
        self.assertTrue(hasattr(seasonDateInfo, "offSeasonEndDate"))
        self.assertTrue(hasattr(seasonDateInfo, "seasonLevelGamedayType"))
        self.assertTrue(hasattr(seasonDateInfo, "gameLevelGamedayType"))
        self.assertTrue(hasattr(seasonDateInfo, "qualifierPlateAppearances"))
        self.assertTrue(hasattr(seasonDateInfo, "qualifierOutsPitched"))
