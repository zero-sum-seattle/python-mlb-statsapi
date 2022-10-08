from dataclasses import dataclass, field, fields
from typing import Dict, List, Union, Any
from .attributes import ScheduleDates

from mlbstatsapi.exceptions import TheMlbStatsApiException

from mlbstatsapi.models.game.gamedata import GameStatus

# https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2022-05-19

@dataclass
class Schedule:
    """
    A class to represent a Schedule.

    Attributes
    ----------
    copyright : str
        Copyright
    totalItems : int 
        Total items in schedule
    totalEvents : int
        Total events in schedule
    totalGames : int
        Total games in schedule
    totalGamesInProgress : int
        Total games in progress in schedule
    dates : ScheduleDates
        List of dates with games in schedule
    """
    copyright: str
    totalItems: int 
    totalEvents: int
    totalGames: int
    totalGamesInProgress: int
    dates: List[ScheduleDates] = field(default_factory=list)
    __statusTypes = []

    def __post_init__(self):
        self.dates = [ScheduleDates(**date) for date in self.dates if self.dates]

    def get_games_with_status(self, abstractGameState = None,
                                    codedGameState = None,
                                    detailedState = None,
                                    statusCode = None,
                                    reason = None,
                                    abstractGameCode = None):
        gameStatuses = {'abstractGameState':abstractGameState,
                        'codedGameState':codedGameState,
                        'detailedState':detailedState,
                        'statusCode':statusCode,
                        'reason':reason,
                        'abstractGameCode':abstractGameCode,}
        gameIds = []
        if all(gameStatuses[status] == None for status in gameStatuses):
            return gameIds 
        else:
            for date in self.dates:
                for game in date.games:
                    gameStatus = game.status                    
                    if all(gameStatuses[status] == getattr(gameStatus,f'{status}') for status in gameStatuses if gameStatuses[status]):
                        gameIds.append(game.gamePk)
            return gameIds

    def get_games_inProgress(self):
        return self.get_games_with_status(abstractGameState='Live')

    def get_games_finnished(self):
        return self.get_games_with_status(abstractGameState='Final')
