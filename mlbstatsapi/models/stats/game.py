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
    first_date_played: str = Field(alias="firstdateplayed")
    games_played: int = Field(alias="gamesplayed")
    games_started: int = Field(alias="gamesstarted")
    last_date_played: str = Field(alias="lastdateplayed")


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
    first_date_played: Optional[str] = Field(default=None, alias="firstdateplayed")
    games_played: Optional[int] = Field(default=None, alias="gamesplayed")
    games_started: Optional[int] = Field(default=None, alias="gamesstarted")
    last_date_played: Optional[str] = Field(default=None, alias="lastdateplayed")


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
    first_date_played: Optional[str] = Field(default=None, alias="firstdateplayed")
    games_played: Optional[int] = Field(default=None, alias="gamesplayed")
    games_started: Optional[int] = Field(default=None, alias="gamesstarted")
    last_date_played: Optional[str] = Field(default=None, alias="lastdateplayed")
