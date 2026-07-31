from typing import Optional, Any
from pydantic import Field, field_validator
from mlbstatsapi.models.base import MLBBaseModel


class PitchBreak(MLBBaseModel):
    """
    A class to hold pitch break data.

    Attributes
    ----------
    break_angle : float
        Degrees clockwise (batter's view) that the plane of
        the pitch deviates from the vertical.
    break_vertical : float
        Vertical break of the pitch.
    break_vertical_induced : float
        Induced vertical break.
    break_horizontal : float
        Horizontal break of the pitch.
    break_length : float
        Max distance that the pitch separates from the straight
        line between pitch start and pitch end.
    break_y : int
        Distance from home plate where the break is greatest.
    spin_rate : float
        Pitch spin rate.
    spin_direction : float
        Pitch spin direction.
    """
    break_angle: Optional[float] = Field(default=None, alias="breakAngle")
    break_vertical: Optional[float] = Field(default=None, alias="breakVertical")
    break_vertical_induced: Optional[float] = Field(default=None, alias="breakVerticalInduced")
    break_horizontal: Optional[float] = Field(default=None, alias="breakHorizontal")
    spin_rate: Optional[float] = Field(default=None, alias="spinRate")
    spin_direction: Optional[float] = Field(default=None, alias="spinDirection")
    break_length: Optional[float] = Field(default=None, alias="breakLength")
    break_y: Optional[float] = Field(default=None, alias="breakY")


class PitchCoordinates(MLBBaseModel):
    """
    A class to hold pitch coordinates for playLog.

    Attributes
    ----------
    ay : float
        Ball acceleration on the y axis.
    az : float
        Ball acceleration on the z axis.
    pfx_x : float
        Horizontal movement of the ball in inches.
    pfx_z : float
        Vertical movement of the ball in inches.
    p_x : float
        Horizontal position in feet of the ball as it
        crosses the front axis of home plate.
    p_z : float
        Vertical position in feet of the ball as it
        crosses the front axis of home plate.
    v_x0 : float
        Velocity of the ball from the x-axis.
    v_y0 : float
        Velocity of the ball from the y axis.
    v_z0 : float
        Velocity of the ball from the z axis.
    x0 : float
        Coordinate location of the ball at release on x axis.
    y0 : float
        Coordinate location of the ball at release on y axis.
    z0 : float
        Coordinate location of the ball at release on z axis.
    ax : float
        Ball acceleration on the x axis.
    x : float
        X coordinate where pitch crossed front of home plate.
    y : float
        Y coordinate where pitch crossed front of home plate.
    """
    ay: Optional[float] = Field(default=None, alias="aY")
    az: Optional[float] = Field(default=None, alias="aZ")
    pfx_x: Optional[float] = Field(default=None, alias="pfxX")
    pfx_z: Optional[float] = Field(default=None, alias="pfxZ")
    p_x: Optional[float] = Field(default=None, alias="pX")
    p_z: Optional[float] = Field(default=None, alias="pZ")
    v_x0: Optional[float] = Field(default=None, alias="vX0")
    v_y0: Optional[float] = Field(default=None, alias="vY0")
    v_z0: Optional[float] = Field(default=None, alias="vZ0")
    x0: Optional[float] = None
    y0: Optional[float] = None
    z0: Optional[float] = None
    ax: Optional[float] = Field(default=None, alias="aX")
    x: Optional[float] = None
    y: Optional[float] = None


class PitchData(MLBBaseModel):
    """
    A class to hold data on a pitch.

    Attributes
    ----------
    start_speed : float
        The starting speed of the pitch.
    end_speed : float
        The ending speed of the pitch.
    strike_zone_top : float
        The top of the strike zone.
    strike_zone_bottom : float
        The bottom of the strike zone.
    coordinates : PitchCoordinates
        The coordinates of the pitch.
    breaks : PitchBreak
        The break data of the pitch.
    zone : float
        The zone in which the pitch was thrown.
    type_confidence : float
        The confidence in the type of pitch thrown.
    plate_time : float
        The amount of time the pitch was in the air.
    extension : float
        The extension of the pitch.
    strike_zone_width : float
        The width of the strike zone.
    strike_zone_depth : float
        The depth of the strike zone.
    """
    strike_zone_top: float = Field(alias="strikeZoneTop")
    strike_zone_bottom: float = Field(alias="strikeZoneBottom")
    breaks: PitchBreak
    coordinates: Optional[PitchCoordinates] = None
    extension: Optional[float] = None
    start_speed: Optional[float] = Field(default=None, alias="startSpeed")
    end_speed: Optional[float] = Field(default=None, alias="endSpeed")
    zone: Optional[float] = None
    type_confidence: Optional[float] = Field(default=None, alias="typeConfidence")
    plate_time: Optional[float] = Field(default=None, alias="plateTime")
    strike_zone_width: Optional[float] = Field(default=None, alias="strikeZoneWidth")
    strike_zone_depth: Optional[float] = Field(default=None, alias="strikeZoneDepth")


class HitCoordinates(MLBBaseModel):
    """
    A class to represent a play event's hit location coordinates.

    Attributes
    ----------
    coord_x : float
        X coordinate for hit.
    coord_y : float
        Y coordinate for hit.
    """
    coord_x: Optional[float] = Field(default=None, alias="coordX")
    coord_y: Optional[float] = Field(default=None, alias="coordY")

    @property
    def x(self):
        return self.coord_x

    @property
    def y(self):
        return self.coord_y


class HitData(MLBBaseModel):
    """
    A class to represent a play event's hit data.

    Attributes
    ----------
    launch_speed : float
        Hit launch speed.
    launch_angle : float
        Hit launch angle.
    total_distance : float
        Hit's total distance.
    trajectory : str
        Hit trajectory.
    hardness : str
        Hit hardness.
    location : int
        Hit location.
    coordinates : HitCoordinates
        Hit coordinates.
    """
    coordinates: HitCoordinates
    trajectory: Optional[str] = None
    hardness: Optional[str] = None
    location: Optional[int] = None
    launch_speed: Optional[float] = Field(default=None, alias="launchSpeed")
    launch_angle: Optional[float] = Field(default=None, alias="launchAngle")
    total_distance: Optional[float] = Field(default=None, alias="totalDistance")


class CodeDesc(MLBBaseModel):
    """
    A class to hold a code and a description.

    Attributes
    ----------
    code : str
        The code to reference the attribute.
    description : str
        The description of the attribute.
    """
    code: str
    description: Optional[str] = None


class Violation(MLBBaseModel):
    """
    A class to represent a violation during play.

    Attributes
    ----------
    type : str
        The type of violation during the play.
    description : str
        The description of the violation that occurred.
    player : dict
        The player that caused the violation.
    """
    type: Optional[str] = None
    description: Optional[str] = None
    player: Optional[dict] = None


class Count(MLBBaseModel):
    """
    A class to hold a pitch count and base runners.

    Attributes
    ----------
    balls : int
        Number of balls.
    outs : int
        Number of outs.
    strikes : int
        Strike count.
    inning : int
        Inning number.
    is_top_inning : bool
        Status of top inning.
    runner_on_1b : bool
        1B runner status.
    runner_on_2b : bool
        2B runner status.
    runner_on_3b : bool
        3B runner status.
    """
    balls: int
    outs: int
    strikes: int
    inning: Optional[int] = None
    runner_on_1b: Optional[bool] = Field(default=None, alias="runnerOn1b")
    runner_on_2b: Optional[bool] = Field(default=None, alias="runnerOn2b")
    runner_on_3b: Optional[bool] = Field(default=None, alias="runnerOn3b")
    is_top_inning: Optional[bool] = Field(default=None, alias="isTopInning")


class PlayDetails(MLBBaseModel):
    """
    A class to represent play details.

    Attributes
    ----------
    call : CodeDesc
        Play call code and description.
    description : str
        Description of the play.
    event : str
        Type of event.
    event_type : str
        Type of event.
    is_in_play : bool
        Is the ball in play.
    is_strike : bool
        Is the ball a strike.
    is_ball : bool
        Is it a ball.
    is_base_hit : bool
        Is the event a base hit.
    is_at_bat : bool
        Is the event at bat.
    is_plate_appearance : bool
        Is the event a plate appearance.
    type : CodeDesc
        Type of pitch code and description.
    bat_side : CodeDesc
        Bat side code and description.
    pitch_hand : CodeDesc
        Pitch hand code and description.
    from_catcher : bool
        From catcher flag.
    """
    call: Optional[CodeDesc] = None
    is_in_play: Optional[bool] = Field(default=None, alias="isInPlay")
    is_strike: Optional[bool] = Field(default=None, alias="isStrike")
    is_scoring_play: Optional[bool] = Field(default=None, alias="isScoringPlay")
    is_out: Optional[bool] = Field(default=None, alias="isOut")
    runner_going: Optional[bool] = Field(default=None, alias="runnerGoing")
    is_ball: Optional[bool] = Field(default=None, alias="isBall")
    is_base_hit: Optional[bool] = Field(default=None, alias="isBaseHit")
    is_at_bat: Optional[bool] = Field(default=None, alias="isAtBat")
    is_plate_appearance: Optional[bool] = Field(default=None, alias="isPlateAppearance")
    bat_side: Optional[CodeDesc] = Field(default=None, alias="batSide")
    pitch_hand: Optional[CodeDesc] = Field(default=None, alias="pitchHand")
    event_type: Optional[str] = Field(default=None, alias="eventType")
    event: Optional[str] = None
    description: Optional[str] = None
    type: Optional[CodeDesc] = None
    away_score: Optional[int] = Field(default=None, alias="awayScore")
    home_score: Optional[int] = Field(default=None, alias="homeScore")
    has_review: Optional[bool] = Field(default=None, alias="hasReview")
    code: Optional[str] = None
    ball_color: Optional[str] = Field(default=None, alias="ballColor")
    trail_color: Optional[str] = Field(default=None, alias="trailColor")
    from_catcher: Optional[bool] = Field(default=None, alias="fromCatcher")
    disengagement_num: Optional[int] = Field(default=None, alias="disengagementNum")
    violation: Optional[Violation] = None

    @field_validator('bat_side', 'pitch_hand', 'type', 'call', 'violation', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v
