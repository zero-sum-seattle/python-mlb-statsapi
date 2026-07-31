from typing import Optional, List, Any
from pydantic import Field, field_validator
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.game.gamedata import GameStatus
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.leagues import LeagueRecord


class ScheduleGameTeam(MLBBaseModel):
    """
    A class to represent the scheduled game's team schedule information.

    Attributes
    ----------
    league_record : LeagueRecord
        League record for this team.
    team : Team
        Team info for this game.
    split_squad : bool
        Split squad.
    series_number : int
        Series number.
    score : int
        Current score for this team in this game.
    is_winner : bool
        If this team is the winner of this game.
    """
    league_record: LeagueRecord = Field(alias="leagueRecord")
    team: Team
    split_squad: bool = Field(alias="splitSquad")
    series_number: Optional[int] = Field(default=None, alias="seriesNumber")
    score: Optional[int] = None
    is_winner: Optional[bool] = Field(default=False, alias="isWinner")


class ScheduleHomeAndAway(MLBBaseModel):
    """
    A class to represent both away and home teams in a schedule's game.

    Attributes
    ----------
    home : ScheduleGameTeam
        Home team info for this game.
    away : ScheduleGameTeam
        Away team info for this game.
    """
    home: ScheduleGameTeam
    away: ScheduleGameTeam


class ScheduleGames(MLBBaseModel):
    """
    A class to represent a game in a schedule's dates.

    Attributes
    ----------
    game_pk : int
        The game's ID number.
    link : str
        The link for this game.
    game_type : str
        This game's game type.
    season : str
        The season this game takes place in.
    game_date : str
        The date for this game.
    official_date : str
        The official date for this game.
    status : GameStatus
        The status of this game.
    teams : ScheduleHomeAndAway
        Holds teams and their info for this game.
    venue : Venue
        The venue this game takes place in.
    content : dict
        Content for this game.
    is_tie : bool
        If this game is a tie.
    game_number : int
        Game number for this game.
    public_facing : bool
        Is this game public facing.
    double_header : str
        The double header status for this game.
    gameday_type : str
        The type of gameday for this game.
    tiebreaker : str
        Tie breaker for this game.
    calendar_event_id : str
        Calendar event ID for this game.
    season_display : str
        Displayed season for this game.
    day_night : str
        Day or night game as a string.
    scheduled_innings : int
        Number of scheduled innings for the game.
    reverse_home_away_status : bool
        If reverse home and away.
    series_description : str
        Description of this current series.
    record_source : str
        Record source.
    if_necessary : str
        If necessary.
    if_necessary_description : str
        If necessary description.
    game_guid : str
        The game's GUID.
    description : str
        Game description.
    inning_break_length : int
        Length of break between innings.
    games_in_series : int
        Number of games in current series.
    series_game_number : int
        Game number in the current series.
    reschedule_date : str
        Rescheduled date if applicable.
    reschedule_game_date : str
        Rescheduled game date.
    rescheduled_from : str
        Rescheduled from.
    rescheduled_from_date : str
        Rescheduled from date.
    resume_date : str
        Resume date.
    resume_game_date : str
        Resume game date.
    resumed_from : str
        Resumed from.
    resumed_from_date : str
        Resumed from date.
    """
    game_pk: int = Field(alias="gamePk")
    link: str
    game_type: str = Field(alias="gameType")
    season: str
    game_date: str = Field(alias="gameDate")
    official_date: str = Field(alias="officialDate")
    venue: Venue
    content: dict
    game_number: int = Field(alias="gameNumber")
    public_facing: bool = Field(alias="publicFacing")
    double_header: str = Field(alias="doubleHeader")
    gameday_type: str = Field(alias="gamedayType")
    tiebreaker: str
    calendar_event_id: Optional[str] = Field(default=None, alias="calendarEventID")
    season_display: str = Field(alias="seasonDisplay")
    day_night: str = Field(alias="dayNight")
    scheduled_innings: int = Field(alias="scheduledInnings")
    reverse_home_away_status: bool = Field(alias="reverseHomeAwayStatus")
    series_description: str = Field(alias="seriesDescription")
    record_source: str = Field(alias="recordSource")
    if_necessary: str = Field(alias="ifNecessary")
    if_necessary_description: str = Field(alias="ifNecessaryDescription")
    status: Optional[GameStatus] = None
    teams: Optional[ScheduleHomeAndAway] = None
    game_guid: Optional[str] = Field(default=None, alias="gameGuid")
    description: Optional[str] = None
    inning_break_length: Optional[int] = Field(default=None, alias="inningBreakLength")
    reschedule_date: Optional[str] = Field(default=None, alias="rescheduleDate")
    reschedule_game_date: Optional[str] = Field(default=None, alias="rescheduleGameDate")
    rescheduled_from: Optional[str] = Field(default=None, alias="rescheduledFrom")
    rescheduled_from_date: Optional[str] = Field(default=None, alias="rescheduledFromDate")
    is_tie: Optional[bool] = Field(default=None, alias="isTie")
    resume_date: Optional[str] = Field(default=None, alias="resumeDate")
    resume_game_date: Optional[str] = Field(default=None, alias="resumeGameDate")
    resumed_from: Optional[str] = Field(default=None, alias="resumedFrom")
    resumed_from_date: Optional[str] = Field(default=None, alias="resumedFromDate")
    series_game_number: Optional[int] = Field(default=None, alias="seriesGameNumber")
    games_in_series: Optional[int] = Field(default=None, alias="gamesInSeries")

    @field_validator('status', 'teams', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class ScheduleDates(MLBBaseModel):
    """
    A class to represent a schedule's dates.

    Attributes
    ----------
    date : str
        Date for the group of games.
    total_items : int
        Total amount of items for this date.
    total_events : int
        The number of events for this date.
    total_games : int
        The number of games for this date.
    total_games_in_progress : int
        The number of games that are currently in progress for this date.
    games : List[ScheduleGames]
        A list of games for this date.
    events : list
        A list of events for this date.
    """
    date: str
    total_items: int = Field(alias="totalItems")
    total_events: int = Field(alias="totalEvents")
    total_games: int = Field(alias="totalGames")
    total_games_in_progress: int = Field(alias="totalGamesInProgress")
    events: List = []
    games: List[ScheduleGames] = []
