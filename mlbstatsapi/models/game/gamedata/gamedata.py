from typing import Union, List, Dict, Any
from dataclasses import dataclass
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.people import Person

from mlbstatsapi.models.game.gamedata.gameteams import GameTeams
from mlbstatsapi.models.game.gamedata.gamevenue import GameVenue
from mlbstatsapi.models.game.gamedata.gamereview import GameReview

@dataclass
class GameDataGame:
    pk: int
    type: str
    doubleHeader: str
    id: str
    gamedayType: str
    tiebreaker: str
    gameNumber: int
    calendarEventID: str
    season: str
    seasonDisplay: str

@dataclass
class GameDatetime:
    dateTime: str
    originalDate: str
    officialDate: str
    dayNight: str
    time: str
    ampm: str

@dataclass
class GameStatus:
    abstractGameState: str
    codedGameState: str
    detailedState: str
    statusCode: str
    startTimeTBD: bool
    abstractGameCode: str

@dataclass
class GameWeather:
    condition: str
    temp: str
    wind: str

@dataclass
class GameInfo:
    attendance: int
    firstPitch: str
    gameDurationMinutes: int
    delayDurationMinutes: int

@dataclass
class GameFlags:
    noHitter:               bool
    perfectGame:            bool
    awayTeamNoHitter:       bool
    awayTeamPerfectGame:    bool
    homeTeamNoHitter:       bool
    homeTeamPerfectGame:    bool

@dataclass
class GameProbablePitchers:
    away: Union[Person, Dict]
    home: Union[Person, Dict]

    def __post_init__(self):
        self.away = Person(**self.away)
        self.home = Person(**self.home)

@dataclass
class GameData:
    game:               Union[GameDataGame, Dict[str, Any]]
    datetime:           Union[GameDatetime, Dict[str, Any]]
    status:             Union[GameStatus, Dict[str, Any]]
    teams:              Union[GameTeams, Dict[str, Any]]
    players:            Union[List[Person], Dict]
    venue:              Union[GameVenue, Dict[str, Any]]
    officialVenue:      Union[Venue, Dict[str, Any]]
    weather:            Union[GameWeather, Dict[str, Any]]
    gameInfo:           Union[GameInfo, Dict[str, Any]]
    review:             Union[GameReview, Dict[str, Any]]
    flags:              Union[GameFlags, Dict[str, Any]]
    alerts:             List
    probablePitchers:   Union[GameProbablePitchers, Dict]
    officialScorer:     Union[Person, Dict[str, Any]]
    primaryDatacaster:  Union[Person, Dict[str, Any]]

    def __post_init__(self):
        self.game = GameDataGame(**self.game)
        self.datetime = GameDatetime(**self.datetime)
        self.status = GameStatus(**self.status)
        self.teams = GameTeams(**self.teams)
        # self.players
        # tempPlayers = self.players
        self.players = [Person(**(self.players[key])) for key in self.players]
        self.venue = GameVenue(**self.venue)
        self.officialVenue = Venue(**self.officialVenue)
        self.weather = GameWeather(**self.weather)
        self.gameInfo = GameInfo(**self.gameInfo)
        self.review = GameReview(**self.review)
        self.flags = GameFlags(**self.flags)
        self.probablePitchers = GameProbablePitchers(**self.probablePitchers)
        self.officialScorer = Person(**self.officialScorer)
        self.primaryDatacaster = Person(**self.primaryDatacaster)
