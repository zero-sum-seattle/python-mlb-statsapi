from typing import Union, Optional
from dataclasses import dataclass

from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.sports import Sport


@dataclass(kw_only=True)
class Prportalcalculatedfields():
    """
    This dataclass represents the calculated fields for a baseball game.

    Attributes:
    ----------
    total7InnGames : int
        The total number of 7-inning games played.
    total9InnGames : int
        The total number of 9-inning games played.
    totalExtraInnGames : int
        The total number of extra-inning games played.
    timePer7InnGame : str
        The average time per 7-inning game.
    timePer9InnGame : str
        The average time per 9-inning game.
    timePerExtraInnGame : str
        The average time per extra-inning game.
    """
    total7InnGames: int
    total9InnGames: int
    totalExtraInnGames: int
    timePer7InnGame: str
    timePer9InnGame: str
    timePerExtraInnGame: str


@dataclass(kw_only=True)
class Gamepacedata():
    """
    This dataclass represents a league in a sport, with various statistics and metrics related to its games and performances.

    Attributes:
    ----------
    hitsPer9Inn : float
        The number of hits per 9 innings played.
    runsPer9Inn : float
        The number of runs scored per 9 innings played.
    pitchesPer9Inn : float
        The number of pitches thrown per 9 innings played.
    plateAppearancesPer9Inn : float
        The number of plate appearances per 9 innings played.
    hitsPerGame : float
        The number of hits per game played.
    runsPerGame : float
        The number of runs scored per game played.
    inningsPlayedPerGame : float
        The number of innings played per game.
    pitchesPerGame : float
        The number of pitches thrown per game played.
    pitchersPerGame : float
        The number of pitchers used per game played.
    plateAppearancesPerGame : float
        The number of plate appearances per game played.
    totalGameTime : str
        The total time spent playing games in the league.
    totalInningsPlayed : float
        The total number of innings played in the league.
    totalHits : int
        The total number of hits in the league.
    totalRuns : int
        The total number of runs scored in the league.
    totalPlateAppearances : int
        The total number of plate appearances in the league.
    totalPitchers : int
        The total number of pitchers used in the league.
    totalPitches : int
        The total number of pitches thrown in the league.
    totalGames : int
        The total number of games played in the league.
    total7InnGames : int
        The total number of 7-inning games played in the league.
    total9InnGames : int
        The total number of 9-inning games played in the league.
    totalExtraInnGames : int
        The total number of extra inning games played in the league.
    timePerGame : str
        The amount of time spent per game in the league.
    timePerPitch : str
        The amount of time spent per pitch in the league.
    timePerHit : str
        The amount of time spent per hit in the league.
    timePerRun : str
        The amount of time spent per run scored in the league.
    timePerPlateAppearance : str
        The amount of time spent per plate appearance in the league.
    timePer9Inn : str
        The amount of time spent per 9 innings played in the league.
    timePer77PlateAppearances : str
        The amount of time spent per 7-7 plate appearances in the league.
    totalExtraInnTime : str
        The total amount of time spent on extra inning games in the league.
    timePer7InnGame : str
        The amount of time spent per 7-inning game in the league.
    timePer7InnGameWithoutExtraInn: str
        The amount of time spent per 7-inning game without extra innings in the league.
    total7InnGamesScheduled : int
        The total number of 7-inning games scheduled in the league.
    total7InnGamesWithoutExtraInn : int
        The total number of 7-inning games played without extra innings in the league.
    total9InnGamesCompletedEarly : int
        The total number of 9-inning games completed early in the league.
    total9InnGamesWithoutExtraInn : int
        The total number of 9-inning games
    total9InnGamesScheduled : int
        The total number of 9 inning games scheduled
    hitsPerRun : float
        The number of hits per run
    pitchesPerPitcher : float
        Number of pitches thrown per pitcher
    season : str
        Season number
    league : Union[League, dict]
        League
    sport : Union[Sport, dict]
        Sport`
    prPortalCalculatedFields : Union[Prportalcalculatedfields, dict]
        calculated fields for a league
    """
    hitsPer9Inn: Optional[float] = None
    runsPer9Inn: Optional[float] = None
    pitchesPer9Inn: Optional[float] = None
    plateAppearancesPer9Inn: Optional[float] = None
    hitsPerGame: Optional[float] = None
    runsPerGame: Optional[float] = None
    inningsPlayedPerGame: Optional[float] = None
    pitchesPerGame: Optional[float] = None
    pitchersPerGame: Optional[float] = None
    plateAppearancesPerGame: Optional[float] = None
    totalGameTime: Optional[str] = None
    totalInningsPlayed: Optional[float] = None
    totalHits: Optional[int] = None
    totalRuns: Optional[int] = None
    totalPlateAppearances: Optional[int] = None
    totalPitchers: Optional[int] = None
    totalPitches: Optional[int] = None
    totalGames: Optional[int] = None
    total7InnGames: Optional[int] = None
    total9InnGames: Optional[int] = None
    totalExtraInnGames: Optional[int] = None
    timePerGame: Optional[str] = None
    timePerPitch: Optional[str] = None
    timePerHit: Optional[str] = None
    timePerRun: Optional[str] = None
    timePerPlateAppearance: Optional[str] = None
    timePer9Inn: Optional[str] = None
    timePer77PlateAppearances: Optional[str] = None
    totalExtraInnTime: Optional[str] = None
    timePer7InnGame: Optional[str] = None
    timePer7InnGameWithoutExtraInn: Optional[str] = None
    total7InnGamesScheduled: Optional[int] = None
    total7InnGamesWithoutExtraInn: Optional[int] = None
    total9InnGamesCompletedEarly: Optional[int] = None
    total9InnGamesWithoutExtraInn: Optional[int] = None
    total9InnGamesScheduled: Optional[int] = None
    hitsPerRun: Optional[float] = None
    pitchesPerPitcher: Optional[float] = None
    season: Optional[str] = None
    league: Optional[Union[League, dict]] = None
    sport: Optional[Union[Sport, dict]] = None
    prPortalCalculatedFields: Optional[Union[Prportalcalculatedfields, dict]] = None

    def __post_init__(self):
        self.league = League(**self.league) if self.league else None   
        self.sport = Sport(**self.sport) if self.sport else None
        self.prPortalCalculatedFields = Prportalcalculatedfields(**self.prPortalCalculatedFields) if self.prPortalCalculatedFields else None  