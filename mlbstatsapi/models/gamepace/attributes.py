from typing import Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.sports import Sport


class PrPortalCalculatedFields(MLBBaseModel):
    """
    A class representing the calculated fields for a baseball game.

    Attributes
    ----------
    total_7_inn_games : int
        The total number of 7-inning games played.
    total_9_inn_games : int
        The total number of 9-inning games played.
    total_extra_inn_games : int
        The total number of extra-inning games played.
    time_per_7_inn_game : str
        The average time per 7-inning game.
    time_per_9_inn_game : str
        The average time per 9-inning game.
    time_per_extra_inn_game : str
        The average time per extra-inning game.
    """
    total_7_inn_games: Optional[int] = Field(default=None, alias="total7inngames")
    total_9_inn_games: Optional[int] = Field(default=None, alias="total9inngames")
    total_extra_inn_games: Optional[int] = Field(default=None, alias="totalextrainngames")
    time_per_7_inn_game: Optional[str] = Field(default=None, alias="timeper7inngame")
    time_per_9_inn_game: Optional[str] = Field(default=None, alias="timeper9inngame")
    time_per_extra_inn_game: Optional[str] = Field(default=None, alias="timeperextrainngame")


class GamePaceData(MLBBaseModel):
    """
    A class representing game pace data for a league, team, or sport.

    Attributes
    ----------
    hits_per_9_inn : float
        The number of hits per 9 innings played.
    runs_per_9_inn : float
        The number of runs scored per 9 innings played.
    pitches_per_9_inn : float
        The number of pitches thrown per 9 innings played.
    plate_appearances_per_9_inn : float
        The number of plate appearances per 9 innings played.
    hits_per_game : float
        The number of hits per game played.
    runs_per_game : float
        The number of runs scored per game played.
    innings_played_per_game : float
        The number of innings played per game.
    pitches_per_game : float
        The number of pitches thrown per game played.
    pitchers_per_game : float
        The number of pitchers used per game played.
    plate_appearances_per_game : float
        The number of plate appearances per game played.
    total_game_time : str
        The total time spent playing games.
    total_innings_played : float
        The total number of innings played.
    total_hits : int
        The total number of hits.
    total_runs : int
        The total number of runs scored.
    total_plate_appearances : int
        The total number of plate appearances.
    total_pitchers : int
        The total number of pitchers used.
    total_pitches : int
        The total number of pitches thrown.
    total_games : int
        The total number of games played.
    total_7_inn_games : int
        The total number of 7-inning games played.
    total_9_inn_games : int
        The total number of 9-inning games played.
    total_extra_inn_games : int
        The total number of extra inning games played.
    time_per_game : str
        The amount of time spent per game.
    time_per_pitch : str
        The amount of time spent per pitch.
    time_per_hit : str
        The amount of time spent per hit.
    time_per_run : str
        The amount of time spent per run scored.
    time_per_plate_appearance : str
        The amount of time spent per plate appearance.
    time_per_9_inn : str
        The amount of time spent per 9 innings played.
    time_per_77_plate_appearances : str
        The amount of time spent per 77 plate appearances.
    total_extra_inn_time : str
        The total amount of time spent on extra inning games.
    time_per_7_inn_game : str
        The amount of time spent per 7-inning game.
    total_7_inn_games_completed_early : int
        The total number of 7-inning games completed early.
    time_per_7_inn_game_without_extra_inn : str
        The amount of time spent per 7-inning game without extra innings.
    total_7_inn_games_scheduled : int
        The total number of 7-inning games scheduled.
    total_7_inn_games_without_extra_inn : int
        The total number of 7-inning games played without extra innings.
    total_9_inn_games_completed_early : int
        The total number of 9-inning games completed early.
    total_9_inn_games_without_extra_inn : int
        The total number of 9-inning games without extra innings.
    total_9_inn_games_scheduled : int
        The total number of 9 inning games scheduled.
    hits_per_run : float
        The number of hits per run.
    pitches_per_pitcher : float
        Number of pitches thrown per pitcher.
    season : str
        Season number.
    team : Team
        Team.
    league : League
        League.
    sport : Sport
        Sport.
    pr_portal_calculated_fields : PrPortalCalculatedFields
        Calculated fields.
    """
    hits_per_9_inn: Optional[float] = Field(default=None, alias="hitsper9inn")
    runs_per_9_inn: Optional[float] = Field(default=None, alias="runsper9inn")
    pitches_per_9_inn: Optional[float] = Field(default=None, alias="pitchesper9inn")
    plate_appearances_per_9_inn: Optional[float] = Field(default=None, alias="plateappearancesper9inn")
    hits_per_game: Optional[float] = Field(default=None, alias="hitspergame")
    runs_per_game: Optional[float] = Field(default=None, alias="runspergame")
    innings_played_per_game: Optional[float] = Field(default=None, alias="inningsplayedpergame")
    pitches_per_game: Optional[float] = Field(default=None, alias="pitchespergame")
    pitchers_per_game: Optional[float] = Field(default=None, alias="pitcherspergame")
    plate_appearances_per_game: Optional[float] = Field(default=None, alias="plateappearancespergame")
    total_game_time: Optional[str] = Field(default=None, alias="totalgametime")
    total_innings_played: Optional[float] = Field(default=None, alias="totalinningsplayed")
    total_hits: Optional[int] = Field(default=None, alias="totalhits")
    total_runs: Optional[int] = Field(default=None, alias="totalruns")
    total_plate_appearances: Optional[int] = Field(default=None, alias="totalplateappearances")
    total_pitchers: Optional[int] = Field(default=None, alias="totalpitchers")
    total_pitches: Optional[int] = Field(default=None, alias="totalpitches")
    total_games: Optional[int] = Field(default=None, alias="totalgames")
    total_7_inn_games: Optional[int] = Field(default=None, alias="total7inngames")
    total_9_inn_games: Optional[int] = Field(default=None, alias="total9inngames")
    total_extra_inn_games: Optional[int] = Field(default=None, alias="totalextrainngames")
    time_per_game: Optional[str] = Field(default=None, alias="timepergame")
    time_per_pitch: Optional[str] = Field(default=None, alias="timeperpitch")
    time_per_hit: Optional[str] = Field(default=None, alias="timeperhit")
    time_per_run: Optional[str] = Field(default=None, alias="timeperrun")
    time_per_plate_appearance: Optional[str] = Field(default=None, alias="timeperplateappearance")
    time_per_9_inn: Optional[str] = Field(default=None, alias="timeper9inn")
    time_per_77_plate_appearances: Optional[str] = Field(default=None, alias="timeper77plateappearances")
    total_extra_inn_time: Optional[str] = Field(default=None, alias="totalextrainntime")
    time_per_7_inn_game: Optional[str] = Field(default=None, alias="timeper7inngame")
    total_7_inn_games_completed_early: Optional[int] = Field(default=None, alias="total7inngamescompletedearly")
    time_per_7_inn_game_without_extra_inn: Optional[str] = Field(default=None, alias="timeper7inngamewithoutextrainn")
    total_7_inn_games_scheduled: Optional[int] = Field(default=None, alias="total7inngamesscheduled")
    total_7_inn_games_without_extra_inn: Optional[int] = Field(default=None, alias="total7inngameswithoutextrainn")
    total_9_inn_games_completed_early: Optional[int] = Field(default=None, alias="total9inngamescompletedearly")
    total_9_inn_games_without_extra_inn: Optional[int] = Field(default=None, alias="total9inngameswithoutextrainn")
    total_9_inn_games_scheduled: Optional[int] = Field(default=None, alias="total9inngamesscheduled")
    hits_per_run: Optional[float] = Field(default=None, alias="hitsperrun")
    pitches_per_pitcher: Optional[float] = Field(default=None, alias="pitchesperpitcher")
    season: Optional[str] = None
    team: Optional[Team] = None
    league: Optional[League] = None
    sport: Optional[Sport] = None
    pr_portal_calculated_fields: Optional[PrPortalCalculatedFields] = Field(default=None, alias="prportalcalculatedfields")
