from typing import Optional, List, Any
from pydantic import Field, field_validator
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person


class EventType(MLBBaseModel):
    """
    A class representing the type of an event.

    Attributes
    ----------
    code : str
        The unique code of the event type.
    name : str
        The name of the event type.
    """
    code: str
    name: str


class Info(MLBBaseModel):
    """
    A class representing information about an event.

    Attributes
    ----------
    id : int
        The unique identifier of the event.
    non_game_guid : str
        GUID of the event.
    name : str
        The name of the event.
    event_type : EventType
        The type of event.
    event_date : str
        The date of the event.
    venue : Venue
        The venue of the event.
    is_multi_day : bool
        Whether the event spans multiple days.
    is_primary_calendar : bool
        Whether the event is on the primary calendar.
    file_code : str
        The code of the file associated with the event.
    event_number : int
        The number of the event.
    public_facing : bool
        Whether the event is public-facing.
    teams : List[Team]
        The teams participating in the event.
    """
    id: int
    non_game_guid: str = Field(alias="nongameguid")
    name: str
    event_type: EventType = Field(alias="eventtype")
    event_date: str = Field(alias="eventdate")
    venue: Venue
    is_multi_day: bool = Field(alias="ismultiday")
    is_primary_calendar: bool = Field(alias="isprimarycalendar")
    file_code: str = Field(alias="filecode")
    event_number: int = Field(alias="eventnumber")
    public_facing: bool = Field(alias="publicfacing")
    teams: List[Team] = []


class Status(MLBBaseModel):
    """
    A class representing the status of a round.

    Attributes
    ----------
    state : str
        The current state of the game or round.
    current_round : int
        The number of the current round in the game.
    current_round_time_left : str
        The amount of time left in the current round.
    in_tiebreaker : bool
        Whether the game or round is currently in a tiebreaker.
    tiebreaker_num : int
        The number of the current tiebreaker, if applicable.
    clock_stopped : bool
        Whether the round clock is currently stopped.
    bonus_time : bool
        Whether the round is currently in bonus time.
    """
    state: str
    current_round: int = Field(alias="currentround")
    current_round_time_left: str = Field(alias="currentroundtimeleft")
    in_tiebreaker: bool = Field(alias="intiebreaker")
    tiebreaker_num: int = Field(alias="tiebreakernum")
    clock_stopped: bool = Field(alias="clockstopped")
    bonus_time: bool = Field(alias="bonustime")


class Coordinates(MLBBaseModel):
    """
    A class representing the coordinates of a hit.

    Attributes
    ----------
    coord_x : float
        The x-coordinate of the hit.
    coord_y : float
        The y-coordinate of the hit.
    landing_pos_x : float
        The x-coordinate of the hit's landing position.
    landing_pos_y : float
        The y-coordinate of the hit's landing position.
    """
    coord_x: Optional[float] = Field(default=None, alias="coordx")
    coord_y: Optional[float] = Field(default=None, alias="coordy")
    landing_pos_x: Optional[float] = Field(default=None, alias="landingposx")
    landing_pos_y: Optional[float] = Field(default=None, alias="landingposy")


class TrajectoryData(MLBBaseModel):
    """
    A class representing data on a hit's trajectory in three-dimensional space.

    Attributes
    ----------
    trajectory_polynomial_x : List[float]
        Coefficients for the polynomial representing the x-coordinate trajectory.
    trajectory_polynomial_y : List[float]
        Coefficients for the polynomial representing the y-coordinate trajectory.
    trajectory_polynomial_z : List[float]
        Coefficients for the polynomial representing the z-coordinate trajectory.
    valid_time_interval : List[float]
        Start and end times for which the polynomial coefficients are valid.
    measured_time_interval : List[float]
        Start and end times of the interval during which trajectory was measured.
    """
    trajectory_polynomial_x: List[float] = Field(alias="trajectorypolynomialx")
    trajectory_polynomial_y: List[float] = Field(alias="trajectorypolynomialy")
    trajectory_polynomial_z: List[float] = Field(alias="trajectorypolynomialz")
    valid_time_interval: List[float] = Field(alias="validtimeinterval")
    measured_time_interval: List[float] = Field(alias="measuredtimeinterval")


class HitData(MLBBaseModel):
    """
    A class representing data on a hit.

    Attributes
    ----------
    total_distance : int
        The total distance the hit traveled.
    launch_speed : float
        The speed at which the hit was launched.
    launch_angle : float
        The angle at which the hit was launched.
    coordinates : Coordinates
        Coordinates for the hit.
    trajectory_data : TrajectoryData
        Trajectory data for the hit.
    """
    total_distance: int = Field(alias="totaldistance")
    launch_speed: Optional[float] = Field(default=None, alias="launchspeed")
    launch_angle: Optional[float] = Field(default=None, alias="launchangle")
    coordinates: Optional[Coordinates] = None
    trajectory_data: Optional[TrajectoryData] = Field(default=None, alias="trajectorydata")


class Hits(MLBBaseModel):
    """
    A class representing a hit in the homerun derby.

    Attributes
    ----------
    bonus_time : bool
        Whether the hit occurred during bonus time.
    homerun : bool
        Whether the hit was a homerun.
    tiebreaker : bool
        Whether the hit occurred during a tiebreaker.
    hit_data : HitData
        The data for the hit.
    is_homerun : bool
        Whether the hit was a homerun.
    time_remaining : str
        Amount of time remaining when the hit occurred.
    is_bonus_time : bool
        Whether the hit occurred during bonus time.
    time_remaining_seconds : int
        Amount of time remaining in seconds.
    is_tiebreaker : bool
        Whether the hit occurred during a tiebreaker.
    play_id : str
        The ID of the play in which the hit occurred.
    """
    bonus_time: bool = Field(alias="bonustime")
    homerun: bool
    tiebreaker: bool
    hit_data: HitData = Field(alias="hitdata")
    is_homerun: bool = Field(alias="ishomerun")
    time_remaining: str = Field(alias="timeremaining")
    is_bonus_time: bool = Field(alias="isbonustime")
    is_tiebreaker: bool = Field(alias="istiebreaker")
    time_remaining_seconds: Optional[int] = Field(default=None, alias="timeremainingseconds")
    play_id: Optional[str] = Field(default=None, alias="playid")


class Seed(MLBBaseModel):
    """
    A class representing a seed in a homerun derby matchup.

    Attributes
    ----------
    complete : bool
        Whether the seed has been completed.
    started : bool
        Whether the seed has been started.
    winner : bool
        Whether the player for this seed is the winner.
    player : Person
        The player associated with this seed.
    top_derby_hit_data : HitData
        The data for the top hit in the seed.
    hits : List[Hits]
        The hits in the seed.
    seed : int
        The seed number.
    order : int
        The order in which the seed was played.
    is_winner : bool
        Whether the player for this seed is the winner.
    is_complete : bool
        Whether the seed has been completed.
    is_started : bool
        Whether the seed has been started.
    num_homeruns : int
        The number of homeruns hit in the seed.
    """
    complete: bool
    started: bool
    winner: bool
    player: Person
    top_derby_hit_data: HitData = Field(alias="topderbyhitdata")
    hits: List[Hits] = []
    seed: int
    order: int
    is_winner: bool = Field(alias="iswinner")
    is_complete: bool = Field(alias="iscomplete")
    is_started: bool = Field(alias="isstarted")
    num_homeruns: int = Field(alias="numhomeruns")


class Matchup(MLBBaseModel):
    """
    A class representing a matchup in the homerun derby.

    Attributes
    ----------
    top_seed : Seed
        The top seed in the matchup.
    bottom_seed : Seed
        The bottom seed in the matchup.
    """
    top_seed: Seed = Field(alias="topseed")
    bottom_seed: Seed = Field(alias="bottomseed")


class Round(MLBBaseModel):
    """
    A class representing a round in the homerun derby.

    Attributes
    ----------
    round : int
        The round number.
    num_batters : int
        The number of batters in the round.
    matchups : List[Matchup]
        The matchups in the round.
    """
    round: int
    matchups: List[Matchup] = []
    num_batters: Optional[int] = Field(default=None, alias="numbatters")
