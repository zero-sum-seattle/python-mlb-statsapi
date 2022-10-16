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
    officialvenue : Venue
        The official venue for this game
    weather : GameWeather
        The weather for this game.
    gameinfo : GameInfo
        information on this game
    review : GameReview
        Game review info and team challenges
    flags : GameFlags
        Flag bools for this game
    alerts : List[]
        Alerts
    probablepitchers : GameProbablePitchers
        Home and away probable pitchers for this game
    officialscorer : Person
        The official scorer for this game
    primarydatacaster : Person
        The official dataCaster for this game
    """

    game: Union[GameDataGame, dict]
    datetime: Union[GameDatetime, dict]
    status: Union[GameStatus, dict]
    teams: Union[GameTeams, dict]
    players: Union[List[Person], dict]
    venue: Union[Venue, dict]
    officialvenue: Union[Venue, dict]
    weather: Union[GameWeather, dict]
    gameinfo: Union[GameInfo, dict]
    review: Union[GameReview, dict]
    flags: Union[GameFlags, dict]
    alerts: List
    probablepitchers: Union[GameProbablePitchers, dict]
    officialscorer: Union[Person, dict]
    primarydatacaster: Union[Person, dict]

    def __post_init__(self):
        self.game = GameDataGame(**self.game)
        self.datetime = GameDatetime(**self.datetime)
        self.status = GameStatus(**self.status)
        self.teams = GameTeams(**self.teams)
        self.players = [Person(**(self.players[key])) for key in self.players]
        self.venue = Venue(**self.venue)
        self.officialvenue = Venue(**self.officialvenue)
        self.weather = GameWeather(**self.weather)
        self.gameinfo = GameInfo(**self.gameinfo)
        self.review = GameReview(**self.review)
        self.flags = GameFlags(**self.flags)
        self.probablepitchers = GameProbablePitchers(**self.probablepitchers)
        self.officialscorer = Person(**self.officialscorer)
        self.primarydatacaster = Person(**self.primarydatacaster)
