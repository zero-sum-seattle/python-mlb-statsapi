from typing import Optional, Any, List, ClassVar
from pydantic import Field, field_validator
from mlbstatsapi.models.base import MLBBaseModel, OptionalFloat
from mlbstatsapi.models.people import Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game
from .stats import Split


class SimpleFieldingSplit(MLBBaseModel):
    """
    A class to represent a simple fielding split.

    Attributes
    ----------
    age : int
        Player age at the start of the season.
    games_played : int
        The number of games played.
    games_started : int
        The number of games started.
    caught_stealing : int
        The number of runners caught stealing.
    caught_stealing_percentage : float
        The percentage of runners caught stealing.
    stolen_bases : int
        The number of stolen bases.
    stolen_base_percentage : float
        The stolen base percentage.
    assists : int
        The number of assists.
    putouts : int
        The number of put outs.
    errors : int
        The number of errors committed.
    chances : int
        The number of chances.
    fielding : float
        The fielding percentage.
    range_factor_per_game : float
        Range rating per game.
    range_factor_per_9_inn : float
        Range factor per 9 innings.
    innings : float
        The number of innings played.
    games : int
        The number of games played.
    passed_ball : int
        The number of passed balls.
    double_plays : int
        The number of double plays.
    triple_plays : int
        The number of triple plays.
    catcher_era : float
        The catcher ERA of the fielding stat.
    catchers_interference : int
        The number of times catchers interference was committed.
    wild_pitches : int
        The number of wild pitches.
    throwing_errors : int
        The number of throwing errors.
    pickoffs : int
        The number of pick offs.
    """
    age: Optional[int] = None
    position: Optional[Position] = None
    games_played: Optional[int] = Field(default=None, alias="gamesPlayed")
    games_started: Optional[int] = Field(default=None, alias="gamesStarted")
    caught_stealing: Optional[int] = Field(default=None, alias="caughtStealing")
    caught_stealing_percentage: OptionalFloat = Field(default=None, alias="caughtStealingPercentage")
    stolen_bases: Optional[int] = Field(default=None, alias="stolenBases")
    stolen_base_percentage: OptionalFloat = Field(default=None, alias="stolenBasePercentage")
    assists: Optional[int] = None
    putouts: Optional[int] = None
    errors: Optional[int] = None
    chances: Optional[int] = None
    fielding: OptionalFloat = None
    range_factor_per_game: OptionalFloat = Field(default=None, alias="rangeFactorPerGame")
    range_factor_per_9_inn: OptionalFloat = Field(default=None, alias="rangeFactorPer9Inn")
    innings: OptionalFloat = None
    games: Optional[int] = None
    passed_ball: Optional[int] = Field(default=None, alias="passedBall")
    double_plays: Optional[int] = Field(default=None, alias="doublePlays")
    triple_plays: Optional[int] = Field(default=None, alias="triplePlays")
    catcher_era: OptionalFloat = Field(default=None, alias="catcherEra")
    catchers_interference: Optional[int] = Field(default=None, alias="catchersInterference")
    wild_pitches: Optional[int] = Field(default=None, alias="wildPitches")
    throwing_errors: Optional[int] = Field(default=None, alias="throwingErrors")
    pickoffs: Optional[int] = None

    @field_validator('position', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class FieldingSeasonAdvanced(Split):
    """
    A class to represent a fielding seasonAdvanced statistic.

    Attributes
    ----------
    position : Position
        The position of the player.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['seasonAdvanced']
    stat: SimpleFieldingSplit
    position: Optional[Position] = None

    @field_validator('position', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class FieldingCareerAdvanced(Split):
    """
    A class to represent a fielding careerAdvanced statistic.

    Attributes
    ----------
    position : Position
        The position of the player.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['careerAdvanced']
    stat: SimpleFieldingSplit
    position: Optional[Position] = None

    @field_validator('position', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class FieldingSingleSeasonAdvanced(Split):
    """
    A class to represent a fielding statsSingleSeasonAdvanced statistic.

    Attributes
    ----------
    position : Position
        The position of the player.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['statsSingleSeasonAdvanced']
    stat: SimpleFieldingSplit
    position: Optional[Position] = None

    @field_validator('position', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class FieldingSeason(Split):
    """
    A class to represent a fielding season statistic.

    Attributes
    ----------
    position : Position
        The position of the player.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['season']
    stat: SimpleFieldingSplit
    position: Optional[Position] = None

    @field_validator('position', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class FieldingSingleSeason(Split):
    """
    A class to represent a fielding statsSingleSeason statistic.

    Attributes
    ----------
    position : Position
        The position of the player.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['statsSingleSeason']
    stat: SimpleFieldingSplit
    position: Optional[Position] = None

    @field_validator('position', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class FieldingCareer(Split):
    """
    A class to represent a fielding career statistic.

    Attributes
    ----------
    position : Position
        The position of the player.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['career', 'careerRegularSeason']
    stat: SimpleFieldingSplit
    position: Optional[Position] = None

    @field_validator('position', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class FieldingCareerPlayoffs(Split):
    """
    A class to represent a fielding careerPlayoffs statistic.

    Attributes
    ----------
    position : Position
        The position of the player.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['careerPlayoffs']
    stat: SimpleFieldingSplit
    position: Optional[Position] = None

    @field_validator('position', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class FieldingHomeAndAway(Split):
    """
    A class to represent a fielding homeAndAway statistic.

    Attributes
    ----------
    is_home : bool
        A bool value for is the game at home.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['homeAndAway']
    is_home: bool = Field(alias="isHome")
    stat: SimpleFieldingSplit


class FieldingHomeAndAwayPlayoffs(Split):
    """
    A class to represent a fielding homeAndAwayPlayoffs statistic.

    Attributes
    ----------
    is_home : bool
        A bool value for is the game at home.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['homeAndAwayPlayoffs']
    is_home: bool = Field(alias="isHome")
    stat: SimpleFieldingSplit


class FieldingYearByYear(Split):
    """
    A class to represent a fielding yearByYear statistic.

    Attributes
    ----------
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['yearByYear']
    stat: SimpleFieldingSplit


class FieldingYearByYearAdvanced(Split):
    """
    A class to represent a fielding yearByYearAdvanced statistic.

    Attributes
    ----------
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['yearByYearAdvanced']
    stat: SimpleFieldingSplit


class FieldingYearByYearPlayoffs(Split):
    """
    A class to represent a fielding yearByYearPlayoffs statistic.

    Attributes
    ----------
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['yearByYearPlayoffs']
    stat: SimpleFieldingSplit


class FieldingWinLoss(Split):
    """
    A class to represent a fielding winLoss statistic.

    Attributes
    ----------
    is_win : bool
        Is the game a win.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['winLoss']
    is_win: bool = Field(alias="isWin")
    stat: SimpleFieldingSplit


class FieldingWinLossPlayoffs(Split):
    """
    A class to represent a fielding winLossPlayoffs statistic.

    Attributes
    ----------
    is_win : bool
        Is the game a win.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['winLossPlayoffs']
    is_win: bool = Field(alias="isWin")
    stat: SimpleFieldingSplit


class FieldingByDayOfWeek(Split):
    """
    A class to represent a fielding byDayOfWeek statistic.

    Attributes
    ----------
    day_of_week : str
        The day of the week.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['byDayOfWeek']
    day_of_week: str = Field(alias="dayOfWeek")
    stat: SimpleFieldingSplit


class FieldingByDateRangeAdvanced(Split):
    """
    A class to represent a fielding byDateRangeAdvanced stat.

    Attributes
    ----------
    position : Position
        The position.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['byDateRangeAdvanced']
    stat: SimpleFieldingSplit
    position: Optional[Position] = None

    @field_validator('position', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class FieldingByMonth(Split):
    """
    A class to represent a fielding byMonth stat.

    Attributes
    ----------
    month : int
        The month of the stat.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['byMonth']
    month: int
    stat: SimpleFieldingSplit


class FieldingByMonthPlayoffs(Split):
    """
    A class to represent a fielding byMonthPlayoffs stat.

    Attributes
    ----------
    month : int
        The month of the stat.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['byMonthPlayoffs']
    month: int
    stat: SimpleFieldingSplit


class FieldingLastXGames(Split):
    """
    A class to represent a fielding lastXGames stat.

    Attributes
    ----------
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['lastXGames']
    stat: SimpleFieldingSplit


class FieldingGameLog(Split):
    """
    A class to represent a fielding gameLog stats.

    Attributes
    ----------
    opponent : Team
        The opponent.
    date : str
        The date.
    is_home : bool
        Is home bool.
    is_win : bool
        Is win bool.
    position : Position
        The position.
    game : Game
        The game.
    stat : SimpleFieldingSplit
        The fielding split stat.
    """
    _stat: ClassVar[List[str]] = ['gameLog']
    date: str
    is_home: bool = Field(alias="isHome")
    is_win: bool = Field(alias="isWin")
    stat: SimpleFieldingSplit
    opponent: Optional[Team] = None
    position: Optional[Position] = None
    game: Optional[Game] = None

    @field_validator('opponent', 'position', 'game', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v
