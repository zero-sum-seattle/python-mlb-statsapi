from typing import Union, List, Any
from dataclasses import dataclass
from mlbstatsapi.models.venue import Venue
from mlbstatsapi.models.person import Person

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

    @property
    def id(self):
        return self.pk

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
    away: Union[Person, Dict[str, Any]]
    home: Union[Person, Dict[str, Any]]

    def __post_init__(self):
        self.away = Person(**away)
        self.home = Person(**home)

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
