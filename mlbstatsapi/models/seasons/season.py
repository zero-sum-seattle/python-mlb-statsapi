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
    season_id: str = Field(alias="seasonid")
    has_wildcard: Optional[bool] = Field(default=None, alias="haswildcard")
    preseason_start_date: Optional[str] = Field(default=None, alias="preseasonstartdate")
    preseason_end_date: Optional[str] = Field(default=None, alias="preseasonenddate")
    season_start_date: Optional[str] = Field(default=None, alias="seasonstartdate")
    spring_start_date: Optional[str] = Field(default=None, alias="springstartdate")
    spring_end_date: Optional[str] = Field(default=None, alias="springenddate")
    regular_season_start_date: Optional[str] = Field(default=None, alias="regularseasonstartdate")
    last_date_1st_half: Optional[str] = Field(default=None, alias="lastdate1sthalf")
    all_star_date: Optional[str] = Field(default=None, alias="allstardate")
    first_date_2nd_half: Optional[str] = Field(default=None, alias="firstdate2ndhalf")
    regular_season_end_date: Optional[str] = Field(default=None, alias="regularseasonenddate")
    postseason_start_date: Optional[str] = Field(default=None, alias="postseasonstartdate")
    postseason_end_date: Optional[str] = Field(default=None, alias="postseasonenddate")
    season_end_date: Optional[str] = Field(default=None, alias="seasonenddate")
    offseason_start_date: Optional[str] = Field(default=None, alias="offseasonstartdate")
    offseason_end_date: Optional[str] = Field(default=None, alias="offseasonenddate")
    season_level_gameday_type: Optional[str] = Field(default=None, alias="seasonlevelgamedaytype")
    game_level_gameday_type: Optional[str] = Field(default=None, alias="gamelevelgamedaytype")
    qualifier_plate_appearances: Optional[float] = Field(default=None, alias="qualifierplateappearances")
    qualifier_outs_pitched: Optional[float] = Field(default=None, alias="qualifieroutspitched")
