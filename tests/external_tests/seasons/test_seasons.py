import unittest
from mlbstatsapi.models.seasons import Season
from mlbstatsapi import Mlb


class TestSeasons(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
    
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_get_season(self):
        """get_season should return a season"""
        season = self.mlb.get_season(season_id="2021")
        self.assertIsInstance(season, Season)

    def test_get_season_leagueid(self):
        """get_season should return a season for a sport"""
        season = self.mlb.get_season(season_id="2022", sport_id=1, leagueId=11)
        self.assertIsInstance(season, Season)

    def test_get_seasons_divisionId(self):
        """get_seasons should return a season for a sport"""
        seasons = self.mlb.get_seasons(sport_id=1, divisionId=11)
        # test if seasons is a list
        self.assertIsInstance(seasons, list)
        self.assertNotEqual(seasons, [])

        # test if list contains seasons
        season = seasons[0]
        self.assertIsInstance(season, Season)

    def test_get_seasons_gametypes(self):
        """get_season should return a Season object"""
        seasons = self.mlb.get_seasons(sport_id=1, withGameTypeDates=True)
        # test if seasons is a list
        self.assertIsInstance(seasons, list)
        self.assertNotEqual(seasons, [])

        # test if list contains seasons
        season = seasons[0]
        self.assertIsInstance(season, Season)

    def test_get_seasons_sportid(self):
        """get_seasons should return a list of all seasons"""
        seasons = self.mlb.get_seasons(sport_id=1)

        # test if seasons is a list
        self.assertIsInstance(seasons, list)
        self.assertNotEqual(seasons, [])

        # test if list contains seasons
        season = seasons[0]
        self.assertIsInstance(season, Season)

    def test_get_seasons_leagueId(self):
        """get_seasons should return a list of all seasons"""
        seasons = self.mlb.get_seasons(sport_id=1, leagueId=104)

        # test if seasons is a list
        self.assertIsInstance(seasons, list)
        self.assertNotEqual(seasons, [])

        # test if list contains seasons
        season = seasons[0]
        self.assertIsInstance(season, Season)
