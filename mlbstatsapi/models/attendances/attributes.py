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
    gamePk : int
        Games Id number
    link : str
        games endpoint link
    content : AttendanceHighLowGameContent
        Content for this game
    dayNight : str
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

@dataclass
class AttendanceRecords:
    """
    A class to represent attendance records.
    Attributes
    ----------
    openingsTotal : int
        Total amount of openings
    openingsTotalAway : int 
        Total amount of opening away games
    openingsTotalHome : int
        Total amount of opening home games
    openingsTotalLost : int
        Total amount of openings lost
    gamesTotal : int
        Total amount of games
    gamesAwayTotal : int
        Total amount of away games
    gamesHomeTotal : int
        Total amount of home games
    year : str
        Year as a string
    attendanceAverageAway : int = None
        Average attendance for away games
    attendanceAverageHome : int = None
        Average attendance for home games
    attendanceAverageYtd : int
        Average attendance year to date
    attendanceHigh : int = None
        Attendance High number
    attendanceHighDate : str = None 
        Attendance high date
    attendanceHighGame : AttendanceHighLowGame = None
        Attendance high game
    attendanceLow : int = None
        Attendance low number
    attendanceLowDate : str = None 
         Attendance low date
    attendanceLowGame : AttendanceHighLowGame = None
         Attendance low game
    attendanceOpeningAverage : int = None
         Attendance opening average
    attendanceTotal : int
        Attendance total
    attendanceTotalAway : int = None
        Attendance total away
    attendanceTotalHome : int = None
        Attendance total home
    gameType : AttendenceGameType
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
    attendancehighdate: Optional[str ] = None
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

@dataclass
class AttendanceTotals:
    """
    A class to represent attendance aggregate toatls.
    Attributes
    ----------
    openingsTotalAway : int
        Total amount of opening game attendance number
    openingsTotalHome : int
        Total amount of opening home game attendance number
    openingsTotalLost : int
        Total amount of opening games lost
    openingsTotalYtd : int
        Total amount of opening games year to date
    attendanceAverageAway : int = None
        Average away game attendance
    attendanceAverageHome : int = None
        Average home game attendance
    attendanceAverageYtd : int
        Average attendance year to date
    attendanceHigh : int
        Attendance high
    attendanceHighDate : str
        Attendance high date
    attendanceTotal : int
        Attendance total
    attendanceTotalAway : int
        Attendace total away
    attendanceTotalHome : int
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