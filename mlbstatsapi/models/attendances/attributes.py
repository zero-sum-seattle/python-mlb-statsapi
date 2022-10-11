from dataclasses import dataclass, field
from typing import Dict, Union, Any
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
    gamePk: int
    link: str
    content: Union[AttendanceHighLowGameContent, Dict[str, Any]]
    dayNight: str

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
    openingsTotal: int
    openingsTotalAway: int 
    openingsTotalHome: int
    openingsTotalLost: int
    gamesTotal: int
    gamesAwayTotal: int
    gamesHomeTotal: int
    year: str
    attendanceAverageYtd: int
    attendanceTotal: int
    gameType: Union[AttendenceGameType, Dict[str, Any]]
    team: Union[Team, Dict[str, Any]]
    attendanceAverageAway: int = None
    attendanceAverageHome: int = None
    attendanceHigh: int = None
    attendanceHighDate: str  = None
    attendanceHighGame: Union[AttendanceHighLowGame, Dict[str, Any]] = None
    attendanceLow: int = None
    attendanceLowDate: str  = None
    attendanceLowGame: Union[AttendanceHighLowGame, Dict[str, Any]] = None
    attendanceTotalAway: int = None
    attendanceTotalHome: int = None
    attendanceOpeningAverage: int = None

    def __post_init__(self):
        self.attendanceHighGame = AttendanceHighLowGame(**self.attendanceHighGame) if self.attendanceHighGame else self.attendanceHighGame
        self.attendanceLowGame = AttendanceHighLowGame(**self.attendanceLowGame) if self.attendanceLowGame else self.attendanceLowGame
        self.gameType = AttendenceGameType(**self.gameType)
        self.team = Team(**self.team)

@dataclass
class AttendanceAggregateTotals:
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
    openingsTotalAway: int
    openingsTotalHome: int
    openingsTotalLost: int
    openingsTotalYtd: int
    attendanceAverageYtd: int
    attendanceHigh: int
    attendanceHighDate: str
    attendanceTotal: int
    attendanceTotalAway: int
    attendanceTotalHome: int
    attendanceAverageAway: int = None
    attendanceAverageHome: int = None