from typing import Optional
from dataclasses import dataclass


@dataclass(repr=False)
class Season:
    """
    This class represents a season object

    Attributes
    ----------
    seasonid : str
        season id
    haswildcard :  bool
        wild card status
    preseasonstartdate : str
        pre-season start date
    preseasonenddate : str
        pre-season end date
    seasonstartdate : str
        season start date
    springstartdate : str
        spring start date
    springenddate : str
        spring end date
    regularseasonstartdate : str
        regular season start date
    lastdate1sthalf : str
        last date 1st half
    allstardate : str
        all star date
    firstdate2ndhalf : str
        first date 2nd half
    regularseasonenddate : str
        regular season end date
    postseasonstartdate : str
        post season start date
    postseasonenddate : str
        post season end date
    seasonenddate : str
        season end date
    offseasonstartdate : str
        off season start date
    offseasonenddate : str
        off season end date
    seasonlevelgamedaytype : str
        season level game day type
    gamelevelgamedaytype : str
        game level game day type
    qualifierplateappearances :  float
        qualifier plate appearances
    qualifieroutspitched : int
        qualifier outs pitched
    """

    seasonid: str
    haswildcard: Optional[bool] = None
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
    qualifierplateappearances: Optional[float] = None
    qualifieroutspitched: Optional[int] = None

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))