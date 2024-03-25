from typing import Optional, Union
from dataclasses import dataclass, field
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team
from pydantic import BaseModel


class GameDataGame(BaseModel):
    """Represents this game's game info.

    Attributes:
        pk (int): This game's game id.
        type (str): This game's game type code.
        doubleHeader (str): Represents if this game is a doubleheader or not.
        id (str): An unknown Id.
        gamedayType (str): This game's gameday type code.
        tiebreaker (str): Indicates if this game is a tiebreaker.
        gameNumber (int): The game number for this game. If doubleheader, will be 2.
        calendarEventId (str): The id for this calendar event.
        season (str): This game's season year.
        seasonDisplay (str): This game's displayed season.
    """
    pk: int
    type: str
    doubleHeader: str
    id: str
    gamedayType: str
    tiebreaker: str
    gameNumber: int
    calendarEventId: Optional[str] = None
    season: str
    seasonDisplay: str


class GameDatetime(BaseModel):
    """Represents the date and time information for this game.

    Attributes:
        datetime (str): The date and time for this game.
        originalDate (str): The original scheduled date for this game.
        officialDate (str): The current scheduled date for this game.
        dayNight (str): The current lighting condition game type (e.g., "day" or "night").
        time (str): The time of the game.
        ampm (str): The game's AM or PM code.
        resumeDate (str, optional): The rescheduled date if the game was postponed. Default is None.
        resumeDatetime (str, optional): The rescheduled date and time if the game was postponed. Default is None.
        resumedFromDate (str, optional): The original date from which the game was resumed. Default is None.
        resumedFromDatetime (str, optional): The original date and time from which the game was resumed. Default is None.
    """
    dateTime: str
    originalDate: str
    officialDate: str
    dayNight: str
    time: str
    ampm: str
    resumeDate: Optional[str] = None
    resumeDateTime: Optional[str] = None
    resumedFromDate: Optional[str] = None
    resumedFromDateTime: Optional[str] = None



class GameStatus(BaseModel):
    """Represents this game's game status.

    Attributes:
        abstractGameState (str): The abstract game state, providing a general description of the game's current phase.
        codedGameState (str): The coded game state, offering a concise, coded representation of the game's status.
        detailedState (str): The detailed game state, giving an in-depth description of the current status of the game.
        statusCode (str): Status code for this game, providing a numeric or short coded representation of the game's state.
        startTimeTBD (bool): Indicates if the start time is to be determined (TBD).
        abstractGameCode (str): The abstract game code, a shorthand code summarizing the game state.
        reason (str): Reason for the current state. This is usually used for delays, cancellations, or other irregularities affecting the game.
    """
    abstractGameState: str
    codedGameState: str
    detailedState: str
    statusCode: str
    startTimeTBD: bool
    abstractGameCode: str
    reason: Optional[str] = None


class GameTeams(BaseModel):
    """Represents the home and away teams in a game.

    Attributes:
        away (Team): The away team.
        home (Team): The home team.
    """
    away: Team
    home: Team



class GameWeather(BaseModel):
    """Represents the weather conditions for this game.

    Attributes:
        condition (str): The weather condition (e.g., "Sunny", "Cloudy").
        temp (str): The temperature in Fahrenheit.
        wind (str, optional): The wind speed in MPH and direction. Default is None.
    """
    condition: str
    temp: str
    wind: Optional[str] = None


class GameInfo(BaseModel):
    """Represents the general information about this game.

    Attributes:
        attendance (int): The attendance number for this game.
        firstPitch (str): The time when the first pitch was thrown.
        gameDurationMinutes (int): The total duration of the game in minutes.
        delayDurationMinutes (int, optional): The total delay duration of the game in minutes. Default is None.
    """
    attendance: int
    firstPitch: str
    gameDurationMinutes: int
    delayDurationMinutes: Optional[int] = None


class ReviewInfo(BaseModel):
    """Represents the review information for a team in this game.

    Attributes:
        used (int): The number of challenges that have been used.
        remaining (int): The number of challenges remaining.
    """
    used: int
    remaining: int


class GameReview(BaseModel):
    """Represents the game review information for this game.

    Attributes:
        hasChallenges (bool): Indicates whether there are challenges in this game.
        away (ReviewInfo): Review information for the away team.
        home (ReviewInfo): Review information for the home team.
    """
    hasChallenges: bool
    away: ReviewInfo
    home: ReviewInfo



class GameFlags(BaseModel):
    """Represents various significant flags for this game.

    Attributes:
        noHitter (bool): Indicates if there is a no-hitter in this game.
        perfectGame (bool): Indicates if this game is a perfect game.
        awayTeamNoHitter (bool): Indicates if the away team has achieved a no-hitter.
        awayTeamPerfectGame (bool): Indicates if the away team has achieved a perfect game.
        homeTeamNoHitter (bool): Indicates if the home team has achieved a no-hitter.
        homeTeamPerfectGame (bool): Indicates if the home team has achieved a perfect game.
    """
    noHitter: bool
    perfectGame: bool
    awayTeamnoHitter: Optional[bool] = None
    awayTeamPerfectGame: bool
    homeTeamNoHitter: bool
    homeTeamPerfectGame: bool


class GameProbablePitchers(BaseModel):
    """Represents the probable pitchers for the home and away teams in this game.

    Attributes:
        away (Person): The probable pitcher for the away team.
        home (Person): The probable pitcher for the home team.
    """
    away: Person
    home: Person


class MoundVisits(BaseModel):
    """Represents the mound visits information for this game.

    Attributes:
        away (dict): Mound visits by the away team.
        home (dict): Mound visits by the home team.
    """
    away: dict = {}
    home: dict = {}

