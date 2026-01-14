from typing import Optional, List, ClassVar
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from .stats import Split


class SimpleGameStats(MLBBaseModel):
    """
    A class to represent simple game statistics.

    Attributes
    ----------
    first_date_played : str
        First date of game played.
    games_played : int
        Number of the games played.
    games_started : int
        Number of the games started.
    last_date_played : str
        Last date of the game played.
    """
    first_date_played: str = Field(alias="firstDatePlayed")
    games_played: int = Field(alias="gamesPlayed")
    games_started: int = Field(alias="gamesStarted")
    last_date_played: str = Field(alias="lastDatePlayed")


class SeasonGame(Split):
    """
    A class to represent a game statistic.

    Used for the following stat types:
    season, statsSingleSeason
    """
    _type: ClassVar[List[str]] = ['season', 'statsSingleSeason']


class CareerGame(Split):
    """
    A class to represent a career game statistic.
    """
    _type: ClassVar[List[str]] = ['career']


class CareerRegularSeasonGame(Split):
    """
    A class to represent a career regular season game statistic.

    Attributes
    ----------
    first_date_played : str
        First date of game played.
    games_played : int
        Number of the games played.
    games_started : int
        Number of the games started.
    last_date_played : str
        Last date of the game played.
    """
    _type: ClassVar[List[str]] = ['careerRegularSeason']
    first_date_played: Optional[str] = Field(default=None, alias="firstDatePlayed")
    games_played: Optional[int] = Field(default=None, alias="gamesPlayed")
    games_started: Optional[int] = Field(default=None, alias="gamesStarted")
    last_date_played: Optional[str] = Field(default=None, alias="lastDatePlayed")


class CareerPlayoffsGame(Split):
    """
    A class to represent a career playoffs game statistic.

    Attributes
    ----------
    first_date_played : str
        First date of game played.
    games_played : int
        Number of the games played.
    games_started : int
        Number of the games started.
    last_date_played : str
        Last date of the game played.
    """
    _type: ClassVar[List[str]] = ['careerPlayoffs']
    first_date_played: Optional[str] = Field(default=None, alias="firstDatePlayed")
    games_played: Optional[int] = Field(default=None, alias="gamesPlayed")
    games_started: Optional[int] = Field(default=None, alias="gamesStarted")
    last_date_played: Optional[str] = Field(default=None, alias="lastDatePlayed")
