from typing import Union, Optional
from dataclasses import dataclass

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.sports import Sport


@dataclass(kw_only=True)
class Prportalcalculatedfields:
    """
    This dataclass represents the calculated fields for a baseball game.

    Attributes:
    ----------
    total7inngames : int
        The total number of 7-inning games played.
    total9inngames : int
        The total number of 9-inning games played.
    totalextrainngames : int
        The total number of extra-inning games played.
    timeper7inngame : str
        The average time per 7-inning game.
    timeper9inngame : str
        The average time per 9-inning game.
    timeperextrainngame : str
        The average time per extra-inning game.
    """
    total7inngames: int
    total9inngames: int
    totalextrainngames: int
    timeper7inngame: str
    timeper9inngame: str
    timeperextrainngame: str


@dataclass(kw_only=True, repr=False)
class Gamepacedata:
    """
    This dataclass represents a league in a sport, with various statistics and metrics related to its games and performances.

    Attributes:
    ----------
    hitsper9inn : float
        The number of hits per 9 innings played.
    runsper9inn : float
        The number of runs scored per 9 innings played.
    pitchesper9inn : float
        The number of pitches thrown per 9 innings played.
    plateappearancesper9inn : float
        The number of plate appearances per 9 innings played.
    hitspergame : float
        The number of hits per game played.
    runspergame : float
        The number of runs scored per game played.
    inningsplayedpergame : float
        The number of innings played per game.
    pitchespergame : float
        The number of pitches thrown per game played.
    pitcherspergame : float
        The number of pitchers used per game played.
    plateappearancespergame : float
        The number of plate appearances per game played.
    totalgametime : str
        The total time spent playing games in the league.
    totalinningsplayed : float
        The total number of innings played in the league.
    totalhits : int
        The total number of hits in the league.
    totalruns : int
        The total number of runs scored in the league.
    totalplateappearances : int
        The total number of plate appearances in the league.
    totalpitchers : int
        The total number of pitchers used in the league.
    totalpitches : int
        The total number of pitches thrown in the league.
    totalgames : int
        The total number of games played in the league.
    total7inngames : int
        The total number of 7-inning games played in the league.
    total9inngames : int
        The total number of 9-inning games played in the league.
    totalextrainngames : int
        The total number of extra inning games played in the league.
    timepergame : str
        The amount of time spent per game in the league.
    timeperpitch : str
        The amount of time spent per pitch in the league.
    timeperhit : str
        The amount of time spent per hit in the league.
    timeperrun : str
        The amount of time spent per run scored in the league.
    timeperplateappearance : str
        The amount of time spent per plate appearance in the league.
    timeper9inn : str
        The amount of time spent per 9 innings played in the league.
    timeper77plateappearances : str
        The amount of time spent per 7-7 plate appearances in the league.
    totalextrainntime : str
        The total amount of time spent on extra inning games in the league.
    timeper7inngame : str
        The amount of time spent per 7-inning game in the league.
    total7inngamescompletedearly: int
        The total number of 7-inning games completed early in the league.
    timeper7inngamewithoutextrainn: str
        The amount of time spent per 7-inning game without extra innings in the league.
    total7inngamesscheduled : int
        The total number of 7-inning games scheduled in the league.
    total7inngameswithoutextrainn : int
        The total number of 7-inning games played without extra innings in the league.
    total9inngamescompletedearly : int
        The total number of 9-inning games completed early in the league.
    total9inngameswithoutextrainn : int
        The total number of 9-inning games
    total9inngamesscheduled : int
        The total number of 9 inning games scheduled
    hitsperrun : float
        The number of hits per run
    pitchesperpitcher : float
        Number of pitches thrown per pitcher
    season : str
        Season number
    team: Team
        Team
    league : League
        League
    sport : Sport
        Sport`
    prportalcalculatedfields : Prportalcalculatedfields
        calculated fields for a league
    """
    hitsper9inn: Optional[float] = None
    runsper9inn: Optional[float] = None
    pitchesper9inn: Optional[float] = None
    plateappearancesper9inn: Optional[float] = None
    hitspergame: Optional[float] = None
    runspergame: Optional[float] = None
    inningsplayedpergame: Optional[float] = None
    pitchespergame: Optional[float] = None
    pitcherspergame: Optional[float] = None
    plateappearancespergame: Optional[float] = None
    totalgametime: Optional[str] = None
    totalinningsplayed: Optional[float] = None
    totalhits: Optional[int] = None
    totalruns: Optional[int] = None
    totalplateappearances: Optional[int] = None
    totalpitchers: Optional[int] = None
    totalpitches: Optional[int] = None
    totalgames: Optional[int] = None
    total7inngames: Optional[int] = None
    total9inngames: Optional[int] = None
    totalextrainngames: Optional[int] = None
    timepergame: Optional[str] = None
    timeperpitch: Optional[str] = None
    timeperhit: Optional[str] = None
    timeperrun: Optional[str] = None
    timeperplateappearance: Optional[str] = None
    timeper9inn: Optional[str] = None
    timeper77plateappearances: Optional[str] = None
    totalextrainntime: Optional[str] = None
    timeper7inngame: Optional[str] = None
    total7inngamescompletedearly: Optional[int] = None
    timeper7inngamewithoutextrainn: Optional[str] = None
    total7inngamesscheduled: Optional[int] = None
    total7inngameswithoutextrainn: Optional[int] = None
    total9inngamescompletedearly: Optional[int] = None
    total9inngameswithoutextrainn: Optional[int] = None
    total9inngamesscheduled: Optional[int] = None
    hitsperrun: Optional[float] = None
    pitchesperpitcher: Optional[float] = None
    season: Optional[str] = None
    team: Optional[Union[Team, dict]] = None
    league: Optional[Union[League, dict]] = None
    sport: Optional[Union[Sport, dict]] = None
    prportalcalculatedfields: Optional[Union[Prportalcalculatedfields, dict]] = None

    def __post_init__(self):
        self.team = Team(**self.team) if self.team else None
        self.league = League(**self.league) if self.league else None   
        self.sport = Sport(**self.sport) if self.sport else None
        self.prportalcalculatedfields = Prportalcalculatedfields(**self.prportalcalculatedfields) if self.prportalcalculatedfields else None

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws)) 