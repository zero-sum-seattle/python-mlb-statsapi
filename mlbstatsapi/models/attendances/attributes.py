from dataclasses import dataclass, field
from typing import Optional, Union
from mlbstatsapi.models.teams import Team


@dataclass
class AttendanceHighLowGameContent:
    """
    A class to represent attendance records.
    Attributes
    ----------
    link : str
        games content endpoint link
    """
    link: str


@dataclass
class AttendanceHighLowGame:
    """
    A class to represent attendance High and Low games.
    Attributes
    ----------
    gamepk : int
        Games Id number
    link : str
        games endpoint link
    content : AttendanceHighLowGameContent
        Content for this game
    daynight : str
        Type of time of day for game
    """
    gamepk: int
    link: str
    content: Union[AttendanceHighLowGameContent, dict]
    daynight: str

    def __post_init__(self):
        self.content = AttendanceHighLowGameContent(**self.content)


@dataclass
class AttendenceGameType:
    """
    A class to represent Attendance Game Type.
    Attributes
    ----------
    id : str
        Game type id 
    description : str
        Game type description
    """
    id: str
    description: str


@dataclass(repr=False)
class AttendanceRecords:
    """
    A class to represent attendance records.
    Attributes
    ----------
    openingstotal : int
        Total amount of openings
    openingstotalaway : int
        Total amount of opening away games
    openingstotalhome : int
        Total amount of opening home games
    openingstotallost : int
        Total amount of openings lost
    gamestotal : int
        Total amount of games
    gamesawaytotal : int
        Total amount of away games
    gameshometotal : int
        Total amount of home games
    year : str
        Year as a string
    attendanceaverageaway : int
        Average attendance for away games
    attendanceaveragehome : int
        Average attendance for home games
    attendanceaverageytd : int
        Average attendance year to date
    attendancehigh : int
        Attendance High number
    attendancehighdate : str
        Attendance high date
    attendancehighgame : AttendanceHighLowGame
        Attendance high game
    attendancelow : int
        Attendance low number
    attendancelowdate : str
         Attendance low date
    attendancelowgame : AttendanceHighLowGame
         Attendance low game
    attendanceopeningaverage : int
         Attendance opening average
    attendancetotal : int
        Attendance total
    attendancetotalaway : int
        Attendance total away
    attendancetotalhome : int
        Attendance total home
    gametype : AttendenceGameType
        Game type
    team : Team
        Team
    """
    openingstotal: int
    openingstotalaway: int
    openingstotalhome: int
    openingstotallost: int
    gamestotal: int
    gamesawaytotal: int
    gameshometotal: int
    year: str
    attendanceaverageytd: int
    attendancetotal: int
    gametype: Union[AttendenceGameType, dict]
    team: Union[Team, dict]
    attendanceaverageaway: Optional[int] = None
    attendanceaveragehome: Optional[int] = None
    attendancehigh: Optional[int] = None
    attendancehighdate: Optional[str] = None
    attendancehighgame: Optional[Union[AttendanceHighLowGame, dict]] = None
    attendancelow: Optional[int] = None
    attendancelowdate: Optional[str] = None
    attendancelowgame: Optional[Union[AttendanceHighLowGame, dict]] = None
    attendancetotalaway: Optional[int] = None
    attendancetotalhome: Optional[int] = None
    attendanceopeningaverage: Optional[int] = None

    def __post_init__(self):
        self.attendancehighgame = AttendanceHighLowGame(**self.attendancehighgame) if self.attendancehighgame else self.attendancehighgame
        self.attendancelowgame = AttendanceHighLowGame(**self.attendancelowgame) if self.attendancelowgame else self.attendancelowgame
        self.gameType = AttendenceGameType(**self.gametype)
        self.team = Team(**self.team)

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass(repr=False)
class AttendanceTotals:
    """
    A class to represent attendance aggregate toatls.
    Attributes
    ----------
    openingstotalaway : int
        Total amount of opening game attendance number
    openingstotalhome : int
        Total amount of opening home game attendance number
    openingstotallost : int
        Total amount of opening games lost
    openingstotalytd : int
        Total amount of opening games year to date
    attendanceaverageaway : int
        Average away game attendance
    attendanceaveragehome : int
        Average home game attendance
    attendanceaverageytd : int
        Average attendance year to date
    attendancehigh : int
        Attendance high
    attendancehighdate : str
        Attendance high date
    attendancetotal : int
        Attendance total
    attendancetotalaway : int
        Attendace total away
    attendancetotalhome : int
        Attendance total home
    """
    openingstotalaway: int
    openingstotalhome: int
    openingstotallost: int
    openingstotalytd: int
    attendanceaverageytd: int
    attendancehigh: int
    attendancehighdate: str
    attendancetotal: int
    attendancetotalaway: int
    attendancetotalhome: int
    attendanceaverageaway: Optional[int] = None
    attendanceaveragehome: Optional[int] = None

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))