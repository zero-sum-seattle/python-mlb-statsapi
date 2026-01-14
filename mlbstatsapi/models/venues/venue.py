from typing import Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from .attributes import Location, TimeZone, FieldInfo


class Venue(MLBBaseModel):
    """
    A class to represent a venue.

    Attributes
    ----------
    id : int
        ID for this venue.
    link : str
        Link to venue's endpoint.
    name : str
        Name for this venue.
    location : Location
        Location for this venue.
    timezone : TimeZone
        Timezone for this venue.
    field_info : FieldInfo
        Info on this venue's field.
    active : bool
        Whether this field is currently active.
    season : str
        The season.
    """
    id: int
    link: str
    name: Optional[str] = None
    location: Optional[Location] = None
    timezone: Optional[TimeZone] = None
    field_info: Optional[FieldInfo] = Field(default=None, alias="fieldInfo")
    active: Optional[bool] = None
    season: Optional[str] = None
