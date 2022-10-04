from typing import Union, List, Any
from dataclasses import dataclass
from mlbstatsapi.models.venue import Venue
from mlbstatsapi.models.person import Person

from gameData_modules.gameDataGame import GameDataGame
from gameData_modules.gameDatetime import GameDatetime
from gameData_modules.gameStatus import GameStatus
from gameData_modules.gameTeams import GameTeams
from gameData_modules.gameVenue import GameVenue
from gameData_modules.gameWeather import GameWeather
from gameData_modules.gameInfo import GameInfo
from gameData_modules.gameReview import GameReview
from gameData_modules.gameFlags import GameFlags
from gameData_modules.gameProbablePitchers import GameProbablePitchers


@dataclass
class GameData:
    game:               Union[GameDataGame, Dict[str, Any]]
    datetime:           Union[GameDatetime, Dict[str, Any]]
    status:             Union[GameStatus, Dict[str, Any]]
    teams:              Union[GameTeams, Dict[str, Any]]
    players:            Union[List[Person], Dict[str, Any]]
    venue:              Union[GameVenue, Dict[str, Any]]
    officialVenue:      Union[Venue, Dict[str, Any]]
    weather:            Union[GameWeather, Dict[str, Any]]
    gameInfo:           Union[GameInfo, Dict[str, Any]]
    review:             Union[GameReview, Dict[str, Any]]
    flags:              Union[GameFlags, Dict[str, Any]]
    alerts:             List
    probablePitchers:   Union[GameProbablePitchers, Dict[str, Any]]
    officialScorer:     Union[Person, Dict[str, Any]]
    primaryDatacaster:  Union[Person, Dict[str, Any]]

    def __post_init__(self):
        self.game = GameDataGame(**game)
        self.datetime = GameDatetime(**datetime)
        self.status = GameStatus(**status)
        self.teams = GameTeams(**teams)
        # self.players
        self.players = [Person(**value) for key, value in players.items()]
        self.venue = GameVenue(**venue)
        self.officialVenue = Venue(**officialVenue)
        self.weather = GameWeather(**weather)
        self.gameInfo = GameInfo(**gameInfo)
        self.review = GameReview(**review)
        self.flags = GameFlags(**flags)
        self.alerts = alerts
        self.probablePitchers = GameProbablePitchers(**probablePitchers)
        self.officialScorer = Person(**officialScorer)
        self.primaryDatacaster = Person(**primaryDatacaster)
