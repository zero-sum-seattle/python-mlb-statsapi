from typing import Optional
from dataclasses import dataclass

@dataclass
class SeasonDateInfo:
    """
    A class to represent a LeagueSeasonDateInfo.

    Attributes
    ----------
    seasonId : str = None
        League season id
    preSeasonStartDate : str = None
        Leagues pre season start date
    preSeasonEndDate : str = None
        Leagues pre season end data
    seasonStartDate : str = None
        Leagues season start date
    springStartDate : str = None
        Leagues spring season start date
    springEndDate : str = None
        Leagues spring season end date
    regularSeasonStartDate : str = None
        Leagues regular season start date
    lastDate1stHalf : str = None
        The date of the last day of the first half of the season
    allStarDate : str = None
        Leagues all star game date
    firstDate2ndHalf : str = None
        The date of the first day of the second half of the season
    regularSeasonEndDate : str = None
        Leagues regular season end date
    postSeasonStartDate : str = None
        Leagues post season start date
    postSeasonEndDate : str = None
        Leagues post season end date
    seasonEndDate : str = None
        Leagues season end date
    offseasonStartDate : str = None
        Leagues off season start date
    offSeasonEndDate : str = None
        Leagues off season end date
    seasonLevelGamedayType : str = None
        Leagues game day type
    gameLevelGamedayType : str = None
        Leagues game day type
    qualifierPlateAppearances : str = None

    qualifierOutsPitched : str = None

    """
    seasonId:                   Optional[str] = None
    preSeasonStartDate:         Optional[str] = None
    preSeasonEndDate:           Optional[str] = None
    seasonStartDate:            Optional[str] = None
    springStartDate:            Optional[str] = None
    springEndDate:              Optional[str] = None
    regularSeasonStartDate:     Optional[str] = None
    lastDate1stHalf:            Optional[str] = None
    allStarDate:                Optional[str] = None
    firstDate2ndHalf:           Optional[str] = None
    regularSeasonEndDate:       Optional[str] = None
    postSeasonStartDate:        Optional[str] = None
    postSeasonEndDate:          Optional[str] = None
    seasonEndDate:              Optional[str] = None
    offseasonStartDate:         Optional[str] = None
    offSeasonEndDate:           Optional[str] = None
    seasonLevelGamedayType:     Optional[str] = None
    gameLevelGamedayType:       Optional[str] = None
    qualifierPlateAppearances:  Optional[str] = None
    qualifierOutsPitched:       Optional[str] = None
