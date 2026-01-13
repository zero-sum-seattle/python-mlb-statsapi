from typing import Optional, List, ClassVar
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game
from .stats import Split


class SimpleCatchingSplit(MLBBaseModel):
    """
    A class to represent a simple catching split.

    Attributes
    ----------
    age : int
        Age at beginning of season.
    games_played : int
        The number of games played by the catcher.
    runs : int
        The number of runs given up while catching.
    home_runs : int
        The number of home runs given up while catching.
    strikeouts : int
        The number of strike outs while catching.
    base_on_balls : int
        The number of base on balls while catching.
    intentional_walks : int
        The number of intentional walks while catching.
    hits : int
        The number of hits while catching.
    hit_by_pitch : int
        The number of batters hit by a pitch while catching.
    avg : str
        The batting average while catching.
    at_bats : int
        The number of at bats while catching.
    obp : str
        The on base percentage while catching.
    slg : str
        The slugging percentage while catching.
    ops : str
        The on-base slugging while catching.
    caught_stealing : int
        The number of runners caught stealing by the catcher.
    caught_stealing_percentage : str
        Percentage of runners caught stealing by the catcher.
    stolen_bases : int
        The number of stolen bases while catching.
    stolen_base_percentage : str
        The stolen base percentage against the catcher.
    earned_runs : int
        The earned run amount against the catcher.
    batters_faced : int
        The number of batters faced while catching.
    games_pitched : int
        The number of games pitched while catching.
    hit_batsmen : int
        The number of batters hit by pitches while catching.
    wild_pitches : int
        The number of wild pitches while catching.
    pickoffs : int
        The number of pick offs while catching.
    total_bases : int
        The total number of bases.
    strikeout_walk_ratio : str
        The strike out to walk ratio while catching.
    catchers_interference : int
        The number of times catcher interference committed.
    sac_bunts : int
        The number of sac bunts performed while catching.
    sac_flies : int
        The number of sac flies while catching.
    passed_ball : int
        The number of passed balls while catching.
    pickoff_attempts : int
        The number of pickoff attempts.
    """
    age: Optional[int] = None
    games_played: Optional[int] = Field(default=None, alias="gamesplayed")
    runs: Optional[int] = None
    home_runs: Optional[int] = Field(default=None, alias="homeruns")
    strikeouts: Optional[int] = None
    base_on_balls: Optional[int] = Field(default=None, alias="baseonballs")
    intentional_walks: Optional[int] = Field(default=None, alias="intentionalwalks")
    hits: Optional[int] = None
    hit_by_pitch: Optional[int] = Field(default=None, alias="hitbypitch")
    avg: Optional[str] = None
    at_bats: Optional[int] = Field(default=None, alias="atbats")
    obp: Optional[str] = None
    slg: Optional[str] = None
    ops: Optional[str] = None
    caught_stealing: Optional[int] = Field(default=None, alias="caughtstealing")
    caught_stealing_percentage: Optional[str] = Field(default=None, alias="caughtstealingpercentage")
    stolen_bases: Optional[int] = Field(default=None, alias="stolenbases")
    stolen_base_percentage: Optional[str] = Field(default=None, alias="stolenbasepercentage")
    earned_runs: Optional[int] = Field(default=None, alias="earnedruns")
    batters_faced: Optional[int] = Field(default=None, alias="battersfaced")
    games_pitched: Optional[int] = Field(default=None, alias="gamespitched")
    hit_batsmen: Optional[int] = Field(default=None, alias="hitbatsmen")
    wild_pitches: Optional[int] = Field(default=None, alias="wildpitches")
    pickoffs: Optional[int] = None
    total_bases: Optional[int] = Field(default=None, alias="totalbases")
    strikeout_walk_ratio: Optional[str] = Field(default=None, alias="strikeoutwalkratio")
    catchers_interference: Optional[int] = Field(default=None, alias="catchersinterference")
    sac_bunts: Optional[int] = Field(default=None, alias="sacbunts")
    sac_flies: Optional[int] = Field(default=None, alias="sacflies")
    passed_ball: Optional[int] = Field(default=None, alias="passedball")
    pickoff_attempts: Optional[int] = Field(default=None, alias="pickoffattempts")


class CatchingSeason(Split):
    """
    A class to represent a catching season statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['season']
    stat: SimpleCatchingSplit


class CatchingSingleSeason(Split):
    """
    A class to represent a catching statsSingleSeason statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['statsSingleSeason']
    stat: SimpleCatchingSplit


class CatchingYearByYearPlayoffs(Split):
    """
    A class to represent a catching yearByYearPlayoffs statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['yearByYearPlayoffs']
    stat: SimpleCatchingSplit


class CatchingYearByYear(Split):
    """
    A class to represent a catching yearByYear statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['yearByYear']
    stat: SimpleCatchingSplit


class CatchingProjected(Split):
    """
    A class to represent a catching projectedRos statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['projectedRos']
    stat: SimpleCatchingSplit


class CatchingCareer(Split):
    """
    A class to represent a catching career statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['career']
    stat: SimpleCatchingSplit


class CatchingCareerRegularSeason(Split):
    """
    A class to represent a catching careerRegularSeason statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['careerRegularSeason']
    stat: SimpleCatchingSplit


class CatchingGameLog(Split):
    """
    A class to represent a catching gameLog statistic.

    Attributes
    ----------
    is_home : bool
        Is home bool.
    is_win : bool
        Is win bool.
    date : str
        The date.
    game : Game
        The game.
    opponent : Team
        The opponent.
    """
    _stat: ClassVar[List[str]] = ['gameLog']
    is_home: bool = Field(alias="ishome")
    is_win: bool = Field(alias="iswin")
    date: str
    game: Game
    opponent: Team


class CatchingLastXGames(Split):
    """
    A class to represent a catching lastXGames statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['lastXGames']
    stat: SimpleCatchingSplit


class CatchingByDateRange(Split):
    """
    A class to represent a catching byDateRange statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['byDateRange']
    stat: SimpleCatchingSplit


class CatchingByDayOfWeek(Split):
    """
    A class to represent a catching byDayOfWeek statistic.

    Attributes
    ----------
    day_of_week : int
        The day of the week.
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['byDayOfWeek']
    day_of_week: int = Field(alias="dayofweek")
    stat: SimpleCatchingSplit


class CatchingHomeAndAway(Split):
    """
    A class to represent a catching homeAndAway statistic.

    Attributes
    ----------
    is_home : bool
        Is home bool.
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['homeAndAway']
    is_home: bool = Field(alias="ishome")
    stat: SimpleCatchingSplit


class CatchingWinLoss(Split):
    """
    A class to represent a catching winLoss statistic.

    Attributes
    ----------
    is_win : bool
        Is win bool.
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['winLoss']
    is_win: bool = Field(alias="iswin")
    stat: SimpleCatchingSplit
