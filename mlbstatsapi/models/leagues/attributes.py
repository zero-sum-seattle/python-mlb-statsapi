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
    seasonid:                   Optional[str] = None
    preseasonstartdate:         Optional[str] = None
    preseasonenddate:           Optional[str] = None
    seasonstartdate:            Optional[str] = None
    springstartdate:            Optional[str] = None
    springenddate:              Optional[str] = None
    regularseasonstartdate:     Optional[str] = None
    lastdate1sthalf:            Optional[str] = None
    allstardate:                Optional[str] = None
    firstdate2ndhalf:           Optional[str] = None
    regularseasonenddate:       Optional[str] = None
    postseasonstartdate:        Optional[str] = None
    postseasonenddate:          Optional[str] = None
    seasonenddate:              Optional[str] = None
    offseasonstartdate:         Optional[str] = None
    offseasonenddate:           Optional[str] = None
    seasonlevelgamedaytype:     Optional[str] = None
    gamelevelgamedaytype:       Optional[str] = None
    qualifierplateappearances:  Optional[str] = None
    qualifieroutspitched:       Optional[str] = None
