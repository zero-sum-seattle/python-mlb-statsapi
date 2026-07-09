from typing import Optional, Any
from pydantic import Field, field_validator
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team


class GameDataGame(MLBBaseModel):
    """
    A class to represent the game's game info.

    Attributes
    ----------
    pk : int
        This game's game ID.
    type : str
        This game's game type code.
    double_header : str
        Represents if this game is a double header or not.
    id : str
        An unknown ID.
    gameday_type : str
        This game's gameday type code.
    tiebreaker : str
        Is this game a tie breaker.
    game_number : int
        The game number for this game. If double header will be 2.
    calendar_event_id : str
        The ID for this calendar event.
    season : str
        This game's season year.
    season_display : str
        This game's displayed season.
    """
    pk: int
    type: str
    double_header: str = Field(alias="doubleHeader")
    id: str
    gameday_type: str = Field(alias="gamedayType")
    tiebreaker: str
    game_number: int = Field(alias="gameNumber")
    calendar_event_id: Optional[str] = Field(default=None, alias="calendarEventId")
    season: str
    season_display: str = Field(alias="seasonDisplay")


class GameDatetime(MLBBaseModel):
    """
    A class to represent the date time for this game.

    Attributes
    ----------
    datetime : str
        Date time for this game.
    original_date : str
        The original scheduled date for this game.
    official_date : str
        The current scheduled date for this game.
    day_night : str
        The current lighting condition game type.
    time : str
        The time.
    ampm : str
        The game's am or pm code.
    resume_date : str
        Resume date if applicable.
    resume_datetime : str
        Resume datetime if applicable.
    resumed_from_date : str
        Resumed from date if applicable.
    resumed_from_datetime : str
        Resumed from datetime if applicable.
    """
    datetime: str = Field(alias="dateTime")
    original_date: str = Field(alias="originalDate")
    official_date: str = Field(alias="officialDate")
    day_night: str = Field(alias="dayNight")
    time: str
    ampm: str
    resume_date: Optional[str] = Field(default=None, alias="resumeDate")
    resume_datetime: Optional[str] = Field(default=None, alias="resumeDatetime")
    resumed_from_date: Optional[str] = Field(default=None, alias="resumedFromDate")
    resumed_from_datetime: Optional[str] = Field(default=None, alias="resumedFromDatetime")


class GameStatus(MLBBaseModel):
    """
    A class to represent this game's game status.

    Attributes
    ----------
    abstract_game_state : str
        The abstract game state.
    coded_game_state : str
        The coded game state.
    detailed_state : str
        The detailed game state.
    status_code : str
        Status code for this game.
    start_time_tbd : bool
        If the start time is TBD.
    abstract_game_code : str
        The abstract game code.
    reason : str
        Reason for a state. Usually used for delays or cancellations.
    """
    abstract_game_state: str = Field(alias="abstractGameState")
    coded_game_state: str = Field(alias="codedGameState")
    detailed_state: str = Field(alias="detailedState")
    status_code: str = Field(alias="statusCode")
    start_time_tbd: Optional[bool] = Field(default=None, alias="startTimeTbd")
    abstract_game_code: str = Field(alias="abstractGameCode")
    reason: Optional[str] = None


class GameTeams(MLBBaseModel):
    """
    A class to represent the home and away teams.

    Attributes
    ----------
    away : Team
        Away team.
    home : Team
        Home team.
    """
    away: Team
    home: Team


class GameWeather(MLBBaseModel):
    """
    A class to represent the weather for this game.

    Attributes
    ----------
    condition : str
        The weather condition.
    temp : str
        The temperature in F.
    wind : str
        The wind in MPH and the direction.
    """
    condition: str
    temp: str
    wind: Optional[str] = None


class GameInfo(MLBBaseModel):
    """
    A class to represent the game info for this game.

    Attributes
    ----------
    first_pitch : str
        The time of the first pitch.
    attendance : int
        The attendance for this game.
    game_duration_minutes : int
        The duration of the game in minutes.
    delay_duration_minutes : int
        The length of delay for the game in minutes.
    """
    first_pitch: str = Field(alias="firstPitch")
    attendance: Optional[int] = None
    game_duration_minutes: Optional[int] = Field(default=None, alias="gameDurationMinutes")
    delay_duration_minutes: Optional[int] = Field(default=None, alias="delayDurationMinutes")


class ReviewInfo(MLBBaseModel):
    """
    A class to represent review info for each team in this game.

    Attributes
    ----------
    used : int
        How many challenges used.
    remaining : int
        How many challenges are remaining.
    """
    used: int
    remaining: int


class GameReview(MLBBaseModel):
    """
    A class to represent the Game Reviews for this game.

    Attributes
    ----------
    has_challenges : bool
        If there are challenges.
    away : ReviewInfo
        Away team review info.
    home : ReviewInfo
        Home team review info.
    """
    has_challenges: bool = Field(alias="hasChallenges")
    away: ReviewInfo
    home: ReviewInfo


class AbsChallengeInfo(MLBBaseModel):
    """
    A class to represent ABS challenge info for each team in this game.

    Attributes
    ----------
    used_successful : int
        How many successful ABS challenges were used.
    used_failed : int
        How many failed ABS challenges were used.
    remaining : int
        How many ABS challenges are remaining.
    """
    used_successful: int = Field(alias="usedSuccessful")
    used_failed: int = Field(alias="usedFailed")
    remaining: int


class AbsChallenges(MLBBaseModel):
    """
    A class to represent ABS challenge information for this game.

    Attributes
    ----------
    has_challenges : bool
        If ABS challenges are available.
    away : AbsChallengeInfo
        Away team ABS challenge info.
    home : AbsChallengeInfo
        Home team ABS challenge info.
    """
    has_challenges: bool = Field(alias="hasChallenges")
    away: AbsChallengeInfo
    home: AbsChallengeInfo


class GameFlags(MLBBaseModel):
    """
    A class to represent the flags for this game.

    Attributes
    ----------
    no_hitter : bool
        If there is a no hitter in this game.
    perfect_game : bool
        If this game is a perfect game.
    away_team_no_hitter : bool
        If the away team has a no hitter.
    away_team_perfect_game : bool
        If the away team has a perfect game.
    home_team_no_hitter : bool
        If the home team has a no hitter.
    home_team_perfect_game : bool
        If the home team has a perfect game.
    """
    no_hitter: bool = Field(alias="noHitter")
    perfect_game: bool = Field(alias="perfectGame")
    away_team_no_hitter: bool = Field(alias="awayTeamNoHitter")
    away_team_perfect_game: bool = Field(alias="awayTeamPerfectGame")
    home_team_no_hitter: bool = Field(alias="homeTeamNoHitter")
    home_team_perfect_game: bool = Field(alias="homeTeamPerfectGame")


class GameProbablePitchers(MLBBaseModel):
    """
    A class to represent the home and away probable pitchers for this game.

    Attributes
    ----------
    home : Person
        Home team probable pitcher.
    away : Person
        Away team probable pitcher.
    """
    away: Optional[Person] = None
    home: Optional[Person] = None

    @field_validator('away', 'home', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class MoundVisits(MLBBaseModel):
    """
    A class to represent the mound visits for a game.

    Attributes
    ----------
    home : dict
        Home team mound visits.
    away : dict
        Away team mound visits.
    """
    away: dict = {}
    home: dict = {}
