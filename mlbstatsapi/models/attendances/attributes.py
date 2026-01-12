from typing import Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.teams import Team


class AttendanceHighLowGameContent(MLBBaseModel):
    """
    A class to represent attendance game content.

    Attributes
    ----------
    link : str
        Games content endpoint link.
    """
    link: str


class AttendanceHighLowGame(MLBBaseModel):
    """
    A class to represent attendance high and low games.

    Attributes
    ----------
    game_pk : int
        Game's ID number.
    link : str
        Games endpoint link.
    content : AttendanceHighLowGameContent
        Content for this game.
    day_night : str
        Time of day for game (day or night).
    """
    game_pk: int = Field(alias="gamepk")
    link: str
    content: AttendanceHighLowGameContent
    day_night: str = Field(alias="daynight")


class AttendanceGameType(MLBBaseModel):
    """
    A class to represent attendance game type.

    Attributes
    ----------
    id : str
        Game type ID.
    description : str
        Game type description.
    """
    id: str
    description: str


class AttendanceRecords(MLBBaseModel):
    """
    A class to represent attendance records.

    Attributes
    ----------
    openings_total : int
        Total number of openings.
    openings_total_away : int
        Total number of opening away games.
    openings_total_home : int
        Total number of opening home games.
    openings_total_lost : int
        Total number of openings lost.
    games_total : int
        Total number of games.
    games_away_total : int
        Total number of away games.
    games_home_total : int
        Total number of home games.
    year : str
        Year as a string.
    attendance_average_away : int
        Average attendance for away games.
    attendance_average_home : int
        Average attendance for home games.
    attendance_average_ytd : int
        Average attendance year to date.
    attendance_high : int
        Attendance high number.
    attendance_high_date : str
        Attendance high date.
    attendance_high_game : AttendanceHighLowGame
        Attendance high game.
    attendance_low : int
        Attendance low number.
    attendance_low_date : str
        Attendance low date.
    attendance_low_game : AttendanceHighLowGame
        Attendance low game.
    attendance_opening_average : int
        Attendance opening average.
    attendance_total : int
        Attendance total.
    attendance_total_away : int
        Attendance total away.
    attendance_total_home : int
        Attendance total home.
    game_type : AttendanceGameType
        Game type.
    team : Team
        Team.
    """
    openings_total: int = Field(alias="openingstotal")
    openings_total_away: int = Field(alias="openingstotalaway")
    openings_total_home: int = Field(alias="openingstotalhome")
    openings_total_lost: int = Field(alias="openingstotallost")
    games_total: int = Field(alias="gamestotal")
    games_away_total: int = Field(alias="gamesawaytotal")
    games_home_total: int = Field(alias="gameshometotal")
    year: str
    attendance_average_ytd: int = Field(alias="attendanceaverageytd")
    game_type: AttendanceGameType = Field(alias="gametype")
    team: Team
    attendance_total: Optional[int] = Field(default=None, alias="attendancetotal")
    attendance_average_away: Optional[int] = Field(default=None, alias="attendanceaverageaway")
    attendance_average_home: Optional[int] = Field(default=None, alias="attendanceaveragehome")
    attendance_high: Optional[int] = Field(default=None, alias="attendancehigh")
    attendance_high_date: Optional[str] = Field(default=None, alias="attendancehighdate")
    attendance_high_game: Optional[AttendanceHighLowGame] = Field(default=None, alias="attendancehighgame")
    attendance_low: Optional[int] = Field(default=None, alias="attendancelow")
    attendance_low_date: Optional[str] = Field(default=None, alias="attendancelowdate")
    attendance_low_game: Optional[AttendanceHighLowGame] = Field(default=None, alias="attendancelowgame")
    attendance_total_away: Optional[int] = Field(default=None, alias="attendancetotalaway")
    attendance_total_home: Optional[int] = Field(default=None, alias="attendancetotalhome")
    attendance_opening_average: Optional[int] = Field(default=None, alias="attendanceopeningaverage")


class AttendanceTotals(MLBBaseModel):
    """
    A class to represent attendance aggregate totals.

    Attributes
    ----------
    openings_total_away : int
        Total opening game attendance number for away games.
    openings_total_home : int
        Total opening home game attendance number.
    openings_total_lost : int
        Total number of opening games lost.
    openings_total_ytd : int
        Total number of opening games year to date.
    attendance_average_away : int
        Average away game attendance.
    attendance_average_home : int
        Average home game attendance.
    attendance_average_ytd : int
        Average attendance year to date.
    attendance_high : int
        Attendance high.
    attendance_high_date : str
        Attendance high date.
    attendance_total : int
        Attendance total.
    attendance_total_away : int
        Attendance total away.
    attendance_total_home : int
        Attendance total home.
    """
    openings_total_away: int = Field(alias="openingstotalaway")
    openings_total_home: int = Field(alias="openingstotalhome")
    openings_total_lost: int = Field(alias="openingstotallost")
    openings_total_ytd: int = Field(alias="openingstotalytd")
    attendance_average_ytd: int = Field(alias="attendanceaverageytd")
    attendance_high: int = Field(alias="attendancehigh")
    attendance_high_date: str = Field(alias="attendancehighdate")
    attendance_total: int = Field(alias="attendancetotal")
    attendance_total_away: int = Field(alias="attendancetotalaway")
    attendance_total_home: int = Field(alias="attendancetotalhome")
    attendance_average_away: Optional[int] = Field(default=None, alias="attendanceaverageaway")
    attendance_average_home: Optional[int] = Field(default=None, alias="attendanceaveragehome")
