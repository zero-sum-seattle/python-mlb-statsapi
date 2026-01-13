from typing import Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel


class Sport(MLBBaseModel):
    """
    A class to represent a sport.

    Attributes
    ----------
    id : int
        ID number of the sport.
    link : str
        API link for the sport.
    name : str
        Name of the sport.
    code : str
        Sport code.
    abbreviation : str
        Abbreviation for the sport.
    sort_order : int
        Sorting order.
    active_status : bool
        Whether the sport is active.
    """
    id: int
    link: str
    name: Optional[str] = None
    code: Optional[str] = None
    abbreviation: Optional[str] = None
    sort_order: Optional[int] = Field(default=None, alias="sortorder")
    active_status: Optional[bool] = Field(default=None, alias="activestatus")
