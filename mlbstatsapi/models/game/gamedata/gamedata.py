from typing import Optional, Union, List
from pydantic import BaseModel
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
from .attributes import MoundVisits

class GameData(BaseModel):
    """Represents the data related to a specific game.

    This class encompasses all relevant information for a game, including details about the game itself, timing, teams involved, players, venue, weather conditions, and additional metadata such as reviews, flags, and alerts.

    Attributes:
        game (GameDataGame): Information about the game.
        dateTime (GameDatetime): Time and dates associated with the game.
        status (GameStatus): Current status of the game.
        teams (GameTeams): Information on the two teams participating in the game, both home and away.
        players (List[Person]): A list of all players participating in the game.
        venue (Venue): Venue information where the game is being held.
        officialVenue (Venue): The official venue for the game.
        weather (GameWeather): Weather conditions for the game.
        gameInfo (GameInfo): General information about the game.
        review (GameReview): Information on game reviews and team challenges.
        flags (GameFlags): Various boolean flags associated with the game.
        alerts (List[]): Alerts related to the game.
        probablePitchers (GameProbablePitchers): Information on the probable pitchers for both the home and away teams.
        officialScorer (Person): The official scorer for the game.
        primaryDatacaster (Person): The official data caster for the game.
    """

    game: GameDataGame
    datetime: GameDatetime
    status: GameStatus
    teams: GameTeams
    players: List[Person]
    venue: Union[Venue]
    officialVenue: Union[Venue]
    review: Union[GameReview]
    flags: Union[GameFlags]
    alerts: List
    probablePitchers: GameProbablePitchers
    moundVisits: Optional[MoundVisits]
    gameInfo: GameInfo
    weather: GameWeather
    officialScorer: Optional[Person]
    primaryDatacaster: Optional[Person]
    secondaryDatacaster: Optional[Person]


