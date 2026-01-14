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
    game_pk: int = Field(alias="gamePk")
    link: str
    content: AttendanceHighLowGameContent
    day_night: str = Field(alias="dayNight")


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
    openings_total: int = Field(alias="openingsTotal")
    openings_total_away: int = Field(alias="openingsTotalAway")
    openings_total_home: int = Field(alias="openingsTotalHome")
    openings_total_lost: int = Field(alias="openingsTotalLost")
    games_total: int = Field(alias="gamesTotal")
    games_away_total: int = Field(alias="gamesAwayTotal")
    games_home_total: int = Field(alias="gamesHomeTotal")
    year: str
    attendance_average_ytd: int = Field(alias="attendanceAverageYtd")
    game_type: AttendanceGameType = Field(alias="gameType")
    team: Team
    attendance_total: Optional[int] = Field(default=None, alias="attendanceTotal")
    attendance_average_away: Optional[int] = Field(default=None, alias="attendanceAverageAway")
    attendance_average_home: Optional[int] = Field(default=None, alias="attendanceAverageHome")
    attendance_high: Optional[int] = Field(default=None, alias="attendanceHigh")
    attendance_high_date: Optional[str] = Field(default=None, alias="attendanceHighDate")
    attendance_high_game: Optional[AttendanceHighLowGame] = Field(default=None, alias="attendanceHighGame")
    attendance_low: Optional[int] = Field(default=None, alias="attendanceLow")
    attendance_low_date: Optional[str] = Field(default=None, alias="attendanceLowDate")
    attendance_low_game: Optional[AttendanceHighLowGame] = Field(default=None, alias="attendanceLowGame")
    attendance_total_away: Optional[int] = Field(default=None, alias="attendanceTotalAway")
    attendance_total_home: Optional[int] = Field(default=None, alias="attendanceTotalHome")
    attendance_opening_average: Optional[int] = Field(default=None, alias="attendanceOpeningAverage")


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
    openings_total_away: int = Field(alias="openingsTotalAway")
    openings_total_home: int = Field(alias="openingsTotalHome")
    openings_total_lost: int = Field(alias="openingsTotalLost")
    openings_total_ytd: int = Field(alias="openingsTotalYtd")
    attendance_average_ytd: int = Field(alias="attendanceAverageYtd")
    attendance_high: int = Field(alias="attendanceHigh")
    attendance_high_date: str = Field(alias="attendanceHighDate")
    attendance_total: int = Field(alias="attendanceTotal")
    attendance_total_away: int = Field(alias="attendanceTotalAway")
    attendance_total_home: int = Field(alias="attendanceTotalHome")
    attendance_average_away: Optional[int] = Field(default=None, alias="attendanceAverageAway")
    attendance_average_home: Optional[int] = Field(default=None, alias="attendanceAverageHome")
