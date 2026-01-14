from typing import Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel


class Season(MLBBaseModel):
    """
    A class to represent a season.

    Attributes
    ----------
    season_id : str
        Season ID.
    has_wildcard : bool
        Wild card status.
    preseason_start_date : str
        Pre-season start date.
    preseason_end_date : str
        Pre-season end date.
    season_start_date : str
        Season start date.
    spring_start_date : str
        Spring start date.
    spring_end_date : str
        Spring end date.
    regular_season_start_date : str
        Regular season start date.
    last_date_1st_half : str
        Last date of 1st half.
    all_star_date : str
        All-star date.
    first_date_2nd_half : str
        First date of 2nd half.
    regular_season_end_date : str
        Regular season end date.
    postseason_start_date : str
        Post season start date.
    postseason_end_date : str
        Post season end date.
    season_end_date : str
        Season end date.
    offseason_start_date : str
        Off season start date.
    offseason_end_date : str
        Off season end date.
    season_level_gameday_type : str
        Season level game day type.
    game_level_gameday_type : str
        Game level game day type.
    qualifier_plate_appearances : float
        Qualifier plate appearances.
    qualifier_outs_pitched : float
        Qualifier outs pitched.
    """
    season_id: str = Field(alias="seasonId")
    has_wildcard: Optional[bool] = Field(default=None, alias="hasWildcard")
    preseason_start_date: Optional[str] = Field(default=None, alias="preseasonStartDate")
    preseason_end_date: Optional[str] = Field(default=None, alias="preseasonEndDate")
    season_start_date: Optional[str] = Field(default=None, alias="seasonStartDate")
    spring_start_date: Optional[str] = Field(default=None, alias="springStartDate")
    spring_end_date: Optional[str] = Field(default=None, alias="springEndDate")
    regular_season_start_date: Optional[str] = Field(default=None, alias="regularSeasonStartDate")
    last_date_1st_half: Optional[str] = Field(default=None, alias="lastDate1stHalf")
    all_star_date: Optional[str] = Field(default=None, alias="allStarDate")
    first_date_2nd_half: Optional[str] = Field(default=None, alias="firstDate2ndHalf")
    regular_season_end_date: Optional[str] = Field(default=None, alias="regularSeasonEndDate")
    postseason_start_date: Optional[str] = Field(default=None, alias="postseasonStartDate")
    postseason_end_date: Optional[str] = Field(default=None, alias="postseasonEndDate")
    season_end_date: Optional[str] = Field(default=None, alias="seasonEndDate")
    offseason_start_date: Optional[str] = Field(default=None, alias="offseasonStartDate")
    offseason_end_date: Optional[str] = Field(default=None, alias="offseasonEndDate")
    season_level_gameday_type: Optional[str] = Field(default=None, alias="seasonLevelGamedayType")
    game_level_gameday_type: Optional[str] = Field(default=None, alias="gameLevelGamedayType")
    qualifier_plate_appearances: Optional[float] = Field(default=None, alias="qualifierPlateAppearances")
    qualifier_outs_pitched: Optional[float] = Field(default=None, alias="qualifierOutsPitched")
