from typing import Dict, Union, Any
from dataclasses import dataclass, field

@dataclass
class LeagueSeasonDateInfo:
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
    seasonId:                   str = None
    preSeasonStartDate:         str = None
    preSeasonEndDate:           str = None
    seasonStartDate:            str = None
    springStartDate:            str = None
    springEndDate:              str = None
    regularSeasonStartDate:     str = None
    lastDate1stHalf:            str = None
    allStarDate:                str = None
    firstDate2ndHalf:           str = None
    regularSeasonEndDate:       str = None
    postSeasonStartDate:        str = None
    postSeasonEndDate:          str = None
    seasonEndDate:              str = None
    offseasonStartDate:         str = None
    offSeasonEndDate:           str = None
    seasonLevelGamedayType:     str = None
    gameLevelGamedayType:       str = None
    qualifierPlateAppearances:  str = None
    qualifierOutsPitched:       str = None
