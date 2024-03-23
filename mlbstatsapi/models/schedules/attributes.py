from dataclasses import dataclass, field
from typing import Optional, Union, List, Any
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.game.gamedata import GameStatus
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.standings import LeagueRecord
from pydantic import BaseModel


class ScheduleGameTeam(BaseModel):
    """Represents the scheduled games teams' schedule information in a Scheduled Dates game.

    Attributes:
        leagueRecord (Union[LeagueRecord, dict]): League record for this team.
        team (Union[Team, dict]): Team info for this game.
        splitSquad (bool): Indicates if it's a split squad.
        seriesNumber (Optional[int]): Series number.
        score (Optional[int]): Current score for this team in this game.
        isWinner (Optional[bool]): Indicates if this team is the winner of this game.
    """
    leagueRecord: Union[LeagueRecord, dict]
    team: Union[Team, dict]
    splitSquad: bool
    seriesNumber: Optional[int] = None
    score: Optional[int] = None
    isWinner: Optional[bool] = None


class ScheduleHomeAndAway(BaseModel):
    """Represents both away and home teams in a Schedule's Dates game.

    Attributes:
        home (ScheduleGameTeam): Home team info for this game.
        away (ScheduleGameTeam): Away team info for this game.
    """
    home: ScheduleGameTeam
    away: ScheduleGameTeam


class ScheduleGames(BaseModel):
    """Represents a Game in a Schedule's Dates.

    Attributes:
        gamePk (int): The game's ID number.
        link (str): The link for this game.
        gameType (str): This game's game type.
        season (str): The season this game takes place in.
        gameDate (str): The date for this game.
        officialDate (str): The official date for this game.
        status (Union[GameStatus, dict[str, Any]]): The status of this game.
        teams (Union[ScheduleHomeAndAway, dict[str, Any]]): Holds teams and their info for this game.
        venue (Union[Venue, dict[str, Any]]): The venue this game takes place in.
        content (dict): Content for this game. Haven't found a populated reference yet; stays as dict.
        gameNumber (int): Game number for this game.
        publicFacing (bool): If this game is public facing.
        doubleHeader (str): The doubleheader status for this game, "n", "y"?
        gamedayType (str): The type of gameday for this game.
        tiebreaker (str): Tiebreaker for this game, 'n', 'y'?
        calendarEventID (str): Calendar event ID for this game.
        seasonDisplay (str): Displayed season for this game.
        dayNight (str): Day or night game as a string, 'am', 'pm'?
        scheduledInnings (int): Number of scheduled innings for the game.
        reverseHomeAwayStatus (bool): If reverse home and away status is applied.
        seriesDescription (str): Description of this current series.
        recordSource (str): Record source.
        ifNecessary (str): If necessary.
        ifNecessaryDescription (str): If necessary description.
        gameGuid (Optional[str]): The game's GUID.
        inningBreakLength (Optional[int]): Length of break between innings.
        gamesInSeries (Optional[int]): Number of games in the current series.
        seriesGameNumber (Optional[int]): Game number in the current series.
        rescheduleDate (Optional[str]): If the game is rescheduled, this is the rescheduled date.
        rescheduleGameDate (Optional[str]): Rescheduled game date.
        rescheduledFrom (Optional[str]): Rescheduled from.
        rescheduledFromDate (Optional[str]): Rescheduled from date.
        isTie (Optional[bool]): Indicates if the game is a tie.
    """
    gamePk: int
    link: str
    gameType: str
    season: str
    gameDate: str
    officialDate: str
    venue: Union[Venue, dict[str, Any]]
    content: dict
    gameNumber: int
    publicFacing: bool
    doubleHeader: str
    gamedayType: str
    tiebreaker: str
    calendarEventID: str
    seasonDisplay: str
    dayNight: str
    scheduledInnings: int
    reverseHomeAwayStatus: bool
    seriesDescription: str
    recordSource: str
    ifNecessary: str
    ifNecessaryDescription: str
    status: Union[GameStatus, dict[str, Any]]
    teams: Union[ScheduleHomeAndAway, dict[str, Any]]
    gameGuid: Optional[str] = None
    description: Optional[str] = None
    inningBreakLength: Optional[int] = None
    rescheduleDate: Optional[str] = None
    rescheduleGameDate: Optional[str] = None
    rescheduledFrom: Optional[str] = None
    rescheduledFromDate: Optional[str] = None
    isTie: Optional[bool] = None
    resumeDate: Optional[str] = None
    resumeGameDate: Optional[str] = None
    resumedFrom: Optional[str] = None
    resumedFromDate: Optional[str] = None
    seriesGameNumber: Optional[int] = None
    gamesInSeries: Optional[int] = None


class ScheduleDates(BaseModel):
    """Represents a Schedules Dates.

    Attributes:
        date (str): Date for the group of games.
        totalItems (int): Total amount of items for this date.
        totalEvents (int): The number of events for this date.
        totalGames (int): The number of games for this date.
        totalGamesInProgress (int): The number of games that are currently in progress for this date.
        games (List[ScheduleGames]): A list of games for this date.
        events (List[None]): A list of events for this date. This attribute is currently a placeholder,
            as a populated reference for the event objects is not available. It remains as a list for now.
    """
    date: str
    totalItems: int
    totalEvents: int
    totalGames: int
    totalGamesInProgress: int
    events: List[None] # empty
    games: List[ScheduleGames]

