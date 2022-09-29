import unittest
from unittest.mock import Mock, patch
from mlbstatsapi.mlbapi import *
from mlbstatsapi.mlb import *


# Game with id of 662242 is used for this testing.
#
# 662242 info:
#           Cincinnati Reds (id:113) at Pittsburgh Pirates (id:134)
#           2022-09-26 at 6:35 pm
#           8766 attended with duration of 185 minutes and 38 minutes of delay
#           Pirates win 8 - 3


class TestGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.game = cls.mlb.get_game(662242)
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_game_instance_type_error(self):
         with self.assertRaises(TypeError):
            game = Game()

    def test_player_instance_position_arguments(self):
        game = self.game
        self.assertEqual(game.id, 662242)
        self.assertIsInstance(game, Game)

    # def test_game_base_class(self):
    #     game = Game(662242)
    #     self.assertIsInstance(game, MlbObject)

    # def test_player_base_class_attributes(self):
    #     game = Game(662242)
    #     self.assertTrue(hasattr(game, "_mlb_adapter"))

    def test_game_attributes(self):
        game = self.game
        self.assertTrue(hasattr(game, "metaData"))
        self.assertTrue(hasattr(game, "gameData"))
        self.assertTrue(hasattr(game, "liveData"))


    def test_game_metaData_attributes(self):
        metaData = self.game.metaData
        self.assertIsInstance(metaData, GameMetaData)
        self.assertTrue(hasattr(metaData, "wait"))
        self.assertTrue(hasattr(metaData, "timeStamp"))
        self.assertTrue(hasattr(metaData, "gameEvents"))
        self.assertTrue(hasattr(metaData, "logicalEvents"))

    def test_game_gameData_attributes(self):
        gameData = self.game.gameData
        self.assertIsInstance(gameData, GameGameData)
        self.assertTrue(hasattr(gameData, "game"))
        self.assertTrue(hasattr(gameData, "datetime"))
        self.assertTrue(hasattr(gameData, "status"))
        self.assertTrue(hasattr(gameData, "teams"))
        self.assertTrue(hasattr(gameData, "players"))
        self.assertTrue(hasattr(gameData, "venue"))
        self.assertTrue(hasattr(gameData, "officialVenue"))
        self.assertTrue(hasattr(gameData, "weather"))
        self.assertTrue(hasattr(gameData, "gameInfo"))
        self.assertTrue(hasattr(gameData, "review"))
        self.assertTrue(hasattr(gameData, "flags"))
        self.assertTrue(hasattr(gameData, "alerts"))
        self.assertTrue(hasattr(gameData, "probablePitchers"))

    def test_game_gameData_game_attributes(self):
        gameData_game = self.game.gameData.game
        self.assertIsInstance(gameData_game, GameGameDataGame)
        self.assertTrue(hasattr(gameData_game, "pk"))
        self.assertTrue(hasattr(gameData_game, "type"))
        self.assertTrue(hasattr(gameData_game, "doubleHeader"))
        self.assertTrue(hasattr(gameData_game, "id"))
        self.assertTrue(hasattr(gameData_game, "gamedayType"))
        self.assertTrue(hasattr(gameData_game, "tiebreaker"))
        self.assertTrue(hasattr(gameData_game, "gameNumber"))
        self.assertTrue(hasattr(gameData_game, "calendarEventID"))
        self.assertTrue(hasattr(gameData_game, "season"))
        self.assertTrue(hasattr(gameData_game, "seasonDisplay"))


    def test_game_gameData_datetime_attributes(self):
        gameData_datetime = self.game.gameData.datetime
        self.assertIsInstance(gameData_datetime, GameGameDataDatetime)
        self.assertTrue(hasattr(gameData_datetime, "dateTime"))
        self.assertTrue(hasattr(gameData_datetime, "originalDate"))
        self.assertTrue(hasattr(gameData_datetime, "officialDate"))
        self.assertTrue(hasattr(gameData_datetime, "dayNight"))
        self.assertTrue(hasattr(gameData_datetime, "time"))
        self.assertTrue(hasattr(gameData_datetime, "ampm"))

    def test_game_gameData_status_attributes(self):
        gameData_status = self.game.gameData.status
        self.assertIsInstance(gameData_status, GameGameDataStatus)
        self.assertTrue(hasattr(gameData_status, "abstractGameState"))
        self.assertTrue(hasattr(gameData_status, "codedGameState"))
        self.assertTrue(hasattr(gameData_status, "detailedState"))
        self.assertTrue(hasattr(gameData_status, "statusCode"))
        self.assertTrue(hasattr(gameData_status, "startTimeTBD"))
        self.assertTrue(hasattr(gameData_status, "abstractGameCode"))

    def test_game_gameData_teams_attributes(self):
        gameData_teams = self.game.gameData.teams
        self.assertIsInstance(gameData_teams, GameGameDataTeams)
        self.assertTrue(hasattr(gameData_teams, "away"))
        self.assertTrue(hasattr(gameData_teams, "home"))

    def test_game_gameData_teams_team_attributes(self):
        teams_away = self.game.gameData.teams.away
        teams_home = self.game.gameData.teams.home
        self.assertIsInstance(teams_away, GameGameDataTeamsTeam)
        self.assertIsInstance(teams_home, GameGameDataTeamsTeam)
        self.assertTrue(hasattr(teams_away, "springLeague"))
        self.assertTrue(hasattr(teams_home, "springLeague"))
        self.assertTrue(hasattr(teams_away, "allStarStatus"))
        self.assertTrue(hasattr(teams_home, "allStarStatus"))
        self.assertTrue(hasattr(teams_away, "id"))
        self.assertTrue(hasattr(teams_home, "id"))
        self.assertTrue(hasattr(teams_away, "name"))
        self.assertTrue(hasattr(teams_home, "name"))
        self.assertTrue(hasattr(teams_away, "link"))
        self.assertTrue(hasattr(teams_home, "link"))
        self.assertTrue(hasattr(teams_away, "season"))
        self.assertTrue(hasattr(teams_home, "season"))
        self.assertTrue(hasattr(teams_away, "venue"))
        self.assertTrue(hasattr(teams_home, "venue"))
        self.assertTrue(hasattr(teams_away, "springVenue"))
        self.assertTrue(hasattr(teams_home, "springVenue"))
        self.assertTrue(hasattr(teams_away, "teamCode"))
        self.assertTrue(hasattr(teams_home, "teamCode"))
        self.assertTrue(hasattr(teams_away, "fileCode"))
        self.assertTrue(hasattr(teams_home, "fileCode"))
        self.assertTrue(hasattr(teams_away, "abbreviation"))
        self.assertTrue(hasattr(teams_home, "abbreviation"))
        self.assertTrue(hasattr(teams_away, "teamName"))
        self.assertTrue(hasattr(teams_home, "teamName"))
        self.assertTrue(hasattr(teams_away, "locationName"))
        self.assertTrue(hasattr(teams_home, "locationName"))
        self.assertTrue(hasattr(teams_away, "firstYearOfPlay"))
        self.assertTrue(hasattr(teams_home, "firstYearOfPlay"))
        self.assertTrue(hasattr(teams_away, "league"))
        self.assertTrue(hasattr(teams_home, "league"))
        self.assertTrue(hasattr(teams_away, "division"))
        self.assertTrue(hasattr(teams_home, "division"))
        self.assertTrue(hasattr(teams_away, "sport"))
        self.assertTrue(hasattr(teams_home, "sport"))
        self.assertTrue(hasattr(teams_away, "shortName"))
        self.assertTrue(hasattr(teams_home, "shortName"))
        self.assertTrue(hasattr(teams_away, "record"))
        self.assertTrue(hasattr(teams_home, "record"))
        self.assertTrue(hasattr(teams_away, "franchiseName"))
        self.assertTrue(hasattr(teams_home, "franchiseName"))
        self.assertTrue(hasattr(teams_away, "clubName"))
        self.assertTrue(hasattr(teams_home, "clubName"))
        self.assertTrue(hasattr(teams_away, "active"))
        self.assertTrue(hasattr(teams_home, "active"))

    def test_game_gameData_teams_team_Record_attributes(self):
        away_Record = self.game.gameData.teams.away.record
        home_Record = self.game.gameData.teams.home.record
        self.assertIsInstance(away_Record, GameGameDataTeamsTeamRecord)
        self.assertIsInstance(home_Record, GameGameDataTeamsTeamRecord)
        self.assertTrue(hasattr(away_Record, "gamesPlayed"))
        self.assertTrue(hasattr(home_Record, "gamesPlayed"))
        self.assertTrue(hasattr(away_Record, "wildCardGamesBack"))
        self.assertTrue(hasattr(home_Record, "wildCardGamesBack"))
        self.assertTrue(hasattr(away_Record, "leagueGamesBack"))
        self.assertTrue(hasattr(home_Record, "leagueGamesBack"))
        self.assertTrue(hasattr(away_Record, "springLeagueGamesBack"))
        self.assertTrue(hasattr(home_Record, "springLeagueGamesBack"))
        self.assertTrue(hasattr(away_Record, "sportGamesBack"))
        self.assertTrue(hasattr(home_Record, "sportGamesBack"))
        self.assertTrue(hasattr(away_Record, "divisionGamesBack"))
        self.assertTrue(hasattr(home_Record, "divisionGamesBack"))
        self.assertTrue(hasattr(away_Record, "conferenceGamesBack"))
        self.assertTrue(hasattr(home_Record, "conferenceGamesBack"))
        self.assertTrue(hasattr(away_Record, "leagueRecord"))
        self.assertTrue(hasattr(home_Record, "leagueRecord"))
        self.assertTrue(hasattr(away_Record, "records"))
        self.assertTrue(hasattr(home_Record, "records"))
        self.assertTrue(hasattr(away_Record, "divisionLeader"))
        self.assertTrue(hasattr(home_Record, "divisionLeader"))
        self.assertTrue(hasattr(away_Record, "wins"))
        self.assertTrue(hasattr(home_Record, "wins"))
        self.assertTrue(hasattr(away_Record, "losses"))
        self.assertTrue(hasattr(home_Record, "losses"))
        self.assertTrue(hasattr(away_Record, "winningPercentage"))
        self.assertTrue(hasattr(home_Record, "winningPercentage"))




    def test_game_gameData_venue(self):
        gameData_venue = self.game.gameData.venue
        self.assertIsInstance(gameData_venue, GameGameDataVenue)
        self.assertTrue(hasattr(gameData_venue, "id"))
        self.assertTrue(hasattr(gameData_venue, "name"))
        self.assertTrue(hasattr(gameData_venue, "link"))
        self.assertTrue(hasattr(gameData_venue, "location"))
        self.assertTrue(hasattr(gameData_venue, "timeZone"))
        self.assertTrue(hasattr(gameData_venue, "fieldInfo"))
        self.assertTrue(hasattr(gameData_venue, "active"))

    def test_game_gameData_venue_fieldInfo(self):
        venue_fieldInfo = self.game.gameData.venue.fieldInfo
        self.assertIsInstance(venue_fieldInfo, GameGameDataVenueFieldInfo)
        self.assertTrue(hasattr(venue_fieldInfo, "capacity"))
        self.assertTrue(hasattr(venue_fieldInfo, "turfType"))
        self.assertTrue(hasattr(venue_fieldInfo, "roofType"))
        self.assertTrue(hasattr(venue_fieldInfo, "leftLine"))
        self.assertTrue(hasattr(venue_fieldInfo, "left"))
        self.assertTrue(hasattr(venue_fieldInfo, "leftCenter"))
        self.assertTrue(hasattr(venue_fieldInfo, "center"))
        self.assertTrue(hasattr(venue_fieldInfo, "rightCenter"))
        self.assertTrue(hasattr(venue_fieldInfo, "rightLine"))

    def test_game_gameData_venue_timeZone(self):
        venue_timeZone = self.game.gameData.venue.timeZone
        self.assertIsInstance(venue_timeZone, GameGameDataVenueTimeZone)
        self.assertTrue(hasattr(venue_timeZone, "id"))
        self.assertTrue(hasattr(venue_timeZone, "offset"))
        self.assertTrue(hasattr(venue_timeZone, "tz"))

    def test_game_gameData_venue_location(self):
        venue_location = self.game.gameData.venue.location
        self.assertIsInstance(venue_location, GameGameDataVenueLocation)
        self.assertTrue(hasattr(venue_location, "address1"))
        self.assertTrue(hasattr(venue_location, "city"))
        self.assertTrue(hasattr(venue_location, "state"))
        self.assertTrue(hasattr(venue_location, "stateAbbrev"))
        self.assertTrue(hasattr(venue_location, "postalCode"))
        self.assertTrue(hasattr(venue_location, "defaultCoordinates"))
        self.assertTrue(hasattr(venue_location, "country"))
        self.assertTrue(hasattr(venue_location, "phone"))

    def test_game_gameData_venue_location_coordinates(self):
        location_coordinates = self.game.gameData.venue.location.defaultCoordinates
        self.assertIsInstance(location_coordinates, GameGameDataVenueLocationCoordinates)
        self.assertTrue(hasattr(location_coordinates, "latitude"))
        self.assertTrue(hasattr(location_coordinates, "longitude"))




    def test_game_gameData_weather(self):
        gameData_weather = self.game.gameData.weather
        self.assertIsInstance(gameData_weather, GameGameDataWeather)
        self.assertTrue(hasattr(gameData_weather, "condition"))
        self.assertTrue(hasattr(gameData_weather, "temp"))
        self.assertTrue(hasattr(gameData_weather, "wind"))




    def test_game_gameData_gameInfo(self):
        gameData_gameInfo = self.game.gameData.gameInfo
        self.assertIsInstance(gameData_gameInfo, GameGameDataGameInfo)
        self.assertTrue(hasattr(gameData_gameInfo, "attendance"))
        self.assertTrue(hasattr(gameData_gameInfo, "firstPitch"))
        self.assertTrue(hasattr(gameData_gameInfo, "gameDurationMinutes"))
        self.assertTrue(hasattr(gameData_gameInfo, "delayDurationMinutes"))




    def test_game_gameData_review(self):
        gameData_review = self.game.gameData.review
        self.assertIsInstance(gameData_review, GameGameDataReview)
        self.assertTrue(hasattr(gameData_review, "hasChallenges"))
        self.assertTrue(hasattr(gameData_review, "away"))
        self.assertTrue(hasattr(gameData_review, "home"))

    def test_game_gameData_review_team(self):
        review_home = self.game.gameData.review.home
        review_away = self.game.gameData.review.away
        self.assertIsInstance(review_home, GameGameDataReviewTeam)
        self.assertIsInstance(review_away, GameGameDataReviewTeam)
        self.assertTrue(hasattr(review_home, "used"))
        self.assertTrue(hasattr(review_away, "used"))
        self.assertTrue(hasattr(review_home, "remaining"))
        self.assertTrue(hasattr(review_away, "remaining"))




    def test_game_gameData_flags(self):
        gameData_flags = self.game.gameData.flags
        self.assertIsInstance(gameData_flags, GameGameDataFlags)
        self.assertTrue(hasattr(gameData_flags, "noHitter"))
        self.assertTrue(hasattr(gameData_flags, "perfectGame"))
        self.assertTrue(hasattr(gameData_flags, "awayTeamNoHitter"))
        self.assertTrue(hasattr(gameData_flags, "awayTeamPerfectGame"))
        self.assertTrue(hasattr(gameData_flags, "homeTeamNoHitter"))
        self.assertTrue(hasattr(gameData_flags, "homeTeamPerfectGame"))


    def test_game_gameData_probablePitchers(self):
        gameData_probablePitchers = self.game.gameData.probablePitchers
        self.assertIsInstance(gameData_probablePitchers, GameGameDataProbablePitchers)
        self.assertTrue(hasattr(gameData_probablePitchers, "away"))
        self.assertTrue(hasattr(gameData_probablePitchers, "home"))
