from typing import Optional, Union, List
from dataclasses import dataclass
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.people import Person

from .attributes import GameDataGame
from .attributes import GameDatetime
from .attributes import GameStatus
from .attributes import GameTeams
from .attributes import GameWeather
from .attributes import GameInfo
from .attributes import GameReview
from .attributes import GameFlags
from .attributes import GameProbablePitchers

@dataclass
class GameData:
    """
    A class to represent a games game data.

    Attributes
    ----------
    game : GameDataGame
        game information about this game
    datetime : GameDatetime
        Time and dates for this game
    status : GameStatus
        information on this game's status
    teams : GameTeams
        Our two teams for this game, home and away
    players : List[Person]
        A list of all the players for this game
    venue : GameVenue
        Venue information for this game
    officialVenue : Venue
        The official venue for this game
    weather : GameWeather
        The weather for this game.
    gameInfo : GameInfo
        information on this game
    review : GameReview
        Game review info and team challenges
    flags : GameFlags
        Flag bools for this game
    alerts : List[]
        Alerts
    probablePitchers : GameProbablePitchers
        Home and away probable pitchers for this game
    officialScorer : Person
        The official scorer for this game
    primaryDatacaster : Person
        The official dataCaster for this game
    """

    game: Union[GameDataGame, dict]
    datetime: Union[GameDatetime, dict]
    status: Union[GameStatus, dict]
    teams: Union[GameTeams, dict]
    players: Union[List[Person], dict]
    venue: Union[Venue, dict]
    officialVenue: Union[Venue, dict]
    weather: Union[GameWeather, dict]
    gameInfo: Union[GameInfo, dict]
    review: Union[GameReview, dict]
    flags: Union[GameFlags, dict]
    alerts: List
    probablePitchers: Union[GameProbablePitchers, dict]
    officialScorer: Union[Person, dict]
    primaryDatacaster: Union[Person, dict]

    def __post_init__(self):
        self.game = GameDataGame(**self.game)
        self.datetime = GameDatetime(**self.datetime)
        self.status = GameStatus(**self.status)
        self.teams = GameTeams(**self.teams)
        self.players = [Person(**(self.players[key])) for key in self.players]
        self.venue = Venue(**self.venue)
        self.officialVenue = Venue(**self.officialVenue)
        self.weather = GameWeather(**self.weather)
        self.gameInfo = GameInfo(**self.gameInfo)
        self.review = GameReview(**self.review)
        self.flags = GameFlags(**self.flags)
        self.probablePitchers = GameProbablePitchers(**self.probablePitchers)
        self.officialScorer = Person(**self.officialScorer)
        self.primaryDatacaster = Person(**self.primaryDatacaster)
