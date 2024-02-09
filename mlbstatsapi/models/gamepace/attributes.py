from typing import Optional
from pydantic import BaseModel

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.sports import Sport


class PrPortalCalculatedFields(BaseModel):
    """Represents the calculated fields for a baseball game.

    Attributes:
        total7InnGames (int): The total number of 7-inning games played.
        total9InnGames (int): The total number of 9-inning games played.
        totalExtraInnGames (int): The total number of extra-inning games played.
        timePer7InnGame (str): The average time per 7-inning game.
        timePer9InnGame (str): The average time per 9-inning game.
        timePerExtraInnGame (str): The average time per extra-inning game.
    """
    total7InnGames: int
    total9InnGames: int
    totalExtraInnGames: int
    timePer7InnGame: str
    timePer9InnGame: str
    timePerExtraInnGame: str



class GamePaceData(BaseModel):
    """Represents a league's game pace data with various statistics and metrics.

    Attributes:
        hitsPer9Inn (float, optional): The number of hits per 9 innings. Optional.
        runsPer9Inn (float, optional): The number of runs scored per 9 innings. Optional.
        pitchesPer9Inn (float, optional): The number of pitches thrown per 9 innings. Optional.
        plateAppearancesPer9Inn (float, optional): The number of plate appearances per 9 innings. Optional.
        hitsPerGame (float, optional): The number of hits per game. Optional.
        runsPerGame (float, optional): The number of runs scored per game. Optional.
        inningsPlayedPerGame (float, optional): The number of innings played per game. Optional.
        pitchesPerGame (float, optional): The number of pitches thrown per game. Optional.
        pitchersPerGame (float, optional): The number of pitchers used per game. Optional.
        plateAppearancesPerGame (float, optional): The number of plate appearances per game. Optional.
        totalGameTime (str, optional): The total game time. Optional.
        totalInningsPlayed (float, optional): The total innings played. Optional.
        totalHits (int, optional): The total number of hits. Optional.
        totalRuns (int, optional): The total number of runs. Optional.
        totalPlateAppearances (int, optional): The total number of plate appearances. Optional.
        totalPitchers (int, optional): The total number of pitchers used. Optional.
        totalPitches (int, optional): The total number of pitches thrown. Optional.
        totalGames (int, optional): The total number of games. Optional.
        total7InnGames (int, optional): The total number of 7-inning games. Optional.
        total9InnGames (int, optional): The total number of 9-inning games. Optional.
        totalExtraInnGames (int, optional): The total number of extra inning games. Optional.
        timePerGame (str, optional): The average time per game. Optional.
        timePerPitch (str, optional): The average time per pitch. Optional.
        timePerHit (str, optional): The average time per hit. Optional.
        timePerRun (str, optional): The average time per run scored. Optional.
        timePerPlateAppearance (str, optional): The average time per plate appearance. Optional.
        timePer9Inn (str, optional): The average time for 9 innings. Optional.
        timePer77PlateAppearances (str, optional): The average time for 77 plate appearances. Optional.
        totalExtraInnTime (str, optional): The total extra inning time. Optional.
        timePer7InnGame (str, optional): The average time per 7-inning game. Optional.
        timePer7InnGameWithoutExtraInn (str, optional): The average time for 7-inning games without extra innings. Optional.
        total7InnGamesScheduled (int, optional): The total number of 7-inning games scheduled. Optional.
        total7InnGamesWithoutExtraInn (int, optional): The total number of 7-inning games without extra innings. Optional.
        total9InnGamesCompletedEarly (int, optional): The total number of 9-inning games completed early. Optional.
        total9InnGamesWithoutExtraInn (int, optional): The total number of 9-inning games without extra innings. Optional.
        total9InnGamesScheduled (int, optional): The total number of 9-inning games scheduled. Optional.
        hitsPerRun (float, optional): The number of hits per run. Optional.
        pitchesPerPitcher (float, optional): The number of pitches thrown per pitcher. Optional.
        season (str, optional): The season. Optional.
        team (Team, optional): The team. Optional.
        league (League, optional): The league. Optional.
        sport (Sport, optional): The sport. Optional.
        prPortalCalculatedFields (PrPortalCalculatedFields, optional): The PR portal calculated fields. Optional.
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
    team: Optional[Team] = None
    league: Optional[League] = None
    sport: Optional[Sport] = None
    prPortalCalculatedFields: Optional[PrPortalCalculatedFields] = None
