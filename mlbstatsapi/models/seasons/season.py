from typing import Optional
from pydantic import BaseModel


class Season(BaseModel):
    """
    Represents a season object, detailing various dates and statuses throughout the season, including pre-season, regular season, and post-season periods.

    Attributes:
        seasonId (str): The season identifier.
        hasWildCard (Optional[bool]): Status indicating the presence of a wild card.
        preSeasonStartDate (Optional[str]): The start date of the pre-season.
        preSeasonEndDate (Optional[str]): The end date of the pre-season.
        seasonStartDate (Optional[str]): The start date of the season.
        springStartDate (Optional[str]): The start date of the spring training.
        springEndDate (Optional[str]): The end date of the spring training.
        regularSeasonStartDate (Optional[str]): The start date of the regular season.
        lastDate1stHalf (Optional[str]): The last date of the first half of the season.
        allStarDate (Optional[str]): The date of the All-Star game.
        firstDate2ndHalf (Optional[str]): The first date of the second half of the season.
        regularSeasonEndDate (Optional[str]): The end date of the regular season.
        postSeasonStartDate (Optional[str]): The start date of the post-season.
        postSeasonEndDate (Optional[str]): The end date of the post-season.
        seasonEndDate (Optional[str]): The end date of the entire season.
        offseasonStartDate (Optional[str]): The start date of the off-season.
        offSeasonEndDate (Optional[str]): The end date of the off-season.
        seasonLevelGamedayType (Optional[str]): The season-level game day type.
        gameLevelGamedayType (Optional[str]): The game-level game day type.
        qualifierPlateAppearances (Optional[float]): The qualifier for plate appearances.
        qualifierOutsPitched (Optional[int]): The qualifier for outs pitched.
    """

    seasonId: str
    haswildcard: Optional[bool] = None
    preSeasonStartDate: Optional[str] = None
    preSeasonEndDate: Optional[str] = None
    seasonStartDate: Optional[str] = None
    springStartDate: Optional[str] = None
    springEndDate: Optional[str] = None
    regularSeasonStartDate: Optional[str] = None
    lastDate1stHalf: Optional[str] = None
    allStarDate: Optional[str] = None
    firstDate2ndHalf: Optional[str] = None
    regularSeasonEndDate: Optional[str] = None
    postSeasonStartDate: Optional[str] = None
    postSeasonEndDate: Optional[str] = None
    seasonEndDate: Optional[str] = None
    offseasonStartDate: Optional[str] = None
    offSeasonEndDate: Optional[str] = None
    seasonLevelGamedayType: Optional[str] = None
    gameLevelGamedayType: Optional[str] = None
    qualifierPlateAppearances: Optional[float] = None
    qualifierOutsPitched: Optional[float] = None