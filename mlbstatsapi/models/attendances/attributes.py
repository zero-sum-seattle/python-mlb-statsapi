from dataclasses import dataclass, field
from typing import Optional, Union
from mlbstatsapi.models.teams import Team
from pydantic import BaseModel

class AttendanceHighLowGameContent(BaseModel):
    """
    A class to represent attendance records.
    Attributes
    ----------
    link : str
        games content endpoint link
    """
    link: str


class AttendanceHighLowGame(BaseModel):
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
    gamePk: int
    link: str
    content: Union[AttendanceHighLowGameContent, dict]
    dayNight: str

class AttendenceGameType(BaseModel):
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


class AttendanceRecords(BaseModel):
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
    gameType: AttendenceGameType
    team: Team
    attendanceAverageAway: Optional[int] = None
    attendanceAverageHome: Optional[int] = None
    attendanceHigh: Optional[int] = None
    attendanceHighDate: Optional[str] = None
    attendanceHighGame: Optional[AttendanceHighLowGame] = None
    attendanceLow: Optional[int] = None
    attendanceLowDate: Optional[str] = None
    attendanceLowGame: Optional[AttendanceHighLowGame] = None
    attendanceTotalAway: Optional[int] = None
    attendanceTotalHome: Optional[int] = None
    attendanceOpeningAverage: Optional[int] = None

class AttendanceTotals(BaseModel):
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
    attendanceAverageAway: Optional[int] = None
    attendanceAverageHome: Optional[int] = None

