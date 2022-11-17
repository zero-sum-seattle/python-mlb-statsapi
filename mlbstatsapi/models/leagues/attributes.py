from typing import Optional
from dataclasses import dataclass


@dataclass
class SeasonDateInfo:
    """
    A class to represent a LeagueSeasonDateInfo.


    Attributes
    ----------
    seasonid : str
        League season id
    preseasonstartdate : str
        Leagues pre season start date
    preseasonenddate : str
        Leagues pre season end data
    seasonstartdate : str
        Leagues season start date
    springstartdate : str
        Leagues spring season start date
    springenddate : str
        Leagues spring season end date
    regularseasonstartdate : str
        Leagues regular season start date
    lastdate1sthalf : str
        The date of the last day of the first half of the season
    allstardate : str
        Leagues all star game date
    firstdate2ndhalf : str
        The date of the first day of the second half of the season
    regularseasonenddate : str
        Leagues regular season end date
    postseasonstartdate : str
        Leagues post season start date
    postseasonenddate : str
        Leagues post season end date
    seasonenddate : str
        Leagues season end date
    offseasonstartdate : str
        Leagues off season start date
    offseasonenddate : str
        Leagues off season end date
    seasonlevelgamedaytype : str
        Leagues game day type
    gamelevelgamedaytype : str
        Leagues game day type
    qualifierplateappearances : str
        Qualfifier plate appearances
    qualifieroutspitched : str
        Qualifier outs pitched
    """
    seasonid: Optional[str] = None
    preseasonstartdate: Optional[str] = None
    preseasonenddate: Optional[str] = None
    seasonstartdate: Optional[str] = None
    springstartdate: Optional[str] = None
    springenddate: Optional[str] = None
    regularseasonstartdate: Optional[str] = None
    lastdate1sthalf: Optional[str] = None
    allstardate: Optional[str] = None
    firstdate2ndhalf: Optional[str] = None
    regularseasonenddate: Optional[str] = None
    postseasonstartdate: Optional[str] = None
    postseasonenddate: Optional[str] = None
    seasonenddate: Optional[str] = None
    offseasonstartdate: Optional[str] = None
    offseasonenddate: Optional[str] = None
    seasonlevelgamedaytype: Optional[str] = None
    gamelevelgamedaytype: Optional[str] = None
    qualifierplateappearances: Optional[str] = None
    qualifieroutspitched: Optional[str] = None
