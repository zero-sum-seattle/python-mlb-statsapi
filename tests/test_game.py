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

    def test_game_gameData_players_attributes(self):
        gameData_players = self.game.gameData.players
        self.assertIsInstance(gameData_players, List)

        for player in gameData_players:
            self.assertIsInstance(player, Person)

    def test_game_gameData_venue_attributes(self):
        gameData_venue = self.game.gameData.venue
        self.assertIsInstance(gameData_venue, GameGameDataVenue)
        self.assertTrue(hasattr(gameData_venue, "id"))
        self.assertTrue(hasattr(gameData_venue, "name"))
        self.assertTrue(hasattr(gameData_venue, "link"))
        self.assertTrue(hasattr(gameData_venue, "location"))
        self.assertTrue(hasattr(gameData_venue, "timeZone"))
        self.assertTrue(hasattr(gameData_venue, "fieldInfo"))
        self.assertTrue(hasattr(gameData_venue, "active"))

    def test_game_gameData_venue_fieldInfo_attributes(self):
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

    def test_game_gameData_venue_timeZone_attributes(self):
        venue_timeZone = self.game.gameData.venue.timeZone
        self.assertIsInstance(venue_timeZone, GameGameDataVenueTimeZone)
        self.assertTrue(hasattr(venue_timeZone, "id"))
        self.assertTrue(hasattr(venue_timeZone, "offset"))
        self.assertTrue(hasattr(venue_timeZone, "tz"))

    def test_game_gameData_venue_location_attributes(self):
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

    def test_game_gameData_venue_location_coordinates_attributes(self):
        location_coordinates = self.game.gameData.venue.location.defaultCoordinates
        self.assertIsInstance(location_coordinates, GameGameDataVenueLocationCoordinates)
        self.assertTrue(hasattr(location_coordinates, "latitude"))
        self.assertTrue(hasattr(location_coordinates, "longitude"))

    def test_game_gameData_weather_attributes(self):
        gameData_weather = self.game.gameData.weather
        self.assertIsInstance(gameData_weather, GameGameDataWeather)
        self.assertTrue(hasattr(gameData_weather, "condition"))
        self.assertTrue(hasattr(gameData_weather, "temp"))
        self.assertTrue(hasattr(gameData_weather, "wind"))

    def test_game_gameData_gameInfo_attributes(self):
        gameData_gameInfo = self.game.gameData.gameInfo
        self.assertIsInstance(gameData_gameInfo, GameGameDataGameInfo)
        self.assertTrue(hasattr(gameData_gameInfo, "attendance"))
        self.assertTrue(hasattr(gameData_gameInfo, "firstPitch"))
        self.assertTrue(hasattr(gameData_gameInfo, "gameDurationMinutes"))
        self.assertTrue(hasattr(gameData_gameInfo, "delayDurationMinutes"))

    def test_game_gameData_review_attributes(self):
        gameData_review = self.game.gameData.review
        self.assertIsInstance(gameData_review, GameGameDataReview)
        self.assertTrue(hasattr(gameData_review, "hasChallenges"))
        self.assertTrue(hasattr(gameData_review, "away"))
        self.assertTrue(hasattr(gameData_review, "home"))

    def test_game_gameData_review_team_attributes(self):
        review_home = self.game.gameData.review.home
        review_away = self.game.gameData.review.away
        self.assertIsInstance(review_home, GameGameDataReviewTeam)
        self.assertIsInstance(review_away, GameGameDataReviewTeam)
        self.assertTrue(hasattr(review_home, "used"))
        self.assertTrue(hasattr(review_away, "used"))
        self.assertTrue(hasattr(review_home, "remaining"))
        self.assertTrue(hasattr(review_away, "remaining"))

    def test_game_gameData_flags_attributes(self):
        gameData_flags = self.game.gameData.flags
        self.assertIsInstance(gameData_flags, GameGameDataFlags)
        self.assertTrue(hasattr(gameData_flags, "noHitter"))
        self.assertTrue(hasattr(gameData_flags, "perfectGame"))
        self.assertTrue(hasattr(gameData_flags, "awayTeamNoHitter"))
        self.assertTrue(hasattr(gameData_flags, "awayTeamPerfectGame"))
        self.assertTrue(hasattr(gameData_flags, "homeTeamNoHitter"))
        self.assertTrue(hasattr(gameData_flags, "homeTeamPerfectGame"))

    def test_game_gameData_probablePitchers_attributes(self):
        gameData_probablePitchers = self.game.gameData.probablePitchers
        self.assertIsInstance(gameData_probablePitchers, GameGameDataProbablePitchers)
        self.assertTrue(hasattr(gameData_probablePitchers, "away"))
        self.assertTrue(hasattr(gameData_probablePitchers, "home"))
        self.assertIsInstance(gameData_probablePitchers.away, Person)
        self.assertIsInstance(gameData_probablePitchers.home, Person)



    def test_Game_LiveData_Plays_attributes(self):
        LiveData_plays = self.game.liveData.plays
        self.assertIsInstance(LiveData_plays, GameLiveDataPlays)
        self.assertTrue(hasattr(LiveData_plays, "allPlays"))
        self.assertTrue(hasattr(LiveData_plays, "currentPlay"))
        self.assertTrue(hasattr(LiveData_plays, "scoringPlays"))
        self.assertTrue(hasattr(LiveData_plays, "playsByInning"))
        self.assertIsInstance(LiveData_plays.currentPlay, GameLiveDataPlaysPlay)
        for play in LiveData_plays.allPlays:
            self.assertIsInstance(play, GameLiveDataPlaysPlay)

    def test_Game_LiveData_Plays_Play_attributes(self):
        LiveData_Play = self.game.liveData.plays.currentPlay
        self.assertIsInstance(LiveData_Play, GameLiveDataPlaysPlay)
        self.assertTrue(hasattr(LiveData_Play, "result"))
        self.assertTrue(hasattr(LiveData_Play, "about"))
        self.assertTrue(hasattr(LiveData_Play, "count"))
        self.assertTrue(hasattr(LiveData_Play, "matchup"))
        self.assertTrue(hasattr(LiveData_Play, "pitchIndex"))
        self.assertTrue(hasattr(LiveData_Play, "actionIndex"))
        self.assertTrue(hasattr(LiveData_Play, "runnerIndex"))
        self.assertTrue(hasattr(LiveData_Play, "runners"))
        self.assertTrue(hasattr(LiveData_Play, "playEvents"))
        self.assertTrue(hasattr(LiveData_Play, "playEndTime"))
        self.assertTrue(hasattr(LiveData_Play, "atBatIndex"))

    def test_Game_LiveData_Plays_Play_PlayEvents_attributes(self):
        Play_PlayEvents = self.game.liveData.plays.currentPlay.playEvents
        for play_event in Play_PlayEvents:
            self.assertIsInstance(play_event, GameLiveDataPlaysPlayPlayEvents)
            self.assertTrue(hasattr(play_event, "details"))
            self.assertTrue(hasattr(play_event, "count"))
            self.assertTrue(hasattr(play_event, "index"))
            self.assertTrue(hasattr(play_event, "startTime"))
            self.assertTrue(hasattr(play_event, "endTime"))
            self.assertTrue(hasattr(play_event, "isPitch"))
            self.assertTrue(hasattr(play_event, "type"))
            self.assertTrue(hasattr(play_event, "player"))
            self.assertIsInstance(play_event.count, GameLiveDataPlaysPlayCount)
            if play_event.player:
                self.assertIsInstance(play_event.player, Person)

    def test_Game_LiveData_Plays_Play_PlayEvents_Details_attributes(self):
        Play_PlayEvents = self.game.liveData.plays.currentPlay.playEvents
        for play_event in Play_PlayEvents:
            event_details = play_event.details
            self.assertIsInstance(event_details, GameLiveDataPlaysPlayPlayEventsDetails)
            self.assertTrue(hasattr(event_details, "description"))
            self.assertTrue(hasattr(event_details, "event"))
            self.assertTrue(hasattr(event_details, "eventType"))
            self.assertTrue(hasattr(event_details, "awayScore"))
            self.assertTrue(hasattr(event_details, "homeScore"))
            self.assertTrue(hasattr(event_details, "isScoringPlay"))
            self.assertTrue(hasattr(event_details, "hasReview"))

    def test_Game_LiveData_Plays_Play_Runners_attributes(self):
        play_runners = self.game.liveData.plays.currentPlay.runners
        for runner in play_runners:
            self.assertIsInstance(runner, GameLiveDataPlaysPlayRunners)
            self.assertTrue(hasattr(runner, "movement"))
            self.assertTrue(hasattr(runner, "details"))
            self.assertTrue(hasattr(runner, "credits"))

    def test_Game_LiveData_Plays_Play_Runners_Credits_attributes(self):
        play_runners = self.game.liveData.plays.currentPlay.runners
        for runner in play_runners:
            for credit in runner.credits:
                self.assertIsInstance(credit, GameLiveDataPlaysPlayRunnersCredits)
                self.assertTrue(hasattr(credit, "player"))
                self.assertTrue(hasattr(credit, "position"))
                self.assertTrue(hasattr(credit, "credit"))
                self.assertIsInstance(credit.player, Person)

    def test_Game_LiveData_Plays_Play_Runners_Credits_Position_attributes(self):
        play_runners = self.game.liveData.plays.currentPlay.runners
        for runner in play_runners:
            for credit in runner.credits:
                position = credit.position
                self.assertIsInstance(position, GameLiveDataPlaysPlayRunnersCreditsPosition)
                self.assertTrue(hasattr(position, "code"))
                self.assertTrue(hasattr(position, "name"))
                self.assertTrue(hasattr(position, "type"))
                self.assertTrue(hasattr(position, "abbreviation"))

    def test_Game_LiveData_Plays_Play_Runners_Details_attributes(self):
        play_runners = self.game.liveData.plays.currentPlay.runners
        for runner in play_runners:
            details = runner.details
            self.assertIsInstance(details, GameLiveDataPlaysPlayRunnersDetails)
            self.assertTrue(hasattr(details, "event"))
            self.assertTrue(hasattr(details, "eventType"))
            self.assertTrue(hasattr(details, "movementReason"))
            self.assertTrue(hasattr(details, "runner"))
            self.assertTrue(hasattr(details, "responsiblePitcher"))
            self.assertTrue(hasattr(details, "isScoringEvent"))
            self.assertTrue(hasattr(details, "rbi"))
            self.assertTrue(hasattr(details, "earned"))
            self.assertTrue(hasattr(details, "teamUnearned"))
            self.assertTrue(hasattr(details, "playIndex"))
            self.assertIsInstance(details.runner, Person)
            if details.responsiblePitcher:
                self.assertIsInstance(details.responsiblePitcher, Person)

    def test_Game_LiveData_Plays_Play_Runners_Movement_attributes(self):
        play_runners = self.game.liveData.plays.currentPlay.runners
        for runner in play_runners:
            movement = runner.movement
            self.assertIsInstance(movement, GameLiveDataPlaysPlayRunnersMovement)
            self.assertTrue(hasattr(movement, "originBase"))
            self.assertTrue(hasattr(movement, "start"))
            self.assertTrue(hasattr(movement, "end"))
            self.assertTrue(hasattr(movement, "outBase"))
            self.assertTrue(hasattr(movement, "isOut"))
            self.assertTrue(hasattr(movement, "outNumber"))

    def test_Game_LiveData_Plays_Play_Matchup_attributes(self):
        play_matchup = self.game.liveData.plays.currentPlay.matchup
        self.assertIsInstance(play_matchup, GameLiveDataPlaysPlayMatchup)
        self.assertTrue(hasattr(play_matchup, "batter"))
        self.assertTrue(hasattr(play_matchup, "batSide"))
        self.assertTrue(hasattr(play_matchup, "pitcher"))
        self.assertTrue(hasattr(play_matchup, "pitchHand"))
        self.assertTrue(hasattr(play_matchup, "batterHotColdZones"))
        self.assertTrue(hasattr(play_matchup, "pitcherHotColdZones"))
        self.assertTrue(hasattr(play_matchup, "splits"))
        self.assertIsInstance(play_matchup.batter, Person)
        self.assertIsInstance(play_matchup.pitcher, Person)

    def test_Game_LiveData_Plays_Play_MatchupSplits_attributes(self):
        matchup_splits = self.game.liveData.plays.currentPlay.matchup.splits
        self.assertIsInstance(matchup_splits, GameLiveDataPlaysPlayMatchupSplits)
        self.assertTrue(hasattr(matchup_splits, "batter"))
        self.assertTrue(hasattr(matchup_splits, "pitcher"))
        self.assertTrue(hasattr(matchup_splits, "menOnBase"))

    def test_Game_LiveData_Plays_Play_Matchup_Side_attributes(self):
        matchup_sides_batSide = self.game.liveData.plays.currentPlay.matchup.batSide
        matchup_sides_pitchHand = self.game.liveData.plays.currentPlay.matchup.pitchHand
        self.assertIsInstance(matchup_sides_batSide, GameLiveDataPlaysPlayMatchupSide)
        self.assertIsInstance(matchup_sides_pitchHand, GameLiveDataPlaysPlayMatchupSide)
        self.assertTrue(hasattr(matchup_sides_batSide, "code"))
        self.assertTrue(hasattr(matchup_sides_pitchHand, "code"))
        self.assertTrue(hasattr(matchup_sides_batSide, "description"))
        self.assertTrue(hasattr(matchup_sides_pitchHand, "description"))

    def test_Game_LiveData_Plays_Play_Count_attributes(self):
        playEvents = self.game.liveData.plays.currentPlay.playEvents
        play = self.game.liveData.plays.currentPlay
        self.assertIsInstance(play.count, GameLiveDataPlaysPlayCount)
        self.assertTrue(hasattr(play.count, "balls"))
        self.assertTrue(hasattr(play.count, "strikes"))
        self.assertTrue(hasattr(play.count, "outs"))
        for playEvent in playEvents:
            self.assertIsInstance(playEvent.count, GameLiveDataPlaysPlayCount)
            self.assertTrue(hasattr(playEvent.count, "balls"))
            self.assertTrue(hasattr(playEvent.count, "strikes"))
            self.assertTrue(hasattr(playEvent.count, "outs"))

    def test_Game_LiveData_Plays_Play_About_attributes(self):
        play_about = self.game.liveData.plays.currentPlay.about
        self.assertIsInstance(play_about, GameLiveDataPlaysPlayAbout)
        self.assertTrue(hasattr(play_about, "atBatIndex"))
        self.assertTrue(hasattr(play_about, "halfInning"))
        self.assertTrue(hasattr(play_about, "isTopInning"))
        self.assertTrue(hasattr(play_about, "inning"))
        self.assertTrue(hasattr(play_about, "startTime"))
        self.assertTrue(hasattr(play_about, "endTime"))
        self.assertTrue(hasattr(play_about, "isComplete"))
        self.assertTrue(hasattr(play_about, "isScoringPlay"))
        self.assertTrue(hasattr(play_about, "hasReview"))
        self.assertTrue(hasattr(play_about, "hasOut"))
        self.assertTrue(hasattr(play_about, "captivatingIndex"))

    def test_Game_LiveData_Plays_Play_Result_attributes(self):
        play_result = self.game.liveData.plays.currentPlay.result
        self.assertIsInstance(play_result, GameLiveDataPlaysPlayResult)
        self.assertTrue(hasattr(play_result, "type"))
        self.assertTrue(hasattr(play_result, "event"))
        self.assertTrue(hasattr(play_result, "eventType"))
        self.assertTrue(hasattr(play_result, "description"))
        self.assertTrue(hasattr(play_result, "rbi"))
        self.assertTrue(hasattr(play_result, "awayScore"))
        self.assertTrue(hasattr(play_result, "homeScore"))

    def test_Game_LiveData_Plays_Play_ByInning_attributes(self):
        Play_ByInning = self.game.liveData.plays.playsByInning
        for inning in Play_ByInning:
            self.assertIsInstance(inning, GameLiveDataPlaysPlayByInning)
            self.assertTrue(hasattr(inning, "startIndex"))
            self.assertTrue(hasattr(inning, "endIndex"))
            self.assertTrue(hasattr(inning, "top"))
            self.assertTrue(hasattr(inning, "bottom"))
            self.assertTrue(hasattr(inning, "hits"))

    def test_Game_LiveData_Plays_Play_ByInning_Hits_attributes(self):
        Play_ByInning = self.game.liveData.plays.playsByInning
        for inning in Play_ByInning:
            inning_hits = inning.hits
            self.assertIsInstance(inning_hits, GameLiveDataPlaysPlayByInningHits)
            self.assertTrue(hasattr(inning_hits, "home"))
            self.assertTrue(hasattr(inning_hits, "away"))

    def test_Game_LiveData_Plays_Play_ByInning_HitsByTeam_attributes(self):
        Play_ByInning = self.game.liveData.plays.playsByInning
        for inning in Play_ByInning:
            inning_hits_home = inning.hits.home
            inning_hits_away = inning.hits.away
            for home_hit in inning_hits_home:
                self.assertIsInstance(home_hit, GameLiveDataPlaysPlayByInningHitsByTeam)
                self.assertTrue(hasattr(home_hit, "team"))
                self.assertTrue(hasattr(home_hit, "inning"))
                self.assertTrue(hasattr(home_hit, "pitcher"))
                self.assertTrue(hasattr(home_hit, "batter"))
                self.assertTrue(hasattr(home_hit, "coordinates"))
                self.assertTrue(hasattr(home_hit, "type"))
                self.assertTrue(hasattr(home_hit, "description"))
                self.assertIsInstance(home_hit.team, Team)
                self.assertIsInstance(home_hit.pitcher, Person)
                self.assertIsInstance(home_hit.batter, Person)
            for away_hit in inning_hits_away:
                self.assertIsInstance(away_hit, GameLiveDataPlaysPlayByInningHitsByTeam)
                self.assertTrue(hasattr(away_hit, "team"))
                self.assertTrue(hasattr(away_hit, "inning"))
                self.assertTrue(hasattr(away_hit, "pitcher"))
                self.assertTrue(hasattr(away_hit, "batter"))
                self.assertTrue(hasattr(away_hit, "coordinates"))
                self.assertTrue(hasattr(away_hit, "type"))
                self.assertTrue(hasattr(away_hit, "description"))
                self.assertIsInstance(away_hit.team, Team)
                self.assertIsInstance(away_hit.pitcher, Person)
                self.assertIsInstance(away_hit.batter, Person)

    def test_Game_LiveData_Plays_Play_ByInning_HitsByTeam_HitCoordinates_attributes(self):
        Play_ByInning = self.game.liveData.plays.playsByInning
        for inning in Play_ByInning:
            inning_hits_home = inning.hits.home
            inning_hits_away = inning.hits.away
            for home_hit in inning_hits_home:
                hit_coord = home_hit.coordinates
                self.assertIsInstance(hit_coord, GameLiveDataPlaysPlayByInningHitsByTeamHitCoordinates)
                self.assertTrue(hasattr(hit_coord, "x"))
                self.assertTrue(hasattr(hit_coord, "y"))
            for away_hit in inning_hits_away:
                hit_coord = away_hit.coordinates
                self.assertIsInstance(hit_coord, GameLiveDataPlaysPlayByInningHitsByTeamHitCoordinates)
                self.assertTrue(hasattr(hit_coord, "x"))
                self.assertTrue(hasattr(hit_coord, "y"))





    # GameLiveDataLinescore
    def test_Game_LiveData_Linescore(self):
        linescore = self.game.liveData.linescore
        self.assertIsInstance(linescore, GameLiveDataLinescore)
        self.assertTrue(hasattr(linescore, "currentInning"))
        self.assertTrue(hasattr(linescore, "currentInningOrdinal"))
        self.assertTrue(hasattr(linescore, "inningState"))
        self.assertTrue(hasattr(linescore, "inningHalf"))
        self.assertTrue(hasattr(linescore, "isTopInning"))
        self.assertTrue(hasattr(linescore, "scheduledInnings"))
        self.assertTrue(hasattr(linescore, "innings"))
        self.assertTrue(hasattr(linescore, "teams"))
        self.assertTrue(hasattr(linescore, "defense"))
        self.assertTrue(hasattr(linescore, "offense"))
        self.assertTrue(hasattr(linescore, "balls"))
        self.assertTrue(hasattr(linescore, "strikes"))
        self.assertTrue(hasattr(linescore, "outs"))

    # GameLiveDataLinescoreInning():
    def test_Game_LiveData_Linescore_Innings(self):
        linescore_Innings = self.game.liveData.linescore.innings
        for inning in linescore_Innings:
            self.assertIsInstance(inning, GameLiveDataLinescoreInnings)
            self.assertTrue(hasattr(inning, "num"))
            self.assertTrue(hasattr(inning, "ordinalNum"))
            self.assertTrue(hasattr(inning, "home"))
            self.assertTrue(hasattr(inning, "away"))

    # class GameLiveDataLinescoreTeamScoreInfo():
    def test_Game_LiveData_Linescore_TeamScoreInfo(self):
        linescore_Innings = self.game.liveData.linescore.innings
        for inning in linescore_Innings:
            home = inning.home
            away = inning.away
            self.assertIsInstance(home, GameLiveDataLinescoreTeamScoreInfo)
            self.assertTrue(hasattr(home, "runs"))
            self.assertTrue(hasattr(home, "hits"))
            self.assertTrue(hasattr(home, "errors"))
            self.assertTrue(hasattr(home, "leftOnBase"))
            self.assertIsInstance(away, GameLiveDataLinescoreTeamScoreInfo)
            self.assertTrue(hasattr(away, "runs"))
            self.assertTrue(hasattr(away, "hits"))
            self.assertTrue(hasattr(away, "errors"))
            self.assertTrue(hasattr(away, "leftOnBase"))

    # class GameLiveDataLinescoreTeams():
    def test_Game_LiveData_Linescore_Teams(self):
        linescore_Innings = self.game.liveData.linescore.teams
        self.assertIsInstance(linescore_Innings, GameLiveDataLinescoreTeams)
        self.assertTrue(hasattr(linescore_Innings, "home"))
        self.assertTrue(hasattr(linescore_Innings, "away"))

    # class GameLiveDataLinescoreDefense():
    def test_Game_LiveData_Linescore_Defense(self):
        linescore_Defense = self.game.liveData.linescore.defense
        self.assertIsInstance(linescore_Defense, GameLiveDataLinescoreDefense)
        self.assertTrue(hasattr(linescore_Defense, "pitcher"))
        self.assertTrue(hasattr(linescore_Defense, "catcher"))
        self.assertTrue(hasattr(linescore_Defense, "first"))
        self.assertTrue(hasattr(linescore_Defense, "second"))
        self.assertTrue(hasattr(linescore_Defense, "third"))
        self.assertTrue(hasattr(linescore_Defense, "shortstop"))
        self.assertTrue(hasattr(linescore_Defense, "left"))
        self.assertTrue(hasattr(linescore_Defense, "center"))
        self.assertTrue(hasattr(linescore_Defense, "right"))
        self.assertTrue(hasattr(linescore_Defense, "batter"))
        self.assertTrue(hasattr(linescore_Defense, "onDeck"))
        self.assertTrue(hasattr(linescore_Defense, "inHole"))
        self.assertTrue(hasattr(linescore_Defense, "battingOrder"))
        self.assertTrue(hasattr(linescore_Defense, "team"))
        self.assertIsInstance(linescore_Defense.pitcher, Person)
        self.assertIsInstance(linescore_Defense.catcher, Person)
        self.assertIsInstance(linescore_Defense.first, Person)
        self.assertIsInstance(linescore_Defense.second, Person)
        self.assertIsInstance(linescore_Defense.third, Person)
        self.assertIsInstance(linescore_Defense.shortstop, Person)
        self.assertIsInstance(linescore_Defense.left, Person)
        self.assertIsInstance(linescore_Defense.center, Person)
        self.assertIsInstance(linescore_Defense.right, Person)
        self.assertIsInstance(linescore_Defense.batter, Person)
        self.assertIsInstance(linescore_Defense.onDeck, Person)
        self.assertIsInstance(linescore_Defense.inHole, Person)
        self.assertIsInstance(linescore_Defense.team, Team)

    # class GameLiveDataLinescoreOffense():
    def test_Game_LiveData_Linescore_Offense(self):
        linescore_Offense = self.game.liveData.linescore.offense
        self.assertIsInstance(linescore_Offense, GameLiveDataLinescoreOffense)
        self.assertTrue(hasattr(linescore_Offense, "batter"))
        self.assertTrue(hasattr(linescore_Offense, "onDeck"))
        self.assertTrue(hasattr(linescore_Offense, "inHole"))
        self.assertTrue(hasattr(linescore_Offense, "pitcher"))
        self.assertTrue(hasattr(linescore_Offense, "battingOrder"))
        self.assertTrue(hasattr(linescore_Offense, "team"))
        self.assertTrue(hasattr(linescore_Offense, "onBase"))
        self.assertIsInstance(linescore_Offense.batter, Person)
        self.assertIsInstance(linescore_Offense.onDeck, Person)
        self.assertIsInstance(linescore_Offense.inHole, Person)
        self.assertIsInstance(linescore_Offense.pitcher, Person)
        self.assertIsInstance(linescore_Offense.team, Team)

    # class GameLiveDataLinescoreOffenseOnBase():
    def test_Game_LiveData_Linescore_Offense_OnBase(self):
        Offense_Onbase = self.game.liveData.linescore.offense.onBase
        self.assertIsInstance(Offense_Onbase, GameLiveDataLinescoreOffenseOnBase)
        self.assertTrue(hasattr(Offense_Onbase, "first"))
        self.assertTrue(hasattr(Offense_Onbase, "second"))
        self.assertTrue(hasattr(Offense_Onbase, "third"))
        if Offense_Onbase.first:
            self.assertIsInstance(Offense_Onbase.first, Person)
        if Offense_Onbase.second:
            self.assertIsInstance(Offense_Onbase.second, Person)
        if Offense_Onbase.third:
            self.assertIsInstance(Offense_Onbase.third, Person)






    # def test_game_liveData_attributes(self);
